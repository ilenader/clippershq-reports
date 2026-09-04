# How the page filter works today, and what it should be

**BL-1495 · 2026-09-04 · an answer-only round.** No code was written, no funnel was run, no
setting was changed. **Vendor spend: $0.00 — no request ever left the machine.**

Everything below is answered from the shipped code and the live configuration, not from
earlier write-ups. Where a figure could be driven and checked, it was. Where it could not, the
line says **NOT VERIFIED**. Where two measurements disagree and neither is settled, **both are
printed** — they are not averaged and the newer one is not preferred.

---

## THE SHORT ANSWER TO YOUR THREE QUESTIONS

**Is the brain built for all four?** Half of it. The *question* the model is asked is genuinely
four different questions — four separate briefs, confirmed at the point the request is built,
with the TikTok wording absent from both Instagram briefs and vice versa. But the *examples*
are not: all four brains are shown the same eight TikTok pictures, because the Instagram
approved list is empty and the loader falls back. And the reference material you asked for —
"five latest videos per account" — **exists for the two memes brains and does not exist at all
for the two edits brains.** Not thin: zero. **Is it thinking or guessing?** Both, and the split
is measurable. Asked the same question twice on the *same picture*, the model agrees with
itself 75.8% on text placement, 67.9% on black bars and **52.6% on cutting rhythm — a coin.**
Every one of the ten good-versus-bad comparisons in the reference corpus sits inside that
noise. One thing does separate, and it is not a model at all: on TikTok your 9s and 10s are
letterboxed and your 6s and 7s are not, measured in pixels, **and only 1 of 200 label-shuffles
reproduced the gap by chance.** **What does 1,000 good pages cost and take?** Not the $2 and 2
hours you asked for. TikTok memes is **$19.52 and 8.2 hours**; Instagram memes is **$176.76 and
265.7 hours**; Instagram edits is **$131.21 and 175.2 hours**; TikTok edits delivered **zero
pages**, so its cost per page is undefined, not free. That is 9.8× to 88× your money target and
4.1× to 133× your time target.

---
---

# DOCUMENT ONE — HOW IT WORKS TODAY

---

## 1. The four brains are real, and they are real in one place only

There are four combinations: **TikTok memes, TikTok edits, Instagram memes, Instagram edits.**
They are never pooled — a page that is a 1 in meme mode can be a 10 in edits mode.

To check whether the machine really treats them as four, the network was blocked — the parts
of the program that open a connection were replaced with parts that refuse — and then the
judge was called for real. Nothing could leave the machine; the outgoing message was captured
instead. **[MEASURED]**

| brain | the brief it is sent | fingerprint |
|---|---|---|
| TikTok memes | 4,918 characters | `28c05f855e13` |
| TikTok edits | 10,079 characters | `d43802ad3f9a` |
| Instagram memes | 5,749 characters | `46a1a4d89cbc` |
| Instagram edits | 10,910 characters | `ff1ff0b70cb0` |

Four different briefs, four different fingerprints. The check was designed so it could fail:
the TikTok-specific wording had to be **present** in both TikTok briefs and **absent** from
both Instagram ones, and it was; the edits wording appears in exactly the two edits briefs.
That is the test working, not just passing.

**In plain words, all four begin the same way** — *"You are screening pages for an operator who
reposts short meme videos."* TikTok then adds a list that starts *"reject AI-generated video of
any kind"* and *"reject real animals as the subject"*. Instagram adds a line that reverses one
rule outright: *"a textless first frame is not a rejection here, and this is the most important
line."* The edits briefs then append *"everything above about meme format is suspended — you
are looking at cover frames, not motion."*

**But the four brains stop being four almost immediately.** Mode changes the wording of the
question and two rule suspensions. **It changes nothing else**: not which pictures are shown as
examples, not where the page is written, not how it is tagged. And your configuration currently
runs **memes on both platforms** — driven through the program's own mode resolver with your
real settings, with a control proving the resolver *can* return edits when told to. So the
edits suspensions are not in force today, and an edits run would walk **zero hashtags on either
platform**. **[MEASURED]**

