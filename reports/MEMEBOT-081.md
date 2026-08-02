# MEMEBOT-081 — the gate now refuses what the renderer refuses, and the boundary clip was decided by rendering it

**Date:** 2026-08-02 · **Class:** Gate term + boundary close + two recorded lessons · **Spend:** **$0.0006** of a **$0.15** budget — one retrieval, because the open question was cheaper to answer than to argue about

Preconditions read before any write: `tools/claims_read.py --holders` per target **and**
`git status --porcelain` with the index and worktree columns read separately. Claimed as
`MEMEBOT-081`, twelve repeated `--write` flags, three advisories accepted and recorded in §0.

---

## 0. THE BRIEF'S SECOND NUMBER IS WRONG, AND IT IS CHECKABLE

> *"151 clips genuinely have no class and 89 lose one to an old rev collision."*

**REFUTED.** The clip library is append-only with `rev`, and `read_all` is last-wins, so a
newer row that omits a field really can bury an older one that has it — the mechanism is
real. It just did not happen here. Walking every raw line and grouping by `clip_id`:

```
clips whose WINNING row has no audio_class : 151
   ...but an EARLIER row does (recoverable):   0
   ...no row anywhere has one (genuine)    : 151
```

The free `declared_class` fallback recovers **none** of them either — 1,852 clips carry a
stored class, and 1,852 have one after the fallback runs. So there is nothing to recover and
exclusion at the gate is the whole fix, not half of it.

---

## 1. NO AUDIO CLASS, NO ADMISSION

`duck.py` refuses a clip whose class is missing rather than guessing `keep` (MEMEBOT-066),
and that refusal is right: guessing loses both ways — on a music-only clip `keep` leaves the
original copyrighted song under the new bed, and on a DASH clip there is nothing to keep so
the file renders **silent**. Both at exit 0, which is how BL-950 got 0 of 25 videos carrying
their song.

A refusal at the renderer still costs a paid re-fetch and ~40 seconds of encoding first, so
the gate now asks the same question — **through the same predicate**:

```
gate: 1,560 admitted before this term -> 1,428 now -> 132 excluded (8.5%)
```

`audio_class_of()` is read by `gate()` **and** by `audio_treatment()`. A gate that decides
admission with its own copy of a rule is a gate that will one day admit what the renderer
rejects; that is the defect this sequence has been unpicking twice already — the duration
floor (BL-958), and now this. `tests/test_gate_audio_class.py` asserts they agree on every
shape, including the two that are not classes at all.

### And a word that ROUTES is not necessarily a word that RENDERS

The first draft of the predicate wrapped `clip_speech.treatment_for()` in a `try/except`, on
the assumption it raises on an unknown word. **It returns `None`.** So `loud-ish` sailed
through as a class until the test written for that case caught it. The predicate now requires
both consumers to accept the word: `treatment_for()` must route it **and** it must be in
`RENDER_AUDIO_CLASSES`, because `render_one` strips a word outside that tuple and edit.py
then falls back to `keep` — the same silent failure, one layer down. All four real classes
satisfy both; if the two lists ever drift apart the clip is gated out rather than rendered
wrong.

### An unknown class no longer produces a treatment word at all

`audio_treatment()` returned `("keep-original", None, "...")`. It now returns
`(None, None, why)`. There is no safe default, so there is no default: the record claims
nothing it cannot back, and the clip never reaches the renderer. The test that pinned the
old contract has now been rewritten three times and each version is recorded in it — v1
asserted `"duck-under"` (a word that rendered as `keep`), v2 `"keep-original"`, v3 asserts
there is no word.

---

## 2. `vision_control_declined` REACHES THE MATCHER

`song_library.vision_suspect()` reads it to decide whether **this row's** vision fields can
be trusted at all: every vision call also asks for the posting date, which is not recoverable
from pixels, so `True` means the model correctly refused an unanswerable question and `False`
means **it answered anyway** and everything else it said about the row is suspect. Dropped at
`dict_of`, it read as `None` on every clip — the "never asked" state — so an honesty signal
that was wired end to end could not fire.

