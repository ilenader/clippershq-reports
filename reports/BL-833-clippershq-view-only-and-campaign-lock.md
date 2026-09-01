# BL-833 — campaign creation is locked to the owner, and "watching only" grants nothing else

**2026-09-01 · DB `now()` = `2026-09-01 17:34:58.030857+00` (first read) to `18:35:37.332743+00` (last) · BUILD AND MERGE.**
Base `origin/main` @ `9e4a7849`. Branch `checkpoint/BL-833` @ `6d13c989`. **Merged and verified pushed: `origin/main == local == fdce6afd`.** Tags `pre-BL-833`, `post-BL-833`, `pre-merge-BL-833`, `post-merge-BL-833`, all on origin. Isolated worktree `C:/w833`, a short path, `node_modules` never junctioned, **removed at the end**. Every database read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted; no wallet address read or printed.

**A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE.**

> ## THE ANSWER, FIRST
> **`tg..d7` CANNOT CREATE A CAMPAIGN AND NEVER COULD.** `POST /api/campaigns` read `role !== "ADMIN" && role !== "OWNER"`, so a REVIEWER was already refused 403. Asked as **him**, on a real minted session: **403**.
> **WHAT HE COULD REACH IS THE CREATE SCREEN**, and that is the real defect. The admin layout admits every REVIEWER to every `/admin/*` page, and the **"New Campaign" button was rendered to anyone who got there**. The form opens, fills in, and ends in a red 403. That is BL-790's finding with the sign flipped.
> **WHO COULD ACTUALLY CREATE ONE WAS ADMIN OR OWNER. Now it is OWNER only.** Three accounts hold OWNER, **zero hold ADMIN**, so nobody lost a power they were using.
> **NO CAMPAIGN WAS EVER CREATED BY A NON-OWNER.** 19 of 34 carry an OWNER id; the other 15 are archived test-harness rows with a NULL creator.
> **THE NEW LEVEL REPLACES REVIEWING RATHER THAN STACKING WITH IT**, and **three server holes had to be closed** before "and nothing else" was true. None was visible from the brief.
> **NOBODY REAL WAS GRANTED ANYTHING.** A synthetic fixture held it for 32 minutes and was removed.

---

## PART 0 — WHO COULD CREATE A CAMPAIGN, MEASURED BEFORE IT WAS CLOSED

**The three creation paths, and the gate on each, `file:line` on `origin/main` @ `9e4a7849`:**

| path | gate before | gate after |
|---|---|---|
| `POST /api/campaigns` | `route.ts:270` — `role !== "ADMIN" && role !== "OWNER"` | `:294` — **`role !== "OWNER"`** |
| `createCampaign` server action | `actions/campaigns.ts:51` — ADMIN or OWNER | `:64` — **OWNER** |
| `POST /api/campaigns/past-create` | `:61` — OWNER only | unchanged |

**Proven by direct request, BEFORE and AFTER, on the same machine, the same database and the same port, with an EMPTY BODY.** The route checks the role first and the required fields second, so a **400 means the permission gate passed and validation refused** — the door is open, measured without walking through it. **No campaign row was written on either side.**

```
BEFORE (main's tree)                        AFTER (this branch)
as dev OWNER     400 "Name and platform…"   as dev OWNER     400 "Name and platform…"
as dev ADMIN     400 "Name and platform…"   as dev ADMIN     403 "Only the owner can create a campaign."
as dev REVIEWER  403 Forbidden              as dev REVIEWER  403 "Only the owner…"
as dev CLIPPER   403 Forbidden              as dev CLIPPER   403 "Only the owner…"
signed out       401 Unauthorized           signed out       401 Unauthorized
past-create ADMIN 403                       past-create ADMIN 403
```

**And again on the production build with REAL minted sessions**, not dev-auth: the owner reaches validation (400); **`tg..d7`, `jdb001`, a real CLIPPER and the watch-only holder are all 403**.

### The named user, and the correction

| | measured `2026-09-01` |
|---|---|
| `tg..d7`, id `cmp9d0xu3…` | role **REVIEWER**, mode TRIAL, capabilities `[]`, `reviewerScopeInvitedOnly` **true**, ACTIVE |
| has he ever been ADMIN or OWNER | **no** — his entire audit history is Discord role syncs and two `REVIEWER_CONFIG_UPDATED` rows from 2026-08-12 |
| could he create a campaign server-side | **no, 403, before and after** |
| could he open the create form | **yes** — `/admin/campaigns` returned 200 for him and the button was ungated |

