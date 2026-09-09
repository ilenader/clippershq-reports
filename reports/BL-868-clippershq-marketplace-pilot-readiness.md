# BL-868 — the duplicate check was hashing the link, not the video, and it failed in both directions

**TEARDOWN FIRST, AS THE ROUND REQUIRES: NOTHING IS UNREMOVABLE. 32 ledgered rows,
27 deleted and 5 already gone, `VERIFIED: 0 of 32 recorded rows remain`. A direct
catalogue sweep confirms **zero** `bl868sbx-` rows survive in `users`, `campaigns`,
`clip_accounts`, `marketplace_poster_listings`, `marketplace_submissions` or
`marketplace_video_hashes`, and `marketplace_video_hashes` reconciles exactly to
its opening count of 9. No SQL is owed.**

**2026-09-09. Shipped on `checkpoint/BL-868`. One source file changed. Requires a Railway REDEPLOY.**

---

## THE HEADLINE: THE SAME VIDEO COULD BE SUBMITTED TWICE, AND TWO DIFFERENT VIDEOS COLLIDED

The owner named duplicate detection specifically, and he was right to. `computeVideoUrlHash`
(`src/lib/video-hash.ts`) hashes the **URL string**, normalised to `hostname + pathname` with the
query string thrown away. Google Drive puts the file's identity **in the query string** in three of
its four link forms. Measured with the product's own function before anything was changed:

| | link | hash |
|---|---|---|
| A | `/file/d/<FILE_1>/view?usp=sharing` | `2d5bb8ca7d22b7ab` |
| B | `/file/d/<FILE_1>/view?usp=drivesdk` | `2d5bb8ca7d22b7ab` |
| C | `/open?id=<FILE_1>` | **`2b48fbc490931cad`** |
| D | `/open?id=<FILE_2>` | **`2b48fbc490931cad`** |
| E | `/uc?id=<FILE_1>` | `3de8b9be295eda7a` |

**Two failures, in opposite directions, and both are live money:**

1. **A, C and E are the SAME FILE and hash three different ways.** The blocking duplicate check at
   `submissions/route.ts:487` keys on this value, so the same video submitted a second time under a
   different Drive link form **was accepted**. That is the same work paid twice.
2. **C and D are COMPLETELY DIFFERENT FILES and hash identically.** `drive.google.com/open` is the
   entire normalised string for every `open?id=` link ever submitted, so every one of them collided
   with every other. An honest second submission was **refused as a duplicate**. The same is true of
   `/uc`. This is the worse of the two, because it blocks real work and looks like a false accusation.

### The fix, and what it still cannot do

`normalizeForHashing` now extracts the Drive file id when the host publishes one and hashes
`gdrive:<id>`, leaving every other URL normalised exactly as before. Deliberately a short explicit
host list rather than "keep the query string", because keeping the query would make `?usp=sharing`
and `?usp=drivesdk` stop matching and reintroduce failure 1 in a new form.

**It still cannot catch a re-upload.** The same video uploaded to Drive again gets a new file id and
therefore a new hash. Only perceptual hashing (download, fingerprint the frames) could catch that; it
is the "Fix B" the file has always deferred and it is not something to build in the same round as
everything else. **That gap is now the only remaining duplicate-payment route, and the owner should
know it is open.**

### The guard, demonstrated failing and then passing

`scripts/sandbox/bl868-hash-probe.ts` is the guard, and it is the round's own proof rather than an
assertion. **Before the fix: 2 of 5 hold. After: 5 of 5.** The three that flipped are exactly the
three failures above.

### And end to end, against the real route

`scripts/sandbox/bl868-walk.ts` drives the real `/api/marketplace/submissions` over HTTP against a
**production build with `DEV_AUTH_BYPASS=false`** and real minted Auth.js cookies, so the session,
ban merge, Discord gate, visibility flag, slot arithmetic and Serializable transaction all run.
**7 of 7 passed:**

- the same link twice: **409**, "You already have a pending submission with this Drive link."
- **the same FILE under `open?id=`: 409**, "You already submitted this video content to a listing on
  this campaign." **This returned 201 before the fix.**
- the same file under `drivesdk`: **409**
- **a DIFFERENT file under `open?id=`: 201.** This was refused before the fix.
- a full listing: **409**, "This listing has reached its daily submission limit. It resets at midnight
  UTC.", with `used: 5, total: 5`
- a second listing has its own slot budget: **201**

### What the duplicate check still does NOT do, reported not changed

