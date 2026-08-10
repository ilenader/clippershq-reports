# BL-764 — merge BL-762 (tell a clipper why he cannot withdraw) to main

**Result: MERGED AND VERIFIED PUSHED.** main `018c22ca` → **`4f1f7113`**. Merge only. Display and
messaging only: **not one clipper's withdrawal verdict changed**, proven by an identical fingerprint
over all 160 (clipper, campaign) positions before and after the push.

## STEP 0 — truth, recorded before anything was merged

| Question | Answer |
| --- | --- |
| Was checkpoint/BL-762 on origin? | Yes, **`e35a58e088a4f8156d206847ce5b998d7bdfb5e3`** |
| Genuinely NOT an ancestor of main? | Yes. `git merge-base --is-ancestor origin/checkpoint/BL-762 origin/main` → **NO-NOT-ANCESTOR** |
| Non-empty diff? | Yes. **4 files, 393 insertions, 24 deletions**, two commits `f9285753` and `e35a58e0` |
| Was BL-723 merged? | **No.** Re-asserted after the push: `origin/checkpoint/BL-723` is still NOT an ancestor of main |
| main starting point | `018c22ca` |

### tsc baseline, recorded on a CLEAN worktree BEFORE merging

```
TSC_BASE_EXIT=0   BASE_ERR_COUNT=0
```

**0 errors.** Recorded first, so every later number is measured against a proven-clean start rather
than assumed. The prior round that reported "2 pre-existing errors" had stray files in its own
worktree; this baseline was taken on a worktree created seconds earlier from `origin/main` with
`git status` showing **0 entries**.

### How the worktree situation was handled

**Every other worktree is gone.** BL-761 removed 151 of them, and `C:/b762` removed itself between the
start of this round and the merge, so `git worktree list` showed only the owner's working copy.

`git checkout main` was still NOT run in that working copy, and the reason is concrete rather than
cautious: **the local `main` ref is stale at `91b84410`**, roughly 180 commits behind. Checking it out
would have dragged the owner's OneDrive-synced tree backwards through every one of those commits and
then forwards again on the pull, churning ~1,380 files for no benefit, when the tree is already
detached at exactly `018c22ca` = `origin/main`.

So the merge was done in a **separate clean worktree at a short path, `C:/m764`**, created detached at
`origin/main`, with `.env` and `.env.local` copied in and **no node_modules junction** (`npm ci` ran
natively). The push was `git push origin HEAD:main` with the BL-288 assertion performed explicitly,
because `safe-push.mjs` takes a branch name and would have pushed the stale local `main`. **The
worktree was removed at the end** and the owner's working copy is byte-for-byte as it was.

## THE MERGE

`git merge --no-ff origin/checkpoint/BL-762` → `MERGE_EXIT=0`, **clean, zero conflicts**, so no union
resolution was needed. Merge commit **`4f1f71135abc13e30cbc3e0fe4136d83132b6743`**.

* **Conflict markers: 0.** `git grep -E '^(<<<<<<<|>>>>>>>)'` over the whole tree returns 0.
* **BACKLOG union, counted with `grep -c` and never piped to `head`:** main **135** entries,
  BL-762 **136**, merged **136**. Entries from main missing in the merged file: **0**. Added: **1**,
  `## BL-762 (2026-08-10) — tell a clipper WHY he cannot withdraw, where he already is`.

## GATES — every one actually run, with its real exit code from a log

| Gate | Result |
| --- | --- |
| npm ci, run FIRST | `NPMCI_EXIT=0` |
| eslint present | **PRESENT** at `node_modules/.bin/eslint`, so the hooks gate did not silently no-op |
| prisma generate, BEFORE tsc, and again after the merge | `PRISMA_EXIT=0`, client 7.8.0 |
| tsc | `TSC_MERGED_EXIT=0`, **0 errors, unchanged from the recorded baseline of 0** |
| **next build** | **`BUILD_EXIT=0`**, echoed from a real run, never piped through `tail` |
| hooks gate | `HOOKS_EXIT=0` — **0 errors, 11 warnings**, exactly at the 11 limit |
| prebuild chain | `check:prisma-bypass` + `check:removed-fields` + `lint:hooks` all ran inside the build |

## CONFIRM ON THE MERGED RESULT, BY CODE READING

No clipper's state was altered to test any of this. Everything below is read from the merged tree.

