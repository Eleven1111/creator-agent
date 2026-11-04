"""宿主模型模式：不配 Anthropic API key，由 agent 终端里正在对话的模型（如 Claude 桌面端里的 Claude）完成模型任务。

工作方式（重放式，不需要改各阶段的代码）：
1. 阶段代码照常调用 llm.json(...) / llm.text(...)。
2. HostLLM 先查答案缓存；没有答案就把这次调用（系统指令、输入、输出格式）存成一个待办任务，抛出 HostTaskPending。
3. MCP 工具把任务交给宿主模型；宿主模型完成后调用 submit_model_output(task_id, output)。
4. 服务器校验输出（JSON 要符合 schema），存进缓存，然后从头重跑同一个工具。前面的调用命中缓存，
   流程推进到下一个待办任务，直到阶段跑完。

缓存键 = 调用内容的哈希 + 同一内容在本次运行里第几次出现。这样“同一提示词独立采样 3 次”（拔刺）仍是 3 个任务。

和 API 模式相比的两个差别（文档里会写明）：
- 评审不再是“干净语境”：宿主模型可能看过你们之前的对话。评审提示词会要求它只依据给定材料。
- 研究用的是宿主模型自己的联网工具；没有联网能力时必须如实说明，不得编造来源（S5 的引语回原网页比对是最后一道防线）。
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from .llm import LLMConfig, LLMError

PENDING_MARK = "【待你完成的模型任务】"


class HostTaskPending(Exception):
    def __init__(self, task: dict):
        super().__init__(task["task_id"])
        self.task = task


def validate(schema: dict, data: Any, path: str = "$") -> list[str]:
    """校验本项目用到的 JSON Schema 子集：object/array/string/integer/number/boolean/enum/required/additionalProperties。"""
    errs: list[str] = []
    t = schema.get("type")
    if "enum" in schema and data not in schema["enum"]:
        errs.append(f"{path}：必须是 {schema['enum']} 之一，实际是 {data!r}")
    if t == "object":
        if not isinstance(data, dict):
            return [f"{path}：应为对象"]
        props = schema.get("properties", {})
        for k in schema.get("required", []):
            if k not in data:
                errs.append(f"{path}.{k}：缺少必填字段")
        if schema.get("additionalProperties") is False:
            errs += [f"{path}.{k}：不允许的字段" for k in data if k not in props]
        for k, v in data.items():
            if k in props:
                errs += validate(props[k], v, f"{path}.{k}")
    elif t == "array":
        if not isinstance(data, list):
            return [f"{path}：应为数组"]
        for i, v in enumerate(data):
            errs += validate(schema.get("items", {}), v, f"{path}[{i}]")
    elif t == "string" and not isinstance(data, str):
        errs.append(f"{path}：应为字符串")
    elif t == "integer" and (not isinstance(data, int) or isinstance(data, bool)):
        errs.append(f"{path}：应为整数")
    elif t == "number" and (not isinstance(data, (int, float)) or isinstance(data, bool)):
        errs.append(f"{path}：应为数字")
    elif t == "boolean" and not isinstance(data, bool):
        errs.append(f"{path}：应为 true/false")
    return errs


class HostLLM:
    """与 LLM 相同的接口（json / text），但把调用交给宿主模型。"""

    backend = "host"

    def __init__(self, root: Path, config: LLMConfig | None = None):
        self.config = config or LLMConfig()
        self.tasks_dir = Path(root) / "runs" / "host_tasks"
        self.answers_dir = Path(root) / "runs" / "host_answers"
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.answers_dir.mkdir(parents=True, exist_ok=True)
        self._seen: Counter = Counter()

    def _key(self, payload: dict) -> str:
        base = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:20]
        self._seen[base] += 1
        return f"{base}-{self._seen[base]}"

    def _call(self, kind: str, stage: str, system: str, user: str, schema: dict | None = None,
              web: bool = False) -> Any:
        payload = {"kind": kind, "system": system, "user": user, "schema": schema, "web": web}
        key = self._key(payload)
        ans = self.answers_dir / f"{key}.json"
        if ans.exists():
            return json.loads(ans.read_text(encoding="utf-8"))["output"]
        task = {"task_id": key, "stage": stage, **payload}
        (self.tasks_dir / f"{key}.json").write_text(json.dumps(task, ensure_ascii=False, indent=2),
                                                    encoding="utf-8")
        raise HostTaskPending(task)

    def json(self, *, stage: str, system: str, user: str, schema: dict) -> dict:
        return self._call("json", stage, system, user, schema=schema)

    def text(self, *, stage: str, system: str, user: str, web_search: bool = False,
             web_fetch: bool = False, max_uses: int | None = None) -> str:
        return self._call("text", stage, system, user, web=web_search or web_fetch)

    # ------------------------------------------------------------------ 提交
    def task(self, task_id: str) -> dict:
        p = self.tasks_dir / f"{task_id}.json"
        if not p.exists():
            raise LLMError(f"没有待办任务 {task_id}；可能已经提交过，重新调用原工具即可")
        return json.loads(p.read_text(encoding="utf-8"))

    def submit(self, task_id: str, output: str) -> dict:
        task = self.task(task_id)
        if task["kind"] == "json":
            text = output.strip()
            m = re.match(r"^```[a-zA-Z]*\s*\n(.*?)\n?```\s*$", text, flags=re.S)
            if m:  # 宿主模型有时会把 JSON 包在代码块里
                text = m.group(1)
            try:
                value = json.loads(text)
            except json.JSONDecodeError as e:
                raise LLMError(f"输出不是合法 JSON：{e}。请只输出符合 schema 的 JSON，重新提交") from e
            errs = validate(task["schema"], value)
            if errs:
                raise LLMError("输出不符合 schema，请修正后重新提交：" + "；".join(errs[:12]))
        else:
            value = output
            if not value.strip():
                raise LLMError("输出为空，请重新提交")
        (self.answers_dir / f"{task_id}.json").write_text(
            json.dumps({"task_id": task_id, "output": value}, ensure_ascii=False), encoding="utf-8")
        (self.tasks_dir / f"{task_id}.json").unlink(missing_ok=True)
        return task


def render_task(task: dict, resume_tool: str) -> str:
    """把待办任务渲染成给宿主模型看的说明。"""
    lines = [
        f"{PENDING_MARK} task_id={task['task_id']}（阶段 {task['stage']}，接着会继续 {resume_tool}）",
        "",
        "creator-agent 运行在“宿主模型模式”：这一步需要你来完成。请严格按下面的【系统指令】处理【输入】，"
        "只依据给定材料，不要使用你在本对话里看到的其他信息，也不要迎合作者。",
    ]
    if task["web"]:
        lines.append("这一步需要联网：请用你可用的网页搜索/抓取工具查原始来源，引语从原文逐字摘录并附 URL。"
                     "如果你没有联网能力，就在输出里明确写“无法联网，未做检索”，绝不编造链接、引语或数字。")
    if task["kind"] == "json":
        lines += ["输出：**只输出一个 JSON**，必须符合下面的 JSON Schema（所有字段必填，不能有多余字段）。",
                  "```json", json.dumps(task["schema"], ensure_ascii=False), "```"]
    else:
        lines.append("输出：按系统指令要求的格式写纯文本或 markdown。")
    lines += ["", "【系统指令】", task["system"], "", "【输入】", task["user"], "",
              f"完成后调用 submit_model_output(task_id=\"{task['task_id']}\", output=<你的输出>)。"
              "提交后服务器会自动继续；如果又返回新的待办任务，照同样方式处理，直到拿到最终结果。"]
    return "\n".join(lines)
