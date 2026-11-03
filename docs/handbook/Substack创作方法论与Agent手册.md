# 从头部 Substack 作者的做法反推一套创作 Agent

头部 Substack 作者没有统一的写作公式。他们反复在用的是四个可以照搬的机制：**一份按兴奋度排序的选题清单**（Lenny Rachitsky）、**用固定视角解读源源不断的新闻**（Heather Cox Richardson 的历史学视角、Kyla Scanlon 的“这跟你有什么关系”）、**一个低门槛的素材收集箱，写作前再统一清理**（Ryan Broderick 用 Raindrop 收藏，写之前倒进 Google Doc 逐条筛），以及**只把稿件交给编辑和可信审读人之后才发**（Lenny、Gergely Orosz）。增长方面，Substack 官方在 2024 年公布，站内推荐网络（Recommendations 加 App）带来了**约 50% 的新订阅和 25% 的新付费订阅**。第三方研究另外发现，Notes 能拉来免费订阅，但很少直接带来付费。基于这些证据，本手册推荐的 Agent 架构是最简单可行的那种：**分阶段流水线，每个阶段之间设人工检查点**。只有研究阶段用并行子 Agent，写稿和改稿由同一个持有完整语境的 Agent 完成，发布这一步永远由人按下。原因有三：Substack 没有官方发文 API；它自 2026 年 7 月起据报道引入了基于 Pangram 的 AI 检测；读者对“完全由 AI 写的内容”的接受度明显低于“人主导、AI 辅助”的内容。所以 Agent 最适合定位成**研究助理、编辑和改编分发员**，不该定位成代笔。还要先说明一点：本报告依据的研究笔记，绝大多数结论来自对一手页面的**搜索引擎摘要**，没有读过全文（原因是会话网络受限）。只有 Anthropic 的三篇工程文章读过原文。所以下文的引语和数字都需要回到原链接核对。

---

## 证据等级与标注约定

研究团队在 2026-11-03 检索时，Substack 自有域名、niemanlab.org、bc.edu 等几乎所有一手站点都无法抓取全文，结论主要来自搜索结果对这些页面的摘要。为了尊重读者对诚实的要求，本报告统一使用以下标注：

| 标注 | 含义 |
|---|---|
| （无标注） | 来自一手页面（作者本人文章、播客节目说明、Substack 官方博客、权威媒体）的搜索摘要，方向可信，但原文措辞需核对 |
| **【待核实】** | 只出现在二手、聚合或低可信站点，或不同来源互相矛盾，或笔记作者明确标为未经验证 |
| **【未找到证据】** | 研究团队检索后没有找到任何来源 |
| **【原文已读】** | 研究团队读过原文全文（仅限 Anthropic 工程博客） |
| **【设计建议】** | 本报告作者自己的设计推断，不是创作者的做法 |

第一部分只写有来源支撑的创作者实践。第二部分的手册凡是超出证据的内容，都标为【设计建议】。

---

# 第一部分：头部创作者的方法论（按阶段综合）

## 创意阶段：选题清单、固定视角和读者投票撑起了题源

