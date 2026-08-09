# BL-754 — adversarial review of BL-752's per-clip CPM spec: two real gaps, four attacks that failed

**VERDICT IN ONE LINE: NOT safe to build exactly as written. The core design survives every attack I made on it, but the spec has TWO material gaps, both of which reintroduce a defect a previous round already paid to fix: BL-736's reassignment silently erases an override, and the admin row would show an owner figure the displayed rate did not produce, which is the exact confusion BL-744 was built to eliminate.**

**2026-08-09 · READ ONLY · Base:** `main @ d169e73b` · **Branch:** `checkpoint/BL-754`
**Nothing changed. `git status --porcelain` is 0 lines and worktree HEAD equals `origin/main`. No code, no data. Every timestamp cast `::text` against DB `now()`. Handles redacted. No probe, $0.00, no Apify actor. Nothing BL-753 holds was touched.**
**No build, `tsc` or lint run was performed and none is claimed.**

---

# PART 1 — EVERY LOAD-BEARING CLAIM, RE-VERIFIED

Nothing below is inherited. Each was counted or computed here.

## 1.1 There are ELEVEN money call sites, not nine

`grep -c` over `src/` for `resolveClipCpms(` excluding the definition returns **11**:

```
admin/fix-earnings/route.ts:202          admin/fix-earnings/route.ts:255
admin/force-recalc-earnings/route.ts:347 clips/[id]/override/route.ts:268
clips/[id]/review/route.ts:473           agency-monitor.ts:125
gamification.ts:826                      owner-submit-core.ts:347
proportional-cut.ts:125                  tracking.ts:2032
tracking.ts:2068
```

**BL-752 contradicts itself.** Its headline says *"I checked all nine `resolveClipCpms` call sites"*, its
table collapses `fix-earnings` `:202` and `:255` into one row to reach ten, and four paragraphs later its own
text says *"until all eleven literals were edited"*. **The correct number is 11.**

**This is a counting error, not a design error**, and I say so plainly rather than inflating it: the
substantive claim survives.

## 1.2 The override branch IS genuinely unreachable, at all eleven. Verified one by one.

I read every one of the 11 rather than trusting the table. **Every single one passes a hand-built object
literal with exactly three keys** (`platform`, `cpmAtSubmissionDecimal`, `ownerCpmAtSubmissionDecimal`).
**Not one spreads the clip object**, which is the only way `clipperCpmOverride` could arrive.

`cpm.ts:170-181` confirms the branch reads keys that no caller supplies:

```ts
const clipperOverride = toNumberOrNull(clip.clipperCpmOverride);
const ownerOverride   = toNumberOrNull(clip.ownerCpmOverride);
return {
  clipperCpm: clipperOverride ?? frozenClipper ?? live.clipperCpm,
  ownerCpm:   ownerOverride   ?? frozenOwner   ?? live.ownerCpm,
};
```

**BL-752's central claim holds. The stamps are the per-clip rate, and the override branch is dead.**

## 1.3 A property BL-752 states loosely and I am tightening

BL-752 says all eleven *"honour the clip's frozen stamps rather than reading the campaign live"*. **That is
true only when the stamp is present.** `cpm.ts:179-180` falls back to the live campaign **per side,
independently**, so a clip with a clipper stamp and a NULL owner stamp resolves **the clipper from the clip
and the owner from the campaign**.

That mixed state is exactly the refusal class, so it does not break the design. **But BL-752's rule 5 has an
OR clause that walks into it:** *"both stamps present and > 0, **or a live campaign pair is available to
derive `r` from**"*. Deriving `r` from the campaign and writing both stamps **converts a clip that was
following the live campaign into a frozen one**, permanently. That is a real semantic change and the spec
does not disclose it. **Either drop the OR clause or state the conversion in the confirmation.**

## 1.4 The arithmetic, recomputed independently including BL-743's non-round case

`s = 0.39005794`, so `implied = s / (1 - s) = 0.639501...`

