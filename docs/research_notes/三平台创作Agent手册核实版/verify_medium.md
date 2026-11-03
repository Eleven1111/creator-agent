# Medium 相关论断核实（针对《Substack X Medium创作Agent手册》）

核实日期：2026-11-03。访问情况：
- help.medium.com 的 HTML 页面返回 **403**（Cloudflare），但 Zendesk 公共 API `https://help.medium.com/api/v2/help_center/en-us/articles/{id}.json` 返回 **200**，拿到的是帮助页全文、`edited_at` 和 `updated_at`。下文引用帮助页时都给 `html_url`，日期取 API 的 `edited_at`（即正文最后一次编辑）。
- medium.com 的文章页：curl 加浏览器 UA 返回 **403**；WebFetch 返回 `ENOTFOUND`（WebFetch 的网络里仍未放行 medium.com）。**RSS 可用**：`https://medium.com/feed/blog`、`https://blog.medium.com/feed`，以及按标签过滤的 `https://medium.com/feed/blog/tagged/{partner-program|boost|medium-partner-program}`，都返回 200，`content:encoded` 里是**全文**。下文 Medium 博客的引用都来自 RSS 全文，日期取 RSS 的 pubDate。
- techcrunch.com：curl 返回 200，可读。towardsdatascience.com：403（Cloudflare 的“Just a moment”页）。

---

## 关键问题 1：每条论断的核实结论（确认 / 修正 / 推翻 / 仍无法核实），附原文、URL 与页面日期

### Takeaway
多数**机制性**论断都得到确认，但有四处必须改：
1. **Boost 提名计划已于 2026-05-31 关闭**，“约一半 Boost 来自出版物编辑提名”、“每月自荐 2 篇”、“超过 6 个月不能提名”三条一并作废；对应的两个帮助页已经 404。
2. “Friend Link 带来的阅读不算钱”**被推翻**：会员通过 Friend Link 阅读照样计入收入。
3. “披露过的 AI 文字可以获得 General Distribution”与现行《Distribution Guidelines》（2026-06-29 版）矛盾。现行指南把“AI-generated content”列为**取消 General Distribution 资格**的低价值内容；AI 政策页还新增了一条：AI 辅助写成的文字也必须披露。
4. 分档名称的现行写法是“Network Distribution”，“Network Only”只是旧称和 AI 政策页里的用词。

### Cited Findings

