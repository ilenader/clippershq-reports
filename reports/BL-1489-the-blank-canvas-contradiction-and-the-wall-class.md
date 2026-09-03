# BL-1489 — the contradiction was a threshold, and he scored a login screen 10 out of 10

> **Reading this cold?** This project runs an automated funnel that finds social-media pages
> worth contacting. A vision model — the "judge" — looks at a screenshot of a page and decides
> whether the operator would want it. The judge is shown **worked examples**: eight real pages
> the operator graded himself, four he loved and four he hated. That set is the **exemplar pack**.
> There are four judges — Instagram and TikTok, each in "memes" and "edits" mode.
>
> Creator handles are redacted throughout. Paths are relative to the repository or use
> `%USERPROFILE%`. No port numbers appear.

---

## 1. Round ID, date, and what it was asked to do

**BL-1489, 2026-09-02/03.** Run alone. Cap $0.50. **Vendor spend: $0.00 by the round's own call
counter** — every instrument ran with the network poisoned before import, and no model was
called. The shared ledger moved during this round by $0.009167 in vision spend; that is another
round's work, and it is exactly why the ledger delta cannot attribute a round.

Two jobs, both of which had to be *proved*, not argued:

1. **Two rounds published opposite numbers about the same eight images.** Settle it by reading
   the pixels, and find out *why each instrument got what it got* — that reason being worth more
   than the answer.
2. **Kill the login-wall class.** A candidate the operator scored **10** was an Instagram login
   screen that passed every existing check.

**Campaigns fingerprint, both forms, verified at round start and again at publication:**
`8e02f8d6f6307ae8` (default serialisation) / `7a029ee5447cddd8` (compact), 5 campaigns —
unchanged, so every figure below describes the same configuration.

---

## 2. What actually shipped

| # | change | category | moves a verdict today? |
|---|---|---|---|
| 1 | An empty declared pack now **RAISES** instead of silently serving another platform's | **GENERAL** — safer default + required opt-in, driven off the declaration table | **No** |
| 2 | The one production call site names the fallback **above** the `except` | LOCAL — without it, #1 is a fix on a branch nothing takes | No |
| 3 | The grid-index fallback yields to the camera's own suppression | **GENERAL** — chokepoint, both sites | **Yes, and deliberately** |
| 4 | `_esc_json_for_script` rebuilt from `chr(92)` + a self-test that refuses a no-op | **GENERAL** — boundary assertion | No |
| 5 | Viewer: banner can go red again, both missing-picture paths announce, receipt is a live region | mixed | No |
| 6 | A corrected `emit` line that had been asserting something measurably false | LOCAL | No |

**Nothing was promoted. `APPROVED_IG_EXEMPLARS` is still `()`.** The funnel may propose; only he
may promote.

---

## 3. What was measured

### 3.1 The blank-canvas contradiction — SETTLED. Round A was right.

Both rounds measured **the same eight files**; that was checked at the byte level and the
"different pack / different files" hypotheses are **refuted**. The encoder is not the
explanation either: on the shipped contact-sheet path the emptiness survives encoding almost
unchanged (85.7% → 85.0%, 91.8% → 91.3%).

They disagreed because they measured **different quantities**, and one threshold is wrong by
eight grey levels.

| exemplar | label sent to the model | empty canvas | undrawn cells | Round B's number |
|---|---|---:|---:|---:|
| 01 | 10/10 **HE WANTS THIS** | **85.7%** | **10 of 12** | 5.5% |
| 02 | 10/10 he wants this | 4.1% | 0 of 12 | 16.0% |
| 03 | 10/10 **HE WANTS THIS** | **83.8%** | **10 of 12** | 1.8% |
| 04 | 10/10 **HE WANTS THIS** | **83.5%** | **10 of 12** | 11.7% |
| 05 | 1/10 not wanted | 1.0% | 0 of 12 | 3.1% |
| 06 | 1/10 not wanted | **91.8%** | **11 of 12** | **0.2%** |
| 07 | 1/10 not wanted | 2.3% | 0 of 12 | 6.3% |
| 08 | 1/10 not wanted | **75.2%** | **9 of 12** | 4.5% |