---

## 2. Where a page comes from — and you are walking your worst source

Four ways in. Measured across **14,108 distinct accounts** the funnel has actually seen:
**[MEASURED]**

| source | share of the walk | pages delivered per page walked | your approval | how many marks that rests on |
|---|---|---|---|---|
| **seed** (following / suggested) | **83.32%** | 1.650% [1.435, 1.897] | **38.6%** [25.7, 53.4] | 44 |
| **hashtag** | 10.53% | 8.552% [7.235, 10.084] | 33.3% [18.0, 53.3] | 24 |
| **reels** | **3.34%** | **14.225%** [11.359, 17.670] | **81.8%** [65.6, 91.4] | 33 |
| search | 2.81% | 5.542% [3.688, 8.248] | 77.8% [54.8, 91.0] | 18 |

**You are walking 83% of your pages on the source that both converts worst and that you
approve least, and your best source is 3.3% of the walk.**

**How solid is that?** The left two columns rest on 14,108 accounts and are solid. **The
approval column rests on 119 marks in total** — reels is 33 pages. What survives that
uncertainty: reels [65.6, 91.4] and seed [25.7, 53.4] **do not overlap**, so that contrast is
real. Hashtag and seed **do** overlap almost entirely and are not distinguishable at this size.

**Three earlier readings of the approval numbers disagree and none is settled.** Depending on
which sheets are counted, reels approval is **81.8%** (119 marks), **75.0%** (129) or **73.8%**
(162). All three are printed here on purpose.

**Why the sample is only 119:** every source correctly stamps where a page came from, and that
stamp reaches your eyes — but it is dropped one line before the sheet is saved
(`scratch/bl1397_build_sheet.py:418`). So almost every page you have ever marked cannot be
traced back to its source. **Naming this is not fixing it — the file was left alone.**

---

## 3. What the model actually sees

**The picture.** It travels as an ordinary embedded image. There is no separate "grid" or
"tile" field — those are the names of two *functions* that build the picture, and which one
runs decides everything. **[MEASURED]**

- **On TikTok, the choice is hard-coded to "single video"** (`tiktok_finder.py:3999`). A
  twelve-panel contact sheet is cropped to its **top-left panel and the other eleven are thrown
  away.** Every image measured arrives at **155×275 pixels** — smaller than a postage stamp on
  a modern screen.
- **On Instagram the picture is variable**: the page arrives at 760×760, the examples at
  215×460.
- **A picture is never enlarged.** Both builders shrink an image if it is too big and otherwise
  leave it alone, so a small source stays small.
- **If there is no picture at all**, the judge abstains — which counts as *keep*, not reject.

**The size is not controlled, and this matters more than it sounds.** Across 600 sheets the
sizes measured **73 distinct sizes on one path and 15 on the other, with a 22.9× spread and a
floor of 103×183**. The reject threshold was tuned across that mixture without anyone knowing
it varied. **[NOT VERIFIED by me — carried from an earlier measurement.]**

**One prompt contradicts itself.** The shared brief says *"You are shown a CONTACT SHEET"*
while the very next section says *"You are shown ONE post cover from the page, not a contact
sheet."* Both sentences are sent in the same message (`free_judge.py:1035-1038`). **[MEASURED]**

**The written facts.** The model is handed: handle, display name, followers, verified, bio,
where it was found, post count, and up to twelve captions. But the two platforms fill in
different halves: **[MEASURED]**

- **Instagram sends no follower count and no verified flag** — those two slots are always
  empty.
- **TikTok sends no captions at all and no "found via"**, and sends two fields under names the
  renderer ignores.

**The post-count field used to lie badly** — a page with 360 videos once reached the model as
5, a median understatement of **168×** across 18 accounts. The first cause is fixed. The
fallback chain still ends in a sample count, so it can still understate when the real total is
missing.

