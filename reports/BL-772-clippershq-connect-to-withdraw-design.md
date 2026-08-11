# BL-772 — connect-to-withdraw and the analytics store, designed before any code

**2026-08-11 · DB `now()` = `2026-08-11 12:05:38.555189+00` · AUDIT ONLY, READ ONLY.**
No code, config, schema or data changed. Nothing built, nothing wired, no vendor called, no account
created. Base `origin/main` @ `9d285c8c`, isolated worktree `C:/m772`, removed at exit,
`node_modules` never junctioned. A markdown-only diff cannot change tsc or build, so neither was run
and neither is claimed. Every figure below is measured from live data this round. Handles redacted.

---

## THE HEADLINE, BEFORE THE DESIGN

> **Do not gate withdrawal on connecting TikTok. The measurement kills it: 59.7% of all unwithdrawn
> money, $1,673.12 across 94 clippers, was earned with ZERO TikTok involvement.** Requiring a TikTok
> connection before someone can withdraw Instagram earnings is not a strict policy, it is a broken one.
>
> **Worse, 76 of the 146 clippers holding a balance have no TikTok account at all**, holding $836.21
> between them. **They could not comply however willing.** The brief called this an edge case. It is
> the majority.
>
> **The good news is that the gate was never needed.** The money is extraordinarily concentrated:
> **the top 5 TikTok clippers hold 71.0% of all TikTok earnings, and the top 10 hold 76.1%.** Ten
> people, asked personally, deliver three quarters of the value the gate was meant to buy. **Ask them.
> Do not build a gate.**
>
> **Verdict, in one line: build the analytics store, ask ten people to connect voluntarily, and do not
> gate withdrawal at all.**

---

## PART 0 — THE POLICY DECISION, PUT TO THE OWNER

### What the population actually looks like

| | Clippers | Money |
|---|---|---|
| **Hold an unwithdrawn balance** | **146** | **$2,804.38** |
| Of those, earned **ZERO** from TikTok | **94** | **$1,673.12 (59.7%)** |
| Of those, earned something from TikTok | 52 | $1,131.26 |
| Of those, have **no TikTok account at all** | **76** | **$836.21** |
| Hold **$50 or more** | **11** | **$1,865.70 (66.5%)** |
| Hold under $50 | 135 | $938.68 |

**Of the 11 clippers holding $50 or more, 3 have no TikTok account** and hold $279.96 between them.
And several of the largest balances are entirely non-TikTok: the biggest, at $548.58, has **$0.00** of
TikTok earnings.

### The four options, measured

**Option A, applies to everyone immediately, including money already earned.**
**Affects all 146 clippers and all $2,804.38.** Strands $1,673.12 belonging to 94 people whose
earnings have nothing to do with TikTok, and $836.21 belonging to 76 people who cannot comply at all.
**Recommend against, strongly.** This platform spent BL-758, BL-762, BL-763 and BL-765 repairing
unreachable balances; BL-758 measured $830.02 unreachable across 130 clippers and it was treated as a
defect. **This option would deliberately create twice that, and the people hit hardest would be the
honest ones who simply post on Instagram.**

**Option B, applies to earnings from a cutoff date forward.**
**Affects 0 clippers and $0.00 today**, since every existing balance stays withdrawable. It is fair,
it is defensible, and it is the most code: earnings must be split by accrual date against the cutoff,
which means a per-clip date test inside the withdrawal gate and a second balance figure on every
clipper-facing surface. **The gate at `payouts/route.ts` currently reasons about totals, not vintages**,
so this is not a small change. **Fair, slow, and it still buys nothing for the 94 non-TikTok clippers,
because they will never connect regardless.**

**Option C, applies only above a threshold, for example $50.**
**Affects 11 clippers holding $1,865.70, which is 66.5% of the unwithdrawn money, while leaving 135
small clippers completely untouched.** This is the best-targeted of the gating options: it puts the
requirement where the money is. **But 3 of those 11 have no TikTok account**, so even here the gate
strands $279.96 unless it carries an exemption, and **several of the 11 have zero TikTok earnings**, so
it would still be demanding a TikTok connection from people whose money came from Instagram.

