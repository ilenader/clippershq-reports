# BL-734 — the owner's two $20 raises, verified; and there were SEVEN copies of the minimum, not five

**FIRST LINE, because that is where a flipped clipper was to be reported: NO CLIPPER FLIPPED FROM ABLE TO
UNABLE. Zero. The blast-radius dialog told the owner the truth.**

**2026-08-07 · Base:** `main @ ab455ac7` · **Branch:** `checkpoint/BL-734` `7a78feb2` · **Tags:** `pre-BL-734` = `ab455ac7`, `post-BL-734` = `7a78feb2`
**No minimum was changed by this round. No clip's status or earnings changed. No payout was created, modified, approved or cancelled.**
**Handles are redacted to an md5 prefix throughout. No wallet address appears anywhere. Every timestamp is cast to `::text` against DB `now()`.**

---

# PART 1 — THE OWNER'S TWO CHANGES, ON LIVE DATA

## 1.1 Which two campaigns, and what they store

Exactly two of the 33 campaigns hold a non-null minimum. Both are **$20.0000**, in the decimal money type.

```
| id                        | name                 | min_text | pg_type | = 20.0000 | status | db_now                           |
| cmsisj3d800f10po8jvz526hf | Zhus Edit (0.50 CPM) | 20.0000  | numeric | true      | ACTIVE | 2026-08-07 18:21:26.376097+00    |
| cmsis9csq00ew0po8gzo98vic | Zhus Meme (0.20 CPM) | 20.0000  | numeric | true      | ACTIVE | 2026-08-07 18:21:26.376097+00    |
```

**Not a float and not a string**, confirmed from `information_schema` rather than asserted:

```
column_name              data_type  precision  scale  is_nullable  column_default
minPayoutAmountDecimal   numeric    18         4      YES          (none)
```

`pg_typeof` returns `numeric`, the equality test against `20.0000` is **true**, and the stored text is
`20.0000` with all four scale digits present.

**A NAMING NOTE, stated plainly rather than smoothed over.** The brief describes the two campaigns as
"Zeus and one referred to as the new tool campaign". What is actually set is **Zhus Edit (0.50 CPM)** and
**Zhus Meme (0.20 CPM)**. There is no campaign anywhere in the database with "tool" in its name, and the
only other "Zhus" campaign is `PAST`. If the owner intended a different second campaign, **the minimum is
on Zhus Meme and not on whatever he had in mind**, and nothing in this round moved it. That is his call to
confirm; I did not change it.

## 1.2 He did it himself, through the dialog, and it is on the record

`audit_logs`, the two `CAMPAIGN_FIELDS_CHANGED` rows, actor role **OWNER**:

```
| minPayoutAmountDecimal change | campaign             | at (::text)                 |
| {"to": 20, "from": null}      | Zhus Meme (0.20 CPM) | 2026-08-07 18:16:46.158     |
| {"to": 20, "from": null}      | Zhus Edit (0.50 CPM) | 2026-08-07 18:16:31.308     |
```

`from: null` matters. NULL resolves to the $10 platform default, and the confirmation step in
`admin/campaigns/page.tsx` intercepts only when `editingId` is set **and** the proposal is strictly
greater than the minimum in force. `$20 > $10`, both times, on an existing campaign. **The dialog fired.**

**This closes BL-731 section 9.** That report recorded the dialog as *"STILL UNVERIFIED... nobody has
pressed the button."* The owner has now pressed it twice, in production, and PART 1.3 shows what it said
was true.

## 1.3 EVERY clipper on those campaigns, before and after. 0 flipped.

Computed by reproducing the gate's own arithmetic in SQL, not a second rule: per-campaign earned
(`APPROVED`, `isDeleted = false`, **`videoUnavailable = false`**) plus the marketplace creator share, minus
money-out (`isPayoutMoneyOut`: `PAID`, or `VOIDED` with a non-null `paidAt`), minus locked
(`REQUESTED`/`UNDER_REVIEW`/`APPROVED`), floored at zero, then clamped by the BL-187-P2 **lifetime** global
available (no `videoUnavailable` filter, exactly as BL-692 set it). Liability is `actualPaidAmount ?? amount`.
The clamp is **ON** (`GLOBAL_PAYOUT_CLAMP_ENABLED` is set nowhere, and the helper defaults to true).

**12 pairs, 12 distinct clippers, no clipper on both campaigns.**

