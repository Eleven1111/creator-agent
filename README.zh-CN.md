# creator-agent · 多平台创作 Agent（P1–P4）

[English](README.md) · **简体中文**

> **第一次用？先看 [从零开始的使用教程](TUTORIAL.md)。**

一个帮你写 newsletter 和社媒内容的创作 Agent：选题、研究、提纲、评审、事实核查、多平台改编、数据复盘。它是研究助理和编辑，不是代笔；**它不会替你发布任何东西**，所有发布都由你本人在各平台客户端完成。

设计依据是调研 Substack、X、Medium 头部创作者的方法论后写成的《[三平台创作 Agent 手册·核实版](docs/handbook/三平台创作Agent手册核实版.md)》，调研笔记和各版手册见 [docs/](docs/README.md)。本工具按手册第三部分的路线图实现了 P0–P4。

**P1** 的范围：一个母站（Substack）加两个辐条（X 单帖、Substack Notes）；研究用单 Agent 加搜索；全部人工发布；带 UTM 生成器、离线测试集和人工编辑时长记录。

**P2** 在此基础上加了 X Thread、X Articles、Medium 英文版三种变体；所有变体都先进待审队列，你可以直接改稿，审批后生成发布包；另外加了只读的指标回流、`edit_diffs` 采集和月度复盘。本工具不调用任何平台的写入接口。

**P3** 加强了研究和评审：研究可以切换成多个子 Agent 并行（默认关闭），每条引语回原网页逐字核对，拔刺改成 3 次独立采样，新增风格漂移检测、访谈模式整理口述稿、短帖晋升长文（R1）和老帖换角度重写（R2）。

**P4** 把整条流程编成 LangGraph 图（每个闸口是 `interrupt()`，SQLite 持久化，关掉终端明天接着来），加了本地语音转写、读者调查的设计与分析、作者盲评和合规审计。

它是一个**工作流**，不是自主 Agent：每个阶段一两次确定的模型调用，结果写成 markdown 交给你审，你用 `ca approve` 放行后才能进下一步。

```
S1 选题定角 ─H1→ S2 研究取证 ─H2→ S3 论点提纲 ─H3→ S4 起草 → S5 编辑评审 ─H4→
S6 平台适配（x_post / substack_note / x_thread / x_article / medium_story + Substack 发布包）
   → 待审队列（你改 variants/<id>.md）─H5（重跑检查）→ publish_kit.md → 你本人发布 → ca published
   → S8 指标回流（只读）→ 月度复盘 ─H7→ R1 选题进选题池
```

## 安装

```bash
pip install -e '.[dev,graph]'
```

凭证：设 `ANTHROPIC_API_KEY`，或先运行 `ant auth login`。默认模型 `claude-opus-5-5`，可在知识库的 `agent.yaml` 里改。

## 第一次使用（P0 建库）

```bash
ca init ~/creator-vault
export CA_VAULT=~/creator-vault
```

然后按提示完成手册 P0 的完成标准：

| 文件 | 要做的事 |
|---|---|
| `voice/profile.yaml` | 写身份、固定视角、理想读者、句长、结尾习惯、平台差异 |
| `voice/never.md` / `deliberate_breaks.md` | 禁用词（命中即拦截）/ 有意破格（lint 跳过） |
| `voice/stances.md` / `stories.md` | 已表态的立场 / 亲口确认过的经历（Agent 只能引用这里的） |
| `voice/exemplars/*.md` | 5–15 段你自己的范文（模式 B 起草时学节奏用） |
| `evals/anchors/good_*.md`、`bad_*.md` | 你认定的好稿、差稿各 ≥2 篇，用来校准评审打分 |
| `evals/testset.jsonl` | ≥20 条离线测试用例（与锚点分开） |

```bash
ca import-rss https://你的名字.substack.com/feed     # 往期文章进 archive/，S1 用来查重
ca idea add "小团队要不要做用户访谈？" --edge "大家默认按项目做，我怀疑"
```

## 一篇稿子的完整流程