### Both screens state campaign, balance, minimum and shortfall with no click

**The payouts screen**, `PayoutsRedesign.tsx:301-315`. The explanation sits inside `{!canRequest && ...}`,
which renders **at first paint**, in the hero, beside the disabled button. It is not inside the payout
flow and not behind the button. That is the whole point of the round: BL-728 had already written the
sentence and BL-734 had already deduplicated the minimum, but both lived **inside a flow opened by a
button that is `disabled` whenever the global balance is $0.00**, which is precisely the state of the
clipper who raised this. BL-689 predicted it in as many words: he "will see it only if they reach the
flow by another route".

The per-campaign strip at `:354-390` then names each campaign, its balance, its own minimum
(`{formatCurrency(c.available)} of {formatCurrency(c.minPayout)} minimum`) and the gap
(`{formatCurrency(shortfallToMinimum(c))} to go`), with a screen-reader sentence on every row.

**The earnings screen**, `EarningsPremium.tsx:162-180`, renders under `{minimumSplit.blocked.length > 0 && ...}`,
also at first paint, stating the blocked total, how many campaigns, and a link to where the per-campaign
detail lives.

### The figures come from the gate's own values, not a duplicate

This was the specific risk, because BL-734 found **seven scattered copies** of the minimum and two had
gone stale.

* `below-minimum-campaigns.ts:52` imports **`toCents` from `@/lib/payout-minimum-shared`**, the same
  function the server gate compares with. `clearsMinimum` at `:100` is
  `toCents(available) >= toCents(minPayout)`, so a campaign this file calls blocked is exactly a
  campaign the gate would refuse. No float comparison can put a message on screen that contradicts
  the block.
* `PayoutsRedesign.tsx:31` imports **`belowMinimumMessage`** from the same shared module and uses it
  verbatim at `:304` and `:390`. **Two surfaces, one string.**
* `minPayout` is never a literal. It arrives per campaign from `/api/earnings`, already resolved
  server-side by `resolveMinPayout` (which turns a NULL column into the $10 platform default).
* **Checked directly:** the only numeric literals resembling a minimum anywhere in the two components
  are `min-h-[44px]` CSS touch targets and two figures inside explanatory comments. **Zero hardcoded
  minimums in executable code.**

### Nothing about money changed

* `below-minimum-campaigns.ts` is a **pure function module**: it takes rows, sorts them into two
  arrays, and sums. It writes nothing, imports no client, and is on no path that can reach a balance,
  an eligibility rule or a payout.
* The diff touches **4 files**: `BACKLOG.md`, two React components and one new pure library. **No API
  route, no gate, no server logic.**
* A row with a zero or negative balance lands in neither list (`:119`), so the screen cannot invent a
  grievance or print a shortfall equal to a whole minimum.
* The blocked figure is the **sum of what is under a minimum, never the whole balance**, which is the
  wrong-number trap BL-698 caught in review.

### Copy stays plain and non-accusatory

The below-minimum sentence explains a campaign rule and says what each campaign still needs. BL-689's
support-ticket wording is **preserved unchanged for everyone it was written for**: the below-minimum
case is tested first and only what is left over reaches it (`:302-313`). Nobody who was getting a
correct message stops getting it. No dashes as bullets, no emoji, lucide-react icons only, CSS
variables rather than hardcoded colours, and the component notes explicitly that it does not reuse
BL-698's `bg-white/[0.04]` because that is white-on-white in the light theme.

### The 8 protected files are byte-identical by blob OID

Verified with `git show` on **both refs and the merged HEAD**, all three equal, and none appears in the
diff:

```
clip-earnings-writer.ts             ac5be7deb061768fec800aa89aae512a56a9e065
earnings-calc.ts                    797e20985ad57475ef321afcf3cb1ea7b0d6ab84
balance.ts                          e887f80acfc70fee438e719a32a60025eda22749
tracking.ts                         83ce4babfd39a6261114465639f2eac4e23bfceb
clip-earnings-invariant-middleware  61cef39395363c31f0c902dd4c64e8c06b3e6449
money-decimal.ts                    ef5cdae757b9ad3c23380ee8b63e279f98d0b6ac
campaign-era.ts                     106e16ad75125c3b10b6949a2981d33614c69ab9
```

That is the 6 money files plus `campaign-era.ts`. **`tracking.ts` is not in the diff.**

