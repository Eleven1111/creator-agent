"""MCP 服务器：让 Claude 桌面端、ChatGPT、OpenClaw、Hermes、WorkBuddy 等 agent 终端直接调用 creator-agent。

两种传输：
- stdio（默认）：终端把 `creator-agent-mcp` 当子进程启动。Claude 桌面端、OpenClaw、Hermes、WorkBuddy 都支持。
- Streamable HTTP：`creator-agent-mcp --http`，默认只监听 127.0.0.1:8765/mcp。需要远程访问时（例如 ChatGPT
  只能连 HTTPS 远程服务器），设置 CA_MCP_TOKEN，并通过隧道暴露；服务器会校验 `Authorization: Bearer <token>`。

规则和命令行完全一样：
- 每个阶段仍然要先过前面的人工闸口；闸口规则与 `ca approve` 相同。
- approve_gate 只能在用户本人明确同意后调用，并且要把用户的原话写进 user_statement；记录里会标明来自 MCP。
  知识库 agent.yaml 里设 `mcp.allow_gate_approval: false`，就只能在命令行批准。
- 没有任何发布工具。mark_published 只是在你本人发完之后记下链接。
- 需要模型的阶段（angles / research / outline / draft B / review / adapt / interview / retro）调用 Anthropic API，
  需要在服务器的环境变量里配置 ANTHROPIC_API_KEY；其余工具不需要。
"""

from __future__ import annotations

import argparse
import functools
import hmac
import json
import os
import sys
from pathlib import Path
from typing import Any, Literal

from . import gates, stages
from .llm import LLM, LLMError
from .vault import Vault, VaultError

INSTRUCTIONS = """creator-agent 是写作者的研究助理和编辑，不是代笔，也从不替作者发布。
工作流：new_hub → run_angles → [H1] → run_research → [H2] → run_outline → [H3] → run_draft（默认模式 A：作者自己写，
你可以帮作者整理，但要用 write_draft 并如实标注 written_by）→ run_review → [H4] → run_adapt → [H5] → 作者本人去各平台发布
→ mark_published → add_metrics / pull_x_metrics → run_retro。
硬规则：
1. 方括号里的闸口必须由作者本人决定。先用 read_hub_file 把要审的文件给作者看，等作者明确同意后才调用 approve_gate，
   并把作者的原话放进 user_statement。H1 的兴奋度（excitement）和 edge 只能由作者说出，不能替作者编。
2. 不编造事实、数字、引语或作者的经历。缺的地方写 [TK: ...]。
3. 不发布、不互动。发布包在 publish_kit.md 里，由作者本人复制到各平台。
4. 工具返回的错误信息是中文的操作提示，照着提示做，不要绕过。
5. 宿主模型模式（服务器没配 ANTHROPIC_API_KEY 时）：run_* 工具会返回“【待你完成的模型任务】”。请按其中的系统指令和输入
   完成任务（只依据给定材料；需要联网时用你的搜索工具，没有就如实说明，绝不编造来源），然后调用 submit_model_output 交回；
   服务器会自动继续，可能再返回下一个任务，直到拿到最终结果。这些任务是流程内部步骤，不需要逐个向作者汇报，
   但最终结果（angles.md、research.md、review.md 等）要给作者看。"""

ALLOWED_FILES = {
    "angles.md", "research.md", "research_notes.md", "outline.md", "cards.md", "draft.md", "draft_agent.md",
    "review.md", "final.md", "final_en.md", "review_queue.md", "substack_package.md", "publish_kit.md",
    "cribs.md", "meta.json",
}


def _vault() -> Vault:
    v = Vault(Path(os.environ.get("CA_VAULT", "creator-vault")).expanduser())
    v.require()
    return v


def llm_backend(v: Vault) -> str:
    """auto（默认）：有 ANTHROPIC_API_KEY 用 API，没有就用宿主模型；也可在 agent.yaml 的 llm.backend 或环境变量
    CA_LLM_BACKEND 里固定为 anthropic / host。"""
    choice = os.environ.get("CA_LLM_BACKEND") or (v._yaml("agent.yaml").get("llm") or {}).get("backend", "auto")
    if choice == "auto":
        return "anthropic" if os.environ.get("ANTHROPIC_API_KEY", "").strip() else "host"
    if choice not in ("anthropic", "host"):
        raise VaultError(f"llm.backend 只能是 auto / anthropic / host，现在是 {choice}")
    return choice


