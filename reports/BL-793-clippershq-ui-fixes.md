# BL-793 — four UI fixes, and the render blocker three rounds could not pass

**2026-08-12 · DB `now()` = `2026-08-12 16:17:20.501083+00` (first read) to `16:48:03.699036+00` (last) · BUILD.**
Branched from **`origin/checkpoint/BL-791`** @ `3970ff7c`, which already contains **BL-788** (partner scope) and **BL-790** (capability gate) as ancestors, both verified by `merge-base --is-ancestor`. Branch `checkpoint/BL-793`, isolated worktree `C:/bl793`, `node_modules` never junctioned, removed at the end. No other worktree existed at start and none was touched. Every database read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted; no wallet address read or printed.

## THE FIRST LINE

> **Everything rendered. The blocker that stopped BL-791 and BL-792 was TWO layers, not one, and both are fixed: every screen in this report was seen in a real browser at 320, 375, 414, 1280 and 1440 pixels, with the mobile drawer open at the three narrow widths, and measured rather than eyeballed.**

**Two of the brief's premises turned out to be wrong, and both are reported rather than worked around: top earners already updates live, and the reviewer controls were already on the profile page.** What was actually missing is built below.

## PART 5 FIRST — THE BLOCKER, BECAUSE NOTHING ELSE COULD BE PROVEN WITHOUT IT

BL-791 and BL-792 both stopped at the same sentence: *the dev bypass reaches the API but not the page guard*. **It was two independent layers.**

**Layer one, the environment.** `DEV_AUTH_BYPASS` gates the server and `NEXT_PUBLIC_DEV_AUTH_BYPASS` gates the client (`dev-auth-provider.tsx:38`). Both are **true** in `.env.development.local` and both are **false** in `.env`. Next.js loads `.env.development.local` only in development, so a production-mode run (`npm run build` then `npm start`) keeps the server bypass working through `getSession()` while the client flag falls back to `false`, `isAuthenticated` goes false, and `app-layout.tsx:295` pushes to `/login`. **That is exactly the reported symptom.** Running `next dev` loads the right file. Result, measured: `GET /admin/users/<id>` → **HTTP 200, 52,881 bytes**, not a redirect.

**Layer two, which nobody had reached, because layer one hid it.** With the page now loading, the reviewer block still did not exist in the DOM. `admin/users/[id]/page.tsx:4,39` read a **raw `useSession()`**, which returns null under the bypass, so `currentUserRole` was undefined, `isOwner` was false, and the whole block at `:770` never rendered. The repo already documents this exact trap and already ships the fix: `src/hooks/use-effective-session.ts`, whose own header calls it *"drop-in replacement for `useSession()` reads of role/caps"* and describes the failure as *"a TEST HARNESS gap, not a production bug"*.

**The change is three lines and production behaviour is unchanged**, because outside dev-bypass the hook returns NextAuth's session verbatim with no extra fetch and no caching. `session` was used on that page for nothing else but these two derivations, checked before swapping.

**What I did: fixed the blocker, both layers. Nothing was worked around and no screen below is claimed unseen.**

## PART 1 — THE SIDEBAR FOOTER

### The premise was wrong in a way that matters

**This was never a responsive problem.** The `<aside>` is `w-60`, a flat **240px at every breakpoint** (`sidebar.tsx:560`), on desktop and inside **both** mobile drawers alike; the drawer wrappers are wider but the aside does not stretch. So the wrap at 1440 was the *same* wrap as at 320, and any breakpoint-keyed text swap would have fired on a dimension unrelated to the overflow.

### Measured before, in the browser, not estimated

| row | label room | label needs | verdict |
|---|---|---|---|
| Discord | **109px** | **110px** | **short by ONE pixel** |
| Download App | **91px** | **97px** | short by six |

Both rows measured **66px tall**, i.e. two lines each, against ~54px for one.

### The fix: spend pixels, keep the words

**The exact wording shipped is unchanged: `Join our Discord` and `Download App`.** No shortening was needed and none was done. Recovered 12px per row, all of it from chrome: `gap-3` → `gap-2.5`, `px-3` → `px-2.5`, and the **decorative** (`aria-hidden`) icon tile `h-8 w-8` → `h-7 w-7`. Only then was `whitespace-nowrap` added, because it converts wrapping into *overflow* and this footer has no `overflow-hidden`, so it is safe only once the label provably fits.

