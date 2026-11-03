import datetime as dt

import pytest

from creator_agent import gates, metrics, stages
from creator_agent.factcheck import factcheck, quote_on_page
from creator_agent.gates import GateError
from creator_agent.llm import LLM
from creator_agent.loops import interview, jaccard, progress, promote, recycle
from creator_agent.style import baseline, drift
from creator_agent.vault import Vault, VaultError

from fakes import FakeClient, _no_network
from test_pipeline import GOOD_DRAFT, run_to_final


@pytest.fixture
def vault(tmp_path):
    v = Vault.init(tmp_path / "vault")
    _no_network(v)
    return v


@pytest.fixture
def client():
    return FakeClient()


@pytest.fixture
def llm(vault, client):
    return LLM(vault.llm_config(), client=client)


def to_h3(vault, llm):
    hub = vault.new_hub(vault.add_idea("小团队要不要做用户访谈？"))
    stages.s1_angles(vault, llm, hub)
    gates.approve(vault, hub, "H1", angle=1, excitement=4, edge="大家默认访谈按项目做")
    stages.s2_research(vault, llm, hub)
    gates.approve(vault, hub, "H2", confirm=True)
    stages.s3_outline(vault, llm, hub)
    gates.approve(vault, hub, "H3")
    return hub


# ------------------------------------------------------------------ 研究
def test_multi_agent_research(vault, llm, client):
    cfg = vault.root / "agent.yaml"
    cfg.write_text(cfg.read_text(encoding="utf-8").replace("mode: single", "mode: multi"), encoding="utf-8")
    hub = vault.new_hub(vault.add_idea("一个题"))
    stages.s1_angles(vault, llm, hub)
    gates.approve(vault, hub, "H1", angle=1, excitement=3, edge="一个足够长的 edge")
    r = stages.s2_research(vault, llm, hub)
    assert r["mode"] == "multi"
    # 两个子问题、两个工作者返回相同的发现 → 去重后仍是 2 条，重新编号
    assert [f["id"] for f in r["findings"]] == ["f01", "f02"]
    assert len(list((vault.hub_dir(hub) / "research_workers").glob("worker_*.md"))) == 2
    worker_calls = [c for c in client.calls if c.get("tools")]
    assert len(worker_calls) == 2
    assert {t["type"] for t in worker_calls[0]["tools"]} == {"web_search_20260209", "web_fetch_20260209"}


def test_single_research_uses_fetch_too(vault, llm, client):
    to_h3(vault, llm)
    tools = [c["tools"] for c in client.calls if c.get("tools")][0]
    assert {t["type"] for t in tools} == {"web_search_20260209", "web_fetch_20260209"}


# ------------------------------------------------------------------ 逐条核查
def test_factcheck_blocks_unsupported_quote_and_needs_override(vault, llm, client):
    hub = to_h3(vault, llm)
    (vault.hub_dir(hub) / "draft.md").write_text(GOOD_DRAFT, encoding="utf-8")
    client.fact_kind, client.entail_verdict = "quote", "partial"
    r = stages.s5_review(vault, llm, hub)
    assert not r["pass"]
    assert r["soft_fails"][0]["check"] == "factcheck"
    assert r["scores"]["hard_support_rate"] == 0.0
    with pytest.raises(GateError, match="override"):
        gates.approve(vault, hub, "H4", quotes_checked=1, numbers_checked=0, ending_ok=True)
    rec = gates.approve(vault, hub, "H4", quotes_checked=1, numbers_checked=0, ending_ok=True,
                        override_reason="我已回原文逐字核对过")
    assert rec["override"]


def test_factcheck_supported_passes(vault, llm):
    hub = to_h3(vault, llm)
    (vault.hub_dir(hub) / "draft.md").write_text(GOOD_DRAFT, encoding="utf-8")
    r = stages.s5_review(vault, llm, hub)
    assert r["pass"] and r["scores"]["support_rate"] == 1.0


def test_factcheck_refetch(vault, llm, client):
    findings = [{"id": "f01", "quote_verbatim": "Talk to customers weekly", "url": "https://a.com",
                 "speaker": "T", "attribution": "own_words", "weak": False}]
    client.fact_kind = "quote"
    draft = "她说 Talk to customers weekly [f01]"
    ok = factcheck(llm, draft, findings, fetcher=lambda u: "<p>You should talk to customers  weekly.</p>")
    assert ok["facts"][0]["quote_on_page"] is True and not ok["blocking"]
    bad = factcheck(llm, draft, findings, fetcher=lambda u: "<p>something else</p>")
    assert bad["facts"][0]["quote_on_page"] is False and bad["blocking"]

    def boom(u):
        raise TimeoutError()

    down = factcheck(llm, draft, findings, fetcher=boom)
    assert down["facts"][0]["quote_on_page"] is None and not down["blocking"]
    assert down["unreachable_pages"] == ["https://a.com"]


def test_factcheck_weak_source_blocks_numbers(vault, llm, client):
    findings = [{"id": "f02", "quote_verbatim": "80% never", "url": "https://agg.com", "speaker": "n/a",
                 "attribution": "n/a", "weak": True}]
    client.fact_kind = "number"
    r = factcheck(llm, "80% 的团队不做访谈 [f02]", findings, refetch=False)
    assert r["blocking"] and r["blocking"][0]["weak_source"]


def test_quote_normalization():
    assert quote_on_page("“It’s the practice.”", "<b>it's the   practice</b>")
    assert not quote_on_page("", "anything")


