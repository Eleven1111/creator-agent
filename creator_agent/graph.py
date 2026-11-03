"""P4：用 LangGraph 把流水线编成一张图，人工闸口是 interrupt()，状态由 SQLite checkpointer 持久化。

- 图会无限期停在闸口，直到你用 `ca flow resume` 给出 Command(resume=...)。
- 闸口的规则和 `ca approve` 完全一样（都调用 gates.approve），文件仍是唯一的事实来源：
  如果某个闸口已经用 `ca approve` 批过，图会直接跳过它。
- 闸口输入不合法时不会让图报错，而是带着错误信息回到同一个闸口重新等待。
- 图只到 H5（生成发布包）为止。发布永远由你本人在客户端完成；H7 月度复盘不属于单篇母稿，仍用 `ca retro-approve`。

需要可选依赖：pip install -e '.[graph]'
"""

from __future__ import annotations

import json
import sqlite3
from typing import Any, TypedDict

from . import gates, stages
from .gates import GateError
from .llm import LLM
from .vault import Vault


class FlowState(TypedDict, total=False):
    hub_id: str
    error: str | None
    route: str | None


HUMAN_STEPS = {
    "H1": ("angles.md", "选一个角度，填兴奋度和 edge",
           {"action": "approve", "angle": 1, "excitement": 4, "edge": "..."}, ["redo"]),
    "H2": ("research.md", "按清单检查研究简报", {"action": "approve", "confirm": True}, ["redo"]),
    "H3": ("outline.md", "批准论点与提纲", {"action": "approve"}, ["redo"]),
    "DRAFT": ("cards.md / draft.md", "在 draft.md 写好（或改好）正文后继续", {"action": "done"}, []),
    "H4": ("review.md", "逐条核对引语和数字，结尾由你拍板",
           {"action": "approve", "quotes_checked": 0, "numbers_checked": 0, "ending_ok": True,
            "canonical_url": "https://..."}, ["revise"]),
    "H5": ("review_queue.md", "审稿（可直接改 variants/<id>.md），放行要发的变体",
           {"action": "approve", "variants": ["all"]}, ["redo"]),
}

INT_FIELDS = {"angle", "excitement", "quotes_checked", "numbers_checked"}


def _human(vault: Vault, gate: str):
    file, ask, example, alts = HUMAN_STEPS[gate]

    def node(state: FlowState) -> dict:
        from langgraph.types import interrupt

        hub = state["hub_id"]
        if gate != "DRAFT" and gate in vault.meta(hub)["gates"]:
            return {"error": None, "route": "next"}  # 已经用 ca approve 批过
        answer = interrupt({"hub_id": hub, "gate": gate, "review": f"hubs/{hub}/{file}", "ask": ask,
                            "example_resume": example, "other_actions": alts, "error": state.get("error")})
        # resume 值以 JSON 字符串传递：LangGraph 会把 dict 形式的 resume 当作“中断 id → 值”的映射
        answer = json.loads(answer) if isinstance(answer, str) else dict(answer or {})
        action = answer.pop("action", "approve")
        if action in ("redo", "revise"):
            return {"error": None, "route": action}
        if gate == "DRAFT":
            return {"error": None, "route": "next"}
        try:
            gates.approve(vault, hub, gate, **answer)
        except GateError as e:
            return {"error": str(e), "route": "retry"}
        return {"error": None, "route": "next"}

    return node


def build_graph(vault: Vault, llm: LLM, checkpointer=None):
    from langgraph.graph import END, START, StateGraph

    def stage(fn, **kw):
        def node(state: FlowState) -> dict:
            fn(vault, llm, state["hub_id"], **kw)
            return {"error": None, "route": None}
        return node

    g = StateGraph(FlowState)
    g.add_node("s1", stage(stages.s1_angles))
    g.add_node("s2", stage(stages.s2_research))
    g.add_node("s3", stage(stages.s3_outline))
    g.add_node("s4", stage(stages.s4_draft))
    g.add_node("s5", stage(stages.s5_review))
    g.add_node("s6", stage(stages.s6_adapt))
    for h in HUMAN_STEPS:
        g.add_node(h, _human(vault, h))

    g.add_edge(START, "s1")
    g.add_edge("s1", "H1")
    g.add_edge("s2", "H2")
    g.add_edge("s3", "H3")
    g.add_edge("s4", "DRAFT")
    g.add_edge("DRAFT", "s5")
    g.add_edge("s5", "H4")
    g.add_edge("s6", "H5")

    def router(nxt: str, redo: str | None = None, retry: str | None = None):
        def r(state: FlowState) -> str:
            route = state.get("route")
            if route == "retry":
                return retry
            if route in ("redo", "revise") and redo:
                return redo
            return nxt
        return r

    g.add_conditional_edges("H1", router("s2", redo="s1", retry="H1"), ["s2", "s1", "H1"])
    g.add_conditional_edges("H2", router("s3", redo="s2", retry="H2"), ["s3", "s2", "H2"])
    g.add_conditional_edges("H3", router("s4", redo="s3", retry="H3"), ["s4", "s3", "H3"])
    g.add_conditional_edges("H4", router("s6", redo="DRAFT", retry="H4"), ["s6", "DRAFT", "H4"])
    g.add_conditional_edges("H5", router(END, redo="s6", retry="H5"), [END, "s6", "H5"])
    return g.compile(checkpointer=checkpointer)


def checkpointer(vault: Vault):
    from langgraph.checkpoint.sqlite import SqliteSaver

    path = vault.root / "runs" / "flow.sqlite"
    return SqliteSaver(sqlite3.connect(str(path), check_same_thread=False))


def _cfg(hub_id: str) -> dict:
    return {"configurable": {"thread_id": hub_id}}


def pending(app, hub_id: str) -> dict | None:
    st = app.get_state(_cfg(hub_id))
    for t in st.tasks:
        for i in t.interrupts:
            return i.value
    return None


def start(vault: Vault, llm: LLM, hub_id: str, app=None) -> dict | None:
    app = app or build_graph(vault, llm, checkpointer(vault))
    if app.get_state(_cfg(hub_id)).next:
        raise GateError(f"{hub_id} 的流程已经在运行；用 `ca flow status {hub_id}` 查看")
    app.invoke({"hub_id": hub_id}, _cfg(hub_id))
    return pending(app, hub_id)


def resume(vault: Vault, llm: LLM, hub_id: str, answer: dict[str, Any], app=None) -> dict | None:
    from langgraph.types import Command

    app = app or build_graph(vault, llm, checkpointer(vault))
    if not app.get_state(_cfg(hub_id)).next:
        raise GateError(f"{hub_id} 没有在等待的闸口（流程未开始或已结束）")
    app.invoke(Command(resume=json.dumps(answer, ensure_ascii=False)), _cfg(hub_id))
    return pending(app, hub_id)


def status(vault: Vault, llm: LLM, hub_id: str, app=None) -> dict:
    app = app or build_graph(vault, llm, checkpointer(vault))
    st = app.get_state(_cfg(hub_id))
    return {"next": list(st.next), "waiting": pending(app, hub_id), "done": not st.next and bool(st.values)}


def parse_answer(pairs: list[str], action: str | None) -> dict:
    out: dict[str, Any] = {}
    if action:
        out["action"] = action
    for kv in pairs:
        k, _, v = kv.partition("=")
        k = k.replace("-", "_")
        if k in INT_FIELDS:
            out[k] = int(v)
        elif v.lower() in ("true", "false"):
            out[k] = v.lower() == "true"
        elif k == "variants":
            out[k] = v.split(",")
        else:
            out[k] = v
    return out
