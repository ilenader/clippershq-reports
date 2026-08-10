# BL-766 — merge BL-765 to main: the per-campaign reminder, and the clamp that hid its predecessor

**2026-08-10 · DB now() = `2026-08-10 20:22:13.714982+00` · MERGE ONLY. No code authored.**
`main` **4f1f7113 → 9d285c8c**, pushed and confirmed on origin. Tags `pre-merge-BL-766` (`4f1f7113`) and `post-merge-BL-766` (`9d285c8c`) both on origin. Display and messaging only: no eligibility rule, minimum, balance or earnings changed and no clipper became newly able or unable to withdraw. `src/app/api/payouts/route.ts` is not in the diff. No `prisma migrate`. Handles redacted, no wallet address printed, every timestamp cast `::text` against DB `now()`.

---

## STEP 0 — TRUTH, BEFORE ANYTHING WAS MERGED

| check | result |
|---|---|
| `origin/checkpoint/BL-765` | **`9d9c19369b0f55cfb0a1152ebf27173771d2a571`**, present on origin |
| `origin/main` before the merge | **`4f1f71135abc13e30cbc3e0fe4136d83132b6743`** (the BL-764 merge of BL-762) |
| Genuinely unmerged? | **YES.** `git merge-base --is-ancestor origin/checkpoint/BL-765 origin/main` exited **1** |
| Diff non-empty? | **YES.** 6 files, **+400 / −29** |
| `checkpoint/BL-723` merged? | **NO.** It is not in `origin/main..origin/checkpoint/BL-765` (`grep -c` = 0) and was never fetched into the merge. It targets business-api and cannot be called by the owner's Login Kit app. |

### The dirty worktree, and how it was handled

The primary repo was **not** usable for this merge, for two independent reasons, and I did not force either:

• Its `HEAD` sat **detached at `018c22ca`**, one merge behind `main`, carrying **8 untracked files** from other sessions (`.claude/`, `docs/BL-533-MERGE-REPORT.md`, `docs/SCRAPBADGER-TIKHUB-AUDIT.md`, and five stray `.html` files).
• The local `main` **branch ref** is checked out by another worktree, `C:/b575`, and is stale at `91b84410`.

So the merge ran in a **separate clean worktree at a short path, `C:/m766`**, detached at `origin/main`, `git status --porcelain` empty at creation. It was pushed as `HEAD:main` and **removed at the end of the round** (confirmed gone, 0 junctions, `node_modules` was a real `npm ci` install and never junctioned). The primary repo and `C:/b575` were left **exactly as found**: `main` still reads `91b84410` locally and the 8 untracked files are untouched.

### The clean tsc baseline, recorded BEFORE merging

On the clean worktree at `4f1f7113`, after `npm ci` (exit 0) and `npx prisma generate` (exit 0, client generated):

> **`TSC_BASELINE_EXIT=0`, `grep -c "error TS"` = 0.**

That baseline is why the post-merge figure below can be attributed to the merge rather than to inherited noise.

---

## THE MERGE

`git merge --no-ff origin/checkpoint/BL-765` → **`MERGE_EXIT=0`**, merge commit **`9d285c8c`**.

**There were no conflicts.** The union instruction therefore had nothing to resolve, and I would rather say that than imply work I did not do. The BACKLOG proves it arithmetically:

| | entries (`grep -c "^## BL-"`, never piped) |
|---|---|
| `main` before | **136** |
| `checkpoint/BL-765` | **137** |
| **merged result** | **137** |
| BL-765's own entry present | **1** |

136 + 1 = 137. Every entry kept, none dropped, none duplicated.

**Conflict markers: 0.** A loose first pass matched 5 files, and I checked rather than reported it: `FULL-REPORT.txt`, `LAST-RESULT.txt`, `SCALING-REPORT.txt`, `VERIFICATION-RESULTS.txt` and `VERY-IMPORTANT.txt` contain `=======` as decorative separators in pre-existing report prose. A precise pattern (`^<{7} `, `^={7}$`, `^>{7} `) returns **0**.

