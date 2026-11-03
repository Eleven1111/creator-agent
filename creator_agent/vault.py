"""知识库（creator-vault）的读写。纯文件：markdown / yaml / json / jsonl。"""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any

import yaml

from . import templates
from .llm import LLMConfig

LAYOUT = {
    "agent.yaml": templates.AGENT_YAML,
    "voice/profile.yaml": templates.PROFILE_YAML,
    "voice/never.md": templates.NEVER_MD,
    "voice/deliberate_breaks.md": templates.DELIBERATE_BREAKS_MD,
    "voice/stances.md": templates.STANCES_MD,
    "voice/stories.md": templates.STORIES_MD,
    "platforms/substack.yaml": templates.PLATFORM_SUBSTACK,
    "platforms/x.yaml": templates.PLATFORM_X,
    "platforms/medium.yaml": templates.PLATFORM_MEDIUM,
    "backlog/ideas.jsonl": templates.IDEAS_JSONL,
    "evals/README.md": templates.TESTSET_README,
    "evals/testset.jsonl": "",
}
DIRS = ["voice/exemplars", "voice/edit_diffs", "swipe", "sources", "hubs", "variants",
        "archive", "metrics/exports", "runs/logs", "evals/anchors", "evals/cases"]


class VaultError(RuntimeError):
    pass


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="minutes")


def slugify(text: str, max_len: int = 40) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w一-鿿]+", "-", text)
    return text.strip("-")[:max_len] or "untitled"