```
| clipper  | campaign             | avail_campaign | avail_global | cap    | BEFORE ($10) | NOW ($20) | flip      |
| 7b9418ec | Zhus Edit (0.50 CPM) | 1.66           | 1.66         | 1.66   | BLOCKED      | BLOCKED   | unchanged |
| b0616ed6 | Zhus Edit (0.50 CPM) | 1.66           | 1.66         | 1.66   | BLOCKED      | BLOCKED   | unchanged |
| 56587987 | Zhus Edit (0.50 CPM) | 0.55           | 0.55         | 0.55   | BLOCKED      | BLOCKED   | unchanged |
| a0f7fdd8 | Zhus Meme (0.20 CPM) | 0.52           | 43.63        | 0.52   | BLOCKED      | BLOCKED   | unchanged |
| 1101a865 | Zhus Meme (0.20 CPM) | 0.42           | 0.42         | 0.42   | BLOCKED      | BLOCKED   | unchanged |
| 009f3500 | Zhus Meme (0.20 CPM) | 0.00           | 0.00         | 0.00   | BLOCKED      | BLOCKED   | unchanged |
| 29961807 | Zhus Meme (0.20 CPM) | 0.00           | 0.00         | 0.00   | BLOCKED      | BLOCKED   | unchanged |
| 56655018 | Zhus Edit (0.50 CPM) | 0.00           | 0.00         | 0.00   | BLOCKED      | BLOCKED   | unchanged |
| ca1427c3 | Zhus Edit (0.50 CPM) | 0.00           | 0.00         | 0.00   | BLOCKED      | BLOCKED   | unchanged |
| e5262b1f | Zhus Edit (0.50 CPM) | 0.00           | 0.00         | 0.00   | BLOCKED      | BLOCKED   | unchanged |
| edf4edf1 | Zhus Meme (0.20 CPM) | 0.00           | 26.89        | 0.00   | BLOCKED      | BLOCKED   | unchanged |
| f35351ad | Zhus Meme (0.20 CPM) | 0.00           | 0.00         | 0.00   | BLOCKED      | BLOCKED   | unchanged |
db_now = 2026-08-07 18:25:23.452528+00
```

**The largest effective cap on either campaign is $1.66.** Nobody could withdraw at $10 and nobody can at
$20, so the raise had **nothing to strand**. The dialog would have reported `clippersAbleNow: 0`,
`clippersStranded: 0`, `dollarsStranded: 0.00`, and that is exactly right.

**Clippers now sitting between $10 and $20 on those campaigns: 0.** Not "none found" by sampling. This is
the whole population of the two campaigns, and the ceiling is $1.66, so the $10 to $20 band is provably
empty.

Two clippers are worth naming as a mechanism note: `a0f7fdd8` holds **$43.63 globally** and `edf4edf1`
holds **$26.89 globally**, both far above $20, but their **Zhus** balances are $0.52 and $0.00. The gate is
per campaign and then clamped, so the campaign side binds. They are not victims of the raise; they simply
have almost nothing on these two campaigns.

---

# PART 2 — THE COPIES. BOTH PRIOR ROUNDS UNDERCOUNTED.

## 2.1 The census

BL-728 found four and called one dead. BL-731 found a fifth and correctly called BL-728's "only place"
claim false. **Both were still wrong: there are seven, and copies 6 and 7 were found by neither. Copy 7 is
LIVE and clipper-facing.**

| # | Site | State | This round |
|---|---|---|---|
| 1 | `api/payouts/route.ts:345` `resolveMinPayout` | **LIVE. The only thing that decides.** | untouched |
| 2 | `PayoutRequestFlow.tsx:268,471,535` | LIVE, reads per campaign | untouched |
| 3 | `payouts/page.tsx:239` `selectedMinPayout` | LIVE, reads per campaign | untouched |
| 4 | `payouts/page.tsx:1081` static `$10` | DEAD (`useNewPayouts` const `true`) | **now READS the per-campaign value** |
| 5 | `help/help-redesigned.tsx:72` static `$10` | **LIVE** | **rewritten** |
| 6 | `help/page.tsx:168` static `$10` | DEAD (`showPremiumHelp` const `true`) | **rewritten to match** |
| 7 | `api/chat/conversations/[id]/messages/route.ts:65` | **LIVE** | **rewritten** |