**The examples.** Eight pictures, every time, for every brain. **All eight are TikTok pages.**
The Instagram approved list is empty (`meme_finder.py:4446`), so the loader falls back to the
TikTok set — verified by asking the loader what platform each picture came from and getting
"TikTok" eight times out of eight. **Mode never changes the examples.** **[MEASURED]**

---

## 4. What it answers, and who can overrule it

The model returns a verdict of WANT or REJECT, a confidence from 0 to 100, and a
twelve-word reason.

**Three different reject thresholds exist and they disagree.** The number most people quote,
**80**, governs only a labelling band; the code says outright that it "governs nothing". The
**actual cut** is a per-model bar, and both live models sit at **90**. A third number, 95,
labels a page a "confident keep". **[MEASURED]**

**Who can overrule the model:** several rules can reject a page the model wanted — a drawn-text
rule and a black-bars rule on Instagram, a green-screen and template rule on TikTok. **Nothing
anywhere can promote a page the model rejected.** The override is one-directional.

**One asymmetry is unguarded:** on Instagram a picture-judge rejection is deliberately *not*
made permanent, so the page can be reconsidered later. **On TikTok the same rejection is
permanent.** The same decision is reversible on one platform and final on the other.

---

## 5. What gets bought, and when

**The order is the whole story, and the two platforms get it opposite ways round.**

- **Instagram spends late.** The page picture is captured free, the free judge runs, and only
  then is the profile bought. The email comes out of a response already paid for.
- **TikTok spends early.** The profile is **bought before the picture judge runs**
  (`tiktok_finder.py:2658` before `:2923`). The model gate cannot save that money. And the code
  records that the bought profile changed **0 of 1,185 verdicts.**

Prices from your live configuration: **[MEASURED]** TikTok $0.000600/call; Instagram
$0.00069064/call; deep-check $0.001/call. There is **no configured price for the judge** — it
is a constant in code, $0.000089/call.

**Per page, the models are tried in this order:** the *paid* one first, then a free one, then
two more free attempts. The paid model is deliberately first.

---

## 6. Where a page ends up

An approved Instagram page lands in a dated spreadsheet and in the master list; an approved
TikTok page lands in a run file and in the master list. **Both carry an email column.**

Two things worth knowing: the TikTok export folder named in the code is **dead** — nothing
writes to it. And when a TikTok address is written to the master list, its origin is
**hard-coded** to one label, so **the master cannot tell a free address from a paid one.**
**[MEASURED]**

---

## 7. Every rule that can reject a page — and which ones are fiction

There are **43 named rejection rules**, roughly 35 of them with a number in them. Each was
tested by feeding it something designed to trip it and something designed not to. **A rule that
cannot be made to fire is dead.**

### Alive today

**TikTok:** low average views (floor 3,000, a code default — your config sets none); language;
"thin evidence" (which produces *unjudged*, not a rejection); recency (**180 days**, from your
config).
**Instagram:** low views (500); too few posts (13); format share; news/media share (0.60); not
English; caption language; creator page; promotional; stale (152 days); photo-heavy; black
bars.
**Account-level gates:** followers (500), verified, average views, theme, niche.

### Dead — the code works, but nothing ever reaches it

| rule | why it never fires |
|---|---|
| TikTok talking-head | its input is hard-assigned "nothing" (`tiktok_finder.py:2741`) |
| TikTok template-overlay | the text list is always empty, for the same reason |
| TikTok share-per-play | switched off by a null setting and a sentinel |
| **Your own hand rules, on TikTok** | they read three fields the facts pack does not contain |
| Short-caption floor | its minimum is **0** |
| Instagram language gate | the setting is absent from your config |
| **Instagram film/TV narration** | it is computed and **never added to the reject list** |
| **The account recency gate** | `gates["recency"] = True` is written **literally** (`quality_gate.py:2213`); the real check runs and its answer is thrown away. **No setting can revive this one.** |
| `page_rules.py` (three rules) | a shipped file with **no callers at all** |