**Option D, optional with an incentive rather than a requirement.**
**Affects nobody involuntarily.** Nothing is stranded, nothing needs an exemption path, no support
queue is created. It converts fewer people, but **the concentration data in PART 1 means it does not
have to convert many.**

### The recommendation, which is the owner's call to overrule

**Recommend Option D, and only for the ten people PART 1 identifies.** The reasoning is arithmetic
rather than sentiment: **a gate's entire purpose is to reach clippers who would not otherwise connect,
and the ten who matter can simply be asked.** Every gating option pays for that reach with stranded
money belonging mostly to people the gate was never aimed at.

**If the owner wants a requirement anyway, take Option C with a threshold, never Option A**, and it
must carry the exemption below.

### The clipper who cannot connect, which is mandatory in every option

**A clipper whose TikTok account is banned, deleted, or no longer accessible must never lose money
already earned.** This is not a courtesy, it is the difference between a policy and a confiscation.
**76 clippers with a balance have no TikTok account right now**, so any gate ships with this path
already load-bearing on day one.

**The rule to implement in any gated option:** the gate may only ever apply to a clipper who **has an
approved TikTok clip account on this platform**. If they have none, the requirement does not apply and
their balance is withdrawable exactly as today. **If they have one but cannot connect it, an
owner-settable per-clipper exemption releases the balance**, recorded with a reason. **BL-696
established the platform cannot record a hand payment, so the exemption must restore normal
withdrawal rather than route around it**, or the money becomes claimable twice.

**No clipper should ever have to ask for that exemption twice, and no clipper should have to explain
why their account is gone.**

---

## PART 1 — WHO IT WOULD COVER, AND THE PILOT LIST

BL-770 measured, over 30 days, that the top 10 TikTok clippers account for 71.0% of TikTok clips.
**That is confirmed for that window.** Measured all-time, and extended to what actually matters:

| Top N TikTok clippers | Share of TikTok **clips** | Their TikTok **earnings** | Share of TikTok **earnings** | Share of their cohort's **payout volume** |
|---|---|---|---|---|
| **Top 5** | 30.3% | **$3,340.29** | **71.0%** | 75.2% |
| **Top 10** | 46.4% | **$3,583.66** | **76.1%** | 78.6% |
| Top 25 | 66.7% | $3,727.82 | 79.2% | 86.7% |
| Top 50 | 81.0% | $4,343.22 | 92.3% | 88.9% |

**The money is far more concentrated than the clips, and that is the finding.** Five people carry 71%
of all TikTok earnings while posting only 30% of the clips, because they are the ones whose clips
actually perform. **For fraud detection, earnings concentration is the relevant axis**, since the
exposure is money paid out, not clips filed.

**The pilot list is five people. The realistic target is ten.** Ten connections buy 76.1% of TikTok
earnings coverage. **Nothing about this needs 1,240 clippers, and nothing about it needs a gate.**

**The share of ALL clips, stated so the ceiling is never forgotten:** TikTok is **308 of the last 30
days' clips**, and Instagram remains roughly 70% of volume. **Even at 100% TikTok connection this
touches under a fifth of clips.** It is a targeted instrument for the highest-value TikTok clippers,
not a platform-wide fraud system, and it should be described that way internally so nobody expects
otherwise.

---

## PART 2 — THE CAPTURE-EARLY STORE

BL-769 established from TikTok's own docs that `reach`, `full_video_watched_rate`,
`total_time_watched`, `average_time_watched`, `impression_sources` and `audience_countries` become
unavailable once a clip has had **no view, like, comment or share for more than 7 days**. **The
platform must therefore capture while the clip is fresh and keep the result itself**, which is also
forced by bundle.social deleting its own analytics after 30 days.

### What is captured, and when