**Cross-user reuse is not blocked.** A second clipper submitting the identical Drive link was
**accepted (201)**. The check is scoped per creator per campaign by design
(`submissions/route.ts:489-498`), and a cross-user collision produces only a
`console.warn("[F-VIDEOHASH-LITE] collision detected: ...")` at `submissions/route.ts:844`. Nobody
reads Railway logs. The owner is told only through `MARKETPLACE_VIDEOHASH_AUTOFLAGGED`, which fires
from the **reject** route at `submissions/[id]/reject/route.ts:205` and only once the same hash has
been **rejected five times**. **Two approvals of the same video are completely silent.** That is a
policy decision about who may reuse whose source video, not a defect, so it is reported rather than
changed.

---

## PART 3 — THE MONEY, COMPUTED BY HAND FIRST

`scripts/sandbox/bl868-money.ts` prints the hand table, then runs the product's functions, then
compares. **No expected value is derived from the thing under test. 64 assertions, 0 failed.**

### The 60/30/10 split, and the parts equal the gross exactly

| case | gross | creator | poster | platform | sum == gross |
|---|---|---|---|---|---|
| plain | $100.00 | $60.00 | $30.00 | $10.00 | yes |
| BL-866 devalued to half CPM | $50.00 | $30.00 | $15.00 | $5.00 | yes |
| capped at $50 | $50.00 | $30.00 | $15.00 | $5.00 | yes |
| sub-cent boundary | $0.55 | $0.33 | $0.17 | **$0.05** | yes |
| odd gross | $33.33 | $20.00 | $10.00 | $3.33 | yes |

The platform leg is computed as the **remainder** (`earnings-calc.ts:663`), not as `gross × 0.1`,
which is why the sub-cent case still sums exactly: the platform absorbs the rounding rather than the
clippers losing a cent.

### The cash, every combination

`finalAmount = amount − fee − express − trainerCut` (`payout-calc.ts:129`). The trainer's basis
excludes express and is $91.00 on a $100 gross whether or not the clipper was referred, so the cut is
$9.10 wherever it applies.

| case | fee | express | trainer | cash |
|---|---|---|---|---|
| plain, unreferred | $9.00 | | | **$91.00** |
| referred | $4.00 | | | **$96.00** |
| trainer | $9.00 | | $9.10 | **$81.90** |
| express | $9.00 | $4.00 | | **$87.00** |
| express + trainer | $9.00 | $4.00 | $9.10 | **$77.90** |
| referred + trainer | $4.00 | | $9.10 | **$86.90** |
| referred + express + trainer | $4.00 | $4.00 | $9.10 | **$82.90** |

Every row also asserts that **the deductions plus the cash equal the gross exactly**.

**THE REFERRED CASH BEING HIGHER IS CORRECT AND IS WORTH SAYING OUT LOUD**, because it looks like a
bug. A referred clipper pays a 4 point platform fee instead of 9, and the referrer's 5 points come
out of the platform's own share rather than the clipper's pocket. CLAUDE.md states it as "Platform fee
9% (4% referred)".

**BL-863 re-checked and still true:** express is 4% of the GROSS, so a $100 express request sends
exactly **$87.00**, not the $87.36 that 4% of the post-fee $91.00 would give.

**The guards hold:** an absurd trainer cut of $9,999 on a $10 request is clamped to the room after
fees and the cash floors at $0.00 rather than going negative; a negative cut cannot add money.

### The marketplace 10 percent still REPLACES the owner's cut

**Verified in code, not inherited.** `isCpmSplit = !isMarketplaceClip && ...` at **`tracking.ts:2122`**
and **`clips/[id]/review/route.ts:554`**. No `AgencyEarning` row is written for a marketplace clip at
either site. **Nothing in this round changed that and nothing in BL-845, BL-847 or BL-849 did either.**

---

## PART 5 — RE-VERIFYING WHAT PRIOR ROUNDS CLAIMED, PER CLAIM

