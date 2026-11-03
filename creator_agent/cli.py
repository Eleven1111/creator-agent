"""命令行入口 `ca`。知识库目录用 --vault 指定，或设环境变量 CA_VAULT（默认 ./creator-vault）。"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from . import gates, stages
from .llm import LLM, LLMError
from .vault import Vault, VaultError


def _vault(args) -> Vault:
    v = Vault(Path(args.vault or os.environ.get("CA_VAULT", "creator-vault")))
    v.require()
    stale = v.stale_platform_rules()
    if stale:
        print(f"⚠️ 平台规则超过 90 天未核对：{'、'.join(stale)}", file=sys.stderr)
    return v


def _llm(v: Vault) -> LLM:
    return LLM(v.llm_config(), log_dir=v.root / "runs/logs")


def cmd_init(args):
    v = Vault.init(Path(args.path))
    print(f"已创建知识库 {v.root}。下一步（P0 建库）：")
    print("  1. 改 voice/profile.yaml、never.md、stances.md、stories.md")
    print("  2. 往 voice/exemplars/ 放 5–15 段你自己的范文")
    print("  3. `ca import-rss <你的 Substack RSS>` 导入往期文章")
    print("  4. 往 evals/anchors/ 放好稿、差稿各 2 篇以上（good_*.md / bad_*.md）")
    print("  5. `ca idea add \"...\" --edge \"...\"` 录入选题")


def cmd_import_rss(args):
    v = _vault(args)
    from .importer import import_rss

    names = import_rss(v, args.url)
    print(f"导入 {len(names)} 篇到 archive/")


def cmd_idea(args):
    v = _vault(args)
    if args.action == "add":
        if not args.text:
            raise VaultError("用法：ca idea add \"选题\" [--edge \"...\"]")
        idea = v.add_idea(args.text, origin=args.origin, edge=args.edge)
        print(f"{idea['id']}  {idea['raw']}")
    else:
        for i in v.ideas():
            edge = i.get("edge") or "（未写 edge）"
            print(f"{i['id']}  [{i['status']}]  {i['raw']}  —— {edge}")


def cmd_new(args):
    v = _vault(args)
    idea = v.idea(args.idea) if args.idea.startswith("idea_") else v.add_idea(args.idea)
    hub_id = v.new_hub(idea)
    print(hub_id)
    if args.angles:
        stages.s1_angles(v, _llm(v), hub_id, n=args.n)
        print(f"选题角度已写入 hubs/{hub_id}/angles.md")


def cmd_angles(args):
    v = _vault(args)
    stages.s1_angles(v, _llm(v), args.hub, n=args.n)
    print(f"hubs/{args.hub}/angles.md")


def cmd_research(args):
    v = _vault(args)
    r = stages.s2_research(v, _llm(v), args.hub)
    weak = sum(1 for f in r["findings"] if f["weak"])
    print(f"{len(r['findings'])} 条发现（{weak} 条弱来源）→ hubs/{args.hub}/research.md")


def cmd_outline(args):
    v = _vault(args)
    o = stages.s3_outline(v, _llm(v), args.hub)
    print(f"{len(o['sections'])} 节，{len(o['problems'])} 个程序检查问题 → hubs/{args.hub}/outline.md")


def cmd_draft(args):
    v = _vault(args)
    name = stages.s4_draft(v, _llm(v), args.hub, mode=args.mode)
    print(f"hubs/{args.hub}/{name}")


def cmd_review(args):
    v = _vault(args)
    r = stages.s5_review(v, _llm(v), args.hub)
    print(f"{'通过' if r['pass'] else '未通过'}，评审分 {r['judge'].get('score', 0):.2f} → hubs/{args.hub}/review.md")


def cmd_adapt(args):
    v = _vault(args)
    formats = args.formats.split(",") if args.formats else None
    vs = stages.s6_adapt(v, _llm(v), args.hub, n_x=args.x, n_notes=args.notes, formats=formats)
    for x in vs:
        mark = "✓" if x["gate_results"]["passed"] else f"✗ {x['gate_results']['failed']}"
        print(f"{x['variant_id']}  {mark}")
    for fmt, why in (v.meta(args.hub).get("skipped_formats") or {}).items():
        print(f"跳过 {fmt}：{why}")
    print(f"待审稿件 → hubs/{args.hub}/review_queue.md（正文可直接改 variants/<id>.md）")
    print(f"Substack 发布包 → hubs/{args.hub}/substack_package.md")
    print(f"审批：`ca approve {args.hub} H5 --variants all`，审批后生成 publish_kit.md")


def cmd_approve(args):
    v = _vault(args)
    fields = {
        "angle": args.angle, "excitement": args.excitement, "edge": args.edge,
        "confirm": args.confirm, "notes": args.notes,
        "quotes_checked": args.quotes_checked, "numbers_checked": args.numbers_checked,
        "ending_ok": args.ending_ok, "override_reason": args.override_reason,
        "canonical_url": args.canonical_url, "canonical_url_en": args.canonical_url_en,
        "ai_assist_level": args.ai_assist_level,
        "variants": args.variants.split(",") if args.variants else None, "force": args.force,
    }
    rec = gates.approve(v, args.hub, args.gate, **fields)
    print(f"{args.gate} 已记录：{json.dumps(rec, ensure_ascii=False)}")
    if args.gate == "H5":
        print(f"发布包 → {rec['publish_kit']}（全部由你本人发布）")


def cmd_published(args):
    v = _vault(args)
    stages.mark_published(v, args.variant, args.url, cost_usd=args.cost)
    print(f"{args.variant} 已记录为 published")


def cmd_log_edit(args):
    v = _vault(args)
    meta = v.meta(args.hub)
    meta["edit_minutes"].append({"stage": args.stage, "minutes": args.minutes})
    v.save_meta(args.hub, meta)
    total = sum(e["minutes"] for e in meta["edit_minutes"])
    print(f"{args.hub} 人工编辑累计 {total} 分钟")


def cmd_status(args):
    v = _vault(args)
    hubs = [v.meta(args.hub)] if args.hub else v.hubs()
    for m in hubs:
        g = ",".join(sorted(m["gates"])) or "-"
        mins = sum(e["minutes"] for e in m.get("edit_minutes", []))
        print(f"{m['id']}  状态 {m['status']}  闸口 {g}  模式 {m.get('draft_mode')}  编辑 {mins} 分钟")
        if args.hub:
            for x in v.variants_of(m["id"]):
                print(f"  {x['variant_id']}  {x['status']}  {x['schedule']['planned_at']}")


def cmd_kit(args):
    v = _vault(args)
    from .adapt import write_publish_kit

    print(write_publish_kit(v, args.hub))


def cmd_due(args):
    import datetime as dt

    v = _vault(args)
    horizon = dt.datetime.now().astimezone() + dt.timedelta(hours=args.hours)
    rows = [x for x in v.all_variants() if x["status"] == "approved"
            and dt.datetime.fromisoformat(x["schedule"]["planned_at"]) <= horizon]
    for x in sorted(rows, key=lambda x: x["schedule"]["planned_at"]):
        print(f"{x['schedule']['planned_at']}  {x['format']:<14} {x['variant_id']}  → hubs/{x['hub_id']}/publish_kit.md")
    if not rows:
        print(f"未来 {args.hours} 小时没有待发布的稿子")


def cmd_metrics(args):
    v = _vault(args)
    from . import metrics as M

    if args.action == "add":
        values = {}
        for kv in args.values:
            k, _, val = kv.partition("=")
            values[k] = float(val) if "." in val else int(val)
        print(json.dumps(M.add_snapshot(v, args.target, values, source="manual"), ensure_ascii=False))
    elif args.action == "pull-x":
        r = M.pull_x(v, dry_run=args.dry_run)
        print(f"{r['posts']} 条已发布的 X 帖子，预估读取费用 ${r['estimated_cost_usd']}，写入 {r['written']} 条快照")
    elif args.action == "import":
        n = M.import_csv(v, Path(args.target), source=args.source)
        print(f"导入 {n} 行")


def cmd_report(args):
    v = _vault(args)
    from .metrics import channel_report

    print(json.dumps(channel_report(v, args.month), ensure_ascii=False, indent=2))


def cmd_retro(args):
    v = _vault(args)
    from .retro import build_retro

    r = build_retro(v, _llm(v), args.month)
    print(f"复盘 → runs/retro_{args.month}.md；R1 候选 {len(r['r1_candidates'])} 条，R2 候选 {len(r['r2_candidates'])} 条")


def cmd_retro_approve(args):
    v = _vault(args)
    from .retro import approve_retro

    rec = approve_retro(v, args.month, args.r1.split(",") if args.r1 else None, args.note)
    print(f"H7 已记录：{json.dumps(rec, ensure_ascii=False)}")


def cmd_interview(args):
    v = _vault(args)
    from .loops import interview

    if args.audio:
        from .transcribe import transcribe

        lang = (v.profile().get("languages") or {}).get("hub", "zh")
        text = transcribe(Path(args.audio), model_size=args.whisper_model, language=lang)
        print(f"本地转写完成：{len(text)} 字")
    elif args.transcript:
        text = Path(args.transcript).read_text(encoding="utf-8")
    else:
        raise VaultError("需要 --transcript 文字稿 或 --audio 音频文件")
    r = interview(v, _llm(v), args.hub, text)
    warn = len(r["suspicious"]) + (1 if r["added_numbers"] else 0)
    print(f"整理稿 → hubs/{args.hub}/draft.md；CRIBS 与检查 → cribs.md（{warn} 处需要你确认）")


def cmd_promote(args):
    v = _vault(args)
    from .loops import promote

    hub = promote(v, args.variant)
    print(f"已晋升为长文母稿 {hub}；下一步 `ca angles {hub}`")


def cmd_recycle(args):
    v = _vault(args)
    from .loops import recycle

    for x in recycle(v, _llm(v), args.variant, n=args.n, force=args.force):
        mark = "✓" if x["gate_results"]["passed"] else f"✗ {x['gate_results']['failed']}"
        print(f"{x['variant_id']}  {mark}  相似度 {x['gate_results']['checks']['similarity_to_published']}")
    print("改稿在 variants/<id>.md；审批：`ca approve <hub> H5 --variants <id>`")


def cmd_progress(args):
    v = _vault(args)
    from .loops import progress

    print(json.dumps(progress(v), ensure_ascii=False, indent=2))


def cmd_flow(args):
    v = _vault(args)
    from . import graph

    llm = _llm(v)
    if args.action == "start":
        hub = args.target
        if not (v.root / "hubs" / hub / "meta.json").exists():
            idea = v.idea(hub) if hub.startswith("idea_") else v.add_idea(hub)
            hub = v.new_hub(idea)
        waiting = graph.start(v, llm, hub)
    elif args.action == "resume":
        hub = args.target
        waiting = graph.resume(v, llm, hub, graph.parse_answer(args.set or [], args.do))
    else:
        hub = args.target
        st = graph.status(v, llm, hub)
        waiting = st["waiting"]
        if st["done"]:
            print(f"{hub} 的流程已走完；去 hubs/{hub}/publish_kit.md 手动发布")
            return
    if waiting is None:
        print(f"{hub} 的流程已走完；去 hubs/{hub}/publish_kit.md 手动发布")
        return
    print(f"{hub} 停在 {waiting['gate']}：{waiting['ask']}")
    print(f"  先看：{waiting['review']}")
    if waiting.get("error"):
        print(f"  上次输入被拒：{waiting['error']}")
    ex = " ".join(f"{k}={','.join(x) if isinstance(x, list) else x}" for k, x in waiting["example_resume"].items()
                  if k != "action")
    cmd = f"ca flow resume {hub} --do {waiting['example_resume'].get('action', 'approve')}"
    print(f"  继续：{cmd} --set {ex}" if ex else f"  继续：{cmd}")
    for alt in waiting.get("other_actions", []):
        print(f"  或者：ca flow resume {hub} --do {alt}")


def cmd_survey(args):
    v = _vault(args)
    from . import survey

    if args.action == "design":
        if not args.goal_or_id:
            raise VaultError("用法：ca survey design \"调查目的\" [--topic ...]")
        sid = survey.design(v, _llm(v), args.goal_or_id, topic=args.topic or "", n=args.n)
        print(f"问卷 → surveys/{sid}/survey.md；收集回答用 responses_template.csv 的表头")
    else:
        if not (args.goal_or_id and args.responses):
            raise VaultError("用法：ca survey analyze <survey_id> <responses.csv>")
        r = survey.analyze(v, _llm(v), args.goal_or_id, Path(args.responses))
        print(f"n={r['n']}，分析 → surveys/{args.goal_or_id}/analysis.md")


def cmd_blind(args):
    v = _vault(args)
    from .audit import blind_prepare, blind_score

    if args.action == "prepare":
        batch = blind_prepare(v, args.ai.split(","), [Path(p) for p in args.human.split(",")])
        print(f"盲评包 → evals/{batch}/：读 item_*.md，在 ratings.csv 打 1–5 分（不要打开 .key.json）")
        print(f"打完：ca blind score {batch}")
    else:
        r = blind_score(v, args.batch)
        verdict = "AI 参与稿不低于纯人写稿 ✓" if r["ai_not_worse"] else "AI 参与稿低于纯人写稿 ✗"
        print(f"AI 组 {r['ai_mean']}（{r['n_ai']} 篇）vs 人写组 {r['human_mean']}（{r['n_human']} 篇）：{verdict}")


def cmd_audit(args):
    v = _vault(args)
    from .audit import audit

    r = audit(v)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    if not r["ok"]:
        raise VaultError(f"审计发现 {len(r['violations'])} 处问题")


def cmd_mcp(args):
    from .mcp_server import main as mcp_main

    argv = ["--vault", args.vault] if args.vault else []
    if args.http:
        argv += ["--http", "--host", args.host, "--port", str(args.port)]
        for h in args.allowed_host:
            argv += ["--allowed-host", h]
    raise SystemExit(mcp_main(argv))


def cmd_install_skill(args):
    from .skill import install_skill

    for p in install_skill(args.target, Path(args.dir) if args.dir else None):
        print(f"已安装 → {p}")


def cmd_eval(args):
    v = _vault(args)
    from .evalset import run_eval

    s = run_eval(v, _llm(v))
    print(json.dumps({k: s[k] for k in s if k != "results"}, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ca", description="多平台创作 Agent（P1–P4）：所有发布都由你本人完成")
    p.add_argument("--vault", help="知识库目录（默认 $CA_VAULT 或 ./creator-vault）")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="P0：创建知识库骨架")
    s.add_argument("path")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("import-rss", help="P0：用 RSS 导入往期文章")
    s.add_argument("url")
    s.set_defaults(func=cmd_import_rss)

    s = sub.add_parser("idea", help="选题池")
    s.add_argument("action", choices=["add", "list"])
    s.add_argument("text", nargs="?")
    s.add_argument("--origin", default="memo",
                   choices=["memo", "reader_reply", "x_outlier", "own_post"])
    s.add_argument("--edge")
    s.set_defaults(func=cmd_idea)

    s = sub.add_parser("new", help="从选题（idea_id 或一句话）新建母稿")
    s.add_argument("idea")
    s.add_argument("--angles", action="store_true", help="创建后立刻跑 S1")
    s.add_argument("-n", type=int, default=4)
    s.set_defaults(func=cmd_new)

    for name, fn, helptext in [("angles", cmd_angles, "S1 选题定角"),
                               ("research", cmd_research, "S2 研究取证（需 H1）"),
                               ("outline", cmd_outline, "S3 论点与提纲（需 H2）"),
                               ("review", cmd_review, "S5 编辑评审")]:
        s = sub.add_parser(name, help=helptext)
        s.add_argument("hub")
        if name == "angles":
            s.add_argument("-n", type=int, default=4)
        s.set_defaults(func=fn)

    s = sub.add_parser("draft", help="S4 起草（需 H3）；默认模式见 profile.yaml")
    s.add_argument("hub")
    s.add_argument("--mode", choices=["A", "B", "I"])
    s.set_defaults(func=cmd_draft)

    s = sub.add_parser("adapt", help="S6 平台适配：X 单帖 / Notes / Thread / Article / Medium（需 H4）")
    s.add_argument("hub")
    s.add_argument("--x", type=int, default=5)
    s.add_argument("--notes", type=int, default=5)
    s.add_argument("--formats", help="逗号分隔：x_post,substack_note,x_thread,x_article,medium_story")
    s.set_defaults(func=cmd_adapt)

    s = sub.add_parser("approve", help="记录人工闸口 H1–H5")
    s.add_argument("hub")
    s.add_argument("gate", choices=list(gates.GATE_DESC))
    s.add_argument("--angle", type=int)
    s.add_argument("--excitement", type=int)
    s.add_argument("--edge")
    s.add_argument("--confirm", action="store_true")
    s.add_argument("--notes")
    s.add_argument("--quotes-checked", type=int)
    s.add_argument("--numbers-checked", type=int)
    s.add_argument("--ending-ok", action="store_true")
    s.add_argument("--override-reason")
    s.add_argument("--canonical-url")
    s.add_argument("--canonical-url-en", help="英文版另有母稿时的 canonical")
    s.add_argument("--ai-assist-level", choices=["none", "edit_only", "outline", "assisted_text", "draft_B"])
    s.add_argument("--variants", help="逗号分隔的 variant_id，或 all")
    s.add_argument("--force", action="store_true")
    s.set_defaults(func=cmd_approve)

    s = sub.add_parser("published", help="人工发布后记录链接")
    s.add_argument("variant")
    s.add_argument("url")
    s.add_argument("--cost", type=float)
    s.set_defaults(func=cmd_published)

    s = sub.add_parser("log-edit", help="记录人工编辑时长（P1 完成标准之一）")
    s.add_argument("hub")
    s.add_argument("minutes", type=int)
    s.add_argument("--stage", default="draft")
    s.set_defaults(func=cmd_log_edit)

    s = sub.add_parser("status", help="查看母稿与变体状态")
    s.add_argument("hub", nargs="?")
    s.set_defaults(func=cmd_status)

    s = sub.add_parser("kit", help="重新生成发布包 publish_kit.md")
    s.add_argument("hub")
    s.set_defaults(func=cmd_kit)

    s = sub.add_parser("due", help="列出接下来要你手动发布的稿子")
    s.add_argument("--hours", type=int, default=24)
    s.set_defaults(func=cmd_due)

    s = sub.add_parser("metrics", help="S8 指标回流（只读）：add 手工录入 / pull-x 拉 X 公开指标 / import CSV")
    s.add_argument("action", choices=["add", "pull-x", "import"])
    s.add_argument("target", nargs="?", help="add：variant_id；import：CSV 路径")
    s.add_argument("values", nargs="*", help="add：key=value，如 impressions=1200 replies=14")
    s.add_argument("--source", default="csv", help="import 的来源标签，如 substack_export")
    s.add_argument("--dry-run", action="store_true", help="pull-x：只估算费用")
    s.set_defaults(func=cmd_metrics)

    s = sub.add_parser("report", help="按平台×体裁汇总指标")
    s.add_argument("--month", help="如 2026-11")
    s.set_defaults(func=cmd_report)

    s = sub.add_parser("retro", help="S8 月度复盘")
    s.add_argument("month", help="如 2026-11")
    s.set_defaults(func=cmd_retro)

    s = sub.add_parser("retro-approve", help="H7：批准复盘，把 R1 候选写进选题池")
    s.add_argument("month")
    s.add_argument("--r1", help="all 或逗号分隔的 variant_id")
    s.add_argument("--note")
    s.set_defaults(func=cmd_retro_approve)

    s = sub.add_parser("interview", help="P3 模式 I：把你的口述转写稿按提纲整理，并做 CRIBS 标注（需 H3）")
    s.add_argument("hub")
    s.add_argument("--transcript", help="口述转写稿（markdown / txt）")
    s.add_argument("--audio", help="P4：音频文件，本地用 faster-whisper 转写（不上传）")
    s.add_argument("--whisper-model", default="small")
    s.set_defaults(func=cmd_interview)

    s = sub.add_parser("promote", help="P3 R1：把一条表现好的短帖晋升为长文母稿")
    s.add_argument("variant")
    s.set_defaults(func=cmd_promote)

    s = sub.add_parser("recycle", help="P3 R2：用新角度重写一条 ≥90 天的高表现短帖")
    s.add_argument("variant")
    s.add_argument("-n", type=int, default=2)
    s.add_argument("--force", action="store_true", help="跳过 90 天限制")
    s.set_defaults(func=cmd_recycle)

    s = sub.add_parser("progress", help="P3 完成度：支撑率、编辑时长趋势、R1 长文数")
    s.set_defaults(func=cmd_progress)

    s = sub.add_parser("flow", help="P4：用 LangGraph 跑整条流程，停在每个闸口等你（需 pip install -e '.[graph]'）")
    s.add_argument("action", choices=["start", "resume", "status"])
    s.add_argument("target", help="start：idea_id 或一句话选题或 hub_id；resume/status：hub_id")
    s.add_argument("--do", help="resume 的动作：approve | redo | revise | done")
    s.add_argument("--set", nargs="*", help="闸口字段 key=value，如 angle=2 excitement=4 edge=...")
    s.set_defaults(func=cmd_flow)

    s = sub.add_parser("survey", help="P4：读者调查 design / analyze")
    s.add_argument("action", choices=["design", "analyze"])
    s.add_argument("goal_or_id", nargs="?")
    s.add_argument("responses", nargs="?", help="analyze：回答 CSV")
    s.add_argument("--topic")
    s.add_argument("-n", type=int, default=10)
    s.set_defaults(func=cmd_survey)

    s = sub.add_parser("blind", help="P4：作者盲评 AI 参与稿 vs 纯人写稿")
    s.add_argument("action", choices=["prepare", "score"])
    s.add_argument("batch", nargs="?")
    s.add_argument("--ai", help="逗号分隔的 hub_id（AI 参与组）")
    s.add_argument("--human", help="逗号分隔的 md 文件（纯人写组）")
    s.set_defaults(func=cmd_blind)

    s = sub.add_parser("audit", help="P4：审计——每次发布都经人工批准、没有自动互动、平台规则 90 天内核对过")
    s.set_defaults(func=cmd_audit)

    s = sub.add_parser("mcp", help="启动 MCP 服务器，供 Claude 桌面端 / ChatGPT / OpenClaw / Hermes / WorkBuddy 接入")
    s.add_argument("--http", action="store_true")
    s.add_argument("--host", default="127.0.0.1")
    s.add_argument("--port", type=int, default=8765)
    s.add_argument("--allowed-host", action="append", default=[])
    s.set_defaults(func=cmd_mcp)

    s = sub.add_parser("install-skill", help="把 SKILL.md 技能包装到 agent 终端的技能目录")
    s.add_argument("target", choices=["claude-code", "openclaw", "hermes", "workbuddy", "agents", "zip", "dir"])
    s.add_argument("--dir", help="target=dir 时的目标目录")
    s.set_defaults(func=cmd_install_skill)

    s = sub.add_parser("eval", help="在离线测试集上检验评审能否区分好稿和差稿")
    s.set_defaults(func=cmd_eval)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        args.func(args)
    except (VaultError, LLMError) as e:
        print(f"错误：{e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
