"""P3：风格漂移闸口（手册 S5“声音”组：句长分布、功能词频，与档案的距离，超出往期均值 2σ 视为漂移）。

基线来自 archive/（RSS 导入的往期文章）和 voice/exemplars/。纯统计，不调用模型。
"""

from __future__ import annotations

import re
import statistics

ZH_FUNCTION = ["的", "了", "是", "我", "你", "就", "也", "但", "而", "很", "都", "在", "这", "那", "吧", "呢"]
EN_FUNCTION = ["the", "and", "but", "i", "you", "it", "is", "that", "of", "to", "so", "just"]
PUNCT = {"comma": "，,", "period": "。.", "question": "？?", "exclaim": "！!", "colon": "：:", "dash": "—"}


def _sentences(text: str) -> list[str]:
    return [s for s in re.split(r"(?<=[。！？!?])|(?<=\.)\s+|\n+", text) if len(s.strip()) > 1]


def _units(text: str) -> int:
    return len(re.findall(r"[一-鿿]", text)) + len(re.findall(r"[A-Za-z0-9']+", text))


def features(text: str) -> dict[str, float]:
    text = re.sub(r"\[[^\]]*\]|https?://\S+|^#.*$", "", text, flags=re.M)
    units = max(_units(text), 1)
    sents = _sentences(text)
    lens = [_units(s) for s in sents] or [0]
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    f = {
        "sent_len_mean": statistics.mean(lens),
        "sent_len_stdev": statistics.pstdev(lens) if len(lens) > 1 else 0.0,
        "para_len_mean": statistics.mean([_units(p) for p in paras]) if paras else 0.0,
        "question_ratio": sum(1 for s in sents if s.strip().endswith(("？", "?"))) / max(len(sents), 1),
    }
    lower = text.lower()
    words = re.findall(r"[a-z']+", lower)
    for w in ZH_FUNCTION:
        f[f"zh_{w}"] = lower.count(w) * 1000 / units
    for w in EN_FUNCTION:
        f[f"en_{w}"] = words.count(w) * 1000 / units
    for name, chars in PUNCT.items():
        f[f"p_{name}"] = sum(lower.count(c) for c in chars) * 1000 / units
    return f


def baseline(docs: list[str]) -> dict[str, tuple[float, float]]:
    feats = [features(d) for d in docs if _units(d) > 200]
    if not feats:
        return {}
    out = {}
    for k in feats[0]:
        vals = [f[k] for f in feats]
        out[k] = (statistics.mean(vals), statistics.pstdev(vals) if len(vals) > 1 else 0.0)
    out["_n"] = (float(len(feats)), 0.0)
    return out


def drift(text: str, base: dict[str, tuple[float, float]], sigma: float = 2.0) -> dict:
    if not base:
        return {"checked": False, "reason": "没有足够长的往期文章做基线"}
    f = features(text)
    z = {}
    for k, (mu, sd) in base.items():
        if k == "_n" or (abs(mu) < 1e-6 and abs(f.get(k, 0)) < 1e-6):
            continue
        # 往期风格很一致时 sd≈0，会把任何微小差异放大成“漂移”；给标准差一个下限（均值的 15%，且 ≥0.5）
        sd_eff = max(sd, 0.15 * abs(mu), 0.5)
        z[k] = round((f[k] - mu) / sd_eff, 2)
    outliers = {k: v for k, v in z.items() if abs(v) > sigma}
    core = {k: v for k, v in outliers.items() if k.startswith(("sent_len", "para_len"))}
    mean_abs = round(statistics.mean(abs(v) for v in z.values()), 2) if z else 0.0
    return {
        "checked": True,
        "baseline_docs": int(base["_n"][0]),
        "mean_abs_z": mean_abs,
        "outliers": dict(sorted(outliers.items(), key=lambda kv: -abs(kv[1]))[:10]),
        # 句长或段长偏离 >2σ，或整体平均偏离 >1σ，算漂移
        "drifted": bool(core) or mean_abs > sigma / 2,
    }
