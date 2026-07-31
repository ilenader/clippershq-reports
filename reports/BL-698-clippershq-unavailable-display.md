# BL-698 (ClippersHQ) — tell clippers the truth about earnings on deleted videos

## NO LIVE PAYOUT IS AFFECTED. Eleven requests are in flight and three belong to affected clippers: `cmosj3qk` $90.00, `cmpfozzs` $22.70 and `cmpl310f` $16.05. **None of them changes value, and none is invalidated.** `/api/earnings` performs **zero writes** (0 write calls across the entire diff), the withdrawal gate is **byte-identical**, and `lockedInPayouts` was already subtracted on both sides of the before/after comparison. All three pay out exactly as submitted. What changes for them is only what they SEE: their displayed balance drops by $3.31, $5.62 and $0.64 respectively, and the page now explains why.

**2026-07-31 · SHIPPED to `checkpoint/BL-698` @ `5ffb55f1`, verified on origin.** Base main `f7a1a344`. Tags `pre-BL-698` / `post-BL-698`. **DB `now()` at measurement: 2026-07-31 10:39:04.59334+00.** Every timestamp is `::text` against that clock.

**Redaction.** The reports repo is PUBLIC. Clippers appear as an 8-character id prefix plus BL-661's `substr(md5(userId),1,6)` short id for private reconciliation. No handle, email or wallet address anywhere.

---

## The number I almost shipped was wrong by 9x, and it would have lied to the people it was meant to help

My first version exposed the retired clips' total earnings, **$3,553.01**, as the figure to show a clipper. The accessibility review caught it. Only **$392.36** actually leaves anyone's displayed balance, because `computeBalance` floors at zero (`balance.ts:200`) and a clipper already **paid** for a retired clip was clamped at $0.00 long before this round.

Showing the larger number would have told someone who was paid in full that they had lost money they in fact received, **contradicting the policy in the same breath as explaining it**. The page is now gated on, and shows, the real per-clipper delta. This is the single most important correction in the round.

---

## PART 1 — the display now agrees with the gate

The gate at `payouts/route.ts:424` has **always** excluded clips whose video no longer exists. `/api/earnings` did not. That is the entire defect: not a wrong rule, a wrong **number on the screen**, with no explanation offered anywhere.

**The filter is in the SELECT, not the WHERE, and that is deliberate.** The same clips array also feeds `clipEarnings`, the clipper's own earnings history and chart. A `WHERE` filter would have silently emptied 26 clippers' history along with their money, which is the opposite of explaining it. The array is fetched whole and split in memory.

```diff
-            select: { id: true, earnings: true, status: true, campaignId: true, createdAt: true },
+            select: { id: true, earnings: true, status: true, campaignId: true, createdAt: true, videoUnavailable: true },

-    const balance = computeBalance({ clips, payouts, marketplaceCreatorEarnings });
-    const campaignBalances = computeCampaignBalances({ clips, payouts, marketplaceCreatorEarnings });
+    const payableClips = clips.filter((c: any) => !c.videoUnavailable);
+    const balance = computeBalance({ clips: payableClips, payouts, marketplaceCreatorEarnings });
+    const campaignBalances = computeCampaignBalances({ clips: payableClips, payouts, marketplaceCreatorEarnings });
+    const unavailableClips = clips.filter((c: any) => c.videoUnavailable && c.status === "APPROVED");
+    const balanceBefore = computeBalance({ clips, payouts, marketplaceCreatorEarnings });
+    const removedFromBalance = Math.round((balanceBefore.available - balance.available) * 100) / 100;
+      unavailableClips: { count: unavailableClips.length, removedFromBalance },
```

**This is a display alignment, not a recalculation.** No stored earnings value is written or recomputed, and BL-538's never-decrease guard is untouched **because nothing here writes at all**.

**Surfaces that change:** the earnings hero balance and the per-campaign balances (both from `/api/earnings`), and the clip card's money treatment. **Surfaces that do not:** the clip's stored earnings row, the earnings history and chart, and every already-paid figure, since `paidOut` is computed from payout rows rather than clips.

---

## PART 3 — who is affected, measured with the real `computeBalance`

**26 clippers, $392.36 leaves displayed balances.** Measured by running the actual `computeBalance` twice per clipper rather than a hand-rolled SQL copy, so these are the figures the page will really render.

