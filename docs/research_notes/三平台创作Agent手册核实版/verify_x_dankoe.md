# X 与 Dan Koe 相关论断核实（针对《Substack X Medium创作Agent手册.md》，核实日 2026-11-03）

> 访问情况：docs.x.com（含 `.md` 原文、llms-full.txt、changelog）、devcommunity.x.com、letters.thedankoe.com、thedankoe.com、justinwelsh.me、ship30for30.com、typefully.com（含 API 文档）、hypefury.com、buffer.com、tech-ish.com、gigazine.net、thenextweb.com、ppc.land、engadget.com、piunikaweb.com、socialpilot.co 能打开，均已用 curl（浏览器 UA）读全文。**打不开的**：help.x.com（curl 返回 403 Cloudflare“Just a moment...”质询页；WebFetch 返回 ENOTFOUND）、axios.com（403）、yespress.io（403）。eden.so 帮助页链接 404。YouTube 仍不可达，所以【转录】类创作者引语**没有**重新核对。help.x.com 上的规则（Original Content Rewards、自动化规则）只能通过二手报道和 docs.x.com 交叉核实。

## 1. X 平台论断（第一部分“X：排序模型……”一节、跨平台对比表、S7、G-X 闸口、“平台工具现实”、风险表）

### Takeaway
X API 定价的核心数字（$0.015/帖，含 URL $0.20，读帖 $0.005）**确认**，官方生效日为 2026-04-20。但报告漏掉了几条对 Agent 设计影响很大的官方事实：**读取自有数据（Owned Reads）只要 $0.001**，所以报告的复盘成本表高估约 5 倍；2026-02-23 起，自助档 API **只能回复“召唤”了你的帖子**；**自助档已取消点赞、关注、引用帖的 API 写入**；**官方 API 从 2026-06-11 起支持起草和发布 Articles**，报告“未找到证据”的说法应改正。Original Content Rewards 的门槛**确认**。“X 在 2025-10-14 宣布取消链接惩罚”一说**推翻**（被引来源里没有这句话）。Hypefury 现在**已经不支持 X**。

### Cited Findings

