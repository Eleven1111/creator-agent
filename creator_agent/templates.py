"""`ca init` 写入的知识库模板（手册“知识库与记忆”“数据结构”两节，P0 建库）。

全部是示例内容，作者必须改成自己的。标了 TODO 的地方不改，后续阶段会给出提醒。
"""

AGENT_YAML = """\
# agent.yaml —— 运行配置
model: claude-opus-5-5          # 所有阶段默认用同一个模型
max_tokens: 32000
use_fallbacks: true              # 服务端 refusal fallback（fallbacks="default"）
web_search_max_uses: 8           # S2 单 Agent 研究的搜索次数上限
effort:                          # low | medium | high | xhigh | max
  default: high
  adapt: medium
  eval: medium
review:
  pass_threshold: 0.6            # 反恭维评审分 >= 阈值 且 无硬拦截 才算通过
  factcheck: true                # P3：SAFE 式逐条核查（拆原子事实 → 对照来源摘录判断是否支撑）
  refetch_quotes: true           # P3：引语回原网页逐字核对（只读 GET）
  briars_samples: 3              # P3：拔刺独立采样次数，至少 2 次命中才进报告
  style_drift_sigma: 2.0         # P3：风格特征偏离往期均值超过 2σ 视为漂移
  style_min_docs: 5              # 往期文章（archive/ + voice/exemplars/）少于 5 篇时不做漂移检测
research:
  mode: single                   # single | multi（编排者-工作者，约 15 倍 token；离线测试证明有提升再开）
"""

PROFILE_YAML = """\
# voice/profile.yaml —— 声音档案（P0 完成标准：作者读它时觉得“这就是我”）
author: "TODO 你的名字"
identity: "TODO 一句话：你是谁，写给谁"
lens: "TODO 你的固定视角：每个话题都回到……"
persona: "TODO 理想读者：职业、处境、他最想解决的问题"
rhythm: systems                  # systems（周母题、批量）| obsession（有东西才写）
default_draft_mode: A            # A：人写核心论证 | B：Agent 按提纲起草，人重写关键段 | I：访谈
languages:
  hub: zh                        # 母稿语言
  medium: en_rewrite_only        # none | en_rewrite_only：只有你本人写了 hubs/<id>/final_en.md 才生成 Medium 包装
formats: [x_post, substack_note, x_thread, x_article, medium_story]   # S6 默认生成的变体
x_article_mode: full             # full（全文）| condensed（精简版并链回母稿）
accounts:
  x_premium: false               # X Articles 需要有效的 Premium 订阅
core:
  person: first_person_singular
  sentence_length: {median_chars: 28, p90_chars: 60}
  paragraph_max_sentences: 4
  signature_moves: ["TODO 例：开头用一个读者原话提问"]
  closings: "TODO 例：以一个反问或下周预告结束，不做总结段"
  banned_endings: ["总之", "综上所述", "In summary", "In conclusion"]
platform_deltas:
  x:     {max_weighted_chars: 280, hashtags: none, tone: "更锋利，一帖一事"}
  notes: {max_sentences: 5, tone: "像对朋友说一句真心话"}
disclosure_line: "研究与校对由 AI 辅助；观点、经历与文字出自我本人。"
medium_disclosure_line: "This story was written with the assistance of an AI writing program."   # 仅在含 AI 辅助生成的文字时，放进前两段
canonical_base_url: "https://TODO.substack.com/p/"
"""

NEVER_MD = """\
# never.md —— 禁用词与禁用结构（lint 会逐行读取以“- ”开头的条目）
# 每行一条；中文 AI 腔词表需要你按自己的口味补充。

- 赋能
- 抓手
- 底层逻辑
- 毋庸置疑
- 值得注意的是
- 不难发现
- 让我们一起
- 深入探讨
- 在当今快速发展的
- delve
- tapestry
- in today's fast-paced world
- it's worth noting
"""

DELIBERATE_BREAKS_MD = """\
# deliberate_breaks.md —— 有意的破格（lint 跳过这些短语）
# 例：你就是喜欢用“说白了”，那就写在这里。

"""

STANCES_MD = """\
# stances.md —— 已公开表态的立场（模式 B 起草只能使用这里有的立场）

- TODO 例：小团队的用户访谈应该按周固定，而不是按项目
"""

STORIES_MD = """\
# stories.md —— 作者亲口确认过的经历（Agent 只能从这里引用经历）
# 格式：- [s_001] 2024-03 | 可公开程度: public|anonymized|private | 经历描述

- [s_001] TODO | 可公开程度: public | 例：2024 年我访谈了 40 个小团队……
"""

PLATFORM_SUBSTACK = """\
# platforms/substack.yaml —— 平台规则（按 2026-11-03 核实结果；超过 90 天请重新核对）
platform: substack
policy_version: "2026-11"
verified_at: "2026-11-03"
posting_api: none                # 没有官方发文接口；MVP 全部人工粘贴发送
official_mcp: read_only_stats_bestsellers_only
canonical_settable: false
notes:
  native_scheduling: true
  weekly_target: [3, 10]
ai_transparency:
  reader_scan: true
  author_prescan: optional
  how_i_make_this_statement: optional
"""

PLATFORM_X = """\
# platforms/x.yaml —— 平台规则（按 2026-11-03 核实结果；超过 90 天请重新核对）
platform: x
policy_version: "2026-11"
verified_at: "2026-11-03"
max_weighted_chars: 280          # 非 Premium；CJK 字符按 2 计，URL 按 23 计
max_cashtags_per_post: 1
api:
  price_usd: {post_create: 0.015, post_create_with_url: 0.20, owned_reads: 0.001}
  reply_only_if_summoned: true
  like_follow_quote_write: removed
monetization_excluded_topics: ["如何在 X 上赚钱", "创作者分成", "creator revenue", "monetize on x"]
min_gap_hours_same_account: 3
"""

PLATFORM_MEDIUM = """\
# platforms/medium.yaml —— 平台规则（按 2026-11-03 核实结果；超过 90 天请重新核对）
platform: medium
policy_version: "2026-11"
verified_at: "2026-11-03"
rules:
  non_english_general_distribution: false
  non_english_boost: false
  ai_generated_paywall_allowed: false
  ai_generated_distribution: network
  ai_assisted_text_requires_disclosure: true      # 前两段内一句
  boost_nomination_program: closed_2026-05-31
  friend_link_member_reads_count: true
mpp_eligibility:
  mainland_china_eligible: false                  # 港澳台在列
api:
  supported: false
  new_tokens: false
publish_default: human_import
canonical_setting_path: "More settings > Advanced Settings > This story was originally published elsewhere"
"""

IDEAS_JSONL = ""

TESTSET_README = """\
# evals/ —— 离线测试集（P1 完成标准：评审在测试集上能区分好稿和差稿）

- anchors/good_*.md、anchors/bad_*.md：作者认定的好稿与差稿，S5 反恭维评审用作锚点（各至少 2 篇）。
- testset.jsonl：每行 {"id": "...", "path": "evals/cases/xxx.md", "label": "good|bad"}，建议 20 条以上。
- 运行 `ca eval` 输出好稿/差稿的平均分、阈值准确率和成对排序准确率（AUC）。
"""
