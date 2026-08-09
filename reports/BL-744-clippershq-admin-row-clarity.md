# BL-744 — the admin clip row now says what its numbers are, so a correct row stops reading as a bug

**2026-08-09 · Base:** `main @ b5bd0651` · **Branch:** `checkpoint/BL-744` `a60d2f75` · **Tags:** `pre-BL-744` = `b5bd0651`, `post-BL-744` = `a60d2f75`
**DISPLAY ONLY. No stored value, no calculation, no earnings, no accrual, no rate and no campaign field changed. No clip status or earnings changed. No payout touched. No schema change and no `prisma migrate`.**

---

## WHY THIS ROUND EXISTS

BL-743 spent an entire audit round proving a campaign reassignment had worked perfectly. **The owner and I
both read the row as a bug before anyone checked.** That is the expensive failure direction: a correct money
system produced a false bug report, and the cost was a full round.

The row showed `CLIPPER $0.24` and `OWNER $0.15`, identically styled, one line under a campaign named
`Zhus Meme (0.20 CPM)`, with no total and neither rate anywhere on screen. The `0.20` in that name is the
**clipper** rate. The campaign carries a **separate $0.1279 owner rate**. $0.39 was always correct.

**The fix is grammar, not more data.**

---

# PART 0 — WHAT EACH DISPLAYED NUMBER ACTUALLY IS

## 0.1 Every figure traced to its formula

| Figure on the row | Value | Produced by | file:line |
|---|---|---|---|
| Clipper amount | `clip.earnings` | `(views / 1000) * cpm`, where `cpm` resolves the clip's STAMP first | `earnings-calc.ts:176`, resolution order `:374-384` |
| Owner amount, normal path | `clip.agencyEarning.amount`, a stored row | written server side at approval | read at `admin/clips/page.tsx:1675` |
| Owner amount, eager fallback | recomputed in the page | `Math.round((viewsForCalc / 1000) * ownerCpm * 100) / 100` using the campaign's LIVE rate | `admin/clips/page.tsx:1693` |
| Rate in the campaign label | **not a computed field at all** | a human typed substring of `Campaign.name` | rendered `admin/clips/page.tsx:1550` |
| Owner rate | **displayed nowhere** | `campaign.ownerCpm`, read only to multiply by | selected `api/clips/route.ts:429`, read `page.tsx:1672` |
| Clipper rate | **displayed nowhere, and not even in the payload** | `clipperCpm` was not selected | `api/clips/route.ts:427` |

**Which rate does the campaign label show? The CLIPPER rate only, and by accident rather than by design.**
It is free text. Nothing derives it, nothing keeps it in sync, and nothing says whose rate it is.

**Is the owner rate displayed anywhere today? No.** The reader was shown two dollar figures and neither of
the two rates that produced them.

## 0.2 Confirmed independently on the real clip

Live, `db_now = 2026-08-09 12:12:45.616178+00`, for `cmsktak4y00qf0pl402jdt3t3`:

```
campaign label   Zhus Meme (0.20 CPM)        pricingModel   CPM_SPLIT
campaign clipperCpm   0.2      cpmInstagramClipper   0.2000
campaign ownerCpm     0.1279   cpmInstagramOwner     0.1279
```

**Both values confirmed: the label's 0.20 is `clipperCpm`, and a separate `ownerCpm` of 0.1279 exists and
was invisible.** At BL-743's 1,203 views that is $0.24 and $0.15, total $0.39, a combined 0.3279 per 1,000.

**Honest note on drift:** the clip has kept earning since BL-743. It now reads **1,867 views, clipper $0.38,
owner $0.24, total $0.62**, on the same rates. The worked example below uses BL-743's figures because that
is the row the brief asks to see; the live figures have moved and the structure is identical.

---

# PART 1 — THE FIX

## 1.1 The insight: the two branches are mathematically opposite and were worded identically