Six of those were already suspected and are **confirmed**. **Three were not, and are new here.**

**There is a sharper version of the fourth row.** Your own rules are dead on TikTok because the
facts pack omits views, video count and post age — and the function that *does* build all three
exists and **has no caller anywhere in production.** The parts are on the shelf.

### What the live rules cost you, on your own marks

Measured on **311 distinct TikTok pages you graded**, of which **you want 101 (32.5%
[27.5, 37.9])**: **[MEASURED]**

| rule | rejects pages you wanted | 95% interval | alive? |
|---|---|---|---|
| **recency at 180 days** | **21 of 101 = 20.8%** | **[14.0, 29.7]** | **yes** |
| share-per-play | 11 of 101 = 10.9% | [6.2, 18.5] | no (dead) |
| low views at 3,000 | **0 of 101 = 0.0%** | [0.0, 3.7] | yes |
| any rule still on today | **21 of 101 = 20.8%** | [14.0, 29.7] | — |

**One in five of the pages you chose by hand is thrown away by a single date threshold**, and
one of those 21 you scored a **9**.

⚠️ **A published figure does not reproduce.** The number **28.8%** has been quoted for this.
Six different ways of counting were swept — 19.7%, 20.8%, 20.0%, 18.8%, 16.7%, 0.0% — and none
produces 28.8%. The measured answer is **20.8% [14.0, 29.7]**. The two are not incompatible
(28.8 sits in the upper half of that interval), but 20.8% is what the data on this machine
says. **Both are named.**

**Instagram cannot be checked at all. [NOT VERIFIED]** No ground-truth file records which rule
fired. Of your Instagram marks, 91 of 100 are in the store, 26 are pages you want, and **13 of
those 26 are marked not-passed (50.0% [32.1, 67.9])** — but the reason is empty on all 26, so
**no rejection can be attributed to any rule.**

---

## 8. Is it thinking, or guessing?

The cleanest test: ask the model the *same question about the same picture twice* and see
whether it agrees with itself. Over **1,083 repeat pairs**: **[MEASURED]**

| what it was asked to read | agreement with itself | 95% interval |
|---|---|---|
| where the text sits | 75.8% | [72.1, 79.2] |
| black bars present | 67.9% | [63.9, 71.7] |
| **cutting rhythm** | **52.6%** | [48.4, 56.8] — **a coin** |
| colour grading | 59.9% | [55.7, 64.0] |
| subject spread | 75.1% | [71.3, 78.5] |

**A feature that agrees with itself 52.6% of the time cannot tell two groups apart by less than
about half.** And when the good pages were compared with the less-good ones on all five
features across both memes brains, **all ten comparisons fell inside that noise** — the largest
gap was 14%, about a quarter of the room noise alone could produce.

⚠️ Two figures in the brief I was given do not match the file: colour grading was quoted at
**3.1%** where the measurement says **59.9%**, and "80 of 80 comparisons" where this file
contains **10**. **Both readings are named; I did not average them or pick one.**

### The most important thing on this page

Rhythm agreement **rises from 52.6% to 77.8% when the picture is cropped to a single frame.**
That looks like an improvement and is the opposite of one: a single frame has no rhythm, so the
model stops varying and settles on a constant answer. The two versions agree with *each other*
only 24.4%. **Destroying the evidence made the instrument look 25 points more reliable** — and
the cropped version is the one production sends on TikTok.

### What genuinely works, and it is not a model

On TikTok, your 9s and 10s are letterboxed and your 6s and 7s are not. Re-derived
independently here from the raw per-page numbers: **[MEASURED]**

- median bar fraction **0.3833 (93 pages) versus 0.1656 (58 pages)**, difference **+0.2177**,
  permutation **p = 0.0037**
- share of panels with any bar: **0.7717 versus 0.6265**, p = 0.0021
- across **all 193 TikTok pages**, rank correlation **+0.2338**
- **control: only 1 of 200 label-shuffles produced a gap that large**

