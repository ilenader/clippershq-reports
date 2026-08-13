# BL-801 — the interrupted merge round, recovered

**NOTHING IS BROKEN ON MAIN. No protection is missing or half applied, and the live product is not exposed.** The BL-800 round had already FINISHED and PUSHED before the machine restarted. All eight branches are merged, the report was published, and the restart interrupted nothing. **No merge was performed in this round, and origin/main was not moved.**

## PART 1 — the state, established before anything was written

The single strongest signal answered itself: **reports/BL-800-clippershq-merge.md EXISTS on origin** (16,444 bytes, tracked at `reports/BL-800-clippershq-merge.md`). My first fetch 404'd only because I guessed the wrong GitHub owner; the repo is `ilenader/clippershq-reports`, and the file is there. The round reached its final step.

| question | answer |
| --- | --- |
| origin/main tip | `d004b396` — "BL-800: merge round report…", authored **2026-08-12 23:31:40 +0200**, committed **00:31:40 +0200** |
| local main tip | `d004b396` — identical, no divergence, nothing stuck locally |
| main BEFORE the chain | `72f05cec` (BL-779 merge report, 2026-08-11 22:27:43 +0200) |
| how far main moved | **10 commits**: eight `--no-ff` merges plus the carried branch commits, then the report commit |
| HEAD | `main` @ `d004b396`, clean |

**Ancestry — all eight landed, and BL-723 correctly did not:**

| branch | SHA | ancestor of origin/main |
| --- | --- | --- |
| checkpoint/BL-788 | `7e57130c` | YES |
| checkpoint/BL-790 | `338ad3a5` | YES |
| checkpoint/BL-791 | `3970ff7c` | YES |
| checkpoint/BL-793 | `89e3579b` | YES |
| checkpoint/BL-794 | `9100adc6` | YES |
| checkpoint/BL-796 | `87d50ba3` | YES |
| checkpoint/BL-797 | `18ef695f` | YES |
| checkpoint/BL-799 | `abe11484` | YES |
| checkpoint/BL-723 | `22039307` | **NO — correctly not merged** |

Each merge commit is present and in dependency order: `8fd1d7ef` BL-788 → `835b377c` BL-790 → `adf1d71d` BL-791 → `9ea56aa2` BL-793 → `a211fde3` BL-794 → `862d11f9` BL-796 → `6fc06f52` BL-799 → `5f6fbd62` BL-797.

**Worktrees.** `git worktree list` reports exactly ONE: the main repo at `…/ClippersHQ`. **No MERGE_HEAD anywhere, no conflict markers (0 across ts/tsx/md), no dirty tracked files (0).** `C:/b575`, `C:/b796`, `C:/b798` do not exist. Two unregistered leftovers do exist, `C:/b791` and `C:/bl790` — **each contains only a `.next` build cache, no `.git`, no source, nothing unique.** I left both exactly as found and cleaned nothing.

**Local-only commits — the one real recovery finding.** Seven branches carry a commit that exists nowhere on origin (five have the branch name on origin but the local tip is one commit ahead; two have no remote branch at all): `checkpoint/BL-361 1b9e21b1`, `BL-363 fe9650ac`, `BL-365 2fbc7ef4`, `BL-367 c19c00fb`, `BL-368 0c5a8c98`, `BL-597 75bc0512`, `BL-600 b5feceec`. **All are dated 2026-07-11 to 2026-07-20 — none is from the interrupted round**, but all would have been lost with the folder. Preserved in PART 4.

**Stashes: 13**, all pre-existing (BL-447 through BL-483 era, plus three WIP entries from BL-384/BL-404/BL-420). None touched.

**Uncommitted work: none.** The working tree has **0 tracked changes**. Nine untracked paths exist; the newest was last modified **2026-08-12 20:24:59**, which is *before* the first merge at 22:50. **Nothing was mid-write when the machine restarted.**

## PART 2 — is main safe right now: YES, and proven by direct request

Baseline on the clean tree at `d004b396`, with **eslint v9.39.4 confirmed present** (otherwise the hooks gate silently no-ops):

