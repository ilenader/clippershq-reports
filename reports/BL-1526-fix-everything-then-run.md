# BL-1526 — Fix everything outstanding, then run edit pages for him to grade

**Round:** BL-1526 · **Filed:** 2026-09-07 · **Cap:** $3.00 · **Spent: $0.3696** (LamaTok, at the wrapper)

---

## 1. Safe to run, and the headline answer

**Safe to run.** No judging rule was added or loosened and no threshold moved. Every fix is
mutation-proved in both directions with the restore verified by sha256, every new test uses `raise`
rather than `assert` and is green under `python -O` (enforced by an AST scan of the test's own
source), and the one repair that would change which pages are labelled walled ships **behind a
switch, default OFF**, because it cannot be scored offline.

### How many pages are in front of him, where the .bat is, and what it cost

**150 rows are in front of him** — **33 the filter kept, 95 it rejected, 22 UNJUDGED** — cut from
577 and **evenly spaced within each side so the run's own proportions survive** (rejected 95 of
366, delivered 33 of 125, unjudged 22 of 86). Both sides, because a sheet of accepts is a demo and
only both sides measures a filter. It asks **KEEP / MAYBE / DROP**, not a number.

**The .bat:** `%USERPROFILE%\...\output\bl1526_sheet_20260907_115932\START_HERE.bat`
Double-click it. **No port, no URL** — a grading session was lost to a bookmarked one.

**What it cost: $0.3696**, from the run's own counter at the wrapper — **616 billed LamaTok calls**
at $0.000600, in **11 minutes 7 seconds**. ⚠️ **That figure is LamaTok only.** The run also made
**172 picture-judge (vision) calls** through a different client that my wrapper does not wrap, so
their cost is **NOT COUNTED IN $0.3696** and I am not going to compose one from a rate I did not
measure.

**⚠️ HE ASKED FOR 100 ADDRESS-BEARING PAGES AND GOT 9. That is a shortfall, reported as a
shortfall, and it has two independent causes that compound.**

1. **The supply is not there, and the funnel says so itself.** Its own estimator prints: *"the tags
   entered support about 88 email(s); 100 were asked for. Add tags or raise depth — the run cannot
   invent supply."* At the shipped `depth: 1` the eight **declared** edit tags support about **21**.
   **100 was never available from the declared tag set at any depth I could run.**
2. **No process survived long enough.** A depth-10 walk is estimated at **4 h 16 m**, and **two
   funded runs were killed from outside the process** — no traceback, no `finally`, empty stderr —
   at ~13 minutes and ~4 minutes. The funnel **persists nothing until the end**, so the first,
   which had already judged **114 handles with 95 passing**, left an **empty directory**. The third
   run was therefore re-sized to **COMPLETE** rather than to reach the target, and it did:
   `error: null`, `stopped: ""`, a real export, and a real sheet.

**The measured address rate is 9 of 125 delivered = 7.2% [3.8, 13.1]**, sitting inside the prior of
6.9% [2.7, 16.4]. **The address rate, not the page rate, is what binds** — the same run delivered
125 pages in 11 minutes.

**And every one of the 9 addresses came free.** `with_email_free: 9` of 9, `profiles_bought: 0`,
`profiles_not_bought_by_switch: 116`. The TikTok paid profile bought **nothing** this run, which is
the third independent confirmation of that result.

---

## 2. What I was asked to do

Fix six measured defects that previous rounds named and left, then run the TikTok edits brain for
**100 delivered pages that carry an email address**, and put them in front of him on a grading
sheet asking **keep / maybe / drop** rather than a 1–100 score. Report the keep rate per brain with
its interval, its denominator and the self-agreement ceiling beside it; report every cost and clock
division including **$ per 1,000 WITH AN ADDRESS**; and classify every address CLIENT / MEME_PAGE /
CLIPPER. One reserved agent on one question: why only 120 of 10,164 addresses are clippers.

---

## 3. What shipped

Six defects fixed. Each mutation-proved **both ways** with the restore **sha256-verified**, tests
using `raise` never `assert`, green under `-O`, and the no-`assert` rule enforced by an AST scan of
each test's own source.

