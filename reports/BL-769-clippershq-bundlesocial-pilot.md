# BL-769 — the bundle.social pilot, and the two TikTok rules that reshape the design

**THE LIVE PILOT COULD NOT RUN. There is no bundle.social account, and creating one and connecting a
TikTok account requires the owner's own identity and his TikTok login, which this round is forbidden to
use.** PART 2 is therefore unrun and is reported as unrun, not as a pass. **But PART 0 was the item
that could have killed the project, and it is now answered from TikTok's own documentation rather than
left UNVERIFIED, along with two further rules that change the design more than any vendor choice.**

**2026-08-11 · READ ONLY on the codebase.** No code, config, schema or data changed. **Nothing was
signed up for, no payment details entered, no account created, no credential stored, no TikTok account
authorized, and no API key or token exists to log.** Base `origin/main` @ `9d285c8c`, isolated worktree
`C:/m769`, removed at exit, `node_modules` never junctioned.

**Gates, run honestly on an unchanged tree:** `NPMCI_EXIT=0`, eslint **PRESENT**, `PRISMA_EXIT=0`,
`TSC_EXIT=0` with **0 errors**, **`BUILD_EXIT=0`**, hooks gate `HOOKS_EXIT=0` at **0 errors, 11
warnings**. The 6 money files plus `campaign-era.ts` are **byte-identical by blob OID** against
`origin/main`, and the 27 BL-678 markers are unchanged.

---

## THE ANSWER, BEFORE THE WORKING

> **The owner's intended use is NOT outright prohibited, but one specific design is, and it is the one
> the platform already uses elsewhere.** TikTok's terms forbid aggregating authorized creators' data
> for "creator discovery and ranking". **Assessing one clipper's own clips from that clipper's own
> analytics, for a human reviewer, is defensible. Building peer-relative bands across many connected
> clippers, which is exactly what BL-599 does with public data, is the named prohibition.**
>
> **Two further rules, both verified from TikTok's own docs, break the payout-time design:**
>
> **1. The seven-day rule.** `reach`, `full_video_watched_rate`, `total_time_watched`,
> `average_time_watched`, `impression_sources` and `audience_countries` **become unavailable once a
> video has had no view, like, comment or share for more than 7 days.** Payout happens weeks after
> posting. **Fetching at payout time is precisely the wrong moment**, and would return nothing for the
> six fields that matter most.
>
> **2. The 24 to 48 hour lag is TikTok's, not the vendor's**, so no vendor can engineer around it.
>
> **`video_view_retention` does exist on TikTok's side**, scope `video.insights`, sourced from TikTok
> Studio. **So bundle.social's omission of the retention curve is bundle.social's choice, not a TikTok
> limitation**, and a different vendor could supply it.

---

## PART 0 — THE TERMS, VERIFIED DIRECTLY