**Why Round A got its number.** It counted the sheet's own empty canvas — cells the builder
never drew a cover into. Correct, and confirmed a second way *without any hard-coded colour*: by
byte-comparing each grid against a sheet produced by calling the shipped builder with no covers.
That agrees with the undrawn-cell count to the pixel.

**Why Round B got its number.** Its detector counts a pixel as blank when greyscale `< 16`.
**The builder paints its canvas at `RGB(24,24,27)`, which converts to grey 24.** 24 is not less
than 16. Round B's detector is **structurally incapable of seeing this builder's empty canvas.**

Its "positive control" was an all-white image, which exercises the near-**white** branch — so it
validated a branch the real data never touches, and the near-**black** branch was never tested at
all. A control that checks what you suspect rather than the mechanism you depend on.

Two consequences, both measured:

- Round B's number is **negatively rank-correlated with actual emptiness** (Spearman ρ = −0.405,
  n=8). Its *lowest* reading, 0.2%, is on the **emptiest** file in the pack.
- Its "worst is 16%" headline is the **fullest** sheet in the pack. That 16% is genuine dark
  *content* — letterbox bars inside real covers — not canvas.

The decisive control is a picture: a synthetic sheet painted entirely in the builder's own canvas
colour. Round A's method reads it **100% empty, 12 of 12 undrawn**. Round B's reads **0.0000**.

> **Both rounds' numbers are simultaneously true of the same file. They were never measuring the
> same thing, and only one of them was measuring the thing that matters.**

### 3.2 The duplicate-cover claim — TRUE, and Round A undercounted

⚠️ **Two grids contain the same cover twice, not one.** Tile pixel buffers are byte-identical
(sha256 equal, mean absolute difference 0.000, perceptual difference 0.00). Both were opened and
visually confirmed as real content, not two black tiles. **Both carry the label "he scored this
10 of 10: HE WANTS THIS."**

Round B's "all 8 carry distinct hashes" is **true and irrelevant** — it hashed whole *files*
while the claim is about *cells within one file*. A grid containing the same cover twice is still
a unique file. The two claims were never in conflict; they were collapsed and refuted together.

**A finding neither round reported:** three of the five sparse grids have a **full 12-of-12 sheet
of the same handle sitting on disk** that the resolver does not pick, because it keeps the
*newest* file per handle. Two others are sparse in every copy — the capture only ever got that
many covers.

### 3.3 ⚠️ He scored a login screen 10 out of 10

Four platform-chrome screenshots reached his delivered sheets and carry his marks:

| what the picture actually shows | his score |
|---|---:|
| **an Instagram login screen** | **10** |
| an age gate (13+) | 10 |
| an age gate (18+) | 9 |
| an age gate (20+) | 5 |

These are pictures of Instagram's own furniture, not of the pages beneath them. One of the age
gates is byte-identical to another handle's picture, so it cannot be about that page at all.

**The Instagram scored denominator is 136, not 140** — that being *distinct Instagram pages
carrying a 1–10 score, resolved last-keystroke-wins, from delivered-sheet mark files only*. Two
sheets move: one from n=49 to 46, and one from n=17 to **16, mean 6.706 → 6.500, want-rate
76.47% → 75.00%**.

⚠️ **Which published figures used 140 was not audited** — only the corrected denominator was
computed. Any Instagram accuracy, want-rate or mean-score figure over that set is affected by
construction; naming them needs a pass this round did not run. **That is an open item, not a
finding.**

### 3.4 ⚠️ "16 walls" was wrong, and it was my own previous round's number

BL-1486 published "16 of 374 stored Instagram grids are walls". Reading the OCR text of each:

| what it actually is | n |
|---|---:|
| login screen | **1** |
| private profile | 4 |
| age gate | 4 |
| **ordinary public profile with zero posts — not a wall at all** | **7** |

The detector fires on "one strong phrase OR two weak chrome phrases", and its weak list is the
logged-out Instagram footer, which is present on **every** logged-out page. On that corpus its
output is identical to simply testing the image dimensions — 374 of 374 concordance. **The class
is real and the count was inflated; 7 of the 16 are healthy pages that merely have no posts.**

### 3.5 The wall suppression already shipped — and was being defeated

This is the finding that reaches the funnel. The camera **already** refuses to photograph a
login wall, a private page or a not-found page, leaving no file path behind. But the funnel then
read, at two sites:

```python
_pp = _gg.get("full_path") or _grids_on_disk.get(str(_h).lower())
```

and that index globs every PNG from every round ever run, keeping the newest per handle. **So the
page the camera had just positively identified and refused to photograph was handed the previous
round's photograph of the same wall.**

- 1,612 of 10,988 indexed handles currently resolve to a full-page (non-grid) shot.
- Seeded sample of 120, positive control fired: **806 [664, 948] of those 1,612 are login
  screens.**

That number counts handles whose *current index entry* is a login-screen picture — **reachable**
by the judge, not proven delivered to it. How many actually reached a judge call was not measured.

Fixed at both sites, **GENERAL**: the fallback now yields when the camera has recorded a
suppression, and is unchanged for every handle the camera did not touch this run. ⚠️ **This closes
the defeat; it does not clean the ~806 stale pictures.** That needs a separate sweep.

### 3.6 The state machine — and a fifth state nobody has

**A wall is UNJUDGED-AND-RETRYABLE. Confirmed.** The capture layer records it as recoverable, the
shot is suppressed, and if the paid grid also fails the funnel marks the page unjudged — which
makes it ineligible to count as decided, so it is re-walked next run.

**PRIVATE is a separate, permanent state. Confirmed.** Marked not-recoverable, and the paid
purchase is refused outright.

**Neither is ever written as "he would not want this page"** — a rejection requires both a verdict
and a judged-by field.

⚠️ **A FIFTH STATE IS MISSING AND NOTHING IN THE TREE HAS IT: THE AGE GATE.** It is not private
(the pattern misses it), not not-found, and not a login wall — the structural test needs a
password field and an age gate has only a button. It falls through to *unknown*, gets
photographed, and gets judged. **Whether a paid grid even recovers an age-gated page is
unmeasured**, and must be before any handling ships. Three of the four pictures he mis-scored are
age gates.

### 3.7 The spend effect — measured, and it is neutral

⚠️ **A wall verdict decides whether a paid grid is bought, so this had to be measured before
anything shipped.**

- Price on record: **$0.00069064 per billed call**, 1.471 calls per page = **$0.001016 per bought
  grid**. The governing limit is unset — no cap. Typical run: 750 pages.
- **Extra purchases: zero.** Walls *already* trigger a purchase. The only class still
  photographed-and-judged is 144 *unknown* records, and OCR of all 144 finds **0 login walls**
  (110 no-wall-text, 22 age gates, 12 not-found).
- Adding age gates later would cost **$0.0051 per run**.
- Judge saving is **clock, not cash**: the rejecting model bills ~$0.00024 a call, so 144 calls
  is $0.035 across the entire corpus. The saving is **8.0 minutes** of run time.

> **Net: spend-neutral to within half a cent per run. This is an accuracy and clock change, not a
> spend change.** The one real bill would be a one-off: invalidating all 1,612 stale pictures
> forces re-capture — free unless the camera is walled, in which case **$1.638**, or 8.2% of the
> Instagram budget.

### 3.8 TikTok — clean, and structurally so

**0 walled of 220 scanned**, sampled from 2,883 unique images (Wilson 95% [0%, 1.72%]).
Positive control fired on the same code path; negative control correctly did not.

Stronger than the sample: **2,883 of 2,883 are exactly the builder's own grid dimensions.** The
TikTok path pastes downloaded cover bytes onto a blank canvas — there is no browser and no page
screenshot — so **a wall cannot structurally become a TikTok grid.** The TikTok exemplar pack: 0
of 8, all full 12-tile grids.

### 3.9 The guard, driven on the production path

Intercepted at the last statement before the HTTP send, with the network poisoned before import
and a `BaseException` raised so no fallback model could swallow the spy.

| brain | exemplars in payload | whose directories | rubric hash | expected | |
|---|---:|---|---|---|---|
| tiktok / memes | 8 | TikTok | `28c05f855e13` | `28c05f855e13` | **MATCH** |
| tiktok / edits | 8 | TikTok | `258d5590748b` | `258d5590748b` | **MATCH** |
| instagram / memes | 8 | **TikTok, 8 of 8** | `46a1a4d89cbc` | `46a1a4d89cbc` | **MATCH** |
| instagram / edits | 8 | **TikTok, 8 of 8** | `eb5bcc28a170` | `eb5bcc28a170` | **MATCH** |

