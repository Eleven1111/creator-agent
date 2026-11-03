import io
import json

import pytest

from creator_agent import gates, metrics, stages
from creator_agent.adapt import check_thread
from creator_agent.cli import main
from creator_agent.gates import GateError
from creator_agent.llm import LLM
from creator_agent.retro import approve_retro, build_retro
from creator_agent.vault import Vault, VaultError

from fakes import FakeClient, _no_network
from test_pipeline import run_to_final


@pytest.fixture
def vault(tmp_path):
    v = Vault.init(tmp_path / "vault")
    _no_network(v)
    return v


@pytest.fixture
def llm(vault):
    return LLM(vault.llm_config(), client=FakeClient(), log_dir=vault.root / "runs/logs")


ENGLISH = """# Weekly interviews

I talked to 40 small teams. The ones that ran interviews per project mostly stopped [f01].

Here is what I do every Tuesday afternoon, from my own experience.

Start next Tuesday with one call."""


def adapted(vault, llm, english=True):
    hub = run_to_final(vault, llm)
    if english:
        (vault.hub_dir(hub) / "final_en.md").write_text(ENGLISH, encoding="utf-8")
    vs = stages.s6_adapt(vault, llm, hub, n_x=2, n_notes=1)
    return hub, {v["variant_id"]: v for v in vs}


def test_all_formats_generated_with_editable_text(vault, llm):
    hub, vs = adapted(vault, llm)
    fmts = sorted({v["format"] for v in vs.values()})
    assert fmts == ["medium_story", "substack_note", "x_article", "x_post", "x_thread"]
    thread = vs[f"v_{hub}_x_thread_01"]
    assert thread["gate_results"]["passed"], thread["gate_results"]["failed"]
    assert "utm_medium=thread_end" in thread["body"]["parts"][-1]  # 链接只在末帖
    article = vs[f"v_{hub}_x_article_01"]
    assert article["gate_results"]["failed"] == ["author_has_premium"]  # 模板默认没有 Premium
    medium = vs[f"v_{hub}_medium_story_01"]
    assert medium["gate_results"]["passed"], medium["gate_results"]["failed"]
    assert medium["canonical"]["method"] == "medium_import"
    for vid in vs:
        assert vault.variant_text(vid) is not None
    queue = (vault.hub_dir(hub) / "review_queue.md").read_text(encoding="utf-8")
    assert "variants/<id>.md" in queue


def test_medium_skipped_without_english_rewrite(vault, llm):
    hub, vs = adapted(vault, llm, english=False)
    assert not any(v["format"] == "medium_story" for v in vs.values())
    assert "final_en.md" in vault.meta(hub)["skipped_formats"]["medium_story"]


def test_medium_skipped_for_mode_b(vault, llm):
    hub = run_to_final(vault, llm)
    meta = vault.meta(hub)
    meta["draft_mode"] = "B"
    vault.save_meta(hub, meta)
    (vault.hub_dir(hub) / "final_en.md").write_text(ENGLISH, encoding="utf-8")
    vs = stages.s6_adapt(vault, llm, hub, formats=["medium_story"])
    assert vs == []
    assert "B 模式" in vault.meta(hub)["skipped_formats"]["medium_story"]


def test_author_edit_is_revalidated_and_diffed(vault, llm):
    hub, vs = adapted(vault, llm)
    good = f"v_{hub}_x_post_01"
    # 作者改稿时加了一个母稿里没有的数字 → H5 重跑检查后不再通过
    vault.write_variant_text(good, vault.variant_text(good) + " 我做了 99 次。")
    with pytest.raises(GateError, match="numbers_in_final"):
        gates.approve(vault, hub, "H5", variants=[good])
    # 改成合规的文字 → 通过，并记录修改对
    vault.write_variant_text(good, "按项目做访谈的团队，三个月后几乎都停了。你们按周还是按项目？")
    rec = gates.approve(vault, hub, "H5", variants=[good])
    assert good in rec["variants"]
    v = vault.variant(good)
    assert v["status"] == "approved" and v["edited"]
    assert v["body"]["text"].startswith("按项目做访谈")
    diffs = vault.edit_diffs()
    assert diffs and diffs[0]["key"] == good and diffs[0]["edit_ratio"] > 0
    kit = (vault.hub_dir(hub) / "publish_kit.md").read_text(encoding="utf-8")
    assert "按项目做访谈的团队" in kit and "没有任何内容会被自动发出" in kit


def test_h5_all_skips_failed_and_accumulates(vault, llm):
    hub, vs = adapted(vault, llm)
    rec = gates.approve(vault, hub, "H5", variants=["all"])
    assert f"v_{hub}_x_article_01" not in rec["variants"]  # 没 Premium 不放行
    assert f"v_{hub}_x_post_article_promo" not in rec["variants"]  # 推广帖跟着文章走
    with pytest.raises(GateError, match="推广帖"):
        gates.approve(vault, hub, "H5", variants=[f"v_{hub}_x_post_article_promo"])
    profile = (vault.root / "voice/profile.yaml").read_text(encoding="utf-8")
    (vault.root / "voice/profile.yaml").write_text(profile.replace("x_premium: false", "x_premium: true"),
                                                   encoding="utf-8")
    rec2 = gates.approve(vault, hub, "H5", variants=[f"v_{hub}_x_article_01", f"v_{hub}_x_post_article_promo"])
    assert set(rec["variants"]) < set(rec2["variants"])