**Who else could, who should not: an ADMIN.** The role exists in code and the gate accepted it. **There are zero ADMIN accounts** (1,562 CLIPPER, 26 REVIEWER, 20 CLIENT, 3 OWNER), so the hole was real and unexercised.

### Was a campaign ever created by a non-owner? No.

| creator | role today | campaigns | first | last |
|---|---|---|---|---|
| `An..ra` | OWNER | 9 | `2026-04-22 16:42:51.374` | `2026-08-07 10:17:06.764` |
| `Ba..34` | OWNER | 9 | `2026-04-29 08:33:36.984` | `2026-08-12 13:38:10.125` |
| `Da..98` | OWNER | 1 | `2026-07-28 12:56:08.777` | `2026-07-28 12:56:08.777` |
| **NULL** | — | **15** | `2026-06-01 22:13:53.495` | `2026-06-02 02:43:10.832` |

**All 15 NULL-creator rows are archived synthetic harness campaigns** (`rv-fix-3-…`, `rvv-…`, `rfvc-…`, `rwf2-…`), `isArchived = true`, created by scripts constructing their own Prisma client in the same window as BL-790's `rwf2-*` test reviewers. **None carries rates the owner did not set, because none is a real campaign.**

### The neighbouring powers, stated because they sit beside creation

| power | route | who | proven |
|---|---|---|---|
| edit / pause | `PATCH /api/campaigns/[id]:145` | ADMIN or OWNER; an ADMIN is further limited to campaigns he created, owns, is assigned to or shares a team with, and his edit **queues as a pending edit** | ADMIN 403 *"You do not have access to edit this campaign"*, REVIEWER 403 |
| archive | `DELETE /api/campaigns/[id]:920` | **OWNER only** | ADMIN 403, REVIEWER 403 |
| permanent delete | `[id]/destroy:26` | **OWNER only** | ADMIN 403 |
| restore | `[id]/restore:21` | **OWNER only** | ADMIN 403 |

**The OWNER side of those four was deliberately NOT probed.** They write, and the only campaigns available are real. Refusals only.

**REPORTED AND NOT CHANGED:** `updateCampaign` (`actions/campaigns.ts:120`) and `deleteCampaign` (`:140`) are still `ADMIN || OWNER`, and `deleteCampaign` is a **hard** delete. Both are **caller-less** (grep across `src/` finds only their definitions), neither is creation, and narrowing them is a separate decision. `createCampaign` beside them **was** closed, because it is creation and because a `"use server"` export is a real network surface whether or not a component imports it.

**The UI now follows the server.** The "New Campaign" button renders only for the owner, the empty state's second create button is gated with it, and the existing subtitle says *"Manage your campaigns. Only the owner can start a new campaign."* Nothing is said until the session settles — the role default is `CLIPPER`, so without that guard the owner would see the denial for a beat on every visit.

---

## PART 1 — THE WATCHING-ONLY LEVEL, DEFINED BY WHAT IT EXCLUDES

**`CLIP_WATCH_ONLY`. OFF by default. One key, one sentence: hold it and you watch; you do not judge.**

**IT REPLACES REVIEWING. It does not stack.** Holding it suppresses the three automatic Basic capabilities (`CLIP_VIEW`, `CLIP_APPROVE`, `CLIP_REJECT`), reusing the mechanism BL-190 built for the referral-only reviewer, so there is **one suppression idea in that file and not two**.

> **The stacking version was designed, reviewed and deleted.** Its escape hatch was ticking the Basic boxes — which are hardcoded `checked` and natively `disabled` with the words *"cannot be turned off"*, so it was **unreachable from any screen**. The server would have been naming a UI contract the UI could not keep, which is BL-790's defect with the sign flipped. It also cost the owner four extra facts to predict one press. The accessibility review measured that memory demand and set the target at zero: the card computes the resulting state and shows it.

### THREE SERVER HOLES HAD TO BE CLOSED, AND NONE WAS VISIBLE FROM THE BRIEF

