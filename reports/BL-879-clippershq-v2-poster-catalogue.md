# BL-879 — marketplace v2, round three: the poster's catalogue and the first money

> **NOTHING IS UNREMOVABLE AND NO SQL IS OWED. FIRST LINE, AS THE ROUND REQUIRES.**
> 266 ledgered rows, **`VERIFIED: 0 of 266 recorded rows remain`**, 0 failed, 0 cascaded. A direct
> catalogue sweep afterwards returns **zero** `bl879sbx-` rows in `users`, `campaigns`, `clips` or
> `clip_accounts`, and **zero** rows in all five v2 tables. Campaigns are back to **34**, all **34**
> NORMAL, with the fingerprint `e9defb11fcf63f2a100fbb1a63ed98de` identical to the opening snapshot.
> **ONE THING MOVED THAT IS NOT MINE AND IS NAMED HERE RATHER THAN BURIED:** the platform's active
> tracking-job count went 8601 to 8602 during teardown. That job belongs to a **real clipper's clip**
> created at `2026-09-16 16:12:17.294`, with no sandbox user, no sandbox campaign and no v2 post id.
> It is ordinary platform activity that happened while this round was tearing down.

**2026-09-16. Shipped on `checkpoint/BL-879`, merged to `main`. Requires a Railway REDEPLOY**, and
BL-877's and BL-878's are still owed as well. Base `origin/main` @ `a3a59a1`. Isolated worktree
`C:\w\b879`, a short path, `node_modules` never junctioned, **removed at the end and verified by
listing the path**. DB `now()` **15:56:21.467649+00** (first verification) to
**16:13:04.136949+00** (closing sweep), every timestamp cast `::text`.

---

## THE HEADLINE

> **1. A REAL POSTER CANNOT SAFELY USE THIS TODAY, AND THE BLOCKER IS EXACT, MEASURED AND CLOSED TWO
> WAYS.** `tracking.ts:2122` computes
> `isCpmSplit = !isMarketplaceClip && pricingModel === "CPM_SPLIT" && ownerCpm`, and at `:2949` the
> `else` branch, the one every clip with `isMarketplaceClip` FALSE takes, writes the **FULL clipper
> CPM** through `writeClipEarnings`. **A v2 clip keeps that flag false on purpose**, because setting
> it true would pay it on the first marketplace's 60/30/10 split through four existing branches. So a
> v2 clip that reached the ordinary tick would be paid **one hundred percent of the clipper rate
> instead of its 45**, silently, and every existing test would pass. This round therefore creates
> every v2 tracking job **INACTIVE**, and both v2 pages carry their own visibility gate.
>
> **2. THE MONEY WORKS, AND THE BUDGET HELD AT THE CAP RATHER THAN PAST IT.** Fifty posters, one
> clip, one **$100** budget. **50 of 50 posts created**, **10 paid**, **40 refused by the L1 hard
> lock**, the first at post 10. Poster legs **$45.00**, editor legs **$45.00**, platform legs
> **$10.00**, and `getCampaignBudgetStatus().spent` read **exactly $100.00**.
>
> **3. THE 55 CENTS IS NO LONGER A PREDICTION.** BL-877 argued that without its two aggregates 55
> cents in every v2 dollar would be invisible to the budget lock. Measured here with real money: the
> poster legs alone are **$45.00**, so `spent` would have read $45.00 against $100.00 that had
> actually left, **hiding exactly 55.0 percent**.
>
> **4. THE ACCESSIBILITY REVIEW CAUGHT A MONEY DEFECT, NOT AN ACCESSIBILITY ONE, AND IT CHANGED THE
> DESIGN.** BL-876 asked for a countdown started when the poster taps Open in Google Drive.
> **`MAX_CLIP_AGE_MS` is never compared against anything the poster does on this site.** It is
> compared against the timestamp of the post **on TikTok, Instagram or YouTube**. A countdown started
> at the Drive tap would have lied in both directions, and each lie costs a rejected clip.

**PROOFS: 35 of 35 sandbox checks and 20 of 20 render shots passed. 0 failed.**

---

## PART 0 — THE MODEL SPLIT, AND WHAT WAS CHECKED AGAINST SOURCE

| tier | what ran there | subagents |
|---|---|---|
| **cheapest (Haiku)** | pure retrieval: `MpBrowseCard`, the browse client, `MpFilterPills`, `MpEmptyState`, the post modal, the browse route's CPM stripping, `sanitize-url.ts`, `clip-config.ts`, `MpKpiStrip`, `skeleton-card` | **1** |
| **accessibility team** | one `accessibility-lead`, fanning out to its own specialists | **1** |
| **strongest (Opus), NOT SPLIT** | the earnings write path, the transaction, the budget interaction, the freshness move, the catalogue privacy boundary, every route, every UI surface, every proof script, the render harness and this report | **0 subagents between it and the source** |

