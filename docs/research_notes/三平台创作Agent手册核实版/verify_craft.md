# 创作心法核实：Part 2 各创作者档案逐条对照原文 / 转录（2026-11-03）

范围：`reports/Substack X Medium创作Agent手册.md` 第二部分“其他十五位创作者的心法档案”中标注【待核实】/【转录】的条目。
方法：用 curl 抓原始页面（带浏览器 UA）；How I Write 访谈用 GitHub 仓库 `liamdonnellyonline-cell/david-perell-nonfiction-transcripts` 的 YouTube 转录（每个文件头部有 YouTube URL 和发布日期）做逐字核对。转录是自动字幕，标点和个别词可能不准，引语以“意思加关键字”为准。

访问记录（被拦截或失败的）：
- **perell.com**：curl 每次都返回 HTTP 429（限流），WebFetch 报 DNS ENOTFOUND。Raymond Chandler Rule、28 Pieces、Personal Monopoly 原页都没读到。转而尝试 web.archive.org，被会话策略拒绝。
- **x.com / twitter.com**：没有直接访问。试过 fxtwitter 镜像 API，被会话策略拒绝（不在允许名单）。所有 X 推文只能用推文 ID 解码出发布时间（Snowflake 时间戳），内容没有核对。
- **tim.blog**：Ferriss #702 转录页返回 429。
- **collabfund.com/blog/how-i-write/**：404，可能没有这个 URL。
- **podscripts.co**：How I Write 节目页 404，没有找到 Ben Thompson 那期的转录。metacast.app 返回 403。
- **howiwrite.substack.com**：可以访问，但 Substack 存档 API 只有 51 篇，最早是 2025-03-05。更早的节目只在 YouTube 和播客平台上。

---

## 每条论断的判定（按创作者分，每条给出判定、原文引语和 URL）

### Takeaway
多数被引用最多的引语都核实了，但有几处需要修正。一是 Housel 的“每个词值 100 美元”是他转述别人的话，他自己说“忘了是谁说的”。二是 Housel 写过“4,000 篇博客”，Motley Fool 的 3,500 篇只是其中一部分。三是 Lenny 的原话是“把引言砍掉 50%”，不是“删掉第一段”。四是 Packy 说 Claude 给的是“A，改一处就是 A+”，播客里没有“A-”这个说法。另外，“妻子是第一读者”在原转录里找不到依据。

### Cited Findings

#### Paul Graham（只抽查 3 条，全部确认）
- **“17 段子树”加“要快刀斩”：确认。** 原文：“In this essay I've already cut a 17-paragraph subtree… In general you want to be quick to cut. One of the most dangerous temptations in writing… is to keep something…” 出自 *The Best Essay*，2024 年 3 月 — [paulgraham.com/best.html](https://paulgraham.com/best.html)
- **四因素“像可以相乘的数”加“不要在窗户上装栏杆”：确认。** 原文：“the four components are like numbers you can multiply together to get a score for usefulness”；“You don't want to spoil your house by putting bars on the windows to protect against dishonest ones.”尾注 1 里还有一句：“Put railings on the balconies, but don't put bars on the windows.” 出自 *How to Write Usefully*，2020 年 2 月 — [paulgraham.com/useful.html](https://paulgraham.com/useful.html)
- **花哨文字“还能掩盖想法的缺失”：确认。** 原文：“fancy writing doesn't just conceal ideas. It can also conceal the lack of them.” 出自 *Write Simply*，2021 年 3 月 — [paulgraham.com/simply.html](https://paulgraham.com/simply.html)

#### Morgan Housel
- **“了解读者”是最糟的写作建议、自私写作：确认。** 原文（How I Write，2025-10-15）：“I think it's the very common, know your reader. Because I think the speed at which 'know your reader' becomes 'pander to your reader'… is astounding.”他还说，几乎每个人写“没人会读的日记”时都写得好。同一期还有：“this is where I came into my selfish writing era of I'm not trying to impress other people anymore… I'm definitely not going to try to pander to other people.” — [howiwrite.substack.com/p/morgan-housel-how-to-master-writing](https://howiwrite.substack.com/p/morgan-housel-how-to-master-writing)；第三方转述见 [Writer Science](https://www.writerscience.com/the-single-worst-piece-of-writing-advice/)（引用 Perell 2025-10-16 的推文）。
  - 注意：“自私写作（selfish writing）”这个说法更早就出现了，Perell 2021-08-06 的视频里已经有：“what's always worked best for me is i just want to write stuff that i personally would be interested in reading that's why i call it selfish” — [YouTube 2eT8SMtbHNI](https://www.youtube.com/watch?v=2eT8SMtbHNI)。Housel 在 2025 年那期里说，自私写作是“later insight”，早年他是靠读每一条评论成长的。
- **“假装每个词要花你 100 美元”：修正（归属）。** 这句话 Housel 是转述别人的，他自己说忘了是谁说的。原文（How I Write，2023-11-06，节目标题“The $100 Rule…”）：“I also heard, I forget who said this, but they're like, when you're writing, you should pretend that every word costs you 100. … do I need this word? Do I need this sentence? Not, is this a good sentence? Just, do I need it?” — [YouTube o84GXnrHdgg](https://www.youtube.com/watch?v=o84GXnrHdgg)。手册应写成“Housel 转述的一条规则”。
- **“人们记住的不是书，是句子”：大体确认，归属要说明。** 这期节目的开场是：“People don't remember books, they remember sentences. When you told me that…”，说话的是 Perell，他在复述 Housel 曾对他说过的话。可以写成 Housel 的观点，但最好注明“经 Perell 复述” — [YouTube o84GXnrHdgg](https://www.youtube.com/watch?v=o84GXnrHdgg)
- **“In summary”是最糟糕的结尾句：确认。** 原文：“The absolute worst writing, is that your last sentence is, in summary, comma… It should be some sort of emotional like, boom.” — 同上，2023-11-06。
- **写完初稿就发：确认。前后措辞看似矛盾，原因在于两种做法同时存在。** 原文（2023-11-06）：“pretty much when I get to the bottom of the article, I just hit publish. And I don't go back and read the whole thing again. But what I do do, is every sentence that I type, After I type it, I'm like, all right, is that good? … Can I change this word?”同一期他还描述过另一套节奏：两天构思，一天写完，再“sit on it for a day… might change a sentence or two and then hit publish”。另一处：“Almost every blog that I publish will have a typo… I kind of just get to the end and I say, all right, I've done my best… send it off to the wild.” — [YouTube o84GXnrHdgg](https://www.youtube.com/watch?v=o84GXnrHdgg)。2025 年那期又补了一条：他最自豪的博客“took me a couple hours… hit publish”，最失望的是“labored over relentlessly for a week”，原因是“the idea sucked” — [howiwrite 2025-10-15](https://howiwrite.substack.com/p/morgan-housel-how-to-master-writing)。所以准确的版本是：逐句精修，写到结尾就发，不回头通读全文。（“初稿像吵架时的情绪爆发，必须清醒后再看”这段话是 **Perell** 说的，不是 Housel。）
- **“写作过程本身就是研究过程”：** 没有找到逐字原话。2025 年那期里，他说 ChatGPT 作为研究工具“unbelievable”，但“every letter will be typed by me”。这一条判为**仍无法核实**。
- **在 Motley Fool 写了约 3,500 篇：确认，但要补充。** 原文：“I think I was in the Motley Fool for nine years and I wrote 3,500 articles when I was there.”（2023-11-06）。他的博客总数是“Pushing 4,000 blog posts. I think I'm really proud of like 10 of them”（同期）；2025 年那期 Perell 的介绍是“more than 4,000 blog posts”，Housel 自己说“I wrote 4,000 blog posts.” — 来源同上。
- **自然单位是博客长度、“每一章就是一篇长博客”：修正，意思对，措辞不同。** 原文：“if you sit down and you're like, I'm going to write a 75,000 word book. It's really daunting… But if you're like, okay, I need 20 long blog posts… I can knock that out.”他还承认，写《金钱心理学》时“I shouldn't have just pretended that that was the same thing as blogging… It's a totally different…”。手册里的“1,500 词单位”这个具体数字，原文中没有找到 — [YouTube o84GXnrHdgg](https://www.youtube.com/watch?v=o84GXnrHdgg)

#### Lenny Rachitsky
- **Coda 点子页：确认。** 原文：“Each topic has a Coda page where I start throwing bullet points of ideas, quotes, stats, anything I have off the top of my head.”同一篇里还有：选题清单约 50 个，“I pick the topic I'm most excited to write about this week”；每篇都以读者提问开头；中位数每篇 10 小时。日期页面上没有标，文中提到约 27 万订阅者，推测在 2022 年前后 — [Compound Planning 访谈](https://manual.compoundplanning.com/chapters/interview-with-lenny-rachitsky-writer-of-lennys-newsletter)
- **改 10 到 30 遍：确认。** 原文（How I Write，2023-10-25）：“I read through my posts 10 20 30 times just again and again looking for what can I tweak what can I simplify what can I cut what can I move around.” — [YouTube DMZem1NYfpM](https://www.youtube.com/watch?v=DMZem1NYfpM)。Compound Planning 访谈里的说法是“read through it dozens of times… probably on the 50th reading, it's ready to go”。Perell 那条推文（ID 1717139432598319521）的时间解码为 2023-10-25，和节目同一天。
- **删掉第一段，文章立刻变强：修正。** 原话是把引言砍短 50%，没有说删掉第一段：“the introductions always just like let's just let's make this 50% shorter and that often makes it a lot better.”另一处：“introductions are often way too long… shut up just tell me the answer already.” — 2023-10-25，同上。
- **“什么让我觉得有意思”：确认（是他写作提示里的一条）。** 原文：“what do I want to learn about what do I want to remember what is interesting to me right now what do someone asked me that I didn't have a great answer to what have I said on Twitter that has resonated” — 同上。
- **10 条写作习惯（公开承诺约占一半动力、离开前在稿子顶部写下一步、来自 Perell）：仍无法核实。** 出处是 X 推文 1347642510445711360（解码为 2021-01-08），X 无法访问。2023 年的转录里也没找到这几条。

#### Packy McCormick
- **“I write the piece, and then I write the piece.”：确认（逐字一致）。** 原文：“Every time I start writing a piece, I have a title up top… And then in brackets beneath it, I put, 'Title image.' And then I write the piece. And then I write the piece.” — How I Write，2024-02-28 — [YouTube 9Fit0knSiH8](https://www.youtube.com/watch?v=9Fit0knSiH8)
- **V0 草稿用作删稿垃圾场：确认。** 原文：“do V zero is the first one, because I know it's just going to get scrapped and I'm going to use that as the doc where I dump all of the stuff that I cut from the other versions.”他通常写 6 到 7 稿 — 同上。
- **发布日早上 4:30 到 8:55 重写，发送日从周一改到周二：确认。** 原文：“4:30 the morning that I'm going to hit send, I wake up to maybe edit, maybe rewrite, rewrite the whole thing from 4:30 to 8:55 AM”；“the last 10 essays that I've written, I've rewritten at 4:30 in the morning”；“I started sending on Tuesday instead of Monday.” — 同上。
- **X 推广时，好条形图或惊人数据比缩略图更有效：确认。** 原文：“the more attention grabbing thing on Twitter is a really good bar chart… or a really good number… I think the thumbnail is probably less and less important.” — 同上。
- **妻子是第一读者、负责判断稿子有没有意思：推翻（依据不足）。** 两期转录（2024-02-28 和 2021-08-20）里，妻子 Pooja 只在两处出现：一是周末帮他带孩子让他写作，二是她不想回办公室，这成了一篇文章的灵感。两期都没有说她是第一读者。转录里能找到的“一个读者”是他每天写日记给一位朋友看：“there's one person who reads it.”第三方摘要 bulletpointpodcast 也没有提妻子是读者 — [YouTube 9Fit0knSiH8](https://www.youtube.com/watch?v=9Fit0knSiH8)；[bulletpointpodcast 摘要](https://bulletpointpodcast.com/howiwrite/packy-mc-cormick-a-tactical-masterclass-in-online-writing/)
- **Claude 几乎给他每份初稿都打 A-：修正或仍无法核实。** 播客原话是 A 和 A+：“Claude in particular is like, 'This is… what a contribution to the field… It's an A. And with this one tweak, it's definitely an A plus. Among the best things ever written.'” — 2024-02-28，同上。手册引用的 X 推文（1821163105830769100，解码为 2024-08-07）无法访问，“A-”这个说法没有核实。建议改用播客原话。

#### Ted Gioia
- **永远诚实，以及三个自查问题：确认。三个问题是 Perell 归纳出来、Gioia 认可的。** 原文（How I Write，2024-05-29）：Perell 说“there's three questions that you ask is this fair is this accurate will this be persuasive to all fair-minded observers”；Gioia 回应：“the reader wants it to be honest they want it to be fair and obviously it has to be convincing to Fair people if I'm not operating at that level I have failed.” — [YouTube cur-LrnN8DM](https://www.youtube.com/watch?v=cur-LrnN8DM)。Perell 的推文 1795800774254985236 解码为 2024-05-29，和节目同一天。
- **藏一本空白日记治写作障碍：确认，需补充来源说明。** 这段是 Perell 在节目里朗读 Gioia 写过的文字：“buy a blank journal and keep in… a safe place… at the end of each day put down what happened during the last 24 hours but there's one unbreakable rule what you write in the journal must be absolutely and totally honest”。Gioia 接着说：“I took this from somebody else the problem is I don't remember who.” — 同上。“连续一个月”这个细节在转录片段里没有找到，**仍无法核实**。
- **追求受众规模就早放弃了，“哪怕只有一个读者也有意义”：确认。** 原文：“If I had focused too much on the size of my audience, I would have given up decades ago. Most of my readers found me after I turned 60.”以及：“reach out and find a reader—make a connection—even just one reader is meaningful.” — *I Give the Worst Writing Advice in the World*，2024-11-27 — [honest-broker.com](https://www.honest-broker.com/p/i-give-the-worst-writing-advice-in)
- **在一两个领域里比别的写作者懂得更多、说服只有在信任时才有效：部分确认。** 2024-05-29 的转录里，Perell 和 Gioia 讨论了“becoming a good writer can begin with deep domain expertise”和“having some expertise other than just write… will make you a more powerful writer”，Gioia 还谈到“build that relationship of trust with the reader”。Athens 博客的逐字说法没有核实 — [YouTube cur-LrnN8DM](https://www.youtube.com/watch?v=cur-LrnN8DM)

#### Henrik Karlsson
- **方法有用，但最好的材料来自打破方法：确认。** 原文：“that list of steps is a good first approximation… But to honor the potential of the material… I almost always have to break out of the process and get lost in the desert.”另一句：“if I make my essays more consistent, I remove not only the mistakes but also much of the upside.” — *How I write essays*，2024-12-04（付费文章，只读到免费部分）— [henrikkarlsson.xyz](https://www.henrikkarlsson.xyz/p/how-i-write-essays)
- **“原始素材（raw footage）”：修正措辞。** 免费部分的原话是“I collect my thoughts in a wild sprawling mess. I have one or two million words in my journals and notes”，没有出现“raw footage”这个词。付费部分没有读到。
- **想法在身体里住大约一年：确认。** 原文：“I need to let things live in my body for about a year before I can actually turn them into essays.”以及：“when I get excited about something, I can't write about it. I have to give it a year… at least.” — How I Write，2025-08-13 — [howiwrite.substack.com](https://howiwrite.substack.com/p/henrik-karlsson-the-writing-process)
- **开头最后写：确认。** 原文：“I write the beginning and the ending when everything is already done… if I start writing an opening… I get really pretentious… Usually, once I've written a piece, the opening is obvious.” — 同上。
- **过早的批评会“压扁想法”：部分确认。** 这期有一个章节叫“[55:10] Protecting Early-Stage Ideas from Criticism”，但“压扁（squash）”这个词没有逐字找到 — 同上。
- **花一倍时间带来四倍以上新订阅：确认（Newport 转述 Karlsson 的数据）。** 原文：“spending twice as long on an article yields, on average, more than four times the number of new subscribers.”这个数据基于 Karlsson 当时写的 37 篇博客 — Cal Newport，*On Slow Writing*，2024-01-18 — [calnewport.com](https://calnewport.com/on-slow-writing/)
- **“你身上古怪的东西才是有趣的东西”、约写到第 50 篇才有感觉：确认，但出处要改。** 这两句出自 Karlsson 2025-01-20 的 X 线程，不是 Substack note：“1. It is the stuff about you that is odd that is interesting.”以及：“13. … You will develop a feel for what it is you do after about 50 essays.” — [threadreaderapp 1881287554999460250](https://threadreaderapp.com/thread/1881287554999460250.html)。Substack note c-87287315 没有核对。

#### Ben Thompson
- **你写的最重要的文章，是读者读的第二篇：确认，但只有二手来源。** 节目是 How I Write，“How Ben Thompson Built a Writing Empire”，2024-08-21。多个播客平台的转录摘要都说节目以这句开场：“The most important article you write is the second article someone reads.” — [metacast 节目页](https://metacast.app/podcast/how-i-write/RRY6pAWO/how-ben-thompson-built-a-writing-empire/H5eVi04V)（403，未能直接读）；[读者笔记 valueb9b](https://valueb9b.substack.com/p/ben-thompson)
- **免费头版文章“需要好钩子”、付费更新“心理上很自由”、“每个分号都用到极致”、“一条共同的线”：仍无法核实。** 这几条的唯一来源是 How-I-Write-Skills 技能包，而那个技能包的 distribute/SKILL.md 里也没有这几句逐字引语。完整转录没有拿到：podscripts 没有这一期，metacast 返回 403，podwise 需要登录。

#### Tyler Cowen
- **不让 AI 替他写、“像我的小宝宝”、别让 AI 抹平怪癖：确认。** 原文：“But I don't let it write for me. I want the writing to be my own; it's like my little baby, so to speak… There's ways you can use AI that will smooth out your writing on average… I don't want to do that. I want to be like Tyler Cowen, this weirdo.”以及：“I want it to stay weird. I will use it to fact-check things in areas I don't know.”节目摘要里的说法是：“Don't let AI smooth out your idiosyncrasies.” — How I Write，2025-03-05 — [howiwrite.substack.com](https://howiwrite.substack.com/p/tyler-cowen-will-ai-kill-writing)

#### David Perell
- **Raymond Chandler Rule（每 250 词一次顿悟）：大体确认，但原页没读到。** perell.com 返回 429。Perell 在 Tim Urban 那期（2024-01-03）口述过：“Raymond Chandler… would have about 250 words per page. And his rule was that on every single page… there had to be one of those moments” — [YouTube dyAiNCF2J3A](https://www.youtube.com/watch?v=dyAiNCF2J3A)
- **Personal Monopoly：确认这个概念存在，并且被学员沿用。** Packy 在 2021-08-20 那期说：“three things that i learned from rite of passage… one is finding your personal monopoly” — [YouTube a0hOyHqli0s](https://www.youtube.com/watch?v=a0hOyHqli0s)。perell.com 上的原文没读到。
- **CRIBS：修正。I 是 Interesting，不是 Insightful。而且原文里 CRIBS 用在口头试讲时听反应，不是用在书面反馈上。** 原文：“As I'm talking through my ideas with them, I'm listening for a few things in how they respond… It's called CRIBS, which stands for confusing, repeated, interesting, boring, and surprising. When an idea I throw out is confusing, repeated… or boring, I move away from it” — *How David Perell Writes an Essay*，Every，2021-10-28 — [every.to](https://every.to/superorganizers/how-david-perell-writes-an-essay)
- **Writing One-Sheet：仍无法核实。** 网上没有找到 Perell 本人发布的 One-Sheet 原件，目前只有第三方 quartz 笔记。
- **2024 年 8 月宣布关停 Write of Passage：确认时间。** Alexandra Allen 2024-08-28 写道：“Last week… Write of Passage… is ending. … David Perell, announced the news on Monday” — [alexandraallen.substack.com](https://alexandraallen.substack.com/p/four-life-hacks-from-the-ultimate)；Ishan Shanavas 2024-09-28 写了 *Goodbye Write of Passage* — [ishanshanavas.substack.com](https://ishanshanavas.substack.com/p/goodbye-write-of-passage)。推文 1825569243854962795 解码为 2024-08-19（周一），时间吻合。
- **关停理由“除了经济账，什么都值得庆祝”、2025 年 2 月说“部分是因为 AI 浪潮”：仍无法核实。** 两条推文都打不开（第二条解码为 2025-02-24）。网页搜索没有找到这两句的逐字原话。

#### Nat Eliason
- **“太守规矩就会像 AI 写的”：确认。** 原文：“good writing is the Grammarly fixes you ignore… If you follow all the normal writing rules too closely, your writing will sound AI generated.” — *On Writing Better: 43 Things…*，2024-06-25 — [nateliason.com/blog/on-writing-better](https://www.nateliason.com/blog/on-writing-better)
- **“一份烂草稿比一份没写完的草稿好得多”：确认。** 原文：“A shitty draft is much better than an unfinished draft. So give yourself permission to write slop for a bit” — 同上，2024-06-25。
- **“删副词”之类的建议没抓住要点，要点是“展示而非告诉”：仍无法核实，而且和他早年的说法相反。** 2024 年的文章里没有找到这句话。他 2018 年的文章恰好主张“delete your adverbs”，只是加了一句“more about extreme pruning than outright abstinence” — [nateliason.com/blog/better-writer](https://www.nateliason.com/blog/better-writer)（2018-03-19）
- **编辑放在尽量不同的场景里做：确认，但出处要改。** 这句在 2018 年那篇里，不在 2024 年那篇。原文：“Looking at a piece in different places in different mental states will help you see it differently.” — [better-writer](https://www.nateliason.com/blog/better-writer)
- **TK 占位、删“我认为/我相信/似乎”、不写 8–10 句长段落、长短句交替：全部确认。** 原文：“put 'TK' anywhere you aren't sure of a detail… Think of it as 'To Come'”；“Avoid 'I think,' 'I believe,' 'It seems'”；“You shouldn't be writing 8-10 sentence paragraphs unless you have an important point that needs the extra meat”；“Vary Your Sentence Length”。另有一条手册漏了：“ignore the rules occasionally” — 2018-03-19，同上。
- **引 Stephen King：初稿为自己写，重写为所有人写：确认。** 原文：“When you first write something, you should write it for yourself. When you rewrite it, write it for everyone else.” — 读书笔记，2020-02-07 读完 — [nateliason.com/notes/writing-stephen-king](https://www.nateliason.com/notes/writing-stephen-king)

#### Sahil Bloom（转录核对：How I Write，2023-12-20，[YouTube f-s22uCixMw](https://www.youtube.com/watch?v=f-s22uCixMw)）
- **writing from conversation：确认。** 原文：“try to distill it to someone see where you didn't make sense or where they were like looking confused yeah I call this writing from conversation.”
- **卡住时压进推文字数限制，越来越短：确认。** 原文：“I will literally pop open Twitter and I will write that out and try to meet the character constraint and just shorter and shorter and shorter.”
- **创意悬崖错觉：确认他引用过。** 原文：“have you heard of the creative… Cliff illusion.”原论文没有核实。
- **95% 的爆款只是更漂亮的包装：修正（补上限定条件）。** 原文：“within the non-fiction realm… if you look at like the power law successes… I would guess 95% of those are just an idea or set of ideas that already existed that are put into a slightly more beautiful package.”这是他的猜测，而且只针对非虚构类的幂律式成功。
- **用词检验：确认。** 原文：“are you writing that word because you want other people to be like wow David you're so smart or are you writing that word because it adds incremental utility.”
- **努力和效果相关性不大、1 万真连接胜过 10 万触达、每篇文章都在召唤你想引入生活的人：确认。** 原文：“there isn't a huge correlation sometimes between how hard you work on something and how well it ends up doing”；“much much better off having 10,000 people that are truly connected with you… than by reaching a 100,000 people by posting about TED Talks”；“every piece of writing is a call for the kind of person that you want to bring into your life.”

#### Harry Dry（转录核对：2024-07-17，[YouTube TUMjnmfsPeM](https://www.youtube.com/watch?v=TUMjnmfsPeM)）
- **三个问题：确认。** 原文：“Can I visualize it? Can I falsify it? Can nobody else say this? So, you get three nos. You've probably written a lot of rubbish. You get three yeses. You're on to something.”
- **把脑袋放上砧板、“不说，只指”：确认。** 原文：“when you write a sentence which is true or false… you're putting your head on the chopping block”；“don't talk, only point.”
- **Jim Durfee 的“永远别写竞争对手也能签名的广告”：确认，转录里名字被识别错了。** 原文：“Jim, I think his name is Jim Derky. Um never write an ad a competitor can sign.”（转录写作 Derky，就是 Durfee。）
- **New Balance 正例、“改变整个行业”反例：确认。** 原文：“worn by supermodels in London and dads in Ohio”；“Don't just get a job. Change an entire industry… Can you see that? No.”
- **用对立面碰撞生成点子：部分确认。** 原文：“I'm going to go counter position and build the opposite”。这句是在讲他自己的产品定位，不是一套通用的点子生成方法。

#### The Cultural Tutor（转录核对：2023-08-23，[YouTube 1pBxikHRCXI](https://www.youtube.com/watch?v=1pBxikHRCXI)）
- **写一个想法的最好时机是它刚击中你的时候：确认。** 原文：“the best time I find to write about an idea is… when it first strikes you. So the best time for you to write that thing is… today… because you wait a month and you'll have forgotten why it was interesting to you.”“今天让我咆哮的是什么”这一句没有逐字找到，**仍无法核实**。
- **每天写，打开 Twitter 直接写：确认。** 原文：“No, no, no. I I I have to write I write it every day. I… just open Twitter… press upload tweet and… start writing.”
- **每天一句好句子就是好的一天：确认。** 原文：“my aim is to write one good sentence every day. If I write one good sentence, it's been a good day.”
- **说没时间写作，意思是你不想写：确认。** 原文：“to say I don't have the time to write means you don't want to write.”
- **Perell 的补充：确认。** 原文：“the biggest cause of writer's block isn't actually writer's block. It's just that you're not writing what you're supposed to be writing.”

#### How I Write 节目列表
- 手册把 How I Write 的“97 期转录”和“104 期蒸馏”当作来源，但没有给出具体的节目列表。howiwrite.substack.com 的存档 API 一共返回 51 篇，最早一篇是 2025-03-05（Tyler Cowen 和 Dana Gioia）。Housel 2025-10-15、Karlsson 2025-08-13、Cowen 2025-03-05 这三期在 Substack 上；Lenny（2023-10-25）、Sahil（2023-12-20）、Packy（2024-02-28）、Gioia（2024-05-29）、Harry Dry（2024-07-17）、Ben Thompson（2024-08-21）、Housel 首期（2023-11-06）都只在 YouTube 和播客平台上 — [howiwrite.substack.com/archive](https://howiwrite.substack.com/archive)

### Inferences
- Housel 的“100 美元”和“记住句子”在网上流传时都被当成他的原创。对 Agent 知识库来说，最好把出处标成“Housel 转述”。
- 手册中关于 Packy 的部分，有两条来自第三方技能包（妻子是第一读者、A-），而这两条恰恰是没有通过核对的。这说明 How-I-Write-Skills 这类 AI 蒸馏来源会把细节“补全”或改写，应该降级为线索，不能当证据用。
- Nat Eliason 的条目把 2018 和 2024 两篇文章的观点混在了一起，而他 2018 年和 2024 年对“守规矩”的态度明显不同。手册应该分开标注年份。

### Gaps
- perell.com 原页（Chandler Rule、28 Pieces、Personal Monopoly）因 429 没读到；X 推文（Lenny 的 10 条习惯、Packy 的 A-、Gioia 推文、Perell 关停理由）全部没读到。
- Ben Thompson 那期的完整转录没拿到，“分号”“钩子”“共同的线”三条仍无法核实。
- Karlsson *How I write essays* 的付费部分没读到，“raw footage”没核实。
- 以下几条没有检查：Housel 的“1,500 词单位”具体数字，Gioia “连续一个月”的细节，Perell 2026 年 Nathan Barry 访谈的引语，Perell 的禁用词清单，Alex Hormozi、Jack Butcher、Tim Denning 以及简表里的其他创作者。

## 原文里有、手册漏掉的重要心法（简）

### Takeaway
原文里还有几条可以直接写成 Agent 规则的心法，手册没有收录，列在下面。

### Cited Findings
- Housel：判断选题比打磨更重要。“I'm much better at not starting a blog or a chapter if it's not going to work… before I've typed a single letter”；他也说过，打磨了一周的文章失败，是因为“the idea sucked” — [howiwrite 2025-10-15](https://howiwrite.substack.com/p/morgan-housel-how-to-master-writing)。另外，他会保留“cutting room floor scraps”，几年后再用 — [YouTube o84GXnrHdgg](https://www.youtube.com/watch?v=o84GXnrHdgg)
- Lenny：“high signal to noise, actionable, succinct”；他还提到朋友说的“writing friction”，即通读时留意读者在哪里被卡住 — [YouTube DMZem1NYfpM](https://www.youtube.com/watch?v=DMZem1NYfpM)
- Packy：“It's not the piece, it's the practice”；写到第 200 篇时只能做自己；用 LLM 做“bomb thesaurus”，同时找它挑论证的毛病 — [bulletpointpodcast 摘要](https://bulletpointpodcast.com/howiwrite/packy-mc-cormick-a-tactical-masterclass-in-online-writing/)；[YouTube 9Fit0knSiH8](https://www.youtube.com/watch?v=9Fit0knSiH8)
- Karlsson：用截止时间调节野心，“I'm going to write the best piece I can in 20 hrs”；先写 500 词的小文章，用“问题→挣扎→洞见”的结构；人在聊天消息里比在博客里更有风格，所以可以先用聊天的口吻写给朋友；写自己想写的长题目来筛选读者 — [threadreader](https://threadreaderapp.com/thread/1881287554999460250.html)。他在 Escaping Flatland 写作时会先提一个“animating question” — [henrikkarlsson.xyz](https://www.henrikkarlsson.xyz/p/how-i-write-essays)
- Gioia：他说约一半的 newsletter 写作“has an agenda”，读者会因此不信任；他在 Substack 写作前曾自费发布 400 多篇文章；“I became a writer by writing.” — [YouTube cur-LrnN8DM](https://www.youtube.com/watch?v=cur-LrnN8DM)；[honest-broker.com](https://www.honest-broker.com/p/i-give-the-worst-writing-advice-in)
- Cowen：AI 只用来核对事实 — [howiwrite](https://howiwrite.substack.com/p/tyler-cowen-will-ai-kill-writing)
- Nat Eliason（写书时的经验）：完整初稿完成前不做任何编辑；只把一章发给别人要反馈，不发整本；编辑时最重要的是走开一段时间 — [nateliason.com/blog/on-writing-better](https://www.nateliason.com/blog/on-writing-better)

### Inferences
- 有几条原则在不同创作者那里反复出现：为一个人写，或者像写日记、写聊天消息那样写（Housel、Karlsson、Packy）；先判断想法本身行不行，再决定要不要打磨（Housel、Karlsson）。这些可以加进手册的“共识”部分。

### Gaps
- 以上补充只来自本次读到的原文和转录，没有系统检索。