**Copy 7 is the one that mattered most and nobody had seen it.** It is the pattern-matched auto-reply,
reached at `route.ts:357` whenever the AI path returns nothing: *"...enter the amount you want to withdraw
**(minimum $10)**..."*. A clipper on Zhus asking the in-app chat "how do payouts work" was told $10 and
would be refused at $20. That is precisely the failure this round exists to prevent, so it was fixed
rather than merely logged.

## 2.2 The help page is campaign-agnostic. It now says so, and what it does assert cannot rot.

`FAQS` is a **module-level `const`** with no props, no fetch and no campaign context, rendered by
`help/page.tsx` as a bare `<HelpRedesigned />`. **It cannot know which campaign a reader means**, so it
must not name their number. Stated plainly, as the brief required.

What it says instead is the **code invariant**, not a fact about today's data:

> Each campaign sets its own minimum payout. That is the smallest amount you can withdraw from that campaign. If a campaign has not set one, the minimum is $10, and the Payouts page always shows the minimum for the campaign you pick.

`resolveMinPayout(null)` returns exactly `PLATFORM_MIN_PAYOUT_USD`. So **"a campaign that has not set one
is $10" stays true no matter what any owner does next** — it is a property of the code, not a count of
rows. And the pointer is real, verified rather than assumed: `PayoutRequestFlow.tsx:531-537` renders
`Minimum withdrawal on {name} is {amount}` **unconditionally** (the element is always mounted so the
`aria-describedby` idref never dangles; only the text changes).

**I OVERRULED THE ACCESSIBILITY LEAD ON ONE POINT, and the reason is the point of the round.** It
recommended *"Most campaigns use $10"* to protect FAQ search. That is a claim about the population, true
today at 31 of 33, and it **rots silently** the moment the owner raises a third campaign. A sentence that
becomes false without anyone touching it is the exact defect being fixed. The conditional form keeps the
same words findable while being unfalsifiable.

The search cost it was protecting was measured, not hand-waved. The filter at line 266 indexes
`q + tag + a.join(" ")` with a raw `includes`. After the rewrite:

```
  "minimum"        -> MATCHES        "payout"    -> MATCHES
  "minimum payout" -> MATCHES        "withdraw"  -> MATCHES  (newly, matched NOTHING in the FAQ before)
  "$10"            -> MATCHES        "$20"/"20"  -> no match  (accepted residual, below)
```

Every query the lead wanted saved is saved, and the entry gained one it never had.

**Accepted residual, disclosed:** a clipper on a $20 campaign searching the FAQ for "20" reaches the
**levels** entry (Icon $20,000), not payouts. Naming `$20` in static copy was refused for the same reason
as "most campaigns": it is wrong the moment a campaign picks $25.

## 2.3 The dead copies: CORRECTED, not deleted, and here is why

Deleting was the obvious move and it is the wrong one. **Both dead copies sit behind one-flip rollback
flags** (`useNewPayouts = true`, `showPremiumHelp = true`), kept deliberately so either page can be
reverted in a single edit. Gutting them means **a rollback restores a false number** — the failure mode
returns at the exact moment someone is already dealing with an incident.

* **Site 4 (`payouts/page.tsx:1081`) now reads the live value.** `selectedMinPayout` is declared at line
  239 inside the same `PayoutsPage()` component, so the dead modal is in its scope. It now renders
  `Minimum payout on this campaign is {formatCurrency(selectedMinPayout)}` — **the same per-campaign
  figure the stepped flow and the server gate use.** This is strictly better than deletion: it cannot
  drift from the gate again even if the flag is flipped back. That satisfies the brief's "make it read the
  shared value" rather than its "delete it" alternative, which is why that branch was chosen.
* **Site 6 (`help/page.tsx:168`)** has no campaign context at all, so it takes the same honest sentence as
  the live page. Both help surfaces now say the same true thing.

**Deleting the legacy shells themselves stays deferred**, exactly as BL-728 set it: that is a bigger change
than a copy round should carry.

## 2.4 The exhaustive count

**112 line-level references across 15 files.** `grep -rcFf` against a fixed-string pattern file, **never
piped to `head`**:

```
admin/campaigns/page.tsx                     24     payout-minimum-shared.ts                  5
payout-minimum.ts                            17     growth/close-signal.ts                    4
campaigns/[id]/route.ts                      10     payout-refusal.ts                         2
payouts/page.tsx                             10     chat/conversations/[id]/messages/route.ts 1
PayoutRequestFlow.tsx                         9     help/page.tsx                             1
campaigns/route.ts                            9     help/help-redesigned.tsx                  1
payouts/route.ts                              7     ------------------------------------------
earnings/route.ts                             6     15 files, 112 line hits
min-payout-impact/route.ts                    6
```