```
dict_of forwards vision_control_declined : True
rows carrying the flag                   : 1,985
values that survive the boundary         : True 199, False 1   (sampled 200)
planted omission is visible to the guard : True
boundary vs HEAD's song_library          : missing []
```

**Resolved by CALLING `dict_of`, never by reading `MATCHER_FIELDS`** — that tuple is the
subject of the test, and a check that reads its own subject cannot fail. The planted omission
removes the field from `MATCHER_FIELDS` and confirms the guard reports it, so the guard is
known to be capable of failing rather than assumed to be.

**BL-972's `EXEMPT` entry went with the fix, not after it.** Their entry recorded the exact
one-line patch and deferred it because `clip_pipeline.py` was held; their own
`test_exempt_cannot_hide_a_field_that_is_actually_passed` fails the moment the field comes
back, so a stale exemption is a lie about the code and had to be removed in the same commit.

---

## 3. THE BOUNDARY CLIP — decided by rendering it

MEMEBOT-073 left this open: the gate reads the **declared** duration, the renderer probes the
**staged** file, and `MIN_DURATION_S` has zero headroom between them. The brief offered two
choices, widen the gate by the measured shortfall or record the loss. Both are guesses about
what the renderer will do; **one retrieval answers it for $0.0006.**

The population had already shrunk — the audio-class term removed one of the two, leaving
**one** clip in `[7.626, 7.725)`:

```
3926658114485360148_47906480774
   declared 7.686s   staged 7.685805s   shortfall -0.0002s
   finished 8.167s   clears the 8.0s floor: True   status: ok
```

**The exposure is zero on this population.** The shortfall on the one clip that matters was
0.0002s — three orders of magnitude below the −0.099s worst case in the 166-record sample
the concern was built from. A worst case is not a distribution, and this is what it cost to
find that out. **The gate is unchanged, and the question is closed rather than parked.**

---

## 4–5. BOTH LESSONS RECORDED, AND THE SWEEP RUN

`docs/TESTING.md` gains rules **17** and **18**.

**17 — verify against what was APPLIED, not what was PLANNED.** `fit_window` widens the
marked hook to cover the clip, so the bed on a 60-second video spans `46.6–107.5s` where the
hook is `46.6–67.0s`. Correlating the finished audio against the hook fails **only on long
clips** — which reads exactly like a real defect with a plausible pattern, and nearly
published *"nine of twenty videos are missing their song"* when the answer was twenty of
twenty. The general form: **if a measurement fails on a subset with a shared property,
suspect the measurement before the subject.**

**18 — a number formatted into a string and tested with `in` is a prefix match.** Decimal
notation is prefix-closed. `scratch/mb081_prefix_sweep.py` is the AST sweep over `tests/`,
`clippershq/` and `tools/`:

| | |
|---|---:|
| candidates found | **6** |
| **real prefix hazards** | **2** |
| right-anchored by a literal (`f"{size:,} bytes"`) | 1 |
| formatting a NAME, not a number | 3 |

Both real ones are fixed to read the value:

- `test_listenbrainz.py` — `f"days={lb.MAX_DAYS}"` also matched `days=900`; now parses the
  query string and compares the integer.
- `test_twitch_finder.py` — `"first: %d" % TWITCH_MAX_FIRST` also matched `first: 1000`, and
  1000 is exactly the value an API maximum drifts to; now matches the whole token and
  compares.

The sweep over-reports by design — it cannot tell whether a `Name` holds a number — so its
output is a list a human triages, not a gate.

---

## 6. NOTED, NOT CHASED

10 of 21 hand-marked windows are unreachable because **0 of 2,003 clips match `triumphant`**
and 3 match `melancholy`. Rotation spreads windows; it cannot spread songs no clip selects.
That is the operator's shopping list.

---

## PROOF