def test_thread_link_only_in_last():
    xr = {"max_weighted_chars": 280}
    ok = check_thread(["一", "二 https://a.com"], "一二", xr, {"first_post_standalone": True})
    bad = check_thread(["一 https://a.com", "二"], "一二", xr, {"first_post_standalone": True})
    assert ok["link_only_in_last"] and not bad["link_only_in_last"]


def _publish_all(vault, hub):
    gates.approve(vault, hub, "H5", variants=["all"])
    for i, v in enumerate(vault.variants_of(hub)):
        if v["status"] == "approved":
            url = f"https://x.com/me/status/{1000 + i}" if v["platform"] == "x" else f"https://e.com/{i}"
            stages.mark_published(vault, v["variant_id"], url)


def test_metrics_pull_x_readonly(vault, llm):
    hub, vs = adapted(vault, llm)
    _publish_all(vault, hub)
    seen = {}

    class Resp(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def opener(req):
        seen["method"] = req.get_method()
        seen["url"] = req.full_url
        seen["auth"] = req.headers.get("Authorization")
        ids = req.full_url.split("ids=")[1].split("&")[0].split("%2C")
        data = [{"id": i, "public_metrics": {"impression_count": 1000, "reply_count": 10 * (n + 1),
                                             "repost_count": 1, "quote_count": 0, "like_count": 5,
                                             "bookmark_count": 2}} for n, i in enumerate(ids)]
        return Resp(json.dumps({"data": data}).encode())

    dry = metrics.pull_x(vault, dry_run=True)
    assert dry["written"] == 0 and dry["estimated_cost_usd"] > 0
    with pytest.raises(VaultError, match="X_BEARER_TOKEN"):
        metrics.pull_x(vault, token=None)
    r = metrics.pull_x(vault, token="t", opener=opener)
    assert seen["method"] == "GET" and seen["url"].startswith("https://api.x.com/2/tweets?")
    assert seen["auth"] == "Bearer t" and "public_metrics" in seen["url"]
    assert r["written"] == r["posts"] > 0
    rep = metrics.channel_report(vault)
    assert rep["x/x_post"]["reply_rate"] > 0


def test_metrics_manual_csv_and_retro(vault, llm, tmp_path):
    hub, vs = adapted(vault, llm)
    _publish_all(vault, hub)
    xs = [v for v in vault.variants_of(hub) if v["format"] == "x_post" and v["status"] == "published"]
    note = [v for v in vault.variants_of(hub) if v["format"] == "substack_note"][0]
    metrics.add_snapshot(vault, note["variant_id"], {"free_subs": 3}, source="manual")
    # 三条 X 帖，其中一条回复率远高于中位数 → R1 候选
    extra = []
    for i in range(3):
        vid = f"v_{hub}_x_post_extra_{i}"
        v = dict(xs[0], variant_id=vid)
        vault.save_variant(v)
        extra.append(vid)
    csv_path = tmp_path / "x.csv"
    rows = ["variant_id,impressions,replies"] + [f"{vid},1000,{r}" for vid, r in
                                                 zip(extra + [x["variant_id"] for x in xs], [5, 5, 60, 5, 5])]
    csv_path.write_text("\n".join(rows), encoding="utf-8")
    assert metrics.import_csv(vault, csv_path, source="x_export") == len(rows) - 1
    month = vault.variant(extra[0])["publish_result"]["published_at"][:7]
    r = build_retro(vault, llm, month)
    assert [c["variant_id"] for c in r["r1_candidates"]] == [extra[2]]
    assert r["analysis"]["proposals"]
    assert (vault.root / f"runs/retro_{month}.md").exists()
    before = len(vault.ideas())
    rec = approve_retro(vault, month, ["all"], note="ok")
    assert len(rec["r1_added"]) == 1 and len(vault.ideas()) == before + 1
    assert vault.ideas()[-1]["origin"] == "own_post"


def test_metrics_require_published(vault, llm):
    hub, vs = adapted(vault, llm)
    with pytest.raises(VaultError, match="还没发布"):
        metrics.add_snapshot(vault, next(iter(vs)), {"likes": 1}, source="manual")


def test_cli_p2_commands(vault, llm, monkeypatch, capsys):
    hub, vs = adapted(vault, llm)
    root = str(vault.root)
    assert main(["--vault", root, "approve", hub, "H5", "--variants", "all"]) == 0
    assert "publish_kit" in capsys.readouterr().out
    assert main(["--vault", root, "due", "--hours", "240"]) == 0
    assert "publish_kit.md" in capsys.readouterr().out
    assert main(["--vault", root, "kit", hub]) == 0
    assert main(["--vault", root, "metrics", "pull-x", "--dry-run"]) == 0
    assert main(["--vault", root, "report"]) == 0
