"""P4：语音访谈的“语音 → 转写”一步，在本地完成，不上传音频。

可选依赖 faster-whisper（pip install faster-whisper）；没装时提示你用任意外部工具转写成文字稿，
再用 `ca interview <id> --transcript 文字稿.md` 继续。
"""

from __future__ import annotations

from pathlib import Path

from .vault import VaultError


def transcribe(audio: Path, model_size: str = "small", language: str | None = "zh") -> str:
    try:
        from faster_whisper import WhisperModel
    except ImportError as e:
        raise VaultError("本地转写需要 faster-whisper：pip install faster-whisper；"
                         "或者先用其他工具转成文字稿，再用 --transcript") from e
    if not Path(audio).exists():
        raise VaultError(f"找不到音频文件 {audio}")
    model = WhisperModel(model_size, device="auto", compute_type="auto")
    segments, _info = model.transcribe(str(audio), language=language, vad_filter=True)
    lines = []
    for seg in segments:
        text = seg.text.strip()
        if text:
            lines.append(f"[{int(seg.start // 60):02d}:{seg.start % 60:04.1f}] {text}")
    if not lines:
        raise VaultError("转写结果为空，请检查音频")
    return "\n".join(lines)