| Claim | Verdict | How |
|---|---|---|
| BL-845: the `(submissionId, platform)` unique index now exists | **VERIFIED** | `pg_index` reports `marketplace_clip_posts_submissionId_platform_key` with `indisunique=true, indisvalid=true, indisready=true`. That is BL-845's own criterion and it is met. |
| BL-845: `marketplace_video_hashes.hash` is unique | **VERIFIED** | `marketplace_video_hashes_hash_key` present in the catalogue. |
| BL-847/BL-849: "six strike entrances", corrected to five | **BOTH OVERSTATED** | `grep -c` for real `marketplaceStrike.create` call sites returns **three**: `admin/users/[id]/marketplace-ban/route.ts:183` (owner issues a ban), `excessive-rejections.ts:207` (rejection threshold), `marketplace-timers.ts:252` (missed post deadline). A fourth grep hit is an autogenerated Prisma JSDoc example. |
| BL-849: the payee ban gate exists in the payout review route | **VERIFIED BY READING, NOT TRIGGERED** | `payouts/[id]/review/route.ts:251` reads `if (!standing.ok && !acknowledgeBannedPayee)`. The file is now 1,377 lines, up from the 1,232 BL-849 measured. I did **not** trigger it, and the reason is in the honesty section below. |
| BL-847: Instagram posting works end to end | **NOT VERIFIED, AND NOT INHERITED EITHER** | Requires a genuine freshly posted Instagram reel and live HikerAPI spend. Not run. Still an open claim, exactly as BL-849 left it. |
| The submit route is "OWNER-gated during hidden phase" | **STALE COMMENT, CONTRADICTED BY THE CODE** | The docstring at `submissions/route.ts:73` says so; the code at `:100` and `:148` uses `role !== "OWNER"` only to ADD checks (ban, Discord) for non-owners. A real clipper can submit. Anyone reading that comment would draw the wrong conclusion about pilot readiness. |

---

## PART 1 — WHAT A CLUMSY POSTER ACTUALLY MEETS

Five listings were built the way a person ends up with them: two identical twins, one with a typo,
one at zero slots, one at 999,999.

**THE ZERO AND THE HUGE ONE CANNOT HAPPEN THROUGH THE PRODUCT, and I am correcting my own fixture
rather than reporting a defect that is not there.** Both the create route
(`listings/route.ts:261` and `:332`) and the PATCH route (`listings/[id]/route.ts:518`) refuse
anything that is not an integer between 1 and the campaign's `maxClipsPerUserPerDay`. My fixture
wrote those values with a direct Prisma insert, bypassing the route. **The validation is real.**

**The twins ARE distinguishable, but only by campaign.** The poster's own list
(`listings/route.ts:743-760`) includes `campaign.name`, and `usedToday` is grouped per listing
(`:775-793`), so the slot count reads correctly for each. Two listings with the identical niche text
are otherwise identical on the row.

**A REAL CONFUSION POINT, AND IT IS A SILENT ONE.** `usedTodayMap` is wrapped in a try/catch at
`listings/route.ts:795-799` whose fallback is an **empty map**, with the comment "Fallback:
usedToday=0". If that aggregation throws, **every listing renders "0 used today"** and a poster whose
slots are entirely consumed is shown full capacity. This is the exact shape BL-864 was caught by, a
helper that reads every value as zero and makes a broken screen look healthy. It is reported, not
changed, because changing it means choosing what a poster should see when the count is unknown, and
that is the owner's call.

**A structural constraint worth knowing before a pilot:** `mla_campaign_clipacct_active_unique` is a
partial unique index on `(campaignId, clipAccountId) WHERE status <> 'FLAGGED'`, so **one connected
account can serve only one active listing per campaign.** The twins had to sit on different
campaigns to exist at all. A poster who tries to run two listings on one campaign with one account
will be refused, and that refusal is correct but will not be obvious to him.

---

## PART 6 — WHAT WAS PROVEN, AND THE HONEST GAPS

### The proofs

- **Money:** 64 assertions, 0 failed, every figure hand-computed first.
- **The hash guard:** 2 of 5 before the fix, **5 of 5 after**.
- **The clipper walk:** 7 of 7 against the real route on a production build.
- **Render:** **100 assertions, 0 failed**, 25 shots across five marketplace surfaces (browse,
  listing detail, my-submissions, incoming, strikes) at 320, 375, 414, 1280 and 1440. Every shot read
  `window.innerWidth` back, measured 0 horizontal overflow, confirmed the splash lifted, and
  **confirmed the page did not bounce to `/login`**, which is the assertion that stops a redirect
  being photographed as a passing screen.
- **Teardown:** 32 ledgered rows, `VERIFIED: 0 of 32 remain`, and zero `bl868sbx-` rows anywhere.
- **Builds:** baseline `TSC_BASELINE_EXIT=0` with 0 errors taken BEFORE any edit, build
  `BUILD1_EXIT=0` with 0 TS errors, hooks gate **0 errors and 10 warnings** against a limit of 11,
  every warning in a file this round did not touch. eslint is genuinely present (3 binaries in
  `node_modules/.bin`), so the gate is not a silent no-op.

