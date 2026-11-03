"""S8 度量回流（只读）。

- X：用只读接口 GET https://api.x.com/2/tweets?ids=...&tweet.fields=public_metrics,created_at
  拉自己已发布帖子的公开指标（docs.x.com “Get Posts by IDs”）。需要环境变量 X_BEARER_TOKEN。
  不调用任何写入接口。按次计费：读自己的帖子在官方价目表里是 Owned Reads $0.001/条，
  用 app-only Bearer Token 读取时能否按 Owned Reads 计价未核实，这里按 $0.005/条保守估算。
- Substack / Medium：没有统计 API，用手工录入或 CSV 导入。
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path

from .vault import Vault, VaultError, now_iso

X_TWEETS_URL = "https://api.x.com/2/tweets"
X_STATUS_RE = re.compile(r"/status(?:es)?/(\d{1,19})")
X_READ_PRICE_CONSERVATIVE = 0.005


def _metrics_path(vault: Vault, variant_id: str) -> Path:
    return vault.root / "metrics" / f"{variant_id}.jsonl"


def _hours_since(published_at: str | None) -> str:
    if not published_at:
        return "unknown"
    try:
        t = dt.datetime.fromisoformat(published_at)
    except ValueError:
        return "unknown"
    if t.tzinfo is None:
        t = t.astimezone()
    h = (dt.datetime.now().astimezone() - t).total_seconds() / 3600
    return f"+{h:.0f}h"


def add_snapshot(vault: Vault, variant_id: str, values: dict, source: str) -> dict:
    v = vault.variant(variant_id)
    if v["status"] != "published":
        raise VaultError(f"{variant_id} 还没发布（{v['status']}），先 `ca published`")
    row = {"variant_id": variant_id, "at": now_iso(),
           "t": _hours_since((v.get("publish_result") or {}).get("published_at")),
           "source": source, **values}
    with _metrics_path(vault, variant_id).open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def snapshots(vault: Vault, variant_id: str) -> list[dict]:
    p = _metrics_path(vault, variant_id)
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def latest(vault: Vault, variant_id: str) -> dict:
    rows = snapshots(vault, variant_id)
    return rows[-1] if rows else {}


# ------------------------------------------------------------------ X（只读）
def x_post_id(url: str | None) -> str | None:
    m = X_STATUS_RE.search(url or "")
    return m.group(1) if m else None


def pull_x(vault: Vault, token: str | None = None, opener=None, dry_run: bool = False) -> dict:
    token = token or os.environ.get("X_BEARER_TOKEN")
    targets = {}
    for v in vault.all_variants():
        if v["platform"] == "x" and v["status"] == "published":
            pid = x_post_id((v.get("publish_result") or {}).get("url"))
            if pid:
                targets[pid] = v["variant_id"]
    est = round(len(targets) * X_READ_PRICE_CONSERVATIVE, 4)
    if dry_run or not targets:
        return {"posts": len(targets), "estimated_cost_usd": est, "written": 0}
    if not token:
        raise VaultError("需要环境变量 X_BEARER_TOKEN（只读）")
    opener = opener or urllib.request.urlopen
    ids = list(targets)
    written = 0
    for i in range(0, len(ids), 100):  # 每次最多 100 个 id
        q = urllib.parse.urlencode({"ids": ",".join(ids[i:i + 100]),
                                    "tweet.fields": "public_metrics,created_at"})
        req = urllib.request.Request(f"{X_TWEETS_URL}?{q}",
                                     headers={"Authorization": f"Bearer {token}"})
        with opener(req) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        for post in payload.get("data", []):
            pm = post.get("public_metrics") or {}
            add_snapshot(vault, targets[post["id"]], {
                "impressions": pm.get("impression_count"),
                "replies": pm.get("reply_count"),
                "reposts": pm.get("repost_count"),
                "quotes": pm.get("quote_count"),
                "likes": pm.get("like_count"),
                "bookmarks": pm.get("bookmark_count"),
            }, source="x_api_read")
            written += 1
        for err in payload.get("errors", []):
            print(f"X API：{err.get('detail') or err}")
    return {"posts": len(targets), "estimated_cost_usd": est, "written": written}


# ------------------------------------------------------------------ CSV 导入
def import_csv(vault: Vault, path: Path, source: str) -> int:
    """CSV 需要有 variant_id 列，或 url 列（与 ca published 记录的链接一致）；其余数值列都当指标。"""
    by_url = {(v.get("publish_result") or {}).get("url"): v["variant_id"]
              for v in vault.all_variants() if v["status"] == "published"}
    n = 0
    with Path(path).open(encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            vid = row.get("variant_id") or by_url.get(row.get("url"))
            if not vid:
                continue
            values = {}
            for k, val in row.items():
                if k in ("variant_id", "url") or val in (None, ""):
                    continue
                try:
                    values[k] = float(val) if "." in val else int(val)
                except ValueError:
                    values[k] = val
            add_snapshot(vault, vid, values, source=source)
            n += 1
    return n


# ------------------------------------------------------------------ 报表
def reply_rate(m: dict) -> float | None:
    imp = m.get("impressions")
    return (m.get("replies", 0) / imp) if imp else None


def channel_report(vault: Vault, month: str | None = None) -> dict:
    """按 平台×体裁 汇总最新快照；month 形如 2026-11，按发布时间过滤。"""
    groups: dict[str, dict] = {}
    for v in vault.all_variants():
        if v["status"] != "published":
            continue
        at = (v.get("publish_result") or {}).get("published_at") or ""
        if month and not at.startswith(month):
            continue
        key = f"{v['platform']}/{v['format']}"
        g = groups.setdefault(key, {"variants": 0, "with_metrics": 0, "totals": {}})
        g["variants"] += 1
        m = latest(vault, v["variant_id"])
        if not m:
            continue
        g["with_metrics"] += 1
        for k, val in m.items():
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                g["totals"][k] = g["totals"].get(k, 0) + val
    for g in groups.values():
        t = g["totals"]
        if t.get("impressions"):
            g["reply_rate"] = round(t.get("replies", 0) / t["impressions"], 4)
    return groups
