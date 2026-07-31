# BL-708 (ClippersHQ) — what is actually left

## Most of it is genuinely optional, and I am not going to pretend otherwise. Of everything collected here, **three** items are worth doing soon, and only one of those is money-adjacent: a quarter of all clippers carry a +2% PWA bonus whose flag can be set from a context that is provably not a PWA. Everything else is either latent, ops housekeeping, or a decision only the owner can make.

**READ ONLY. No code, data, schema, config or money change; nothing merged, nothing fixed, no env flag flipped.** Every database access was a `SELECT` through `run-select.js`, which refuses write keywords. Every timestamp is `::text` against DB `now()`, which read **2026-07-31 17:5x to 18:19 UTC** across the queries. Handles, emails, captions and wallet addresses are redacted or never selected. Base `main` `4b1d86aa`, worktree `C:/b708` at a short path, `node_modules` never junctioned. No UI code was written, so there was nothing for an accessibility review to act on. A markdown-only round cannot change `tsc` or `next build`, and neither was run.

**Every claim below was re-verified today against code or the database. Where I could not verify something, I say so by name.**

---

## PART 1 — unmerged branches: 69 of 792, and 3 matter

`origin` carries **792** `checkpoint/*` branches. **69** are genuinely not ancestors of `main`. **65 of those 69 change exactly one file**, and that file is a document: `docs/DOUBLE-PAY-PROOF.md`, `docs/BALANCE-CLAMP-ASYMMETRY.md`, `docs/HUMAN-BASELINE.md`, `docs/BUDGET-ENDGAME-AUDIT.md`, `docs/CAMPAIGN-SPEND-PERF.md` and so on. **BL-680's conclusion holds: this is not 69 pieces of unshipped work, it is 65 audit documents that were published as reports instead.**

**The four that carry source, each checked against main rather than assumed:**

| branch | SHA | date | what it is | source landed on main? |
|---|---|---|---|---|
| `checkpoint/BL-704` | `61fb19f1` | 2026-07-31 | four distinct `freshnessSource` labels so a genuine provider failure is distinguishable from our own code skipping the fetch, plus removal of 3 dead imports | **NO.** All four label strings return `grep -c` **0** on main, and the dead `MAX_CLIP_AGE_MS` import it removed is still present (count 1) |
| `checkpoint/BL-493` | `5cbfc740` | 2026-07-14 | growth-engine message catalog: `src/lib/growth/catalog.ts` and `src/components/admin/GrowthCatalog.tsx` | **NO.** Both files are **absent from main entirely**. A whole unshipped feature |
| `checkpoint/BL-524` | `8fc8a331` | 2026-07-16 | admin growth dashboard showing the real per-trigger send state and the specific reason a message is held | **NO.** 354 changed lines across the dashboard and its API, none on main |
| `checkpoint/BL-351` | `e436f5ee` | 2026-07-11 | clip thumbnails | **YES, by another route.** `src/lib/clip-thumbnail.ts` exists on main and `thumbnailUrl` is in the schema. The branch is stale and can be deleted |

> **What the owner still needs to merge: arguably only `BL-704`, and it is not urgent.** Its own report is explicit that it changes no accept-or-refuse decision; it only makes a log field honest. `BL-493` and `BL-524` are real unshipped features on an owner-only surface, so merging them is a product choice, not a debt. The other 66 need nothing.

## PART 2 — deferred and flagged, not fixed

### 2.1 The Deja Shoe rule. STILL LIVE, and it is a content question now, not an enforcement one

BL-707 flipped all 9 `auto_reject` rules to `rank`, so **0 auto_reject rules remain platform-wide** (verified today). What survives untouched is the rule's **content**: the campaign named "Deja Shoe" (PAUSED) carries rule `r1` requiring the caption token a brand handle belonging to a DIFFERENT campaign (redacted), which is the CROCS campaign's handle. **Impact today: none.** A `rank` rule flags for a human and refuses nothing. **What closing it takes:** one owner sentence saying whether that token is right, then a one-line data edit. **Raised by:** BL-707.

### 2.2 The light-theme contrast risk on "Get started". STILL LIVE

