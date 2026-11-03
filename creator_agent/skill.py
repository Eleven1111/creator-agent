"""把 SKILL.md 技能包安装到各 agent 终端的技能目录。

目录依据（2026-11 检索，部分来自第三方文档，路径以各终端当前版本为准）：
- claude-code：~/.claude/skills/<name>/SKILL.md
- openclaw：  ~/.openclaw/skills/<name>/SKILL.md
- hermes：    ~/.hermes/skills/<name>/SKILL.md
- workbuddy： ~/.workbuddy/skills/<name>/SKILL.md
- agents：    ./.agents/skills/<name>/SKILL.md（项目级，供支持该约定的终端读取）
- zip：       在当前目录生成 creator-agent-skill.zip，用于 Claude 桌面端等需要上传技能包的界面
"""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

from .vault import VaultError

SKILL_SRC = Path(__file__).parent / "skill" / "creator-agent"
TARGETS = {
    "claude-code": Path("~/.claude/skills"),
    "openclaw": Path("~/.openclaw/skills"),
    "hermes": Path("~/.hermes/skills"),
    "workbuddy": Path("~/.workbuddy/skills"),
    "agents": Path(".agents/skills"),
}


def install_skill(target: str, directory: Path | None = None) -> list[Path]:
    if target == "zip":
        out = (directory or Path.cwd()) / "creator-agent-skill.zip"
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for f in SKILL_SRC.rglob("*"):
                if f.is_file():
                    z.write(f, Path("creator-agent") / f.relative_to(SKILL_SRC))
        return [out]
    if target == "dir":
        if directory is None:
            raise VaultError("target=dir 需要 --dir")
        base = directory
    else:
        base = TARGETS[target]
    dest = base.expanduser() / "creator-agent"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        # 只覆盖我们自己装过的技能包，避免误删用户同名目录
        existing = dest / "SKILL.md"
        if not existing.exists() or "name: creator-agent" not in existing.read_text(encoding="utf-8"):
            raise VaultError(f"{dest} 已存在且不是 creator-agent 技能包，没有覆盖；请先手动处理")
        shutil.rmtree(dest)
    shutil.copytree(SKILL_SRC, dest)
    return [dest / "SKILL.md"]