That block has two branches. **A marketplace clip's three figures PARTITION one gross** (60/30/10). **A
CPM_SPLIT clip's two figures are ADDITIVE**, produced by two independent rates. They were given the same
labels, the same weight, the same 10px uppercase muted treatment and the same flex row, which is the
standard idiom for slices of one pot. **One visual treatment was carrying two opposite arithmetics.**

So the primary fix is not a total. It is **two grammars**.

## 1.2 The exact labels shipped, quoted

**CPM_SPLIT, the additive branch:**

```
Clipper gets $0.24    Owner gets $0.15    Campaign pays = $0.39
Rates per 1,000 views: clipper $0.20, owner $0.1279
```

**Marketplace, the partition branch:**

```
Clipper share $0.60   Poster share $0.30   Owner share $0.10   Total paid = $1.00
```

Quoted verbatim: **`Clipper gets`**, **`Owner gets`**, **`Campaign pays`**, **`Clipper share`**,
**`Poster share`**, **`Owner share`**, **`Total paid`**, and
**`Rates per 1,000 views: clipper $0.20, owner $0.1279`**.

Plus two sr-only sentences, which are the first child of each total cell so the relationship arrives before
the number: **`Clipper and owner amounts added together.`** and
**`Clipper, poster and owner shares all come out of this.`**

**`gets` versus `share`. `Campaign pays` versus `Total paid`.** A reader who learns the two verbs tells the
branches apart without reading a sentence, at zero extra lines.

## 1.3 No figure sits beside a rate that did not produce it, and that is structural

This was the brief's hard rule and the trap that caused BL-743. **It is satisfied by construction, not by
care: the rates shown are the CLIP'S OWN STAMPS**, `cpmAtSubmissionDecimal` and
`ownerCpmAtSubmissionDecimal`. Those are exactly what `earnings-calc` resolves first
(`schema.prisma:982-989`, resolution order `earnings-calc.ts:374-384`), so the rate displayed **is** the
rate that produced the dollars beside it. A live campaign rate would only match by luck, and stops matching
the moment the campaign is edited.

## 1.4 Justification against the frontend-design skill

The skill's anchors govern a visual direction for a new surface. **This round adds no new surface, no new
component and no new palette**, so no anchor applies and picking one would mean redesigning a working admin
page. What does apply is **§2, "Content is not design"**: every string on screen must name real information,
and what is forbidden is content pretending to be something it is not.

**That is precisely the defect.** `CLIPPER` names a party, not a relationship, so the reader supplied the
relationship from the layout and the layout said "partition". `Clipper gets` names real information.
`Campaign pays` names real information. The rate line names the two real rates. **Nothing added here is
filler, themed copy or decoration**, and the density rule was respected: on desktop the money block is still
a **single 19px line**, because the total and the rate ride in the existing `flex-wrap` container rather
than adding a block.

## 1.5 I overruled the accessibility lead on one item, and solved its objections rather than dismissing them

The lead reviewed before any UI was written and returned **NO GO on the rate line**, with three verified
blockers. The brief requires the rate behind each figure, so I solved all three:

| Blocker | Resolution |
|---|---|
| **B1** `clipperCpm` is not in the payload, and adding campaign rates touches a money select | Added the **clip's own two stamps** instead, at `api/clips/route.ts:459-460`, inside the existing `if (canSeeMoney)` block, and redacted on the same reviewer branch as `ownerCpm` at `:598-600`. Narrower than campaign rates and it reuses the file's own pattern. |
| **B2** `formatCurrency` is 2dp, so `formatCurrency(0.1279)` returns **`"$0.13"`**, and a reader multiplying 0.13 by the views gets a figure that disagrees with the total, **manufacturing a new false alarm** | Rates never touch that formatter. A dedicated 4dp formatter trims trailing zeros but never below two: `$0.20`, `$0.1279`, `$0.50`, `$0.125`. Asserted in the harness, including an explicit assertion that 0.1279 never renders as `$0.13`. |
| **B3** a live campaign rate need not be the rate that produced the dollars | Solved by the stamp choice in PART 1.3. |

**Every other recommendation was adopted in full**, and several were better than my plan:

