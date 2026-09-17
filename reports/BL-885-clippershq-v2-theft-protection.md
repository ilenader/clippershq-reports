# BL-885 — marketplace v2 round nine: the theft protection BL-876 designed and nobody built

Merged `fcbb2a9`. Branch `checkpoint/BL-885` at `3e9480a8`. Tags `pre-BL-885`, `pre-merge-BL-885`,
`post-BL-885`. Merge tree `a1775065` equals the branch tree, so the branch build **is** the merge build.

**Model split.** Opus wrote every line that moves money between two people: the conversion, the
poster's paid floor, the strike gating, the reconciliation verdict and this report, with no subagent
between it and the source. One Sonnet retrieval agent mapped `clipper-submit-core.ts`, the schema
models and `campaignType`'s readers; every load-bearing claim it returned is marked VERIFIED below
because I re-read it myself. One accessibility agent reviewed the new surface; all six of its findings
were verified against source before being acted on.

## PART 0 — what exists today, measured before building

| | measured 2026-09-17 |
|---|---|
| v2 clips / posts / editor earnings | **0 / 0 / 0** |
| campaigns of type `BOTH` / `MARKETPLACE_ONLY` / `NORMAL` | **0 / 0 / 34** |
| `marketplace_strikes` rows | **31**, every one `EXCESSIVE_REJECTIONS`, every one `EXPIRED`, 22 people |
| live bans, all three sources | **0** |
| strikes issued by a fetch result | **0** — the missed-deadline class BL-845 found has zero rows |
| v1 strike creation sites (VERIFIED by my own grep) | **5**: one human, four automatic — matching BL-871 |
| conversion actions of any kind | **none** |
| anything attributing a clip to a non-owner | **none** |

> **THIS PROTECTION PRECEDES THE EXPOSURE, AND THAT IS THE RIGHT ORDER.** With zero v2 clips and the
> campaign type never set, **no editor's work exists to steal**. This round closes no live wound, and
> saying so plainly is better than implying otherwise.

All 31 strikes came from `excessive-rejections.ts:207` — automatic, but counting rejections a human
made. **Nobody is banned today because of one.**

## PART 1 — the conversion, which is the one that pays somebody

An owner action that re-attributes a NORMAL clip to a named editor and splits it 45/45/10. Available
**generally**, as the owner asked, not only as a theft remedy; nothing in it mentions or records theft.

**It writes no money code, and that is the point.** Every dollar goes through
`recomputeV2PostEarnings` → `writeMarketplaceV2Earnings` → `writeClipEarnings`, so it inherits the L1
budget hard lock, the four-field invariant, BL-881's three-leg sync, both paid floors and BL-882's
campaign-comes-from-the-clip rule without restating any of them. BL-881 put the sync in the chokepoint
precisely so a new writer would inherit it. `check:v2-leg-sync` passes.

### The money question, answered by tracing the tick rather than by preference

BL-876 offered three shapes and called the choice the owner's. **Two are not buildable**, and that is
a finding, not an opinion:

1. **Forward only** — nowhere to live. `Clip.earnings` is a running total recomputed from lifetime
   views every tick, not a ledger of increments.
2. **Redistribute the remainder** — **undone by the very next tick**, which recomputes the editor's 45
   percent *from gross* and knows nothing about the poster's floor. That is the BL-882 trap exactly.
3. **The platform covers the gap** — what the architecture already does, and the only one that
   survives.

**So the recommendation is not really a recommendation: it is the only shape a tick does not reverse.**
The editor gets a full 45 percent, the poster is held at what he has already been paid, and when the
floor binds the difference is the owner's. He is not asked to choose; **he is shown the number before
he presses the button.**

**The worked example, from the sandbox, both cases:**

| | poster before | poster after | editor | platform | campaign spend | costs the owner |
|---|---|---|---|---|---|---|
| **paid nothing** (every case today) | $100.00 | $45.00 | $45.00 | $10.00 | $100.00 → **$100.00** | **$0.00** |
| **paid $80.00 already** | $100.00 | **$80.00, held** | $45.00 | $10.00 | $100.00 → $135.00 | **$35.00** |

