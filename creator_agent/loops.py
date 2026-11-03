"""P3：访谈模式（模式 I）、R1 短养长、R2 常青回收、P3 完成度。"""

from __future__ import annotations

import datetime as dt
import json
import re
import statistics

from . import prompts as P
from .adapt import _result, check_x_post, check_note, numbers_in
from .gates import check
from .llm import LLM
from .metrics import latest
from .vault import Vault, VaultError, now_iso


def _grams(s: str, n: int = 2) -> set[str]:
    s = re.sub(r"[^0-9a-z一-鿿]+", "", s.lower())
    return {s[i:i + n] for i in range(len(s) - n + 1)}


def jaccard(a: str, b: str, n: int = 4) -> float:
    ga, gb = _grams(a, n), _grams(b, n)
    return len(ga & gb) / len(ga | gb) if ga and gb else 0.0


# ================================================================ 访谈模式 I
def interview(vault: Vault, llm: LLM, hub_id: str, transcript: str) -> dict:
    """作者口述 → Agent 按提纲整理，只调整顺序和删冗，不添加内容；同时按 CRIBS 标注。"""
    meta = vault.meta(hub_id)
    check(meta, "draft")
    outline = vault.read_hub_file(hub_id, "outline.json", as_json=True)
    vault.write_hub_file(hub_id, "interview_transcript.md", transcript)
    out = llm.json(stage="draft", system=P.INTERVIEW_SYSTEM, schema=P.INTERVIEW_SCHEMA,
                   user=P.INTERVIEW_USER.format(outline=json.dumps(outline["sections"], ensure_ascii=False),
                                                transcript=transcript))
    draft = out["draft_markdown"]
    # 确定性检查：整理稿不得出现口述里没有的数字；和口述重合度很低的句子标为“可能新增”
    tgrams = _grams(transcript)
    suspicious = []
    for sent in re.split(r"(?<=[。！？!?\n])", draft):
        sg = _grams(sent)
        if len(sg) >= 6 and len(sg & tgrams) / len(sg) < 0.3 and not sent.strip().startswith("#"):
            suspicious.append(sent.strip())
    added_numbers = not numbers_in(draft, transcript)
    vault.write_hub_file(hub_id, "draft_agent.md", draft)
    vault.write_hub_file(hub_id, "draft.md", draft)
    lines = [f"# {hub_id} · 访谈整理（模式 I）", "", "## 听众反应（CRIBS）"]
    lines += [f"- {r['label']}：“{r['passage']}” {r['note']}" for r in out["reactions"]]
    lines += ["", "## 建议追问"] + [f"- {q}" for q in out["follow_up_questions"]]
    lines += ["", "## 整理稿检查"]
    lines += ["- ⚠️ 整理稿里出现了口述中没有的数字" if added_numbers else "- 数字都来自口述"]
    lines += [f"- ⚠️ 可能是新增内容（与口述重合度低）：{s}" for s in suspicious] or ["- 没有发现明显新增的句子"]
    lines += ["", f"整理稿已写入 hubs/{hub_id}/draft.md，你改完后运行 `ca review {hub_id}`。"]
    vault.write_hub_file(hub_id, "cribs.md", "\n".join(lines))
    meta["draft_mode"] = "I"
    meta["status"] = "drafting"
    vault.save_meta(hub_id, meta)
    return {"reactions": out["reactions"], "suspicious": suspicious, "added_numbers": added_numbers}


# ================================================================ R1 短养长
def promote(vault: Vault, variant_id: str) -> str:
    """把一条表现好的短帖晋升为长文选题，并建好母稿；S1 会把短帖和它的指标当作市场信号。"""
    v = vault.variant(variant_id)
    if v["format"] not in ("x_post", "substack_note"):
        raise VaultError("只有 X 单帖和 Notes 能晋升为长文选题")
    if v["status"] != "published":
        raise VaultError(f"{variant_id} 还没发布，没有表现数据")
    idea = vault.add_idea(v["body"]["text"], origin="own_post")
    hub_id = vault.new_hub(idea)
    meta = vault.meta(hub_id)
    meta["promoted_from"] = {"variant_id": variant_id, "text": v["body"]["text"],
                             "metrics": latest(vault, variant_id)}
    vault.save_meta(hub_id, meta)
    return hub_id


