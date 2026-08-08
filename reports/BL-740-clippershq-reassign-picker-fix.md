# BL-740 — the reassignment picker offered zero destinations, on every clip
**Branch** `checkpoint/BL-740` · **Base** `origin/main` `6d906941` · 2026-08-08
**ONE LINE: one wrong condition refused 92 of 93 destinations, and it was never protecting anything.** Worked in a
clean worktree at `C:/b740` because `C:/b575` is stale (`91b84410`) and dirty (77 paths); b575 left exactly as found,
real `npm ci`, never a `node_modules` junction.
## PART 0 — Which block was firing, measured before anything changed
The real exported `evaluateDestination` was run with the real lookups over three real PENDING clips against every
campaign. **Result: 0 of 31 offered, for all three clips.** Block frequency across all 93 clip-campaign pairs:
```
CLIPPER_NOT_ON_DEST            92     <-- fires on essentially every pair
DEST_ARCHIVED                  54
DEST_PLATFORM_NOT_ACCEPTED     38
DEST_PAST                      24
DEST_PAUSED                    15
DEST_OVER_BUDGET                6
DEST_NOT_ACCEPTING              6
```
**THE CULPRIT: `src/lib/campaign-reassign.ts:234-240`**, the condition
`if (!(await lookups.accountOnCampaign(clip.clipAccountId, d.id)))`, backed by a lookup that asked whether a
`CampaignAccount` row **already existed** linking this clip's account to that destination.
**Why it fired universally:** measured on the same clips, each clipper's account was joined to **1 or 2 campaigns out
of 32**. So roughly thirty destinations per clip were refused for a row that simply had not been created yet. It is
the only block that fires on nearly every pair; every other block fires selectively and correctly.
**The other candidates the brief asked me to test explicitly, each cleared:**
| Candidate | Verdict |
|---|---|
| Era boundary applied to non-era campaigns | **Clear.** Fires **0** times. Only 2 campaigns carry a boundary |
| Daily limit counting the clipper at cap everywhere | **Clear.** Fires **0** times |
| Campaign status case or spelling mismatch | **Clear.** Prod stores exactly `ACTIVE` x17, `PAST` x8, `PAUSED` x5, `DRAFT` x2, and the code compares those literals |
| Pool headroom reading null or wrong | **Clear.** Fires 6 times, on genuinely spent campaigns |
| Null accepted-platforms treated as accepting nothing | **Clear.** The check is `if (platform && d.platform)`, so a null `platform` column skips the block entirely. No campaign has a null `platform` anyway |
| Platform comparison case-sensitive (the BL-601 trap) | **Clear.** Already `.toLowerCase()` on both sides, which matters because prod really does store `TIKTOK` x15, `TikTok` x4, and accounts carry `TikTok`, `TIKTOK` and `tiktok` |
**Only one block was firing universally.** No second cause.
## PART 1 — Fixing the condition, not removing the protection
**It was never protecting anything.** Joining a campaign is **self-serve**: the only gate in
`api/campaign-accounts/route.ts:69-76` is that the clip account belongs to the user and is `APPROVED`. There is no
owner approval and no campaign-side eligibility. The clipper could create that row themselves with one click, so
refusing the owner's correction for its absence was not a safety property, it was **a missing write**.
So the condition becomes the one that actually admits an account anywhere, and the row is created rather than demanded:
**The block stays, with the right condition.** `CLIPPER_NOT_ON_DEST` becomes `CLIPPER_ACCOUNT_NOT_APPROVED`: the
account itself must be `APPROVED`. That is a real refusal and it still refuses.
**The membership is established inside the same transaction**, an idempotent `campaignAccount.upsert` next to the
`TrackingJob` repoint, so it rolls back with everything else and leaves the destination in exactly the state it would
have been in had the clipper submitted there originally. Without it the clip would sit on a campaign its own account
was not a member of, a state no ordinary submission can produce.
**Nothing was deleted or downgraded.** All seven blocks remain hard refusals: the count of `blocks.push` sites is
unchanged and `allowed` is still `blocks.length === 0`.
**After the fix, offered goes 0 → 3, 2, 2** for the same three clips. What is now offered and what is still refused,
for the first clip (TikTok, on BAD BITCH ANTHEM 2.50):
```
OFFERED  BAD BITCH ANTHEM (0.50 CPM)   ACTIVE
OFFERED  Zhus Edit (0.50 CPM)          ACTIVE
OFFERED  Zhus Meme (0.20 CPM)          ACTIVE
BLOCKED  bees.n.honey  Gainzalgo  Grateful Songs  Hapday  somesome  STRAENGE  Zhus   DEST_PAST
BLOCKED  SomeSome                                                                   DEST_PAUSED
BLOCKED  Panic Baby                                                    DEST_PAUSED + DEST_OVER_BUDGET
```
**The protections BL-730 measured still refuse:** era-freezing, PAST, paused, spent, and platform-incompatible
destinations are all still blocked, which matters because BL-730 proved 5 of 8 pending clips would be permanently
frozen by an era move and 8 of 14 campaigns are PAST.
## PART 2 — Making the refusal legible
**Archived campaigns are no longer listed.** Measured: **18 of 31** campaigns in the picker were archived, so more
than half the list was unchoosable noise burying the handful that were real. Every other list in the app already
filters `isArchived: false` (BL-732 catalogued them), so this follows the house convention. **It is a list filter, not
a relaxation:** `DEST_ARCHIVED` remains a hard block, so a POST naming an archived campaign is still refused.
**The empty-state message no longer dead-ends, and it is now ANNOUNCED.** It said only "No campaign can take this
clip right now", which is exactly what the owner saw on every clip while one wrong block refused everything. It now
reads "No campaign can take this clip right now. Every campaign that was refused is listed below with its reason.
Archived campaigns are not shown." That sentence is derived once and consumed by **both** the visible paragraph and
the existing `role="status"` region, so a screen reader user is told rather than left to hunt for it. Three guards are
load-bearing: `!loading` and `data` (without them `selectable.length === 0` is trivially true during the entire load
and would announce a FALSE dead end on every open) and `!clipBlocked` (that branch never renders the list the sentence
points at).
**Blocked campaigns remain listed with reasons and keyboard-reachable**, unchanged from BL-736's post-review state:
they are a plain `<ul>`, **not** natively disabled radios (native `disabled` removes an option from arrow-key roving,
which is BL-556's documented house rule and the defect BL-736's review caught).
## PART 3 — Proof on real data
The three sampled clips, every campaign, offered or blocked with the reason, are in PART 0 and PART 1 above and in the
committed diagnostic. The restamp trace, computed by the same resolvers the POST uses:
```
CLIP mq8oew  TikTok, on "BAD BITCH ANTHEM (2.50 CPM)"  effective rate now 2.5
  OFFERED  Zhus Edit (0.50 CPM)   would restamp clipper 2.5 -> 0.5, owner 1.636 -> 0.3197  [PAY CUT: clipper warned]
CLIP 11n45s  Instagram, on "Zhus Meme (0.20 CPM)"  effective rate now 0.2
  OFFERED  BAD BITCH ANTHEM (0.50 CPM)  would restamp clipper 0.2 -> 0.2, owner 0.1279 -> 0.13
  OFFERED  Zhus Edit (0.50 CPM)         would restamp clipper 0.2 -> 0.5, owner 0.1279 -> 0.3197
```
Note the second clip: a campaign named "0.50 CPM" restamps an **Instagram** clip to **0.20**, because the rate is
per-platform. The trace reads the real per-platform columns rather than the campaign's name.
**NO REAL CLIP WAS MOVED, and the reason is not caution for its own sake.** Every pending clip in production belongs
to a **real CLIPPER**, not the owner and not a test account. A reassignment sends that person a notification, and a
rate drop leads it with "this clip will earn less than the campaign it was submitted to". Moving a clip and moving it
back leaves **two** such messages in a real clipper's inbox about a move that never needed to happen. **A notification
cannot be un-sent**, so the round trip is not reversible in the sense the brief requires, and the brief's own
alternative was taken: proof by trace, moving nothing. `CLIP_CAMPAIGN_REASSIGNED` audit rows: **0**. Reassignment
notifications: **0**.
## PART 4 — Why 69 of 69 passed while production offered nothing
**The harness only ever proved refusals.** Every block was tested in isolation, each with synthetic lookups where the
other five conditions were forced to pass, proving each block **can** refuse. Not one check asked the only question
the owner cares about: with all six real lookups running against real rows, **does anything get through?** A suite
built entirely from refusal tests is perfectly satisfied by a feature that refuses everything, which is precisely what
shipped. The live half compounded it by measuring only the era block, the one that fires rarely.
**The check added:** `LIVE POSITIVE CASE: the picker actually offers something`. It runs the real evaluator with all
six real lookups over up to 10 real pending clips against every real campaign and fails unless **at least one clip has
at least one destination**. It now reports **10 of 10 sampled clips have at least one real destination, 30 pairs
offered**. Run against the pre-fix code it would have failed, and that is not a guess: the pre-fix diagnostic recorded
`OFFERED: 0 of 31` for all three clips using the same evaluator and the same live lookups.
Harness **70 passed, 0 failed**.
## What did not change
**Money files byte-identical by blob OID on both refs:** `clip-earnings-writer` `ac5be7de`, `earnings-calc` `797e2098`,
`balance` `e887f80a`, `tracking` `83ce4bab`, `clip-earnings-invariant-middleware` `61cef393`, `money-decimal`
`ef5cdae7`, `campaign-era` `106e16ad`. The CPM restamp stays inside the atomic transaction and the null-CPM pay-cut
warning still fires (both re-verified). **0** reassignments, **0** notifications, **0** invariant violations, 161
payout rows unchanged, 587 campaign_account rows unchanged. No wallet address printed; handles redacted.
## Accessibility — the review returned FAIL, and one defect was mine from this round
It returned **FAIL on four blocking defects**, all fixed. It also confirmed **all three BL-736 fixes are intact and
un-regressed**: the shared trap's radio roving tab stops, blocked campaigns as a plain list rather than dead controls,
and the selection indicator not being colour alone.
**D1 was a functional regression I introduced in this very round, and it is the serious one.** Filtering archived
campaigns out of the list was correct, but `current` (the clip's OWN campaign) was still being resolved out of that
same filtered array. **A clip sitting on an archived campaign therefore resolved its source campaign to `null`.**
Measured: **2 pending clips are on archived campaigns right now**, so this was reachable, not theoretical. Two failure
modes: the dialog reads "Currently on: **Unknown**" for a move that changes a clipper's pay, and for a clip with no
frozen stamp `getEffectiveCpmForClip` falls through to `getCampaignCpmForPlatform(null, ...)`, which **dereferences its
argument with no null guard** (`cpm.ts:52-60`), throwing and **500ing the whole picker**. I would have shipped a fix
that broke the picker for a different set of clips. The source is now its own `findUnique`, which also realigns GET
with POST (POST always re-read it separately). **The `as any` I had put on that call is what let it compile**, and it
is gone.
**D2:** the dialog's `aria-describedby` description promised unconditionally that refused campaigns are "listed
underneath", which became false for archived ones and was always false when the blocked list was empty. Now
conditional. **D3:** "All N are listed below" asserted a completeness the list does not have, since archived, test and
same-campaign refusals are all excluded; a sighted owner can sample the list to sanity-check, a screen reader user
counts to N and concludes they have the whole picture. The quantifier and the number are gone and the exclusion is
disclosed. **D4:** the dead end existed only in non-live DOM, so the user heard "Loading campaigns." then permanent
silence, ambiguous between still-loading, failed and succeeded-with-nothing; in forms mode the tab ring is Cancel
alone, so it was unreachable without a deliberate mode switch. Now announced through the existing region.
**On hiding archived campaigns, it agreed with the call and sharpened the reasoning:** all 18 carry the *identical*
reason string, so a sighted owner skims them in a second while a screen reader user hears one fact repeated 18 times,
burying the ~10 entries whose reasons genuinely differ and are actionable. Removing them helps the screen reader user
**more**. But silence about a whole category is what BL-730 objects to, so the exclusion is now stated in one sentence
rather than 18 rows, and the route returns `archivedHiddenCount` so the client can say it honestly.
**Reported, not fixed, deliberately:** a WCAG 2.1.2 keyboard trap while `saving` (Cancel, Move and the radios are all
disabled at once, so the trap parks focus on the panel and Escape returns early; there is no `AbortController`). It is
**pre-existing from BL-736**, it is Level A, and the fix is a behavioural change to a money-writing submit path that
deserves its own round rather than being bolted onto a picker fix. Also reported: `getCampaignCpmForPlatform` should
reject null defensively rather than relying on callers, which is money-adjacent shared code and not this round's
business.
## Gates, stated honestly
`npm ci` exit 0, 822 packages, no junction. `npx prisma generate` exit 0, **before** tsc. `tsc --noEmit` **0 errors**.
`npm run build` **exit 0**, "Compiled successfully in 44s", read from a log with the exit code **echoed, never piped**.
BL-348 hooks gate **0 errors, 11 warnings — at the limit of 11**, eslint **v9.39.4 confirmed present**.
