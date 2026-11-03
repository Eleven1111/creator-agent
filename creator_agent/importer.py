"""P0：用 RSS 把往期文章导入 archive/（Substack 与 Medium 都提供公开 RSS）。"""

from __future__ import annotations

import html
import re

import feedparser

from .vault import Vault, slugify


def _strip_html(s: str) -> str:
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", s, flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>|</p>|</h\d>|</li>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\n{3,}", "\n\n", html.unescape(s)).strip()


def import_rss(vault: Vault, url: str) -> list[str]:
    feed = feedparser.parse(url)
    if feed.bozo and not feed.entries:
        raise RuntimeError(f"RSS 解析失败：{feed.bozo_exception}")
    written = []
    for e in feed.entries:
        body = ""
        if e.get("content"):
            body = e.content[0].get("value", "")
        body = body or e.get("summary", "")
        title = e.get("title", "untitled")
        date = (e.get("published") or e.get("updated") or "")[:16]
        name = f"{slugify(title, 50)}.md"
        text = f"# {title}\n\n来源：{e.get('link', '')}\n日期：{date}\n\n{_strip_html(body)}\n"
        (vault.root / "archive" / name).write_text(text, encoding="utf-8")
        written.append(name)
    return written