#### 第一部分 › “Medium：人工策展决定上限……” › 三档分发（Network Only / General / Boost）
- **结论：确认，但名称需修正。** 现行《Distribution Guidelines》（页内写“Updated: June 29, 2026”，API 显示 edited_at 2026-06-29）原文：“We categorize stories on Medium into one of three distribution categories: **Network Distribution** —stories that are matched to readers who are following that specific writer… This is the baseline category for any story on Medium which does not violate Medium rules. **General Distribution** — matched to readers based on their interests… **Boost** —especially high-quality stories that meet our Boost Guidelines… These get a higher priority in being matched to readers and are also given General and Network Distribution.” — [Help: Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution)
- 报告引用的 360018677974 号文章，标题已改为 “What happens to your story when you publish on Medium”（edited 2025-09-10），原文：“By default, all stories published on Medium are eligible for general distribution via our recommendations algorithm (we do filter for spam, NSFW, etc)”，并保留“Network only”小节：“we will also remove low-quality stories from distribution to Medium's network, though they will still be distributed to the writer's personal network.” — [Help: What happens to your story](https://help.medium.com/hc/en-us/articles/360018677974-What-happens-to-your-story-when-you-publish-on-Medium)
- 2023 年博客里的旧名：“Network Only: Stories that are not Boosted nor in General Distribution…”（2023-08-10）— [Medium Blog: Updated Guidelines for Boost](https://medium.com/blog/updated-guidelines-for-boost-47799aad8899)
- 新细节：“We can only review stories written in English at this time, so unfortunately stories in other languages will not be Boosted or be given General Distribution yet.” 这一条对中文作者是硬约束，报告漏了。— [Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution)

#### 同节 › “约一半 Boost 来自受邀出版物编辑提名，另一半由内部策展团队挑选；普通作者不能提名；提名人每月最多自荐 2 篇；超过 6 个月不能提名；被拒无反馈、不能申诉”
- **结论：推翻（已过时）。** Medium 博客（2026-05-06）原文：“we found the program couldn't scale, and it limited the kinds of stories we could reward editors for, so **we'll be closing the Boost Nomination Program on May 31st, 2026**.” 又说：“The way we review stories for Boost is staying the same… The publications you know and love working with are already one of our main sources for finding stories to Boost, so your best bet remains submitting your story to a high quality publication and working with an editor.” — [Medium Blog: An update on the Boost Nomination Program, and what's next](https://medium.com/blog/an-update-on-the-boost-nomination-program-and-whats-next-40331b1a9c0a)
- 报告引用的两个帮助页 26729526741399（Participation）和 26716107269527（How do I nominate），以及 section 26573008251543（Nominations），Zendesk API 都返回 `{"error":"RecordNotFound"}`，说明已删除。
- 现行指南只写：“Our human curation team reviews stories seven days a week… **We review stories we discover through our own internal curation tools.**”（2026-06-29）— [Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution)
- 正确的现行说法：Boost 全部由 Medium 内部策展团队决定；进入高质量出版物仍是被发现的主要途径（官方说法）；提名配额和 180 天上限已不存在。`platforms/medium.yaml` 里的 `boost_self_nomination_per_month` 和 `boost_max_story_age_days` 两项应删除。
- 另有一个报告没提到的出版物机制：编辑可以用配额（token）在出版物里 “Feature” 文章（“you will not earn a token back and will need to wait until the Publication's next allotment”，edited 2026-09-18）。这是出版物内的推荐，不是 Boost。— [Help: How to feature a story in your publication](https://help.medium.com/hc/en-us/articles/28221990368791)

#### 同节 › Boost 标准“读者的生活是否因此更丰富”“原创、人写、探讨此前未知或少有人审视之物”
- **结论：修正。** 后半句是 **2023 年 8 月**版的措辞。2023-08-10 博客原文：“Is it original, human-created content? The story is original in that it explores something previously unknown or not frequently examined, or it re-examines something we think we know a lot about…” — [Medium Blog (2023-08-10)](https://medium.com/blog/updated-guidelines-for-boost-47799aad8899)
- 现行版（2026-06-29）的结构改成五项：Writer's experience / Value and impact / Respect for the reader / Non-derivative / Writing and craftsmanship。原文分别是：“The reader's life is enriched by reading the story”（**确认**）；“The story is human-created and does not appear to be generated by Artificial Intelligence, a large language model, or other text-generating technology”（现归在 Writer's experience 下）；“Non-derivative: The writer brings a fresh perspective, something new, or re-examines something with new insight… It doesn't just paraphrase, recombine, or rehash information that is easily found elsewhere.” 新增：“The writer has credible, first-hand experience with the subject… This is a more important element than the credentials a writer may claim.”；“Republished translations of work from other sources are not eligible for Boost.” — [Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution)

#### 同节 › “标题、副标题、封面图语境不够就不 Boost”
- **结论：确认（逐字）。** 原文：“We will not Boost a story if we don't believe the title, subtitle, and cover image provide enough context about the story to appeal to readers in the feed.” 同页还写：“Being overly generic, mysterious, or formulaic is just as bad as being sensationalistic”；“AI-generated cover art sometimes works (if properly credited as such) but is often a turn-off”；“using no cover image can be better than using a poorly chosen one.”（2026-06-29）— [Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution)

#### 第二部分 › 创意第四条“Medium 的指南称赞‘直接基于作者经历’的内容”；创作节“官方说篇幅要服务于故事本身”
- **结论：确认。** 原文：“all original content based directly on the writer's experience”（出自 Boosted 示例点评），以及“The length of the story is appropriate and serves the purpose and context of the story itself. Well-crafted stories can be short or long.” — [Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution)

#### 同节 › MPP 计算：30 秒算一次阅读、闲置不计、Boost 倍率更高、非会员和 Friend Link 的阅读不算钱
- **30 秒阅读：确认。** “A member read is counted when a paying member reads or listens to your story for 30 seconds or more.”（edited 2026-03-18）— [Help: MPP earnings calculation](https://help.medium.com/hc/en-us/articles/360036691193-Medium-Partner-Program-earnings-calculation)
- **闲置不计：确认。** “idle time is not counted.”（同页）
- **Boost 倍率：确认，但已削弱。** “Stories that are Boosted earn engagement points at a higher rate… Non-boosted stories now receive a larger share of Partner Program earnings than before.”（同页）
- **“每种互动只在第一次计分”：仍无法核实。** 现行页没有这句话，只写“combined with the number of claps, highlights, and replies your story receives from members”。
- **非会员阅读不算钱：确认。** “non-members' reads will still not contribute to them.”（同页）
- **Friend Link 阅读不算钱：推翻。** 原文：“**Can I still earn through a Friend Link? Yes. Reads from a Friend Link are treated the same as regular reads.** Members who read your story through the Friend Link will still contribute to your earnings.”（同页）
- 现行公式还有报告漏掉的新项，见关键问题 3。

#### 同节 › “2025 年 10 月起 5% 转给站外流量；11 月起 15% 转给搜索进站的会员阅读”
- **结论：确认。** 2025-09-30 博客原文：“The change shifts **5% of the payouts** toward stories that get this external traffic and especially to external traffic that converts to members.” 生效日期为 10 月 1 日。— [Medium Blog: Starting October 1, rewarding external traffic](https://medium.com/blog/partner-program-update-starting-october-1-were-rewarding-external-traffic-15cb28f75bc9)
- 2025-11-03 博客原文：“This month, we're shifting **15% of the Partner Program budget** to activity on stories that members discover through search engines like Google.” 该文还写明：“Will this affect earnings on stories published before November 1? Yes”。— [Medium Blog: Starting November 1, rewarding search traffic](https://medium.com/blog/partner-program-update-starting-november-1-were-rewarding-search-traffic-3ac0635f9f6b)
- 现行帮助页对两项的表述：“A 5% bonus is applied to member reads that come from outside Medium”；搜索流量是“An additional share of the Partner Program budget”，没写具体的 15%。— [Help: earnings calculation](https://help.medium.com/hc/en-us/articles/360036691193-Medium-Partner-Program-earnings-calculation)

#### 同节 › “2026 年 1 月把 Boost 稿的收入分散；2 月 17 日起奖励带来新会员的付费墙文章；6 月 1 日起推出 Editor Partner Program”
- **1 月：确认。** 2026-01-13 博客原文：“we have spread the Partner Program earnings that typically go to Boosted stories more broadly beyond Boosted stories… On average, stories that are not Boosted will now earn more than they did before. Boosted stories will still earn at a higher rate than unboosted stories, but not as much.” — [Medium Blog: Starting January 1](https://medium.com/blog/partner-program-update-starting-january-1-were-rewarding-writing-more-broadly-4907e149e38c)
- **2 月 17 日：确认，需补细节。** 2026-02-18 博客原文（含 2/24 的更新）：“when a user becomes a member after hitting the paywall on your story, you'll earn a **small, one-time amount** of that new member's membership fee. In the previous referral program, about half of the new member's membership fee went to the writer every month.” 又写：“a small percentage of Partner Program funds are now going toward conversions”，并且“We are excluding members who quickly cancel”。— [Medium Blog: Starting February 17](https://medium.com/blog/partner-program-update-starting-february-17-were-rewarding-stories-that-bring-in-new-members-3e84d2eb6e68)
- **6 月 1 日 EPP：确认，需补细节。** 2026-05-05 博客原文：“when a publication editor in a qualifying publication assigns themselves to a story in the publication submission queue, that editor earns **25%** of what the story earns. The writer will keep all their original earnings.” 6 月先向少量出版物开放，7 月扩大。— [Medium Blog: Starting June 1](https://medium.com/blog/partner-program-update-starting-june-1-were-rewarding-editors-for-stories-they-edit-aaec12a97cea)
- 2026-07-01 博客原文：“Over 100 publications and 300+ editors qualify… New publications can join the Editor Partner Program at the start of every month as they qualify.” — [Medium Blog: New: A program to pay publication editors](https://medium.com/blog/new-a-program-to-pay-publication-editors-d9c4f1ed40d8)
- **报告漏掉了第三项调整（2025-12-01，邮件通知）。** 2025-12-02 博客原文：“If a member comes to Medium to read that story because you sent it to them in an email notification, you'll earn slightly more for that member engagement than if they had found that story on Medium through the app or website.” — [Medium Blog: On December 1, rewarding email notifications](https://medium.com/blog/partner-program-update-on-december-1-were-rewarding-email-notifications-4910c47d4cb7)。这个系列共六项：10 月站外流量、11 月搜索、12 月邮件通知、1 月非 Boost 稿、2 月新会员转化、6 月编辑（官方称 EPP 为“our sixth Partner Program update”）。

#### Editor Partner Program 的资格与规则（报告只提一句，这里给现行原文）
- “As an editor, you earn 25% of a writer's monthly earnings for every paywalled story you claim in your publication. This doesn't affect the writer's pay.”
- 一般条件：“The publication owner must be enrolled in the Partner Program. The publication must have the 'open to all' submission mode.”
- 月度条件：“The paywalled stories in the publication must earn at least $200 dollars collectively… The publication must publish at least one story and no more than 100 stories… The publication must publish a story from at least two writers.”
- “To qualify, a publication must meet the monthly requirements for three out of six months.”
- “Editing your own stories does not qualify for earnings.”（edited 2026-09-10）— [Help: EPP eligibility and overview](https://help.medium.com/hc/en-us/articles/40661484998679-Editor-Partner-Program-eligibility-and-overview)
- “There's no cap on editor earnings… You earn on all paywalled stories you've claimed in your publication — not just curated or boosted ones.”（edited 2026-09-29）— [Help: How editor earnings work](https://help.medium.com/hc/en-us/articles/40661926684055-How-editor-earnings-work)

#### 同节 › Partner Program 公式 2023 年 8 月的改动（任务列出，报告正文只引了 Vocal）
- **结论：部分确认。** 2023-08-12 博客原文：“we've made changes so that earnings are determined by more meaningful engagement metrics.” — [Medium Blog: Partner Program Updates, Part II: Stats Edition](https://medium.com/blog/partner-program-updates-part-ii-stats-edition-194ddd7c016c)。Part I（2023 年 7 月公告、8 月 1 日生效）没在 RSS 里，未能直接读到。
- **“2023 年收入 ≥$10 的作者中约 65% 在 $10–$100”：仍无法核实。** 只有 Vocal 的二手转述，未找到官方原文。

#### 同节 › MPP 资格（任务要求核实；报告未写现行条件）
- **现行原文：** “You are a Medium member with an active membership subscription. You have published at least 1 story. You have a complete profile. Your bank is located in a country that is eligible for payouts. You are 18 years of age or older. You agree to the Medium Partner Program Terms. You agree to the Content eligible for the paywall policy. When you meet all requirements, you can enroll right away.”（edited 2026-09-24，列出约 120 个国家和地区，**中国大陆不在列**，香港、澳门、台湾在列）— [Help: MPP eligibility](https://help.medium.com/hc/en-us/articles/39121627791639-Medium-Partner-Program-eligibility)
- 2026-08-26 博客原文：“The Partner Program is open again, now with a faster and easier enrollment process… you don't need to fill out an application and wait for a response.” — [Medium Blog: The MPP is open again](https://medium.com/blog/the-medium-partner-program-is-open-again-now-with-a-faster-and-easier-enrollment-process-96c01f0e0670)。“open again”说明此前有一段时间改为申请制或暂停；具体起止时间未能核实。

#### 同节 › CEO 称 Medium 是“联合发布、给其他平台做增长”的地方（Medium Handbook，2026）
- **结论：仍无法核实。** 原帖在 medium.com 上，文章页 403，Medium Handbook 的 RSS 也没有抓。

#### 同节 › AI 政策：2024-05-01 起 AI 文字不能设付费墙；披露过的可进 General、不能 Boost；未披露的只有 Network Only；屡次违规可能被取消 MPP
- **不能设付费墙：确认。** 现行 AI 政策页（edited 2026-04-29，created 2024-04-04）原文：“AI-generated writing (disclosed as such or not) is not allowed to be paywalled as part of our Partner Program. Accounts that have fully-generated AI writing behind the paywall may have those stories removed from the paywall, and/or have their Partner Program enrollment revoked.” — [Help: AI content policy](https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy)。现行页没有写“2024 年 5 月 1 日”这个生效日。
- **未披露只有 Network Only：确认。** 原文：“Undisclosed AI-generated writing will be given Network Only distribution.”（同页）
- **“披露过的 AI 文字可获 General Distribution”：推翻（按现行指南）。** 现行 AI 政策页已不写这句。现行《Distribution Guidelines》在 “What disqualifies a story from General Distribution?” 的 Low-value content 下逐字列出：“**AI-generated content**”。— [Distribution Guidelines (2026-06-29)](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution)。所以报告怀疑的“可能是后来收紧了”属实：AI 生成的文字即使披露了，也只拿 Network Distribution，不能 General，更不能 Boost。原 Nominations 帮助页已经 404，那句“不具备分发资格（更别说 Boost）”无法再读原文，但它和现行指南一致。
- **“屡次违规可能被取消 MPP”：修正。** 现行措辞没有“屡次”这个条件，原文是“may have those stories removed from the paywall, and/or have their Partner Program enrollment revoked”。
- **“AI 生成”的定义：确认，这是官方原文，不只是 zidailma 的转述。** 原文：“writing where the majority of the content has been created by an AI-writing program with little or no edits, improvements, fact-checking, or changes. This does not include AI writing tools such as AI outlining, or AI assisted fact, spelling, or grammar checkers.”（同 AI 政策页）
- **新增，报告漏了：AI 辅助也要披露。** 原文：“We require that any story incorporating AI assistance be clearly labeled as such. AI-assisted text without a disclosure will similarly be restricted to distribution on the author's personal network.” FAQ 又说语法、拼写、提纲和事实核查工具不用披露：“You must disclose if you are using text or images generated by AI”。披露方式：“include a simple sentence within the first two paragraphs. For example, 'This story was written with the assistance of an AI writing program.'” 检测方式：“a wide variety of tools and technologies… combined with human review of any positive results.”（同页）
- 同页其他禁令：禁止用 AI 改写他人内容形成近似衍生作品（按剽窃处理）；禁止“easily disprovable AI-hallucinated stories, statistics, events”；禁止为 SEO 和联盟链接批量生成的 AI 内容。
- 付费墙政策页（edited 2026-09-24）重申：“Stories where the majority of the content has been generated by an AI writing tool, with little or no human editing, fact-checking, or original contribution, are not eligible for the paywall.” — [Help: Content eligible for the paywall policy](https://help.medium.com/hc/en-us/articles/31090080813591-Content-eligible-for-the-paywall-policy)

#### 同节 › API 已停止支持；2025 年 1 月 1 日起不再发新 token，旧 token 仍可用（据 StackOne）
- **结论：修正，官方来源可以取代厂商文档。** 帮助页 “API/Importing”（edited 2024-12-17）原文：“Medium will not be issuing any new integration tokens for our API and will not allow any new integrations. **All existing tokens will continue to work.**” — [Help: API/Importing](https://help.medium.com/hc/en-us/articles/213480228)。官方页没有写“2025 年 1 月 1 日”这个具体日期，只能说 2024 年 12 月起官方已公告。
- “API no longer supported”这句报告读的是 GitHub 原文，本次未重读（报告标为【原文已读】）。

#### 同节 › Import 工具回溯日期并自动加 canonical；手动粘贴不带 canonical
- **结论：确认。** 原文：“Using the import tool will automatically backdate the post to the original date, as well as add a canonical link to make sure your SEO won't be penalized… Imported stories will automatically apply a canonical URL referencing the original source material.” 现行入口是“On your homepage, click **Stories** in the left rail menu. Click **Import a story**”（edited 2026-08-26）— [Help: Importing a post](https://help.medium.com/hc/en-us/articles/214550207-Importing-a-post-to-Medium)
- 手动设置的原文：“Medium's official tools for cross-posting add the source it is importing from as the canonical link automatically, but you can also add your canonical link manually.” 路径是：three-dot → More settings → Advanced Settings → “This story was originally published elsewhere” → Save canonical link。另有一句：“**Only the story's author can set a canonical link.**”（edited 2025-05-06）— [Help: Set a canonical link](https://help.medium.com/hc/en-us/articles/360033930293-Set-a-canonical-link)。报告写的设置名“Customize canonical link”应改为上面的实际路径。
- 现行指南原文：“(The story does not need to be originally published on Medium… Syndicating your own work from other platforms is a great idea!)” 联合发布的内容可以拿 Boost，但“Republished translations of work from other sources are not eligible for Boost.” — [Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution)

#### 同节 › 盈利与会员：2024 年 8 月首次月度盈利并一直保持；2024 年 4 月付费会员超过 100 万
- **盈利：确认。** TechCrunch（datePublished 2025-07-11T10:32:53-07:00）原文：“Medium CEO Tony Stubblebine announced on Friday that the publishing platform has remained profitable since August of last year, when it first achieved this milestone… the company was losing $2.6 million per month when he joined in 2022… When he joined as CEO, Medium's membership had topped 760,000.” — [TechCrunch 2025-07-11](https://techcrunch.com/2025/07/11/mediums-ceo-explains-what-it-took-to-stop-losing-2-6m-monthly/)
- TechCrunch 2024-08-21 的标题“August was Medium's first profitable month — ever”经 JSON-LD 确认（datePublished 2024-08-21）。— [TechCrunch 2024-08-21](https://techcrunch.com/2024/08/21/august-was-mediums-first-profitable-month-ever/)
- **100 万会员（2024 年 4 月）：确认，摘要级。** 搜索摘要显示 TechCrunch 2024-08-21 写“over a million subscribers as of April”，Medium 博客也有一篇 “Thank you for one million members”。两处正文都没有逐字读到。— [TechCrunch 2024-08-21](https://techcrunch.com/2024/08/21/august-was-mediums-first-profitable-month-ever/); [Medium Blog](https://blog.medium.com/thank-you-for-one-million-members-d0b39d1be8b3)。没有找到更新的官方会员数。

#### 第三部分 › G-MD 闸口“标签最多 5 个”“策展人看不到标签”（Zulie @ Medium）
- **结论：仍无法核实。** Help Center 搜索没有找到 5 个标签上限的现行说明，Zulie 那句话的原帖也没读到。现行指南只说滥用标签（topic spamming）会失去 General Distribution 资格。

#### 第二部分 › Medium 作者事实（Denning、Awosika、Rane、Ashley、Kuegler、Cole、Günel、Göke、Foroux、Hardy）
- **结论：基本仍无法核实。** 作者个人 RSS（`medium.com/feed/@user`）只返回最近 10 篇，报告引用的老文章不在其中，文章页又 403，所以引语没能逐字核对。只能确认这些账号的活跃状态（RSS pubDate）：
  - Tim Denning（@timdenning）：最近一篇 Medium 文章是 **2024-12-09**，此后没有再发。这与报告用 timdenning.com 和 Substack 作来源相符，说明他已离开或停更 Medium。— [RSS](https://medium.com/feed/@timdenning)
  - Tom Kuegler（@tomkuegler）：最近一篇是 **2023-08-17**，与报告“全押 Substack”的说法一致。— [RSS](https://medium.com/feed/@tomkuegler)
  - Zulie Rane（@zulie）：最近一篇 2026-09-21，仍活跃。— [RSS](https://medium.com/feed/@zulie)
  - Shannon Ashley（@Shesreallyfat）：最近一篇 2026-10-26，仍活跃。— [RSS](https://medium.com/feed/@Shesreallyfat)
  - Nicolas Cole（@nicolascole77）：近 10 篇集中在 2026-09-17 至 10-01，仍在发。— [RSS](https://medium.com/feed/@nicolascole77)
  - Darius Foroux（@dariusforoux）：最近一篇 2026-11-03，非常活跃。— [RSS](https://medium.com/feed/@dariusforoux)
  - Benjamin Hardy（@benjaminhardy）：最近一篇 2026-08-06，发文稀疏（10 篇跨越 2022-01 到 2026-08）。— [RSS](https://medium.com/feed/@benjaminhardy)
  - Ayodeji Awosika（@ayotheauthor）、Sinem Günel（@sinemgunel）、Niklas Göke（@niklasgoeke）：用这些猜测的用户名查 RSS，没有返回内容，**未能确认**（可能是用户名不对）。
- **Towards Data Science 独立：确认，摘要级。** TDS 自己的公告（站点 403，内容来自搜索摘要和 AI Singapore 的转载索引）称新站于 **2025 年 2 月 3 日**上线；原因是“Medium began redirecting content from our custom domain at the end of January 2025”；此前（2024 年）Insight Media Group 收购了 TDS。— [TDS announcement](https://towardsdatascience.com/towards-data-science-is-launching-as-an-independent-publication/); [Medium: Insight Media Group acquires TDS](https://towardsdatascience.com/community-announcement-insight-media-group-llc-acquires-towards-data-science-publication-fc1adcb3e378)。正文未能逐字读到。

### Inferences
- 报告里 `platforms/medium.yaml` 的 `verification_level: snippet` 现在大部分可以升为 full_text（来源是 Zendesk API 和 RSS 全文）。需要改的配置项：
  - 删除 `boost_self_nomination_per_month` 和 `boost_max_story_age_days`；
  - `ai_disclosed_distribution` 应设为 network（不是 general）；
  - 新增 `ai_assisted_text_requires_disclosure: true`；
  - 新增 `non_english_general_distribution: false`；
  - 新增 `friend_link_member_reads_count: true`；
  - `payout_extra` 补上 email_notification、new_member_conversion 和 read_ratio_adjustment；
  - 新增 `meta_about_medium_paywall: false`。
- 对中文作者，“非英文不进 General、不进 Boost”，加上中国大陆银行不在 MPP 国家列表里，意味着 Medium 只适合作为**英文**稿的辐条。这比报告给的定位更窄。
- Boost 提名关闭、EPP 上线后，“投稿到合格出版物、让编辑认领”取代了“找提名人”，成为 Agent 发布流程里的推荐动作（官方原话：“your best bet remains submitting your story to a high quality publication”）。

### Gaps
- “每种互动只在第一次计分”：现行官方页未写，无法核实。
- AI 政策“2024 年 5 月 1 日”生效日：现行页没写，Plagiarism Today 的原文也未重读。
- MPP 在 2026 年 8 月 26 日“open again”之前，暂停或改为申请制的具体时间。
- CEO 那句“联合发布、给其他平台做增长”（Medium Handbook，2026）：medium.com 文章页 403。
- Vocal 引用的 2023 年收入分布：没有官方原文。
- 各作者引语（Cole 的标题公式、Ashley 的真实写作规则、Rane 的 20% 时间与“策展人看不到标签”、Günel 的 Jennifer、Hardy/Awosika 的 10 个标题）：原文不在 RSS 最近 10 篇里，文章页 403，均未逐字核对。
- 5 个标签上限：未找到现行官方说明。

---

## 关键问题 2：原文引语、URL 与页面日期汇总（速查表）

### Takeaway
下表是关键问题 1 中各条的出处速查。帮助页日期是 Zendesk API 的 `edited_at`，博客日期是 RSS 的 pubDate。

### Cited Findings
- Distribution Guidelines，edited 2026-06-29（页内 “Updated: June 29, 2026”）— [链接](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution)
- What happens to your story when you publish on Medium，edited 2025-09-10 — [链接](https://help.medium.com/hc/en-us/articles/360018677974-What-happens-to-your-story-when-you-publish-on-Medium)
- AI content policy，edited 2026-04-29 — [链接](https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy)
- Content eligible for the paywall policy，edited 2026-09-24 — [链接](https://help.medium.com/hc/en-us/articles/31090080813591-Content-eligible-for-the-paywall-policy)
- MPP earnings calculation，edited 2026-03-18 — [链接](https://help.medium.com/hc/en-us/articles/360036691193-Medium-Partner-Program-earnings-calculation)
- MPP eligibility，edited 2026-09-24 — [链接](https://help.medium.com/hc/en-us/articles/39121627791639-Medium-Partner-Program-eligibility)
- MPP overview，edited 2026-11-02 — [链接](https://help.medium.com/hc/en-us/articles/25267383906711-Medium-Partner-Program-overview)
- EPP eligibility and overview，edited 2026-09-10 — [链接](https://help.medium.com/hc/en-us/articles/40661484998679-Editor-Partner-Program-eligibility-and-overview)
- How editor earnings work，edited 2026-09-29 — [链接](https://help.medium.com/hc/en-us/articles/40661926684055-How-editor-earnings-work)
- Importing a post，edited 2026-08-26 — [链接](https://help.medium.com/hc/en-us/articles/214550207-Importing-a-post-to-Medium)
- Set a canonical link，edited 2025-05-06 — [链接](https://help.medium.com/hc/en-us/articles/360033930293-Set-a-canonical-link)
- API/Importing，edited 2024-12-17 — [链接](https://help.medium.com/hc/en-us/articles/213480228)
- 博客文章：
  - 2023-08-10 Updated Guidelines for Boost — [链接](https://medium.com/blog/updated-guidelines-for-boost-47799aad8899)
  - 2025-09-30 Starting October 1（站外流量）— [链接](https://medium.com/blog/partner-program-update-starting-october-1-were-rewarding-external-traffic-15cb28f75bc9)
  - 2025-11-03 Starting November 1（搜索）— [链接](https://medium.com/blog/partner-program-update-starting-november-1-were-rewarding-search-traffic-3ac0635f9f6b)
  - 2025-12-02 On December 1（邮件通知）— [链接](https://medium.com/blog/partner-program-update-on-december-1-were-rewarding-email-notifications-4910c47d4cb7)
  - 2026-01-13 Starting January 1（非 Boost 稿）— [链接](https://medium.com/blog/partner-program-update-starting-january-1-were-rewarding-writing-more-broadly-4907e149e38c)
  - 2026-02-18 Starting February 17（新会员转化）— [链接](https://medium.com/blog/partner-program-update-starting-february-17-were-rewarding-stories-that-bring-in-new-members-3e84d2eb6e68)
  - 2026-05-05 Starting June 1（EPP）— [链接](https://medium.com/blog/partner-program-update-starting-june-1-were-rewarding-editors-for-stories-they-edit-aaec12a97cea)
  - 2026-05-06 Boost Nomination Program 关闭 — [链接](https://medium.com/blog/an-update-on-the-boost-nomination-program-and-whats-next-40331b1a9c0a)
  - 2026-07-01 EPP 全面开放 — [链接](https://medium.com/blog/new-a-program-to-pay-publication-editors-d9c4f1ed40d8)
  - 2026-08-26 MPP 即时注册 — [链接](https://medium.com/blog/the-medium-partner-program-is-open-again-now-with-a-faster-and-easier-enrollment-process-96c01f0e0670)
- TechCrunch 2025-07-11 — [链接](https://techcrunch.com/2025/07/11/mediums-ceo-explains-what-it-took-to-stop-losing-2-6m-monthly/)；TechCrunch 2024-08-21 — [链接](https://techcrunch.com/2024/08/21/august-was-mediums-first-profitable-month-ever/)

### Inferences
- 帮助页的 `updated_at` 普遍晚于 `edited_at`（比如 Distribution Guidelines 的 updated 是 2026-10-28），说明页面元数据有变动，但正文最后一次编辑以 `edited_at` 为准。

### Gaps
- help.medium.com 的 HTML 页（403）和 medium.com 的文章页（403，WebFetch 报 ENOTFOUND）仍被屏蔽。要逐字核对单篇作者文章，需要在会话网络设置里为 WebFetch 放行 medium.com，或者换用浏览器。

---

## 关键问题 3：报告遗漏的重要新事实（现行 Partner Program 与 AI 政策措辞）

### Takeaway
报告遗漏了 2025 年 12 月到 2026 年 9 月的一批变化：Boost 提名关闭、邮件通知加成、阅读率调整、Friend Link 计费、MPP 即时注册与资格清单、关于 Medium 的“元内容”不得进付费墙、AI 辅助须披露、非英文内容不进 General 和 Boost。

### Cited Findings
- **阅读率调整（新）：** “a final adjustment is applied based on the member read ratio… Member reads (30 seconds or more) ÷ Total member views. Stories with a below-average read ratio are adjusted down; stories with an above-average read ratio are adjusted up… does not penalize longer stories.” — [Help: earnings calculation](https://help.medium.com/hc/en-us/articles/360036691193-Medium-Partner-Program-earnings-calculation)
- **邮件通知加成：** “Member reads that come from email notifications sent to your subscribers earn at a higher rate.”（同页）
- **新会员转化是一次性的：** “Conversion earnings are a one-time amount… different from the previous referral program (2021–2025).”（同页）
- **收听上限：** “a maximum of two full listens per member is applied toward earnings.”（同页）
- **关于 Medium 的元内容不得进付费墙：** “Stories primarily focused on Medium itself, the Partner Program, or the mechanics of the platform are not eligible for the paywall… Medium-focused stories are set to network-only distribution by default.” — [Help: paywall policy](https://help.medium.com/hc/en-us/articles/31090080813591-Content-eligible-for-the-paywall-policy)。Distribution Guidelines 也写：“Posts about the Medium Partner Program, making money on Medium, or Boost itself are set to Network Distribution.”
- **General Distribution 的其他失格项：** sponsored content 和 content marketing；“Stories that have a primary point of gathering signups/traffic, selling something”；summaries 和 link round-ups；滥用标签；一次提及大量用户（例如 20 人）。— [Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution)。这与报告“文末 CTA 导向 newsletter”的建议有张力：CTA 可以有，但文章的主要目的不能是收集订阅。
- **MPP 即时注册（2026-08-26）：** 不再需要申请；资格是会员、至少 1 篇文章、完整资料（照片加简介）、银行所在国合格、年满 18 岁。博客原文：“Most common issues include paywalling fully AI-generated writing and stories about Medium.” — [Medium Blog](https://medium.com/blog/the-medium-partner-program-is-open-again-now-with-a-faster-and-easier-enrollment-process-96c01f0e0670); [Help: eligibility](https://help.medium.com/hc/en-us/articles/39121627791639-Medium-Partner-Program-eligibility)
- **AI 辅助须披露**（见关键问题 1），以及 **AI 生成内容不进 General Distribution**（2026-06-29 指南）。
- **非英文稿不进 General、不进 Boost**（2026-06-29 指南）。
- **Medium 官方定性：** 2026-05-05 博客称当前为“the Curation Era”，原文：“We see what a lot of synthetic, AI-generated content is doing to the internet.” — [Medium Blog](https://medium.com/blog/partner-program-update-starting-june-1-were-rewarding-editors-for-stories-they-edit-aaec12a97cea)
- 其他近期博文（RSS 中可见，未展开读）：2026-10-07 “Writers distrust AI, but love using it”；2026-09-18 “Medium's State of Writing Report 2026”；2026-04-14 默认付费墙和订阅通知设置可以“set-and-forget”。— [Medium Blog RSS](https://medium.com/feed/blog)

### Inferences
- 给 Agent 的直接含义：
  - B 模式（AI 起草）的稿子即使披露，在 Medium 上也只能拿到关注者分发。这种稿子不值得发 Medium，或者应当重写到“人写为主”后再发。
  - A/I 模式下只要用了 AI 生成的句子或图片，就要在前两段写披露语。这会影响 Boost，因为现行标准要求“does not appear to be generated by AI”。
  - 发布时勾选“send to subscribers”有直接收入加成，S7 应把它设为默认动作。
  - 标题不能夸大：阅读率调整和转化排除“快速取消的会员”都在惩罚标题党。

### Gaps
- 15% 搜索份额、5% 站外加成在 2026 年是否调整过：现行帮助页只给出 5%，搜索部分只写“additional share”，未给数字。
- 新会员转化的具体金额比例：官方只说“small, one-time amount”。
- 未检查：Medium 的 Terms 对自动化或抓取的条款（报告第 850 行）、“About the No Duplicate Content rule”（360039513913）、出版物最佳实践（41530252213655）、Partner Program forfeiture 与 revocation 政策页（已列出 ID，未读）。