Money already paid stays paid and his **record** stays above it. BL-826 measured what breaking that
costs: 40 clips carrying $140.54 multiplied down to $25.65 against $78.54 paid, and Mark Paid then
jammed permanently against the `payout_amount_positive` CHECK constraint.

### The v2 poster had no paid floor on any path

The v1 marketplace poster has one (`tracking.ts:2985`). The v2 **editor** has one
(`floorV2EditorEarnings`). Between them the v2 **poster** was left with none:
`recomputeV2PostEarnings` writes a breakdown computed from views, the v2 fork in `tracking.ts` calls
`writeClipEarnings` directly, and neither consults what he has been paid — while `writeClipEarnings`
says in its own header that *"Decreases always pass."* With zero v2 clips it has never bitten.
`floorV2PosterEarnings` now sits **inside** `writeMarketplaceV2Earnings`, deliberately, because a
floor applied only at the conversion is a floor the next tick removes.

### The first draft was broken in the most important way

It created the post row, wrote all three legs, and **never set `Clip.marketplaceV2PostId`**. That
column is what `tracking.ts:2292`, `marketplace-v2-sync.ts:146` and `V2_RECONCILE_BODY:313` all use to
identify a v2 clip. **The next tracking tick would have paid the poster 100 percent again and silently
reversed every conversion.** Found by BL-881's own leg-sync guard refusing an opt-out the file had
asked for — a guard catching the *absence* of a line.

### Reversible, and what the undo does to money

The undo deletes the post and both legs, clears the stamp and restores the poster to 100 percent.
Two things stop it, and both **refuse rather than half-act**: if the editor has been paid on that
campaign it refuses with `EDITOR_ALREADY_PAID`, because deleting a leg he has withdrawn against is the
clawback BL-824 forbids; and the restoration is an INCREASE, so the L1 budget lock applies and a
campaign over budget rolls the whole Serializable transaction back. Proved in the sandbox: undo
restored $45.00 → $100.00, then reconverted cleanly.

Every conversion writes an audit row carrying `posterBefore`, `posterAfter`, `editorAfter`,
`platformAfter`, `extraCost`, `posterClamped` and `dbNow` cast to `::text` against the database's own
`now()`. BL-732 found a cascade that wrote no audit row and went unnoticed for three days.

## PART 2 — the strikes, built with the history in front of me

Three strikes, the third a **seven day ban from NORMAL posting only**. A **new** table, and both
reasons are hard: `isUserMarketplaceBanned` derives a MARKETPLACE ban from the old one and this
penalty is the opposite surface; and that table has **four automatic writers against one human**, so
sharing it would be sharing an automatic entrance into a count that must be human-only.

- **ONE creation site**, `issueV2Strike`, with `issuedById` required against a NOT NULL column.
  `check:v2-strike-sites` counts it and fails the build at anything but exactly one, and fails if any
  file under `src/app/api/cron/` so much as *mentions* the table.
- **No ban scalar.** BL-841 measured `User.clipperMarketplaceBannedUntil` written by one cron and
  **cleared by nothing**. The ban is `count of live strikes >= 3` computed at read time, so revoking
  lifts it by construction.
- **No cron.** BL-841 measured `decay-strikes` at **zero rows in `cron_runs`** — it has never run, so
  strikes have never decayed here. Expiry is a WHERE clause.
- **A banned poster's money is untouched.** BL-883's pair, followed exactly: the leg stands and the
  withdrawal is refused.

**The copy, at all three stages, and nobody is called a thief.** Strike one warns explicitly:

> A clip you posted was made by another editor and submitted as your own work. When you post someone
> else's marketplace clip, post it through the marketplace so the editor gets paid too. **This is
> warning one of three. A second warning follows if it happens again, and a third stops you posting
> your own clips for seven days. Nothing has been taken from your earnings.**

Strike two: *"This is warning two of three. One more and you will not be able to post your own clips
for seven days…"* Strike three: *"From now until [date] you cannot submit your own clips. You can
still post marketplace clips and you still earn on everything already live. Your earnings are
untouched. If you think this is wrong, reply in Discord and the owner will look at it again."* On
revoke: *"The owner looked again and removed one of your warnings. Nothing was counted against you."*
The sandbox asserts that none of *thief, steal, stole, fraud, cheat* appears anywhere. **The owner is
looking at two videos with his own eyes and may be wrong.**