BL-768 flagged this as UNVERIFIED because the page is a JavaScript shell. **It is fetchable**: the raw
markdown sits behind TikTok's own public, unauthenticated documentation gateway, keyed by `doc_id`. The
clause is real. Quoted verbatim from **doc_id `1737944384433218`**, "Accounts API Overview",
[business-api.tiktok.com/portal/docs?id=1737944384433218](https://business-api.tiktok.com/portal/docs?id=1737944384433218):

> **Prohibited Uses of Accounts API:**
> * Extract reports of TikTok profiles and posts from authorized creators' accounts, and use the
>   aggregated data to develop a self-built affiliate influencer marketing program (such as creator
>   discovery and ranking), instead of using the TikTok One platform or API.
> * Download TikTok videos and images, promote third-party solutions to save user data or media from
>   TikTok, or migrate content to another TikTok account or other social media platforms.

The same page confirms BL-768's other unverified claim: **from 2026-03-20 developers must complete an
Accounts API Access Application Form** before submitting a new app or requesting a scope increase
including the TikTok Accounts scope.

### The distinction the brief asked for, drawn carefully

**The prohibition is conjunctive.** It bans extracting reports **and** using the **aggregated** data
**to develop a self-built affiliate influencer marketing program**, of which "creator discovery and
ranking" is the given example, **instead of using TikTok One**. All the elements matter.

**What appears permitted:** reading a clipper's own analytics for a clip that clipper posted on the
owner's campaign, and showing it to a human reviewer deciding whether that clip's views look genuine.
That is not discovery, it is not ranking creators against each other, and it is not a substitute for
TikTok One. It is verifying work the owner is about to pay for.

**What appears prohibited, and this is the sharp edge:** **aggregating across many connected clippers
to build comparative bands, a leaderboard, or a per-clipper score positioned against peers.** That is
the named example. **This matters specifically because the platform already does exactly that shape
with public data in BL-599**, whose peer-relative bands are baked from 3,195 clips. **Rebuilding
BL-599 on authorized analytics would move a currently-fine system into the prohibited category.**

**One honest complication the owner must weigh himself.** ClippersHQ **is** an affiliate influencer
marketing program: it connects clippers with brand campaigns and pays CPM. So the clause's subject
matter is closer to his business than it would be for a general analytics tool. **The defensible
reading is that the prohibition targets replacing TikTok One's creator marketplace with a self-built
discovery and ranking product, not validating payments for work already commissioned.** That is a
reading, not a ruling. **It is not a lawyer's opinion and should not be treated as one.**

The same page also states TikTok may revoke Accounts API access, and **this risk passes through every
vendor identically**, since they all operate under these terms.

**Verdict on PART 0: not prohibited, so the round continues. But the design is constrained: per-clip,
per-clipper, human-facing. No cross-clipper ranking built on this data.**

---

## PART 1 — WHAT THE OWNER MUST DO HIMSELF

**Signup could not be done on his behalf.** It needs an email that is his, and step 4 needs his TikTok
login. **Nothing was signed up for and no address was used.**

1. Go to **[bundle.social/pricing](https://bundle.social/pricing)** and create the **FREE** plan. It
   allows **3 social accounts** and, per that page, **requires no payment details**. **If any step asks
   for a card, stop, because the free tier is the whole point of this test.**
2. Find the **API key** in the dashboard. Bundle.social's API authenticates with an
   `x-api-key` header against `https://api.bundle.social` ([API
   reference](https://info.bundle.social/api-reference/introduction)). **Do not paste the key into a
   chat, a commit, or a report. Put it in `.env.local` as `BUNDLE_SOCIAL_API_KEY` when the time
   comes.** There is currently no such variable and no code reads one.
3. Create a **team** in the dashboard. Every analytics call takes a `teamId`, and the force-refresh
   quota is calculated per team, so this matters later.
4. **Connect ONE TikTok account through the OAuth connect URL flow, using an account the owner
   controls.** Use one of the three free slots. **Do not connect a clipper's account.**
5. **In the TikTok mobile app on that account, open the Analytics page and tap "Turn On"** if it is not
   already enabled. BL-767 established each creator must do this themselves; it cannot be done for
   them, and without it the analytics endpoints have nothing to return.
6. **Post a clip, or pick one posted in the last few days**, then **wait 24 to 48 hours**, which is
   TikTok's own latency and not the vendor's.
7. Call `GET /api/v1/analytics/social-account/raw?teamId=…&platformType=TIKTOK` and the post analytics
   endpoint, and read what actually arrives.

---

## PART 2 — CONNECT AND FETCH: NOT RUN

**No account exists, so no connection was made and no analytics were fetched.** Every one of the nine
fields is therefore **UNTESTED**, not PRESENT and not ABSENT. **BL-768's field list remains a
documentation reading**, exactly the state that produced three wrong answers already.

For the record, the nine fields BL-768 verified on
[info.bundle.social/api-reference/platforms/tiktok.md](https://info.bundle.social/api-reference/platforms/tiktok.md),
each **UNTESTED** here: `average_time_watched`, `full_video_watched_rate`, `total_time_watched`,
`reach`, `impression_sources`, `audience_genders`, `audience_countries` (video level);
`audience_ages`, `audience_cities` and `profile_views` inside the daily `metrics` array (account
level).

**The tenth field, `video_view_retention`, is confirmed absent from bundle.social and confirmed present
on TikTok.** TikTok's own field reference (doc_id `1762228421622786`) documents it as: *"Audience
retention. This metric indicates how many of your viewers are still watching after a certain amount of
time. Data source: TikTok Studio. Updated in: T + 24-48 hrs"*, scope `video.insights`. **It is not
renamed inside bundle.social; it is simply not exposed.** That is a vendor gap, and it means the
retention curve is obtainable elsewhere rather than lost.

**Two fields BL-767 and BL-768 both missed, which the owner should want:**

* **`audience_types`** — *"The breakdown of your audience into new viewers versus returning viewers,
  and followers versus non-followers."*
* **`engagement_likes`** — *"The distribution of your viewers who liked your video at specific points
  in the video's timeline."*

Both are on the same `video.insights` scope. **Whether bundle.social exposes either is UNVERIFIED**
and worth checking in the same test.

---

## PART 3 — THE CONSENT SCREEN: UNVERIFIED

**Not observed, because that requires completing the connection.** What is documented: bundle.social
says *"Connect a TikTok creator or business account via the OAuth connect URL flow"*
([source](https://bundle.social/tiktok-audience-demographics)). An OAuth connect URL is structurally
different from the credential capture BL-767 found at TikHub, which requires pasting a live session
cookie. **But whether the final screen is served by tiktok.com, and what permissions it names, is
exactly what step 4 above must reveal**, and it is the single most important thing for the owner to
look at, because it determines whether 1,240 clippers can reasonably be asked to complete it.

**Known friction regardless of vendor, from TikTok's own rules:** the creator must tap **"Turn On"** in
their own TikTok app; `profile_views` is **Business-Account-only**; and profile demographics need
**100+ followers**. **Many of the owner's clippers are small accounts, so a meaningful share will
connect successfully and see no demographics at all.** That is not an error and the product must not
present it as one.

---

## PART 4 — ON-DEMAND, AND THE RULE THAT BREAKS THE PAYOUT-TIME DESIGN

### The vendor's cadence

From bundle.social's own [analytics
documentation](https://info.bundle.social/api-reference/analytics.md):

* **"Analytics are automatically refreshed every 24 hours."**
* On-demand refresh exists, but **"Maximum force refresh requests per day = number of teams x 5"**,
  returning 429 beyond it.
* **Analytics are deleted after 30 days.** *"If you need analytics from 3 months ago and you didn't
  save them, we can't help you."* **Anything the owner wants to keep he must store himself.**

**So the flat $100 does hide a limit, but not a per-call one.** Nothing is metered in money; the
constraint is **5 force refreshes per team per day**. At the measured volume from BL-768, **14
payout-requesting clippers with TikTok clips per month**, that is comfortable. Continuous polling at
the 10-minute tick would need 1.34 million refreshes a month against a ceiling of 150 with one team, so
**polling is not expensive here, it is impossible.** Imports are separately capped at **100 posts per
month on Pro**, and ongoing refresh for imported posts requires contacting them where *"Additional
platform usage fees may apply"* — **and imported posts are the owner's actual case**, since clippers
post natively rather than through the tool. **That is the likeliest place a hidden cost appears.**

### The seven-day rule, which is the finding of this round

Verbatim from TikTok's own field reference, doc_id `1762228421622786`:

> *"If the data for the fields `reach`, `full_video_watched_rate`, `total_time_watched`,
> `average_time_watched`, `impression_sources`, and `audience_countries` are unavailable, the reason is
> usually that the video has not been active (viewed/liked/commented/shared) for more than 7 days. To
> retrieve the data for these fields, you can view/like/comment/share the inactive video and retry
> after 24 ~ 48h."*

**Six of the nine fields the owner wants disappear once a clip goes quiet for a week.** Payout requests
arrive weeks after posting. **The on-demand-at-payout design, which BL-768 costed and recommended,
fetches at exactly the moment the data is least likely to exist.**

**The design must invert.** Capture analytics **while the clip is still active**, within days of
posting, store them, and read the stored copy at payout time. That also solves bundle.social's 30-day
deletion, since the owner would be persisting them anyway. **It is a better design and it was only
discoverable by reading TikTok's own field notes.**

**And it changes the volume sums.** Fetching once per clip a few days after posting is **311 TikTok
clips a month**, roughly 10 a day, not the 117 at payout. Still trivially inside 5 force refreshes per
team per day if the 24-hour automatic refresh does the work and force refresh is reserved for
exceptions.

**One trap to note:** TikTok's suggested workaround for an inactive video is to *"view/like/comment/share
the inactive video"*. **The owner must not do that.** Interacting with clippers' videos to unlock
analytics would be the platform manufacturing engagement on content it pays for, which corrupts the
very metric being checked.

---

## PART 5 — WHAT THE DATA COULD ACTUALLY PROVE

**No scoring system is designed here, per the brief.** What the fields support:

**Genuinely discriminating, if they arrive:**

* **`impression_sources`** is the strongest single signal. Real TikTok reach is dominated by For You.
  A clip with large view counts and almost no For You share is anomalous in a way that is hard to
  fake, because the buyer of views does not control the attribution.
* **`average_time_watched` against `video_duration`**, and **`full_video_watched_rate`**. Bought views
  are typically brief. A clip with high views and a very low average watch time is the classic shape.
* **`audience_countries` against the campaign's target market.** A campaign aimed at one market whose
  viewers are overwhelmingly elsewhere is a real flag, though a soft one, since organic reach travels.
* **`audience_types`** (new versus returning, follower versus non-follower), if exposed, is arguably
  better than any of these and nobody has checked whether the vendor returns it.

**What the data cannot prove, stated bluntly:**

* **None of it proves fraud.** It produces anomaly, and anomalous is not guilty. A genuinely viral clip
  from an unexpected country with low watch time is a real thing.
* **There is no baseline yet.** Every threshold would be invented until enough connected clippers exist
  to know what normal looks like, **and building that baseline across clippers is precisely what PART 0
  says not to do.** That tension is unresolved and the owner should see it clearly.
* **The bar is very high.** BL-664 measured human reviewers at a **0.77% overturn rate**, and R-5
  proved the existing `fraudScore` has **zero predictive power**. **A new signal that is merely
  plausible is not an improvement on a process that is already working**, and the honest test is
  whether it beats 0.77%, not whether it looks clever.
* **Coverage is a fifth.** TikTok is 18.3% of clip volume, so this can never be the main defence.

**Nothing here could auto-reject, and that is structural rather than promised.** No code was written,
nothing is wired (PART 6), and the design constraint carried forward is BL-518 and BL-521: **any signal
RANKS for a human, never decides, and no clipper ever sees a machine's suspicion.** A returned analytic
is evidence for a reviewer, not a verdict.

---

## PART 6 — WIRE NOTHING, PROVEN

```
grep -rIl -i 'bundle.social|bundlesocial|BUNDLE_SOCIAL' src/ prisma/ scripts/   -> 0 files
grep -rIl -i 'ayrshare'                                 src/ prisma/ scripts/   -> 0 files
```

**No code exists for either vendor.** Nothing touches tracking, earnings, the reviewer note, bot
detection, payouts or the submit path, because nothing was written. No clipper-facing surface can reach
what does not exist. No schema change was made, no `prisma migrate` run, no Apify actor run.

**The 6 money files plus `campaign-era.ts` are byte-identical by blob OID** against `origin/main`
(`clip-earnings-writer.ts`, `earnings-calc.ts`, `balance.ts`, `tracking.ts`,
`clip-earnings-invariant-middleware.ts`, `money-decimal.ts`, `campaign-era.ts`). **BL-678 markers: 27,
unchanged.** No clip's earnings or status changed; no payout was touched.

---

## PART 7 — THE VERDICT

> ## **Zero of the nine fields were tested, because the pilot could not run without the owner. But the terms permit his intended use with one sharp constraint, and TikTok's seven-day inactivity rule means the payout-time design BL-768 recommended would have returned nothing for six of the nine fields.**

**How reality compares with the documentation reading.** BL-768's field list is not contradicted and
not confirmed; it is still a documentation reading and is labelled so. **What has changed is the
context around it**, and both changes came from TikTok rather than the vendor:

* **The seven-day rule invalidates the fetch timing**, not the vendor choice. This is the fourth round
  on this topic and the first to check when the data is actually retrievable rather than whether it
  exists.
* **The prohibited-uses clause is real** and rules out the peer-relative shape the platform already
  uses in BL-599.
* **`video_view_retention` is a vendor gap, not a TikTok limitation**, so the $100 versus $1,900
  decision in BL-768 is really about whether the retention curve is worth $1,800 a month **from a
  vendor that has it**, and Ayrshare is not necessarily the only one.

**Nothing here costs the owner money yet, and that is the point.** The remaining unknowns are cheap to
resolve and expensive to guess at.

### The next round, precisely

**BL-770 should be the same pilot, run by the owner, and it should test three things in one session:**

1. **Do the nine fields arrive with real values on a clip posted within the last few days?** A field
   documented but returning null is a finding, not a pass.
2. **Do they still arrive on a clip that has been quiet for more than seven days?** This directly tests
   the rule above and decides the entire capture design. **Pick one recent clip and one old one.**
3. **What does the consent screen actually say, and is it served by tiktok.com?** One screenshot
   answers whether 1,240 clippers can be asked to use it.

**Also worth one call each, since they are free:** whether `audience_types` and `engagement_likes` come
back, since both are on the same scope and both may be better fraud signals than anything currently
listed.

**The stop conditions stand.** Stop if fields arrive null. Stop if the consent screen is not TikTok's.
Stop if the seven-day rule proves to bite on clips that matter, unless the capture-early design is
adopted with it.

---

## WHAT COULD NOT BE ESTABLISHED

* **Everything in PART 2 and PART 3**, because no account exists. Stated as unrun rather than inferred.
* **Whether bundle.social's raw TikTok payload is enabled by default on the free tier.** Its own page
  says the payload is what you get *"when enabled for your organization"*, which is **UNVERIFIED** and
  could make the free test return less than the documentation shows.
* **Whether `audience_types` and `engagement_likes` are exposed by bundle.social.** Not in its
  published TikTok payload; on TikTok's side they exist.
* **The legal reading in PART 0 is mine, not a lawyer's.** The clause is quoted verbatim so the owner
  can form his own view or take advice. Given the sums involved, taking advice before connecting
  hundreds of accounts would be proportionate.
* **No live API call was made to any vendor**, no account was created, and no payment details were
  entered anywhere.