**1. `requireOwnerOrCapability` carried its own copy of the Basic-set rule.** It knew nothing about suppression, so **five routes gating on `CLIP_VIEW` would have answered a watch-only account**: both `review-evidence` routes (BL-775's measurements panel), both `reviewer-note` routes (BL-666's bot note), and `clip-analytics`. The level would have shipped granting machine suspicion and platform analytics — the exact things it is defined to exclude. It now delegates to `hasCapability`, so there is **one rule and not two**, which is BL-821's lesson in a different file. **It also fixes BL-190's suppression, which that helper never honoured. Measured before the change: ZERO users hold `REFERRAL_MANAGE`, so no live person's access changed.**

**2. `/api/clips` never checked `CLIP_VIEW` at all.** Its own comment said so: *"CLIP_VIEW is the universal Basic floor, so we don't gate on it here."* True of every reviewer until a suppression existed. Without the check the **whole review queue** — clipper handles, campaign names carrying CPM figures, rejection reasons, fraud scores — would still have been served. It checks now, **read from the DB row rather than a cold token**, on the round trip that was already being made. **Zero live effect: `hasCapability` returns true for all thirteen live reviewer rows exactly as before.**

**3. The key suppresses only the Basic three.** `hasCapability` then falls through to `granted.includes(key)`, so a row also holding `EARNINGS_VIEW` or `PAYOUT_VIEW` would have kept it, and the page perimeter narrows *pages* while `/api/admin/*` is a different tree. A card promising *"and nothing else"* over such a row would have been a false statement about money. **The grant route now refuses `CLIP_WATCH_ONLY` beside any other key and names the ones to turn off first** — enforced at the server, because a rule that lives in a component is not a rule.

### Every exclusion, proven individually by direct request

Production build, real minted sessions, never the dev-auth bypass (a bypass session carries an empty capability list and every assertion would pass for the wrong reason). **52 checks, 0 failures.**

```
approve                                   403      the review queue itself (/api/clips)   403
reject                                    403      agency earnings                        403
flag                                      403      payouts                                403
undo (back to PENDING)                    403      unpaid payouts                         403
reassign picker, GET   (levels 1 and 2)   403      clip accounts                          403
reassign move,   POST  (levels 1 and 2)   403      the full user list                     403
track-now                                 403      the audit log                          403
                                                   the ratification queue                 403
bot note, single       403                         clip analytics                         403
bot note, batched      403                         evidence panel, single                 403
                                                   evidence panel, batched                403
campaigns  ->  HTTP 200 with 0 campaigns, so no budget, no rate and no owner economics reach him
```

**By grep over the real response bytes: 0 of 31 forbidden field names appear**, and the word `campaign` does not appear at all. The list covers BL-531's owner economics (`ownerCpm`, `agencyFee`, `clientName`, `aiKnowledge`, `budget`, every rate and earnings column) and BL-518/BL-521's machine suspicion (`fraudScore`, `fraudReasons`, `noteJson`, `noteText`, `wouldReject`, `draftReply`, `blindSpots`, `humanChecks`, `metadataHealth`).

**The six owner-only surfaces BL-799 proved return 403 still answer the OWNER 200**, all six, so the refusals above are the gate biting and not a broken build.

### SCOPE, STATED PLAINLY

**PLATFORM WIDE. Every clip that came in — 8,580 live clips — not the campaigns they are assigned to and not their own invitees'.** That is what was asked for.

**IT DOES NOT INTERACT WITH THE PARTNER SCOPE FLAG.** The route reads neither `reviewerScopeCampaignIds` nor `reviewerScopeInvitedOnly`. BL-802's flag is on for exactly one partner, deliberately; this round **neither reads nor writes it**, and his own queue is unchanged (proven: he still reaches `/api/clips` 200 and is refused the watch feed 403).

**The consequence is stated on the card, UNCONDITIONALLY** rather than only for that one partner, because the watch list is wider than the review queue for nearly every reviewer and a warning shown to one person would tell the owner the opposite about everyone else:

> **Note.** This list is every clip on the site. It ignores the campaign list you ticked for them. **That includes clips from clippers you kept out of their list on purpose.**

---

## PART 2 — HOW THE OWNER GRANTS IT, AND HOW HE TELLS THE LEVELS APART

**On the profile card BL-799 placed the reviewer controls on**, as a peer of *"Move clips between campaigns"*, behind **one relabelling `<button>`** — not a checkbox. A checkbox's DOM checkedness flips on activation before any handler runs, so a screen reader would announce "checked" and then a panel would appear saying nothing had been granted; and it would be the only checkbox among four grants that are buttons.