def _llm(v: Vault):
    if llm_backend(v) == "host":
        from .host_llm import HostLLM

        return HostLLM(v.root, v.llm_config())
    return LLM(v.llm_config(), log_dir=v.root / "runs/logs")


def _mcp_settings(v: Vault) -> dict:
    return v._yaml("agent.yaml").get("mcp") or {}


def build_server(vault_factory=_vault, llm_factory=_llm):
    from mcp.server.mcpserver import MCPServer
    from mcp.server.mcpserver.exceptions import ToolError
    from mcp.types import ToolAnnotations

    server = MCPServer("creator-agent", instructions=INSTRUCTIONS, version="0.3.0")
    READ = ToolAnnotations(read_only_hint=True, destructive_hint=False, open_world_hint=False)
    LOCAL = ToolAnnotations(read_only_hint=False, destructive_hint=False, open_world_hint=False)
    MODEL = ToolAnnotations(read_only_hint=False, destructive_hint=False, open_world_hint=True)

    from .host_llm import HostTaskPending, render_task

    wrapped_tools: dict[str, Any] = {}  # 工具名 → 带错误处理的函数，供 submit_model_output 续跑

    def tool(annotations):
        """注册工具，并把业务错误转成 ToolError，让中文提示原样回到模型。
        宿主模型模式下，阶段需要模型时返回一个待办任务，宿主模型完成后用 submit_model_output 交回。"""
        def deco(fn):
            @functools.wraps(fn)
            def wrapped(*a, **kw):
                try:
                    return fn(*a, **kw)
                except HostTaskPending as p:
                    task = dict(p.task, resume={"tool": fn.__name__, "args": kw})
                    path = vault_factory().root / "runs" / "host_tasks" / f"{task['task_id']}.json"
                    path.write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")
                    return render_task(task, fn.__name__)
                except (VaultError, LLMError, FileNotFoundError, ValueError) as e:
                    msg = str(e)
                    if "ca approve" in msg:
                        msg += "（在 agent 终端里：把待审文件给作者看，作者明确同意后调用 approve_gate）"
                    raise ToolError(msg) from e
            wrapped_tools[fn.__name__] = wrapped
            return server.tool(annotations=annotations)(wrapped)
        return deco

    # ------------------------------------------------------------- 读取
    @tool(READ)
    def vault_status(hub_id: str | None = None) -> dict[str, Any]:
        """查看知识库状态。不传 hub_id：列出所有母稿及其状态和已过闸口；传 hub_id：该母稿的详情、变体和下一步。"""
        v = vault_factory()
        stale = v.stale_platform_rules()
        if not hub_id:
            return {"vault": str(v.root), "model_backend": llm_backend(v), "stale_platform_rules": stale,
                    "hubs": [{"id": m["id"], "status": m["status"], "gates": sorted(m["gates"]),
                              "idea": m["idea"]} for m in v.hubs()]}
        m = v.meta(hub_id)
        return {"hub": {k: m.get(k) for k in ("id", "idea", "status", "draft_mode", "language",
                                               "canonical_url", "edge")},
                "gates": sorted(m["gates"]), "next_step": _next_step(m),
                "variants": [{"id": x["variant_id"], "format": x["format"], "status": x["status"],
                              "passed": x["gate_results"]["passed"], "failed": x["gate_results"]["failed"],
                              "planned_at": x["schedule"]["planned_at"]} for x in v.variants_of(hub_id)],
                "stale_platform_rules": stale}

    @tool(READ)
    def read_hub_file(hub_id: str, name: str) -> str:
        """读取母稿目录里的文件，用来给作者看待审内容。可读：angles.md、research.md、outline.md、cards.md、
        draft.md、review.md、final.md、final_en.md、review_queue.md、substack_package.md、publish_kit.md、cribs.md、meta.json。"""
        if name not in ALLOWED_FILES:
            raise VaultError(f"只能读取：{', '.join(sorted(ALLOWED_FILES))}")
        return vault_factory().read_hub_file(hub_id, name)

    @tool(READ)
    def read_variant(variant_id: str) -> dict[str, Any]:
        """读取一个平台变体的当前正文（作者可能改过）和检查结果。"""
        v = vault_factory()
        x = v.variant(variant_id)
        return {"variant_id": variant_id, "format": x["format"], "status": x["status"],
                "text": v.variant_text(variant_id) or x["editable_original"],
                "gate_results": x["gate_results"], "link": x["link_policy"].get("url"),
                "planned_at": x["schedule"]["planned_at"]}

    @tool(READ)
    def list_ideas() -> list[dict]:
        """列出选题池。"""
        return vault_factory().ideas()

    @tool(READ)
    def due(hours: int = 24) -> list[dict]:
        """列出接下来 N 小时内、已经批准、需要作者本人手动发布的稿子。"""
        import datetime as dt

        v = vault_factory()
        horizon = dt.datetime.now().astimezone() + dt.timedelta(hours=hours)
        rows = [x for x in v.all_variants() if x["status"] == "approved"
                and dt.datetime.fromisoformat(x["schedule"]["planned_at"]) <= horizon]
        return [{"variant_id": x["variant_id"], "format": x["format"], "planned_at": x["schedule"]["planned_at"],
                 "text": v.variant_text(x["variant_id"]) or x["editable_original"],
                 "publish_kit": f"hubs/{x['hub_id']}/publish_kit.md"}
                for x in sorted(rows, key=lambda x: x["schedule"]["planned_at"])]

    @tool(READ)
    def lint_text(text: str) -> dict[str, Any]:
        """不调用模型的确定性检查：TK、作者禁用词、AI 腔密度、对冲词、感叹号、总结式结尾、引言占比、句长。
        适合在作者改稿时随手检查。"""
        from .lint import lint_draft

        v = vault_factory()
        return lint_draft(text, never=v.list_items("voice/never.md"),
                          deliberate_breaks=v.list_items("voice/deliberate_breaks.md")).to_dict()

    @tool(READ)
    def check_x_post(text: str, hub_id: str | None = None) -> dict[str, Any]:
        """按 X 规则检查一条单帖：加权字数（汉字算 2）、链接、hashtag、@、cashtag、变现话题；
        给了 hub_id 时还检查数字是否都出现在定稿里。"""
        from .adapt import _x_text_checks

        v = vault_factory()
        final = v.read_hub_file(hub_id, "final.md") if hub_id else text
        return _x_text_checks(text, final, v.platform("x"))

    @tool(READ)
    def audit() -> dict[str, Any]:
        """合规审计：每次发布都经过 H5 批准且晚于批准时间、没有自动互动、平台规则 90 天内核对过。"""
        from .audit import audit as _audit

        return _audit(vault_factory())

    @tool(READ)
    def report(month: str | None = None) -> dict[str, Any]:
        """按 平台×体裁 汇总已发布变体的最新指标。month 形如 2026-11。"""
        from .metrics import channel_report

        return channel_report(vault_factory(), month)

    # ------------------------------------------------------------- 本地写入
    @tool(LOCAL)
    def add_idea(text: str, edge: str | None = None,
                 origin: Literal["memo", "reader_reply", "x_outlier", "own_post"] = "memo") -> dict:
        """往选题池加一条选题。edge 是作者觉得“别人视为理所当然、但值得怀疑”的点，必须来自作者。"""
        return vault_factory().add_idea(text, origin=origin, edge=edge)

    @tool(LOCAL)
    def new_hub(idea: str) -> dict:
        """从选题新建母稿。idea 可以是 idea_0001 这样的选题编号，也可以是一句话选题。"""
        v = vault_factory()
        i = v.idea(idea) if idea.startswith("idea_") else v.add_idea(idea)
        hub = v.new_hub(i)
        return {"hub_id": hub, "next_step": f"run_angles(hub_id='{hub}')"}

    @tool(LOCAL)
    def write_draft(hub_id: str, markdown: str,
                    written_by: Literal["author_typed", "agent_assisted"] = "author_typed") -> dict:
        """把正文写进 draft.md。作者口述或粘贴给你的原文用 author_typed；你替作者组织或改写过的，必须用 agent_assisted，
        H4 会据此把 AI 参与程度记为 assisted_text（影响 Medium 是否需要披露）。写完需要重新 run_review。"""
        v = vault_factory()
        meta = v.meta(hub_id)
        gates.check(meta, "draft")
        v.write_hub_file(hub_id, "draft.md", markdown)
        if written_by == "agent_assisted":
            meta["agent_assisted_draft"] = True
            v.save_meta(hub_id, meta)
        return {"saved": f"hubs/{hub_id}/draft.md", "next_step": f"run_review(hub_id='{hub_id}')"}

    @tool(LOCAL)
    def write_variant_text(variant_id: str, text: str) -> dict:
        """按作者的修改意见改一个变体的正文（写进 variants/<id>.md）。H5 批准时会用改后的文字重跑检查。"""
        v = vault_factory()
        v.variant(variant_id)
        v.write_variant_text(variant_id, text)
        return {"saved": f"variants/{variant_id}.md"}

    @tool(LOCAL)
    def mark_published(variant_id: str, url: str) -> dict:
        """作者本人在平台上发完之后，记下帖子链接。这个工具不会发布任何东西。"""
        x = stages.mark_published(vault_factory(), variant_id, url)
        return {"variant_id": variant_id, "status": x["status"], "url": url}

    @tool(LOCAL)
    def add_metrics(variant_id: str, values: dict[str, float]) -> dict:
        """为已发布的变体手工录入一次指标快照，如 {"impressions": 1200, "replies": 14}。"""
        from .metrics import add_snapshot

        return add_snapshot(vault_factory(), variant_id, values, source="manual_mcp")

    @tool(ToolAnnotations(read_only_hint=False, destructive_hint=False, open_world_hint=True))
    def pull_x_metrics(dry_run: bool = True) -> dict:
        """用只读接口 GET /2/tweets 拉取已发布 X 帖子的公开指标（需要服务器环境变量 X_BEARER_TOKEN，按次计费）。
        默认只估算费用；作者同意后再用 dry_run=false。"""
        from .metrics import pull_x

        return pull_x(vault_factory(), dry_run=dry_run)

    @tool(LOCAL)
    def approve_gate(hub_id: str, gate: Literal["H1", "H2", "H3", "H4", "H5"], user_statement: str,
                     angle: int | None = None, excitement: int | None = None, edge: str | None = None,
                     confirm: bool = False, quotes_checked: int | None = None,
                     numbers_checked: int | None = None, ending_ok: bool = False,
                     canonical_url: str | None = None, override_reason: str | None = None,
                     variants: list[str] | None = None) -> dict:
        """记录人工闸口。只能在作者本人明确同意之后调用；user_statement 必须逐字写入作者表示同意的那句话。
        H1：angle、excitement（1–5，作者本人打）、edge（作者自己的一句话）。H2：confirm=true。H3：无额外字段。
        H4：quotes_checked、numbers_checked（作者亲自回原链接核对的数量）、ending_ok、canonical_url，未通过评审时 override_reason。
        H5：variants（["all"] 或变体编号列表）。"""
        v = vault_factory()
        if _mcp_settings(v).get("allow_gate_approval", True) is False:
            raise VaultError(f"知识库设置了 mcp.allow_gate_approval: false；请作者在命令行运行 `ca approve {hub_id} {gate} ...`")
        if len((user_statement or "").strip()) < 2:
            raise VaultError("user_statement 不能为空：必须逐字写入作者表示同意的原话")
        meta = v.meta(hub_id)
        level = "assisted_text" if (gate == "H4" and meta.get("agent_assisted_draft")) else None
        rec = gates.approve(v, hub_id, gate, angle=angle, excitement=excitement, edge=edge, confirm=confirm,
                            quotes_checked=quotes_checked, numbers_checked=numbers_checked, ending_ok=ending_ok,
                            canonical_url=canonical_url, override_reason=override_reason,
                            variants=variants, ai_assist_level=level)
        meta = v.meta(hub_id)
        meta["gates"][gate].update({"channel": "mcp", "user_statement": user_statement})
        v.save_meta(hub_id, meta)
        return {"gate": gate, "record": meta["gates"][gate], "next_step": _next_step(meta)}

    # ------------------------------------------------------------- 需要模型的阶段
    def _stage(fn, hub_id, **kw):
        v = vault_factory()
        out = fn(v, llm_factory(v), hub_id, **kw)
        return v, out

    @tool(MODEL)
    def run_angles(hub_id: str, n: int = 4) -> str:
        """S1 选题定角：查重往期文章，给出 n 个角度。返回 angles.md，给作者看并请作者选角度、打兴奋度、说 edge（H1）。"""
        v, _ = _stage(stages.s1_angles, hub_id, n=n)
        return v.read_hub_file(hub_id, "angles.md")

    @tool(MODEL)
    def run_research(hub_id: str) -> str:
        """S2 研究取证（需 H1）：搜索、读原文、引用绑定，弱来源会标出。可能要几分钟。返回 research.md（含 H2 检查清单）。"""
        v, _ = _stage(stages.s2_research, hub_id)
        return v.read_hub_file(hub_id, "research.md")

    @tool(MODEL)
    def run_outline(hub_id: str) -> str:
        """S3 论点与提纲（需 H2）。返回 outline.md，请作者批准（H3）。"""
        v, _ = _stage(stages.s3_outline, hub_id)
        return v.read_hub_file(hub_id, "outline.md")

    @tool(MODEL)
    def run_draft(hub_id: str, mode: Literal["A", "B", "I"] = "A") -> str:
        """S4 起草（需 H3）。A：只生成素材卡片 cards.md，正文由作者写（默认）；B：按提纲起草，经历/数字/立场留 [TK]；
        I：返回访谈提问，作者口述后用 run_interview 整理。"""
        v, name = _stage(stages.s4_draft, hub_id, mode=mode)
        return v.read_hub_file(hub_id, name)

    @tool(MODEL)
    def run_interview(hub_id: str, transcript: str) -> str:
        """模式 I：把作者的口述转写稿按提纲整理（只调顺序、删冗，不加内容），并做 CRIBS 标注。返回 cribs.md。"""
        from .loops import interview

        v = vault_factory()
        interview(v, llm_factory(v), hub_id, transcript)
        return v.read_hub_file(hub_id, "cribs.md")

    @tool(MODEL)
    def run_review(hub_id: str) -> str:
        """S5 编辑评审：lint、陌生人重读、拔刺、Dry 三问、逐条事实核查、风格漂移、反恭维打分。
        返回 review.md；末尾有 H4 人工核对清单，引语和数字必须由作者本人回原链接核对。"""
        v, _ = _stage(stages.s5_review, hub_id)
        return v.read_hub_file(hub_id, "review.md")

    @tool(MODEL)
    def run_adapt(hub_id: str, formats: list[Literal["x_post", "substack_note", "x_thread", "x_article",
                                                     "medium_story"]] | None = None,
                  n_x: int = 5, n_notes: int = 5) -> str:
        """S6 平台改编（需 H4）：生成各平台变体和 Substack 发布包，每个变体都过平台检查。返回 review_queue.md，
        请作者审稿；要改哪条用 write_variant_text，再由作者批准 H5。"""
        v, _ = _stage(stages.s6_adapt, hub_id, formats=formats, n_x=n_x, n_notes=n_notes)
        return v.read_hub_file(hub_id, "review_queue.md")

    @tool(MODEL)
    def run_retro(month: str) -> str:
        """S8 月度复盘（如 2026-11）：前/后 20% 特征、作者反复做的修改、修改建议、R1/R2 候选。建议不会自动生效。"""
        from .retro import build_retro

        v = vault_factory()
        build_retro(v, llm_factory(v), month)
        return (v.root / "runs" / f"retro_{month}.md").read_text(encoding="utf-8")

    @tool(LOCAL)
    def submit_model_output(task_id: str, output: str) -> str:
        """宿主模型模式：交回一个待办模型任务的结果（JSON 任务交 JSON 文本，文本任务交 markdown）。
        服务器会校验格式，然后自动继续原来的工具；可能返回下一个待办任务，照做直到拿到最终结果。"""
        from .host_llm import HostLLM

        v = vault_factory()
        host = HostLLM(v.root, v.llm_config())
        task = host.task(task_id)
        resume = task.get("resume")
        host.submit(task_id, output)
        if not resume or resume["tool"] not in wrapped_tools:
            return "已保存。请重新调用原来的工具继续。"
        return wrapped_tools[resume["tool"]](**resume["args"])

    @tool(READ)
    def model_backend() -> dict[str, Any]:
        """查看需要模型的阶段由谁来做：anthropic（服务器调用 Anthropic API）或 host（交给你，即当前对话的模型）。"""
        v = vault_factory()
        b = llm_backend(v)
        return {"backend": b, "note": "host 模式下，run_* 工具会返回待办任务，你完成后用 submit_model_output 交回"
                if b == "host" else "使用服务器配置的 ANTHROPIC_API_KEY"}

    @server.prompt()
    def creator_workflow() -> str:
        """creator-agent 的完整工作流和硬规则（给 agent 终端的系统提示）。"""
        return INSTRUCTIONS

    return server