| # | fix | `file:line` | category | how it was proved |
|---|---|---|---|---|
| 1 | **The wall detector's dead arm** — `\b` in a NON-RAW string became a literal BACKSPACE (0x08), so `/<BS>log in<BS>/` could never match | `page_capture.py:182` | **LOCAL, 1 site**, 0 elsewhere in 650 files | **three** instruments, each answering a different question (see §6); repaired arm **driven in a real browser** against planted HTML |
| 2 | **The paid-grid precondition** — `_paid_grid_needed` returned True on a 9-tile record down **two** arms | `page_capture.py:945-979` | LOCAL | driven, not inferred; ships as **defence** — its briefed saving is refuted in §6 |
| 3 | **The decode probe** — an undecodable file is now **UNJUDGED**, never a rejection | `tiktok_finder.py:1483-1529`, `:1567`, `:1310-1312` | **LOCAL, 1 production site**; 18 non-production copies are the positive control | two-armed: undecodable `NOT_TARGET`→`TARGET`+`ocr_unjudged`; **decodable unchanged, decision hash byte-identical** |
| 4 | **The watermark ranking** — `download_addr`, which burns the handle onto every frame, demoted to **last** (demoted, not deleted) | `tiktok_finder.py:1462` | LOCAL | selected **0 of 117** [0.0, 3.2] while present on 114 of 173 |
| 5 | **The 1.4-second hero floor** | `video_strip.py:188`; constant moved from `:324` to `:107` | **LOCAL fix, GENERAL defect class — 8 sites, 6 still live** | old sampler broke the rule on **163 of 388 = 42.0% [37.2, 47.0]**, earliest 0.451 s; new sampler **0 of 388** |
| 6 | **The purchase census, both instruments** | — | — | union **19 sites**; AST misses **1 of 13 (7.7%)**, text reports **6 of 19 non-calls (31.6%)** |

⚠️ **Defect 1 ships behind `WALL_WORD_ARM`, DEFAULT OFF**, and the reason is an absence rather than
caution: **no capture record stores the page text** (33 keys; `text_chars` is a length), so the
repaired arm **cannot be replayed against the 3,329 stored captures.** No paired score is possible,
and the label both suppresses the shot and orders a paid grid — so it does not go live on my say-so.

⚠️ **Named and LEFT, deliberately:** the six live sites still sampling a first frame before 1.4 s
(`clip_ocr.py:385`, `clip_pipeline.py:2924`, `harvest_run.py:173`, `clip_label_text.py:1477`,
`layout_read.py:47`, `paste_batch.py:1552`) — BL-1507 measured this rule at only **+1.7 points
pooled (p=0.227)**, so changing live behaviour is not free. And the two ungated profile-purchase
sites in §6.

---

## 4. What was measured

### 4a. THE TWO CORRECTIONS HE NEEDS BEFORE HE READS ANYTHING ELSE

**CORRECTION 1 — the last-post date is not purchasable, and he believes it is.** He said "we
already have this, we just pay one more call." **There is no call to make.** The paid
`/v1/user/by/username` response has **56 leaf keys and no last-post field** — its `createTime` is
**account creation**, and `nickNameModifyTime` / `uniqueIdModifyTime` are name changes. LamaTok has
no user-videos endpoint at all: `api_client.py:439-447` **raises `UnsupportedEndpoint` rather than
spend a call to be told 404**, recording that 23 paths were tested and none returns a user's posts.

The hashtag route does carry a date on **239 of 239 items** — but it is **the date of the video
that matched the tag**, not the account's latest post. Of the authors appearing more than once,
**50.0% carried DIFFERENT timestamps, the largest 449.8 days apart**; **0 of 8 pages were in time
order**; and **no pinned flag exists on that route at all**, which matters because pinned median
views are 1,562,246 against unpinned 2,658 — a pinned post is a page's best work, not its latest.

**So the shipped floor treatment — "posted at least this recently" — is the best available AT ANY
PRICE.** Not a compromise, not a placeholder: the ceiling.