| case | old pair | typed clipper | derived owner (round4) | new ratio | \|implied − ratio\| | verdict |
|---|---|---|---|---|---|---|
| BL-743 live | 0.2000 / 0.1279 | $0.50 | 0.31975 → **0.3198** | 0.639600 | **0.0000989** | PASS |
| non-dividing | 0.2000 / 0.1279 | $0.33 | 0.211035 → **0.2110** | 0.639394 | **0.000107** | PASS |
| boundary | 0.2000 / 0.1279 | $0.005 | 0.0031975 → **0.0032** | 0.640000 | **0.000499** | PASS |
| owner's 50/50 | 0.3000 / 0.3000 | $0.50 | **0.5000** | 1.000000 | 0.000000 | PASS |

**BL-752's table is arithmetically correct**, including the case it flagged as non-round. The absorbing side
is the owner side, as stated, and the clipper receives the typed number to the digit.

## 1.5 The counts are wrong, and the tolerance margin is smaller than BL-752 implies

Re-measured live, `db_now = 2026-08-09 19:05:55.382295+00`:

| | BL-752 | **measured today** |
|---|---|---|
| never-earned on ACTIVE | 123 | **130** |
| refused, no split to preserve | 49 | **27** in this population |
| **eligible after all rules** | "123 minus up to 49" | **103** |

The 123 to 130 gap is ordinary churn. **The 49 is a different denominator**: BL-752 counted owner-stamp
gaps across all 5,193 clips in its PART 2 table, not within the eligible set. Within the eligible set it is
**27**. The spec should quote 103 and 27, because those are the numbers the owner will see in the UI.

**What "no split to preserve" means, and how it fails:** the clip has a clipper stamp but a null or zero
owner stamp, so `r = o/c` is undefined or 0. Such a clip is **already ambiguous under today's guard and the
owner already earns $0.00 on it.** BL-752 is right to refuse rather than repair. It fails **safely** provided
the UI names the reason; refusing with a generic error would be confusing, and the spec does say to give a
reason.

**A margin claim I am correcting.** BL-752 says the rounding perturbation leaves *"a margin of more than
100x"*. That is the margin on the **CPM floor**, not on the **ratio budget**, and the two are different
quantities. I measured the ratio gap that eligible clips **already carry before any scaling**:

```
eligible clips already ambiguous              0
eligible clips within half the tolerance      0
WORST existing |implied - stampedRatio|       0.004000   against a 0.01 tolerance
```

**40% of the tolerance is already consumed on the worst eligible clip**, from 4dp stamping at submission and
hand-set pre-calculator rates. Adding the worst scaling perturbation (0.0005 at the $0.005 floor) gives
0.0045, still inside. **So the design holds, but the true worst-case margin is about 2.2x, not 100x**, and
the spec should say so rather than imply comfort it does not have.

---

# PART 2 — ATTACKING THE ARITHMETIC. Every attack failed.

| attack | result |
|---|---|
| **Owner CPM zero** | `r = 0`, derived owner 0, ratio 0 against implied > 0, gap > 0.01. **Refused by rule 5.** BL-752 is correct. |
| **Clipper CPM zero** | `r` divides by zero. Measured: the clipper stamp is **never** null or zero on any eligible clip, so the denominator always exists. Rule 5's `> 0` closes it regardless. |
| **Non-dividing ratio** | 0.1279/0.2000 scaled to $0.33 gives gap 0.000107. PASS. |
| **Very small** | $0.005 gives 0.000499. PASS, and it is the documented floor. |
| **Very large** | The perturbation is `0.00005 / newClipperCpm`, which **shrinks** as the rate grows. Large values are strictly safer. No attack available. |
| **Ghost-fee campaign (BL-630)** | **No fee column exists at runtime.** BL-627 risk 1 records that `campaign.budget` stores the marketed figure and the ghost fee has no runtime representation. There is nothing for a rate change to restate. |
| **Hand-set pre-calculator campaign** | This is where the 0.004 worst-case gap comes from. It does **not** break the guard, and the design preserves whatever gap exists rather than widening it. |

**Which side absorbs the fractional cent, and do the parts reconcile.** The **owner** side absorbs it, by
construction: the clipper's rate is the typed number and the owner's is `round4(clipper × r)`. The parts
reconcile because **nothing downstream re-derives the owner from the clipper at cent precision** on this
path; the owner amount is computed from its own stamp, or on the guarantee path from `s` directly. The
maximum owner-side error is **$0.00005 per 1,000 views**.