**Negative control fired twice** — one byte flipped in the captured buffer, and separately one
character appended to the real addendum and re-driven end to end. The instrument sees one byte.

**The two Instagram brains receive byte-identical exemplar payloads** (0 differences across all
8), with a positive control: planting one different exemplar made the spy report exactly 1
difference.

**The defect.** The guard read `if want == "instagram" and APPROVED_IG_EXEMPLARS:` — and that
tuple is **empty**. The condition was always False, so both Instagram brains fell through to the
eight TikTok pages, and **passing the platform changed nothing**. It also named one platform by
hand, so the next empty pack would fall through identically.

**The fix, GENERAL.** The lookup is inverted off the declaration table: any platform that
*declares* a pack and has none now **raises**, whoever asks. A test drives a platform the code has
never seen, declared at runtime, to prove the refusal is table-driven rather than name-driven —
with a negative control on the same fixture showing a non-empty declared pack is still served.

**Why not simply return an empty pack.** Measured: 0 exemplars scored **53.0%** against a
**65.0%** constant-answer baseline, while 8 scored 66.7%. ⚠️ **Quote that with its caveats:
n=100, unpaired, no p-value anywhere in the repo, measured on an older rubric and a model that
404s today.** It is enough to refuse an empty pack by default; it is **not** enough to call the
current pack good — the winning arm beats "reject everything" by 1.0 point.

**And the refusal had to move up a layer.** Placed inside the loader alone, the call site's own
`except Exception` caught the raise and set the pack to `[]` — continuing into the exact condition
the raise exists to prevent. **A refusal must sit where the untrusted value enters, not one layer
below the code that has already swallowed it.**

**Verdict neutrality, checked as full tuples, not lengths:** with the approved list empty, every
brain receives the identical eight files, in the identical order, as before. **No verdict moved.**

### 3.10 Mode — deliberately not shipped, and the honest reason

`_exemplar_pack` takes no mode, which is why the two Instagram brains get the same pack. The
plumbing is free — the run mode is already bound 571 lines above the call site and already passed
to both judge entry points.

**The supply is not free.** Instagram-edits has **21 marked pages and only 2 at ≥9** against a
rule needing 4. A mode-aware pack for that brain would be **empty** — which is precisely the
condition the new refusal exists to reject. Shipping mode today would ship a guaranteed refusal.

⚠️ **And the reason that cell is empty is weaker than I previously published.** The exclusion is a
**file-granularity blanket**: the mark reader matches on the directory name, so all 21 pages are
excluded for the sitting they belong to, not for their subjects. The 21 handles do **not** read as
car/gym/motivation at all — they are anime, movie-VFX and quotes pages. **Nobody has checked them
page by page**, and doing so might recover the cell.

### 3.11 The viewer — ⚠️ the browser test was NOT performed this round

**This is the one deliverable that was not met, and it is stated rather than dressed up.** No
Chrome instance with the extension was connected at any point during this round; a broadcast
Connect request found no browsers at all. **The page was therefore not opened in a real browser,
no screenshot was taken, the console was not read, and the double-click round trip was not
re-proved.** A previous round did perform that test on this same viewer; this round did not, and
that earlier result is not evidence about the code as it stands now.

What *was* proved, and what it does and does not cover:

- **`node --check` passes on the shipped script.** That is syntax, not execution.
- **The specific mechanism that hid last time was tested directly, with a negative control.**
  The original bug was a single-threaded server that served a simple fetcher perfectly and
  rendered the browser's error page, because a browser *preconnects* — opening sockets it has not
  yet spoken on — and then requests ~32 images in parallel, while a serial accept loop sits behind
  the idle socket. Holding one idle socket open and firing 12 parallel requests:

  | server | result |
  |---|---|
  | threaded (what ships now) | **12 of 12 succeeded, 0.52s** |
  | serial (the shape that shipped originally) | **0 of 12 succeeded, timed out at 4.02s** |

  The control pair fires: the fix is the difference, and a sequential fetcher cannot see it.

