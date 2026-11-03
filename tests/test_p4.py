import csv
import importlib.util
import sys
import types

import pytest

needs_graph = pytest.mark.skipif(importlib.util.find_spec("langgraph") is None,
                                 reason="需要 pip install -e '.[graph]'")

from creator_agent import gates, graph, stages
from creator_agent.audit import audit, blind_prepare, blind_score
from creator_agent.cli import main
from creator_agent.llm import LLM
from creator_agent.survey import analyze, design
from creator_agent.vault import Vault, VaultError

from fakes import FakeClient, _no_network
from test_pipeline import GOOD_DRAFT, run_to_final


@pytest.fixture
def vault(tmp_path):
    v = Vault.init(tmp_path / "vault")
    _no_network(v)
    return v


@pytest.fixture
def llm(vault):
    return LLM(vault.llm_config(), client=FakeClient())


def fresh_app(vault, llm):
    """每次都新建 app 和 checkpointer，模拟“关掉终端、明天再继续”。"""
    return graph.build_graph(vault, llm, graph.checkpointer(vault))


# ------------------------------------------------------------------ LangGraph 流程
@needs_graph
def test_flow_end_to_end_with_persistence(vault, llm):
    hub = vault.new_hub(vault.add_idea("小团队要不要做用户访谈？"))
    w = graph.start(vault, llm, hub, app=fresh_app(vault, llm))
    assert w["gate"] == "H1" and w["review"].endswith("angles.md")

    # 闸口输入不合法：不报错，带着错误回到同一个闸口
    w = graph.resume(vault, llm, hub, {"action": "approve", "angle": 1}, app=fresh_app(vault, llm))
    assert w["gate"] == "H1" and "excitement" in w["error"]

    w = graph.resume(vault, llm, hub, {"angle": 1, "excitement": 4, "edge": "大家默认访谈按项目做"},
                     app=fresh_app(vault, llm))
    assert w["gate"] == "H2"
    w = graph.resume(vault, llm, hub, {"confirm": True}, app=fresh_app(vault, llm))
    assert w["gate"] == "H3"
    w = graph.resume(vault, llm, hub, {}, app=fresh_app(vault, llm))
    assert w["gate"] == "DRAFT"
    # 没写正文就继续 → 评审被 TK 拦下 → H4 拒绝 → 选择 revise 回到 DRAFT
    w = graph.resume(vault, llm, hub, {"action": "done"}, app=fresh_app(vault, llm))
    assert w["gate"] == "H4"
    w = graph.resume(vault, llm, hub, {"quotes_checked": 1, "numbers_checked": 0, "ending_ok": True},
                     app=fresh_app(vault, llm))
    assert w["gate"] == "H4" and w["error"]
    w = graph.resume(vault, llm, hub, {"action": "revise"}, app=fresh_app(vault, llm))
    assert w["gate"] == "DRAFT"
    (vault.hub_dir(hub) / "draft.md").write_text(GOOD_DRAFT, encoding="utf-8")
    w = graph.resume(vault, llm, hub, {"action": "done"}, app=fresh_app(vault, llm))
    assert w["gate"] == "H4"
    w = graph.resume(vault, llm, hub, {"quotes_checked": 1, "numbers_checked": 0, "ending_ok": True,
                                       "canonical_url": "https://me.substack.com/p/w"}, app=fresh_app(vault, llm))
    assert w["gate"] == "H5"
    assert (vault.hub_dir(hub) / "review_queue.md").exists()
    w = graph.resume(vault, llm, hub, {"variants": ["all"]}, app=fresh_app(vault, llm))
    assert w is None
    assert (vault.hub_dir(hub) / "publish_kit.md").exists()
    assert set(vault.meta(hub)["gates"]) == {"H1", "H2", "H3", "H4", "H5"}
    assert graph.status(vault, llm, hub, app=fresh_app(vault, llm))["done"]
    # 流程结束后不会有任何变体被标为已发布
    assert not any(v["status"] == "published" for v in vault.variants_of(hub))


@needs_graph
def test_flow_skips_gates_already_approved_by_cli(vault, llm):
    hub = vault.new_hub(vault.add_idea("一个题"))
    stages.s1_angles(vault, llm, hub)
    gates.approve(vault, hub, "H1", angle=1, excitement=3, edge="一个足够长的 edge")
    w = graph.start(vault, llm, hub, app=fresh_app(vault, llm))
    assert w["gate"] == "H2"  # s1 重跑了，但 H1 已经批过，直接跳过


@needs_graph
def test_flow_redo(vault, llm):
    hub = vault.new_hub(vault.add_idea("一个题"))
    graph.start(vault, llm, hub, app=fresh_app(vault, llm))
    w = graph.resume(vault, llm, hub, {"action": "redo"}, app=fresh_app(vault, llm))
    assert w["gate"] == "H1"


@needs_graph
def test_flow_cli(vault, llm, monkeypatch, capsys):
    import creator_agent.cli as cli

    monkeypatch.setattr(cli, "_llm", lambda v: llm)
    root = str(vault.root)
    assert main(["--vault", root, "flow", "start", "小团队要不要做用户访谈？"]) == 0
    out = capsys.readouterr().out
    assert "停在 H1" in out and "ca flow resume" in out
    hub = out.split()[0]
    assert main(["--vault", root, "flow", "resume", hub, "--set", "angle=1", "excitement=4",
                 "edge=大家默认访谈按项目做"]) == 0
    assert "停在 H2" in capsys.readouterr().out
    assert main(["--vault", root, "flow", "status", hub]) == 0
    assert "H2" in capsys.readouterr().out