```
off →  Watching only: let this person watch every clip
on  →  Watching only: stop this person watching every clip
```

**No typed phrase, deliberately.** `FULL AUTHORITY` hands over the final say and `MOVE CLIPS` / `ANY CLIPPER` each change what a clipper is paid. This one grants strictly **less** than the reviewer role beside it. **Taking it away needs nothing at all**, because obstructing the safe direction is a defect rather than a safeguard.

**Turning it ON opens a confirmation, because it takes judging away.** The panel is a `role="group"` disclosure, not a dialog, focus lands on the container, and it states the before and the after **computed, not remembered**:

> **Now:** they can judge clips, and they cannot watch other clippers' clips.
> **After:** they can watch every clip on the site, and they cannot judge any clip.
> You can turn this off again at any time. One press gives judging back.

### AT A GLANCE, which of the levels a person holds

There are now four, so the card carries a block headed **"What they hold now"**, inside the `<Card>` under its `h3` — inside, because the card itself sits behind a collapsed disclosure and a line above it would not be there when the card is. `<ul role="list">` (the CSS reset strips `list-style`, and WebKit then drops the implicit role). **No `role="status"`, no `aria-live"`** — BL-825 settled that here: the text changes in the same commit as a `.focus()` call, which flushes the polite queue.

```
Judging clips: off. They cannot approve or reject.
Moving clips: off.                     (or "invited clippers' clips only" / "any clip in their list")
Watching only: on. They watch every clip on the site.
They make no decisions, so there is nothing for you to agree to.
```

**Every line reads `hasCapability`, the same function the server gates on**, so the card cannot describe a permission the server would refuse.

**And the rest of the card stops lying.** The Basic group's intro said *"Always granted to a reviewer; cannot be turned off"* — false the moment this is on. It now reads *"Turned off for this person. You set them to Watching only…"*, the three boxes render **unchecked**, and they carry `aria-disabled` with a **visible** reason rather than native `disabled`, because a natively disabled input cannot take focus and its description is never announced. One further sentence covers the reviewing settings below: *"The review settings below do not apply while Watching only is on. They are kept so they are still there when you turn it off."*

**STACKS OR REPLACES: it REPLACES, and the card says so before the press.** Nobody loses the ability to judge silently.

---

## PART 3 — WHAT THEY SEE

**`/admin/watch`, fed by `GET /api/admin/watch-clips`.** Newest first, 30 at a time, 8,580 clips.

Each item: **the video** (a cover image and one link, "Open clip"), **the platform**, **when it came in**, and **the four public counts**.

| figure | where it comes from |
|---|---|
| Views | `clip_stats.views` on the newest snapshot for that clip |
| Likes | `clip_stats.likes`, same row |
| Comments | `clip_stats.comments`, same row |
| Shares | `clip_stats.shares`, judged by BL-820's shared `shareState` |

**These are the numbers a member of the public could count off the post.** They are what the tracking pipeline scraped from the public page, not the platform's internal state.

**AND THEY SAY WHEN THEY ARE NOT NUMBERS.** `sharesSource` is the **only** source column on `ClipStat`; `views`, `likes` and `comments` are `Int NOT NULL DEFAULT 0`. So:

* **a clip with no snapshot at all shows all four as unmeasured**, never as 0;
* **with a snapshot, only shares takes the per-cell rule**, through `shareState`, which also knows YouTube publishes no share count at all and says so rather than promising a number that can never arrive;
* **the legend says nothing about the other three**, because explaining one column would teach the reader that a plain 0 in the others was measured.

Measured across the newest snapshot of every live clip: **Instagram 5,653/5,736 with a positive view count, 5,139 likes, 1,529 comments, 1,830 with a labelled share count. TikTok 1,345/1,411, 1,270, 590, 251. YouTube 1,306/1,395, 673, 204 and 0 labelled shares** — which is why YouTube reads *"YouTube does not publish share counts"* and not *"not measured"*.

### What is deliberately absent, and why each had to be thought about

* **the clipper** — no id, no name, no handle, no account username;
* **the campaign, not even its NAME**, because campaign names here carry the rate inside the name (*"Zhus Meme (0.20 CPM)"*), so the name **is** owner economics;
* **the clip URL as text** — a TikTok or Instagram address contains `@handle`, so the address is a link and never printed;
* **status, rejection reason, reviewer, earnings, rates, fraud score, bot note, evidence** — none reaches the route.

