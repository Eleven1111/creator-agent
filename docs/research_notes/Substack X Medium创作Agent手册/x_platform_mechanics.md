# X (Twitter) Platform Mechanics for a Creator Automation Agent (as of Nov 2026)

> Method note: In this session only github.com could be fetched directly. docs.x.com, help.x.com, postproxy.dev, opentweet.io, tech-ish.com and other hosts failed DNS resolution (outside the sandbox allowlist). As a result:
> - **Code-verified** claims below were read directly from a shallow clone of `xai-org/x-algorithm` (HEAD `b220448`, committed 2026-11-03) and from `twitter/the-algorithm-ml` on GitHub.
> - Claims marked **[snippet-only]** come from search-engine summaries of pages I could not open. Treat them as unverified until someone checks the primary page.
> - Official X help-center and developer-docs pages were never opened directly. Their content here is snippet-level only.

## 1. The recommendation algorithm: what is known from code vs. folklore

### Takeaway
X's current "For You" ranker is open source in `xai-org/x-algorithm`: a Grok-derived transformer ("Phoenix") predicts the probability of about 20 actions, then a weighted sum ranks posts. The code shows these defaults: reply (5.0), quote (5.0), DM share (5.0) and copy-link share (20.0) far outweigh a like (0.66). Strong negative signals carry very large penalties: report −234, mute −58.8, "not interested" −52.3. I found no explicit Premium boost and no explicit external-link penalty in the current code. Both were part of the 2023 codebase or of folklore. Musk and product head Nikita Bier publicly said in July 2026 that the link penalty is gone.