- **tsc: exit 0, `grep -c "error TS"` = 0**
- **build: `BUILD_EXIT=0`** (echoed from the log, never piped through `tail`). Prebuild gate: prisma-bypass 0 violations, removed-fields OK, **hooks 0 errors / 11 warnings**. Compiled in 36.8s, 61/61 static pages generated.

No half-applied chain is possible, because every base landed before its dependent. Proven by **asking the server**, not by reading code — `next dev --webpack` on :3800 with the dev-auth cookie:

| protection | result |
| --- | --- |
| Reviewer 403 on owner-only money and admin surfaces | **7/7 got 403**: payouts, agency-earnings, accounts, admin users, unpaid payouts, audit log, owner ratification queue |
| …and the same routes are alive | **7/7 got 200 as OWNER** |
| Six capability checkboxes gated server-side | **6/6 got 400** written onto a non-reviewer (TRACK_NOW, CAMPAIGN_VIEW, ACCOUNT_VIEW, ANALYTICS_VIEW, EARNINGS_VIEW, PAYOUT_VIEW); the REFERRAL_MANAGE ride-along still 200 |
| Full authority off by default behind the typed phrase | **LIVE with no phrase → 400; LIVE with a wrong phrase → 400**; TRIAL back → 200; LIVE with the correct phrase → 200 |
| Invitee scope defaults ON at grant time | fresh REVIEWER grant returns `reviewerScopeInvitedOnly` **true**; demote returns false |
| Partner sees only his own invitees, failing closed at zero | **unscoped 200 with 42 pending clips across 11 clippers → scoped 200 with 0 clips.** Fails closed |
| Reviewer without `canActAsClipper` reaches every clipper page | **6/6 got 200** including `/api/referrals` (`canActAsClipper` confirmed **false** on that account, so the test was real) |

**NOT proven, and not claimed: the self-review block.** The dev reviewer owns **zero clips**, so there is no self-owned clip to submit. The only way to create one is to write a clip, which this round forbids — and if the rule were broken, the test itself would change a clip. Same limit BL-800 stated; I add the structural reason.

Every write in this pass hit only the dev seed accounts `dev-reviewer-001` / `dev-clipper-001`. **I restored `dev-reviewer-001` to exactly the state I found it in** (mode LIVE, invitedOnly false). The three real LIVE reviewers and the partner were never touched.

## PART 3 — what the database says

All timestamps cast `::text` against DB `now()` = `2026-08-13 11:15:28+00`.

| check | value | verdict |
| --- | --- | --- |
| Earnings invariant violations | **0** | clean |
| Payouts | **167**, last write **2026-08-12 11:24:15.661** | unchanged, and that write predates the round by 11 hours. **Nothing created, modified, approved or cancelled** |
| 5 percent referral earning | **6 rows, $109.57, rateBps 500**, last created 2026-07-10 | **unchanged**, exactly as BL-800 recorded |
| Chat | **54 conversations / 13 escalated / 50 people** | exact match |
| Clip decisions since the round began | 69 APPROVED + 21 REJECTED, **every one by the real OWNER account**; zero by any reviewer | expected owner activity |
| Clip decisions during MY session | **0** | I changed nothing |

**The BL-799 referral-code write DID land.** The ledger records **1,039 written, 0 failed**. Coverage now: **1,360 of 1,400 users hold a code, all 1,360 distinct** (no collisions). The 40 without one break down honestly: 12 are REVIEWERs (out of scope), and of the 28 clippers, **20 are soft-deleted**, 6 signed up after the backfill, and **2 are live clippers who registered on 2026-08-12 between 17:55 and 20:14 — hours before the 20:28 backfill snapshot**. So **8 live clippers currently lack a code, all very recent signups**. Not a failure; a residual worth one follow-up backfill.

One honest note: clip `updatedAt` moves continuously (last 11:06 today) — that is the tracking cron writing view snapshots, not a status or earnings change. Status totals are APPROVED 4,538 / PENDING 44 / REJECTED 1,035 / FLAGGED 6.

## PART 4 — everything unique preserved, verified from origin

Pushed as **eight additive `recovery/BL-801-*` branches**, none merged, nothing discarded. Verified with `git ls-remote`, not with push output — every local SHA matches origin:

`recovery/BL-801-BL-361` `1b9e21b1` · `-BL-363` `fe9650ac` · `-BL-365` `2fbc7ef4` · `-BL-367` `c19c00fb` · `-BL-368` `0c5a8c98` · `-BL-597` `75bc0512` · `-BL-600` `b5feceec` — **all VERIFIED ON ORIGIN.**

`recovery/BL-801-untracked-artifacts` `2944662d` — **VERIFIED ON ORIGIN.** Holds the eight untracked working-tree files (8 files, 5,051 insertions), including the **BL-799 referral-code ledger**, two July audit docs, and five August 6 render dumps. Built with git plumbing on a temporary index, so **the shared working tree and the real index were never touched** (re-confirmed afterwards: 0 tracked changes, same nine untracked paths, HEAD still `main@d004b396`).

No worktree was mid-merge, so nothing had to be preserved before an abort, and no abort was needed.

## PART 5 — nothing to finish

**Main is already complete and coherent, so I merged nothing.** The forward-versus-revert question does not arise: main is not half-merged and not broken. `origin/main` is still `d004b396`, exactly as the interrupted round left it.

BACKLOG was checked by the union rule rather than a raw count, which is the stronger test: **zero BL ids lost from any of the nine source refs.** Main carries **556 unique BL ids**, a superset of the pre-chain tip (547) and of all eight branches (548 to 553). **0 conflict markers.** (My heading-based count differs from BL-800's 687 because the counting rule differs, not because entries are missing — no id from any source is absent.)

## PART 6 — the end state, proven

Everything in PART 2 was proven on this exact tree — it *is* the final tree, since no merge occurred. Re-confirmed at the close: **invariant 0, payouts 167 with the same last-write timestamp, referral total $109.57, chat 54/13/50, zero clip decisions during my session.**

**Money files byte-identical by blob OID**, compared `git show 72f05cec` versus `origin/main` across the entire chain — all seven **IDENTICAL**: `clip-earnings-writer.ts ac5be7de`, `earnings-calc.ts 797e2098`, `balance.ts e887f80a`, `tracking.ts 83ce4bab`, `clip-earnings-invariant-middleware.ts 61cef393`, `money-decimal.ts ef5cdae7`, `campaign-era.ts 106e16ad`.

**BL-678 guards intact.** All seven Apify guard files are byte-identical across the chain (`apify-hard-off.ts`, `apify.ts`, `clipper-submit-core.ts`, `verify-cascade.ts`, `account-profile.ts`, `apidojo.ts`, `lamatok.ts`) and `APIFY_HARD_OFF: true` still stands. **No Apify actor was run.**

### What the owner must do himself

1. **REDEPLOY.** BL-797's report-a-problem feature is merged into main but **will not work in production until a redeploy**. No schema needs applying — `problem_reports` already exists in production.
2. **Decision 1 — the partner's invitee scope flag.** Still **OFF** (`reviewerScopeInvitedOnly` false), in TRIAL mode, with **0 invitees**. He can therefore see **all 44 pending clips, of which 0 are from anyone he invited** (BL-800 measured this as 82 of 82; the pending pool has since shrunk to 44, the ratio is unchanged). Turning the flag on would drop him to 0 visible clips. **I did not change it.**
3. **Decision 2 — the three reviewers in LIVE mode**, whose decisions land immediately and who are all **unscoped** (`invitedOnly` false), holding 27, 5 and 1 invitees. **I did not change them.**

### Ambiguity reported rather than smoothed over

- One real LIVE reviewer's row shows `updatedAt` 2026-08-13 09:25:59 and the partner's shows 00:35:44, both after the round. **No `REVIEWER_CONFIG_UPDATED` audit row exists for either**, so these are almost certainly session or last-active field writes, not config changes. I could not prove that positively and am not claiming it.
- The 6 owner `SERVER_ERROR` rows from 2026-08-12 21:52 to 22:01 are BL-800's already-disclosed render-pass side effect, not new.
- I created no worktree, so there is none to remove. Both pre-existing leftover directories were left exactly as found.