**CORRECTION 2 — ask him for keep/drop, not 1–100.** His exact score reproduces at **49–54%**. The
same judgement expressed as keep/drop at his own line reproduces at **84–88%**, measured two ways
on two corpora. **36.9% of his scores are a 1 and 19.0% are a 9 or 10 — the scale is already a
three-way switch**, and a finer one would be worse. A middle band costs about **4.5 points**
against pure binary while still beating the raw score by 30, so the sheet offers **KEEP / MAYBE /
DROP** and says why in the sheet itself.

**AND HIS INSTAGRAM POINT IS ACCEPTED AND CORRECT: paying there is fine.** The Instagram hashtag
payload carries **no biography, no follower count, no email and no post count — only `is_verified`
(33/33)** — and **51.03% [47.96, 54.09] of 1,019 Instagram addresses came from the paid contact
button and are provably absent from the bio.** The Instagram profile call is deferred to survivors
and must never be removed.

### 4b. The run — TikTok edits, completed

**MEASURED**, from the run's own counters. `mode: edits`, resolved from `CLIPPERSHQ_MODE` and
reported as such by the resolver; `config.json` was **never written**.

| | |
|---|---:|
| billed LamaTok calls (wrapper counter) | **616** |
| **cost** | **$0.3696** |
| elapsed | **667.1 s** |
| videos seen | 1,421 |
| distinct authors | 1,050 |
| handles searched | 553 |
| reachable | 510 |
| **delivered — the PASS counter, not `leads`** | **125** |
| **carrying an address** | **9** |
| …of which came from the FREE bio | **9 of 9** |
| paid profiles bought | **0** |
| profiles not bought because the switch is off | 116 |
| profiles saved by the verdict ordering | 45 |
| picture-judge calls / rejections / errors | 172 / 45 / **0** |
| dropped as stale (before paying) | 232 (214) |
| skipped: already in master / already seen | 212 / 71 |
| sheets built / refused | 172 / **0** |
| master offered / appended / merged / errors | 9 / **9** / 0 / none |

⚠️ **`ocr_ran: false` and `ocr_skipped_inert: 172`** — the TikTok OCR stage **did not run**, which
confirms independently that both defects fixed in items 3 and 4 above are **LATENT, not live**: the
wrong rejection needs that stage on. What is wrong *today* is the reported provenance, not a lost
page. Saying so is the difference between a fix and a claimed saving.

### 4c. The sheet

**150 rows, both sides, KEEP / MAYBE / DROP.** Cut from 577 and evenly spaced *within each side*, so
the run's proportions survive the cap: rejected **95 of 366**, delivered **33 of 125**, unjudged
**22 of 86**. ⚠️ Capped at 150 because agreement runs 88% early and **67% past row 300**, and his
median gap between marks is 3.0 seconds.

⚠️ **190 rows were REFUSED for having no picture from this run of that page** — a hard refusal, not
a fallback. That matters because a previous builder fell back to an image search and served him
pictures **12–13 days old from other rounds, including an Instagram login form he scored 10**; 33 of
his points landed on pictures unrelated to the pages beneath them. All 150 pictures that did ship
were **copied in and verified byte-identical by sha256**.

**Every row carries** the exact image with its **delivered** pixel size, the verdict and the model's
own sentence, **the number against its threshold** (4,200 against a 1,000 floor, not "low views"),
the address **and where it came from**, mode/platform/source stamped at write time, and **UNJUDGED
as a visible third state** — never rendered as REJECTED.

⚠️ **The picture on disk is NOT the picture the model saw**, and printing the on-disk size would
have been a third repeat of an old mistake: sheets are written at 465×992, and the judge re-encodes
in memory to **356×760**, or crops one cell to **427×760**. The row prints what `as_sent()`
**measures** by calling the judge's own encoders with the funnel's own arguments.

**Proved from File Explorer, not asserted:** `.bat` double-clicked → writability marker → real
browser → **24 assertions ALL_PASS** → keyboard marks → **5 marks read back off disk** → reload kept
them → **console 0 messages, 0 page errors, 0 non-2xx** → **test marks deleted** (asserted mine
first). **Mode survives resolution: 5/5 raw rows carry a mode, 4/4 resolved pages return it** — the
thing that made 2,323 previous rows unusable.

