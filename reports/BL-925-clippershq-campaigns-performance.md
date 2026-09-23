# BL-925: the clipper campaigns page. The scroll's cost is the frosted glass; the photos now load at the size they are drawn

> **FIRST LINE, AS REQUIRED: NOTHING IS UNREMOVABLE AND NO SQL IS OWED.**
>
> This round created **no sandbox row**. It measured the page as a real clipper through a minted read-only session, and `bl925sbx-` names **0 rows at open and 0 at close** across users, campaigns, clips, audit, activity and notifications.
>
> **Real rows touched by this round: none that can be shown to be its own.** The measured clipper's user row was written twice during the round, `updatedAt` only, at 12:12:30.927 and 12:47:39.345 UTC. He also has three marketplace arrival rows at 12:47:44, 12:47:46 and 12:47:53. Section 4.6 sets out why these are his own production visit and not this session. In short:
> * This session never requested `/marketplace-v2` or any `/api/marketplace-v2` route.
> * Arrivals are deduped per server process per hour, and neither of this round's two server processes wrote one when it started.
> * 5,556 logged requests from this session (13:15:51 to 13:32:02 UTC) wrote nothing to his row.
>
> The two `updatedAt`-only writes are therefore not attributed to this round, and not proven either way. They are disclosed here rather than smoothed.

**2026-09-23.** Branch `checkpoint/BL-925`: `a0aa5358` (the change) and `7f7aa92d` (backlog). Merged to `main` as **`45f52641`**; `main` and the branch are both pushed and verified (`safe-push`: origin == local).

* **Tags:** `pre-BL-925`, `post-BL-925`, `pre-merge-BL-925`, `post-merge-BL-925`.
* **Main moved during the round.** BL-926 landed while this round ran. It changed no product code; the only conflict was `BACKLOG.md`, resolved as a union.
* **BACKLOG:** 233 entries → **235** (BL-926 and BL-925).
* **Builds:**
  * the baseline on `main`'s tree;
  * build 1 and build 2 on the branch;
  * the merge commit itself.
  * All four exit 0, with the hooks gate at 0 errors and 10 warnings (cap 11).
* **Worktree:** `C:\w\b925` removed; `ls` reports "No such file or directory".
* **Leftover sweep:** would reclaim 0 directories, all 10 candidates refused as too young or not round telemetry.
* **Not merged:** `checkpoint/BL-723` (verified not an ancestor).
* **Deploy:** requires a Railway redeploy.

**THIS SHIPS TO EVERYONE, not behind `isTestUser`.** `campaigns/page.tsx` hard-codes `isTestUser = true` (BL-477 rollout), so every clipper renders `CampaignsRedesign`.

---

## PART 0: THE MODEL SPLIT, THE CAPS, AND WHAT WAS NOT DONE

**Model split.** Opus did everything here, with no subagent between it and a measurement that drove a decision:
* designed and ran every measurement, read every figure, ruled on every cause;
* wrote the one product change and every harness;
* wrote this report.

One subagent ran: the **accessibility lead**, reviewing the image change BEFORE it was written. Its claims were checked as follows:
* **VERIFIED:** CSP `img-src` includes `'self'`; Next 16's default widths and qualities include every URL used; the image is `aria-hidden` with `alt=""`.
* **VERIFIED by render:** nothing left the tab order (PART 4).

No cheaper model was used. The brief allowed one for enumeration and profiling. I kept those in-house because the attribution work kept overturning its own intermediate results (section 5), and a summary written between the machine and the decision would have carried those errors forward.

**Caps.**
* **Database:** one connection at a time throughout (`run-select.js` and one Prisma client per script, sequential); the subagent opened none.
* **Profiling:** one Chromium, one production server, every measurement pass strictly sequential. After section 5.2 this was enforced by killing a duplicate loop.
* **Renders:** five browser contexts in parallel, one per width, in one Chromium against one server.

**Not done:**
* no vendor call and no Apify actor;
* no `prisma migrate`, no schema change;
* no money path touched, no guard touched;
* the owner-notify step was not run, because it sends through Resend and this brief forbids vendor calls (BL-924 made the same call).

