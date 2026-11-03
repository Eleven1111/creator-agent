# creator-agent 从零开始使用教程

这份教程带你从一台什么都没装的电脑开始，走到“第一篇稿子发出去、数据收回来、月底做复盘”。不需要会编程，只需要会复制粘贴命令。

> **先记住三件事**
> 1. 它是你的研究助理、编辑和改编员，**不是代笔**。默认模式下正文由你写。
> 2. 每一步都要你点头（`ca approve` 或 `ca flow resume`），它才会往下走。
> 3. **它不会替你发布任何东西。** 它只生成稿子和发布包，最后一步永远是你本人在 Substack、X、Medium 的客户端里发。

---

## 目录

1. [准备工作](#1-准备工作)
2. [安装](#2-安装)
3. [建知识库（P0）](#3-建知识库p0一次性大约-23-小时)
4. [校准评审](#4-校准评审一次性大约-1-小时)
5. [写第一篇：逐步命令版](#5-写第一篇逐步命令版)
6. [写第一篇：一条龙版（ca flow）](#6-写第一篇一条龙版ca-flow)
7. [审稿、改稿、手动发布](#7-审稿改稿手动发布)
8. [收数据](#8-收数据)
9. [月度复盘与选题回流](#9-月度复盘与选题回流)
10. [进阶功能](#10-进阶功能)
11. [每周节奏建议](#11-每周节奏建议)
12. [配置速查](#12-配置速查)
13. [常见问题](#13-常见问题)
14. [文件地图](#14-文件地图)

---

## 1. 准备工作

| 需要 | 说明 | 必须？ |
|---|---|---|
| Python 3.10 或更新 | 终端输入 `python3 --version` 查看 | 必须 |
| Anthropic API key | 在 console.anthropic.com 创建；所有模型调用都靠它 | 必须 |
| 一个 Substack | 当母站。没有的话先注册一个 | 必须 |
| X 账号 | 发单帖、Thread、Article。Article 需要 Premium | 可选 |
| X 开发者 Bearer Token | 只用来**读取**你已发帖子的公开数据，按次计费 | 可选 |
| Medium 账号 | 只有你会自己写英文版时才有用 | 可选 |

> **中国大陆作者注意**（依据手册核实版）：Medium 的非英文文章既拿不到 General 分发也拿不到 Boost，中国大陆也不在 Medium Partner Program 的收款国家里（港澳台在）。所以建议：**中文母稿发 Substack，X 用来试题，Medium 只发你亲手写的英文版。**

**大概花多少钱？** 每篇稿子会调用十几次模型（研究、提纲、评审、核查、改编），具体费用取决于文章长度和你开不开多 Agent 研究。每次调用的 token 用量都记在 `runs/logs/`，跑完第一篇看一眼就有数了。

---

## 2. 安装

```bash
git clone https://github.com/Eleven1111/creator-agent.git
```

```bash
cd creator-agent
```

建议用虚拟环境，避免和系统 Python 打架：

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

Windows 上是 `.venv\Scripts\activate`。

安装（`graph` 是一条龙流程需要的，强烈建议装上）：

```bash
pip install -e '.[dev,graph]'
```

想用语音访谈（本地转写，不上传音频）再加装：

```bash
pip install -e '.[voice]'
```

设置 API key：

```bash
export ANTHROPIC_API_KEY=sk-ant-你的key
```

检查是否装好：

```bash
ca --help
```

能看到一长串命令就说明装好了。可以顺手跑一下自带测试：

```bash
pytest -q
```

---

## 3. 建知识库（P0，一次性，大约 2–3 小时）

知识库是一个普通文件夹，里面全是 markdown 和 yaml，你可以用任何编辑器打开。**它决定了 Agent 写出来像不像你**，这一步别偷懒。

### 3.1 创建

```bash
ca init ~/creator-vault
```

```bash
export CA_VAULT=~/creator-vault
```

建议把 `export CA_VAULT=~/creator-vault` 和 `export ANTHROPIC_API_KEY=...` 写进 `~/.zshrc` 或 `~/.bashrc`，以后不用每次输入。

### 3.2 填声音档案 `voice/profile.yaml`（最重要）

打开文件，把所有 `TODO` 换成你自己的内容。示例：

```yaml
author: "林小满"
identity: "前产品经理，写给 0→1 阶段的产品负责人"
lens: "每个话题都回到：这对一个 5 人团队本周的决策意味着什么"
persona: "刚拿到种子轮的产品负责人，团队 3–8 人，最缺的是时间和判断力"
rhythm: systems            # systems：每周一篇母稿、批量拆短帖；obsession：有东西才写
default_draft_mode: A      # A：你写正文（默认，推荐）；B：Agent 起草你重写；I：你口述 Agent 整理
languages:
  hub: zh
  medium: en_rewrite_only  # 不打算发 Medium 就改成 none
accounts:
  x_premium: false         # 有 X Premium 才改成 true，否则 X Article 会被拦下
core:
  signature_moves: ["开头用一个读者原话提问", "每节结尾给一个可执行的小动作"]
  closings: "以一个反问或下周预告结束，不做总结段"
canonical_base_url: "https://linxiaoman.substack.com/p/"
```

**判断标准**：你自己读一遍，觉得“这就是我”。

### 3.3 填另外四个文件

| 文件 | 填什么 | 为什么重要 |
|---|---|---|
| `voice/never.md` | 你讨厌的词和句式，每行一条，以 `- ` 开头 | 评审时命中就**硬拦截** |
| `voice/deliberate_breaks.md` | 你故意保留的“毛病”，比如口头禅“说白了” | lint 会跳过它们，不会把你的个性当错误 |
| `voice/stances.md` | 你公开表过态的立场 | 模式 B 起草时，Agent 只能用这里的立场 |
| `voice/stories.md` | 你**亲口确认过**的经历，每条带编号和可公开程度 | Agent 只能引用这里的经历，**绝不编造** |

`stories.md` 的格式：

```markdown
- [s_001] 2024-03 | 可公开程度: public | 我访谈了 40 个小团队，按项目做访谈的三个月后几乎都停了
- [s_002] 2025-01 | 可公开程度: anonymized | 一位创始人告诉我……（不写真名）
```

建议至少写 20 条。这是 Agent 最没法替代你的部分，也是 Medium 现行 Boost 标准最看重的“亲身经验”。

### 3.4 放范文

往 `voice/exemplars/` 里放 5–15 段你自己写得最满意的文字，每段一个 `.md` 文件，长文和短帖都要有。Agent 只学节奏和手法，不会复用句子。

### 3.5 导入往期文章

```bash
ca import-rss https://你的名字.substack.com/feed
```

往期文章会进 `archive/`。它有两个用处：选题时查重，避免重复写过的论点；评审时当作“你平时怎么写”的风格基线（至少要 5 篇，风格漂移检测才会启用）。

### 3.6 录入选题

```bash
ca idea add "小团队要不要做用户访谈？" --edge "大家默认按项目做访谈，我怀疑固定节奏才是关键"
```

```bash
ca idea list
```

`--edge` 是这个选题里“别人视为理所当然、你却有疑问”的点。写不出 edge 的选题，到 H1 闸口也会被退回。建议先攒 30 条以上。

---

## 4. 校准评审（一次性，大约 1 小时）

Agent 评审天生爱夸人（Packy McCormick 说 Claude 几乎给他每篇初稿都打 A），所以要给它锚点。

### 4.1 放锚点

在 `evals/anchors/` 放你认定的好稿和差稿，各至少 2 篇：

```
evals/anchors/good_1.md
evals/anchors/good_2.md
evals/anchors/bad_1.md
evals/anchors/bad_2.md
```

差稿可以是你自己不满意的旧稿。少于 2 篇时，评审报告顶部会提醒“评审分没有校准”。

### 4.2 建离线测试集（建议，非必须）

在 `evals/cases/` 放另外 20 篇左右（**不要和锚点重复**），一半你满意、一半不满意，然后在 `evals/testset.jsonl` 每行写一条：

```json
{"id": "c01", "path": "evals/cases/c01.md", "label": "good"}
{"id": "c02", "path": "evals/cases/c02.md", "label": "bad"}
```

跑一下：

```bash
ca eval
```

看输出里的 `pairwise_auc`：0.8 以上（`"discriminates": true`）说明评审分得清好坏。低于 0.8 就换更有代表性的锚点，或者调高 `agent.yaml` 里的 `review.pass_threshold`。

---

## 5. 写第一篇：逐步命令版

适合第一次用，每一步都能看清它做了什么。熟悉以后可以改用第 6 节的一条龙版。

### S1 选题定角 → H1

```bash
ca new idea_0001 --angles
```

会输出一个母稿 ID，比如 `2026w45-idea0001`，后面都用它。下文用 `<id>` 代替。

打开 `hubs/<id>/angles.md`，里面有 3–5 个角度，每个都写了 edge、可以被反驳的论点、需要你提供的证据和风险。挑一个，**亲手**填兴奋度（1–5），并用一句话写下你自己的 edge：

```bash
ca approve <id> H1 --angle 2 --excitement 4 --edge "大家默认按项目做访谈，我怀疑固定节奏才是关键"
```

### S2 研究取证 → H2

```bash
ca research <id>
```

打开 `hubs/<id>/research.md`。每条发现都有原文引语、链接、信源类型，以及是读了整页还是只看到搜索摘要。标着 ⚠️**弱来源**的（只有摘要、聚合站、AI 蒸馏），不能单独支撑数字或引语。文件末尾有一份检查清单，逐条过一遍再批准：

```bash
ca approve <id> H2 --confirm
```

### S3 提纲 → H3

```bash
ca outline <id>
```

打开 `hubs/<id>/outline.md`，看页顶的“一句话答案”对不对，每段一句话的提纲顺不顺，有没有“⚠️ 程序检查”提示的问题。满意就：

```bash
ca approve <id> H3
```

不满意可以直接改 `outline.json` 再批，或者重跑 `ca outline <id>`。

### S4 起草

```bash
ca draft <id>
```

默认是**模式 A**：Agent 不写正文，只生成 `hubs/<id>/cards.md` 素材卡片，每节要说的一句话、可用的引语和链接、可用的经历编号都列在里面。你在 `hubs/<id>/draft.md` 里写正文。

写作时的两条约定：

- 用到研究发现时，在句子后面标 `[f03]` 这样的编号，评审会逐条核对。
- 还没补完的地方写 `[TK: 需要的东西]`。只要稿子里还有 TK，评审就会直接拦下，不会白花模型调用。

其他两种模式：

```bash
ca draft <id> --mode B
```

Agent 按提纲起草，所有经历、数字、立场的位置都留 TK，由你重写关键段落。**模式 B 的稿子不会生成 Medium 版本。**

```bash
ca interview <id> --transcript 我的口述.md
```

模式 I：你对着提纲把想法讲出来（或者直接录音，见第 10 节），Agent 只调顺序、删重复，不添加内容。

写的时候顺手记一下花了多久，这是最便宜的质量信号：

```bash
ca log-edit <id> 90
```

### S5 编辑评审

```bash
ca review <id>
```

打开 `hubs/<id>/review.md`，从上往下看：

| 部分 | 怎么用 |
|---|---|
| 硬拦截 | **必须处理**：TK、禁用词、AI 腔密度过高、引用了不存在的来源编号、没有来源的引语或数字、诚实三问没通过 |
| 未通过 | 逐条核查没过（引语找不到、数字不被支撑、归属不对、只有弱来源）或风格漂移。可以改了重评，也可以在 H4 写明理由后定稿 |
| 陌生人重读 | 一个不认识你的读者会怎么复述你的观点、缺了哪些前提、可能怎么误读 |
| 拔刺 | 3 次独立通读都卡住的句子，优先改 |
| Dry 三问 | 核心句能想象吗？能证伪吗？只有你能说吗？ |
| 读者反应 | 哪些段落让人困惑、重复、无聊 |
| 逐条核查 | 每条事实：是否被来源支撑、引语在原网页能否找到 |
| 风格漂移 | 和你往期文章比，句长、段长、用词是否明显变了 |

改完 `draft.md` 要重新运行 `ca review <id>`：评审之后改过稿，H4 会拒绝。

### H4 定稿

先按 `review.md` 末尾的“H4 人工核对清单”，把每条引语、每个数字**亲自回原链接核对**，然后：

```bash
ca approve <id> H4 --quotes-checked 3 --numbers-checked 2 --ending-ok --canonical-url https://你的名字.substack.com/p/文章链接
```

- `--quotes-checked` 和 `--numbers-checked` 不能少于评审提取出来的数量（`review.md` 末尾那行命令已经帮你填好了）。
- `--canonical-url` 是这篇文章在 Substack 上的最终链接。Substack 发布前就能在编辑器里看到网址，先填进来，所有 UTM 链接都基于它。
- 评审“未通过”但你确认没问题时，加 `--override-reason "我已逐字核对过原文"`。
- 如果文章里有 AI 辅助生成的句子，加 `--ai-assist-level assisted_text`。这会影响 Medium 版本是否需要披露。

### S6 改编

```bash
ca adapt <id>
```

一次生成：5 条 X 单帖、5 条 Substack Notes、1 条 Thread、1 篇 X Article 加 1 条推广帖、Medium 包装（如果有英文版），外加 Substack 发布包 `substack_package.md`。

只想要部分格式：

```bash
ca adapt <id> --formats x_post,substack_note
```

接下来看第 7 节。

---

## 6. 写第一篇：一条龙版（ca flow）

和第 5 节做的事完全一样，只是不用记每一步的命令：它自动跑到下一个闸口，停下来告诉你该看哪个文件、怎么继续。进度存在 `runs/flow.sqlite`，**关掉终端第二天接着来也没问题。**

```bash
ca flow start "小团队要不要做用户访谈？"
```

输出类似：

```
2026w45-idea0002 停在 H1：选一个角度，填兴奋度和 edge
  先看：hubs/2026w45-idea0002/angles.md
  继续：ca flow resume 2026w45-idea0002 --do approve --set angle=1 excitement=4 edge=...
  或者：ca flow resume 2026w45-idea0002 --do redo
```

照着提示一步步走：

```bash
ca flow resume <id> --set angle=2 excitement=4 edge="大家默认按项目做，我怀疑固定节奏才是关键"
```

```bash
ca flow resume <id> --set confirm=true
```

```bash
ca flow resume <id>
```

到 DRAFT 时，去 `hubs/<id>/draft.md` 写正文，写完：

```bash
ca flow resume <id> --do done
```

```bash
ca flow resume <id> --set quotes_checked=3 numbers_checked=2 ending_ok=true canonical_url=https://你的名字.substack.com/p/xxx
```

```bash
ca flow resume <id> --set variants=all
```

几个要点：

- **输错了不要紧**：比如漏了兴奋度，它会带着错误提示停在同一个闸口，不会中断。
- **不满意可以退回**：H1、H2、H3、H5 用 `--do redo` 重跑上一步；H4 用 `--do revise` 回去改稿。
- **随时查看停在哪**：`ca flow status <id>`。
- **可以混着用**：某个闸口已经用 `ca approve` 批过，flow 会自动跳过。
- **要发 Medium**：在 H4 之前把英文版放到 `hubs/<id>/final_en.md`，因为 H4 一过就会立刻改编。

---

## 7. 审稿、改稿、手动发布

### 7.1 审稿

打开 `hubs/<id>/review_queue.md`，每个变体的正文和检查结果都在里面：✅ 是通过，❌ 后面写着没过的原因。

| 常见的 ❌ | 意思 | 怎么改 |
|---|---|---|
| `within_limit` | 超字数（X 上一个汉字算 2 个字符，280 约等于 140 个汉字） | 删字 |
| `no_link` | X 根帖带了链接 | 删掉链接，导流链接由你发布后在回复里手动贴 |
| `no_hashtags` / `no_mentions` | 带了 # 或 @ | 删掉 |
| `numbers_in_final` | 出现了母稿里没有的数字 | 删掉，或先把数字补进母稿 |
| `dry_at_least_2` | 三问只过了 0–1 项 | 换一个更具体、可证伪的说法 |
| `reply_hook` | 结尾没有让人接话的点 | 加一个读者能回答的问题 |
| `link_only_in_last` | Thread 中间帖带了链接 | 链接只放末帖 |
| `author_has_premium` | 没有 X Premium | 在 profile.yaml 改 `x_premium: true`，或放弃 Article |
| `not_light_edit` | R2 重写和旧帖太像 | 换角度重写 |

### 7.2 改稿

想改哪条，就**直接改 `variants/<变体id>.md`**。Thread 的每帖之间用单独一行 `---` 分隔；Article 第一行是 `# 标题`。

### 7.3 放行（H5）

```bash
ca approve <id> H5 --variants all
```

它会**先用你改后的文字重跑所有检查**，再放行通过的。几个细节：

- 你改过的地方会记进 `voice/edit_diffs/`，月度复盘会用。
- 推广帖必须和它推广的 Article 一起放行。
- 只放行几条：`--variants v_<id>_x_post_01,v_<id>_x_thread_01`。
- 坚持放行没过检查的：加 `--force`（会被记录下来）。

放行后自动生成 `hubs/<id>/publish_kit.md`。

### 7.4 手动发布

**第一步，发 Substack 母稿。** 打开 `substack_package.md`：

1. 把“正文”部分粘贴进 Substack 编辑器。
2. 用“标题候选”做 Substack 自带的标题 A/B 测试。
3. 填副标题、文末 CTA，把 AI 使用说明放进 post template。
4. 过一遍“发送前清单”，然后发送。

**第二步，按 `publish_kit.md` 的时间顺序发其余稿子。** 每条都有可直接复制的正文和该平台的步骤。看今天该发什么：

```bash
ca due
```

```bash
ca due --hours 72
```

各平台的要点：

- **X 单帖**：粘贴正文发布，**不带链接**。发布后 1–2 小时在线亲手回复评论。要导流，就在自己帖子下面**手动**回复发布包里那条带 UTM 的链接。
- **X Thread**：在客户端用“添加帖子”逐条串起来，链接只在末帖。
- **X Article**：客户端 → Articles → 新建，粘贴标题和正文，检查排版。发完再发对应的推广帖。
- **Substack Notes**：同一天不连发，亲手回复评论。
- **Medium**：母稿发出 1–7 天后，用 Stories → Import a story 填母稿链接（会自动设 canonical），再到 More settings → Advanced Settings 核对 canonical；投稿给目标出版物，勾选通知订阅者。

**第三步，每发完一条就记下链接：**

```bash
ca published v_<id>_x_post_01 https://x.com/你/status/1234567890
```

只有记录过链接的帖子，后面才能收数据。

---

## 8. 收数据

所有数据接口都是**只读**的。

### X（自动拉取）

```bash
ca metrics pull-x --dry-run
```

先看会花多少钱（按每条 $0.005 保守估算），然后：

```bash
export X_BEARER_TOKEN=你的只读token
```

```bash
ca metrics pull-x
```

建议在帖子发出后 2 小时、24 小时、7 天各拉一次。

### Substack 和 Medium（手动录入或 CSV）

它们没有统计接口，需要你从后台抄数或导出：

```bash
ca metrics add v_<id>_substack_note_01 likes=12 restacks=3 free_subs=2
```

```bash
ca metrics import 导出文件.csv --source substack_export
```

CSV 只要有 `variant_id` 列或 `url` 列（和 `ca published` 记录的链接一致），其余数字列都会被当作指标导入。

### 看汇总

```bash
ca report --month 2026-11
```

按“平台 × 体裁”汇总，X 会算回复率（回复 ÷ 曝光）。手册的建议是：**X 看回复率，不看点赞；Substack 看打开者点击率和订阅，不只看打开率。**

---

## 9. 月度复盘与选题回流

每月初跑一次：

```bash
ca retro 2026-11
```

打开 `runs/retro_2026-11.md`，里面有：

- 各平台表现前 20% 和后 20% 的共同特征（样本太少时会直说）；
- 你反复做的修改，比如你总是删掉某类开头；
- 对声音档案、禁用词、选题权重的**修改建议**；
- **R1 候选**：回复率超过 30 天中位数 2 倍的短帖，值得写成长文；
- **R2 候选**：发布 90 天以上、表现前 20% 的帖子，值得换个角度重写。

批准复盘，把 R1 候选写进选题池：

```bash
ca retro-approve 2026-11 --r1 all --note "十一月复盘"
```

**修改建议不会自动生效**，声音档案永远由你自己改。觉得哪条有道理，就手动改 `profile.yaml` 或 `never.md`。

把一条爆款短帖直接变成长文母稿：

```bash
ca promote v_<id>_x_post_03
```

选题时，Agent 会把这条短帖的表现当作市场信号，要求长文回答它引出的追问，而不是把短帖拉长。

用新角度重写一条老帖（要求已发布满 90 天）：

```bash
ca recycle v_<id>_x_post_01
```

重写稿会出现在 `variants/` 里，照常用 H5 放行。和旧帖太像的会被拦下，因为 X 的创作者分成不计“轻改”的内容。

---

## 10. 进阶功能

### 语音访谈（模式 I）

对着 `cards.md` 里的提问录音，然后：

```bash
ca interview <id> --audio 口述.m4a
```

音频在本地用 faster-whisper 转写，不上传。第一次运行会下载模型；`--whisper-model small` 是默认值，电脑性能好可以用 `medium`。

整理结果在 `draft.md`，`cribs.md` 里有听众反应（哪里让人困惑、哪里重复、哪里有意思）、建议追问，以及**整理稿里可能新增的句子和数字**。这些地方一定要核对，确认没有偏离你的原话。

### 多 Agent 研究

在 `agent.yaml` 改：

```yaml
research:
  mode: multi
```

子问题会并行交给多个子 Agent，每个都会读网页全文。代价是 token 大约是普通对话的 15 倍。手册建议：**先用默认的单 Agent 跑几篇，发现它确实漏掉了关键信息再开。**

### 读者调查

```bash
ca survey design "了解读者做用户访谈的频率和障碍" --topic "每周一次访谈" -n 10
```

问卷在 `surveys/<调查id>/survey.md`，复制到任意问卷工具发给读者。回收的回答整理成 CSV，表头用 `responses_template.csv` 那一行；多选题的多个选项用分号 `;` 分隔。然后：

```bash
ca survey analyze <调查id> 回答.csv
```

开放题里引用的每句话都会逐字核对是否真在回答里。写文章时记得说“我的读者中”，因为愿意填问卷的读者不代表全体。

### 盲评

积累 3–5 篇 AI 参与的稿子之后，检验它们是否真的不比你纯手写的差：

```bash
ca blind prepare --ai <id1>,<id2>,<id3> --human 旧文1.md,旧文2.md,旧文3.md
```

打开 `evals/<批次>/`，逐篇读 `item_*.md`，在 `ratings.csv` 里打 1–5 分。**不要打开 `.key.json`**，那是答案。打完：

```bash
ca blind score <批次>
```

### 审计与进度

```bash
ca audit
```

检查每次发布是否都经过你的 H5 批准、发布时间晚于批准时间、没有任何自动互动，以及平台规则在 90 天内核对过。有问题会列出来并返回非 0。

```bash
ca progress
```

查看三项指标：论据支撑率是否 ≥95%、人工编辑时长是否在下降、是否至少有 1 篇长文来自 R1。

---

## 11. 每周节奏建议

以周更、`rhythm: systems` 为例（来自手册核实版）：

| 时间 | 做什么 | 命令 |
|---|---|---|
| 每天早上 | 90 分钟写作：前 30 分钟写短帖，后 60 分钟写母稿（Dan Koe 的分法） | — |
| 周一 | 从选题池挑题，跑到 H3 | `ca flow start ...` |
| 周二至周四 | 写正文、评审、定稿 | `ca flow resume ...` |
| 周五 | 改编、审稿、放行 | `ca flow resume <id> --set variants=all` |
| 发布日 D0 | 先发 Substack，再发第一条 Note 和最强的一条 X 单帖，在线回复 1–2 小时 | `ca due` |
| D1–D6 | 每天 1–2 条 X 单帖、1 条 Note，酌情发 Thread 或 Article | `ca due` → 手动发 → `ca published` |
| D1–D7 | 有英文版的话导入 Medium | — |
| D7 | 收数据 | `ca metrics pull-x` |
| 每月初 | 复盘 | `ca retro` → `ca retro-approve` |

---

## 12. 配置速查

`agent.yaml`：

| 字段 | 默认 | 说明 |
|---|---|---|
| `model` | `claude-opus-5-5` | 所有阶段使用的模型 |
| `max_tokens` | 32000 | 单次输出上限；报“被截断”时调高 |
| `use_fallbacks` | true | 模型拒答时由服务端自动换模型重试 |
| `web_search_max_uses` | 8 | 研究阶段每次调用的搜索次数上限 |
| `effort.*` | high / adapt 用 medium | 各阶段的思考深度：low、medium、high、xhigh、max |
| `review.pass_threshold` | 0.6 | 评审分达到多少算通过 |
| `review.factcheck` | true | 逐条事实核查 |
| `review.refetch_quotes` | true | 引语回原网页逐字核对 |
| `review.briars_samples` | 3 | 拔刺独立采样次数 |
| `review.style_drift_sigma` | 2.0 | 风格偏离多少个标准差算漂移 |
| `review.style_min_docs` | 5 | 往期文章少于这个数时不检测风格漂移 |
| `research.mode` | single | single 或 multi |

`platforms/*.yaml` 记录各平台的规则，每份都带 `verified_at` 核对日期。**超过 90 天，每条命令都会提醒你重新核对。** 平台规则变化很快：手册核实时发现，Medium 在 13 个月里改了至少八次规则。

---

## 13. 常见问题

**报错 “还没通过 H1……”**
每个阶段都要先过前面的闸口，照提示里的 `ca approve` 命令做就行。

**报错 “draft.md 在评审之后又改过”**
重新运行 `ca review <id>`。

**报错 “评审仍有硬拦截”**
打开 `review.md` 看“硬拦截”部分。最常见的是 TK 没补完，或者用了禁用词。

**评审没通过，但我确定没问题**
H4 加 `--override-reason "理由"`。理由会被记录下来。

**引语核查说“原网页找不到”，但我明明看到了**
有些网站的正文靠 JavaScript 加载，程序抓不到。你人工核对确认无误后，在 H4 用 `--override-reason` 说明即可。

**Medium 版本没生成**
看 `ca adapt` 的输出或 `review_queue.md` 末尾“跳过”的原因。通常是没有 `final_en.md`，或者用的是模式 B。

**X Article 总是被拦下**
模板默认 `x_premium: false`。有 Premium 就改成 true。

**`ca flow` 提示需要安装**
运行 `pip install -e '.[graph]'`。

**`ca interview --audio` 提示需要 faster-whisper**
运行 `pip install -e '.[voice]'`，或者先用其他工具转成文字稿，再用 `--transcript`。

**报错 “输出被 max_tokens 截断”**
调高 `agent.yaml` 里的 `max_tokens`。

**想看一共花了多少 token**
看 `runs/logs/日期.jsonl`，每行是一次调用。

**它会不会偷偷发东西？**
不会。代码里没有任何平台的写入接口；唯一的网络读取是研究搜索、引语回原网页核对、读取 X 公开指标。`ca audit` 可以随时检查。

---

## 14. 文件地图

```
creator-vault/
├── agent.yaml                  运行配置
├── voice/                      你的声音：profile.yaml、never.md、stances.md、stories.md、exemplars/、edit_diffs/
├── backlog/ideas.jsonl         选题池
├── archive/                    往期文章（RSS 导入）
├── platforms/                  三个平台的规则配置（带核对日期）
├── hubs/<id>/                  每篇母稿一个文件夹：
│   ├── meta.json               状态和闸口记录
│   ├── angles.md               S1 选题角度
│   ├── research.md             S2 研究简报
│   ├── outline.md              S3 提纲
│   ├── cards.md                S4 素材卡片（模式 A）
│   ├── draft.md                你的正文
│   ├── review.md               S5 评审报告
│   ├── final.md                H4 定稿
│   ├── final_en.md             你写的英文版（可选）
│   ├── review_queue.md         S6 待审稿件
│   ├── substack_package.md     Substack 发布包
│   └── publish_kit.md          H5 之后的手动发布包
├── variants/                   每个平台变体：.yaml 存元数据，.md 是你可以改的正文
├── metrics/                    指标快照
├── evals/                      锚点、测试集、盲评
├── surveys/                    读者调查
└── runs/                       调用日志、复盘报告、flow 进度
```

---

遇到教程没覆盖的问题，可以运行 `ca <命令> --help` 查看参数说明；设计依据见 [三平台创作 Agent 手册·核实版](docs/handbook/三平台创作Agent手册核实版.md)。