### 4d. Cost and clock, TikTok edits

Every division written out. **The denominator is the PASS counter (`passing`), not `leads`** —
`leads` is delivered AND has an email AND is new to master, three conditions, and reading it as
"delivered" once overstated a brain's price by 5.00×.

| measure | value |
|---|---:|
| pages walked per delivered | **6.14** (767 rows) |
| authors seen per delivered | 8.40 |
| paid calls per delivered | **4.93** |
| **$ per 1,000 delivered** | **$2.96** |
| **$ per 1,000 WITH AN ADDRESS** | **$41.07** |
| seconds per delivered page | **5.34** |
| hours per 1,000 delivered | **1.48** |
| address carry rate | **9 / 125 = 7.2% [3.8, 13.1]** |

⚠️ **This is measured directly, never composed from a carry rate** — that is how $137.31 and $78.53
were each manufactured in earlier rounds. **And it is LamaTok only:** the 172 vision calls are not
in it.

**Every address classified — and the stamp cannot be taken at face value.** All **9** were written
`lead_kind: clipper` by `tiktok_finder.py:3792`, a writer **BL-1445 never migrated**. Under the
taxonomy in force since 30 August these are curated pages — **`meme_page`** — which means **all 9
are routed to the PRIMARY send file instead of `MEME_PAGES_BOT_READY.csv`**, the exact failure
`writer.py:1301` exists to prevent. **This round's own output demonstrates the bug live.**

| taxonomy | CLIENT | MEME_PAGE | CLIPPER |
|---|---:|---:|---:|
| as stamped by the unmigrated writer | 0 | 0 | **9** |
| under BL-1445's taxonomy (curated pages) | 0 | **9** | 0 |

---
### 4e. The reserved question — why only 120 of 10,164 addresses are clippers

**BOTH — and the labelling half is 91.2% of it.** $0.00 spent; the whole answer came off disk.

The 120 was reproduced **to the row**. The era cutoff `date_added >= 2026-07-11` was confirmed two
ways (12,968 − 2,804 = 10,164, and the 2,804 excluded are **100% clipper**; independently
`spend.json["runs"][0]["ts"] == "2026-07-11 21:41:12"`).

| step | rows |
|---|---:|
| clipper addresses under the label in force until 2026-08-30 | **4,186** |
| − predate the ledger (one 8-day burst) | **−2,804** = 95.90% [95.11, 96.56] |
| = era clipper addresses as of 30 Aug | **1,382** |
| − reclassified `clipper` → `meme_page` by BL-1445 | **−1,274** = 92.19% [90.65, 93.49] |
| = genuine era editor addresses | **108** |
| + rows two STALE funnels still stamp `clipper` | **+12** |
| = **120** ✔ | |

**Proved with a byte-on-disk control rather than inferred**, and **re-derived independently by me**
against the migration's own backup `master_leads.csv.20260830_212124.bl1445_kind.bak`: row-matching
gives **`clipper` → `meme_page` on 1,490 rows (1,274 with an address) and ZERO other transitions**,
with **72,942 rows paired** and the matcher proved in both directions first. Two instruments, same
numbers exactly.

**The migration is not called an error** — `writer.py:295-299` defines `meme_page` deliberately as
a third audience — so both taxonomies are reported rather than one being picked.

⚠️ **THE LIVE BUG IT EXPOSED, AND IT RUNS THE WRONG WAY.** BL-1445 restamped the **store** and never
updated its **writers**: `meme_finder.py:8838` and `tiktok_finder.py:3792` still hardcode
`"lead_kind": "clipper"`. Master shows a clean break — every curated-page row **≤ 30 Aug is
`meme_page` (1,911, no exceptions)**, every one **≥ 31 Aug is `clipper` (12, no exceptions)** — and
those 12 are routed to the **PRIMARY send file** instead of `MEME_PAGES_BOT_READY.csv`, **the exact
failure `writer.py:1301` was written to prevent.** So **the honest era figure is 108, not 120**: the
bug inflates the clipper count while misrouting the rows it inflates it with.