* **First capture at about 48 hours after submission.** Earlier returns nulls, because TikTok's own
  documented latency for these offline fields is 24 to 48 hours.
* **Then daily while the clip is still growing**, which the vendor's free 24-hour refresh cycle
  already does without consuming any force-refresh quota.
* **Stop after 7 consecutive days of flat views.** Past that the six fields expire anyway and further
  calls buy nothing.
* **One final capture at approval**, so the record a reviewer sees is anchored to the decision.

### The schema, additive and nullable

A single new table, no change to any existing one, created with `ALTER TABLE ... IF NOT EXISTS` style
DDL through `run-schema-sql.js` and **never `prisma migrate`**:

```
ClipAnalyticsSnapshot
  id                      text primary key
  clipId                  text not null    -- FK to clips, indexed
  capturedAt              timestamptz not null
  source                  text not null    -- 'bundle.social' etc, so a vendor change is visible
  viewsAtCapture          integer null
  averageTimeWatched      numeric null
  fullVideoWatchedRate    numeric null
  totalTimeWatched        numeric null
  reach                   integer null
  impressionSources       jsonb null
  audienceCountries       jsonb null
  audienceGenders         jsonb null
  audienceAges            jsonb null
  profileViews            integer null
  raw                     jsonb null       -- the untouched payload, for fields nobody anticipated
```

**Every analytic column is nullable, because a null is the honest representation of a field TikTok did
not return**, and PART 4 depends on being able to tell "not captured" from "captured as zero". **No
column on `clips` changes, and nothing here is read by any money path.**

### The late viral spike, which is the owner's specific worry

**UNVERIFIED, and it must not be assumed either way.** BL-770's pilot could not run, so nobody has
tested whether a clip that goes quiet and then takes 100,000 views regains its expired fields.
**TikTok's own remedy wording is suggestive but not a guarantee**: it says that to retrieve the fields
*"you can view/like/comment/share the inactive video and retry after 24 ~ 48h"*, which implies renewed
activity does restore them.

**The refresh policy should be written to survive either answer:** keep a dormant clip on a **weekly
cheap check of view count only**, which costs nothing extra since view counts do not expire, and **if
views jump by a material margin, re-enter the daily capture cycle for another 7 days.** If
re-engagement does restore the fields, this catches the spike. If it does not, the platform still has
the early snapshot it took while the clip was fresh, which is the whole point of capturing early.

**The trap, restated because it is tempting:** TikTok's suggested remedy is to interact with the
inactive video. **The platform must never do that on clips it pays for.** Manufacturing engagement on
content being assessed for genuine engagement destroys the measurement and would be indefensible if it
were ever noticed.

### Storage growth, and whether to delete

Measured reference: `clip_stats` is **87 MB across 211,490 rows, about 434 bytes per row**. A snapshot
row here is richer, with several JSONB columns, so call it **2 KB**.

At **308 TikTok clips a month** and roughly **8 captures per clip**, that is about **2,500 rows and
5 MB a month, or 30,000 rows and 60 MB a year.** At full 42-clipper coverage it stays under 100 MB a
year.

**Nothing here should ever be deleted, and the reason is the point of the feature.** The whole design
exists because the vendor deletes at 30 days and TikTok expires at 7. **The platform's copy is the only
durable record**, and a fraud question about a payout can arrive months later. Storage is negligible
against that.

---

## PART 3 — THE IMPORT CAP, AND WHETHER THE ECONOMICS SURVIVE

BL-770 found bundle.social's Pro plan caps imports at **100 posts per month** against the platform's
**308 TikTok clips a month**, with ongoing refresh for imported posts requiring contact where
*"Additional platform usage fees may apply"*.

**What counts as an import, whether a refresh recounts, and whether analytics-only reads count at all
are UNVERIFIED.** No account exists and the vendor's documentation does not define it. **This is the
single most important commercial question and it cannot be answered by reading.**

**What can be said, conditionally, at each pilot size:**

