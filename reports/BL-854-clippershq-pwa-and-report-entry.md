# BL-854 — the install bonus stays, because the signal cannot tell an uninstall from a quiet week, and the report entry now has two more doors

## THE ANSWER IN ONE LINE

> **`lastPWAOpenAt` records when somebody OPENED the installed app, not whether they still HAVE it, and nothing else on the server can tell those apart. Every staleness threshold that is safe today saves $0.00 a month, and the only one that saves anything at all ($0.06 a month) sits 2.23 days away from stripping the bonus off a clipper who is submitting clips right now. So nothing was revoked, no revocation mechanism was built, and I recommend against revoking. The Help entry and the marketplace pointer shipped, and all four report doors reach one form.**

**Merged to main and verified pushed. `origin/main` == local at `84e08ac7`.** Branch `checkpoint/BL-854` @ `bcf75abc`, base `2c108cd3`. Tags `pre-BL-854` (`2c108cd3`) / `post-BL-854` (`bcf75abc`) / `pre-merge-BL-854` (`ee15936d`) / `post-merge-BL-854` (`84e08ac7`), all on origin. Isolated worktree `C:/w854`, short path, `node_modules` never junctioned, **removed at the end and verified gone by listing the path**. DB `now()` from `2026-09-07 15:54:40.201446+00` to `16:53:32.956`, every timestamp cast `::text`. Handles, emails and user ids are never selected; no wallet address was read or printed.

**A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE.**

**Collision, and how it was avoided.** Three sessions were live in this repository. `C:/w852` and `C:/w853` existed when this round started, both with a modification time inside the same minute, so the shared tree was never used for editing: this round created its own worktree at `C:/w854` on its own branch and did every edit, build, typecheck and render there. **BL-852 then merged to main mid-round**, moving it from `2c108cd3` to `ee15936d` under me. The merge into current main is a real `--no-ff` merge with **two conflicts, both resolved by keeping BOTH sides**, and the merged tree was rebuilt and re-rendered from scratch, so everything below is proven on main and not only on the branch. `C:/w853` still holds `checkpoint/BL-853` and was not touched. **`checkpoint/BL-723` is NOT an ancestor of this branch or of main, checked directly.**

**BL-852 also shipped a second mechanism for the same dialog, and that is dealt with head-on in PART 4 rather than left as two systems nobody reconciled.**

---

## PART 1 — THE SIGNAL, MEASURED BEFORE ANYTHING WAS TAKEN FROM ANYONE

### What actually writes the signal, traced rather than assumed

One place, and it is not a background process. `app-layout.tsx:224-236`:

```ts
const lastSync = localStorage.getItem("pwa_last_sync");
const oneHour = 60 * 60 * 1000;
if (isPWA && (!lastSync || Date.now() - parseInt(lastSync) > oneHour)) {
  localStorage.setItem("pwa_last_sync", Date.now().toString());
  fetch("/api/user/pwa-status", { method: "POST", headers: { "X-PWA-Mode": "standalone" } });
}
```

`isPWA` is `useIsPWA()`, which reads the browser's own `matchMedia("(display-mode: standalone)")`. **BL-710 was right that a recent value cannot be produced by a one-off forged request.** But read what it measures: it fires **when the app shell mounts in a standalone context**, at most once an hour. There is no service worker, no periodic background sync and no push anywhere in the repository.

> **So the column's meaning, stated exactly: `lastPWAOpenAt` is the last time this person OPENED the installed app. It is not, and cannot be, a statement about whether the app is still on their phone. If the phone is in a pocket, nothing is written.** A clipper who installed in June, still has it, and has not opened it since August is byte-identical in the database to a clipper who deleted it in August.

### The population today

| measure | value |
|---|---|
| users / clippers | 1,679 / 1,629 |
| **flagged clippers (`isPWAUser`)** | **398** |
| flagged, all roles | 402 |
| flagged with `lastPWAOpenAt` NULL | **0** |
| earliest open | `2026-04-19 15:58:05.088` |
| latest open | `2026-09-07 15:53:03.176` (97 seconds before the query) |
| grants carrying BL-711 provenance (`pwaGrantedAt`) | **118** |
| of those, corroborated by a later standalone open | **81 (68.6%)** |

**The brief's figure of 357 is out of date. It is 398 flagged clippers, not 357.** BL-710 measured 319 and BL-711 measured 323 five weeks ago. Real people are still installing.

### The staleness distribution the brief asked for

| last opened the installed app | flagged clippers | oldest in bucket | newest in bucket |
|---|---|---|---|
| within 24 hours | **33** | `2026-09-06 16:01:42.147` | `2026-09-07 15:53:03.176` |
| 1 to 7 days | **41** | `2026-08-31 17:14:42.714` | `2026-09-06 14:30:29.554` |
| 7 to 14 days | **25** | `2026-08-24 17:44:36.137` | `2026-08-31 08:07:42.58` |
| 14 to 30 days | **68** | `2026-08-09 01:58:41.069` | `2026-08-24 14:28:55.646` |
| 30 to 60 days | **71** | `2026-07-09 16:00:14.51` | `2026-08-08 08:53:33.774` |
| 60 to 90 days | **90** | `2026-06-10 09:40:04.612` | `2026-07-09 13:40:59.335` |
| over 90 days | **70** | `2026-04-24 17:23:18.229` | `2026-06-09 09:25:02.946` |