```bash
ca new idea_0001 --angles                 # 建母稿并跑 S1 → hubs/<id>/angles.md
ca approve <id> H1 --angle 2 --excitement 4 --edge "一句话写下你的 edge"
ca research <id>                          # S2：拆子问题 → web_search → 引用绑定 → research.md
ca approve <id> H2 --confirm              # 按 research.md 末尾的清单查过
ca outline <id>                           # S3：页顶简报 + 逐段一句话提纲 → outline.md
ca approve <id> H3
ca draft <id>                             # S4 模式 A：只给素材卡片 cards.md，你自己写 draft.md
ca review <id>                            # S5：lint + 陌生人重读 + 编辑评审 + 反恭维打分 → review.md
ca approve <id> H4 --quotes-checked 3 --numbers-checked 2 --ending-ok \
                   --canonical-url https://你的名字.substack.com/p/xxx
ca adapt <id>                             # S6：X 单帖、Notes、Thread、Article（+推广帖）、Medium 包装
# 打开 hubs/<id>/review_queue.md 审稿；想改哪条就直接改 variants/<variant_id>.md
ca approve <id> H5 --variants all         # 用你改后的文字重跑检查，只放行通过的；生成 publish_kit.md
ca due                                    # 接下来 24 小时要你手动发的稿子
# 你本人照 publish_kit.md 在各平台客户端发布，然后：
ca published v_<id>_x_post_01 https://x.com/你/status/...
ca log-edit <id> 45                       # 记录人工编辑分钟数
ca status <id>

# 指标回流（只读）与复盘
ca metrics pull-x --dry-run               # 先估算读取费用
X_BEARER_TOKEN=... ca metrics pull-x      # 用 GET /2/tweets 拉已发布帖子的公开指标
ca metrics add v_<id>_substack_note_01 free_subs=3 restacks=5     # Substack / Medium 手工录入
ca metrics import export.csv --source substack_export              # CSV：需有 variant_id 或 url 列
ca report --month 2026-11
ca retro 2026-11                          # 前/后 20% 特征、你反复做的修改、修改提议、R1/R2 候选
ca retro-approve 2026-11 --r1 all         # H7：把 R1 候选写进选题池（声音档案由你手动改）
```

`ca draft <id> --mode B` 会让 Agent 按批准过的提纲起草，但它不会编造经历、数字和立场，这些位置一律留 `[TK: ...]`。草稿里只要还有 TK，`ca review` 就直接拦截，不会调用模型。

## 每个阶段对应手册的哪条规则

| 阶段 | 实现了什么 | 手册依据 |
|---|---|---|
| S1 | 往期查重；3–5 个角度，每个带 edge、可证伪论点、Rule of One、需要你提供的证据；按排序表算预排序分 | S1 排序表（兴奋度 0.30 必须由你填） |
| H1 | 不填兴奋度、写不出 edge 就不放行 | “写不出 edge 的题目退回选题池” |
| S2 | 拆子问题 → `web_search` 研究 → 单独一次调用做引用绑定；snippet、聚合站、AI 蒸馏来源标为弱来源 | 编排者-工作者的简化版；`read_level`、`attribution` 字段 |
| S3 | 页顶简报（One-Sheet）、逐段一句话、来源 id 校验、跑题分支、核心画面 | Perell、Doomberg、PG |
| S4 | 模式 A 素材卡片 / 模式 I 访谈提问 / 模式 B 带 TK 的草稿 | 三种起草模式 |
| S5 | TK、禁用词硬拦截；AI 腔密度、对冲词、感叹号、总结式结尾、引言占比；陌生人重读与误读；有用性四因子、诚实三问、Dry 三问、CRIBS 维度、拔刺；带锚点的反恭维打分；无来源的引语和数字硬拦截 | S5 评审表（MVP 版） |
| H4 | 评审后改过稿就要重评；核对数量不能少于评审提取的引语和数字数；未通过评审必须写理由 | H4 人工核对清单 |
| S6 | X 加权字数（汉字算 2）、根帖无链接、无 hashtag、无 @、cashtag ≤1、Dry 至少 2 项、有回复钩子、不碰变现话题、**变体里的数字必须出现在定稿里**；每个变体带 UTM；X 单帖分散在一周，Notes 每天至多一条 | G-XP、G-SN、UTM 规范 |
| S6 · Thread | 首帖能独立成立、每帖不超字数、链接只在末帖（带 `utm_medium=thread_end`） | G-XT |
| S6 · Article | 开头按 Proof → Promise → Plan 重写、不新增数字、账号要有 Premium；附一条推广帖，推广帖跟着文章一起审批 | G-XA |
| S6 · Medium | 只在你写了 `final_en.md` 且起草模式是 A/I 时生成；只做包装不改正文；检查英文、亲身经验、非衍生、CTA 次要、不写 Medium 元内容、canonical、出版物、AI 披露 | G-MD；Medium 非英文不进 General/Boost、B 模式稿不发 |
| H5 | 读取你改后的 `variants/<id>.md` 重跑确定性检查；记录修改对到 `voice/edit_diffs/`；生成 `publish_kit.md`（按时间排序的可复制正文 + 每个平台的手动步骤） | H5 批量审批 |
| 发布 | 不调用任何平台写入接口；`automated_interaction` 永远是 `none` | 设计原则：发布永远由人完成；另外 X 自助档 API 限制互动、Substack 无发文 API |
| S8 | X 用只读 `GET /2/tweets?tweet.fields=public_metrics` 拉指标；Substack、Medium 手工录入或导 CSV；按平台×体裁汇总 | 指标口径表 |
| 复盘 | 每个平台各自排出前/后 20%；模式 B 和你改过的变体算编辑比；R1：回复率 > 30 日中位数 × 2；R2：≥90 天、前 20%；修改提议只写进报告 | 反馈闭环；“声音档案的修改永远由人一票否决” |