**The tail does not separate** (p90 0.5292 versus 0.5615, p = 0.31) — this is a step at score 9,
not a gradient. **On Instagram it carries nothing**: the difference is 0.0271 with **113 of 200
shuffles beating it** — that one is pure noise.

**So, plainly:** the counting parts — followers, views, dates, language, and letterboxing
measured in pixels — are real arithmetic. The model's opinions about rhythm and colour are
inside their own noise and should not be used to decide anything. The overall page verdict is
above noise but **has never been checked against a real outcome.**

---

## 9. The money and the clock

**[MEASURED]** Denominator: pages actually appended to the master list by that run. Sample is
small — one to six runs per brain — and the seconds are a pooled ratio, not a median.

| brain | billed calls per delivered page | $ per 1,000 | hours per 1,000 |
|---|---|---|---|
| TikTok memes | 32.3 | **$19.52** | **8.21** |
| Instagram edits | 176.0 | **$131.21** | **175.22** |
| Instagram memes | 233.6 | **$176.76** | **265.69** |
| TikTok edits | — | **undefined — 0 delivered** | undefined |

**Every delivered page carried an address (24 of 24, [86.2, 100])**, so cost per 1,000
*addresses* equals cost per 1,000 pages here.

**Against your targets of $2.00 and 2 hours per 1,000:**

| brain | money | time |
|---|---|---|
| TikTok memes | **9.8× over** | **4.1× over** |
| Instagram edits | **65.6× over** | **87.6× over** |
| Instagram memes | **88.4× over** | **132.8× over** |

**TikTok edits delivered nothing at all. That is not "cheap" — it is undefined.**

### Why it takes so long — the bottleneck, named

It is not the picture capture. It is the judging, and inside the judging it is **one model**:
**[MEASURED, 200 pages]**

- overall per page: median **9.07 s**, p90 26.53 s, **p99 138.40 s**
- the fast model, 191 pages: median **8.60 s**
- the slow model, 9 pages: median **116.33 s** — **13.5× slower**

**9 of 200 pages (4.5%) consume 30.85% of the entire judging stage.**

### Three costs that do not appear anywhere

1. **The run record excludes the judge entirely** — it filters on campaign, and the judge books
   under a different one. One window was **7.94% low**.
2. **The slow model bills per token, is counted as a free send, and never books to the
   ledger** — so the most expensive thing on the clock is invisible on the bill.
3. **Five files price Instagram calls 13.1% too low.** **52,918 of 73,122 Instagram calls
   (72.4%) were booked at the wrong price — $4.80 of real spend was never recorded, and the
   Instagram ledger is 9.56% low.**

### Where your addresses actually come from

**[MEASURED, August: 14,599 rows, 8,247 addresses]** Spotify supplied **83.97%** of them at
**$1.27 per 1,000**. The page funnel supplied **15.63%** at **$20.98 per 1,000**. **The page
funnel is about 16.5× more expensive per address** (range 9.6×–19.7× depending on scope).

⚠️ **A widely-quoted price should be retired.** **$137.31 per 1,000 addresses** was
`$3.58 ÷ 0.0261` — a division, not a measurement — and the only denominator named was *pages*
for a *per-address* figure. The exact quotient is **137.1648**, not 137.31. ⚠️ **And its
proposed replacement has the same defect**: **$78.53 × 0.0396 = $3.11 per 1,000 pages** — again
a page price divided by a carry rate. Measured directly instead, the answers are **$131.21**,
**$176.76** and **$20.71–24.59**. **None lands in the $78–82 range. Both are named.**

### The real lever for addresses is page size

**[MEASURED, 72,956 rows]** Share of pages carrying an address, by follower count:

| followers | carry rate | 95% interval | n |
|---|---|---|---|
| under 1k | 1.11% | [0.94, 1.31] | 12,096 |
| 1k–10k | 2.56% | [2.38, 2.76] | 26,571 |
| 10k–100k | 11.17% | [10.66, 11.70] | 13,868 |
| 100k–1M | 33.27% | [31.77, 34.80] | 3,718 |
| **1M+** | **69.29%** | [65.67, 72.69] | 661 |

**A page with a million followers is 62× more likely to carry an address than one under 1k.**
⚠️ The published curve (12.5 → 28.9 → 46.5 → 49.0 → 58.1) **does not reproduce on any of three
denominators**. The *direction* reproduces everywhere; the levels do not, because the master
list holds only pages that were already delivered. **Both named.**

### And you cannot see any of this

Your dashboard's run file holds **25 runs, all clip-rendering work from 2–5 August. Zero page-
funnel runs.** Every number in this section lives only in files the dashboard does not read.

---

## 10. Did you actually get reference material for all four?

**No. Two of the four brains have none at all.**

You asked for: *"For each account take the five latest videos, download them, and use them as
reference for what it should look like."*

**What is actually on disk, counted directly: [MEASURED]**

- **276 page folders — 193 TikTok, 83 Instagram**
- **Zero video files.** 13,815 images. (The counter was proved able to see files — it found
  13,815 of them — so that zero is real.)
- The images are six stills per video: 2,303 × 6 = 13,818, minus 3 missing = **13,815. The
  arithmetic closes.**

**So "2,303 videos" is true as a count of videos *processed*. No video survives. What survives
is six stills each.** Most pages have ten videos behind them, not the five you asked for.

**And every one of those 276 pages was graded on the memes brief**, before an edits brief
existed anywhere in the project. Nineteen pages were *found* using an edits search term and
then *judged as memes*. Discovery is not mode.

| brain | pages of reference material |
|---|---|
| TikTok memes | 193 |
| Instagram memes | 83 |
| **TikTok edits** | **0** |
| **Instagram edits** | **0** |

**And separately: none of the 130 edit pages you supplied by URL (66 TikTok, 64 Instagram) is
in the corpus at all**, on any of three matching rules — and none has ever been put in front of
you in a sheet. They are ungraded because you were never asked, not because you declined.

**One more thing about the corpus: it is not a good-versus-bad set.** Your marks cover 795
pages; **423 scored below 6, and none of those was ever downloaded** — while 220 of 326 pages
scoring 6+ were. (That contrast is itself the control that proves the zero is real.) So the
only comparison the pictures can support is *"9s and 10s versus 6s and 7s, among pages the
filter already delivered and you already liked."* **There are no examples of what you reject.**

---

## 11. Your grades change nothing

**Confirmed, and it is worse than "not wired".**

Of the **113 files a real run can actually reach**, **zero** read your marks. The 52 files that
do read them are **50 throwaway analysis scripts and 2 tests**. The single place in production
that opens a mark file is dead code.

**The write side and the read side are not one broken connection — they are two separate
systems that have never been joined.** The tool that collects your marks is launched from a
desktop shortcut, not from the funnel, and sits among 60 files no run can reach.

**And two more record-keeping holes: [MEASURED]**

- **All nine outcome columns are empty on all 72,956 rows.** (The counter was proved on a
  column with only five entries, so the zeros are real.) **No accuracy figure this project has
  ever produced — yours or the machine's — has been checked against a reply.**
- **The picture verdict is stored nowhere**, on any of the 72,956 rows, while being used to
  make decisions. That stage is **14.0% of all spending** and is **unauditable**. (Correction
  to the record: the decision-time consumer *recomputes* the verdict rather than reading a
  stored column — the effect is the same, the mechanism is not.)

---
---

# DOCUMENT TWO — WHAT IT SHOULD BE

**Ranked by what it costs you, not by how interesting it is.**

---

## First, the honest truth about 95%

You want the filter to be 95% right. **Measured against your own marks, that is not available
to any model, however good** — and the reason is not the model.