* **`Campaign pays`, not `Budget pays`.** "Budget" is overloaded here (cap, era, hard-lock, auto-pause, versioning) and costs a half-second parse as something about the remaining pool.
* **The total is gated on `typeof v === "number"` and ALWAYS rendered**, never on `v > 0`. The `v > 0` shape would suppress the total on exactly the rows where a genuine zero owner share is most worth confirming, and a vanishing cell varies row height down a long list.
* **The relationship is sr-only text, never `+` and `=` as the carrier**, since both are punctuation and suppressed at default verbosity. The visible `=` is `aria-hidden`.
* **`whitespace-nowrap` plus a literal `{" "}` replaces `inline-flex items-baseline gap-1` on all five cells.** The lead corrected BL-743's diagnosis here: the cell is a flex container, which blockifies **its children**, splitting each label and value into two unlinked screen reader stops. The proof is 70 lines up in the same row, where `page.tsx:1628` uses a plain `<span>` and announces `"1,203 views"` as one utterance.
* **No `<dl>`.** It would add "list with 4 items" and "out of list" to every row on a fifty-clip page and creates no name relationship between `dt` and `dd` anyway.
* **Sentence case in the DOM**, with the existing `uppercase` class doing the visual work, because `text-transform` does not reach the accessibility tree and literal all-caps invites initialism spelling.
* **The em dash is now `aria-hidden` plus sr-only `no amount yet`.** Deliberately neutral wording, not "not yet calculated", because the predicate is still `v > 0` so a genuine $0.00 renders that same dash and the stronger wording would be false.

---

# PART 2 — EVERY OTHER SURFACE WITH THE SAME TRAP

Audited every file that renders a CPM alongside money.

| Surface | file:line | Verdict | Action |
|---|---|---|---|
| Admin clips row | `admin/clips/page.tsx:1719-1732` | **THE trap** | **FIXED**, PART 1 |
| Admin submit clip | `admin/submit-clip/page.tsx:342`, `:426` | **SAME TRAP.** Labelled **"Campaign CPM"** while reading `clipperCpm` (`:112`), sitting directly beside **Budget** | **FIXED** to `Clipper CPM` |
| Admin submit clip, custom rate | `admin/submit-clip/page.tsx:355` | Ambiguous. "Custom CPM (max $X)" where the cap is the clipper rate | **FIXED** to `Custom clipper CPM` |
| Reassignment dialog, BL-736 | `reassign-campaign-dialog.tsx:277` | Bare **"Current rate"** | **FIXED** to `Current clipper rate` |
| Reassignment dialog, live region | `reassign-campaign-dialog.tsx:234` | Bare **"New rate"** | **FIXED** to `New clipper rate` |
| Reassignment dialog, confirm step | `reassign-campaign-dialog.tsx:368` | "The rate changes from X to Y" | **FIXED** to `The clipper rate changes from` |
| Campaign archive detail | `admin/archive/[campaignId]/page.tsx:167`, `:173`, badge `:156-158` | **Already correct.** Separate `Clipper CPM` and `Owner CPM` plus a `CPM Split` badge | **LEFT.** This is the model the others now follow |
| Agency earnings | `admin/agency-earnings/page.tsx:112`, `:268` | Already correct, owner scoped, says `Owner CPM` | **LEFT** |
| Past campaigns | `admin/past-campaigns/page.tsx:147`, `:352` | Already correct, says `Clipper CPM` | **LEFT** |
| Clipper facing (campaigns, favorites, marketplace, preview, help) | various | **No trap.** They show a clipper rate beside CLIPPER money only. No owner figure exists on them | **LEFT, deliberately.** PART 3 |

## 2.1 The reassignment dialog, specifically

**It was partly clear and is now unambiguous.** Its prose already said *"This pays the clipper less, and
they will be told"* (`:239`) and *"This pays the clipper less than the campaign they submitted to"*
(`:375`), so the context was clipper scoped. **But every label was bare.** The state it renders is literally
`newClipperCpm`, and the campaign also carries an owner rate, so a bare "rate" invited the same misreading
in the one dialog where an owner acts on the number. All three now name the clipper explicitly.

