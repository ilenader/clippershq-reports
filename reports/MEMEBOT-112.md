# MEMEBOT-112 — the commentary defect is real, and no stored signal separates it

**One number: 0.700.** That is the precision of the best discriminator I could build,
measured exactly on **all 40** matches it would suppress. My bar was 0.80. **It does not
clear, so nothing ships against defect (a)** — the measurement is the deliverable.

MEMEBOT-111 declined to fix this because a keyword marker was unreliable. That was right,
and this round found the reason it is unreliable, which is not the one anybody assumed.

---

## MY BAR, STATED BEFORE ANY VERDICT WAS FORMED

> Does the **matched phrase** sit in a description of something **happening on screen**
> (ACTION), or of someone **talking** / a **still artefact** (COMMENTARY)?
> The verdict is about the phrase's context, not whether the clip is "actiony" overall.

I adopt **MEMEBOT-111's bar deliberately and unchanged**, because the defect being fixed is
defined by it and a fresh bar would make the fix unmeasurable against the thing it fixes.
Adopting the bar is not adopting the verdicts: **every label here is mine**, formed by
reading each row in this round.

**Positive = COMMENTARY**, and the bar is on **precision** because a false positive
*suppresses a good match* — the clip falls out of the vision tier and parks. Catching half
the commentary is worth having; wrongly parking a fifth of the action clips is not.

### The rate, on a bigger sample

| | |
|---|---:|
| Sample (deterministic, sorted by `clip_id`, every 4th) | **77** of 308 |
| COMMENTARY | **19** |
| ACTION | 58 |
| **Commentary rate** | **24.7%** |

MEMEBOT-111 measured **30.0%** (9/30) under **this same bar**, so the two *are* comparable —
95% Wilson [0.17, 0.35] against [0.17, 0.47], heavily overlapping. **No comparison is made to
56.1% or 68.8%**: BL-1002's own 35.0% strict and 82.5% lenient straddle the published figure,
and comparing across bars is arithmetic dressed as evidence.

---

## 1. PER-SIGNAL PRECISION AND RECALL, WITH n

Against my 77 hand labels. `speech_frac` and `motion` thresholds are **swept over every
observed cut in both directions** rather than hand-picked, and a cut firing on fewer than 3
rows is discarded — a precision of 1.00 on n=2 is not evidence.

| signal | n | flagged | tp | fp | precision | 95% CI | recall |
|---|---:|---:|---:|---:|---:|---|---:|
| `bag` — MEMEBOT-111's marker | 77 | 8 | 5 | 3 | 0.625 | [0.31, 0.86] | 0.263 |
| **`governed`** — speech verb *before* the phrase | 77 | 6 | 5 | 1 | **0.833** | [0.44, 0.97] | 0.263 |
| **`ocr_only`** — phrase in burned-in text only | 77 | 3 | 3 | 0 | **1.000** | [0.44, 1.00] | 0.158 |
| `bag OR ocr_only` | 77 | 11 | 8 | 3 | 0.727 | [0.43, 0.90] | 0.421 |
| **`governed OR ocr_only`** | 77 | 9 | 8 | 1 | **0.889** | [0.56, 0.98] | 0.421 |
| `audio_class` starts with `dialogue` | 70 | 30 | 11 | 19 | 0.367 | [0.22, 0.55] | 0.611 |
| `speech_frac >= 0.842` (best of 37 cuts) | 48 | 6 | 4 | 2 | 0.667 | [0.30, 0.90] | 0.308 |
| `motion <= 24.47` (best of 12 cuts) | 12 | 4 | 3 | 1 | 0.750 | [0.30, 0.95] | 0.750 |

Three clear 0.80 **on the point estimate**. **None clears it at the interval's lower bound**,
which is the honest test at these n.

### Two of the four candidates cannot be discriminators at all

Not because they score badly — because they are **not there**:

| field | on the library | on the 77-row sample |
|---|---:|---:|
| `speech_frac` | 1,859 / 2,728 (68.1%) | 48 / 77 |
| `audio_class` | 2,568 / 2,728 (94.1%) | 70 / 77 |
| **`motion`** | **92 / 2,728 (3.4%)** | 12 / 77 |

`motion` reads the best recall in the table and **cannot be used at any precision**: it is
absent from 96.6% of the library. A signal that is missing is not a weak signal, it is not a
signal, and that is a cheaper finding than tuning its threshold.

**And none of the three is visible to the matcher.** `clip_pipeline.dict_of()` copies exactly
`MATCHER_FIELDS`, which lists none of them — so any fix built on one needs a `MATCHER_FIELDS`
line before the matcher can read it at all.

---

## 2. THE DECIDING MEASUREMENT — precision on **every** flagged row, not a sample

`governed OR ocr_only` read **0.889 on nine flagged rows**. Nine. Shipping on that would be
the exact error this project keeps recording, so I measured the thing the decision actually
depends on: **precision is a property of the flagged set alone**, so labelling *every* row
the rule fires on across all 308 matches measures it with **no sampling error at all**.