**99 within a fortnight. 231 beyond 30 days. The oldest is 141 days.**

### THE TEST THAT DECIDES IT: is a stale flag an uninstall, or just a quiet clipper?

If staleness meant *uninstalled*, some of those people would still be using the platform through a browser tab. That is exactly what an uninstall looks like from a server: the account keeps working and the standalone signal stops. So I asked the database.

**Of the flagged clippers whose last standalone open is more than 14 days ago, how many have submitted a single clip since that open?**

| last opened | flagged clippers | still submitting clips after that open | clips submitted since |
|---|---|---|---|
| within 14 days | 99 | 2 | 2 |
| 14 to 30 days | 68 | **0** | **0** |
| 30 to 60 days | 71 | **0** | **0** |
| 60 to 90 days | 90 | **0** | **0** |
| over 90 days | 70 | **0** | **0** |

**Zero. Not one of the 299 has posted a clip since their last standalone open.** The two in the first bucket opened the app and submitted later the same fortnight, which is ordinary use.

The same question from the other end, over the clippers who are actually active:

```
flagged clippers who submitted a clip in the last 30 days       54
  of those whose last standalone open is 7+ days older           0
  of those whose last standalone open is 30+ days older          0
  oldest standalone open anywhere in that group   2026-08-09 12:36:21.748
```

> **There is no population in this data that looks like "uninstalled but still here." Every stale flag belongs to somebody who stopped using Clippers HQ entirely, through every channel. Staleness is perfectly confounded with dormancy.** The signal is not measuring what the owner wants it to measure. It is measuring whether the person is still clipping.

### The threshold, stated and justified, and then declined

Over the **38 flagged clippers who submitted a clip in the last 14 days**, which is the population the platform actually runs on:

| | value |
|---|---|
| average days since their last standalone open | **1.54** |
| **worst case in that group** | **11.77 days** |
| would lose the bonus at a **7 day** threshold | **1** (a clipper submitting clips right now) |
| would lose it at a **14 day** threshold | 0 |
| would lose it at a **30 day** threshold | 0 |

And what each threshold saves, measured on **clips approved in the last 30 days**, which is the only thing a forward-only revocation can ever touch:

| the clipper's last standalone open | clippers earning | clips in 30 days | base earned | **2% ceiling per month** |
|---|---|---|---|---|
| within 14 days | 42 | 2,591 | $4,572.14 | $91.44 |
| 14 to 30 days | 3 | 4 | $3.21 | **$0.06** |
| **over 30 days** | **0** | **0** | **$0.00** | **$0.00** |

**Read the two tables together and the question answers itself.**

* **A 30 day threshold is safe and saves exactly $0.00 a month.** Nobody beyond 30 days has earned anything in 30 days, so there is nothing to stop paying.
* **A 14 day threshold saves $0.06 a month** and clears today's active population by **2.23 days**. One quiet fortnight from one clipper and it starts taking money off somebody holding the app in their hand.
* **A 7 day threshold takes the bonus off 1 clipper who is submitting clips today.** That is not a projection. It is a row in the database right now.

> **So the only threshold I could defend is 30 days, and at 30 days the feature does nothing at all. Anything shorter buys a few cents a month and starts producing exactly the error the owner said he wanted to avoid.**

**And coming back after a long quiet spell is a thing people here actually do: five flagged clippers have already returned after a gap of more than 30 days, and the longest observed gap is 84.1 days.** Under a revocation rule each of those five would have come back to a smaller rate at the exact moment the platform most wants them clipping.

### THE PLAIN ANSWER THE BRIEF ASKED FOR

**The signal cannot distinguish uninstalled from simply-not-opened, and I recommend AGAINST revoking.**

Nothing else on the server closes the gap, and I checked rather than assumed:

* **`beforeinstallprompt`** is captured at `use-pwa.ts:70-75` and **never reported to the server**. It is also useless for this even if it were: Chrome fires it on heuristics, **iOS Safari never fires it at all**, and it only fires in a browser tab, so somebody with the app on their phone who opens a link on a laptop would be reported as not having it.
* **`getInstalledRelatedApps()`** appears nowhere in the repository, is Android Chrome only, and needs a `related_applications` manifest entry pointing at a Play Store listing that does not exist.
* **The revocation door already exists and nothing walks through it.** `pwa-status/route.ts:169-172` clears `isPWAUser` when a request carries `installed: false`, and **not one of the four callers in the entire codebase ever sends it** (`app-layout.tsx:234`, `sidebar.tsx:883`, `pwa-install-popup.tsx:248` and `:384`, all defaulting to `installed: true`). That is why the flag is permanent today, exactly as the brief says.

**BL-711's provenance is working, and it is the one genuinely new fact here.** Of **118 grants since `2026-07-31 19:47:31.308`, 81 (68.6%) have been corroborated** by a later standalone open at least ten minutes after the grant. The **37 that have not** hold **$127.89** of base earnings between them, a **$2.56** ceiling, ever, and that number includes people who installed today and whose first hourly sync has not fired yet. That is the only population where this data says anything, and it says $2.56.

