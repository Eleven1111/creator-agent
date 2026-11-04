import asyncio
import importlib.util
import json
import os
import zipfile

import pytest

pytestmark = pytest.mark.skipif(importlib.util.find_spec("mcp") is None,
                                reason="需要 pip install -e '.[mcp]'")

from creator_agent.host_llm import PENDING_MARK, HostLLM, HostTaskPending, validate
from creator_agent.llm import LLMError
from creator_agent.vault import Vault

from fakes import FakeClient, _no_network
from test_pipeline import GOOD_DRAFT


@pytest.fixture
def vault(tmp_path):
    v = Vault.init(tmp_path / "vault")
    _no_network(v)
    return v


def fake_host_answer(task, client=None):
    """扮演宿主模型：用测试用的假模型逻辑完成待办任务。"""
    client = client or FakeClient()
    params = {"system": task["system"], "messages": [{"role": "user", "content": task["user"]}],
              "output_config": {"format": {"type": "json_schema", "schema": task["schema"]}}
              if task["kind"] == "json" else {}}
    with client.beta.messages.stream(**params) as s:
        return s.get_final_message().content[0].text


def task_id_of(text):
    return text.split("task_id=")[1].split("（")[0].strip()


# ------------------------------------------------------------------ HostLLM 单元
def test_validate_schema_subset():
    schema = {"type": "object", "properties": {"a": {"type": "integer"},
                                               "b": {"type": "string", "enum": ["x", "y"]}},
              "required": ["a", "b"], "additionalProperties": False}
    assert validate(schema, {"a": 1, "b": "x"}) == []
    errs = validate(schema, {"a": True, "c": 1})
    assert any("b" in e and "缺少" in e for e in errs)
    assert any("c" in e and "不允许" in e for e in errs)
    assert any("$.a" in e and "整数" in e for e in errs)


def test_host_llm_pending_submit_replay(tmp_path):
    h = HostLLM(tmp_path)
    schema = {"type": "object", "properties": {"x": {"type": "integer"}}, "required": ["x"],
              "additionalProperties": False}
    with pytest.raises(HostTaskPending) as e:
        h.json(stage="t", system="s", user="u", schema=schema)
    tid = e.value.task["task_id"]
    with pytest.raises(LLMError, match="不符合 schema"):
        h.submit(tid, '{"x": "nope"}')
    with pytest.raises(LLMError, match="不是合法 JSON"):
        h.submit(tid, "not json")
    h.submit(tid, '```json\n{"x": 3}\n```')  # 代码块包裹也接受
    h2 = HostLLM(tmp_path)  # 重放：新实例命中缓存
    assert h2.json(stage="t", system="s", user="u", schema=schema) == {"x": 3}


def test_identical_prompts_are_separate_samples(tmp_path):
    h = HostLLM(tmp_path)
    ids = []
    for _ in range(3):
        try:
            h.text(stage="briars", system="s", user="same")
        except HostTaskPending as e:
            ids.append(e.task["task_id"])
            h.submit(ids[-1], f"answer {len(ids)}")
    h2 = HostLLM(tmp_path)
    assert [h2.text(stage="briars", system="s", user="same") for _ in range(3)] == \
           ["answer 1", "answer 2", "answer 3"]
    assert len(set(ids)) == 3


def test_web_task_forbids_fabrication(tmp_path):
    from creator_agent.host_llm import render_task

    h = HostLLM(tmp_path)
    with pytest.raises(HostTaskPending) as e:
        h.text(stage="research", system="s", user="u", web_search=True)
    text = render_task(e.value.task, "run_research")
    assert "无法联网" in text and "绝不编造" in text and "submit_model_output" in text