# ================================================================ R2 常青回收
def recycle(vault: Vault, llm: LLM, variant_id: str, n: int = 2, min_age_days: int = 90,
            force: bool = False, max_similarity: float = 0.5) -> list[dict]:
    v = vault.variant(variant_id)
    if v["format"] not in ("x_post", "substack_note"):
        raise VaultError("R2 目前只回收 X 单帖和 Notes")
    if v["status"] != "published":
        raise VaultError(f"{variant_id} 还没发布")
    at = dt.datetime.fromisoformat(v["publish_result"]["published_at"])
    at = at if at.tzinfo else at.astimezone()
    age = (dt.datetime.now().astimezone() - at).days
    if age < min_age_days and not force:
        raise VaultError(f"{variant_id} 才发布 {age} 天；常青回收要求 ≥{min_age_days} 天（--force 跳过）")
    hub_id = v["hub_id"]
    final = vault.read_hub_file(hub_id, "final.md")
    xrules = vault.platform("x")
    x_limit = int(xrules.get("max_weighted_chars", 280))
    out = llm.json(stage="adapt", system=P.RECYCLE_SYSTEM, schema=P.RECYCLE_SCHEMA,
                   user=P.RECYCLE_USER.format(fmt=v["format"], text=v["body"]["text"],
                                              metrics=json.dumps(latest(vault, variant_id), ensure_ascii=False),
                                              final=final, n=n, x_limit=x_limit))
    published_texts = [x["body"].get("text", "") for x in vault.variants_of(hub_id)
                       if x["status"] == "published" and x["format"] == v["format"]]
    made = []
    existing = len([x for x in vault.variants_of(hub_id) if x.get("derivation") == "recycle"])
    for i, r in enumerate(out["rewrites"], existing + 1):
        text = r["text"].strip()
        vid = f"v_{hub_id}_{v['format']}_r2_{i:02d}"
        flags = {k: r[k] for k in ("visualize", "falsify", "only_you", "reply_hook")}
        checks = check_x_post(text, final, xrules, flags) if v["format"] == "x_post" else check_note(text, final)
        sim = max((jaccard(text, t) for t in published_texts), default=0.0)
        checks["similarity_to_published"] = round(sim, 2)
        checks["not_light_edit"] = sim < max_similarity
        gate = _result("G-XP" if v["format"] == "x_post" else "G-SN", checks)
        nv = {**{k: v[k] for k in ("hub_id", "platform", "format", "language", "link_policy", "canonical",
                                  "compliance")},
              "variant_id": vid, "derivation": "recycle", "parent_variant": variant_id,
              "status": "gated" if gate["passed"] else "draft",
              "body": {"text": text, "idea": r["new_angle"], "llm_flags": flags},
              "editable_original": text, "packaging": {"new_angle": r["new_angle"]},
              "schedule": {"planned_at": (dt.datetime.now().astimezone() + dt.timedelta(days=i))
                           .replace(hour=9, minute=20, second=0, microsecond=0).isoformat(timespec="minutes")},
              "gate_results": gate, "publish_result": None, "created_at": now_iso()}
        vault.save_variant(nv)
        vault.write_variant_text(vid, text)
        made.append(nv)
    return made


# ================================================================ P3 完成度
def progress(vault: Vault) -> dict:
    """手册 P3 完成标准：论据支撑率 ≥95%；人工编辑时长比 P1 下降；至少 1 篇长文选题来自 R1。"""
    rates, minutes_by_month = [], {}
    r1_hubs = 0
    for m in vault.hubs():
        if m.get("promoted_from") or (m.get("idea_id") and _origin(vault, m["idea_id"]) == "own_post"):
            r1_hubs += 1
        p = vault.root / "hubs" / m["id"] / "review.json"
        if p.exists():
            r = json.loads(p.read_text(encoding="utf-8"))
            sr = (r.get("scores") or {}).get("support_rate")
            if sr is not None:
                rates.append(sr)
        mins = sum(e["minutes"] for e in m.get("edit_minutes", []))
        if mins:
            minutes_by_month.setdefault(m["created_at"][:7], []).append(mins)
    edit_trend = {k: round(statistics.mean(v), 1) for k, v in sorted(minutes_by_month.items())}
    months = list(edit_trend)
    return {
        "support_rate_mean": round(statistics.mean(rates), 3) if rates else None,
        "support_rate_ok": bool(rates) and statistics.mean(rates) >= 0.95,
        "edit_minutes_by_month": edit_trend,
        "edit_minutes_down": len(months) >= 2 and edit_trend[months[-1]] < edit_trend[months[0]],
        "r1_hubs": r1_hubs,
        "r1_ok": r1_hubs >= 1,
        "research_mode": vault.research_mode(),
    }


def _origin(vault: Vault, idea_id: str) -> str | None:
    try:
        return vault.idea(idea_id).get("origin")
    except VaultError:
        return None
