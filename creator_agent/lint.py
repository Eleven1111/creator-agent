"""S5 里不需要模型的确定性检查（手册 S5 “行级 lint”“TK 拦截”“引言与删减”）。

原则（Eliason 2024）：lint 只标记，不自动改；deliberate_breaks.md 里登记的破格跳过。
"""

from __future__ import annotations

import re
import statistics
from dataclasses import dataclass, field

TK_RE = re.compile(r"\[TK[^\]]*\]|\bTK\b")
URL_RE = re.compile(r"https?://\S+")

# 通用 AI 腔词表（中英）。作者的 never.md 会在此基础上追加。
AI_TELLS = [
    "delve", "tapestry", "underscore", "testament to", "in today's fast-paced",
    "it's important to note", "it is worth noting", "navigate the complexities",
    "值得注意的是", "不难发现", "总而言之", "在当今", "深入探讨", "至关重要",
    "不可或缺", "赋能", "助力", "打造闭环", "全方位", "多维度",
]
HEDGES = ["我觉得", "我认为", "或许", "可能会", "某种程度上", "i think", "i believe",
          "perhaps", "sort of", "kind of"]
SUMMARY_ENDINGS = ["总之", "综上所述", "总而言之", "in summary", "in conclusion", "to sum up"]


@dataclass
class LintReport:
    blocking: list[dict] = field(default_factory=list)
    flags: list[dict] = field(default_factory=list)
    stats: dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.blocking

    def to_dict(self) -> dict:
        return {"ok": self.ok, "blocking": self.blocking, "flags": self.flags, "stats": self.stats}


def _paragraphs(text: str) -> list[str]:
    body = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return [p for p in body if not p.startswith("#")]  # 标题不算段落


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[。！？!?])|(?<=[.])\s+", text)
    return [s.strip() for s in parts if len(s.strip()) > 1]


def _count_units(text: str) -> int:
    """中文按字、英文按词计数。"""
    cjk = len(re.findall(r"[一-鿿]", text))
    words = len(re.findall(r"[A-Za-z0-9']+", text))
    return cjk + words


def lint_draft(text: str, never: list[str] | None = None,
               deliberate_breaks: list[str] | None = None) -> LintReport:
    rep = LintReport()
    never = never or []
    breaks = [b.lower() for b in (deliberate_breaks or [])]
    lower = text.lower()

    def skipped(term: str) -> bool:
        return term.lower() in breaks

    # 1) TK 硬拦截：未补的事实、经历、立场
    for m in TK_RE.finditer(text):
        rep.blocking.append({"check": "tk", "match": m.group(0),
                             "context": text[max(0, m.start() - 30): m.end() + 30]})

    # 2) 作者禁用词：硬拦截（作者自己定的规矩）
    for term in never:
        if term and not skipped(term) and term.lower() in lower:
            rep.blocking.append({"check": "never_list", "term": term})

    # 3) AI 腔与对冲词：只标记，按千字密度统计
    units = max(_count_units(text), 1)
    tells = [t for t in AI_TELLS if not skipped(t) and t in lower and t not in [n.lower() for n in never]]
    tell_hits = sum(lower.count(t) for t in tells)
    if tells:
        rep.flags.append({"check": "ai_tells", "terms": tells, "hits": tell_hits})
    hedge_hits = {h: lower.count(h) for h in HEDGES if h in lower and not skipped(h)}
    if hedge_hits:
        rep.flags.append({"check": "hedges", "terms": hedge_hits})
    excl = text.count("!") + text.count("！")
    if excl and not skipped("!"):
        rep.flags.append({"check": "exclamation", "count": excl})

    # 4) 结尾：不做总结段
    paras = _paragraphs(text)
    if paras:
        last = paras[-1].lower()
        for e in SUMMARY_ENDINGS:
            if last.startswith(e) or f"\n{e}" in last:
                rep.flags.append({"check": "summary_ending", "term": e})
                break

    # 5) 段落长度、引言占比、句长分布
    sents_per_para = [len(_sentences(p)) for p in paras]
    long_paras = [i + 1 for i, n in enumerate(sents_per_para) if n > 6]
    if long_paras:
        rep.flags.append({"check": "long_paragraphs", "paragraphs": long_paras})
    intro_ratio = (_count_units(paras[0]) / units) if paras else 0.0
    if intro_ratio > 0.15 and len(paras) > 3:
        rep.flags.append({"check": "intro_ratio", "ratio": round(intro_ratio, 2),
                          "note": "试试删掉首段，看是否立刻变强（Lenny）"})
    lens = [_count_units(s) for s in _sentences(text)]
    rep.stats = {
        "units": units,
        "paragraphs": len(paras),
        "intro_ratio": round(intro_ratio, 2),
        "ai_tells_per_1k": round(tell_hits * 1000 / units, 2),
        "sentence_len_median": statistics.median(lens) if lens else 0,
        "sentence_len_stdev": round(statistics.pstdev(lens), 1) if len(lens) > 1 else 0,
    }
    if rep.stats["ai_tells_per_1k"] > 3:
        rep.blocking.append({"check": "ai_tells_density", "per_1k": rep.stats["ai_tells_per_1k"],
                             "note": "AI 腔每千字超过 3 次"})
    return rep


# ---------------------------------------------------------------- X 字数
def _weight(ch: str) -> int:
    """twitter-text v3：这些区间按 1 计，其他（含 CJK、emoji）按 2 计。"""
    cp = ord(ch)
    if (0 <= cp <= 0x10FF or 0x2000 <= cp <= 0x200D or 0x2010 <= cp <= 0x201F
            or 0x2032 <= cp <= 0x2037):
        return 1
    return 2


def x_weighted_length(text: str) -> int:
    total, pos = 0, 0
    for m in URL_RE.finditer(text):
        total += sum(_weight(c) for c in text[pos:m.start()]) + 23  # t.co 固定 23
        pos = m.end()
    return total + sum(_weight(c) for c in text[pos:])
