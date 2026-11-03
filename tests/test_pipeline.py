import json

import pytest

from creator_agent import gates, stages
from creator_agent.cli import main
from creator_agent.gates import GateError
from creator_agent.lint import lint_draft, x_weighted_length
from creator_agent.llm import LLM, LLMConfig
from creator_agent.utm import with_utm
from creator_agent.vault import Vault

from fakes import FakeClient, _no_network


@pytest.fixture
def vault(tmp_path):
    v = Vault.init(tmp_path / "vault")
    _no_network(v)
    (v.root / "archive/old.md").write_text("# 用户访谈怎么做\n\n小团队访谈经验", encoding="utf-8")
    return v


@pytest.fixture
def client():
    return FakeClient()


@pytest.fixture
def llm(vault, client):
    return LLM(vault.llm_config(), client=client, log_dir=vault.root / "runs/logs")


GOOD_DRAFT = """# 每周一次访谈

按周固定访谈比按项目访谈更能坚持 [f01]。

我每周二下午打三个电话。三个月下来，从没断过。我访谈过的 40 个小团队里，按项目做的几乎都停了。

你可以从下周二开始，先约一个人。"""


def run_to_final(vault, llm):
    hub = vault.new_hub(vault.add_idea("小团队要不要做用户访谈？"))
    stages.s1_angles(vault, llm, hub)
    gates.approve(vault, hub, "H1", angle=1, excitement=4, edge="大家默认访谈按项目做，我怀疑")
    stages.s2_research(vault, llm, hub)
    gates.approve(vault, hub, "H2", confirm=True)
    stages.s3_outline(vault, llm, hub)
    gates.approve(vault, hub, "H3")
    stages.s4_draft(vault, llm, hub, mode="A")
    (vault.hub_dir(hub) / "draft.md").write_text(GOOD_DRAFT, encoding="utf-8")
    review = stages.s5_review(vault, llm, hub)
    assert review["pass"], review.get("blocking")
    gates.approve(vault, hub, "H4", quotes_checked=1, numbers_checked=0, ending_ok=True,
                  canonical_url="https://me.substack.com/p/weekly")
    return hub


def test_full_pipeline(vault, llm, client):
    hub = run_to_final(vault, llm)
    variants = stages.s6_adapt(vault, llm, hub, n_x=2, n_notes=1, formats=["x_post", "substack_note"])
    by_fmt = {}
    for v in variants:
        by_fmt.setdefault(v["format"], []).append(v)
    good, bad = by_fmt["x_post"]
    assert good["gate_results"]["passed"]
    assert not bad["gate_results"]["passed"]
    assert {"no_link", "no_hashtags", "dry_at_least_2", "reply_hook"} <= set(bad["gate_results"]["failed"])
    assert "utm_content=" + good["variant_id"] in good["link_policy"]["url"]
    assert good["gate_results"]["checks"]["numbers_in_final"]

    assert good["compliance"]["automated_interaction"] == "none"
    assert (vault.hub_dir(hub) / "substack_package.md").exists()

    gates.approve(vault, hub, "H5", variants=["all"])
    assert vault.variant(good["variant_id"])["status"] == "approved"
    assert vault.variant(bad["variant_id"])["status"] == "draft"
    stages.mark_published(vault, good["variant_id"], "https://x.com/me/status/1")
    assert vault.variant(good["variant_id"])["status"] == "published"

    # 每次调用都用默认模型、开启 fallback，并写了成本日志
    assert all(c["model"] == "claude-opus-5-5" for c in client.calls)
    assert all(c.get("fallbacks") == "default" for c in client.calls)
    research_calls = [c for c in client.calls if c.get("tools")]
    assert research_calls and research_calls[0]["tools"][0]["type"] == "web_search_20260209"
    assert list((vault.root / "runs/logs").glob("*.jsonl"))


def test_adapt_rejects_numbers_not_in_final(vault, llm):
    hub = run_to_final(vault, llm)
    final = (vault.hub_dir(hub) / "final.md").read_text(encoding="utf-8")
    (vault.hub_dir(hub) / "final.md").write_text(final.replace("40 个", "几十个"), encoding="utf-8")
    good = stages.s6_adapt(vault, llm, hub, n_x=2, n_notes=1)[0]
    assert "numbers_in_final" in good["gate_results"]["failed"]

def test_gates_block_out_of_order(vault, llm):
    hub = vault.new_hub(vault.add_idea("一个题"))
    with pytest.raises(GateError):
        stages.s2_research(vault, llm, hub)
    stages.s1_angles(vault, llm, hub)
    with pytest.raises(GateError, match="excitement"):
        gates.approve(vault, hub, "H1", angle=1, edge="一个足够长的 edge")
    with pytest.raises(GateError, match="edge"):
        gates.approve(vault, hub, "H1", angle=1, excitement=3, edge="")
    with pytest.raises(GateError):
        gates.approve(vault, hub, "H3")


def test_weak_sources_flagged_and_ids_assigned(vault, llm):
    hub = vault.new_hub(vault.add_idea("一个题"))
    stages.s1_angles(vault, llm, hub)
    gates.approve(vault, hub, "H1", angle=1, excitement=3, edge="一个足够长的 edge")
    r = stages.s2_research(vault, llm, hub)
    assert [f["id"] for f in r["findings"]] == ["f01", "f02"]
    assert [f["weak"] for f in r["findings"]] == [False, True]
    assert "弱来源" in (vault.hub_dir(hub) / "research.md").read_text(encoding="utf-8")


