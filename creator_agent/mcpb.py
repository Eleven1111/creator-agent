"""打包 Claude 桌面端扩展（.mcpb）。

采用 MCPB 规范 v0.4 的 `uv` 服务器类型：包里只放源码和 pyproject.toml，依赖由 Claude 桌面端用 uv 安装，
用户电脑上不需要预先装 Python。安装时 Claude 桌面端会根据 user_config 生成设置界面：
- 知识库文件夹（必填；不存在或为空时首次启动会自动创建）
- Anthropic API key（可选；留空则用“宿主模型模式”，由 Claude 桌面端里的 Claude 完成模型任务）
- X Bearer Token（可选；只用于读取已发布帖子的公开指标）

规范：https://github.com/modelcontextprotocol/mcpb/blob/main/MANIFEST.md
"""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

from . import __version__

ROOT = Path(__file__).resolve().parent.parent
INCLUDE = ["pyproject.toml", "LICENSE", "README.md", "README.zh-CN.md", "mcpb_server.py"]
EXCLUDE_PARTS = {"__pycache__", ".pytest_cache", ".venv"}


def manifest(tools: list[dict] | None = None) -> dict:
    m = {
        "manifest_version": "0.4",
        "name": "creator-agent",
        "display_name": "creator-agent 创作助理",
        "version": __version__,
        "description": "Research assistant and editor for Substack, X and Medium writers. Never publishes for you.",
        "long_description": (
            "选题、研究、提纲、编辑评审与事实核查、多平台改编、手动发布包、数据复盘。它是研究助理和编辑，不是代笔，"
            "也从不替你发布。每个阶段都要你亲口同意才往下走。\n\n"
            "不填 Anthropic API key 时使用“宿主模型模式”：需要模型的步骤由当前对话里的 Claude 完成。"
        ),
        "author": {"name": "Eleven1111", "url": "https://github.com/Eleven1111"},
        "repository": {"type": "git", "url": "https://github.com/Eleven1111/creator-agent"},
        "homepage": "https://github.com/Eleven1111/creator-agent",
        "documentation": "https://github.com/Eleven1111/creator-agent/blob/main/docs/integrations.md",
        "support": "https://github.com/Eleven1111/creator-agent/issues",
        "license": "MIT",
        "keywords": ["writing", "newsletter", "substack", "x", "medium", "editor", "research"],
        "server": {
            "type": "uv",
            "entry_point": "mcpb_server.py",
            "mcp_config": {
                "command": "uv",
                "args": ["run", "--directory", "${__dirname}", "--extra", "mcp", "mcpb_server.py",
                         "--vault", "${user_config.vault_dir}", "--init-if-missing"],
                "env": {
                    "ANTHROPIC_API_KEY": "${user_config.anthropic_api_key}",
                    "X_BEARER_TOKEN": "${user_config.x_bearer_token}",
                },
            },
        },
        "user_config": {
            "vault_dir": {
                "type": "directory",
                "title": "知识库文件夹",
                "description": "存放声音档案、选题、稿件和数据的文件夹。选一个空文件夹或新建一个，首次启动会自动初始化。",
                "required": True,
                "default": "${DOCUMENTS}/creator-vault",
            },
            "anthropic_api_key": {
                "type": "string",
                "title": "Anthropic API key（可选）",
                "description": "填了：研究、评审等由服务器调用 Anthropic API 完成（单独计费）。"
                               "留空：由当前对话里的 Claude 完成（宿主模型模式）。",
                "sensitive": True,
                "required": False,
            },
            "x_bearer_token": {
                "type": "string",
                "title": "X Bearer Token（可选）",
                "description": "只用于读取你已发布帖子的公开指标，按次计费。",
                "sensitive": True,
                "required": False,
            },
        },
        "compatibility": {
            "platforms": ["darwin", "win32", "linux"],
            "runtimes": {"python": ">=3.10"},
        },
        "privacy_policies": ["https://www.anthropic.com/legal/privacy"],
    }
    if tools:
        m["tools"] = tools
    return m


def tool_list() -> list[dict]:
    import asyncio

    from .mcp_server import build_server

    srv = build_server(lambda: None, lambda v: None)

    async def go():
        return await srv.list_tools()

    return [{"name": t.name, "description": (t.description or "").strip().splitlines()[0][:200]}
            for t in asyncio.run(go())]


def build(out_dir: Path | None = None) -> Path:
    out_dir = Path(out_dir or ROOT / "dist")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"creator-agent-{__version__}.mcpb"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("manifest.json", json.dumps(manifest(tool_list()), ensure_ascii=False, indent=2))
        for name in INCLUDE:
            p = ROOT / name
            if p.exists():
                z.write(p, name)
        for p in sorted((ROOT / "creator_agent").rglob("*")):
            if p.is_file() and not (EXCLUDE_PARTS & set(p.parts)) and p.suffix != ".pyc":
                z.write(p, p.relative_to(ROOT).as_posix())
    return out