# ------------------------------------------------------------------ 拔刺采样
def test_briars_cross_sampling(vault, llm, client):
    hub = to_h3(vault, llm)
    (vault.hub_dir(hub) / "draft.md").write_text(GOOD_DRAFT, encoding="utf-8")
    r = stages.s5_review(vault, llm, hub)
    assert client.briars_calls == 3
    assert [b["sentence"] for b in r["briars"]["items"]] == ["这很重要。"]
    assert r["briars"]["items"][0]["hits"] == 3 and r["briars"]["single_hits"] == 3


# ------------------------------------------------------------------ 风格漂移
STYLE_DOC = ("我每周二下午打三个电话。电话很短，十分钟就够了。你可以试试。" * 12)


def test_style_drift_detected():
    base = baseline([STYLE_DOC + str(i) for i in range(6)] + [STYLE_DOC.replace("。", "，", 3)])
    same = drift(STYLE_DOC, base)
    assert same["checked"] and not same["drifted"]
    other = ("综上所述，在当今快速发展的时代背景之下，我们必须从多个维度全方位深入地思考用户访谈这一至关重要的问题，"
             "并且以系统性的方法论来构建可持续的、可复制的、可规模化的用户研究体系以实现长期价值。") * 4
    assert drift(other, base)["drifted"]


def test_style_gate_in_review(vault, llm):
    for i in range(5):
        (vault.root / f"archive/a{i}.md").write_text(STYLE_DOC + f"第{i}篇。", encoding="utf-8")
    hub = to_h3(vault, llm)
    long_winded = ("# t\n\n按周固定访谈比按项目访谈更能坚持 [f01]，" + "并且以系统性的方法论来构建可持续的、可复制的、"
                   "可规模化的用户研究体系，从而在长期维度上实现组织层面的价值沉淀与能力跃迁" * 3 + "。")
    (vault.hub_dir(hub) / "draft.md").write_text(long_winded, encoding="utf-8")
    r = stages.s5_review(vault, llm, hub)
    assert r["style"]["checked"] and r["style"]["drifted"]
    assert any(f["check"] == "style_drift" for f in r["soft_fails"])


# ------------------------------------------------------------------ 访谈模式
def test_interview_mode(vault, llm, client):
    hub = to_h3(vault, llm)
    client.interview_draft = "# 访谈稿\n\n我每周二下午打三个电话。\n\n根据麦肯锡研究，87% 的企业采用季度战略复盘机制以提升组织效能。"
    r = interview(vault, llm, hub, "我每周二下午打三个电话，然后然后，就这样坚持了三个月。")
    assert r["added_numbers"]
    assert any("麦肯锡" in s for s in r["suspicious"])
    assert vault.meta(hub)["draft_mode"] == "I"
    assert (vault.hub_dir(hub) / "draft_agent.md").exists()
    assert "Repeated" in (vault.hub_dir(hub) / "cribs.md").read_text(encoding="utf-8")


# ------------------------------------------------------------------ R1 / R2
def _published_post(vault, llm, days_ago=0):
    hub = run_to_final(vault, llm)
    stages.s6_adapt(vault, llm, hub, n_x=1, n_notes=0, formats=["x_post"])
    gates.approve(vault, hub, "H5", variants=["all"])
    vid = f"v_{hub}_x_post_01"
    at = (dt.datetime.now().astimezone() - dt.timedelta(days=days_ago)).isoformat(timespec="minutes")
    stages.mark_published(vault, vid, "https://x.com/me/status/1", at=at)
    metrics.add_snapshot(vault, vid, {"impressions": 1000, "replies": 40}, source="manual")
    return hub, vid


def test_promote_feeds_s1(vault, llm, client):
    _, vid = _published_post(vault, llm)
    new_hub = promote(vault, vid)
    assert vault.meta(new_hub)["promoted_from"]["metrics"]["replies"] == 40
    assert vault.idea(vault.meta(new_hub)["idea_id"])["origin"] == "own_post"
    stages.s1_angles(vault, llm, new_hub)
    assert "R1 短养长" in client.calls[-1]["messages"][0]["content"]
    assert progress(vault)["r1_hubs"] == 1


def test_recycle_requires_age_and_new_angle(vault, llm, client):
    hub, vid = _published_post(vault, llm, days_ago=10)
    with pytest.raises(VaultError, match="90"):
        recycle(vault, llm, vid)
    made = recycle(vault, llm, vid, force=True, n=1)
    assert made[0]["derivation"] == "recycle" and made[0]["parent_variant"] == vid
    assert made[0]["gate_results"]["checks"]["not_light_edit"]
    # 轻改版本会被拦下
    client.recycle_text = vault.variant(vid)["body"]["text"].replace("。", "！", 1)
    light = recycle(vault, llm, vid, force=True, n=1)[0]
    assert "not_light_edit" in light["gate_results"]["failed"]
    rec = gates.approve(vault, hub, "H5", variants=[made[0]["variant_id"]])
    assert made[0]["variant_id"] in rec["variants"]


def test_jaccard():
    assert jaccard("我每周二下午打三个电话", "我每周二下午打三个电话") == 1.0
    assert jaccard("完全不同的一句话内容", "我每周二下午打三个电话") < 0.2


def test_progress_support_rate(vault, llm):
    run_to_final(vault, llm)
    p = progress(vault)
    assert p["support_rate_mean"] == 1.0 and p["support_rate_ok"]
    assert p["research_mode"] == "single"