| | |
|---|---:|
| Vision-tier matches | 308 |
| Flagged (would be suppressed) | **40** (13.0% of the tier) |
| True positives | 28 |
| **False positives** | **12** |
| **Precision, exact** | **0.700** (95% CI [0.55, 0.82]) |
| Recall (from the random sample — it cannot come from here) | 0.421 |
| **Verdict vs my 0.80 bar** | **DOES NOT CLEAR** |

**The n=9 estimate of 0.889 was luck.** The population truth is 0.700.

**Label consistency: 9 rows overlap the two independent passes, 0 disagreements.** If they
had disagreed, both numbers would be worthless — a bar measured twice differently is not two
measurements — so the check is asserted in code rather than assumed.

### Why `governed` fails, which is a different finding from MEMEBOT-111's

All twelve false positives have one shape. The vision model writes **long run-on descriptions
with almost no sentence punctuation**, so the "carrying sentence" is routinely a 300-character
blob of five clauses. A speech verb *before* the phrase in such a blob does not govern it —
it is an earlier, unrelated clause:

| flagged text | what is actually on screen |
|---|---|
| "an elite is shown **speaking** to a human **soldier**…" | the soldier is shown |
| "a **commentator** stands…while a **soccer player** runs past" | the player runs past |
| "another soldier…**holding** a large machine **gun** **speaks** emphatically" | the gun is held, on camera |
| "'po **says**…' po and shifu are in a stylized **action sequence**" | the sequence is shown |

So position is not the wrong idea. **The sentence boundary it depends on does not exist in
this corpus.** MEMEBOT-111 concluded "a keyword list is unreliable"; the sharper statement is
that *any* variant of this idea — including a better word list — needs a **clause splitter**
first. That is the finding worth carrying forward.

---

## 3. THE SPLIT-SCREEN MISS — fixed at the cause

`_compile_terms` joined a phrase's words with `\s+` **and split the phrase on whitespace**, so
a rule entry matched exactly one spelling of itself.

**Measured in this corpus:** `split screen` on **83** clips, `split-screen` on **28**,
**104 distinct** (7 carry both).

MEMEBOT-111 worked around this by listing *both* spellings in `excludes_any`. That fixes the
term and leaves the cause — **every other multi-word phrase in every rule stayed blind to its
own hyphenated form**. The gap class is now `[\s\-]+`, applied to the split **and** the join
so it works in both directions: an author who writes `split-screen` also matches a corpus
that writes `split screen`. Nobody should have to guess which spelling a model will emit.

| | before | after |
|---|---:|---:|
| clips one `split screen` entry matches | 83 | **104** |
| MEMEBOT-111's duplicate entry | load-bearing | **redundant** |

**Library-wide behaviour change: one clip.** `3747940273235374236_69471547833` now matches
`vision strong:kung-fu -> mood:hype` — the rule says `kung fu`, the corpus wrote `kung-fu`,
and nobody had hand-patched *that* term. That is the whole point: the workaround covered the
case somebody noticed.

`tests/test_song_library_terms.py`, 10 tests, both directions, including the property that
must **not** change — a separator is still **required**, so `splitscreen` does not match — and
a separator-only term must not compile to an empty alternative, which would match everywhere.

---

## 4. THE NAMED CLIP — it is in the class, and the best signal misses it

`3931285888038729468_15165051384` still routes **hype**, on `vision strong:explosion`, and its
carrying sentence is:

> **"reacting to an explosion."**

Against my best discriminator: `governed=False`, `ocr_only=False`. **It is not caught.**

The marker that *would* catch it is the bare `reacting to` — which **MEMEBOT-109 removed** at
MEMEBOT-104's measured **58.3%** precision (24 fires, 10 wrong). I measured what re-adding it
would do today rather than inventing a fifth marker:

| | |
|---|---:|
| clips whose vision text says `reacting to` | 129 |
| of those, currently VISION_RULE-matched | 20 |
| already caught by the **narrowed** forms | **0** |
| so a bare marker would newly park | **20** |

At 58.3% that is roughly **8 wrong parks**. Below my 0.80 bar, so it stays refused. **No fifth
marker was invented.**

---

## 5. FOUR BUCKETS, PER CLIP, SUMMING TO THE LIBRARY

| bucket | count |
|---|---:|
| **KEPT** (state unchanged, *including parked-in-both*) | 2,727 |
| **MOVED** (matched before and after, different mood) | **0** |
| **PARKED** (matched → nothing) | 0 |
| **GAINED** (nothing → matched) | **1** |
| **TOTAL** | **2,728 = the library** ✅ |

`KEPT` means **state unchanged**. Defining it as "matched in both" is what made MEMEBOT-109's
first run fail to sum — the parked-in-both clips fall into no bucket at all. The sum is
asserted in code, not eyeballed. A set difference would have reported `MOVED 0` as "harmless"
while being structurally incapable of seeing a move.

