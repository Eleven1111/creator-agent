"""UTM 生成器（手册“跨平台内容流”：每个变体都带 UTM，按平台、篇目、位置区分）。"""

from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def with_utm(url: str, *, source: str, medium: str, campaign: str, content: str) -> str:
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.update({
        "utm_source": source,
        "utm_medium": medium,
        "utm_campaign": campaign,
        "utm_content": content,
    })
    return urlunsplit(parts._replace(query=urlencode(query)))