## 2.2 Why this matters more than it looks

**4 of the 33 campaigns embed a rate in their name, and all 4 are ACTIVE:** `Zhus Edit (0.50 CPM)`,
`Zhus Meme (0.20 CPM)`, `BAD BITCH ANTHEM (0.50 CPM)`, `BAD BITCH ANTHEM (2.50 CPM)`. The trap is live on
the campaigns being worked on right now.

---

# PART 3 — NO CLIPPER EXPOSURE

**The two stamps are selected in exactly ONE place in the entire repository.** `grep -rn` over
`src/app/api/`, count **1**:

```
src/app/api/clips/route.ts:459:      clipSelect.cpmAtSubmissionDecimal = true;
src/app/api/clips/route.ts:460:      clipSelect.ownerCpmAtSubmissionDecimal = true;
```

**Both sit inside `if (canSeeMoney) {`**, which opens at `:448` and closes at `:464`, verified by reading
the block.

**That route is not clipper facing.** `api/clips/route.ts:65` gates on
`if (role !== "ADMIN" && role !== "OWNER")`, and every role other than a REVIEWER falls to
`return NextResponse.json({ error: "Forbidden" }, { status: 403 })` at **`:92`**. A CLIPPER cannot reach the
endpoint at all.

**A reviewer without `EARNINGS_VIEW` is redacted on the same branch as `ownerCpm`**, at `:598-600`, using
the pattern the file already established.

**No clipper facing route selects the stamps or the owner rate**, by `grep -c`:

```
api/earnings/route.ts          stamps=0   ownerCpm=0
api/campaigns/route.ts         stamps=0   ownerCpm=0
api/payouts/route.ts           stamps=0   ownerCpm=0
api/campaigns/past/route.ts    stamps=0   ownerCpm=0
```

**And the owner RATE is gated more tightly than the owner AMOUNT.** The amount already renders for
`isAdminOrOwner`. The new rate line renders only when **`isOwner`** is true. CLAUDE.md puts agency and owner
data out of an ADMIN's reach, and this round does not widen that.

**None of the four files I changed is clipper facing.**

---

# PART 4 — THE EVIDENCE

## 4.1 The row, before and after, for BL-743's real clip

**BEFORE**, exactly what cost a round:

```
someclipper · Zhus Meme (0.20 CPM) · 2h ago
CLIPPER  $0.24        OWNER  $0.15
```

**AFTER**, rendered in Chromium and read back out of the DOM:

```
Clipper gets $0.24  Owner gets $0.15  Campaign pays = $0.39
Rates per 1,000 views: clipper $0.20, owner $0.1279
```

Both figures, the total they sum to, and the rate behind each. The marketplace branch, same run:

```
Clipper share $0.60  Poster share $0.30  Owner share $0.10  Total paid = $1.00
```

## 4.2 Legibility at all five widths, measured

`scripts/test-bl-744-row-clarity.mjs`. **It does not retype the labels or the rate formatter: it extracts
both from the shipped source** and renders against the app's own compiled Tailwind (236,478 bytes from
`.next/static/chunks`), so it cannot drift. **46 passed, 0 failed, exit 0.**

| width | horizontal scroll | any cell clipped | cells | min font | row height | money block |
|---|---|---|---|---|---|---|
| 320px | none (320 vs 320) | no | 4 | 10px | 143px | 83px |
| 375px | none | no | 4 | 10px | 143px | 83px |
| 414px | none | no | 4 | 10px | 143px | 83px |
| 1280px | none | no | 4 | 10px | 79px | **19px, one line** |
| 1440px | none | no | 4 | 10px | 79px | **19px, one line** |

**Zero new lines on desktop.** On mobile the container was already `flex-col`, so the cells stack as they
always did and the block is 83px.

The harness also asserts the grammars cannot be confused: **`the two branches do NOT share grammar`** passes,
checking that the marketplace text contains no "gets" and the CPM_SPLIT text contains no "share".

## 4.3 The rate formatter, asserted