**The residual 108 is dormancy, not failure.** The editor channel's last master append was
**2026-08-01, 37 days ago**. Its campaigns ran on exactly **8 ledger dates for $1.7774 = 2.78% of
the ledger**, and those 8 dates are precisely the 8 dates era editor addresses landed on. The
10,877 `TIKTOK_FINDER` calls are a different funnel plus roughly 4,200 calls of agent probes.

**The one genuine quality finding, and it is large:** editor pages carry an address at **5.17%
[4.99, 5.36]** (2,757/53,327) against Spotify's **56.02% [55.20, 56.84]** — **10.8×, and the
intervals do not overlap.** Meanwhile `MEME_FINDER` at **$22.08 is 34.53% of all ledger dollars**,
the largest paid campaign, buying the bucket BL-1445 has just declared is *not* clippers.

**Refused and named as refusals:** a $/address for `TIKTOK_FINDER` (the denominator is **ABSENT,
not zero**); adjudicating whether meme pages "are" clippers (his call, not a measurement); and
whether era TikTok calls **merged** rather than appended — `crossdedup` returns that count but
nothing on disk stores it, and there is **no `output/rejections/tiktok.jsonl`** while six other
funnels have one. Throughout, the denominator was **master rows with a non-blank `email`** — never
`delivered`, never `leads`.

---

## 5. What was refused

* **Switching off the two ungated profile-purchase sites.** `email_finder.py:248` feeds the
  **address** route and returns `bioLink`, the one genuinely paid-only TikTok field, worth a
  measured **1 address in 60**. BL-1525's "52 calls, 0 addresses" was measured *inside the funnel*,
  a different population. Killing a paid call that feeds addresses, in a round whose goal is
  addresses, without measuring the cost, is the argument that once took a brain from 18 delivered
  to 0. **Named with `file:line`, left running.**
* **Shipping the repaired wall arm ON.** No stored capture holds page text, so it cannot be scored
  offline. **ABSENT, not zero.**
* **Fixing the six live 1.4-second sites.** They are live, and the rule measured **+1.7 points
  pooled (p=0.227)**.
* **Naming a cause for the two killed runs.** No traceback, no stderr, no exit code. **ABSENT.** I
  am not naming a mechanism I did not measure — this round has already corrected two figures that
  came from exactly that.
* **Padding the sheet to 100 address-bearing pages.** The supply is not there and the funnel says
  so. **A shortfall is reported as a shortfall, never as a zero and never padded.**
* **Reporting a keep rate.** **He has not graded yet.** The sheet is the deliverable; the rate
  belongs to the round that reads his marks.

---

## 6. What I got wrong

### ⚠️ Two numbers I published in BL-1525 are refuted, and this brief inherited both

**"257 pages that already had a grid were ordering a paid grid, which then overwrote the picture
they already had" is 0 of 310, Wilson [0.0, 1.2].** `rec["tiles"]` is **overwritten by the PAID
tile count** inside `capture_one`, so on a finished record `tiles > 0` measures *the purchase that
happened*, not the picture the page already had. I read a post-purchase field as a pre-purchase one
and inverted the direction of time. The cross-tab separates perfectly — paid-OK/`tiles>0` = 257,
paid-failed/`tiles==0` = 53, and `rec.tiles == paid.tiles` on **257/257**. The pre-purchase witness
settles it: `clip` is **empty on 310 of 310** walled records, against a control showing `clip` set
on **2,484 of 2,484** free captures that have tiles. ⚠️ **BL-1525's own in-file comment carries the
same misreading**, so the error is in the repository as well as in the report. **A real bug,
correctly fixed, with a fabricated price tag.**

**"The TikTok profile purchase is now switched OFF" covers ONE OF THREE SITES.** A two-instrument
census found `tiktok_finder.py:935` **OFF**, `email_finder.py:248` **LIVE AND UNGATED** (the string
`buy_profile` appears nowhere in that file; it is called with a real client at `control.py:1787`,
`:2213`, `:2613` and `youtube_finder.py:1523`), and `exemplar_sheet.py:267` **REACHABLE** through a
generated `serve.py`. That is the "count the sites" failure, in my own work, one round after I
catalogued it in someone else's.