**选题的第一个引擎是读者问题清单，排序标准是作者自己的兴致。** Lenny Rachitsky 把 Lenny's Newsletter 定位成一个专栏，每周回答读者关于“打造产品、驱动增长、加速职业发展”的问题 ([Lenny's Newsletter](https://www.lennysnewsletter.com/p/increasing-virality))。他说自己有一份**约 50 个题目**的清单，对接下来 2–3 篇已有大致想法 ([Compound Planning interview](https://manual.compoundplanning.com/chapters/interview-with-lenny-rachitsky-writer-of-lennys-newsletter))。在约 2021 年的 Indie Hackers AMA 里，他说清单约 30 个题目，读者问题一来就往里加，然后“按我最想写的排序” ([Indie Hackers AMA](https://www.indiehackers.com/post/i-write-lennys-newsletter-the-1-paid-business-newsletter-on-substack-generating-over-500k-arr-ama-46fe3dfdc4))。约 2020 年的访谈里，他每个题目单独开一个 Coda 页面收集笔记 ([The Proof](https://theproofwellness.com/interviews/lenny-rachitsky-on-flow-state-ambition-and-angel-investing))。值得注意的是，这里的排序看的是作者的精力和兴趣，不是 SEO 或数据。这对 Agent 设计有直接影响：排序器不能只看外部热度，必须让作者本人的兴奋度权重最高。

**第二个引擎是用一个固定视角去处理无穷的输入流。** Heather Cox Richardson（HCR）每天早上先花**一到两个小时浏览多个社交媒体**，“看看公众在聊什么” ([KALX interview](https://kalx.berkeley.edu/kalx-news-heather-cox-richardson-interview))。她自称“不是记者……是历史学家”，工作是解读，不是报道发生了什么 ([Boston College Magazine, Fall 2022](https://www.bc.edu/content/bc-web/sites/bc-magazine/fall-2022-issue/features/history-s-first-draft.html))。Kyla Scanlon 的过滤器是把抽象的宏观经济（比如美联储）翻译成对个人的影响，她在 2022 年的一篇 Substack 文章里创造了“vibecession”一词 ([Fortune, Jun 2024](https://fortune.com/2024/06/26/kyla-scanlon-tiktok-youtube-newsletter-economist-vibecession))。Emily Oster 的 ParentData 把最新科研“翻译成你日常生活中问题的答案” ([ParentData](https://www.parentdata.org/))。Anne Helen Petersen 认为什么都可以框定为“文化”，所以她可以写任何想写的东西 ([Seattle Met, May 2025](https://www.seattlemet.com/news-and-city-life/2025/05/anne-helen-petersen-culture-study))。这几位的共同点是：输入的领域很宽，解读的视角只有一个。

**第三个引擎是读者投票，用来减少作者的猜测。** 据 Brad DeLong 转述，Matt Yglesias 的 mailbag 分两步：周日晚开帖征集问题，周一晚开帖让读者在三个候选里投票（日期不详）([Brad DeLong](https://braddelong.substack.com/p/should-i-be-running-a-mail-answers))。Noah Smith 发投票帖问读者想看什么，并发布“即将推出的文章预告”来测兴趣 ([Noahpinion poll](https://www.noahpinion.blog/p/tell-me-what-you-want-what-you-really); [A preview of upcoming posts](https://www.noahpinion.blog/p/a-preview-of-upcoming-posts))。Ted Gioia 每年发“Open Mic”和征求建议的帖子 ([Open Mic](https://www.honest-broker.com/p/open-mic-at-the-honest-broker))。他的创刊故事“How I Became the Honest Broker”在 18 个月时仍是阅读量最高的一篇 ([The Honest Broker turns 18 months](https://tedgioia.substack.com/p/the-honest-broker-turns-18-monthshere))。由此可见，一篇“定位宣言”式的文章可以多年保持头部流量。

**定位更多靠“身份 + 视角”，不靠收窄题材。** Elle Griffin 投稿过 100 多位文学经纪人后，判断自己的作品适合“1,000 人的小众读者”而不是 10 万人的大众读者，于是开始每周连载一章小说，后来转型为 The Elysian ([Newsletter Crew](https://newsletter-crew.pages.dev/blog/switching-it-up-2022-growth-strategy-with-elle-griffin))。Slow Boring 公开的定位是“艰难、严谨、不总是迎合我们偏见的对话” ([Slow Boring About](https://www.slowboring.com/about))。研究团队**没有找到**任何一位头部作者公开过“我不写什么”的清单【未找到证据】。“不做什么”通常表现为拒绝相邻的形式或渠道：Ryan Broderick 曾因为播客“很难增长”、Garbage Day“已经够忙”而犹豫要不要做播客 ([Tinkmedia](https://tinkmedia.co/interviews/ryan-broderick))；Gioia 创刊时推掉了其他自由撰稿机会 ([Jazz Journalists Association](https://news.jazzjournalists.org/gioia-goes-substack/))。

**栏目通常是“一个高投入旗舰栏目 + 若干低投入的社区型固定栏目”。** Culture Study 几乎每周两篇正文，外加两次仅限付费用户的“Threads”讨论帖 ([Culture Study](https://annehelen.substack.com/))。Slow Boring 每周四篇以上，外加 mailbag ([Slow Boring About](https://www.slowboring.com/about))。The Pragmatic Engineer 周二发深度长文，周四发时效新闻或独家 ([Write That Blog](https://writethatblog.substack.com/p/gergely-orosz-on-technical-blogging))。频率决定题源：日更作者（HCR、Noah、Yglesias）靠新闻周期供题，周更或更慢的作者（Lenny、Packy McCormick）靠选题清单或核心论点供题。据二手总结，Packy 在 2025 年从高频转向“更少、更深、研究更重”的长文【待核实】([Aakash Gupta](https://www.news.aakashg.com/p/packy-mccormicks-story))。Tim Denning 先写标题、批量发给自己、再写正文的做法只有二手来源【待核实】([Medium](https://medium.com/illuminations-mirror/tim-denning-5779d8d52593))。

## 素材阶段：靠“收集箱 + 写前清理 + 个人核实规则”，不靠精致的第二大脑

**文档最详细的素材系统其实很简单。** Ryan Broderick 用 **Raindrop** 的分文件夹全天“被动”收藏链接，newsletter、直播、播客各一个文件夹。写作那天早上，他把收集到的条目从一个 Google Doc 倒进浏览器，逐条检查链接是否已删除或有更新 ([The Story](https://thestory.au/articles/ryan-broderick-garbage-day-newsletter-interview/))。Lenny 做研究型文章时，把所有发现“乱糟糟地”扔进一个文档，持续往里加，最后再把“原始素材块”塑成文章 ([Compound Planning](https://manual.compoundplanning.com/chapters/interview-with-lenny-rachitsky-writer-of-lennys-newsletter))。Casey Newton 用 Readwise、Capacities、Raycast，并说 NotebookLM 能让人“把一堆 PDF 存进虚拟笔记本，再对它们整体提问” ([Platformer](https://www.platformer.news/ai-productivity-apps-capacities-raycast-readwise/))。但他在 2023 年也写过，“用了三年昂贵的笔记软件，似乎并没让我成为更好的思考者” ([Casey Newton on X](https://twitter.com/CaseyNewton/status/1694870152276570328))。研究团队**没有找到**任何一位头部作者使用 Obsidian、RSS 阅读器或刻意维护“swipe file”（他人佳作摘抄库）的证据【未找到证据】。手册里的 swipe file 属于【设计建议】。

**输入量远大于输出量。** Ted Gioia 每天早上读书约两小时，另有说法是每天至少三小时 ([I Answer 18 Questions](https://www.honest-broker.com/p/i-answer-18-questions); [My Lifetime Reading Plan](https://www.honest-broker.com/p/my-lifetime-reading-plan))。Noah Smith 引用导师“每写一篇论文要读约 100 篇”的规则，并说博客文章大约是 **20 比 1** ([Noahpinion](https://www.noahpinion.blog/p/noah-smiths-writing-advice))。Adam Tooze 的 Chartbook 起源于把“过去几天在推特上发过的重要图表和链接”汇编起来，付费的“Top Links”就是把精选后的收集箱直接发出去 ([Chartbook #1](https://adamtooze.com/2020/11/15/chartbook-1/))。

**能形成护城河的素材是专有数据和一手信源。** Lenny 2025 年 12 月的 AI 生产力调查约 1,750 人参与，由 Noam Segal 设计、执行和分析 ([Lenny's Newsletter](https://www.lennysnewsletter.com/p/ai-tools-are-overdelivering-results); [Lenny on X](https://x.com/lennysan/status/2009308394918707476))。Orosz 的 2025 技术栈调查有 3,000 多份回复，与 Elin Nilsson 联合署名 ([Pragmatic Engineer 2025 Survey](https://newsletter.pragmaticengineer.com/p/the-pragmatic-engineer-2025-survey))。他也提醒，这类数据来自读者自选样本，不具代表性 ([PE Three Years](https://newsletter.pragmaticengineer.com/p/the-pragmatic-engineer-three-years))。据 Nieman Lab 2026 年 4 月的标题，Casey Newton 正把 Platformer 改为“更多独家、更少聚合与分析”，明确是为了和 AI 竞争 ([Nieman Lab](https://www.niemanlab.org/2026/04/more-scoops-less-aggregation-and-analysis-how-casey-newton-is-revamping-his-newsletter-to-compete-with-ai/))。这一点对 Agent 设计非常关键：**AI 最容易替代的环节（聚合、摘要）恰恰是读者最不愿付费的环节**，所以 Agent 应该为人类节省时间，让人去做独家采访和原创数据。

**准确性靠个人规则，不靠专职核查团队。** 据一篇访谈摘要，HCR 的规则是**没有三个不同来源佐证就不发**，她曾为确认一艘美国航母的位置放慢写作 ([Brian Boyles](https://brianboyles.substack.com/p/my-conversation-with-heather-cox))。Platformer 尽可能实名引用信源，匿名信源则尽量具体描述其身份 ([Platformer About](https://www.platformer.news/about/))。Noah Smith 用 FRED 原始序列重建图表，来拆穿病毒式传播的图表 ([Noahpinion](https://www.noahpinion.blog/p/how-not-to-be-fooled-by-viral-charts))。ParentData 称每个主题都会查阅“数百项研究”，优先引用次数高的研究、随机对照、大样本和客观测量，并承诺说明局限 ([ParentData About](https://parentdata.org/about-us/))。Oster 在没有数据时会直接说没有 ([Deseret News](https://www.deseret.com/family/2024/10/23/emily-oster-parenting-data-raising-parents-podcast))。研究团队**没有找到**任何一家公开的更正政策，也没有找到聘用付费事实核查员的证据【未找到证据】。

**AI 在素材环节的公开用法。** Packy McCormick 在 Every 的播客里谈到用 AI 做深入研究、用 Claude Projects 编辑，以及现场做了一个给文章打分的工具 ([Every](https://every.to/chain-of-thought/how-packy-mccormick-finds-his-next-big-idea))。ParentData 用一个名为 Petey 的 AI“图书管理员”基于自家资料库回答读者问题 ([ParentData](https://parentdata.org/))。有第三方 newsletter 称 Newton 每周四跑一个 Claude 流程“扫描多个空间”，原话“AI 做扫描，我做编辑”，但无法确认是否为 Newton 本人所说【待核实】([Project C](https://newsletter.projectc.biz/p/agreeing-to-disagree-with-casey-newton-on-ai))。

## 创作阶段：卖深度的作者每篇投入 10 小时以上，日更作者靠阅读量和惯性

**写作流程分成两种原型。** 第一种是日更或高产型：HCR 每天约 **1,200 字**，多在夜间写作，常常写到凌晨四五点 ([BC Magazine](https://www.bc.edu/content/bc-web/sites/bc-magazine/fall-2022-issue/features/history-s-first-draft.html))；Noah Smith 说自己“没什么正式流程”，有时先写小标题，很少修改 ([Noahpinion](https://www.noahpinion.blog/p/noah-smiths-writing-advice))。第二种是深度旗舰型：Lenny 说每篇**中位数 10 小时，少则 3 小时，多则 100 小时以上** ([Lenny's Newsletter, "500,000"](https://www.lennysnewsletter.com/p/500000))。他有编辑负责结构和内容反馈，另有文字编辑和设计师；给每位客座作者的稿子投入 10 小时以上、迭代 5–6 轮 ([Growth Curve, Mar 2025](https://www.growthcurvenewsletter.com/p/how-lenny-rachitsky-built-the-world-s-largest-product-newsletter-with-no-full-time-employees))。不同年份、不同来源给出的工时（10–30 小时、10–20 小时）互相矛盾【待核实】([CNBC](https://www.cnbc.com/make-it/2024/01/15/lenny-rachitskys-advice-for-success-in-a-podcast-and-newsletter.html))。Orosz 每篇深度长文横跨数周，按天拆分为研究、初稿、可信审读人反馈和编辑润色，并始终保持每周约两篇存稿 ([Lenny's Podcast summary](https://podpage.com/lennys-podcast/blog/summary-leaving-big-tech-to-build-the-1-technology-newsletter-gergely-orosz-the-pragmatic-engin))。

**有几种结构化写法可以直接借来。** Doomberg 先凭直觉确定想说什么，围绕这个核心做研究，然后**先定标题，再为每段写一句话摘要** ([Fire2Fission ep. 50](https://www.fire2fission.com/podcast-episodes/050-doomberg))。这本身就是一个现成的“提纲门槛”。Packy 发布前有两道自检：有没有做出一个好的“画面”？如果写的是公司，这是不是写这家公司最好的一篇？([How I Write w/ Packy McCormick](https://metacast.app/podcast/how-i-write/RRY6pAWO/packy-mccormick-how-to-publish-your-best-ideas-online/E1uwO8D4))。Lenny 建议“在纸上用最简单的方式把想法画出来” ([podcast summary](https://podcasts-distilled-hugo-content.pages.dev/lennys-podcast-product-career-growth/how-i-built-a-1m-subscriber-newsletter-and-top-10-tech-podcast-lenny-rachitsky/))。研究团队**没有找到**任何一位作者公开发布的编辑检查清单【未找到证据】，手册中的清单都是【设计建议】。

**AI 编辑打分偏高，这对 Agent 评估很有提醒意义。** Packy 在 2024 年 8 月写道：“我用 Claude 当编辑好几个月了，很好用，但几乎我发过去的每份初稿它都给 A-” ([Packy on X](https://x.com/packyM/status/1821163105830769100))。这说明不加校准的 LLM 评审会给出缺乏区分度的高分，评审 Agent 必须配锚定样例和明确的扣分规则。Ethan Mollick 据报道每篇都自己写，完整写完初稿后才让 AI 给反馈，并把“写作即思考”作为防止通用聊天机器人腔调的方法 ([One Useful Thing](https://www.oneusefulthing.org/about); [WBUR, Jul 2025](https://www.wbur.org/onpoint/2025/07/25/ethan-mollick-ai))。

**声音来自身份和持续写作，不来自修辞技巧。** Gioia 说“只有不停地写才能学会写”，还说“学规则很好，自己发明规则更好” ([Substack "The Active Voice"](https://read.substack.com/p/the-active-voice-ted-gioia))。Packy 说他是通过心流和随意的对话语气找到自己的声音的 ([The Proof](https://theproofwellness.com/packy-mccormick-on-writing-flow-finding-his-voice))。Tim Denning“直说别人不敢说的话”、刻意保留语法怪癖等特征，只见于第三方分析【待核实】([Illumination](https://medium.com/illumination/i-spent-100-hours-studying-tim-dennings-writing-47b5fd24a2d0))。

**标题的证据基本是个人经验。** Substack 推出了原生标题 A/B 测试：先给一部分订阅者测试不同标题，再把胜出者发给其余人。官方只说测试结果“令人鼓舞”，没有给出数字 ([On Substack](https://on.substack.com/p/new-on-substack-ab-testing-for-headlines))。据二手报道，最多可测 4 个变体，默认测 1 小时；小于 1 万订阅的列表建议只测 2–3 个【待核实】([Pubstack Success](https://pubstacksuccess.substack.com/p/how-to-do-title-tests-in-substack?r=nu825))。几条单人经验方向一致但证据很弱：一位作者的测试里“I”开头的标题持续胜出 ([Annabel Gat](https://annabelgat.substack.com/p/substack-ab-testing-how-i-increased))；另一位分析约 150 封邮件，发现打开率最高的都戳中了读者已有的某种紧张感 ([Mike J Searles](https://mikejsearles.substack.com/p/one-thing-high-open-emails-share-substack))；还有报告称反直觉标题打开率最低，但打开者的点击率最高【待核实】([Pubstack Success](https://pubstacksuccess.substack.com/p/how-to-make-your-substack-posts-perform))。“主题行占打开率 80%”“28–50 字符最优”之类的说法**没有找到来源**【未找到证据】。此外，部分邮箱会隐藏打开行为，打开率本身就不准，评估标题时应看“打开者点击率”。

## 发布阶段：站内网络是主要增长引擎，付费转化要按 2–3% 做规划

**站内网络带来大约一半的新订阅。** Substack 官方 2024 年 2 月的说法是：“Recommendations 与 Substack App 构成的网络，带来了**全部新订阅的 50% 和新付费订阅的 25%**” ([On Substack](https://on.substack.com/cp/142007285); [TechCrunch, Feb 2024](https://techcrunch.com/2024/02/22/substack-now-lets-writers-curate-a-network-of-recommended-publications-for-their-subscribers/amp/))。注意这是 2024 年的数据。“三个月 App 内新增 3,200 万订阅”只出现在二手来源【待核实】([Blog Herald](https://blogherald.com/blog-platforms-tools/n-substack-reported-32-million-new-subscribers-from-inside-the-app-in-three-months-most-bloggers-are-missing-what-that-means/))；“Notes 占新付费转化 25%”可能是误读了上面那条 2024 年数据【待核实】([creatorstack](https://creatorstack-io.pages.dev/blog/substack-creator-guide-2026))。也有反例：一个约 6.7 万人的列表，推荐只带来 189 名订阅者【待核实】([eden.so](https://eden.so/blog/substack-growth-strategy/))。这说明推荐对已经成名的作者更有利。

**Notes 拉免费订阅，很少直接卖出付费。** 一项第三方研究分析了 **396,143 条 Notes**：13.1% 至少带来一位免费订阅者，只有 **0.70%** 卖出过付费订阅；即便在最受欢迎的 2,781 条里，也只有 7.2% 卖出过付费 ([The Writing Edge, ~Oct 2026](https://thewritingedge.substack.com/p/substack-notes-convert-paid-subscribers))。Lenny 把自己的增长归功于稳定的每周更新、客座作者和一篇早期在 Medium 上爆火的文章 ([On Substack](https://on.substack.com/p/how-lenny-rachitsky-earned-65000))。

**付费有两种主流模式。** 一种是几乎全免费、靠忠诚付费：HCR“很少设付费墙”，2025 年 11 月订阅者超过 270 万 ([Wikipedia](https://en.wikipedia.org/wiki/Heather_Cox_Richardson))。另一种是重付费墙加权益捆绑：Lenny 每月只开放一篇免费文章，付费价格为 $15/月、$150/年，附带 Slack 社区 ([Newsletter Circle](https://newslettercircle.substack.com/p/8-proven-paywalling-strategies-used))；年费还捆绑了多款软件订阅【待核实】([tripledart](https://www.tripledart.com/hub/newsletters/lennys-newsletter))。Noah Smith 认为“免费邮件订阅数是最重要的指标”，免费文章是比付费文章更好的营销 ([Noahpinion](https://www.noahpinion.blog/p/how-to-write-a-successful-substack))。转化率方面，Substack 官方指南给的是免费转付费 **5–10%**、目标 10% ([Substack Going Paid Guide](https://substack.com/going-paid-guide))；独立分析给出的中位数约 **3%**，记者调查为 2–5% ([Simon Owens](https://simonowens.substack.com/p/whats-a-realistic-conversion-rate))。规划时应该按 2–3% 算，把 5–10% 当作垂直、高价值内容的上限。

**发送时间远没有稳定更新重要。** Substack 从未发布过官方发送时间研究【未找到证据】。一位员工在评论里提过“周末打开率略高，周日好于周六” ([On Substack comment](https://on.substack.com/p/new-tools-paywall-embeds/comment/3384439))。Eden.so 分析了 473,405 条 Notes，最佳与最差发布时段的差距只有**约 3 个百分点** ([Eden.so](https://eden.so/blog/best-time-to-post-on-substack/))。

**2026 年的平台功能把改编分发做进了产品。** 据 AlternativeTo 的产品新闻汇总【待核实】：2026 年 3 月 Substack 推出 Recording Studio，可自动生成宣传短片；同月支持统计数据 **CSV 导出**和 Notes 草稿；4 月支持 Notes 定时发布和文章模板 ([AlternativeTo Mar 2026](https://alternativeto.net/news/2026/3/substack-adds-draft-notes-multi-post-pinning-stats-csv-exports-and-live-video-management); [AlternativeTo Apr 2026](https://alternativeto.net/news/2026/4/substack-adds-note-scheduling-post-templates-drop-caps-new-livestream-options-and-more))。官方的推荐奖励可以设三档，订阅者达标时 Substack 会自动发邮件通知；官方还称欢迎邮件和页眉页脚是“常被忽视的增长工具” ([On Substack: subscriber referrals](https://on.substack.com/p/subscriber-referrals))。

### 四阶段证据速览

| 阶段 | 证据最强的可复制机制 | 代表来源 | 主要证据缺口 |
|---|---|---|---|
| 创意 | 读者问题清单 + 按兴奋度排序；固定视角解读新闻流；两步投票 mailbag | Lenny、HCR、Yglesias | 没有公开的“不写什么”清单；Free Press 和 Garbage Day 的选题流程不详 |
| 素材 | 收藏收集箱 → 写前清理；每篇一个“乱文档”；三源佐证；回到原始数据 | Broderick、Lenny、HCR、Noah | 没有 RSS、Obsidian、swipe file 使用证据；没有更正政策 |
| 创作 | 先标题再逐段一句话提纲；编辑 + 可信审读人；发布前“画面/最佳”自检 | Doomberg、Orosz、Packy | 没有公开的编辑清单；“How I Write”播客的完整转录未获取 |
| 发布 | 站内网络（推荐/App/Notes）；免费即营销；稳定的固定节奏 | Substack 官方、Noah、Lenny | 2025–26 年无官方增长占比数据；无发送时间研究；无流失基准 |

---

# 第二部分：创作 Agent 工作手册

> 本部分除注明来源者外，均为【设计建议】。架构依据 Anthropic 三篇工程文章（【原文已读】）和第一部分的创作者实践。

## 总体架构：七段流水线、六个人工闸口，只有研究阶段并行

**先用“工作流”，不急着上“自主 Agent”。** Anthropic 把**工作流**（LLM 和工具按预定义的代码路径编排）与**Agent**（LLM 在循环里根据环境反馈自主调用工具）区分开，建议“找到最简单的方案，只在需要时才增加复杂度”，并且先直接调用 LLM API，再考虑框架，因为框架可能把提示词藏起来 【原文已读】([Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents))。多 Agent 在宽度优先、可并行的研究任务上收益明显：Opus 4 主控加 Sonnet 4 子 Agent 在内部研究评测上比单 Agent 高 **90.2%**。代价是 token 消耗约为对话的 **15 倍**，而且在“所有 Agent 必须共享同一语境”的任务上并不合适 【原文已读】([Anthropic, multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system))。用同一种声音写作，正属于需要共享语境的任务。Cognition 也主张“写入保持单线程”，并认为评审 Agent 从干净语境出发效果更好【待核实，仅读到二手摘要】([jxnl.co](https://jxnl.co/writing/2025/09/11/why-cognition-does-not-use-multi-agent-systems/); [Cognition](https://cognition.ai/blog/multi-agents-working))。

由此得到本手册的推荐架构：**路由式收件 → 并行生成角度 → 编排者-工作者研究 → 链式提纲与成稿（单写手）→ 干净语境的评审-优化循环 → 确定性的打包流程 → 人工发送 → 指标回流。**

```
 ┌────────────┐   ┌────────────┐  H1  ┌────────────┐  H2  ┌────────────┐  H3
 │ S0 收件分拣 │──▶│ S1 选题定角 │──▶│ S2 研究取证 │──▶│ S3 论点提纲 │──▶
 │ (routing)  │   │(并行+排序)  │ 选题 │(编排-工作者)│ 简报 │ (链式+闸口) │ 提纲
 └────────────┘   └────────────┘     └────────────┘     └────────────┘
       ▲                                                        │
       │                                                        ▼
 ┌────────────┐  H6  ┌────────────┐  H5  ┌────────────┐  H4  ┌────────────┐
 │ S7 复盘学习 │◀──│ S6 打包分发 │◀──│  人工发布   │◀──│S4/S5 成稿编辑│
 │(指标回流)   │ 批准 │(确定性流程) │ 发送 │ (Substack) │ 定稿 │(单写手+评审) │
 └────────────┘     └────────────┘     └────────────┘     └────────────┘
            共享：知识库（声音档案 / 选题池 / 摘抄库 / 资料库 / 往期档案）
```

六个人工闸口（H1–H6）分别是：选定题目、确认研究简报、批准论点和提纲、定稿（包括逐条核对引语和数字）、按下发送、批准声音档案和排序规则的修改。如果用 LangGraph 实现，每个闸口对应一个 `interrupt()`：状态由 checkpointer 持久化，图会“无限期等待”，直到收到 `Command(resume=...)`；演示环境可以用 `InMemorySaver`，生产环境应换成 Postgres 或 SQLite ([LangGraph HITL docs](https://docs.langchain.com/oss/python/langgraph/add-human-in-the-loop))。MVP 阶段完全可以不用任何框架：一个 Python 脚本，每个阶段把结果写进 markdown 文件，人在文件里编辑后再运行下一步。

**写作模式要二选一，并写进配置。** 模式 A 是“人先写”（Mollick 式）：作者自己写核心论证初稿，Agent 只负责研究、编辑、核查和改编分发。模式 B 是“AI 辅助起草”：Agent 根据人批准的提纲写分节初稿，人重写其中的关键段落。考虑到 Substack 的 AI 检测和读者信任数据（见后文），**默认推荐模式 A**，只在资讯汇编、链接合集这类低风险栏目里使用模式 B。

## 各阶段模块规格：输入、输出、工具、提示词、闸口

### S0 收件分拣（routing，一次 LLM 调用）

这一步对应 Broderick 的“被动收藏 → 写前清理”。输入包括 RSS 条目、Readwise Reader 存档、读者回复和评论、语音备忘录转写、作者随手记。输出是给每条素材打标签，并路由到选题池、资料库、摘抄库或“即时可写”四个去向之一。工具方面：RSS 用 feedparser；Readwise Reader API v3 是 `GET https://readwise.io/api/v3/list/`，带 `Authorization: Token XXX` 请求头、游标分页，有社区工具报告 LIST 接口限流为每分钟 20 次 ([Reader API docs](https://docs.readwise.io/reader/docs/api); [readwise-reader-api](https://github.com/Scarvy/readwise-reader-api))。这一步不设人工闸口，但每周要人工抽查一次路由准确率。

```text
[系统] 你是{作者名}的收件分拣员。作者的固定视角是：{lens}。
对每条输入，只输出 JSON：{"route": "backlog|source|swipe|now",
"why": "≤20字", "lens_fit": 0-3, "tags": [...]}。
规则：与视角无关(lens_fit=0)的一律 route=source 且不进选题池；
读者原话提问必须 route=backlog 并保留原文；不要改写原文。
[输入] {item_text} | 来源:{url} | 类型:{rss|reader|reply|memo}
```

### S1 选题定角（并行生成 + 排序；闸口 H1）

这一步对应 Lenny 的选题清单加兴奋度排序，以及 Yglesias 和 Noah 的读者投票。输入是选题池中的候选题、本周新闻流、往期档案摘要和读者投票结果。输出是 3–5 个“题目 × 角度”方案，每个包含一句话论点、为什么现在写、读者能得到什么、与往期的重复风险。方法上，并行生成 N 个角度（Anthropic 所说的 parallelization/voting），再由一次排序调用打分。

| 排序维度 | 权重建议 | 依据 |
|---|---|---|
| 作者兴奋度（人工 1–5 分） | 0.35 | Lenny“按最想写的排序” |
| 视角契合度 | 0.20 | HCR、Scanlon、Oster 的固定视角 |
| 读者需求信号（提问数、投票数） | 0.20 | Yglesias、Noah、Gioia |
| 原创性 / 可获得独家素材 | 0.15 | Newton 2026 转向独家、Orosz 调查 |
| 时效性 | 0.10 | 日更作者依赖新闻钩子 |

```text
[系统] 为{作者名}生成选题角度。视角：{lens}。读者：{audience}。
已发布过的相似题目（禁止重复其论点）：{archive_hits}。
对题目「{idea}」给出 {N} 个互不相同的角度，每个包含：
thesis(一句可被反驳的论点) / why_now / reader_payoff /
needs(需要什么独家素材或数据) / risk(与往期重复或无法证实之处)。
不要给出你无法从已有素材中支撑的事实。
```

闸口 H1 由人选题并给出兴奋度分；没选中的角度回流到选题池。【设计建议】每月自动生成一篇“mailbag 候选”，供作者发起读者投票。

### S2 研究取证（编排者-工作者；闸口 H2）

这是唯一值得用多 Agent 的阶段。主控 Agent 把问题拆成子问题；每个子 Agent 都要拿到明确的目标、输出格式、工具与信源指引和边界，否则会重复劳动。研究遵循“先广后窄”：简单的事实查找用 1 个 Agent、3–10 次工具调用；复杂研究再扩到更多子 Agent。研究结束后由单独的 CitationAgent 把每条结论绑定到来源。人工测试曾发现 Agent 偏爱 SEO 内容农场，需要在提示词里加入信源质量启发式 【原文已读】([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system))。上下文管理上，子 Agent 只返回“浓缩、提炼”的摘要，原文以路径或链接形式保存，用的时候再加载 【原文已读】([Anthropic, context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents))。

输出是一份研究简报：每条论据带 `source_id`，并标注证据等级（一手 / 二手 / 摘要级）和反方证据。工具包括网络搜索 API（Google 的 SAFE 事实核查用的是 Serper，见 [arXiv 2403.18802](https://arxiv.org/abs/2403.18802v3)）、资料库检索、需要数据时直接查原始库（学 Noah Smith 查 FRED）。

```text
[子Agent任务书]
目标：回答「{sub_question}」，服务于论点「{thesis}」。
输出：最多 8 条 finding，每条 {claim, quote_verbatim, url, source_type:
primary|secondary|aggregator, date, confidence}，外加 counter_evidence 列表。
信源优先级：作者原文/官方数据/同行评审 > 权威媒体 > 聚合站；
禁止只用聚合站支撑数字。找不到就写 "未找到证据"，不要推测。
边界：不写文章，不评价论点好坏；最多 {k} 次工具调用。
```

闸口 H2 的检查清单：

| 检查项 | 通过标准 |
|---|---|
| 关键数字有一手来源 | 每个数字至少 1 个 primary；HCR 式的高风险事实需 3 个独立来源 |
| 引语逐字可查 | `quote_verbatim` 能在原文中找到 |
| 反方证据 | 至少列出 1 条，或明确写“未找到” |
| 独家素材缺口 | 列出需要人去做的采访、调查、数据请求 |

### S3 论点与提纲（链式 + 闸口 H3）

这一步借用 Doomberg 的方法：先定标题，再给每段写一句话摘要。输入是研究简报加声音档案；输出是标题候选、一句话论点和逐段提纲，每段写明用了哪些 `source_id`，以及 Packy 式的“核心画面/图表”设想。提纲生成后先过程序检查：每段至少引用一条来源，或者标为“观点段”；论点必须是可以被反驳的。程序检查通过后才交给人。闸口 H3 由人改写或批准论点和提纲；在模式 A 下，人在这里接手写初稿。

### S4 成稿（单写手 Agent，模式 B 才启用）

只用一个写手 Agent，一次性装入声音档案、5–15 段范文、提纲和研究简报，避免多个 Agent 各写一节导致声音分裂。Anthropic 建议提示词使用精选的多样化范例，而不是罗列详尽规则 ([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents))。写手必须在文中内联标注 `[S12]` 这样的来源 ID，**没有来源就不写事实陈述**。

```text
[系统] 你在为{作者名}起草，不是替他发表。严格遵守 voice_profile 与 never_list。
范文（只学节奏与手法，禁止复用其句子）：{exemplars}
提纲（不得增删论点）：{outline}
事实只能来自研究简报，每个事实后标注 [source_id]；缺来源的地方写 [[需作者补充]]。
观点段使用作者 stances.md 中已有立场；不在其中的立场写 [[作者确认立场]]。
```

### S5 编辑与核查（评审-优化循环，干净语境；闸口 H4）

评审 Agent 不继承写手的对话历史，只读终稿、声音档案和评分标准。评审-优化模式适用于“评估标准清晰”的场景 【原文已读】([Anthropic](https://www.anthropic.com/engineering/building-effective-agents))。事实核查借用 SAFE 的思路：先把长文拆成单条事实，再逐条用搜索验证。SAFE 与人工标注的一致率为 **72%**，成本低 20 倍以上 ([arXiv 2403.18802](https://arxiv.org/abs/2403.18802v3))。72% 的一致率意味着自动核查只能做初筛，**引语和数字必须由人逐条核对**。

评审 Agent 按下表打分（每项 0–1 分外加通过/不通过；Anthropic 发现单次调用、0.0–1.0 评分加通过/不通过的 LLM 评审与人工判断最一致 【原文已读】([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system))）：

| 维度 | 自动检查方法 | 不通过阈值（建议） |
|---|---|---|
| 论点清晰度 | 评审 LLM 复述论点，与 S3 论点比对 | 复述与原论点不一致 |
| 声音匹配 | LLM 对照范文打分 + 风格统计距离（句长分布、功能词频） | 距离超出往期均值 2σ |
| AI 腔检查 | 用词黑名单 + 结构模式（见“声音档案”一节） | 每千字命中 > 3 次 |
| 论据支撑率 | 已核实论据数 / 可核查论据数 | < 100%（引语和数字）；< 90%（其他） |
| 原创性 | 与来源、往期文章的 n-gram 重叠 | 连续 8 词以上重叠且未加引号 |
| 读者收益 | “读完能做什么或理解什么”，用一句话回答 | 回答不出来 |

为了不重蹈 Packy 遇到的“几乎全给 A-”的覆辙，评审提示词里要附上 2 篇作者认为“差”的旧稿和 2 篇“好”的旧稿作为锚点，并要求对每个扣分点引用原文句子。闸口 H4 由人定稿，人工核对清单如下：所有引语逐字回到原链接；所有数字回到一手来源；涉及真实人物的负面陈述再查一遍（诽谤风险）；文末加 AI 使用说明（见“风险”一节）。

### S6 打包分发（确定性流程；闸口 H5）

这一步用工作流，不用 Agent。产出包括：2–4 个标题候选（用于 Substack 原生 A/B 测试，小列表只测 2–3 个）、副标题、导语、付费墙位置建议（Substack 支持文中付费墙，见 [On Substack](https://on.substack.com/p/new-tools-paywall-embeds/comment/3384439)）、3–10 条 Notes 草稿（金句、图表、钩子），以及给外部平台的改编版本。Notes 的目标是拉免费订阅，不是直接转化付费（依据 0.70% 的研究结果）。闸口 H5：人把稿件粘贴进 Substack 编辑器，人选标题测试方案，人按下发送。Notes 也由人在 Substack 内定时发布。

### S7 复盘学习（指标回流；闸口 H6）

每篇发布约 7 天后，人导出 Substack 的 CSV（2026 年 3 月起支持【待核实】），由脚本导入往期档案。每月一次，Agent 提出三类修改：声音档案、选题排序权重、范文库的增删；由人批准（H6）。具体方法见“评估与反馈”一节。

## 知识库与记忆：一个纯 markdown 仓库就够用

在 newsletter 这个规模，几百篇往期文章完全可以靠 Agent 用 grep/glob 按需检索，暂时不需要向量数据库。这符合 Anthropic“按需检索，用文件路径保存引用”的建议 【原文已读】([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents))，不过这一点未经实测【设计建议】。

```
creator-vault/
├── voice/
│   ├── profile.yaml          # 声音档案（结构化）
│   ├── exemplars/            # 5–15 段范文，按“开头/转折/论证/吐槽/结尾”分类
│   ├── never.md              # 禁用词与禁用结构
│   ├── stances.md            # 作者已表态的立场（声音也包括“想什么”）
│   └── edit_diffs/           # AI稿→终稿的修改对，用于反推风格
├── backlog/ideas.jsonl       # 选题池
├── swipe/                    # 摘抄库：他人佳作的结构、钩子（只学手法）
├── sources/                  # 资料库：每条来源一个 md，含原文摘录与证据等级
├── archive/posts/            # 往期文章（front matter 含指标）
├── metrics/exports/          # Substack CSV 原文件
└── runs/{post_id}/           # 每篇的流水线中间产物（简报、提纲、评审结果）
```

**声音档案**由四部分组成，按优先级排序：范文（最重要）、风格表、禁用清单、立场文件。风格表要写成可以检查的具体指标，不要写成形容词。

```yaml
# voice/profile.yaml
author: "示例作者"
identity: "前产品经理，写给 0→1 阶段的产品负责人"   # 身份
lens: "每个话题都回到：这对一个 5 人团队本周的决策意味着什么"  # 固定视角
person: first_person_singular
sentence_length: {median_words: 16, p90_words: 32}
paragraph_max_sentences: 4
signature_moves:
  - "开头用一个读者原话提问"
  - "每节结尾给一个可执行的小动作"
openers_banned: ["在当今快速变化的世界", "众所周知"]
closings: "以一个反问或下周预告结束，不做总结段"
formatting: {headers: true, bullets: sparingly, bold_key_numbers: true}
disclosure_line: "研究与校对由 AI 辅助；观点与文字出自我本人。"
```

`never.md` 可以合并 Wikipedia“Signs of AI writing”里的高频词。它自称“观察而非规则”，二手引述的词包括 *Additionally*（尤其在句首）、*crucial*、*delve*、*showcase*、*tapestry*、*testament*、*underscore*、*valuable*、*vibrant* ([Boing Boing, Aug 2025](https://boingboing.net/2025/08/20/wikipedia-publishes-list-of-ai-writing-tells.html); [mirror](https://cavac.at/cavacopedia/Wikipedia%3ASigns_of_AI_writing))。研究笔记作者凭记忆补充的结构性特征（“三连排比”、否定式平行句、滥用破折号、宣传腔）未能直接核实【待核实】。中文写作者应另建中文 AI 腔词表；研究团队**没有找到**权威的中文 AI 腔清单【未找到证据】。

## 数据结构：五个核心对象

```json
// backlog/ideas.jsonl —— 每行一条
{"id":"idea_0142","created":"2026-10-28","origin":"reader_reply",
 "raw":"读者原话：小团队要不要做用户访谈？","lens_fit":3,
 "excitement":null,"demand_signals":{"questions":4,"votes":0},
 "exclusive_access":"可约 2 位创始人访谈","status":"candidate",
 "related_posts":["post_0031"],"tags":["research","discovery"]}
```

```json
// sources/src_0871.md 的 front matter（以 JSON 表示）
{"id":"src_0871","url":"https://...","title":"...","author":"...",
 "published":"2026-09-12","retrieved":"2026-10-29",
 "source_type":"primary","read_level":"full_text|snippet",
 "quotes":[{"text":"逐字摘录","loc":"第3段"}],
 "used_in":["post_0045"],"reliability_note":"官方数据页"}
```

```yaml
# runs/post_0045/brief.yaml —— 研究简报
thesis: "小团队的用户访谈应该按周固定，而不是按项目"
findings:
  - claim: "..."
    sources: [src_0871, src_0874]
    evidence_level: primary
    verified_by_human: false
counter_evidence: ["..."]
gaps: ["需要作者本人的 3 个访谈案例"]
```

```json
// archive/posts/post_0045.md 的 front matter
{"id":"post_0045","published":"2026-11-02T08:41","format":"flagship",
 "title_variants":[{"t":"我访谈了 40 个小团队…","share":0.5,"won":true},
                   {"t":"小团队别再按项目做访谈","share":0.5,"won":false}],
 "word_count":2300,"paywall_at":"section_3","ai_mode":"A",
 "metrics_d7":{"recipients":8120,"open_rate":0.41,"click_per_open":0.07,
   "new_free":96,"new_paid":3,"unsubs":11,"comments":18,"restacks":22},
 "human_edit_minutes":95,"edit_distance_ratio":0.38,
 "judge":{"voice":0.82,"support_rate":1.0,"ai_tells_per_1k":1.2}}
```

```json
// runs/post_0045/eval.json —— 评审结果
{"pass":false,"scores":{"thesis":1,"voice":0.71,"ai_tells":0.6,
 "support":0.92,"originality":1,"payoff":1},
 "blocking":[{"dim":"support","sentence":"……增长了 3 倍","fix":"补一手来源或删除"}],
 "anchored_to":["post_0012(bad)","post_0031(good)"]}
```

## 评估与反馈：二十条测试集起步，人工修改量是最便宜的质量信号

**离线评估**：不需要等到有几百条用例。Anthropic 用**约 20 条**代表性查询就看到了明显效果 【原文已读】([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system))。做法是从往期文章里选 20 篇，包括 10 篇作者满意的和 10 篇不满意的，逆向构造它们的选题、简报、提纲作为输入，每次改提示词后重跑 S3–S5，比较评审分数和作者的盲评。系统提示词从最简版本开始，出现失败再加指令 【原文已读】([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents))。

**在线指标**分三层。第一层是质量，也是成本最低的信号：**人工编辑时长**和**AI 稿到终稿的编辑距离比**。两者持续下降，说明 Agent 在变好；如果下降的同时读者指标也在变差，说明作者在“放水”。第二层是读者，看打开者点击率、评论数、转发（restack）数。打开率受邮箱隐藏打开的影响，只适合看趋势。第三层是商业，看新增免费订阅、免费转付费（按 2–3% 做基准）和退订数。

**反馈闭环**：每月由 S7 Agent 生成复盘，包括表现前 20% 文章的共同特征（栏目形式、角度类型、开头手法）、`edit_diffs` 里反复出现的修改（比如作者总把“此外”删掉，就加进 never.md），以及提议的排序权重调整。作者批准后才写回知识库。表现好的文章，其段落可以经作者同意晋升为范文。研究团队**没有找到**任何 newsletter 作者把文章数据接回提示词调优的公开案例【未找到证据】，所以这个闭环属于【设计建议】，需要自己验证。要警惕古德哈特定律：只按打开率优化标题会侵蚀声音和信任，所以声音档案的修改永远由人一票否决。

## Substack 工具现实：只能读，不能写，最后一步必须由人点

**没有官方的发文、草稿或订阅者管理 API。** 据第三方描述，Substack 的官方 Developer API 范围很窄（查询公开的创作者资料），需要人工审批申请，接受 API 使用条款（2026 年 1 月 8 日更新），上线时间有“2026 年初”和“2026 年 4 月”两种说法【待核实】([Substack API ToS](https://substack.com/api-tos); [dev.to](https://dev.to/equinoxaifinancergb/does-substack-have-an-api-2026-and-what-you-can-actually-get-29il))。只有一个来源称，2026 年 7 月起有一个仅限 Bestseller 刊物的官方只读 MCP 端点，另一说法是 CEO 当时称其“即将推出”【待核实】([smtpedia](https://smtpedia.com/platforms/substack/api/))。**最稳的读取路径是公开 RSS**（`<pub>.substack.com/feed`），可以拿来同步自己的往期档案，也可以跟踪同行 ([smtpedia](https://smtpedia.com/platforms/substack/api/))。官方 API **不提供**分析数据，指标只能从后台看或导出 CSV ([dev.to](https://dev.to/equinoxaifinancergb/does-substack-have-an-api-2026-and-what-you-can-actually-get-29il))。

**非官方 API 有封号和违约风险。** 非官方的发文 API 和 MCP server 都靠浏览器会话 cookie（`substack.sid`）认证，遇到 401/403 就要刷新，稳定性差，而且部分评测页面是自我推广 ([aiindigo review](https://aiindigo.com/blog/review-unofficial-substack-posting-api-2026-edition); [Noah-Bjorner/SubstackAPI](https://github.com/Noah-Bjorner/SubstackAPI))。据第三方条款追踪站，Substack 的使用条款禁止抓取和爬取 ([ConductAtlas](https://conductatlas.com/platform/substack/substack-terms-of-use/provision/CA-P-029302/prohibition-on-scraping-or-crawling-substack/))。条款是否明确禁止用会话 cookie 自动发文，研究团队未能核实【未找到证据】。建议的做法是：Agent 只输出可以直接粘贴的 markdown 或 HTML。如果一定要自动化，用 Playwright 在作者已登录的会话里**只创建草稿、绝不发送**，同时接受这条路随时可能失效的风险。研究团队**没有找到** Substack 支持“邮件发文”的证据【未找到证据】。

**AI 政策（按报道）。** Axios 2026 年 7 月 23 日报道，Substack 押注“读者愿意为人写的内容付费”，引入了基于 **Pangram** 的检测，给出 AI 与人写的百分比评分，引发部分创作者“猎巫”式的反弹 ([Axios](https://www.axios.com/2026/07/23/substack-subscribers-ai-generated-content-pangram); [Artiverse](https://www.artiverse.ca/substacks-ai-detection-sparks-backlash-and-debate-on-transparency/))。检测结果是只给读者看、作为标签，还是会影响分发，研究团队**未能核实**。一条法语标题称 Substack“禁止 AI 生成的 newsletter”【待核实】([munci.org](https://www.munci.org/substack-bannit-les-newsletters-generees-par-lia/))；2026 年 5 月又有标题称“Substack 正在向 AI 开放”，可能指的是工具层面而非内容政策【待核实】([pulse.bot](https://www.pulse.bot/ai/news/substack-is-opening-up-to-ai-b2f22f31-de42-4fdd-a374-cf1b552c1f09/))。更早的 2025 年报道称 Substack 没有限制 AI 使用的官方政策 ([Tubefilter](https://www.tubefilter.com/2025/07/25/substack-publisher-creator-survey-generative-ai/))，可见政策在 2025 到 2026 年间明显收紧。对 Agent 设计的含义是：**最终发出的文字应以人写为主**，AI 主要放在研究、提纲、核查和改编分发环节。

## 风险：幻觉、声音同质化和读者信任，各配一道闸

**幻觉。** 最高风险是捏造引语和统计数字，因为它们会直接损害信任，还可能构成诽谤。对应的三道防线是：写手“无来源不写”；核查 Agent 重新打开原链接，确认论据确实出现在原文里；人在 H4 逐条核对引语和数字。另外要警惕“源头本身就是摘要”：如果资料库里某条来源的 `read_level` 是 `snippet`，它就不能单独支撑一个数字。本报告自身的证据状况就是一个现成的例子。

**声音同质化。** 这是有实证的默认风险，不是假设。对照实验发现，LLM 改写人类文本会**降低风格方差** ([arXiv 2502.11266](https://arxiv.org/pdf/2502.11266))；2,200 篇申请文书的研究发现，LLM 能提升个人创意，但会**缩小群体的观点多样性** ([Stanford SCALE](https://scale.stanford.edu/ai/repository/homogenizing-effect-large-language-models-llms-creative-diversity-empirical))；2026 年的预注册随机对照实验发现，高度依赖 AI 草稿的参与者写出的故事更趋同 ([arXiv 2604.03529](https://arxiv.org/html/2604.03529v1))。对策有四条：默认采用模式 A；范文库要多样，并且每季度更新；风格统计距离作为 S5 的硬性闸口；摘抄库只学结构，不学句子。

**读者信任。** 据二手报道，Reuters Institute 2025 年的报告显示，只有 **12%** 的人能接受完全由 AI 生成的新闻，**62%** 更偏好人写；人主导、AI 辅助的接受度升到 **43%**。人们认为 AI 只是“辅助”时，披露的重要性远低于 AI“生成内容”时【待核实，二手报道】([NewscastStudio, Oct 2025](https://www.newscaststudio.com/2025/10/16/public-use-of-generative-ai-grows-but-trust-and-comfort-with-news-applications-remain-low))。Substack 2025 年的 AI 报告（2,000 多名出版者参与）显示，约 52% 使用生成式 AI，主要用于研究（64.9%）和头脑风暴（56.4%），而非成稿；另一家媒体给出的采用率是 45.4%，数字互相矛盾【待核实】([Tubefilter](https://www.tubefilter.com/2025/07/25/substack-publisher-creator-survey-generative-ai/))。由此建议在文末写一行简短的披露，例如“研究与校对由 AI 辅助；观点与文字出自我本人”。它成本很低，但效果没有针对 newsletter 的 A/B 证据【设计建议】。

**其他风险。** 一是信源质量：Agent 偏爱 SEO 内容农场，需要信源白名单和启发式规则 ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system))。二是成本：多 Agent 研究约耗 15 倍 token，只适合每周的旗舰文章，日常分拣用单次调用。三是平台风险：非官方 API 可能导致封号。四是价值错位：Newton 的转向提醒我们，AI 能做的聚合恰恰在贬值，Agent 省下来的时间应该投入采访、调查和原创数据。

## 分阶段实施路线：从一个脚本到带闸口的流水线

| 阶段 | 时间 | 范围 | 完成标准 |
|---|---|---|---|
| **P0 建库** | 第 1–2 周 | 用 RSS 导入全部往期文章到 `archive/`；人工挑 10 段范文；写 `profile.yaml`、`never.md`、`stances.md`；把手头的选题想法录入 `ideas.jsonl` | 作者读 `profile.yaml` 时觉得“这就是我”；选题池有 30 条以上（Lenny 的规模） |
| **P1 MVP** | 第 3–6 周 | 不用框架，单个脚本串起 S1（角度生成）→ S3（提纲）→ S5（评审 + AI 腔检查）→ S6（标题与 Notes 草稿）；研究用单 Agent 加搜索；全部人工粘贴发布 | 连续 4 周按固定节奏发出；20 条离线测试集建好；记录每篇的人工编辑时长 |
| **P2 取证与回流** | 第 7–12 周 | S2 升级为编排者-工作者加引用绑定；S5 加入 SAFE 式逐条核查；CSV 指标导入；`edit_diffs` 采集；首次月度复盘（H6） | 引语和数字的人工核对 100% 覆盖；论据支撑率 ≥ 95%；人工编辑时长较 P1 下降 |
| **P3 进阶** | 第 4–6 个月 | 用 LangGraph 加持久化 checkpointer 实现 H1–H6 的 `interrupt()`；风格统计距离闸口；选题排序权重按数据自动提议；Readwise 和语音备忘录自动分拣；（可选，有风险）Playwright 只建草稿 | 声音距离无漂移；作者盲评 AI 参与的稿件不低于纯人写稿件；没有任何一次未经人工按键的发送 |
| **P4 扩展（按需）** | 6 个月后 | 读者调查设计与分析（学 Lenny/Segal、Orosz/Nilsson）；mailbag 投票自动化；Recording Studio 和直播的改编分发 | 每季度至少产出 1 份基于专有数据的旗舰文章 |

每一阶段都遵循同一条规则：**只有在离线测试集上证明有提升，才增加复杂度**。比如在 P1 证明单 Agent 研究确实漏掉了关键信息之前，就不上多 Agent。

---

## 结论

头部 Substack 作者的方法论里，真正难以复制的是三样东西：作者身份带来的固定视角、远大于产出的阅读量，以及独家信源和专有数据。容易交给机器的部分，比如素材分拣、选题清单维护、提纲检查、逐条核查和改编分发，恰好是他们公开描述中最机械、最耗时的环节。所以，一个好的创作 Agent 衡量的不是它能写出多少字，而是它为作者腾出了多少时间去做那三件难以复制的事。Casey Newton 2026 年转向独家报道、Substack 同年引入 AI 检测，都在把市场往同一个方向推：可替代的内容在贬值，人本身的署名和判断在升值。

还有一个反直觉的结论：当前证据最薄弱的环节，正好是 Agent 最想优化的那些指标，包括标题公式、发送时间、文章特征与付费转化的关系。这几项基本只有个人经验，没有大样本研究。因此，本手册的反馈闭环应该被当作作者自己的小样本实验平台，而不是可以直接套用的行业规律。另外，本报告的创作者证据几乎都来自搜索摘要。在把任何一条引语写进自己的文章之前，请先回到原链接核对。这也正是手册里 H4 闸口要求作者做的事。