**Your grades agree with themselves 75.8%** — independently reproduced here as **135 of 178 =
75.84% [69.05, 81.54]**. And that splits into two very different numbers: **[MEASURED]**

- **92.9% [88.2, 95.8]** on pages far from your keep/drop line
- **59.6% [45.3, 72.4]** on pages within one point of it — **exactly the population the filter
  exists to sort**
- the intervals **do not overlap**

⚠️ That headline is **scope-fragile**: on wider definitions it reads 56.5% or 80.3%. The
row-position decay (88% early, 67% past row 300) is **NOT VERIFIED** here.

**A model that agreed with you perfectly would still score ~24% "wrong", because the answer key
disagrees with itself.** Chasing 95% against that target is chasing noise.

### Two free things that raise your own ceiling

1. **Ask for keep/drop instead of 1–10.** Exact 1–10 reproduces **49–54%**; a simple keep/drop
   at your own line reproduces **84–88%** — measured two ways on two corpora. Same person, same
   pages. **The score is the wrong instrument.**
2. **Cap sheets at about 150 rows.**

Neither costs a cent.

### The number that *can* reach 95%, and matters more

Not "does the model agree with your score" — capped at ~76%. Instead: **of the pages you want,
what share does the filter kill?** That is one-sided, it has a real answer, and it is the
number worth targeting.

**Today, on TikTok: 21 of 101 = 20.8%, Wilson upper bound 29.7%.** To get that upper bound
under 5% you would need roughly **n ≈ 500 wanted pages** with zero kills — about **five times**
the marked set you have. **On Instagram it cannot be computed at all**, because no rule outcome
is ever recorded.

---

## The ranked list

### 1 — Stop throwing away one in five pages you want, for a date
**Change:** raise the TikTok recency threshold from 180 days. **Measured sweep on your own 101
wanted pages:** 62 days → **37.6%** killed; **180 days (today) → 20.8%**; 1,095 days → **5.9%
[2.8, 12.4]**.
**Buys:** ~15 percentage points of pages you wanted, recovered. At today's TikTok cost that is
roughly **$19.52 → ~$15.50 per 1,000 delivered** for the same walk, and it costs **no extra
time and no extra money** — it is one number.
**Risks:** older pages may be less active; you would be trading freshness for recall.
**Difficulty:** trivial. One value.
**Confidence: high** — measured on your own marks, re-derived two ways.

### 2 — Walk reels instead of seed
**Change:** shift the mix toward reels and search.
**Buys, with the arithmetic shown:** today the walk yields **1 page you'd approve per 74.6
walked**. At a 25% reels / 15% search / 40% hashtag / 20% seed mix that becomes **1 per 20.7 —
a 3.6× improvement.** Even putting reels at its *worst* plausible rate and seed at its *best*,
it is **1 per 23.6 — still 3.2×**.
**Risks — and this is the one that could sink it:** reels is **471 of 14,108 accounts** today.
A 25% reels walk needs roughly **7.5× more reels supply than the funnel has ever produced**.
**NOT VERIFIED that that supply exists.** ⚠️ And it **does not fix the clock**: this exact mix
was costed at **8.6 hours per 1,000 against your 2-hour target**.
**Difficulty:** moderate. **Confidence: high on the ratio, unknown on the supply.**

### 3 — Kill the slow model
**Change:** drop or time-box the model that takes **116 s per page against the other's 8.6 s**.
**Buys:** **9 of 200 pages consume 30.85% of the judging stage.** Removing that tail cuts the
dominant cost on the clock — the single largest time win available, and it is a deletion.
**Risks:** it holds reject authority and said REJECT on 7 of its 9 pages, so removing it will
change verdicts. Measure the change on your marks first.
**Difficulty:** easy. **Confidence: high.**

### 4 — Target big pages for addresses
**Change:** prefer pages with more followers when the goal is an address.
**Buys:** carry rate rises **1.11% → 2.56% → 11.17% → 33.27% → 69.29%**. A page with 1M+
followers is **62× more likely to carry an address** than one under 1k.
**Risks:** big pages may be less likely to reply, and that is unmeasurable today because **all
nine outcome columns are empty**. **Confidence: high on carry, zero on value.**