def test_review_blocks_tk_without_llm_calls(vault, llm, client):
    hub = vault.new_hub(vault.add_idea("小团队要不要做用户访谈？"))
    stages.s1_angles(vault, llm, hub)
    gates.approve(vault, hub, "H1", angle=1, excitement=4, edge="大家默认访谈按项目做")
    stages.s2_research(vault, llm, hub)
    gates.approve(vault, hub, "H2", confirm=True)
    stages.s3_outline(vault, llm, hub)
    gates.approve(vault, hub, "H3")
    stages.s4_draft(vault, llm, hub, mode="B")  # 模式 B 草稿带 [TK: 作者定结尾]
    n_before = len(client.calls)
    r = stages.s5_review(vault, llm, hub)
    assert not r["pass"] and len(client.calls) == n_before
    with pytest.raises(GateError):
        gates.approve(vault, hub, "H4", quotes_checked=0, numbers_checked=0, ending_ok=True)


def test_h4_rejects_edits_after_review(vault, llm):
    hub = vault.new_hub(vault.add_idea("小团队要不要做用户访谈？"))
    stages.s1_angles(vault, llm, hub)
    gates.approve(vault, hub, "H1", angle=1, excitement=4, edge="大家默认访谈按项目做")
    stages.s2_research(vault, llm, hub)
    gates.approve(vault, hub, "H2", confirm=True)
    stages.s3_outline(vault, llm, hub)
    gates.approve(vault, hub, "H3")
    (vault.hub_dir(hub) / "draft.md").write_text(GOOD_DRAFT, encoding="utf-8")
    stages.s5_review(vault, llm, hub)
    (vault.hub_dir(hub) / "draft.md").write_text(GOOD_DRAFT + "\n\n新加一段。", encoding="utf-8")
    with pytest.raises(GateError, match="重新运行"):
        gates.approve(vault, hub, "H4", quotes_checked=1, numbers_checked=0, ending_ok=True)


def test_review_blocks_unknown_source_id(vault, llm):
    hub = vault.new_hub(vault.add_idea("小团队要不要做用户访谈？"))
    stages.s1_angles(vault, llm, hub)
    gates.approve(vault, hub, "H1", angle=1, excitement=4, edge="大家默认访谈按项目做")
    stages.s2_research(vault, llm, hub)
    gates.approve(vault, hub, "H2", confirm=True)
    stages.s3_outline(vault, llm, hub)
    gates.approve(vault, hub, "H3")
    (vault.hub_dir(hub) / "draft.md").write_text(GOOD_DRAFT.replace("[f01]", "[f09]"), encoding="utf-8")
    r = stages.s5_review(vault, llm, hub)
    assert not r["pass"]
    assert any(b["check"] == "unknown_source_ids" for b in r["blocking"])


def test_lint():
    rep = lint_draft("# t\n\n值得注意的是，这很重要！\n\n总之，就这样。", never=["抓手"])
    checks = {f["check"] for f in rep.flags}
    assert {"ai_tells", "exclamation", "summary_ending"} <= checks
    assert lint_draft("我们的抓手是……", never=["抓手"]).blocking[0]["check"] == "never_list"
    assert lint_draft("说白了就这样", never=["说白了"], deliberate_breaks=["说白了"]).ok
    assert lint_draft("还没写 [TK: 数据]").blocking[0]["check"] == "tk"


def test_x_weighted_length():
    assert x_weighted_length("abc") == 3
    assert x_weighted_length("中文") == 4
    assert x_weighted_length("看 https://example.com/a/very/long/path") == 2 + 1 + 23


def test_utm():
    u = with_utm("https://me.substack.com/p/a?ref=1", source="x", medium="post",
                 campaign="c", content="v1")
    assert "ref=1" in u and "utm_source=x" in u and "utm_content=v1" in u


def test_eval_discrimination(vault, client):
    for i in range(2):
        (vault.root / f"evals/anchors/good_{i}.md").write_text(f"好锚点{i}", encoding="utf-8")
        (vault.root / f"evals/anchors/bad_{i}.md").write_text(f"差锚点{i}", encoding="utf-8")
    rows = []
    for i, label in enumerate(["good", "good", "bad", "bad"]):
        p = f"evals/cases/c{i}.md"
        (vault.root / p).write_text(f"{label} case {i}", encoding="utf-8")
        rows.append(json.dumps({"id": f"c{i}", "path": p, "label": label}))
    (vault.root / "evals/testset.jsonl").write_text("\n".join(rows), encoding="utf-8")
    fake = FakeClient(judge_score=lambda params: 0.85 if "good case" in params["messages"][0]["content"] else 0.3)
    from creator_agent.evalset import run_eval

    s = run_eval(vault, LLM(vault.llm_config(), client=fake))
    assert s["pairwise_auc"] == 1.0 and s["accuracy_at_threshold"] == 1.0 and s["discriminates"]


def test_cli_init_and_idea(tmp_path, capsys):
    root = tmp_path / "v"
    assert main(["init", str(root)]) == 0
    assert main(["--vault", str(root), "idea", "add", "一个选题", "--edge", "大家默认 X"]) == 0
    assert main(["--vault", str(root), "idea", "list"]) == 0
    assert "idea_0001" in capsys.readouterr().out
    assert main(["--vault", str(root), "status"]) == 0


def test_refusal_raises(vault):
    from types import SimpleNamespace

    from creator_agent.llm import LLMError

    class C(FakeClient):
        pass

    c = C()

    def stream(**params):
        from fakes import FakeStream, _msg

        m = _msg("", stop="refusal")
        m.stop_details = SimpleNamespace(category="cyber", explanation="x")
        return FakeStream(m)

    c.beta = SimpleNamespace(messages=SimpleNamespace(stream=stream))
    with pytest.raises(LLMError, match="拒答"):
        LLM(LLMConfig(), client=c).text(stage="t", system="s", user="u")