**Two counting failures happened on the way to that number and both are disclosed, because the brief warns
about exactly this.** A first pass with a combined `-E` alternation returned **112 hits across 14 files and
silently omitted the chat route** through shell escaping of `\$10` — the very truncation failure the rule
exists to prevent, arriving by a different door than `head`. A second pass matched `AdminPayoutShape` and
`AdminPayoutsPage` as false positives, because `Ad|minPayout|Shape` contains the substring. The figure
above is from the fixed-string pattern file, with the chat route present and the marketplace false
positives gone.

## 2.5 Three more literals, REPORTED NOT FIXED

`growth/close-signal.ts:16` (`PAYOUT_MIN_USD = 10`), `growth/in-app.ts:381` and
`growth-email/templates.ts:537` (both `Math.max(0, 10 - totalEarnings)`) frame the ALMOST_THERE
*"you are about $X from the payout minimum"* copy.

Left alone on three grounds, not one. They are **dormant** (`isTriggerLiveEnabled` is default-OFF: an empty
allowlist returns `false` before anything else is considered, so ALMOST_THERE cannot fire today). They are
**lifetime-scoped, not per-campaign**, so a per-campaign minimum does not map onto them cleanly and a naive
substitution would be wrong in a new way. And the growth engine is **ALWAYS-OPUS and outside a display
round's remit**. **Their own round.**

---

# PART 3 — THE STRANDED POPULATION, RE-MEASURED. THE RAISE MOVED IT BY $0.00.

Same arithmetic as PART 1.3, across **all** campaigns, all pairs with a positive effective cap:

```
pairs_total  can_now  stranded_now        under a flat $10 (pre-raise)   flipped_by_raise
144          26       118 / $338.20       118 / $338.20                  0

split of the 118:   $10-default campaigns  113 pairs / $333.39
                    the two $20 campaigns    5 pairs /   $4.81
db_now = 2026-08-07 18:26:09.905208+00
```

**The decisive column is the third against the fourth.** The old rule (flat $10) and the new rule
(per-campaign) were evaluated **on the same rows in the same query**, and they return the **same 118 pairs
and the same $338.20**. `flipped_by_raise = 0`. **The owner's raise changed the stranded figure by exactly
zero pairs and zero dollars.**

That is not a coincidence, it is PART 1.3 restated: the 5 stranded pairs on the raised campaigns hold
$4.81 between them, every one of them was already below $10, and raising the bar above someone already
under it strands nobody new.

**Against BL-731: 115 pairs / $332.00 then, 118 pairs / $338.20 now — a delta of +3 pairs and +$6.20.**
That is ordinary data drift between two measurements (earnings accrued, payouts moved), **not raise
effect**, and the pre-raise column proves it: had the raise contributed, the two columns would differ.

**No minimum was changed by this round.** Still exactly 2 campaigns with a non-null minimum, both $20.0000.

---

# PART 4 — THE EVIDENCE

| Claim | Evidence |
|---|---|
| Both campaigns store exactly $20.00, decimal | PART 1.1: `min_text = 20.0000`, `pg_typeof = numeric`, `= 20.0000` true, `information_schema` says `numeric(18,4)` |
| Per-clipper before and after verdicts | PART 1.3, all **12** pairs, redacted, `BEFORE ($10)` and `NOW ($20)` columns |
| **Nobody flipped from able to unable** | PART 1.3: max cap **$1.66**; `flip = unchanged` on every row; **0** in the $10 to $20 band |
| Help page cannot be wrong | PART 2.2: states the `resolveMinPayout(null)` invariant, points at the always-rendered per-campaign hint |
| Dead copy resolved | PART 2.3: site 4 now reads `selectedMinPayout`; site 6 corrected; choice justified |
| Exhaustive grep count | PART 2.4: **112 hits, 15 files**, `grep -rcFf`, never piped to `head`, two counting failures disclosed |
| Current stranded total | PART 3: **118 pairs / $338.20**, split 113/$333.39 and 5/$4.81 |
| No verdict changed **by this round** | Below |
| No payout touched | Below |

## 4.1 No verdict changed as a result of THIS round

The verdict query was re-run **after** the commit and push:

```
13 pairs. Every row still BLOCKED before and BLOCKED now. flip = unchanged on all 13. Max cap $1.66.
db_now = 2026-08-07 18:48:00.419264+00
```