**The select list is exhaustive and IS the enforcement.** No `include`, no spread, no rest, so a column added to `Clip` later cannot arrive here by accident.

**The cover image is `alt="" aria-hidden="true"`.** A description would either be a guess or would leak what the page withholds, and a non-empty alt paints its literal text thirty times when the re-host bucket is down. The link carries the purpose instead: *"Open clip 3 on Instagram (opens in a new tab)"* — an **ordinal**, because on a same-day page timestamps share their leading words and NVDA's Elements List filters by leading characters. When there is no thumbnail an `aria-hidden` placeholder renders; `CampaignImage` is deliberately **not** reused, because its fallback draws campaign-name initials.

---

## PART 4 — PROVED BY REQUEST, AND ONE MEASUREMENT LIMIT NAMED

**`scripts/bl833-verify.mjs`: 52 passed, 0 failed.** Production build, real minted sessions. Nothing mutated: every request is a GET or a deliberate refusal, and the four review calls were aimed at a real PENDING clip precisely so a 200 would have been visible — all four answered **403**.

**An ungranted user sees no change at all.** `tg..d7` and `jdb001`: refused the watch feed 403, still reach their own review queue 200, `jdb001` still holds his reassignment picker. A real CLIPPER: refused the feed 403, still reaches his own clips 200, and **none of twelve forbidden field names appears in his own payload**. BL-531, BL-518 and BL-521 hold.

**THE PAGE PERIMETER COULD NOT BE PROVEN BY STATUS CODE, AND THAT IS SAID RATHER THAN FUDGED.** `notFound()` called from a **dynamic** layout returns **HTTP 200 with a 404 body**, and every page in this tree is a client component whose text is absent from the server HTML entirely. A status assertion would have passed or failed for reasons unrelated to the perimeter. It is proven **in a real browser on the rendered DOM**, at all five widths: as the watch-only holder `/admin/watch` renders the `h1` **"Clip watch"** and `/admin/clips`, `/admin/payouts`, `/admin/campaigns` and `/admin/users` all render **"This page could not be found"**. The byte lengths agree: his `/admin/watch` is the **same page the owner gets** (43,542 vs 43,541), his `/admin/clips` is the **anonymous 404** (43,482 vs 43,482) against the owner's 43,778.

**ONE THING HE STILL SEES, STATED RATHER THAN HIDDEN.** BL-799 made the ordinary **clipper** navigation unconditional for every REVIEWER, so a watch-only holder's sidebar still carries Earnings, Payouts and Referrals — **their own**, the same pages any account has. That is not another clipper's money and it was deliberately left: removing someone's view of their own balance to tidy a screen would be a harm, not a tightening. The render pass asserts those links point at `/earnings` and `/payouts` and **never** at `agency-earnings` or `/admin/payouts`, and that the only `/admin` link in his sidebar is `/admin/watch`.

---

## PART 5 — RENDERED, AND MERGED

**`scripts/bl833-render.mjs`: 25 shots, 0 at the wrong width, 0 with horizontal overflow, 135 assertions, 0 failures.** `window.innerWidth` printed beside every shot; viewport set on the Playwright **context**, so the page really is 320 CSS pixels wide.

```
watch-feed              320 · 375 · 414 · 1280 · 1440
watch-perimeter-clips   320 · 375 · 414 · 1280 · 1440
owner-grant-card        320 · 375 · 414 · 1280 · 1440
campaigns-reviewer      320 · 375 · 414 · 1280 · 1440
campaigns-owner         320 · 375 · 414 · 1280 · 1440
```

**Read at 375** as the watch-only holder: *Clip watch · "Every clip that comes in, newest first. Watch the video and see its public counts." · Showing 30 of 8580 clips*, then cards each carrying a cover, **Open clip**, *"Instagram • Came in September 1, 2026"*, and Views / Likes / Comments / **Shares —**. **Read at 1280** as `jdb001`: *Campaign Manager · "Manage your campaigns. Only the owner can start a new campaign."*, no New Campaign button, and the empty state repeating it. **Read at 375** as the real OWNER on the fixture's profile: **What they hold now** — *Judging clips: off · Moving clips: off · Watching only: on · They make no decisions*.

> **THE RENDER PASS CAUGHT A CONTRADICTION NOTHING ELSE WOULD HAVE.** BL-788's explainer still said *"On each clip they can suggest approve or suggest reject"* four inches under the new line saying *"Judging clips: off"*. It is branched in this diff and asserted against from now on.