**A. X API 按量计费与含 URL 帖子的价格（报告：“自 2026 年 2 月起默认按次付费，新开发者没有免费档……普通帖约 $0.015，含 URL $0.20（2026-04-20 起），读取约 $0.005”）**
- 结论：**基本确认，三处需修正**。官方价目表原文：“**Post: Create** | $0.015 per request”“**Post: Create (with URL)** | $0.200 per request”“**Post: Create (summoned)** | $0.010 per request”“**Posts: Read** | $0.005 per resource”“**User: Read** | $0.010 per resource”。— [docs.x.com pricing](https://docs.x.com/x-api/getting-started/pricing)（2026-11-03 读取的 .md 版本）
- 上线日期：changelog 原文为“**Feb 6, 2026** … Today, we officially launched X API Pay-Per-Use pricing … Recently active Legacy Free tier users receive a one-time $10 voucher. **Basic and Pro plans remain available**, and existing subscribers can opt in to Pay-Per-Use.” 所以“默认按次付费”大致成立，但 Basic/Pro 订阅当时仍然保留。— [docs.x.com changelog](https://docs.x.com/changelog)
- 涨价与 URL 定价原文（2026-04-16 公告）：“Starting Monday, April 20, 2026 … Writes via X API will increase to $0.015 per post (from $0.01) … Posting a URL via X API will be priced at $0.20 per post, **except for summoned replies (which will remain at $0.01)**.” — [devcommunity.x.com 公告 263025](https://devcommunity.x.com/t/x-api-pricing-update-owned-reads-now-0-001-other-changes-effective-april-20-2026/263025)
- **修正一（“没有免费档”）**：现在有一次性的免费额度。2026-10-02 changelog 原文：“a one-time **$20** when an account saves its first eligible payment card, and a one-time match of the first successful auto-recharge, **up to $50** … expire 3 months after they are granted.” 另有消费返还：消费满 $200 起按 10%、15%、20% 返 xAI API 额度。“Public Utility Apps continue to receive free scaled access.” — [changelog](https://docs.x.com/changelog); [pricing](https://docs.x.com/x-api/getting-started/pricing)
- **修正二（报告的复盘成本表）**：“**Owned Reads** … These endpoints are priced at **$0.001 per resource** (1,000 resources for $1)”。适用于 `id` 等于已认证用户、且该用户就是开发者 App 所有者时的 `GET /2/users/{id}/tweets`、`/mentions`、`/followers` 等端点。另外，“All resources are deduplicated within a **24-hour UTC day window**”，同一天重复读同一资源不重复计费。报告表里“每天读取 1,000 条自有帖子的指标，约 30,000 × $0.005 ≈ $150”，按自有读取计价应约为 **$30**，如果是同一批帖子还有去重；“只读最近 7 天，每天 1 次，约 600 × $0.005 ≈ $3”应约为 **$0.6**。— [pricing](https://docs.x.com/x-api/getting-started/pricing)
- **修正三（自回复里放 URL 的价格，报告写“未找到证据”）**：官方只给“summoned replies”留了 $0.01 的例外，自回复是否算“summoned”没有写。见下文 C 条，自回复能不能通过 API 发都有疑问。
- 每月读取上限：“Pay-per-usage plans are capped at **3 million Post reads per monthly billing cycle**.” — [pricing](https://docs.x.com/x-api/getting-started/pricing)
- 速率限制：POST /2/tweets 为“200 requests per 15 minutes … 300 requests per 3 hours”（按用户计）。— [docs.x.com llms-full.txt，Manage Posts 一节](https://docs.x.com/llms-full.txt)

**B. 自动化与标签规则（报告：“自动化账号必须开启‘Automated’标签并关联一个真人账号；据报 AI 自动回复机器人需要事先获得 X 的书面批准”）**
- 结论：**确认，一处修正**。官方写的是“prior approval”（事先批准），**没有写“书面”**。原文：“AI-powered app generates and posts replies | Requires **prior approval** from X”；“AI-Generated Content & Replies: Requires prior approval from X before deployment … Contact X via the Policy Support form before launching … Even with approval, cannot impersonate humans … Deploying AI-generated replies without approval is a violation, even if the content itself is helpful.” — [docs.x.com Developer Guidelines](https://docs.x.com/developer-guidelines)
- 自动化账号的六条要求（原文标题）：“1. Enable the 'Automated' profile label … 2. Disclose in bio … 3. Link to a human-managed account … 4. Honor opt-out requests immediately … 5. Use only the official X API … 6. Stay within rate limits”。该节适用范围：“applies specifically to automated accounts (bots) that post, reply, or interact on behalf of users. If you're building an analytics dashboard … these labeling requirements don't apply”。— [Developer Guidelines](https://docs.x.com/developer-guidelines)
- 自动化动作表原文：回复“Only if user engaged first. Max **1 reply per interaction**”；点赞“Must be directly user-initiated. Auto-liking, bulk liking, and selling likes are prohibited”；“No bulk, aggressive, or automated following”；“App auto-DMs new followers with welcome message — Unsolicited, even to followers”。— 同上
- 非 API 自动化：“**Non-API automation (scraping, browser automation) results in permanent suspension.**” 另有“App stores X data to train AI/ML models — Prohibited (except Grok)”。— 同上
- 已确认，可强化报告的措辞：浏览器自动化的后果是“permanent suspension”，不只是“违反服务条款”。
- help.x.com/en/rules-and-policies/x-automation 页面打不开（403），未读到原文。

**C. 报告漏掉的官方 API 写入限制（影响 S7 和“自回复放链接”的决策树）**
- 2026-02-23 原文：“replies via the API will only be permitted if the replier has been explicitly summoned by the original post's author. This means: The original author @mentions the replying user/account in their post, or The original author quotes a post from the replying user/account. If neither condition is met, attempts to post a reply via the API will be blocked/rejected.” 同时限制 @ 和引用：“you may only @mention and quote users who are already participants in the thread”。该限制“apply only to self-serve tiers: legacy Free, Basic, Pro subscriptions, and Pay-per-use packages”。— [devcommunity 257909：Addressing LLM-Generated Spam](https://devcommunity.x.com/t/x-api-v2-update-addressing-llm-generated-spam/257909)（2026-02-23）；[Create Post 文档](https://docs.x.com/x-api/posts/create-post)
- 2026-04-20 起：“Following, Likes, and Quote-Posts via API Writes will be removed for all self-serve tiers”。Create Post 文档原文：“Quote-posting (using the `quote_tweet_id` parameter) requires an Enterprise plan. It is not available on self-serve (pay-per-use) tiers.” — [devcommunity 263025](https://devcommunity.x.com/t/x-api-pricing-update-owned-reads-now-0-001-other-changes-effective-april-20-2026/263025); [create-post](https://docs.x.com/x-api/posts/create-post)
- 自助档 API 发帖最多带 1 个 cashtag。— [llms-full.txt](https://docs.x.com/llms-full.txt)
- 视频上限按发帖用户的 Premium 状态计：默认 20 分钟、8 GB；Premium/认证用户 125 分钟、16 GB（2026-09-01 changelog）。— [changelog](https://docs.x.com/changelog)

**D. X API 能否发 Articles（报告：“官方 API 是否支持 Articles 未找到证据”）**
- 结论：**推翻，官方支持**。changelog 原文：“**Jun 11, 2026** … Articles draft and publish endpoints. Today, we added new endpoints for drafting and publishing Articles via the X API.” 端点是 `POST https://api.x.com/2/articles/draft`（title + DraftJS `content_state` + 可选封面媒体）和 `POST https://api.x.com/2/articles/{article_id}/publish`，返回 `post_id`。需要用户授权（OAuth 1.0a 或 OAuth 2.0 PKCE），scope 为 `tweet.read`、`tweet.write`、`users.read`。— [docs.x.com Articles introduction](https://docs.x.com/x-api/articles/introduction)
- 价目表里**没有单列 Article 的价格**，不清楚按哪一项计费。此外，API 能否绕过“发 Articles 需要 Premium”的要求，文档没有写。
- Typefully 的 API 也有 `x_article` 平台，文档原文：“X Article configuration. This platform is standalone: do not combine it with other platforms”，正文字段为 `content_markdown`（“The first non-empty block must be `# Title`”）。报告“Typefully 据报支持发 Articles”一条**确认**。— [Typefully API docs](https://typefully.com/docs/api.md)

**E. Original Content Rewards（报告：“Creator Revenue Sharing 于 2026-09-07 停止计酬……至少 500 名认证粉丝、过去 90 天认证用户首页曝光 50 万次，回复不计；只按原创帖被 Premium 用户看到的次数计算”）**
- 结论：**确认，并补充细节**（help.x.com 打不开，以下来自三家互相独立、日期一致的报道）。
- 门槛：“18 or over, an active Premium, Premium+ or Premium Business subscription, 500 verified followers, and 500,000 Home Timeline impressions from verified users in 90 days, replies excluded.” — [tech-ish，2026-08-08](https://tech-ish.com/2026/08/08/x-is-scrapping-creator-revenue-sharing-on-7-september-everyone-has-to-apply-again/)；[GIGAZINE，2026-08-08](https://gigazine.net/gsc_news/en/20260808-x-original-content-rewards-program/)；[TNW，2026-08-08](https://thenextweb.com/news/x-original-content-rewards-program-revenue-sharing-ends)
- 计酬依据：“qualified impressions: unique views of your original post by an X Premium Basic, Premium, Premium+ or Premium Business subscriber, in the Home Timeline feed, with at least half the post visible … paid, promoted, artificial and fraudulent impressions never count. Payouts stay fortnightly, $30 minimum.” — [tech-ish](https://tech-ish.com/2026/08/08/x-is-scrapping-creator-revenue-sharing-on-7-september-everyone-has-to-apply-again/)。注意：Basic 订阅用户的浏览**计入**，但 Basic 用户自己**不能**参加赚钱。
- 排除项：“content copied wholesale, altered only slightly with a filter or text overlay, compiled from other people’s work, or lifted off another platform … A post carrying a helpful Community Note earns nothing, and content that only discusses monetisation or coaches payouts is ineligible.” — 同上。报告漏了 Community Note 和“教人变现”两条排除项。
- 时间线：2026-08-07 宣布；9 月 7 日旧计划结束；9 月 8 日起旧成员重新申请；9 月 25 日首付（GIGAZINE、tech-ish 一致）。另据 tech-ish，Nikita Bier 于 **2026-08-05** 卸任产品负责人。
- 另据搜索摘要，help.x.com 页面写有：自 2026-03-03 起，发布武装冲突类 AI 视频而不披露的用户，会被暂停计划资格 90 天【未能打开原页】。— [WebSearch 摘要，help.x.com](https://help.x.com/en/using-x/original-content-rewards)

**F. AI 媒体标签（对比表：“文字无披露要求；AI 媒体可标‘Made with AI’”）**
- 结论：**修正**。2026-03-03 Engadget 原文：“X will suspend creators from its revenue sharing program if they post AI-generated videos depicting armed conflicts without disclosing they were made with AI … first-time violators will be cut off for 90 days and repeat offenders would be permanently removed … The new policy is the platform’s first rule requiring any kind of AI content disclosure … The platform is separately testing a broader AI labeling toggle that would let users mark any post”。— [Engadget，2026-03-03](https://www.engadget.com/social-media/x-to-require-ai-labels-on-armed-conflict-videos-from-paid-creators-citing-times-of-war-183631400.html)
- 2026-02-25 GIGAZINE（引 Nima Owji）：X 正在开发一个开关，“content generated or edited by AI may be labeled”，覆盖任何帖子，不只是媒体。— [GIGAZINE](https://gigazine.net/gsc_news/en/20260225-x-ai-labels/)
- 修正后的写法：“Made with AI”是一个可选标签，可用于任何帖子（包括文字），2026 年 3 月起据报处于测试或推出阶段，全面上线未能确认；强制披露目前只适用于参加变现计划的创作者发布的武装冲突 AI 视频。

**G. Premium 档位（报告提到“Premium 长帖上限”，Articles 已对 Premium 开放）**
- 价格只有二手来源：Basic $3/月、Premium $8/月、Premium+ $40/月（2025 年起，年付 $395）。也有来源仍写 $16，研究判断已过时。【仍无法核实】官方定价页未读到。— [WebSearch 汇总：MacRumors 2024-12-23 等](https://www.macrumors.com/2024/12/23/x-raises-premium-plus-subscription-prices/)
- tech-ish 引用 SpaceX 2026 年 5 月 IPO 招股书：Premium 与 Premium+ 合计约 440 万订阅者，月活约 5.5 亿。【二手】— [tech-ish](https://tech-ish.com/2026/08/08/x-is-scrapping-creator-revenue-sharing-on-7-september-everyone-has-to-apply-again/)

**H. Articles 开放范围与 100 万美元奖（报告：“2024 年 3 月面向 Premium+ 上线，2026 年 1 月开放给全部 Premium 用户，并设 100 万美元最受欢迎文章奖”）**
- 结论：**确认**。PiunikaWeb（2026-01-07）原文：“X just opened up Articles to all Premium subscribers, ending the feature’s exclusivity to Premium+ users … Articles launched back in March 2024 as a Premium+ perk.” — [PiunikaWeb](https://piunikaweb.com/2026/01/07/x-articles-premium-nikita-bier-updates/)
- 奖项细则（二手）：文章须为原创、不少于 1,000 词，主要按认证用户首页曝光评判，仅限美国 Premium 用户。— [WebSearch 汇总，Business Standard 等](https://www.business-standard.com/world-news/elon-musk-s-x-offers-1-million-reward-for-best-long-form-article-126011700647_1.html)

**I. 链接惩罚的历史（报告：2026-07-29 Musk 回复 PG；“另有摘要称 X 在 2025-10-14 就宣布取消了链接惩罚”）**
- 2026-07 那次交流：**确认**。PPC Land（2026-07-30）原文：Bier 2026-07-28 23:56 写“Hello Mark, you do not need to put the links in replies anymore”；Graham 问“You no longer penalize tweets with links in them?”；Musk 于 2026-07-29 03:38 回复“**We haven't for over a year.**”；“The statement arrived without a formal announcement.” — [ppc.land](https://ppc.land/x-drops-year-old-link-penalty-musk-tells-zuckerberg-on-platform/)
- “2025-10-14 宣布取消”：**推翻**。我读了被引的 SocialPilot 页面全文，里面没有这句话，反而写着“Posts with external links are penalized in reach … suppressed by up to 80%”，并建议把链接放进回复。— [SocialPilot](https://www.socialpilot.co/blog/twitter-algorithm)。2025 年 10 月真正发生的事是：tech-ish 2025-10-13 报道 X 在测试新的链接处理方式；10 月 17 日 Musk 说推荐系统的改动可能提升链接帖的触达；**10 月 19 日** Bier 宣布 iOS 测试，链接在浮层中打开，并解释链接帖触达低是因为“the web browser covers the post and people forget to Like or Reply”。这说明当时 X 是在改链接的显示方式，不是宣布取消惩罚。“10 月 14 日”很可能和 Buffer 链接研究的发布日期（2025-10-14）弄混了。— [tech-ish 2025-10-13](https://tech-ish.com/2025/10/13/x-is-testing-changes-to-how-it-handles-web-links-to-external-sites); [iPhone in Canada 2025-10-20](https://www.iphoneincanada.ca/2025/10/20/link-engagement-test-for-x-on-ios/)
- 时间上的矛盾：Musk 说的“over a year”往回推是 2025 年 7 月以前，这和 Buffer 观察到的“2025 年 3 月后普通账号链接帖互动中位数为零”是冲突的。

**J. Buffer 的链接研究与发帖时间研究**
- 链接研究：**确认，一处修正**。页面写“Published Oct 14, 2025”，“We analyzed 18.8 million X posts from 71,000 accounts”；“As of August 2025, Link posts had 0% engagement rate on regular accounts, ~0.28% engagement rate on Premium accounts”；“Since March 2025, link posts from non-Premium accounts have been effectively invisible, with median engagement rates stuck at zero.” 需要修正的是指标：Buffer 用的是**互动率**中位数，报告写成“互动中位数”，应改成“互动率中位数为零”。同一页面还写“Premium accounts now see around 10x the reach of regular ones … Premium Plus subscribers get the highest reach”。— [Buffer](https://buffer.com/resources/links-on-x/)
- 发帖时间研究（报告没有引用，属于补充）：Buffer 2026-03-13 页面称分析了 870 万条推文，“Tuesday at 9 a.m. is the #1 time … followed closely by Wednesday at 10 a.m. and 9 a.m.”，“the worst times to post are during the evening (6 p.m. – 11 p.m.)”，周五、周六最差。时区口径页面未在摘录中说明。— [Buffer best time](https://buffer.com/resources/best-time-to-post-on-twitter-x/)

**K. 工具（Hypefury 与 Typefully）**
- **报告漏掉的新事实：Hypefury 已不再支持 X。** 其 llms-info 原文（“Last updated: November 2026”）：“Platforms: Instagram, Facebook (Pages), Threads, LinkedIn (profiles and company pages), TikTok and Bluesky.” 列表里没有 X。所以报告把 Hypefury 的 Auto-plug 和“自动私信触发 X 反垃圾”当作 X 方面的参考已经过时；该页面也**没有**“激进自动私信会触发 X 反垃圾过滤”的说法。— [hypefury.com/llm-info](https://hypefury.com/llm-info)
- Typefully：**确认**支持 X、LinkedIn、Threads、Bluesky、Mastodon、Instagram，API 里有 `substack`（“Substack Notes configuration”，返回 `substack_published_url` 如 `https://substack.com/@username/note/c-…`）和 `x_article`；首页列有“Auto-Plug & Auto-RT”“Free API”和 MCP。— [Typefully API](https://typefully.com/docs/api.md); [typefully.com](https://typefully.com); [llms.txt](https://typefully.com/llms.txt)

**L. 2026-10-09 服务条款修订（Agent 行为由用户负责）**
- 【仍无法核实】：没有找到官方条款原文；x.com/tos 不在本次检查范围内。

### Inferences
- 手册的 X 发布模块需要重写。在自助档 API 下，Agent **不能**回复别人的帖子（除非被 @ 或被引用），**不能**引用帖子，**不能**点赞或关注。这意味着“自动互动”的风险在技术上已经基本被堵死，合规闸口可以简化成“只发原创帖、只读自有数据”。
- 线程（自己回复自己）和“链接放自回复”能否通过 API 实现，官方文档没有说明，应该在 P2 阶段先做实测。如果自回复不算“summoned”，线程就只能人工发或通过 Typefully 发。
- 复盘读取成本应该按 Owned Reads 的 $0.001 计。
- Articles 可以作为 API 自动化目标（先建草稿，人工点发布），对应 H6 闸口。

### Gaps
- help.x.com 被 Cloudflare 拦截（403），Original Content Rewards 和 X Automation Rules 的原文都没读到。
- Article 发布的 API 价格、自回复的计价和准入，官方都没有说明。
- Premium 官方定价页没有读到。

## 2. Dan Koe 论断（“Dan Koe：一篇周更 newsletter 养活整个媒体矩阵”一节与“先交代证据”一节）

### Takeaway
晨间流程和“平台分成每月 $300–1,000、自有产品 $5 万–20 万以上”两条都**确认为 Koe 原文**。“$1M 奖 runner up”**有冲突**：据二手报道他拿的是单独的“Creator Choice”奖（$25 万），不是亚军。营收和订阅数仍然只有第三方来源，彼此不一致。

### Cited Findings
- **晨间流程（中文摘要：散步 30 分钟、写作 90 分钟，然后健身，之后才处理邮件和会议）**：**确认，并补充细节**。原文：“Go on a walk (30 min) / Start writing (90 min) / After that, I eat a small meal, go on another walk, respond to a few messages along the way, go to the gym, then start emails, meetings, and other non-creative work.” 细节：“the first 30 minutes of writing are dedicated to short-form posts for social media … The second 60 minutes … is dedicated to writing a newsletter.” 页面标题是“The 2 hour morning routine that changed my life”，`datePublished` 为 2025-08-22（可能是重新发布）。— [letters.thedankoe.com](https://letters.thedankoe.com/p/the-1-million-dollar-morning-routine)
- 同一篇原文还写到：“my newsletter analytics wouldn't be double my YouTube analytics with 900,000 fewer subscribers”；以及“I use that as a general outline for a weekly YouTube video … may even post the newsletter itself to Medium and my personal blog”。— 同上
- **平台分成 vs 自有产品**：**确认**。原文：“As someone with a few million followers, I can tell you that platform monetization is not enough. I can make about 300-1000 a month on Instagram or X, but with my own product/offer, I can make 50k-200k+.” 页面 2026-03-11。— [How to start a one-person business in 2026](https://letters.thedankoe.com/p/how-to-start-a-one-person-business)
- **“100 万美元”算账（$2,777/天，2.5% 转化，720 访客）**：报告引的是视频【转录】，现在找到了 newsletter 原文，**确认**：“$1,000,000 / 12 = $83,333 per month / $83,333 / 30 = $2,777 per day … Sell 18 $150 products a day … At a 2.5% conversion rate … you need 720 people to visit that page a day”。同文还写“Get 500k to 1 million impressions on social media per month”。— 同上
- 同文对 Agent 的看法：“You have everyone spending thousands a month on agents … they don't know what good looks like”，和视频转录一致。— 同上
- **Eden**：thedankoe.com 首页自称“co-founder of Eden”和“author of The Art of Focus”，并写“I am not accepting calls, clients … grab one of my courses above”。Eden 作为他的工具**确认**；早期访问日期（2025-11-24）没有核实，因为 eden.so 帮助页返回 404。— [thedankoe.com](https://thedankoe.com)
- **$1M Articles 奖“runner up”**：**修正（证据较弱）**。二手报道称 2026-02-04 公布结果：@beaverd 获 $100 万，The Kobeissi Letter 获亚军 $50 万，Koe 的“How to Enter a State of Extreme Focus Anytime”获 $25 万“Creator Choice”奖。手册应写成“Koe 自称 runner up；据报他拿的是 Creator Choice 奖”。— [KuCoin 快讯](https://www.kucoin.com/news/flash/x-announces-winners-of-1m-long-form-writing-contest-beaverd-takes-top-prize)（聚合源，未读原帖）
- **营收与订阅**：**仍无法核实**。beehiiv 案例页写 $200 万/年、17.5 万订阅者；YesPress（2026 年 4 月）写 $410 万和 29.3 万订阅者（站点 403）；KuCoin 写约 17 万。数字互相冲突，没有一手来源。— [beehiiv case study](https://www.beehiiv.com/case-studies/dan-koe); [yespress](https://yespress.io/dan-koe)
- **“How to fix your entire life in 1 day”浏览量与 $4,495 分成**：本轮没有找到一手来源，维持【待核实】。
- **框架名“idea bank”“content multiplication”“APAG”**：在本轮读到的两篇 newsletter 原文里同样**没有出现**，报告的“无法核实”判断维持。

### Inferences
- Koe 自述的晨间流程是“30 分钟短帖 + 60 分钟 newsletter”，这可以直接写进手册的节奏配置。

### Gaps
- YouTube 不可达，19 个视频的转录没有和原视频逐字核对。
- 2 Hour Writer 等课程的细节和价格没有核实。
- Eden 的“AI 额度开销”和险些破产的说法，只来自视频转录，没有其他来源。

## 3. X 创作者论断（Welsh、Ship 30、Bloom、Puri、Naval、Hormozi、Butcher、Dry、Cultural Tutor）

### Takeaway
官网层面只核实到少量事实。各人的【转录】引语来自 YouTube，本轮没有逐字核对。

### Cited Findings
- **Justin Welsh**：官网自述原文：“After helping build two companies past $1B in valuation, I left my executive role at 38 … built a **$15M** one-person business.” 报告没有这个数字，可以补充，标为自述、未审计。“Content Operating System”的官方定义在首页没有看到。— [justinwelsh.me](https://www.justinwelsh.me)
- **Ship 30 for 30**：官网原文：“Ship 30 for 30 is a cohort-based writing challenge … Next live cohort starts January 18, 2027 … 11 Live Sessions With Replays”；Bush 写道：“Launched Ship 30 in November 2020—now 24 live cohorts and 10,000+ students taught with Cole”。首页**没有**出现“1-3-1”或“4A”，这两个框架的官方措辞仍然无法核实。— [ship30for30.com](https://www.ship30for30.com)
- 本轮**没有**核实：Bloom、Hormozi、Butcher、Dry、Cultural Tutor、Naval 的视频转录（YouTube 不可达），Shaan Puri 的 Recapio 摘要，Bush 的 quotewise 引语，Cole 和 Bush 的 threadreader 线程。podscripts.co 可达，但本轮没有用它去找对应的转录。

### Inferences
- 创作者心法部分的证据等级维持不变；Welsh 的营收可以按“自述 $15M”补充进去。

### Gaps
- 上面列出的创作者引语仍需要在 YouTube 可达或通过 podscripts.co 的转录逐字核对。