**Honest about the one difference:** the re-run returns **13 rows where the first returned 12**. A new
clipper (`143d1586`) appeared on Zhus Meme at **$0.00**, verdict `BLOCKED` under both rules. That is the
tracking cron approving an ordinary clip during the round, not an effect of it — **this round changed four
files of display copy and did not touch the gate, the availability math or any money file.**

## 4.2 No payout was created, modified, approved or cancelled

```
payout_rows 158   newest updatedAt 2026-08-07 15:12:04.108   invariant_violations 0
campaigns_with_min 2   approved_clips 4020   db_now 2026-08-07 18:48:13.935694+00
```

**158 payout rows at the start of the round and 158 at the end**, and the newest `updatedAt` across the
whole table is still `15:12:04.108` — **three hours before the owner's 18:16 edits and hours before this
round**. Nothing in that table was written by the owner's raise or by me. Approved clips moved 4,017 to
4,020 on ordinary cron accrual; **invariant violations 0** at both ends.

## 4.3 Money files, byte-identical by blob OID

Working tree `git hash-object` against the `origin/main` blob OID, on both refs:

```
ac5be7de clip-earnings-writer   797e2098 earnings-calc   e887f80a balance   83ce4bab tracking
61cef393 clip-earnings-invariant-middleware   ef5cdae7 money-decimal   106e16ad campaign-era
```

All seven **IDENTICAL**. `tracking.ts` does not appear in the diff. No schema change, **no `prisma migrate`**.

## 4.4 Gates, stated honestly

* `npm ci` **exit 0**, `npx prisma generate` **exit 0** (run after `npm ci`, which wipes the client). Isolated worktree at `C:/b734`, a short path, `.env` and `.env.local` copied, **no `node_modules` junction**.
* `tsc --noEmit` **exit 0, 0 errors** (log was 0 lines).
* `npm run build` **exit 0** pre-commit and **exit 0** post-commit, `✓ Compiled successfully` both times, read from a log with the exit code **echoed by me, never piped through `tail`**.
* Hooks gate **11 problems, 0 errors, 11 warnings — at the limit of 11**, with **eslint v9.39.4 confirmed present**, so the gate is not silently a no-op.
* `check:prisma-bypass` and `check:removed-fields` both ran and passed as part of `prebuild`.
* Push **verified**: `safe-push.mjs` reported `VERIFIED PUSHED`, and `git ls-remote` independently agrees — `refs/heads/checkpoint/BL-734` and `refs/tags/post-BL-734` are both `7a78feb2`, `refs/tags/pre-BL-734` is `ab455ac7`.

## 4.5 Accessibility

Reviewed by the accessibility lead **before any UI was written**, coordinating the ARIA, live-region and
cognitive specialists. Findings applied: rendering is structurally inert to the change (the `role="region"`
panel has no required owned elements, the accessible name comes from `aria-labelledby` on the button, and
the `role="status"` result count derives from the same `useMemo` as the list so they cannot desync); the
entry stays at three paragraphs; the wording drops "per campaign", which reads distributively to a teen
audience, and avoids "platform default", since "platform" already means TikTok/IG/YouTube two lines below.
**One recommendation overruled with the reason recorded** (PART 2.2). The added lines were re-scanned for
smart quotes and dashes: **the only non-ASCII characters are four em dashes inside code comments**, matching
the `BL-XXX —` house style used throughout the repo, and **zero appear in any UI string**. **No dashes as
bullets. No emojis.**

Reported, not fixed, all pre-existing: the zero-results recovery hint is never announced; clearing the
search empties the live region silently; the "start" FAQ renders steps as paragraphs rather than an `<ol>`;
12 panels each carry `role="region"` where APG advises against more than about six; and the Help page says
"minimum payout" while the payout flow says "minimum withdrawal", a terminology split worth settling
product-wide.

---

# WHAT SHIPPED

4 files, **31 insertions, 4 deletions**, display copy only:
`help/help-redesigned.tsx`, `help/page.tsx`, `payouts/page.tsx`,
`api/chat/conversations/[id]/messages/route.ts`, plus the `BACKLOG.md` entry.

**Rollback:** `git revert -m 1 <merge>`, or `git reset --hard pre-BL-734`. **Nothing to undo in the
database** — this round wrote no data at all.

**Not merged to main.** This is a branch round; the merge is its own step per the workflow.