**Is this BL-539's ambiguous-row shape returning?** **No, and I tried to make it so.** BL-539's shape is a
ratio that **drifts away from `s`**. Here `s` never moves and `r` is preserved to within 0.0005, so the gap
after equals the gap before plus a perturbation two orders of magnitude below the tolerance. **Cumulative
drift across many clips is impossible because each clip is scaled from its own stamps independently; there
is no accumulator.** A clip scaled ten times in succession would drift, but each application re-derives `r`
from the current stamps, so the drift is 0.0005 per application and would need roughly 12 successive
overrides on the same clip to breach the tolerance. **Worth one line in the spec; not a blocker.**

---

# PART 3 — ATTACKING THE BOUNDARY. One race is genuinely open.

## 3.1 A clip that begins earning mid-check. CLOSED, if built as specified.

BL-752 specifies re-checking eligibility **inside** the transaction under `SELECT ... FOR UPDATE`, the
BL-736 pattern. That genuinely closes it: the tracking tick writes `Clip.earnings` through
`writeClipEarnings`, which updates the same row, so the row lock serialises them. **The spec is right, and it
is right for the right reason.** It also correctly identifies that the tick fires at exactly `:00 UTC`, so
the window between dialog and confirm is real.

## 3.2 The tick firing mid-transaction. CLOSED, same lock.

## 3.3 A simultaneous BL-736 reassignment. **NOT CLOSED. This is gap 1.**

`reassign-campaign/route.ts:347-354` writes, in one update:

```ts
data: {
  campaignId: destination.id,
  cpmAtSubmissionDecimal: stamps.clipperCpm as any,
  ownerCpmAtSubmissionDecimal: stamps.ownerCpm as any,
},
```

**It overwrites BOTH stamps from the destination campaign, and it has no knowledge of any override.**

**The two features target overlapping populations by construction.** Reassignment requires `PENDING` and
`earnings = 0`; the override's eligible set contains **22 PENDING clips with `earnings = 0`**. The same clip
can be both.

**The row lock does not save it.** Both operations take `FOR UPDATE` on the clip, so they serialise rather
than interleave, but serialising them does not help: reassignment re-asserts only `status = PENDING`,
`campaignId` unchanged and `earnings = 0`. **An override changes none of those**, so every assertion still
passes and the reassignment proceeds to erase the override **silently, with no trace and no warning.**

**BL-752's `cpmOverriddenAt` column does not cover this.** Its failure mode 6 names only
`restampClipsForCampaign`, and its PART 7 edits exactly one file, `cpm-restamp.ts`. I confirmed
`cpmOverriddenAt` appears **nowhere** in the codebase today, so there is no existing guard to inherit.
**Reassignment is a second eraser the spec does not name.**

**What must be added:** `reassign-campaign/route.ts` must either refuse a clip whose `cpmOverriddenAt` is
non-null, or carry the override forward by re-deriving the pair against the destination's `s`, and must say
which in the confirmation. **Refusing is the safer default**, because carrying it forward silently changes
the economics the owner agreed to.

---

# PART 4 — ATTACKING DOWNSTREAM

## 4.1 BL-642's two spend filters. Attack FAILED.

`balance.ts:312` filters the clip side on `videoUnavailable: false`; `:315-317` leaves the legacy agency
aggregate **unfiltered**. **That asymmetry is about WHICH ROWS are counted, not about rates.** An override
scales both sides of one clip together, so it moves both aggregates by the same clip's contribution and
introduces **no new disagreement**. I looked for one and there is none.

## 4.2 Pool cap, fully-spent, no-overpayment, no-over-budget. Attack FAILED.

An override that raises a rate raises projected spend, so the campaign reaches its cap sooner and
auto-pauses. **That is correct behaviour and BL-752 says so.** The L1 lock in `clip-earnings-writer.ts`
rejects any write whose `projected > budget` on an increase, and this feature adds no cap and writes above
none, so **BL-627's no-overpayment and the no-over-budget property BL-718 nearly broke are both preserved.**