That is a proof about the *server*. It is **not** a proof that the page renders, that the
JavaScript executes, or that a click reaches disk. Those need a browser and did not happen.

A dozen accessibility defects were fixed in the same file and are likewise **unverified in a
browser** this round — among them: the connection banner could never return to red once the
server died mid-session (the check ran exactly once), the second of two missing-picture paths
announced nothing at all, and two independent facts wrote the same description attribute so
"not connected" was always overwritten. Each is a code change with a stated mechanism; none has
been watched working.

---

## 4. What was refused, and why — and the price

**Nothing was promoted.** The approved list is committed empty.

**The backspace hole was NAMED, not fixed.** Four literal backspace bytes sit where a regex word
boundary was meant, in one of four wall-detection arms — caused by a non-raw Python string eating
the escape. It is the **phrasal** arm; the **structural** arm (a password field) is intact, and
detection fires on **696 of 3,262** records through the other three. **0 pages are provably lost —
but that is a no-evidence zero, not a measured one**, because no store keeps the raw page text to
replay the intended pattern against. The instruction was to fix it only on a proven spend effect;
there is none, so it is named. ⚠️ *The 3,292 denominator quoted to me is not reproducible from any
file in the tree; the reproducible figure is 3,262.*

**No age-gate handling shipped.** The fifth state is named and quantified; whether a paid grid
recovers an age-gated page is unmeasured, and shipping a handler on an unmeasured recovery would
be the same mistake in a new place.

**The stale-picture sweep was not run.** ~806 handles still index to a login-screen photograph.
Closing the defeat stops it growing; cleaning it is a bigger, riskier change.

**The full test suite was not run** — a suite here asserts on a shared filename prefix and cannot
run concurrently, and two other rounds were live. The targeted runs are reported instead: 26
tests across the three exemplar files, and **10 of 10 suites / 120 checks green** through the
project's own runner across the neighbouring rounds' suites.

**The browser test was not performed** (§3.11). No Chrome with the extension was connected; a
broadcast found none. Reported as not done rather than inferred from an HTTP fetch — which is
precisely the substitution that let the last defect through.

### The iteration sequence, as asked

| # | tried | returned | changed | returned next |
|---|---|---|---|---|
| 1 | Applied the `</script` escape as a string literal | built clean, `node --check` OK | — | looked correct |
| 2 | Ran a **positive control** with a planted `</script` | **escape did nothing** — one backslash read as the character `<` | rebuilt the escape from `chr(92)`, added a self-test | control passes, and a mutation control proves the self-test refuses a no-op |
| 3 | Put the empty-pack refusal inside the loader only | the call site's own `except` caught it and set the pack to `[]` | moved the opt-in **above** the `except` | the refusal is reachable; 26 tests green |
| 4 | Fetched the review page with `urllib` | 200, correct bytes | — | proves nothing about a browser |
| 5 | Held an idle socket and fired 12 parallel requests | threaded 12/12; **serial 0/12** | — | the mechanism is proved; the browser test still is not |

**Price of the refusals:** the funnel keeps ~806 stale wall pictures until a sweep runs, and the
edits brains stay unfillable. Both are stated rather than papered over.

---

## 5. What I got wrong

**I shipped a no-op wearing a fix's name, in this very round.** The new JSON escape read
`.replace("<", "<")` with **one** backslash — which Python reads as the character `<`
itself, making the call `.replace("<", "<")`. It did nothing. Nothing about it looked wrong, it
passed `node --check`, and the page built cleanly. **It was caught only because I ran a positive
control against it** — and it is the *identical* failure this round found in the capture path,
where a non-raw string ate a regex escape into four backspace bytes. A backslash in a Python
string literal is not evidence of a backslash in the string. The escape is now built from
`chr(92)` and the builder runs a self-test that refuses to ship a no-op; the mutation control
fires.

**I published "16 of 374 are walls" last round.** Seven of those sixteen are ordinary public
profiles with no posts. The detector's weak-phrase arm matches the logged-out footer, which every
logged-out page has. The class is real; my count was inflated by 44%.