### 5 — Make letterboxing a measurement, not a question
**Change:** stop asking the model about black bars on TikTok and measure them in pixels.
**Buys:** the model agrees with itself only **67.9%** on bars; the pixel measurement is exact
and reproducible, separates your 9s from your 6s at **p = 0.0037**, and survived a
label-shuffle control **199 times out of 200**. It is also free and instant.
**Risks:** it is a **step at score 9, not a gradient**, and **on Instagram it carries nothing**
— apply it to TikTok only. **Difficulty:** easy. **Confidence: high.**

### 6 — Stop buying the TikTok profile before the judge runs
**Change:** move the profile purchase after the picture judge.
**Buys:** the profile is bought on every page and **changed 0 of 1,185 verdicts**. On TikTok's
32.3 billed calls per delivered page this is a direct, safe saving.
**Risks:** low — the data is still available if needed later. **Confidence: high.**

### 7 — Show each brain its own examples, and get the edits material
**Change:** all four brains currently see the same **eight TikTok pictures**, and the two edits
brains have **zero** reference material.
**Buys:** unknown, and that is the honest answer — no measurement exists because the material
does not exist. This is the difference between the system you asked for and the one you have.
**Difficulty:** moderate: put your 130 supplied pages in a sheet and ask you to grade them —
they have **never been shown to you.**
**Confidence: high that it is missing, unmeasured that fixing it helps.**

### 8 — Record what happened
**Change:** persist the picture verdict and the rule that fired; fill the outcome columns.
**Buys:** nothing this week. **Everything after.** Today **14.0% of spending is unauditable**,
no Instagram rejection can be attributed to a rule, and no accuracy figure has ever been
checked against a reply. Every item above is measured on 101 to 311 marked pages because that
is all that exists.
**Difficulty:** small. **Confidence: high that it is the ceiling on every future answer.**

### 9 — Fix the ledger so the numbers mean something
**Change:** four defects, each small. The ledger is written **before** the request
(`free_judge.py:1503` before `:1507`), so **failed attempts are billed**. The run record
excludes the judge. The slow model never books. Five files price Instagram 13.1% low, so
**72.4% of Instagram calls were booked wrong and the ledger is 9.56% low.**
**Buys:** no money directly — but every cost figure above inherits these errors.
**Difficulty:** small. **Confidence: high, all four confirmed.**

### 10 — Delete or revive nine dead rules
**Change:** nine rules can never fire — including your own hand rules on TikTok, and one
recency gate that is **literally assigned true** and can never be revived by any setting.
**Buys:** no money and no time. It buys **an honest rule list.** Today the documented filter
and the real filter are different objects, and every conversation about "the filters" has been
partly about fiction.
**Difficulty:** small. **Confidence: high — each proved by a planted control.**

---

## What I did not verify

- **Instagram rule-level rejection rates** — nothing records which rule fired.
- **The published carry curve, the $78–82 cluster, the 65× Spotify ratio, "28.8%", "80 of 80",
  colour grading at 3.1%, and the 12.5→58.1 band** — none reproduced; measured alternatives are
  given beside each.
- **Whether reels supply can reach 25%** — the single largest open question in the ranked list.
- **The row-position decay in your grading.**
- **Whether any of this improves replies** — the outcome columns are empty.

## One disclosure

This round made **no vendor calls and spent $0.00**. But a probe that captured the outgoing
request wrote **four rows to the ledger totalling $0.000356**, because the ledger is written
*before* the request is sent. No connection was ever opened. **The ledger now over-states by
four calls, and it was left that way rather than hand-edited.** That is item 9 above,
demonstrated accidentally.

---

*Read-only round. No file under the application, the configuration, the ledger, the lead store,
the seen stores, the documentation or the example packs was modified.*