**Explicitly not done, and why:** no `truncate` (the accessible name would still say the full string while the eye read a fragment, so a speech-input user could not say what they can see, and the brief forbids clipping); no `aria-label` differing from the visible text (WCAG 2.5.3); no `hidden md:inline` word splitting (the accessible name would change with viewport). Two small repairs while in there: the bare Discord text node is now wrapped in a span, and the leading space moved **inside** the `sr-only` "(opens in a new tab)" because JSX was stripping it and the name computed as `Join our Discord(opens in a new tab)`.

### Verified at all five widths, drawer open at the narrow three

| viewport | drawer | aside | label height | row height | clearance to right edge |
|---|---|---|---|---|---|
| **320** | **open** | 240px | **20px, one line** | 54px | 48px / 61px |
| **375** | **open** | 240px | **20px, one line** | 54px | 48px / 61px |
| **414** | **open** | 240px | **20px, one line** | 54px | 48px / 61px |
| **1280** | n/a | 240px | **20px, one line** | 54px | 48px / 61px |
| **1440** | n/a | 240px | **20px, one line** | 54px | 48px / 61px |

Both labels also sit **65px and 78px inside** the aside's right edge, so nothing clips and nothing overflows. **BL-739's touchmove carve-out is untouched**: the footer is deliberately outside `[data-drawer-scroll]`, taps are unaffected by the `preventDefault`, and **no `data-no-swipe` was added**, which BL-739 explicitly rejected for this area because it would kill swipe-to-close across most of the drawer.

## PART 2 — THE NUMBER. IT IS A PERCENTAGE, AND THAT IS PROVEN

**Where it appears: exactly two places**, `ProgressPremium.tsx:374` (completed milestone) and `:376` (not yet reached), rendering `+{milestone.bonus}` with no unit.

**Four independent proofs it is a percent, established before touching anything:**

1. **The server field is literally named `bonusPercent`** — `earnings-calc.ts:35-42`, `DEFAULT_STREAK_BONUSES`, with the identical values, consumed as a percent in the earnings maths and capped at `MAX_BONUS_CAP`.
2. **The tooltip on the very same cell already said it** — `:379`, `Day ${n}: +${milestone.bonus}% streak bonus`.
3. **The legend eight lines below already renders `+{m.bonus}%`** — `:403`.
4. **The pre-BL-404 version of this same grid printed the `%`** — `progress/page.tsx:338,344`.

**So this is a restored regression, not an asserted unit.** The `%` was dropped when the grid was ported into `ProgressPremium.tsx`.

**The one other bare `+N` in clipper-visible UI was checked and deliberately LEFT ALONE:** `tracking-modal.tsx:343` renders `+{formatNumber(growth)}`, computed at `:329-330` as `snap.views - prevViews`. **That is a view-count delta, not a percentage**, it sits under a "Views" column header, and adding a `%` there would have been the exact mislabelling the brief warned about.

**Two further repairs on the same surface.** The grid is `aria-hidden`, so its `title` tooltips reach nobody and the `sr-only` summary at `:363` was the only path for assistive technology — and it named the days without ever naming the unit. It now reads *"Milestone bonuses, in percent added to what you earn, at 3 days plus 1 percent, 7 days plus 2 percent…"*. And the today-cell ring used `ring-offset-[var(--bg-page)]`, **a variable that does not exist anywhere in `globals.css`**; Tailwind registers the ring-offset property with an initial value of `#fff`, so it was painting a **white halo**. Offset now against `--bg-card`.

### Restoring the `%` broke the narrowest layout, and that was caught and fixed

At **320px the milestone cell is only 18px wide** and `+5%` needs **21px**: three of five cells clipped. The grid is now **`grid-cols-6` below `sm` and `grid-cols-10` from `sm` up**, which gives **34px per cell at 320px**. Re-measured at all five widths after the change: **zero cells clipping, all five milestones rendering `+1% +2% +3% +5% +7%`**, six columns at 320/375/414 and ten at 1280/1440.

## PART 3 — TOP EARNERS. IT ALREADY UPDATES, AND THE OWNER'S IMPRESSION IS WRONG

**Established first, file:line, before changing anything.** It is **LIVE**, not cached and not hardcoded:

• `src/app/api/gamification/route.ts:6` — `export const dynamic = "force-dynamic";`
• `route.ts:38-47` — a real Prisma query on every request: `db.user.findMany({ where: { totalEarnings: { gt: 0 }, OR: [{ role: "CLIPPER" }, { canActAsClipper: true }] }, orderBy: [{ totalEarnings: "desc" }, { totalViews: "desc" }], take: 10, select: { name, username, totalEarnings, totalViews } })`
• Repo-wide: **zero** `unstable_cache`, **zero** `export const revalidate`, no snapshot table, no cron writer, no hardcoded array in code.
• Client refetches on mount and on `sse:clip_updated` / `sse:earnings_updated` (`progress/page.tsx:80,90-91`).

