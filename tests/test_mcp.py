import asyncio
import importlib.util
import json
import os
import sys
import zipfile
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(importlib.util.find_spec("mcp") is None,
                                reason="需要 pip install -e '.[mcp]'")

from creator_agent.llm import LLM
from creator_agent.vault import Vault

from fakes import FakeClient, _no_network
from test_pipeline import GOOD_DRAFT


@pytest.fixture
def vault(tmp_path):
    v = Vault.init(tmp_path / "vault")
    _no_network(v)
    return v


@pytest.fixture
def server(vault):
    from creator_agent.mcp_server import build_server

    fc = FakeClient()
    return build_server(lambda: vault, lambda v: LLM(v.llm_config(), client=fc))


def run(coro):
    return asyncio.run(coro)


async def call(c, name, args):
    r = await c.call_tool(name, args)
    text = r.content[0].text if r.content else ""
    if r.is_error:
        return {"error": text}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def test_full_flow_over_mcp(server, vault):
    from mcp import Client

    async def go():
        async with Client(server) as c:
            names = {t.name for t in (await c.list_tools()).tools}
            assert {"approve_gate", "run_adapt", "mark_published"} <= names
            assert not any("publish" in n and n != "mark_published" for n in names)  # 没有发布工具
            hub = (await call(c, "new_hub", {"idea": "小团队要不要做用户访谈？"}))["hub_id"]
            # 闸口顺序：没过 H1 不能研究，错误提示会告诉 agent 去问作者
            err = (await call(c, "run_research", {"hub_id": hub}))["error"]
            assert "H1" in err and "approve_gate" in err
            assert "角度 1" in await call(c, "run_angles", {"hub_id": hub})
            assert "user_statement" in (await call(c, "approve_gate", {
                "hub_id": hub, "gate": "H1", "user_statement": " ", "angle": 1, "excitement": 4,
                "edge": "大家默认按项目做"}))["error"]
            rec = await call(c, "approve_gate", {"hub_id": hub, "gate": "H1", "user_statement": "选 1，兴奋度 4",
                                                 "angle": 1, "excitement": 4, "edge": "大家默认按项目做"})
            assert rec["record"]["channel"] == "mcp" and rec["record"]["user_statement"] == "选 1，兴奋度 4"
            assert "H2 检查清单" in await call(c, "run_research", {"hub_id": hub})
            await call(c, "approve_gate", {"hub_id": hub, "gate": "H2", "user_statement": "研究没问题", "confirm": True})
            await call(c, "run_outline", {"hub_id": hub})
            await call(c, "approve_gate", {"hub_id": hub, "gate": "H3", "user_statement": "提纲可以"})
            assert "素材卡片" in await call(c, "run_draft", {"hub_id": hub})
            await call(c, "write_draft", {"hub_id": hub, "markdown": GOOD_DRAFT, "written_by": "agent_assisted"})
            assert "通过" in await call(c, "run_review", {"hub_id": hub})
            h4 = await call(c, "approve_gate", {"hub_id": hub, "gate": "H4", "user_statement": "我核对过了",
                                                "quotes_checked": 1, "numbers_checked": 0, "ending_ok": True,
                                                "canonical_url": "https://me.substack.com/p/x"})
            assert "error" not in h4
            queue = await call(c, "run_adapt", {"hub_id": hub, "formats": ["x_post", "substack_note"],
                                                "n_x": 2, "n_notes": 1})
            assert "待审稿件" in queue
            vid = f"v_{hub}_x_post_01"
            await call(c, "write_variant_text", {"variant_id": vid,
                                                 "text": "按项目做访谈的团队，三个月后几乎都停了。你们按周还是按项目？"})
            await call(c, "approve_gate", {"hub_id": hub, "gate": "H5", "user_statement": "都发吧",
                                           "variants": ["all"]})
            kit = await call(c, "read_hub_file", {"hub_id": hub, "name": "publish_kit.md"})
            assert "按项目做访谈的团队" in kit
            due = await call(c, "due", {"hours": 240})
            assert any(d["variant_id"] == vid for d in (due if isinstance(due, list) else [due]))
            await call(c, "mark_published", {"variant_id": vid, "url": "https://x.com/me/status/1"})
            await call(c, "add_metrics", {"variant_id": vid, "values": {"impressions": 100, "replies": 3}})
            audit = await call(c, "audit", {})
            assert audit["ok"] and len(audit["mcp_approvals"]) == 5
            return hub

    hub = run(go())
    # 作者让 agent 代写过正文 → H4 记为 assisted_text
    assert vault.meta(hub)["ai_assist_level"] == "assisted_text"


def test_read_hub_file_whitelist(server, vault):
    from mcp import Client

    hub = vault.new_hub(vault.add_idea("一个题"))

    async def go():
        async with Client(server) as c:
            return await call(c, "read_hub_file", {"hub_id": hub, "name": "../../agent.yaml"})

    assert "只能读取" in run(go())["error"]