def test_parse_answer():
    a = graph.parse_answer(["angle=2", "ending_ok=true", "variants=a,b", "edge=x=y"], "approve")
    assert a == {"action": "approve", "angle": 2, "ending_ok": True, "variants": ["a", "b"], "edge": "x=y"}


# ------------------------------------------------------------------ 语音转写
def test_interview_audio_uses_local_whisper(vault, llm, monkeypatch, tmp_path, capsys):
    import creator_agent.cli as cli

    seg = types.SimpleNamespace
    fake = types.ModuleType("faster_whisper")

    class WhisperModel:
        def __init__(self, size, device, compute_type):
            self.size = size

        def transcribe(self, path, language, vad_filter):
            return iter([seg(start=0.0, text="我每周二下午打三个电话。"), seg(start=3.2, text=" ")]), None

    fake.WhisperModel = WhisperModel
    monkeypatch.setitem(sys.modules, "faster_whisper", fake)
    monkeypatch.setattr(cli, "_llm", lambda v: llm)
    hub = vault.new_hub(vault.add_idea("一个题"))
    stages.s1_angles(vault, llm, hub)
    gates.approve(vault, hub, "H1", angle=1, excitement=3, edge="一个足够长的 edge")
    stages.s2_research(vault, llm, hub)
    gates.approve(vault, hub, "H2", confirm=True)
    stages.s3_outline(vault, llm, hub)
    gates.approve(vault, hub, "H3")
    audio = tmp_path / "a.m4a"
    audio.write_bytes(b"x")
    assert main(["--vault", str(vault.root), "interview", hub, "--audio", str(audio)]) == 0
    t = (vault.hub_dir(hub) / "interview_transcript.md").read_text(encoding="utf-8")
    assert "[00:00.0] 我每周二下午打三个电话。" in t


def test_transcribe_without_dependency(monkeypatch, tmp_path):
    from creator_agent.transcribe import transcribe

    monkeypatch.setitem(sys.modules, "faster_whisper", None)
    with pytest.raises(VaultError, match="faster-whisper"):
        transcribe(tmp_path / "a.m4a")


# ------------------------------------------------------------------ 读者调查
def test_survey_design_and_analyze(vault, llm, tmp_path):
    sid = design(vault, llm, "了解读者的访谈习惯", topic="每周一次访谈", n=3)
    d = vault.root / "surveys" / sid
    header = (d / "responses_template.csv").read_text(encoding="utf-8").strip()
    assert header == "respondent_id,q01,q02,q03"
    assert "不代表全体人群" in (d / "survey.md").read_text(encoding="utf-8")
    resp = tmp_path / "r.csv"
    with resp.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["respondent_id", "q01", "q02", "q03"])
        w.writerows([["1", "每周", "4", "没时间约人"], ["2", "按项目", "2", "不知道问什么"],
                     ["3", "按项目", "3", "没时间约人，老板也不支持"]])
    r = analyze(vault, llm, sid, resp)
    assert r["n"] == 3
    assert r["stats"]["q01"]["counts"]["按项目"]["n"] == 2
    assert r["stats"]["q02"]["mean"] == 3.0
    t = r["themes"][0]
    assert t["quotes"] == ["没时间约人"] and t["dropped_quotes"] == 1  # 编造的引用被丢掉
    assert "样本只有 3 份" in (d / "analysis.md").read_text(encoding="utf-8")


# ------------------------------------------------------------------ 盲评与审计
def test_blind_eval(vault, llm, tmp_path):
    hub = run_to_final(vault, llm)
    human = tmp_path / "h.md"
    human.write_text("# 我手写的\n\n纯人写。", encoding="utf-8")
    batch = blind_prepare(vault, [hub], [human], seed=1)
    d = vault.root / "evals" / batch
    items = sorted(p.name for p in d.glob("item_*.md"))
    assert len(items) == 2
    for name in items:
        assert "[f01]" not in (d / name).read_text(encoding="utf-8")
    with pytest.raises(VaultError, match="没打分"):
        blind_score(vault, batch)
    import json

    key = json.loads((d / ".key.json").read_text(encoding="utf-8"))
    rows = [[n, "4" if key[n]["group"] == "ai" else "3", ""] for n in items]
    with (d / "ratings.csv").open("w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows([["item", "score_1_to_5", "note"]] + rows)
    r = blind_score(vault, batch)
    assert r["ai_not_worse"] and r["ai_mean"] == 4.0


def test_audit(vault, llm):
    hub = run_to_final(vault, llm)
    stages.s6_adapt(vault, llm, hub, n_x=1, n_notes=0, formats=["x_post"])
    gates.approve(vault, hub, "H5", variants=["all"])
    vid = f"v_{hub}_x_post_01"
    stages.mark_published(vault, vid, "https://x.com/me/status/1")
    assert audit(vault)["ok"]
    # 篡改：发布时间早于批准时间、出现自动互动
    v = vault.variant(vid)
    v["publish_result"]["published_at"] = "2020-01-01T00:00+00:00"
    v["compliance"]["automated_interaction"] = "auto_reply"
    vault.save_variant(v)
    rules = {x["rule"] for x in audit(vault)["violations"]}
    assert {"human_approval_before_publish", "no_automated_interaction"} <= rules
    p = vault.root / "platforms/x.yaml"
    p.write_text(p.read_text(encoding="utf-8").replace('verified_at: "2026-11-03"', 'verified_at: "2025-01-01"'),
                 encoding="utf-8")
    assert "platform_rules_verified_90d" in {x["rule"] for x in audit(vault)["violations"]}