def _next_step(meta: dict) -> str:
    g = meta.get("gates", {})
    hub = meta["id"]
    if "H1" not in g:
        return f"run_angles(hub_id='{hub}')，然后请作者决定 H1" if meta["status"] == "created" else "请作者决定 H1"
    if "H2" not in g:
        return f"run_research(hub_id='{hub}')，然后请作者检查 research.md 并决定 H2"
    if "H3" not in g:
        return f"run_outline(hub_id='{hub}')，然后请作者决定 H3"
    if "H4" not in g:
        return "run_draft → 作者写 draft.md → run_review → 作者核对后决定 H4"
    if "H5" not in g:
        return f"run_adapt(hub_id='{hub}') → 作者审稿 → 作者决定 H5"
    return "作者按 publish_kit.md 手动发布，发完调用 mark_published 记下链接"


# ------------------------------------------------------------------ 入口
def _http_app(server, token: str | None, allowed_hosts: list[str]):
    from mcp.server.transport_security import TransportSecuritySettings

    security = TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=["127.0.0.1:*", "localhost:*", "[::1]:*", *allowed_hosts],
        allowed_origins=["http://127.0.0.1:*", "http://localhost:*", *[f"https://{h}" for h in allowed_hosts]],
    )
    app = server.streamable_http_app(transport_security=security)
    return token_guard(app, token) if token else app


