"""S8 月度复盘 + H7 审批（手册“反馈闭环”）。

- 每个平台各看各的口径：X 看回复率（回复/曝光），Notes 和 Medium 看作者录入的指标。
- R1 短养长：回复率高于账号 30 日中位数 2 倍的 X 单帖 → 选题候选（origin: own_post）。
- R2 常青回收：发布 90 天以上、表现前 20% 的变体 → 用新角度重写的候选（不原样重发）。
- 提议只写进复盘报告；声音档案和规则文件由作者本人修改，H7 只负责记录批准和把 R1 写进选题池。
"""

from __future__ import annotations

import datetime as dt
import json
import statistics

from . import prompts as P
from .llm import LLM
from .metrics import latest, reply_rate
from .vault import Vault, VaultError, now_iso


def _score(v: dict, m: dict) -> float | None:
    if v["platform"] == "x":
        return reply_rate(m)
    for k in ("new_subs", "free_subs", "member_reads", "restacks", "likes"):
        if isinstance(m.get(k), (int, float)):
            return float(m[k])
    return None


def _published_at(v: dict) -> dt.datetime | None:
    at = (v.get("publish_result") or {}).get("published_at")
    try:
        t = dt.datetime.fromisoformat(at)
        return t if t.tzinfo else t.astimezone()
    except (TypeError, ValueError):
        return None


