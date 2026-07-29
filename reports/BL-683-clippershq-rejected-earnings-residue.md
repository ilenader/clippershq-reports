# BL-683 (ClippersHQ) — the 10 REJECTED clips carrying stale baseEarnings are clean, and no code needed changing

> **Filename note, per CONVENTION.md.** `reports/BL-683.md` was already taken by a different project (clipper-finder, *"`energy_step_ts`: built, measured, and honest about which number it is"*). The collision check was run against `origin/main` before pushing and that file was **not** touched. This report is published beside it under the `-<project>-<slug>` suffix the convention prescribes.

**2026-07-29 · SHIPPED to `checkpoint/BL-683` @ `1abad013`, verified on origin.** Base main `fdde504f`. Tags `pre-BL-683` / `post-BL-683`. **Zero source files changed.** The invariant now holds with **0 violations across all 4,411 clips**.

---

## PART 0 — the truth, established before anything was touched

BL-680's query was re-run from scratch rather than inherited. **DB `now()` at the time: 2026-07-29 18:18:36.936334+00.** It reproduced exactly:

| status | clips | violations | max drift | total earnings |
|---|---|---|---|---|
| APPROVED | 3488 | 0 | $0.0100 | $9,845.76 |
| FLAGGED | 6 | 0 | $0.0000 | $113.50 |
| PENDING | 69 | 0 | $0.0000 | $0.00 |
| **REJECTED** | 848 | **10** | **$17.0200** | **$0.00** |

### The exact ten

Clipper ids are salted-hash prefixes, never handles.

| clip id | campaign | clipper | status | earnings | baseEarnings | bonusPct | bonusAmount | drift | REJECTED at (audit) |
|---|---|---|---|---|---|---|---|---|---|
| `cmoel4p3200030ppx1mrt23oy` | somesome | `a2533901` | REJECTED | 0.00 | 16.69 | 2 | 0.33 | **17.02** | 2026-04-26 13:26:22 |
| `cmp1kmcar00010pmnulf7rbx0` | somesome | `97a13709` | REJECTED | 0.00 | 8.55 | 0 | 0.00 | 8.55 | 2026-05-12 14:14:27 |
| `cmoc044zw000y0ppkrp6nktki` | somesome | `f95b37db` | REJECTED | 0.00 | 6.86 | 0 | 0.00 | 6.86 | 2026-04-24 08:10:02 |
| `cmpe6u43a00270ppz363vbqoi` | GainzAlgo (REPOST) | `96fb4a73` | REJECTED | 0.00 | 3.77 | 0 | 0.00 | 3.77 | 2026-05-20 16:39:55 |
| `cmp15x8zl00150po63n5qvrq7` | somesome | `2abe41f9` | REJECTED | 0.00 | 3.40 | 4 | 0.14 | 3.54 | 2026-05-11 15:19:00 |
| `cmp2fdf5m001a0prqcc668pqw` | somesome | `1cf7c57e` | REJECTED | 0.00 | 3.34 | 0 | 0.00 | 3.34 | 2026-05-13 11:51:34 |
| `cmobl5ltw000h0po4u1de5l2k` | somesome | `11e72ed3` | REJECTED | 0.00 | 2.75 | 0 | 0.00 | 2.75 | 2026-04-25 09:28:10 |
| `cmod1aquw000i0ppea065q12s` | somesome | `a2533901` | REJECTED | 0.00 | 2.38 | 2 | 0.05 | 2.43 | 2026-04-26 13:26:56 |
| `cmoyisygy00200pqdw5eq31r5` | somesome | `420b6411` | REJECTED | 0.00 | 1.29 | 2 | 0.03 | 1.32 | 2026-05-10 09:28:36 |
| `cmpex6aum00090pnbxc7apxg3` | GainzAlgo (REPOST) | `88113857` | REJECTED | 0.00 | 1.12 | 0 | 0.00 | 1.12 | 2026-05-22 14:18:55 |

**Totals: $50.15 baseEarnings + $0.55 bonusAmount = $50.70 of residue.** Matches BL-680 to the cent.

### NONE of it is payable, proven three independent ways

This was the STOP condition, so it was settled first and it was settled empirically, not by reasoning about intent.

1. **Every one already has `earnings = 0.00`**, and `earnings` is the only field that pays.
2. **No payout has ever drawn on any of them.** `payout_requests.clipIdsSnapshot` is the definitive linkage. There are **140 payout requests**, **97** carrying a clip snapshot, referencing **2,307 clip ids** in total. Of those 2,307 references, the number matching any of these 10 clips is **0**.
3. **They carry 0 `agency_earnings` rows**, so there is no owner-side money on them either.

And structurally, `balance.ts` cannot reach them by **two** independent locks: it filters `c.status === "APPROVED"` (lines 164 and 168) and it sums `earnings`, never `baseEarnings`. A REJECTED clip is excluded by status, and the field it would read is already zero.

**Conclusion: nothing here is owed to anybody. Cleaning is safe.** Had any of it been payable I would have stopped and reported instead.

### How it happened, named by the code itself

The audit trail shows all 10 followed the same route: **APPROVED, then PENDING, then REJECTED**, with `REJECTED_CLIP` audit rows spanning **2026-04-24 08:10:03 to 2026-05-22 14:18:55**. They earned legitimately, then a reviewer took the approval back.

The code documents its own bug at `src/app/api/clips/[id]/review/route.ts:1141-1148`:

> *"REJECTED / PENDING → status fields + zero the 4 invariant earnings fields. F-CLIPPER-UNDO-FIX1: **previously written as a single `clip.update` with `earnings: 0` only**; L2 invariant middleware rejects that as INCOMPLETE since **baseEarnings + bonusAmount were left unwritten**. Migrated to the two-step pattern ... `writeClipEarningsZero` clears the 4 invariant fields atomically and satisfies L2."*

That is precisely this residue: `earnings` was zeroed, `baseEarnings` and `bonusAmount` were not.

---

## PART 1 — no code was changed, and the reason is decisive

**F-CLIPPER-UNDO-FIX1 landed in commit `eed25fa6` on 2026-05-23 15:25.**

The newest of the 10 rejections is **2026-05-22 14:18:55**, roughly **25 hours before the fix**. **Every single one predates it.** The live path today calls `writeClipEarningsZero`, which writes `{ earnings: 0, baseEarnings: 0, bonusPercent: 0, bonusAmount: 0 }` in one validated write (`clip-earnings-writer.ts:720-731`), so all four fields move together and the L2 middleware validates rather than rejects.

**There is no live cause left to fix, so I changed no code.** Inventing a fix for a cause I could not demonstrate would have been worse than doing nothing, and the brief said so.

### A correction to BL-680's framing, and it matters

BL-680 reported *"the newest is 2026-07-22 16:50:30, the oldest 2026-06-24 16:31:21"*, and read that as evidence the defect was recent. **Those are `updatedAt` values, not rejection dates.** `updatedAt` is Prisma's `@updatedAt` and bumps on **any** column write.

What actually happened in June and July was bulk activity on other columns:

| window | clips updated platform-wide | of which REJECTED |
|---|---|---|
| 2026-06-24 16:31 | 104 | 48 |
| 2026-06-24 16:32 | 264 | 120 |
| 2026-07-22 13:51 | 18 | 18 |
| 2026-07-22 15:51 | 17 | 17 |
| 2026-07-22 16:50 | 6 | 6 |

**368 clips were touched on 2026-06-24 alone.** None of those writes went through the earnings writer, which is exactly why the residue survived them untouched. **Read by rejection date the defect is two months old and already fixed at source; read by `updatedAt` it looks a week old and unfixed.** The first reading is the correct one.

---

## PART 2 — the cleanup

### Written through the chokepoint, not with raw SQL

CLAUDE.md is explicit that `writeClipEarnings` is the **only** allowed path to `earnings` / `baseEarnings` / `bonusAmount`, and that a direct `clip.update` on those three is forbidden. So the cleanup calls **`writeClipEarningsZero`**, the same function the live reject path calls today. Each write is validated by the L2 invariant middleware rather than bypassing it. This is the fix being applied retroactively to rows rejected before it existed.

**The 10 ids are hardcoded in the script.** It carries three refusal guards and aborts on any of them:

* every target must be `REJECTED`
* every target must already have `earnings = 0` (**if any had real money on it, the script refuses to run**)
* every target must actually violate the invariant

**Never a broad UPDATE. Never `agency-monitor --fix`. Never an owner re-derive.**

### The exact rollback, printed BEFORE any write

```sql
BEGIN;
UPDATE clips SET "baseEarnings" = 2.75,  "bonusPercent" = 0, "bonusAmount" = 0.00, earnings = 0.00 WHERE id = 'cmobl5ltw000h0po4u1de5l2k';
UPDATE clips SET "baseEarnings" = 6.86,  "bonusPercent" = 0, "bonusAmount" = 0.00, earnings = 0.00 WHERE id = 'cmoc044zw000y0ppkrp6nktki';
UPDATE clips SET "baseEarnings" = 2.38,  "bonusPercent" = 2, "bonusAmount" = 0.05, earnings = 0.00 WHERE id = 'cmod1aquw000i0ppea065q12s';
UPDATE clips SET "baseEarnings" = 16.69, "bonusPercent" = 2, "bonusAmount" = 0.33, earnings = 0.00 WHERE id = 'cmoel4p3200030ppx1mrt23oy';
UPDATE clips SET "baseEarnings" = 1.29,  "bonusPercent" = 2, "bonusAmount" = 0.03, earnings = 0.00 WHERE id = 'cmoyisygy00200pqdw5eq31r5';
UPDATE clips SET "baseEarnings" = 3.40,  "bonusPercent" = 4, "bonusAmount" = 0.14, earnings = 0.00 WHERE id = 'cmp15x8zl00150po63n5qvrq7';
UPDATE clips SET "baseEarnings" = 8.55,  "bonusPercent" = 0, "bonusAmount" = 0.00, earnings = 0.00 WHERE id = 'cmp1kmcar00010pmnulf7rbx0';
UPDATE clips SET "baseEarnings" = 3.34,  "bonusPercent" = 0, "bonusAmount" = 0.00, earnings = 0.00 WHERE id = 'cmp2fdf5m001a0prqcc668pqw';
UPDATE clips SET "baseEarnings" = 3.77,  "bonusPercent" = 0, "bonusAmount" = 0.00, earnings = 0.00 WHERE id = 'cmpe6u43a00270ppz363vbqoi';
UPDATE clips SET "baseEarnings" = 1.12,  "bonusPercent" = 0, "bonusAmount" = 0.00, earnings = 0.00 WHERE id = 'cmpex6aum00090pnbxc7apxg3';
COMMIT;
```

This restores every value byte for byte. It is a plain per-id `UPDATE` precisely because a rollback must not depend on the writer being reachable.

### The dry run, shown in full before applying

```
GUARDS PASSED: all 10 are REJECTED, all pay 0.00, all violate the invariant.

clip                       status    earnings  baseEarnings  bonusPct  bonusAmount  drift    ->  AFTER
cmobl5ltw000h0po4u1de5l2k  REJECTED      0.00          2.75         0         0.00    2.75   ->  0.00 / 0.00 / 0 / 0.00
cmoc044zw000y0ppkrp6nktki  REJECTED      0.00          6.86         0         0.00    6.86   ->  0.00 / 0.00 / 0 / 0.00
cmod1aquw000i0ppea065q12s  REJECTED      0.00          2.38         2         0.05    2.43   ->  0.00 / 0.00 / 0 / 0.00
cmoel4p3200030ppx1mrt23oy  REJECTED      0.00         16.69         2         0.33   17.02   ->  0.00 / 0.00 / 0 / 0.00
cmoyisygy00200pqdw5eq31r5  REJECTED      0.00          1.29         2         0.03    1.32   ->  0.00 / 0.00 / 0 / 0.00
cmp15x8zl00150po63n5qvrq7  REJECTED      0.00          3.40         4         0.14    3.54   ->  0.00 / 0.00 / 0 / 0.00
cmp1kmcar00010pmnulf7rbx0  REJECTED      0.00          8.55         0         0.00    8.55   ->  0.00 / 0.00 / 0 / 0.00
cmp2fdf5m001a0prqcc668pqw  REJECTED      0.00          3.34         0         0.00    3.34   ->  0.00 / 0.00 / 0 / 0.00
cmpe6u43a00270ppz363vbqoi  REJECTED      0.00          3.77         0         0.00    3.77   ->  0.00 / 0.00 / 0 / 0.00
cmpex6aum00090pnbxc7apxg3  REJECTED      0.00          1.12         0         0.00    1.12   ->  0.00 / 0.00 / 0 / 0.00

residue to clear: baseEarnings $50.15 + bonusAmount $0.55 = $50.70
earnings paid by these rows, before and after: $0.00

DRY RUN. Nothing was written.
```

Then applied, one clip per transaction, each logging through the writer:

```
[CLIP-EARNINGS-WRITE] clipId=... earnings=0 base=0 bonusPct=0 bonus=0 reason=bl683:clear-rejected-residue
rows written: 10
rows still violating the invariant: 0  (MUST be 0)
rows whose status moved: 0  (MUST be 0)
```

---

## PART 3 — proof, from a whole-population before/after diff

A separate read-only script snapshotted **every one of the 4,411 clips** before and after. The complete diff:

```
5c5
< REJECTED   clips=  848 violations= 10 maxDrift= 17.0200 totalEarnings=0.00
---
> REJECTED   clips=  848 violations=  0 maxDrift=  0.0000 totalEarnings=0.00
10,11c10,11
< baseEarnings = 9548.26          > baseEarnings = 9498.11
< bonusAmount  = 461.71           > bonusAmount  = 461.16
21,30c21,30
  (the ten target rows, base/bonus going to 0.00)
```

**Nothing else moved.** Every other line is byte-identical between the two runs:

| check | before | after | verdict |
|---|---|---|---|
| **Invariant violations, whole population** | **10** | **0** | fixed |
| Max drift, REJECTED | $17.0200 | $0.0000 | fixed |
| APPROVED / FLAGGED / PENDING violations | 0 / 0 / 0 | 0 / 0 / 0 | untouched |
| **Total platform `earnings`** | **$9,959.26** | **$9,959.26** | **unchanged to the cent** |
| **APPROVED earnings** | **$9,845.76** | **$9,845.76** | **unchanged to the cent** |
| Platform `baseEarnings` | $9,548.26 | $9,498.11 | **-$50.15**, exactly the residue |
| Platform `bonusAmount` | $461.71 | $461.16 | **-$0.55**, exactly the residue |
| **Checksum over the other 4,401 clips** | `e4169843e8a8bca2b99b5a79b238d45d` | `e4169843e8a8bca2b99b5a79b238d45d` | **IDENTICAL. No other clip changed by a cent** |
| **Per-clipper APPROVED earnings, all 224 clippers** | `27625f359715d053ad8f2657ceca3a47` | `27625f359715d053ad8f2657ceca3a47` | **IDENTICAL. No withdrawable balance moved** |
| Payouts: count / amount / final / actualPaid | 140 / 13954.59 / 12375.64 / 984.14 | 140 / 13954.59 / 12375.64 / 984.14 | unchanged |
| Clip count, and any status change | 4411, 0 moved | 4411, 0 moved | unchanged |

**BL-680's own invariant query, re-run after the cleanup:**

```
APPROVED   clips= 3488 violations=  0 maxDrift=  0.0100 totalEarnings=9845.76
FLAGGED    clips=    6 violations=  0 maxDrift=  0.0000 totalEarnings=113.50
PENDING    clips=   69 violations=  0 maxDrift=  0.0000 totalEarnings=0.00
REJECTED   clips=  848 violations=  0 maxDrift=  0.0000 totalEarnings=0.00
```

**Zero violations, every status, whole population.**

### Invisible to every clipper

Worth stating plainly because these are real people's rejected clips. **There are zero clipper-facing reads of `baseEarnings` anywhere** in `src/app/(app)/` or `src/components/`. Both clip cards gate their entire money block on `status === "APPROVED" && earnings > 0` (`ClipCardNew.tsx:190`, legacy `clips/page.tsx:439`), so a REJECTED clip renders no earnings figure and no bonus pill at all. The a11y lead confirmed the DOM node is **omitted entirely**, not merely visually hidden, so no rendered text, no accessible name and no DOM node changed for any clipper or any screen-reader user. Its verdict on this round was an **empty must-fix list**: a cleanup script and a BACKLOG entry touch no markup.

---

## Safety and gates, stated honestly

* **6 money files + `tracking.ts` + `campaign-era.ts` BYTE-IDENTICAL by blob OID** (`pre-BL-683:<f>` vs the working tree): writer `7aa6be48`, earnings-calc `797e2098`, balance `e887f80a`, tracking `847dcf70`, middleware `61cef393`, money-decimal `ef5cdae7`, campaign-era `106e16ad`.
* **0 source files changed.** The diff is two new scripts plus `BACKLOG.md`. No schema change, no `prisma migrate`, no config change.
* **Gates, honest.** `npm ci` exit 0, then `npx prisma generate` exit 0 **before** typecheck. `npx tsc --noEmit` **exit 0 with 0 lines of output**. `npm run build` **BUILD_EXIT=0**, read from a captured log and echoed directly, never piped through `tail`. Prebuild: **BYPASS detector 0 violations across `src/` + `scripts/`, including its earnings-write check**, which is the gate that would have caught a script writing these columns outside the writer; `check:removed-fields` OK; `lint:hooks` **11 problems (0 errors, 11 warnings)** at the ≤11 cap with **eslint v9.39.4 present**, not a silent no-op. Compiled 61/61 pages. Counts taken with `grep -c`, never `head`.
* **No dashes as bullets.** Clipper identities appear only as salted-hash prefixes. Isolated worktree at the short path `C:/b683`, `node_modules` never junctioned. Nothing held by a live round (BL-682) was touched.
* **Rollback:** the per-id SQL above, which restores every value byte for byte. Re-running the script's dry run now correctly **refuses** with *"already satisfy the invariant"*, which is the third guard working as designed.

## What I would do next

1. **Nothing about the cause.** It is fixed and every affected row predates the fix. This defect class is closed.
2. **BL-680's second finding is the live one:** Instagram delivers 0 captions and 0 sound ids on organic shadow rows after the BL-668 deploy, while TikTok delivers 7 of 8. That is a working pipeline on one platform and a dead one on the other, and it is worth more than any further data hygiene.
3. **Consider whether `updatedAt` should be trusted as an age signal in future audits.** It was the one thing that made this defect look a week old when it was two months old and already fixed.
