"""P3：SAFE 式逐条核查（手册 S5“事实”组）。

1. 把稿子拆成原子事实（引语 / 数字 / 事实），带上它引用的来源标记 [fNN]。
2. 对每条有来源的事实，让模型只根据来源摘录判断：supported / partial / unsupported，以及归属是否正确。
3. 引语再回原网页逐字核对一次（只读 GET；页面打不开不算失败，只提示你在 H4 人工核）。

SAFE 与人工标注的一致率约 72%（待核实），所以它只做初筛，H4 的人工核对不能省。
"""

from __future__ import annotations

import html
import json
import re
import urllib.request

from . import prompts as P
from .llm import LLM

UA = "Mozilla/5.0 (compatible; creator-agent-factcheck/0.1)"


def _norm(s: str) -> str:
    s = html.unescape(s).lower()
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"[^0-9a-z一-鿿]+", "", s)


def fetch_text(url: str, timeout: int = 15) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read(2_000_000).decode("utf-8", errors="ignore")
    raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    return re.sub(r"<[^>]+>", " ", raw)


def quote_on_page(quote: str, page: str) -> bool:
    q = _norm(quote)
    return bool(q) and q in _norm(page)


def factcheck(llm: LLM, draft: str, findings: list[dict], *, refetch: bool = True,
              fetcher=fetch_text) -> dict:
    by_id = {f["id"]: f for f in findings}
    facts = llm.json(stage="review", system=P.ATOMIZE_SYSTEM, user=draft, schema=P.ATOMIZE_SCHEMA)["facts"]

    sourced = [(i, f) for i, f in enumerate(facts) if f["source_id"] in by_id]
    verdicts = {}
    if sourced:
        payload = [{"index": i, "fact": f["fact"], "attributed_to": f["speaker"],
                    "source_excerpt": by_id[f["source_id"]]["quote_verbatim"],
                    "source_speaker": by_id[f["source_id"]]["speaker"],
                    "source_attribution": by_id[f["source_id"]]["attribution"]} for i, f in sourced]
        out = llm.json(stage="review", system=P.ENTAIL_SYSTEM, schema=P.ENTAIL_SCHEMA,
                       user=json.dumps(payload, ensure_ascii=False))
        verdicts = {v["index"]: v for v in out["verdicts"]}

    page_cache: dict[str, str | None] = {}
    rows = []
    for i, f in enumerate(facts):
        src = by_id.get(f["source_id"])
        row = {"fact": f["fact"], "sentence": f["sentence"], "kind": f["kind"], "source_id": f["source_id"]}
        if not src:
            row.update({"verdict": "unsourced", "attribution_ok": None})
        else:
            v = verdicts.get(i, {"verdict": "unsupported", "attribution_ok": False, "reason": "核查员未返回"})
            row.update({"verdict": v["verdict"], "attribution_ok": v["attribution_ok"], "reason": v.get("reason", ""),
                        "weak_source": bool(src.get("weak"))})
            if refetch and f["kind"] == "quote":
                url = src["url"]
                if url not in page_cache:
                    try:
                        page_cache[url] = fetcher(url)
                    except Exception as e:  # noqa: BLE001 —— 网络错误只提示
                        page_cache[url] = None
                        row["refetch_error"] = type(e).__name__
                page = page_cache[url]
                row["quote_on_page"] = None if page is None else quote_on_page(src["quote_verbatim"], page)
        rows.append(row)

    total = len(rows)
    supported = sum(1 for r in rows if r["verdict"] == "supported")
    hard = [r for r in rows if r["kind"] in ("quote", "number")]
    hard_ok = sum(1 for r in hard if r["verdict"] == "supported" and r["attribution_ok"] is not False
                  and r.get("quote_on_page") is not False and not r.get("weak_source"))
    return {
        "facts": rows,
        "support_rate": round(supported / total, 3) if total else 1.0,
        "hard_support_rate": round(hard_ok / len(hard), 3) if hard else 1.0,
        "blocking": [r for r in hard if not (r["verdict"] == "supported" and r["attribution_ok"] is not False
                                             and r.get("quote_on_page") is not False
                                             and not r.get("weak_source"))],
        "unreachable_pages": [u for u, p in page_cache.items() if p is None],
    }