## 4.3 BL-744's admin row. **GAP 2, and it is the sharpest finding of this review.**

**BL-752's own eligibility rule 2 forces every overridden clip into the one display branch that reads the
campaign instead of the clip.**

`admin/clips/page.tsx:1705-1724`:

```ts
let normalOwnerAmt: number | null = null;
if (clip.agencyEarning?.amount != null) {
  normalOwnerAmt = clip.agencyEarning.amount;        // :1707  stamp-derived, correct
} else if (pricing === "CPM_SPLIT" && ownerCpm && viewsForCalc > 0 && clip.status === "APPROVED" && ...) {
  normalOwnerAmt = Math.round((viewsForCalc / 1000) * ownerCpm * 100) / 100;   // :1724  CAMPAIGN rate
}
```

`ownerCpm` on `:1724` is `clip.campaign?.ownerCpm`, the **campaign's live rate**. Meanwhile BL-744's rate
line at `:1807-1810` prints `fmtRate(stampOwner)`, the **clip's stamp**.

**Rule 2 requires that no AgencyEarning row exists**, so `:1707` can never fire for an overridden clip and
`:1724` always does. After an override scaling the owner stamp from $0.1279 to $0.3198, the row would render:

```
Owner gets  (views/1000) x 0.1279        <- campaign rate, the figure
Rates per 1,000 views: clipper $0.50, owner $0.3198   <- clip stamp, the rate
```

**A figure sitting beside a rate that did not produce it, differing by 2.5x. That is precisely the confusion
BL-744 was built to eliminate, reintroduced on the only clips this feature can touch.**

**Current exposure is ZERO, and I am saying so rather than overstating the find.** Measured today:

```
eligible PENDING   22   would hit the eager branch:  0   (the branch requires status APPROVED)
eligible APPROVED  81   would hit the eager branch:  0   (none has views >= campaign minViews)
```

Every APPROVED eligible clip is below its campaign's minimum view threshold, which is **why** it has zero
earnings. **The mismatch fires the moment one of those 81 crosses `minViews` after an override and before
its next tick writes the agency row.** That window is one tick, up to an hour, and it recurs for every
override applied to an APPROVED clip.

**What must be added:** either the spec extends `:1724` to prefer the clip's owner stamp over the campaign
rate, which is a one-line display change and is correct independently of this feature, or the override is
restricted to PENDING clips only, where the branch cannot fire at all.

---

# PART 5 — WHAT BL-752 DID NOT ASK

| # | Omission | Severity | Status in BL-752 |
|---|---|---|---|
| 1 | **Survives reassignment** | **HIGH** | **Absent.** PART 3.3. |
| 2 | **Admin row rate versus figure** | **HIGH** | **Absent.** PART 4.3. |
| 3 | Rejection then re-approval | MEDIUM | **Absent.** Eligibility covers PENDING and APPROVED but says nothing about a clip overridden while PENDING, then REJECTED, then re-approved. `review/route.ts:473` resolves from the stamps, so the override would most likely survive, **but I did not verify whether the review path re-stamps on approval** and the spec should prove it either way. |
| 4 | Removing or changing an override | LOW | **Partly covered.** Failure mode 7 allows reversal by writing `prev` back while still never-earned. It does not say whether a second override may be applied on top of the first, which matters because `r` would then be re-derived from already-scaled stamps and the 0.0005 perturbation compounds (PART 2). |
| 5 | Clipper visibility and notification | LOW | **Covered well.** Notify on a raise, not on a decrease, and deliberately not reusing `email.ts:820`, which is a campaign-edit promise. Sound, and consistent with BL-518 and BL-521. |
| 6 | Owner-economics leakage per BL-531 | NONE | **Verified and holds.** `ownerCpmAtSubmissionDecimal: true` appears in exactly **one** select repo-wide, inside `canSeeMoney` on a route that 403s clippers. `clips/mine`, `earnings` and `payouts` select **0**. Attack failed. |

---

# PART 6 — THE VERDICT

**NOT safe to build exactly as written.** The core design is sound and survived every attack I made on its
arithmetic, its guard interaction, its spend accounting and its leakage posture. **Two gaps must be closed
first, and both are cases of a previous round's fix being undone by this one.**