The merge touched **6 files** and neither `package.json`, `package-lock.json` nor `prisma/schema.prisma` is among them (`grep -c` = 0), so the baseline install and generated client remained valid.

---

## THE GATES, STATED HONESTLY

`eslint` **is present** in the worktree's `node_modules/.bin` (`grep -c "^eslint$"` = 1), so the BL-348 hooks gate is a real check and not a silent no-op. `npm ci` ran **first**, and `npx prisma generate` ran **before** every `tsc`, because `npm ci` wipes the generated Prisma client.

| gate | baseline at `4f1f7113` | merged `9d285c8c` |
|---|---|---|
| `npm ci` | **exit 0** | not re-run; no dependency file changed |
| `npx prisma generate` | **exit 0**, client generated | still valid |
| `npx tsc --noEmit` | **exit 0**, 0 errors | **exit 0**, 0 errors, **unchanged** |
| `npm run build` (runs `prebuild`) | | **`BUILD_EXIT=0`**, compiled in 31.3s |
| `lint:hooks` | | **`HOOKS_EXIT=0`**, 0 errors, **11 warnings** |

Every exit code was captured with `echo "..._EXIT=$?"` immediately after the command and read from a log, never through a pipe. The gate permits `--max-warnings 11` and sits at exactly 11, so this merge had to add zero and did.

### The money files

Blob OIDs via `git rev-parse` on **both** refs, `4f1f7113` and the merged `9d285c8c`:

| file | blob OID | |
|---|---|---|
| `clip-earnings-writer.ts` | `ac5be7deb061` | **IDENTICAL** |
| `earnings-calc.ts` | `797e20985ad5` | **IDENTICAL** |
| `balance.ts` | `e887f80acfc7` | **IDENTICAL** |
| `tracking.ts` | `83ce4babfd39` | **IDENTICAL** |
| `clip-earnings-invariant-middleware.ts` | `61cef3939536` | **IDENTICAL** |
| `money-decimal.ts` | `ef5cdae757b9` | **IDENTICAL** |
| `campaign-era.ts` | `106e16ad7512` | **IDENTICAL** |

---

## CONFIRMED ON THE MERGED RESULT, BY CODE READING

No clipper's state was altered to test any of this.

**A blocked row states balance, minimum and shortfall.** `EarningsPremium.tsx:395` renders `{formatCurrency(balanceOnCampaign(c.row))} of {formatCurrency(c.row.minPayout)} minimum`, and `:399` appends `• {shortfallToMinimum(c.row)} to go`.

**A row on a campaign that can never accrue reads as finished and shows NO shortfall.** `:397-398` selects `"• campaign finished, so this balance will not grow"`, and the `to go` string at `:399` is the **else** branch only, so it is unreachable for a finished row. The payouts side matches at `PayoutsRedesign.tsx:415-419` (`"will not grow"` in place of `"to go"`) and its spoken sentence at `:423-425` carries no target. **`shortfallToMinimum` is never called on a finished row on either screen.** This matters because 85 clippers holding $262.69 sit on such campaigns, and the owner has confirmed that frozen state is settled policy, so the copy had to stop instructing them to do something impossible.

**A healthy row is untouched.** `:389` gates the reminder on `c.row && c.state && c.state !== "ready"`, so a withdrawable row renders no reminder block at all and its visual markup is the pre-existing row.

**The clamp defect is fixed.** `below-minimum-campaigns.ts:186` now reads `if (!row || balanceOnCampaign(row) <= 0) continue`, the **unclamped** balance, so a clipper whose global figure is $0.00 keeps his per-campaign rows instead of having them dropped. `/api/earnings` supplies `campaignBalance` and `canAccrue` additively, and all three consumers read them (`payouts/page.tsx`, `EarningsPremium.tsx`, `below-minimum-campaigns.ts`).

