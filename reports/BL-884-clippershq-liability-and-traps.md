# BL-884 — marketplace v2 round eight: the liability, the erase trap, and the test campaign

Merged `3694df45`. Branch `checkpoint/BL-884` at `f4e0ba9f`. Tags `pre-BL-884`, `pre-merge-BL-884`, `post-BL-884`.

## PART 1 — the premise was wrong, and measuring it first is the finding

The round was set on the reading that both reports **understate** the platform's liability and that
the gap is growing. Measured on 2026-09-17, read-only, **before either report was touched**
(`scripts/bl884-true-liability.ts`, which derives the truth independently from source rows and then
reads `/api/admin/liability` over HTTP with a minted owner cookie, because `liability.ts` imports
`server-only`):

| | gross | cash |
|---|---|---|
| TRUE owed, derived from source rows, 158 people | **$2,980.40** | **$2,726.86** |
| `liability.ts` reports | $3,614.58 | — |
| `admin/payouts/unpaid` reports | $3,704.71 | — |

- First marketplace creator leg: **$0.00 across ZERO rows platform wide.**
- v2 editor leg: **$0.00.** Trainer PENDING: **$0.00.**
- Both reports **OVERSTATE**, by **$634.18** and **$724.31**, for the same documented reason and not a
  new one: both sit on the **LIFETIME** basis, which counts money frozen on videos that no longer
  exist. BL-824's guard records that as deliberate for `unpaid`; `liability.ts` partitions it
  explicitly.
- **Nobody owed money appears in neither report.** Named as required; the list is empty.

So the defect is real, structural and **latent, worth $0.00 today**. It was corrected anyway: the first
creator or editor who earns without owning a clip is the day it stops being worth nothing, and that
person would have been owed money and been in no report at all.

## PART 2 — both reports, both earners, one round

BL-882 and BL-883 each measured this and each refused to half-fix it, because teaching one earner
while the other stays invisible makes a report wrong in a **new** way. Both are counted now, in both
reports, in the same round.

**The legs go INTO each person-and-campaign cell, not beside it.** This is the load-bearing decision. A
separate bucket computed as `max(creator − 0, 0)` would apply the paid offset to one leg and not the
other: $50 of clip money plus $30 of creator money against $60 paid is **$20 owed**, and two buckets
report **$30**.

`owed` gains an **of which** — `clipOwed + mpCreatorOwed + mpEditorOwed` — which closes on it **to the
cent**, because the clip share is a **residual** rather than a third proportional slice.

**I overrode the accessibility spec's Ruling 0 after disproving its premise.** It argued that folding
the legs into `T.owed` would falsify the rendered prose at `LiabilityView.tsx:349-354`. Reading the
code: `retired = owed − withdrawable − stuck` is a **residual**, so that identity holds by construction
whatever `owed` becomes. The reason given for separate buckets was the reason not to have them.

Also shipped: an `invisibleEarners` list naming anyone whose whole position is marketplace money; a
per-campaign of-which inside the existing disclosure; `aria-controls`/`id` on that disclosure; and on
`admin/payouts` a **Kind** column, a `<caption>`, `scope` on all nine heads, `<th scope="row">` on the
clipper cell, and `colSpan` 8 → **9**.

## PART 3 — the erase trap, and why a third option was built

**Why the price cleared, established before deciding how to fix it:** `settle/route.ts:222-238`,
`clipperLiability` **prefers** `actualPaidAmount`, so a priced-then-closed request releases most of its
money. Leaving the price on a closed row was therefore never an option, and preserving the owner's
decision by doing nothing would have been worse than the bug.

The figure is copied to `settledPriceSnapshot`, a column **no money path reads**, enforced by a guard
that walks `src/` and allows exactly one file. The full gross stays held, and reopening puts it back
with a stamp naming the **restoration** rather than replaying a stale one. A row closed before the
column existed reopens with no price — the honest outcome; inventing one would be worse.

The shipped dialog sentence that warned the price would be lost now reads, with the amount named:

> The $7.00 you set on this request is kept. Reopening brings it back exactly as it is now.

Proved at all three points for **both** earners: set, close, reopen.

## PART 4 — the test campaign, decided rather than mirrored a fourth time

The gate's inclusion was never a decision: its creator query simply carried no campaign relation
filter, and everything beside it copied that shape. **Measured before deciding:** one test campaign
exists, holding ZERO clips, ZERO earnings and ZERO payout requests, so the rule strands nothing and
nobody. Enforced with a typed `CAMPAIGN_IS_TEST` refusal at the **one place that decides payment**
rather than in five display aggregates — if nothing can be requested, whether an owner's accounting
view counts one is a question about a screen, not about money. **The one consequence, named rather
than left to be found:** flipping the flag ON for a campaign that already holds real earnings would
stop those people withdrawing.

## PART 5 — the guards, and the two that could not fail

**Two checks in this round's own guard could not fail.** The L check tested `src.includes(...)` for the
editor table while `liability.ts` holds **two** such calls; the T check tested for one exclusion site
while each clipper surface holds three to six. Breaking one of each left the guard green. That is the
**fifth and sixth** guard on this platform caught unable to fail, after BL-835, BL-881, BL-882 and
BL-883's S4 — and all six were caught the same way, by running the demonstration rather than trusting
the guard. Both assert **counts** now.

