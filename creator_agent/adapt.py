"""S6 平台适配层 + 平台闸口（G-XP / G-XT / G-XA / G-SN / G-MD）+ 发布包。

原则：
- 一份定稿母稿，多个原生变体；改写，不要转贴。
- 每个变体的可编辑正文单独存成 variants/<id>.md，作者可以直接改；H5 审批时用改后的文字重跑确定性检查。
- 所有发布都由作者本人完成。这里只生成稿子、检查结果和发布包，不调用任何平台写入接口。
"""

from __future__ import annotations

import datetime as dt
import json
import re

from . import prompts as P
from .gates import check
from .lint import URL_RE, x_weighted_length
from .llm import LLM
from .utm import with_utm
from .vault import Vault, VaultError

THREAD_SEP = "\n\n---\n\n"
ALL_FORMATS = ["x_post", "substack_note", "x_thread", "x_article", "medium_story"]
HASHTAG_RE = re.compile(r"(^|\s)#[^\s#]+")
MENTION_RE = re.compile(r"(^|\s)@\w+")
CASHTAG_RE = re.compile(r"\$[A-Za-z]{1,6}\b")
MEDIUM_META_RE = re.compile(r"\b(medium partner program|mpp|boost(ed)?|medium earnings)\b", re.I)


# ================================================================ 确定性检查
def numbers_in(variant_text: str, final: str) -> bool:
    """变体里的每个数字都必须出现在定稿里：改编不得新增事实。"""
    body = URL_RE.sub("", variant_text)
    return all(n in final for n in re.findall(r"\d+(?:[.,]\d+)?%?", body))


def _x_text_checks(text: str, final: str, xrules: dict, *, allow_link: bool = False) -> dict:
    limit = int(xrules.get("max_weighted_chars", 280))
    banned = [t.lower() for t in xrules.get("monetization_excluded_topics", [])]
    n = x_weighted_length(text)
    c = {
        "weighted_length": n,
        "within_limit": n <= limit,
        "no_hashtags": not HASHTAG_RE.search(text),
        "no_mentions": not MENTION_RE.search(text),
        "cashtags_ok": len(CASHTAG_RE.findall(text)) <= int(xrules.get("max_cashtags_per_post", 1)),
        "not_monetization_meta": not any(t in text.lower() for t in banned),
        "no_tk": "TK" not in text,
        "numbers_in_final": numbers_in(text, final),
    }
    if not allow_link:
        c["no_link"] = not URL_RE.search(text)
    return c


def check_x_post(text: str, final: str, xrules: dict, llm_flags: dict) -> dict:
    c = _x_text_checks(text, final, xrules)
    dry = sum(bool(llm_flags.get(k)) for k in ("visualize", "falsify", "only_you"))
    c.update({"dry_tests": f"{dry}/3", "dry_at_least_2": dry >= 2,
              "reply_hook": bool((llm_flags.get("reply_hook") or "").strip())})
    return c


def check_thread(parts: list[str], final: str, xrules: dict, llm_flags: dict) -> dict:
    c: dict = {"parts": len(parts), "has_parts": len(parts) >= 2,
               "first_post_standalone": bool(llm_flags.get("first_post_standalone"))}
    for i, p in enumerate(parts):
        last = i == len(parts) - 1
        for k, v in _x_text_checks(p, final, xrules, allow_link=last).items():
            if isinstance(v, bool):
                c[k] = c.get(k, True) and v
        c["max_weighted_length"] = max(c.get("max_weighted_length", 0), x_weighted_length(p))
    c["link_only_in_last"] = not any(URL_RE.search(p) for p in parts[:-1])
    return c


def check_article(title: str, body: str, final: str, llm_flags: dict, premium: bool) -> dict:
    opening = llm_flags.get("opening") or {}
    return {
        "has_title": bool(title.strip()),
        "opening_proof_promise_plan": all((opening.get(k) or "").strip() for k in ("proof", "promise", "plan")),
        "no_tk": "TK" not in body,
        "numbers_in_final": numbers_in(body, final),
        "author_has_premium": premium,
    }