| clipper | retired (n) | disappears | before | after | locked |
|---|---|---|---|---|---|
| `cmps3tgl` | 147.61 (16) | **147.61** | 147.61 | **0.00** | 0.00 |
| `cmponzpo` | 60.06 (13) | **60.06** | 81.05 | **20.99** | 0.00 |
| `cmpbazci` | 34.24 (4) | **34.24** | 34.52 | **0.28** | 0.00 |
| `cmpe951o` | 34.23 (2) | **34.23** | 34.23 | **0.00** | 0.00 |
| `cmr1rz2j` | 50.84 (32) | 19.09 | 19.09 | 0.00 | 0.00 |
| `cmpfp1mw` | 18.52 (22) | 18.52 | 18.52 | 0.00 | 0.00 |
| `cmp7153e` | 1329.31 (48) | 15.45 | 15.45 | 0.00 | 0.00 |
| `cmqgqnw4` | 11.98 (11) | 11.98 | 60.03 | 48.05 | 0.00 |
| `cmp75zkf` | 10.57 (32) | 10.57 | 13.25 | 2.68 | 0.00 |
| **`cmpfozzs`** | 32.13 (57) | 5.62 | 5.62 | 0.00 | **22.70 in flight** |
| `cmp7ic4p` | 21.92 (10) | 4.92 | 4.92 | 0.00 | 0.00 |
| `cmp5a6k0` | 3.76 (10) | 3.76 | 19.67 | 15.91 | 0.00 |
| **`cmosj3qk`** | 10.44 (12) | 3.31 | 3.31 | 0.00 | **90.00 in flight** |
| `cmpfn1e5` | 3.12 (7) | 3.12 | 4.00 | 0.88 | 0.00 |
| `cmp5j44i` | 2.99 (1) | 2.99 | 2.99 | 0.00 | 0.00 |
| `cmoibh57` | 2.82 (1) | 2.82 | 2.82 | 0.00 | 0.00 |
| `cmp48eh8` | 2.76 (5) | 2.76 | 2.76 | 0.00 | 0.00 |
| `cmpb8lbj` | 2.42 (3) | 2.42 | 2.42 | 0.00 | 0.00 |
| `cmoagj49` | 2.12 (4) | 2.12 | 6.35 | 4.23 | 0.00 |
| `cmpqxvna` | 1.51 (1) | 1.51 | 15.89 | 14.38 | 0.00 |
| `cmq2is2j` | 1.38 (21) | 1.38 | 1.38 | 0.00 | 0.00 |
| `cmn4nlfg` | 1.26 (3) | 1.26 | 155.24 | 153.98 | 0.00 |
| `cmogxget` | 0.96 (9) | 0.96 | 0.96 | 0.00 | 0.00 |
| `cmosmyqk` | 0.94 (1) | 0.94 | 1.46 | 0.52 | 0.00 |
| **`cmpl310f`** | 25.54 (21) | 0.64 | 0.64 | 0.00 | **16.05 in flight** |
| `cmp71p89` | 8.44 (22) | 0.08 | 0.08 | 0.00 | 0.00 |

**Note the gap between columns 2 and 3.** `cmp7153e` holds $1,329.31 of retired earnings but only **$15.45** leaves his balance, because he has already been paid $1,252.27. That gap is exactly why the earnings-page line must be gated on the delta and not on the retired total.

**Reconciliation with BL-695.** BL-695 measured **$387.81 across 23** using a per-campaign-reachable formula. This measures the **global display drop** across 26, days later, on a population that grew as the daily cron retired more clips. Both are correct measures of different questions.

**29 clippers hold retired earnings in total; only 26 see a balance change.** The other three were already at $0.00.

---

## PART 2B — recovery is real but rare, so the old promise is GONE

The copy that shipped until today, at `ClipCardNew.tsx:242` and `clips/page.tsx:384`, read:

> *"This video appears to be unavailable. Earnings are paused until the video is accessible again."*

**That promise is mostly unkeepable, and the code says so.** `tracking.ts:1726-1742` genuinely does clear `videoUnavailable`, clear `videoUnavailableSince` and freshly recompute earnings through `writeClipEarnings` when views return, and BL-584 spared 24 of 734 clips that had revived. So recovery is real. **But `tracking.ts:3592` excludes PAST, COMPLETED and DRAFT campaigns from the sweep**, so a retired clip on a finished campaign is never re-polled and can never recover.

Measured split of the $3,553.01 of retired money:

| where it sits | amount | can it recover? |
|---|---|---|
| ACTIVE or PAUSED campaigns | **$42.75** | yes, if views return |
| finished campaigns (PAST / COMPLETED / DRAFT) | **$3,510.26** | **no, never re-polled** |