### Merged and pushed

| | |
|---|---|
| clean `tsc` baseline on the **untouched** worktree, before any edit | `npm ci` **0**, `npx prisma generate` **0** (before tsc, because `npm ci` wipes the client), `npx tsc --noEmit` **0**, `grep -c "error TS"` = **0** |
| branch | `checkpoint/BL-833` @ **`6d13c989`**, VERIFIED on origin by `safe-push` |
| merge commit | **`fdce6afd`**, `origin/main == local` VERIFIED by `safe-push` |
| conflicts | **none**; main never moved from `9e4a7849`, and the **merged tree OID equals the branch tree OID exactly** (`d60a4c17`), so the branch's green build IS the merge's build |
| BACKLOG | **169 sections before, 170 after**, `BL-833` ×3, **0 conflict markers**, counted with `grep -c`, never piped to `head` |
| **`checkpoint/BL-723`** | **confirmed NOT an ancestor of main** |
| files | 19 changed, 1,783 insertions, 34 deletions |
| worktree `C:/w833` | **removed**, 0 node processes left behind |

---

## THE ACCESSIBILITY REVIEW — RUN BEFORE ANY UI, 14 BLOCKING ITEMS, ALL IMPLEMENTED

The lead and nine specialists reviewed the **design**. The ones that changed the work:

**It killed the stacking design outright (B1).** The escape hatch it depended on was unreachable, so the server comment would have named a UI contract the UI could not keep.

**It found that "and nothing else" was false (B13)** — the key suppresses only the three Basic capabilities, and the page perimeter narrows pages while `/api/admin/*` is a different tree. The server now refuses the combination.

**It caught that `--bg-page`, which the house rules name, has 42 uses and ZERO declarations app-wide (B11).** No second stylesheet, no `setProperty`, no inline `<style>`; a positive control against `--bg-primary` finds both theme blocks. The new page uses real tokens, and the four counts are **not** `font-bold text-accent` — the accent measures 3.40:1 in the light theme the navbar exposes, below the 4.5:1 bar for normal-size text.

**It caught that a natively `disabled` input can never announce its own reason (B14)**, which is BL-790's rationale applied to the new suppressed state.

**It caught the missing fourth Escape branch and fourth focus branch (B6).** The old final `else cancelMoveAny()` routes to a setter written `p === "MOVE_ANY" ? null : p` — a no-op for any other panel, so Escape would have moved focus to the wrong trigger and left the new panel open; and without a fourth focus branch the panel opens with focus nowhere.

**It caught that the sidebar hand-copied BL-190's rule (B4)** and would have handed a watch-only reviewer links to five pages that now 404. The mode is derived once, in `getReviewerNavMode`.

**It caught the shares regression in the landed route (B9).** My first draft collapsed the field with `sharesSource ? shares : null`, which silently discards the **32,937 TikTok snapshots** holding a real positive count written before the label column existed, and erased the third state entirely.

**It caught B12**, the finding above about the other three columns, and **B8**, three separate defects on the campaigns screen: the missing `status` from `useSession`, a **second** ungated create button inside the empty state, and that prose in the button's flex cell crushes the `h1` at 375px.

**It measured the copy.** Flesch-Kincaid on every rendered string: the whole card grade **4.8**, my first draft sentence grade **18.3** (46 words, eight consecutive negations). Ceiling set at **FK ≤ 6.0, no sentence over 20 words**, and the shipped copy is written to it.

**Reported, NOT fixed:** BL-825's own *"Level 1 / Level 2"* button copy names the number rather than the reach; the worst shipped sentence on this card is BL-825's 35-word payouts line at grade 15.6; and BL-821's page-wide silent list replacement on `/admin/clips` (B12 there) still deserves its own round.

---

## SAFETY

| | |
|---|---|
| the 6 money files plus `tracking.ts`, `campaign-era.ts`, `apify.ts` and `campaign-reassign.ts` | **byte-identical by blob OID on BOTH refs**: `ac5be7de`, `797e2098`, `81a683c1`, `359bcbbe`, `61cef393`, `ef5cdae7`, `106e16ad`, `d66d4534`, `3e513702` |
| schema | **no change**, no `prisma migrate`; `prisma generate` only. No index created. The new capability is a string in an existing `text[]` column |
| Apify | **no actor run**; `apify.ts` untouched, its 11 BL-678 guards intact |
| payouts | **208 rows before and after**; no payout created, modified, approved or cancelled **by this round** |
| earnings invariant | **0 violations** before and after |
| capability fingerprint across all **1,612** other users | **`4cca3bbfb5bfe7f60ede09c2dd8eb663` before and after, identical** |
| Supabase pool errors | **0** across all three server runs |