def check_note(text: str, final: str) -> dict:
    return {
        "self_contained": len(text) > 20,
        "no_tk": "TK" not in text,
        "no_hashtags": not HASHTAG_RE.search(text),
        "numbers_in_final": numbers_in(text, final),
    }


def check_medium(pkg: dict, final_en: str, meta: dict, canonical: str | None) -> dict:
    ascii_ratio = sum(1 for ch in final_en if ord(ch) < 128) / max(len(final_en), 1)
    links = len(URL_RE.findall(final_en))
    return {
        "english": ascii_ratio > 0.9,
        "human_written_mode": meta.get("draft_mode") in ("A", "I"),
        "disclosure_ok": (not pkg.get("disclosure_required")) or bool(pkg.get("disclosure_in_first_two_paragraphs")),
        "context_packaging": bool(pkg.get("title")) and bool(pkg.get("subtitle")),
        "first_hand_experience": bool(pkg.get("first_hand_experience_present")),
        "not_derivative": not pkg.get("derivative_risk"),
        "cta_secondary": links <= 3,
        "not_about_medium": not MEDIUM_META_RE.search(final_en),
        "no_tk": "TK" not in final_en,
        "canonical_set": bool(canonical),
        "publications_chosen": len(pkg.get("target_publications") or []) >= 1,
    }


def _result(gate: str, checks: dict) -> dict:
    failed = [k for k, v in checks.items() if v is False]
    return {"gate": gate, "checks": checks, "failed": failed, "passed": not failed}


# ================================================================ 变体构造
def _variant(vid, hub_id, platform, fmt, meta, *, editable: str, body: dict, gate: dict,
             link_url, link_placement, ai_level, planned, packaging=None, derivation="atomize",
             parent=None) -> dict:
    return {
        "variant_id": vid,
        "hub_id": hub_id,
        "platform": platform,
        "format": fmt,
        "language": body.pop("language", meta.get("language", "zh")),
        "derivation": derivation,
        "parent_variant": parent,
        "status": "gated" if gate["passed"] else "draft",
        "body": body,
        "editable_original": editable,
        "packaging": packaging or {},
        "link_policy": {"placement": link_placement, "url": link_url},
        "canonical": {"url": meta.get("canonical_url"), "method": "n/a"},
        "compliance": {"ai_assist_level": ai_level, "automated_interaction": "none"},
        "schedule": {"planned_at": planned.isoformat(timespec="minutes")},
        "gate_results": gate,
        "publish_result": None,
    }


def _utm(canonical, source, medium, campaign, content):
    return with_utm(canonical, source=source, medium=medium, campaign=campaign,
                    content=content) if canonical else None