`src/app/preview/preview-landing.tsx` still contains **1** occurrence of `var(--bg-primary,#09090b)`, on the secondary hero button. `--bg-primary` is declared only inside `.dark` and `.light`, never on `:root`, so the fallback is dead code and under `.light` the pill composites 78% `#fafafa` with white text at about **1.03:1**. **Impact: bounded and probably zero in practice.** BL-703 measured that a stale `theme=light` in `localStorage` did **not** actually flip `/preview` in dev, so the trigger was not reproducible even when deliberately provoked. **What closing it takes:** a `--hero-scrim` token on `:root` plus validating the persisted theme value at `theme-provider.tsx:26`. **Raised by:** BL-699, recorded in BACKLOG by BL-705.

### 2.3 The two Completed-row arrow findings. ONE IS CLOSED, ONE IS STILL LIVE

BL-671 deferred both. Checked against the current file today:

* **SC 4.1.2, `opacity-0` leaving a fully named button with nothing saying it is unavailable: CLOSED.** `preview-campaign-row.tsx:309` now carries `aria-disabled={disabled}` and `:311` uses `opacity-35`, which is exactly the fix BL-671 prescribed. A later round landed it.
* **SC 2.5.7, no visible non-drag affordance below 640px: STILL LIVE.** `preview-campaign-row.tsx:246` still reads `hidden shrink-0 items-center gap-2 sm:flex`, so the arrows do not render below `sm`, and `:266` still suppresses the scrollbar with `[scrollbar-width:none]` and `[&::-webkit-scrollbar]:hidden`. A sub-640px or 400%-zoom **mouse** user has drag and nothing else.

**Impact:** narrow. It needs a mouse at a phone-width viewport, which in practice means a desktop user at 400% zoom. **What closing it takes:** render the arrows at every width instead of `sm:flex`, which is the change BL-671's brief ring-fenced.

### 2.4 The client CTA still dominant and first in tab order. STILL LIVE, by design

In `preview-landing.tsx` the signed-out hero renders the Calendly anchor at **line 319** and the `/login` link at **line 357**, so the client CTA is still first in DOM and tab order, and it still carries the solid `bg-accent` fill against the secondary's outline. Two independent reviews called this the real cause of clipper mis-clicks. BL-699 addressed it by **relabelling** ("Brands: book a call") rather than by reordering or de-emphasising, and BL-705 then removed the clarifying line beneath at the owner's request. **Impact: this is the one item on the list with a measured behavioural history**, a clipper actually booked a sales call by mistake. **What closing it takes:** an owner decision, see PART 3.

### 2.5 Instagram cover frames. THE FIX IS NOW PROVEN WORKING. The backfill still has not run

BL-675 shipped the fix but could **not** prove it on live traffic, because zero Instagram clips had been submitted since its deploy at that moment. **Today it is provable, and it works:**

| platform | clips | missing thumbnail | new in 7 days | of those, missing |
|---|---|---|---|---|
| Instagram | 1,961 | 1,007 (51.4%) | 280 | **32 (11.4%)** |
| TikTok | 1,161 | 525 (45.2%) | 97 | **7 (7.2%)** |
| YouTube | 1,375 | **1,375 (100%)** | 51 | **51 (100%)** |

**Instagram capture on new traffic now succeeds 88.6% of the time**, so BL-675's fix is confirmed live. The historic backlog remains because `scripts/backfill-clip-thumbnails.ts` has never been run.

**A finding neither BL-673 nor BL-675 covered: YouTube thumbnails have never worked at all.** 1,375 of 1,375, including all 51 submitted this week. That is not a backlog, it is an unimplemented path.

**On BL-673's "169 Instagram clips": I could not reproduce that number and I am not going to pretend I did.** Today's Instagram figure is 1,007 missing. BL-673's 169 was almost certainly scoped to a narrower cohort whose exact predicate the report does not state in a form I could re-run.

### 2.6 Worktrees each holding a working Apify key. STILL LIVE AND GROWING

BL-678 counted 41. **Today the count is 65** worktrees whose `.env.local` contains a live-looking `APIFY_API_KEY`, out of **104** worktrees total. It grew because every audit round, including this one, copies `.env.local` into a fresh worktree to reach the database. **BL-678's point stands exactly: the in-code guard cannot neutralise this, because any script can call `https://api.apify.com/v2` directly with the key and never touch the guarded module.** **Impact:** the blast radius is a local disk, not the internet, but it is 65 copies of a billable credential. **What closing it takes:** rotate the Apify key, which also makes all 65 copies inert at once, and stop copying `.env.local` into worktrees by pointing scripts at a single shared env path.

### 2.7 The surviving Apify call sites. STILL LIVE, and my count differs from the inherited one

