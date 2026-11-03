# 拆解三平台头部创作者，搭一套自己的创作 Agent

Substack、X、Medium 三个平台的头部创作者，在方法上比他们各自的平台更接近。几乎所有人都在跑同一个循环：先要有自己的切入点（Paul Graham 叫它 **edge**），再把写作当作思考本身，然后狠删，最后**一份母稿多处分发**，同时用短内容低成本试水，把试出来的赢家扩写成长文。Dan Koe 每周只写一篇 newsletter，再把它拆成 X Articles、推文、Notes、图片帖、YouTube 和短视频，这是最完整的公开样本【转录】([YouTube](https://www.youtube.com/watch?v=KCjwU4XYBL8))。三个平台的分发机制却差别很大。Substack 靠站内网络，官方数据是 Recommendations 加 App 带来**约 50% 的新订阅和 25% 的新付费订阅**（2024 年口径）【待核实】([On Substack](https://on.substack.com/cp/142007285))。X 的排序代码已开源，默认权重下，回复（5.0）、引用（5.0）、私信分享（5.0）、复制链接分享（**20.0**）远高于点赞（0.66），而举报（**−234**）、屏蔽作者（−58.8）这类负反馈的惩罚极重【原文已读】([xai-org/x-algorithm](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs))。Medium 的 Boost 由人工策展决定，Partner Program 按付费会员的阅读时长付钱，而且 **AI 生成的文字不能放进付费墙**【待核实】([Medium Help](https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy))。三个平台都没有给创作者一条干净的官方发文通道：Substack 没有发文 API，X 改成了按次付费（含链接的帖子据报每条 **$0.20**），Medium 官方 API 已停止支持，也不再发放新 token【原文已读】([Medium API docs](https://github.com/Medium/medium-api-docs))。由此，本手册推荐的架构是：一条与平台无关的核心流水线，产出一份经人批准的母稿；母稿默认发在 Substack 或自有域名上，作为规范来源；之后经过**平台适配层**生成各平台的原生变体，交给各平台的发布模块，**最后一次按键永远由人完成**；所有变体都带 UTM，数据回流到复盘环节。Agent 的定位是研究助理、严苛编辑和改编分发员，不是代笔。PG 的“陌生人重读”和“刺”、Harry Dry 的三问、Perell 的 CRIBS、Gioia 的三个诚实问题，都可以写成评审提示词和闸口。选题的 edge、真实兴趣、亲身证据、声音和结尾的判断，必须留给人。最后要先交代一点：受会话网络限制，绝大多数网页来源只读到了搜索摘要。真正读过全文的，只有下文列出的几个 GitHub 语料库和 Anthropic 的工程文章。

---

## 先交代证据：哪些读过全文，哪些只是摘要

**大多数网站都无法抓取。** 2026-11-03 前后，研究团队所在的会话网络屏蔽了 paulgraham.com、perell.com、substack.com 及其子域、medium.com、help.medium.com、docs.x.com、help.x.com、thedankoe.com、beehiiv.com、threadreaderapp.com、YouTube 等几乎所有一手站点。能直接访问的只有 github.com（通过 `git clone`）和 anthropic.com。所以下文的大部分创作者引语和平台规则，来自搜索引擎对原页面的摘要，措辞可能被改写过。真正读到全文的材料只有以下几类：

| 语料 | 内容 | 本报告标注 |
|---|---|---|
| `antoinejeannot/graham` | Paul Graham 文章全文镜像（抓取自 paulgraham.com） | 【原文已读】 |
| `xai-org/x-algorithm`（HEAD `b220448`，2026-11-03）与 `twitter/the-algorithm-ml` | X “For You”排序代码，含默认权重参数 | 【原文已读】 |
| `Medium/medium-api-docs` | Medium 官方 API 文档 | 【原文已读】 |
| Anthropic 工程博客三篇（Building effective agents、multi-agent research system、context engineering） | Agent 架构原则 | 【原文已读】 |
| `jpeslar1/john-peslar-ai-skills` | Tim Denning 与 David Perell 的逐字语料（编者称经作者自己的 WordPress/Substack API 拉取） | 【原文已读】（二手转载，未与在线页面逐字核对） |
| `tjxj/dankoe-archive` | Dan Koe 2026 年 19 个 YouTube 视频的自动字幕 | 【转录】 |
| `liamdonnellyonline-cell/david-perell-nonfiction-transcripts` | 97 期 Perell / How I Write 访谈转录 | 【转录】 |
| `ray-amjad/alex-hormozi-transcripts` | 514 个 Hormozi YouTube 转录（无日期） | 【转录】 |
| `itsMelo/dan-koe-notes-zh` | 61 篇 Koe 免费 newsletter 的中文压缩摘要（原文 30–50% 篇幅） | 【待核实】（意译，非原话） |
| `AlonMichael/How-I-Write-Skills` | 第三方从 104 期 How I Write 转录“蒸馏”出的 AI 技能包 | 【待核实】（AI 蒸馏，引语未与音频核对） |
| `joesmusings/quartz`、`faculorca/thenotegarden` | 第三方对 Perell One-Sheet、Günel 文章的笔记转录 | 【待核实】 |

**标注约定**：

| 标注 | 含义 |
|---|---|
| 【原文已读】 | 研究团队读过全文（见上表） |
| 【转录】 | 机器字幕或转录稿，可用，但人名和个别词可能有误（例如字幕把 Alex Hormozi 写成“Alex Hermosa”） |
| 【待核实】 | 只有搜索摘要、二手或聚合来源、AI 蒸馏，或来源之间互相矛盾 |
| 【未找到证据】 | 检索后没有找到来源 |
| 【设计建议】 | 本报告作者自己的设计，不是创作者的做法 |

为避免满篇标签，本报告另立一条默认规则：**凡带链接、但没有标注的创作者事实或平台规则，一律按【待核实】（摘要级）处理**。第一、二部分只写有来源的内容，第三部分（手册）里没有来源的部分都是【设计建议】。

**无法核实的框架名必须先说清楚。** 在能读到的 Koe 原话材料里（19 个视频的转录和 61 篇中文摘要），**没有出现**“idea bank”“content multiplication”“APAG”这几个名字，也没有出现被广泛转述的“hook → aha → practical steps”newsletter 提纲。最后这个提纲只来自 beehiiv 案例页的摘要【待核实】。Koe 自己用的词是“validated ideas/topics”“outlier content”“swipe file”“reverse engineer”“packaging”和“one topic or theme for the week”【转录】([YouTube](https://www.youtube.com/watch?v=KCjwU4XYBL8))。另外几项也没能核实：Justin Welsh 的“Content Operating System”的官方定义，Nicolas Cole 的“category creation”是否算一个写作框架（“Category of One”其实是 Cole 等人合著的 *Snow Leopard* 一书的副标题），以及 Ship 30 “1-3-1”结构的官方措辞。Welsh 的“content matrix”确有其事，但据播客章节列表，他**已经不再用了**【待核实】([Everand](https://www.everand.com/podcast/592304229/How-Justin-Welsh-Went-From-Burned-Out-Executive-to-Making-400-000-As-A-Digital-Writer-Creator-In-this-session-we-chatted-with-Justin-about-his-wr))。

**还有一层偏差需要提防。** 2026 年网上关于 X 算法的文章，大部分出自卖排期工具的厂商（OpenTweet、Blotato、Publora 等），存在利益冲突【待核实】([Blotato](https://www.blotato.com/blog/best-x-twitter-schedulers))。创作者公开的方法，很多又是他们课程的卖点（Koe 的 2 Hour Writer、Welsh 的 Content OS、Ship 30），他们有动机把系统讲得更简单。几乎所有创作者经验都带幸存者偏差，引用它们之前要记住这一点。

---
# 第一部分：平台机制与分阶段综合

## 三个平台奖励的是三种不同的东西

### Substack：拥有读者，增长靠站内网络

Substack 的核心资产是**作者自己拥有的邮件列表**。增长的主引擎是站内网络：官方 2024 年 2 月称，Recommendations 与 Substack App 带来了全部新订阅的 **50%** 和新付费订阅的 **25%**【待核实】([On Substack](https://on.substack.com/cp/142007285); [TechCrunch](https://techcrunch.com/2024/02/22/substack-now-lets-writers-curate-a-network-of-recommended-publications-for-their-subscribers/amp/))。也有二手文章称站内发现只占约 30%，两组数字互相矛盾【待核实】([wanderwealth](https://wanderwealth.substack.com/p/whats-the-1-way-to-grow-on-substack))。推荐对已经成名的作者更有利：一个约 6.7 万人的列表，推荐只带来了 189 名订阅者【待核实】([eden.so](https://eden.so/blog/substack-growth-strategy/))。Notes 能拉来免费订阅，但很少直接卖出付费。一项第三方研究分析了 **396,143 条 Notes**，发现 13.1% 至少带来一位免费订阅者，只有 **0.70%** 卖出过付费订阅【待核实】([The Writing Edge](https://thewritingedge.substack.com/p/substack-notes-convert-paid-subscribers))。Substack 官方建议的免费转付费率是 5–10%，独立分析给出的中位数约 **3%**，规划时应按 2–3% 来算【待核实】([Substack Going Paid Guide](https://substack.com/going-paid-guide); [Simon Owens](https://simonowens.substack.com/p/whats-a-realistic-conversion-rate))。Substack 没有发布过发送时间研究。一项 473,405 条 Notes 的分析发现，最佳和最差发布时段的差距只有约 3 个百分点【待核实】([Eden.so](https://eden.so/blog/best-time-to-post-on-substack/))。2026 年 Substack 陆续上线了 Notes 草稿与定时、统计 CSV 导出、Recording Studio 自动生成宣传短片等功能【待核实】([AlternativeTo](https://alternativeto.net/news/2026/4/substack-adds-note-scheduling-post-templates-drop-caps-new-livestream-options-and-more))。2026 年 7 月 Axios 报道，Substack 引入基于 **Pangram** 的 AI 检测，给出 AI 与人写的百分比评分，引起部分创作者反弹；这个评分是否影响分发，未能核实【待核实】([Axios](https://www.axios.com/2026/07/23/substack-subscribers-ai-generated-content-pangram))。工具层面，Substack **没有官方的发文、草稿或订阅者管理 API**。官方 Developer API 只能查询公开的创作者资料。最稳的读取途径是公开 RSS（`<pub>.substack.com/feed`）。非官方 API 靠浏览器 cookie（`substack.sid`）认证，稳定性差，还可能违反服务条款【待核实】([dev.to](https://dev.to/equinoxaifinancergb/does-substack-have-an-api-2026-and-what-you-can-actually-get-29il); [codalanguez/substack-mcp](https://github.com/codalanguez/substack-mcp))。Substack 也**不能把规范链接（canonical）指向别处**，所以在跨平台拓扑里它天然是“母站”【待核实】([anshulkumar](https://anshulkumar.substack.com/p/can-you-post-the-same-blog-on-substack))。

### X：排序模型奖励对话和私下转发，惩罚负反馈

X 是三个平台里唯一能从代码层面读到机制的。现在的 “For You” 排序器开源在 `xai-org/x-algorithm`。它由一个 Grok 衍生的 Transformer（Phoenix）预测约 20 种用户行为的概率，最终得分为 **Σ（权重 × 预测概率）**。README 特别提醒：权重乘的是**预测概率**，不是原始计数，所以权重之比不能当成“几个赞抵一次举报”的汇率【原文已读】([README](https://github.com/xai-org/x-algorithm))。`param.rs` 里的默认权重如下【原文已读】([param.rs](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs))：

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

2023 年的数据来自 `twitter/the-algorithm-ml` 的 recap README【原文已读】([the-algorithm-ml](https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md))。读这张表有三点要注意：第一，这些是包在 `param!` 特性开关里的**默认值**，线上实验可以覆盖，生产环境的真实权重未公开；第二，作者多样性衰减和站外（OON）乘数在开源代码里默认是 1.0，也就是不起作用，生产值同样未公开；第三，Phoenix 模型的权重本身不在仓库里【原文已读】([x-algorithm](https://github.com/xai-org/x-algorithm/tree/main/xai-value-model))。代码里还能读到几条直接影响节奏的机制。**冷启动扶持**用 Thompson 采样：发帖者粉丝不超过 **50,000**、帖子曝光不足 **200** 次、发布不超过 **2 小时**时，会被提到第 15–16 位。**AgeFilter** 会把超过 48 小时的帖子移出 For You 候选。**DedupConversationFilter** 会把同一会话的多条帖子合并显示。仓库里还有 `botmaker`、`scarecrow` 等反垃圾规则引擎和 `user-cred-v2` 用户可信度服务【原文已读】([param.rs](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs))。

**外链和 Premium 是传言最多的两项。** 当前代码里没有显式的 URL 惩罚参数，`has_url` 只作为 VMRanker 去偏实验里的一个内容特征出现【原文已读】([scorers](https://github.com/xai-org/x-algorithm/tree/main/home-mixer/scorers))。2026 年 7 月 29 日，Musk 回复 Paul Graham，说 X 已经“一年多”没有惩罚链接帖；此前产品负责人 Nikita Bier 也对 Zuckerberg 说过，链接不必再藏到回复里【待核实】([ppc.land](https://ppc.land/x-drops-year-old-link-penalty-musk-tells-zuckerberg-on-platform/))。另有摘要称 X 在 2025 年 10 月 14 日就宣布取消了链接惩罚【待核实】([SocialPilot](https://www.socialpilot.co/blog/twitter-algorithm))。但 Buffer 分析 1,880 万条帖子后发现，2025 年 3 月起，非 Premium 账号链接帖的互动中位数为**零**【待核实】([Buffer](https://buffer.com/resources/links-on-x/))；OpenTweet 2026 年分析 28,124 条帖子，链接帖的曝光是非链接帖的 1.05 倍【待核实】([OpenTweet](https://opentweet.io/answers/does-x-penalize-links-2026))。这些数据来自不同时期、不同厂商。比较可信的结论是：显式惩罚很可能已经取消，但 `open_link` 权重只有 0.2，用户点链接离站还会损失停留时长，所以链接帖在期望值上大概率仍然吃亏，需要自己做 A/B 测试。Premium 方面，2023 年代码据报有认证用户站内 4 倍、站外 2 倍的乘数，但这一条是摘要级，研究团队没有打开 2023 年的文件核实【待核实】([Blck Alpaca](https://blckalpaca.at/en/knowledge-base/social-media/social-media-algorithms-distribution/x-twitter-algorithm-open-source))。研究团队在当前仓库里检索 `premium`、`verified`、`blue`，**没有找到排序乘数**，只找到 `LimitRepliesVerified` 这类可见性规则【原文已读】([x-algorithm](https://github.com/xai-org/x-algorithm))。

**变现和 API 在 2026 年都变了。** Creator Revenue Sharing 于 2026 年 9 月 7 日停止计酬，由 **Original Content Rewards** 取代。新计划据报要求至少 500 名认证粉丝，以及过去 90 天内认证用户在首页时间线上贡献的 **50 万次曝光**，回复的曝光不计入；收入只按**原创**帖子被 Premium 用户看到的次数计算，主要价值来自他人作品的内容不计酬【待核实】([help.x.com](https://help.x.com/en/using-x/original-content-rewards); [tech-ish](https://tech-ish.com/2026/08/08/x-is-scrapping-creator-revenue-sharing-on-7-september-everyone-has-to-apply-again/))。X Articles 2024 年 3 月面向 Premium+ 上线，2026 年 1 月开放给全部 Premium 用户，并设了 **100 万美元**的最受欢迎文章奖【待核实】([PiunikaWeb](https://piunikaweb.com/2026/01/07/x-articles-premium-nikita-bier-updates/))。Koe 在视频里说自己是这项奖的“runner up”【转录】([YouTube](https://www.youtube.com/watch?v=3rNqNvwNcrM))。API 自 2026 年 2 月起默认按次付费，新开发者没有免费档。据第三方报道，发一条普通帖约 **$0.015**，**含 URL 的帖子 $0.20**（2026 年 4 月 20 日起），读取一条帖子约 $0.005【待核实】([Postproxy](https://postproxy.dev/blog/x-api-pricing-2026/); [OpenTweet](https://opentweet.io/x-api-pricing))。自动化账号必须开启“Automated”标签并关联一个真人账号；据报 AI 自动回复机器人需要事先获得 X 的书面批准【待核实】([docs.x.com](https://docs.x.com/developer-guidelines); [OpenTweet](https://opentweet.io/x-automation-rules))。另据单一来源，2026 年 10 月 9 日生效的服务条款修订，明确了用户要为自主功能或 Agent 的行为负责【待核实】([note.com](https://note.com/munou_ac/n/n0fb681d97ded?hl=en))。

### Medium：人工策展决定上限，钱跟着会员阅读时长走

Medium 有三档分发：Network Only（只推给关注者）、General Distribution（默认的算法分发）和 **Boost**（人工策展）【待核实】([Medium Help](https://help.medium.com/hc/en-us/articles/360018677974-About-Medium-s-distribution-and-earnings-system))。约一半 Boost 来自受邀出版物编辑的提名，另一半由 Medium 内部策展团队直接挑选。普通作者不能提名自己的稿子；身为提名人的作者每月最多自荐 2 篇；超过 6 个月的稿子不能被提名；被拒的稿子不给反馈，也不能申诉【待核实】([Help: Participation](https://help.medium.com/hc/en-us/articles/26729526741399-Boost-Nomination-Program-Participation); [Help: nominate](https://help.medium.com/hc/en-us/articles/26716107269527-How-do-I-nominate-a-story-for-Boosting))。Boost 的现行标准是：读者的生活是否因这篇文章变得更丰富，以及是否是“原创、人写、探讨此前未知或少有人审视之物”的内容【待核实】([Medium Blog](https://medium.com/blog/updated-guidelines-for-boost-47799aad8899))。官方还写明，如果标题、副标题和封面图提供的语境不够，就**不会 Boost**【待核实】([Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution))。

Partner Program（MPP）从付费会员的订阅费里分钱。付费会员阅读满 30 秒才算一次阅读，闲置时间不计；每种互动（鼓掌、高亮、回复）只在第一次计分；Boost 稿件的互动计分倍率更高；非会员的阅读和 Friend Link 带来的阅读都不算钱【待核实】([Help: Earnings](https://help.medium.com/hc/en-us/articles/360036691193-Medium-Partner-Program-earnings-calculation))。2025 年 10 月起，Medium 把 **5%** 的预算转给带来站外流量的稿件；11 月起，又把 **15%** 转给通过搜索引擎进站的会员阅读【待核实】([Medium Blog](https://medium.com/blog/partner-program-update-starting-november-1-were-rewarding-search-traffic-3ac0635f9f6b))。之后还有几项调整：2026 年 1 月把原本集中给 Boost 稿的收入分散到更多稿件，2 月 17 日起奖励带来新会员的付费墙文章，6 月 1 日起推出 Editor Partner Program 给编辑付钱【待核实】([Medium Blog: Jan](https://medium.com/blog/partner-program-update-starting-january-1-were-rewarding-writing-more-broadly-4907e149e38c); [Feb](https://medium.com/blog/partner-program-update-starting-february-17-were-rewarding-stories-that-bring-in-new-members-3e84d2eb6e68); [Jun](https://medium.com/blog/partner-program-update-starting-june-1-were-rewarding-editors-for-stories-they-edit-aaec12a97cea))。收入呈幂律分布：2023 年在收入至少 $10 的作者里，约 65% 收入在 $10–$100 之间【待核实】([Vocal](https://vocal.media/journal/massive-changes-to-how-medium-pays-its-writers-are-you-ready))。CEO Tony Stubblebine 自己也说，Medium 是用来“联合发布、给其他平台做增长”的地方，光靠 MPP 维持不了生计【待核实】([Medium Handbook](https://medium.com/medium-handbook/is-medium-worth-it-in-2026-194a85fb2f35))。

**AI 政策是 Medium 对 Agent 最硬的约束。** 自 2024 年 5 月 1 日起，AI 生成的文字无论是否披露，都不能放进付费墙；披露过、且不设付费墙的 AI 文字可以获得 General Distribution，但不能获得 Boost；未披露的 AI 文字只能拿到 Network Only；屡次违规可能被取消 MPP 资格【待核实】([Help: AI policy](https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy); [Plagiarism Today](https://www.plagiarismtoday.com/2024/04/11/medium-sets-new-policies-on-ai-generated-writing/))。Boost 帮助页的措辞更严，写的是 AI 生成的文字“不具备分发资格（更别说 Boost）”，可能是后来收紧了，需要再核实【待核实】([Help: Nominations](https://help.medium.com/hc/en-us/sections/26573008251543-Nominations))。2025 年的一份通知把“AI 生成”定义为“大部分内容由 AI 写作程序生成，几乎没有编辑、改进、事实核查或修改”；用 AI 辅助列提纲、检查语法、核对事实，不在禁止之列【待核实】([zidailma](https://zidailma.medium.com/a-new-medium-policy-you-didnt-know-76a751aaaf16))。工具层面，官方文档写明：“The Medium API is no longer supported… We don't allow any new integrations with our API.” 旧接口 `POST /v1/users/{authorId}/posts` 支持 `contentFormat`（html/markdown）、`canonicalUrl` 和 `publishStatus`（public/draft/unlisted），但没有编辑、删除、统计或定时功能【原文已读】([medium-api-docs](https://github.com/Medium/medium-api-docs))。据厂商文档，2025 年 1 月 1 日起 Medium 不再发放新的集成 token，旧 token 据报仍可用【待核实】([StackOne](https://docs.stackone.com/connectors/medium/guides/link-account/integration-token))。人工可用的 **Import a story** 工具会把文章回溯到原始发布日期，并自动加上指向原文的 canonical 链接；手动粘贴则不会带 canonical【待核实】([Help: Import](https://help.medium.com/hc/en-us/articles/214550207-Import-post); [Help: canonical](https://help.medium.com/hc/en-us/articles/360033930293))。平台本身是稳定的：2024 年 8 月首次实现月度盈利，之后一直保持盈利；2024 年 4 月付费会员超过 100 万【待核实】([TechCrunch](https://techcrunch.com/2025/07/11/mediums-ceo-explains-what-it-took-to-stop-losing-2-6m-monthly))。不过它的规则几乎按月变化，**Agent 应当从配置文件读取 Medium 的政策参数，不要写死在代码里**【设计建议】。

### 跨平台对比

| 维度 | Substack | X | Medium |
|---|---|---|---|
| 分发核心 | 邮件列表 + 站内网络（推荐、App、Notes） | Phoenix 预测行为概率的加权和；48 小时候选窗口 | 三档分发；Boost 由人工策展（一半来自出版物提名） |
| 受众归属 | 作者拥有邮件列表 | 平台拥有关注关系 | 平台拥有；作者不能直接给关注者发邮件 |
| 主要体裁 | 长文（邮件+网页）、Notes、直播/视频 | 单帖、Thread、X Articles、视频 | 文章（标题+副标题+封面图是分发入口） |
| 增长主杠杆 | 推荐网络约 50% 新订阅（2024） | 回复、引用、私信/复制链接分享；小号的冷启动 2 小时窗口 | Boost；进入有提名资格的出版物；站外和搜索流量 |
| 变现 | 订阅（中位转化约 3%）、赞助 | Original Content Rewards（门槛 50 万认证曝光/90 天）；主要价值在导流到自有产品 | MPP 按会员阅读时长+互动；多数人每月不到 $100 |
| AI 政策 | 2026 年 7 月起 Pangram 检测（影响未知） | 文字无披露要求；AI 媒体可标“Made with AI”；AI 自动回复需批准 | AI 文字不能设付费墙，不能 Boost；未披露降为 Network Only |
| 官方写入通道 | 无 | 按次付费 API（$0.015/帖，含 URL $0.20） | API 不再支持、不发新 token；人工 Import |
| 外链 | 自身就是链接目的地 | 显式惩罚据称已取消；`open_link` 权重仅 0.2 | 文内 CTA 导向 newsletter |
| Canonical | 不能指向别处，适合当母站 | 无 canonical 概念 | Import 自动设置；也可手动设置 |
| 证据强度 | 官方摘要 + 第三方研究 | **代码可读**（机制强，量级弱） | 官方帮助页摘要 |
| Agent 定位【设计建议】 | 母稿与关系经营，发送由人完成 | 测题场与引流；节制自动化 | 联合发布与搜索资产；人写为主 |

---

## 分阶段综合：四个阶段的可复制机制

### 创意：题源有四条，排序权交给作者的兴奋度

**第一条题源是读者问题清单。** Lenny Rachitsky 维护一份 30–50 个题目的清单，读者问题来了就加进去，然后“按我最想写的排序”【待核实】([Indie Hackers AMA](https://www.indiehackers.com/post/i-write-lennys-newsletter-the-1-paid-business-newsletter-on-substack-generating-over-500k-arr-ama-46fe3dfdc4))。Matt Yglesias 的 mailbag 分两步，先周日征集问题，再周一让读者在三个候选里投票【待核实】([Brad DeLong](https://braddelong.substack.com/p/should-i-be-running-a-mail-answers))。Noah Smith 和 Ted Gioia 也会定期发投票帖或征求建议的帖子【待核实】([Noahpinion](https://www.noahpinion.blog/p/tell-me-what-you-want-what-you-really))。

**第二条是用一个固定视角处理无穷的输入。** Heather Cox Richardson 每天早上先花 1–2 小时浏览社交媒体，再用历史学家的视角解读当天新闻【待核实】([KALX](https://kalx.berkeley.edu/kalx-news-heather-cox-richardson-interview))。Kyla Scanlon 把宏观经济翻译成对个人的影响，Emily Oster 把科研翻译成育儿问题的答案【待核实】([Fortune](https://fortune.com/2024/06/26/kyla-scanlon-tiktok-youtube-newsletter-economist-vibecession))。Dan Koe 说“你不需要细分领域，你需要一个视角”，“你就是那个细分领域”【转录】([YouTube](https://www.youtube.com/watch?v=3rNqNvwNcrM))。Perell 的 Personal Monopoly 是“技能、兴趣和个性的独特交集”【原文已读】([perell.com](https://perell.com/note/build-a-personal-monopoly/))。Denning 说“读者买的是人，不是细分领域”【原文已读】([timdenning.com](https://timdenning.com/tim-denning-is-rich/))。这几种说法用词不同，指向的是同一件事：**定位靠身份加视角，不靠收窄题材**。

**第三条是市场验证过的题。** 这是 X 生态最有特色的做法。Koe 按热度排序其他创作者的内容，研究异常值（outlier），并反复挖掘自己的旧爆款。他 2019 年写过一条以“how to get ahead of 99% of people”开头的推文，2023 年改成 YouTube 视频，到 2026 年 5 月是他播放量最高的视频（**170 万次**）【转录】([YouTube](https://www.youtube.com/watch?v=7HM-rptYdTs))。他把“借”的边界划得很清楚：别人的措辞和结构归别人，想法可以拿；“复制粘贴、换几个词”会让你“看起来像个白痴”【转录】(同上)。Hormozi 把 X 和 TikTok 当试验场，跑出效果的点子再扩写【待核实】([Video Creatr](https://www.buzzsprout.com/1887347/episodes/17152925-how-alex-hormozi-posts-300-times-a-week))。Ship 30 的 **4A**（Actionable、Analytical、Aspirational、Anthropological）和 Welsh 的“主题 × 体裁”矩阵，提供的是组合式的选题生成方法【待核实】([Bush thread](https://threadreaderapp.com/thread/1534574544895234049.html))。

**第四条是作者自己的经历。** Medium 体系最强调这一条。Medium 的指南称赞“直接基于作者经历”的内容【待核实】([Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution))。Awosika 的建议是“采访过去的自己”【待核实】([LinkedIn](https://www.linkedin.com/in/ayotheauthor/))。Perell 说：“50 加仑树汁才熬出 1 加仑糖浆……觉得点子不够时，我就去收集更多经历。”【原文已读】([perell.com](https://perell.com/essay/expression-is-compression/))

这四条题源最后都要过 PG 的一道关：**没有 edge 就不该动笔**。edge 不需要是完整论点，“对别人视为理所当然的事抱有疑问”就够了；而且这种切入点“没法系统地生成”【原文已读】([The Best Essay](https://paulgraham.com/best.html))。这一点直接决定了 Agent 在选题阶段的边界：它可以找出候选的“缝隙”，但提供不了洞见本身。

### 素材：一个收集箱、写前统一清理，再加上真实证据

**有文档的素材系统都出奇地简单。** Ryan Broderick 全天把链接收进 Raindrop 的分类文件夹，写作当天早上倒进一个 Google Doc，逐条检查链接有没有被删或更新【待核实】([The Story](https://thestory.au/articles/ryan-broderick-garbage-day-newsletter-interview/))。Lenny 每篇研究型文章开一个“乱糟糟的”文档，最后再把“原始素材块”塑成文章【待核实】([Compound Planning](https://manual.compoundplanning.com/chapters/interview-with-lenny-rachitsky-writer-of-lennys-newsletter))。Koe 明确反对精致的第二大脑：“系统都会熵增……拥抱混乱”，“如果需要记住，那它就不重要”【转录】([YouTube](https://www.youtube.com/watch?v=KCjwU4XYBL8))。他的做法是每周一个看板，里面放一份粗提纲、粘进来当研究材料的 YouTube 链接，旁边开着 AI 对话，用来从这些视频里“提取需要的观点”【转录】(同上)。Sahil Bloom 用一本口袋笔记本，每周日带着它散步一小时【待核实】([Practical PKM](https://practicalpkm.kit.com/posts/creativity-flywheels-vol-2-sahil-bloom))。Henrik Karlsson 先收集“原始素材”再起稿，因为一旦觉得自己在写文章，人就会紧张，过早开始打磨文字【待核实】([Escaping Flatland](https://www.henrikkarlsson.xyz/p/on-the-preparations-before-writing))。

**真正形成护城河的素材，是 AI 拿不到的东西。** Lenny 和 Orosz 都和数据伙伴一起做读者调查，样本分别约 1,750 人和 3,000 多人【待核实】([Lenny's Newsletter](https://www.lennysnewsletter.com/p/ai-tools-are-overdelivering-results); [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/the-pragmatic-engineer-2025-survey))。据 Nieman Lab 标题，Casey Newton 2026 年把 Platformer 改为“更多独家，更少聚合”，明确是为了和 AI 竞争【待核实】([Nieman Lab](https://www.niemanlab.org/2026/04/more-scoops-less-aggregation-and-analysis-how-casey-newton-is-revamping-his-newsletter-to-compete-with-ai/))。Hormozi 的说法更直接：利害越高，人越不会听一个没有第三方证明的人。他的做法是把真实会议录下来转成文字，让 AI 挑出“有意思的时刻”，“而不是自己编故事”【转录】([YouTube](https://www.youtube.com/watch?v=XsWSvz-aewA))。Jack Butcher 把做事过程中留下的副产品叫作“锯末”（sawdust），认为它本身就是可以发布的素材【转录】([YouTube](https://www.youtube.com/watch?v=EGnSx3EYEU0))。准确性方面，HCR 的规则据报是没有三个独立来源就不发【待核实】([Brian Boyles](https://brianboyles.substack.com/p/my-conversation-with-heather-cox))，Noah Smith 会回到 FRED 的原始数据重建图表【待核实】([Noahpinion](https://www.noahpinion.blog/p/how-not-to-be-fooled-by-viral-charts))。

### 创作：每种体裁的写法不同，但“松后紧”的循环是共通的

**通用循环来自 PG，而且是读过全文的。** 他的建议是尽快写出一个糟糕的初版，并预期文章 80% 的想法在动笔之后才出现，起初的想法有一半是错的。整篇 2005 年的文章他用了 67 分钟，其中 23 分钟写、44 分钟改【原文已读】([Writing, Briefly](https://paulgraham.com/writing44.html))。写作把想法“从模糊变成糟糕”，而这是进步，因为糟糕的地方看得见，看得见就能改；文章至少一半的工夫，花在反问“这对吗？完整吗？”上【原文已读】([The Best Essay](https://paulgraham.com/best.html))。他说自己的策略是“先松后紧”：有些句子发布前读了 100 遍，那些别扭的段落像“刺”一样勾住袖子，“不全拔掉我不发”【原文已读】([How to Write Usefully](https://paulgraham.com/useful.html))。

**Substack 长文**分两种原型。日更型靠阅读量和惯性，例如 HCR 每天写约 1,200 字【待核实】([BC Magazine](https://www.bc.edu/content/bc-web/sites/bc-magazine/fall-2022-issue/features/history-s-first-draft.html))。旗舰深度型投入大，例如 Lenny 每篇中位数 10 小时，多则 100 小时以上，并且有专门的编辑【待核实】([Lenny's Newsletter](https://www.lennysnewsletter.com/p/500000))。Packy 先写出 V0，然后把它当作“删稿垃圾场”，前后写六七稿，经常每一稿都新开一个文档【待核实】([How-I-Write-Skills](https://github.com/AlonMichael/How-I-Write-Skills/blob/main/skills/format-adapt/SKILL.md))。Ben Thompson 区分免费稿和付费稿：免费稿需要好钩子，付费稿可以默认读者知道得更多；他还说“你写的最重要的文章，是读者读的第二篇”【待核实】(同上)。Doomberg 先定标题，再给每段写一句话摘要【待核实】([Fire2Fission](https://www.fire2fission.com/podcast-episodes/050-doomberg))。

**Substack Notes** 的作用是拉新和维系关系。Tom Kuegler 说“Notes 本身就让 newsletter 增长了起来”【待核实】([Newsletter Circle](https://newslettercircle.com/interviews/tom-kuegler-the-writing-long-game/))。Koe 把推文同步发到 Notes，并说 Notes 信息流里的人“真正欣赏深度思考”【转录】([YouTube](https://www.youtube.com/watch?v=3rNqNvwNcrM))。

**X 单帖**的核心技法是压缩和具体。Bloom 卡住的时候会打开 Twitter，把要写的东西压进字数限制里，“越写越短”【转录】([YouTube](https://www.youtube.com/watch?v=f-s22uCixMw))。Harry Dry 用三个问题检验每一句话：能想象出画面吗？能被证伪吗？只有你能说吗？【转录】([YouTube](https://www.youtube.com/watch?v=TUMjnmfsPeM))。

**X Thread** 起源于 Andreessen 的“tweetstorm”，因为 140 字“显然不够用”【转录】([YouTube](https://www.youtube.com/watch?v=tV6kDr1rwTs))。Bloom 的线程模仿 Ben Thompson 和 David Senra，在新想法里串起自己以前的想法，“做一个 Twitter 原生的博客”【转录】([YouTube](https://www.youtube.com/watch?v=f-s22uCixMw))。Cole 的建议是首条推文给出一个故事或一个框架，或者预告后面的可操作建议，标题要“清楚，而不是聪明”【待核实】([Cole thread](https://threadreaderapp.com/thread/1441450057119592456.html))。代码层面，DedupConversationFilter 会合并同一会话，所以线程的分发主要靠首帖【原文已读】([README](https://github.com/xai-org/x-algorithm))。

**X Articles** 目前**没有找到**创作者自己总结的模板【未找到证据】。Koe 的做法就是把 newsletter 原样粘贴过去【转录】([YouTube](https://www.youtube.com/watch?v=KCjwU4XYBL8))。

**Medium 文章**最依赖结构和包装。Cole 的标题公式要回答三个问题：写什么、写给谁、承诺什么；他建议先写标题，正文用“引言 + 约 3 个要点 + 结论”的骨架【待核实】([Nicolas Cole](https://nicolascole77.medium.com/3-simple-ways-to-make-your-medium-headlines-irresistible-click-6a401cc0a02b))。Denning 的标题测试是“五年级学生能看懂”，并且要回答“凭什么有人点”【原文已读】([timdenning.com](https://timdenning.com/writing-harsh-truths/))。“5–7 分钟阅读最佳”只是社区传言，官方的说法是篇幅要“服务于故事本身”【待核实】([Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution))。

### 发布：长拆短是主流，短养长是研发层

**两种流向构成一个循环。** 以 newsletter 为核心资产的经营者，主流做法是“长拆短”，也就是 hub-and-spoke：Welsh 每周一篇 newsletter 拆出 6–10 个短帖，附 2 个导流 CTA【待核实】([Growing Viral](https://growingviral.beehiiv.com/p/justin-welsh-turning-1-piece-content-100-highvalue-posts))；Koe 的拆分链是全公开样本里最完整的【转录】([YouTube](https://www.youtube.com/watch?v=KCjwU4XYBL8))；Gary Vaynerchuk 把这叫作“reverse pyramid”【待核实】([garyvaynerchuk.com](https://garyvaynerchuk.com/THE-GARYVEE-CONTENT-STRATEGY-HOW-TO-GROW-AND-DISTRIBUTE-YOUR-BRANDS-SOCIAL-MEDIA-CONTENT/))。“短养长”则是研发层：Naval 的推文风暴后来由 Eric Jorgenson 编成书，播客逐条“展开”【转录】([YouTube](https://www.youtube.com/watch?v=mWYMRCcYn-Q))；Dickie Bush 据报说过“我的每篇文章都从一条推文开始”【待核实】([quotewise](https://quotewise.io/q/w8hnsw/))。

**改编必须做成平台原生的。** Denning 说：“复制粘贴行不通，每个平台……都像在学一门语言。”【转录】([Small Business Big Marketing #637](https://podcasts.apple.com/us/podcast/how-writing-changed-tim-dennings-business-life-forever-637/id319019197?i=1000613999291))。Kuegler 的立场相反，他认为“同时在 38 个平台上”被高估了，于是全押 Substack【待核实】([Kuegler Note](https://substack.com/@tomkuegler/note/c-53765421))。Koe 还提醒，产量不要太多：“降低量，提高质量……给品牌加一点稀缺感。”【转录】([YouTube](https://www.youtube.com/watch?v=KCjwU4XYBL8))

**归因只能靠 UTM。** Substack 文章统计里有“流量来源”和“订阅来源”两个排名，但流量第一的渠道不一定是订阅第一的渠道，而且看不到读者点的是文内哪一个链接【待核实】([On Substack](https://on.substack.com/p/post-stats-substack-app); [simonkjones](https://simonkjones.substack.com/p/understanding-substacks-analytics))。至于 X 到订阅的转化率、Medium 到 Substack 的转化率，研究团队**都没有找到**可靠的公开数据【未找到证据】。

### 四阶段证据速览

| 阶段 | 证据最强的可复制机制 | 代表人物 | 主要证据缺口 |
|---|---|---|---|
| 创意 | 读者问题清单按兴奋度排序；固定视角；验证过的异常值选题；edge 检验 | Lenny、HCR、Koe、PG | “不写什么”清单；X 上追热点的方法 |
| 素材 | 收集箱 → 写前清理；每篇一个乱文档；真实会议转录；专有调查 | Broderick、Lenny、Hormozi、Orosz | RSS、Obsidian 的使用证据；更正政策 |
| 创作 | 快速烂初稿 → 陌生人重读 → 拔刺；句子三问；压缩到 280 字 | PG、Dry、Bloom、Cole | X Articles 模板；体裁与转化之间的定量关系 |
| 发布 | 长拆短 + 短养长；平台原生改编；站内网络 | Koe、Welsh、Naval、Substack 官方 | X 和 Medium 到订阅的转化数据；Typefully、Buffer 的 API 细节 |

---
# 第二部分：创作心法

## Dan Koe：一篇周更 newsletter 养活整个媒体矩阵

> 本节主要依据 `tjxj/dankoe-archive` 里 2026 年 1–9 月的 19 个视频的自动字幕【转录】，以及 `itsMelo/dan-koe-notes-zh` 的中文摘要【待核实】。其余来源都是搜索摘要。

**定位与哲学：写作是“撬动其他杠杆的杠杆”。** Koe 的说法是：“写作是解锁其他形式杠杆的杠杆。”他认为一份 1,000 到 10,000 人的邮件列表，一封邮件就能赚“1 万到 10 万美元”【转录】([KCjwU4XYBL8](https://www.youtube.com/watch?v=KCjwU4XYBL8))。“写作即思考”在他那里叫“强制线性”：脑子里自以为懂了，写作逼你把它压成一条单线。他还说“80% 的写作是研究和学习”【转录】(同上)。他把内容分成“快内容”和“慢内容”。快内容是清单体、愤怒推文、“AI 生成的摘要”和“为互动优化的线程”；慢内容是长文、长对话，以及“让你得思考才能领会的推文”【转录】([3rNqNvwNcrM](https://www.youtube.com/watch?v=3rNqNvwNcrM))。他有两个内容支柱：一是怎样弄清自己想要什么（心理学、哲学、个人成长），二是怎样做成它（技能、商业、技术、AI）【转录】([VyR8nqD3sQ8](https://www.youtube.com/watch?v=VyR8nqD3sQ8))。

**选题：市场验证在先，个人视角过滤在后。** 他挑题的两条原则是：第一，这件事我是否觉得重要、值得分享，因为“只要经过我的视角过滤，它就变得独特”；第二，它的包装或框定能否抓住注意力，因为“有日记，也有写作”【转录】([KCjwU4XYBL8](https://www.youtube.com/watch?v=KCjwU4XYBL8))。动笔前他会做市场研究：“发 YouTube 视频之前，先看什么标题有效……反复读高表现的推文……问自己它为什么比我的好……做有效的事，但加上你自己的东西。”【转录】(同上)。2026 年 7 月那期视频的选题，就来自一个约 70 万播放、叫“The Notebook System that saved my brain”的视频，他把它改成了“The Writing System That Saved My Brain”【转录】(同上)。他的具体做法是：找一个创作者，按热度给他的内容排序，然后点自家 Eden 应用里的“reverse engineer”按钮；他也提到 YouTube 异常值工具 1of10 可以替代【转录】(同上)。他还持续挖自己的旧爆款，“这其实就是我现在还在增长的方式”；他也承认有些题目“已经死了”，需要一段“重置期”【转录】([7HM-rptYdTs](https://www.youtube.com/watch?v=7HM-rptYdTs))。

**素材：每周一个看板，不搞第二大脑。** 他总结过这套系统需要的东西：一周一个主题（对他来说就是 newsletter），一个能快速记下想法的地方，一个收集灵感的方式（社交帖、YouTube 视频、Substack 文章、PDF、图片），懂得怎样包装钩子和标题，以及写作时能从想法、灵感和研究里顺手取用【转录】([KCjwU4XYBL8](https://www.youtube.com/watch?v=KCjwU4XYBL8))。他把“一周一个目标”带来的被动收集归功于《Psycho-Cybernetics》：散步、听人聊天时冒出来的点子，“会自己连到我的 newsletter 上”【转录】(同上)。

**写作与打包：内容是自己的，包装可以研究别人。** 他把写作比作礼物：有内容，也有包装；标题和缩略图“可以之后再做”【转录】(同上)。他给写长文的建议是：写真正感兴趣的东西；只抓一个主要观点；把写作当成研究和学习的机会，钻进兔子洞；不要把单一来源当成定论；先别套模板，先写；和自己辩论，用提问把文字推下去，结构的事放到后面；先把思考做完，问自己“我真的相信这个吗”，因为写作的意义在于“改变你相信的东西”【转录】([3rNqNvwNcrM](https://www.youtube.com/watch?v=3rNqNvwNcrM))。他做视频时打开 newsletter，“不是逐字念，而是把它当成可以即兴发挥的提纲”【转录】([7HM-rptYdTs](https://www.youtube.com/watch?v=7HM-rptYdTs))。至于 newsletter 怎么分节、写多少字、有没有单独的逐句编辑环节，研究团队**没有找到**他本人的说法。他只说提纲和结构“值得单独做一期视频”，并推荐了社区根据他的头部文章做的写作提示词【转录】([KCjwU4XYBL8](https://www.youtube.com/watch?v=KCjwU4XYBL8))。有一位编辑写过文章，标题是“My So-called Creator Life and Editing Dan Koe”，但内容没能读到【未找到证据】([otherwordy](https://otherwordy.substack.com/p/my-so-called-creator-life-and-editing))。

**分发链：他自己讲得最完整。** 原话如下：“我把一篇 newsletter 发到 Substack……复制粘贴到 X Articles……它最终变成一份宽松的 YouTube 脚本，YouTube 视频再上传到播客频道，然后我一整周都可以从原来的 newsletter 里找推文点子……这些推文同步到 Substack Notes，我再把它们做成图片发到 Instagram 和 LinkedIn。有些我特别喜欢的推文，我就坐到镜头前把它念出来，于是就有了 Reels、TikTok 和 Shorts，而这每天只花一两个小时。”【转录】(同上)。他的 Instagram 帖子“全是做成图片的文字帖”【转录】(同上)。他还建议先写作再做视频：先攒出“一批脚本”，再用写作平台积累的受众去带动 YouTube【转录】(同上)。

**时间与工具。** 他说：“我整个生意建立在每天早上 1 到 2 小时的写作上。”【转录】(同上)。中文摘要记录的晨间流程是：散步 30 分钟，写作 90 分钟，然后去健身，之后才处理邮件和会议【待核实】([letters.thedankoe.com](https://letters.thedankoe.com/p/the-1-million-dollar-morning-routine))。给新手的配方是每天 60 分钟：30 分钟研究验证过的帖子并起草，30 分钟在私信和回复里交朋友，比如“每天私信 5 个人，坚持 30 或 60 天”【转录】([7HM-rptYdTs](https://www.youtube.com/watch?v=7HM-rptYdTs))。工具从 Kortex 换成了 Eden（2025 年 11 月 24 日开始早期访问），里面有看板、swipe file、按内容支柱筛选的异常值发现流、按创作者的热门过滤、reverse engineer 和 AI 对话【转录】(同上); 【待核实】([eden.so](https://eden.so/help/kortex-to-eden-everything-you-need-to-know))。他也承认 Eden 曾经“因为 AI 额度开销而破产”，不得不转型【转录】([7HM-rptYdTs](https://www.youtube.com/watch?v=7HM-rptYdTs))。

**AI 观：拿来做迭代和研究，不交出思考。** 他的用法是：“我拿我喜欢的好帖子，让 AI 给我出一些变体，我读一遍，等某一个击中我……它先经过 AI，再经过我的脑子，因为我通常不会照搬它的话……到最后通常会得到一个相当原创的东西。”【转录】(同上)。他也会把某个创作者的热门视频丢给 AI，问“这个人的世界观是什么？他怎么组织视频？我下一期可以怎么用？”【转录】(同上)。他的警告同样明确：AI“非常快地耗尽创造力”；“你可以让 AI 说点新东西，但你已经在预期它了，它就不再新了”；“只有人能写长文，因为机器人没有一个处境中的视角”；AI“能模仿看起来像真思考的东西，而不需要创作者或读者付出任何认知努力”；“AI 的默认输出通常不怎么样”；“当所有人都有超能力时，就没有人有超能力”【转录】([3rNqNvwNcrM](https://www.youtube.com/watch?v=3rNqNvwNcrM); [VXgusdDbsQE](https://www.youtube.com/watch?v=VXgusdDbsQE); [7HM-rptYdTs](https://www.youtube.com/watch?v=7HM-rptYdTs))。关于 Agent 热潮，他说很多人在 AI 额度上花了几百到上千美元，最后系统崩掉，“因为他们不知道好是什么样子……那他们怎么当 Agent 的经理或 CEO？”【转录】([VXgusdDbsQE](https://www.youtube.com/watch?v=VXgusdDbsQE))。粉丝根据 Greg Isenberg 对他的访谈做了一个 Claude Code 系统，包括 swipe file 拆解器、从 newsletter 生成 5 份提纲、生成 60 条推文、生成 30 个 YouTube 标题。这属于**第三方的解读**，不是他本人的工作流【待核实】([vincentchan/AI-Content-Engine](https://github.com/vincentchan/AI-Content-Engine))。

**变现与数字。** 他的模型是：“写内容，拿到流量……流量多少加上产品多好，决定你赚多少。”产品阶梯是电子书、课程、cohort、社区【转录】([VyR8nqD3sQ8](https://www.youtube.com/watch?v=VyR8nqD3sQ8))。他引用 Eugene Schwartz 的市场成熟度理论，认为信息产品已经到了“最后阶段”，普通产品会卖得很差【转录】(同上)。他算过一笔“100 万美元”的账：每天约 $2,777，在 2.5% 的转化率下大约需要每天 720 名访客【转录】([VXgusdDbsQE](https://www.youtube.com/watch?v=VXgusdDbsQE))。据中文摘要，拥有几百万粉丝的他，从 Instagram 或 X 拿到的平台分成每月只有约 $300–1,000，而自有产品每月有 $5 万–20 万以上【待核实】([letters.thedankoe.com](https://letters.thedankoe.com/p/how-to-start-a-one-person-business))。“How to fix your entire life in 1 day”一文 2026 年 1 月在 X 上走红，各来源报的浏览量在 1.47 亿到 1.7 亿之间【待核实】([Pocket Casts](https://pocketcasts.com/podcast/the-koe-cast/45f95490-82f5-0139-34c5-0acc26574db2/how-to-fix-your-entire-life-in-1-day/b0008693-b693-4edb-aa3a-e77d5b946362))，但平台 14 天只付了约 $4,495【待核实】([KuCoin](https://www.kucoin.com/news/flash/dan-koe-s-article-on-x-hits-150m-views-sparks-discussion-on-solo-creator-earnings))。年收入 $250 万（2023）、$400 万以上，以及 newsletter 约 29.3 万订阅（2026 年 4 月）这些数字，都来自第三方，没有审计【待核实】([yespress](https://yespress.io/dan-koe))。

**批评与内在张力。** 有分量的批评文章研究团队没有找到【未找到证据】，能找到的只有 Reddit 上对“导师”的怀疑、Tim Denning 的讽刺帖，以及 Eden 险些破产和他所宣扬的精益经营之间的反差【待核实】([Tim Denning](https://timdenning.substack.com/p/twelve-quotes-from-philosopher-dan); [huxiu](https://www.huxiu.com/article/4858483.html))。他自己的材料里就有一处明显的张力：他批评“为互动优化的线程”是快内容，自家工具却专门为互动验证过的包装而做（异常值发现流、reverse engineer）【转录】([3rNqNvwNcrM](https://www.youtube.com/watch?v=3rNqNvwNcrM); [7HM-rptYdTs](https://www.youtube.com/watch?v=7HM-rptYdTs))。研究团队的推断是：他在 2019–2021 年就开始做 X，吃到了早期红利，存在幸存者偏差；而且他主要的变现对象，正是想学“怎么增长”的创作者【设计建议·分析推断】。

**对手册的启示。** Koe 的系统可以直接拆成 Agent 模块：每周选一个母题，异常值和旧爆款扫描，swipe file，母稿之后的拆分链，包装放到最后做，AI 只做变体和研究问答。必须留给人的有三样：视角过滤（“我是否觉得重要”），对 AI 变体的取舍（“等某一个击中我”），以及判断什么是好的品味。

---

## 其他十五位创作者的心法档案

### Paul Graham：一套可以逐字复制的写作“源代码”【原文已读】

PG 的系统在 2005 到 2024 年的文章里一以贯之，而且读得到原文，是最适合翻译成 Agent 规则的材料。**选题**要有 edge，好问题往往带点“出格”：反直觉、野心过大或者离经叛道，最好三样都占；如果人们觉得某个问题“早被研究透了”，那反而是好信号；另外你必须真的对它感兴趣【原文已读】([The Best Essay](https://paulgraham.com/best.html))。**写作过程**是一次树搜索：每个问题有多个可能的回答，沿着“普遍性和新颖性组合最高”的那条分支走；跑题时先别管，事后发现走太远了再回头。他在那篇文章里删掉了一个“17 段的子树”，并且说“要快刀斩”，因为最危险的诱惑是留下一段不对的东西，只因为里面有几句好话或者花了很多功夫【原文已读】(同上)。**检验**有两道。一是“中立陌生人”：假装自己是一个对你脑子里的东西一无所知的读者，问它对吗、完整吗。“陌生人是理性的，所以只要问他需要什么，你总能过关。”他一篇文章写两周，草稿读 50 遍【原文已读】([Putting Ideas into Words](https://paulgraham.com/words.html))。二是有用性公式：有用的写作告诉人们一件**真实、重要、他们还不知道**的事，而且说得**尽可能明确**；这四个因素“像可以相乘的数”，论断应该“在不失真的前提下尽可能强”【原文已读】([How to Write Usefully](https://paulgraham.com/useful.html))。**防误读**的原则是：预先堵住“一个相当聪明且善意的人”可能产生的误读；对恶意曲解的辩护放进尾注，“不要在窗户上装栏杆”【原文已读】(同上)。**措辞**方面，花哨的文字不仅掩盖想法，“还能掩盖想法的缺失”；用复杂句子和生僻词“永远不要是无意的”【原文已读】([Write Simply](https://paulgraham.com/simply.html))。**战术清单**里有几条：卡住时把打算写的东西讲给别人听，再把说过的话写下来；朗读，找出读起来会磕绊的地方和“你害怕读的段落”；要为一个不会像你那样仔细阅读的读者写；收工时给自己留一个容易开头的地方【原文已读】([Writing, Briefly](https://paulgraham.com/writing44.html))。**AI 时代**，他判断世界会分成“会写的人和不会写的人”，因为“写作就是思考”【原文已读】([Writes and Write-Nots](https://paulgraham.com/writes.html))。

### Morgan Housel：自私写作，每个词值 100 美元【待核实】

Housel 认为“了解你的读者”是最糟糕的写作建议，因为它会滑向迎合。他只写自己觉得有意思的东西，也就是所谓“自私写作”【待核实】([Writer Science](https://www.writerscience.com/the-single-worst-piece-of-writing-advice/))。他边写边改每一句，问有没有更好的词，并说写作过程本身就是他的研究过程。关于他对“写完初稿就发”的态度，摘要措辞前后矛盾，需要回原文核对【待核实】([Ferriss #702](https://tim.blog/2023/11/02/morgan-housel-transcript/))。他的另外几条原则是：“假装每个词要花你 100 美元”，“人们记住的不是书，是句子”，“In summary”是最糟糕的结尾句【待核实】([How-I-Write-Skills](https://github.com/AlonMichael/How-I-Write-Skills/blob/main/catalog.md))。他在 Motley Fool 大约写了 3,500 篇文章，用这种方式完成学徒期；写《金钱心理学》时他发现自己的自然单位是博客长度，“每一章就是一篇长博客”【待核实】(同上)。

### Lenny Rachitsky：选题清单、狠删和“明天的提示”【待核实】

Lenny 的习惯包括：公开承诺，他说这提供了约一半的初始动力；保持可持续的节奏；保护深度工作时间；准备一个“点子倾倒场”，避免面对空白页；离开前在稿子顶部写一句接下来要做什么，这条他说来自 Perell【待核实】([X thread](https://x.com/lennysan/status/1347642510445711360))。编辑时他问“什么让我觉得有意思”，删掉一切非必要的字；据说删掉初稿的第一段，文章通常立刻变强（这句话没能定位到具体出处）【待核实】([Compound Planning](https://manual.compoundplanning.com/chapters/interview-with-lenny-rachitsky-writer-of-lennys-newsletter))。他每篇稿子改 10 到 30 遍【待核实】([Perell](https://twitter.com/david_perell/status/1717139432598319521))。

### Packy McCormick：先写一遍，再写一遍【待核实】

他的原话是：“I write the piece, and then I write the piece.” V0 草稿会被推翻，变成删稿垃圾场；他需要强烈的截稿压力，因此把发送日从周一挪到周二，有时在发布当天早上 4:30 到 8:55 重写整篇【待核实】([How-I-Write-Skills](https://github.com/AlonMichael/How-I-Write-Skills/blob/main/skills/format-adapt/SKILL.md))。妻子是他的第一读者，负责判断稿子有没有意思【待核实】([Bullet Point](https://bulletpointpodcast.com/howiwrite/packy-mc-cormick-a-tactical-masterclass-in-online-writing/))。在 X 上做推广时，一张“好条形图或一个惊人数据”比缩略图更有效【待核实】(How-I-Write-Skills distribute)。他发过一句被广泛引用的抱怨：Claude 编辑几乎给他的每份初稿都打 A-【待核实】([Packy on X](https://x.com/packyM/status/1821163105830769100))。

### Ted Gioia：永远诚实，先成为专家【待核实】

Gioia 的金律是“永远诚实”，并配有三个自查问题：公平吗？准确吗？能说服所有公正的观察者吗？【待核实】([Perell thread](https://x.com/david_perell/status/1795800774254985236))。治写作障碍，他转述过一个方法：藏起一本空白日记，连续一个月每天如实记下过去 24 小时发生的事，不加修饰【待核实】([Perell X](https://x.com/david_perell/status/1795893535717081570))。他说如果自己当初追求的是受众规模，几十年前就放弃了；动力要从写作本身找，“哪怕只有一个读者也有意义”【待核实】([Honest Broker](https://www.honest-broker.com/p/i-give-the-worst-writing-advice-in))。他还建议，在一两个领域里比别的写作者懂得更多，因为说服“只有在人们信任你时才有效”【待核实】([Athens](https://tryathens.com/blog/ted-gioia-writing-advice))。

### Henrik Karlsson：让想法在身体里住一年【待核实】

Karlsson 先收集“原始素材”，避免过早打磨文字；他说方法有用，但最好的材料来自打破方法【待核实】([How I write essays](https://www.henrikkarlsson.xyz/p/how-i-write-essays))。他让想法“在身体里住大约一年”，因为过早的批评会“压扁想法”；开头他放到最后写【待核实】([How I Write](https://howiwrite.substack.com/p/henrik-karlsson-the-writing-process))。Cal Newport 转述了他自己的数据：一篇文章多花一倍时间，平均带来四倍以上的新订阅【待核实】([Cal Newport](https://calnewport.com/on-slow-writing/))。关于声音，他说：“你身上古怪的东西才是有趣的东西”；大约写到第 50 篇，人才会对自己在做什么有感觉【待核实】([Substack note](https://substack.com/@henrikkarlsson/note/c-87287315))。

### Ben Thompson：第二篇文章最重要【待核实】

据第三方蒸馏的 How I Write 技能包，Thompson 说过三点：你写的最重要的文章，是读者读的第二篇；免费的头版文章“需要好钩子”，给付费读者的更新可以“默认读者知道得多得多”，这让他“心理上很自由”；日更截稿逼得他“每个分号都用到极致”。他还说，涵盖多个话题的更新需要“一条共同的线”【待核实】([How-I-Write-Skills](https://github.com/AlonMichael/How-I-Write-Skills/blob/main/skills/distribute/SKILL.md))。

### Sahil Bloom：从对话里写作，用推文框压缩【转录】

这部分依据 Perell 访谈的完整转录（2023-12-20）([YouTube](https://www.youtube.com/watch?v=f-s22uCixMw))。Bloom 写之前先把想法讲给人听，看哪里对方没听懂、露出困惑，他把这叫作“writing from conversation”。卡住时他会把内容压进推文的字数限制，“越来越短”。他引用“创意悬崖错觉”研究，认为最好的点子往往在“趟过泥泞”之后才出现；这篇论文本身研究团队没有核实。他找角度的方法是：拿一个已知的、有意思的想法，看它在自己生活里怎样应用、自己怎样挣扎过。他估计“95% 的爆款只是把已有的想法装进稍微更漂亮的包装”。他的用词检验是：你用这个词，是想让别人觉得你聪明，还是它真的给句子增加了效用？他还说，努力程度和最终效果之间的相关性“并不大”；与其为 TED 演讲这类话题追求 10 万触达，不如拥有 1 万个真正与你连接的人；“每一篇文章都是在召唤你想引入生活的那类人”。

### Alex Hormozi：一个大想法，证据先行【转录】

**Rule of One** 来自 Michael Masterson：在史上最好的 100 个 offer 里，有 91 个围绕单一概念，这个“大想法”必须好懂、好信、有趣或独特；所有子要点都只能强化这一个信息，“最难的是找出那一个想法”【转录】([OyGKFhTf0go](https://www.youtube.com/watch?v=OyGKFhTf0go))。91/100 这个数字是经他转述的，没有独立核实。他的开场公式是 **Proof → Promise → Plan**：先证明你懂行，再告诉观众能得到什么，最后交代接下来会发生什么；顺序可以调，商业受众头上始终挂着一个“凭什么听你的”的牌子【转录】([Jmkq5RLjm0U](https://www.youtube.com/watch?v=Jmkq5RLjm0U))。他总结过 40 个月的六个转变：从寓教于乐到教育，从“为我们”到“为你”，从宽到窄，从看播放量到看收入，从短视频到长视频，从“假设观众知道”到“什么都不假设”；包装要“从模糊到清楚”，并且明确反对“必须制造好奇缺口”的流行说法【转录】([HVOubeXUcx0](https://www.youtube.com/watch?v=HVOubeXUcx0))。给新手，他说别指望 90 天就爆，“第一年你都在找自己的声音”，要把行动本身当目标【转录】([7ITff1fIbSc](https://www.youtube.com/watch?v=7ITff1fIbSc))。他给《$100M Leads》测试书名时“毫无自我”：一个副标题版本以 71% 比 29% 胜出，样本量不明【转录】([yCcySsSkmjs](https://www.youtube.com/watch?v=yCcySsSkmjs))。

### Harry Dry：三个问题筛句子【转录】

这部分依据 Perell 访谈转录（2024-07-17）([YouTube](https://www.youtube.com/watch?v=TUMjnmfsPeM))。他的三个问题是：“能想象吗？能证伪吗？只有你能说吗？三个都是否，你大概写了一堆垃圾；三个都是是，你就抓到点东西了。”能想象，指具体胜过抽象。能证伪，指“把脑袋放上砧板”，他的说法是“你不能说，只能指”。只有你能说，来自 Jim Durfee 的“永远别写竞争对手也能签名的广告”。正面例子是 New Balance 的“伦敦超模和俄亥俄老爸都穿”，反面例子是“改变整个行业”，三项全不及格。他生成点子的方法是碰撞：找一组对立的东西，把它们撞在一起。

### The Cultural Tutor：只写当天让我“咆哮”的东西【转录】

这部分依据 Perell 访谈转录（2023-08-23）([YouTube](https://www.youtube.com/watch?v=1pBxikHRCXI))。Alexander Learmonth 说：“写一个想法的最好时机是它刚击中你的时候……今天让我咆哮的是什么？”他不攒稿、不定时：“不，不，不……我每天写。打开 Twitter，点发帖，开始写。”他的标准是：“每天写出一句好句子，就是好的一天。”他说：“说没时间写作，意思是你不想写。”Perell 在同一期补了一句：写作障碍最大的原因，其实是你没在写你该写的东西。

### Jack Butcher：一万次迭代【转录】

这部分依据 Perell 工作坊转录（2021-08-13，早于 2022 年）([YouTube](https://www.youtube.com/watch?v=EGnSx3EYEU0))。Butcher 认为做事的过程会产生大量“锯末”，可以直接拿来发布。他引用 Naval 的话：造就异类的不是 1 万小时，而是 1 万次迭代；“大多数人没有 20 年经验，只有 1 年经验重复了 20 次”。他 2010 年的博客没有读者，早期 Visualize Value 的帖子在 Facebook 上“零反响”，转到 Twitter 这个开放网络之后才扩散开。他找到的定位是“你有复杂的东西要解释，我帮你可视化”。

### David Perell：一页纸写作法与 CRIBS

Perell 的命名框架大多有逐字原文：Personal Monopoly；“别找细分领域，去创造一个”；Raymond Chandler Rule，即每 250 词让读者有一次顿悟；Expression Is Compression；“Consistency comes before choice”；“重写就是重想”；感叹号测试，即想用感叹号说明你的词不够生动，应该重写这句【原文已读】([perell.com](https://perell.com/note/the-raymond-chandler-rule/); [28 Pieces](https://perell.com/note/28-pieces-of-life-advice/))。第三方转录的 **Writing One-Sheet** 列了这些规则：短句；简单词，“酒吧里不会说的词就别写”；不用陈词滥调；先选定一个读者；页面顶部写下语境、要回答的问题和一句话答案，并“确保每句话都和顶部相关”；卡住时停笔，把想法讲出来再转写；编辑时换字体、换地方、朗读；反馈用 **CRIBS**，即 Confusing（困惑）、Repeated（重复）、Insightful（有洞见）、Boring（无聊）、Surprising（意外）【待核实】([joesmusings/quartz](https://github.com/joesmusings/quartz))。他的写作系统里还有一份“禁用词清单”【待核实】(同上)。2026 年他在访谈里说：“很多人想被听见，多过他们真有话要说”；他要的是“故事、例子和观点”；写不出来的原因之一是“没有勇气说出那些想法”；“受众永远是对的……能火的东西就是更好，当然有明显例外”【转录】([Nathan Barry Show](https://nathanbarry.com/how-to-stand-out-as-a-writer-in-the-age-of-ai-2026-138/))。他 2024 年 8 月宣布关停 Write of Passage，理由是“除了经济账，什么都值得庆祝”；2025 年 2 月又说，停止教学“部分是因为 AI 浪潮”【待核实】([X](https://x.com/david_perell/status/1825569243854962795); [X](https://x.com/david_perell/status/1894143267878703562))。

### Tim Denning：角度胜过新意，情绪是 AI 写不出来的【原文已读】为主

Denning 说：“我偶然学会的技能不是有新想法，而是从不寻常的视角攻击想法。”他还说：“在 AI 的世界里，你写不过 ChatGPT，所以你剩下的只有声音，和你脑子里那一库存的故事。”【原文已读】([timdenning.com](https://timdenning.com/tim-denning-is-rich/))。他的标题标准是让五年级学生也能看懂，并问“凭什么有人点”；他认为“发布了的内容”和“平台上真能被看到的内容”是两回事【原文已读】([16 Harsh Truths](https://timdenning.com/writing-harsh-truths/))。他先写标题和要点再起稿，写和改放在不同的日子【待核实】([timdenning.com](https://timdenning.com/never-run-out-of-ideas/))。2026 年他的说法是：“精致的东西会被遗忘，失控的东西永远不会被忘。”【原文已读】([Substack](https://timdenning.substack.com/p/not-being-unhinged-is-quietly-costing))。语料编者统计的风格数据显示，他的句子中位数约 9 个词，约 60% 的段落只有一行【待核实】([jpeslar1 corpus](https://github.com/jpeslar1/john-peslar-ai-skills))。

### Nat Eliason：太守规矩就像 AI 写的【待核实】

Eliason 说：“如果你太严格地遵守所有常规写作规则，你的文字听起来会像 AI 生成的。”他还说，“删副词”之类的建议没抓住要点，真正的要点是“展示而非告诉”；“一份烂草稿比一份没写完的草稿好得多”；编辑要放在尽量不同的场景里做【待核实】([nateliason.com](https://www.nateliason.com/blog/on-writing-better))。他的战术清单包括：缺细节的地方先写“TK”占位；删掉“我认为”“我相信”“似乎”；没有重要论点需要展开，就别写 8–10 句的长段落；长短句交替【待核实】([nateliason.com](https://www.nateliason.com/blog/better-writer))。他引用 Stephen King：初稿为自己写，重写为所有人写【待核实】([nateliason.com](https://www.nateliason.com/notes/writing-stephen-king))。

### 其他值得收进知识库的心法（简表）

| 创作者 | 心法 | 证据 |
|---|---|---|
| Sam Parr | “从很多地方偷，然后搅在一起……每个词都要有用”；用五年级阅读水平写作；不必思路清晰也能当好演讲者，但要当好作者必须思路清晰 | 【转录】([YouTube](https://www.youtube.com/watch?v=CO2ELWa3jsc)) |
| Naval / Eric Jorgenson | 压缩越精确，失去的读者越多；推文是压缩版，书和播客是“展开”版 | 【转录】([YouTube](https://www.youtube.com/watch?v=mWYMRCcYn-Q)) |
| Marc Andreessen | 杠铃式阅读：只读极新的和永恒的；带着“一点怒气”时写得最好 | 【转录】([YouTube](https://www.youtube.com/watch?v=tV6kDr1rwTs)) |
| Tyler Cowen | 不让 AI 替他写，“它像我的小宝宝”；别让 AI 抹平你的怪癖 | 【待核实】([How I Write](https://howiwrite.substack.com/p/tyler-cowen-will-ai-kill-writing)) |
| Shaan Puri | 故事 = 意图 + 阻碍 + 利害；“像说话一样写”；卡住就说出来再删 | 【待核实】([Recapio](https://recapio.com/digest/masterclass-in-storytelling-for-beginners-with-shaan-puri-by-david-perell)) |
| Dickie Bush | “抵制想显得聪明的冲动，力求清楚”；为一个具体的人解决一个具体问题 | 【待核实】([quotewise](https://quotewise.io/q/w8hnsw/)) |
| Nicolas Cole | 标题回答写什么、写给谁、承诺什么；“没有细分领域的作者是挨饿的艺术家” | 【待核实】([Medium](https://nicolascole77.medium.com/3-simple-ways-to-make-your-medium-headlines-irresistible-click-6a401cc0a02b)) |
| Justin Welsh | 先试一堆东西看什么有效；内容矩阵（据称已停用） | 【待核实】([Productive Insights](https://share.transistor.fm/s/82af7ab4)) |
| Darius Foroux | 不定字数目标，每天写一句也算；25–30 分钟计时、不改；“阅读养成品味，品味指导修改” | 【待核实】([dariusforoux.com](https://dariusforoux.com/daily-writing-habit/)) |
| Ali Abdaal | FBR（Fast, Bad, Wrong）初稿；搜集、起草、编辑三种模式分开 | 【待核实】([aliabdaal.com](https://aliabdaal.com/newsletter/the-acronym-that-changed-how-i-write/)) |
| Shannon Ashley | “不在于完美，在于诚实”；袒露多少由作者决定；不能天天写脆弱的内容 | 【待核实】([Medium](https://medium.com/@Shesreallyfat/my-rules-for-authentic-and-vulnerable-writing-364c0aeeb5ce)) |
| Zulie Rane | 20% 时间写不赚钱的东西（例如关机写小说）以防倦怠；Medium 是“载体不是终点” | 【待核实】([Zulie Writes](https://www.zuliewrites.com/blog/why-i-spend-20-of-my-writing-time-on-unprofitable-work)) |
| Sinem Günel | 理想读者画像“Jennifer”：背景、信念、目标、困难与恐惧 | 【待核实】([Write Build Scale](https://writebuildscale.substack.com/p/how-to-build-ideal-reader-persona)) |
| Benjamin Hardy / Ayodeji Awosika | 先搭结构再自由写；每天写 10 个标题；“采访过去的自己” | 【待核实】([Kickstarter](https://medium.com/the-kickstarter/how-to-write-like-a-1-medium-com-writer-ben-hardys-system-916dd720069b)) |
| George Mack | 在 Kindle 上读自己的稿子（换媒介检验） | 【待核实】（只有弱来源，未能取得链接原文） |

---

## 心法共识与分歧，以及哪些能交给机器

### 七条强共识

**第一，写作产生想法，不只是记录想法。** PG 说 80% 的想法在动笔后才出现【原文已读】([Writing, Briefly](https://paulgraham.com/writing44.html))；Koe 说“强制线性”【转录】；Perell 说“重写就是重想”【原文已读】。**第二，选题的过滤器是真实兴趣。** PG 说“你必须在乎”，Housel 主张自私写作，Lenny 选让自己兴奋的题，Cultural Tutor 写让自己“咆哮”的东西，Koe 问“我是否觉得重要”。**第三，删是核心技能。** PG 的“快刀斩”，Housel 的每词 100 美元，Bloom 的“拿不准就删”，Lenny 的删首段。**第四，清楚胜过聪明。** Bush、Cole、Hormozi 的“从模糊到清楚”、Bloom 的效用检验、PG 的“写得简单”都是这个意思。**第五，具体和证据是护城河。** Dry 的能想象、能证伪，Hormozi 的证据先行，Denning 的故事库，Medium 对“基于亲身经历”的偏好。**第六，量是学徒期，时间尺度是年。** Housel 写了 3,500 篇，Karlsson 说要写到约 50 篇，Butcher 说一万次迭代，Hormozi 说“第一年在找声音”。**第七，不是新意，是视角。** Denning 从不寻常的视角攻击想法，Bloom 认为 95% 是包装，Koe 主张借想法不借措辞，Perell 和 Koe 都说视角比细分领域重要。

### 六处真实分歧，以及怎样调和

| 分歧 | 一方 | 另一方 | 调和方式【设计建议】 |
|---|---|---|---|
| 为谁写 | Housel：别管读者，自私写作 | PG：过陌生人测试；为“破车载收音机”式的读者写 | 分阶段：选题可以自私，执行要对读者严格 |
| 起稿方式 | PG、Abdaal、Eliason、Foroux：先快后改 | Housel、Ashley：边写边改 | 由作者的自然单位决定：短篇可以边写边改，长篇综合稿需要多轮重写 |
| 节奏 | Welsh、Koe、Göke：批量、排期 | Cultural Tutor、Andreessen：当天的执念，当场写 | Agent 先问作者是“系统型”还是“执念型”，再选工作流 |
| 钩子 | Welsh 的标题（据报）偏开放式悬念 | Hormozi：从模糊到清楚，反对好奇缺口；Medium：标题要有足够语境 | 默认用清楚的承诺；悬念式标题当作 A/B 变体测试 |
| 病毒传播 | Perell：受众永远是对的，能火的就是更好 | Medium 官方：别追求爆款；Kuegler：“病毒垃圾” | 把爆款当信号而不是目标；负反馈和退订是红线 |
| 规则与声音 | Perell 的 One-Sheet、禁用词，规则很重 | Eliason、Denning：守规矩就像 AI，好文字会打破规则 | 规则检查只标记，不自动改；保留作者有意的破格 |

还有一处争议是孵化时长。Karlsson 让想法住一年，PG 说“几天”，Thompson 日更，Packy 周更且发布当天还在重写【待核实】。这说明“稿子好了没有”的判断，对有截稿的作者部分由时钟决定，对没有截稿的作者由“刺”和“饱足感”决定。

### 心法到 Agent 的映射：哪些写成清单，哪些必须留给人

| 心法 | 来源 | Agent 形态 | 归属 |
|---|---|---|---|
| 中立陌生人重读 | PG【原文已读】 | 只拿到终稿的干净语境评审者，逐条列出缺失前提、未限定的论断和跳跃 | Agent |
| 拔刺 | PG【原文已读】 | 多次采样通读，产出“摩擦热点”报告 | Agent 标记，人决定 |
| 有用性四因子 | PG【原文已读】 | 对每条论断打真实/重要/新颖/强度分，同时标出含糊的对冲和过度的断言 | Agent |
| 树搜索与快刀斩 | PG【原文已读】 | 提纲树视图；标出偏离初始问题的子树；把跑题内容移进尾注 | Agent 建议，人裁剪 |
| 防误读 | PG【原文已读】 | 扮演“聪明而善意的误读者” | Agent |
| 句子三问 | Dry【转录】 | 逐句打能想象/能证伪/只有你能说 | Agent |
| Rule of One | Hormozi【转录】 | 一句话写出大想法，检查每个小节是否都在强化它 | Agent |
| Proof → Promise → Plan | Hormozi【转录】 | 开头结构检查 | Agent |
| 效用还是炫耀 | Bloom【转录】 | 标出只为显得聪明的词 | Agent |
| 压缩到 280 字 / 展开 | Bloom、Jorgenson【转录】 | 论点压缩练习；为外行解释每个压缩过的术语 | Agent |
| CRIBS、顶部简报、每 250 词一次顿悟、感叹号测试、禁用词 | Perell【原文已读】/【待核实】 | 评审维度与 lint 规则 | Agent |
| 三个诚实问题 | Gioia【待核实】 | 公平、准确、能否说服公正者三问评分 | Agent 初评，人终审 |
| 每词 100 美元、不写“In summary”、删首段 | Housel、Lenny【待核实】 | 行级 lint | Agent |
| TK 占位、删对冲词 | Eliason【待核实】 | lint，并拦截含 TK 的稿件发布 | Agent |
| 五年级标题、凭什么点、写什么/给谁/承诺什么 | Denning【原文已读】、Cole【待核实】 | 标题评分 | Agent |
| 讲出来再写、采访过去的自己、写成给朋友的邮件 | PG【原文已读】、Awosika、Ferriss/Denning【待核实】 | 访谈模式：Agent 提问，人口述，Agent 转写 | 人出内容，Agent 出结构 |
| 异常值和旧爆款扫描 | Koe【转录】 | 抓取热门内容，拆解结构 | Agent |
| edge / 初始洞见 | PG：“没法系统地生成” | 只能列出候选“缝隙” | **人** |
| 真实兴趣、让我咆哮的东西 | PG、Cultural Tutor、Housel | 让作者给兴奋度打分 | **人** |
| 其他领域的深度、专家身份 | PG、Gioia | — | **人** |
| 亲身故事、第三方证明、真实数据 | Hormozi、Denning、Medium 政策 | Agent 只能从人提供的材料里取用，**绝不编造** | **人** |
| 袒露多少、情绪基调 | Ashley、Denning | — | **人** |
| 声音与怪癖 | Cowen、Karlsson、Eliason | 只做风格漂移监控 | **人** |
| 结尾的“饱足感” | PG | 可以提几个候选结尾 | **人** |
| 赌哪个想法、品味 | Perell、Koe、Foroux | 提供选项和数据 | **人** |

Hormozi、Denning 和 Medium 的政策，从三个方向指向同一个结论：**Agent 永远不能编造轶事、数字或“亲身经历”**。这一条在下文的所有闸口里都是一票否决项。

---
# 第三部分：可构建的多平台创作 Agent 手册

> 本部分除注明来源者外，均为【设计建议】。架构原则依据 Anthropic 的三篇工程文章【原文已读】，平台约束依据第一部分，质量闸口依据第二部分。

## 架构：一条核心流水线，加一层平台适配和多个发布模块

**先用工作流，不急着上自主 Agent。** Anthropic 区分了两种系统：**工作流**是 LLM 和工具按预定义的代码路径编排；**Agent** 是 LLM 在循环里根据环境反馈自己决定调用工具。它的建议是“找到最简单的方案，只在需要时增加复杂度”，并且先直接调用 LLM API，因为框架可能把提示词藏起来【原文已读】([Building effective agents](https://www.anthropic.com/engineering/building-effective-agents))。多 Agent 只适合宽度优先、可以并行的研究任务：Opus 4 主控配 Sonnet 4 子 Agent，在内部研究评测上比单 Agent 高 **90.2%**，代价是约 **15 倍**于普通对话的 token；而在“所有 Agent 必须共享同一语境”的任务上并不合适【原文已读】([multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system))。用同一种声音写作，正好属于后者。所以这套系统只在研究阶段并行，写作和编辑都交给单一写手完成，评审者从干净语境出发。

**新架构在原来的单平台流水线上加了三层。** 第一层是**平台适配层**：把一份母稿转成各平台原生的变体，每个变体是一条独立记录，有自己的闸口和指标。第二层是**按平台划分的发布模块**：每个平台按它实际能做到的程度，分成 API、排期工具、人工粘贴和人工 Import 四种能力等级，统一由人按下最后一键。第三层是**度量回流**：每个变体都带 UTM，按平台口径采集数据，再回写到知识库。

```
                         ┌──────────────── L0 知识库 / 记忆 ────────────────┐
                         │ voice/ · backlog/ · swipe/ · sources/ · archive/ │
                         │ platforms/*.yaml（平台规则配置，按月更新）        │
                         └──────────────────────────────────────────────────┘
 L1 核心流水线（平台无关，产出“母稿 hub”）
 S0 收件分拣 → S1 选题定角 ─H1→ S2 研究取证 ─H2→ S3 论点提纲 ─H3→
 S4 起草（模式A人写 / 模式B辅助 / 访谈模式）→ S5 编辑评审 ─H4（定稿·事实）→ hub
                                                                              │
 L2 平台适配层  S6：hub → variants[]                                           ▼
   ┌───────────────┬───────────────┬──────────────┬──────────────┬─────────────┐
   │substack_post  │substack_note×N│ x_post×N     │ x_thread     │ medium_story│
   │（母稿本体）    │               │ x_article    │              │（Import）   │
   └───────┬───────┴───────┬───────┴──────┬───────┴──────┬───────┴──────┬──────┘
           │ 各变体：平台闸口 G-SS / G-SN / G-XP / G-XT / G-XA / G-MD ─H5（批量审批）
 L3 发布模块 S7（每个平台按能力分级，统一 H6 人工按键）
   Substack：人工粘贴/发送；Notes 原生定时 | X：OAuth 按次付费 API 或排期工具
   Medium：旧 token 只建草稿，或人工 Import（自动 canonical）
           │
 L4 度量回流 S8：UTM 归因 → 各平台指标 → 月度复盘 ─H7（规则变更审批）→ L0
 旁路：R1 短养长（爆款短帖 → 晋升为长文选题）；R2 常青回收（间隔 ≥30–90 天）
```

**七个人工闸口。** H1 选定题目，并由作者给兴奋度打分。H2 确认研究简报。H3 批准论点和提纲。H4 定稿，逐条核对引语和数字。H5 批量审批各平台变体。H6 按下发布键，每个平台各按一次。H7 批准对声音档案、排序权重和平台规则的修改。用 LangGraph 实现的话，每个闸口就是一个 `interrupt()`：状态由 checkpointer 持久化，图会“无限期等待”，直到收到 `Command(resume=...)`；演示可以用 `InMemorySaver`，生产环境要换成 Postgres 或 SQLite【待核实】([LangGraph docs](https://docs.langchain.com/oss/python/langgraph/add-human-in-the-loop))。MVP 阶段可以完全不用框架：一个脚本，每个阶段把结果写进 markdown 文件，人改完文件再跑下一步。

**三个必须写进配置的开关。**

| 开关 | 选项 | 依据 | 默认 |
|---|---|---|---|
| `draft_mode` | A：人写核心论证，Agent 负责研究、编辑和改编；B：Agent 按批准过的提纲起草，人重写关键段；I：访谈模式，Agent 提问、人口述、Agent 转写整理 | Mollick 先写后问 AI【待核实】；PG“讲给别人听，再写下来”【原文已读】；Medium 付费墙只收人写的内容 | A（如果文章要进 Medium 付费墙，**只能**选 A 或 I） |
| `rhythm` | systems（周母题、批量、排期）或 obsession（当天执念、当场写） | Welsh、Koe 对 Cultural Tutor | 问作者 |
| `flow` | long→short（母稿拆分）、short→long（爆款晋升）、both | Koe、Welsh 对 Naval、Bush | both |

## 各阶段模块规格

### S0 收件分拣（一次路由调用，不设闸口）

输入包括 RSS 条目、Readwise Reader 存档、读者回复、语音备忘录转写、随手记、作者自己的爆款短帖（R1 回流）和他人的异常值内容。输出是给每条素材打标签，并路由到四个去向之一：选题池、资料库、swipe 库，或“立刻可写”。工具方面，RSS 用 feedparser；Readwise Reader API v3 是 `GET https://readwise.io/api/v3/list/`，请求头带 `Authorization: Token XXX`，游标分页，社区工具报告 LIST 接口限流每分钟 20 次【待核实】([Reader API](https://docs.readwise.io/reader/docs/api))。每周人工抽查一次路由准确率。

```text
[系统] 你是{作者}的收件分拣员。作者的固定视角：{lens}。
对每条输入只输出 JSON：{"route":"backlog|source|swipe|now","why":"≤20字",
"lens_fit":0-3,"is_outlier":bool,"tags":[...]}
规则：lens_fit=0 的一律 route=source；读者原话提问必须 route=backlog 并保留原文；
他人高表现内容 route=swipe，只记录结构、钩子类型和数据，不保存可直接复用的原句。
```

### S1 选题定角（并行生成 + 排序；闸口 H1）

输入是选题池候选、本周输入流、往期档案、读者投票，以及 swipe 库里的异常值（Koe 的做法）。输出是 3–5 个“题目 × 角度”方案。每个方案都要写清：edge（别人视为理所当然、作者却有疑问的点）、一句可以被反驳的论点、Rule of One 的大想法、4A 角度、为什么是现在、读者收益、需要哪些人类证据（亲身经历、数据、采访），以及和往期内容重复的风险。

| 排序维度 | 权重 | 依据 |
|---|---|---|
| 作者兴奋度（人工 1–5 分） | 0.30 | Lenny、PG、Cultural Tutor |
| edge 强度（人工确认） | 0.20 | PG |
| 视角契合度 | 0.15 | HCR、Koe“你就是细分领域” |
| 市场信号（读者提问、投票、异常值、自己旧帖的表现） | 0.15 | Yglesias、Koe |
| 可获得的人类证据或独家素材 | 0.15 | Hormozi、Newton |
| 时效 | 0.05 | 日更作者 |

```text
[系统] 为{作者}生成选题角度。视角：{lens}。读者画像：{persona}。
往期相似题目（禁止重复其论点）：{archive_hits}。参考的异常值结构：{outlier_patterns}
（只借结构与包装类型，禁止借措辞）。
对「{idea}」给出 {N} 个互不相同的角度，每个包含：
edge（列出一个“人们视为理所当然、但值得怀疑”的前提）/ thesis（一句可证伪的论点）/
one_big_idea（易懂、易信、独特）/ angle_4a / why_now / reader_payoff /
human_evidence_needed（需要作者提供的亲身经历、数据或采访）/ risk。
不得编造任何事实或经历；不确定的地方写“[需作者确认]”。
```

H1 的规则：作者必须亲手填写兴奋度，并用一句话写下自己的 edge。**写不出 edge 的题目退回选题池。**这一条就是 PG 的“没有 edge 就别动笔”。

### S2 研究取证（编排者-工作者；闸口 H2）

这是唯一使用多 Agent 的阶段。主控把问题拆成子问题，每个子 Agent 都要拿到明确的目标、输出格式、工具和信源指引以及边界，否则会重复劳动。研究遵循“先广后窄”：简单的事实查找用 1 个 Agent、3–10 次工具调用。研究完成后由单独的引用 Agent 把每条结论绑定到来源。Anthropic 的人工测试发现，Agent 偏爱 SEO 内容农场，需要在提示词里加入信源质量启发式【原文已读】([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system))。子 Agent 只返回“浓缩、提炼”的摘要，原文以路径保存，用的时候再加载【原文已读】([context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents))。另外增加一个**人类素材子任务**：从作者的会议转录、语音备忘录、旧日记里挑出“有意思的时刻”（Hormozi 的做法），交给作者确认。

```text
[子Agent任务书]
目标：回答「{sub_question}」，服务于论点「{thesis}」。
输出：最多 8 条 finding：{claim, quote_verbatim, url, source_type: primary|secondary|aggregator,
read_level: full_text|snippet, date, confidence}，外加 counter_evidence。
信源优先级：作者原文/官方数据/同行评审 > 权威媒体 > 聚合站；聚合站或 snippet 不得单独支撑数字。
找不到就写“未找到证据”。边界：不写文章，最多 {k} 次工具调用。
```

H2 检查清单：每个数字至少有 1 个一手来源，高风险事实要有 3 个独立来源（HCR 规则）；引语能在原文里逐字找到；至少列出 1 条反方证据；列出需要人去补的采访或数据；`read_level=snippet` 的来源不能单独支撑结论。

### S3 论点与提纲（链式；闸口 H3）

输出分三块。第一块是 Perell 式的**页顶简报**：语境、要回答的问题、一句话答案。第二块是逐段提纲，每段注明 `source_id` 或标为“观点段”（Doomberg 式的一段一句摘要）。第三块是提纲树，按 PG 的方法标出每个分支的普遍性和新颖性，以及偏离初始问题的子树。另附一个“核心画面”或图表设想，供推广使用（Packy 的做法）。程序检查有四项：论点必须可证伪；每节都要服务于 one_big_idea；每段要有来源，或者被标为观点；每约 250 词至少规划一个顿悟点（Chandler Rule）。

### S4 起草（三种模式）

**模式 A（默认）**：Agent 不写正文，只提供提纲、素材卡片和“明天从这里开始”的提示（Lenny 的做法）。**模式 I（访谈）**：Agent 按提纲逐节提问，作者口述，Agent 整理成稿，**只调整顺序和删冗，不添加内容**。这对应 PG 的“讲给别人听”和 Perell 的“说出来再转写”。**模式 B**：由单一写手 Agent 起草，一次装入声音档案、5–15 段范文、提纲和研究简报。

```text
[系统·模式B] 你在为{作者}起草，不是替他发表。严格遵守 voice_profile 与 never_list。
范文（只学节奏与手法，禁止复用句子）：{exemplars}
页顶简报（每句都必须与之相关）：{top_of_page}
事实只能来自研究简报，每个事实后标 [source_id]；缺来源的地方写 [TK: 需作者补充]。
亲身经历、数字、对话一律不得生成，留 [TK: 作者经历]。
立场只能用 stances.md 中已有的；没有的写 [TK: 作者确认立场]。
先写最重要的一句话（PG：deadline 下先说最重要的句子）。
```

含有 `TK` 的稿件在 S5 会被**硬拦截**（Eliason 的做法）。

### S5 编辑评审（评审-优化循环，干净语境；闸口 H4）

评审 Agent 不继承写手的对话历史，只读终稿、页顶简报、声音档案和评分标准。Anthropic 认为评审-优化模式适用于“评估标准清晰”的场景；它的实践是用单次调用打 0.0–1.0 分，再加通过/不通过，这样与人工判断最一致【原文已读】([Anthropic](https://www.anthropic.com/engineering/building-effective-agents); [multi-agent](https://www.anthropic.com/engineering/multi-agent-research-system))。评审分成五组并行跑，结果汇总成一份报告。

| 组 | 检查项 | 方法 | 不通过阈值 |
|---|---|---|---|
| 理解 | **陌生人重读**（PG） | 无背景的评审者复述论点，列出缺失前提和跳跃 | 复述和页顶答案不一致；或者有任何未解释的前提 |
| 理解 | 防误读（PG） | “聪明而善意的误读者”列出 3 种可能的误读 | 误读在正文里没被堵住 |
| 论证 | **有用性四因子**（PG） | 对每条核心论断打真实/重要/新颖/强度分 | 任一核心论断的“真实”分低于 1；或过度断言 |
| 论证 | **Gioia 三问** | 公平？准确？能说服所有公正的观察者？ | 任一项为否 |
| 论证 | Rule of One / 树剪枝 | 每节和大想法的相关度；标出跑题子树 | 有节与大想法无关，又没移进尾注 |
| 句子 | **Dry 三问** | 抽检核心句：能想象、能证伪、只有你能说 | 核心句三项全否 |
| 句子 | 效用还是炫耀（Bloom）、清楚还是聪明（Bush） | 标出为显得聪明而用的词 | 只标记，不拦截 |
| 句子 | 行级 lint | 禁用词、对冲词（“我认为”）、感叹号、“In summary”式结尾、超长段落、句长方差、AI 腔词表 | AI 腔每千字超过 3 次；结尾是总结段 |
| 读者 | **CRIBS**（Perell） | 按段标注 Confusing / Repeated / Insightful / Boring / Surprising | C 或 B 段占比超过 15% |
| 读者 | 每 250 词一次顿悟 | 标出连续 500 词以上没有新信息的区段 | 只标记 |
| 读者 | **拔刺**（PG） | 3 次独立采样通读，交叉出现的摩擦点进报告 | 有未处理的刺（由人决定） |
| 事实 | 逐条核查（SAFE 式） | 拆出可核查论断 → 重新打开来源 → 确认原文里确实有 | 引语或数字的支撑率低于 100% |
| 事实 | 原创性 | 和来源、往期文章做 n-gram 重叠检测 | 连续 8 个词以上重叠且未加引号 |
| 声音 | 风格漂移 | 句长分布、功能词频，和档案比较的距离 | 超出往期均值 2σ |

事实核查借用 Google 的 SAFE：先把长文拆成单条事实，再逐条用搜索验证。SAFE 和人工标注的一致率为 **72%**，成本低 20 倍以上【待核实】([arXiv 2403.18802](https://arxiv.org/abs/2403.18802v3))。72% 意味着它只能做初筛。**评审需要校准**：Packy 抱怨过 Claude 几乎给每份初稿打 A-【待核实】([Packy on X](https://x.com/packyM/status/1821163105830769100))，所以每个评审提示词都要附 2 篇作者认定的“差”稿和 2 篇“好”稿作为锚点，每个扣分点都要求引用原句。**lint 只标记、不自动改**：Eliason 和 Denning 都提醒过，完全守规矩的文字读起来像 AI；作者可以在 `voice/deliberate_breaks.md` 里登记自己有意的破格，lint 会跳过这些。

```text
[系统·陌生人评审] 你是一位聪明、善意、对作者一无所知的读者。你只看到下面这篇文章。
1) 用一句话复述它的核心主张；2) 列出你读到时缺少的每一个前提（引用原句）；
3) 列出每一处“为什么突然说这个”的跳跃；4) 列出你最可能产生的 3 种误读。
不要评价文采，不要给总分，不要提出新论点。
[系统·拔刺] 慢读全文。只标出让你“卡一下”的句子：别扭、含糊、可能不真、读来乏味。
每条给出原句、卡住的原因（≤15字）。不要改写。
```

H4 的人工核对清单：每条引语逐字回到原链接；每个数字回到一手来源；每段亲身经历由作者确认确实发生过；涉及真实人物的负面陈述再查一遍；全文由作者朗读一遍（PG、Orlean），或换一种媒介读（换字体、换设备）；**结尾由作者本人拍板**。

### S6 平台适配层：一份母稿，多个原生变体（闸口 H5）

适配层的输入是定稿 hub 和 `platforms/*.yaml` 里的平台规则，输出是一组 `variant` 记录（结构见数据部分）。每类变体有自己的生成提示词和闸口。原则只有一条，就是 Denning 说的“像学一门语言”：**改写，不要转贴**。

| 变体 | 生成规则 | 依据 |
|---|---|---|
| `substack_post`（母稿本体） | 2–4 个标题候选，用于原生 A/B 测试（小列表只测 2–3 个）；副标题；付费墙位置；页脚放推荐和转介绍；文末一行 AI 使用披露 | Substack 功能【待核实】 |
| `substack_note` ×3–10 | 金句、图表、反直觉断言、提问；目标是拉免费订阅，不是卖付费 | 0.70% 研究；Koe 把推文同步到 Notes |
| `x_post` ×3–7（散布在一周里） | 每条一个自足的想法，用 Bloom 的压缩练习，过 Dry 三问；根帖不放链接；每条都设计一个能引发回复的点 | 回复权重 5.0；作者多样性衰减 |
| `x_thread` ×0–1 | 首帖要能单独成立（故事、框架或承诺），中间每帖一个要点，末帖回扣钩子并放 CTA；长度不设死规则 | DedupConversationFilter；Cole |
| `x_article` ×0–1 | 母稿的完整版或精简版；开头按 Proof → Promise → Plan 重写；不设付费墙的语境 | Koe 的做法；Articles 已对 Premium 开放 |
| `medium_story` ×0–1 | 默认用 Import 从母稿 URL 导入；另写 Medium 专用的标题、副标题和封面图说明，回答写什么、给谁、承诺什么；结尾加 newsletter CTA；只有人写的稿子才能设付费墙 | Medium 的 Boost 和 AI 政策 |

```text
[系统·X 单帖改编] 从母稿中挑出 {n} 个可以独立成立的想法。每条：
≤280 字符（或作者 Premium 长帖上限 {limit}）；一个想法；开头一句就给出具体的东西（数字、画面、反常识）；
过三问（能想象/能证伪/只有作者能说）；不加链接、不加 hashtag；
结尾留一个读者能回答的具体问题或可反驳的断言（目标：回复，而非点赞）。
禁止新增母稿中没有的事实或经历。输出 JSON 数组并给每条打三问分。
[系统·Medium 包装] 为 Import 后的文章写：title（五年级学生能懂；回答写什么/给谁/承诺什么）、
subtitle（补足语境，不制造悬念缺口）、cover_alt（图像说明与 ALT 文本）、
cta（一句指向 newsletter 的话，带 UTM）。不改正文。
```

### S7 发布模块：每个平台按能力分级（闸口 H6）

| 平台 / 体裁 | 能力等级 | 推荐实现 | 禁止做法 |
|---|---|---|---|
| Substack 长文 | 人工粘贴 | Agent 输出可直接粘贴的 HTML/markdown 和发送前清单；人粘贴、选标题测试、按发送 | 默认不用 cookie 型非官方 API；如果作者明确选择开启，也**只建草稿** |
| Substack Notes | 原生定时 / 排期工具 | 人在 Substack 里定时（2026 年 4 月起据报支持）；或用 Typefully（据报支持发 Notes）【待核实】 | 批量刷屏 |
| X 单帖 / Thread | API（按次付费）或排期工具 | 用作者本人的 OAuth 2.0 用户 token；Agent 排好队列，人逐条或按批批准；帖子之间间隔数小时 | 自动点赞、自动关注、自动 @、AI 自动回复（需要书面批准）、浏览器自动化 |
| X Articles | 排期工具 / 人工 | Typefully 据报支持发 Articles【待核实】；否则人工粘贴；官方 API 是否支持 Articles **未找到证据** | — |
| Medium | 人工 Import / 旧 token 建草稿 | 母稿发出 1–7 天后，人用 Import a story 导入（自动加 canonical）；有 2025 年前的旧 token 的，用 API 以 `publishStatus: draft` 加 `canonicalUrl` 建草稿，人在界面里补标签、选出版物、决定付费墙后再发布 | 无头浏览器自动发布；未披露的 AI 文字 |

发布模块在每次执行前都要读一遍 `platforms/*.yaml`，检查政策版本。如果某条规则的 `verified_at` 超过 90 天，就提醒作者重新核对一次【设计建议】。

### S8 复盘学习（闸口 H7）

S8 每天拉取一次 X 自有帖子的指标（只读本账号近期的帖子，以控制读取费用），每周人工导出 Substack 的 CSV，每周人工记录 Medium 的统计（Medium 没有统计 API，RSS 只能用来确认文章已发布）。每月生成一份复盘，内容包括：表现前 20% 变体的共同特征（按平台分别统计）、`edit_diffs` 里反复出现的修改、R1 候选（互动显著高于基线的短帖，建议晋升为长文选题）、R2 候选（发布 90 天以上的常青内容，可以重新改写发布），以及排序权重和平台规则的修改提议。全部由人批准（H7）后才写回知识库。

---
## 各平台的质量闸口清单

所有变体都要先过**通用底线 G0**：无 TK；没有任何编造的事实、经历或数字；引语逐字可查；不含他人的原句（Koe 的界线是借想法、不借措辞）；AI 参与程度已记录在案；发布账号就是作者本人。在此之上，每个平台再加自己的检查项。

**G-SS · Substack 长文**

| 检查项 | 标准 | 依据 |
|---|---|---|
| 页顶答案 | 文章开头 3 段内出现一句话答案，或者明确的承诺 | Perell；Thompson 说免费稿需要钩子 |
| 首段 | 测试删掉第一段：删了以后不影响理解，就删 | Lenny【待核实】 |
| 免费/付费分层 | 免费部分本身完整；付费墙落在自然的停顿处 | Thompson；Substack 文中付费墙 |
| 第二篇 | 文中至少链接 1 篇最相关的旧文 | Thompson 的“第二篇文章” |
| 画面 | 至少有一张核心图表或一个核心画面，可以拿去做推广 | Packy |
| 标题测试 | 2–3 个变体；看“打开者点击率”，不只看打开率 | Substack A/B；邮箱会隐藏打开行为 |
| 结尾 | 不是总结段；由作者拍板 | Housel；PG |
| 披露 | 文末一行 AI 使用说明 | Reuters 信任数据【待核实】 |

**G-SN · Substack Notes**

| 检查项 | 标准 |
|---|---|
| 自足 | 不点开原文也能拿到一个完整的想法 |
| 目标 | 以拉免费订阅为目标（0.70% 研究），不硬推付费 |
| 密度 | 每周 3–10 条，同一天内不连发 |
| 互动 | 作者本人在 Notes 里回复和评论（Kuegler 每天 30 分钟） |

**G-XP · X 单帖**

| 检查项 | 标准 | 依据 |
|---|---|---|
| 一个想法 | 只有一个可以复述的想法 | Rule of One |
| 句子三问 | 至少 2 项为是 | Dry |
| 首行 | 第一行就给出具体内容：数字、画面或反常识 | Hormozi 的“从模糊到清楚” |
| 回复设计 | 有一个读者能接话的点（可以被反驳的断言、具体的提问） | 回复权重 5.0 |
| 负反馈风险 | 不蹭无关热点，不 @ 陌生人，不重复发同样的内容 | 举报 −234，静音 −58.8；反垃圾引擎 |
| 链接 | 根帖默认不放链接；放与不放作为 A/B 记录 | `open_link` 权重 0.2；API 含 URL 每条 $0.20 |
| 原创 | 不是他人作品的改写（Original Content Rewards 只算原创） | X 帮助页【待核实】 |
| 间隔 | 和本账号上一条帖子至少隔 2–3 小时 | 作者多样性衰减【设计建议】 |

**G-XT · X Thread**

| 检查项 | 标准 |
|---|---|
| 首帖独立 | 只看首帖也有价值，并能引发回复（同一会话会被合并显示，首帖承载分发） |
| 每帖一个要点 | 每条都能单独截图转发 |
| 末帖 | 回扣首帖的钩子，加 CTA；链接放在末帖或作者的自回复里 |
| 长度 | 不设硬性条数；“7–12 条”只是第三方的说法【待核实】 |
| 在场 | 发布后 1–2 小时内作者本人在线回复（冷启动窗口 2 小时） |

**G-XA · X Articles**

| 检查项 | 标准 |
|---|---|
| 开头 | 按 Proof → Promise → Plan 重写，不假设读者认识作者（Hormozi 的“什么都不假设”） |
| 推广帖 | 配一条能独立成立的推广单帖，不只贴文章卡片 |
| 原创 | 是作者自己的母稿，不是汇编 |

**G-MD · Medium 文章**

| 检查项 | 标准 | 依据 |
|---|---|---|
| 人写 | 设付费墙的稿子必须是 `draft_mode` A 或 I；B 模式的稿子不设付费墙，并且要披露 | Medium AI 政策 |
| 包装语境 | 标题、副标题、封面图三者合起来能说清楚“写什么、给谁、承诺什么” | 官方 Boost 要求；Cole |
| 标题 | 五年级学生能懂，能回答“凭什么点” | Denning |
| 经历 | 有基于作者亲身经历或专业知识的部分 | Distribution Guidelines |
| 工艺 | 没有错别字，来源恰当，图片有 ALT 和署名 | 同上 |
| canonical | Import 之后核对 canonical 指向母稿 URL | Help: canonical |
| CTA | 文末有带 UTM 的 newsletter 链接（Medium 关注者不是你的邮件列表） | 平台机制 |
| 翻译稿 | 转载自己的翻译版不能获得 Boost，要预期较低的分发 | Distribution Guidelines【待核实】 |
| 标签 | 最多 5 个；不要指望靠标签获得策展（Medium 员工称“策展人看不到标签”） | Zulie @ Medium【待核实】 |

---

## 跨平台内容流：母站、canonical、链接和 UTM

**拓扑：Substack（或自有域名）当母站，其余平台当辐条。** 选它当母站有三个原因：Substack 不能把 canonical 指向别处，所以它只能当原文；邮件列表是作者唯一真正拥有的受众资产；Medium 的 Import 工具会自动把 canonical 指回原文。有自有域名的作者，优先用自有域名的 URL 当 canonical，并把 X 上的链接也换成自有域名。2023 年 4 月，X 曾短暂限制带 substack.com 链接的推文，自定义域名不受影响【待核实】([Engadget](https://www.engadget.com/twitter-stops-throttling-tweets-with-substack-links-171858782.html))。这只是一次历史事件，但它说明了把链接域名掌握在自己手里的价值。

**一周的标准节奏（周更型，`rhythm: systems`）：**

| 时间 | 动作 | 渠道 |
|---|---|---|
| D-7 至 D-1 | X 单帖试水本周母题的 2–3 个分论点；记录各自的回复率 | X（短养长） |
| D0 上午 | 母稿发送（邮件 + 网页） | Substack |
| D0 当天 | 第一条 Note（核心金句或图表）；第一条 X 单帖（最强的一个想法，不带链接）；作者在线 1–2 小时 | Notes、X |
| D1–D6 | 每天 1–2 条 X 单帖和 1 条 Note，从母稿里挖；视情况发 1 条 Thread 或 X Article | X、Notes |
| D1–D7 | 人工 Import 到 Medium；核对 canonical；补包装 | Medium |
| D7 | 采集 7 日指标；S8 打标签 | 全部 |
| D+90 起 | 常青内容进入 R2 回收池（间隔 ≥30–90 天，参照 Welsh / Hypefury） | X、Notes |

执念型作者（`rhythm: obsession`）的流向反过来：当天在 X 上写下让自己“咆哮”的东西；Agent 在后台把它记进选题池；当周表现最好的那条，晋升为周末长文的选题（R1）。

**X 链接处理的决策树。** 第一步，根帖默认不带链接，内容要完整到不点链接也能获得价值；链接放在末帖、自回复或个人主页。这样做一是因为 `open_link` 权重只有 0.2，用户离站还会损失停留时长【原文已读】；二是因为 API 发含 URL 的帖子据报每条 $0.20，而普通帖只要 $0.015【待核实】。第二步，2026 年官方已表示不再惩罚链接【待核实】，所以每月拿 10% 的帖子做“正文带链接”和“回复带链接”的对照，按 UTM 点击数和曝光量来判断，不靠传言。第三步，自回复里的 URL 是否同样按 $0.20 计费，研究团队**未找到证据**，成本模型要按最坏情况估算。第四步，不要设置“互动过阈值就自动插入推广回复”这类自动化。Hypefury 的 Auto-plug 是现成产品，但 Hypefury 自己也提醒过，激进的自动私信会触发 X 的反垃圾过滤【待核实】([Hypefury](https://hypefury.com/llm-info))，而且 AI 自动回复需要 X 的批准。

**Canonical 规则。**

| 情形 | 做法 |
|---|---|
| Substack → Medium | 母稿发布后 1–7 天，人工用 Import a story 导入（会回溯日期并自动设 canonical）；导入后在设置里核对“Customize canonical link” |
| 手动粘贴到 Medium | 必须手动设置 canonical；否则就是重复内容，而且 Google 可能先收录 Medium 版本【待核实】([byburk](https://blog.byburk.net/how-to-cross-post-without-hurting-your-seo)) |
| 旧 token 走 API | 发帖时带 `canonicalUrl`，并设 `publishStatus: draft`【原文已读】 |
| X Articles | 没有 canonical 机制；可以发全文（Koe 的做法），也可以发精简版并链回母稿；搜索引擎层面的影响**未找到证据** |
| Import 失败 | 降级为手动粘贴加手动设 canonical；记录失败原因 |

**UTM 规范。** Substack 的“订阅来源”报表能否直接显示 UTM 值，研究团队未能确认【未找到证据】，所以 UTM 主要用于点击归因，最好配合自有域名上的 GA4。X 和 LinkedIn 的应用内浏览器和短链可能会丢掉 referrer，这时只能靠 UTM 归因【待核实】([Narrareach](https://www.narrareach.com/blog/substack-traffic-sources-explained))。

```text
utm_source   = x | substack_notes | medium | linkedin | threads
utm_medium   = post | thread_end | self_reply | article_footer | story_cta | profile
utm_campaign = <hub_slug>              # 例：2026w45-user-interviews
utm_content  = <variant_id>            # 例：v_x_post_03
示例：https://letters.example.com/p/user-interviews?utm_source=x&utm_medium=self_reply&utm_campaign=2026w45-user-interviews&utm_content=v_x_post_03
```

---

## 知识库与记忆：一个 markdown 仓库，外加平台规则配置

在 newsletter 这个规模，几百篇往期文章完全可以让 Agent 用 grep 或 glob 按需检索，暂时用不着向量数据库。这符合 Anthropic“按需检索、以文件路径保存引用”的建议【原文已读】([context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents))，不过这一点没有实测过【设计建议】。

```
creator-vault/
├── voice/
│   ├── profile.yaml            # 声音档案（结构化，含各平台差异）
│   ├── exemplars/              # 5–15 段范文，按开头/转折/论证/吐槽/结尾分类，按平台分文件夹
│   ├── never.md                # 禁用词与禁用结构（含中文 AI 腔词表，需自建）
│   ├── deliberate_breaks.md    # 作者有意的破格，lint 时跳过
│   ├── stances.md              # 已表态的立场
│   ├── stories.md              # 作者亲口确认过的经历库（Denning 的“故事库”），每条带日期和可公开程度
│   └── edit_diffs/             # AI 稿 → 终稿的修改对
├── backlog/ideas.jsonl         # 选题池（含 edge、兴奋度、市场信号）
├── swipe/                      # 他人佳作：只存结构、钩子类型、指标与链接，不存可复用原句
├── sources/                    # 每个来源一个 md：逐字摘录、read_level、证据等级
├── hubs/{hub_id}/              # 每篇母稿：brief / outline / draft / eval / final
├── variants/{variant_id}.json  # 各平台变体及其发布结果、指标
├── platforms/                  # substack.yaml / x.yaml / medium.yaml：平台规则与政策版本
├── metrics/exports/            # Substack CSV、Medium 手工记录、X API 拉取
└── runs/logs/                  # 每次运行的提示词、模型、成本
```

`stories.md` 是这次新加的关键文件。Hormozi、Denning 和 Medium 的政策都指向同一个结论：**亲身证据只能来自人**。Agent 想引用作者的经历时，只能从这个文件里取，而且每条都必须标明 `consent`，也就是这件事可以公开到什么程度（Ashley 说过，“袒露多少”由作者决定）。

## 数据结构

```yaml
# voice/profile.yaml
author: "示例作者"
identity: "前产品经理，写给 0→1 阶段的产品负责人"
lens: "每个话题都回到：这对一个 5 人团队本周的决策意味着什么"
persona_ref: personas/jennifer.yaml          # Günel 式读者画像
rhythm: systems                              # systems | obsession
default_draft_mode: A                        # A | B | I
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
  medium:   {subtitle_required: true, tone: "更完整的语境，假设读者不认识我"}
disclosure_line: "研究与校对由 AI 辅助；观点、经历与文字出自我本人。"
```

```json
// backlog/ideas.jsonl —— 每行一条
{"id":"idea_0142","created":"2026-10-28","origin":"reader_reply|x_outlier|own_post|memo",
 "raw":"读者原话：小团队要不要做用户访谈？",
 "edge":"大家默认访谈要按项目做；我怀疑固定节奏才是关键",
 "angle_4a":"actionable","lens_fit":3,"excitement":null,
 "market_signals":{"reader_questions":4,"votes":0,"own_x_post":{"id":"18…","reply_rate":0.021},
                   "outlier_refs":["swipe_0311"]},
 "human_evidence":["stories#s_017","可约 2 位创始人访谈"],
 "status":"candidate","related_hubs":["hub_0031"]}
```

```json
// hubs/hub_0045/meta.json —— 母稿
{"id":"hub_0045","slug":"2026w45-user-interviews","canonical_url":"https://letters.example.com/p/user-interviews",
 "top_of_page":{"context":"…","questions":["…"],"answer":"小团队的用户访谈应该按周固定，而不是按项目"},
 "one_big_idea":"固定节奏胜过按需访谈","draft_mode":"A","word_count":2300,
 "sources":["src_0871","src_0874"],"stories_used":["s_017"],
 "gates":{"H4":{"approved_by":"author","at":"2026-11-02T07:50","quotes_checked":6,"numbers_checked":4}},
 "status":"final"}
```

**平台变体 schema**（用户要求的核心结构）：

```yaml
# variants/v_x_post_03.yaml
variant_id: v_x_post_03
hub_id: hub_0045
platform: x                      # substack | substack_notes | x | medium
format: x_post                   # substack_post | substack_note | x_post | x_thread | x_article | medium_story
derivation: atomize              # atomize(长拆短) | promote(短养长) | recycle(回收) | native(原生)
parent_variant: null             # recycle 时指向旧变体
status: approved                 # draft | gated | approved | scheduled | published | failed | retired
body:
  text: "我访谈了 40 个小团队。按项目做访谈的，三个月后几乎都停了。…你们团队是按周还是按项目？"
  parts: []                      # thread / article 分段
  char_count: 212
  media: [{type: image, path: "assets/chart_0045.png", alt: "按周 vs 按项目的访谈坚持率"}]
packaging:
  title: null                    # medium / substack / article 用
  subtitle: null
  title_variants: []
link_policy:
  placement: none                # none | inline | thread_end | self_reply | footer | profile
  url: "https://letters.example.com/p/user-interviews"
  utm: {source: x, medium: self_reply, campaign: 2026w45-user-interviews, content: v_x_post_03}
canonical:
  url: "https://letters.example.com/p/user-interviews"
  method: n/a                    # medium_import | api_canonicalUrl | manual_setting | n/a
compliance:
  ai_assist_level: edit_only     # none | edit_only | outline | draft_B
  disclosure_required: false
  paywall: false                 # medium/substack；若 ai_assist_level=draft_B 则必须 false（Medium）
  originality_check: pass        # 非他人作品改写
  automation_label_required: false
schedule:
  planned_at: "2026-11-03T09:20+08:00"
  min_gap_hours_same_account: 3
  author_online_window_min: 90
gate_results:
  gate: G-XP
  checks: {one_idea: pass, dry_tests: "2/3", first_line_concrete: pass, reply_hook: pass,
           negative_risk: low, link_root: none}
  judge_score: 0.78
  human_approved_by: author
  approved_at: "2026-11-02T21:10+08:00"
publish_result:
  channel: x_api_pay_per_use     # x_api | typefully | substack_manual | medium_import | medium_api_draft
  platform_post_id: "1985…"
  url: "https://x.com/…/status/1985…"
  cost_usd: 0.015
  published_at: "2026-11-03T09:21+08:00"
metrics_ref: metrics/v_x_post_03.jsonl
```

```yaml
# platforms/medium.yaml —— 平台规则配置（规则多变，必须可以热更新）
platform: medium
policy_version: "2026-11"
verified_at: "2026-11-03"
verification_level: snippet      # full_text | snippet：本手册所有 Medium 规则均为摘要级
rules:
  ai_paywall_allowed: false
  ai_undisclosed_distribution: network_only
  ai_disclosed_boost_eligible: false
  boost_self_nomination_per_month: 2      # 仅限身为提名人的作者
  boost_max_story_age_days: 180
  max_tags: 5                             # 历史值，未核实
  read_counts_after_seconds: 30
  payout_extra: {external_traffic_pct: 5, search_traffic_pct: 15}
api:
  supported: false
  new_tokens: false                       # 据厂商文档，2025-01-01 起
  legacy_endpoint: "POST /v1/users/{authorId}/posts"
  fields: [title, contentFormat, content, canonicalUrl, tags, publishStatus]
publish_default: human_import
```

```json
// metrics/v_x_post_03.jsonl —— 指标快照（每行一个时间点）
{"variant_id":"v_x_post_03","t":"+2h","impressions":1840,"replies":22,"reposts":6,"quotes":3,
 "likes":61,"bookmarks":14,"profile_visits":38,"follows":5,"link_clicks_utm":0,"source":"x_api"}
```

```json
// hubs/hub_0045/eval.json —— 评审结果
{"pass":false,"scores":{"stranger":0.7,"usefulness":0.8,"gioia":1,"dry_core":0.67,"cribs_cb_ratio":0.18,
 "support_rate":0.92,"originality":1,"voice_drift_sigma":1.1,"ai_tells_per_1k":2.4},
 "blocking":[{"check":"support_rate","sentence":"……坚持率高 3 倍","fix":"补一手来源或删除"},
             {"check":"cribs","para":7,"label":"Boring","note":"与第 4 段重复"}],
 "briars":[{"sentence":"……","reason":"含糊","hits":3}],
 "anchored_to":["hub_0012(bad)","hub_0031(good)"]}
```

---
## 平台工具现实：哪些能自动化，哪些必须由人点

**Substack：只能读，不能写。** 官方没有发文、草稿或订阅者 API。官方 Developer API 只能查公开的创作者资料，需要申请，并接受 2026 年 1 月 8 日更新的 API 条款【待核实】([Substack API ToS](https://substack.com/api-tos))。只有单一来源称存在一个仅限 Bestseller 刊物的官方只读 MCP 端点，和“CEO 称即将推出”的说法互相矛盾【待核实】([smtpedia](https://smtpedia.com/platforms/substack/api/))。可行的通道有四条：RSS 用来读取（同步自己的往期档案、追踪同行），CSV 导出用来拿指标，人工粘贴用来发长文，原生定时或 Typefully 用来发 Notes。非官方的 cookie 型 API 和 MCP server（例如 `codalanguez/substack-mcp`，自带约每秒 1 次的限流，并警告“发布是公开且不可撤销的”）只能在作者明确选择开启之后使用，而且只建草稿【待核实】([substack-mcp](https://github.com/codalanguez/substack-mcp))。据第三方条款追踪站，Substack 条款禁止抓取和爬取【待核实】([ConductAtlas](https://conductatlas.com/platform/substack/substack-terms-of-use/provision/CA-P-029302/prohibition-on-scraping-or-crawling-substack/))。条款是否明确禁止用 cookie 自动发文，研究团队**未找到证据**。

**X：按次付费 API，标签与限制，排序权重有前提。** 写入成本很低，真正贵的是读取。下面是一个成本模型（单价都是第三方报道【待核实】）：

| 场景 | 月用量 | 估算成本 |
|---|---|---|
| 每天 3 条普通帖 | 约 90 条 × $0.015 | 约 $1.35 |
| 同样数量，全部在正文带链接 | 约 90 条 × $0.20 | 约 $18 |
| 每天读取 1,000 条自有帖子的指标 | 约 30,000 次 × $0.005 | 约 $150 |
| 只读最近 7 天的自有帖子，每天 1 次（约 20 条） | 约 600 次 × $0.005 | 约 $3 |

因此，复盘模块应该只批量拉取本账号近期的帖子。合规方面有五条：只用作者本人的 OAuth 用户 token，以作者身份发布经过人工批准的内容，这是普通的排期用法；一旦 Agent 自主回复或自主互动，账号就成了“自动化账号”，必须挂 Automated 标签并关联真人账号，这对创作者的品牌不利；AI 回复机器人据报需要事先书面批准；自动点赞、自动关注、批量重复发帖、未经请求的自动 @ 都是长期以来的封号风险【待核实】([docs.x.com](https://docs.x.com/developer-guidelines))；浏览器自动化和抓取违反服务条款。第三方的低价数据转售商不是官方渠道，处于灰色地带【待核实】([twitterapi.io](https://twitterapi.io/blog/x-api-cost-breakdown-2026))。排序权重有四个使用前提：它们是默认值，线上可以被实验覆盖；乘的是预测概率，不是计数；作者多样性衰减和站外乘数的生产值没有公开；Phoenix 模型权重不在仓库里【原文已读】([x-algorithm](https://github.com/xai-org/x-algorithm))。**能从代码推出的是机制，推不出的是量级。**

**Medium：API 不再支持，只能靠 Import 和人工判断。** 官方文档原话：“The Medium API is no longer supported… We do not recommend using it… We don't allow any new integrations with our API.” 自发 token 不会过期，除非被撤销；在出版物里，writer 只能建草稿，要等 editor 批准；文档里没有写明速率限制【原文已读】([medium-api-docs](https://github.com/Medium/medium-api-docs))。2025 年起不再发新 token，Make 的 Medium 应用已经下线，Write.as 的集成也被切断【待核实】([apps.make.com](https://apps.make.com/medium); [write.as](https://write.as/blog/page/3))。RSS（`medium.com/feed/@username`）只能读。没有统计 API。存在一些“无 API 发布”的浏览器自动化仓库，有违反条款的风险，不建议用【待核实】。在发布策略上，AI 政策比工具更重要：**进付费墙的稿子必须是人写的**。

| 能力 | Substack | X | Medium |
|---|---|---|---|
| 读取自己的内容 | RSS ✅ | API（付费）✅ | RSS ✅ |
| 读取指标 | CSV 导出（人工） | API（付费）✅ | 人工记录 |
| 写长文 | ❌ 人工粘贴 | Articles：排期工具或人工 | 旧 token 建草稿，或人工 Import |
| 写短内容 | Notes：原生定时 / Typefully【待核实】 | API ✅ / 排期工具 | — |
| canonical | 不能指向外部 | 无 | Import 自动设置 / API `canonicalUrl` |
| 自动化红线 | cookie API 存在条款风险 | 自主互动需挂标签；AI 回复需批准 | 无头浏览器；AI 文字进付费墙 |

---

## 指标与评估：每个平台各看各的口径

| 平台 | 质量信号（最便宜） | 读者信号 | 商业信号 | 不要优化的虚荣指标 |
|---|---|---|---|---|
| Substack 长文 | 人工编辑时长；AI 稿到终稿的编辑距离 | 打开者点击率、评论、restack | 按来源统计的新增免费和付费订阅、退订；转化按 2–3% 设基准 | 单看打开率（邮箱会隐藏打开） |
| Substack Notes | — | 点赞、restack、回复 | 由 Notes 带来的免费订阅数 | 点赞数本身 |
| X 单帖 / Thread | 三问分和实际表现的相关性 | 回复/曝光、引用、收藏、主页访问、新增关注、发布后 2 小时的增长速度 | UTM 点击、对应时段的订阅增量；认证用户首页曝光的 90 天累计（Original Content Rewards 资格） | 点赞（权重 0.66）、总曝光 |
| X Articles | — | 停留（作为代理指标）、引用、分享 | UTM 点击 | — |
| Medium | Boost 与否；策展结果 | 会员阅读、阅读率、高亮、回复 | MPP 收入、站外和搜索流量占比、新会员转化；newsletter CTA 的 UTM 点击 | 鼓掌数 |

X 的负反馈（静音、屏蔽、举报）作者是看不到的，能代理它的只有取关数和曝光的突然下滑。**一旦出现负反馈信号，立即降低发帖频率**【设计建议】。

**离线评估从约 20 条用例起步就够了。** Anthropic 用约 20 条代表性查询就看到了明显效果【原文已读】([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system))。具体做法：从往期作品里选 20 份，10 份作者满意、10 份不满意，覆盖长文、单帖和 Medium；倒推出它们的选题、简报和提纲，作为测试输入。每次改提示词都重跑 S3–S6，比较评审分数和作者盲评的结果。系统提示词从最简版本开始，出现失败再加指令【原文已读】([context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents))。**评审本身也要评估**：在测试集上，评审给“差稿”的分数必须显著低于“好稿”，否则就是 Packy 遇到的 A- 问题，评审没有区分度。

**反馈闭环。** 每月复盘输出三类修改提议：声音档案与范文、选题排序权重、平台规则与变体模板。R1（短养长）的规则是：回复率高于账号 30 日中位数 2 倍的短帖，自动进入选题池，标为 `origin: own_post`，正好对应 Koe 说的“从自己的爆款迭代”。R2（常青回收）的规则是：发布 90 天以上、表现在前 20% 的变体，**用新角度重写**后再进入发布队列，不原样重发。Denning 的做法是用新角度回访旧题【待核实】；X 的 Original Content Rewards 只算原创，原样重复还会撞上去重过滤。研究团队**没有找到**任何创作者把数据接回提示词调优的公开案例【未找到证据】，所以这个闭环需要作者自己做小样本实验。还要防古德哈特定律：Perell 说“能火的东西就是更好”，Medium 官方说“别追求爆款”，两者的张力只能由作者来裁决，**声音档案的修改永远由人一票否决**。

---

## 风险与合规：每类风险配一道闸

| 风险 | 表现 | 对策 | 依据 |
|---|---|---|---|
| 幻觉与编造 | 捏造引语、数字、经历 | 没有来源就不写；经历只能从 `stories.md` 取；H4 人工逐条核对；snippet 级来源不能单独支撑数字 | SAFE 一致率 72%【待核实】；Hormozi 说编故事不管用 |
| 声音同质化 | 风格方差下降，观点趋同 | 默认模式 A；范文多样并每季度更新；风格漂移硬闸口；swipe 库只存结构 | LLM 改写会降低风格方差【待核实】([arXiv 2502.11266](https://arxiv.org/pdf/2502.11266))；高度依赖 AI 草稿的人写出的故事更趋同【待核实】([arXiv 2604.03529](https://arxiv.org/html/2604.03529v1)) |
| 读者信任 | 读者感觉“AI 腔” | 文末披露；AI 主要用在研究、编辑和改编上 | Reuters：完全 AI 生成的新闻只有 12% 的人能接受，人主导、AI 辅助的接受度 43%【待核实】([NewscastStudio](https://www.newscaststudio.com/2025/10/16/public-use-of-generative-ai-grows-but-trust-and-comfort-with-news-applications-remain-low)) |
| Medium 政策 | AI 文字进付费墙，被取消 MPP 资格 | `compliance.paywall` 和 `draft_mode` 硬绑定；B 模式稿必须披露且不设付费墙 | Medium AI 政策【待核实】 |
| Substack 检测 | Pangram 评分高，读者信任下降 | 最终文字以人写为主 | Axios【待核实】 |
| X 自动化 | 封号、被迫挂 Automated 标签 | 不做自主互动；不做 AI 自动回复；不做自动点赞或关注；人逐批批准 | X 开发者规则【待核实】；2026-10-09 条款修订【待核实】 |
| 原创与抄袭 | 照搬异常值的措辞 | swipe 库不存原句；n-gram 重叠闸口；对齐 Koe 的“借想法不借措辞” | Koe【转录】；Original Content Rewards 只算原创【待核实】 |
| 条款与账号 | cookie API、抓取、无头浏览器 | 默认关闭；开启需作者明确选择，并在日志里记录 | Substack、Medium 条款【待核实】 |
| 隐私与袒露 | 写出不该公开的经历 | `stories.md` 每条带 `consent` 字段；涉及他人的经历需要匿名化 | Ashley【待核实】 |
| 倦怠 | 量压垮作者 | 节奏上限写进配置；预留 20% 不为数据写的时间 | Rane、Ashley【待核实】；Koe 说“降低量” |
| 成本 | 多 Agent 研究和 X 读取 | 多 Agent 只用于每周的母稿；X 只读自有的近期帖子 | Anthropic：约 15 倍 token【原文已读】 |
| 证据偏差 | 把厂商的“算法秘籍”当事实 | 证据分级：代码 > 官方 > 厂商数据 > 增长博客 | 厂商利益冲突【待核实】 |

---

## 分阶段路线图：从一个脚本到多平台流水线

| 阶段 | 时间 | 范围 | 完成标准 |
|---|---|---|---|
| **P0 建库** | 第 1–2 周 | 用 RSS 导入 Substack 和 Medium 的往期内容；人工挑 10 段范文（区分长文和短帖）；写 `profile.yaml`、`never.md`、`stances.md`、`stories.md`；把现有的点子录进 `ideas.jsonl`，每条都写上 edge；建好三份 `platforms/*.yaml` | 作者读 `profile.yaml` 时觉得“这就是我”；选题池 30 条以上，并且都有 edge；`stories.md` 有 20 条以上已确认的经历 |
| **P1 MVP：一个母站加一个辐条** | 第 3–6 周 | 一个脚本串起 S1 → S3 → S5（陌生人评审、Dry 三问、lint、TK 拦截）→ S6（只生成 `x_post` 和 `substack_note`）；研究用单 Agent 加搜索；全部人工发布；UTM 生成器 | 连续 4 周按节奏发出；20 条离线测试集建好；评审在测试集上能区分好稿和差稿；每篇都记录人工编辑时长 |
| **P2 平台适配与回流** | 第 7–12 周 | 加入 `x_thread`、`x_article`、`medium_story` 适配器和对应的 G-* 闸口；接入 X API（OAuth、按次付费）只读自有指标，发布由人逐批批准；Medium 走 Import 流程并核对 canonical；导入 Substack CSV；`edit_diffs` 采集；第一次月度复盘（H7） | 每篇母稿至少产出 3 类平台变体；Medium 的 canonical 核对率 100%；引语和数字的人工核对 100% 覆盖；有一张按渠道统计 UTM 点击和订阅的报表 |
| **P3 研究与循环** | 第 4–6 个月 | S2 升级为编排者-工作者加引用绑定；SAFE 式逐条核查；拔刺采样；CRIBS；R1 短养长与 R2 常青回收；评审锚点校准；风格漂移闸口 | 论据支撑率 ≥95%；人工编辑时长比 P1 下降，读者指标不下降；至少 1 篇长文选题来自 R1 |
| **P4 进阶（按需）** | 6 个月后 | 用 LangGraph 加持久化 checkpointer 实现 H1–H7 的 `interrupt()`；接入排期工具的 API；访谈模式（语音 → 转写 → 整理）；读者调查设计与分析；（可选、有风险）cookie API 或 Playwright 只建草稿 | 作者盲评 AI 参与的稿件不低于纯人写稿件；没有任何一次未经人工按键的发布；平台规则 90 天内都核对过 |

每个阶段都遵循同一条规则：**只有在离线测试集上证明有提升，才增加复杂度**。举例来说，如果 P1 没有证明单 Agent 研究漏掉了关键信息，P3 就不上多 Agent。

---

## 结论

三个平台的头部创作者，最难复制的东西几乎相同：一个别人没有的切入点，一个只属于作者的故事库和证据，一个经过多年迭代形成的视角。三个平台对这些东西的定价却各不相同。Substack 把它们换成可以拥有的读者关系，X 把它们换成回复和私下转发，Medium 把它们换成人工策展和会员的阅读时长。所以，一个好的多平台 Agent，不是一台能把一篇文章复制到三个地方的机器。它要做的，是**同一个人类内核，按三种语法各说一遍**，并且把每一种语法的规则都写进可以检查、可以按月更新的配置里。PG 的陌生人测试、Dry 的三问和 Gioia 的诚实三问之所以适合写进机器，是因为它们检验的是“有没有说清楚”；而 edge、兴奋度和亲身证据必须留给人，是因为它们回答的是“值不值得说”。

还有一个反直觉的结论：平台机制里证据最硬的那部分，也就是 X 的开源代码，恰好最不支持“多发、批量、自动化”。负反馈的惩罚是点赞的几十到几百倍，作者多样性衰减会让同一账号的连发互相竞争，冷启动扶持只给 2 小时，原创才计酬。Koe 主动“降低量，提高质量”，从代码这一侧看是讲得通的。本手册所有关于标题公式、发帖时间、线程长度的建议都只是起点，作者应该把复盘环节当作自己的小样本实验平台。另外，本报告的创作者证据大多是搜索摘要，任何引语在写进自己的文章之前，都请先回到原链接核对一次。这也正是 H4 闸口要求作者做的事。