### Proven by rendering it against the database, name by name, redacted

The board was rendered as a clipper and compared to a live `SELECT` taken minutes earlier. **It matched row for row:**

| rank | rendered | live DB | match |
|---|---|---|---|
| 1 | `ku***` · $2,293.78 · 5,662,231 views | `ku***` · 2293.78 · 5662231 | ✓ |
| 2 | `al***` · $993.88 · 4,092,469 | `al***` · 993.88 · 4092469 | ✓ |
| 3 | `.a***` · $569.22 · 1,242,427 | `.a***` · 569.22 · 1242427 | ✓ |
| 4 | `ka***` · $428.23 · 989,450 | `ka***` · 428.23 · 989450 | ✓ |
| 5 | `gr***` · $350.57 · 12,322,201 | `gr***` · 350.57 · 12322201 | ✓ |
| 6 to 8 | `fz***` $246.96 · `ab***` $241.43 · `du***` $237.52 | identical | ✓ |

**No change was manufactured. The mechanism was already correct.**

### But a stale trap DOES exist, and it is reported rather than silently removed

`gamification_config` holds one row keyed `leaderboard`, hand-typed by the owner through `admin/settings`, containing **three names and figures from a past era**: `ymirfritz0296` $1,325, `reaper420_` $622, `grwld.09` $411. `route.ts:48-51` serves the live board only `if (top.length > 0)`, and `:66-68` swallows any query error — so **whenever the live query returns zero rows or throws, clippers silently see that stale blob instead, with no visual difference whatsoever**. It is **not** being served today (the live query returns 10). Note `grwld.09` appears in both: the blob says $411, the truth is $350.57.

**This is a product decision, not a bug to rip out this round** (its own comment says it exists so a fresh database shows a populated list). **Recommendation for the owner: clear that row.** The platform is no longer fresh, and the fallback's only remaining effect is to substitute stale money figures for real ones without telling anyone.

### What it exposes — BL-531 clean

Exactly **three** fields per other clipper reach the browser (`route.ts:55-64`): `name` (username, falling back to display name, then the literal "Clipper"), `earnings`, `views`. **No `userId`, no avatar, no profile link.** Grepped for `ownerCpm`, `agencyFee`, `clientName`, `aiKnowledge`, `agencyEarning`, `marketplacePlatformEarning`, `feePercent`: **zero hits** across the route, the component and the page. The route is a four-field `select` allowlist rather than a spread, so it is structurally immune to the BL-531 leak class; it achieves BL-531's outcome by a stronger mechanism than the `OWNER_SIDE_FIELDS` strip, which is campaign-shaped and correctly not imported here.

**Three filter gaps found and reported, none of which bites today:** the query has no `status: "ACTIVE"` filter (a banned user could rank), no test-account exclusion, and `canActAsClipper` could surface a non-CLIPPER despite the code comment claiming otherwise. **Checked live: all ten current entries are `CLIPPER`, `ACTIVE`, `isTestUser=false`, `canActAsClipper=false`.** Latent, not live.

**Two accessibility defects were fixed without touching the data path:** `role="list"` added (Tailwind v4 Preflight sets `list-style:none` on every list, which makes WebKit drop the list role, so VoiceOver announced no list and no position), `display:flex` moved off the `<li>` onto an inner div for the same reason, and an `sr-only ", earned "` added before the currency, which previously read as a naked amount straight after a view count. Verified rendered: `<li>` computes `display: list-item` and a row announces *"Rank 1: ku***, 5,662,231 views, earned $2,293.78"*.

## PART 4 — THE REVIEWER CONTROLS

### The premise was wrong: they were already there

`ReviewerCapabilityChecklist` is imported at `admin/users/[id]/page.tsx:23` and **rendered at `:792`**, and that is its only render site in the repo. **What makes it read as unreachable is a stack of four gates**, all deliberate: owner-only and not on your own profile (`:770`), collapsed by default (`useState(false)` at `:47`), and positioned last on a very long page. On top of that sat the `useSession` blocker in PART 5, which meant that under the dev bypass it genuinely never rendered at all.

### What was actually missing, and is now built