**Only 1.2% of the money sits where recovery is possible.** So the promise is **removed, not qualified**. Nothing in the shipped copy promises recovery. Conditioning the sentence on campaign status was considered and rejected, because the reviewer established that PAUSED is not safely "recoverable" either: budget exhaustion auto-pauses a campaign (`cpm-restamp.ts:383`) and clips submitted before `lastBudgetPauseAt` are earnings-locked. A "live campaign" branch would have been a second false promise.

**Recorded as a known gap:** a revived clip on a finished campaign stays permanently unpayable, and the copy correctly does not suggest otherwise.

---

## `videoUnavailable` has TWO causes, and conflating them was the real BL-518 exposure

The owner-ban cascade at `clip-account-cascade.ts:188` **also** sets `videoUnavailable = true` when an ACCOUNT is suspended. Those videos are usually still live.

Telling that clipper *"this video is not available"* would be **false**, and it would **misattribute an enforcement action to a missing video**, contradicting a suspension notice they were already sent (`clip-account-cascade.ts:324`). That is precisely the accusation BL-518 and BL-521 forbid, and it was hiding inside a single shared flag.

`clipAccount.status` is now selected in `/api/clips/mine` (additive, read-only) so the card can tell the two apart.

---

## PART 2 — the exact copy shipped

**Clip card, ordinary case:**

> **This video is not available, so this clip cannot be paid. Videos can stop being available for lots of reasons.**

**Clip card, suspended account:**

> **This account is suspended, so this clip cannot be paid.**

**Earnings page, shown only when `removedFromBalance > 0`:**

> **Clips whose video is not available cannot be paid, so they are not counted in this balance. Money you were already paid stays yours. Your other clips keep earning as normal.**
>
> *See which clips are affected* (link to `/clips`)

**Why this wording.** *"cannot be paid"* is **agentless**: it states a consequence, names no actor, and cannot be parsed as "you did something". The cause is **never asserted** as "deleted" or "private", because the system stores no reason field and *"deleted"* is exactly the word that implies the clipper did it. *"Videos can stop being available for lots of reasons"* acknowledges it can happen outside their control without guessing which reason applies. The clawback reassurance appears **once, on the earnings page** where the drop is visible, rather than on every clip card where it would plant the idea unprompted.

**The money treatment.** An unpayable clip used to render its earnings in `text-accent`, the exact treatment of real payable money, with the green bonus pill beside it, because `showEarnings` passes for a retired clip that is still APPROVED. It now shows:

> **$0.00 PAYABLE**
> ~~$147.61~~ earned

Every number carries a **visible word**, because NVDA and JAWS announce neither `line-through` nor `<s>` by default. The strike is a CSS utility, never `<s>` or `<del>`, and the meaning survives without it. The green bonus pill is dropped in this state, since green is the paid signal and beside $0.00 it reverses the message; nothing is lost because `clip.earnings` already includes the bonus by the invariant.

**Amber is gone.** On the earnings page amber already means *"pending review, money is coming"* (`EarningsPremium.tsx:159`). Reusing it for *"money is not coming"* was an active miscue. The notice is neutral with a lucide `VideoOff`, so meaning is carried by icon plus words rather than colour alone.

**Placement and announcement.** The earnings line sits **inside the hero card, immediately under the figure it explains**, so a screen-reader user meets it while reading the balance rather than long after. Deliberately **no** `aria-live`, `role="status"` or `role="alert"`: this is content present at first paint, not a change. A `role="alert"` present at load is never announced, and a polite region on mount either misses the AT or interrupts the user's own read.

---

## A known gap, disclosed rather than hidden

The **"Approved"** stat on the earnings page is computed from `/api/clips/mine`, which is **not** filtered, while **"Available for payout"** now is. So a clipper can see **Approved $147.61** against **Available $0.00**.

**That gap is intentional.** PART 1 requires the earnings record to stay visible for audit and history, so the right fix is to **explain** the gap, which the new line does, not to erase what they earned. Filtering the Approved figure too would hide the record the round was told to preserve.

---

## PART 4 — what did not change, proven