---

## PART 2 — NOTHING WAS REVOKED, AND HERE IS WHAT THAT COSTS

**No revocation shipped, and no revocation mechanism was built.** The brief made PART 2 conditional on the signal being reliable; PART 1 measured that it is not. **Building the machinery and leaving it switched off would be worse than not building it**: it is a loaded gun for the next round to find, read as finished work, and enable.

**So forward-only, never-decrease and paid-is-final are answered the strongest way available. No code that computes, writes or reads earnings was touched at all, and this round wrote nothing to the database.**

| the guarantee | how it holds |
|---|---|
| **no past earning falls** | **0 clips written by this round.** Earnings invariant **0 violations** before and after |
| **no balance drops** | `balance.ts` byte-identical by blob OID `81a683c1a6ed` on the base, the branch and merged main; nothing calls `recalculateUnpaidEarnings` |
| **BL-538 never-decrease** | `src/lib/earnings-never-decrease.ts` **byte-identical** `c15145f51a56`, untouched and never approached |
| **BL-824 paid-is-final** | `balance.ts` unchanged, so `effectivePaid = min(paidGross, payableEarnings)` is intact |
| **no payout touched** | `payout_fp` **byte-identical** `c46a71674ffc2945582bc9720403efde`, 222 rows, newest payout write `2026-09-07 12:51:23.15`, **three hours before this round's first read**. Created, modified, approved or cancelled: **0** |
| **the bonus itself** | `earnings-calc.ts` **byte-identical** `797e20985ad5`, `PWA_BONUS_PERCENT = 2` at `:61` unchanged, still additive into the capped `Math.min(levelBonus + streakBonus + pwaBonus, maxBonusCap)` at `:164` with `MAX_BONUS_CAP = 25` |
| **every existing flag** | flagged users **402 before, 402 after** |

**What it costs to leave it alone: the $91.44 a month ceiling belongs to the 42 clippers who opened the app within a fortnight and are clipping now.** That is the bonus paying for precisely the behaviour it exists to buy. The part any safe rule could stop is **$0.00 a month**.

**Reversibility already works, and it is faster than the brief assumed.** The hourly sync fires on the first standalone mount after a reinstall, and `pwa-status/route.ts:148-167` refreshes `lastPWAOpenAt` on that request. **A returning clipper is therefore restored on their first app open, which is seconds, not an hour**; the hour is the ceiling on how often the sync repeats, not a delay before the first one. A fresh grant also resets `pwaGrantCorroboratedAt` to null by design (`:137`), so a reinstall never inherits the previous install's corroboration.

**Against BL-1528's "$2 per $100 across 357 real people": I could not reconcile that figure and I am saying so rather than restating it.** BL-1528 is the round about page-scoring in the clipper-finder project and contains no PWA measurement, no 357 and no per-$100 rate. The comparable numbers, measured here, are a **2% ceiling on $4,572.14 of base earned in the last 30 days by the 42 flagged clippers who are active**, and a population of **398**, not 357.

---

## PART 3 — WHAT AN AFFECTED CLIPPER WOULD BE TOLD, WRITTEN AND QUOTED, AND DELIBERATELY NOT SHIPPED

**Nobody is affected, because nothing was revoked, so this copy has no screen to live on today.** It is written, quoted in full, and ready, so that if the owner overrules the recommendation the words exist and nobody has to invent them in a hurry. **Shipping it now would be worse than useless: a notice about a bonus stopping, shown when no bonus has stopped, is a false statement about somebody's money.**

> ### The app bonus has paused
>
> The extra 2% applies while you are using the installed app. Your account has not opened it since 12 August, so clips from today are earning without it.
>
> Everything you have already earned stays exactly as it is. This does not change any past clip, your balance, or anything you have been paid.
>
> Open Clippers HQ from your home screen and the 2% comes back on your next clip.

**Why it is worded that way.** *"Has paused"* rather than *removed* or *lost*, because it is reversible in one tap and the word should say so. **No accusation and no implication of wrongdoing**: it names a fact about the app, never a judgement about the person, which is BL-518 and BL-521's rule. The date is stated so the clipper can check it against their own memory rather than being asked to accept it. **The second paragraph exists because it is the thing people will actually fear**, and it is a promise the code already keeps: BL-538's never-decrease guard and BL-824's paid-is-final rule both hold regardless. And the route back is one sentence with no support ticket in it.

**Where it would go, if it ever ships:** the earnings page beside the bonus breakdown, not an email and not a popup, because that is the screen where somebody would otherwise notice the number and have no explanation. **Nobody should ever discover this by seeing their earnings drop**, which is exactly why a revocation without this copy must not ship.

**One thing the platform promises today that is worth the owner knowing:** the sidebar's Download App row carries a visible `+2%` badge and an `sr-only` *", +2% earnings bonus"* (`sidebar.tsx:918-919`). **That is an unconditional promise on screen right now.** Any revocation rule would make it conditional, and that badge would have to change in the same round.