`src/lib/apify.ts` is byte-identical to its BL-678 state (blob `656bf4c0`, re-verified in BL-707). Counted today with `grep -c`: **8** `BL-678` markers and **6** `fetch(` call sites against `https://api.apify.com/v2`. **I could not reproduce the figure of 11 guarded call sites**, and I am reporting what I measured rather than repeating the number. **Is deleting them safe now?** Not from this evidence. `apify.ts` is still imported by the tracking path and the guards return early rather than the calls being dead; proving deletion safe needs a caller-by-caller trace this read-only round did not do.

### 2.8 The 52 unencrypted wallet rows. EXACTLY STILL LIVE

`payout_requests` holds **147** rows with a wallet address. **95** have `walletAddressEnc` populated. **52** have a plaintext `walletAddress` and no encrypted twin. The figure is unchanged to the row. The owner declined to encrypt them. **Impact:** 52 payout addresses sit in plaintext in a database whose RLS is deny-all and which Prisma reaches with a service credential. **What closing it takes:** a backfill through the same encryption path the other 95 already use.

### 2.9 The screenshot reader. STILL INERT, ACCURACY STILL UNMEASURED

`src/lib/creator-scan/screenshot-ocr.ts` exists and `scripts/test-bl-650-screenshot-reader.ts` alongside it. `OCR_SPACE_API_KEY` returns `grep -c` **0** in both `.env` and `.env.local`, so the reader cannot run. **Its accuracy has never been measured against a real screenshot**, which is the actual blocker: the code is written, the evidence is not. **What closing it takes:** the owner supplying a set of real creator screenshots, then one measurement round. Until then it is dormant code that costs nothing.

### 2.10 The reviewer-note shadow data. STILL FAR SHORT OF USABLE

BL-659 estimated 2 to 3 months. **Where it actually stands today:** `rule_shadow_decisions` holds **340 rows**, first row **2026-07-24 16:09:38.961**, latest **2026-07-31 17:09:58.865**, so **7 days** of data. Of those 340 rows only **98** carry a caption at all. Across them, **26** rule evaluations produced a verdict and **2,612** failed open, so **99.0% of evaluations decided nothing**, and the table records **zero** `wouldReject` rows. **Impact:** there is no false-rejection rate and will not be one soon. **What closing it takes:** time, and a higher caption-capture rate; at the current rate the sample will still be thin in a month.

## PART 3 — open owner decisions

**1. The $387.81 across 23 clippers, now that BL-698 has aligned the display. Is any of it still owed?**
Measured today with the real `computeBalance`: **26 clippers, $392.45** now excluded from displayed balances. Of the retired money platform-wide, **$42.75 sits on ACTIVE or PAUSED campaigns and could still recover if the video returns; $3,510.26 sits on finished campaigns and cannot**, because `tracking.ts` excludes PAST, COMPLETED and DRAFT campaigns from the sweep.
*Options.* **(a) Pay the $42.75 recoverable slice** and treat the rest as genuinely unpayable, which matches the copy clippers now see. **(b) Pay nothing**, which is what the current code does and what the on-screen wording already says. **(c) Pay all $392.45** as goodwill, which contradicts the platform's own stated rule that a video that is gone cannot be billed to a client.
*Consequence of not deciding:* nothing breaks. The display and the gate already agree, and clippers have been given a plain explanation.

**2. The hero CTA order. Should the client button stop being first and dominant?**
*Options.* **(a) Leave it**, accepting the mis-click risk the relabel reduced but did not remove. **(b) Swap the DOM order** so "Get started" is first in tab order, keeping both visible. **(c) De-emphasise the client button** to the outline treatment and promote "Get started" to the fill.
*Consequence:* (b) and (c) both touch a conversion surface the owner has iterated on four times in two days; neither is a correctness fix.

**3. The Deja Shoe token.** Is a brand handle belonging to a DIFFERENT campaign (redacted) correct on a campaign named Deja Shoe, or a copy-paste? One sentence closes it.

**4. The 52 plaintext wallet rows.** Does the earlier decision not to encrypt still stand?

**5. The screenshot reader.** Will the owner supply real screenshots so its accuracy can be measured, or should the code be deleted rather than left dormant?

**6. `BL-493` and `BL-524`.** Ship the growth catalog and the growth dashboard, or abandon the branches?

## PART 4 — known defects still live, measured today