---

## 6. THE FINAL DISTRIBUTION

| | |
|---|---:|
| Clips | 2,728 |
| **Matched** | **458 (16.8%)** |
| **Park** | **83.2%** |

| tier | | mood | |
|---|---:|---|---:|
| VISION_RULE | **309** | hype | 288 |
| TRACK_TITLE_MOOD | 140 | warm | 91 |
| FRANCHISE_MOOD | 9 | melancholy | 68 |
| | | triumphant | 11 |

My **baseline** this round measured 457 matched / VISION 308, against the brief's last-measured
442 / VISION 298. Same bar, later tree — the library and rules moved between rounds. The
delta this round caused is the four buckets above: **+1**.

**`scratch/songs.json` was not edited.** The operator's rules file needed no change: the one
prior proposal I could have applied — MEMEBOT-111's speech-scoped exclusion — is the one this
round **measured and refused**. Recording consent for a change I am declining to make would be
worse than not recording it.

---

## WHAT I GOT WRONG

**I read three stored fields through the wrong door and nearly refuted two candidates on it.**
The first run of `mb112_signals.py` reported `speech_frac`, `motion` and `audio_class` as
**0 / 77 present** and I was one step from reporting that two of the brief's four named
candidates do not exist. They do: 1,859, 92 and 2,568 records respectively. I was reading them
off `clip_pipeline.dict_of()`, which copies only `MATCHER_FIELDS` and drops everything else —
so the zero was real *for the matcher* and wrong as a statement about the data. Caught by
checking the raw record before writing it down.

That is the same boundary this repo has now lost values at repeatedly, and the reason it was
survivable here is that a coverage count of exactly zero on a field the brief called "already
stored" was too clean to believe.

---

## STILL BROKEN, AND WHOSE

| what | whose |
|---|---|
| **Defect (a) is unfixed** — ~25% of vision matches are commentary and no stored signal separates them at 0.80 | open; needs a **clause splitter**, not a better word list |
| `motion` is on 3.4% of the library, so the clearest static-image signal is unusable | open — a backfill would make it testable |
| None of `speech_frac` / `motion` / `audio_class` is in `MATCHER_FIELDS` | open; a one-line change *if* a signal ever earns its place |
| `3931285888038729468_15165051384` still routes hype | open, and deliberately: the only marker that catches it is 58.3% precise |
| MEMEBOT-111's duplicate `split-screen` entry is now redundant | left in place — it is the operator's file and removing it was not proposed |

---

## VERIFICATION

| | |
|---|---|
| **Suite** | **183 of 187 green** (1,579 s, one runner covering both repos). **4 red, all four green on re-run** — see below. |
| **Campaigns** | unchanged — `test_governance_rules.py` 25/25, where rule 3 pins `7a029ee5447cddd8` ≡ `8e02f8d6f6307ae8` |
| **Config** | valid — 161 keys |
| **`scratch/songs.json`** | untouched (`git status --porcelain` clean on it) |
| **Spend** | **$0.00** — no paid calls. Every field read was already on disk. |

### I did not get a single all-green full run, and I am not going to claim one

| red in the run | green alone | what it is |
|---|---|---|
| `test_doc_citations.py` | ✅ | scans operator docs; BL-1025 was editing `docs/FIRST_DAY.md` during the run |
| `test_filelock.py` | ✅ | timing-sensitive — 14.3 s inside the run, 23–31 s alone |
| `test_no_unchecked_stdout.py` | ✅ | scans the tree for unchecked reads |
| `test_paid_call_writes.py` | ✅ | scans the tree for paid-then-silent branches |

Three of the four **scan the working tree** and one is a **timing** test, run against a tree
that five other rounds were writing to — 44 concurrent Python processes at the time. None
touches the matcher. The suites that *do* cover this change — `test_song_library_terms.py`,
`test_song_library.py`, `test_matcher_boundary.py`, `test_song_library_meme_rule.py`,
`test_clip_vision.py`, `test_vision_failure_reason.py`, `test_vision_required_every_tier.py`,
`test_selection_gate_wired.py`, `test_clip_postable.py` — are green individually and in the run.

**A caveat about one of them that is mine.** `test_doc_citations.py` is INFRA-024's guard, and
this round's commit added net **+19 lines at line 317** of `song_library.py`, shifting every
citation below it. `docs/FIRST_DAY.md` cites `place_at_detail` at `song_library.py:1017`. Both
resolve now, but for a window they did not — **my line-shift transiently reddened another
round's doc**, which is exactly the drift that guard was built to catch. It caught it.

Two earlier full-suite attempts had to be abandoned: the first produced no output for 38
minutes and was killed (verified first that **no `bl932_probe_` file was planted** — killing
mid-probe is what leaves a permanent red), the second was killed by the harness after one
suite. Only the third, run with `-u`, completed.