def test_gate_approval_can_be_disabled(server, vault):
    from mcp import Client

    cfg = vault.root / "agent.yaml"
    cfg.write_text(cfg.read_text(encoding="utf-8").replace("allow_gate_approval: true",
                                                           "allow_gate_approval: false"), encoding="utf-8")
    hub = vault.new_hub(vault.add_idea("一个题"))

    async def go():
        async with Client(server) as c:
            await call(c, "run_angles", {"hub_id": hub})
            return await call(c, "approve_gate", {"hub_id": hub, "gate": "H1", "user_statement": "好",
                                                  "angle": 1, "excitement": 3, "edge": "一个足够长的 edge"})

    assert "ca approve" in run(go())["error"]
    assert "H1" not in vault.meta(hub)["gates"]


def test_lint_and_check_x_post_tools(server, vault):
    from mcp import Client

    async def go():
        async with Client(server) as c:
            lint = await call(c, "lint_text", {"text": "还没写完 [TK: 数据]"})
            x = await call(c, "check_x_post", {"text": "看这里 https://a.com #增长"})
            return lint, x

    lint, x = run(go())
    assert not lint["ok"] and lint["blocking"][0]["check"] == "tk"
    assert x["no_link"] is False and x["no_hashtags"] is False


def test_stdio_subprocess(vault):
    from mcp import Client, StdioServerParameters

    params = StdioServerParameters(command=sys.executable, args=["-m", "creator_agent.mcp_server",
                                                                 "--vault", str(vault.root)],
                                   env={**os.environ, "PYTHONPATH": str(Path(__file__).parent.parent)})

    async def go():
        async with Client(params) as c:
            tools = (await c.list_tools()).tools
            status = await call(c, "vault_status", {})
            return tools, status

    tools, status = run(go())
    assert len(tools) >= 20 and status["vault"] == str(vault.root)


def test_http_token_guard():
    from creator_agent.mcp_server import token_guard

    async def inner(scope, receive, send):
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"ok"})

    app = token_guard(inner, "s3cret")
    sent = []

    async def go(auth, qs=b""):
        headers = [(b"host", b"127.0.0.1:8765")] + ([(b"authorization", auth)] if auth else [])
        scope = {"type": "http", "method": "POST", "path": "/mcp", "headers": headers, "query_string": qs,
                 "scheme": "http", "server": ("127.0.0.1", 8765), "client": ("127.0.0.1", 1), "root_path": ""}

        async def receive():
            return {"type": "http.request", "body": b"", "more_body": False}

        async def send(msg):
            sent.append(msg)

        await app(scope, receive, send)
        return next(m["status"] for m in sent if m["type"] == "http.response.start")

    assert run(go(None)) == 401
    sent.clear()
    assert run(go(b"Bearer wrong")) == 401
    sent.clear()
    assert run(go(None, b"token=wrong")) == 401
    sent.clear()
    assert run(go(None, b"token=s3cret")) == 200
    sent.clear()
    assert run(go(b"Bearer s3cret")) == 200


def test_http_refuses_public_bind_without_token(vault, monkeypatch, capsys):
    from creator_agent.mcp_server import main

    monkeypatch.delenv("CA_MCP_TOKEN", raising=False)
    assert main(["--vault", str(vault.root), "--http", "--host", "0.0.0.0"]) == 1
    assert main(["--vault", str(vault.root), "--http", "--allowed-host", "x.trycloudflare.com"]) == 1
    assert "CA_MCP_TOKEN" in capsys.readouterr().err


# ------------------------------------------------------------------ 技能包
def test_skill_frontmatter():
    from creator_agent.skill import SKILL_SRC

    text = (SKILL_SRC / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---\n")
    front = text.split("---\n")[1]
    import yaml

    meta = yaml.safe_load(front)
    assert meta["name"] == "creator-agent"
    assert 20 < len(meta["description"]) <= 1024


def test_install_skill(tmp_path, monkeypatch):
    from creator_agent.skill import install_skill
    from creator_agent.vault import VaultError

    monkeypatch.setenv("HOME", str(tmp_path))
    for target, rel in [("openclaw", ".openclaw/skills"), ("hermes", ".hermes/skills"),
                        ("workbuddy", ".workbuddy/skills"), ("claude-code", ".claude/skills")]:
        p = install_skill(target)[0]
        assert p == tmp_path / rel / "creator-agent" / "SKILL.md" and p.exists()
    install_skill("openclaw")  # 覆盖自己装过的：可以
    foreign = tmp_path / ".hermes/skills/creator-agent"
    (foreign / "SKILL.md").write_text("---\nname: something-else\n---\n", encoding="utf-8")
    with pytest.raises(VaultError, match="没有覆盖"):
        install_skill("hermes")
    z = install_skill("zip", tmp_path)[0]
    assert "creator-agent/SKILL.md" in zipfile.ZipFile(z).namelist()