| Required | Result |
|---|---|
| classless clips excluded at the gate | **132 of 1,560 (8.5%)**, through the same predicate the renderer uses; `tests/test_gate_audio_class.py` **11/11** |
| the brief's rev-collision figure | **REFUTED** — 0 of 151 recoverable from an earlier row; the free fallback recovers 0 as well |
| `vision_control_declined` forwarded | yes; **boundary vs HEAD: missing []**; 1,985 rows carry it and the values survive |
| the drop guard fails on a plant | **yes**, and resolved BY CALLING `dict_of`, never by reading `MATCHER_FIELDS` |
| the 2-clip boundary decided | **1 clip left after the gate term; it rendered and cleared the floor.** Exposure zero, gate unchanged |
| both lessons recorded | `docs/TESTING.md` rules **17** and **18** |
| the prefix sweep | 6 candidates, **2 real**, both fixed to compare values |
| suites | **142 of 146 green, 4,940 checks** (1,407s, 9 rounds in flight). Every suite this round touched is green: `test_gate_audio_class` **11/11**, `test_matcher_boundary` 9/9, `test_clip_pipeline` 82/82, `test_clip_pipeline_entrypoint` 32/32, `test_listenbrainz` 13/13, `test_twitch_finder` 83/83. All four reds attributed below; **none is in a file this round changed** |
| campaigns | `8e02f8d6f6307ae8` (sort_keys) **and** `7a029ee5447cddd8` (compact) — both **MATCH** |
| config.json | parses, **161 keys, 5 campaigns** |
| budget | $0.15 allowed; **$0.0006** on this round's own record |

---

## Method / limits

**`track_title` is missing at the boundary in the worktree, and it is not mine.** The
measurement is deliberately taken twice: against `git show HEAD:clippershq/song_library.py`
it is **clean**, and against the live worktree copy `track_title` is missing — a field
another round added minutes ago and has not yet threaded through `dict_of`. Their round, their
close; the boundary test will hold them to it exactly as it held me.

**I edited two files other rounds hold.** `tests/test_matcher_boundary.py` (INFRA-017, which
had written nothing) to remove the `EXEMPT` entry, because BL-972's own test fails while a
stale exemption stands; and `docs/TESTING.md` (MEMEBOT-080, BL-980) to append rules 17 and
18 at the end of the file where they cannot collide with an edit in the body. Both were
committed with `Claim-Override:` on the record and path-limited so the shared index did not
carry anyone else's staged work into my commit. `clippershq/clip_pipeline.py` is still held
by BL-899, stale at **18 hours** with its own files untouched for 18 hours.

**Two fixtures had to grow a field, and that is the second time.** `_clip()` in
`test_clip_pipeline.py` and the `clip()` helper inside `_selftest` both predated this gate
term, so `rank_candidates` returned `[]` and read as a broken RANK rather than a stale
fixture — the same shape BL-899's vision term produced. Both now carry `audio_class` with the
reason written next to it.

**The four red suites, attributed. Two reproduce, two do not.**

| red | verdict |
|---|---|
| `test_caption_fit.py` (37/37 standalone) | load flake, 1,407s run, 9 rounds in flight |
| `test_spotify_serial_fix.py` (22/22 standalone) | load flake, same |
| `test_render_argv.py` | REPRODUCES. `edit.py accepts --force-caption and clip_pipeline neither passes it nor records why not.` The flag exists **only in memebot's uncommitted worktree** — `git show HEAD:scraper/edit.py` has zero occurrences. Wiring it now would commit a caller for a flag that is not committed, which is precisely the shape MEMEBOT-063 recorded (the promise landing ahead of the thing it promises). Left for the round adding the flag |
| `test_track_title_tier.py` | REPRODUCES as *"asserted NOTHING"* — a new suite (MEMEBOT-078) whose subject, the `track_title` tier, is also uncommitted. Their round |

Both real reds are the same situation from two directions: a suite at HEAD measuring a
worktree that several rounds are mid-write in. The test to apply is whether the red
**reproduces** and whether it is **in a file you changed** — neither of these is.

**The exposure figure is a population, not a property.** "Zero" means the one clip in the
band today rendered. A future library with different sources could produce a larger
declared-vs-staged shortfall; what this retires is the specific open item, not the mechanism.