---

## PART 1: WHAT THE PAGE COSTS, MEASURED BEFORE NAMING A CAUSE

### Method

**Build and user.** A production build of `main` (`103c1d3e`), served by `next start`, with the dev bypass off. The page was loaded as a **real, active, non-test clipper** (12 campaign joins, 554 clips, an installed-app user) through a minted Auth.js cookie.

**Harness:** `scripts/bl925-measure.mjs`.
* Bytes are wire bytes (CDP `encodedDataLength`).
* Paint figures come from the page's own Paint Timing.
* **ready** = every campaign card link is in the DOM.
* **TTI** = the end of the last long task before a 2 s quiet window after ready.
* Every profile loads the page **cold** (first visit, empty cache), then **warm** (second load, reported as the headline).

**Profiles:**
* **phone**: 375×812, touch, DPR 2, **4× CPU**, 1.6 Mbit down / 750 Kbit up / 150 ms RTT.
* **phone6x**: the same at **6× CPU**, the lowest-end case.
* **desktop**: 1280×900, unthrottled.

**Scroll.** Down the whole of `<main>` and back up. This shell scrolls on `<main>`, not the window: `app-layout.tsx:222`, and the document is 900 px tall.
* **Desktop:** a wheel gesture.
* **Phones:** **real finger drags** via `Input.dispatchTouchEvent`, 380 px each, one move per 16 ms.
* Recorded during it:
  * every rAF frame interval (a frame is dropped when an interval exceeds 25 ms);
  * a CDP trace with CPU per thread and self time per event;
  * a JS sampling profile;
  * Long Animation Frames;
  * the acknowledgement time of every `touchmove`.

### Load, warm and cold (medians of three runs)

| | first paint | ready | TTI | requests | wire | DOM nodes | largest single payload |
|---|---|---|---|---|---|---|---|
| **375, 4× CPU, warm** | 832 ms | 1,294 ms | 1,454 ms | 93 | 146.0 KB | 888 | `/api/campaigns`, 17.0 KB |
| **375, 4× CPU, cold** | 888 ms | 4,797 ms | | 93 | **1,433.1 KB** | | a card photo, **256.6 KB** (262,046 bytes, 800×800 JPEG) |
| **375, 6× CPU, warm** | 1,408 ms | 1,809 ms | 1,944 ms | 94 | 146 to 149 KB | 888 | `/api/campaigns`, 17.0 KB |
| **1280, warm** | 136 ms | 285 ms | 285 ms | 102 | 142.8 KB | 891 | `/api/campaigns`, 17.0 KB |
| **1280, cold** | 56 ms | 584 ms | | 101 | **2,969.1 KB** | | card photos, **2,124.6 KB = 72 percent of the page** |

**What the cold phone downloads:**
* **scripts 605 KB**: the shell's JavaScript, shared by every page;
* **photos 586.1 KB** (4 loaded; the rest are lazy);
* fetches about 145 KB: 53 fetches, of which 11 are API routes and the rest are Next's route prefetches for the sidebar.

**Caveat on 6× CPU cold.** The 6× cold figures are unreliable: in two of three runs the photos were still arriving when the 20 s settle window closed, so they fell into the warm load instead. The 4× phone is the figure for cold bytes.

### Rows (`scripts/bl925-rows.mjs`)

* A real clipper sees **16 rows: 4 live, 12 completed**.
* A live row is **35 to 42 DOM nodes**, a completed row **26**: 464 of the page's 888.
* **One row causes exactly ONE request**, its photo (16 image requests for 16 rows), and **0 API calls**.
* Components per live row: `MiniCard`, `Link`, `TypeBadge` with one icon, `CampaignTypeBadge` (marketplace campaigns only), `JoinStatus` with one icon, and the favourite `Star` button.
* **There is no BL-816-style request storm on this page.**

### The scroll, which is what he described

The phone scroll takes 2,106 px down and back up:

