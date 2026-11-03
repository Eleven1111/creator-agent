"""P4：读者调查的设计与分析（手册“素材”阶段：专有数据和一手信源是护城河）。

- design：生成问卷（questions.json + survey.md + 收集用的 CSV 表头），你在任意问卷工具里发出去。
- analyze：导入回答 CSV，选择题和量表题用确定性统计；开放题让模型归纳主题，
  每条引用都会逐字核对是否真的出现在回答里，对不上的直接丢掉。
- 结论一律写“我的读者中”，并附样本自选偏差的提醒（Orosz）。
"""

from __future__ import annotations

import csv
import json
import statistics
from collections import Counter
from pathlib import Path

from . import prompts as P
from .llm import LLM
from .vault import Vault, VaultError, now_iso, slugify


def _dir(vault: Vault, survey_id: str) -> Path:
    return vault.root / "surveys" / survey_id


def design(vault: Vault, llm: LLM, goal: str, topic: str = "", n: int = 10) -> str:
    profile = vault.profile()
    out = llm.json(stage="outline", system=P.SURVEY_SYSTEM, schema=P.SURVEY_SCHEMA,
                   user=P.SURVEY_USER.format(goal=goal, topic=topic or "未指定",
                                             persona=profile.get("persona", ""), n=n))
    survey_id = f"{now_iso()[:10]}-{slugify(goal, 20)}"
    d = _dir(vault, survey_id)
    d.mkdir(parents=True, exist_ok=True)
    for i, q in enumerate(out["questions"], 1):
        q["id"] = f"q{i:02d}"
    out["goal"], out["topic"], out["created_at"] = goal, topic, now_iso()
    (d / "questions.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [f"# {out['title']}", "", out["intro"], ""]
    for q in out["questions"]:
        lines.append(f"**{q['id']}. {q['text']}**（{q['type']}）")
        lines += [f"- {o}" for o in q["options"]]
        lines.append(f"  <!-- 为什么问：{q['why']} -->")
        lines.append("")
    lines += ["---", "## 偏差提醒"] + [f"- {b}" for b in out["bias_notes"]]
    lines += ["- 这是读者自选样本，不代表全体人群；写文章时只能说“我的读者中”。"]
    (d / "survey.md").write_text("\n".join(lines), encoding="utf-8")
    with (d / "responses_template.csv").open("w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow(["respondent_id"] + [q["id"] for q in out["questions"]])
    return survey_id


def analyze(vault: Vault, llm: LLM, survey_id: str, responses: Path) -> dict:
    d = _dir(vault, survey_id)
    if not (d / "questions.json").exists():
        raise VaultError(f"没有调查 {survey_id}")
    qs = json.loads((d / "questions.json").read_text(encoding="utf-8"))["questions"]
    with Path(responses).open(encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise VaultError("回答 CSV 是空的")
    n = len(rows)
    stats: dict[str, dict] = {}
    open_answers: dict[str, list[str]] = {}
    for q in qs:
        vals = [r.get(q["id"], "").strip() for r in rows if r.get(q["id"], "").strip()]
        s: dict = {"question": q["text"], "type": q["type"], "answered": len(vals)}
        if q["type"] in ("single", "multi"):
            c: Counter = Counter()
            for v in vals:
                for opt in (v.split(";") if q["type"] == "multi" else [v]):
                    c[opt.strip()] += 1
            s["counts"] = {k: {"n": cnt, "pct": round(cnt / len(vals), 3)} for k, cnt in c.most_common()}
        elif q["type"] in ("scale", "number"):
            nums = []
            for v in vals:
                try:
                    nums.append(float(v))
                except ValueError:
                    pass
            if nums:
                s.update({"mean": round(statistics.mean(nums), 2), "median": statistics.median(nums),
                          "min": min(nums), "max": max(nums)})
        else:
            open_answers[q["id"]] = vals
        stats[q["id"]] = s

    themes = []
    if open_answers:
        out = llm.json(stage="eval", system=P.SURVEY_ANALYZE_SYSTEM, schema=P.SURVEY_ANALYZE_SCHEMA,
                       user=json.dumps({qid: {"question": stats[qid]["question"], "answers": a}
                                        for qid, a in open_answers.items()}, ensure_ascii=False)[:120000])
        for t in out["themes"]:
            pool = open_answers.get(t["question_id"], [])
            verified = [q for q in t["quotes"] if any(q.strip() and q.strip() in a for a in pool)]
            t["dropped_quotes"] = len(t["quotes"]) - len(verified)
            t["quotes"] = verified
            themes.append(t)

    report = {"survey_id": survey_id, "n": n, "stats": stats, "themes": themes, "at": now_iso()}
    (d / "analysis.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [f"# 调查分析 · {survey_id}", "", f"回答数 n = {n}。以下都是“我的读者中”，读者自选样本，不代表全体。", ""]
    for qid, s in stats.items():
        lines.append(f"## {qid}. {s['question']}（{s['answered']}/{n} 作答）")
        if "counts" in s:
            lines += [f"- {k}：{v['n']}（{v['pct']:.0%}）" for k, v in s["counts"].items()]
        if "mean" in s:
            lines.append(f"- 均值 {s['mean']}，中位数 {s['median']}，范围 {s['min']}–{s['max']}")
        for t in [t for t in themes if t["question_id"] == qid]:
            lines.append(f"- 主题：{t['theme']}（约 {t['approx_count']} 条）")
            lines += [f"  - “{q}”" for q in t["quotes"]]
            if t["dropped_quotes"]:
                lines.append(f"  - （丢弃 {t['dropped_quotes']} 条在原回答里找不到的引用）")
        if n < 30:
            lines.append(f"- ⚠️ 样本只有 {n} 份，比例波动会很大")
        lines.append("")
    (d / "analysis.md").write_text("\n".join(lines), encoding="utf-8")
    return report