| Connected clippers | Their TikTok clips/month (est. from concentration) | Under the 100 cap? |
|---|---|---|
| **5** | roughly 93 | **Yes, just inside** |
| **10** | roughly 143 | **No, 43% over** |
| 25 | roughly 205 | No, doubled |
| 50 | roughly 250 | No |

**So the flat $100 covers a five-clipper pilot and probably nothing beyond it.** At ten clippers,
which is the target, the cap is exceeded by roughly 43% and the real price becomes **unknown**, because
the overage is quoted as "contact us" rather than published.

**Stated plainly: the economics are unproven beyond five clippers, and the vendor has not published
the number that would settle it.** This does not make the design unworkable, but it does mean **no
plan should assume $100 a month covers ten clippers.** The pilot must establish the import definition
before anyone budgets.

**One mitigation worth testing:** if analytics reads on posts the platform never published through
bundle.social do **not** count as imports, the cap may be irrelevant entirely, since the platform's
clippers post natively. **That is the first question to ask, and it is free to ask.**

---

## PART 4 — WHAT THE REVIEWER SEES

BL-769 verified the line from TikTok's own terms: **per-clip, per-clipper, shown to a human is
defensible; aggregating creators into peer bands for ranking or discovery is prohibited verbatim.**
Nothing below aggregates creators.

### For a clip from a connected clipper

A single block beside the existing reviewer note, stating **numbers and nothing else**:

```
Creator analytics, captured 2 days after posting
  Views at capture      41,220
  Average watch time    8.4s of a 34s video
  Watched in full       11.2%
  Traffic sources       For You 78%, Following 9%, Search 6%, Profile 4%, Other 3%
  Top countries         DE 41%, AT 12%, CH 9%
  Compared with this clipper's own last 10 clips:
    average watch time  8.4s, versus their usual 7.9s
    For You share       78%, versus their usual 81%
```

**The comparison is against the clipper's own history, never against other clippers.** That is not a
stylistic choice; it is what keeps the feature inside TikTok's terms, and it happens to be the more
informative comparison anyway, since creators differ enormously.

**No score, no verdict, no colour-coded risk level, and nothing that sorts clippers against each
other.** BL-518 and BL-521 stand: the block **ranks nothing and decides nothing**. R-5 proved the
existing `fraudScore` had zero predictive power, and BL-664 measured human reviewers at a **0.77%
overturn rate**, so **the burden is on any new signal to beat a process that is already working.**

### For a clip from an unconnected clipper, which will be most clips for a long time

```
Creator analytics
  Not connected. This clipper has not linked their TikTok account, which is optional.
```

**That wording is deliberate and it is the most important copy in this report.** It must read as a
neutral fact, never as a gap, never as a flag, and never as a reason to look harder. **Most clips will
carry this line for the foreseeable future, and if it acquires any suspicious connotation the feature
has made review worse rather than better.**

**Explicitly forbidden in the UI:** any warning colour, any icon, any sort order, any filter labelled
"unverified", and any wording implying the clipper declined something. **Absence of analytics is
absence of data, not evidence.**

---

## PART 5 — WHAT THE CLIPPER EXPERIENCES

Copy is plain, non-accusatory, written for a fifteen-year-old, no dashes as bullets, no emoji. **Under
the recommended Option D nobody is ever blocked, so all of this is an invitation.**

**The invitation, shown on the earnings page to connected-eligible clippers only:**

> **Link your TikTok account**
> You can link your TikTok account to Clippers HQ. When you do, we can see the same analytics you see
> in your own TikTok app, like average watch time and where your views came from.
> It helps us check your clips faster, and it means fewer questions before a payout.
> Linking is optional and you can unlink at any time.
> [ Link TikTok ]  [ Not now ]

**At the permission screen**, one line of context before they leave the site:

> TikTok will ask you to allow Clippers HQ to read your account's analytics. We can read your view
> counts and audience information. We cannot post, delete, or message anyone from your account.

**If they decline:**