| must not change | evidence |
|---|---|
| the withdrawal gate | `payouts/route.ts` **byte-identical**, `a9c7164e973b5dc4140172a0ed01c982b0ff7f44` |
| any stored earnings value | **zero write calls in the entire diff** (`grep -c` on added lines = 0) |
| BL-538's never-decrease guard | unaffected; nothing writes |
| any historical payment | `paidOut` is computed from payout rows, not clips, and no payout row was touched |
| campaign budget, spend, pool cap, owner accrual | none appears in the diff; the changed files are two read endpoints and two display components |
| the 6 money files + `tracking.ts` + `campaign-era.ts` | byte-identical by blob OID: `7aa6be48`, `797e2098`, `e887f80a`, `847dcf70`, `61cef393`, `ef5cdae7`, `106e16ad` |

---

## PART 5 — evidence

| claim | evidence |
|---|---|
| displayed balance now matches what can be withdrawn | both sides now use the same payable-clip base as `payouts/route.ts:424` |
| a deleted-video clip shows the explanation at $0.00 payable | copy and markup quoted above; earned figure struck through and labelled |
| a clipper with only live clips sees no change | `PASS nobody's displayed balance INCREASES`; only 26 of ~220 drop. `cmqez5c2` (110 clips, $1,865.67, zero retired) is unaffected |
| no stored earnings value moved | zero writes; APPROVED total **$10,208.93** across 3,675 clips, unchanged and above BL-693's $10,191.26 |
| earnings invariant | **0 violations**: APPROVED 3675, FLAGGED 6, PENDING 7, REJECTED 871 |
| no payout created, modified or cancelled | **146 rows, $14,162.14, 11 in flight**, newest still `2026-07-31 10:18:22.921` |
| no displayed balance goes negative | `PASS no displayed balance goes negative` |

---

## The accessibility review, and what it changed

It ran **before** any UI was written and it materially changed what shipped. Three of its findings were decisive and I have credited them above rather than presenting them as my own: the **9x wrong number**, the **account-ban conflation**, and the fact that a **PAUSED campaign is not safely recoverable** either, which killed the conditional wording I had planned.

Also applied: neutral styling instead of amber, the `$0.00 payable` treatment with a CSS-only strike and a visible word on every number, dropping the green bonus pill, the no-live-region ruling, placement inside the hero card, and the "See which clips are affected" link for SC 2.4.4 and 2.4.9.

**Deliberately not actioned, with reasons:** it recommended patching the legacy clip card at `clips/page.tsx:384`, but it separately established that `clips/page.tsx:57,65` are hard-coded `true` so everything below line 330 is **dead code**; patching it would have been noise. It also flagged that `globals.css:43-45` sets `--text-primary`, `--text-secondary` and `--text-muted` all to `#ffffff`, so muted tokens give zero de-emphasis, which is why the new copy uses `text-white/80` and `text-white/70` rather than the muted token. It logged that as a separate BACKLOG item, not this round.

**Two of its specialists were still running when it reported.** It said so plainly and did not wait to assert conclusions it had not verified, and it noted its Q1 single-sentence ruling rests on the campaign-status and ban-cascade facts rather than on style, so late style input could not overturn it.

**One caveat it raised that I could not fully close:** `globals.css:113` defines a `.light` theme in which `--bg-card` is `#ffffff`. It found no code applying that class, and neither did I, but if anything ever does, the amber it replaced would have read at about 1.5:1 there. The neutral treatment now shipped is less exposed to that, but the light theme remains unverified territory.

---

## Gates, stated honestly

* **`npm ci` exit 0**, then **`npx prisma generate` exit 0**, before typecheck.
* **`npx tsc --noEmit` exit 0**, **0 lines** of output.
* **`npm run build` BUILD_EXIT=0**, read from a captured log, never piped through `tail`. BYPASS detector **0 violations across `src/` + `scripts/`** including its earnings-write check, `check:removed-fields` OK, `lint:hooks` **11 problems (0 errors, 11 warnings)** at the ≤11 cap, compiled successfully, **61/61** pages.
* **eslint v9.39.4 present**, so the hooks gate is real.
* The real diff is non-empty: **4 source files** plus four read-only measurement scripts and `BACKLOG.md`. Counts by `grep -c`, never `head`. **No heredocs used**; every file was written with the file tool and shells were run one at a time.
* **No `prisma migrate`. `GLOBAL_PAYOUT_CLAMP_ENABLED` not flipped. No Apify actor run.** Every timestamp `::text` against DB `now()`.
* **NO dashes** as bullets. Isolated worktree at the short path `C:/b698`, `node_modules` never junctioned.

**Rollback:** `git revert 5ffb55f1`, or `reset --hard pre-BL-698`. Reverting restores the previous behaviour, which is 26 clippers seeing $392.36 they cannot withdraw, with no explanation.