## AFTER THE PUSH — CONFIRMATION FROM LIVE DATA THAT NOTHING MOVED

Every timestamp cast `::text` against DB `now()`. Handles redacted, no wallet address selected.

| Measure | Before push `17:55:11` | After push `17:56:09` |
| --- | --- | --- |
| **Withdrawal verdict fingerprint** (md5 over every clipper+campaign position, its available balance, its minimum and its CAN/CANNOT verdict) | `10fc6d70633c535d4a30110369118564` | **`10fc6d70633c535d4a30110369118564` — IDENTICAL** |
| **Clippers below their minimum** | **112** | **112** |
| **Amount held below minimum** | **$432.18** | **$432.18** |
| Positions below minimum | 137 (clipper, campaign) pairs | 137 |
| Clippers who CAN withdraw | 23 | **23** |
| Amount withdrawable | $2,021.80 | **$2,021.80** |
| payout_requests rows | 165 | **165** |
| Payout fingerprint (id, status, amount, finalAmount, paidAt) | `13f44d060fd0d06d49a8e6d62868a6d3` | **`13f44d060fd0d06d49a8e6d62868a6d3` — IDENTICAL** |
| Clip fingerprint (id, earnings, status) over 5,360 clips | `0521826eba656d68686b76d6e02de265` | **`0521826eba656d68686b76d6e02de265` — IDENTICAL** |
| Earnings invariant violations | 0 | **0** |
| Campaigns over budget | — | **0** |

**The below-minimum population reads exactly the 112 clippers holding $432.18 that BL-762 measured**,
independently recomputed here from clips, payouts and each campaign's own `minPayoutAmountDecimal`
(NULL resolving to the $10 platform default), not read from that report.

**Not one withdrawal verdict flipped.** The fingerprint covers all 160 positions with a positive
balance and encodes each one's CAN or CANNOT verdict; an identical hash before and after is a stronger
statement than counting the two populations, because it would change if any single clipper crossed the
line in either direction. **Nobody became newly able or unable to withdraw.**

**No payout was created, modified, approved or cancelled**, and no clip's earnings or status changed.

## SAFETY LEDGER

* Merge only. The diff is 2 React components, 1 new pure module and BACKLOG.
* No eligibility rule, minimum, balance or earnings changed. No server route touched.
* The displayed minimum reads the gate's own `toCents` and `belowMinimumMessage`, never a duplicate.
* Copy plain and non-accusatory; BL-689's wording preserved for the cases it was written for.
* BL-723 **not** merged, re-checked after the push.
* 6 money files + `campaign-era.ts` byte-identical by blob OID on both refs and the merge.
* No `prisma migrate`. No Apify actor. No clip status, earnings or payout touched.
* Worktree `C:/m764` **removed**; `git worktree list` shows only the owner's working copy.
* Handles redacted, no wallet address printed, every timestamp `::text`. No dashes as bullets.

## HONEST RESIDUALS

* **This round fixes the explanation, not the trap.** The 112 clippers still cannot reach their
  $432.18, and 17 of them are on WinGram, an archived campaign whose accrual is frozen, so they can
  never reach it by earning. BL-763 named that as the ongoing defect. **BL-762 makes the wall visible;
  it does not remove it.** Do not read the merge as having paid anyone.
* Everything in the CONFIRM section is established by code reading against the merged tree. No browser
  session and no screen-reader pass was run this round, and no clipper's state was altered to test the
  rendering, which was the instruction.
* The hooks gate sits at **exactly 11 of its 11 permitted warnings**. It passes, but there is no
  headroom, and the component notes say the `useMemo` was deliberately omitted for that reason. The
  next round that adds a hook dependency warning will fail the gate.

## ROLLBACK

```
git revert -m 1 4f1f71135abc13e30cbc3e0fe4136d83132b6743
```

or `git reset --hard pre-merge-BL-764` (`018c22ca`). Both tags are on origin. **No data rollback
exists or is needed: this merge wrote no data.**

## PUSH VERIFICATION (BL-288)

```
local HEAD  = 4f1f71135abc13e30cbc3e0fe4136d83132b6743
origin/main = 4f1f71135abc13e30cbc3e0fe4136d83132b6743
VERIFIED PUSHED — origin == local
tags on origin: post-merge-BL-764 -> 4f1f7113, pre-merge-BL-764 -> 018c22ca
```