| defect | BL-680's figure | today, measured | verdict |
|---|---|---|---|
| **force-recalc raw-campaign caps** | live, latent | **still live.** `admin/force-recalc-earnings/route.ts:193-194` selects live `minViews` and `maxPayoutPerClip` off the campaign; `grep -c` for `maxPayoutPerClipAtApproval` and `minViewsAtApproval` in that file returns **0**, so a manual recompute re-prices against today's caps rather than the caps at approval | **UNCHANGED.** Admin-manual path only, so it fires only when someone presses the button |
| **PWA predicate mismatch** | live, latent | **still live, and larger than "latent" suggests.** See below | **UPGRADED by measurement** |
| **FLAGGED phantom** | 6 clips, $113.50 clipper, $92.17 owner | **6 clips, $113.50** exactly. The **$92.17 owner side I did not re-derive**, for the same reason BL-680 did not: it sits on agency rows and re-deriving them is a write-adjacent operation | **UNCHANGED on the clipper side; owner side unverified and named as such** |
| **stale UNDER_REVIEW payouts** | 3, $166.45, oldest 55 days | **3, $147.12 in `finalAmount`, oldest `2026-06-05 01:06:42.901`, now 56.7 days** | **UNCHANGED in count, GROWN in age.** The $ differs from BL-680 because I summed `finalAmount`; the money is still reserved and unpaid |
| **over-held clippers** (BL-627) | varies by method | **3 clippers, $37.35 total excess, worst case $17.52**, measuring lifetime PAID against lifetime APPROVED non-deleted earnings | small and stable. My method is stated so it can be compared rather than trusted |

**The PWA predicate mismatch, described precisely because the measurement changes its priority.** The client decides "am I a PWA" in `src/hooks/use-pwa.ts:9-12` via `matchMedia("(display-mode: standalone)")` or `navigator.standalone`. It then sends a **hardcoded** `X-PWA-Mode: standalone` header. The server (`api/user/pwa-status/route.ts:34-37`) checks only that the header equals that constant, and its own comment concedes headers "can be forged with curl". The substantive mismatch is not forgery: **`pwa-install-popup.tsx` sends the same hardcoded standalone header at `:250` and `:386`, and that popup only renders when the user is NOT a PWA** (`app-layout.tsx:1141` gates it on `!isPWA`). So the one component that exists exclusively for non-installed users asserts installed context to the endpoint that sets the flag.

That flag is money. `earnings-calc.ts:61` defines `PWA_BONUS_PERCENT = 2` and `:157` applies it whenever `isPWAUser` is true. **Today 319 of 1,240 clippers, 25.7%, carry `isPWAUser: true`.** **To be exact about what I proved and what I did not: I proved the mechanism permits the flag to be set from a non-PWA context. I did not prove that any of the 319 was set that way, and this read-only round could not.**

## PART 5 — what is silently degrading

| thing | current number | rate | headroom |
|---|---|---|---|
| **`videoUnavailable` population** | **789** clips (598 APPROVED), of 4,499 live clips | **45 in the last 7 days, about 6.4 a day.** Daily counts run 1 to 15 | comfortable. **Correction worth stating: the 30-day figure of 785 is misleading**, because **710 of them carry a `videoUnavailableSince` of 2026-07-18**, a single sweep. The ongoing rate is single digits |
| **tracking headroom** | **4,421 active jobs, and 2,184 of them are due NOW** | average check interval 4,273 minutes, range 60 to 21,600 | **this is the one number I would not ignore.** `clipsPerTick` (`tracking.ts:160-174`) defaults to **30**, not 90, and `CLIPS_PER_TICK` is **absent from both local env files**, so I cannot see what Railway sets. At the code default the comment itself claims about 180 clips an hour against about 142 an hour of demand. A 2,184 backlog takes roughly 12 hours to drain at that rate, and new work keeps arriving |
| **`/api/campaigns/spend` aggregate** | **4,499 clips** against BL-642's roughly 50,000-clip threshold | **+1,899 in 30 days, about 63 a day** | **9% of the way there, roughly 720 days at the current rate.** Not a concern |
| **provider cost** | **not measured, and deliberately so.** Apify is hard-off per BL-678 and reading spend means calling the Apify API, which this round is forbidden to do | | named as unverified |

## PART 6 — the ranked list

Effort is rough: **S** is under an hour, **M** is a round, **L** is several.

### SHOULD DO SOON, and it is a short list