def build_retro(vault: Vault, llm: LLM, month: str, now: dt.datetime | None = None) -> dict:
    now = now or dt.datetime.now().astimezone()
    published = [v for v in vault.all_variants() if v["status"] == "published"]
    scored = []
    for v in published:
        m = latest(vault, v["variant_id"])
        s = _score(v, m) if m else None
        if s is not None:
            scored.append((v, m, s))

    month_rows = [r for r in scored if (r[0]["publish_result"]["published_at"] or "").startswith(month)]
    top, bottom = {}, {}
    for platform in sorted({r[0]["platform"] for r in month_rows}):
        rows = sorted([r for r in month_rows if r[0]["platform"] == platform], key=lambda r: -r[2])
        k = max(1, len(rows) // 5)
        top[platform] = rows[:k]
        bottom[platform] = rows[-k:] if len(rows) > k else []

    # R1：近 30 天 X 单帖，回复率 > 中位数 × 2
    recent_x = [r for r in scored if r[0]["format"] == "x_post" and _published_at(r[0])
                and (now - _published_at(r[0])).days <= 30]
    r1 = []
    if len(recent_x) >= 3:
        med = statistics.median(r[2] for r in recent_x)
        r1 = [{"variant_id": v["variant_id"], "text": v["body"]["text"], "reply_rate": round(s, 4),
               "median": round(med, 4)} for v, m, s in recent_x if med > 0 and s > 2 * med]

    # R2：发布 ≥90 天、在同平台前 20%
    r2 = []
    for platform in {r[0]["platform"] for r in scored}:
        rows = sorted([r for r in scored if r[0]["platform"] == platform], key=lambda r: -r[2])
        k = max(1, len(rows) // 5)
        for v, m, s in rows[:k]:
            t = _published_at(v)
            if t and (now - t).days >= 90:
                r2.append({"variant_id": v["variant_id"], "format": v["format"], "score": round(s, 4)})

    diffs = [d for d in vault.edit_diffs() if d["at"].startswith(month)]

    def fmt(groups):
        return json.dumps({p: [{"variant_id": v["variant_id"], "format": v["format"],
                                "text": (v["body"].get("text") or v["body"].get("title") or "")[:300],
                                "score": round(s, 4), "metrics": m} for v, m, s in rows]
                           for p, rows in groups.items()}, ensure_ascii=False)

    analysis = None
    if month_rows or diffs:
        analysis = llm.json(stage="eval", system=P.RETRO_SYSTEM, schema=P.RETRO_SCHEMA,
                            user=P.RETRO_USER.format(
                                top=fmt(top), bottom=fmt(bottom),
                                diffs=json.dumps([{k: d[k] for k in ("key", "kind", "edit_ratio", "diff")}
                                                  for d in diffs], ensure_ascii=False)[:30000]))
    retro = {
        "month": month, "at": now_iso(),
        "published_this_month": len([v for v in published
                                     if (v["publish_result"]["published_at"] or "").startswith(month)]),
        "with_metrics": len(month_rows),
        "edit_ratio_mean": round(statistics.mean(d["edit_ratio"] for d in diffs), 3) if diffs else None,
        "top": {p: [r[0]["variant_id"] for r in rows] for p, rows in top.items()},
        "bottom": {p: [r[0]["variant_id"] for r in rows] for p, rows in bottom.items()},
        "r1_candidates": r1,
        "r2_candidates": r2,
        "analysis": analysis,
        "approved": None,
    }
    path = vault.root / "runs" / f"retro_{month}.json"
    path.write_text(json.dumps(retro, ensure_ascii=False, indent=2), encoding="utf-8")
    _write_md(vault, retro)
    return retro


def _write_md(vault: Vault, r: dict) -> None:
    lines = [f"# 月度复盘 · {r['month']}（S8）", "",
             f"本月发布 {r['published_this_month']} 个变体，其中 {r['with_metrics']} 个有指标；"
             f"AI 稿平均编辑比 {r['edit_ratio_mean']}", ""]
    a = r.get("analysis")
    if a:
        lines += [f"> 样本说明：{a['sample_size_warning']}", "", "## 前 20% 的共同特征"]
        lines += [f"- [{x['platform']}] {x['pattern']}（{', '.join(x['evidence'])}）" for x in a["top_patterns"]]
        lines += ["", "## 后 20% 的共同特征"]
        lines += [f"- [{x['platform']}] {x['pattern']}（{', '.join(x['evidence'])}）" for x in a["bottom_patterns"]]
        lines += ["", "## 你反复做的修改"]
        lines += [f"- {x['pattern']}：“{x['before']}” → “{x['after']}”" for x in a["recurring_edits"]]
        lines += ["", "## 修改提议（由你决定是否采纳，手动改对应文件）"]
        lines += [f"- **{x['target']}**：{x['change']}（依据：{x['rationale']}）" for x in a["proposals"]]
    else:
        lines += ["本月没有可分析的指标或修改记录。"]
    lines += ["", "## R1 短养长候选（回复率 > 30 日中位数 × 2）"]
    lines += [f"- `{x['variant_id']}` 回复率 {x['reply_rate']}（中位数 {x['median']}）：{x['text']}"
              for x in r["r1_candidates"]] or ["- 无"]
    lines += ["", "## R2 常青回收候选（≥90 天、前 20%；用新角度重写，不原样重发）"]
    lines += [f"- `{x['variant_id']}`（{x['format']}，{x['score']}）" for x in r["r2_candidates"]] or ["- 无"]
    lines += ["", "---", f"H7：`ca retro-approve {r['month']} --r1 all`（把 R1 候选写进选题池；不改任何声音档案）"]
    (vault.root / "runs" / f"retro_{r['month']}.md").write_text("\n".join(lines), encoding="utf-8")


def approve_retro(vault: Vault, month: str, r1_ids: list[str] | None, note: str | None) -> dict:
    path = vault.root / "runs" / f"retro_{month}.json"
    if not path.exists():
        raise VaultError(f"没有 {month} 的复盘；先运行 `ca retro {month}`")
    r = json.loads(path.read_text(encoding="utf-8"))
    cands = {c["variant_id"]: c for c in r["r1_candidates"]}
    ids = list(cands) if r1_ids == ["all"] else (r1_ids or [])
    added = []
    for vid in ids:
        c = cands.get(vid)
        if c is None:
            raise VaultError(f"{vid} 不在 R1 候选里")
        added.append(vault.add_idea(c["text"], origin="own_post")["id"])
    r["approved"] = {"by": "author", "at": now_iso(), "r1_added": added, "note": note}
    path.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    return r["approved"]