```
fmtRate(0.2)    -> $0.20      fmtRate(0.1279) -> $0.1279
fmtRate(0.5)    -> $0.50      fmtRate(0.125)  -> $0.125
fmtRate(0.1279) NEVER returns $0.13     (the B2 blocker, asserted explicitly)
```

## 4.4 Nothing stored or calculated changed

The four changed files are two admin pages, one admin component and one **`select`** addition. **No
arithmetic was altered**: the owner fallback at `page.tsx:1693` and the clipper figure are byte identical,
and the only new computation is `sum2`, which adds two numbers already on screen and is never persisted.
**The dash predicate `v > 0` is unchanged**, so which figures appear is exactly as before.

Money files, working tree `git hash-object` against the `origin/main` blob OID, all **IDENTICAL**:

```
ac5be7de clip-earnings-writer   797e2098 earnings-calc   e887f80a balance   83ce4bab tracking
61cef393 clip-earnings-invariant-middleware   ef5cdae7 money-decimal   106e16ad campaign-era
```

`tracking.ts` is not in the diff. No payout row, clip status or earning was written this round.

## 4.5 Gates, stated honestly

* `npm ci` **exit 0**, `npx prisma generate` **exit 0**, run after it because `npm ci` wipes the client. Clean worktree at `C:/b744`, a short path, `.env` and `.env.local` copied, **no `node_modules` junction**.
* `tsc --noEmit` **exit 0, 0 errors** (log 0 lines).
* `npm run build` **exit 0 pre-commit and exit 0 post-commit**, `✓ Compiled successfully`, read from a log with the exit code **echoed, never piped through `tail`**.
* Hooks gate **11 problems, 0 errors, 11 warnings, at the limit of 11**, with **eslint v9.39.4 confirmed present** so the gate is not a silent no-op. `check:prisma-bypass` and `check:removed-fields` both ran in `prebuild`.
* Harness **46/0, exit 0**.
* Push **verified**: `safe-push.mjs` reported `VERIFIED PUSHED`, and `git ls-remote` agrees. `pre-BL-744` points at the true base `b5bd0651`, confirmed equal to `HEAD~1`.
* **`C:/b575` left exactly as found**: `91b84410`, 77 dirty paths, re-checked after the push. It was stale and dirty, so this round used a separate clean worktree, as the brief required.

## 4.6 Accessibility

Reviewed by the accessibility lead with the cognitive accessibility and data table specialists **before any
UI was written**. One item overruled with its blockers solved (PART 1.5); every other recommendation
adopted.

**Reported, not fixed, all pre-existing and none introduced here:** `globals.css:43-45` sets
`--text-primary`, `--text-secondary` and `--text-muted` **all to `#ffffff`**, so the dark theme has no muted
ramp at all and secondary emphasis is only expressible through size and weight; `text-accent` measures
**3.40:1** and `text-emerald-400` **1.92:1** in the LIGHT theme, both AA failures, though light mode is
effectively unreachable since `toggleTheme` is never called; `layout.tsx:130` ships
`maximum-scale=1, user-scalable=no`, a **1.4.4** failure that removes the usual defence for 10px text;
`PlatformIcon.tsx:51-55` puts `aria-label` on a bare lucide `<svg>` with no `role="img"`, so every row opens
with an announced `"graphic TikTok"` stop; and BL-743's zero-versus-null dash merge at `page.tsx:1666`,
left deliberately because changing that predicate changes **which figures appear**, which a legibility round
must not do.

---

# WHAT SHIPPED

`admin/clips/page.tsx`, `admin/submit-clip/page.tsx`, `api/clips/route.ts`,
`admin/reassign-campaign-dialog.tsx`, plus `scripts/test-bl-744-row-clarity.mjs` and the `BACKLOG.md` entry.
**6 files, 400 insertions, 27 deletions.**

**Rollback:** `git revert -m 1 <merge>`, or `git reset --hard pre-BL-744`. **Nothing to undo in the
database.**

**Not merged to main.** This is a branch round; the merge is its own step.
