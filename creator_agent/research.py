"""P3：S2 升级为编排者-工作者（手册 S2；Anthropic 多 Agent 研究系统）。

- 主控把论点拆成子问题；每个子问题交给一个工作者，工作者自带 web_search + web_fetch，并行运行。
- 每个工作者的笔记单独做一次引用绑定，最后合并、按 URL+引语去重、重新编号。
- 只返回浓缩后的发现；原始笔记以文件形式保存在 hubs/<id>/research_workers/，用时再读。
- 是否启用由 agent.yaml 的 research.mode 决定（single | multi）。手册规则：只有离线测试证明单 Agent
  会漏掉关键信息，才值得付多 Agent 的 token 成本（Anthropic 报告约 15 倍于普通对话）。
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from . import prompts as P
from .llm import LLM
from .vault import Vault


def run_workers(vault: Vault, llm: LLM, hub_id: str, angle: dict, sub_questions: list[str],
                max_workers: int = 4, k: int = 10) -> tuple[dict, str]:
    out_dir = vault.hub_dir(hub_id) / "research_workers"
    out_dir.mkdir(exist_ok=True)

    def work(i_q):
        i, q = i_q
        notes = llm.text(stage="research", system=P.RESEARCH_SYSTEM, web_search=True, web_fetch=True,
                         max_uses=k, user=P.WORKER_USER.format(sub_question=q, thesis=angle["thesis"], k=k))
        (out_dir / f"worker_{i:02d}.md").write_text(f"# 子问题：{q}\n\n{notes}", encoding="utf-8")
        bound = llm.json(stage="research", system=P.BIND_SYSTEM, user=notes, schema=P.RESEARCH_SCHEMA)
        for f in bound["findings"]:
            f["sub_question"] = q
        return notes, bound

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        results = list(pool.map(work, enumerate(sub_questions, 1)))

    merged = {"findings": [], "counter_evidence": [], "human_todo": [], "not_found": []}
    seen = set()
    for _, b in results:
        for f in b["findings"]:
            key = (f["url"].rstrip("/"), f["quote_verbatim"].strip())
            if key in seen:
                continue
            seen.add(key)
            merged["findings"].append(f)
        for k_ in ("counter_evidence", "human_todo", "not_found"):
            for item in b[k_]:
                if item not in merged[k_]:
                    merged[k_].append(item)
    notes_all = "\n\n---\n\n".join(n for n, _ in results)
    return merged, notes_all