**MOVED IN THE WINDOW AND NOT MINE, NAMED RATHER THAN SMOOTHED.** Approved clips fell 7,251 → 7,237, rejected rose 1,287 → 1,301, approved earnings moved $11,856.30 → $11,813.57, and the newest payout `updatedAt` moved. **Every audit row in the window is accounted for:** 14 `REJECTED_CLIP` and 14 `PENDING_CLIP`, one `APPROVED_PAYOUT`, one `PAID_PAYOUT` and two `REJECTED_PAYOUT`, **all by the REAL OWNER working live in production between 18:15 and 18:33**, plus one consequent strike. **Exactly 3 rows are mine**: `REVIEWER_CONFIG_UPDATED` written by `dev-owner-001` on the synthetic fixture.

**THE FIXTURE, NAMED AND REMOVED.** `bl833-watch-only` — synthetic, `isTestUser`, no clips, no clip accounts, no campaign assignment, **`referredById` NULL** so it cannot appear as anyone's invitee or touch the platform-fee and referral arithmetic. Created `18:01`, capability granted **through the real route** by the dev-auth owner (never the real owner's account, so no audit row claims he did something he did not), removed `18:35`: capabilities cleared, soft-deleted, suspended. Both SQL files are committed.

**NOBODY REAL WAS GRANTED THE NEW LEVEL.** The instruction was not unambiguous — the owner asked for the level to exist, not for anyone to hold it. If he grants it, **reverse it by pressing *"Watching only: stop this person watching every clip"* on their profile**; no confirmation is required.

### Gates, honestly

* **eslint confirmed present**, `v9.39.4`, so the hooks gate is a real check and not a silent no-op.
* `npx tsc --noEmit` exit **0**, `grep -c "error TS"` = **0**, run six times, the first on the **untouched** worktree so no error could be misattributed.
* `npm run build` **five times**, each written to a log with the exit code echoed by hand and **never piped through `tail`**: `BUILD1..5_EXIT=0`, the last post-commit. Prebuild clean every time: `check:prisma-bypass` **0 violations**, `check:removed-fields` OK, hooks gate **11 problems (0 errors, 11 warnings)** at the ceiling with **zero added**.
* Counted with `grep -c`, never piped through `head`. **No heredocs** were used to write any file. One shell at a time.
* `npm ci` had to be re-run once: a backgrounded first attempt was killed mid-install and left `ENOTEMPTY` on `node_modules`. An environment mishap, recorded rather than hidden.

## WHAT COULD NOT BE PROVEN, AND WHY

* **No real person has held this level.** The flow is proven end to end by real HTTP requests through the real routes as a real minted session, on a synthetic account — not by a person clicking in production.
* **Nothing was verified against production over HTTP.** Every request ran locally against the merged tree, pointed at the production database.
* **A real screen reader was not run.** DOM order, roles, focus behaviour and announcement paths are reasoned and measured; NVDA, JAWS and VoiceOver were not.
* **The page perimeter's HTTP status is not a signal**, for the reason in PART 4. It is proven on the rendered DOM instead.
* **The `updateCampaign` / `deleteCampaign` server actions were not exercised**, only read; they have no caller to exercise them through.

## WHAT THE OWNER SHOULD DECIDE NEXT

1. **Whether to grant it to anyone.** The level exists and is off for everyone. One press on a profile turns it on.
2. **`deleteCampaign` in `actions/campaigns.ts` is still `ADMIN || OWNER` and is a hard delete.** Caller-less today, and zero ADMIN accounts exist, so it is dormant rather than open. It is one line to close.
3. **Every REVIEWER can still load every `/admin/*` page** and meet an empty or refused screen. Only the watch-only holder is carved out. Narrowing the perimeter per capability is its own round.
4. **`CLIP_REVIEW` residue.** Six soft-deleted reviewer rows carry the string `CLIP_REVIEW`, which is not a valid capability key and matches nothing anywhere. Inert, and left alone.