# ------------------------------------------------------------------ 通过 MCP 的宿主模式全流程
def test_full_flow_in_host_mode(vault, monkeypatch):
    from mcp import Client

    from creator_agent.mcp_server import build_server, _llm

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    srv = build_server(lambda: vault, _llm)  # 真实的后端选择：没有 key → host
    answered = {"n": 0}

    async def run_tool(c, name, args):
        r = await c.call_tool(name, args)
        text = r.content[0].text
        assert not r.is_error, text
        while text.startswith(PENDING_MARK):
            tid = task_id_of(text)
            task = json.loads((vault.root / "runs/host_tasks" / f"{tid}.json").read_text(encoding="utf-8"))
            answered["n"] += 1
            r = await c.call_tool("submit_model_output", {"task_id": tid, "output": fake_host_answer(task)})
            text = r.content[0].text
            assert not r.is_error, text
        return text

    async def go():
        async with Client(srv) as c:
            backend = json.loads((await c.call_tool("model_backend", {})).content[0].text)
            assert backend["backend"] == "host"
            hub = json.loads((await c.call_tool("new_hub", {"idea": "小团队要不要做用户访谈？"})).content[0].text)["hub_id"]
            assert "角度 1" in await run_tool(c, "run_angles", {"hub_id": hub})
            await c.call_tool("approve_gate", {"hub_id": hub, "gate": "H1", "user_statement": "选 1，兴奋度 4",
                                               "angle": 1, "excitement": 4, "edge": "大家默认按项目做"})
            assert "H2 检查清单" in await run_tool(c, "run_research", {"hub_id": hub})
            await c.call_tool("approve_gate", {"hub_id": hub, "gate": "H2", "user_statement": "可以", "confirm": True})
            await run_tool(c, "run_outline", {"hub_id": hub})
            await c.call_tool("approve_gate", {"hub_id": hub, "gate": "H3", "user_statement": "可以"})
            await run_tool(c, "run_draft", {"hub_id": hub})
            await c.call_tool("write_draft", {"hub_id": hub, "markdown": GOOD_DRAFT})
            review = await run_tool(c, "run_review", {"hub_id": hub})
            assert "通过" in review and "3 次独立采样" in review
            await c.call_tool("approve_gate", {"hub_id": hub, "gate": "H4", "user_statement": "核对过",
                                               "quotes_checked": 1, "numbers_checked": 0, "ending_ok": True,
                                               "canonical_url": "https://me.substack.com/p/x"})
            queue = await run_tool(c, "run_adapt", {"hub_id": hub, "formats": ["x_post", "substack_note"],
                                                    "n_x": 2, "n_notes": 1})
            assert "待审稿件" in queue
            return hub

    hub = asyncio.run(go())
    assert answered["n"] >= 12  # 选题、研究 3 步、提纲、评审 8 步、改编
    assert (vault.hub_dir(hub) / "substack_package.md").exists()
    assert not list((vault.root / "runs/host_tasks").glob("*.json"))  # 没有遗留的待办任务


def test_backend_selection(vault, monkeypatch):
    from creator_agent.mcp_server import llm_backend

    monkeypatch.delenv("CA_LLM_BACKEND", raising=False)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-x")
    assert llm_backend(vault) == "anthropic"
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")
    assert llm_backend(vault) == "host"
    monkeypatch.setenv("CA_LLM_BACKEND", "anthropic")
    assert llm_backend(vault) == "anthropic"
    monkeypatch.setenv("CA_LLM_BACKEND", "weird")
    from creator_agent.vault import VaultError

    with pytest.raises(VaultError):
        llm_backend(vault)


# ------------------------------------------------------------------ Claude 桌面端扩展
def test_mcpb_bundle_valid(tmp_path):
    jsonschema = pytest.importorskip("jsonschema")
    from creator_agent.mcpb import build

    out = build(tmp_path)
    z = zipfile.ZipFile(out)
    names = z.namelist()
    for required in ("manifest.json", "pyproject.toml", "mcpb_server.py", "LICENSE",
                     "creator_agent/mcp_server.py", "creator_agent/skill/creator-agent/SKILL.md"):
        assert required in names, required
    assert not any("__pycache__" in n or n.endswith(".pyc") for n in names)
    manifest = json.loads(z.read("manifest.json"))
    with open(os.path.join(os.path.dirname(__file__), "data/mcpb-manifest-v0.4.schema.json"),
              encoding="utf-8") as f:
        schema = json.load(f)
    jsonschema.validate(manifest, schema)
    assert manifest["server"]["type"] == "uv"
    assert manifest["user_config"]["anthropic_api_key"]["required"] is False
    assert {t["name"] for t in manifest["tools"]} >= {"submit_model_output", "approve_gate", "run_review"}


def test_init_if_missing_and_placeholder_keys(tmp_path, monkeypatch):
    from creator_agent import mcp_server

    started = {}

    class FakeServer:
        def run(self, transport):
            started["transport"] = transport

    monkeypatch.setattr(mcp_server, "build_server", lambda *a, **k: FakeServer())
    monkeypatch.setenv("ANTHROPIC_API_KEY", "${user_config.anthropic_api_key}")
    new = tmp_path / "fresh"
    assert mcp_server.main(["--vault", str(new), "--init-if-missing"]) == 0
    assert (new / "agent.yaml").exists() and started["transport"] == "stdio"
    assert "ANTHROPIC_API_KEY" not in os.environ  # 未替换的占位符当作没填
    # 已有内容、但不是知识库的文件夹：不初始化，直接报错
    other = tmp_path / "other"
    other.mkdir()
    (other / "notes.txt").write_text("x", encoding="utf-8")
    assert mcp_server.main(["--vault", str(other), "--init-if-missing"]) == 1
    assert not (other / "agent.yaml").exists()