---

## PART 4 — THE HELP ENTRY

**It is the second block on the page**, directly beneath the Discord ticket entry, at every width.

> ### Report a problem
> Something broken, wrong, or just not adding up? Send it straight to the team along with the page you were on. It goes one way, so no reply comes back here. For an answer, open a Discord ticket above.
>
> **[ Report a problem ]**

**Why there and not in the right-hand `<aside>`, stated because the owner said "beneath the Discord links" and there are TWO Discord entries on that page.** One is the prominent `Open a Discord ticket` CTA at the top of the left column; the other is the channel list in the aside. **The aside stacks LAST below `lg` and is a `lg:sticky` scroller above it**, so an entry inside it would be the final thing on a phone page and below the fold of its own scroller on a desktop. That is *beneath the Discord links* and it is not *big and obvious*. The position shipped is both. **There is exactly one report entry on `/help`**, asserted at all five widths.

**It is deliberately NOT the solid accent fill its neighbour uses.** In that file `bg-accent` plus `#09090b` ink plus `ArrowUpRight` plus an `sr-only` "(opens in a new tab)" means *this leaves the site*, three times over. This opens a dialog in place, so borrowing that treatment would say something untrue (3.2.4). It is outlined on `--border-strong` (3.48:1 dark / 3.42:1 light on the card) rather than `--border-color`, which `globals.css:44` records as **1.18:1** against the card and therefore has no perceivable extent. **No arrow, no `target`, no `rel`, no new-tab cue in any form.**

### BL-809's sidebar row is untouched, and both lead to the same one form

**Proven, not asserted.** `scripts/bl854-three-doors.ts`, run against the merged tree: **29 assertions, 0 failures.**

```
DOOR 2 (/help, BL-854)                 opens the panel, focus inside, 1 dialog, 1 box, 1 form, Escape closes it
DOOR 1 (sidebar row, BL-809)           opens the panel, focus inside, 1 dialog, 1 box, 1 form, Escape closes it
DOOR 3 (marketplace pointer, BL-854)   opens the panel, focus inside, 1 dialog, 1 box, 1 form, Escape closes it
DOOR 4 (/account trainer, BL-852)      opens the panel, focus inside, 1 dialog, 1 box, 1 form, Escape closes it
exactly one report dialog exists in the DOM and it is CLOSED at rest (1, open=false)
```

**One form, one `<textarea>`, one `<form>`, one `problem_reports` row. No arrangement of triggers can produce two.** The mechanism is a `ReportProblemProvider` publishing the SAME `onReportProblem` callback that `app-layout` already threads into the three `<Sidebar>` mounts. Every trigger sets the same `reportOpen` boolean on the same single `<ReportProblemWidget>` instance.

### THE COLLISION WITH BL-852, RECONCILED RATHER THAN LEFT AS TWO SYSTEMS

**BL-852 merged mid-round and shipped a typed window-event bridge for this same dialog** (`src/lib/ui-events.ts`), with a new prebuild gate (`scripts/check-event-wiring.js`) that fails the build if either half of the pair goes missing. Its file header explicitly rejects context, on the ground that *"a consumer outside it would read a default value and no-op SILENTLY"*.

**That objection is right in general and cannot occur here, and the reason is written into the merge rather than assumed.** The context's default value is `{ open: undefined }`, and **every consumer is required to render nothing when `open` is undefined**. So a consumer outside the provider produces no control at all, which is a visible absence, never a button carrying `aria-haspopup="dialog"` that does nothing when pressed.

**That same absence IS the OWNER gate, and the event bridge cannot express it.** `onReportProblem` is `undefined` for an OWNER at `app-layout.tsx:292`, so `/help` and the marketplace render no entry for him **without either surface having to re-derive his role**. A window event has no such gate: a future call site that forgot to check the role would put a control in front of the owner that opens a form whose reports arrive at the owner.

**Both mechanisms call the same `openReport` and set the same boolean on the same single widget.** BL-852's gate still reports `1 dispatcher, 1 listener, 0 problems` on the merged tree, and DOOR 4 above is BL-852's own entry, exercised through its real button and proven to raise the same panel.

---

## PART 5 — THE MARKETPLACE POINTER

**The exact copy shipped, asserted character for character on the rendered DOM at all five widths:**

> The marketplace is new. If anything here looks wrong, **report a problem**.

**Small and unobtrusive, and explicitly not a banner.** Measured on the running page: the whole line is **250px wide at 320, 305 at 375, 344 at 414**, two lines on a phone and one on a desktop, in `--text-quiet` `#a1a1a8`, with the inline control **95 x 16** in `--link-text` `#2596be`, underlined at rest.

**Confidence rather than apology, because of what it is standing in front of.** The marketplace holds **1 listing, 0 submissions and 0 posted clips**, measured this round, so this really is the first thing a real user will meet there. The sentence states a fact and offers a route; it names no fault, carries no warning colour, and is not styled as a warning surface.

**Where it lives, and why that placement is three fixes at once.** It sits in `MpChrome`, immediately after `</MpNav>`:

* **outside the `<nav aria-label="Marketplace">` landmark**, so it is not announced as navigation (1.3.1);
* **outside `MpPageShell` and `.mp-section`**, whose rules kill a Tailwind focus ring (`button:focus { box-shadow: none }`) and replace it with a 1px **1.64:1** outline, and whose entrance stagger starts at `opacity: 0`;
* **and MpChrome persists across marketplace tab navigation** (BL-313), so this is ONE pointer on every marketplace surface rather than a copy per page, which also keeps the pressed element alive for BL-809's focus-return ladder.

**No role and no live region.** It is permanent static text, not a notification. `MpBanner` was rejected outright: it hardcodes `role="status"` / `role="alert"`, which would announce this sentence on every entry into the marketplace segment and would compete in the same tick with the real ban alert and strike warning below it (4.1.3).

**One token correction found by looking at the render rather than trusting the class name.** The first version used `text-[var(--text-secondary)]`, and the rendered colour came back `rgb(255, 255, 255)`. In this theme `--text-primary`, `--text-secondary` and `--text-muted` are **all `#ffffff`** (`globals.css:72-74`), so "secondary" is byte-identical to body text and the line was not unobtrusive at all. It now uses `--text-quiet` (`#a1a1a8`, added by BL-818 for exactly this), which measures **7.67:1** on the dark page and **7.33:1** light.

---

## PART 6 — THE EVIDENCE

### Rendered, at five widths, twice

BL-793's method, unchanged: real Chromium, **CSS viewport set through `browser.newContext({ viewport })`** rather than `resize_window`, `next dev --webpack` because Turbopack was the render blocker, `window.innerWidth` read back and asserted every time. **200 assertions on the merged main tree, 0 failures**, plus **29** from the three-doors pass and **3** phone-geometry reads.

| measured at every width | 320 | 375 | 414 | 1280 | 1440 |
|---|---|---|---|---|---|
| CSS viewport really is the asked width | yes | yes | yes | yes | yes |
| `/help` has exactly ONE report entry | 1 | 1 | 1 | 1 | 1 |
| the entry is at least 44px tall | 44 | 44 | 44 | 44 | 44 |
| it is a `<button>`, not a link | yes | yes | yes | yes | yes |
| `aria-haspopup="dialog"`, and no `aria-expanded` / `aria-controls` | yes | yes | yes | yes | yes |
| pressing it **actually opens** the panel (inert removed, opacity 1) | yes | yes | yes | yes | yes |
| focus lands on the dialog heading | yes | yes | yes | yes | yes |
| **focus returns to the exact entry that was pressed** | yes | yes | yes | yes | yes |
| the marketplace pointer is present, one only | 1 | 1 | 1 | 1 | 1 |
| the pointer sentence is exactly the shipped copy | yes | yes | yes | yes | yes |
| it carries no `role`, no `aria-live`, no `aria-label` | yes | yes | yes | yes | yes |
| it is underlined at rest and outside the nav landmark | yes | yes | yes | yes | yes |
| the pointer opens the SAME single form | yes | yes | yes | yes | yes |
| **an OWNER sees ZERO report triggers on `/help` and `/marketplace`** | **0** | **0** | **0** | **0** | **0** |
| no floating launcher anywhere | 0 | 0 | 0 | 0 | 0 |
| no sideways scroll on any of the three routes | yes | yes | yes | yes | yes |

