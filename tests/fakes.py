"""假的 Anthropic 客户端：按系统提示词里的关键词返回预设输出，并记录每次请求参数。"""

from __future__ import annotations

import json
import re
from types import SimpleNamespace


def _msg(text: str, stop: str = "end_turn"):
    return SimpleNamespace(
        content=[SimpleNamespace(type="text", text=text)],
        stop_reason=stop, stop_details=None, model="claude-opus-5-5",
        usage=SimpleNamespace(input_tokens=100, output_tokens=50),
    )


ANGLE = {
    "edge": "大家默认访谈按项目做", "thesis": "小团队的用户访谈应按周固定",
    "one_big_idea": "固定节奏胜过按需访谈", "angle_type": "actionable",
    "why_now": "年底规划", "reader_payoff": "一个可执行的节奏",
    "human_evidence_needed": ["你访谈过的团队数"], "risk": "样本偏差",
    "edge_strength": 2, "lens_fit": 3, "market_signal": 2, "evidence_availability": 2, "timeliness": 1,
}

RESEARCH = {
    "findings": [{
        "id": "x", "claim": "持续访谈提高产品决策质量", "quote_verbatim": "Talk to customers weekly",
        "url": "https://example.com/a", "date": "2024-01-01", "source_type": "primary",
        "read_level": "full_text", "speaker": "Teresa Torres", "attribution": "own_words", "access_path": "web_fetch_full_page",
        "confidence": "high"}, {
        "id": "y", "claim": "某聚合站说 80% 团队不做访谈", "quote_verbatim": "80% never",
        "url": "https://agg.example.com", "date": "2023", "source_type": "aggregator",
        "read_level": "snippet", "speaker": "n/a", "attribution": "n/a", "confidence": "low", "access_path": "search_result_snippet"}],
    "counter_evidence": [{"claim": "早期团队更该看数据", "url": "https://example.com/c"}],
    "human_todo": ["约 2 位创始人访谈"], "not_found": [],
}

OUTLINE = {
    "title_options": ["每周一次访谈"], "top_of_page": {
        "context": "小团队", "questions": ["访谈该怎么安排？"], "answer": "按周固定"},
    "thesis": "小团队的用户访谈应按周固定", "one_big_idea": "固定节奏胜过按需访谈",
    "sections": [
        {"heading": "问题", "one_sentence": "按项目访谈会断", "source_ids": ["f01"], "story_ids": [],
         "is_opinion": False, "serves_big_idea": True},
        {"heading": "我的做法", "one_sentence": "每周二下午", "source_ids": [], "story_ids": ["s_001"],
         "is_opinion": False, "serves_big_idea": True}],
    "off_topic_branches": [], "core_image": "坚持率对比图", "next_start_hint": "从读者那封邮件写起",
}

STRANGER = {"core_claim_restated": "访谈要按周固定", "missing_premises": [], "jumps": [],
            "misreadings": [{"misreading": "以为反对项目制访谈", "blocked_in_text": True}]}

CRITIQUE = {
    "usefulness": [{"claim": "按周固定", "true": 2, "important": 2, "novel": 1, "strong": 1,
                    "overclaim": False}],
    "honesty": {"fair": True, "accurate": True, "persuasive_to_fair_observers": True, "notes": ""},
    "off_topic_paragraphs": [],
    "dry_tests": [{"sentence": "每周二下午我打三个电话", "visualize": True, "falsify": True,
                   "only_you": True}],
    "reader_reactions": [{"paragraph": 1, "label": "Interesting", "note": ""},
                         {"paragraph": 2, "label": "Fine", "note": ""}],
    "briars": [{"sentence": "这很重要", "reason": "含糊"}],
    "checkable_claims": [{"text": "Talk to customers weekly", "kind": "quote", "has_source_marker": True}],
}

JUDGE = {"rank_vs_anchors": "介于两者之间偏好", "strengths_with_quotes": [],
         "weaknesses_with_quotes": [], "score": 0.72, "pass": True}

ADAPT = {
    "x_posts": [
        {"text": "我访谈了 40 个小团队。按项目做访谈的，三个月后几乎都停了。你们是按周还是按项目？",
         "idea": "按项目会断", "reply_hook": "按周还是按项目？", "visualize": True, "falsify": True,
         "only_you": True},
        {"text": "读这篇 https://example.com #产品", "idea": "导流", "reply_hook": "",
         "visualize": False, "falsify": False, "only_you": False}],
    "notes": [{"text": "固定节奏胜过按需访谈：每周二下午三个电话，比任何项目制访谈都管用。", "type": "金句"}],
    "substack": {"title_variants": ["每周一次访谈", "别再按项目做访谈"], "subtitle": "小团队版",
                 "cta": "订阅获取访谈模板"},
}


THREAD = {"parts": ["按项目做访谈的团队，三个月后几乎都停了。为什么？", "因为项目会结束，节奏不会。",
                   "我的做法：每周二下午三个电话。", "你可以从下周二开始。"],
          "first_post_standalone": True, "hook": "为什么会停", "cta": "全文在这里"}

ARTICLE = {"title": "每周一次访谈", "body_markdown": "我访谈过的 40 个小团队里，按项目做的几乎都停了 [f01]。\n\n## 做法\n每周二下午。",
           "opening": {"proof": "40 个团队", "promise": "一个能坚持的节奏", "plan": "三步"},
           "promo_post": "按项目做访谈的团队，三个月后几乎都停了。我写了一篇长文讲怎么改。"}

