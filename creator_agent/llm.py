"""对 Anthropic Messages API 的薄封装。

设计要点（见手册第三部分“架构”）：
- 先用工作流，不上自主 Agent：每个阶段是一次或几次确定的调用。
- 结构化输出用 output_config.format（JSON Schema），不做字符串解析。
- 长输出一律走 streaming + get_final_message()，避免 HTTP 超时。
- 默认开启服务端 refusal fallback（fallbacks="default"），可在 agent.yaml 关闭。
- 每次调用的模型、token 用量写入 runs/logs/，供成本复盘。
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

FALLBACK_BETA = "server-side-fallback-2026-07-01"
WEB_SEARCH_TOOL = {"type": "web_search_20260209", "name": "web_search"}
WEB_FETCH_TOOL = {"type": "web_fetch_20260209", "name": "web_fetch"}
MAX_CONTINUATIONS = 5


class LLMError(RuntimeError):
    """模型拒答、被截断或返回了无法解析的内容。"""


@dataclass
class LLMConfig:
    model: str = "claude-opus-5-5"
    effort: dict[str, str] = field(default_factory=lambda: {
        "default": "high",
        "angles": "high",
        "research": "high",
        "outline": "high",
        "draft": "high",
        "review": "high",
        "adapt": "medium",
        "eval": "medium",
    })
    max_tokens: int = 32000
    use_fallbacks: bool = True
    web_search_max_uses: int = 8

    def effort_for(self, stage: str) -> str:
        return self.effort.get(stage, self.effort.get("default", "high"))


class LLM:
    def __init__(self, config: LLMConfig | None = None, client: Any = None,
                 log_dir: Path | None = None):
        self.config = config or LLMConfig()
        if client is None:
            import anthropic  # 延迟导入：测试时可注入假客户端

            client = anthropic.Anthropic()
        self.client = client
        self.log_dir = log_dir

    # ------------------------------------------------------------------ core
    def _request(self, *, stage: str, system: str, messages: list[dict],
                 tools: list[dict] | None = None,
                 output_format: dict | None = None) -> Any:
        output_config: dict[str, Any] = {"effort": self.config.effort_for(stage)}
        if output_format is not None:
            output_config["format"] = output_format
        params: dict[str, Any] = {
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "system": system,
            "messages": messages,
            "output_config": output_config,
        }
        if tools:
            params["tools"] = tools
        if self.config.use_fallbacks:
            params["betas"] = [FALLBACK_BETA]
            params["fallbacks"] = "default"

        started = time.time()
        with self.client.beta.messages.stream(**params) as stream:
            message = stream.get_final_message()

        # 服务端工具（web_search）可能在 10 轮后暂停：把助手内容原样回传即可续跑。
        continuations = 0
        while getattr(message, "stop_reason", None) == "pause_turn" and continuations < MAX_CONTINUATIONS:
            continuations += 1
            params["messages"] = messages + [{"role": "assistant", "content": message.content}]
            with self.client.beta.messages.stream(**params) as stream:
                message = stream.get_final_message()

        self._log(stage, message, time.time() - started)
        stop = getattr(message, "stop_reason", None)
        if stop == "refusal":
            details = getattr(message, "stop_details", None)
            raise LLMError(f"[{stage}] 模型拒答：{getattr(details, 'category', None)} "
                           f"{getattr(details, 'explanation', '')}")
        if stop == "max_tokens":
            raise LLMError(f"[{stage}] 输出被 max_tokens 截断，请调高 agent.yaml 里的 max_tokens")
        if stop == "pause_turn":
            raise LLMError(f"[{stage}] 服务端工具连续暂停 {MAX_CONTINUATIONS} 次仍未完成")
        return message

    @staticmethod
    def _text_of(message: Any) -> str:
        return "".join(b.text for b in message.content if getattr(b, "type", None) == "text")

    def _log(self, stage: str, message: Any, seconds: float) -> None:
        if self.log_dir is None:
            return
        self.log_dir.mkdir(parents=True, exist_ok=True)
        usage = getattr(message, "usage", None)
        row = {
            "t": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "stage": stage,
            "model": getattr(message, "model", self.config.model),
            "input_tokens": getattr(usage, "input_tokens", None),
            "output_tokens": getattr(usage, "output_tokens", None),
            "stop_reason": getattr(message, "stop_reason", None),
            "seconds": round(seconds, 1),
        }
        path = self.log_dir / f"{time.strftime('%Y%m%d')}.jsonl"
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # ------------------------------------------------------------ public API
    def json(self, *, stage: str, system: str, user: str, schema: dict) -> dict:
        """返回符合 schema 的 dict。schema 必须是 additionalProperties=false 的 object。"""
        message = self._request(
            stage=stage, system=system,
            messages=[{"role": "user", "content": user}],
            output_format={"type": "json_schema", "schema": schema},
        )
        text = self._text_of(message)
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise LLMError(f"[{stage}] 结构化输出无法解析：{e}；原文前 200 字：{text[:200]}") from e

    def text(self, *, stage: str, system: str, user: str, web_search: bool = False,
             web_fetch: bool = False, max_uses: int | None = None) -> str:
        tools = []
        if web_search:
            tools.append(dict(WEB_SEARCH_TOOL, max_uses=max_uses or self.config.web_search_max_uses))
        if web_fetch:
            # web_fetch 只能抓对话里已出现的 URL（搜索结果或提示词里给的链接），用来读全文而非摘要
            tools.append(dict(WEB_FETCH_TOOL, max_uses=max_uses or self.config.web_search_max_uses))
        tools = tools or None
        message = self._request(stage=stage, system=system,
                                messages=[{"role": "user", "content": user}], tools=tools)
        return self._text_of(message)