> No problem. Nothing changes, and you can link it later from this page whenever you want.

**If the owner overrules the recommendation and gates withdrawal**, the copy must still never imply
suspicion:

> **Before your next withdrawal**
> Withdrawals over $50 now need a linked TikTok account. This lets us confirm your clip results
> directly with TikTok instead of asking you for screenshots.
> Your balance is safe and it is not going anywhere.
> [ Link TikTok ]

**For someone whose account cannot be linked**, which is the path that must never fail:

> **Cannot link your account?**
> If your TikTok account was banned, deleted, or you have lost access to it, you do not need to link
> anything. Message us and we will remove the requirement for you. Your balance stays yours either
> way.

**The phrase "your balance is safe and it is not going anywhere" is load-bearing**, because the single
biggest risk of a gate is a clipper concluding their money has been taken. BL-762 documented exactly
that: a clipper saw $0.00 with no explanation and opened a support ticket.

---

## PART 6 — THE BUILD PLAN AND THE VERDICT

### Ordered plan

**Step 1, the owner, free and before any code.** Finish the BL-770 pilot: supply the API key, connect
one TikTok account he controls, and answer the four open questions, above all **whether analytics reads
count against the 100-post import cap**. **Nothing below is worth building until the fields are proven
to arrive.**

**Step 2, the store, owner-only.** The `ClipAnalyticsSnapshot` table and a capture job behind an
owner-only route or flag. Nothing clipper-facing. Nothing reads it except an owner view. **This is the
whole of the first build**, and it is useful on its own because it starts accumulating a record that
cannot be recovered later.

**Step 3, ask five people.** Personally, by name, with the copy in PART 5. **Five connections cover
71% of TikTok earnings.** No gate, no announcement, no policy change.

**Step 4, the reviewer block**, read-only, per-clip, own-history comparison only, after enough
snapshots exist to be worth showing.

**Step 5, and only if steps 1 to 4 prove out**, revisit whether any requirement is needed at all.
**The honest expectation is that it will not be.**

### Where it stops

* **Stop if the pilot returns nulls** for the six fields that matter.
* **Stop if the import cap makes ten clippers cost materially more than $100**, until the real number
  is known in writing.
* **Stop if fewer than three of the top five agree to connect.** If the highest-earning clippers will
  not link voluntarily, a gate would be forcing exactly the people most likely to leave.
* **Stop before building any score.** That is a separate decision with a 0.77% bar to clear.

### The verdict

> ## **Worth building as a store and a voluntary ask for about ten people, and NOT worth building as a withdrawal gate: the gate would strand $1,673.12 belonging to 94 clippers whose earnings have nothing to do with TikTok, while five voluntary connections already cover 71% of TikTok earnings.**

**The effort does not exceed the value, provided the scope stays where the measurement points.** The
store is small, additive, and useful the day it starts recording. The ask is a conversation with five
people. **What would exceed the value is the gate**: it is the most code, it creates the support
burden, it strands money, it needs an exemption path, and it buys reach the owner can get by asking.

**Said plainly, because the brief invited it: the feature is worth building and the requirement is
not.**

---

## WHAT COULD NOT BE ESTABLISHED

* **Whether the nine fields actually arrive**, at any clip age. BL-770's pilot never ran for want of an
  API key. **Everything in PARTs 2 and 4 is conditional on that.**
* **Whether a late viral spike restores fields expired past the 7-day window.** UNVERIFIED, and the
  refresh policy in PART 2 is deliberately written to work either way.
* **What counts as an import against the 100-post cap, and whether refreshes recount.** UNVERIFIED and
  commercially decisive.
* **Whether bundle.social's raw TikTok payload is enabled by default on the free tier**, since its own
  page says the payload is what you get *"when enabled for your organization"*.
* **The per-clipper clip counts behind PART 3's estimates** are derived from the concentration curve
  rather than counted per candidate, so they are approximate and labelled as estimates.
* **No vendor was called, no account created, no payment details entered, and no code written.**