### A tooling defect this round hit and fixed

Driving the REAL submit route mints product rows with cuid ids, which the sandbox ledger cannot know.
`sweep.ts` adopted notifications and clip stats but **had no marketplace block at all**, so 6
submissions and 5 video hashes would have been orphaned in production permanently. The sweep now
adopts marketplace submissions, posts and strikes.

**Video hashes could not be adopted, and the safeguard is why.** A hash row has no column holding a
sandbox id, so it cannot satisfy LOCK 2, and when this round first tried to force it with a
non-existent `creatorId` column **the destroyer refused the entire run before deleting a single
row**. That is the tooling working. They are removed instead by `bl868-hash-cleanup.ts`, bounded by
the ledger's own submission ids rather than by any pattern, which printed the exact five ids and the
exact `DELETE` before running it and verified 0 remained.

### What I did NOT run, stated plainly rather than implied

- **No OWNER was created and no owner-side HTTP route was driven.** `notifications.ts` enumerates
  owners with no `isTestUser` filter anywhere in its email fan-out, so a sandbox OWNER row would be
  emailed by any production cron tick landing inside this round's window, at an address that cannot
  receive mail. The owner-side money is proven by pure function instead, and the banned-payee gate
  was read rather than triggered.
- **The concurrent double-post race was not re-run.** The index was verified enforcing in the
  catalogue, which is BL-845's own criterion, but reproducing the race needs the post path, live
  provider spend and a real posted video.
- **Instagram posting end to end was not run**, for the same reason.
- **PART 4's later-breaking cases were not exercised.** Months-later earnings, an indefinite listing,
  a mid-payout ban, a deleted poster, post-payment devaluation, a COMPLETED campaign under a live
  listing and quota resets across daylight saving are all still open. The quota boundary was read and
  is **UTC midnight** at all five call sites (`submissions/route.ts:449-450`, `:585`, `:785`,
  `browse/route.ts:397`, `listings/route.ts:771`), so it does not drift with the poster's timezone,
  but that is a code reading and not a test.

**One cycle was run, not several.** The suite found the hash defect, the fix was made, and the entire
suite was re-run green. Nothing else this round changed required a second cycle.

### Concurrency with BL-869

BL-869's rows were present throughout and are visible in the closing census: 12 users, 1 campaign and
6 clip accounts carrying its prefix. `verify-gone.ts` reports **50 checks, 39 passed, 11 failed**, and
**every one of the eleven is BL-869's rows or real platform activity**, not this round's residue:
`trainer_relationships 0 → 7`, `active_pairings 0 → 4` and `trainer_holders 0 → 1` are BL-869 testing
the trainer alone; `users +14`, `campaigns +1`, `clip_accounts +6` and `real_clips +11` are BL-869
plus 14 real signups and 10 clips from 7 real people during the window. **The real payout fingerprint
`caf939b6ebfd6dc5367681eb3aa2d326` is byte-identical before and after and zero payouts were created,
so no money moved.**

### Invariants

Nothing was weakened. The only source change is `video-hash.ts`, which touches no money, no status
and no invariant. **The 6 money files, `tracking.ts` and `campaign-era.ts` are byte-identical by blob
OID on both refs.** No schema change, no `prisma migrate`, no index created, no Apify actor run, the
11 BL-678 guards intact, no Prisma in a browser bundle, no Supabase pool errors.

---

## THE ACCESSIBILITY REVIEW, AND WHY I REPORTED IT RATHER THAN FIXED IT

The mandatory review ran across the five marketplace surfaces. **This round changed no UI**, so there
was no changed surface to review; it was pointed at the surfaces a pilot will actually touch, which
is the more useful question. Its verdict: **not yet safe for a non-visual pilot user**, with ten MUST
FIX items.

**Nine of the ten are one component.** `src/components/ui/modal.tsx` is shared by SubmitClipModal,
post-clip-modal, reject-modal, request-delete-modal and rate-user-modal, and it has no focus trap
(Tab escapes to the page behind the overlay), never moves focus into the dialog on open, never
returns focus to the trigger on close, carries no `role="dialog"`, `aria-modal` or `aria-labelledby`,
and its close button has no accessible name. The remaining items are the Drive URL field's error not
being wired to the field itself (`SubmitClipModal.tsx:238-244`), the Mark-as-posted validation error
being **completely silent** with no live region at all (`post-clip-modal.tsx:305-307`), the reject
reason field having no `required`, the submission counters not being in a live region
(`MpCommandBar.tsx:35-42`), and the submission lists having no list semantics.