def token_guard(app, token: str):
    """校验 `Authorization: Bearer <token>`，或 `?token=<token>`（有些终端如 ChatGPT 自定义连接器可能不支持自定义请求头；
    代价是 Token 会出现在 URL 里）。"""
    from urllib.parse import parse_qs

    from starlette.responses import JSONResponse

    async def guarded(scope, receive, send):
        if scope["type"] == "http":
            headers = dict(scope.get("headers") or [])
            given = headers.get(b"authorization", b"").decode()
            q = parse_qs((scope.get("query_string") or b"").decode()).get("token", [""])[0]
            ok = hmac.compare_digest(given.encode(), f"Bearer {token}".encode()) or (
                bool(q) and hmac.compare_digest(q.encode(), token.encode()))
            if not ok:
                await JSONResponse({"error": "unauthorized"}, status_code=401)(scope, receive, send)
                return
        await app(scope, receive, send)

    return guarded


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="creator-agent-mcp",
                                description="creator-agent 的 MCP 服务器（默认 stdio）")
    p.add_argument("--vault", help="知识库目录（默认 $CA_VAULT）")
    p.add_argument("--http", action="store_true", help="改用 Streamable HTTP（默认 127.0.0.1:8765/mcp）")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--init-if-missing", action="store_true",
                   help="知识库目录不存在或为空时自动创建（Claude 桌面端扩展安装后首次启动用）")
    p.add_argument("--allowed-host", action="append", default=[],
                   help="经隧道暴露时，允许的外部 Host（如 abc.trycloudflare.com），可重复")
    args = p.parse_args(argv)
    if args.vault:
        os.environ["CA_VAULT"] = args.vault
    # Claude 桌面端扩展里，可选字段留空时可能传空串或未替换的 ${user_config.*}；都当作没填
    for k in ("ANTHROPIC_API_KEY", "X_BEARER_TOKEN"):
        if os.environ.get(k, "").strip().startswith("${") or not os.environ.get(k, "x").strip():
            os.environ.pop(k, None)
    if args.init_if_missing:
        root = Path(os.environ.get("CA_VAULT", "creator-vault")).expanduser()
        if not (root / "agent.yaml").exists() and (not root.exists() or not any(root.iterdir())):
            Vault.init(root)
            print(f"已创建知识库 {root}", file=sys.stderr)
    try:
        _vault()
    except VaultError as e:
        print(f"错误：{e}", file=sys.stderr)
        return 1
    server = build_server()
    if not args.http:
        server.run("stdio")
        return 0
    token = os.environ.get("CA_MCP_TOKEN")
    if args.host not in ("127.0.0.1", "localhost", "::1") and not token:
        print("错误：监听非本机地址时必须设置 CA_MCP_TOKEN", file=sys.stderr)
        return 1
    if args.allowed_host and not token:
        print("错误：允许外部 Host（隧道）时必须设置 CA_MCP_TOKEN", file=sys.stderr)
        return 1
    import uvicorn

    print(f"creator-agent MCP 正在 http://{args.host}:{args.port}/mcp 上运行"
          f"{'（已启用 Bearer Token）' if token else '（仅本机）'}", file=sys.stderr)
    uvicorn.run(_http_app(server, token, args.allowed_host), host=args.host, port=args.port, log_level="warning")
    return 0


if __name__ == "__main__":
    sys.exit(main())