**Screens I actually looked at, rather than only counted:** `/help` at 375 (the entry rendered second on the page, outlined, beneath the filled Discord CTA); `/marketplace` at 1440 (the quiet grey pointer above the Marketplace heading, with BL-809's sidebar row still in place beside `Download App +2%`); `/marketplace` at 375 scrolled to the pointer (two lines, 305px wide, control 95x16); and `/marketplace` at 1280 as an **OWNER**, where the nav cards run straight into the Marketplace panel with **no pointer line and no sidebar report row at all**.

**Four false failures, reported rather than replaced by the clean re-runs.**

1. **Five failures, all one assertion:** the marketplace pointer's label is `report a problem` in sentence case inside a sentence, and the first harness compared case-sensitively. Assertion fixed, not the copy.
2. **The tightened open-state check failed at all five widths on its first run.** `<ReportProblemWidget>` is mounted at ALL times and keeps `role="dialog"` while closed, because BL-809 closes it with `inert` and opacity 0 rather than unmounting it. So `waitForSelector('[role="dialog"]')` returns instantly and the read landed mid-transition. Both scripts now wait on the **open state** and assert that. **This is worth the space: the earlier, looser assertion counted elements and would have passed whether or not a press did anything.**
3. **The three-doors run first reported BL-852's `/account` entry missing.** That was hydration timing after `page.goto`, not a breakage; with a wait for the client tree the real button is there and DOOR 4 passes through it.
4. **A blue 2px outline appears around the marketplace content wrapper on load in dev.** I suspected my own change and checked instead of assuming: reverting `MpChrome.tsx` to `HEAD` and re-reading the live page produced **the same outline on the same `div.outline-none`**, MpChrome's pre-existing focus-landing div. Pre-existing, dev-only, not mine, and reported below rather than fixed.

### One real defect fixed on the way, found by the accessibility review

**`MpChrome` focused its content wrapper on every pathname change.** Above `md` the report panel is a corner card with **no backdrop and nothing `inert`ing the page behind it**, so a marketplace nav link sitting immediately above the new pointer is still clickable while the dialog is open, and that line would then land focus **behind an `aria-modal` dialog** (2.4.3 / 4.1.2). The focus trap intercepts Tab and Escape; it cannot block a programmatic `focus()`.

It now skips the steal while the dialog is up, driven off the same state that opens it and never off the panel's transition end. **Proven at all five widths by navigating with the dialog open and reading `document.activeElement` back:**

```
320  navigating with the dialog open does NOT steal focus out of it (path /marketplace/browse, active H2)
375  same     414  same     1280  same     1440  same
```

### Nothing retroactive, nothing paid, invariant clean

| claim | evidence |
|---|---|
| **no clip's earnings or status changed** | **0 clips written by this round.** 7 clips arrived and **222 were updated** between the first and last read, and **all 222 took a tracking snapshot inside the same window** with **0 manual snapshots**. That is the production tracking cron and real clippers; this round issued no clip request of any kind |
| **no payout touched** | `payout_fp` byte-identical `c46a71674ffc2945582bc9720403efde`, 222 rows, newest write `2026-09-07 12:51:23.15`, three hours before the first read. Created, modified, approved or cancelled: **0** |
| **the earnings invariant** | **0 violations**, before and after |
| **no problem report created** | `problem_reports` **11 before, 11 after**. Every row is a real user's and none was touched. Unlike BL-804, BL-808 and BL-809, this round proved the dialog by its open state and focus behaviour rather than by sending, so **no proof rows were created and none had to be deleted** |
| **no flag changed** | flagged users **402 before, 402 after**; **0** grants recorded (`pwaGrantedAt`) in the window; **0** users created since `2026-09-07 14:01:24.864`; **0** audit_logs rows in the whole window |
| **schema** | `prisma/schema.prisma` byte-identical `d7b8263a1bf0` on all three refs. **No change, no `prisma migrate`, no index** |
| **BL-678 guards** | **12** `APIFY_HARD_OFF` references across 3 files, identical before and after, `apify.ts` and `apify-hard-off.ts` byte-identical. **No Apify actor run** |

**THE ONE THING I COULD NOT ATTRIBUTE, AND I AM NOT SMOOTHING IT.** A fingerprint over `users.id || ':' || isPWAUser` moved during the round, from `23436d105596105a6a62e2bb4629ac8f` at `16:00` to `d0088c0c216a85187cdb8388d05b6d71` at `16:51`, where it is now stable across repeated reads. **Everything I can test rules out the mechanisms that would matter:** the column is `NOT NULL` with **0 nulls**, the flagged count is **402 on both sides**, **0 grants** were recorded in the window, **no user was created since 14:01:24** (before the first read), there were **0 audit_logs rows**, and **this round wrote nothing to any table and shipped no code that writes `isPWAUser`**. 28 user rows were updated in the window by ordinary traffic, 9 of them carrying a genuine standalone open, and an `updatedAt` touch does not change this fingerprint. **The most likely explanation left is a single account deletion of an unflagged user, which would change the id set while leaving the flagged count at 402, but I have no before-count of total users to confirm it and I am not going to assert it. Recorded as unexplained.** `clip_money_fp` also moved and **that one is fully attributed above** to the 222 cron-updated clips.

### Gates, honestly

**Clean baseline recorded on the untouched worktree BEFORE any edit**, with `npm ci` **exit 0** and `npx prisma generate` **exit 0** first: `npx tsc --noEmit` **TSC_EXIT=0**, `grep -c "error TS"` = **0**.

| gate | branch | merged main | final commit |
|---|---|---|---|
| `npx tsc --noEmit` | **exit 0, 0 errors** | **exit 0, 0 errors** | **exit 0, 0 errors** |
| `npm run build` | **`REAL_BUILD_EXIT=0`**, compiled in 42s | **`REAL_BUILD_EXIT_MERGED=0`**, 31.2s | **`REAL_BUILD_EXIT_FINAL=0`**, 29.0s |
| `check:prisma-bypass` | 0 violations | 0 violations | 0 violations |
| `check:removed-fields` | OK | OK | **OK across 764 files** |
| `check:event-wiring` (BL-852, new) | n/a | **0 problems**, 1 dispatcher, 1 listener | **0 problems** |
| **hooks gate** | **0 errors, 10 warnings** | **0 errors, 10 warnings** | **0 errors, 10 warnings** |

**Every exit code echoed by hand from a log, never piped through `tail`. eslint `v9.39.4` confirmed present at `node_modules/.bin/eslint` first, so the hooks gate did not silently no-op.** The 11-warning ceiling was not merely respected: **the pre-round baseline was measured by stashing the three edited files and re-running the gate, and it read exactly 10 warnings too**, so **zero new warnings were introduced**. The two hooks added are a `useMemo` with a complete dependency list and an early return inside an existing effect whose `[pathname]` list is unchanged, reading a ref.

**Merge, counted.** `d276c746` merges `bcf75abc` into `ee15936d`; `84e08ac7` adds the tightened proof scripts. **Two conflicts, both union-resolved by keeping BOTH sides, 0 conflict markers remaining, verified by grep.** **BACKLOG counted with `grep -c`, never piped to `head`: 190 sections at my base, 192 after, since BL-852 arrived with the merge and mine is the other; 23,837 lines to 24,039. `BL-854` appears once, `BL-852` once.** **`checkpoint/BL-723` is NOT an ancestor of the branch or of main.**

### Money files, by blob OID, on all three refs

All twelve **IDENTICAL on the base (`pre-merge-BL-854`), the branch (`checkpoint/BL-854`) and merged main (`verify/BL-854`)**:

```
clip-earnings-writer.ts               ac5be7deb061      tracking.ts             9563a4fc9994
earnings-calc.ts                      797e20985ad5      campaign-era.ts         106e16ad7512
balance.ts                            81a683c1a6ed      apify.ts                d66d4534dbbf
clip-earnings-invariant-middleware.ts 61cef3939536      apify-hard-off.ts       29258a5d0fb0
money-decimal.ts                      ef5cdae757b9      earnings-never-decrease.ts c15145f51a56
payout-calc.ts                        f4bc15592d0b      prisma/schema.prisma    d7b8263a1bf0
```

**`tracking.ts` does not appear in the diff.** The whole change is 7 files: one new context module, one new comment block plus a provider wrapper and a memo in `app-layout`, one section in `help-redesigned`, one line plus one early return in `MpChrome`, and four throwaway proof scripts, plus BACKLOG.

---

## ACCESSIBILITY — reviewed BEFORE any code was written, twelve blocking items, all twelve implemented

The lead coordinated five specialists and returned twelve blocking items after being sent a mid-review placement correction. **All twelve are in the shipped code.** The load-bearing ones:

1. **Both triggers gated on the callback being present**, rendering nothing when it is absent, so an OWNER never gets a control announcing "Report a problem, button, has dialog popup" that does nothing (4.1.2). Also correct when `userId` is empty, since the widget returns `null` at `:326`.
2. **`<button type="button">` on both.** A bare `<button>` defaults to `type="submit"` and `/help` carries a live `<input type="search">`.
3. **`aria-haspopup="dialog"` and nothing else, identical on all triggers.** No `aria-expanded` (that is the disclosure contract, and `aria-modal` hides the trigger while the dialog is up, so "expanded" would only ever be true when nobody can read it). No `aria-controls` (the panel is `inert` while closed, so the IDREF resolves into a subtree outside the accessibility tree, and it would now mean threading one `useId()` into three call sites). **Applying a different attribute set to one of them would itself be a 3.2.4 failure.**
4. **No `aria-label` on either control.** Visible text IS the accessible name (2.5.3): an `aria-label` of "Report a problem with the marketplace" over a visible "tell us" is a hard Level A failure, because a voice-control user saying "click tell us" gets no match.
5. **The pointer sits after `</nav>`**, not inside the navigation landmark (1.3.1), and not routed through `MpCommandBar`, whose `subtitle` prop is typed `string`.
6. **No `MpBanner` and no role at all** on the sentence, for the live-region reasons in PART 5.
7. **`--link-text` plus a permanent underline** on the inline control, because raw `text-accent` is **3.25:1** on the light page and fails 4.5:1 at that size, and because colour alone cannot distinguish a control from its sentence (1.4.1) and a touch user never hovers.
8. **The route-change focus steal**, which was a real defect and is described in PART 6.
9. **`scroll-mt-20` on both triggers and `max-lg:[scroll-padding-top:80px]` on `<main>`.** `<main>` already carried `max-md:[scroll-padding-bottom:112px]` against the phone tab bar, while a `max-lg:fixed` h-14 bar overlays the top of the same scrollport, so a focus-driven scroll-into-view aligned a control under it (2.4.11).
10. **`forced-colors:` outline spelled out on both**, because a Tailwind `ring` is a box-shadow and Windows High Contrast erases it. The lead's honest caveat is recorded too: this is **Tailwind v4**, utilities live in `@layer utilities`, and the unlayered sitewide `*:focus-visible` rule wins anyway, so `outline-none` never actually suppresses it. That is a cascade argument rather than a guarantee, which is why it is spelled out.
11. **The `ReportProblemWidget` focus-ring recipe, not the neighbouring CTA's.** `ring-white/90` measures **1.12:1** in light theme over `ring-offset-[var(--bg-card)]` (white on white), which is the exact failure the widget itself documents and fixed.
12. **The zero-results empty state** on `/help` now names the report entry as well as the Discord ticket, since somebody who searched and found nothing is exactly who it is for. Plain text pointing up the page rather than a second button, because two controls with the same name in one view is the 3.2.4 problem this round is avoiding.

**Checked and found acceptable, and worth recording:** the `<h2>` outline stays flat under one `<h1>`; three controls named "Report a problem" is required rather than a violation, since only two are ever exposed at once (exactly one `<Sidebar>` copy is in the accessibility tree per viewport, and the help and marketplace controls never co-render); the inline pointer passes 2.5.8 under the **inline exception** and vertical padding would NOT enlarge it, so none was added; the Help button meets 2.5.5 at `min-h-[44px]`; and the focus trap, `inert` and restore effect needed no change.

---

## REPORTED, NOT FIXED

* **`sidebar.tsx:883` POSTs `/api/user/pwa-status` with NO `X-PWA-Mode` header**, immediately after a genuinely accepted install, and the route returns **400** without it (`:34-37`). **So an install started from the "Download App +2%" row does not grant the bonus at that moment.** It self-heals on the clipper's first standalone open, when `app-layout`'s sync sends the header, so it is a delay rather than a loss. Out of scope, and it is a one-line fix whenever you want it.
* **The `/help` `<aside>` is roughly 40px taller than it can ever display.** `lg:top-4` inside `<main>`, whose scrollport starts 56px down, pins its top at 72px, and `lg:max-h-[calc(100dvh-2rem)]` then puts its bottom at `100dvh + 40px`. Being sticky, no scroll recovers it. The cap should be `calc(100dvh-3.5rem-2rem)`.
* **That aside is an `overflow-y-auto` scroller with no `tabIndex={0}`**, so a keyboard-only user cannot read the channel list below its fold at `lg` (2.1.1). Pre-existing.
* **The v1 drawer panel** (`app-layout.tsx:960-981`, the variant every non-OWNER gets unless the env flag is on) has neither `aria-hidden` nor `inert` when closed, only `translateX(-100%)`, so its off-screen report row stays focusable below `lg`. The v2 panel does this correctly. Pre-existing.
* **MpChrome's focus-landing div paints a 2px accent outline on load in dev**, proven present on the unmodified tree as well. Dev-only React StrictMode double-invoking the effect.
* **The marketplace pointer inherits `showNav`**, which `deriveCurrent` returns `null` for on listing detail, `/apply` and `/create`, and the whole chrome is skipped for flag-gated viewers. Not a failure, since the sidebar entry persists everywhere, but it is a conscious choice rather than an accident.

---

## WHAT THE OWNER DOES NOW

1. **REDEPLOY ON RAILWAY.** Main carries all of this; production does not.
2. **Decide on the PWA bonus.** My recommendation is to leave it, and PART 1 is the argument. If you want it revoked anyway, the copy in PART 3 must ship in the same round and the `+2%` badge in the sidebar has to stop being an unconditional promise.
3. **You can re-check this yourself at any time without any code that can strip anybody.** Run the two queries in PART 1 against `run-select.js`: the staleness distribution, and clips approved in the last 30 days split by the clipper's last standalone open. **The day the second table stops reading $0.00 for the stale bucket is the day this decision is worth revisiting, and not before.**
4. **The marketplace pointer is standing in front of an empty marketplace** (1 listing, 0 submissions). When the first real clip goes through it, tell me and it can be reworded or retired.

**Rollback:** `git revert -m 1 d276c746` or `git reset --hard pre-merge-BL-854`. **Nothing in the database needs undoing, because nothing was written to it.**

---

## SAFETY

**Verification came first and it said no.** The install signal cannot distinguish uninstalled from simply-not-opened, so **nothing was revoked from anybody, no revocation mechanism was built, and the recommendation is against revoking**, with the staleness threshold stated, justified and then declined on its own arithmetic. **No past earning, balance, clip status or payout was reduced, moved or touched**, and it could not have been: this round wrote nothing to the database and shipped no code that computes, writes or reads money. Reversibility on reinstall is stated with its real timing, and the affected count and monthly saving are reported ahead of any decision, alongside the note that BL-1528's "$2 per $100 across 357" could not be reconciled and was not restated. **The plain, non-accusatory copy an affected clipper would see is written and quoted, and deliberately not shipped, because a notice about a bonus stopping when none has stopped is a false statement about somebody's money.**

**The Help entry and the marketplace pointer reach the SAME single form**, proven by opening it from every door and reading its open state, its one `<textarea>` and its one `<form>` back, with exactly one dialog in the DOM and closed at rest; **no duplicate report is possible.** The marketplace pointer is one quiet two-line sentence with no role, no live region and no banner styling. **The 6 money files plus `tracking.ts`, `campaign-era.ts`, `apify.ts`, `apify-hard-off.ts`, `earnings-never-decrease.ts`, `payout-calc.ts` and `prisma/schema.prisma` are byte-identical by blob OID on all three refs.** No schema change, additive or otherwise; `prisma generate` only, `prisma migrate` never run. **No Apify actor was run and the BL-678 guards are intact at 12 references.** Every timestamp is `::text` against DB `now()`. Handles, emails and user ids were never selected; no wallet address was read or printed. Collision was avoided by working only in `C:/w854` while two peer worktrees were live, and by rebuilding and re-rendering the merged tree after BL-852 landed under me. **The worktree is verified gone: `git worktree list` shows only the shared tree and `C:/w853`, and listing `C:/w854` returns "No such file or directory".** No heredocs in the shipped scripts; one shell at a time; the dev server was killed by PID from `netstat`, never by image name, so no peer session was taken down. Gate results are the real ones, echoed by hand from logs. NO dashes as bullets.