| | dropped frames | longest frame | p95 frame | display compositor CPU | main thread CPU | `touchmove` ack p95 |
|---|---|---|---|---|---|---|
| **4× CPU** | 35 | 33 ms | 17 ms | 3,289 ms | 6,656 ms | 36 ms |
| **6× CPU** | 125 | 50 ms | 33 ms | 3,305 ms | 11,306 ms | 46 ms |
| desktop | 2 | 33 ms | 17 ms | 1,570 ms | 406 ms | |

**What was on the main thread:**
* JS is NOT the cost: under 150 ms of JS self time in a 12.7 s phone scroll, and the main thread was idle for about 10 s of it.
* The main-thread time is frame production and input handling. The sampling profile is dominated by idle.

**Attributing it by difference** (`scripts/bl925-experiments.sh`). Each suspect was switched off at runtime (injected CSS or a listener patch, no app code changed) and the phone scroll re-measured, two runs each.

| switched off | display compositor, ms | verdict |
|---|---|---|
| nothing (baseline) | 3,375 / 2,878 | |
| **every `backdrop-filter`** | **922 / 829** | **the cost: about 70 percent** |
| only the shell chrome's blur (mobile top bar `backdrop-blur-xl`, bottom nav pill `backdrop-blur-lg backdrop-saturate-180`) | 2,082 / 2,093 | about 1.0 s of it |
| only the 2 px blur on the card badges | 2,511 / 2,431 | about 0.65 s of it |
| the scroll-driven nav hook (`use-scroll-nav-translate`, 3 listeners) | 2,839 / 3,138 | not a cost |
| the non-passive `document` touchmove (swipe drawer) | 2,853 / 2,989 | not a cost; `touchmove` ack p95 25 against 28 |
| the grayscale on completed cards | 3,211 / 3,126 | not a cost |
| the photos (hidden) | 3,206 / 3,248 | not a cost to the scroll |
| the gradients | 3,242 / 3,196 | not a cost |
| each card on its own compositing layer | 3,220 / 3,142 | no mitigation |
| the finished entrance animations released | 2,861 / 3,187 / 3,004 | no mitigation |
| chrome transitions off | 3,215 / 3,168 | not a cost |

**No infinite animation exists** (`scripts/bl925-anim-probe.mjs`): at rest and mid-scroll the only animations are the 16 one-shot `fadeUp` card entrances, all finished.

### The three biggest costs, in order

1. **The frosted glass over scrolling content.** It takes about **2.2 s of the display compositor's 3.1 s** in every phone scroll pass.
   * The mobile top bar and the bottom nav pill blur whatever scrolls under them, every frame: about 1.0 s.
   * The 2 px blur on the card badges: about 0.65 s.
   * Together more than the sum, about 2.2 s.
2. **The shell's JavaScript on a first visit: 605 KB.** This is 42 percent of a cold phone load, shared by every page and cached after the first.
3. **The card photos on a first visit.**
   * Desktop: 2,124.6 KB of 2,969.1 KB (72 percent).
   * Phone: 586.1 KB of 1,433.1 KB (41 percent).
   * They are 800×800 originals drawn into a card about 290 CSS px wide (desktop) or 343 (phone).

Everything after this fixes only these, and PART 2 says which could be fixed without changing the page.

---

## PART 2: WHAT WAS FIXED, CHEAPEST FIRST, AND WHAT STOPPED

### Cost 3, the photos: FIXED

**The file:** `src/app/(app)/campaigns/CampaignsRedesign.tsx`, the only product file changed.