## 离线测试集

```bash
ca eval
```

只跑反恭维评审，输出好稿和差稿的平均分、阈值准确率和成对排序准确率（AUC）。P1 的完成标准是“评审能区分好稿和差稿”，这里用 AUC ≥ 0.8 作为判断线（`discriminates: true`）。

## P3 新增

```bash
ca interview <id> --transcript 口述.md    # 模式 I：按提纲整理你的口述，只调顺序、删冗；标 CRIBS；标出可能新增的句子和数字
ca promote v_<id>_x_post_03              # R1：把表现好的短帖晋升为长文母稿，S1 会把它的表现当作市场信号
ca recycle v_<id>_x_post_01              # R2：≥90 天的高表现短帖，用新角度重写（与已发版本相似度 ≥0.5 会被拦下）
ca progress                              # P3 完成度：支撑率 ≥95%、编辑时长是否下降、R1 长文数 ≥1
```

| 能力 | 做法 | 开关（agent.yaml） |
|---|---|---|
| 编排者-工作者研究 | 子问题并行交给工作者，每个工作者用 `web_search` + `web_fetch` 读全文；各自做引用绑定后合并、去重；原始笔记存 `research_workers/` | `research.mode: single \| multi`，默认 single。手册规则：离线测试证明单 Agent 会漏掉关键信息再开（约 15 倍 token） |
| 信源字段 | 每条发现记录 `access_path`（读了整页 / 只看到搜索摘要 / API·RSS / PDF）和 `attribution`（本人原话 / 转述 / 主持人复述） | — |
| SAFE 式逐条核查 | 把稿子拆成原子事实 → 只根据来源摘录判断 supported/partial/unsupported 和归属 → 引语回原网页逐字比对（只读 GET） | `review.factcheck`、`review.refetch_quotes` |
| 拔刺采样 | 3 次独立采样，≥2 次命中的句子才进报告 | `review.briars_samples` |
| 风格漂移 | 用 `archive/` 和 `voice/exemplars/` 算句长、段长、功能词、标点的基线，偏离 >2σ 视为漂移；往期文章少于 5 篇时不检测 | `review.style_drift_sigma`、`review.style_min_docs` |

逐条核查和风格漂移不通过时，评审结论是“未通过”，但不是硬拦截：你可以改稿重评，也可以在 H4 用 `--override-reason` 写明理由后定稿。引语或数字只有弱来源支撑、原网页找不到引语、归属不对，都算核查不通过；原网页打不开时只提示，交给你在 H4 人工核对。

## P4 新增