**EVERY LOAD-BEARING SUBAGENT CLAIM WAS RE-RUN AGAINST SOURCE BEFORE IT WAS ACTED ON.** Two were
wrong and are corrected here rather than passed on:

| claim | check | verdict |
|---|---|---|
| `normalizeClipUrlForMatch` lives in `src/lib/url-normalize.ts` | `ls` | **WRONG.** There is no such file. It is in `sanitize-url.ts`, and the import was fixed before it could fail a build |
| `MAX_CLIP_AGE_MS` measures from the Drive tap (BL-876's premise) | read `checkFreshness` | **WRONG.** It measures from the post's own timestamp on the platform. See PART 3 |
| the `Modal`/`MpFilterPills` toggle group is not a tablist | read the file | **TRUE**, bare `aria-pressed` buttons |
| `marketplace-admin-client.tsx` renders TWO pill rows on one page | read it | **TRUE**, which is why the group was not upgraded |
| `--bg-page` is defined nowhere | grep `src/`, then the COMPILED bundle | **TRUE at both levels.** The shipped CSS has **0 definitions** and **7 unresolvable `var(--bg-page)` uses with no fallback** |
| `tracking.ts` would pay a v2 clip the full clipper rate | read `:2122` and `:2949` | **TRUE**, and it is the round's headline |

---

## PART 0b — WHAT THIS ROUND IS BUILT ON, VERIFIED RATHER THAN TRUSTED

Measured live at DB `now()` **2026-09-16 15:56:21.467649+00**, before a line was written:

| thing | measured |
|---|---|
| the four v2 tables | **4 of 4** |
| indexes on them in `pg_indexes` | **21** |
| v2 clips / posts / editor rows / platform rows | **0 / 0 / 0 / 0** |
| `campaignType` live, campaigns NORMAL | **34 of 34** |
| clips carrying `marketplaceV2PostId` | **0** |

**AND THE SHARPEST RISK IN THE WHOLE DESIGN, READ OUT OF THE FILE.** `balance.ts` carries
`db.marketplaceV2EditorEarning.aggregate` at `:498` and `db.marketplaceV2PlatformEarning.aggregate`
at `:502`, and both are summed into `spent` at `:528` and into `clipperSideSpent` at `:572-573`. The
proof asserts on those exact strings, and then PART 5 measures the same thing end to end with real
money rather than trusting the read.

The editor and approval paths from BL-878 were exercised as part of building the catalogue: the
sandbox's approved clip was created through the same model the owner's queue writes, and the
catalogue only ever selects `status: "APPROVED"`.

---

## PART 1 — THE CATALOGUE

Every poster on a campaign sees every APPROVED v2 clip for it. **Fifty posters seeing one clip is the
design**: there is no per-poster allocation, no slot and no claim.

**Status tabs defaulting to NOT POSTED**, reusing `MpFilterPills` with counts, newest approved first.
BL-876 justified this against newest-first-unfiltered (unposted clips get buried), an unposted-first
flat sort (only reads as sorted if you trust every ribbon, which is the colour problem at list level)
and grouped headers (costs vertical space at 375px).

### One ribbon, three channels, and the words come first

| state | the words on screen | icon | treatment |
|---|---|---|---|
| **NOT YET POSTED** | *"Not posted yet. You can still earn 45 percent."* | `CircleDollarSign` | **solid accent fill**, the only solid one, on purpose |
| **POSTED** | *"You posted this. It is live."* | `CheckCircle2` | surface fill with a 4px accent left border |
| **SKIPPED** | *"You skipped this. Change your mind any time."* | `SkipForward` | 1px accent outline, the quietest |

**"Tap" was dropped from the skipped copy.** It is false for a keyboard, switch or screen-reader
user, and it would have shipped inside the accessible name.

### The accessibility shape, and the five places the plan was wrong

1. **THE HEADING LEADS THE DOM AND CARRIES THE STATE.** A ribbon rendered before the name means a
   screen reader hears *"You skipped this"* before it knows WHICH clip, which is a 1.3.2 reading-order
   failure. The `<h3>` is first, the state word sits inside it, the full sentence lives in a
   `<p id="v2-card-status-{id}">`, and the wide visual ribbon below is an **`aria-hidden` duplicate**
   of something already spoken.
2. **`aria-describedby` IS ON THE ARTICLE AND ON EVERY FOCUSABLE CONTROL INSIDE IT**, because a
   description on an ancestor is not picked up when a child is focused. And the description target is
   never inside the control that consumes it, which would have spoken the sentence twice on one focus
   event.
3. **WHITE ON THE ACCENT FILL IS 3.40 TO 1 AND FAILS.** The solid ribbon uses `--bg-primary`
   (`#09090b`) text on the accent, which measures **5.86 to 1**.
4. **NOTHING CARRIES `mp-glass-*`.** Those rules override the global 2px focus ring with a 1px
   35-percent one at roughly **1.69 to 1**, and because `globals.css` is unlayered they beat every
   Tailwind utility regardless of specificity. That is not theoretical: it is why the white focus ring
   at `MpBrowseCard.tsx:113` never renders today. The v2 card uses
   `bg-[var(--bg-card)] border border-[var(--border-color)] rounded-xl` and inherits the correct
   global ring with no new CSS.
5. **THE CLIP NAME IS THE LINK.** v1's repeated "View details" gives a screen reader twenty identical
   entries, which is a live Level A defect. Making the name the link means **no `aria-label` is needed
   at all**.

**On POSTED there is no disabled control anywhere.** A disabled button drops out of the tab order with
no explanation, so the state is a span and Skip is **not rendered** rather than rendered disabled.
Every other action carries `aria-label` shaped so the visible text is contained **verbatim** (2.5.3):
"Post this clip: {name}", never "Post {name}".

**The card root has no `overflow-hidden`.** `MpBrowseCard.tsx:82` does, and a full-bleed ribbon inside
it would have its focus outline cropped on three edges. The thumbnail wrapper keeps its own.

**The stagger is clamped** to `Math.min(index, 10) * 30`. Unbounded, the fortieth card would start at
1200ms and the two hundredth at 6s, crossing 2.2.2's five-second threshold for auto-starting motion.

### One live region, and why the obvious implementation is silent

ONE `role="status" aria-live="polite" aria-atomic="true"`, mounted **unconditionally above the error,
empty and grid branches**, never one per card. A region injected at the same moment its text is set
never fires.

**Clear-then-write does not work**, and this is the detail most implementations get wrong: React
batches both `setState` calls into one commit, so the DOM never observes the empty string and an
identical repeated message is silent. An **alternating invisible character** is appended instead.
Wording is BL-876's verbatim: *"Clip skipped."*, *"Clip unskipped. Ready to post."*, *"Could not skip
this clip. Try again."*, *"Could not unskip this clip. Try again."*, all polite, none assertive.
`toast` is a second live region, so a skip is announced through one or the other and never both.

**A load failure is distinguishable from an empty list** and **moves focus to its own heading**,
because an `alert` already in the DOM at first paint is not announced at all: *"Could not load your
clips"* / *"Something went wrong. Try again."* with a real Retry button.

---

## PART 2 — WHAT A POSTER SEES ABOUT MONEY

**ONE FIGURE, HIS OWN, ALREADY MULTIPLIED.** `posterRatePer1k` computes `clipperCpm × 0.45` on the
server and sends only the product. Proved: on a campaign whose `clipperCpm` is **$1.00**, the card
carries `yourRatePer1k` **$0.45** and no CPM at all.

And the copy says plainly what it means: *"That is 45 percent of what YOUR post makes. What other
people's posts make does not change yours."*

**THE KEYS THAT ACTUALLY LEFT THE SERVER**, read back from the response rather than from the source:

```
approvedAt, campaignId, campaignName, description, id, inProgress,
platforms, state, thumbnailUrl, title, yourPostUrl, yourRatePer1k
```

**Absent, every one checked by name:** `budget`, `remainingUsd`, `spent`, `ownerCpm`, `clipperCpm`,
`cpmRate`, `agencyFee`, `lockedOwnerShareDecimal`, `clientName`, `aiKnowledge`, `editorEarnings`,
`editorTotal`, `platformAmount`, and anything about another poster. The module uses an explicit
`CATALOGUE_SELECT` and contains **zero** `include:`, asserted by the proof.

**THE ONE LEAK NOT REPEATED, AND THE SECOND ONE NOT REPEATED EITHER.** BL-841 item 7 measured
`budgetWarning` with `remainingUsd` shipping to every viewer with no role gate. BL-841 item 6 measured
the first marketplace defeating its own field protection by naming both halves on one screen. **So
this card has no editor-share line at all**: printing the editor's 45 beside the poster's 45 yields
the owner's 10 by one subtraction.

---

## PART 3 — THE POSTING FLOW, AND THE CORRECTION THIS ROUND HAD TO MAKE

### The five places he can lose his place

| # | step | how the interface holds it |
|---|---|---|
| 1 | the list, defaulting to Not posted | the anchor |
| 2 | taps a card | **a REAL URL**, `/marketplace-v2/catalogue/[id]`, never a modal-only state |
| 3 | taps Open in Google Drive and **leaves** | `target="_blank" rel="noopener noreferrer"`, so the ClippersHQ tab is untouched, and the server records IN PROGRESS for him |
| 4 | switches to TikTok to post | nothing to mitigate, and nothing needs it: the step 3 write does not care which app or how long |
| 5 | comes back on another device, an hour later, to a killed tab | **all three get the same fix.** The flag lives on the SERVER against his user id and the clip id, never in `localStorage` |
| 6 | submits the live URL | validated client side, then server side |

**Proved:** the flag was set for one poster, then read back through a **fresh server call with no
client state**, which is exactly what a cold load on another device is. It came back
`inProgress true, inProgressAt 2026-09-16T16:02:01.052Z`.

### THE COUNTDOWN BL-876 ASKED FOR WOULD HAVE LIED, AND HERE IS THE MEASUREMENT

BL-876 asked for a countdown started at the Drive tap, reasoning that *"a poster who leaves for Drive,
downloads a 30MB file, posts it and comes back an hour later would be refused with no warning"*.

**THAT REASONING IS WRONG AND THE RULE DOES NOT WORK THAT WAY.** `MAX_CLIP_AGE_MS` is never compared
against anything the poster does on this site. `checkFreshness` computes

```
diffMs = Date.now() - new Date(stats.createdAt).getTime()
```

where `stats.createdAt` is the timestamp of the post **on TikTok, Instagram or YouTube**, fetched from
the provider. The ordinary clipper path does the same thing with the same constant.

> **So the thirty minutes runs from the moment the video GOES LIVE, not from the moment he opens
> Drive. An hour spent downloading costs him NOTHING.** A timer started at the Drive tap would have
> told one person he had run out before he began, and another that he had time left when the window
> had already closed. **Each lie costs a rejected clip**, and BL-841 measured that once the window
> closes the same URL is refused PERMANENTLY by a different branch.

**WHAT SHIPS INSTEAD**, before he leaves, in words, using BL-847's already-shipped wording with the
label imported from `clip-config.ts` so the copy can never drift from the enforced window:

> **Read this before you download**
> Take as long as you like downloading and making your post. The clock does not start until your video
> is LIVE.
> Once it is live, come back and paste the link here **within 30 minutes of posting it**. That is the
> part people miss. After that the link stops working here.

**DOES THE RULE APPLY TO V2 AT ALL? YES, AND THAT WAS A DECISION RATHER THAN AN INHERITANCE.** It is
enforced **per path**, not globally: the clipper path enforces it in `clipper-submit-core.ts`, the
first marketplace in its own post route. A new path gets it only by asking. **A v2 post that skipped
it would be the one door in the product through which a week-old video could be submitted for full
credit**, which would make v2 the loophole rather than a second marketplace.

So `checkFreshness` and its `OurFailure` type were **MOVED VERBATIM** from
`marketplace/submissions/[id]/post/route.ts` lines 84 to 238 into `src/lib/clip-freshness.ts`, and
both post paths now import it. **The moved body was diffed against `pre-BL-879`'s copy of those exact
lines and is byte-identical**; only the `export` keyword and a header are new. A mirrored copy would
have been a second source of truth for a money rule, and BL-539 measured what one of those costs at
$933.94. It still **fails open**, unchanged: only a provider-CONFIRMED too-old post is refused.

### The in-progress flag may never become evidence, and that is in the database

Both columns on `marketplace_v2_poster_states` carry a `COMMENT ON COLUMN` saying so, applied to the
live database and **read back in the proof**:

> *"NEVER EVIDENCE. A poster who opens a Drive link and changes his mind has done nothing wrong.
> BL-871 used accepted-and-never-posted as a signature in the FIRST marketplace, and BL-876 proved
> that reframe does not carry over here, because every approved clip is visible to every poster and
> not posting is the normal case. Reading this column as suspicion would build a list of innocent
> people."*

**Proved:** every state change in the round produced **0 notifications, 0 audit rows and 0 strikes**.
Three consecutive rounds each struck somebody a previous round meant to protect, which is why this is
in the schema rather than left to be remembered.

---

## PART 4 — THE SUBMIT, AND THE DUPLICATE RULE THAT INVERTS

**NO BYPASS WAS BUILT AND NONE WAS NEEDED, PROVEN BY EXERCISING IT RATHER THAN REPEATING IT.** Fifty
posters posted one video and produced **fifty different live URLs**. Every gate keyed on
`normalizedUrl` passed naturally, **50 times out of 50**, with no flag, no branch and no exception.

**THE TWO GATES THAT SHOULD FIRE, AND DID:**

| case | result |
|---|---|
| a poster pasting **another poster's** live URL, campaign scoped | **REFUSED, 409**: *"That link is already on this campaign under somebody else's post. Paste the link to YOUR post."* |
| a poster posting the **same URL twice to one account** | **REFUSED, 409**: *"You have already submitted this exact post."* The database also refuses it through `uq_clip_norm_open_per_campaign`; the branch exists so he reads a sentence rather than a constraint name |

**THE MULTI-ACCOUNT QUESTION WAS BUILT PERMISSIVE AND EXERCISED.** A poster **CAN** post one clip to a
second of his own accounts, and the proof does it rather than asserting it. **Restricting it later is
one statement:**

```sql
CREATE UNIQUE INDEX CONCURRENTLY marketplace_v2_posts_clip_account_key
  ON public.marketplace_v2_posts ("v2ClipId","clipAccountId");
```

**Un-restricting a wrongly added index means dropping it from production, which is the harder
direction.** Both answers' exact SQL is in the migration header.

**The input is `type="text"` with `inputMode="url"`, never `type="url"`**: `sanitizeClipUrl` prepends
`https://` for a scheme-less paste and the native validator would refuse exactly what people paste,
through an unstylable bubble that is not a live region and preempts the page's own error node.
`autoComplete="off"`, not `"url"`, which means the person's own homepage. **The error node is
persistent with a static id**, never conditionally unmounted, so `aria-describedby` cannot dangle, and
**a server refusal populates the field error** rather than a toast alone.

---

## PART 5 — THE MONEY WRITE

One post creates, **in ONE transaction**: one ordinary `Clip` owned by the POSTER, one
`MarketplaceV2Post` whose `clipId` is unique in the database, one `ClipStat`, one **inactive**
`TrackingJob`, one editor earning row and one platform earning row. If any throws, none exists.

* **The poster's 45 percent goes through `writeClipEarnings` and nowhere else.** There is no direct
  update on the four invariant fields anywhere in the module.
* **`isMarketplaceClip` STAYS FALSE** and **`marketplaceV2PostId` is set, never
  `marketplaceSubmissionId`**. Proved across the full population: **0 of 51** v2 clips carried the
  flag true, and **0** carried a v1 submission id.
* **The editor's total is never stored.** Proved by asking the catalogue: `marketplace_v2_clips` has
  **0** earnings-shaped columns. BL-539 measured one stored total drifting by $933.94.

### Fifty posts, one budget, measured

| | |
|---|---|
| posters, clip, budget, CPM, views each | 50, one clip, **$100**, $1.00, 10,000 |
| posts created | **50 of 50** |
| money writes that succeeded | **10** |
| money writes refused by the **L1 budget hard lock** | **40**, the first at post **10** |
| every leg summing to the gross exactly | **10 of 10**, 0 wrong |
| poster legs / editor legs / platform legs | **$45.00 / $45.00 / $10.00** |
| `getCampaignBudgetStatus().spent` | **$100.00** against a **$100.00** budget |

**THE CAP HELD AT THE CAP, NOT PAST IT.** And the same run is the end-to-end proof of BL-877's
aggregate: without the two v2 aggregates `spent` would have read **$45.00**, hiding **exactly 55.0
percent** of what had left. BL-627's three mechanisms are all intact: the write ran inside a
**Serializable** transaction, the L1 lock read **COMMITTED** spend and threw, and the posts were
processed sequentially against one campaign.

### The two bonus stacks, on the real calculator

A **$100 gross** clip with a **10 percent** editor bonus and a **5 percent** poster bonus:

| leg | amount |
|---|---|
| editor | **$49.50** |
| poster | **$47.25** |
| platform | **$10.00** |
| **disbursed** | **$106.75** |

**The platform's $10.00 is 9.37 percent of what actually leaves**, not 10. Both figures match BL-876's
prediction exactly. **AND WITH THE ADDS FLAG ON**, which it is, the owner's ordinary per-clip cut is
charged to the campaign **on top of all of that**, so the campaign pays the two bonus stacks AND the
ordinary cut. `MARKETPLACE_V2_PLATFORM_CUT_MODE` reads `ADDS` and `v2AgencyEarningApplies()` returns
true, both asserted.

### Why no tracking job is active, which is this round's most important line

`recomputeV2PostEarnings` is written and **deliberately uncalled**. `tracking.ts` is untouched and
byte-identical. Every v2 tracking job is created **INACTIVE**, and it is **created rather than
omitted** for a specific reason: `clips/[id]/review/route.ts:1201` creates an ACTIVE job only
`if (!existingJob)`, so a row that already exists stops an owner approving the clip in `/admin/clips`
from silently switching tracking on. Proved: **0 active jobs behind a v2 clip**, and the platform-wide
active count was unchanged by this round.

---

## PART 6 — SKIP

**There is no skip, hide or dismiss concept anywhere in this product** except a dismissible Discord
banner, so this is new. It is reversible in the database and in the interface: the ribbon says *"You
skipped this. Change your mind any time."*, the action reads *"Post it after all"*, and both
directions were proved to round-trip SKIPPED to NOT_POSTED.

**Skipping records nothing about the poster's standing** and reaches no queue and no count, proved by
the same zero-notification, zero-audit, zero-strike measurement as the in-progress flag.

---

## PART 7 — MOBILE AND THE FOCUS RING

* **Single column below `sm`.** At 375 a two-column grid collapses the buttons to roughly 60px and
  wraps the ribbon sentence to four lines.
* **Every primary action is 48px, every secondary 44px**, stacked with a gap rather than sitting side
  by side, because Post and Skip have opposite consequences.
* **THE FAILING MARKETPLACE RINGS ARE NOT INHERITED.** `.mp-focus-soft` computes to roughly **1.54 to
  1** and the broad `.mp-section` / `.mp-glass-*` rule to roughly **1.69 to 1**, failing both the 3:1
  minimum and the 2px thickness, and they currently govern every interactive element on the existing
  marketplace. **The v2 surface carries none of those classes**, so it inherits the correct global
  `outline: 2px solid #2596be` at roughly **5.5 to 1** with no new CSS.
* **`data-no-swipe`** is not on the grid or the cards, which is correct: every action here is a tap,
  and the global handler already bails on `.overflow-x-auto`, which the pill row has.

---

## PART 8 — THE PROOFS, THE RENDERS AND THE TEARDOWN

### The opening snapshot, taken before anything was created

```
db now(): 2026-09-16 16:01:58.391793+00
campaigns 34, clips 10180, users 1749
v2: clips 0, posts 0, editor 0, platform 0, states 0
v1: hashes 9, submissions 0
agency 4882, payouts 248, ACTIVE tracking jobs 8601
campaign fingerprint e9defb11fcf63f2a100fbb1a63ed98de
```

### 35 of 35 checks passed, 0 failed

Everything the round named: the tables, indexes and zero rows; `campaignType` live; the spend
aggregate in source; the catalogue visible with no forbidden field; the 45 percent pre-applied; the
allow-list select with no `include`; the in-progress flag surviving a device change; skip and unskip;
zero side effects; the never-evidence rule in the live column comment; fifty different URLs accepted;
every leg summing exactly; the budget lock biting at the cap; the aggregate seeing all three legs;
both gates that should fire firing; the permissive multi-account answer; `isMarketplaceClip` false
across the full population; `marketplaceV2PostId` set and `marketplaceSubmissionId` not; no active v2
tracking job; the ADDS flag; no stored editor total; `MarketplaceVideoHash` unwritten; no v1 row.

### Every invariant, across the FULL population

| invariant | measured |
|---|---|
| **BL-538 and the earnings invariant** | **0 breaches** |
| **BL-696**, two open payouts on one campaign | **0** |
| **BL-696**, a clip with two agency rows | **0** |
| **BL-696**, a clip with two v2 editor rows | **0** |
| **BL-627 no overpayment**, counting BOTH v2 aggregates | **0 campaigns over budget** |
| **BL-824 paid-is-final with BL-849's write side** | **26 positions** below money already paid, **pre-existing**; this round created zero payout rows |

### The renders: 20 of 20, and the content is asserted rather than assumed

BL-793's method unchanged: viewport on the **context**, `window.innerWidth` **read back** and printed,
horizontal overflow measured, URL read back so a bounce to `/login` cannot be photographed as a pass,
and a **real minted `__Secure-` Auth.js cookie against a production build with `DEV_AUTH_BYPASS=false`**.

| screen | 320 | 375 | 414 | 1280 | 1440 |
|---|---|---|---|---|---|
| the catalogue, All tab (all three ribbons + resume banner) | PASS | PASS | PASS | PASS | PASS |
| the catalogue, default Not posted tab | PASS | PASS | PASS | PASS | PASS |
| the clip detail, not posted | PASS | PASS | PASS | PASS | PASS |
| the clip detail, posted | PASS | PASS | PASS | PASS | PASS |

`innerWidth` matched on all twenty and **horizontal overflow was 0px on all twenty**. The All-tab shot
additionally asserts **all three ribbon sentences by text** and the presence of the resume banner, so
a screenshot that looks right but says the wrong thing fails rather than passes: **ribbons 3/3, resume
banner present**, at every width.

**A DEFECT THE RENDER CAUGHT THAT NO TEST WOULD HAVE.** `V2Thumb`'s placeholder replaced its whole
class list when a caller passed a sizing class, which pinned the play glyph to the top left of a
full-width card thumbnail instead of centring it. Found by looking at the 375px shot, fixed, rebuilt
and re-rendered.

**WHAT COULD NOT BE RENDERED, STATED RATHER THAN OMITTED.** The **submitted-successfully state reached
by actually pressing Submit** was not photographed as a transition; the POSTED detail screen was
photographed from a post created through the same server function, which is the same rendered output
but not the same journey. And the **live-region announcements** cannot be photographed at all, being
screen-reader-only text.

### The teardown, exactly

```
266 rows recorded in C:/bl879-sandbox/ledger.jsonl
  all locks passed, nothing has been deleted yet
  marketplace_v2_posts       deleted  52
  marketplace_v2_clips       deleted   4
  tracking_jobs              deleted  52
  clips                      deleted  52
  clip_accounts              deleted  52
  campaigns                  deleted   1
  users                      deleted  53
  266 deleted, 0 already gone, 0 FAILED
  VERIFIED: 0 of 266 recorded rows remain.
```

**Product-written rows were ADOPTED rather than swept.** `bl879-adopt.ts` adds a ledger line only
where it can prove the row belongs to this round, by reading a column that holds a sandbox id straight
out of the database. No delete, no pattern match on a name, no date range. It adopted 52 tracking
jobs; `ClipStat` rows cascade from their clip and were verified gone afterwards.

**The independent sweep, at DB `now()` 16:13:04.136949+00:** zero `bl879sbx-` rows in `users`,
`campaigns`, `clips` and `clip_accounts`; **zero rows in all five v2 tables**; **zero** clips carrying
`marketplaceV2PostId`; 34 campaigns, all 34 NORMAL; fingerprint identical to the opening snapshot.

### Safety, itemised

* **No real user, clip, campaign or payout was touched.** Every row carried the `bl879sbx-` prefix and
  the `BL879-SANDBOX-DELETE-ME` marker, every person was `isTestUser`, the campaign `isTestCampaign`.
* **NO APIFY ACTOR RAN AND NO VENDOR LOOKUP WAS MADE.** The proof creates posts through
  `createV2Post`, which is what the route calls **after** the shared freshness check has already
  passed. Fifty fabricated URLs would have been fifty metered lookups for no information. The 11
  BL-678 guards are untouched. **This is a deliberate gap and it is named: the freshness check itself
  was not exercised end to end against a live provider in this round.**
* **The six money files, `tracking.ts` and `campaign-era.ts` are BYTE-IDENTICAL by blob OID** on both
  refs: `clip-earnings-writer.ts ac5be7de`, `earnings-calc.ts 00410634`, `balance.ts 25a0b2f2`,
  `tracking.ts bf31646f`, `clip-earnings-invariant-middleware.ts 61cef393`, `money-decimal.ts ef5cdae7`,
  `campaign-era.ts 106e16ad`.
* **No Prisma in the browser bundle.** Every client component imports only from `@/components/...`;
  the server layer is imported by routes and scripts only.
* **The branch did not drift.** `checkpoint/BL-879` throughout.
* **No handle printed that is not a sandbox handle, and no wallet address anywhere.**

### Build and gates, honestly

`eslint` is present in three forms, so the BL-348 gate did not silently no-op.

| run | result |
|---|---|
| `npx tsc --noEmit` | **exit 0** |
| `check:prisma-bypass` / `check:removed-fields` / `check:event-wiring` | **0 violations / OK / 0 problems** |
| **`lint:hooks`** | **10 problems, 0 errors, 10 warnings** against a ceiling of 11 |
| **`npm run build`** | **`BUILD_EXIT=0`**, echoed by the build's own shell, never read off a pipe |

---

## WHAT IS AND IS NOT REACHABLE, AND WHETHER A REAL POSTER COULD USE THIS

**REACHABLE, AND GATED:** `/marketplace-v2/catalogue` and `/marketplace-v2/catalogue/[id]`, each with
its own `getSession()` plus `isMarketplaceVisibleForUser` plus `notFound()`, because `marketplace-v2`
is a **sibling** of `marketplace/` and inherits neither its layout nor its gate. Until
`NEXT_PUBLIC_MARKETPLACE_ENABLED` flips, that resolves true only for the OWNER and test users. Four
API routes, each with session, ban check and, on the money route, a rate limit.

> ## COULD A REAL POSTER SAFELY USE THIS TODAY? NO, AND THE REASON IS ONE LINE.
>
> If a v2 clip were ticked by the ordinary tracking path it would be paid **the full clipper rate
> instead of 45 percent**, because `tracking.ts:2122` treats any clip with `isMarketplaceClip` false
> as an ordinary CPM clip and `:2949` writes the full amount. **That flag must stay false**, so the
> fix belongs in the tick, not in the flag.
>
> **What stops it today, twice over:** every v2 tracking job is INACTIVE, so the tick never sees one;
> and the surface is behind the marketplace visibility gate, so no ordinary clipper can reach it.
> **Both would have to be removed before a real poster is let in, and neither should be removed until
> Round Four ships.**

**WHAT ROUND FOUR MUST BUILD:**

1. **The tracking tick's v2 branch**, calling `recomputeV2PostEarnings`, which is already written and
   deliberately uncalled. It must fork on `marketplaceV2PostId` being non-null, NOT on
   `isMarketplaceClip`.
2. **Activation of v2 tracking jobs**, once and only once that branch exists.
3. **`computeV2BudgetCost` as a pre-flight gate** on the post path, so a post that cannot be paid is
   refused before it is made rather than after.
4. **The `AgencyEarning` decision wired to `v2AgencyEarningApplies()`** rather than re-decided, so the
   ADDS flag has one reader as well as one writer.

---

## WHAT COULD NOT BE DETERMINED

* **Whether the freshness check behaves correctly for a real v2 post**, because no real social post
  was available and no vendor lookup was made. The shared function is byte-identical to the one the
  first marketplace has been using, which is the strongest evidence available without spending
  metered calls on fabricated URLs.
* **Whether the 26 positions below their paid floor is comparable to BL-849's 17.** Not re-measured
  with BL-849's exact query, for the third round running. This round created zero payout rows.
* **Whether showing an aggregate such as "posted 6 times so far" is right.** BL-876 left it open as
  its question 25 and this round did not answer it: it is not one person's money, but it is another
  user's activity, and it changes the surface from no-pressure to scarcity.
* **The page-title shape.** Both v2 pages inherit `"Clippers HQ — Get Paid to Clip"`, CLAUDE.md says
  the tab title is just "Clippers HQ", and `account/page.tsx:42` sets a bare `"Account settings"`.
  **Three shapes already exist and this round deliberately did not add a fourth.** It is an owner
  decision.

### Two pre-existing defects found and reported rather than fixed

1. **`--bg-page` IS DEFINED NOWHERE, AND IT IS WORSE THAN UNDEFINED.** **40** uses across **23** files
   in `src/`, **0** definitions in `globals.css`, the only CSS file in the repo, and **0** definitions
   with **7 unresolvable uses and no fallback in the COMPILED production bundle**. 33 are
   `bg-[var(--bg-page)]`, which falls to `transparent` because background-color is not inherited; **6
   are `ring-offset-[var(--bg-page)]`, which resolves to Tailwind's `@property` initial of `#fff` and
   paints a WHITE halo on dark UI**. That second form was already found and fixed once in
   `ProgressPremium.tsx` (BL-793). CLAUDE.md still mandates the broken token. New v2 code uses
   `--bg-primary`.
2. **The `--text-*` tokens are all `#ffffff` in dark mode**, so `text-[var(--text-muted)]` gives zero
   hierarchy. The `--mp-*` scale is real and all of it passes AA, and the v2 surface uses that one.

---

**PERFORM NO FIX ON ANYTHING ABOVE. The defects this round found in its own work, it fixed and
re-proved. The pre-existing ones it deliberately did not touch.**