**I attributed a statistic to the wrong file, and it is worse than a wrong platform.** My last
report cited a 63.3%-versus-94.1% agreement swing against the Instagram edits mark file. That pair
comes from a **TikTok** scoring run — the source report identifies its own platform by the rubric
hash in its payload, and that hash is the tiktok/edits one, which this round's boundary spy
independently reproduced. Worse, the figure is **undefined** on the file I named: every one of its
45 rows carries the literal verdict `UNJUDGED`, by design, per the sheet's own metadata. There is
no pipeline answer to agree or disagree with. The *conclusion* survives; the supporting statistic
was borrowed from the wrong platform and could not have been computed where I put it.

**My previous round's per-brain claim was too strong.** I wrote that Instagram-edits is empty
because its pages come from the reversed-subject sitting. The exclusion is real but is a blanket
on the *file*, not a judgement on the *pages*, and the pages are not on the reversed subjects.

---

## 6. Money and safety

**Vendor spend: $0.00** by the round's own counter. No model call was made.

**Backups before any write**, timestamped, each verified by comparing sha256 against its source:
`config.json` and all five seen stores, **6 of 6 byte-identical**. There is no external backup on
this machine.

**No seen-store row was read, written, moved or deleted.** A recent round deleted 56 rows another
live round had paid for and manufactured a false finding from the gap; this round did not touch
them at all.

**The 16 quarantined grids were COPIED, never moved.** Every source sha256 is recorded and the
originals sit untouched in their sheet directories.

**Process safety.** Nothing was killed that this round did not start. Identity came from the
listening-port table, never a command-line match. The dashboard port was re-checked **immediately
before every write** under the funnel package, not once at the start — it was not listening at any
of those moments.

**The pre-commit hook is fixed and was verified working before anything was concluded from it.**
It previously refused every commit in this tree while printing a false reason, because it invoked
a bare interpreter lacking a dependency. It now resolves the project interpreter explicitly, and
the facts guard ran and reported real numbers on every commit this round.

---

## 7. What to do next — ranked, with the arithmetic

1. **Exclude the four mis-scored pictures from every accuracy denominator, and audit which
   published figures used 140.** He scored a login screen 10. Every Instagram accuracy number
   computed over that set is wrong by an unknown amount until someone names them. Cost: one pass.
2. **Sweep the ~806 stale wall pictures out of the index.** Closing the fallback stops the problem
   growing; it does not clean it. Worst case $1.638 one-off if every re-capture is walled.
3. **Measure whether a paid grid recovers an age-gated page**, then add the fifth state. 22 of 144
   unknown records are age gates today, and three of the four pictures he mis-scored are age
   gates. $0.0051/run if handled.
4. **Fix the blank-canvas threshold** and re-run every quality claim derived from it. It scores a
   fully empty sheet as 0.0%, so every figure it produced is wrong in one direction.
5. **Replace the two duplicate-cover exemplars.** Two of the four "HE WANTS THIS" examples show
   the same cover twice, and three of them have a full 12-tile sheet of the same handle already on
   disk that the resolver simply does not pick.
6. **Spend ten minutes deciding whether the 21 Instagram-edits pages actually fall under the
   reversal.** They are anime/VFX/quotes, not car/gym/motivation. That is the cheapest path to a
   brain that currently cannot be filled at all — and it needs his judgement, not code.

---

## 8. Paths to open

| what | where |
|---|---|
| the page he opens | `output\bl1486_pack_review\OPEN_THE_PACK_REVIEW.bat` |
| his decisions land here | `output\bl1486_pack_review\approvals.jsonl` |
| the empty gate only he may fill | `clippershq\meme_finder.py` — `APPROVED_IG_EXEMPLARS` |
| the refusal and its declaration table | `clippershq\meme_finder.py` — `_exemplar_pack`, `EXEMPLAR_PACK_PLATFORM` |
| the refusal proved, incl. an unknown platform | `tests\test_bl1489_empty_pack_refuses.py` |
| the blank-canvas settlement | `scratch\bl1489_blank_measure.py` / `_recheck.py` / `.json` |
| the decisive control, as a picture | `output\bl1489_blank_evidence\` |
| the quarantined chrome screenshots | `output\bl1489_wall_quarantine\` |
| the wall walk and its taxonomy | `scratch\bl1489_wall_*` |

**The one instruction that matters:** open that `.bat`, look at the pictures, and press APPROVE or
REJECT under each one. Nothing enters the live pack until you do.