```bash
pip install -e '.[graph]'                 # ca flow 需要
pip install -e '.[voice]'                 # ca interview --audio 需要（本地转写，不上传音频）

# 1) LangGraph 编排：一条命令走到下一个闸口，停下等你
ca flow start "小团队要不要做用户访谈？"
ca flow resume <id> --set angle=2 excitement=4 edge="大家默认按项目做"   # H1
ca flow resume <id> --set confirm=true                                  # H2
ca flow resume <id>                                                     # H3
# 写好 hubs/<id>/draft.md 后：
ca flow resume <id> --do done                                           # DRAFT → S5 评审
ca flow resume <id> --set quotes_checked=3 numbers_checked=2 ending_ok=true canonical_url=https://...   # H4
ca flow resume <id> --set variants=all                                  # H5 → publish_kit.md
ca flow status <id>
# 不满意可以退回：H1–H3、H5 用 --do redo 重跑上一阶段；H4 用 --do revise 回去改稿

# 2) 语音访谈
ca interview <id> --audio 口述.m4a --whisper-model small

# 3) 读者调查
ca survey design "了解读者做用户访谈的频率和障碍" --topic "每周一次访谈" -n 10
ca survey analyze <survey_id> responses.csv

# 4) P4 完成标准
ca blind prepare --ai <hub1>,<hub2> --human 旧文1.md,旧文2.md   # 去掉来源标记后打乱，你在 ratings.csv 盲打分
ca blind score <batch>
ca audit                                  # 每次发布都经 H5 批准且晚于批准时间、没有自动互动、平台规则 90 天内核对过
```

| 能力 | 做法 |
|---|---|
| 图编排 | 节点 S1–S6 加人工节点 H1、H2、H3、DRAFT、H4、H5；状态存在 `runs/flow.sqlite`，线程 id 就是母稿 id。闸口规则与 `ca approve` 完全相同；已用 `ca approve` 批过的闸口会被跳过；输入不合法时带着错误信息回到同一闸口，不会中断流程。图在 H5 生成发布包后结束，**发布仍由你本人完成** |
| 语音转写 | faster-whisper 在本地转写，带时间戳，交给访谈模式整理；没装就提示你用外部工具转成文字稿 |
| 读者调查 | 问卷按“一题一事、不诱导、先行为后态度、开放题 ≤3”设计，附自选样本偏差提醒；分析时选择题和量表题用确定性统计，开放题由模型归纳主题，**每条引用都逐字核对是否真在回答里**，对不上的丢掉；样本少于 30 时提示 |
| 盲评 | 去掉 `[fNN]`、TK 和 AI 披露行后打乱；对照表存在 `.key.json`，打分前不要打开 |
| 审计 | 检查已发布变体：发布渠道是 manual、有 H5 批准且发布时间晚于批准时间、母稿 H1–H5 齐全、`automated_interaction` 为 none；平台规则 90 天内核对过 |

**手册 P4 里刻意没做的两项：** 接排期工具 API（如 Typefully）、用 cookie 调非官方接口建 Substack 草稿。前者会替你定时发布，后者有违反服务条款的风险，而且两者都要往平台写入，与“所有发布都由人完成”的设计原则冲突。

## 和手册 P2 的差异

- **不接 X 发帖 API，也不实测"API 自回复"和 Articles 的 API 计费**：本工具的发布全部由人完成，这几项就没有必要了。Thread 和 Article 都由你在 X 客户端里粘贴发布。
- **X 指标用 app-only Bearer Token 读公开指标**：官方价目表里读自己帖子的 Owned Reads 是 $0.001/条，但用 Bearer Token 能否按这个价计费尚未核实，所以 `--dry-run` 按 $0.005/条保守估算。
- **Substack 导出 CSV 的列名没核实**：导入器只要求有 `variant_id` 或 `url` 列，其余数值列都当作指标。

## 之后可以做的

- 用真实数据跑通后再调：评审阈值、风格漂移的 σ、R1 的“2 倍中位数”这些参数目前都是手册里的默认值。
- 盲评目前是 1–5 分的均值比较，样本多了以后可以换成成对比较。

## 开发

```bash
pytest -q
```

测试用假客户端覆盖了完整流水线、闸口顺序、TK 拦截、来源 id 校验、改编不得新增数字、X 加权字数、UTM、测试集打分，以及 P2 的五种变体、Medium 跳过条件、改稿后重检与修改对、推广帖跟随母体、只读 X 指标、CSV 导入、月度复盘与 R1 入池，以及 P4 的图编排（跨实例持久化、非法输入回到闸口、redo / revise、跳过已批闸口、全程不发布）、本地转写、调查统计与引用核对、盲评和审计，以及 P3 的多 Agent 研究去重、逐条核查与回原网页比对、弱来源拦截、拔刺交叉采样、风格漂移、访谈整理的新增检测、R1 晋升、R2 相似度拦截和完成度统计。**这个版本还没有用真实 API 跑过**，第一次真实运行时请留意各阶段的结构化输出是否符合预期。

## 许可

[MIT](LICENSE)