### ⚠️ My run was hard-killed and left NOTHING, because the harness held the only copy

The first funded attempt ran for minutes, judged **114 handles with 95 passing**, and was then
**terminated without a traceback, without a FINISHED line, and without executing `finally`.** The
output directory was **empty**: no export, no summary, and the billed-call counter died with the
process.

**The brief warned about exactly this** — three previous edits runs were killed the same way and one
lost 140 paid calls before its meter wrote its report — **and I still wrote a harness that only
flushed its counter at the end.** Routing the wall-clock stop through the funnel's own ceiling was
necessary and not sufficient: it protects against *my* stop, not against being killed. The harness
now checkpoints the counter **every 25 calls**, so a kill costs at most 25 calls of accounting, and
the run is launched **genuinely detached** rather than as a child of the tool shell that killed it.

### The cap refused to spend a cent, and it was right

My first run spent **$0.00** because I clamped **`spend_cap_usd`** — which is the **LIFETIME**
ceiling, at 100.0 with about $63.94 already spent — to $2.50. `effective_run_cap` returns
`min(per-run cap, lifetime cap − everything ever spent)`, so the room was **$0.00** and the run
**refused**. The machinery behaved exactly as designed; the harness conflated two different
numbers. Only the per-run key may be lowered.

### The shipped depth is 1, and I did not notice until the funnel told me

`tiktok_finder.depth` is **1** — one page per tag — while the estimator quotes its own rates at
depth 10. At depth 1 the eight declared edit tags support about **21** addresses; at depth 10, about
**88**. **The funnel printed the shortfall itself** — *"the tags entered support about 88 email(s);
100 were asked for. Add tags or raise depth — the run cannot invent supply"* — which is a better
instrument than anything I brought to it. I raised depth rather than adding tags, because every
walked tag must be declared proven or a bet and the eight that exist already are; adding tags is
his judgement, not mine.

### A shell heredoc silently deleted two class names from my own comment

Fixing the harness through a bash heredoc, **backticks are COMMAND SUBSTITUTION**: two identifiers
were executed as shell commands and replaced with **nothing**, leaving a comment that named neither
class it existed to explain. The code was correct and the reasoning was blank — **the more
dangerous half**, because a wrong comment survives review that a wrong line would not.

### And the instruments needed a third pass before "1 site" could be believed

The wall-detector census looked settled at two instruments and was not:

* the **byte scan** reads bytes on disk, so a backspace written as the ESCAPE `\x08` is invisible
  to it;
* the **AST census** reads source text, so a byte **already collapsed on disk** is invisible to it —
  which is precisely why it never found `page_capture.py:182`, the actual defect.

**Two instruments answering the same narrow question is not corroboration.** A third — an AST scan
of every string literal's *value*, however written, with a planted `"\x08word"` as its positive
control — returned **zero BS/VT/FF values across 650 files**, and the 14 remaining control-byte
sites are all deliberate NULs. Only then did "1 site found, 1 patched" rest on anything.

---

## 7. Money and safety

**Spend: $0.3696 of $3.00**, counted at the wrapper on the client's own counter, never a ledger
delta — `api_client.py` contains no ledger writer at all, so every LamaTok call ever made was
invisible to `spend.json`.

**The cap was proven to bind before the first call** by driving `harvest_run.Budget.reserve`, with
a **funded positive control** so a refusal means something: a $1.00 cap **ALLOWS**, an exhausted cap
refuses, a **$0.00 cap refuses the FIRST call**, a negative cap refuses, every refusal is a raised
`BudgetExceeded` rather than a returned value, and **the meter does not advance on a refusal.**