### Cited Findings
**Repo and architecture (2026, Grok-era)**
- X published its Grok-based recommendation code as `xai-org/x-algorithm`, reportedly first released around Jan 20, 2026 under Apache 2.0. It has had large updates since, including one reported on May 15, 2026 at about 187 files changed and 18k+ lines **[snippet-only for dates]**. Sources: [ppc.land](https://ppc.land/xs-algorithm-source-code-drops-what-it-reveals-about-the-platforms-feed-mechanics/), [keywordseverywhere](https://keywordseverywhere.com/news/social-algorithm-updates/x-algorithm-open-source/), [explainx](https://www.explainx.ai/blog/x-algorithm-open-source-github-elon-musk-2026).
- The README lists further updates on Aug 13, 2026 (a major release adding visibility-filtering, SimClusters and Phoenix model code), Aug 14, Sep 18, Oct 8, Oct 13 and Oct 26, 2026. The Oct 26 update removed a `Brazil2026ElectionFilter`. The main branch had 62 commits at the time of reading. — [GitHub xai-org/x-algorithm README](https://github.com/xai-org/x-algorithm)
- Pipeline, from the README:
  - **Thunder** is an in-memory store of recent posts from accounts the viewer follows (in-network candidates).
  - **Phoenix retrieval**, **SimClusters** and `popular_posts_source` supply out-of-network (OON) candidates.
  - **Home Mixer** orchestrates the steps: query hydration → candidate sources → hydration → pre-scoring filters → scoring → top-K → post-selection filters. A separate blending pipeline then adds ads, Who-to-Follow and prompts.
  - **VMRanker** reorders results using a determinantal point process (DPP) for diversity.
  - **Visibility filtering** returns one of ALLOW / NOTICE / INTERSTITIAL / DROP for each post.
  - Source: [GitHub README](https://github.com/xai-org/x-algorithm)
- Actions Phoenix predicts, per the README:
  - Engagement: favorite, reply, repost, quote, share, share via DM, share via copy link.
  - Clicks: post, profile, link, photo expand, video open, quoted post.
  - Attention: video quality view, dwell, dwell time, click dwell time, video continuation seconds, profile visit seconds.
  - Follow author.
  - Negative signals: not interested, mute author, block author, report, not dwelled.
  - Source: [GitHub README](https://github.com/xai-org/x-algorithm)
- How the score is computed: Final Score = Σ (weight_i × P(action_i)). The README warns that the weights scale *predicted probabilities*, not raw counts, so a weight ratio is not an exchange rate between likes and reports. — [GitHub README](https://github.com/xai-org/x-algorithm)

**Default action weights, read from code** — [home-mixer/params/param.rs](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs)
- Positive: FavoriteWeight 0.66 · ReplyWeight 5.0 · BidirectionalFollowReplyWeightBoost 15.0 (replies between mutual follows) · RetweetWeight 1.0 · QuoteWeight 5.0 · ShareWeight 2.0 · ShareViaDmWeight 5.0 · ShareViaCopyLinkWeight 20.0 · FollowAuthorWeight 4.0 · ClickWeight 0.3 · OpenLinkWeight 0.2 · ContClickDwellTimeWeight 0.4 · DwellWeight 0.05 · ContDwellTimeWeight 0.006 · PhotoExpandWeight 0.05 · VideoOpenWeight 0.02 · QuotedClickWeight 0.05 · PostUnexploredWeight 0.015.
- Set to 0.0: ProfileClickWeight, VqvWeight (video quality view), PostVideoWeight.
- Negative: NotInterestedWeight −52.272 · MuteAuthorWeight −58.8 · BlockAuthorWeight −31.2 · ReportWeight −234.0 · NotDwelledWeight −0.02.
- Caveat: these are defaults wrapped in `param!` feature switches (for example `rust_home_mixer_reply_weight`). Production values can be overridden by experiments, so the live weights are not guaranteed to match.

**Other mechanics read from code**
- Score multipliers: the final score is multiplied by an `author_diversity` factor and an `oon` (out-of-network) factor. Author diversity is computed as `(1 − floor) × decay^exponent + floor`, so each additional post from the same author in a feed decays toward a floor. Replies and reposts from followed accounts can also receive the OON treatment (`oon_rescore_in_network_replies_retweets`). — [xai-value-model/scoring.rs](https://github.com/xai-org/x-algorithm/tree/main/xai-value-model)
- In the open-source scorer, `author_diversity_decay` and `author_diversity_floor` default to 1.0 (no effect), and `effective_oon_weight` defaults to 1.0. The production values are therefore not public. — [home-mixer/scorers/value_model.rs](https://github.com/xai-org/x-algorithm/tree/main/home-mixer/scorers); [xai-value-model/inputs.rs](https://github.com/xai-org/x-algorithm/tree/main/xai-value-model)
- New and small-author boost (`author_cold_start.rs`). It uses Thompson sampling over Beta priors (ColdStartBetaAlpha0 0.75, ColdStartBetaBeta0 49.25) and applies to:
  - posts from authors under ColdStartImpressionThreshold = 200 impressions,
  - authors with ColdStartFollowerCap = 50,000 followers or fewer,
  - posts no older than ColdStartMaxPostAgeSecs = 7200 (2 hours).
  - Lifted posts are moved to slots 15–16 (ColdStartSlotMin and ColdStartSlotMax).
  - Source: [param.rs](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs)
- Pre-scoring filters include AgeFilter (drops posts older than 48 hours from For You candidates), PreviouslySeenPostsFilter, MutedKeywordFilter, AuthorSocialgraphFilter (blocks and mutes), NewUserMinEngagementFilter, OONRetweetReplyFilter and DropDuplicatesFilter. Post-selection filters include visibility filtering (VFFilter) and DedupConversationFilter. SimclustersMaxCandidateAgeHours = 48. — [README](https://github.com/xai-org/x-algorithm); [param.rs](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs)
- The repo also contains anti-abuse and spam services (`botmaker`, `botmaker-rules/scarecrow`, `abuse-enforcement-service`, `user-cred-v2` for user credibility, `safety-label-*`). Automated behavior is scored by these systems, not only by the ranker. — [repo tree](https://github.com/xai-org/x-algorithm)
- Separate servers exist for For You, Following and a "ranked Following" feed (`for_you_server.rs`, `following_feed_server.rs`, `ranked_following_feed_server.rs`), so "Following" can be either chronological or ranked. — [home-mixer/](https://github.com/xai-org/x-algorithm/tree/main/home-mixer)

**Links**
- No explicit URL penalty parameter exists in the current home-mixer. `has_url` appears only as a content feature in a VMRanker debias or experiment payload (`vm_ranker_debias_payload.rs`), alongside `has_video`, `weighted_text_len` and `newline_count`. Phoenix still predicts `open_link` and weights it 0.2. Code-verified: [home-mixer/scorers](https://github.com/xai-org/x-algorithm/tree/main/home-mixer/scorers)
- PPC Land argues there is no explicit penalty, but that the model implicitly demotes links because link clicks take users off-platform and lower dwell **[snippet-only]**. — [ppc.land](https://ppc.land/how-xs-algorithm-silently-kills-your-links-without-explicitly-penalizing-them/)
- On Jul 29, 2026, Musk replied to Paul Graham that X has not penalized link posts "for over a year". This followed Nikita Bier telling Mark Zuckerberg that links no longer need to be hidden in replies **[snippet-only]**. — [ppc.land](https://ppc.land/x-drops-year-old-link-penalty-musk-tells-zuckerberg-on-platform/); [Siècle Digital, 2026-07-31](https://siecledigital.fr/2026/07/31/elon-musk-affirme-que-x-ne-penalise-plus-les-publications-contenant-un-lien-externe/); [Free Press Journal](https://www.freepressjournal.in/amp/tech/x-product-head-nikita-bier-confirms-link-penalty-removed-over-a-year-ago-tells-mark-zuckerberg-he-can-post-them-directly)
- Earlier history: in Nov 2024, Musk hinted that X deprioritizes links. — [Washington Times, 2024-11-26](https://m.washingtontimes.com/news/2024/nov/26/elon-musk-hints-x-deprioritizes-links-keep-users-p/). X also tested in-app link handling meant to reduce link-post penalties. — [Social Media Today](https://www.socialmediatoday.com/news/x-formerly-twitter-testing-links-in-app-link-post-penalties/803176/)
- Vendor data: OpenTweet analyzed 28,124 posts from Jan 1 to Oct 10, 2026. The median account's link posts received 1.05× the impressions of its non-link posts. This is vendor research, not peer-reviewed **[snippet-only]**. — [opentweet](https://opentweet.io/answers/does-x-penalize-links-2026)

**Premium boost**
- The 2023 Twitter code reportedly had a Blue-verified author multiplier of 4.0× in-network and 2.0× out-of-network **[snippet-only; I did not open the 2023 file]**. — [Blck Alpaca](https://blckalpaca.at/en/knowledge-base/social-media/social-media-algorithms-distribution/x-twitter-algorithm-open-source)
- Glitchwire claims the same 4×/2× boost exists in the current repo. A grep of the current repo (Nov 3, 2026) for `premium`, `verified` and `blue` in Rust and Python found no ranking multiplier. Matches were limited to visibility-filtering rules, such as `LimitRepliesVerified` (replies restricted to verified users) and age-verification rules. **Code-verified absence in home-mixer; contradicts** [Glitchwire](https://glitchwire.pages.dev/news/x-open-sources-its-algorithm-again-10-things-you-need-to-know-about-how-your-fee/).
- Buffer reportedly found that Premium accounts get about 10× more reach per post, from 18M+ posts **[snippet-only, secondhand via Postsyncer]**. — [postsyncer](https://postsyncer.com/tips/best-time-to-post-on-x-twitter)

**2023 baseline (for comparison)**
- Heavy-ranker weights as of Apr 5, 2023 — [twitter/the-algorithm-ml recap README](https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md):

  | Signal | Weight |
  |---|---|
  | fav (like) | 0.5 |
  | retweet | 1.0 |
  | reply | 13.5 |
  | good_profile_click | 12.0 |
  | video_playback50 | 0.005 |
  | reply_engaged_by_author | 75.0 |
  | good_click | 11.0 |
  | good_click_v2 | 10.0 |
  | negative_feedback_v2 | −74.0 |
  | report | −369.0 |

### Inferences
- **Design for conversation and private sharing, not likes.** The default reply weight is about 7.6× the like weight. Copy-link shares weigh about 30× a like, and DM shares about 7.6×. Mutual-follow replies get a large extra boost (+15). An agent should optimize for posts that spark replies and get forwarded.
- **The largest risk is negative feedback.** One predicted "report" or "mute" outweighs dozens of likes in expected value. Spammy, repetitive or off-topic automated posts are actively costly.
- **Freshness matters a lot.** For You candidates expire after about 48 hours. The cold-start boost lasts only 2 hours and applies to authors under 50k followers, so the first 1–2 hours after posting are the decisive window for small accounts.
- **Author-diversity decay penalizes bursts.** Posting many times in quick succession likely competes with yourself within the same viewer's feed. The production decay values are not public.
- **Links:** an inline link is now probably acceptable. Because `open_link` is weighted low (0.2) and dwell is lost, a link-heavy post likely still underperforms a native post on expected value. A/B test rather than assume.
- **Premium:** the explicit 2023 multiplier is not visible in the 2026 code. Any Premium advantage now likely works indirectly, through reply prioritization, `LimitRepliesVerified`, longer posts and monetization eligibility. This is an inference, not confirmed.

### Gaps
- The production values of OON weight, author-diversity decay and floor, and the live feature-switch overrides are not public.
- I did not see the Phoenix model weights or the Grok content-understanding layer. Some sources say the latter is not in the repo **[snippet-only]**: [publora](https://publora.com/blog/x-algorithm-open-source).
- I could not verify the 2023 Premium multiplier directly in `twitter/the-algorithm`.
- There is no official X engineering-blog post on the 2026 system in my results.

## 2. Creator features and monetization

### Takeaway
Creator Revenue Sharing (2023 to Sep 2026) has been replaced by the **Original Content Rewards** program. It pays on qualified Home-Timeline impressions of *original* posts from Premium-tier viewers. Eligibility is reported as 500 verified followers plus 500k verified-user Home-Timeline impressions in 90 days, with reply impressions excluded. Rates are not published. Premium+ costs about $40/month in the US.

### Cited Findings
**Original Content Rewards eligibility and payout**
- Requirements from the help page snippet: age 18+, residence in a supported country, at least 500 verified followers, and at least 500,000 Home Timeline impressions from verified users in the last 90 days, with reply impressions excluded. Content whose value mostly comes from someone else's work does not earn qualified impressions **[snippet-only]**. — [help.x.com Original Content Rewards](https://help.x.com/en/using-x/original-content-rewards)
- Payout basis: unique views of the creator's original post by a Premium Basic, Premium, Premium+ or Premium Business subscriber, in the Home Timeline, with at least 50% of the post visible. Repeat, promoted and fraudulent views are excluded. No per-impression rate is published **[snippet-only, secondary]**. — [climbx](https://climbx.so/blog/x-original-content-rewards); [PaidHype](https://www.paidhype.com/guides/x-original-content-rewards); [International Finance](https://internationalfinance.com/technology/x-kills-revenue-sharing-to-start-paying-only-for-work-you-actually-made/)
- Timeline of the transition **[snippet-only]**:
  - Aug 7, 2026: Creator Revenue Sharing stopped accepting new enrollments.
  - Sep 7, 2026: existing members stopped earning, with a final payment around Sep 11.
  - Existing members must re-apply. One report lists Aug 28 as the first payout of the new program.
  - Sources: [tech-ish, 2026-08-08](https://tech-ish.com/2026/08/08/x-is-scrapping-creator-revenue-sharing-on-7-september-everyone-has-to-apply-again/); [DEV Community](https://dev.to/iassets/x-ended-creator-revenue-sharing-what-changed-and-who-still-owns-their-revenue-25ef)
- Old program, for context: an active Premium subscription, 500 followers, 5M organic impressions in 3 months, and a reported $30 minimum payout. These terms are superseded. — [influencermarketinghub](https://influencermarketinghub.com/x-twitter-ads-revenue-sharing/); [greyjournal](https://greyjournal.net/hustle/x-original-content-rewards-program/)
- Country coverage conflicts: about 116 vs. about 120 supported countries in different secondary sources. — [usefastlane](https://www.usefastlane.ai/blog/x-original-content-rewards-program); [sirency](https://www.sirency.com/blog/x-original-content-rewards)

**Premium pricing**
- Premium+ rose to $40/month (or $395/year, up from $22 and $229) after the Grok 3 launch in Feb 2025. — [TechCrunch, 2025-02-19](https://techcrunch.com/2025/02/19/x-doubles-its-premium-plan-prices-after-xai-releases-grok-3); [tech.co](https://tech.co/news/x-premium-price-increase-grok-3)
- X Pro (formerly TweetDeck) was moved behind Premium+ in Mar 2026 without notice. — [MacRumors, 2026-03-26](https://macrumors.com/2026/03/26/x-pro-premium-plus-restriction)
- Basic is about $3/month and Premium about $8/month in the US. Regional and app-store prices are higher **[snippet-only]**. — [opentherank](https://opentherank.com/ai-pricing/x/); [subger](https://subger.com/en/service/x-premium)

### Inferences
- Revenue now depends on *verified-viewer* reach and on originality. An agent that reposts, aggregates or "AI-rewrites" other people's content risks earning nothing from it.
- Replies do not count toward eligibility. Engagement-farming in reply threads builds audience but not payout eligibility.
- X Pro being Premium+-only matters for any manual monitoring dashboard workflow.

### Gaps
- I could not open current official pages on Subscriptions (paid follower subscriptions), Articles (long-form, Premium-gated), Communities, Spaces or video monetization in this session, so I have no verified 2026 details on them.
- No published Original Content Rewards payout rate (RPM).
- I could not confirm whether Premium tier affects payout share.

## 3. X API: tiers, pricing, limits, automation and AI policy

### Takeaway
Since Feb 2026, X's default API model is **pay-per-use** from prepaid credits, with no free tier for new developers. Reported rates are about $0.015 per post created, $0.20 per post *containing a URL* (since Apr 20, 2026), about $0.005 per post read and about $0.01 per user lookup, with a monthly read cap of 2–3M before Enterprise. Enterprise reportedly starts around $42k/month. Automated accounts must carry the "Automated" label and be linked to a human operator. AI reply bots reportedly need prior written approval from X. AI-written *text* has no disclosure requirement, but AI *media* can be labeled "Made with AI".

### Cited Findings
**Pricing**
- Pay-per-use launched publicly Feb 6, 2026 and is now the default. Credits are bought in the Developer Console and deducted per request. There is no free tier for new developers. Legacy Basic moved to pay-per-use after Jun 1, 2026 **[snippet-only; official docs.x.com pricing page was unreachable]**. — [outstand](https://www.outstand.so/blog/x-api-pricing); [postproxy](https://postproxy.dev/blog/x-api-pricing-2026/); [blotato](https://www.blotato.com/blog/twitter-api-pricing)
- Reported rates **[snippet-only]**: post read about $0.005, user profile lookup about $0.010, post create about $0.015, and post containing a link $0.20. Zernio lists post create at about $0.010, an outlier. — [opentweet price table](https://opentweet.io/x-api-pricing); [sorsa](https://api.sorsa.io/blog/twitter-api-pricing-2026); [zernio](https://zernio.com/blog/twitter-api-pricing)
- URL-post surcharge: since Apr 20, 2026, an API-created post containing a URL bills at $0.20 vs. $0.015 for a plain post. This is about 13× the plain rate (some outlets call it "20-fold", likely measured against the $0.01 rate) **[snippet-only]**. — [opentweet](https://opentweet.io/answers/does-x-penalize-links-2026); [WebProNews](https://www.webpronews.com/xs-20-fold-api-surge-for-link-posts-hits-news-aggregators-and-developers-hard/)
- Monthly read cap before Enterprise: 2M in some sources, 3M in an Oct 2026 update. Since about Oct 2026 there is reportedly a starter credit of $20 on the first card plus a match of up to $50 on the first auto-recharge, still rolling out. Full-archive search requires Enterprise, reportedly from $42,000/month **[snippet-only, conflicting]**. — [opentweet](https://opentweet.io/x-api-pricing); [xpoz](https://www.xpoz.ai/blog/guides/understanding-twitter-api-pricing-tiers-and-alternatives/)
- Third-party data resellers (TwitterAPI.io, GetXAPI) advertise cheaper reads. These are unofficial and likely ToS-gray. — [twitterapi.io](https://twitterapi.io/blog/x-api-cost-breakdown-2026); [getxapi](https://www.getxapi.com/pay-per-use-pricing)

**Automation and AI policy**
- Developer Guidelines: automated accounts must enable the "Automated" profile label, which shows under the name, and must link to a human-managed account. Non-automated apps such as analytics tools do not need the label but must still follow the technical restrictions **[snippet-only]**. — [docs.x.com/developer-guidelines](https://docs.x.com/developer-guidelines)
- The automation rules, marked as updated Apr 2026, reportedly require "prior written and explicit approval" from X for AI reply bots **[snippet-only via third parties]**. — [opentweet automation rules](https://opentweet.io/x-automation-rules); [opentweet blog](https://opentweet.io/blog/twitter-automation-rules-2026)
- AI text has no disclosure label or penalty in X's rules as of Oct 2026. The "Made with AI" label applies to AI-generated or edited media **[snippet-only, secondary]**. — [opentweet](https://opentweet.io/answers/does-x-allow-ai-generated-content); [climbx](https://climbx.so/blog/does-x-penalize-ai-generated-posts); [verifiedher](https://verifiedher.com/platforms/x)
- A Terms of Service revision effective Oct 9, 2026 reportedly addresses user responsibility for actions taken by autonomous features or agents **[snippet-only, single source]**. — [note.com](https://note.com/munou_ac/n/n0fb681d97ded?hl=en)
- The open-source repo includes anti-spam rule engines (`botmaker`, `scarecrow`) and `user-cred-v2`, which computes user credibility from the follow and engagement graph, including linked-account edges. Code-verified existence: [repo](https://github.com/xai-org/x-algorithm)

### Inferences
- **Cost model for an agent:** 3 plain posts/day is about 90 posts/month, roughly $1.35/month. The same volume with links in the post body is about $18/month. Reading 1,000 own-post metrics per day costs about $150/month. **Put links in a self-reply only if a plain post plus a URL reply is billed cheaper.** That is unverified, since the reply also contains a URL and likely costs $0.20.
- Write cost is low and read or analytics cost dominates. Design the analytics loop to batch-fetch only the agent's own recent posts.
- Suspension risks from automation rules (based on long-standing rules; current wording not verified this session): auto-likes, auto-follows, bulk or duplicate posts across accounts, unsolicited automated @mentions or replies, trend hijacking, and **AI auto-replies without approval**. Keep a human-in-the-loop for replies.
- An agent posting *as the creator* (scheduled, human-approved content) is a normal scheduling use case. An agent that autonomously replies or engages likely makes the account an "automated account" that needs the label, which would be undesirable for a creator brand.

### Gaps
- I could not open official docs.x.com pricing or rate-limit pages. Per-15-minute and per-24-hour post-creation limits (historically 100 per 15 minutes per user and about 2,400/day for app-plus-user) are unverified for 2026.
- No exact current text of help.x.com/rules/automation.
- Whether a URL in a *reply* is also billed at $0.20 is unknown (likely yes, since the charge is per URL-containing post).

## 4. Third-party scheduling and analytics tools

### Takeaway
Schedulers such as Buffer, Hootsuite and Typefully use OAuth and the official X API, so they inherit pay-per-use costs. Some tools have dropped X entirely (Later, reportedly). I found no reliable 2026 reporting on how Buffer or Hootsuite repriced X support.

### Cited Findings
- Buffer plans: Free, Essentials at about $6 per channel per month, and Team at about $12 per channel per month. No X-specific surcharge was found **[snippet-only]**. — [zernio Buffer pricing](https://changelog.zernio.com/blog/buffer-pricing)
- Later reportedly cut ties with X over API changes and demands. — [WebProNews](https://www.webpronews.com/later-cuts-ties-with-x-over-api-changes-and-musk-demands)
- Hootsuite removed its free plan in Mar 2023, citing rising API costs including X's (2023 context). — [rapidevelopers](https://www.rapidevelopers.com/md/clone/hootsuite)
- A wave of "agent-native" X schedulers built on the pay-per-use API appeared in 2026: OpenTweet, Blotato, PostEverywhere, Zernio, Publora and others. Much of the 2026 "algorithm" content online comes from these vendors, which is a conflict of interest. — e.g. [blotato](https://www.blotato.com/blog/best-x-twitter-schedulers)

### Inferences
- For a creator agent, there are two routes: (a) call the X API directly with the creator's own OAuth 2.0 user token on pay-per-use, or (b) delegate to a scheduler's API. Either way, X's API is the only compliant write path. Browser automation or scraping violates the ToS and risks suspension.

### Gaps
- No verified 2026 data on Buffer, Hootsuite or Sprout per-post X pricing changes or rate-limit handling.

## 5. Posting time, frequency, format and links: evidence quality

### Takeaway
The only large dataset found is Buffer's (8.7M posts, Mar 2026). It found weekday mornings (Tue 9–11am local) perform best. It is vendor data with modest effect sizes. Code-level facts matter more: 48-hour candidate expiry, a 2-hour cold-start window, and author-diversity decay. Evidence on threads vs. single posts and on links in replies is mostly folklore. The link-in-reply rationale was officially disavowed in Jul 2026.

### Cited Findings
- Buffer (published Mar 13, 2026) analyzed 8.7M+ posts. Best slot was Tuesday 9am, with Tue 10–11am close behind. Buffer notes there is no universal best time, and its scheduler adapts recommended slots. Buffer sells a scheduler. — [Buffer](https://buffer.com/library/best-time-to-tweet-research/)
- Postsyncer reads the same Buffer data as Wednesday being the strongest day, an interpretation that conflicts with Buffer's Tuesday headline. Picmim's "1M posts" figure conflicts with Buffer's 8.7M. — [postsyncer](https://postsyncer.com/tips/best-time-to-post-on-x-twitter); [picmim](https://blog.picmim.com/blog/best-time-to-post-on-x-twitter-2026)
- "Thread-only strategy is dead" claims (2026) are opinion pieces with no dataset. — [DEV Community](https://dev.to/tahseen_rahman/the-thread-only-strategy-is-dead-xs-2026-algorithm-shift-4jp0)
- Link-in-reply: officially said to be unnecessary since Jul 2026 (see Section 1). — [ppc.land](https://ppc.land/x-drops-year-old-link-penalty-musk-tells-zuckerberg-on-platform/)
- Code facts relevant to cadence: AgeFilter at 48 hours; cold-start window of 2 hours for authors under 50k followers with under 200 impressions; `DedupConversationFilter` collapses multiple posts from one conversation in the feed. — [README](https://github.com/xai-org/x-algorithm); [param.rs](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs)

### Inferences
- **Evidence ranking:**
  1. Code (strong for mechanisms, weak for magnitudes because of feature-switch overrides).
  2. Official statements (moderate).
  3. Vendor datasets such as Buffer and OpenTweet (moderate, with conflicts of interest).
  4. "Growth hacker" blogs (weak).
- Recommended defaults for the agent:
  - Post 1–3 original posts per day, spaced hours apart (because of author-diversity decay).
  - Schedule in the audience's local weekday morning, then learn per account from its own analytics.
  - Be available for replies in the first 1–2 hours.
  - Put the reply-provoking hook in the root post. `DedupConversationFilter` collapses multiple posts from one conversation, so a thread's root carries the distribution.
  - A/B test link placement.

### Gaps
- No rigorous 2025–2026 study on thread vs. single post, optimal frequency, or video vs. text on X.
- Sprout Social and Hootsuite 2026 X timing studies were not retrieved.