def s6_adapt(vault: Vault, llm: LLM, hub_id: str, *, n_x: int = 5, n_notes: int = 5,
             formats: list[str] | None = None, start: dt.datetime | None = None) -> list[dict]:
    meta = vault.meta(hub_id)
    check(meta, "adapt")
    final = vault.read_hub_file(hub_id, "final.md")
    profile = vault.profile()
    xrules = vault.platform("x")
    x_limit = int(xrules.get("max_weighted_chars", 280))
    formats = formats or profile.get("formats") or ALL_FORMATS
    canonical = meta.get("canonical_url")
    ai_level = "draft_B" if meta.get("draft_mode") == "B" else "edit_only"
    start = start or (dt.datetime.now().astimezone().replace(hour=9, minute=20, second=0, microsecond=0)
                      + dt.timedelta(days=1))
    deltas = json.dumps(profile.get("platform_deltas", {}), ensure_ascii=False)
    system = P.ADAPT_SYSTEM.format(deltas=deltas)
    variants: list[dict] = []
    skipped: dict[str, str] = {}

    # ---- X 单帖 + Notes + Substack 包装（一次调用）
    out = llm.json(stage="adapt", system=system, schema=P.ADAPT_SCHEMA,
                   user=P.ADAPT_USER.format(final=final, n_x=n_x if "x_post" in formats else 0,
                                            n_notes=n_notes if "substack_note" in formats else 0,
                                            x_limit=x_limit, x_cjk=x_limit // 2))
    if "x_post" in formats:
        for i, p in enumerate(out["x_posts"], 1):
            vid = f"v_{hub_id}_x_post_{i:02d}"
            text = p["text"].strip()
            flags = {k: p[k] for k in ("visualize", "falsify", "only_you", "reply_hook")}
            variants.append(_variant(
                vid, hub_id, "x", "x_post", meta, editable=text,
                body={"text": text, "idea": p["idea"], "llm_flags": flags},
                gate=_result("G-XP", check_x_post(text, final, xrules, flags)),
                link_url=_utm(canonical, "x", "self_reply", hub_id, vid), link_placement="self_reply_manual",
                ai_level=ai_level, planned=start + dt.timedelta(days=(i - 1) * 7 / max(n_x, 1))))
    if "substack_note" in formats:
        for i, n in enumerate(out["notes"], 1):
            vid = f"v_{hub_id}_substack_note_{i:02d}"
            text = n["text"].strip()
            variants.append(_variant(
                vid, hub_id, "substack_notes", "substack_note", meta, editable=text,
                body={"text": text, "note_type": n["type"]},
                gate=_result("G-SN", check_note(text, final)),
                link_url=_utm(canonical, "substack_notes", "post", hub_id, vid), link_placement="none",
                ai_level=ai_level, planned=start + dt.timedelta(days=i - 1, hours=4)))

    # ---- X Thread
    if "x_thread" in formats:
        t = llm.json(stage="adapt", system=system, schema=P.THREAD_SCHEMA,
                     user=P.THREAD_USER.format(final=final, min_parts=4, max_parts=10,
                                               x_limit=x_limit, x_cjk=x_limit // 2))
        vid = f"v_{hub_id}_x_thread_01"
        link = _utm(canonical, "x", "thread_end", hub_id, vid)
        parts = [p.strip() for p in t["parts"] if p.strip()]
        if parts and link:
            parts[-1] = f"{parts[-1]}\n\n{link}"
        flags = {"first_post_standalone": t["first_post_standalone"], "hook": t["hook"]}
        variants.append(_variant(
            vid, hub_id, "x", "x_thread", meta, editable=THREAD_SEP.join(parts),
            body={"parts": parts, "llm_flags": flags},
            gate=_result("G-XT", check_thread(parts, final, xrules, flags)),
            link_url=link, link_placement="thread_end", ai_level=ai_level,
            planned=start + dt.timedelta(days=2, hours=2)))

    # ---- X Article（+ 一条推广单帖）
    if "x_article" in formats:
        mode = "完整版" if (profile.get("x_article_mode") or "full") == "full" else "精简版，结尾链回母稿"
        a = llm.json(stage="adapt", system=system, schema=P.ARTICLE_SCHEMA,
                     user=P.ARTICLE_USER.format(final=final, mode=mode, x_limit=x_limit))
        vid = f"v_{hub_id}_x_article_01"
        premium = bool((profile.get("accounts") or {}).get("x_premium"))
        body_md = a["body_markdown"].strip()
        link = _utm(canonical, "x", "article_footer", hub_id, vid)
        variants.append(_variant(
            vid, hub_id, "x", "x_article", meta, editable=f"# {a['title']}\n\n{body_md}",
            body={"title": a["title"], "markdown": body_md, "llm_flags": {"opening": a["opening"]}},
            gate=_result("G-XA", check_article(a["title"], body_md, final, {"opening": a["opening"]}, premium)),
            link_url=link, link_placement="footer", ai_level=ai_level,
            planned=start + dt.timedelta(days=4, hours=2)))
        pid = f"v_{hub_id}_x_post_article_promo"
        promo = a["promo_post"].strip()
        pflags = {"visualize": True, "falsify": True, "only_you": True, "reply_hook": "推广帖"}
        variants.append(_variant(
            pid, hub_id, "x", "x_post", meta, editable=promo,
            body={"text": promo, "idea": "X Article 推广帖", "llm_flags": pflags},
            gate=_result("G-XP", _x_text_checks(promo, final, xrules)),
            link_url=None, link_placement="quote_article_manual", ai_level=ai_level,
            planned=start + dt.timedelta(days=4, hours=2, minutes=5), derivation="promote", parent=vid))

    # ---- Medium（仅英文人写版，仅 A / I 模式）
    if "medium_story" in formats:
        reason = _medium_ineligible(vault, hub_id, meta, profile)
        if reason:
            skipped["medium_story"] = reason
        else:
            final_en = vault.read_hub_file(hub_id, "final_en.md")
            m = llm.json(stage="adapt", system=system, schema=P.MEDIUM_SCHEMA,
                         user=P.MEDIUM_USER.format(final_en=final_en))
            vid = f"v_{hub_id}_medium_story_01"
            disclosure_required = meta.get("ai_assist_level") == "assisted_text"  # H4 时由作者声明
            pkg = {**m, "disclosure_required": disclosure_required,
                   "disclosure_in_first_two_paragraphs": _disclosure_in_head(final_en, profile)}
            en_canonical = meta.get("canonical_url_en") or canonical
            variants.append(_variant(
                vid, hub_id, "medium", "medium_story", meta, editable=final_en,
                body={"source_file": "final_en.md", "language": "en"},
                packaging=pkg,
                gate=_result("G-MD", check_medium(pkg, final_en, meta, en_canonical)),
                link_url=_utm(canonical, "medium", "story_cta", hub_id, vid), link_placement="story_cta",
                ai_level=ai_level, planned=start + dt.timedelta(days=3)))
            variants[-1]["canonical"] = {"url": en_canonical, "method": "medium_import"}

    for v in variants:
        vault.save_variant(v)
        vault.write_variant_text(v["variant_id"], v["editable_original"])
    _write_substack_package(vault, hub_id, meta, profile, final, out["substack"], canonical)
    _write_review_queue(vault, hub_id, variants, skipped)
    meta["status"] = "adapted"
    meta["skipped_formats"] = skipped
    vault.save_meta(hub_id, meta)
    return variants


def _medium_ineligible(vault: Vault, hub_id: str, meta: dict, profile: dict) -> str | None:
    langs = profile.get("languages") or {}
    if langs.get("medium", "none") == "none":
        return "profile.yaml 里 languages.medium 为 none"
    if meta.get("draft_mode") not in ("A", "I"):
        return "B 模式稿不发 Medium：AI 生成内容在 Medium 不进 General，也不能进付费墙"
    if meta.get("language") != "en" and not (vault.hub_dir(hub_id) / "final_en.md").exists():
        return ("母稿不是英文，且没有 final_en.md。Medium 非英文稿不进 General、不进 Boost；"
                "请你本人写英文版放到 hubs/<id>/final_en.md")
    if meta.get("language") == "en" and not (vault.hub_dir(hub_id) / "final_en.md").exists():
        vault.write_hub_file(hub_id, "final_en.md", vault.read_hub_file(hub_id, "final.md"))
    return None


def _disclosure_in_head(text: str, profile: dict) -> bool:
    line = (profile.get("medium_disclosure_line") or "").strip().lower()
    head = "\n\n".join([p for p in re.split(r"\n\s*\n", text) if p.strip() and not p.startswith("#")][:2]).lower()
    return bool(line) and line in head


# ================================================================ 审核与发布包
def revalidate(vault: Vault, v: dict) -> dict:
    """用作者改后的文字重跑确定性检查，返回更新后的变体。"""
    hub_id = v["hub_id"]
    meta = vault.meta(hub_id)
    final = vault.read_hub_file(hub_id, "final.md")
    xrules = vault.platform("x")
    text = vault.variant_text(v["variant_id"])
    if text is None:
        text = v["editable_original"]
    edited = text.strip() != v["editable_original"].strip()
    flags = v["body"].get("llm_flags", {})
    fmt = v["format"]
    if fmt == "x_post":
        v["body"]["text"] = text.strip()
        checks = (check_x_post(text, final, xrules, flags) if v["derivation"] != "promote"
                  else _x_text_checks(text, final, xrules))
        gate = "G-XP"
    elif fmt == "substack_note":
        v["body"]["text"] = text.strip()
        checks, gate = check_note(text, final), "G-SN"
    elif fmt == "x_thread":
        parts = [p.strip() for p in re.split(r"\n\s*---\s*\n", text) if p.strip()]
        v["body"]["parts"] = parts
        checks, gate = check_thread(parts, final, xrules, flags), "G-XT"
    elif fmt == "x_article":
        lines = text.strip().splitlines()
        title = lines[0].lstrip("# ").strip() if lines else ""
        body = "\n".join(lines[1:]).strip()
        v["body"].update({"title": title, "markdown": body})
        premium = bool((vault.profile().get("accounts") or {}).get("x_premium"))
        checks, gate = check_article(title, body, final, flags, premium), "G-XA"
    elif fmt == "medium_story":
        vault.write_hub_file(hub_id, "final_en.md", text)
        pkg = v["packaging"]
        pkg["disclosure_in_first_two_paragraphs"] = _disclosure_in_head(text, vault.profile())
        checks, gate = check_medium(pkg, text, meta, v["canonical"]["url"]), "G-MD"
    else:
        raise VaultError(f"未知格式 {fmt}")
    if v.get("derivation") == "recycle":
        from .loops import jaccard

        others = [x["body"].get("text", "") for x in vault.variants_of(hub_id)
                  if x["status"] == "published" and x["format"] == fmt]
        sim = max((jaccard(text, t) for t in others), default=0.0)
        checks["similarity_to_published"] = round(sim, 2)
        checks["not_light_edit"] = sim < 0.5
    if edited:
        checks["edited_by_author"] = "yes（LLM 打的三问/首帖分基于原稿，供参考）"
    prev = v.get("gate_results", {})
    v["gate_results"] = {**_result(gate, checks),
                         **{k: prev[k] for k in ("human_approved_by", "approved_at") if k in prev}}
    v["edited"] = edited
    return v


PLATFORM_STEPS = {
    "x_post": ["打开 X 客户端，粘贴正文（不要带链接）", "发布后 1–2 小时内在线，亲手回复评论",
               "如需导流：在自己这条帖子下手动回复带 UTM 的链接（不要用任何自动化）",
               "发布后执行 `ca published <id> <帖子链接>`"],
    "x_thread": ["在 X 客户端里逐条粘贴（以 --- 分隔），用“添加帖子”串成 Thread", "链接只在末帖",
                 "发布后 1–2 小时在线回复", "发布后执行 `ca published <id> <首帖链接>`"],
    "x_article": ["X 客户端 → Articles → 新建，粘贴标题与正文，检查排版和图片", "确认账号 Premium 有效",
                  "发布后再发对应的推广帖", "发布后执行 `ca published <id> <文章链接>`"],
    "substack_note": ["Substack → Notes 新建或定时，粘贴正文", "同一天不连发",
                      "亲手回复评论", "发布后执行 `ca published <id> <Note 链接>`"],
    "medium_story": ["母稿发布 1–7 天后：Medium → Stories → Import a story，填母稿 URL（自动回溯日期并设 canonical）",
                     "More settings → Advanced Settings 核对 “This story was originally published elsewhere” 指向母稿",
                     "填入包装里的标题、副标题；封面没有好图宁可不用", "投稿给目标出版物；发布时勾选通知订阅者",
                     "发布后执行 `ca published <id> <文章链接>`"],
}


def write_publish_kit(vault: Vault, hub_id: str) -> str:
    vs = [v for v in vault.variants_of(hub_id) if v["status"] == "approved"]
    vs.sort(key=lambda v: v["schedule"]["planned_at"])
    lines = [f"# 发布包 · {hub_id}", "",
             "全部由你本人在各平台客户端发布。本文件只是稿子和步骤，没有任何内容会被自动发出。", "",
             "Substack 母稿见 `substack_package.md`，请最先发。", ""]
    for v in vs:
        lines += [f"## {v['schedule']['planned_at']} · {v['format']} · `{v['variant_id']}`", ""]
        fmt = v["format"]
        if fmt in ("x_post", "substack_note"):
            lines += ["```text", v["body"]["text"], "```"]
        elif fmt == "x_thread":
            for i, p in enumerate(v["body"]["parts"], 1):
                lines += [f"**{i}/{len(v['body']['parts'])}**", "```text", p, "```"]
        elif fmt == "x_article":
            lines += [f"标题：**{v['body']['title']}**", "", "```markdown", v["body"]["markdown"], "```"]
        elif fmt == "medium_story":
            pk = v["packaging"]
            lines += [f"- 标题：{pk['title']}", f"- 副标题：{pk['subtitle']}", f"- 封面：{pk['cover_note']}",
                      f"- 目标出版物：{'、'.join(pk['target_publications'])}",
                      f"- 文末 CTA：{pk['cta']} → {v['link_policy']['url']}",
                      f"- canonical：{v['canonical']['url']}", "- 正文：`final_en.md`"]
        if v["link_policy"].get("url") and fmt != "medium_story":
            lines += ["", f"带 UTM 的链接（{v['link_policy']['placement']}）：{v['link_policy']['url']}"]
        steps = PLATFORM_STEPS[fmt]
        if v.get("derivation") == "promote":
            steps = ["在 X Article 发布后发这条，引用或附上文章卡片"] + steps[1:]
        lines += [""] + [f"- [ ] {s.replace('<id>', v['variant_id'])}" for s in steps] + [""]
    path = vault.write_hub_file(hub_id, "publish_kit.md", "\n".join(lines))
    return str(path)


def _write_review_queue(vault: Vault, hub_id: str, variants: list[dict], skipped: dict) -> None:
    lines = [f"# 待审稿件 · {hub_id}（H5）", "",
             "每个变体的正文在 `variants/<id>.md`，你可以直接改。改完运行 H5 审批时会用改后的文字重跑检查。", ""]
    for v in variants:
        g = v["gate_results"]
        mark = "✅" if g["passed"] else f"❌ {', '.join(g['failed'])}"
        lines += [f"## `{v['variant_id']}` · {v['format']} · {v['schedule']['planned_at']} · {mark}", "",
                  "```text", v["editable_original"][:3000], "```", ""]
    for fmt, why in skipped.items():
        lines += [f"## 跳过 {fmt}", why, ""]
    lines += ["---", f"全部放行（只放行通过检查的）：`ca approve {hub_id} H5 --variants all`",
              f"逐条放行：`ca approve {hub_id} H5 --variants v1,v2`"]
    vault.write_hub_file(hub_id, "review_queue.md", "\n".join(lines))


def _write_substack_package(vault, hub_id, meta, profile, final, s, canonical) -> None:
    footer = _utm(canonical, "substack", "email", hub_id, "footer") or "<母稿链接>"
    package = [f"# Substack 发布包 · {hub_id}", "",
               "## 标题候选（用原生 A/B 测试，看打开者点击率）"] + [f"- {t}" for t in s["title_variants"]]
    package += ["", f"## 副标题\n{s['subtitle']}", "", f"## 文末 CTA\n{s['cta']}",
                "", f"## AI 使用说明（建议放进 post template）\n{profile.get('disclosure_line', '')}",
                "", f"## 带 UTM 的分享链接\n{footer}", "",
                "## 发送前清单（G-SS）",
                "- [ ] 开头 3 段内有一句话答案或明确承诺",
                "- [ ] 引言不超过全文 15%",
                "- [ ] 免费部分本身完整；付费墙落在自然停顿处，或选用 freewall / metered paywall",
                "- [ ] 文中至少链接 1 篇最相关的旧文",
                "- [ ] 至少一张核心图表或一个核心数字",
                "- [ ] 结尾不是总结段",
                "- [ ] 是否发布“How I make this”声明、是否关闭本篇 AI 扫描：由你决定",
                "", "## 正文（粘贴到 Substack 编辑器）", "", final]
    vault.write_hub_file(hub_id, "substack_package.md", "\n".join(package))