class Vault:
    def __init__(self, root: Path):
        self.root = Path(root)

    # ------------------------------------------------------------- setup
    @classmethod
    def init(cls, root: Path) -> "Vault":
        root = Path(root)
        for d in DIRS:
            (root / d).mkdir(parents=True, exist_ok=True)
        for rel, content in LAYOUT.items():
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            if not p.exists():
                p.write_text(content, encoding="utf-8")
        return cls(root)

    def require(self) -> None:
        if not (self.root / "agent.yaml").exists():
            raise VaultError(f"{self.root} 不是知识库目录；先运行 `ca init {self.root}`")

    # ------------------------------------------------------------- config
    def _yaml(self, rel: str) -> dict:
        p = self.root / rel
        if not p.exists():
            return {}
        return yaml.safe_load(p.read_text(encoding="utf-8")) or {}

    def llm_config(self) -> LLMConfig:
        raw = self._yaml("agent.yaml")
        cfg = LLMConfig()
        cfg.model = raw.get("model", cfg.model)
        cfg.max_tokens = int(raw.get("max_tokens", cfg.max_tokens))
        cfg.use_fallbacks = bool(raw.get("use_fallbacks", cfg.use_fallbacks))
        cfg.web_search_max_uses = int(raw.get("web_search_max_uses", cfg.web_search_max_uses))
        cfg.effort.update(raw.get("effort") or {})
        return cfg

    def research_mode(self) -> str:
        return str((self._yaml("agent.yaml").get("research") or {}).get("mode", "single"))

    def p3_settings(self) -> dict:
        raw = self._yaml("agent.yaml")
        review = raw.get("review") or {}
        return {
            "factcheck": bool(review.get("factcheck", True)),
            "refetch_quotes": bool(review.get("refetch_quotes", True)),
            "briars_samples": int(review.get("briars_samples", 3)),
            "style_drift_sigma": float(review.get("style_drift_sigma", 2.0)),
            "style_min_docs": int(review.get("style_min_docs", 5)),
        }

    def review_threshold(self) -> float:
        return float((self._yaml("agent.yaml").get("review") or {}).get("pass_threshold", 0.6))

    def profile(self) -> dict:
        return self._yaml("voice/profile.yaml")

    def platform(self, name: str) -> dict:
        return self._yaml(f"platforms/{name}.yaml")

    def text(self, rel: str) -> str:
        p = self.root / rel
        return p.read_text(encoding="utf-8") if p.exists() else ""

    def list_items(self, rel: str) -> list[str]:
        """读取 markdown 里以 '- ' 开头的条目。"""
        return [line[2:].strip() for line in self.text(rel).splitlines()
                if line.startswith("- ") and line[2:].strip()]

    def exemplars(self, limit: int = 8) -> str:
        files = sorted((self.root / "voice/exemplars").glob("*.md"))[:limit]
        return "\n\n---\n\n".join(f.read_text(encoding="utf-8") for f in files)

    def style_corpus(self) -> list[str]:
        files = sorted((self.root / "archive").glob("*.md")) + sorted((self.root / "voice/exemplars").glob("*.md"))
        return [f.read_text(encoding="utf-8") for f in files]

    def anchors(self) -> dict[str, list[str]]:
        d = self.root / "evals/anchors"
        return {
            "good": [f.read_text(encoding="utf-8") for f in sorted(d.glob("good_*.md"))],
            "bad": [f.read_text(encoding="utf-8") for f in sorted(d.glob("bad_*.md"))],
        }

    def stale_platform_rules(self, max_age_days: int = 90) -> list[str]:
        stale = []
        for p in sorted((self.root / "platforms").glob("*.yaml")):
            raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
            v = raw.get("verified_at")
            try:
                age = (dt.date.today() - dt.date.fromisoformat(str(v))).days
            except ValueError:
                stale.append(f"{p.name}（verified_at 缺失）")
                continue
            if age > max_age_days:
                stale.append(f"{p.name}（{age} 天前核对）")
        return stale

    # ------------------------------------------------------------- backlog
    def add_idea(self, raw: str, origin: str = "memo", edge: str | None = None) -> dict:
        ideas = self.ideas()
        idea = {
            "id": f"idea_{len(ideas) + 1:04d}",
            "created": dt.date.today().isoformat(),
            "origin": origin,
            "raw": raw,
            "edge": edge,
            "excitement": None,
            "status": "candidate",
        }
        with (self.root / "backlog/ideas.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(idea, ensure_ascii=False) + "\n")
        return idea

    def ideas(self) -> list[dict]:
        p = self.root / "backlog/ideas.jsonl"
        if not p.exists():
            return []
        return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]

    def idea(self, idea_id: str) -> dict:
        for i in self.ideas():
            if i["id"] == idea_id:
                return i
        raise VaultError(f"选题池里没有 {idea_id}")

    # ------------------------------------------------------------- archive
    def archive_hits(self, query: str, k: int = 5) -> list[dict]:
        """往期文章的朴素检索：中文用字符二元组，英文用词，按重叠度排序。"""
        def grams(s: str) -> set[str]:
            s = s.lower()
            words = set(re.findall(r"[a-z0-9]{3,}", s))
            cjk = re.sub(r"[^一-鿿]", "", s)
            return words | {cjk[i:i + 2] for i in range(len(cjk) - 1)}

        q = grams(query)
        if not q:
            return []
        scored = []
        for f in (self.root / "archive").glob("*.md"):
            body = f.read_text(encoding="utf-8")
            g = grams(body[:4000])
            score = len(q & g) / len(q)
            if score > 0:
                title = body.splitlines()[0].lstrip("# ").strip() if body else f.stem
                scored.append({"file": f.name, "title": title, "score": round(score, 2)})
        return sorted(scored, key=lambda x: -x["score"])[:k]

    # ------------------------------------------------------------- hubs
    def hub_dir(self, hub_id: str) -> Path:
        d = self.root / "hubs" / hub_id
        if not d.exists():
            raise VaultError(f"没有母稿 {hub_id}；用 `ca hubs` 查看")
        return d

    def new_hub(self, idea: dict) -> str:
        today = dt.date.today()
        year, week, _ = today.isocalendar()
        # 只用 ASCII：hub_id 会进 UTM 的 campaign/content，中文会被编码成长串
        tag = (idea.get("id") or "hub").replace("_", "")
        base = f"{year}w{week:02d}-{tag}"
        hub_id, n = base, 2
        while (self.root / "hubs" / hub_id).exists():
            hub_id, n = f"{base}-{n}", n + 1
        d = self.root / "hubs" / hub_id
        d.mkdir(parents=True)
        profile = self.profile()
        meta = {
            "id": hub_id,
            "idea_id": idea.get("id"),
            "idea": idea["raw"],
            "language": (profile.get("languages") or {}).get("hub", "zh"),
            "draft_mode": profile.get("default_draft_mode", "A"),
            "canonical_url": None,
            "status": "created",
            "gates": {},
            "edit_minutes": [],
            "created_at": now_iso(),
        }
        self.save_meta(hub_id, meta)
        return hub_id

    def meta(self, hub_id: str) -> dict:
        return json.loads((self.hub_dir(hub_id) / "meta.json").read_text(encoding="utf-8"))

    def save_meta(self, hub_id: str, meta: dict) -> None:
        p = self.root / "hubs" / hub_id / "meta.json"
        p.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    def hubs(self) -> list[dict]:
        out = []
        for d in sorted((self.root / "hubs").iterdir()) if (self.root / "hubs").exists() else []:
            if (d / "meta.json").exists():
                out.append(json.loads((d / "meta.json").read_text(encoding="utf-8")))
        return out

    def write_hub_file(self, hub_id: str, name: str, content: Any) -> Path:
        p = self.hub_dir(hub_id) / name
        if isinstance(content, (dict, list)):
            content = json.dumps(content, ensure_ascii=False, indent=2)
        p.write_text(content, encoding="utf-8")
        return p

    def read_hub_file(self, hub_id: str, name: str, as_json: bool = False) -> Any:
        p = self.hub_dir(hub_id) / name
        if not p.exists():
            raise VaultError(f"{hub_id} 缺少 {name}")
        text = p.read_text(encoding="utf-8")
        return json.loads(text) if as_json else text

    # ------------------------------------------------------------- variants
    def save_variant(self, variant: dict) -> Path:
        p = self.root / "variants" / f"{variant['variant_id']}.yaml"
        p.write_text(yaml.safe_dump(variant, allow_unicode=True, sort_keys=False), encoding="utf-8")
        return p

    def write_variant_text(self, variant_id: str, text: str) -> Path:
        p = self.root / "variants" / f"{variant_id}.md"
        p.write_text(text, encoding="utf-8")
        return p

    def variant_text(self, variant_id: str) -> str | None:
        p = self.root / "variants" / f"{variant_id}.md"
        return p.read_text(encoding="utf-8") if p.exists() else None

    def all_variants(self) -> list[dict]:
        out = []
        for p in sorted((self.root / "variants").glob("*.yaml")):
            v = yaml.safe_load(p.read_text(encoding="utf-8"))
            if v:
                out.append(v)
        return out

    # ------------------------------------------------------------- edit diffs
    def save_edit_diff(self, key: str, before: str, after: str, kind: str) -> dict:
        """AI 稿 → 终稿的修改对（手册 voice/edit_diffs/）。编辑距离比是最便宜的质量信号。"""
        import difflib

        ratio = 1 - difflib.SequenceMatcher(None, before, after).ratio()
        diff = "".join(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
                                            fromfile="agent", tofile="author", n=1))
        rec = {"key": key, "kind": kind, "edit_ratio": round(ratio, 3), "at": now_iso(),
               "before": before, "after": after, "diff": diff}
        p = self.root / "voice/edit_diffs" / f"{key}.json"
        p.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
        return rec

    def edit_diffs(self) -> list[dict]:
        d = self.root / "voice/edit_diffs"
        return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(d.glob("*.json"))]

    def variant(self, variant_id: str) -> dict:
        p = self.root / "variants" / f"{variant_id}.yaml"
        if not p.exists():
            raise VaultError(f"没有变体 {variant_id}")
        return yaml.safe_load(p.read_text(encoding="utf-8"))

    def variants_of(self, hub_id: str) -> list[dict]:
        out = []
        for p in sorted((self.root / "variants").glob("*.yaml")):
            v = yaml.safe_load(p.read_text(encoding="utf-8"))
            if v and v.get("hub_id") == hub_id:
                out.append(v)
        return out