| # | what | who feels it | effort | risk of fixing | risk of not fixing |
|---|---|---|---|---|---|
| 1 | **Confirm the PWA bonus flag is not being set from non-PWA contexts**, then fix the popup's hardcoded header if it is | 319 clippers carry the +2% bonus; the owner pays it | **S to measure, M to fix** | low; the fix is to stop sending a constant from a component that means the opposite | a quarter of clippers may carry a bonus they did not earn, and nobody has checked |
| 2 | **Process or void the 3 UNDER_REVIEW payouts**, $147.12, oldest 56.7 days | 3 clippers waiting nearly two months | **S**, it is ops not code | none, it is a decision | clipper trust, and it grows a day older every day |
| 3 | **Rotate the Apify key** | nobody today; it is a credential-hygiene ceiling | **S** | low, Apify is already hard-off so nothing depends on the key working | 65 local copies of a billable credential, growing every round |

### CAN WAIT

| # | what | who feels it | effort | risk of fixing | risk of not fixing |
|---|---|---|---|---|---|
| 4 | Run the thumbnail backfill for 1,007 Instagram and 525 TikTok clips | clippers see a blank card on old clips | M | low; BL-673 priced it and the fix it depends on is now proven live | cosmetic only, and it does not grow, since new capture works |
| 5 | Implement YouTube thumbnails at all, 1,375 of 1,375 missing | every YouTube clipper | M to L | medium, it is a new path not a fix | cosmetic, but it is 100% and permanent |
| 6 | Merge `BL-704`'s freshness labels | whoever next debugs a fail-open acceptance | S | none, it changes no decision | the next freshness investigation starts blind again |
| 7 | Encrypt the 52 plaintext wallet rows | 52 clippers, if the database were ever exposed | M | low, the path already exists for the other 95 | unchanged risk, and the owner already declined once |
| 8 | Fix the force-recalc caps read | only fires when an admin presses recompute | M | medium, it touches an earnings path | latent mis-pricing, invisible until it happens |
| 9 | Render the campaign-row arrows at every width, SC 2.5.7 | mouse users at 400% zoom | S | low, but the owner ring-fenced arrow behaviour once already | narrow accessibility gap |
| 10 | The `--hero-scrim` token and theme validation | nobody reproducibly | S | low | a contrast failure whose trigger could not be reproduced |

### PROBABLY NEVER

| # | what | why |
|---|---|---|
| 11 | Delete the 65 doc-only unmerged branches | they cost nothing and the reports repo already holds the content |
| 12 | Delete the 6 guarded Apify call sites | the guard works, Apify is off, and proving deletion safe costs more than leaving them |
| 13 | The screenshot reader | inert, unmeasured, and blocked on screenshots the owner has not supplied. Either measure it or delete it, but doing neither costs nothing |
| 14 | `BL-351` | its feature already landed by another route; delete the branch |
| 15 | `/api/campaigns/spend` | 720 days of headroom |

### The single thing I would do next

**Check whether the 319 clippers carrying `isPWAUser: true` actually installed the app.** It is the only item on this list where a mechanism I verified today can quietly move money, it affects a quarter of the clipper base, and the check is one query against `lastPWAOpenAt` and the install-popup dismissal state rather than a code change. Everything else here is either latent, cosmetic, ops housekeeping, or a decision that is the owner's to make and nobody else's.

**And the honest summary: nothing on this list is on fire.** The platform's money paths are byte-identical and verified across the last six rounds, the earnings invariant reports 0 violations, the withdrawal gate agrees with the displayed balance, auto-rejection is off in code and in data, and the freshness rule holds for every non-owner. What is left is a short maintenance list and six questions only the owner can answer.

---

## What I could not verify, named

* **The $92.17 FLAGGED owner phantom.** Re-deriving owner agency rows is write-adjacent and outside a read-only round. The clipper side, 6 clips at $113.50, is confirmed unchanged.
* **BL-678's "11 guarded Apify call sites".** I count 8 `BL-678` markers and 6 `fetch(` sites to `api.apify.com` in `src/lib/apify.ts`. I report my count, not the inherited one.
* **BL-673's "169 Instagram clips".** Today's figure is 1,007 missing; the report's predicate is not stated in a re-runnable form.
* **The live `CLIPS_PER_TICK`.** The code default is 30 and the variable is absent from both local env files; Railway's environment is not readable from here, so the effective production value is unknown.
* **Provider cost trend.** Reading Apify spend requires calling Apify, which this round is forbidden to do.
* **Whether any of the 319 `isPWAUser` flags was set from a non-PWA context.** The mechanism permits it; the instances were not measured.