MEDIUM = {"title": "Run Customer Interviews Every Week, Not Per Project",
          "subtitle": "A cadence small teams can keep", "cover_note": "no cover",
          "cta": "Get the template in my newsletter", "target_publications": ["The Startup（需确认）"],
          "first_hand_experience_present": True, "derivative_risk": False}

RETRO = {"top_patterns": [{"platform": "x", "pattern": "以反问结尾", "evidence": ["v1"]}],
         "bottom_patterns": [], "recurring_edits": [], "proposals": [
             {"target": "voice/profile.yaml", "change": "x tone 更口语", "rationale": "前 20% 都口语"}],
         "sample_size_warning": "样本很少"}


class FakeStream:
    def __init__(self, msg):
        self.msg = msg

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def get_final_message(self):
        return self.msg


class FakeMessages:
    def __init__(self, owner):
        self.owner = owner

    def stream(self, **params):
        self.owner.calls.append(params)
        system = params["system"]
        fmt = params["output_config"].get("format")
        if "子问题" in system:
            out = {"questions": ["访谈频率与决策质量", "小团队访谈成本"]}
        elif "选题角度" in system:
            out = {"angles": [ANGLE, dict(ANGLE, one_big_idea="另一个角度")]}
        elif "引用绑定员" in system:
            out = RESEARCH
        elif "研究子 Agent" in system:
            return FakeStream(_msg("研究笔记：Teresa Torres 说 Talk to customers weekly（https://example.com/a）"))
        elif "论点和提纲" in system:
            out = OUTLINE
        elif "对作者一无所知" in system:
            out = STRANGER
        elif "严格的编辑" in system:
            out = CRITIQUE
        elif "事实核查员" in system:
            items = json.loads(params["messages"][0]["content"])
            out = {"verdicts": [{"index": it["index"], "verdict": self.owner.entail_verdict,
                                 "attribution_ok": True, "reason": ""} for it in items]}
        elif "原子事实" in system:
            draft = params["messages"][0]["content"]
            sid = (re.findall(r"\[(f\d{2})\]", draft) or [""])[0]
            out = {"facts": [{"fact": "按周固定访谈比按项目访谈更能坚持", "sentence": "按周固定访谈比按项目访谈更能坚持",
                              "source_id": sid, "kind": self.owner.fact_kind, "speaker": "Teresa Torres"}]}
        elif "卡一下" in system:
            self.owner.briars_calls += 1
            out = {"briars": [{"sentence": "这很重要。", "reason": "含糊"}]
                   + ([{"sentence": f"偶发{self.owner.briars_calls}", "reason": "x"}])}
        elif "访谈整理员" in system:
            out = {"reactions": [{"passage": "我每周二", "label": "Interesting", "note": ""},
                                 {"passage": "然后然后", "label": "Repeated", "note": "重复"}],
                   "follow_up_questions": ["坚持了多久？"],
                   "draft_markdown": self.owner.interview_draft}
        elif "回收一条" in system:
            out = {"rewrites": [{"text": self.owner.recycle_text, "new_angle": "讲一次失败",
                                 "reply_hook": "你停过吗？", "visualize": True, "falsify": True, "only_you": True}]}
        elif "开放题回答" in system:
            out = {"themes": [{"question_id": "q03", "theme": "时间不够", "approx_count": 2,
                               "quotes": ["没时间约人", "这句根本不在回答里"]}]}
        elif "读者调查" in system:
            out = {"title": "访谈习惯调查", "intro": "5 分钟",
                   "questions": [
                       {"id": "x", "text": "你多久做一次用户访谈？", "type": "single",
                        "options": ["每周", "每月", "按项目", "从不"], "why": "行为"},
                       {"id": "x", "text": "你对现在的访谈节奏满意吗？", "type": "scale",
                        "options": ["1", "2", "3", "4", "5"], "why": "态度"},
                       {"id": "x", "text": "最大的障碍是什么？", "type": "open", "options": [], "why": "开放"}],
                   "bias_notes": ["只有愿意填问卷的读者会回答"]}
        elif "过度夸奖" in system:
            out = dict(JUDGE, score=self.owner.judge_score(params))
        elif "平台原生变体" in system:
            user = params["messages"][0]["content"]
            if "X Thread" in user:
                out = THREAD
            elif "X Article" in user:
                out = ARTICLE
            elif "Medium 包装" in user:
                out = MEDIUM
            else:
                out = ADAPT
        elif "月度复盘" in system:
            out = RETRO
        elif "替他发表" in system:
            return FakeStream(_msg("# 草稿\n\n按周固定访谈 [f01]。\n\n[TK: 作者定结尾]"))
        else:
            raise AssertionError(f"unexpected system prompt: {system[:40]}")
        assert fmt is not None, "结构化输出调用必须带 output_config.format"
        return FakeStream(_msg(json.dumps(out, ensure_ascii=False)))


class FakeClient:
    def __init__(self, judge_score=None):
        self.calls: list[dict] = []
        self.fact_kind = "fact"
        self.entail_verdict = "supported"
        self.briars_calls = 0
        self.interview_draft = "# 访谈稿\n\n我每周二下午打三个电话。"
        self.recycle_text = "我也停过一次访谈。那次是因为项目结束了，节奏就断了。你停过吗？"
        self._judge = judge_score or (lambda params: 0.72)
        self.beta = SimpleNamespace(messages=FakeMessages(self))

    def judge_score(self, params):
        return self._judge(params)


def _no_network(vault):
    """测试里不回原网页抓取引语。"""
    p = vault.root / "agent.yaml"
    p.write_text(p.read_text(encoding="utf-8").replace("refetch_quotes: true", "refetch_quotes: false"),
                 encoding="utf-8")