**Should a strike and a conversion be one action? No, and the recommendation is in the route.** They
answer different questions: **a conversion pays the editor; a strike only deters the poster.** The
first event is usually confusion, which BL-876 §3.5 showed the interface itself causes on a BOTH
campaign. The comparison screen shows the poster's current warning count so pairing is one click away
without being forced. **Convert first; warn only on a repeat.**

## PART 3 — the comparison aid, and what it cannot do

The owner's eyes are the instrument. The page puts the clip beside the campaign's approved catalogue,
newest first, with thumbnails and a link to **watch** each editor's clip. **No score, no flag, no
ranking, no suspicion list** — the sandbox asserts that *score, suspicion, likelihood, confidence,
match* appear nowhere in the response, and the render asserts the same of the rendered page.

The page says what it cannot do, in its own copy, first and not in a tooltip: it cannot tell you
whether two videos are the same video; it does not score or rank; and it only shows clips on **this**
campaign, so work taken from another campaign or from outside the platform does not appear at all.

## PART 5 — the guards

**A seventh check could not fail, and it was this round's own.** The reconciliation check asserted
`>= 2` uses of the poster floor — a presence test wearing a number. The demonstration removed one and
it stayed green. It asserts an exact **4** now, each load-bearing. That is the seventh after BL-835,
BL-881, BL-882, BL-883's S4 and BL-884's L and T — and like all of them, caught by *running* the
demonstration.

**All 20 checks this round adds or touches were demonstrated failing, one at a time, never sampled**,
each required to name itself, tree restored and re-verified after each. **20 of 20.**

**Three guards on this platform counted prose rather than code, and all three are fixed.**
`check-v2-leg-sync.js` refused a file that had *removed* the opt-out because the comment explaining
the removal still contained the word; `check-v2-editor-balance.js` S4 refused a route that had
switched to the relation for the same reason; and BL-885's own guard reported *three* creation sites
on a tree with one, counting its own documentation. A guard a comment can break gets silenced by
deleting the comment.

| prebuild guard | wired | result |
|---|---|---|
| `check:prisma-bypass` | yes | 0 violations |
| `check:removed-fields` | yes | OK, 826 files |
| `check:event-wiring` | yes | 0 problems |
| `check:v2-leg-sync` | yes | OK, 3 documented opt-outs |
| `check:v2-editor-balance` | yes | 19 passed, 0 failed |
| `check:paid-is-final` | yes | 14 passed, 0 failed |
| `check:payout-snapshot` | yes | 9 passed, 0 failed |
| `check:css-tokens` | yes | 3 passed, 0 failed |
| `check:liability-rules` | yes | 13 passed, 0 failed |
| `check:v2-strike-sites` | yes (**new**) | **16 passed, 0 failed** |
| `lint:hooks` | yes | 0 errors, 10 warnings (ceiling 11) |
| `check:schema-drift` | **NO** | **RED, 10 pre-existing drift items — NOT fixed here, stated so it is not lost** |

## PART 6 — the sandbox

**75 of 75 checks. 5 of 5 renders.** After runs that failed 1, 11 and 1, all reported.

The theft ran end to end as people, through real HTTP routes with real minted session cookies: the
editor submitted, the owner approved, **the poster submitted it as his own normal clip and earned 100
percent** (nothing refused him, and nothing should have — the ordinary submit route carries zero
marketplace references), the owner compared, converted, and the editor was paid. Then three warnings,
the ban, and the reversal.

**Four of my own checks were caught wrong and rewritten:**

1. The paid-is-final invariant compared against the **payable** basis, where **26 pre-existing
   person-campaign pairs** legitimately sit because a retired video leaves that basis while the
   payment against it was real. Measured with every sandbox row excluded. It now asserts this run
   added none.
2. The audit check read properties off a **JSON string** and reported a perfect row as all zeros.
3. `setViews` used `updateMany` on clips with no `ClipStat` row, so views stayed 0, the gross was 0,
   and **the whole money proof read $0.00 while every route returned 200**. It asserts the value
   landed now.
4. The render counted **every** live region in the document rather than this page's two.