**Nobody can withdraw more than before, by construction.** `clearsMinimum` at `below-minimum-campaigns.ts:161-162` still compares `toCents(row.available)`, the **clamped** figure. So `ready` is decided by exactly the number it was decided by before the merge; only rows the clamp had flattened enter `blocked`, the group that by definition offers nothing.

**Zero hardcoded minimums.** A literal scan returned 10 hits and I inspected every one: all are either explanatory prose inside comments citing example figures, or `minimumSplit.blocked.length === 1` style comparisons the regex caught. **No rendered figure is a literal.** Every displayed minimum is `c.minPayout`, which is `resolveMinPayout(campaign.minPayoutAmountDecimal)` resolved server-side.

**The two screens cannot disagree.** Both import `belowMinimumMessage` from `payout-minimum-shared.ts` (`EarningsPremium.tsx:34`, `PayoutsRedesign.tsx:31`) and both classify through `below-minimum-campaigns.ts`, which imports `toCents` from the same module at `:52`. The server gate imports the same two names at `payouts/route.ts:25`. One predicate, one sentence, one source.

### Accessibility, verified on the merged tree

BL-765 was reviewed by the accessibility lead **before** it was written. Because this merge lands that UI on main, the lead re-verified the merged tree by code reading. **No regression, nothing blocking.** Every property confirmed with a line reference: one `sr-only` sentence per row with all numeric fragments `aria-hidden` (`:367`, `:368`, `:372`, `:390`, sentence `:410-420`); both figures self-scoped in words, since the earned amount is period-scoped and the balance is all-time (`:411` "earned in the period shown", `:413/:417/:419` "Your balance on this campaign is"); no `aria-live`, `role="status"` or `aria-atomic` on this first-paint content; reminder text on `--text-secondary` and `--text-muted`, never `text-accent`, with the lead independently recomputing `#2596be` on white as **3.40:1**, matching the code comment; campaign name spoken once from the visible node; list semantics and heading levels intact on the payouts strip.

Two items logged, **neither introduced by this merge**:

• **A mixed group heading.** `PayoutsRedesign.tsx:384` reads "Not at the minimum yet" whenever the blocked group is mixed, so on a group of, say, three growing campaigns and one finished one, the word "yet" sits above a campaign that cannot grow. Every such **row** still self-corrects at `:400` ("Campaign finished") and `:417` ("will not grow"), so no row claims growth. Minor, and worth a follow-up.
• **Two 12px `text-accent` links** at `EarningsPremium.tsx:250` and `:436` fail 1.4.3 for normal-size text in the light theme at 3.40:1. This is the same pattern as the pre-existing BL-698 link at `:199` and several in `PayoutsRedesign.tsx`, so it is **systemic and pre-existing**, not a regression. Both are underlined, so link identification never depends on colour.

---

## AFTER THE PUSH — NOTHING MOVED

Measured on live data at `2026-08-10 20:22:13.714982+00`.

| | BL-765 pre-merge | now | verdict |
|---|---|---|---|
| Positions with a balance | 165 | **165** | unchanged |
| **Positions that CAN withdraw** | **26** | **26** | **unchanged** |
| **Clippers who can withdraw** | **23** | **23** | **unchanged** |
| Below-minimum positions | 139 | **139** | unchanged |
| Below-minimum clippers | 112 | **112** | unchanged |
| Below-minimum dollars | $433.59 | **$435.84** | +$3.66 accrual |
| Previously-invisible positions | 3 | **3** | unchanged |
| Previously-invisible clippers | 2 | **2** | unchanged |
| Previously-invisible dollars | $13.49 | **$13.52** | +$0.03 accrual |
| Frozen positions / clippers / dollars | 93 / 85 / $262.69 | **93 / 85 / $262.69** | unchanged to the cent |

**No withdrawal verdict flipped.** The can-withdraw set is 26 positions across 23 clippers before and after, and the below-minimum set is 139 across 112. The brief cited 160 positions and $432.18 from BL-764; the live figure is **165 positions and $435.84**, and the difference is ordinary tracking-cron accrual on ACTIVE campaigns over the intervening days, not merge effect. Position and clipper **counts** are identical, which is the invariant that matters.

