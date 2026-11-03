"""离线测试集（P1 完成标准：评审在测试集上能区分好稿和差稿）。

evals/testset.jsonl 每行：{"id": "...", "path": "evals/cases/xxx.md", "label": "good|bad"}
只跑 S5 里的反恭维评审（JUDGE），报告好稿/差稿平均分、阈值准确率和成对排序准确率。
"""

from __future__ import annotations

import json
import statistics

from . import prompts as P
from .llm import LLM
from .vault import Vault, VaultError


def run_eval(vault: Vault, llm: LLM) -> dict:
    path = vault.root / "evals/testset.jsonl"
    cases = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    if not cases:
        raise VaultError("evals/testset.jsonl 是空的；先放入作者认定的好稿和差稿（建议各 10 篇以上）")
    anchors = vault.anchors()
    anchor_texts = set(anchors["good"] + anchors["bad"])
    threshold = vault.review_threshold()
    results = []
    for c in cases:
        draft = (vault.root / c["path"]).read_text(encoding="utf-8")
        if draft in anchor_texts:
            raise VaultError(f"{c['id']} 同时是锚点稿；测试集和锚点必须分开，否则结果没有意义")
        j = llm.json(stage="eval", system=P.JUDGE_SYSTEM, schema=P.JUDGE_SCHEMA,
                     user=P.JUDGE_USER.format(bad="\n\n---\n\n".join(anchors["bad"]) or "（无）",
                                              good="\n\n---\n\n".join(anchors["good"]) or "（无）",
                                              draft=draft))
        results.append({"id": c["id"], "label": c["label"], "score": float(j["score"])})

    good = [r["score"] for r in results if r["label"] == "good"]
    bad = [r["score"] for r in results if r["label"] == "bad"]
    correct = sum(1 for r in results if (r["score"] >= threshold) == (r["label"] == "good"))
    pairs = [(g, b) for g in good for b in bad]
    auc = (sum(1.0 if g > b else 0.5 if g == b else 0.0 for g, b in pairs) / len(pairs)) if pairs else None
    summary = {
        "n": len(results),
        "threshold": threshold,
        "mean_good": round(statistics.mean(good), 3) if good else None,
        "mean_bad": round(statistics.mean(bad), 3) if bad else None,
        "accuracy_at_threshold": round(correct / len(results), 3),
        "pairwise_auc": round(auc, 3) if auc is not None else None,
        "discriminates": bool(auc is not None and auc >= 0.8),
        "results": results,
    }
    (vault.root / "evals/last_run.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary
