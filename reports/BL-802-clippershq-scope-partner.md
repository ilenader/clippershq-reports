# BL-802 — the partner is scoped, the three LIVE reviewers are deliberately left, and the 82-of-82 figure was wrong

**2026-08-13 · DB `now()` = `11:40:22.746108+00` (first read) to `11:45:38.503724+00` (after the write) · DATA ONLY.**
Base `origin/main` @ `d004b396`, branch `checkpoint/BL-802`, isolated worktree `C:/b802`, `node_modules` never junctioned, removed at the end. Every read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted, no wallet address read or printed.

## THE FIRST LINE
> **He DOES have a referral code now.** BL-799's issuance reached him: **`VSHJYM4H`**, confirmed on his row and again by asking `/api/referrals` as him. His link is `https://clipershq.com/login?ref=VSHJYM4H` and it works. **Scoping him therefore does not strand him.**
> **He has 0 invitees, so his queue is empty from now until clippers join through that link.** That is the trade-off the owner accepted, restated as asked.
> **The flag is ON for him and for nobody else.** One boolean, one row, by explicit id, `rowCount 1`. **The three LIVE reviewers were not touched** and are verified unchanged. **26 of the 27 reviewer rows remain unscoped**, 13 of them live, so the position is on the record rather than forgotten.

## PART 0 — THE STATE BEFORE THE WRITE, AND A CORRECTION FOUR ROUNDS HAVE CARRIED
| measure | value |
|---|---|
| user | `tg…d7`, id `cmp9d0xu3000q…` |
| role · mode | **REVIEWER** · **TRIAL**, so his press writes a recommendation and leaves the clip PENDING |
| `reviewerScopeInvitedOnly` | **false** |
| `referralCode` | **`VSHJYM4H`** — present, issued by BL-799 |
| his invitees | **0** |
| capabilities · `canActAsClipper` | `[]` · false |
| his queue RIGHT NOW, the exact request his page makes | **0 clips**, HTTP 200 |
| the same read with archived campaigns included | **500 returned** (the take cap) of **1,047 matching**, from **34 clippers**, in **1 campaign**, **1,047 of 1,047 not his invitees** |
| pending or flagged on the whole platform today | **17**, from 16 clippers across 9 campaigns |

**The 82-of-82 figure is not what he sees, and I am correcting it rather than repeating it.** It was a platform-wide pending count. Two facts no prior round reported change the picture.

**One. He has been CAMPAIGN-scoped since 2026-06-18.** `reviewer_clip_scopes` holds one row for him: a single campaign `cmq853xl8…`, cutoff `2026-05-31 15:21:00Z` on `createdAt`, created by the owner; `reviewerScopeCampaignIds` carries the same single id. **That campaign is ARCHIVED and PAUSED**, and `/api/clips` excludes archived campaigns unless asked otherwise, which is why the exact request `/admin/clips` makes for him returned **0** before this round changed anything.

**Two. He carries `reviewerCanSeeDecided = true`**, so inside that campaign his read is not limited to pending and flagged. It is every status: 701 approved, 344 rejected, 1 pending, 1 flagged. **So the real exposure was wider in kind and narrower in reach than reported** — not 82 pending clips across 9 campaigns, but up to 1,047 clips of every status in one archived campaign, reachable only on a request that asks for archived rows. **Today's platform figure, for the record: 17 clips pending or flagged (11 PENDING, 6 FLAGGED), from 16 clippers across 9 campaigns.** The pool has fallen 82 → 44 → 17 as the owner has worked through it.

## PART 1 — THE WRITE, SNAPSHOTTED AND REVERSIBLE
**Snapshot, taken before anything was written:** `role REVIEWER · reviewerMode TRIAL · reviewerScopeInvitedOnly false · canActAsClipper false · referralCode VSHJYM4H · referredById null · reviewerCapabilities {} · reviewerCanSeeDecided true · reviewerScopeCampaignIds {cmq853xl8…} · status ACTIVE · isDeleted false · updatedAt 2026-08-13 00:35:44.576`.

**The exact rollback, printed BEFORE the write and committed at `scripts/migrations/BL-802-scope-partner.sql`:**
```sql
UPDATE users SET "reviewerScopeInvitedOnly" = false WHERE id = 'cmp9d0xu3000q0pmqwyq7hegd';
```
**What was applied**, through `scripts/run-mutation-once.js`, which echoes the file before running it:
```sql
UPDATE users SET "reviewerScopeInvitedOnly" = true
 WHERE id = 'cmp9d0xu3000q0pmqwyq7hegd' AND "reviewerScopeInvitedOnly" = false;
```
**`rowCount = 1`.** Never a broad UPDATE; no role, mode, capability, campaign-scope or referral-code change. **His `updatedAt` did not even move** (2026-08-13 00:35:44.576 before and after), which confirms the write was the single column and nothing triggered a wider touch.

**The reviewers the owner decided to LEAVE, verified after the write:**

| reviewer | mode | invitees | scoped? | `updatedAt` |
|---|---|---|---|---|
| `cmoagb7e` | **LIVE** | 27 | **no, left as decided** | 2026-08-13 09:25:59.679, unchanged |
| `cmovb0q6` | **LIVE** | 5 | **no, left as decided** | 2026-08-03 13:01:44.615, unchanged |
| `cmpod0dh` | **LIVE** | 1 | **no, left as decided** | 2026-08-02 08:52:24.264, unchanged |

**Reviewer population after this round: 27 rows, 1 scoped, 26 unscoped, of which 13 are live rows.** The three above are the ones that matter; the rest are dev and test seeds. **Recorded here so the decision stays a decision and not a gap nobody remembers making.**

## PART 2 — THE SCOPE BITES, PROVEN BY ASKING THE SERVER AS HIM
**Proof method, stated because it matters.** I did not read code and conclude. I minted a real Auth.js session for **his id only** and made the requests as him against `next dev --webpack` on :3802. **The mint writes nothing to the database**: it carries only `sub` and a `lastLoginDay` marker set to today, which suppresses the fire-and-forget `lastLoginAt` stamp the auth callback would otherwise make on his row. `/api/auth/session` returned his real id, role REVIEWER, mode TRIAL, capabilities `[]`, `canActAsClipper` false — the account in question, not a stand-in.
```
BEFORE  /api/clips                                  -> 200, 0 clips
BEFORE  /api/clips?includeArchived=true             -> 200, 500 clips (cap), 34 clippers, 1 campaign
BEFORE  /api/clips?includeArchived=true&status=PENDING  -> 200, 1 clip
AFTER   /api/clips                                  -> 200, 0 clips
AFTER   /api/clips?includeArchived=true             -> 200, 0 clips
AFTER   /api/clips?status=PENDING                   -> 200, 0 clips
AFTER   /api/clips?includeArchived=true&status=PENDING   -> 200, 0 clips
AFTER   /api/clips?includeArchived=true&status=APPROVED  -> 200, 0 clips
```
**500 to 0 on the archived-inclusive read is the measurement that proves it.** Every count is **0 at HTTP 200** — an empty queue with a plain empty state, not an error. **It fails closed**, exactly as BL-788 built it: he has no invitees, so nothing matches. **Control, so this is not a platform break dressed as a fix:** an **unscoped** reviewer on the same server still reads **14 clips from 13 clippers across 7 campaigns**, and the **OWNER** still reads **9 pending**. The filter is his flag.

**The reviewer role still ADDS and never removes**, checked as him after the change:
```
/api/referrals 200   /api/earnings 200   /api/accounts/mine 200   /api/payouts/mine 200
/api/clips/mine 200  /api/campaigns 200  /api/gamification 200
POST /api/clips {}  -> 400 {"error":"Campaign, account, and clip URL are required"}
/api/referrals body -> {"referralCode":"VSHJYM4H","referralCount":0,"referralEarnings":0,...}
pages /referrals /earnings /accounts /payouts /campaigns /clips /admin/clips /reviewer/proposals -> all 200
```
**The submission proof is the important one.** A 400 for missing fields means the request passed the permission gate and failed validation. The gate is open and **no clip was created to prove it**.

## PART 3 — NOTHING ELSE MOVED
| check | before | after |
|---|---|---|
| earnings invariant violations | **0** | **0** |
| payout rows · fingerprint · last write | 167 · `f7abba85…` · 2026-08-12 11:24:15.661 | **identical on all three** |
| clip status + earnings fingerprint, 5,545 clips | `65c47df0…` | **identical** |
| referral commissions | 6 rows · $109.57 · `6a2c2570…` | **identical** |
| all-users flag fingerprint, 1,400 users | `d63d5ad9…` | `e6df8ce9…`, and **reverting only his one boolean in the expression reproduces `d63d5ad9…` exactly** |

**That last line is the strongest evidence in the round.** Recomputing the fingerprint over all 1,400 users with a single `CASE` forcing his flag back to false returns the baseline hash byte for byte. **One field, on one row, changed. No other user's role, mode, `canActAsClipper`, referral code or inviter moved.** **No payout was created, modified, approved or cancelled** (167 rows, same fingerprint, last write 11 hours before this round). **No clip's status or earnings changed.** The **4 clip decisions** inside my window (11:40:11 to 11:41:01) were all by the **real OWNER account** in live traffic, before my baseline was taken; **zero by any reviewer and zero by me**. **Zero `reviewer_audit_log` rows** written in the window.

**No code change was necessary and none was made.** The **6 money files plus `tracking.ts` and `campaign-era.ts` are byte-identical by blob OID on BOTH refs** (`origin/main` and `checkpoint/BL-802`): `ac5be7de`, `797e2098`, `e887f80a`, `83ce4bab`, `61cef393`, `ef5cdae7`, `106e16ad`. **The commit contains two files, both documentation: the BACKLOG entry and the applied SQL, kept so the rollback is one line inside the repo. No source file was touched, so there is no diff to justify.** No schema change, no `prisma migrate`, **no Apify actor run**, the 11 BL-678 guards untouched. I also confirmed in passing that the BL-240 money redaction still holds for him: earnings and bonuses come back zeroed and `campaign.ownerCpm` null.

**One honest gap.** The write went through raw SQL, so **there is no `REVIEWER_CONFIG_UPDATED` audit row for it.** The record of this change is this report, the BACKLOG entry and the committed SQL file. If the owner would rather it appear in the audit log, the same flag can be re-set from his own reviewer-config screen, which writes one.

## PART 4 — WHAT HAPPENS NEXT, IN PLAIN WORDS
**What he will see.** His review queue will be empty. Not broken, not an error: a normal empty screen that says there is nothing to review. Everything else stays as it was — his own clips, earnings, accounts, payouts, campaigns, referrals page and clip submission all still work, all proven above.

**What he must do to gain a queue.** Clippers have to join through **his** link. Nothing else creates an invitee. The link is **`https://clipershq.com/login?ref=VSHJYM4H`**. Anyone who signs up through it is stamped as his, and from that moment their clips appear in his queue and nobody else's.

**What the owner should tell him**, in one message: *"Your review queue is now limited to clippers who join through your own link. It will show nothing until the first one joins. Here is your link, share it with the people you recruit. Everything else in your account works as before."*

**The case that will actually come up, stated plainly.** The clippers he already works with, who signed up before he had a link, **will never appear as his invitees on their own.** Nothing in the signup path attributes someone retroactively, and `attachReferral` refuses to overwrite an existing inviter. **The owner CAN attribute them by hand**, at **`/admin/referral-override`**, which stamps `referrerOverriddenBy` and `referrerOverriddenAt` so a manual attribution is always distinguishable from a natural one. **It is not a free action: `referredById` is the same column that decides the platform fee**, so attributing a clipper to him moves that clipper from a 9% fee to a 4% fee and starts a 5% lifetime referral earning for him. That is a money decision as well as a visibility one, and it belongs to the owner.

**Two things this round found and did not act on.** His campaign scope is a single **archived, paused** campaign, so even with the invitee scope off his queue would still read 0 on the normal request. And `reviewerCanSeeDecided` is **true** for him, so once he does have invitees he will see their decided clips too, not only the pending ones. **Both are pre-existing owner settings, both changeable from the same screen, and neither was touched.**

## GATES, HONESTLY
`npm ci` **exit 0**; `npx prisma generate` **exit 0** before tsc; `npx tsc --noEmit` **exit 0**, `grep -c "error TS"` = **0**; `npm run build` written to a log with the exit code echoed by hand and **never piped through `tail`**: **BUILD_EXIT=0**, "Compiled successfully in 30.7s". **eslint v9.39.4 confirmed present first**, so the hooks gate did not silently no-op: `check:prisma-bypass` **0 violations**, `check:removed-fields` **OK across 732 files**, `lint:hooks` **11 problems, 0 errors, 11 warnings** at the ceiling. Branch `checkpoint/BL-802` @ `873728ab` **VERIFIED on origin** by `scripts/safe-push.mjs`, tags `pre-BL-802` and `post-BL-802` pushed. **The worktree `C:/b802` was removed.**

**Rollback:** the one-line `UPDATE` at the top of `scripts/migrations/BL-802-scope-partner.sql` puts his flag back to false; `git reset --hard pre-BL-802` reverses the documentation side. The two are independent.