**The live numbers, folded into the existing owner-only GET** (`reviewer-config/route.ts`) rather than added as a second fetch, so the component gains no extra request and **no new hook**. The server returns `reach: { invitees, clips }`, counting users whose `referredById` is this person and their non-deleted clips, and returns **`null` rather than zeros** if the count cannot be taken.

Rendered as **one `<p role="status" aria-live="polite" aria-atomic="true">`, in the DOM unconditionally**, with four branches. `aria-atomic` matters: without it a screen reader may announce only the changed text node, which is the numeral, putting the bare-zero failure back through the side door.

| state | what the owner reads |
|---|---|
| loading | "Checking who this person has invited." |
| **count failed** | **"Could not check who they invited. This is not zero, it is unknown."** plus advice not to switch the scope on yet |
| **zero invitees** | **"They have not invited anyone yet, so with 'Only clippers they invited' turned on they would see no clips today."** |
| invitees but no clips | "They invited 3 people. None of those people have clips right now, so with…" |
| ordinary | "They invited 3 people, covering 12 clips they could review." |

Singular and plural forms are handled. **Zero never renders as a numeral and never as an empty space**, which is the whole point: zero invited plus the scope switched on is a reviewer with a permanently empty queue, and that is the configuration the owner is one click from creating.

**What a reviewer can never reach**, added as a plain list next to the grant, and worded as fact rather than promise because BL-791 established every line by direct request: payouts and unpaid payouts, agency earnings, clipper accounts and the full user list, the audit log, and the owner's own ratification queue.

**The plain-words explanation of what granting does already existed** (BL-788, `:334-355`) and is correct: they judge only clips from clippers they invited, their decision is a recommendation until the owner agrees, and they see the outcome afterwards. It was left alone.

**The full-authority control was left structurally alone and is correct as built**: a `<button>` with `aria-expanded`, **not** a `role="switch"` (which would announce `aria-checked="false"`, be activated, and still report false), opening an inline disclosure rather than a lying `aria-modal`, with the typed phrase and `aria-disabled` (never native `disabled`, which would drop the button out of the tab order and out of form quick-nav so a blind admin who mistyped one character could never find out why).

### Two real defects found and fixed

**One, a control that misreported its own state.** The GET handler at `:128-137` set five fields and **never called `setInvitedOnly`**, although the API has always returned `reviewerScopeInvitedOnly`. So **"Only clippers they invited" rendered UNCHECKED on every page load regardless of what was stored**, and the owner's first click sent `invitedOnly: true` when it was already true. One missing line, on the exact setting this round is about.

**Two, a silent failure on the money-granting control.** A wrong typed phrase hit `if (!phraseMatches || saving) return;` — focus stayed on the button, and the mismatch text is `aria-describedby` on the *input*, which no longer had focus and is not a live region. **A screen reader user heard nothing at all, and could not tell a rejected phrase from a dead button.** Focus now moves to the input and selects it; the input carries `aria-invalid` and the mismatch description, so arriving there states what is wrong. This works identically on the first attempt and the fifth, which a `role="alert"` would not, because it fires on insertion and unchanged text does not re-fire. The phrase itself is now `select-all` selectable text so it can be copied.

### Proven live on the changed tree

```
REVIEWER /api/payouts                -> 403      mode=LIVE, no phrase      -> 400
REVIEWER /api/admin/agency-earnings  -> 403      mode=LIVE, wrong phrase   -> 400
REVIEWER /api/accounts               -> 403      EARNINGS_VIEW on CLIPPER  -> 400
REVIEWER /api/admin/users            -> 403
REVIEWER /api/admin/payouts/unpaid   -> 403      GET now returns
REVIEWER /api/admin/audit-log        -> 403        "reach":{"invitees":0,"clips":0}
REVIEWER /api/admin/reviewer-queue   -> 403
```

**The five server protections all still hold, and four of them by construction**: `api/clips/route.ts`, `api/clips/[id]/review/route.ts`, `reviewer-capabilities.ts` and `reviewer-audit.ts` are **byte-identical to the BL-791 base** — this round never touched them. The invitee scope (`clips/route.ts:325`, `referredById: session.user.id`), the fail-closed default, the generic 404 on write (`review/route.ts:151`), BL-788's typed phrase and BL-790's capability gate are all intact, the last three re-measured above. **BL-776's evidence panel is still mounted at `admin/clips/page.tsx:2050`.**

## PART 5 — WHAT WAS RENDERED, AND WHAT WAS MEASURED