**The demonstration no longer samples.** It breaks **all thirteen** checks one at a time, each required
to name itself, tree restored and re-verified after each: **13 of 13 failed on demand.** The seven I
had not sampled were exactly the ones I had no evidence about, and two of the six I had sampled were
broken.

| prebuild guard | wired | result |
|---|---|---|
| `check:prisma-bypass` | yes | 0 violations |
| `check:removed-fields` | yes | OK |
| `check:event-wiring` | yes | 0 problems |
| `check:v2-leg-sync` | yes | OK, 3 files documented |
| `check:v2-editor-balance` | yes | 19 passed, 0 failed |
| `check:paid-is-final` | yes | 14 passed, 0 failed |
| `check:payout-snapshot` | yes | 9 passed, 0 failed |
| `check:css-tokens` | yes | 3 passed, 0 failed |
| `check:liability-rules` | yes | **13 passed, 0 failed** |
| `lint:hooks` | yes | 0 errors, 10 warnings (ceiling 11) |
| `check:schema-drift` | **NO** | **RED, 10 pre-existing drift items** |

`check:schema-drift` is the only guard `prebuild` does not run, and it is red on seven orphan tables
and three orphan columns, **none of them this round's**. It cannot be wired until those are resolved,
because wiring a red guard breaks every build. It does **not** flag
`payout_requests.settledPriceSnapshot`, which independently confirms this round's `ALTER` and its
`schema.prisma` field agree. Second unwired guard found, after BL-882 found BL-824's.

## PART 6 — the sandbox, and three checks caught passing for the wrong reason

**77 of 77 sandbox checks. 10 of 10 renders.** After runs that failed 1, 3 and 1, all reported.

Every failure path has its own user, asserts the status is **not 429**, and states **what made it
pass**. Three of this round's own checks were caught wrong and rewritten:

1. Two failure paths asserted a bare status **number** where the route answers a **typed code**, and
   409 rather than 400 deliberately. Both now assert the code.
2. The setup for six failure paths was silently producing **no payout at all** — the editor was minting
   a clip per person and hitting the submission limit — so a 404 from an `undefined` id was being read
   as the refusal under test. The setup is a **check** now.
3. The check asserting both invisible earners were listed matched **one row twice**, because every
   sandbox id truncates to the same 8 characters. **This found a real defect in what shipped:**
   `InvisibleEarner` carried a truncated id whose entire purpose was to let the owner find the person,
   and **40 of 1,762 users share an 8-character prefix**. It carries the whole id now, and the screen
   links to `/admin/users/{id}`.

**Accessibility review: six findings and one correction to my own comment, all verified against source
before being acted on, all seven applied.** The settle dialog's state string is now a live region — as
an `aria-describedby` target it is spoken on focus and never again, so a person sitting on the
focusable `aria-disabled` button and pressing Enter heard nothing. The price dialog deliberately did
**not** get one: `bl861-price-cash` is already `aria-live` and would double-speak. The blocking
condition is now visible as well as spoken. The profile link's bare icon made the new
`<th scope="row">` resolve to "name Open profile" and say it before all eight figures on the row. Both
surfaces now name the two earner kinds identically. And my own rationale comment claiming the dialog
had "exactly one tab stop" was overstated and is corrected — a wrong reason in a comment is how the
next round re-derives a wrong conclusion.

**Measured and deliberately not swept in: 262 dangling `aria-controls`** on `/admin/payouts` at every
one of five widths, from `page.tsx:1818` emitting the attribute unconditionally against a
conditionally-rendered target. `LiabilityView.tsx:803` gets the identical pattern right. One line, but
inside the thirteen `admin/payouts` defects this round was told not to fold in, so it is in BACKLOG
with the measurement.

**Renders measure the pan, not `scrollWidth`:** 0 px at 320, 375, 414, 1280 and 1440 on both surfaces,
`innerWidth` and the URL read back each time, against a production build with `DEV_AUTH_BYPASS=false`
and a real minted session cookie.

**Seven protected money files byte-identical by blob OID**, `tracking.ts` among them. **49 of 49
sandbox rows removed and verified**, nothing unremovable; the platform re-measured afterwards at zero
creator rows, zero editor rows and zero held price snapshots. No Apify actor ran; no wallet address was
printed; the 11 BL-678 guards are intact.

## What the owner truly owes, right now

**$2,980.40 gross, $2,726.86 cash, to 158 people.** Not the $3,614.58 the liability page was showing,
and not the $3,704.71 the unpaid report was showing. The difference is money frozen on videos that no
longer exist, which both surfaces count on purpose and now say so on the row.

**Rollback:** revert the merge commit, then
`ALTER TABLE payout_requests DROP COLUMN IF EXISTS "settledPriceSnapshot"`. Nothing reads that column
except the settle route, so dropping it strands no money; any price kept on a row closed while it
existed is lost on the drop, which is the state BL-864 measured as the bug.