**The teardown also refused three times, correctly**, because I ledgered product-minted rows without
naming a sandbox-owned column. That is LOCK 2b working. Two ledger rows pointed at rows a SELECT
confirmed were **already gone**; those lines were dropped and it is recorded here rather than quietly.

**Nothing is unremovable.** 37 of 40 rows deleted, 3 already gone by cascade, 0 failed, and the
destroyer's own verification reads *0 of 40 recorded rows remain*. Afterwards: 0 sandbox users, 0 v2
clips, 0 v2 strikes, 0 editor legs, v1 strikes still 31, and **both fingerprints identical to the
opening snapshot** — payouts `4b25d9d0…`, clips `b9ed8c77…`.

Reconciliation, both forms, before and after: **0 leaks, 0 rows out of balance** at both ends. The
clamped-poster row read `EXPLAINED: the poster is held at money already paid to him` with
`poster_paid_floor $80.00` — without the arm this round added to the verdict it would have read LEAK,
which is the exact defect BL-883 rewrote that query to remove for the editor.

Renders measure **the pan**, not `scrollWidth`: **0 px at 320, 375, 414, 1280 and 1440**, with
`innerWidth` and the URL read back, against a production build with `DEV_AUTH_BYPASS=false`.

**The accessibility review found the live regions did not work at all**, and it was right: `role` was
patched on one reconciled DOM node rather than remounted, the loading region was born already holding
its text, and the loaded state unmounted the only one there was — **a successful load completed in
silence**. The repo already had the fix as a house convention at `admin/fraud-review/page.tsx:311`. It
also found the page said *"Watch both and decide for yourself"* while **there was no way to watch the
editor's clip at all**, which defeated the page's whole premise. Both fixed, plus `--link-text` for
contrast, `role="list"`, a fourth landmark label, and a readable fallback where a username is null.

**Six protected money files BYTE-IDENTICAL by blob OID on both refs.** `marketplace-v2-writer.ts`
**CHANGED**, 185 insertions and 8 deletions, declared loudly: it is the only place a poster floor
survives a tick. No Apify actor ran, no wallet address was printed, the 11 BL-678 guards are intact.

## Everything still between the owner and a real editor using this

1. **BL-879's visibility gates are closed.** No editor can reach the marketplace v2 surfaces until
   they are opened.
2. **No campaign has a type set.** All 34 are `NORMAL`, so no editor can submit anywhere and no poster
   sees a catalogue. He must set at least one campaign to `BOTH` or `MARKETPLACE_ONLY`.
3. **A redeploy is owed.** `marketplace_v2_strikes` is applied to the database, but the code that
   reads it ships with this merge.
4. **The strike window is 90 days and the ban is 7**, both one-line constants. BL-876 said the window
   is his call, not a round's.
5. **Question 16 is still open** — whether a poster may see which other posters took the same clip.
6. **Question 14 is still open** — whether changing a campaign's type mid-flight should be blocked or
   grandfathered.
7. **`check:schema-drift` is red and unwired**, ten pre-existing drift items.
8. **262 dangling `aria-controls` on `/admin/payouts`**, measured at five widths by BL-884.
9. **The thirteen `admin/payouts` accessibility defects** are still open.
10. **The 33 inert `bg-[var(--bg-page)]` sites** still need a real token and a visual review.
11. **`text-accent` fails 1.4.3 in the light theme, repo-wide.** `globals.css:102` documents it and
    ships `--link-text` as the fix, but CLAUDE.md mandates `font-bold text-accent` for money on every
    page. **That is a rulebook conflict and his call.**
12. **No admin page sets a `<title>`** — all 43 inherit one, a 2.4.2 failure, in tension with
    CLAUDE.md's "Tab title: just Clippers HQ".

**The worktree, stated exactly.** Git's registration is pruned and `git worktree list` shows only
the main checkout; every file under `C:/w/b885` is deleted and the directory measures **0 entries**.
The bare directory NODE survives because one of this session's own lingering shells still holds it as
its working directory, and six removal attempts over thirty seconds did not clear it. It is empty and
unregistered, and it disappears when those shells exit. Nothing about it is claimed as clean that is
not.

**Rollback:** revert the merge commit, then `DROP TABLE IF EXISTS marketplace_v2_strikes`. Nothing
else reads that table and no conversion has been run on real data, so dropping it strands no money.
