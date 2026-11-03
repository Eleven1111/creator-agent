# Medium Platform Mechanics for a Creator Automation Agent (as of Nov 2026)

> Method note: WebFetch could not reach help.medium.com, blog.medium.com, medium.com, techcrunch.com or most third-party sites from this session, because those hosts were outside the session's allowed network domains. The only page fetched in full was github.com/Medium/medium-api-docs. Every other claim below comes from search-engine snippets, marked **[snippet]**. The help-center URLs are the official sources, but I could only read them through snippets. Verify exact wording before you build hard rules on it.

## 1. Distribution: Boost, publications, tags, feed, followers, SEO, canonical links

### Takeaway
Medium has three distribution tiers: Network Only (followers only), General Distribution (the default, algorithmic) and Boost (picked by human curators). Boost is the main lever for reach and earnings. About half of Boosts come from nominations by editors of selected publications and half from Medium's in-house curators. Writers can't nominate their own work unless they are nominators themselves. Imported posts get a canonical link to the original automatically, so cross-posting from Substack or a blog is safe for SEO. External traffic and search traffic are now rewarded financially (see section 2).

### Cited Findings
- **Distribution tiers (official):** Stories get "general distribution" by default through the recommendation algorithm, with filtering for spam and NSFW content. They can appear in the "For you" feed, in Medium Digest emails to readers who don't follow the writer, on topic pages and in the app's Explore section. A "Network only" tier pulls low-quality stories from wider distribution but still shows them to the writer's followers. [snippet] — [Help: What happens to your story when you publish](https://help.medium.com/hc/en-us/articles/360018677974-About-Medium-s-distribution-and-earnings-system)
- A third-party guide (updated June 2026) gives the same three levels: network (followers), general (interest-matched readers) and boost (human curators). [snippet, secondary] — [CMO Owls](https://www.cmoowls.com/blog/how-to-write-for-medium/); older summary at [Kristina God](https://kristinagod.com/do-you-know-the-three-distribution-categories-on-medium/)
- **Who nominates for Boost:** Editors in the Boost Nomination Program can nominate stories in their topic area, including stories outside their own publications. Medium's internal curation team then reviews each nomination against its distribution guidelines. [snippet] — [Help: How do I nominate a story](https://help.medium.com/hc/en-us/articles/26716107269527-How-do-I-nominate-a-story-for-Boosting)
- **Share of Boosts:** Program nominations account for about half of Boosted stories. Medium's internal curation team sources the other half directly. [snippet] — [Help: Boost Nomination Program Participation](https://help.medium.com/hc/en-us/articles/26729526741399-Boost-Nomination-Program-Participation)
- **Nomination rules:** A story can't be nominated if it has already been nominated, reviewed or Boosted, is older than 6 months, has an invalid URL, or is unlisted or deleted. Nominators can add an optional note. Nominators who also write may self-nominate no more than 2 of their own stories per month. [snippet] — [Help: How do I nominate](https://help.medium.com/hc/en-us/articles/26716107269527-How-do-I-nominate-a-story-for-Boosting)
- **Nominator requirements:** To stay active, nominators must submit at least 1 nomination a month, keep an approval rate above 20% and follow Trust & Safety rules. The help page says Medium is "not reviewing new applications at this time" (no date shown). [snippet] — [Help: Participation](https://help.medium.com/hc/en-us/articles/26729526741399-Boost-Nomination-Program-Participation)
- **Outcome:** A Boosted story gets "higher priority to be distributed in readers' feeds." Declined stories get no feedback and there is no appeal. [snippet] — [Help: What happens after I nominate](https://help.medium.com/hc/en-us/articles/26716468567959-What-happens-after-I-nominate-a-story-for-Boosting)
- **Criteria page:** Medium publishes a "What makes a story great for Boosting?" page. I could not read its contents. — [Help](https://help.medium.com/hc/en-us/articles/26716922635159-Which-stories-are-eligible-to-be-Boosted)
- **Pilot history:** The program started as a pilot with about 60 publishers, then grew to about 100 publications (2023–2024). — [Blog: Meet 60 publishers](https://blog.medium.com/meet-60-publishers-in-the-boost-nomination-pilot-bb4923442864); [Help: Browse 100 publications](https://help.medium.com/hc/en-us/articles/23964242497559-Browse-100-publications-in-the-Boost-Nomination-Pilot). A third-party list of nominating publications is at [Online Writing Club](https://www.onlinewritingclub.com/p/13-medium-publications-that-can-nominate).
- **Boost reach:** Stubblebine reportedly said a Boosted story gets at least 500 additional views in its first two weeks. [snippet, secondhand, source page not identified; unverified] — attributed via a search summary; see [Zulie @ Medium: Everything about the Boost list](https://medium.com/@zulie_at_medium/list/everything-about-the-boost-aea02a8f55f9)
- **Boost and earnings:** Boosted stories earn engagement points at a higher rate. [snippet] — [Help: Earnings calculation](https://help.medium.com/hc/en-us/articles/360036691193-Calculating-earnings-in-the-Partner-Program)
- **AI and Boost:** "AI-generated writing is not eligible for distribution (let alone Boosting)." [snippet] — [Help: Nominations section](https://help.medium.com/hc/en-us/sections/26573008251543-Nominations)
- **Import and canonical link (official):** On the profile's Stories page, choose "Import a story" and paste the URL. The import tool backdates the post to its original date and adds a canonical link to the original. The author can change the canonical link later in the story settings. [snippet] — [Help: Importing a post](https://help.medium.com/hc/en-us/articles/214550207-Import-post); [Help: Set a canonical link](https://help.medium.com/hc/en-us/articles/360033930293)
- The API also supports `canonicalUrl` when creating a post (see section 4). — [GitHub medium-api-docs](https://github.com/Medium/medium-api-docs)
- **SEO:** Medium's November 2025 announcement describes Medium as one of the best writing platforms for technical SEO, and it now pays extra for search-referred member reads (section 2). [snippet] — [Medium blog: Starting November 1, we're rewarding search traffic](https://medium.com/blog/partner-program-update-starting-november-1-were-rewarding-search-traffic-3ac0635f9f6b)
- **Owning the audience:** One review warns that Medium followers can't be emailed directly by the writer, so you don't own the list. [snippet] — via search summary of [Creator Economy Tools review](https://creatoreconomytools.com/tool/medium)
- **CEO positioning:** Stubblebine calls Medium a place "to syndicate, to grow one of these other platforms." About two-thirds of stories published each month are not paywalled. [snippet; Medium's own publication, so promotional] — [Medium Handbook: Is Medium Worth It in 2026?](https://medium.com/medium-handbook/is-medium-worth-it-in-2026-194a85fb2f35)

### Inferences
- For an agent, the useful levers are:
  1. Get accepted as a writer in Boost-nominating publications, since editors there can nominate your stories.
  2. Pass the curators' quality bar, because Boost is decided by humans and can't be gamed by volume.
  3. Cross-post with canonical links back to Substack or a blog.
  4. Drive external and search traffic, which is now paid.
- Medium followers aren't an email list you own. The agent should funnel Medium readers to a Substack or newsletter signup link in each story. This also matches how the CEO himself frames Medium (syndication).
- Low-quality or high-volume posting risks Network Only distribution, so a quality gate before publishing matters more than posting frequency.

### Gaps
- I couldn't read the full Boost criteria, the distribution guidelines, the tag/topic limit (historically 5 tags, unverified here) or how follower email notifications work.
- I found no official, current data on how much Boost lifts views, and no Boost rate as a share of all stories.
- I couldn't confirm whether the nominator program has reopened applications in 2025–2026.
- For the history of "Featured"/curation (the 2023 move from in-house "distributed" curation to Boost), I found no fetched source in this session.

## 2. Monetization: Medium Partner Program (MPP)

### Takeaway
Writers are paid from paying members' subscription fees, based on member reading time plus engagement (model live since August 2023). Boosted stories get a higher engagement multiplier. A series of changes from October 2025 shifted part of the budget to external traffic (5%), search traffic (15%) and one-time conversion payments, replacing the recurring 2021–2025 referral scheme. Non-member reads earn nothing. Most writers earn under $100 a month, and the CEO says MPP alone won't support a living.

### Cited Findings
- **Eligibility (official):** You must be a Medium member, have published at least one story in the past 6 months, live in a supported country and be 18 or older. [snippet] — [Medium Partner Program page](https://medium.com/partner-program); [Help: MPP eligibility](https://help.medium.com/hc/en-us/articles/39121627791639-Medium-Partner-Program-eligibility)
  - Conflicting snippet: one help-center result says paid membership is not required to apply. Enrollment requires a bank account and tax filing in a supported country, and outlying territories are excluded. — [Help: Application and enrollment](https://help.medium.com/hc/en-us/articles/115011694187-Medium-Partner-Program-Application-and-enrollment)
  - No follower threshold appears in the official sources (the old 100-follower rule was dropped in 2023, per my background knowledge; unverified here).
  - **Country count conflicts:** one third-party guide says 119 countries as of August 2024, while an older post lists 42 and another says 77. Use the official list. — [Medium post: MPP expands to 77 countries](https://medium.com/illumination/medium-partner-program-expands-to-77-countries-b16a2668ca62); [country guide](https://medium.com/@dinojaam24/medium-partner-program-eligible-countries-a-comprehensive-guide-4d8187aae8da)
- **Payouts:** A $10 minimum that rolls over until reached, paid via Stripe. [snippet, third-party] — [Lilach Bullock MPP 2026](https://www.lilachbullock.com/medium-partner-program/)
- **August 2023 formula change:** Announced July 2023, it took effect August 1, 2023, with the first new payout in early September 2023. Member reading and listening time stayed in the formula, and claps, highlights, replies and follows were added as signals. [snippet] — [Medium blog: New Partner Program incentives focus on high-quality human writing](https://blog.medium.com/new-partner-program-incentives-focus-on-high-quality-human-writing-7335f8557f6e)
- **Current mechanics (help center):**
  - A read counts once a paying member has spent 30 seconds or more on the story, and idle time is excluded.
  - Each type of engagement (clap, highlight, reply) adds points the first time it happens, however often it's repeated.
  - Boosted stories earn engagement points at a higher rate.
  - Only paying members' activity counts.
  - Reads from a non-member or a free logged-in account earn nothing.
  - Friend Link reads don't count.

  [snippet] — [Help: Earnings calculation](https://help.medium.com/hc/en-us/articles/360036691193-Medium-Partner-Program-earnings-calculation); [Help: Earnings scenario examples](https://help.medium.com/hc/en-us/articles/16030675401879-Medium-Partner-Program-earnings-scenario-examples)
- **October 1, 2025 – external traffic:** Medium shifted "5% of the payouts toward stories that get this external traffic and especially to external traffic that converts to members." That covers social shares, search and direct links. Distribution is unchanged, and Medium said it would make changes monthly for the next six months. [snippet] — [Medium blog: Starting October 1, we're rewarding external traffic](https://medium.com/blog/partner-program-update-starting-october-1-were-rewarding-external-traffic-15cb28f75bc9); [Medium Handbook: Writer newsletter – first in a series of small changes](https://medium.com/medium-handbook/writer-newsletter-the-first-in-a-series-of-small-partner-program-changes-f59be742524d)
- **November 1, 2025 – search traffic:** Medium shifted 15% of the MPP budget to activity on stories that members find through search engines like Google, paid at a higher rate than the external-traffic bonus. [snippet] — [Medium blog: Starting November 1, we're rewarding search traffic](https://medium.com/blog/partner-program-update-starting-november-1-were-rewarding-search-traffic-3ac0635f9f6b); [Help: Earnings calculation](https://help.medium.com/hc/en-us/articles/360036691193-Medium-Partner-Program-earnings-calculation)
- **Conversion payment:** A one-time payment when a non-member becomes a paying member to read a paywalled story. It replaces the "previous referral program (2021–2025), which paid a recurring share of the new member's subscription fee." Members who cancel shortly after joining are excluded. [snippet] — [Help: Earnings calculation](https://help.medium.com/hc/en-us/articles/360036691193-Medium-Partner-Program-earnings-calculation)
- **Further changes, unverified:** A third-party guide says payout rules also changed in December 2025 and January 2026, and that an "Editor Partner Program" launches June 2026. A Substack post covers a "February 2026" MPP update, but I couldn't read it. [snippet, unverified] — [Lilach Bullock](https://www.lilachbullock.com/medium-partner-program/); [Bin Jiang Substack](https://thebinjiang.substack.com/p/medium-partner-program-update-for)
- **Membership price:** Sources conflict: one says $5/month, another $7/month. A third-party pricing page lists $5/mo or $50/yr. [snippet] — [Contentmation pricing](https://contentmation.com/p/pricing/medium-pricing); [Amy Suto comparison](https://www.amysuto.com/desk-of-amy-suto/substack-vs-medium)
- **Earnings distribution (2023):** Among authors earning $10 or more, about 65% earned $10–$100, 29% earned $100–$1,000 and 6% earned over $1,000. [snippet, secondhand quote of Medium] — [Vocal](https://vocal.media/journal/massive-changes-to-how-medium-pays-its-writers-are-you-ready)
- **December 2020 data:** 8% of writers earned more than $100, and the top story earned $8,855.75. — [Zulie Writes](https://www.zuliewrites.com/blog/how-much-do-medium-writers-make)
- **Under-$100 estimates (critics):** One critic says 92% of MPP writers earned under $100 a month when Medium last published data (date unspecified). Another estimates 94% earn under $100 a month. — [Lehewych Substack](https://lehewych.substack.com/p/the-medium-con-how-a-600-million); [Amy Suto](https://www.amysuto.com/desk-of-amy-suto/substack-vs-medium)
- **Stubblebine on pay:** He reportedly said only about 5% of writers saw a drop in earnings, and that "even as we cut other costs to make Medium profitable, we paid the writers more." This is disputed by critic writers. [snippet, secondhand] — [Lehewych Substack](https://lehewych.substack.com/p/the-medium-con-how-a-600-million)
- **Earnings decline claim:** One site claims a 70–90% income crash in early 2025 for many established writers. It's promotional and low-reliability. [snippet] — [Alidropship](https://alidropship.com/is-medium-partner-program-legit/)
- **CEO, 2026:** MPP is not how a writer makes a living. Medium is for syndication and audience growth. [snippet] — [Medium Handbook interview](https://medium.com/medium-handbook/is-medium-worth-it-in-2026-194a85fb2f35)

### Inferences
- Earnings depend on reads by paying members and on Boost. Since late 2025, bringing in external and especially Google search traffic that converts readers into members is directly paid. So SEO-optimized evergreen posts and sharing paywalled links on X or Substack now make sense.
- Because about 20% of the budget (5% + 15%) now follows off-platform traffic, the agent's "grow" module should treat Medium as a target for traffic it sends from elsewhere, not only as a closed feed.
- Revenue is too small and unpredictable for most writers to plan around. Model it as a side channel, roughly $0–$100 a month for most accounts, with occasional spikes when a story is Boosted.

### Gaps
- I have no official 2024–2026 aggregate payout distribution. Medium doesn't publish one.
- I couldn't read the exact Boost multiplier, the size of the conversion payment, the December 2025 to February 2026 changes or the Editor Partner Program details.
- The current supported-country list is unverified.

## 3. AI content policy

### Takeaway
AI-generated writing must be disclosed. Since May 1, 2024 it can't be paywalled (so it can't earn in MPP), even when disclosed. Disclosed, non-paywalled AI writing can get General Distribution but never Boost. Undisclosed AI writing is limited to Network Only. Repeat violators risk losing MPP enrollment, and later wording says possibly permanently. AI help with outlining, grammar or fact-checking is allowed.

### Cited Findings
- **Paywall ban:** "AI-generated writing (disclosed as such or not) is not allowed to be paywalled as part of our Partner Program." Effective May 1, 2024. [snippet] — [Help: AI content policy](https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy); coverage: [Plagiarism Today, Apr 11 2024](https://www.plagiarismtoday.com/2024/04/11/medium-sets-new-policies-on-ai-generated-writing/), [Dataconomy, Apr 15 2024](https://dataconomy.com/2024/04/15/medium-wont-pay-for-ai-partners), [MediaNama, Apr 2024](https://www.medianama.com/2024/04/223-medium-ai-transparency-bars-paywalled-ai-content/)
- **Penalty:** "Accounts that have fully AI-generated writing behind the paywall may have those stories removed from the paywall and/or have their Partner Program enrollment revoked." [snippet] — [Help: AI content policy](https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy)
- **Distribution:** Disclosed, non-paywalled AI writing can get General Distribution but not Boost. Undisclosed AI writing gets only "Network Only" distribution. [snippet] — [Plagiarism Today](https://www.plagiarismtoday.com/2024/04/11/medium-sets-new-policies-on-ai-generated-writing/); [MediaNama](https://www.medianama.com/2024/04/223-medium-ai-transparency-bars-paywalled-ai-content/)
- **Stricter Boost wording:** The Boost help section says AI-generated writing "is not eligible for distribution (let alone Boosting)." This is stricter than the 2024 coverage and may reflect a later change, so verify it. [snippet] — [Help: Nominations](https://help.medium.com/hc/en-us/sections/26573008251543-Nominations)
- **Allowed uses:** AI-assisted outlining, spell-checking, grammar and fact verification aren't covered by the ban. [snippet] — [Help: AI content policy](https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy); [Online Writing Club](https://www.onlinewritingclub.com/p/mediums-new-rules-for-ai-generated)
- **2025 definition:** A 2025 MPP notice, reproduced in a third-party post, defines AI-generated writing as content where "the majority of the content has been created by an AI-writing program with little or no edits, improvements, fact-checking, or changes." It says repeated violations may lead to permanent loss of MPP eligibility. [snippet, secondary] — [zidailma: A new Medium policy you didn't know](https://zidailma.medium.com/a-new-medium-policy-you-didnt-know-76a751aaaf16)
- **Not-paywallable content page:** Medium has a help page listing content that can't go behind the paywall. I couldn't read it. — [Help: Content not eligible for the paywall](https://help.medium.com/hc/en-us/articles/31090080813591-Content-not-eligible-for-the-paywall)
- **Detection and enforcement:**
  - Medium will revoke MPP enrollment from writers who publish AI-generated or other low-quality content, and deceptive or harmful content leads to immediate suspension.
  - Enforcement is case-by-case.
  - Medium says it uses "a wide variety of tools and technologies to detect and identify AI-writing… combined with human review."

  [snippet] — [Medium blog: Ramping up efforts against spam and fraud](https://blog.medium.com/were-ramping-up-efforts-to-protect-the-medium-community-from-spam-and-fraud-7efaadd76247)
- **Criticism:** AI detectors are inaccurate and can flag human writing. At least one writer left Medium over the policy. — [Plagiarism Today](https://www.plagiarismtoday.com/2024/04/11/medium-sets-new-policies-on-ai-generated-writing/); [jpolak: Why I'm leaving Medium](https://medium.com/@jpolak/why-im-leaving-medium-ai-policy-ce925cffb91c)

### Inferences
- **Design constraint for the agent:** the agent may help with ideation, outlining, editing and fact-checking. It must not publish mostly-AI drafts behind the paywall. A human-authored final draft plus a substantive-human-edit workflow is mandatory for monetized posts.
- If any AI-generated text is published, it must be disclosed and left off the paywall. Expect at best General Distribution, and possibly none under the stricter Boost wording.
- Auto-publishing AI text at scale risks losing MPP enrollment, being limited to Network Only, or account suspension. That is the biggest single risk for an automation agent on Medium.

### Gaps
- I found no public enforcement figures (accounts removed, stories de-paywalled) for 2024–2026.
- I couldn't confirm whether the disclosure mechanism has a required format (for example, mentioned in the first two paragraphs). Background knowledge says yes, but I didn't verify it here.

## 4. API and automation access

### Takeaway
The official Medium API is officially unsupported, and new integrations are blocked. Third-party reports say new self-issued integration tokens stopped being issued around January 1, 2025, while old tokens reportedly still work. Posting via an existing token can create drafts, public or unlisted posts with markdown or HTML and a canonical URL. The API can't edit, delete, read stats or schedule. RSS feeds give read-only access. The import tool is manual (one story at a time).

### Cited Findings
- **Status (fetched in full):** "The Medium API is no longer supported… We do not recommend using it." Also: "We don't allow any new integrations with our API." Browser-based OAuth is limited to existing integrations, and self-issued tokens are generated from account settings and don't expire unless revoked. — [GitHub: Medium/medium-api-docs](https://github.com/Medium/medium-api-docs)
- **Endpoints (fetched):**
  - `POST /v1/users/{authorId}/posts` and `POST /v1/publications/{publicationId}/posts`.
  - `contentFormat` (`html` or `markdown`, required), `canonicalUrl` (optional) and `publishStatus` (`public`, `draft` or `unlisted`; default `public`).
  - The publications list returns publications where the user is editor or writer, plus up to 200 others. In a publication, writers can only create drafts, which need editor approval, while editors can publish directly.
  - No rate limits are documented.

  — [GitHub: medium-api-docs](https://github.com/Medium/medium-api-docs)
- **Token cutoff:** Integration-vendor docs say Medium stopped issuing new integration tokens on January 1, 2025. Only users with a token generated before that date can connect, and those tokens keep working. [snippet, third-party] — [StackOne docs: Medium integration token](https://docs.stackone.com/connectors/medium/guides/link-account/integration-token)
- **No-code tools:** Make.com users report that Medium stopped providing integration tokens, breaking Make and Zapier posting workflows. RSS is suggested for reading Medium content only. [snippet] — [Make Community](https://community.make.com/t/integrating-medium-with-make-com/65838); see also [Drafts forum](https://forums.getdrafts.com/t/problems-with-post-to-medium-action-solved/14561)
- **2026 article:** Old tokens reportedly still work. Medium's RSS importer is for one-time migration, not ongoing auto-publishing, and native scheduling exists in the editor. [snippet, unofficial] — [TimeToPost blog (2026)](https://timetopost.co/blog/medium-api-auto-post-2026/)
- **Workarounds:** Third-party "RSS to Medium" auto-publish tools with canonical protection (2026) and browser-automation repos ("medium-publishing-without-api") exist. They have unclear reliability and terms-of-service risk. — [StartupHub.ai](https://www.startuphub.ai/ai-news/ai-tools/2026/rss-to-medium-auto-publish-blog-posts); [medium-publishing-without-api mirror](https://gh.r-mj.com/iancarson/medium-publishing-without-api)
- **RSS (read-only):**
  - Profile feed: `https://medium.com/feed/@username`.
  - Publication feed: `https://medium.com/feed/<publication-slug>`, and custom-domain publications still proxy via medium.com.
  - Feed content and full text vary.

  [snippet, third-party] — [FeedPress](https://support.feedpress.com/tutorials/importing-medium-rss-feeds); [WP RSS Aggregator](https://finder.wprssaggregator.com/rss-feeds/platform/medium); a live example at [medium.com/feed/@jpolak](https://medium.com/feed/@jpolak)
- **Import tool:** Manual "Import a story" by URL. It backdates and sets the canonical link automatically. [snippet] — [Help: Importing a post](https://help.medium.com/hc/en-us/articles/214550207-Import-post)
- **Import failures:** Reports exist of Medium failing to import some sites (2019 Webflow thread; old). — [Webflow forum](https://forum.webflow.com/t/medium-will-no-longer-import-any-of-our-articles/85974)

### Inferences
- Agent design for Medium "publish":
  1. If the user has a legacy token, call `POST /users/{id}/posts` with `publishStatus: draft` and `canonicalUrl`. A human then reviews, adds tags or a publication, chooses the paywall setting and publishes in the UI.
  2. Without a token, the agent prepares a ready-to-import source URL (Substack or blog), or a clipboard-ready markdown package, and a human-in-the-loop checklist for Import a story, tags, paywall, AI disclosure and scheduling.
  3. Use RSS to monitor the user's own published stories, and the stats dashboard manually, since there is no stats API.
- Avoid headless-browser auto-posting. It risks ToS violations and anti-spam flags, and it fits poorly with the AI policy. Defaulting to "drafts only" keeps a human in control.
- Since the API is unsupported, it could be switched off without notice. Treat it as optional with a fallback.

### Gaps
- I couldn't confirm the January 1, 2025 token cutoff on an official Medium page. It comes from a vendor doc only.
- I don't know whether pre-2025 tokens work for all accounts in late 2026. That rests on one unofficial report.
- There is no official info on Medium's partner APIs, its stats export, or whether the editor's native scheduling is available to all users.

## 5. Medium business health (platform viability)

### Takeaway
Medium has been profitable every month since August 2024. Before that it was losing $2.6M a month and carried $37M of debt. The last official member count is over 1 million paying members (April 2024). No newer official count was found. Revenue is roughly $50–60M a year by third-party estimate. The platform looks stable but small, and the CEO positions it for syndication rather than as a writer's only income.

### Cited Findings
- **First profit:** August 2024 was Medium's first profitable month ever, per CEO Tony Stubblebine (TechCrunch, Aug 21 2024). [snippet] — [TechCrunch](https://techcrunch.com/2024/08/21/august-was-mediums-first-profitable-month-ever)
- **Sustained profit:** On July 11, 2025, Stubblebine said Medium had stayed profitable since August 2024. [snippet] — [TechCrunch, Jul 11 2025](https://techcrunch.com/2025/07/11/mediums-ceo-explains-what-it-took-to-stop-losing-2-6m-monthly); also [Simon Willison, Jul 16 2025](https://simonwillison.net/2025/Jul/16/fell-in-a-hole-got-out)
- **The turnaround:**
  - Medium had been losing $2.6M a month, losing subscribers and carrying $37M in loans.
  - The fixes were layoffs, renegotiated loans, less office space and a product redesign around high-quality content.
  - Stubblebine declined to give a valuation ("We are profitable and they are not").
  - Some aggregator summaries misdate profitability to 2022 or 2023. Those are errors.

  [snippet] — [TechCrunch, Jul 2025](https://techcrunch.com/2025/07/11/mediums-ceo-explains-what-it-took-to-stop-losing-2-6m-monthly); [Fast Company interview](https://www.fastcompany.com/91407562/medium-ceo-tony-stubblebine-interview)
- **Members:** Stubblebine reported over 1 million paid members in April 2024. Earlier figures were about 725k and about 700k (2021). A 2026 review's "about 700,000" figure is likely stale. No 2025–2026 official count was found. [snippet] — [Writing Long Game Substack](https://thewritinglonggame.substack.com/p/medium-is-dead-as-a-doornail-despite); [Feedium: 725,000 paying members](https://medium.com/feedium/pssst-medium-has-725-000-paying-members-and-more-insights-you-need-to-know-now-91538530e729); [Techwise Insider](https://techwiseinsider.com/medium-review/)
- **Revenue:** About $50–60M a year by third-party estimate (unofficial). A $100M claim is unsourced. — [Writing Long Game Substack](https://thewritinglonggame.substack.com/p/medium-is-officially-cooked); [Gitnux](https://gitnux.org/medium-statistics/) (unreliable)
- **Ad strategy:** Medium refuses advertising, according to the episode title "Why Medium said no to easy ad money." — [AdExchanger](https://www.adexchanger.com/adexchanger-talks/why-medium-said-no-to-easy-ad-money/)
- **2023 context:** TechCrunch (October 2023) covered Medium's push toward profitability in 2024. — [TechCrunch, Oct 12 2023](https://techcrunch.com/2023/10/12/medium-profitability-2024-interview/)
- **Risk view:** One commentator argues LLMs threaten Medium's model (summaries and AI search cut into reads). — [BD TechTalks Substack](https://bdtechtalks.substack.com/p/how-llms-will-kill-mediums-business)

### Inferences
- Medium is viable as a medium-term syndication channel. It is profitable, has no ad dependence and its leadership is stable. Its scale (around 1M+ members, about $50–60M revenue) is modest, and MPP rules change often (six monthly changes from October 2025). The agent's Medium module should load policy and payout rules from config rather than hard-coding them.

### Gaps
- No official 2025–2026 member count, revenue or total writer payout figure was found. Nieman Lab and Press Gazette coverage didn't show up in searches.
- I couldn't read Stubblebine's own Medium posts directly, because medium.com was blocked for fetching.
