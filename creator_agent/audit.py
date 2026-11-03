"""P4：作者盲评 + 合规审计（手册 P4 完成标准）。

完成标准：
1. 作者盲评 AI 参与的稿件不低于纯人写稿件 → `ca blind prepare / score`
2. 没有任何一次未经人工按键的发布          → `ca audit`
3. 没有任何一次自动互动                    → `ca audit`
4. 平台规则 90 天内都核对过                → `ca audit`
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import random
import re
import statistics
from pathlib import Path

from .vault import Vault, VaultError, now_iso


# ================================================================ 盲评
def _strip(text: str) -> str:
    """去掉会暴露来源的痕迹：来源标记、TK、AI 披露行。"""
    text = re.sub(r"\[(f\d{2}|s_\d+|TK[^\]]*)\]", "", text)
    text = re.sub(r"(?im)^.*(AI 辅助|with the assistance of an AI).*$", "", text)
    return text.strip()


def blind_prepare(vault: Vault, ai_hubs: list[str], human_files: list[Path], seed: int | None = None) -> str:
    items = []
    for hub in ai_hubs:
        meta = vault.meta(hub)
        if meta.get("ai_assist_level") in (None, "none"):
            raise VaultError(f"{hub} 没有 AI 参与记录，不能当作 AI 组")
        items.append(("ai", hub, vault.read_hub_file(hub, "final.md")))
    for f in human_files:
        items.append(("human", str(f), Path(f).read_text(encoding="utf-8")))
    if not any(k == "ai" for k, *_ in items) or not any(k == "human" for k, *_ in items):
        raise VaultError("AI 组和纯人写组各至少 1 篇")
    rnd = random.Random(seed)
    rnd.shuffle(items)
    batch = f"blind_{now_iso()[:16].replace(':', '').replace('-', '')}"
    d = vault.root / "evals" / batch
    d.mkdir(parents=True)
    key = {}
    for i, (kind, src, text) in enumerate(items, 1):
        name = f"item_{i:02d}.md"
        (d / name).write_text(_strip(text), encoding="utf-8")
        key[name] = {"group": kind, "source": src}
    (d / ".key.json").write_text(json.dumps(key, ensure_ascii=False, indent=2), encoding="utf-8")
    with (d / "ratings.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item", "score_1_to_5", "note"])
        for name in key:
            w.writerow([name, "", ""])
    return batch


def blind_score(vault: Vault, batch: str) -> dict:
    d = vault.root / "evals" / batch
    key = json.loads((d / ".key.json").read_text(encoding="utf-8"))
    with (d / "ratings.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    missing = [r["item"] for r in rows if not r["score_1_to_5"].strip()]
    if missing:
        raise VaultError(f"还有 {len(missing)} 篇没打分：{', '.join(missing)}")
    groups: dict[str, list[float]] = {"ai": [], "human": []}
    for r in rows:
        groups[key[r["item"]]["group"]].append(float(r["score_1_to_5"]))
    res = {
        "batch": batch,
        "ai_mean": round(statistics.mean(groups["ai"]), 2),
        "human_mean": round(statistics.mean(groups["human"]), 2),
        "n_ai": len(groups["ai"]), "n_human": len(groups["human"]),
    }
    res["ai_not_worse"] = res["ai_mean"] >= res["human_mean"]
    (d / "result.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    return res


# ================================================================ 合规审计
def _t(s: str | None) -> dt.datetime | None:
    try:
        t = dt.datetime.fromisoformat(s)
        return t if t.tzinfo else t.astimezone()
    except (TypeError, ValueError):
        return None


def audit(vault: Vault) -> dict:
    violations = []
    published = 0
    for v in vault.all_variants():
        vid = v["variant_id"]
        if v.get("compliance", {}).get("automated_interaction") != "none":
            violations.append({"variant": vid, "rule": "no_automated_interaction",
                               "detail": v.get("compliance", {}).get("automated_interaction")})
        if v["status"] != "published":
            continue
        published += 1
        pr = v.get("publish_result") or {}
        gr = v.get("gate_results") or {}
        if pr.get("channel") != "manual":
            violations.append({"variant": vid, "rule": "manual_publish_only", "detail": pr.get("channel")})
        if gr.get("human_approved_by") != "author" or not gr.get("approved_at"):
            violations.append({"variant": vid, "rule": "human_approval_before_publish", "detail": "缺少 H5 批准"})
        else:
            a, p = _t(gr["approved_at"]), _t(pr.get("published_at"))
            if a and p and p < a:
                violations.append({"variant": vid, "rule": "human_approval_before_publish",
                                   "detail": f"发布 {pr['published_at']} 早于批准 {gr['approved_at']}"})
        meta = vault.meta(v["hub_id"])
        missing = [g for g in ("H1", "H2", "H3", "H4", "H5") if g not in meta["gates"]]
        if missing:
            violations.append({"variant": vid, "rule": "all_gates_passed", "detail": missing})
    mcp_approvals = []
    for m in vault.hubs():
        for g, rec in m.get("gates", {}).items():
            if rec.get("channel") == "mcp":
                mcp_approvals.append({"hub": m["id"], "gate": g, "at": rec.get("at"),
                                      "user_statement": rec.get("user_statement")})
    stale = vault.stale_platform_rules()
    if stale:
        violations.append({"variant": None, "rule": "platform_rules_verified_90d", "detail": stale})
    return {"published_variants": published, "violations": violations, "ok": not violations,
            "mcp_approvals": mcp_approvals}