## Ranked gaps and required spec additions

| # | Gap | Severity | Required addition |
|---|---|---|---|
| **1** | **BL-736 reassignment silently erases an override.** Overlapping populations (22 PENDING eligible), all of reassignment's assertions still pass, and `cpmOverriddenAt` is spec'd only for `cpm-restamp.ts`. | **HIGH** | Extend the guard to `reassign-campaign/route.ts:347`. Refuse a clip with a non-null `cpmOverriddenAt`, or re-derive against the destination `s` and disclose it. |
| **2** | **The admin row would show an owner figure the displayed rate did not produce**, because rule 2 forces the `:1724` campaign-rate branch. Zero exposure today; fires when an APPROVED eligible clip crosses `minViews`. | **HIGH** | Prefer `clip.ownerCpmAtSubmissionDecimal` over `clip.campaign.ownerCpm` at `admin/clips/page.tsx:1724`, or restrict the override to PENDING clips. |
| 3 | **Rule 5's OR clause** silently converts a live-following clip into a frozen one. | MEDIUM | Drop the OR clause, or disclose the conversion in the confirmation. |
| 4 | **Rejection then re-approval** is unaddressed. | MEDIUM | Prove whether `review/route.ts` re-stamps on approval; add a test either way. |
| 5 | **Counts are wrong in the spec**: 103 eligible and 27 refused, not 123 and 49. Eleven call sites, not nine. | LOW | Correct the figures before they reach a UI. |
| 6 | **The margin claim is about the wrong quantity.** The worst eligible clip already consumes 0.004 of the 0.01 ratio budget, so the true worst case is about 2.2x, not 100x. | LOW | Restate the margin honestly and add the measured 0.004 to the harness as a starting offset. |
| 7 | **Repeated overrides compound** the 0.0005 perturbation; roughly 12 successive applications would breach the tolerance. | LOW | Either derive `r` from `s` rather than the current stamps when `cpmOverriddenAt` is already set, or cap re-application. |

## What I tried that did NOT break it, so the owner can judge the attack

* Recomputed the full ratio arithmetic on BL-743's live non-round pair, a non-dividing target, the $0.005 boundary and the owner's 50/50 case. **All pass; BL-752's table is correct.**
* Hunted for an eligible clip already near the guard tolerance, which would tip into ambiguity on scaling. **Zero found; worst gap 0.004 of 0.01.**
* Tested zero owner CPM, zero clipper CPM, extreme values, ghost-fee campaigns and hand-set pre-calculator campaigns. **All refused correctly or strictly safer.**
* Looked for cumulative drift across many clips that would be BL-539's shape returning. **None; there is no accumulator, each clip scales from its own stamps.**
* Tried to make BL-642's two spend filters disagree. **They cannot; the asymmetry is about rows, not rates.**
* Tried to break no-overpayment and no-over-budget. **Both preserved by the L1 lock.**
* Checked all eleven call sites individually for a spread that would reach the dead override branch. **None; every one is a 3-key literal.**
* Checked every clipper-facing route for owner-stamp leakage. **One select repo-wide, inside `canSeeMoney`.**

**The design is good. The spec is not finished.** Close gaps 1 and 2 and it is safe to build.

---

# WHAT COULD NOT BE VERIFIED

* **Whether `review/route.ts` re-stamps on approval**, which decides gap 4. I read its `resolveClipCpms` call at `:473` and it resolves from the stamps, but I did not trace whether an earlier line in the approval path writes the stamps afresh. **The spec must prove this; I am not asserting it either way.**
* **The 13 `ownerCpm` matches in `api/campaigns/route.ts`.** They are the campaign field, not the clip stamp, and are pre-existing BL-531 territory. I did not audit whether all 13 are behind an owner gate, and this feature does not change them.
* **Behaviour under genuine concurrency.** The race analysis in PART 3 is read from the lock semantics and the assertion lists, not from an executed concurrent test. Proving it would need a harness that runs the tick and the override against the same clip simultaneously, which the spec should include.
* **Whether the owner intends a decrease to be permitted at all.** BL-752 correctly leaves this as a policy question. I have no basis to overrule it and did not try.