**The 3 previously-invisible positions across 2 clippers still exist and now render.** They are the rows whose clamped figure is $0.00 while their real balance is positive; before this merge `payouts/page.tsx` dropped them and `splitCampaignsByMinimum` received nothing. The inclusion test now reads the unclamped balance, so they reach the blocked group and state their position. That is a code-path fact, verified by reading `below-minimum-campaigns.ts:186`, not by altering anyone's data.

**No payout was created, modified, approved or cancelled.** 165 payout rows, newest `createdAt` **`2026-08-09 23:44:41.815`** and newest `updatedAt` **the same timestamp**, both a day before this round began. **0 rows touched in the last 3 hours.**

**The earnings invariant is at zero violations:** `|earnings − (baseEarnings + bonusAmount)| > 0.01` returns **0** across **4,332** approved live clips holding **$12,185.87**. Two campaigns carry a custom minimum, the owner's own two $20.00 raises.

---

## THE HONEST LIMIT THE OWNER MUST CLOSE HIMSELF

**The page was never rendered in a browser, and I am not claiming it was.** The clipper earnings page sits behind a Discord OAuth session neither BL-765 nor this round had, so every claim above is from **code reading and live database measurement**. The logic is proven; the pixels are not.

Three things specifically **cannot** be settled without a real clipper login, and the accessibility lead named them as such:

1. Whether the reminder line lays out cleanly beside each campaign at 320px through 1440px.
2. Whether the hero's in-page anchor actually moves DOM focus to the "Earnings by campaign" heading under the Next App Router, rather than only scrolling. If focus does land, `outline-none` on that heading means there is no visible focus ring.
3. Rendered contrast in the live light theme.

**Please open your own clipper account on `/earnings` and check the campaign rows.** You should see, beside a blocked campaign, a line of the form "$12.19 of $20.00 minimum • $7.81 to go"; beside a finished campaign, "campaign finished, so this balance will not grow" and no target; and beside a withdrawable campaign, nothing at all.

---

## ROLLBACK

`git revert -m 1 9d285c8c`, or `git reset --hard pre-merge-BL-766` (`4f1f7113`) before anything else lands. **No data rollback exists or is needed: this merge wrote nothing to the database.**

---

## VERIFICATION

BL-765 was genuinely unmerged (`--is-ancestor` exit 1) at `9d9c1936` with a non-empty 6-file, +400/−29 diff; a clean-worktree tsc baseline of exit 0 and 0 errors was recorded at `4f1f7113` before merging; BL-723 was not merged and is absent from the merged range; the dirty primary repo was left exactly as found and the merge ran in a separate clean short-path worktree that has been removed, with `node_modules` a real install and never a junction. On the merged tree a blocked row states balance, minimum and shortfall, a never-accruing row reads as finished with no shortfall on either screen, a healthy row renders no reminder, a clipper with a $0.00 global balance keeps his per-campaign rows, every figure reads the gate's own `toCents` and `belowMinimumMessage` with zero rendered literals, and both screens classify through one module. After the push no withdrawal verdict flipped across all 165 live positions (26 can withdraw, 23 clippers, before and after), the below-minimum figure is 139 positions / 112 clippers / **$435.84**, the 3 previously-invisible positions across 2 clippers now render, no payout was touched (0 rows updated in 3 hours), and the earnings invariant is at 0 violations across 4,332 clips. The 6 money files plus `tracking.ts` and `campaign-era.ts` are byte-identical by blob OID on both refs. BACKLOG unioned to 137 from 136 + 1 with a properly counted `grep -c`, no conflict markers, `npm ci` clean, `prisma generate` before every `tsc`, tsc unchanged from baseline, `next build` actually run at `BUILD_EXIT=0` from a log, hooks gate `HOOKS_EXIT=0` at 0 errors and 11 warnings with eslint confirmed present. `origin/main == 9d285c8c == local`. The browser render is stated as unverified. No dashes as bullets.