**Backups** at round start under a path built from one round constant, sha256-verified, with **all
four required controls firing**: an identical copy verifies, a one-byte flip is caught, a LIST body
is read as a body, and — the one that makes the rest meaningful — **a planted deletion that leaves
the natural key set IDENTICAL is invisible to a key-set check and IS caught by the index-qualified
row hash.** 8 files: `config.json`, `spend.json` (30,081 rows in the `runs` LIST), `master_leads.csv`,
and all five seen stores (2,193 / 6,196 / 2,518 / 1,930 / 4,146), **body found by shape**.

**No dashboard was listening** in the dashboard port range at round start, read from the
**listening-port table** — never a command-line grep, which once matched its own command line, and
never `dashboard/.running.json`, a stale marker since 30 August. Every agent re-checked immediately
before each write under `clippershq/`. **No Python process was killed.**

⚠️ **NOTHING SHARED WAS MUTATED TO RUN THE EDITS BRAIN.** `config.json` is read by concurrent
sessions, so the mode was selected through `CLIPPERSHQ_MODE` — whose provenance the resolver
reports back as *"CLIPPERSHQ_MODE in the environment"* — and the target, depth and per-run cap were
overridden **in memory**, because `run_funnel` takes the config as a parameter. The file was never
written.

**Deliberately not committed, and neither is an orphan.**

* **The browser screenshot** (`scratch/bl1526_agentS_shot_redacted.png`). It is redacted with
  black boxes rather than blur, and it is **still withheld** — ⚠️ **the handle detector has a known
  false negative on alpha-blended watermarks, so it CANNOT PROVE a sheet clean**, and a previous
  round withheld images for exactly this reason. The console output, the 24 passing assertions and
  the marks read back off disk are all reported in text instead. **An image I cannot prove clean
  does not get published because it would have been convenient.**
* **`clippershq/api_client.py`**, which is modified in the working tree and **belongs to another
  round** — its added lines carry BL-1221 and BL-1469 markers, not mine. I listed it in my claim's
  write-set at round start and should not have; claiming a file I did not touch is how a round
  blocks a peer. **Left exactly as found.**
* **Everything under `output/`** — the run's own artefacts, the 577 handle-named PNGs and the
  built sheet. `output/` is gitignored (`.gitignore:98`) and it holds real creator handles and one
  real address.

**The claim was released with `--force` for these three reasons, and this sentence is the record of
it** — the next round should not stand off from those paths wondering who owns them.

Paths in this report are relative to the repository root under `%USERPROFILE%`.

---

## 8. What he should do next, ranked

| # | action | why, measured |
|---|---|---|
| 1 | **Migrate the two `lead_kind` writers** — `meme_finder.py:8838`, `tiktok_finder.py:3792` | **9 of 9 addresses this run** were stamped `clipper` and routed to the **primary send file** instead of the meme-pages one. It is misrouting leads today |
| 2 | **Give him more edit tags, or accept ~88** | the funnel prints its own ceiling: the eight declared tags support **~21 at depth 1, ~88 at depth 10**. Tags need his judgement — every walked tag must be declared proven or a bet |
| 3 | **Find out why a long run gets killed** | two funded runs died with no traceback and the funnel **persists nothing until the end**, so a run killed at 95% delivers 0. This is the ceiling on every future run, not just this one |
| 4 | **Decide the two ungated profile buys** (§5) | `email_finder.py:248` is live and returns the only paid-only TikTok field |
| 5 | **Grade the 150 rows** | 33 kept / 95 rejected / 22 unjudged. ⚠️ **Nothing scored against his marks can exceed his own self-agreement: 75.6% overall, 89.2% on obvious pages, and 48.0% [30.0, 66.5] NEAR HIS DECISION LINE** — an interval spanning 50%, on exactly the population the filter sorts. ⚠️ **And the constant-answer baseline is 58.1, 66.1, 56.4 or 59.1 depending on the pool — not one number.** Say which pool before quoting a score |
| 6 | **Then re-ask the keep rate** with a named denominator. At n=33 delivered rows a keep rate carries roughly ±17 points; **~200 graded delivered pages** would put it inside ±7 |
| 7 | **Fix the six live 1.4-second samplers** (§3) | 42.0% of clips sampled before the floor, earliest 0.451 s |

---