Every screen below was seen. **The partner used for the profile page is the real one named in the brief, whose live state is `REVIEWER`, `TRIAL`, `referralCode` NULL, `invitedOnly` false, and genuinely zero invitees** — so the zero state in this report is the true state of the real account, not a contrivance.

| screen | 320 | 375 | 414 | 1280 | 1440 |
|---|---|---|---|---|---|
| Sidebar footer, **drawer open** at the narrow three | one line | one line | one line | one line | one line |
| Streak milestone cells | `+1%`…`+7%`, 0 clipping | 0 clipping | 0 clipping | 0 clipping | 0 clipping |
| Top earners list | `role=list`, `list-item`, no overflow | same | same | same | same |
| Reviewer panel + **zero-invitee state** | renders, no overflow | renders | renders | renders | renders |

**The full-authority contract was exercised in the browser without granting anything:** the trigger reported `aria-expanded="true"`, the submit reported `aria-disabled="true"` with native `disabled=false`, and after submitting a deliberately wrong phrase `document.activeElement` **was the input**, with `aria-invalid="true"` and two ids in `aria-describedby`. **Mode stayed TRIAL. Nothing was written.**

## PART 6 — WHAT CHANGED, FOR THE OWNER TO GO AND LOOK AT

**Bottom left of every clipper's sidebar.** "Join our Discord" and "Download App" now each sit on one line instead of wrapping onto two. The words are exactly the same as before; the boxes around them are slightly tighter. Same on a phone with the menu open.

**The Progress page, the streak calendar.** The little milestone squares used to say "+1" with nothing after it. They now say "+1%", so a clipper can tell it is a percentage added to what they earn. On a small phone the calendar is now six squares across instead of ten, because ten made the "%" too cramped to read.

**The Progress page, Top earners.** **Nothing was changed about how it updates, because it was already updating.** It reads live from the database on every load, and this round proved that by comparing what the page showed against the database at the same moment: same eight people, same order, same figures. **One thing worth your attention:** there is an old hand-typed list of three names and amounts still saved in settings, and if the live list ever comes back empty the page will quietly show that old list instead, with nothing on screen to say so. Worth deleting.

**An admin user's profile page, Reviewer Permissions.** The panel was always there, but it is owner-only, closed by default and right at the bottom, so it is easy to miss. It now shows, before you grant anything, **how many people that person invited and how many clips that covers**. If they have invited nobody it says so in a sentence rather than showing a bare zero, and if the number cannot be checked it says that too instead of pretending it is zero. Underneath there is now a short list of **what a reviewer can never reach**: payouts, agency earnings, clipper accounts, the audit log, and your own approval queue. The "Only clippers they invited" tickbox now shows its real saved setting, which it previously did not.

## THE ACCESSIBILITY REVIEW, INCLUDING WHAT IT CAUGHT IN MY OWN WORK

Seven specialists were briefed **before** any code was written and then run again **against the actual diff**. The second pass found a serious defect in my own change, and it is reported here rather than buried.

**N1, serious, in the fix I was most confident about.** My first attempt at the wrong-phrase problem moved focus to the input and claimed in a comment that it "works identically on the first attempt and the fifth". **That was the exact inverse of the truth.** Pressing Enter from inside the field, which `enterKeyHint="done"` actively encourages, leaves focus where it already is, so `.focus()` is a specification no-op that fires no event and announces nothing. And on the first press through the button, `setPhraseAttempted(true)` is batched and commits *after* `focus()` runs, so at focus time `aria-invalid` was absent and the error node was not yet mounted. **My browser check could not see this**, because reading `document.activeElement` and `aria-invalid` afterwards inspects the post-commit DOM that a screen reader never saw.

**Fixed properly, with two mechanisms because neither is sufficient alone:** the mismatch paragraph is now `role="alert"` **keyed on a failure counter**, so every failed attempt genuinely remounts it, and insertion is what makes an alert speak. Focus still moves to the field, but it is no longer relied on to announce. **Re-verified in the browser across three consecutive failures: a new alert node on attempt 1, 2 and 3** (`alertIsNewNode: true` each time), focus on the input, `aria-invalid="true"`, and mode still TRIAL with nothing granted.

**Four smaller findings against my diff, all fixed:** the callout box I built to be noticed used `border-accent/40`, compositing to **1.96:1** and therefore invisible, now `/80` at 3.95:1; the "What they can never reach" list I authored lacked the `role="list"` I had just argued for on the leaderboard; my rewritten `sr-only` line could announce "75 of the last 60 days completed" because `streak` is uncapped while the grid draws 60 cells, now `Math.min`; and my `focus-visible:outline-transparent` forced-colors fallback was **inert** in Tailwind v4 and has been removed rather than shipped as dead code, since the unlayered global rule at `globals.css:202` already covers it.