**What stays exactly as it was on the card `<img>`:**
* `src` (the original);
* `alt=""` and `aria-hidden`;
* `loading="lazy"`;
* every class (including `group-hover:scale-[1.03]` and its `isPast` exception);
* no `draggable` (the strip's drag relies on that);
* both gradient overlays.

**What it gains:**
1. **`srcset`** on the optimiser `next.config.ts:142` already allows for `*.supabase.co`: `/_next/image?url=…&w=256|384|640|750|828|1080&q=75`. Only for that host; any other host keeps the old markup byte for byte.
2. **`sizes` in rem** (the accessibility lead's hard requirement), so a large default font picks a bigger file and never an undersized one:
   * live cards: `(min-width: 96rem) 25vw, (min-width: 80rem) 33vw, (min-width: 40rem) 50vw, 100vw`;
   * completed cards: `(min-width: 64rem) 24vw, (min-width: 48rem) 31vw, (min-width: 40rem) 42vw, 62vw`.
   * Never below the drawn width. The largest candidate (1080) is above every original (800), and the optimiser never upscales, so no zoom level gets less detail than before.
3. **`onError`:** an optimised failure falls back to the ORIGINAL (the `srcset` is removed), and only a second failure shows the existing letter placeholder. The optimiser can never make the page show less.
4. `decoding="async"`.

**Checks behind it:**
* **Production answers.** `GET https://clipershq.com/_next/image?…&w=384&q=75` returned 200 `image/webp`, **38,878 bytes** for the 262,046-byte original; `w=750` returned **110,602 bytes**.
* **Nothing takes the fallback today.** **All 20 stored campaign pictures return 200 `image/jpeg`**; 0 are broken.
* **The one timing difference, disclosed.** For a stored picture that is ITSELF broken, the placeholder would now appear after two failed loads instead of one. That applies to 0 campaigns today.

| cold first visit | before | after | change |
|---|---|---|---|
| phone, 4× CPU: photos | 586.1 KB | **208.5 KB** | −64 percent |
| phone, 4× CPU: whole page | 1,429 to 1,433 KB | **1,055.7 KB** | −26 percent |
| desktop: photos | 2,124.6 KB | **319.6 KB** | −85 percent |
| desktop: whole page | 2,969.1 KB | **1,161.6 KB** | −61 percent |

The phone figures are from the interleaved A/B (PART 3); the desktop figures are the sequential medians. Byte counts are deterministic, so machine load does not move them.

### Cost 1, the frosted glass: STOPPED AND REPORTED, NOT SHIPPED

Removing the blur is the only measured way to cut the scroll's main cost, and it changes how the page looks:
* The top bar and the bottom nav lose their frosted glass on every clipper page (the chrome is sitewide).
* The card badges lose a 2 px blur behind a 60 percent black pill.

The brief says a fix that changes what the page shows is reported, not shipped. Two mitigations that would have kept the look were tested and bought nothing:
* **each card on its own layer:** 3,220 / 3,142 ms;
* **the entrance animations released:** 2,861 / 3,187 / 3,004 ms.

What the owner's option buys, measured as three runs on the same build at the same time of day (no blur, rAF instrumentation on):

| | dropped frames today | without the blur | display compositor |
|---|---|---|---|
| phone, 4× CPU | 35 | 17 | 3,289 → 1,296 ms |
| phone, 6× CPU | 125 | 82 | 3,305 → 1,314 ms |
| phone, 4× CPU, chrome blur only removed | 35 | 32 | 3,289 → 1,954 ms |

**Caveat, stated honestly.** These are headless Chromium with software compositing. A real phone blurs on its GPU, so its absolute cost differs; the ranking should not.

### Cost 2, the shell JavaScript: STOPPED AND REPORTED, NOT SHIPPED

605 KB is the app shell every page shares. Cutting it is a bundle round across the whole app, not a change that "cannot change behaviour" on one page.

---

## PART 3: THE PHONE, THE INSTALLED APP, AND THE PAN

### The fair before and after: ONE build, the two arms interleaved (`scripts/bl925-ab.sh`)

* **Arm "before":** refuses the two attributes this round adds (`srcset` and `sizes`, at `setAttribute` and at the property setter). That is `main`'s image loading exactly, **verified**: 0 of 16 images carried `srcset` in that arm, and 16 of 16 in the other.
* **Rounds:** three, alternating, on the phone profiles.

| phone | arm | dropped frames | longest | display compositor | `touchmove` p95 | TTI (warm) | cold wire | cold photos |
|---|---|---|---|---|---|---|---|---|
| **4× CPU** | before | 1 / 2 / 1 | 33 ms | 2,239 ms | 25 ms | 1,264 ms | 1,429.0 KB | 586.1 KB |
| **4× CPU** | after | 2 / 1 / 2 | 33 ms | 2,151 ms | 21 ms | 1,254 ms | **1,055.7 KB** | **208.5 KB** |
| **6× CPU** | before | 4 / 9 / 5 | 33 ms | 2,250 ms | 25 ms | 1,628 ms | 1,433.3 KB | 586.1 KB |
| **6× CPU** | after | 6 / 7 / 6 | 50 ms | 2,189 ms | 21 ms | 1,585 ms | **1,053.3 KB** | **208.5 KB** |

**Does the scroll hold its frame budget?**
* **At the 95th percentile, yes, on both arms:** p95 frame 17 ms at 4× and at 6×.
* **The worst frames are 33 to 50 ms, and this change does not move the scroll.** The photos were never a scroll cost (hiding them saved nothing).
* **Under load the page drops real frames.** When this machine was busier (the sequential runs), the same page dropped 35 frames at 4× and 125 at 6×. That is the low-end phone doing anything else, and the frosted glass is what makes it worse.

### The installed app

* **Production is already right.** `manifest.json` in production says `"start_url": "/campaigns"` (BL-829).
* **Installs that predate it may still start at `/dashboard`.** Measured today on the phone profile, a `/dashboard` launch reaches the cards in **1,894 to 1,965 ms against 1,294 ms**, and costs **166 to 168 KB against 146 KB warm** (1,460 to 1,463 KB against 1,433 KB cold).
* **So it costs about 0.6 s and 20 to 30 KB today**, against BL-828's 4,981 ms and 979.5 KB. BL-829's guard holds: `/api/clips/mine` is not fetched.
* **How many people.** At most **76**: installed clippers whose install (or, for the 291 with no grant stamp, whose account) predates 2026-08-25 18:00 UTC and who logged in within 30 days (356 before the fix in all). iOS and Android cannot be told apart, because no platform is recorded, and Android re-reads its manifest. So the true number is lower, and cannot be established from the data.
* **Not a top-three cost, so not changed.**

### The pan

**The pan is 0 px at 320, 375, 414, 1280 and 1440, in every state, before and after.** It was measured by scrolling the document and `<main>` sideways and reading back where they landed, never from `scrollWidth`.

---

## PART 4: PROOF THAT NOTHING CHANGED EXCEPT THE SPEED

### 4.1 The page says the same things

`scripts/bl925-render.mjs` plus `scripts/bl925-compare.mjs`.

**Method:**
* **Widths:** 320, 375, 414, 1280 and 1440, five contexts in parallel (cap 5), with `window.innerWidth` and the URL read back.
* **States:** default; scrolled to the end; Type = Song; Type = App.
* **What is captured, in DOM order:**
  * every campaign row's visible text, accessible name, favourite button name and `aria-pressed`, and screen-reader-only text;
  * every heading and every paragraph;
  * the polite status line;
  * every image's `src` and `alt`;
  * the keyboard tab order.

**Results:**
* **Same build, both arms back to back at 13:24 UTC: 185 comparisons, 0 differences**, pan 0 everywhere.
* **The earlier sequential pair (before on `main`'s build, after on the branch's): 15 differences, all one kind.** Two live spend figures moved between the renders:
  * ANGIE BROWN $4.66 → $9.87;
  * Zhus Edit $1,547.88 → $1,547.93.
  * That is the production cron's 13:00 UTC earnings writes landing in between. Every other field was identical, and no figure is computed by anything this round changed.
* **States asserted in words, at every width:**
  * "Showing 4 campaigns" (default);
  * "Showing 2 campaigns" (Song), headings Active and Completed;
  * "Showing 1 campaign" (App), headings Paused and Completed;
  * 4 live and 12 completed rows;
  * no install sheet on screen (asserted in the DOM, not just the picture).

### 4.2 Tab order and targets

* **The tab order is identical before and after at every width:** 13 stops at 320, 375 and 414; 24 at 1280 and 1440.
* **Nothing left it and nothing joined it.** The photo is `aria-hidden` and not focusable, and this round touched no control.
* **Pre-existing, logged, not changed:** 8 of the 13 phone tab stops are under 44 px tall. The favourite star is `h-9 w-9`, 36 px.

### 4.3 Accessibility review

**Accessibility lead: GO**, reviewed before the code was written. Its four hard requirements are all met:
1. rem breakpoints;
2. never undershoot the drawn width;
3. the fallback applies to optimised images only and clears `srcset` itself;
4. every other attribute, class and wrapper byte-identical.

Its advisory, which is pre-existing and not changed: an image that fails before hydration never fires `onError`.

### 4.4 Money

* **The six protected files are byte-identical by blob OID:** `git rev-parse pre-BL-925:<file>` equals `HEAD:<file>` on the merge commit.

| file | blob |
|---|---|
| `clip-earnings-writer.ts` | `80418a18` |
| `earnings-calc.ts` | `00410634` |
| `balance.ts` | `67c30c89` |
| `tracking.ts` | `672d2ab3` |
| `clip-earnings-invariant-middleware.ts` | `61cef393` |
| `money-decimal.ts` | `ef5cdae7` |

* `tracking.ts` is in no diff.
* **Full population, open (12:28:45 UTC) and close (13:33:03 UTC)**, `scripts/sandbox/bl925-invariants.ts`:
  * F1 earnings invariant on every live clip (10,338);
  * F2 maker leg invariant;
  * F3 no double pay (agency, maker, platform, posts);
  * **F4 no campaign over budget**, counting both v2 aggregates and the owner's cut;
  * **F5 paid is final for the maker and for the v2 poster, asked separately**;
  * **F6 ANGIE BROWN found by name, one row, $2,700, ACTIVE**;
  * G1 **both reconciliation forms**, 0 rows;
  * **never decrease** across every real clip between open and close.
  * **All pass at 0 violations.**
* **The shared money tables' fingerprints MOVED** between open and close (clip earnings, agency, v2 legs), because the production cron ticked at 13:00. Every clip that moved ROSE.
* **Identical at open and close:** clip status, campaign state and payout state. Clips 10,338 → 10,338.

### 4.5 Guards

* **All 21 prebuild guards ran and passed** in build 1, build 2 and the merge build, including `check:cron-wiring`, `check:css-tokens` and `check:page-titles`, and `check:schema-drift` against the live database.
* **Hooks gate:** 0 errors, 10 warnings, cap 11. eslint 9.39.4 was confirmed present first.
* **Baseline `tsc`** on `main`'s tree: 0 errors; on the branch: 0 errors.
* **This round touched no guard**, so none was owed a failing demonstration.

### 4.6 The measured clipper's own rows

`H2` of the invariant script **FAILED** at close, on two of five checks:
* his user row fingerprint;
* his activity count.

**The evidence that it is his own use of production, not this round:**
1. **His three new activity rows are marketplace arrivals** (`mkt2.arrive` 12:47:44.600, `mkt2.campaigns` 12:47:46.622, `mkt2.catalogue` 12:47:53.419), two and seven seconds apart, the shape of a person walking in. `mkt2.arrive` is written only by `src/app/(app)/marketplace-v2/page.tsx:54`; the other two only by marketplace API routes.
2. **This session never requested `/marketplace-v2` or `/api/marketplace-v2`.** 5,556 logged requests; its only marketplace requests were 108 Next prefetches of the old `/marketplace` route.
3. **`recordArrival` dedups per server process per hour** (`activity-record.ts:175`). This round's servers started at about 12:12 and 13:15 UTC and wrote no arrival at either time.
4. **His row's `updatedAt` moved at 12:47:39.345**, five seconds before those arrivals. No dated column changed with it.
5. **After request logging began at 13:15:51**, 5,556 requests by this session left his row untouched.
6. **The earlier write at 12:12:30.927 remains unexplained.** No auth path writes on a session refresh: every `user.update` in `auth.ts` is sign-in, sign-up or owner promotion. Single-user writes happen across the platform every few minutes (10 in the hour measured).

**Not attributed to this round; not proven either way.**

---

## PART 5: WHAT WENT WRONG IN THE ROUND, DISCLOSED

1. **Synthetic touch scrolling moved nothing.** `Input.synthesizeScrollGesture` with the touch source measured **0 px even on a bare control page** (`scripts/bl925-touch-control.mjs`), so my first phone scroll figures were of a page that never scrolled. They were replaced by real `Input.dispatchTouchEvent` drags (285 px moved for a 300 px drag, verified).
2. **Two experiment loops ran at once for part of the first set.** `TaskStop` stopped the wrapper, not its loop. Every figure from that period was discarded, both loops were killed by PID (8 processes, all mine), and the set was rerun alone.
3. **The "no animations" experiment was invalid.** It appeared to save 40 percent. It did so by making the 16 cards INVISIBLE: they rest at `motion-safe:opacity-0` and are held visible by a `forwards` fill, so switching animations off drew nothing. The corrected variant (`nofill`, opacity forced to 1) saves nothing. The finding was withdrawn.
4. **My sequential before/after overstated a scroll win that does not exist.** Measured one after the other on a shared machine, the phone dropped 35 frames before and 2 after. **Interleaved on one build, it drops 1 to 2 in both arms.** The difference was machine load. The byte savings are deterministic and stand; the scroll claim was never made.
5. **The `/dashboard` measurement failed once.** Git Bash rewrote `PAGE_PATH=/dashboard` into a Windows path. It was rerun with `MSYS_NO_PATHCONV=1`.
6. **The harness's own rAF loop inflates main-thread time.** It forces a main frame every vsync. Main-thread figures are therefore quoted from runs without it (`NORAF=1`), and dropped frames from runs with it.
7. **A new harness bug, caught before it mattered.** `networkidle` never arrives on this shell (30 s heartbeat, 60 s polls), so the first harness waited up to 300 s per load. It was capped at a fixed 20 s settle.

---

## OWNER DECISIONS, MEASURED AND NOT MADE HERE

1. **The frosted glass.** Remove or soften `backdrop-blur` on the mobile top bar (`app-layout.tsx`, `backdrop-blur-xl`) and the bottom nav pill (`BottomNav.tsx`, `backdrop-blur-lg backdrop-saturate-180`), and the 2 px blur on the card badges (`CampaignsRedesign.tsx` and `CampaignFlowNotice.tsx`).
   * **Measured, all together:** display compositor about 3.1 s → 0.9 s per phone scroll; dropped frames 35 → 17 (4×) and 125 → 82 (6×).
   * **Chrome alone:** about 1.0 s.
   * It is a look decision, and it is sitewide for the chrome.
2. **The shell JavaScript, 605 KB on a first visit.** A bundle round, not a page round.

## LEFT FOR LATER, WITH MEASUREMENTS

1. **Pre-BL-829 installs** starting at `/dashboard`: about 0.6 s and 20 to 30 KB per cold launch; at most 76 active people; platform unknown.
2. **The swipe drawer's non-passive `document` touchmove:** within noise today (`touchmove` p95 23 to 25 ms passive against 28 to 29 ms). Not worth the drawer risk.
3. **8 of 13 phone tab stops are under 44 px** (the favourite star, 36 px). Pre-existing.
4. **The accessibility lead's advisory:** an image that fails before hydration never fires `onError`, so its square stays empty. Pre-existing, on both paths.

**IN ONE LINE, THE THROTTLED PHONE (4× CPU, 1.6 Mbit, interleaved on one build), BEFORE → AFTER:** cold bytes **1,429.0 KB → 1,055.7 KB**, requests **93 → 92**, DOM nodes **888 to 891 → 888 to 891** (unchanged; the notification badge varies by 3 nodes), time to interactive **1,264 ms → 1,254 ms**, dropped frames on the scroll **1 → 2** (per 2,106 px down and back, median of three; unchanged, since the scroll's cost is the frosted glass, reported above).
