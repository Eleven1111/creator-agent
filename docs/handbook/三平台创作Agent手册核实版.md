# 核对原文后，重搭三平台创作 Agent

这次核实把手册的地基换掉了一大块，架构没有变。母稿放在 Substack 或自有域名，各平台出原生变体，发布前最后一键由人按，Agent 不代笔。这套设计站得住，但它下面的平台事实有三分之一要改。**Medium 的 Boost 提名计划已于 2026 年 5 月 31 日关闭**；现行《Distribution Guidelines》（2026-06-29 版）把“AI-generated content”列为取消 General Distribution 资格的低价值内容，所以 AI 生成的文字即使披露了，也只能拿到关注者分发；**非英文稿件不进 General、不进 Boost**；MPP 的收款国家列表里**没有中国大陆**【原文已核】([Medium Blog](https://medium.com/blog/an-update-on-the-boost-nomination-program-and-whats-next-40331b1a9c0a); [Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution); [MPP eligibility](https://help.medium.com/hc/en-us/articles/39121627791639-Medium-Partner-Program-eligibility))。对一位用中文写作、身在大陆的作者来说，Medium 因此只适合当**英文稿的辐条**。X 方面，2026 年 2 月 23 日起，自助档 API **只能回复“召唤”了你的帖子**，4 月 20 日起又**取消了点赞、关注和引用帖的 API 写入**；读自己的数据（Owned Reads）只要 **$0.001** 一条；官方 API 从 2026 年 6 月 11 日起**可以起草和发布 Articles**【原文已核】([devcommunity 257909](https://devcommunity.x.com/t/x-api-v2-update-addressing-llm-generated-spam/257909); [devcommunity 263025](https://devcommunity.x.com/t/x-api-pricing-update-owned-reads-now-0-001-other-changes-effective-april-20-2026/263025); [X Articles API](https://docs.x.com/x-api/articles/introduction))。这样一来，“Agent 自动互动”在技术上基本被堵死，X 发布模块可以简化成“只发原创帖，只读自有数据”。Substack 方面，官方 2026 年 10 月的数字是：过去六个月，App 带来近 **80 万**付费订阅和 **8,000 多万**免费订阅，其中一半以上的付费订阅直接来自 Notes 信息流；2026 年 7 月 6 日，官方给 bestseller 上线了**只读的统计 MCP**；它的 AI 检测是**读者主动发起扫描、作者可以逐篇关闭**的透明度工具，官方文字没有说扫描结果会影响分发【原文已核】([On Substack 2026-10-14](https://on.substack.com/p/you-told-us-you-wanted-more-control); [MCP](https://on.substack.com/p/new-on-substack-subscriber-perks); [AI 透明度](https://on.substack.com/p/how-writers-are-reacting-to-substacks))。创作心法这边，多数高频引语经得起核对，但有几处归属要改：Housel 的“每个词值 100 美元”是他转述别人的话；Perell 的 CRIBS 里，I 代表 **Interesting**，不是 Insightful；“Packy 的妻子是第一读者”找不到依据；Claude 给 Packy 打的分是 A 和 A+，不是 A-。PG 的陌生人重读、Harry Dry 的三问、Gioia 的诚实三问，仍然是最适合写进评审提示词的材料；edge、兴奋度、亲身证据、声音和结尾，仍然只能由人判断。

---

## 本版核实变更摘要

2026-11-03 网络放开后，研究团队把上一版手册的论断逐条对照原文。下表列出影响手册设计的变更。“判定”栏的四个值是：**确认**（原文逐字支持）、**修正**（原文说法不同，以新版为准）、**推翻**（原文与旧版相反，或旧版的说法在所引来源里不存在且与现行规则冲突）、**仍无法核实**。

| # | 论断 | 旧版写法 | 判定 | 新版写法 |
|---|---|---|---|---|
| 1 | Substack 推荐网络的贡献 | 50% 新订阅、25% 新付费（2024-02）【待核实】 | 确认 | 原句逐字核到（2024-02-22）；另补 2026-10 官方新数字：App 六个月带来近 80 万付费、8,000 多万免费订阅，一半以上的 App 付费订阅来自 Notes 信息流 |
| 2 | “站内发现只占约 30%” | 二手文章称约 30%，与官方矛盾 | 修正 | 所引页面没有这个数字，只有作者自述“54% 的新订阅来自 Notes”；删掉“两组数字矛盾”一句 |
| 3 | 6.7 万人列表推荐只带来 189 人 | 【待核实】 | 仍无法核实 | 所引 eden.so 页面里找不到这组数字，正文删除 |
| 4 | Notes 转化研究 | 396,143 条，13.1% 带来免费，0.70% 卖出付费 | 确认 | 补样本：1,569 位作者、2026-01-01 至 09-18；作者属工具厂商 WriteStack |
| 5 | 免费转付费基准 | 官方 5–10%；Simon Owens 中位数约 3% | 修正 | 官方 5–10% 确认；**Owens 给的是约 5%**；“约 3%”只来自未核实的第三方汇总；规划仍按 2–3% 保守估算 |
| 6 | Substack AI 检测 | Axios：Pangram 评分，影响分发未知 | 修正 | 读者主动扫描；作者可在草稿阶段预扫、逐篇关闭、发布“How I make this”声明；官方未提分发影响 |
| 7 | Substack 官方 MCP | “单一来源，与 CEO 说法矛盾” | 修正 | 2026-07-06 已为 bestseller 上线，只读统计，不能发文 |
| 8 | 2026 新功能（Notes 草稿与定时、CSV、Recording Studio） | AlternativeTo 摘要 | 确认 | 改引 Substack 官方博文（03-09、03-12、04-08） |
| 9 | Substack freewall 与 metered paywall | 未收录 | 新增 | 2026-10-30 上线：读全文前先留邮箱；每月让免费订阅者读固定篇数的付费文 |
| 10 | 2023 年 X 限流 Substack 链接 | “自定义域名不受影响” | 修正 | Engadget 原文只说限流和恢复，没提自定义域名；该半句删除 |
| 11 | X API 单价 | $0.015/帖、含 URL $0.20、读 $0.005（第三方） | 确认 | 改引官方价目表；URL 定价 2026-04-20 生效，“被召唤的回复”仍为 $0.01 |
| 12 | X API “没有免费档” | 新开发者无免费档 | 修正 | 首次绑卡一次性送 $20，首次自动充值再匹配最多 $50（合计最多 $70），3 个月过期；Basic/Pro 订阅仍保留 |
| 13 | 读自有数据的成本 | 按 $0.005 估，每月最高约 $150 | 修正 | Owned Reads 为 $0.001，24 小时内同一资源去重；成本表改为约 $30 / $0.6 |
| 14 | API 回复 | 未收录 | 新增 | 2026-02-23 起，自助档只能回复 @ 了你或引用了你的帖子；只能 @ 和引用已在线程里的用户 |
| 15 | API 点赞、关注、引用 | 列为“禁止做法” | 新增 | 2026-04-20 起自助档 API 已取消这三项写入；引用需 Enterprise |
| 16 | X Articles 的 API | “官方 API 是否支持未找到证据” | 推翻 | 2026-06-11 起有 `POST /2/articles/draft` 与 `/publish` 端点；价格未单列 |
| 17 | AI 自动回复 | “据报需要书面批准” | 修正 | 官方写的是“prior approval”（事先批准），没有“书面”；浏览器自动化的后果是“permanent suspension” |
| 18 | Original Content Rewards | 门槛与“只算原创”【待核实】 | 确认（三家报道一致）并补充 | 补排除项：带有 helpful Community Note 的帖子、只谈变现或教人赚分成的内容不计酬；双周结算，$30 起付；Basic 订阅者的浏览计入 |
| 19 | “2025-10-14 X 宣布取消链接惩罚” | 【待核实】 | 推翻 | 被引页面里没有这句话；2025 年 10 月 X 只是在测试链接的显示方式 |
| 20 | Musk “一年多没惩罚链接” | 【待核实】 | 确认 | 2026-07-29 03:38 原话“We haven't for over a year”，无正式公告 |
| 21 | Buffer 链接研究 | “互动中位数为零” | 修正 | 是**互动率**中位数为零；样本 1,880 万帖、7.1 万账号；Premium 账号触达约为普通账号的 10 倍 |
| 22 | X 的 AI 标签 | “文字无披露要求；AI 媒体可标 Made with AI” | 修正 | 强制披露只针对变现计划内的武装冲突 AI 视频（2026-03-03）；可用于任何帖子的 AI 标签开关仍在测试 |
| 23 | Hypefury | 作为 X 的 Auto-plug 参考 | 推翻 | Hypefury 现已不支持 X（2026-11 自述）；相关引用全部删除 |
| 24 | Typefully 发 Notes 与 Articles | 【待核实】 | 确认 | API 有 `substack`（Notes）和 `x_article` 平台 |
| 25 | Koe 在 $1M 文章奖中的名次 | 自称“runner up”【转录】 | 修正 | 据二手报道，他获得的是单独的 Creator Choice 奖（$25 万），亚军是 The Kobeissi Letter |
| 26 | Koe 晨间流程 | 中文摘要【待核实】 | 确认 | 原文：散步 30 分钟，写作 90 分钟（前 30 分钟写短帖，后 60 分钟写 newsletter），之后才是邮件和会议 |
| 27 | Koe 平台分成 vs 自有产品 | 中文摘要【待核实】 | 确认 | 原文：平台每月约 $300–1,000，自有产品 $5 万–20 万以上（2026-03-11） |
| 28 | Medium Boost 提名 | 一半 Boost 来自出版物提名；每月自荐 2 篇；180 天上限 | 推翻 | 提名计划 2026-05-31 关闭，相关帮助页已删除；Boost 由内部策展决定，投稿高质量出版物仍是主要路径 |
| 29 | Medium 分档名称 | Network Only | 修正 | 现行名称是 Network Distribution |
| 30 | Boost 标准 | “原创、人写、探讨此前未知之物” | 修正 | 那是 2023 年版；现行五项：作者经验、价值与影响、尊重读者、非衍生、写作工艺；新增“亲身经验比头衔更重要” |
| 31 | Friend Link | 带来的阅读不算钱 | 推翻 | 官方原文：Friend Link 带来的会员阅读与普通阅读同等计入收入 |
| 32 | Medium 披露过的 AI 文字 | 可获 General Distribution | 推翻 | 现行指南把 AI-generated content 列为不得进入 General 的低价值内容 |
| 33 | Medium AI 辅助的披露 | 未收录 | 新增 | 任何含 AI 辅助生成文字或图片的稿件都要在前两段内披露；语法、拼写、提纲、事实核查工具除外 |
| 34 | Medium 非英文稿 | 未收录 | 新增 | 非英文稿不 Boost、不进 General（目前只能审英文） |
| 35 | MPP 资格 | 未写 | 新增 | 2026-08-26 起即时注册；银行须在合格国家，**中国大陆不在列**，香港、澳门、台湾在列 |
| 36 | MPP 收入调整 | 列了 10 月、11 月、1 月、2 月、6 月五项 | 修正 | 漏了 2025-12-01 的邮件通知加成（共六项）；另有阅读率调整、收听上限两项 |
| 37 | “屡次违规取消 MPP” | “屡次” | 修正 | 现行措辞没有“屡次”这个条件 |
| 38 | Medium 新 token | 据厂商文档 2025-01-01 起停发 | 修正 | 改引官方帮助页（2024-12-17 编辑）：不发新 token，旧 token 继续可用 |
| 39 | Medium canonical 设置 | “Customize canonical link” | 修正 | 实际路径：More settings → Advanced Settings → “This story was originally published elsewhere” |
| 40 | Lenny 删首段 | “未能定位出处” | 确认（语境修正） | 出自“500,000”一文，针对他编辑的**嘉宾稿**；播客里的说法是“把引言砍掉 50%” |
| 41 | Lenny 改稿遍数 | 10–30 遍（Perell 推文） | 确认 | 播客原话“10 20 30 times”；另一访谈说“几十遍，大概第 50 遍” |
| 42 | Lenny 每篇中位数 10 小时 | “有专门的编辑” | 修正 | 是文字编辑（copyeditor）加设计师 |
| 43 | Packy 妻子是第一读者 | 【待核实】 | 推翻（无依据） | 两期转录都没有；转录里的“一个读者”是读他日记的一位朋友 |
| 44 | Claude 给 Packy 打分 | A-（X 推文） | 修正 | 播客原话是“It's an A… with this one tweak… an A plus” |
| 45 | Housel“每个词值 100 美元” | 当作他的原则 | 修正 | 他自己说“忘了是谁说的”，是转述 |
| 46 | Housel 的写作量 | Motley Fool 约 3,500 篇 | 修正 | 3,500 篇是 Motley Fool 九年的量；博客总数“接近 4,000 篇” |
| 47 | Perell CRIBS | I = Insightful，用于书面反馈 | 修正 | I = Interesting；原文用在口头试讲时听对方反应 |
| 48 | Broderick 素材流程 | Raindrop → Google Doc → 逐条查链接 | 修正 | 只确认 Raindrop 分文件夹收集、写时直接取用；“Google Doc、查链接”原文没有 |
| 49 | Kyla Scanlon / Emily Oster | 同引 Fortune | 修正 | Fortune 原文没有 Oster；Scanlon 的重点是给年轻人讲清经济 |
| 50 | Noah Smith 定期投票 | “定期发投票帖” | 修正 | 所引页面只是 2020 年的一次征题 |
| 51 | Newton 改版 | 据 Nieman Lab 标题 | 确认 | 改引 Platformer 原文（2026-04-28）：取消链接合集 Side Quests，改为不定时发稿 |
| 52 | Eliason“删副词没抓住要点” | 【待核实】 | 仍无法核实 | 2024 年文里没有；他 2018 年反而主张“delete your adverbs” |
| 53 | Karlsson“原始素材（raw footage）” | 【待核实】 | 修正 | 免费部分原话是“wild sprawling mess”，有一两百万字笔记 |
| 54 | Bloom 的“95% 是包装” | 无限定 | 修正 | 他说的是“我猜”，并且只针对非虚构类的幂律式成功 |

**仍然打不开的来源。** help.x.com（Cloudflare 403 质询页），所以 Original Content Rewards 和 X Automation Rules 的帮助页原文没读到，只能用三家独立报道和 docs.x.com 交叉核实；x.com 和 twitter.com 只返回 JS 外壳，Lenny 的十条写作习惯、Perell 关于 Write of Passage 的推文、Packy 的“A-”推文都无法逐字核对；perell.com 每次返回 429（限流），Raymond Chandler Rule、28 Pieces、Personal Monopoly 的原页没读到；axios.com 和 niemanlab.org 文章页返回 Cloudflare 403，已用 Substack 官方博文和 Platformer 原文替代；YouTube 不可达，Dan Koe 的 19 个视频转录、Hormozi 和 Butcher 的转录都没有和原视频重新核对；medium.com 的文章页返回 403，Medium 博客改用 RSS 全文核实，但各位 Medium 作者的单篇旧文无法逐字核对；tim.blog（429）、towardsdatascience.com（403）、newslettercircle.com（TLS 证书过期）、indiehackers.com 和 alternativeto.net 也没读到。

---

## 先交代证据：哪些核过原文，哪些仍是摘要

**上一版的大部分来源只读到了搜索摘要，这一版核过了大半。** 上一版写作时，会话网络屏蔽了几乎所有一手站点，能直接读的只有 github.com 和 anthropic.com。这一版网络放开，核实员用 curl（带浏览器 UA）抓原页面，并绕开了几处拦截。Substack 刊物用 `<pub>/api/v1/posts/<slug>` 和 `/api/v1/archive` 的 JSON 读正文和日期；Medium 帮助中心的 HTML 页返回 403，但 Zendesk 公共 API（`help.medium.com/api/v2/help_center/en-us/articles/{id}.json`）返回全文，日期取 `edited_at`；Medium 博客用 RSS（`medium.com/feed/blog`）读全文；docs.x.com 读的是 `.md` 原文、`llms-full.txt` 和 changelog；How I Write 访谈用 GitHub 上带 YouTube 链接和日期的转录做逐字核对。

| 语料 | 内容 | 本报告标注 |
|---|---|---|
| on.substack.com、substack.com、各 *.substack.com 刊物、platformer.news、lennysnewsletter.com、honest-broker.com 等 | Substack 官方博文、条款、创作者原文 | 【原文已核】 |
| help.medium.com（Zendesk API）、Medium 博客 RSS、TechCrunch | Medium 现行政策与 Partner Program 公告 | 【原文已核】 |
| docs.x.com、devcommunity.x.com、Buffer、Engadget、ppc.land 等 | X API 官方文档、开发者公告、报道 | 【原文已核】 |
| tech-ish、GIGAZINE、TNW（同为 2026-08-08） | Original Content Rewards 规则（help.x.com 打不开） | 【原文已核】（三家二手报道互证，非 X 原页） |
| letters.thedankoe.com、thedankoe.com | Dan Koe newsletter 原文 | 【原文已核】 |
| `antoinejeannot/graham`、paulgraham.com | Paul Graham 全文（本轮抽查 3 条，全部一致） | 【原文已读】/【原文已核】 |
| `xai-org/x-algorithm`（HEAD `b220448`）与 `twitter/the-algorithm-ml` | X “For You” 排序代码与默认权重 | 【原文已读】 |
| `Medium/medium-api-docs` | Medium 官方 API 文档 | 【原文已读】 |
| Anthropic 工程博客三篇 | Agent 架构原则 | 【原文已读】 |
| `jpeslar1/john-peslar-ai-skills` | Tim Denning、David Perell 的逐字语料（编者称经作者本人的 API 拉取） | 【原文已读】（二手转载） |
| `liamdonnellyonline-cell/david-perell-nonfiction-transcripts` | How I Write 访谈的 YouTube 自动字幕 | 【转录·已核】：本轮逐字核过 Lenny、Packy、Gioia、Housel、Bloom、Dry、Cultural Tutor 等期 |
| `tjxj/dankoe-archive`、`ray-amjad/alex-hormozi-transcripts` | Koe 2026 年 19 个视频、Hormozi 514 个视频的自动字幕 | 【转录】（本轮未重核） |
| `AlonMichael/How-I-Write-Skills` | 第三方用 AI 从 How I Write 蒸馏出的技能包 | **降级为线索**：本轮发现它补全或改写了细节（Packy 的妻子、A-），不再作为证据 |
| `itsMelo/dan-koe-notes-zh` | Koe newsletter 中文压缩摘要 | 【待核实】（凡已找到英文原文的条目，均改引原文） |

**标注约定**：

| 标注 | 含义 |
|---|---|
| 【原文已核】 | 本轮（2026-11-03）对照原页面逐字核过 |
| 【原文已读】 | 上一轮已读过全文（GitHub 语料、Anthropic 文章），本轮未逐条重核 |
| 【转录·已核】 | 机器字幕，本轮已与转录稿逐字核对，但未与音频核对；标点和个别词可能有误 |
| 【转录】 | 机器字幕，本轮未重核 |
| 【待核实】 | 只有搜索摘要、二手聚合或 AI 蒸馏，或原页打不开、页面里找不到 |
| 【未找到证据】 | 检索后没有找到来源 |
| 【设计建议】 | 本报告自己的设计或推断，不是平台规则或创作者的做法 |

默认规则不变：**带链接但没有标注的事实，一律按【待核实】处理**；第三部分（手册）里没有来源的内容都是【设计建议】。

**框架名的核实结果没有变。** 本轮读到的两篇 Koe newsletter 原文里，同样**没有出现**“idea bank”“content multiplication”“APAG”这几个名字；“hook → aha → practical steps”的 newsletter 提纲只出自 beehiiv 案例页【待核实】。Koe 自己用的词是“validated ideas/topics”“outlier content”“swipe file”“reverse engineer”“packaging”“one topic or theme for the week”【转录】([YouTube](https://www.youtube.com/watch?v=KCjwU4XYBL8))。Ship 30 官网首页没有出现“1-3-1”和“4A”，这两个框架的官方措辞仍无法核实【原文已核】([ship30for30.com](https://www.ship30for30.com))。Justin Welsh 官网首页没有“Content Operating System”的定义，倒是写着“built a **$15M** one-person business”（自述，未审计）【原文已核】([justinwelsh.me](https://www.justinwelsh.me))。

**利益冲突仍然要提防。** 2026 年网上谈 X 算法的文章多数出自卖排期工具的厂商【待核实】([Blotato](https://www.blotato.com/blog/best-x-twitter-schedulers))。本轮确认的 Substack Notes 转化研究来自 WriteStack，eden.so 的两项研究来自 Koe 联合创办的 Eden，它们都是工具厂商。创作者公开的方法常常也是他们课程的卖点（Koe 的 2 Hour Writer、Welsh 的产品、Ship 30）。这次核实还发现了一种新的偏差：**AI 蒸馏的二手材料会把细节“补全”**。How-I-Write-Skills 技能包里关于 Packy 的两条细节，恰好是本轮没有通过核对的两条。

---
# 第一部分：平台机制与分阶段综合

## 三个平台奖励的是三种不同的东西

### Substack：拥有读者，Notes 已成为站内增长的主入口

Substack 的核心资产仍是**作者自己拥有的邮件列表**，增长主要靠站内网络。2024 年 2 月 22 日，官方原文是：“Recommendations, along with the Substack app, powers a network that drives **50%** of all new subscriptions and **25%** of new paid subscriptions on Substack”；同文称平台付费订阅超过 300 万【原文已核】([On Substack](https://on.substack.com/cp/142007285); [TechCrunch](https://techcrunch.com/2024/02/22/substack-now-lets-writers-curate-a-network-of-recommended-publications-for-their-subscribers/amp/))。这组数字已经过时。2026 年 10 月 14 日官方的新口径是：“In the past six months, the Substack app has driven nearly **800,000** paid subscriptions and more than **80 million** free subscriptions… More than half of paid subscriptions from the app came directly from the Notes feed.”【原文已核】([On Substack 2026-10-14](https://on.substack.com/p/you-told-us-you-wanted-more-control))。2025 年 10 月 27 日的说法是，三个月内 App 带来近 50 万付费和 3,200 多万免费订阅，“Most of these connections come from the feed”【原文已核】([Demystifying the feed](https://on.substack.com/p/demystifying-the-feed))。个人口径上，Lenny Rachitsky 说 Substack 的发现功能（尤其是推荐）给他带来 **12% 的新付费订阅和 78% 的免费订阅**，“Their fee is 10%, so they now pay for themselves”【原文已核】([Compound Planning](https://manual.compoundplanning.com/chapters/interview-with-lenny-rachitsky-writer-of-lennys-newsletter))。上一版说“二手文章称站内发现只占约 30%”，所引页面里并没有这个数字，作者写的是自己“54% 的新订阅来自 Substack Notes”，所以“两组数字互相矛盾”的说法删除【原文已核】([wanderwealth](https://wanderwealth.substack.com/p/whats-the-1-way-to-grow-on-substack))。“6.7 万人列表、推荐只带来 189 人”在所引 eden.so 页面里也找不到，同样删除【待核实】。

**Notes 的两种数字口径不同，并不矛盾。** WriteStack 的 Orel Zilberman 分析了 1,569 位作者在 2026 年 1 月 1 日至 9 月 18 日发布的 **396,143 条**原创 Notes：“0.70% of Notes sold one or more paid subscriptions, against 13.1% that brought in one or more free subscribers… that's 33 paid subscribers per million impressions”；在免费拉新最好的 2,781 条 Notes 里，也只有 16.5% 卖出过付费【原文已核】([The Writing Edge](https://thewritingedge.substack.com/p/substack-notes-convert-paid-subscribers))。WriteStack 是工具厂商，这篇是付费帖。逐条看，Notes 很少直接卖出付费；从平台总量看，App 带来的付费订阅一半以上出自 Notes 信息流。Agent 的设计应当两种口径都用：单条 Note 按拉免费订阅来考核，Notes 整体当作付费增长的主入口来经营【设计建议】。

**转化率和发布时间都有了更准确的出处。** 官方原文：“We tend to see **5-10%** of free subscribers convert to paying subscriptions, with 10% being a rate to aim for.”【原文已核】([Going Paid Guide](https://substack.com/going-paid-guide))。上一版说 Simon Owens 给出“中位数约 3%”，这是错的。Owens 的原话是“Newton's **5%** estimate sounds about right, both from my own experience and also speaking to other professional newsletter writers”，评论区有人说科技类“far closer to 2%”【原文已核】([Simon Owens](https://simonowens.substack.com/p/whats-a-realistic-conversion-rate))。“约 3%”只来自未核实的第三方汇总【待核实】。Lenny 的参照点是：“when I hit **1,000** paid subscribers, I was able to make a real living from this newsletter”【原文已核】([Lenny's Newsletter](https://www.lennysnewsletter.com/p/500000))。手册的规划基准仍按 2–3% 保守估算【设计建议】。发布时间上，Eden.so 分析了 3,034 位作者过去 12 个月的 473,405 条 Notes（2025-08 至 2026-08），最差时段的“破圈”概率（点赞达到作者自身中位数的 2 倍）是 18.1%，最好时段是 20.8%，差约三个百分点；周一最好（19.9%），周五最差（18.8%），美东晚 8–10 点最差【原文已核】([Eden.so](https://eden.so/blog/best-time-to-post-on-substack/))。Eden 是 Koe 联合创办的工具公司。

**2026 年的产品更新，有四项直接影响 Agent。** 第一，Notes 草稿与定时、统计 CSV 导出：“Publisher stats are now exportable as a CSV file, directly from your dashboard”（2026-03-09），Notes 可以“scheduling… in advance”（2026-04-08）【原文已核】([On Substack 03-09](https://on.substack.com/p/new-on-substack-draft-notes-hide); [04-08](https://on.substack.com/p/new-on-substack-post-templates-notes))。第二，长文模板可以保存“recurring elements like calls to action, disclaimers, section structures, sponsorship placements”，这正好用来固化 CTA 和 AI 披露语【原文已核】([04-08](https://on.substack.com/p/new-on-substack-post-templates-notes))。第三，Recording Studio 支持单人或最多两位嘉宾录视频，“with auto-generated clips and thumbnails included”，目前只支持桌面端【原文已核】([03-12](https://on.substack.com/p/introducing-the-substack-recording))。第四，2026 年 10 月 30 日上线了 **freewall** 和 **metered paywall**：前者“asking readers for their email address before they can read a full post”，后者“give free subscribers access to a set number of paid posts each month”【原文已核】([10-30](https://on.substack.com/p/new-on-substack-chat-channels-lists))。

**AI 检测是读者的透明度工具，不是分发过滤器。** 上一版依据 Axios 写“引入基于 Pangram 的 AI 检测，给出百分比评分，影响分发未知”。Axios 原文（2026-07-23）本轮仍然打不开，但官方博文写得很清楚：“we announced a feature that allows readers to scan text published to Substack to see how much of it is estimated to be written by hand or with AI assistance. We also launched tools for publishers, including the ability to run the program… on drafts prior to publication, disable scanning on a post-by-post basis, and add a ‘How I make this’ statement”；官方立场是“while the use of AI isn't necessarily a problem, a lack of transparency around it definitely is”。作者的反弹集中在误判和“moral purity test in disguise”上，官方随后改为作者可以“disable scanning on a post-by-post basis without having to scan the post first or interact with Pangram at all”【原文已核】([On Substack 2026-07-24](https://on.substack.com/p/how-writers-are-reacting-to-substacks))。官方文字**没有提到**扫描结果影响排序或推荐【待核实】。Platformer 的 Casey Newton 另有一句旁证：“Already, it seems that a staggering percentage of Substack posts are AI-generated in whole or part.”【原文已核】([Platformer](https://www.platformer.news/platformer-schedule-changes-ai-automation/))。

**工具层面：仍然只能读，不能写，但读的通道多了一条。** Substack **没有官方的发文、草稿或订阅者管理 API**。官方 API 条款“Last updated: January 8, 2026”，返回的只是“information that is publicly available on creators' public profiles”，而且“Substack may revoke this license at any time”【原文已核】([Substack API ToS](https://substack.com/api-tos))。dev.to 的概括是，这个 API 只能凭 LinkedIn 账号查公开资料，要人工审批【原文已核】([dev.to](https://dev.to/equinoxaifinancergb/does-substack-have-an-api-2026-and-what-you-can-actually-get-29il))。新的读取通道是 2026 年 7 月 6 日上线的官方 MCP：“We're introducing Model Context Protocol (MCP) support for bestsellers on Substack… You can get up-to-date analytics about your publication's performance, subscribers, and engagement over time. MCP for stats and analytics is available for bestsellers.”【原文已核】([On Substack 2026-07-06](https://on.substack.com/p/new-on-substack-subscriber-perks))。它只读统计，不能发文，而且只对 bestseller 开放。其余读取途径是公开 RSS（`<pub>.substack.com/feed`）和 CSV 导出。非官方 API 靠浏览器 cookie（`substack.sid`）认证，稳定性差，还可能违反条款【待核实】([codalanguez/substack-mcp](https://github.com/codalanguez/substack-mcp))。Substack **不能把 canonical 指向别处**：“Substack doesn't allow you to specify canonical URLs for your posts”（第三方博文，来源较弱），所以在跨平台拓扑里它天然是母站【原文已核】([anshulkumar](https://anshulkumar.substack.com/p/can-you-post-the-same-blog-on-substack))。文章统计里有两个排名，“Subscriber sources”和“Traffic sources”，其中“Substack”一类包括 Notes、搜索、排行榜和推荐【原文已核】([On Substack](https://on.substack.com/p/post-stats-substack-app))。官方没有直接写“看不到读者点了文内哪个链接”，这一句是推断【设计建议】。

### X：排序模型奖励对话和私下转发，API 只留下“发原创、读自己”

X 仍是三个平台里唯一能从代码层面读到机制的。现行“For You”排序器开源在 `xai-org/x-algorithm`：一个 Grok 衍生的 Transformer（Phoenix）预测约 20 种用户行为的概率，最终得分为 **Σ（权重 × 预测概率）**。README 提醒，权重乘的是**预测概率**，不是原始计数，所以权重之比不能当成“几个赞抵一次举报”的汇率【原文已读】([README](https://github.com/xai-org/x-algorithm))。`param.rs` 里的默认权重如下【原文已读】([param.rs](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs))：

| 行为 | 2026 默认权重 | 2023 Heavy Ranker（对照） |
|---|---|---|
| 点赞 Favorite | 0.66 | 0.5 |
| 回复 Reply | 5.0（互关之间的回复另加 15.0） | 13.5（作者回复互动 75.0） |
| 转发 Retweet | 1.0 | 1.0 |
| 引用 Quote | 5.0 | — |
| 私信分享 Share via DM | 5.0 | — |
| 复制链接分享 Share via copy link | **20.0** | — |
| 关注作者 Follow author | 4.0 | — |
| 打开链接 Open link | 0.2 | good_click 11.0 |
| 停留 Dwell | 0.05 | — |
| 不感兴趣 Not interested | −52.272 | negative_feedback_v2 −74.0 |
| 静音作者 Mute | −58.8 | — |
| 屏蔽作者 Block | −31.2 | — |
| 举报 Report | **−234.0** | −369.0 |

2023 年的数据来自 `twitter/the-algorithm-ml` 的 recap README【原文已读】([the-algorithm-ml](https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md))。读这张表有三个前提：它们是包在 `param!` 特性开关里的**默认值**，线上实验可以覆盖；作者多样性衰减和站外（OON）乘数在开源代码里默认是 1.0，生产值未公开；Phoenix 模型权重不在仓库里【原文已读】([x-algorithm](https://github.com/xai-org/x-algorithm/tree/main/xai-value-model))。代码里还能读到几条影响节奏的机制。**冷启动扶持**用 Thompson 采样，发帖者粉丝不超过 50,000、曝光不足 200 次、发布不超过 2 小时的帖子会被提到第 15–16 位；**AgeFilter** 把超过 48 小时的帖子移出候选；**DedupConversationFilter** 把同一会话的多条帖子合并显示；仓库里还有 `botmaker`、`scarecrow` 等反垃圾规则引擎和 `user-cred-v2` 可信度服务【原文已读】([param.rs](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs))。

**链接惩罚：代码里没有，官方说已取消，数据仍显示吃亏。** 当前代码里没有显式的 URL 惩罚参数，`has_url` 只在 VMRanker 去偏实验里作为内容特征出现【原文已读】([scorers](https://github.com/xai-org/x-algorithm/tree/main/home-mixer/scorers))。2026 年 7 月 28 日 23:56，Nikita Bier 对 Mark Zuckerberg 说“you do not need to put the links in replies anymore”；Paul Graham 追问“You no longer penalize tweets with links in them?”，Musk 在 7 月 29 日 03:38 回复“**We haven't for over a year.**”，PPC Land 注明这句话“arrived without a formal announcement”【原文已核】([ppc.land](https://ppc.land/x-drops-year-old-link-penalty-musk-tells-zuckerberg-on-platform/))。上一版另引“X 在 2025 年 10 月 14 日就宣布取消了链接惩罚”，这一条**推翻**：被引的 SocialPilot 页面里没有这句话，反而写着链接帖触达“suppressed by up to 80%”【原文已核】([SocialPilot](https://www.socialpilot.co/blog/twitter-algorithm))。2025 年 10 月真正发生的是：X 测试新的链接处理方式（tech-ish，10-13），10 月 19 日 Bier 宣布在 iOS 上让链接在浮层中打开，并解释链接帖触达低是因为“the web browser covers the post and people forget to Like or Reply”【原文已核】([tech-ish](https://tech-ish.com/2025/10/13/x-is-testing-changes-to-how-it-handles-web-links-to-external-sites); [iPhone in Canada](https://www.iphoneincanada.ca/2025/10/20/link-engagement-test-for-x-on-ios/))。“10 月 14 日”很可能和 Buffer 链接研究的发布日混在了一起。Buffer 那篇（2025-10-14）分析了 7.1 万个账号的 **1,880 万条**帖子：“As of August 2025, Link posts had 0% engagement rate on regular accounts, ~0.28% engagement rate on Premium accounts”；“Since March 2025, link posts from non-Premium accounts have been effectively invisible, with median **engagement rates** stuck at zero”。注意它说的是**互动率**中位数为零，不是互动数。同文还说“Premium accounts now see around **10x** the reach of regular ones”【原文已核】([Buffer](https://buffer.com/resources/links-on-x/))。Musk 的“一年多”往回推是 2025 年 7 月以前，和 Buffer 观察到的 2025 年 3–8 月数据冲突。OpenTweet 2026 年分析 28,124 条帖子，链接帖曝光是非链接帖的 1.05 倍【待核实】([OpenTweet](https://opentweet.io/answers/does-x-penalize-links-2026))。比较稳妥的结论是：显式惩罚很可能已经取消，但 `open_link` 权重只有 0.2，用户离站还会损失停留，普通账号的链接帖在期望值上仍然吃亏，需要自己做 A/B 测试【设计建议】。Premium 的排序乘数方面，2023 年代码据报有站内 4 倍、站外 2 倍的乘数，但研究团队没有打开 2023 年的文件核实【待核实】([Blck Alpaca](https://blckalpaca.at/en/knowledge-base/social-media/social-media-algorithms-distribution/x-twitter-algorithm-open-source))；在当前仓库里检索 `premium`、`verified`、`blue`，**没有找到排序乘数**，只有 `LimitRepliesVerified` 这类可见性规则【原文已读】([x-algorithm](https://github.com/xai-org/x-algorithm))。发帖时间方面，Buffer 2026 年 3 月分析 870 万条推文，称周二上午 9 点最好，其次是周三 10 点和 9 点，晚上 6–11 点最差，周五、周六最差；摘录里没有说明时区口径【原文已核】([Buffer best time](https://buffer.com/resources/best-time-to-post-on-twitter-x/))。

**变现：Original Content Rewards 只奖励被付费用户看到的原创。** help.x.com 的原页本轮仍被 Cloudflare 拦截，以下规则来自三家日期一致的独立报道（2026-08-08）。门槛是“18 or over, an active Premium, Premium+ or Premium Business subscription, **500 verified followers**, and **500,000 Home Timeline impressions** from verified users in 90 days, replies excluded”。计酬依据是“qualified impressions”，也就是原创帖在首页时间线被 Premium Basic、Premium、Premium+ 或 Premium Business 订阅者看到、且至少一半帖子可见的独立浏览，付费推广、人为和欺诈曝光都不算；双周结算，**$30 起付**。Basic 订阅者的浏览计入，但 Basic 用户自己不能参加。排除项有四类：整体照搬、只加滤镜或文字覆盖的轻改、汇编他人作品、从其他平台搬运；另外，“A post carrying a helpful **Community Note** earns nothing, and content that only discusses monetisation or coaches payouts is ineligible”。时间线是 8 月 7 日宣布，9 月 7 日旧的 Creator Revenue Sharing 结束，9 月 8 日起所有人重新申请，9 月 25 日首次付款【原文已核】([tech-ish](https://tech-ish.com/2026/08/08/x-is-scrapping-creator-revenue-sharing-on-7-september-everyone-has-to-apply-again/); [GIGAZINE](https://gigazine.net/gsc_news/en/20260808-x-original-content-rewards-program/); [TNW](https://thenextweb.com/news/x-original-content-rewards-program-revenue-sharing-ends))。据 tech-ish，Bier 于 2026 年 8 月 5 日卸任产品负责人【原文已核】(同上)。

**AI 披露只在一处是强制的。** 2026 年 3 月 3 日 Engadget：X 会暂停在变现计划里发布**未披露的武装冲突类 AI 视频**的创作者，初犯停 90 天，再犯永久移除；“The new policy is the platform's first rule requiring any kind of AI content disclosure”，同时 X 在测试一个可以标记任何帖子的 AI 标签开关【原文已核】([Engadget](https://www.engadget.com/social-media/x-to-require-ai-labels-on-armed-conflict-videos-from-paid-creators-citing-times-of-war-183631400.html))。GIGAZINE 2 月 25 日引 Nima Owji 的发现，这个开关覆盖文字帖，不只是媒体【原文已核】([GIGAZINE](https://gigazine.net/gsc_news/en/20260225-x-ai-labels/))。所以上一版“文字无披露要求，AI 媒体可标 Made with AI”的写法要改：可选的 AI 标签据报适用于任何帖子，是否全面上线未能确认【待核实】。

**Articles：对全部 Premium 开放，而且有了 API。** PiunikaWeb 2026 年 1 月 7 日：“X just opened up Articles to all Premium subscribers, ending the feature's exclusivity to Premium+ users… Articles launched back in March 2024 as a Premium+ perk.”【原文已核】([PiunikaWeb](https://piunikaweb.com/2026/01/07/x-articles-premium-nikita-bier-updates/))。$100 万最受欢迎文章奖的细则据报是：原创、不少于 1,000 词，主要按认证用户首页曝光评判，仅限美国 Premium 用户【待核实】([Business Standard](https://www.business-standard.com/world-news/elon-musk-s-x-offers-1-million-reward-for-best-long-form-article-126011700647_1.html))。上一版说官方 API 是否支持 Articles“未找到证据”，这一条**推翻**。changelog 原文：“**Jun 11, 2026**… Today, we added new endpoints for drafting and publishing Articles via the X API.”端点是 `POST https://api.x.com/2/articles/draft`（title、DraftJS 格式的 `content_state`、可选封面媒体）和 `POST https://api.x.com/2/articles/{article_id}/publish`（返回 `post_id`），需要用户授权（OAuth 1.0a 或 OAuth 2.0 PKCE），scope 为 `tweet.read`、`tweet.write`、`users.read`【原文已核】([X Articles API](https://docs.x.com/x-api/articles/introduction))。价目表**没有单列 Article 的价格**，API 能否绕开“发 Articles 需要 Premium”的要求，文档也没写【待核实】。

**API：便宜、能发帖，但互动类写入基本被拿走了。** 按次付费在 2026 年 2 月 6 日正式上线，“Basic and Pro plans remain available”，活跃的旧免费档用户拿到一次性 $10 代金券【原文已核】([changelog](https://docs.x.com/changelog))。2026 年 4 月 20 日起的官方价目：

| 项目 | 单价 | 备注 |
|---|---|---|
| Post: Create | **$0.015** / 次 | 4 月 20 日前为 $0.01 |
| Post: Create (with URL) | **$0.20** / 次 | 被召唤的回复（summoned replies）例外，仍为 $0.01 |
| Post: Create (summoned) | $0.010 / 次 | |
| Posts: Read | $0.005 / 条 | 每月上限 300 万条帖子读取 |
| User: Read | $0.010 / 条 | |
| **Owned Reads** | **$0.001** / 条 | 已认证用户读自己的 tweets、mentions、followers 等，且该用户就是 App 所有者 |

资源在 24 小时 UTC 窗口内去重，同一天重复读同一条不重复计费【原文已核】([pricing](https://docs.x.com/x-api/getting-started/pricing); [devcommunity 263025](https://devcommunity.x.com/t/x-api-pricing-update-owned-reads-now-0-001-other-changes-effective-april-20-2026/263025))。“新开发者没有免费档”也要修正：2026 年 10 月 2 日起，账号首次绑定合格支付卡时一次性获得 **$20**，首次自动充值成功时再匹配一次，**最多 $50**，额度 3 个月后过期；累计消费满 $200 起按 10%、15%、20% 返还 xAI API 额度【原文已核】([changelog](https://docs.x.com/changelog))。速率限制是 POST /2/tweets 每用户“200 requests per 15 minutes… 300 requests per 3 hours”【原文已核】([llms-full.txt](https://docs.x.com/llms-full.txt))。

上一版漏掉了两条对 Agent 影响最大的写入限制。第一条，2026 年 2 月 23 日 X 以“Addressing LLM-Generated Spam”为题宣布：“replies via the API will only be permitted if the replier has been explicitly summoned by the original post's author”，也就是原帖作者 @ 了你，或引用了你的帖子；“you may only @mention and quote users who are already participants in the thread”；这些限制“apply only to self-serve tiers: legacy Free, Basic, Pro subscriptions, and Pay-per-use packages”【原文已核】([devcommunity 257909](https://devcommunity.x.com/t/x-api-v2-update-addressing-llm-generated-spam/257909); [Create Post](https://docs.x.com/x-api/posts/create-post))。第二条，2026 年 4 月 20 日起，“Following, Likes, and Quote-Posts via API Writes will be removed for all self-serve tiers”；Create Post 文档写明“Quote-posting (using the `quote_tweet_id` parameter) requires an Enterprise plan”【原文已核】(同上)。另外，自助档 API 发帖最多带 1 个 cashtag；视频上限默认 20 分钟、8 GB，Premium 或认证用户 125 分钟、16 GB（2026-09-01）【原文已核】([llms-full.txt](https://docs.x.com/llms-full.txt); [changelog](https://docs.x.com/changelog))。一个关键问题官方文档没有回答：**作者回复自己的帖子（线程、自回复里放链接）算不算“被召唤”**。如果不算，线程就只能人工发或交给排期工具发【待核实】。

**自动化规则：AI 回复要事先批准，非 API 自动化永久封号。** docs.x.com 的 Developer Guidelines 原文：“AI-powered app generates and posts replies | Requires **prior approval** from X”；“Contact X via the Policy Support form before launching… Even with approval, cannot impersonate humans… Deploying AI-generated replies without approval is a violation, even if the content itself is helpful.”上一版写的“书面批准”，原文没有“书面”二字。自动化账号要满足六条：开启“Automated”资料标签、在简介里披露、关联真人管理的账号、立即响应退出请求、只用官方 API、遵守速率限制；这一节只适用于代表用户发帖、回复或互动的 bot，分析面板之类不受约束。动作层面：回复“Only if user engaged first. Max 1 reply per interaction”；自动点赞、批量点赞、买卖点赞都禁止；禁止批量或自动关注；给新粉丝自动发欢迎私信属于“Unsolicited”。最重的一条是：“**Non-API automation (scraping, browser automation) results in permanent suspension.**”另外，“App stores X data to train AI/ML models — Prohibited (except Grok)”【原文已核】([Developer Guidelines](https://docs.x.com/developer-guidelines))。help.x.com 上的 X Automation Rules 原页没读到。据单一来源，2026 年 10 月 9 日生效的服务条款修订明确了用户要为自主功能或 Agent 的行为负责【待核实】([note.com](https://note.com/munou_ac/n/n0fb681d97ded?hl=en))。Premium 档位价格只有二手来源：Basic $3/月、Premium $8/月、Premium+ $40/月【待核实】([MacRumors](https://www.macrumors.com/2024/12/23/x-raises-premium-plus-subscription-prices/))。

### Medium：人工策展决定上限，英文、人写、亲身经验是三张门票

**三档分发的名字变了，门槛更清楚了。** 现行《Distribution Guidelines》（页内写“Updated: June 29, 2026”）原文：“**Network Distribution** — stories that are matched to readers who are following that specific writer… This is the baseline category for any story on Medium which does not violate Medium rules. **General Distribution** — matched to readers based on their interests… **Boost** — especially high-quality stories that meet our Boost Guidelines… These get a higher priority in being matched to readers and are also given General and Network Distribution.”【原文已核】([Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution))。“Network Only”是 2023 年的旧称，现在只在 AI 政策页里还这么写【原文已核】([Medium Blog 2023-08-10](https://medium.com/blog/updated-guidelines-for-boost-47799aad8899))。同页有一句对中文作者是硬约束：“We can only review stories written in English at this time, so unfortunately **stories in other languages will not be Boosted or be given General Distribution** yet.”【原文已核】([Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution))。General Distribution 的失格项包括：AI 生成的内容；赞助内容和内容营销；“Stories that have a primary point of gathering signups/traffic, selling something”；摘要和链接合集；滥用标签；一次提及大量用户；以及关于 Partner Program、在 Medium 赚钱或 Boost 本身的文章，这类文章一律设为 Network Distribution【原文已核】(同上)。最后一条和上一版“文末 CTA 导向 newsletter”的建议有张力：CTA 可以有，但文章的**主要目的**不能是收集订阅。

**Boost 提名计划已经关闭。** 上一版写“约一半 Boost 来自受邀出版物编辑的提名；提名人每月最多自荐 2 篇；超过 6 个月的稿子不能被提名”，这些全部**作废**。Medium 2026 年 5 月 6 日的博文原文：“we found the program couldn't scale, and it limited the kinds of stories we could reward editors for, so **we'll be closing the Boost Nomination Program on May 31st, 2026**”；“The way we review stories for Boost is staying the same… The publications you know and love working with are already one of our main sources for finding stories to Boost, so your best bet remains submitting your story to a high quality publication and working with an editor.”【原文已核】([Medium Blog](https://medium.com/blog/an-update-on-the-boost-nomination-program-and-whats-next-40331b1a9c0a))。上一版引用的两个提名帮助页，Zendesk API 现在都返回 `RecordNotFound`。现行指南只说：“Our human curation team reviews stories seven days a week… We review stories we discover through our own internal curation tools.”【原文已核】([Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution))。出版物内部另有一个 Feature 机制，编辑用配额把文章设为精选，用掉的配额要等下一期分配；这是出版物内的推荐，不是 Boost【原文已核】([Help: feature a story](https://help.medium.com/hc/en-us/articles/28221990368791))。

**Boost 标准换成了五项。** 上一版引的“原创、人写、探讨此前未知或少有人审视之物”是 2023 年 8 月的措辞。现行版分五项：Writer's experience、Value and impact、Respect for the reader、Non-derivative、Writing and craftsmanship。其中“The reader's life is enriched by reading the story”保留；“The story is human-created and does not appear to be generated by Artificial Intelligence, a large language model, or other text-generating technology”现归在作者经验下；非衍生的要求是“It doesn't just paraphrase, recombine, or rehash information that is easily found elsewhere”；新增两句值得写进闸口：“The writer has credible, first-hand experience with the subject… This is a more important element than the credentials a writer may claim”，以及“Republished translations of work from other sources are not eligible for Boost”。包装要求逐字确认：“We will not Boost a story if we don't believe the title, subtitle, and cover image provide enough context about the story to appeal to readers in the feed”；同页还写“Being overly generic, mysterious, or formulaic is just as bad as being sensationalistic”，AI 生成的封面“sometimes works (if properly credited as such) but is often a turn-off”，“using no cover image can be better than using a poorly chosen one”；篇幅方面，“Well-crafted stories can be short or long”【原文已核】([Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution))。

**MPP：钱跟着会员阅读走，六次调整都在奖励“带来人”。** 现行收入计算页（2026-03-18 编辑）：“A member read is counted when a paying member reads or listens to your story for **30 seconds** or more”；“idle time is not counted”；“non-members' reads will still not contribute”；Boost 稿件“earn engagement points at a higher rate”，但“Non-boosted stories now receive a larger share of Partner Program earnings than before”。上一版说 Friend Link 带来的阅读不算钱，这一条**推翻**：“**Can I still earn through a Friend Link? Yes. Reads from a Friend Link are treated the same as regular reads.** Members who read your story through the Friend Link will still contribute to your earnings.”上一版“每种互动只在第一次计分”在现行页里找不到【待核实】。现行公式还有三项上一版漏掉的内容：按会员阅读率（30 秒以上阅读 ÷ 会员浏览）做最后调整，低于平均的下调、高于平均的上调，并且“does not penalize longer stories”；来自邮件通知的会员阅读“earn at a higher rate”；每位会员最多两次完整收听计入收入【原文已核】([Help: earnings](https://help.medium.com/hc/en-us/articles/360036691193-Medium-Partner-Program-earnings-calculation))。

六次调整的原文依次是。2025 年 10 月 1 日起，“shifts **5%** of the payouts toward stories that get this external traffic”【原文已核】([Medium Blog](https://medium.com/blog/partner-program-update-starting-october-1-were-rewarding-external-traffic-15cb28f75bc9))。11 月起，“shifting **15%** of the Partner Program budget to activity on stories that members discover through search engines like Google”，并且对 11 月 1 日之前发布的文章同样适用；现行帮助页只写“An additional share”，没给 15% 这个数【原文已核】([Medium Blog](https://medium.com/blog/partner-program-update-starting-november-1-were-rewarding-search-traffic-3ac0635f9f6b))。12 月 1 日起，会员因为你发的邮件通知来读，你“earn slightly more”，这一项上一版漏了【原文已核】([Medium Blog](https://medium.com/blog/partner-program-update-on-december-1-were-rewarding-email-notifications-4910c47d4cb7))。2026 年 1 月起，原本集中给 Boost 稿的收入“spread… more broadly”，Boost 稿仍然更高，“but not as much”【原文已核】([Medium Blog](https://medium.com/blog/partner-program-update-starting-january-1-were-rewarding-writing-more-broadly-4907e149e38c))。2 月 17 日起，读者在你的付费墙前转成会员，你获得“a **small, one-time amount** of that new member's membership fee”，快速取消的会员不算；此前 2021–2025 年的转介绍计划是每月分走约一半会费【原文已核】([Medium Blog](https://medium.com/blog/partner-program-update-starting-february-17-were-rewarding-stories-that-bring-in-new-members-3e84d2eb6e68))。6 月 1 日起推出 **Editor Partner Program**：合格出版物的编辑在投稿队列里认领一篇稿子，可以拿到这篇稿子收入的 **25%**，“The writer will keep all their original earnings”；7 月 1 日时已有 100 多个出版物、300 多位编辑合格【原文已核】([Medium Blog 05-05](https://medium.com/blog/partner-program-update-starting-june-1-were-rewarding-editors-for-stories-they-edit-aaec12a97cea); [07-01](https://medium.com/blog/new-a-program-to-pay-publication-editors-d9c4f1ed40d8))。出版物要合格，必须由 MPP 成员拥有、采用“open to all”投稿模式，并在六个月中有三个月满足：付费墙文章合计月收入至少 $200、当月发 1 到 100 篇、至少来自两位作者；编辑自己的稿子不计；编辑收入没有上限，覆盖所有认领的付费墙文章，不限于被 Boost 的【原文已核】([Help: EPP](https://help.medium.com/hc/en-us/articles/40661484998679-Editor-Partner-Program-eligibility-and-overview); [How editor earnings work](https://help.medium.com/hc/en-us/articles/40661926684055-How-editor-earnings-work))。Medium 在 EPP 公告里把当前阶段称为“the Curation Era”，原话是“We see what a lot of synthetic, AI-generated content is doing to the internet”【原文已核】([Medium Blog 05-05](https://medium.com/blog/partner-program-update-starting-june-1-were-rewarding-editors-for-stories-they-edit-aaec12a97cea))。

**MPP 资格：即时注册，但中国大陆银行不在列。** 2026 年 8 月 26 日起，“The Partner Program is open again, now with a faster and easier enrollment process… you don't need to fill out an application and wait for a response”；最常见的问题是“paywalling fully AI-generated writing and stories about Medium”【原文已核】([Medium Blog](https://medium.com/blog/the-medium-partner-program-is-open-again-now-with-a-faster-and-easier-enrollment-process-96c01f0e0670))。“open again”说明此前有一段时间暂停或改为申请制，起止时间未能核实【待核实】。现行资格是：有效的付费会员、至少发过 1 篇文章、资料完整、“Your bank is located in a country that is eligible for payouts”、年满 18 岁、同意 MPP 条款和付费墙内容政策。资格页列出约 120 个国家和地区，**中国大陆不在列**，香港、澳门、台湾在列【原文已核】([Help: MPP eligibility](https://help.medium.com/hc/en-us/articles/39121627791639-Medium-Partner-Program-eligibility))。关于 Medium 本身、Partner Program 或平台机制的文章不能进付费墙，默认只给 Network Distribution【原文已核】([Help: paywall policy](https://help.medium.com/hc/en-us/articles/31090080813591-Content-eligible-for-the-paywall-policy))。上一版引的“2023 年收入 ≥$10 的作者中约 65% 在 $10–$100”，没有找到官方原文【待核实】([Vocal](https://vocal.media/journal/massive-changes-to-how-medium-pays-its-writers-are-you-ready))；CEO 那句“联合发布、给其他平台做增长”，原帖在 medium.com 上，文章页 403【待核实】([Medium Handbook](https://medium.com/medium-handbook/is-medium-worth-it-in-2026-194a85fb2f35))。

**AI 政策比上一版写的更严。** 现行 AI 政策页（2026-04-29 编辑）原文：“AI-generated writing (disclosed as such or not) is not allowed to be paywalled as part of our Partner Program. Accounts that have fully-generated AI writing behind the paywall may have those stories removed from the paywall, and/or have their Partner Program enrollment revoked.”上一版写的“屡次违规”，原文没有这个条件；“2024 年 5 月 1 日起”的生效日，现行页也没写。“AI 生成”的官方定义是：“writing where the majority of the content has been created by an AI-writing program with little or no edits, improvements, fact-checking, or changes. This does not include AI writing tools such as AI outlining, or AI assisted fact, spelling, or grammar checkers.”未披露的处理是“Undisclosed AI-generated writing will be given Network Only distribution”。新增的一条是：“We require that **any story incorporating AI assistance be clearly labeled** as such. AI-assisted text without a disclosure will similarly be restricted to distribution on the author's personal network.”披露方式是在前两段内加一句，例如“This story was written with the assistance of an AI writing program”；检测方式是“a wide variety of tools and technologies… combined with human review of any positive results”。同页还禁止用 AI 改写他人内容形成近似衍生作品（按剽窃处理）、“easily disprovable AI-hallucinated stories, statistics, events”，以及为 SEO 和联盟链接批量生成的 AI 内容【原文已核】([Help: AI policy](https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy))。上一版说“披露过的 AI 文字可以获得 General Distribution”，这一条**推翻**：现行《Distribution Guidelines》在“What disqualifies a story from General Distribution?”下逐字列出了“**AI-generated content**”【原文已核】([Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution))。合起来是三层：AI 生成的文字，披露了也只有关注者分发，不能 General，更不能 Boost，不能设付费墙；人写为主、用了 AI 辅助生成的句子或图片，必须在前两段披露；只用 AI 列提纲、查语法拼写、核事实，不必披露。

**工具层面：API 停了，Import 是唯一干净的通道。** 官方 API 文档原话是“The Medium API is no longer supported… We don't allow any new integrations with our API.”旧接口 `POST /v1/users/{authorId}/posts` 支持 `contentFormat`（html/markdown）、`canonicalUrl` 和 `publishStatus`（public/draft/unlisted），没有编辑、删除、统计或定时【原文已读】([medium-api-docs](https://github.com/Medium/medium-api-docs))。上一版引厂商文档说“2025 年 1 月 1 日起不发新 token”，现在可以换成官方帮助页（2024-12-17 编辑）：“Medium will not be issuing any new integration tokens for our API and will not allow any new integrations. **All existing tokens will continue to work.**”页面没有写具体日期【原文已核】([Help: API/Importing](https://help.medium.com/hc/en-us/articles/213480228))。Import 工具确认：“Using the import tool will automatically backdate the post to the original date, as well as add a canonical link”，入口是首页左栏 **Stories → Import a story**【原文已核】([Help: Importing](https://help.medium.com/hc/en-us/articles/214550207-Importing-a-post-to-Medium))。手动设置 canonical 的路径是三点菜单 → More settings → Advanced Settings → “This story was originally published elsewhere” → Save canonical link，而且“Only the story's author can set a canonical link”【原文已核】([Help: canonical](https://help.medium.com/hc/en-us/articles/360033930293-Set-a-canonical-link))。官方鼓励联合发布：“Syndicating your own work from other platforms is a great idea!”【原文已核】([Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution))。平台本身稳定：TechCrunch 2025 年 7 月 11 日报道 Stubblebine 说 Medium 自 2024 年 8 月首次盈利后一直保持盈利，他 2022 年接手时公司每月亏损 $260 万；2024 年 4 月付费会员超过 100 万（摘要级）【原文已核】([TechCrunch 2025-07-11](https://techcrunch.com/2025/07/11/mediums-ceo-explains-what-it-took-to-stop-losing-2-6m-monthly/); [TechCrunch 2024-08-21](https://techcrunch.com/2024/08/21/august-was-mediums-first-profitable-month-ever/))。Medium 的规则在过去 13 个月里改了至少八次，**Agent 必须从配置文件读取 Medium 的政策参数，不能写死在代码里**【设计建议】。

### 跨平台对比

| 维度 | Substack | X | Medium |
|---|---|---|---|
| 分发核心 | 邮件列表 + 站内网络；App 付费订阅一半以上来自 Notes 信息流（2026-10） | Phoenix 预测行为概率的加权和；48 小时候选窗口 | Network / General / Boost 三档；Boost 由内部人工策展，提名计划已关闭 |
| 受众归属 | 作者拥有邮件列表 | 平台拥有关注关系 | 平台拥有；可给订阅者发邮件通知（有收入加成） |
| 主要体裁 | 长文、Notes、视频与直播 | 单帖、Thread、X Articles、视频 | 文章（标题、副标题、封面图是分发入口） |
| 增长主杠杆 | Notes 信息流与推荐 | 回复、引用、私信与复制链接分享；小号 2 小时冷启动 | Boost；投稿给高质量出版物；站外、搜索和邮件流量 |
| 变现 | 订阅（官方 5–10%，规划按 2–3%）、赞助 | Original Content Rewards（500 认证粉丝 + 90 天 50 万认证首页曝光）；主要价值在导流 | MPP 按会员阅读、阅读率、转化；EPP 给编辑 25% |
| AI 政策 | 读者可扫描、作者可逐篇关闭；倡导透明，官方未提分发影响 | 只有变现计划里的武装冲突 AI 视频强制披露；AI 自动回复须事先批准 | AI 生成：只给关注者分发、不进付费墙；AI 辅助：必须前两段披露 |
| 语言 | 不限 | 不限 | **非英文不进 General、不进 Boost** |
| 官方写入通道 | 无 | 按次付费 API：原创帖 $0.015、含 URL $0.20、Articles 草稿与发布；不能主动回复、点赞、关注、引用 | 无新 token；旧 token 可建草稿；人工 Import |
| 官方读取通道 | RSS、CSV、bestseller 统计 MCP | Owned Reads $0.001 | RSS；无统计 API |
| 外链 | 自身就是链接目的地 | 官方称已不惩罚；普通账号链接帖互动率中位数仍为零（2025） | 主要目的是导流的文章失去 General 资格 |
| Canonical | 不能指向别处，适合当母站 | 无 canonical 概念 | Import 自动设置；也可手动设置 |
| 证据强度 | 官方博文 + 厂商研究 | 代码（机制）+ 官方 API 文档 | 官方帮助页与博文全文 |
| Agent 定位【设计建议】 | 母稿与关系经营，发送由人完成 | 测题场与引流，只发原创 | 英文稿的联合发布与搜索资产，人写为主 |

### 对中文作者、身在中国大陆的作者意味着什么【设计建议】

这一节是根据上面已核实的规则推出来的，属于设计建议。**第一，Medium 只适合发英文稿。** 中文稿在 Medium 上只能拿到 Network Distribution，不会被 Boost，也不会进入 General Distribution；如果只有中文稿，Medium 只是一个存档，不是分发渠道。打算用 Medium 的作者，应当为部分母稿准备人写为主的英文版。Medium 只说“从其他来源转载的翻译稿”不能 Boost，作者自己翻译自己的中文母稿算不算，规则没有写清【待核实】。如果英文版大量靠机器翻译，那就属于 AI 辅助，必须在前两段披露，Boost 基本无望；稳妥的做法是作者用英文重写，Agent 只做术语表和校对。**第二，MPP 收款要求银行位于合格国家或地区。** 中国大陆不在列，香港、澳门、台湾在列；没有合格地区银行账户的作者，应把 Medium 定位成导流和搜索资产，不计划 MPP 收入。**第三，X 的写入成本和支付门槛都很低**（首次绑卡送 $20，最多 $70 额度），但 Original Content Rewards 需要 Premium 订阅，各国家和地区能否收款本轮没有核实【待核实】。**第四，Substack 的付费订阅依赖 Stripe 收款**，作者所在地区能否开通 Stripe 本轮没有核实，开启付费前要先确认【待核实】。**第五，运行环境。** 三个平台在中国大陆都不能直接访问，Agent 的发布和数据拉取模块应部署在能稳定访问这些平台的境外服务器上，同时要遵守各平台“只用官方 API、不做浏览器自动化”的要求，X 对非 API 自动化的处罚是永久封号。**第六，平台组合。** 对中文作者，比较现实的组合是：Substack（或自有域名）发中文母稿，X 发中文或双语短帖测题，Medium 只发精选的英文重写稿。

---
## 分阶段综合：四个阶段的可复制机制

### 创意：题源有四条，排序权交给作者的兴奋度

**第一条题源是读者问题清单。** Lenny Rachitsky 的原话是：“I keep a list of topics I want to write about (have about **50** currently), and have a rough idea of what the next 2-3 posts will be. I pick the topic I'm most excited to write about this week (as I optimize for my own curiosity vs. what people want…)”；而且“the post always starts with a concrete, simple, direct question from a reader”【原文已核】([Compound Planning](https://manual.compoundplanning.com/chapters/interview-with-lenny-rachitsky-writer-of-lennys-newsletter))。他在播客里列过自己的选题提示：“what do I want to learn about… what is interesting to me right now… someone asked me that I didn't have a great answer to… what have I said on Twitter that has resonated”【转录·已核】([YouTube](https://www.youtube.com/watch?v=DMZem1NYfpM))。Matt Yglesias 2024 年 2 月定下的 mailbag 是两步：“a Sunday evening thread to submit questions and a Monday evening thread to vote on the three finalists… whatever is ahead at 5pm Eastern on Tuesday—will be our Friday topic”；这是 2024 年的格式，现在是否还这样做未核实【原文已核】([Brad DeLong](https://braddelong.substack.com/p/should-i-be-running-a-mail-answers))。上一版说 Noah Smith 和 Ted Gioia 也“定期”发投票帖，这要修正：所引 Noah 页面是 2020 年 11 月的一次征题（“I wanted to gauge what subscribers like to see me write about”），Gioia 那半句没有来源【原文已核】([Noahpinion](https://www.noahpinion.blog/p/tell-me-what-you-want-what-you-really))。

**第二条是用一个固定视角处理无穷的输入。** Heather Cox Richardson 说：“I start every morning by reading through social media… probably for an hour to two hours. just to see what the public conversation is about”；她解读新闻的底气来自史学训练，“that's where a doctorate in history and a number of books in history really matter”，被问到是不是记者，她回答“No, I do not… I'm a historian”【原文已核】([KALX](https://kalx.berkeley.edu/kalx-news-heather-cox-richardson-interview))。Fortune 对 Kyla Scanlon 的描述是“explain important concepts about the economy in ways young people can understand”，她自己说“The reason people are freaked out is because they don't understand the world around them… I try to cut through the noise”【原文已核】([Fortune](https://fortune.com/2024/06/26/kyla-scanlon-tiktok-youtube-newsletter-economist-vibecession))。上一版把 Emily Oster 也挂在这篇 Fortune 下，原文里没有她；Lenny 的“500,000”一文只用一句话提到“Help me parent better: ParentData by Emily Oster”【原文已核】([Lenny's Newsletter](https://www.lennysnewsletter.com/p/500000))。Dan Koe 说“你不需要细分领域，你需要一个视角”【转录】([YouTube](https://www.youtube.com/watch?v=3rNqNvwNcrM))。Perell 的 Personal Monopoly 是“技能、兴趣和个性的独特交集”；perell.com 本轮返回 429，但 Packy 在 2021 年的播客里说过，他从 Write of Passage 学到的第一件事就是“finding your personal monopoly”【原文已读】([perell.com](https://perell.com/note/build-a-personal-monopoly/))【转录·已核】([YouTube](https://www.youtube.com/watch?v=a0hOyHqli0s))。Denning 说“读者买的是人，不是细分领域”【原文已读】([timdenning.com](https://timdenning.com/tim-denning-is-rich/))。这几种说法指向同一件事：**定位靠身份加视角，不靠收窄题材**。

**第三条是市场验证过的题。** 这是 X 生态最有特色的做法。Koe 按热度排序其他创作者的内容，研究异常值，并反复挖掘自己的旧爆款。他 2019 年写过一条以“how to get ahead of 99% of people”开头的推文，2023 年改成 YouTube 视频，到 2026 年 5 月是他播放量最高的视频（170 万次）【转录】([YouTube](https://www.youtube.com/watch?v=7HM-rptYdTs))。他划的边界是：别人的措辞和结构归别人，想法可以拿；“复制粘贴、换几个词”会让你“看起来像个白痴”【转录】(同上)。Hormozi 把 X 和 TikTok 当试验场，跑出效果的点子再扩写【待核实】([Video Creatr](https://www.buzzsprout.com/1887347/episodes/17152925-how-alex-hormozi-posts-300-times-a-week))。Ship 30 的 4A（Actionable、Analytical、Aspirational、Anthropological）提供组合式的选题生成方法，但官网首页没有出现这个名字，官方措辞仍无法核实【待核实】([Bush thread](https://threadreaderapp.com/thread/1534574544895234049.html))。

**第四条是作者自己的经历。** Medium 现行 Boost 标准把它写成了明文：“The writer has credible, first-hand experience with the subject… This is a more important element than the credentials a writer may claim”；指南在点评被 Boost 的示例时称赞“all original content based directly on the writer's experience”【原文已核】([Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution))。Awosika 的建议是“采访过去的自己”【待核实】([LinkedIn](https://www.linkedin.com/in/ayotheauthor/))。Perell 说：“50 加仑树汁才熬出 1 加仑糖浆……觉得点子不够时，我就去收集更多经历。”【原文已读】([perell.com](https://perell.com/essay/expression-is-compression/))

这四条题源最后都要过 PG 的一道关：**没有 edge 就不该动笔**。edge 不需要是完整论点，对别人视为理所当然的事抱有疑问就够了，而且这种切入点“没法系统地生成”【原文已读】([The Best Essay](https://paulgraham.com/best.html))。Morgan Housel 补了一个同方向的说法：他最擅长的是在动笔之前就放弃不会成功的题，“I'm much better at not starting a blog or a chapter if it's not going to work… before I've typed a single letter”；他打磨了一周仍然失败的那篇，原因是“the idea sucked”【转录·已核】([How I Write 2025-10-15](https://howiwrite.substack.com/p/morgan-housel-how-to-master-writing))。这决定了 Agent 在选题阶段的边界：它可以找候选的“缝隙”，但洞见和取舍都要由人来定。

### 素材：一个收集箱，写时取用，再加上 AI 拿不到的证据

**有文档的素材系统都出奇地简单。** Ryan Broderick 的原话是：“I use a passive planning system for the most part. I have an app called Raindrop that's synced across all my devices and I have folders in it that I add links to as I go about my day. So I have a folder for the newsletter, a folder for things I want to include in my live shows, another for podcast ideas… when it comes time to put together an issue… it's all there for me already.”上一版写的“倒进 Google Doc、逐条检查链接是否被删”在原文里没有，已删除。同篇还有几条实务细节：每周一、三、五上午 9 点到 12 点排版并写主文，争取下午 3 点前发出；每周约 6,000 字；有一位研究员 Adam Bumas；近 7 万读者，约 3,000 付费【原文已核】([The Story](https://thestory.au/articles/ryan-broderick-garbage-day-newsletter-interview/))。Lenny 的研究型文章是：“I throw all of my findings into the doc, in a messy way, and keep adding to it as I learn more. Once I have some raw nuggets, I start to mold it into something that's interesting”；“Each topic has a Coda page where I start throwing bullet points of ideas, quotes, stats”；请专家供稿“usually requires 2-3 weeks lead time”【原文已核】([Compound Planning](https://manual.compoundplanning.com/chapters/interview-with-lenny-rachitsky-writer-of-lennys-newsletter))。Koe 反对精致的第二大脑：“系统都会熵增……拥抱混乱”【转录】([YouTube](https://www.youtube.com/watch?v=KCjwU4XYBL8))。他每周开一个看板，放一份粗提纲、当研究材料的 YouTube 链接，旁边开着 AI 对话，用来“提取需要的观点”【转录】(同上)。Henrik Karlsson 先把想法收进“a wild sprawling mess”，他的日记和笔记有“one or two million words”；上一版说的“原始素材（raw footage）”一词，免费部分没有出现，付费部分没读到【原文已核】([How I write essays](https://www.henrikkarlsson.xyz/p/how-i-write-essays))。Sahil Bloom 用口袋笔记本、每周日散步一小时的说法，本轮未核【待核实】([Practical PKM](https://practicalpkm.kit.com/posts/creativity-flywheels-vol-2-sahil-bloom))。

**真正形成护城河的素材，是 AI 拿不到的东西。** Lenny 和 Figma 的 Noam Segal 合作做了“one of the largest independent, in-depth surveys on how AI is affecting productivity for tech workers (**1,750** respondents)”【原文已核】([Lenny's Newsletter](https://www.lennysnewsletter.com/p/ai-tools-are-overdelivering-results))。Gergely Orosz 和 Elin Nilsson 的 2025 年调查“received more than 3,000 responses”，去重和清除垃圾后有 **2,997** 份【原文已核】([Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/the-pragmatic-engineer-2025-survey))。最有力的一手证据是 Casey Newton 2026 年 4 月 28 日的改版说明。他的判断是：“If Platformer's three pillars are original reporting, news analysis, and link aggregation, then, it would seem that one of those has already been commoditized and the second may be on its way.”具体做法有三项：免费订阅者每周一篇专栏，付费订阅者周四另有一篇，外加记者笔记和 mailbag；“instead of promising to show up on a set schedule, we're promising to show up when we find out something interesting”；收尾的链接合集 Side Quests 取消，因为“Techmeme does this particular job better”。他的结论是：“we're betting that the value in tech journalism is moving away from aggregation and predictability and toward original reporting and surprise.”他还自己做了一个自动化的每日链接摘要来找选题，“It does about as good a job as I do in finding stories of interest”【原文已核】([Platformer](https://www.platformer.news/platformer-schedule-changes-ai-automation/))。这段话几乎可以直接当作 Agent 的分工说明：**聚合交给机器，原创报道和意外留给人**。Hormozi 的说法更直接：利害越高，人越不会听一个没有第三方证明的人；他把真实会议录下来转成文字，让 AI 挑出“有意思的时刻”，“而不是自己编故事”【转录】([YouTube](https://www.youtube.com/watch?v=XsWSvz-aewA))。Jack Butcher 把做事过程中留下的副产品叫作“锯末”（sawdust）【转录】([YouTube](https://www.youtube.com/watch?v=EGnSx3EYEU0))。准确性方面，HCR 的规则是“she won't include anything in the newsletter that hasn't been corroborated by **three different sources**”，这是采访者的转述，不是她的原话【原文已核】([Brian Boyles](https://brianboyles.substack.com/p/my-conversation-with-heather-cox))；Noah Smith 的做法是“Let's go to FRED, the data page maintained by the Federal Reserve, and see what the true numbers are”【原文已核】([Noahpinion](https://www.noahpinion.blog/p/how-not-to-be-fooled-by-viral-charts))。

### 创作：体裁不同，“先松后紧”的循环是共通的

**通用循环来自 PG。** 他的建议是尽快写出一个糟糕的初版，并预期文章 80% 的想法在动笔之后才出现。2005 年那篇文章他用了 67 分钟，其中 23 分钟写、44 分钟改【原文已读】([Writing, Briefly](https://paulgraham.com/writing44.html))。写作把想法“从模糊变成糟糕”，糟糕的地方看得见，看得见就能改；文章至少一半的工夫，花在反问“这对吗？完整吗？”上【原文已读】([The Best Essay](https://paulgraham.com/best.html))。他的策略是“先松后紧”：有些句子发布前读了 100 遍，别扭的段落像“刺”一样勾住袖子，“不全拔掉我不发”【原文已读】([How to Write Usefully](https://paulgraham.com/useful.html))。

**Substack 长文有两种原型。** 日更型靠惯性：HCR 每天写约 **1,200 字**，原文是“She continues to post her 1,200-word essays for free on Facebook, but hundreds of thousands of people also pay for subscriptions”【原文已核】([BC Magazine](https://www.bc.edu/content/bc-web/sites/bc-magazine/fall-2022-issue/features/history-s-first-draft.html))。旗舰深度型投入大：Lenny 说“It takes me a median of **10 hours** per post. Sometimes just 3 hours, sometimes 100+ hours”，定稿后“I have my copyeditor review it and fix all the issues. I may have my designer create a fun graphic for it”，所以他身边是文字编辑加设计师，不是上一版写的“专门的编辑”【原文已核】([Compound Planning](https://manual.compoundplanning.com/chapters/interview-with-lenny-rachitsky-writer-of-lennys-newsletter); [500,000](https://www.lennysnewsletter.com/p/500000))。Packy McCormick 的说法是：“do V zero is the first one, because I know it's just going to get scrapped and I'm going to use that as the doc where I dump all of the stuff that I cut from the other versions”，通常写 6 到 7 稿【转录·已核】([YouTube](https://www.youtube.com/watch?v=9Fit0knSiH8))。Doomberg 的流程是：“before we start writing anything, we pick a title. Title is the most important thing. And then once we have a title, we will write a one sentence summary of each of the paragraphs.”【原文已核】([Fire2Fission](https://www.fire2fission.com/podcast-episodes/050-doomberg))。Ben Thompson 区分免费稿和付费稿的说法，只来自 AI 蒸馏的技能包，本轮没拿到完整转录【待核实】。

**Substack Notes 的作用是拉新和维系关系。** 上一版引 Tom Kuegler 的“Notes 本身就让 newsletter 增长了起来”，出处 newslettercircle.com 的证书过期，本轮仍未核实【待核实】。他另一条 Note 确认是原话：“I wrote on LinkedIn for 6 years. I quit recently. I wrote on Medium for 7 years. I quit last year… This whole ‘being on 38 platforms at once’ thing is way overrated. I'm all-in on Substack.”（2024-04-12）【原文已核】([Kuegler Note](https://substack.com/@tomkuegler/note/c-53765421))。他的 Medium RSS 最后一篇停在 2023 年 8 月 17 日，和这句话一致【原文已核】([RSS](https://medium.com/feed/@tomkuegler))。Koe 把推文同步发到 Notes，并说 Notes 信息流里的人“真正欣赏深度思考”【转录】([YouTube](https://www.youtube.com/watch?v=3rNqNvwNcrM))。

**X 单帖的核心技法是压缩和具体。** Bloom 卡住时“will literally pop open Twitter and I will write that out and try to meet the character constraint and just shorter and shorter and shorter”【转录·已核】([YouTube](https://www.youtube.com/watch?v=f-s22uCixMw))。Harry Dry 用三个问题检验每一句：“Can I visualize it? Can I falsify it? Can nobody else say this? So, you get three nos. You've probably written a lot of rubbish. You get three yeses. You're on to something.”【转录·已核】([YouTube](https://www.youtube.com/watch?v=TUMjnmfsPeM))。The Cultural Tutor 说他每天写，“just open Twitter… press upload tweet and… start writing”【转录·已核】([YouTube](https://www.youtube.com/watch?v=1pBxikHRCXI))。

**X Thread** 起源于 Andreessen 的“tweetstorm”【转录】([YouTube](https://www.youtube.com/watch?v=tV6kDr1rwTs))。Bloom 的线程模仿 Ben Thompson 和 David Senra，在新想法里串起自己以前的想法【转录】([YouTube](https://www.youtube.com/watch?v=f-s22uCixMw))。Cole 建议首条推文给出一个故事、一个框架，或者预告后面的可操作建议，标题要“清楚，而不是聪明”【待核实】([Cole thread](https://threadreaderapp.com/thread/1441450057119592456.html))。代码层面，DedupConversationFilter 会合并同一会话，线程的分发主要靠首帖【原文已读】([README](https://github.com/xai-org/x-algorithm))。新的工程约束是，API 能否发自回复构成的线程，官方没有写清（见第一部分）。

**X Articles** 仍然**没有找到**创作者自己总结的模板【未找到证据】。Koe 的做法是把 newsletter 原样粘贴过去【转录】([YouTube](https://www.youtube.com/watch?v=KCjwU4XYBL8))。现在 Articles 有了官方 API，Agent 可以把母稿转成 DraftJS 格式建草稿，由人点发布【设计建议】。

**Medium 文章最依赖结构和包装。** Cole 的标题公式要回答写什么、写给谁、承诺什么，正文用“引言 + 约 3 个要点 + 结论”的骨架【待核实】([Nicolas Cole](https://nicolascole77.medium.com/3-simple-ways-to-make-your-medium-headlines-irresistible-click-6a401cc0a02b))；他的 Medium RSS 显示 2026 年 9–10 月仍在发文【原文已核】([RSS](https://medium.com/feed/@nicolascole77))。Denning 的标题测试是“五年级学生能看懂”，并且要回答“凭什么有人点”【原文已读】([timdenning.com](https://timdenning.com/writing-harsh-truths/))；他在 Medium 的最后一篇停在 2024 年 12 月 9 日，此后转向自有站点和 Substack【原文已核】([RSS](https://medium.com/feed/@timdenning))。官方对篇幅的说法是“The length of the story is appropriate and serves the purpose and context of the story itself”，“5–7 分钟最佳”只是社区传言【原文已核】([Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution))。阅读率调整上线后，标题夸大的代价变成了直接的收入损失【设计建议】。

### 发布：长拆短是主流，短养长是研发层

**两种流向构成一个循环。** 以 newsletter 为核心资产的经营者，主流做法是“长拆短”：Welsh 每周一篇 newsletter 拆出 6–10 个短帖、附 2 个导流 CTA【待核实】([Growing Viral](https://growingviral.beehiiv.com/p/justin-welsh-turning-1-piece-content-100-highvalue-posts))；Koe 的拆分链是全公开样本里最完整的，他在 newsletter 原文里也写过，会把每周 newsletter 当成 YouTube 视频的大纲，“may even post the newsletter itself to Medium and my personal blog”【原文已核】([letters.thedankoe.com](https://letters.thedankoe.com/p/the-1-million-dollar-morning-routine))；Gary Vaynerchuk 把这叫作“reverse pyramid”【待核实】([garyvaynerchuk.com](https://garyvaynerchuk.com/THE-GARYVEE-CONTENT-STRATEGY-HOW-TO-GROW-AND-DISTRIBUTE-YOUR-BRANDS-SOCIAL-MEDIA-CONTENT/))。“短养长”是研发层：Naval 的推文风暴后来由 Eric Jorgenson 编成书【转录】([YouTube](https://www.youtube.com/watch?v=mWYMRCcYn-Q))；Dickie Bush 据报说过“我的每篇文章都从一条推文开始”【待核实】([quotewise](https://quotewise.io/q/w8hnsw/))。

**改编必须做成平台原生的。** Denning 说：“复制粘贴行不通，每个平台……都像在学一门语言。”【转录】([Small Business Big Marketing #637](https://podcasts.apple.com/us/podcast/how-writing-changed-tim-dennings-business-life-forever-637/id319019197?i=1000613999291))。Kuegler 的立场相反，他全押 Substack（见上）。Packy 给了一条推广上的具体经验：“the more attention grabbing thing on Twitter is a really good bar chart… or a really good number… I think the thumbnail is probably less and less important.”【转录·已核】([YouTube](https://www.youtube.com/watch?v=9Fit0knSiH8))。Koe 提醒产量不要太多：“降低量，提高质量……给品牌加一点稀缺感。”【转录】([YouTube](https://www.youtube.com/watch?v=KCjwU4XYBL8))

**归因只能靠 UTM。** Substack 文章统计有“流量来源”和“订阅来源”两个排名，流量第一的渠道不一定是订阅第一的渠道【原文已核】([On Substack](https://on.substack.com/p/post-stats-substack-app))。X 到订阅、Medium 到 Substack 的转化率，研究团队仍然**没有找到**可靠的公开数据【未找到证据】。

### 四阶段证据速览

| 阶段 | 证据最强的可复制机制 | 代表人物 | 主要证据缺口 |
|---|---|---|---|
| 创意 | 约 50 个题的清单按兴奋度挑；读者问题开篇；固定视角；异常值选题；edge 检验；动笔前先砍掉不成立的题 | Lenny、HCR、Koe、PG、Housel | “不写什么”清单；X 上追热点的方法；4A 官方措辞 |
| 素材 | Raindrop 式分文件夹收集；每篇一个乱文档；专有调查；真实会议转录；聚合交给机器 | Broderick、Lenny、Orosz、Hormozi、Newton | RSS、Obsidian 的使用证据；更正政策 |
| 创作 | 快速烂初稿 → 陌生人重读 → 拔刺；句子三问；压缩到 280 字；V0 删稿库 | PG、Dry、Bloom、Packy | X Articles 模板；体裁与转化的定量关系 |
| 发布 | 长拆短 + 短养长；平台原生改编；一张图或一个数字做推广 | Koe、Welsh、Naval、Packy | X 和 Medium 到订阅的转化数据；API 发线程是否可行 |

---
# 第二部分：创作心法

## Dan Koe：一篇周更 newsletter 养活整个媒体矩阵

> 本节的视频引语来自 `tjxj/dankoe-archive` 里 2026 年 1–9 月 19 个视频的自动字幕【转录】，本轮因 YouTube 不可达没有重核。凡是找到了 newsletter 英文原文的条目，都已改引原文并标【原文已核】。

**定位与哲学：写作是“撬动其他杠杆的杠杆”。** Koe 说：“写作是解锁其他形式杠杆的杠杆。”他认为一份 1,000 到 10,000 人的邮件列表，一封邮件就能赚“1 万到 10 万美元”【转录】([KCjwU4XYBL8](https://www.youtube.com/watch?v=KCjwU4XYBL8))。“写作即思考”在他那里叫“强制线性”：脑子里自以为懂了，写作逼你把它压成一条单线；他还说“80% 的写作是研究和学习”【转录】(同上)。他把内容分成快内容和慢内容：快内容是清单体、愤怒推文、“AI 生成的摘要”和“为互动优化的线程”，慢内容是长文、长对话和“让你得思考才能领会的推文”【转录】([3rNqNvwNcrM](https://www.youtube.com/watch?v=3rNqNvwNcrM))。两个内容支柱是：怎样弄清自己想要什么（心理学、哲学、个人成长），怎样做成它（技能、商业、技术、AI）【转录】([VyR8nqD3sQ8](https://www.youtube.com/watch?v=VyR8nqD3sQ8))。

**选题：市场验证在先，个人视角过滤在后。** 他挑题有两条：这件事我是否觉得重要，因为“只要经过我的视角过滤，它就变得独特”；包装能否抓住注意力，因为“有日记，也有写作”【转录】([KCjwU4XYBL8](https://www.youtube.com/watch?v=KCjwU4XYBL8))。动笔前他会研究“什么标题有效……反复读高表现的推文……问自己它为什么比我的好……做有效的事，但加上你自己的东西”【转录】(同上)。2026 年 7 月那期视频的选题，来自一个约 70 万播放、叫“The Notebook System that saved my brain”的视频，他改成了“The Writing System That Saved My Brain”【转录】(同上)。具体做法是找一个创作者，按热度排序他的内容，点 Eden 里的“reverse engineer”按钮；他也提到 YouTube 异常值工具 1of10【转录】(同上)。他持续挖自己的旧爆款，“这其实就是我现在还在增长的方式”，也承认有些题目“已经死了”，需要一段“重置期”【转录】([7HM-rptYdTs](https://www.youtube.com/watch?v=7HM-rptYdTs))。

**素材：每周一个看板，不搞第二大脑。** 他总结的系统要素是：一周一个主题，一个能快速记想法的地方，一个收集灵感的方式（社交帖、YouTube、Substack 文章、PDF、图片），懂得包装钩子和标题，写作时能从想法和研究里顺手取用【转录】([KCjwU4XYBL8](https://www.youtube.com/watch?v=KCjwU4XYBL8))。他把“一周一个目标”带来的被动收集归功于《Psycho-Cybernetics》：散步、听人聊天时冒出的点子“会自己连到我的 newsletter 上”【转录】(同上)。

**写作与打包：内容是自己的，包装可以研究别人。** 他把写作比作礼物，有内容也有包装，标题和缩略图“可以之后再做”【转录】(同上)。他给写长文的建议是：写真正感兴趣的东西；只抓一个主要观点；把写作当成钻兔子洞的学习机会；不要把单一来源当定论；先别套模板；和自己辩论，用提问把文字推下去；先把思考做完，问自己“我真的相信这个吗”【转录】([3rNqNvwNcrM](https://www.youtube.com/watch?v=3rNqNvwNcrM))。newsletter 怎么分节、写多少字、有没有逐句编辑环节，研究团队**没有找到**他本人的说法【未找到证据】。

**分发链：他自己讲得最完整。** 视频里的原话是：“我把一篇 newsletter 发到 Substack……复制粘贴到 X Articles……它最终变成一份宽松的 YouTube 脚本，YouTube 视频再上传到播客频道，然后我一整周都可以从原来的 newsletter 里找推文点子……这些推文同步到 Substack Notes，我再把它们做成图片发到 Instagram 和 LinkedIn。有些我特别喜欢的推文，我就坐到镜头前把它念出来，于是就有了 Reels、TikTok 和 Shorts，而这每天只花一两个小时。”【转录】([KCjwU4XYBL8](https://www.youtube.com/watch?v=KCjwU4XYBL8))。newsletter 原文里他给了这条链的一个效果数据：如果不这样做，“my newsletter analytics wouldn't be double my YouTube analytics with 900,000 fewer subscribers”【原文已核】([letters.thedankoe.com](https://letters.thedankoe.com/p/the-1-million-dollar-morning-routine))。

**时间与工具：晨间流程有了原文。** 视频里他说：“我整个生意建立在每天早上 1 到 2 小时的写作上。”【转录】(同上)。上一版只引了中文摘要，现在找到了原文：“Go on a walk (30 min) / Start writing (90 min) / After that, I eat a small meal, go on another walk, respond to a few messages along the way, go to the gym, then start emails, meetings, and other non-creative work.”而且这 90 分钟有明确分工：“the first 30 minutes of writing are dedicated to short-form posts for social media… The second 60 minutes… is dedicated to writing a newsletter.”页面标题是“The 2 hour morning routine that changed my life”，`datePublished` 为 2025-08-22（可能是重新发布）【原文已核】([letters.thedankoe.com](https://letters.thedankoe.com/p/the-1-million-dollar-morning-routine))。给新手的配方是每天 60 分钟：30 分钟研究验证过的帖子并起草，30 分钟在私信和回复里交朋友【转录】([7HM-rptYdTs](https://www.youtube.com/watch?v=7HM-rptYdTs))。注意，这条建议里的“私信和回复”必须由人亲手做，自助档 API 已经不能主动回复【设计建议】。工具方面，thedankoe.com 首页自称“co-founder of Eden”和“author of The Art of Focus”【原文已核】([thedankoe.com](https://thedankoe.com))；Eden 里有看板、swipe file、异常值发现流、reverse engineer 和 AI 对话【转录】([7HM-rptYdTs](https://www.youtube.com/watch?v=7HM-rptYdTs))。Eden 早期访问日期（2025-11-24）没有核实，帮助页返回 404【待核实】。他说 Eden 曾经“因为 AI 额度开销而破产”，只有视频这一个来源【转录】(同上)。

**AI 观：拿来做迭代和研究，不交出思考。** 他的用法是：“我拿我喜欢的好帖子，让 AI 给我出一些变体，我读一遍，等某一个击中我……它先经过 AI，再经过我的脑子”【转录】(同上)。他的警告是：AI“非常快地耗尽创造力”；“只有人能写长文，因为机器人没有一个处境中的视角”；“当所有人都有超能力时，就没有人有超能力”【转录】([3rNqNvwNcrM](https://www.youtube.com/watch?v=3rNqNvwNcrM); [VXgusdDbsQE](https://www.youtube.com/watch?v=VXgusdDbsQE))。对 Agent 热潮，newsletter 原文写的是“You have everyone spending thousands a month on agents… they don't know what good looks like”【原文已核】([letters.thedankoe.com](https://letters.thedankoe.com/p/how-to-start-a-one-person-business))。粉丝根据他的访谈做的 Claude Code 系统（swipe 拆解、5 份提纲、60 条推文、30 个标题）是**第三方解读**，不是他本人的工作流【待核实】([vincentchan/AI-Content-Engine](https://github.com/vincentchan/AI-Content-Engine))。

**变现与数字：两条关键数字已核到原文。** 他的模型是“流量多少加上产品多好，决定你赚多少”，产品阶梯是电子书、课程、cohort、社区【转录】([VyR8nqD3sQ8](https://www.youtube.com/watch?v=VyR8nqD3sQ8))。2026 年 3 月 11 日的 newsletter 原文：“As someone with a few million followers, I can tell you that platform monetization is not enough. I can make about **300-1000 a month** on Instagram or X, but with my own product/offer, I can make **50k-200k+**.”同文给出那笔“100 万美元”的账：“$1,000,000 / 12 = $83,333 per month / $83,333 / 30 = $2,777 per day… Sell 18 $150 products a day… At a 2.5% conversion rate… you need **720** people to visit that page a day”，并建议“Get 500k to 1 million impressions on social media per month”【原文已核】([letters.thedankoe.com](https://letters.thedankoe.com/p/how-to-start-a-one-person-business))。他在视频里说自己是 X $100 万文章奖的“runner up”【转录】([YouTube](https://www.youtube.com/watch?v=3rNqNvwNcrM))，但据二手报道，2026 年 2 月 4 日公布的结果是 @beaverd 获 $100 万，亚军是 The Kobeissi Letter（$50 万），Koe 的“How to Enter a State of Extreme Focus Anytime”获得的是单独的 $25 万 **Creator Choice** 奖【待核实】([KuCoin](https://www.kucoin.com/news/flash/x-announces-winners-of-1m-long-form-writing-contest-beaverd-takes-top-prize))。手册应写成“Koe 自称 runner up，据报获得的是 Creator Choice 奖”。“How to fix your entire life in 1 day”的浏览量（1.47 亿到 1.7 亿）和 14 天约 $4,495 的分成，没有一手来源【待核实】([KuCoin](https://www.kucoin.com/news/flash/dan-koe-s-article-on-x-hits-150m-views-sparks-discussion-on-solo-creator-earnings))。营收和订阅数也互相冲突：beehiiv 案例页写 $200 万/年、17.5 万订阅者，YesPress（2026 年 4 月，站点 403）写 $410 万和 29.3 万订阅者【待核实】([beehiiv](https://www.beehiiv.com/case-studies/dan-koe); [yespress](https://yespress.io/dan-koe))。

**批评与内在张力。** 有分量的批评文章仍然没有找到【未找到证据】，只有 Reddit 上对“导师”的怀疑、Tim Denning 的讽刺帖，以及 Eden 险些破产和他宣扬的精益经营之间的反差【待核实】([Tim Denning](https://timdenning.substack.com/p/twelve-quotes-from-philosopher-dan))。他批评“为互动优化的线程”是快内容，自家工具却专门为互动验证过的包装而做【转录】。他在 2019–2021 年就开始做 X，吃到了早期红利，存在幸存者偏差；他主要的变现对象，正是想学“怎么增长”的创作者【设计建议】。

**对手册的启示。** Koe 的系统可以拆成 Agent 模块：每周一个母题，异常值和旧爆款扫描，swipe file，母稿之后的拆分链，包装放到最后做，AI 只做变体和研究问答。他的晨间分工（30 分钟短帖、60 分钟 newsletter）可以直接写进节奏配置。必须留给人的有三样：视角过滤（“我是否觉得重要”），对 AI 变体的取舍（“等某一个击中我”），以及判断什么是好的品味。

---

## 其他十五位创作者的心法档案

### Paul Graham：一套可以逐字复制的写作“源代码”【原文已读】

PG 的系统在 2005 到 2024 年的文章里一以贯之，本轮又抽查了 3 条，全部与原文一致。**选题**要有 edge，好问题往往带点出格：反直觉、野心过大或者离经叛道；如果人们觉得某个问题“早被研究透了”，那反而是好信号；你必须真的对它感兴趣【原文已读】([The Best Essay](https://paulgraham.com/best.html))。**写作过程**是一次树搜索：沿着“普遍性和新颖性组合最高”的分支走。他在那篇文章里写道：“In this essay I've already cut a **17-paragraph subtree**… In general you want to be quick to cut.”最危险的诱惑是留下一段不对的东西，只因为里面有几句好话或者花了很多功夫【原文已核】([The Best Essay](https://paulgraham.com/best.html))。**检验**有两道。一是“中立陌生人”：假装自己是一个对你脑子里的东西一无所知的读者，问它对吗、完整吗；他一篇文章写两周，草稿读 50 遍【原文已读】([Putting Ideas into Words](https://paulgraham.com/words.html))。二是有用性公式：告诉人们一件**真实、重要、他们还不知道**的事，并且说得**尽可能明确**，“the four components are like numbers you can multiply together to get a score for usefulness”【原文已核】([How to Write Usefully](https://paulgraham.com/useful.html))。**防误读**：预先堵住“一个相当聪明且善意的人”可能产生的误读，对恶意曲解的辩护放进尾注，“You don't want to spoil your house by putting bars on the windows to protect against dishonest ones”，尾注里还有一句“Put railings on the balconies, but don't put bars on the windows”【原文已核】(同上)。**措辞**：“fancy writing doesn't just conceal ideas. It can also conceal the lack of them.”【原文已核】([Write Simply](https://paulgraham.com/simply.html))。**战术清单**：卡住时把要写的东西讲给别人听，再把说过的话写下来；朗读，找出读起来会磕绊的地方；为一个不会像你那样仔细阅读的读者写；收工时给自己留一个容易开头的地方【原文已读】([Writing, Briefly](https://paulgraham.com/writing44.html))。**AI 时代**，他判断世界会分成“会写的人和不会写的人”，因为写作就是思考【原文已读】([Writes and Write-Nots](https://paulgraham.com/writes.html))。

### Morgan Housel：自私写作，以及一条转述来的“100 美元规则”【转录·已核】

Housel 认为最糟的写作建议是“know your reader”，因为“the speed at which ‘know your reader’ becomes ‘pander to your reader’… is astounding”；他说自己进入了“selfish writing era”，“I'm not trying to impress other people anymore”【转录·已核】([How I Write 2025-10-15](https://howiwrite.substack.com/p/morgan-housel-how-to-master-writing))。“自私写作”这个说法更早，Perell 2021 年的视频里就有“that's why i call it selfish”；Housel 自己说这是“later insight”，早年他是靠读每一条评论成长的【转录·已核】([YouTube](https://www.youtube.com/watch?v=2eT8SMtbHNI))。“假装每个词要花你 100 美元”**不是他的原创**，原话是：“I also heard, I forget who said this, but they're like, when you're writing, you should pretend that every word costs you 100… do I need this word? Do I need this sentence? Not, is this a good sentence? Just, do I need it?”【转录·已核】([YouTube 2023-11-06](https://www.youtube.com/watch?v=o84GXnrHdgg))。“People don't remember books, they remember sentences”是 Perell 在节目开场复述 Housel 对他说过的话，可以写成 Housel 的观点，但要注明“经 Perell 复述”【转录·已核】(同上)。“In summary”那条是他的原话：“The absolute worst writing, is that your last sentence is, in summary, comma… It should be some sort of emotional like, boom.”【转录·已核】(同上)。上一版说他对“写完初稿就发”的态度前后矛盾，原因是两种做法同时存在：“pretty much when I get to the bottom of the article, I just hit publish. And I don't go back and read the whole thing again. But what I do do, is every sentence that I type, After I type it, I'm like, all right, is that good?… Can I change this word?”；另一套节奏是两天构思、一天写完，“sit on it for a day… might change a sentence or two and then hit publish”。准确的版本是：**逐句精修，写到结尾就发，不回头通读全文**【转录·已核】(同上)。“初稿像吵架时的情绪爆发”这段话是 Perell 说的，不是 Housel。写作量要修正：“I was in the Motley Fool for nine years and I wrote **3,500** articles when I was there”，他的博客总数是“Pushing **4,000** blog posts. I think I'm really proud of like 10 of them”【转录·已核】(同上)。关于写书，他说一下子想写 75,000 字的书“really daunting”，但“I need 20 long blog posts… I can knock that out”；他也承认写《金钱心理学》时“I shouldn't have just pretended that that was the same thing as blogging”【转录·已核】(同上)。“写作过程本身就是研究过程”没有找到逐字原话，他 2025 年说的是 ChatGPT 作为研究工具“unbelievable”，但“every letter will be typed by me”【转录·已核】([How I Write 2025-10-15](https://howiwrite.substack.com/p/morgan-housel-how-to-master-writing))。他还保留“cutting room floor scraps”，几年后再用【转录·已核】([YouTube](https://www.youtube.com/watch?v=o84GXnrHdgg))。

### Lenny Rachitsky：约 50 个题的清单，狠删引言，改几十遍【原文已核】

Lenny 的选题和素材习惯见第一部分（约 50 个题的清单、读者问题开篇、Coda 页、乱文档）。删稿方面，上一版说“删掉初稿第一段，文章通常立刻变强（未能定位出处）”，现在找到了原句，但它说的是**他编辑的嘉宾稿**：“As an example, with almost every guest post that I edit, if I remove the first paragraph of the first draft, the post immediately gets stronger. Try this with your next piece of writing. Cut the intro and get right into it.”同一节的小标题是“Cut 30%-50% of your words”，正文还有“Make your intro 50% shorter”【原文已核】([Lenny's Newsletter “500,000”](https://www.lennysnewsletter.com/p/500000))。播客里的说法是“the introductions always just like let's just let's make this 50% shorter and that often makes it a lot better”，以及“introductions are often way too long… shut up just tell me the answer already”【转录·已核】([YouTube 2023-10-25](https://www.youtube.com/watch?v=DMZem1NYfpM))。Compound 访谈的版本是“people get in their own way and fill their writing with long intros, useless context, and uninteresting pontification… Get to the point”，并推荐《On Writing Well》“just teaches you cut cut cut, and cut some more”【原文已核】([Compound Planning](https://manual.compoundplanning.com/chapters/interview-with-lenny-rachitsky-writer-of-lennys-newsletter))。改稿遍数有两个原文版本，都成立：播客里是“I read through my posts **10 20 30 times** just again and again looking for what can I tweak what can I simplify what can I cut what can I move around”【转录·已核】([YouTube](https://www.youtube.com/watch?v=DMZem1NYfpM))；Compound 访谈里是“I then read through it dozens of times… I email myself a copy to look at it with fresh eyes… (probably on the **50th** reading), it's ready to go”【原文已核】([Compound Planning](https://manual.compoundplanning.com/chapters/interview-with-lenny-rachitsky-writer-of-lennys-newsletter))。节奏上，“500,000”一文写道：“Having a deadline to ship is an essential forcing function… Pick a cadence, share it publicly, and try your hardest to stick to it… I can only sustainably write one great post a week.”【原文已核】([500,000](https://www.lennysnewsletter.com/p/500000))。他还提到“high signal to noise, actionable, succinct”，以及朋友说的“writing friction”，即通读时留意读者在哪里被卡住【转录·已核】([YouTube](https://www.youtube.com/watch?v=DMZem1NYfpM))。上一版引自 X thread 的“公开承诺约占一半动力”和“离开前在稿子顶部写下一步”，X 打不开，2023 年的转录里也没有，**仍无法核实**【待核实】([X thread](https://x.com/lennysan/status/1347642510445711360))。

### Packy McCormick：先写一遍，再写一遍【转录·已核】

原话逐字确认：“Every time I start writing a piece, I have a title up top… And then in brackets beneath it, I put, ‘Title image.’ And then I write the piece. And then I write the piece.”V0 是删稿库（见第一部分）。截稿压力也确认：“4:30 the morning that I'm going to hit send, I wake up to maybe edit, maybe rewrite, rewrite the whole thing from 4:30 to 8:55 AM”；“the last 10 essays that I've written, I've rewritten at 4:30 in the morning”；“I started sending on Tuesday instead of Monday”【转录·已核】([YouTube 2024-02-28](https://www.youtube.com/watch?v=9Fit0knSiH8))。推广时一张好条形图或一个好数字胜过缩略图（见第一部分）。上一版说“妻子是第一读者，负责判断稿子有没有意思”，**找不到依据**：两期转录里，妻子 Pooja 只出现在两处，一是周末帮他带孩子让他写作，二是她不想回办公室成了一篇文章的灵感；转录里能找到的“一个读者”是他每天写日记给一位朋友看，“there's one person who reads it”【转录·已核】([YouTube](https://www.youtube.com/watch?v=9Fit0knSiH8); [YouTube 2021-08-20](https://www.youtube.com/watch?v=a0hOyHqli0s))。上一版引用的“Claude 几乎给每份初稿打 A-”来自打不开的 X 推文；播客里的原话是：“Claude in particular is like, ‘This is… what a contribution to the field… It's an **A**. And with this one tweak, it's definitely an **A plus**. Among the best things ever written.’”BulletPoint 的摘要写的是他用 LLM“partly for encouragement during slogs”【转录·已核】([YouTube](https://www.youtube.com/watch?v=9Fit0knSiH8); [BulletPoint](https://bulletpointpodcast.com/howiwrite/packy-mc-cormick-a-tactical-masterclass-in-online-writing/))。核心意思没变：**LLM 评审过分恭维**。他还有几条可以写成规则：“It's not the piece, it's the practice”；用 LLM 当“bomb thesaurus”，同时让它挑论证的毛病【转录·已核】(同上)。

### Ted Gioia：永远诚实，哪怕只有一个读者【原文已核】

“诚实三问”需要说明出处：三个问题是 Perell 在节目里归纳的，“there's three questions that you ask is this fair is this accurate will this be persuasive to all fair-minded observers”，Gioia 回应：“the reader wants it to be honest they want it to be fair and obviously it has to be convincing to Fair people if I'm not operating at that level I have failed.”【转录·已核】([YouTube 2024-05-29](https://www.youtube.com/watch?v=cur-LrnN8DM))。空白日记法是 Perell 在节目里朗读 Gioia 的文字：“buy a blank journal and keep in… a safe place… at the end of each day put down what happened during the last 24 hours but there's one unbreakable rule what you write in the journal must be absolutely and totally honest”，Gioia 说“I took this from somebody else the problem is I don't remember who”；“连续一个月”这个细节在转录里没有找到【转录·已核】(同上)。受众规模那句逐字确认：“If I had focused too much on the size of my audience, I would have given up decades ago. Most of my readers found me after I turned 60”；“reach out and find a reader—make a connection—even just one reader is meaningful”；“From the start, I always thought of my reader as an individual, almost as a friend”【原文已核】([Honest Broker](https://www.honest-broker.com/p/i-give-the-worst-writing-advice-in))。“先成为专家”部分确认：节目里两人讨论了“having some expertise other than just write… will make you a more powerful writer”和“build that relationship of trust with the reader”，Athens 博客的逐字说法没核【转录·已核】([YouTube](https://www.youtube.com/watch?v=cur-LrnN8DM))。他还说约一半的 newsletter 写作“has an agenda”，读者会因此不信任；“I became a writer by writing”【转录·已核】(同上)。

### Henrik Karlsson：让想法在身体里住一年【原文已核】

他说方法有用，但要“break out of the process and get lost in the desert”，并且“if I make my essays more consistent, I remove not only the mistakes but also much of the upside”【原文已核】([How I write essays](https://www.henrikkarlsson.xyz/p/how-i-write-essays))。孵化期逐字确认：“I need to let things live in my body for about a year before I can actually turn them into essays”；开头最后写：“I write the beginning and the ending when everything is already done… if I start writing an opening… I get really pretentious”【转录·已核】([How I Write 2025-08-13](https://howiwrite.substack.com/p/henrik-karlsson-the-writing-process))。那一期有一章叫“Protecting Early-Stage Ideas from Criticism”，但“压扁（squash）”这个词没有逐字找到【待核实】。Cal Newport 转述他基于 37 篇博客的数据：“spending twice as long on an article yields, on average, more than four times the number of new subscribers”【原文已核】([Cal Newport](https://calnewport.com/on-slow-writing/))。“It is the stuff about you that is odd that is interesting”和“You will develop a feel for what it is you do after about 50 essays”确认，但出处是他 2025 年 1 月 20 日的 X 线程，不是 Substack note；同一线程还有几条可用的：用截止时间调节野心（“I'm going to write the best piece I can in 20 hrs”）、先写 500 词的“问题 → 挣扎 → 洞见”小文、人在聊天消息里比在博客里更有风格【原文已核】([threadreaderapp](https://threadreaderapp.com/thread/1881287554999460250.html))。

### Ben Thompson：第二篇文章最重要【待核实】

多个播客平台的摘要都说 How I Write 那期（2024-08-21）以这句开场：“The most important article you write is the second article someone reads.”【待核实】([valueb9b](https://valueb9b.substack.com/p/ben-thompson))。“免费头版需要好钩子”“付费更新心理上很自由”“每个分号都用到极致”“一条共同的线”这四条，唯一来源是 AI 蒸馏的技能包，而技能包里也没有这几句逐字引语；完整转录没有拿到，**仍无法核实**【待核实】。

### Sahil Bloom：从对话里写作，用推文框压缩【转录·已核】

这部分依据 How I Write 转录（2023-12-20）([YouTube](https://www.youtube.com/watch?v=f-s22uCixMw))。他写之前先把想法讲给人听：“try to distill it to someone see where you didn't make sense or where they were like looking confused yeah I call this **writing from conversation**”。卡住时压进推文的字数限制，越写越短。他引用过“creative cliff illusion”，原论文未核。上一版写“95% 的爆款只是更漂亮的包装”，要补上他的限定：“within the non-fiction realm… if you look at like the power law successes… **I would guess** 95% of those are just an idea or set of ideas that already existed that are put into a slightly more beautiful package”。用词检验：“are you writing that word because you want other people to be like wow David you're so smart or are you writing that word because it adds incremental utility”。他还说“there isn't a huge correlation sometimes between how hard you work on something and how well it ends up doing”；与其靠 TED 演讲类话题触达 10 万人，不如有 1 万个真正连接的人；“every piece of writing is a call for the kind of person that you want to bring into your life”。

### Alex Hormozi：一个大想法，证据先行【转录】

本轮未重核。**Rule of One** 来自 Michael Masterson：史上最好的 100 个 offer 里有 91 个围绕单一概念，“最难的是找出那一个想法”；91/100 是他转述的数字【转录】([OyGKFhTf0go](https://www.youtube.com/watch?v=OyGKFhTf0go))。开场公式是 **Proof → Promise → Plan**【转录】([Jmkq5RLjm0U](https://www.youtube.com/watch?v=Jmkq5RLjm0U))。他总结过 40 个月的六个转变，包括从“假设观众知道”到“什么都不假设”，包装要“从模糊到清楚”，并明确反对“必须制造好奇缺口”【转录】([HVOubeXUcx0](https://www.youtube.com/watch?v=HVOubeXUcx0))。给新手：“第一年你都在找自己的声音”【转录】([7ITff1fIbSc](https://www.youtube.com/watch?v=7ITff1fIbSc))。

### Harry Dry：三个问题筛句子【转录·已核】

依据 2024-07-17 的转录([YouTube](https://www.youtube.com/watch?v=TUMjnmfsPeM))。三个问题见第一部分。能证伪就是“putting your head on the chopping block”，他的说法是“don't talk, only point”。只有你能说，来自 Jim Durfee 的“never write an ad a competitor can sign”（转录把名字识别成了 Derky）。正例是 New Balance 的“worn by supermodels in London and dads in Ohio”，反例是“Don't just get a job. Change an entire industry… Can you see that? No.”上一版说他“用对立面碰撞生成点子”，要修正：原话“I'm going to go counter position and build the opposite”讲的是他自己的产品定位，不是一套通用的点子生成法。

### The Cultural Tutor：想法刚击中你时就写【转录·已核】

依据 2023-08-23 的转录([YouTube](https://www.youtube.com/watch?v=1pBxikHRCXI))。Alexander Learmonth 说：“the best time I find to write about an idea is… when it first strikes you… because you wait a month and you'll have forgotten why it was interesting to you.”上一版标题里的“今天让我咆哮的是什么”没有逐字找到，标题已改。其余三句逐字确认：每天打开 Twitter 直接写；“my aim is to write one good sentence every day. If I write one good sentence, it's been a good day”；“to say I don't have the time to write means you don't want to write”。Perell 在同一期补了一句：“the biggest cause of writer's block isn't actually writer's block. It's just that you're not writing what you're supposed to be writing.”

### Jack Butcher：一万次迭代【转录】

依据 Perell 工作坊转录（2021-08-13，本轮未重核）([YouTube](https://www.youtube.com/watch?v=EGnSx3EYEU0))。做事过程产生的“锯末”可以直接发布。他引用 Naval：造就异类的不是 1 万小时，而是 1 万次迭代。他的定位是“你有复杂的东西要解释，我帮你可视化”。

### David Perell：CRIBS 是口头试讲时听的五种反应

perell.com 本轮返回 429，命名框架的原页没读到，但有两条经旁证确认。Raymond Chandler Rule（每 250 词一次顿悟）是他在 Tim Urban 那期口述过的：“Raymond Chandler… would have about 250 words per page. And his rule was that on every single page… there had to be one of those moments”【转录·已核】([YouTube 2024-01-03](https://www.youtube.com/watch?v=dyAiNCF2J3A))。Personal Monopoly 被学员沿用（见第一部分）。**CRIBS 要修正两处**：I 是 Interesting，不是 Insightful；而且它用在口头试讲时，不是书面反馈。原文是：“As I'm talking through my ideas with them, I'm listening for a few things in how they respond… It's called CRIBS, which stands for confusing, repeated, interesting, boring, and surprising. When an idea I throw out is confusing, repeated… or boring, I move away from it”【原文已核】([Every 2021-10-28](https://every.to/superorganizers/how-david-perell-writes-an-essay))。第三方转录的 **Writing One-Sheet**（短句、简单词、先选定一个读者、页顶写语境和一句话答案、换字体换地方朗读）仍然没有找到 Perell 本人发布的原件【待核实】([joesmusings/quartz](https://github.com/joesmusings/quartz))。他 2026 年在 Nathan Barry 访谈里说：“很多人想被听见，多过他们真有话要说”；“受众永远是对的……能火的东西就是更好，当然有明显例外”【转录】([Nathan Barry Show](https://nathanbarry.com/how-to-stand-out-as-a-writer-in-the-age-of-ai-2026-138/))。Write of Passage 的关停时间确认：Alexandra Allen 2024 年 8 月 28 日写道“Last week… Write of Passage… is ending… David Perell, announced the news on Monday”，推文 ID 解码为 2024 年 8 月 19 日（周一）【原文已核】([alexandraallen](https://alexandraallen.substack.com/p/four-life-hacks-from-the-ultimate))。关停理由“除了经济账，什么都值得庆祝”和 2025 年 2 月“部分是因为 AI 浪潮”的说法，推文打不开，仍无法核实【待核实】([X](https://x.com/david_perell/status/1825569243854962795))。

### Tim Denning：角度胜过新意，情绪是 AI 写不出来的【原文已读】

Denning 说：“我偶然学会的技能不是有新想法，而是从不寻常的视角攻击想法”；“在 AI 的世界里，你写不过 ChatGPT，所以你剩下的只有声音，和你脑子里那一库存的故事。”【原文已读】([timdenning.com](https://timdenning.com/tim-denning-is-rich/))。标题标准是五年级学生能懂，并问“凭什么有人点”【原文已读】([16 Harsh Truths](https://timdenning.com/writing-harsh-truths/))。2026 年他的说法是：“精致的东西会被遗忘，失控的东西永远不会被忘。”【原文已读】([Substack](https://timdenning.substack.com/p/not-being-unhinged-is-quietly-costing))。先写标题和要点、写和改分日做，本轮未核【待核实】([timdenning.com](https://timdenning.com/never-run-out-of-ideas/))。

### Nat Eliason：太守规矩就像 AI 写的（区分 2018 与 2024）【原文已核】

本轮发现上一版把他 2018 年和 2024 年两篇文章的观点混在了一起，这里分开。**2024 年《On Writing Better》**：“good writing is the Grammarly fixes you ignore… If you follow all the normal writing rules too closely, your writing will sound AI generated”；“A shitty draft is much better than an unfinished draft. So give yourself permission to write slop for a bit”；写书时完整初稿完成前不做任何编辑，只发一章给别人要反馈，编辑时最重要的是走开一段时间【原文已核】([nateliason.com](https://www.nateliason.com/blog/on-writing-better))。**2018 年《How to Become a Better Writer》**：“put ‘TK’ anywhere you aren't sure of a detail… Think of it as ‘To Come’”；“Avoid ‘I think,’ ‘I believe,’ ‘It seems’”；“You shouldn't be writing 8-10 sentence paragraphs unless you have an important point”；“Vary Your Sentence Length”；“Looking at a piece in different places in different mental states will help you see it differently”；还有一条“ignore the rules occasionally”。上一版说他认为“删副词没抓住要点”，2024 年文里找不到，而 2018 年他恰好主张“delete your adverbs”，只是加了一句“more about extreme pruning than outright abstinence”【原文已核】([better-writer](https://www.nateliason.com/blog/better-writer))。他引 Stephen King：“When you first write something, you should write it for yourself. When you rewrite it, write it for everyone else.”【原文已核】([nateliason.com/notes](https://www.nateliason.com/notes/writing-stephen-king))。

### 其他值得收进知识库的心法（简表）

| 创作者 | 心法 | 证据 |
|---|---|---|
| Tyler Cowen | “I don't let it write for me… it's like my little baby”；“I want it to stay weird. I will use it to fact-check things in areas I don't know” | 【转录·已核】([How I Write 2025-03-05](https://howiwrite.substack.com/p/tyler-cowen-will-ai-kill-writing)) |
| Sam Parr | “从很多地方偷，然后搅在一起……每个词都要有用”；用五年级阅读水平写作 | 【转录】([YouTube](https://www.youtube.com/watch?v=CO2ELWa3jsc)) |
| Naval / Eric Jorgenson | 压缩越精确，失去的读者越多；推文是压缩版，书和播客是“展开”版 | 【转录】([YouTube](https://www.youtube.com/watch?v=mWYMRCcYn-Q)) |
| Marc Andreessen | 杠铃式阅读：只读极新的和永恒的 | 【转录】([YouTube](https://www.youtube.com/watch?v=tV6kDr1rwTs)) |
| Justin Welsh | 先试一堆东西看什么有效；内容矩阵据称已停用；官网自述“$15M one-person business” | 【待核实】([Productive Insights](https://share.transistor.fm/s/82af7ab4))；营收【原文已核】([justinwelsh.me](https://www.justinwelsh.me)) |
| Dickie Bush / Nicolas Cole | Ship 30 自 2020 年 11 月起已办 24 期、教过 10,000 多名学员；下一期 2027-01-18 | 【原文已核】([ship30for30.com](https://www.ship30for30.com)) |
| Shaan Puri | 故事 = 意图 + 阻碍 + 利害；“像说话一样写” | 【待核实】([Recapio](https://recapio.com/digest/masterclass-in-storytelling-for-beginners-with-shaan-puri-by-david-perell)) |
| Darius Foroux | 不定字数目标，每天写一句也算；Medium 上至今非常活跃（RSS 最新一篇 2026-11-03） | 方法【待核实】([dariusforoux.com](https://dariusforoux.com/daily-writing-habit/))；活跃度【原文已核】([RSS](https://medium.com/feed/@dariusforoux)) |
| Ali Abdaal | FBR（Fast, Bad, Wrong）初稿；搜集、起草、编辑三种模式分开 | 【待核实】([aliabdaal.com](https://aliabdaal.com/newsletter/the-acronym-that-changed-how-i-write/)) |
| Shannon Ashley | “不在于完美，在于诚实”；袒露多少由作者决定；仍在 Medium 活跃（2026-10-26） | 心法【待核实】([Medium](https://medium.com/@Shesreallyfat/my-rules-for-authentic-and-vulnerable-writing-364c0aeeb5ce))；活跃度【原文已核】([RSS](https://medium.com/feed/@Shesreallyfat)) |
| Zulie Rane | 20% 时间写不赚钱的东西以防倦怠；仍在 Medium 活跃（2026-09-21） | 心法【待核实】([Zulie Writes](https://www.zuliewrites.com/blog/why-i-spend-20-of-my-writing-time-on-unprofitable-work))；活跃度【原文已核】([RSS](https://medium.com/feed/@zulie)) |
| Sinem Günel | 理想读者画像“Jennifer”：背景、信念、目标、困难与恐惧 | 【待核实】([Write Build Scale](https://writebuildscale.substack.com/p/how-to-build-ideal-reader-persona)) |
| Benjamin Hardy / Ayodeji Awosika | 先搭结构再自由写；每天写 10 个标题；“采访过去的自己” | 【待核实】([Kickstarter](https://medium.com/the-kickstarter/how-to-write-like-a-1-medium-com-writer-ben-hardys-system-916dd720069b)) |
| George Mack | 在 Kindle 上读自己的稿子（换媒介检验） | 【待核实】（只有弱来源） |

一条平台层面的旁证：Towards Data Science 据其自己的公告于 **2025 年 2 月 3 日**作为独立刊物上线，原因是“Medium began redirecting content from our custom domain at the end of January 2025”；正文未能逐字读到【待核实】([TDS](https://towardsdatascience.com/towards-data-science-is-launching-as-an-independent-publication/))。连同 Denning、Kuegler 停更 Medium，可以看出头部作者和大型刊物都在把 Medium 从“主场”降为“辐条”。

---

## 心法共识与分歧，以及哪些能交给机器

### 八条强共识

**第一，写作产生想法，不只是记录想法。** PG 说 80% 的想法在动笔后才出现【原文已读】；Koe 说“强制线性”【转录】。**第二，选题的过滤器是真实兴趣。** PG 说“你必须在乎”，Housel 主张自私写作，Lenny 选让自己最兴奋的题，Cultural Tutor 在想法刚击中自己时就写，Koe 问“我是否觉得重要”。**第三，删是核心技能。** PG 删掉 17 段的子树，Housel 转述的“每个词值 100 美元”，Lenny 把引言砍掉一半、全文删 30–50%。**第四，清楚胜过聪明。** Hormozi 的“从模糊到清楚”、Bloom 的效用检验、PG 的“写得简单”是一个意思。**第五，具体和证据是护城河。** Dry 的能想象、能证伪，Hormozi 的证据先行，Newton 的“原创报道和意外”，Medium 把“亲身经验比头衔更重要”写进了 Boost 标准。**第六，量是学徒期，时间尺度是年。** Housel 在 Motley Fool 九年写了 3,500 篇、博客近 4,000 篇，Karlsson 说要写到约 50 篇，Hormozi 说“第一年在找声音”。**第七，不是新意，是视角。** Denning 从不寻常的视角攻击想法，Bloom 猜非虚构爆款 95% 是包装，Koe 借想法不借措辞。**第八（本轮新增），先判断想法行不行，再决定要不要打磨。** Housel 说失败的那篇是因为“the idea sucked”，Karlsson 让想法住一年，PG 说没有 edge 就别写；另外，为一个具体的人写，像写日记、写聊天消息那样写，这一点在 Housel（日记）、Karlsson（聊天消息）、Packy（写给一位朋友看的日记）、Gioia（把读者当朋友）那里反复出现。

### 六处真实分歧，以及怎样调和

| 分歧 | 一方 | 另一方 | 调和方式【设计建议】 |
|---|---|---|---|
| 为谁写 | Housel：别管读者，自私写作 | PG：过陌生人测试 | 分阶段：选题可以自私，执行要对读者严格 |
| 起稿方式 | PG、Abdaal、Eliason（2024）、Foroux：先快后改 | Housel：逐句精修，写到结尾就发 | 由作者的自然单位决定：短篇可以边写边改，长篇综合稿需要多轮重写 |
| 节奏 | Welsh、Koe：批量、排期 | Cultural Tutor、Newton（2026）：有东西才写 | Agent 先问作者是“系统型”还是“执念型”，再选工作流 |
| 钩子 | Welsh 的标题（据报）偏悬念 | Hormozi：从模糊到清楚；Medium：过于神秘和过于煽情一样糟 | 默认用清楚的承诺；悬念式标题只当 A/B 变体 |
| 病毒传播 | Perell：能火的就是更好 | Medium 官方：别追求爆款；Kuegler：“病毒垃圾” | 把爆款当信号而不是目标；负反馈和退订是红线 |
| 规则与声音 | Eliason（2018）：删对冲词、删副词；Perell 的 One-Sheet | Eliason（2024）、Denning：守规矩就像 AI | 规则检查只标记，不自动改；保留作者有意的破格 |

孵化时长也有分歧：Karlsson 让想法住一年，PG 说几天，Packy 周更且发布当天凌晨 4:30 还在重写，Housel 两天构思一天写完。这说明“稿子好了没有”的判断，对有截稿的作者部分由时钟决定，对没有截稿的作者由“刺”和饱足感决定。

### 心法到 Agent 的映射：哪些写成清单，哪些必须留给人

| 心法 | 来源 | Agent 形态 | 归属 |
|---|---|---|---|
| 中立陌生人重读 | PG【原文已读】 | 只拿到终稿的干净语境评审者，列出缺失前提、未限定论断和跳跃 | Agent |
| 拔刺 | PG【原文已读】 | 多次采样通读，产出“摩擦热点”报告 | Agent 标记，人决定 |
| 有用性四因子 | PG【原文已核】 | 对每条论断打真实/重要/新颖/强度分 | Agent |
| 树搜索与快刀斩 | PG【原文已核】 | 提纲树视图；标出偏离初始问题的子树 | Agent 建议，人裁剪 |
| 防误读 | PG【原文已核】 | 扮演“聪明而善意的误读者” | Agent |
| 句子三问 | Dry【转录·已核】 | 逐句打能想象/能证伪/只有你能说 | Agent |
| Rule of One；Proof → Promise → Plan | Hormozi【转录】 | 一句话写出大想法；开头结构检查 | Agent |
| 效用还是炫耀 | Bloom【转录·已核】 | 标出只为显得聪明的词 | Agent |
| 压缩到 280 字 / 展开 | Bloom【转录·已核】、Jorgenson【转录】 | 论点压缩练习 | Agent |
| CRIBS（Interesting）| Perell【原文已核】 | **访谈模式里**：Agent 扮听众，作者口述，Agent 按五种反应标注；书面评审里作为辅助维度 | Agent 标注，人取舍 |
| 每 250 词一次顿悟 | Perell【转录·已核】 | 标出连续 500 词以上没有新信息的区段 | Agent |
| 诚实三问 | Perell 归纳、Gioia 认可【转录·已核】 | 公平、准确、能否说服公正者三问评分 | Agent 初评，人终审 |
| 每词 100 美元、不写“In summary” | Housel（前者为转述）【转录·已核】 | 行级 lint | Agent |
| 引言砍半、全文删 30–50% | Lenny【原文已核】 | 字数与引言长度检查；生成“删掉首段”对照版 | Agent 建议，人选 |
| TK 占位、删对冲词 | Eliason 2018【原文已核】 | lint，并拦截含 TK 的稿件发布 | Agent |
| 五年级标题、凭什么点 | Denning【原文已读】、Cole【待核实】 | 标题评分 | Agent |
| 讲出来再写、写成给朋友的消息 | PG【原文已读】、Bloom【转录·已核】、Karlsson【原文已核】 | 访谈模式：Agent 提问，人口述，Agent 转写 | 人出内容，Agent 出结构 |
| 异常值和旧爆款扫描 | Koe【转录】 | 抓取热门内容，拆解结构 | Agent |
| 聚合与每日链接摘要 | Newton【原文已核】 | Agent 自动做，只当选题线索，不当成品 | Agent |
| edge / 初始洞见 | PG：“没法系统地生成” | 只能列出候选“缝隙” | **人** |
| 真实兴趣、这个想法行不行 | PG、Housel、Cultural Tutor | 让作者给兴奋度打分，并写一句 edge | **人** |
| 亲身故事、第三方证明、真实数据 | Hormozi、Denning、Medium 政策 | Agent 只能从人提供的材料里取用，**绝不编造** | **人** |
| 袒露多少、情绪基调 | Ashley、Denning | — | **人** |
| 声音与怪癖 | Cowen、Karlsson、Eliason | 只做风格漂移监控 | **人** |
| 结尾、品味 | PG、Housel（“boom”）、Koe | 可以提几个候选结尾 | **人** |

Hormozi、Denning 和 Medium 的政策从三个方向指向同一个结论：**Agent 永远不能编造轶事、数字或“亲身经历”**。Medium 的 AI 政策还把“easily disprovable AI-hallucinated stories, statistics, events”单列为禁止项【原文已核】([Help: AI policy](https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy))。这一条在下文所有闸口里都是一票否决项。另一条本轮新得到的教训是：**LLM 评审天生过分恭维**（Packy 被打 A 和 A+），评审必须用作者认定的好稿和差稿做锚点。

---
# 第三部分：可构建的多平台创作 Agent 手册

> 本部分除注明来源者外，均为【设计建议】。架构原则依据 Anthropic 的三篇工程文章【原文已读】，平台约束依据第一部分（本轮已核），质量闸口依据第二部分。与上一版相比，改动集中在 S5 评审、S6 适配、S7 发布、S8 复盘和 `platforms/*.yaml` 配置。

## 架构：一条核心流水线，加一层平台适配和多个发布模块

**先用工作流，不急着上自主 Agent。** Anthropic 区分两种系统：**工作流**是 LLM 和工具按预定义的代码路径编排；**Agent** 是 LLM 在循环里根据环境反馈自己决定调用工具。它的建议是“找到最简单的方案，只在需要时增加复杂度”，并且先直接调用 LLM API【原文已读】([Building effective agents](https://www.anthropic.com/engineering/building-effective-agents))。多 Agent 只适合宽度优先、可以并行的研究任务：Opus 4 主控配 Sonnet 4 子 Agent，在内部研究评测上比单 Agent 高 **90.2%**，代价是约 **15 倍**于普通对话的 token；在“所有 Agent 必须共享同一语境”的任务上并不合适【原文已读】([multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system))。用同一种声音写作正属于后者。所以这套系统只在研究阶段并行，写作和编辑交给单一写手，评审者从干净语境出发。

**平台规则的变化让架构更简单了。** 上一版担心 Agent 在 X 上“自主互动”带来的封号风险，需要层层设闸。现在 X 的自助档 API 已经不能主动回复、点赞、关注和引用，Medium 不发新 token，Substack 没有写入接口。三个平台的官方写入通道加起来只剩三件事：**X 发原创帖、X 建 Articles 草稿、Medium 旧 token 建草稿**。所有互动类动作都只能由人在客户端里做。这反而让 Agent 的边界变清楚了：它负责生产和准备，人负责发布和对话。

**在单平台流水线上加三层。** 第一层是**平台适配层**：把一份母稿转成各平台的原生变体，每个变体是一条独立记录，有自己的闸口和指标。第二层是**按平台划分的发布模块**：按平台实际允许的程度，分为 API、排期工具、人工粘贴、人工 Import 四种能力等级，统一由人按最后一键。第三层是**度量回流**：每个变体都带 UTM，按平台口径采集，再写回知识库。

```
                         ┌──────────────── L0 知识库 / 记忆 ────────────────┐
                         │ voice/ · backlog/ · swipe/ · sources/ · archive/ │
                         │ platforms/*.yaml（平台规则配置，按月核对）        │
                         └──────────────────────────────────────────────────┘
 L1 核心流水线（平台无关，产出“母稿 hub”）
 S0 收件分拣 → S1 选题定角 ─H1→ S2 研究取证 ─H2→ S3 论点提纲 ─H3→
 S4 起草（模式A人写 / 模式B辅助 / 访谈模式I）→ S5 编辑评审 ─H4（定稿·事实）→ hub
                                                                              │
 L2 平台适配层  S6：hub → variants[]（按语言与 draft_mode 过滤可发平台）        ▼
   ┌───────────────┬───────────────┬──────────────┬──────────────┬─────────────┐
   │substack_post  │substack_note×N│ x_post×N     │ x_thread     │ medium_story│
   │（母稿本体）    │               │ x_article    │              │（英文·Import）│
   └───────┬───────┴───────┬───────┴──────┬───────┴──────┬───────┴──────┬──────┘
           │ 各变体：平台闸口 G-SS / G-SN / G-XP / G-XT / G-XA / G-MD ─H5（批量审批）
 L3 发布模块 S7（每个平台按能力分级，统一 H6 人工按键）
   Substack：人工粘贴/发送；Notes 原生定时或 Typefully
   X：单帖走 OAuth 按次付费 API；Articles 走 API 建草稿、人点发布；线程待实测
   Medium：人工 Import（自动 canonical）→ 投稿出版物 → 勾选通知订阅者
           │
 L4 度量回流 S8：UTM 归因 → X Owned Reads / Substack CSV 或 MCP / Medium 人工 → 月度复盘 ─H7 → L0
 旁路：R1 短养长（爆款短帖 → 晋升为长文选题）；R2 常青回收（≥90 天，用新角度重写）
 人工通道：所有回复、点赞、关注、引用、私信只由作者本人在客户端完成
```

**七个人工闸口。** H1 选定题目，作者给兴奋度打分并写一句 edge。H2 确认研究简报。H3 批准论点和提纲。H4 定稿，逐条核对引语和数字。H5 批量审批各平台变体。H6 按下发布键，每个平台各按一次。H7 批准对声音档案、排序权重和平台规则的修改。用 LangGraph 实现的话，每个闸口就是一个 `interrupt()`：状态由 checkpointer 持久化，图会无限期等待，直到收到 `Command(resume=...)`；演示用 `InMemorySaver`，生产环境换成 Postgres 或 SQLite【待核实】([LangGraph docs](https://docs.langchain.com/oss/python/langgraph/add-human-in-the-loop))。MVP 阶段可以完全不用框架：一个脚本，每个阶段把结果写进 markdown 文件，人改完再跑下一步。

**四个必须写进配置的开关。**

| 开关 | 选项 | 依据 | 默认 |
|---|---|---|---|
| `draft_mode` | A：人写核心论证，Agent 负责研究、编辑和改编；B：Agent 按批准过的提纲起草，人重写关键段；I：访谈模式，Agent 提问、人口述、Agent 转写整理 | PG“讲给别人听，再写下来”【原文已读】；Medium 现行 AI 政策【原文已核】 | A。**B 模式的稿子不发 Medium**：即使披露，AI 生成的内容在 Medium 只有关注者分发 |
| `rhythm` | systems（周母题、批量、排期）或 obsession（有东西才写、当场写） | Welsh、Koe 对 Cultural Tutor、Newton 2026 | 问作者 |
| `flow` | long→short（母稿拆分）、short→long（爆款晋升）、both | Koe、Welsh 对 Naval | both |
| `languages` | 母稿语言；是否另出人写的英文版 | Medium 非英文不进 General、不进 Boost【原文已核】 | 中文作者：`hub: zh`，`medium: en_rewrite_only` |

## 各阶段模块规格

### S0 收件分拣（一次路由调用，不设闸口）

输入包括 RSS 条目、Readwise Reader 存档、读者回复、语音备忘录转写、随手记、作者自己的爆款短帖（R1 回流）和他人的异常值内容。输出是给每条素材打标签，路由到四个去向之一：选题池、资料库、swipe 库，或“立刻可写”。RSS 用 feedparser；Readwise Reader API v3 是 `GET https://readwise.io/api/v3/list/`，请求头带 `Authorization: Token XXX`，游标分页，社区工具报告 LIST 接口限流每分钟 20 次【待核实】([Reader API](https://docs.readwise.io/reader/docs/api))。Newton 用自动化的每日链接摘要找选题，自评“about as good a job as I do”【原文已核】([Platformer](https://www.platformer.news/platformer-schedule-changes-ai-automation/))，S0 就是这个角色：**聚合只当线索，不当成品**。每周人工抽查一次路由准确率。

```text
[系统] 你是{作者}的收件分拣员。作者的固定视角：{lens}。
对每条输入只输出 JSON：{"route":"backlog|source|swipe|now","why":"≤20字",
"lens_fit":0-3,"is_outlier":bool,"tags":[...]}
规则：lens_fit=0 的一律 route=source；读者原话提问必须 route=backlog 并保留原文；
他人高表现内容 route=swipe，只记录结构、钩子类型和数据，不保存可直接复用的原句。
```

### S1 选题定角（并行生成 + 排序；闸口 H1）

输入是选题池候选、本周输入流、往期档案、读者投票和 swipe 库里的异常值。输出是 3–5 个“题目 × 角度”方案。每个方案写清：edge（别人视为理所当然、作者却有疑问的点）、一句可以被反驳的论点、Rule of One 的大想法、角度类型、为什么是现在、读者收益、需要哪些人类证据（亲身经历、数据、采访），以及和往期重复的风险。

| 排序维度 | 权重 | 依据 |
|---|---|---|
| 作者兴奋度（人工 1–5 分） | 0.30 | Lenny“I pick the topic I'm most excited to write about”【原文已核】；PG |
| edge 强度（人工确认） | 0.20 | PG；Housel“动笔前就放弃不成立的题” |
| 视角契合度 | 0.15 | HCR、Koe |
| 市场信号（读者提问、投票、异常值、自己旧帖的表现） | 0.15 | Lenny 读者问题开篇、Yglesias、Koe |
| 可获得的人类证据或独家素材 | 0.15 | Hormozi、Newton、Medium“first-hand experience” |
| 时效 | 0.05 | 日更作者 |

```text
[系统] 为{作者}生成选题角度。视角：{lens}。读者画像：{persona}。
往期相似题目（禁止重复其论点）：{archive_hits}。参考的异常值结构：{outlier_patterns}
（只借结构与包装类型，禁止借措辞）。
对「{idea}」给出 {N} 个互不相同的角度，每个包含：
edge（列出一个“人们视为理所当然、但值得怀疑”的前提）/ thesis（一句可证伪的论点）/
one_big_idea（易懂、易信、独特）/ angle_type（actionable|analytical|aspirational|anthropological）/
why_now / reader_payoff / human_evidence_needed（需要作者提供的亲身经历、数据或采访）/ risk。
不得编造任何事实或经历；不确定的地方写“[需作者确认]”。
```

`angle_type` 借用了 Ship 30 的 4A 分类，官方措辞未核实，只当作生成多样性的提示【待核实】。H1 的规则是：作者必须亲手填兴奋度，并用一句话写下自己的 edge。**写不出 edge 的题目退回选题池。**

### S2 研究取证（编排者-工作者；闸口 H2）

这是唯一使用多 Agent 的阶段。主控把问题拆成子问题，每个子 Agent 都要拿到明确的目标、输出格式、工具和信源指引以及边界，否则会重复劳动；简单的事实查找用 1 个 Agent、3–10 次工具调用；研究完成后由单独的引用 Agent 把每条结论绑定到来源。Anthropic 的人工测试发现，Agent 偏爱 SEO 内容农场，需要在提示词里加入信源质量启发式【原文已读】([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system))。子 Agent 只返回浓缩摘要，原文以路径保存，用时再加载【原文已读】([context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents))。另设一个**人类素材子任务**：从作者的会议转录、语音备忘录、旧日记里挑出“有意思的时刻”（Hormozi 的做法），交给作者确认。

本轮核实本身给 S2 提供了一条经验：**AI 蒸馏的二手材料会补全细节**，而原页常被 Cloudflare、429 限流挡住。研究子 Agent 应当优先走官方的机器可读通道（Zendesk API、RSS、`.md` 文档、`/api/v1/posts/` JSON），并把 `read_level` 和 `access_path` 记进每条 finding【设计建议】。

```text
[子Agent任务书]
目标：回答「{sub_question}」，服务于论点「{thesis}」。
输出：最多 8 条 finding：{claim, quote_verbatim, url, access_path, source_type: primary|secondary|aggregator|ai_distilled,
read_level: full_text|transcript|snippet, date, confidence}，外加 counter_evidence。
信源优先级：作者原文/官方数据/同行评审 > 权威媒体 > 聚合站 > AI 蒸馏；
聚合站、AI 蒸馏或 snippet 不得单独支撑数字或引语。
找不到就写“未找到证据”。边界：不写文章，最多 {k} 次工具调用。
```

H2 检查清单：每个数字至少有 1 个一手来源，高风险事实要有 3 个独立来源（HCR 的规则）；引语能在原文里逐字找到，而且**归属正确**（是本人说的，还是转述别人、还是主持人复述）；至少列出 1 条反方证据；列出需要人去补的采访或数据；`read_level=snippet` 和 `ai_distilled` 的来源不能单独支撑结论。

### S3 论点与提纲（链式；闸口 H3）

输出分三块。第一块是**页顶简报**：语境、要回答的问题、一句话答案（Perell 的 One-Sheet 做法，原件未核实，当作通用技巧）。第二块是逐段提纲，每段注明 `source_id` 或标为“观点段”，并用一句话写出这段要说什么（Doomberg：先定标题，再给每段写一句话摘要【原文已核】）。第三块是提纲树，按 PG 的方法标出每个分支的普遍性和新颖性，以及偏离初始问题的子树。另附一个“核心画面”：一张条形图或一个惊人数字，供推广使用（Packy【转录·已核】）。程序检查有四项：论点可证伪；每节服务于 one_big_idea；每段有来源或被标为观点；每约 250 词至少规划一个顿悟点（Chandler Rule）。

### S4 起草（三种模式）

**模式 A（默认）**：Agent 不写正文，只提供提纲、素材卡片和“下次从这里开始”的提示。这一条依据的是 PG 的“收工时给自己留一个容易开头的地方”【原文已读】；上一版挂在 Lenny 名下的“明天的提示”，出处推文打不开，仍待核实。**模式 I（访谈）**：Agent 按提纲逐节提问，作者口述，Agent 整理成稿，**只调整顺序和删冗，不添加内容**。这对应 PG 的“讲给别人听”、Bloom 的“writing from conversation”和 Karlsson 的“人在聊天消息里更有风格”。Agent 在访谈中扮演听众，按 Perell 的 CRIBS 标注作者口述里哪些地方 Confusing、Repeated、Interesting、Boring、Surprising，这正是 CRIBS 的原始用法【原文已核】。**模式 B**：单一写手 Agent 起草，一次装入声音档案、5–15 段范文、提纲和研究简报。

```text
[系统·模式B] 你在为{作者}起草，不是替他发表。严格遵守 voice_profile 与 never_list。
范文（只学节奏与手法，禁止复用句子）：{exemplars}
页顶简报（每句都必须与之相关）：{top_of_page}
事实只能来自研究简报，每个事实后标 [source_id]；缺来源的地方写 [TK: 需作者补充]。
亲身经历、数字、对话一律不得生成，留 [TK: 作者经历]。
立场只能用 stances.md 中已有的；没有的写 [TK: 作者确认立场]。
开头直奔主题，不写铺垫段（Lenny：删掉初稿第一段，文章往往立刻变强）。
```

含有 `TK` 的稿件在 S5 会被**硬拦截**（Eliason 2018 的 TK 做法）。模式 B 产出的稿子在 `compliance.ai_assist_level` 里记为 `draft_B`，S6 不会为它生成 `medium_story` 变体。

### S5 编辑评审（评审-优化循环，干净语境；闸口 H4）

评审 Agent 不继承写手的对话历史，只读终稿、页顶简报、声音档案和评分标准。Anthropic 认为评审-优化模式适用于“评估标准清晰”的场景，它的实践是用单次调用打 0.0–1.0 分，再加通过或不通过，这样与人工判断最一致【原文已读】([Anthropic](https://www.anthropic.com/engineering/building-effective-agents); [multi-agent](https://www.anthropic.com/engineering/multi-agent-research-system))。评审分五组并行跑，结果汇总成一份报告。

| 组 | 检查项 | 方法 | 不通过阈值 |
|---|---|---|---|
| 理解 | **陌生人重读**（PG） | 无背景的评审者复述论点，列出缺失前提和跳跃 | 复述和页顶答案不一致；或有未解释的前提 |
| 理解 | 防误读（PG） | “聪明而善意的误读者”列出 3 种可能的误读 | 误读在正文里没被堵住 |
| 论证 | **有用性四因子**（PG） | 对每条核心论断打真实/重要/新颖/强度分 | 任一核心论断“真实”分低于 1；或过度断言 |
| 论证 | **诚实三问**（Perell 归纳、Gioia 认可） | 公平？准确？能说服所有公正的观察者？ | 任一项为否 |
| 论证 | Rule of One / 树剪枝 | 每节与大想法的相关度；标出跑题子树 | 有节与大想法无关，又没移进尾注 |
| 句子 | **Dry 三问** | 抽检核心句：能想象、能证伪、只有你能说 | 核心句三项全否 |
| 句子 | 效用还是炫耀（Bloom） | 标出为显得聪明而用的词 | 只标记 |
| 句子 | 引言与删减（Lenny） | 引言占比；生成“删掉首段”的对照版；全文能否再删 30% | 引言超过全文 15% 时提示 |
| 句子 | 行级 lint | 禁用词、对冲词、感叹号、“In summary”式结尾、超长段落、句长方差、AI 腔词表 | AI 腔每千字超过 3 次；结尾是总结段 |
| 读者 | 五类读者反应（借 CRIBS 的维度） | 按段标注 Confusing / Repeated / Interesting / Boring / Surprising | C 或 B 段占比超过 15% |
| 读者 | 每 250 词一次顿悟 | 标出连续 500 词以上没有新信息的区段 | 只标记 |
| 读者 | **拔刺**（PG） | 3 次独立采样通读，交叉出现的摩擦点进报告 | 有未处理的刺（由人决定） |
| 事实 | 逐条核查（SAFE 式） | 拆出可核查论断 → 重新打开来源 → 确认原文里确实有，归属正确 | 引语或数字的支撑率低于 100% |
| 事实 | 原创性 | 与来源、往期文章做 n-gram 重叠检测 | 连续 8 个词以上重叠且未加引号 |
| 声音 | 风格漂移 | 句长分布、功能词频，与档案的距离 | 超出往期均值 2σ |
| 平台 | AI 透明度预检（可选） | Substack 允许作者在发布前对草稿运行官方扫描【原文已核】；把结果和作者的 AI 使用记录对照 | 只提示，不拦截；由作者决定是否开扫描、是否写“How I make this” |

事实核查借用 Google 的 SAFE：先把长文拆成单条事实，再逐条搜索验证；SAFE 与人工标注的一致率为 72%，成本低 20 倍以上【待核实】([arXiv 2403.18802](https://arxiv.org/abs/2403.18802v3))。72% 意味着它只能做初筛。**评审必须校准**：Packy 在播客里说 Claude 给他的稿子打“A，改一处就是 A+”【转录·已核】([YouTube](https://www.youtube.com/watch?v=9Fit0knSiH8))，所以每个评审提示词都要附 2 篇作者认定的差稿和 2 篇好稿作为锚点，每个扣分点都要求引用原句。**lint 只标记，不自动改**：Eliason 2024 年说完全守规矩的文字读起来像 AI【原文已核】，作者可以在 `voice/deliberate_breaks.md` 里登记有意的破格，lint 跳过这些。

```text
[系统·陌生人评审] 你是一位聪明、善意、对作者一无所知的读者。你只看到下面这篇文章。
1) 用一句话复述它的核心主张；2) 列出你读到时缺少的每一个前提（引用原句）；
3) 列出每一处“为什么突然说这个”的跳跃；4) 列出你最可能产生的 3 种误读。
不要评价文采，不要给总分，不要提出新论点。
[系统·拔刺] 慢读全文。只标出让你“卡一下”的句子：别扭、含糊、可能不真、读来乏味。
每条给出原句、卡住的原因（≤15字）。不要改写。
[系统·反恭维] 你的默认倾向是过度夸奖。先对照锚点稿 {bad_1},{bad_2},{good_1},{good_2}
给本稿排位，再说理由；没有引用原句的优点一律不计。
```

H4 的人工核对清单：每条引语逐字回到原链接，并确认是本人原话还是转述；每个数字回到一手来源；每段亲身经历由作者确认确实发生过；涉及真实人物的负面陈述再查一遍；全文由作者朗读一遍，或换一种媒介读；**结尾由作者本人拍板**。

### S6 平台适配层：一份母稿，多个原生变体（闸口 H5）

适配层的输入是定稿 hub 和 `platforms/*.yaml` 里的平台规则，输出是一组 `variant` 记录。原则仍是 Denning 说的“像学一门语言”：**改写，不要转贴**。新增一条前置过滤：根据 `hub.language` 和 `compliance.ai_assist_level`，先决定哪些平台可以出变体。中文母稿或 B 模式母稿，不出 `medium_story`；需要 Medium 版的，另走“英文人写重写”子流程。

| 变体 | 生成规则 | 依据 |
|---|---|---|
| `substack_post`（母稿本体） | 2–4 个标题候选供原生 A/B 测试；副标题；付费墙位置，或 freewall / metered paywall 的设置；用 post template 固定 CTA、免责声明和 AI 披露；页脚放推荐 | Substack 2026 功能【原文已核】 |
| `substack_note` ×3–10 | 金句、图表、反直觉断言、提问；单条以拉免费订阅为目标，整体当作付费增长入口 | 0.70% 研究与“App 付费一半以上来自 Notes”【原文已核】 |
| `x_post` ×3–7（散布在一周） | 每条一个自足的想法，过 Dry 三问；根帖默认不放链接；每条设计一个能引发回复的点（回复由作者本人做） | 回复权重 5.0；API 不能主动回复【原文已核】 |
| `x_thread` ×0–1 | 首帖要能单独成立，中间每帖一个要点，末帖回扣钩子并放 CTA；**发布方式待 P2 实测**（API 自回复是否被允许未明） | DedupConversationFilter；2026-02-23 回复限制 |
| `x_article` ×0–1 | 母稿的完整版或精简版，转成 DraftJS `content_state`；开头按 Proof → Promise → Plan 重写；配一条能独立成立的推广单帖 | Koe 的做法；Articles API【原文已核】 |
| `medium_story` ×0–1（**仅英文、仅 A 或 I 模式**） | 默认用 Import 从母稿 URL 导入；另写 Medium 专用的标题、副标题和封面图说明；含 AI 辅助生成的句子或图片时，前两段放披露句；结尾 CTA 是次要目的；选定要投稿的出版物 | Medium 现行指南与 AI 政策【原文已核】 |

```text
[系统·X 单帖改编] 从母稿中挑出 {n} 个可以独立成立的想法。每条：
≤280 字符（或作者 Premium 长帖上限 {limit}）；一个想法；开头一句就给出具体的东西（数字、画面、反常识）；
过三问（能想象/能证伪/只有作者能说）；不加链接、不加 hashtag、不 @ 线程外的人；
结尾留一个读者能回答的具体问题或可反驳的断言（目标：回复，而非点赞）。
不得写“如何在 X 上赚钱”一类的变现教学内容（Original Content Rewards 不计酬）。
禁止新增母稿中没有的事实或经历。输出 JSON 数组并给每条打三问分。
[系统·Medium 包装] 前提：本文为英文、人写为主。为 Import 后的文章写：
title（五年级学生能懂；回答写什么/给谁/承诺什么；不神秘、不套路、不煽情）、
subtitle（补足语境）、cover_note（建议用真实图片；无合适图片宁可不用封面）、
disclosure（如含 AI 辅助生成的文字或图片：一句放进前两段）、
cta（一句指向 newsletter 的话，带 UTM；不得成为全文主要目的）、
target_publications（2–3 个开放投稿的高质量出版物）。不改正文。
```

### S7 发布模块：每个平台按能力分级（闸口 H6）

| 平台 / 体裁 | 能力等级 | 推荐实现 | 禁止或不可行 |
|---|---|---|---|
| Substack 长文 | 人工粘贴 | Agent 输出可直接粘贴的 HTML/markdown、所选 post template 名称、付费墙或 freewall 设置、发送前清单；人粘贴、选标题测试、按发送 | 默认不用 cookie 型非官方 API；作者明确开启时也**只建草稿** |
| Substack Notes | 原生定时 / 排期工具 | 人在 Substack 里起草和定时（2026 年起官方支持）；或用 Typefully 的 `substack` 平台【原文已核】([Typefully API](https://typefully.com/docs/api.md)) | 批量刷屏 |
| X 单帖 | API（按次付费） | 作者本人的 OAuth 2.0 用户 token；Agent 排队，人逐条或按批批准；帖子间隔数小时；正文含 URL 的帖子按 $0.20 计 | API 已不能点赞、关注、引用；只能回复召唤了你的帖子；AI 自动回复须事先批准；**浏览器自动化永久封号**【原文已核】 |
| X Thread | 待实测 | P2 先用测试账号验证“API 回复自己的帖子”能否通过；不行就交给 Typefully 或人工发 | 不要为了发线程去 @ 自己或绕规则 |
| X Articles | API 建草稿 + 人工发布 | `POST /2/articles/draft` 建草稿 → 人在客户端检查排版 → 人点发布，或人批准后调用 `/publish`；也可用 Typefully 的 `x_article` | 价格未单列，先小量试；不与其他平台混发 |
| X 互动（回复、点赞、关注、私信） | 仅人工 | Agent 每天给作者一份“值得回复的评论”清单和可选的回复要点，作者自己在客户端写和发 | 任何自动互动 |
| Medium | 人工 Import / 旧 token 建草稿 | 母稿发出 1–7 天后，人用 Stories → Import a story 导入（自动加 canonical）；核对 canonical；投稿给目标出版物（编辑可通过 EPP 认领）；发布时勾选通知订阅者；有旧 token 的可用 API 以 `publishStatus: draft` 加 `canonicalUrl` 建草稿 | 无头浏览器自动发布；AI 生成的文字；非英文稿期待 General 分发 |

发布模块每次执行前都读一遍 `platforms/*.yaml`，检查政策版本。如果某条规则的 `verified_at` 超过 90 天，就提醒作者重新核对。本轮核实的经验是，Medium 在 13 个月里改了至少八次规则，X 在 2026 年至少改了五次 API 规则（2 月两次、4 月、6 月、10 月），90 天是上限，不是下限。

### S8 复盘学习（闸口 H7）

S8 的数据来源按平台分开。**X**：用 Owned Reads（$0.001/条，24 小时内同一资源去重）每天拉一次本账号近 7 天的帖子和 mentions【原文已核】。**Substack**：每周人工导出 CSV；如果作者是 bestseller，可以通过官方只读 MCP 让 Agent 直接取统计【原文已核】。**Medium**：没有统计 API，每周人工记录；RSS 只用来确认文章已发布。每月生成一份复盘：表现前 20% 变体的共同特征（按平台分别统计）、`edit_diffs` 里反复出现的修改、R1 候选、R2 候选，以及排序权重和平台规则的修改提议。全部由人批准（H7）后才写回知识库。

---
## 各平台的质量闸口清单

所有变体都要先过**通用底线 G0**：无 TK；没有任何编造的事实、经历或数字；引语逐字可查且归属正确；不含他人的原句（Koe 的界线是借想法、不借措辞）；AI 参与程度已记录在案；发布账号就是作者本人；不含自动互动动作。在此之上，每个平台再加自己的检查项。

**G-SS · Substack 长文**

| 检查项 | 标准 | 依据 |
|---|---|---|
| 页顶答案 | 开头 3 段内出现一句话答案或明确的承诺 | Perell；Lenny“Get to the point” |
| 引言 | 引言不超过全文 15%；对照“删掉首段”版本，删了不影响理解就删 | Lenny【原文已核】 |
| 免费/付费分层 | 免费部分本身完整；付费墙落在自然停顿处；或明确选用 freewall / metered paywall | Substack 2026-10 功能【原文已核】 |
| 第二篇 | 文中至少链接 1 篇最相关的旧文 | Thompson“第二篇文章”【待核实】 |
| 画面 | 至少一张核心图表或一个核心数字，可拿去做推广 | Packy【转录·已核】 |
| 标题测试 | 2–3 个变体；看打开者点击率，不只看打开率 | Substack A/B |
| 结尾 | 不是总结段；由作者拍板 | Housel“boom”【转录·已核】；PG |
| 披露 | 用 post template 固定一行 AI 使用说明；作者决定是否发布“How I make this”声明、是否关闭本篇扫描 | Substack AI 透明度工具【原文已核】 |

**G-SN · Substack Notes**

| 检查项 | 标准 |
|---|---|
| 自足 | 不点开原文也能拿到一个完整的想法 |
| 目标 | 单条以拉免费订阅为目标（0.70% 研究）；整体经营 Notes 信息流，因为 App 付费订阅一半以上来自这里 |
| 密度 | 每周 3–10 条，同一天内不连发 |
| 时段 | 不必纠结时段（最好与最差时段只差约 3 个百分点）；避开美东晚 8–10 点即可 |
| 互动 | 作者本人在 Notes 里回复和评论（具体时长的说法未核实） |

**G-XP · X 单帖**

| 检查项 | 标准 | 依据 |
|---|---|---|
| 一个想法 | 只有一个可以复述的想法 | Rule of One |
| 句子三问 | 至少 2 项为是 | Dry【转录·已核】 |
| 首行 | 第一行就给出具体内容：数字、画面或反常识 | Hormozi |
| 回复设计 | 有一个读者能接话的点；作者本人负责发布后的回复 | 回复权重 5.0；API 不能主动回复 |
| 负反馈风险 | 不蹭无关热点，不 @ 线程外的人，不重复发同样的内容 | 举报 −234，静音 −58.8；API 只能 @ 线程内参与者 |
| 链接 | 根帖默认不放链接；放与不放作为 A/B 记录；含 URL 的 API 帖按 $0.20 计 | `open_link` 0.2；官方价目表【原文已核】 |
| 原创 | 不是他人作品的整体照搬、轻改、汇编或跨平台搬运 | Original Content Rewards 排除项【原文已核】 |
| 变现话题 | 不发“教人赚分成”类内容（不计酬） | 同上 |
| 可被 Community Note 的断言 | 所有事实性断言都有来源；被加 helpful Community Note 的帖子不计酬 | 同上 |
| 间隔 | 和本账号上一条帖子至少隔 2–3 小时 | 作者多样性衰减【设计建议】 |
| cashtag | 最多 1 个 | 自助档 API 限制【原文已核】 |

**G-XT · X Thread**

| 检查项 | 标准 |
|---|---|
| 首帖独立 | 只看首帖也有价值，并能引发回复（同一会话会合并显示，首帖承载分发） |
| 每帖一个要点 | 每条都能单独截图转发 |
| 末帖 | 回扣首帖的钩子，加 CTA；链接放在末帖 |
| 发布通道 | 已确认所选通道（API 自回复 / Typefully / 人工）可行 |
| 长度 | 不设硬性条数；“7–12 条”只是第三方说法【待核实】 |
| 在场 | 发布后 1–2 小时内作者本人在线回复（冷启动窗口 2 小时） |

**G-XA · X Articles**

| 检查项 | 标准 |
|---|---|
| 开头 | 按 Proof → Promise → Plan 重写，不假设读者认识作者 |
| 格式 | DraftJS `content_state` 转换后由人在客户端预览一次 |
| 推广帖 | 配一条能独立成立的推广单帖，不只贴文章卡片 |
| 原创 | 是作者自己的母稿，不是汇编 |
| 账号 | 作者有有效的 Premium 订阅 |

**G-MD · Medium 文章**

| 检查项 | 标准 | 依据 |
|---|---|---|
| 语言 | 英文；中文稿不发，或明确只当存档 | 非英文不进 General、不进 Boost【原文已核】 |
| 人写 | `draft_mode` 必须是 A 或 I；B 模式稿不发 Medium | AI 生成内容不进 General、不进付费墙【原文已核】 |
| 披露 | 含 AI 辅助生成的文字或图片时，前两段内有一句披露；只用于提纲、语法、事实核查的不必披露 | AI 政策【原文已核】 |
| 翻译 | 不是从其他来源转载的翻译稿（这类稿不能 Boost）；作者自译自己的稿件是否受限未明，按低预期处理 | Distribution Guidelines【原文已核】 |
| 包装语境 | 标题、副标题、封面图合起来能说清“写什么、给谁、承诺什么”；不过分神秘、套路或煽情 | 官方 Boost 要求【原文已核】 |
| 亲身经验 | 有基于作者亲身经验的部分（官方认为比头衔更重要） | 同上 |
| 非衍生 | 不只是转述、重组网上容易找到的信息 | 同上 |
| 主要目的 | 不以收集订阅、导流或卖东西为主要目的；CTA 是次要的 | General 失格项【原文已核】 |
| 元内容 | 不写关于 Medium、MPP、Boost 本身的文章（默认只给关注者分发，且不能进付费墙） | 付费墙政策【原文已核】 |
| 工艺 | 没有错别字，来源恰当，图片有 ALT 和署名；AI 封面要标注，没有好图宁可不用 | 同上 |
| canonical | Import 之后核对 canonical 指向母稿 URL | Help: canonical【原文已核】 |
| 出版物 | 已选好 2–3 个开放投稿的高质量出版物 | 官方：“your best bet remains submitting your story to a high quality publication” |
| 标签 | 不滥用标签；“最多 5 个”“策展人看不到标签”都未核实 | 现行指南只禁止 topic spamming【待核实】 |

---

## 跨平台内容流：母站、canonical、链接和 UTM

**拓扑：Substack（或自有域名）当母站，其余平台当辐条。** 理由有三：Substack 不能把 canonical 指向别处，所以它只能当原文；邮件列表是作者唯一真正拥有的受众资产；Medium 的 Import 工具会自动把 canonical 指回原文。有自有域名的作者，优先用自有域名的 URL 当 canonical，并把 X 上的链接也换成自有域名。2023 年 4 月，X 曾在 Substack 发布 Notes 后几天开始限流带 substack.com 链接的推文，随后恢复【原文已核】([Engadget](https://www.engadget.com/twitter-stops-throttling-tweets-with-substack-links-171858782.html))；上一版说“自定义域名不受影响”，原文里没有这句，已删除。把链接域名握在自己手里，理由仍然成立，但这是设计判断，不是已证实的规避效果【设计建议】。对中文作者，母稿用中文写在 Substack，Medium 只承接其中精选的英文人写重写版，canonical 是否该指向中文原文，取决于两版是不是同一篇文章；英文版内容差异大时，可以当作独立文章发布，不设 canonical【设计建议】。

**一周的标准节奏（周更型，`rhythm: systems`）：**

| 时间 | 动作 | 渠道 |
|---|---|---|
| 每天早上 | 90 分钟写作块：前 30 分钟写短帖，后 60 分钟写母稿（Koe 的分工【原文已核】） | — |
| D-7 至 D-1 | X 单帖试水本周母题的 2–3 个分论点；记录各自的回复率 | X（短养长） |
| D0 上午 | 母稿发送（邮件 + 网页） | Substack |
| D0 当天 | 第一条 Note（核心金句或图表）；第一条 X 单帖（最强的想法，不带链接）；作者在线 1–2 小时，亲手回复 | Notes、X |
| D1–D6 | 每天 1–2 条 X 单帖和 1 条 Note，从母稿里挖；视情况发 1 条 Thread 或 X Article（API 建草稿，人发布） | X、Notes |
| D1–D7 | 若有英文人写版：Import 到 Medium，核对 canonical，投稿出版物，勾选通知订阅者 | Medium |
| D7 | 采集 7 日指标；S8 打标签 | 全部 |
| D+90 起 | 常青内容进入 R2 回收池，用新角度重写后再发 | X、Notes |

执念型作者（`rhythm: obsession`）的流向反过来：当天在 X 上写下刚击中自己的想法；Agent 在后台把它记进选题池；当周表现最好的那条，晋升为周末长文的选题（R1）。Newton 2026 年的改版说明了这种节奏也能用于付费刊物：“we're promising to show up when we find out something interesting”【原文已核】。

**X 链接处理的决策树。** 第一步，根帖默认不带链接，内容要完整到不点链接也能获得价值；链接放在末帖或个人主页。原因有二：`open_link` 权重只有 0.2，用户离站还会损失停留【原文已读】；API 发含 URL 的帖子每条 $0.20，普通帖 $0.015【原文已核】。第二步，Musk 2026 年 7 月说已经“一年多”不惩罚链接【原文已核】，但 Buffer 的数据显示 2025 年普通账号链接帖的互动率中位数为零，所以每月拿 10% 的帖子做“正文带链接”和“不带链接”的对照，按 UTM 点击和曝光判断，不靠传言。第三步，“链接放自回复”这一招在 API 下有两个未知：自回复能不能通过 API 发（2026-02-23 的回复限制），以及自回复里的 URL 是按 $0.20 还是按“summoned reply”的 $0.01 计；P2 用测试账号实测之前，成本模型按 $0.20 估算，发布通道按“人工自回复”设计【待核实】。第四步，不设置任何“互动过阈值就自动插入推广回复”的自动化。上一版引用 Hypefury 的 Auto-plug 作参考，但 Hypefury 现已不支持 X，它 2026 年 11 月的自述只列 Instagram、Facebook、Threads、LinkedIn、TikTok 和 Bluesky【原文已核】([Hypefury](https://hypefury.com/llm-info))；Typefully 首页仍列有“Auto-Plug & Auto-RT”【原文已核】([typefully.com](https://typefully.com))，但在 API 只能回复召唤者的规则下，这类功能能否继续工作未核实【待核实】。

**Canonical 规则。**

| 情形 | 做法 |
|---|---|
| Substack → Medium（英文版） | 母稿发布后 1–7 天，人工用 Stories → Import a story 导入（回溯日期并自动设 canonical）；导入后在 More settings → Advanced Settings 里核对“This story was originally published elsewhere” |
| 手动粘贴到 Medium | 在同一路径手动设置 canonical；只有作者本人能设置 |
| 旧 token 走 API | 发帖时带 `canonicalUrl`，并设 `publishStatus: draft`【原文已读】 |
| X Articles | 没有 canonical 机制；可以发全文（Koe 的做法），也可以发精简版并链回母稿；搜索引擎层面的影响**未找到证据** |
| Import 失败 | 降级为手动粘贴加手动设 canonical；记录失败原因 |

**UTM 规范。** Substack 的“订阅来源”报表能否直接显示 UTM 值，研究团队仍未确认【未找到证据】，所以 UTM 主要用于点击归因，最好配合自有域名上的 GA4。X 和 LinkedIn 的应用内浏览器可能丢掉 referrer，这时只能靠 UTM【待核实】([Narrareach](https://www.narrareach.com/blog/substack-traffic-sources-explained))。Medium 的 Friend Link 带来的会员阅读照样计入收入【原文已核】，所以在 newsletter 或 X 里推广 Medium 文章时，可以放带 UTM 的 Friend Link，非会员也能读全文。

```text
utm_source   = x | substack_notes | medium | linkedin | threads
utm_medium   = post | thread_end | self_reply | article_footer | story_cta | profile | friend_link
utm_campaign = <hub_slug>              # 例：2026w45-user-interviews
utm_content  = <variant_id>            # 例：v_x_post_03
示例：https://letters.example.com/p/user-interviews?utm_source=x&utm_medium=thread_end&utm_campaign=2026w45-user-interviews&utm_content=v_x_thread_01
```

---

## 知识库与记忆：一个 markdown 仓库，外加平台规则配置

在 newsletter 这个规模，几百篇往期文章完全可以让 Agent 用 grep 或 glob 按需检索，暂时用不着向量数据库。这符合 Anthropic“按需检索、以文件路径保存引用”的建议【原文已读】([context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents))，但没有实测【设计建议】。

```
creator-vault/
├── voice/
│   ├── profile.yaml            # 声音档案（结构化，含各平台、各语言差异）
│   ├── exemplars/              # 5–15 段范文，按开头/转折/论证/吐槽/结尾分类，按平台和语言分文件夹
│   ├── never.md                # 禁用词与禁用结构（含中文 AI 腔词表，需自建）
│   ├── deliberate_breaks.md    # 作者有意的破格，lint 时跳过
│   ├── stances.md              # 已表态的立场
│   ├── stories.md              # 作者亲口确认过的经历库，每条带日期和可公开程度
│   ├── glossary_zh_en.md       # 中英术语表（英文重写版用，Agent 只做术语一致性检查）
│   └── edit_diffs/             # AI 稿 → 终稿的修改对
├── backlog/ideas.jsonl         # 选题池（含 edge、兴奋度、市场信号）
├── swipe/                      # 他人佳作：只存结构、钩子类型、指标与链接，不存可复用原句
├── sources/                    # 每个来源一个 md：逐字摘录、read_level、access_path、证据等级、归属
├── hubs/{hub_id}/              # 每篇母稿：brief / outline / draft / eval / final
├── variants/{variant_id}.yaml  # 各平台变体及其发布结果、指标
├── platforms/                  # substack.yaml / x.yaml / medium.yaml：平台规则与政策版本
├── metrics/exports/            # Substack CSV 或 MCP 拉取、Medium 手工记录、X Owned Reads
└── runs/logs/                  # 每次运行的提示词、模型、成本
```

`stories.md` 是关键文件。Hormozi、Denning 和 Medium 的政策都指向同一个结论：**亲身证据只能来自人**。Medium 现行 Boost 标准把“credible, first-hand experience”放在头衔之前【原文已核】，这让 `stories.md` 在 Medium 上直接变成分发资产。Agent 引用作者的经历时只能从这个文件里取，每条都要标 `consent`，也就是可以公开到什么程度。`sources/` 里新增的 `attribution` 字段，用来记录这句话是本人原话、转述他人，还是主持人复述，这是本轮核实里最常见的错误（Housel 的 100 美元规则、Gioia 的三问）。

## 数据结构

```yaml
# voice/profile.yaml
author: "示例作者"
identity: "前产品经理，写给 0→1 阶段的产品负责人"
lens: "每个话题都回到：这对一个 5 人团队本周的决策意味着什么"
persona_ref: personas/jennifer.yaml          # Günel 式读者画像
rhythm: systems                              # systems | obsession
default_draft_mode: A                        # A | B | I
languages:
  hub: zh                                    # 母稿语言
  medium: en_rewrite_only                    # none | en_rewrite_only
daily_block: {total_min: 90, short_form_min: 30, longform_min: 60}   # Koe 的分工
core:
  person: first_person_singular
  sentence_length: {median_words: 14, p90_words: 30}
  paragraph_max_sentences: 4
  signature_moves: ["开头用一个读者原话提问", "每节结尾给一个可执行的小动作"]
  closings: "以一个反问或下周预告结束，不做总结段"
  banned_endings: ["总之", "In summary", "综上所述"]
platform_deltas:                             # “像学一门语言”：各平台差异
  x:        {max_chars: 280, line_breaks: frequent, hashtags: none, tone: "更锋利，一帖一事"}
  notes:    {max_sentences: 5, tone: "像在朋友圈说一句真心话"}
  medium:   {language: en, subtitle_required: true, tone: "更完整的语境，假设读者不认识我"}
disclosure_line: "研究与校对由 AI 辅助；观点、经历与文字出自我本人。"
medium_disclosure_line: "This story was written with the assistance of an AI writing program."   # 仅在含 AI 辅助生成的文字或图片时，放入前两段
```

```json
// backlog/ideas.jsonl —— 每行一条
{"id":"idea_0142","created":"2026-10-28","origin":"reader_reply|x_outlier|own_post|memo",
 "raw":"读者原话：小团队要不要做用户访谈？",
 "edge":"大家默认访谈要按项目做；我怀疑固定节奏才是关键",
 "angle_type":"actionable","lens_fit":3,"excitement":null,
 "market_signals":{"reader_questions":4,"votes":0,"own_x_post":{"id":"18…","reply_rate":0.021},
                   "outlier_refs":["swipe_0311"]},
 "human_evidence":["stories#s_017","可约 2 位创始人访谈"],
 "status":"candidate","related_hubs":["hub_0031"]}
```

```json
// sources/src_0871.json —— 来源卡片（本版新增 access_path 与 attribution）
{"id":"src_0871","url":"https://howiwrite.substack.com/p/morgan-housel-how-to-master-writing",
 "access_path":"substack_api_json","read_level":"transcript","date":"2025-10-15",
 "quote_verbatim":"…know your reader becomes pander to your reader…",
 "speaker":"Morgan Housel","attribution":"own_words",   // own_words | relayed_from_unknown | host_paraphrase
 "evidence_label":"转录·已核"}
```

```json
// hubs/hub_0045/meta.json —— 母稿
{"id":"hub_0045","slug":"2026w45-user-interviews","language":"zh",
 "canonical_url":"https://letters.example.com/p/user-interviews",
 "top_of_page":{"context":"…","questions":["…"],"answer":"小团队的用户访谈应该按周固定，而不是按项目"},
 "one_big_idea":"固定节奏胜过按需访谈","draft_mode":"A","word_count":2300,
 "sources":["src_0871","src_0874"],"stories_used":["s_017"],
 "gates":{"H4":{"approved_by":"author","at":"2026-11-02T07:50","quotes_checked":6,"numbers_checked":4}},
 "eligible_platforms":["substack_post","substack_note","x_post","x_thread","x_article"],
 "status":"final"}
```

**平台变体 schema**（核心结构）：

```yaml
# variants/v_x_post_03.yaml
variant_id: v_x_post_03
hub_id: hub_0045
platform: x                      # substack | substack_notes | x | medium
format: x_post                   # substack_post | substack_note | x_post | x_thread | x_article | medium_story
language: zh
derivation: atomize              # atomize(长拆短) | promote(短养长) | recycle(回收) | native(原生) | rewrite_en(英文人写重写)
parent_variant: null
status: approved                 # draft | gated | approved | scheduled | published | failed | retired
body:
  text: "我访谈了 40 个小团队。按项目做访谈的，三个月后几乎都停了。…你们团队是按周还是按项目？"
  parts: []                      # thread 分段
  content_state: null            # x_article：DraftJS 结构
  char_count: 212
  media: [{type: image, path: "assets/chart_0045.png", alt: "按周 vs 按项目的访谈坚持率"}]
packaging:
  title: null
  subtitle: null
  title_variants: []
  target_publications: []        # medium 专用
link_policy:
  placement: none                # none | inline | thread_end | self_reply | footer | profile | friend_link
  url: "https://letters.example.com/p/user-interviews"
  utm: {source: x, medium: post, campaign: 2026w45-user-interviews, content: v_x_post_03}
canonical:
  url: "https://letters.example.com/p/user-interviews"
  method: n/a                    # medium_import | api_canonicalUrl | manual_setting | n/a
compliance:
  ai_assist_level: edit_only     # none | edit_only | outline | assisted_text | draft_B
  disclosure_required: false     # medium：assisted_text 时为 true，且须在前两段
  paywall: false                 # medium：draft_B 不得发布；assisted_text 可设，但须披露
  originality_check: pass        # 非他人作品照搬、轻改、汇编、搬运
  monetization_meta: false       # x：教人变现的内容不计酬；medium：关于平台本身的内容不进付费墙
  automated_interaction: none    # 永远是 none：回复、点赞、关注、引用只由人做
schedule:
  planned_at: "2026-11-03T09:20+08:00"
  min_gap_hours_same_account: 3
  author_online_window_min: 90
gate_results:
  gate: G-XP
  checks: {one_idea: pass, dry_tests: "2/3", first_line_concrete: pass, reply_hook: pass,
           negative_risk: low, link_root: none, cashtags: 0}
  judge_score: 0.78
  judge_anchors: ["hub_0012(bad)","hub_0031(good)"]
  human_approved_by: author
  approved_at: "2026-11-02T21:10+08:00"
publish_result:
  channel: x_api_pay_per_use     # x_api | x_api_article_draft | typefully | substack_manual | medium_import | medium_api_draft
  platform_post_id: "1985…"
  url: "https://x.com/…/status/1985…"
  cost_usd: 0.015
  published_at: "2026-11-03T09:21+08:00"
metrics_ref: metrics/v_x_post_03.jsonl
```

```yaml
# platforms/medium.yaml —— 本版按 2026-11-03 核实结果重写
platform: medium
policy_version: "2026-11"
verified_at: "2026-11-03"
verification_level: full_text    # 来源：Zendesk API 全文 + 博客 RSS 全文
sources:
  distribution_guidelines: {edited_at: "2026-06-29"}
  ai_policy: {edited_at: "2026-04-29"}
  earnings_calculation: {edited_at: "2026-03-18"}
  mpp_eligibility: {edited_at: "2026-09-24"}
rules:
  distribution_tiers: [network, general, boost]          # 现行名称 Network Distribution
  non_english_general_distribution: false
  non_english_boost: false
  ai_generated_paywall_allowed: false                    # 无论是否披露
  ai_generated_distribution: network                     # 即使披露也不进 General
  ai_undisclosed_distribution: network
  ai_assisted_text_requires_disclosure: true             # 前两段内一句
  ai_disclosure_exempt: [outlining, grammar, spelling, fact_check]
  boost_requires_human_created: true
  boost_nomination_program: closed_2026-05-31            # 已删除自荐配额与 180 天上限
  republished_translation_from_other_sources_boost: false
  meta_about_medium_paywall: false                       # 且默认 network
  general_disqualifiers: [ai_generated, sponsored, content_marketing, primary_purpose_signups,
                          summaries_link_roundups, tag_spam, mass_mentions, about_mpp_or_boost]
  read_counts_after_seconds: 30
  idle_time_counted: false
  non_member_reads_paid: false
  friend_link_member_reads_count: true
  max_full_listens_per_member: 2
  payout_extra:
    external_traffic_pct: 5
    search_traffic: additional_share                     # 2025-11 博文为 15%，现行帮助页未给数字
    email_notification: higher_rate                      # 2025-12-01 起
    new_member_conversion: one_time_small                # 2026-02-17 起，快速取消不计
    read_ratio_adjustment: true
    boosted_rate: higher_but_reduced                     # 2026-01 起
  editor_partner_program: {editor_share_pct: 25, writer_share_unchanged: true}
  max_tags: unverified
mpp_eligibility:
  instant_enrollment: true                               # 2026-08-26 起
  requires: [active_membership, one_story, complete_profile, eligible_bank_country, age_18]
  eligible_country_examples: [HK, MO, TW]
  mainland_china_eligible: false
api:
  supported: false
  new_tokens: false                                      # 官方帮助页 2024-12-17
  existing_tokens_work: true
  legacy_endpoint: "POST /v1/users/{authorId}/posts"
  fields: [title, contentFormat, content, canonicalUrl, tags, publishStatus]
publish_default: human_import
canonical_setting_path: "More settings > Advanced Settings > This story was originally published elsewhere"
```

```yaml
# platforms/x.yaml —— 本版新增
platform: x
policy_version: "2026-11"
verified_at: "2026-11-03"
verification_level: full_text    # docs.x.com 与 devcommunity；OCR 规则为三家二手报道，help.x.com 未读
api:
  billing: pay_per_use           # 2026-02-06 上线；Basic/Pro 订阅仍保留
  price_usd:
    post_create: 0.015
    post_create_with_url: 0.20
    post_create_summoned_reply: 0.01
    posts_read: 0.005
    user_read: 0.010
    owned_reads: 0.001           # 24 小时 UTC 窗口内去重
    article: unlisted
  monthly_post_read_cap: 3000000
  free_credits: {first_card_usd: 20, first_autorecharge_match_max_usd: 50, expires_months: 3}
  rate_limit_post: {per_15min: 200, per_3h: 300}
  self_serve_restrictions:
    reply_only_if_summoned: true            # 2026-02-23 起
    mention_quote_only_thread_participants: true
    like_write: removed                     # 2026-04-20 起
    follow_write: removed
    quote_post: enterprise_only
    max_cashtags_per_post: 1
  self_reply_thread_via_api: unverified     # P2 实测
  articles: {draft: "POST /2/articles/draft", publish: "POST /2/articles/{id}/publish", since: "2026-06-11"}
automation:
  ai_replies: prior_approval_required
  non_api_automation: permanent_suspension
  automated_account_requirements: [automated_label, bio_disclosure, linked_human_account,
                                   honor_opt_out, official_api_only, rate_limits]
monetization:
  program: original_content_rewards        # 2026-09-08 起
  thresholds: {premium: true, verified_followers: 500, verified_home_impressions_90d: 500000, replies_excluded: true}
  excluded: [copied, lightly_altered, compilations, cross_platform_lifts, helpful_community_note, monetization_coaching]
  payout: {cadence: fortnightly, minimum_usd: 30}
ai_disclosure:
  mandatory: "monetized creators, AI videos of armed conflict (2026-03-03)"
  optional_label_any_post: testing
links:
  explicit_penalty: "officially denied (Musk 2026-07-29)"
  open_link_weight_default: 0.2
```

```json
// metrics/v_x_post_03.jsonl —— 指标快照（每行一个时间点）
{"variant_id":"v_x_post_03","t":"+2h","impressions":1840,"replies":22,"reposts":6,"quotes":3,
 "likes":61,"bookmarks":14,"profile_visits":38,"follows":5,"link_clicks_utm":0,"source":"x_owned_reads"}
```

```json
// hubs/hub_0045/eval.json —— 评审结果
{"pass":false,"scores":{"stranger":0.7,"usefulness":0.8,"honesty_3q":1,"dry_core":0.67,"cribs_cb_ratio":0.18,
 "intro_ratio":0.19,"support_rate":0.92,"attribution_ok":0.83,"originality":1,"voice_drift_sigma":1.1,"ai_tells_per_1k":2.4},
 "blocking":[{"check":"support_rate","sentence":"……坚持率高 3 倍","fix":"补一手来源或删除"},
             {"check":"attribution","sentence":"Housel 说每个词值 100 美元","fix":"改为 Housel 转述的规则"},
             {"check":"cribs","para":7,"label":"Boring","note":"与第 4 段重复"}],
 "briars":[{"sentence":"……","reason":"含糊","hits":3}],
 "anchored_to":["hub_0012(bad)","hub_0031(good)"]}
```

---
## 平台工具现实：哪些能自动化，哪些必须由人点

**Substack：只能读，不能写；bestseller 多了一条官方读取通道。** 官方没有发文、草稿或订阅者 API。官方 Developer API 只返回创作者公开资料，凭 LinkedIn 账号查询，需要人工审批，适用 2026 年 1 月 8 日更新的条款，且“Substack may revoke this license at any time”【原文已核】([Substack API ToS](https://substack.com/api-tos))。bestseller 可以用 2026 年 7 月 6 日上线的官方 MCP 读取统计，只读【原文已核】([On Substack](https://on.substack.com/p/new-on-substack-subscriber-perks))。上一版说“只有单一来源称存在 bestseller 只读 MCP，与 CEO 说法矛盾”，现已更正。可行的通道是：RSS 读取往期和同行，CSV 或 MCP 拿指标，人工粘贴发长文，原生定时或 Typefully 发 Notes（Typefully API 的 `substack` 平台返回 `substack_published_url`，形如 `https://substack.com/@username/note/c-…`【原文已核】([Typefully API](https://typefully.com/docs/api.md))）。非官方的 cookie 型 API 和 MCP server（例如 `codalanguez/substack-mcp`，自带约每秒 1 次的限流，并警告发布“公开且不可撤销”）只能在作者明确开启后使用，而且只建草稿【待核实】([substack-mcp](https://github.com/codalanguez/substack-mcp))。据第三方条款追踪站，Substack 条款禁止抓取和爬取【待核实】([ConductAtlas](https://conductatlas.com/platform/substack/substack-terms-of-use/provision/CA-P-029302/prohibition-on-scraping-or-crawling-substack/))；条款是否明确禁止用 cookie 自动发文，仍**未找到证据**。

**X：发原创便宜，读自己更便宜，互动只能人做。** 按官方价目重算的成本模型如下【原文已核】([pricing](https://docs.x.com/x-api/getting-started/pricing))：

| 场景 | 月用量 | 估算成本 |
|---|---|---|
| 每天 3 条普通帖 | 约 90 条 × $0.015 | 约 $1.35 |
| 同样数量，全部在正文带链接 | 约 90 条 × $0.20 | 约 $18 |
| 每天读取 1,000 条自有帖子的指标（Owned Reads） | 约 30,000 次 × $0.001 | 约 $30（同一天重复读同一条不重复计费） |
| 只读最近 7 天的自有帖子，每天 1 次（约 20 条） | 约 600 次 × $0.001 | 约 $0.6 |
| 每月 4 篇 X Articles | 价格未单列 | 先小量试，按账单回填 |
| 首次绑卡与首次自动充值赠额 | 最多 $70，3 个月过期 | 足够覆盖 P1–P2 阶段的全部测试 |

上一版按 $0.005 估算读取成本，高估了约 5 倍。现在的结论反过来了：**写入和读取都便宜，真正的约束是规则，不是钱**。合规方面有六条。一，只用作者本人的 OAuth 用户 token，以作者身份发布经人批准的原创内容，这是普通的排期用法，不受自动化账号的六条要求约束。二，自助档 API 已经不能主动回复、点赞、关注和引用，**任何互动都由作者在客户端亲手做**；Agent 能做的是整理“值得回复的评论”清单。三，AI 生成并自动发布回复的应用必须事先获得 X 批准，即使获批也不能冒充人类【原文已核】([Developer Guidelines](https://docs.x.com/developer-guidelines))。四，抓取和浏览器自动化的后果是**永久封号**，不是一般的违反条款【原文已核】(同上)。五，存储 X 数据用于训练 AI 模型被禁止（Grok 除外），所以 swipe 库里存的应该是结构笔记和链接，不是批量抓下来的帖子全文【原文已核】(同上)。六，第三方低价数据转售商不是官方渠道，处于灰色地带【待核实】([twitterapi.io](https://twitterapi.io/blog/x-api-cost-breakdown-2026))。排序权重的四个使用前提不变：它们是默认值，乘的是预测概率，作者多样性衰减和站外乘数的生产值未公开，Phoenix 权重不在仓库里【原文已读】([x-algorithm](https://github.com/xai-org/x-algorithm))。**能从代码推出的是机制，推不出的是量级。**

**Medium：API 停了，Import 加出版物投稿是主路径。** 官方 API 文档原话：“The Medium API is no longer supported… We don't allow any new integrations with our API.”自发 token 不会过期，除非被撤销；在出版物里，writer 只能建草稿，等 editor 批准；文档没写速率限制【原文已读】([medium-api-docs](https://github.com/Medium/medium-api-docs))。官方帮助页确认不发新 token、旧 token 继续可用【原文已核】([Help: API/Importing](https://help.medium.com/hc/en-us/articles/213480228))。Make 的 Medium 应用下线、Write.as 的集成被切断，本轮未重核【待核实】([apps.make.com](https://apps.make.com/medium))。RSS（`medium.com/feed/@username`）只能读，而且只返回最近 10 篇。没有统计 API。“无 API 发布”的浏览器自动化仓库存在条款风险，不建议用【待核实】。Boost 提名关闭后，作者能主动做的只有两件事：把英文人写稿投给高质量出版物，和让编辑通过 EPP 有动力认领它【原文已核】。

| 能力 | Substack | X | Medium |
|---|---|---|---|
| 读取自己的内容 | RSS ✅ | Owned Reads $0.001 ✅ | RSS ✅（最近 10 篇） |
| 读取指标 | CSV 导出（人工）；bestseller 可用官方 MCP ✅ | Owned Reads ✅ | 人工记录 |
| 写长文 | ❌ 人工粘贴 | Articles：API 建草稿 ✅，人发布 | 旧 token 建草稿，或人工 Import |
| 写短内容 | Notes：原生定时 / Typefully ✅ | 原创帖 API ✅；线程待实测 | — |
| 互动 | 人工 | **API 不能主动回复、点赞、关注、引用**；人工 | 人工 |
| canonical | 不能指向外部 | 无 | Import 自动设置 / 手动 / API `canonicalUrl` |
| 语言限制 | 无 | 无 | 非英文不进 General、不进 Boost |
| 自动化红线 | cookie API 存在条款风险 | 非 API 自动化永久封号；AI 回复须事先批准 | 无头浏览器；AI 生成文字进付费墙 |

---

## 指标与评估：每个平台各看各的口径

| 平台 | 质量信号（最便宜） | 读者信号 | 商业信号 | 不要优化的虚荣指标 |
|---|---|---|---|---|
| Substack 长文 | 人工编辑时长；AI 稿到终稿的编辑距离 | 打开者点击率、评论、restack | 按来源统计的新增免费和付费订阅、退订；转化按 2–3% 设基准 | 单看打开率 |
| Substack Notes | — | 点赞、restack、回复 | 由 Notes 带来的免费订阅数；Notes 信息流贡献的付费订阅 | 点赞数本身 |
| X 单帖 / Thread | 三问分和实际表现的相关性 | 回复/曝光、引用、收藏、主页访问、新增关注、发布后 2 小时的增长 | UTM 点击、对应时段的订阅增量；90 天认证首页曝光累计（OCR 门槛 50 万） | 点赞（权重 0.66）、总曝光 |
| X Articles | — | 停留（代理指标）、引用、分享 | UTM 点击 | — |
| Medium | 分发档位（Network / General / Boost）；是否被出版物收录 | 会员阅读、**阅读率**、高亮、回复 | MPP 收入、站外/搜索/邮件流量占比、新会员转化；newsletter CTA 的 UTM 点击 | 鼓掌数 |

X 的负反馈（静音、屏蔽、举报）作者看不到，能代理它的只有取关数和曝光的突然下滑；被加上 helpful Community Note 的帖子还会失去计酬资格。**一旦出现负反馈信号，立即降低发帖频率**【设计建议】。Medium 的阅读率调整意味着标题党会被直接扣钱，所以 Medium 的标题评分要同时预测“点开率”和“读完率”，不能只优化前者【设计建议】。

**离线评估从约 20 条用例起步。** Anthropic 用约 20 条代表性查询就看到了明显效果【原文已读】([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system))。做法是从往期作品里选 20 份，10 份作者满意、10 份不满意，覆盖长文、单帖和（如有）英文 Medium 稿；倒推出它们的选题、简报和提纲作为测试输入。每次改提示词都重跑 S3–S6，比较评审分数和作者盲评。系统提示词从最简版本开始，出现失败再加指令【原文已读】([context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents))。**评审本身也要评估**：评审给差稿的分数必须显著低于好稿，否则就是 Packy 遇到的“A 和 A+”问题。

**反馈闭环。** 每月复盘输出三类修改提议：声音档案与范文、选题排序权重、平台规则与变体模板。R1（短养长）：回复率高于账号 30 日中位数 2 倍的短帖，自动进入选题池，标为 `origin: own_post`，对应 Koe 说的“从自己的爆款迭代”。R2（常青回收）：发布 90 天以上、表现前 20% 的变体，**用新角度重写**后再进入发布队列，不原样重发，因为 Original Content Rewards 排除轻改和重复内容【原文已核】。研究团队**没有找到**任何创作者把数据接回提示词调优的公开案例【未找到证据】，这个闭环需要作者自己做小样本实验。还要防古德哈特定律：Perell 说“能火的东西就是更好”，Medium 说别追求爆款，两者的张力只能由作者裁决，**声音档案的修改永远由人一票否决**。

---

## 风险与合规：每类风险配一道闸

| 风险 | 表现 | 对策 | 依据 |
|---|---|---|---|
| 幻觉与编造 | 捏造引语、数字、经历 | 没有来源就不写；经历只能从 `stories.md` 取；H4 人工逐条核对；snippet 和 AI 蒸馏来源不能单独支撑 | Medium 明文禁止“AI-hallucinated stories, statistics, events”【原文已核】；SAFE 72%【待核实】 |
| 归属错误 | 把转述当原话，把主持人的话当嘉宾的话 | `sources/` 记录 `attribution`；H2、H4 检查归属 | 本轮核实发现 Housel、Gioia、Packy 三处【原文已核】 |
| 声音同质化 | 风格方差下降，观点趋同 | 默认模式 A；范文多样并每季度更新；风格漂移硬闸口；swipe 库只存结构 | LLM 改写降低风格方差【待核实】([arXiv 2502.11266](https://arxiv.org/pdf/2502.11266))；高度依赖 AI 草稿的故事更趋同【待核实】([arXiv 2604.03529](https://arxiv.org/html/2604.03529v1)) |
| 评审过分恭维 | LLM 评审给什么稿都打高分 | 好稿差稿锚点；扣分须引原句；“反恭维”提示 | Packy【转录·已核】 |
| 读者信任 | 读者感觉“AI 腔”，或扫描结果与作者声明不符 | 用 post template 固定披露；作者决定是否发“How I make this”；AI 主要用在研究、编辑和改编 | Substack“lack of transparency… definitely is [a problem]”【原文已核】；Reuters 信任数据【待核实】([NewscastStudio](https://www.newscaststudio.com/2025/10/16/public-use-of-generative-ai-grows-but-trust-and-comfort-with-news-applications-remain-low)) |
| Medium 政策 | AI 文字进付费墙被取消 MPP；未披露 AI 辅助被降到关注者分发；中文稿零分发 | `draft_mode`、`language` 与 `medium_story` 硬绑定；B 模式稿不发 Medium；assisted_text 前两段披露 | Medium AI 政策与分发指南【原文已核】 |
| Medium 收款 | 中国大陆银行无法加入 MPP | 无合格地区银行的作者不把 MPP 计入收入规划 | MPP 资格页【原文已核】 |
| X 自动化 | 永久封号；被迫挂 Automated 标签 | 不做任何自动互动；不用浏览器自动化；只用官方 API 发原创 | X Developer Guidelines【原文已核】；2026-10-09 条款修订【待核实】 |
| X 计酬资格 | 帖子被判为搬运、汇编或带 Community Note | 原创性闸口；事实断言都有来源；不写变现教学内容 | Original Content Rewards 排除项【原文已核】 |
| 原创与抄袭 | 照搬异常值的措辞 | swipe 库不存原句；n-gram 重叠闸口；借想法不借措辞 | Koe【转录】；Medium 把 AI 改写他人内容按剽窃处理【原文已核】 |
| 条款与账号 | cookie API、抓取、无头浏览器 | 默认关闭；开启需作者明确选择，并记录日志 | Substack 条款【待核实】；X“permanent suspension”【原文已核】 |
| 规则漂移 | 平台按月改规则，配置过期 | `platforms/*.yaml` 带 `verified_at`；超过 90 天提醒重核；订阅三家官方博客和 changelog 的 RSS | Medium 13 个月内至少八次改动；X 2026 年至少五次 API 规则变化【原文已核】 |
| 访问与支付 | 运行环境无法稳定访问平台；收款渠道不可用 | 发布与数据模块部署在可稳定访问的境外环境；开启付费前确认 Stripe、MPP、OCR 的收款可行性 | 【设计建议】；各地区收款条件【待核实】 |
| 隐私与袒露 | 写出不该公开的经历 | `stories.md` 每条带 `consent`；涉及他人的经历需要匿名化 | Ashley【待核实】 |
| 倦怠 | 量压垮作者 | 节奏上限写进配置；预留 20% 不为数据写的时间 | Rane【待核实】；Koe 说“降低量” |
| 成本 | 多 Agent 研究 | 多 Agent 只用于每周的母稿；X 读取一律走 Owned Reads | Anthropic：约 15 倍 token【原文已读】 |
| 证据偏差 | 把厂商的“算法秘籍”或 AI 蒸馏当事实 | 证据分级：代码 > 官方文档 > 原文 > 厂商数据 > 增长博客 > AI 蒸馏 | 本轮核实【原文已核】 |

---

## 分阶段路线图：从一个脚本到多平台流水线

| 阶段 | 时间 | 范围 | 完成标准 |
|---|---|---|---|
| **P0 建库** | 第 1–2 周 | 用 RSS 导入 Substack 和 Medium 的往期内容；人工挑 10 段范文（区分长文和短帖，区分中英文）；写 `profile.yaml`、`never.md`、`stances.md`、`stories.md`；把现有点子录进 `ideas.jsonl`，每条写上 edge；按本版核实结果建好三份 `platforms/*.yaml`；决定 `languages.medium` | 作者读 `profile.yaml` 时觉得“这就是我”；选题池 30 条以上且都有 edge；`stories.md` 有 20 条以上已确认的经历 |
| **P1 MVP：一个母站加一个辐条** | 第 3–6 周 | 一个脚本串起 S1 → S3 → S5（陌生人评审、Dry 三问、反恭维锚点、lint、TK 拦截）→ S6（只生成 `x_post` 和 `substack_note`）；研究用单 Agent 加搜索；全部人工发布；UTM 生成器 | 连续 4 周按节奏发出；20 条离线测试集建好；评审在测试集上能区分好稿和差稿；每篇都记录人工编辑时长 |
| **P2 平台适配与回流** | 第 7–12 周 | 接入 X API（OAuth、按次付费，用赠额测试）：原创帖发布由人逐批批准，Owned Reads 拉指标；**用测试账号实测 API 自回复和线程**、实测 Articles 草稿与计费；加入 `x_thread`、`x_article` 适配器和 G-* 闸口；若有英文人写版，跑通 Medium 的 Import → canonical 核对 → 投稿出版物 → 通知订阅者；导入 Substack CSV（bestseller 接 MCP）；`edit_diffs` 采集；第一次月度复盘（H7） | 每篇母稿至少产出 3 类平台变体；线程和 Articles 的发布通道有实测结论并写回 `x.yaml`；Medium 的 canonical 核对率 100%；引语、数字与归属的人工核对 100% 覆盖；有一张按渠道统计 UTM 点击和订阅的报表 |
| **P3 研究与循环** | 第 4–6 个月 | S2 升级为编排者-工作者加引用绑定（含 `access_path`、`attribution`）；SAFE 式逐条核查；拔刺采样；访谈模式里的 CRIBS 标注；R1 短养长与 R2 常青回收；风格漂移闸口 | 论据支撑率 ≥95%；人工编辑时长比 P1 下降，读者指标不下降；至少 1 篇长文选题来自 R1 |
| **P4 进阶（按需）** | 6 个月后 | 用 LangGraph 加持久化 checkpointer 实现 H1–H7 的 `interrupt()`；接入排期工具 API（Typefully 的 Notes 与 `x_article`）；访谈模式（语音 → 转写 → 整理）；读者调查设计与分析；（可选、有风险）cookie API 只建草稿 | 作者盲评 AI 参与的稿件不低于纯人写稿件；没有任何一次未经人工按键的发布；没有任何一次自动互动；平台规则 90 天内都核对过 |

每个阶段都遵循同一条规则：**只有在离线测试集上证明有提升，才增加复杂度**。如果 P1 没有证明单 Agent 研究漏掉了关键信息，P3 就不上多 Agent。

---

## 结论

这次核实最大的收获，不是改正了几十处细节，而是看清了一个方向：三个平台都在从“谁发得多”转向“谁是真人、谁有原创”。X 在 2026 年 2 月以“Addressing LLM-Generated Spam”为由拿走了 API 回复权，4 月又拿走了点赞、关注和引用；Medium 把 AI 生成的内容挡在 General Distribution 之外，把“亲身经验”写进 Boost 标准，自称进入了“Curation Era”；Substack 把 AI 扫描交到读者手里，同时把 App 和 Notes 做成付费增长的主入口。对创作 Agent 来说，这意味着上一版里最费心设计的那部分，也就是防止 Agent 自主互动的层层闸口，已经被平台替你做完了；剩下要做好的，恰恰是机器替代不了的那部分：一个真实的视角、一库作者亲口确认的故事、一份能经得起逐字核对的证据链。Newton 的判断可以当作整套系统的分工原则：聚合和可预测性正在被商品化，价值在原创报道和意外。

第二个收获是方法上的。本轮被推翻或修正的论断，大多出在三类来源上：AI 蒸馏的二手材料（Packy 的妻子、A-）、被转述多次的“名言”（Housel 的 100 美元、Gioia 的三问其实是 Perell 归纳的）、厂商博客里的平台规则（“2025-10-14 取消链接惩罚”）。这三类恰好也是一个创作 Agent 最容易大量吸收的材料。所以研究模块的 `attribution` 字段和 `access_path` 字段不是锦上添花，它们是这套系统可信度的底线。对一位在中国大陆用中文写作的作者，现实的组合是 Substack 或自有域名发中文母稿、X 发短帖测题，Medium 只承接少量英文人写重写稿；而且每个平台的规则都应当在 `platforms/*.yaml` 里带着核对日期，过了 90 天就重新核一遍。help.x.com、x.com、perell.com 和 YouTube 上那些仍然打不开的来源，等网络条件允许时，应当按本版“仍无法核实”的清单逐条补核。