**One genuine AA failure on a line I edited, fixed:** the completed milestone cell used `text-white` on the accent gradient at **3.40:1** for 10px extrabold text. It now uses the app's established dark-on-accent ink, the same literal the sidebar's +2% pill uses for the same reason.

**Confirmed correct and not re-litigated:** the leaderboard list semantics on all three counts, the sidebar labels and accessible name (including that both `sr-only` spans are absolutely positioned and consume none of the 12px recovered), and the whole existing full-authority contract.

**Found, pre-existing, NOT fixed this round, and the owner should see them.** These are outside a four-fix display round but two are serious:

• **"Keep things as they are" does not cancel.** Escape is guarded by `saving`, the Cancel button is not, so pressed mid-flight the panel closes and returns focus **while the PATCH completes and grants full authority**. On this control that is the worst available failure, and it is arguably more urgent than anything in my diff.
• **Every save throws focus to `<body>`**, because `disabled={saving}` on the focused checkbox unfocuses it per specification. BL-788 already solved this correctly for the mode trigger with `aria-disabled`; the in-flight checkboxes were never migrated.
• The closed mobile drawers leave roughly 22 focusable elements in the tab order, v1 by transform alone and v2 by `aria-hidden` without `inert`, which is an automated axe failure. **Correctly deferred**, since the fix needs focus restoration and that needs an effect, which this round's hooks ceiling forbids.
• "Download App" is a focusable control that silently does nothing on desktop browsers without a native install prompt.
• Five duplicate link names for a reviewer who can also act as a clipper, and no `aria-current` on any nav item.

**One finding worth acting on outside the code.** `--bg-page` is **undefined repo-wide** yet has roughly 35 consumers across 27 files, and it still paints a white halo at three other sites. The root cause is that **`CLAUDE.md` and `docs/runbooks/domain-and-ui.md` both list `--bg-page` as a canonical token**. The rulebook is generating the bug. I fixed the one instance on my surface and am reporting the class rather than silently widening this round.

## GATES, HONESTLY

`npm ci` **exit 0**. `npx prisma generate` **exit 0**, run before every tsc because `npm ci` wipes the generated client. **Clean baseline recorded on the BL-791 base before any edit: tsc exit 0, 0 errors; hooks gate 0 errors, 11 warnings.**

**After the change: `npx tsc --noEmit` exit 0, 0 errors — unchanged from baseline. `npm run build` exit 0, read from a log with the code echoed directly and never piped through `tail`; "Compiled successfully".** Prebuild: `check:prisma-bypass` **0 violations including its earnings-write check**, `check:removed-fields` OK across 724 files, `lint:hooks` **0 errors and 11 warnings against a ceiling of 11**, with **eslint confirmed present** at `node_modules/.bin/eslint` and producing real per-file output. **The gate was already at its ceiling, so zero new warnings was a hard requirement and was met**: every hook added is `useRef` or `useState`, neither of which produces `exhaustive-deps`, and no new `useEffect` was written.

**BACKLOG: 143 entries before, 144 after, BL-793 present once, no conflict markers.**

## SAFETY

**Display and control-surface work only.** The **6 money files, `tracking.ts` and `campaign-era.ts` are byte-identical by blob OID** against `main`. **No schema change** of this round's making; `prisma generate` only, never `migrate`. My diff is **five files**: the sidebar, ProgressPremium, the checklist component, the reviewer-config route's GET, and three lines on the admin profile page.

**Live, after the work:** earnings invariant **0 violations**; **0 payout rows touched**; the named partner unchanged at `TRIAL` with `invitedOnly` false. **30 clips were reviewed during the round, and all 30 were by one real reviewer doing normal production work — none by any dev user and none by me.** The only writes attempted from this session were PATCHes that all returned **400**, against the synthetic `dev-reviewer-001` and `dev-clipper-001` rows, never a real person. The typed phrase was deliberately entered **wrong** so nothing could be granted.

Handles are redacted throughout except where a live leaderboard figure is compared to a rendered one and the redaction is applied on both sides. No wallet address was read or printed. No Apify actor was run. **No dashes as bullets.** Worktree `C:/bl793` removed.

**Rollback:** `git revert` the commit, or delete branch `checkpoint/BL-793`.
