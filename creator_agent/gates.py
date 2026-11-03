"""人工闸口 H1–H5（手册“七个人工闸口”；P1 用到其中五个）。

每个阶段运行前检查前置闸口；闸口只能由 `ca approve` 记录，记录里带批准时间和必填字段。
"""

from __future__ import annotations

from .vault import Vault, VaultError, now_iso

GATE_DESC = {
    "H1": "选定题目：作者亲手填兴奋度（1–5）并用一句话写下 edge",
    "H2": "确认研究简报：数字有一手来源、引语归属正确、列出反方证据",
    "H3": "批准论点与提纲",
    "H4": "定稿：逐条核对引语和数字，确认亲身经历属实，结尾由作者拍板",
    "H5": "批量审批各平台变体",
}

# 阶段 → 必须已通过的闸口
REQUIRES = {
    "research": ["H1"],
    "outline": ["H1", "H2"],
    "draft": ["H1", "H2", "H3"],
    "review": ["H1", "H2", "H3"],
    "adapt": ["H1", "H2", "H3", "H4"],
    "publish": ["H1", "H2", "H3", "H4", "H5"],
}


class GateError(VaultError):
    pass


def check(meta: dict, stage: str) -> None:
    missing = [g for g in REQUIRES.get(stage, []) if g not in meta.get("gates", {})]
    if missing:
        hints = "；".join(f"{g}（{GATE_DESC[g]}）" for g in missing)
        raise GateError(f"{meta['id']} 还没通过 {hints}。用 `ca approve {meta['id']} <闸口>` 记录批准。")