**I DID NOT FIX THEM, AND THE REASON IS THE SHARED PRIMITIVE.** `modal.tsx` is used well beyond the
marketplace. Adding a focus trap and a dialog role to it changes keyboard behaviour on every modal in
the product, and this round rendered five marketplace surfaces, not every screen that opens a modal.
Shipping an unverified change to a shared interaction primitive is the shape of defect these rounds
keep finding, so it goes on the record as a focused follow-up rather than a late addition here. The
review notes the same thing from the other side: every MUST FIX is centralised, so one small round on
`modal.tsx` plus two modal files plus `MpCommandBar.tsx` clears all ten.

What is already correct is worth recording too, because it means the gap is narrow: icon-only buttons
are named correctly across all 19 files, the toast and banner live regions work, SubmitClipModal's
platform-slot fieldset and its screen-reader slot announcer are right, every textarea is labelled, the
star rating uses proper radiogroup semantics, load failures use `role="alert"`, and Escape closes
every modal.

**One thing to pass on without overstating it:** one of the review's subagents reported that it had
encountered what it read as an injected instruction telling it to switch to a Bash-only,
bypass-permissions mode, and that it ignored it and stayed read-only. I could not confirm whether that
was a genuine injection or the subagent misreading an ordinary harness message it inherited, and I am
not claiming it was an attack. It is recorded because it is the kind of thing the owner would rather
hear about unconfirmed than not hear about at all.

---

## THE MODEL SPLIT

**Opus** did every money determination and every judgement that decides what gets written: reading
the hash function and deciding it was a money defect, designing and writing the fix, the hand
arithmetic for all seven cash cases and five split cases, the decision not to create a sandbox OWNER,
the teardown design when the destroyer refused, and this report.

**Sonnet** did two retrieval jobs: distilling fourteen prior reports, and mapping the marketplace code
surface to file:line. **I corrected the second one before using it:** it reported the ~1,232-line file
as the marketplace post route when it is `payouts/[id]/review/route.ts`, and it counted strike
entrances correctly at three where the reports claimed six and then five. Sonnet also ran the
accessibility review.

**Nothing money-touching was split.** The obvious candidate was running the split arithmetic in a
subagent. It was not delegated, because a subagent reporting "the parts equal the gross" is a claim
about whether a clipper is paid correctly, and this round already contains one case of a prior
round's claim being overstated by a factor of three.

---

## THE PILOT VERDICT

**Yes, one poster and a handful of clippers can run this tomorrow, with three conditions.**

The submission path is genuinely solid: the slot arithmetic is per listing and enforced in a
Serializable transaction with two further re-checks, a full listing refuses clearly and says when it
resets, the ban merge and Discord gate both run, the unique index that once let two posts earn on one
slot is enforcing, and the money splits exactly with the platform absorbing the rounding. The
duplicate hole that would have paid twice for one video is closed.

**The three conditions:**

1. **Redeploy.** The hash fix does nothing until it is deployed.
2. **Run the pilot on ONE campaign with ONE poster account**, because one connected account can serve
   only one active listing per campaign.
3. **Do not rely on duplicate detection across clippers.** Two different clippers submitting the same
   source video is accepted and produces only a log line.
4. **Do not put a screen-reader user in the pilot yet.** The modal primitive has no focus trap and no
   dialog role, and the Mark-as-posted error is silent. A sighted pilot is fine today; a non-visual
   one should wait for the follow-up round named above.

**What to watch on day one, in order:**

- **Every approved submission's Drive link, by eye.** The re-upload gap is real and unclosed: a
  clipper who re-uploads the same video gets a new file id and a new hash. Ten submissions is a
  number a person can still check by hand.
- **The poster's "used today" count against the actual submissions.** If it ever reads 0 while
  submissions exist, the aggregation threw and the fallback is lying.
- **The first payout's cash figure against this report's table.** A $100 gross must send $91.00
  plain, $87.00 express, $81.90 with a trainer.
- **`marketplace_strikes` for anything with reason `MISSED_POST_DEADLINE`.** That is the entrance
  BL-847 and BL-849 both fought over and it is the one that strikes a poster for the platform's own
  failure.
- **Instagram specifically**, because posting end to end there has still never been proven by anyone,
  including this round.