def approve(vault: Vault, hub_id: str, gate: str, **fields) -> dict:
    if gate not in GATE_DESC:
        raise GateError(f"未知闸口 {gate}；可选 {', '.join(GATE_DESC)}")
    meta = vault.meta(hub_id)
    prior = {"H1": [], "H2": ["H1"], "H3": ["H1", "H2"], "H4": ["H1", "H2", "H3"],
             "H5": ["H1", "H2", "H3", "H4"]}[gate]
    missing = [g for g in prior if g not in meta["gates"]]
    if missing:
        raise GateError(f"{gate} 之前还要先通过 {', '.join(missing)}")

    record = {"approved_by": "author", "at": now_iso()}
    if gate == "H1":
        angles = vault.read_hub_file(hub_id, "angles.json", as_json=True)["angles"]
        idx = fields.get("angle")
        if idx is None or not (1 <= idx <= len(angles)):
            raise GateError(f"H1 需要 --angle 1..{len(angles)}")
        exc = fields.get("excitement")
        if exc is None or not (1 <= exc <= 5):
            raise GateError("H1 需要 --excitement 1..5（作者本人的兴奋度，不能由 Agent 代填）")
        edge = (fields.get("edge") or "").strip()
        if len(edge) < 6:
            raise GateError("H1 需要 --edge：一句话写下你的 edge。写不出 edge 的题目退回选题池。")
        chosen = angles[idx - 1]
        record.update({"angle": idx, "excitement": exc, "edge": edge,
                       "score": score_angle(chosen, exc)})
        meta["chosen_angle"] = chosen
        meta["edge"] = edge
    elif gate == "H2":
        if not fields.get("confirm"):
            raise GateError("H2 需要 --confirm：表示你已按 research.md 末尾的清单检查过")
        record["notes"] = fields.get("notes")
    elif gate == "H3":
        vault.read_hub_file(hub_id, "outline.json", as_json=True)
    elif gate == "H4":
        review = vault.read_hub_file(hub_id, "review.json", as_json=True)
        draft = vault.read_hub_file(hub_id, "draft.md")
        if review.get("draft_sha") != _sha(draft):
            raise GateError("draft.md 在评审之后又改过；先重新运行 `ca review`")
        if not review["lint"]["ok"]:
            raise GateError("评审仍有硬拦截（TK、禁用词或 AI 腔密度），不能定稿")
        q, n = fields.get("quotes_checked"), fields.get("numbers_checked")
        if q is None or n is None:
            raise GateError("H4 需要 --quotes-checked N --numbers-checked N（你逐条回原链接核对过的数量）")
        claims = review.get("checkable_claims", [])
        need_q = sum(1 for c in claims if c.get("kind") == "quote")
        need_n = sum(1 for c in claims if c.get("kind") == "number")
        if q < need_q or n < need_n:
            raise GateError(f"评审提取了 {need_q} 条引语、{need_n} 个数字，核对数量不足")
        if not fields.get("ending_ok"):
            raise GateError("H4 需要 --ending-ok：结尾由作者本人拍板")
        record.update({"quotes_checked": q, "numbers_checked": n,
                       "judge_score": review["judge"]["score"], "passed_review": review["pass"]})
        if not review["pass"]:
            record["override"] = fields.get("override_reason") or ""
            if not record["override"]:
                raise GateError("评审未通过；如坚持定稿，用 --override-reason 写明理由")
        vault.write_hub_file(hub_id, "final.md", draft)
        if fields.get("canonical_url"):
            meta["canonical_url"] = fields["canonical_url"]
        if fields.get("canonical_url_en"):
            meta["canonical_url_en"] = fields["canonical_url_en"]
        level = fields.get("ai_assist_level") or ("draft_B" if meta.get("draft_mode") == "B" else "edit_only")
        if level not in ("none", "edit_only", "outline", "assisted_text", "draft_B"):
            raise GateError("--ai-assist-level 只能是 none|edit_only|outline|assisted_text|draft_B")
        meta["ai_assist_level"] = level
        agent_draft = vault.hub_dir(hub_id) / "draft_agent.md"
        if agent_draft.exists():  # 模式 B：记录 AI 稿 → 终稿的修改对
            rec = vault.save_edit_diff(hub_id, agent_draft.read_text(encoding="utf-8"), draft, "hub_draft_B")
            record["edit_ratio"] = rec["edit_ratio"]
        meta["status"] = "final"
    elif gate == "H5":
        from .adapt import revalidate, write_publish_kit

        ids = fields.get("variants") or []
        if not ids:
            raise GateError("H5 需要 --variants all 或逗号分隔的 variant_id")
        # 先用作者改后的文字重跑检查
        variants = {}
        for v in vault.variants_of(hub_id):
            if v["status"] in ("published", "retired"):
                continue
            v = revalidate(vault, v)
            vault.save_variant(v)
            variants[v["variant_id"]] = v
        all_mode = ids == ["all"]
        if all_mode:
            ids = [vid for vid, v in variants.items() if v["gate_results"]["passed"]]
        # 推广帖跟着母体走：母体（如 X Article）没获批就不能放行推广帖
        approved_now = set(ids) | {x["variant_id"] for x in vault.variants_of(hub_id)
                                   if x["status"] in ("approved", "published")}
        orphans = [vid for vid in ids if variants.get(vid, {}).get("parent_variant")
                   and variants[vid]["parent_variant"] not in approved_now]
        if orphans and not all_mode:
            raise GateError(f"{orphans} 是推广帖，它推广的变体还没获批")
        ids = [vid for vid in ids if vid not in orphans]
        failed_force = []
        for vid in ids:
            v = variants.get(vid)
            if v is None:
                raise GateError(f"{hub_id} 没有可审批的变体 {vid}")
            if not v["gate_results"]["passed"]:
                if not fields.get("force"):
                    raise GateError(f"{vid} 没通过平台闸口：{v['gate_results']['failed']}；"
                                    "改 variants/<id>.md 后重试，或用 --force")
                failed_force.append(vid)
        for vid in ids:
            v = variants[vid]
            v["status"] = "approved"
            v["gate_results"]["human_approved_by"] = "author"
            v["gate_results"]["approved_at"] = record["at"]
            if v.get("edited"):
                vault.save_edit_diff(vid, v["editable_original"], vault.variant_text(vid) or "",
                                     f"variant_{v['format']}")
            vault.save_variant(v)
        prev = (meta["gates"].get("H5") or {}).get("variants", [])
        record["variants"] = sorted(set(prev) | set(ids))
        if failed_force:
            record["forced"] = failed_force
        record["publish_kit"] = write_publish_kit(vault, hub_id)

    meta["gates"][gate] = record
    vault.save_meta(hub_id, meta)
    return record


# 手册 S1 排序表：兴奋度 0.30、edge 0.20、视角契合 0.15、市场信号 0.15、人类证据 0.15、时效 0.05
def score_angle(angle: dict, excitement: int | None, edge_strength: int | None = None) -> float:
    e = (excitement or 0) / 5
    edge = (edge_strength if edge_strength is not None else angle.get("edge_strength", 0)) / 3
    s = (0.30 * e + 0.20 * edge
         + 0.15 * angle.get("lens_fit", 0) / 3
         + 0.15 * angle.get("market_signal", 0) / 3
         + 0.15 * angle.get("evidence_availability", 0) / 3
         + 0.05 * angle.get("timeliness", 0) / 3)
    return round(s, 3)


def _sha(text: str) -> str:
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
