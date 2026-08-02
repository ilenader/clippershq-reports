# MEMEBOT-110 — the selection gate is LIVE. **Pool 2,061 → 1,723, 338 removed at 16.4%** against BL-988's predicted 16.0%. And the script refusal the renderer has had since MEMEBOT-102 now runs at selection — the fourth time a gate has admitted what the next stage rejects.

**Date:** 2026-08-02 · **Type:** wiring · **Spend:** **$0.00**, zero paid calls
**Wrote:** `clippershq/clip_pipeline.py` (`9df8552`), `tests/test_selection_gate_wired.py`
(`8d5b762`), `scratch/mb110_*`. **Read but never wrote:** `clippershq/clip_postable.py`
(held by BL-1004), `memebot/scraper/edit.py`.

---

## 1. BL-988's three terms are live

They went into **`gate()`**, not into a separate filter, and that choice is the whole reason
this is a small change: **`rank_candidates` calls `gate()` itself**, so a term added there is
honoured by the ranker, by `gate_report`, and by `run_batch`'s `gating` decision-log stage
without any of the three being told about it. A parallel filter would have needed wiring into
all three and would have got two.

Proved through the real `run_batch` with a stub fetcher that raises on any paid call:

```
gating: in=2728  out=1592  dropped=1136  unaccounted=0     calls=0  cost=$0.0000
   non_english_caption                            171
   third_party_watermark                           74
   caption script unrenderable: Katakana           26
   caption script unrenderable: Han                16
   static_non_clip                                 15
   caption script unrenderable: Hangul              8
   caption script unrenderable: Hiragana            2
```

**Every exclusion drops through the decision log with its named reason, and `unaccounted` is
0** — nothing vanishes silently.

---

## 2. The script gate was at RENDER only. Now it is at selection too.

MEMEBOT-102 measured, per glyph against **U+E000**, that CJK / Kana / Hangul / Thai /
Devanagari come out as `.notdef` boxes in **both** shipped faces — and it landed the refusal
in `edit.py:_caption_survives_filter`. That is the **render** side.

Selection never learned it. So a Chinese-captioned clip still paid a re-fetch and ~40 s of
encoding to be refused at the end — and **MEMEBOT-074 shipped two Persian-captioned videos
that rendered as rows of boxes**, because at that point nothing asked the question at all.

This is **MEMEBOT-081's shape a fourth time** — the gate admitting what the next stage
rejects. The other three are duration (BL-958), a blank cover frame, and the audio class.

**The predicate is imported from the renderer, not copied.** `edit.unrenderable_script` is
pure, has no I/O, costs 0.33 s once per process, and is the *same function*
`_caption_survives_filter` refuses on — so the gate and the renderer cannot disagree about
which scripts are drawable, which is the entire point of asking here. Copying it would have
been the treatment-vocabulary mistake again: three copies of one answer, and a guard that
hardcodes what it checks cannot detect drift.

### The marginal value, stated honestly

```
caught by the script term      : 52
of those, NOT also non-English :  3   <- genuinely new refusals, not renames
```

**49 of the 52 would have been refused anyway** as `non_english_caption`. The script term's
independent contribution is **3 clips** — captions mostly Latin with a few CJK characters,
under the 5% non-Latin threshold, which would have rendered with boxes in the middle. The
other 49 gain a *better-named* refusal, not a new one. That is a smaller win than the count
suggests and it is worth saying so.

---

## 3. The gated pool and the top 30

| | clips |
|---|---:|
| library | 2,728 |
| passing the gate **before** these four terms | **2,061** |
| passing **after** | **1,723** |
| removed by the four terms | **338 (16.4%)** |
| BL-988 predicted | 427 of 2,661 (**16.0%**) |

**The rate matches within drift; the absolute does not, and the reason is not drift.** BL-988's
427/2,661 is a **library-wide** figure. These terms apply to the pool that actually reaches
selection, and the pre-existing gate already removes 667 clips before they are consulted
(duration 382, already-rendered 162, no audio class 140, blank cover 117, …). 338 of 2,061 is
the same 16% applied to a smaller base. Quoting "expected ~2,234" against a *pool* would have
been comparing two different denominators.

Drops by reason, primary attribution (as the decision log counts them):

| reason | n | BL-988's library-wide figure |
|---|---:|---:|
| `non_english_caption` | 189 | 289 |
| `third_party_watermark` | 76 | 99 |
| `caption script unrenderable` | 52 | *(not in BL-988)* |
| `static_non_clip` | 21 | 57 |

Co-occurrence is kept rather than lost to the primary-attribution choice — 44 clips trip
script **and** non-English, 5 non-English **and** watermark, 4 trip three terms at once.

### The top 30

```
candidates returned            : 90 (3x over-provision)
distinct accounts in the top 30: 11
  moviezar 10 · cawncept 7 · songss 5 · then eight accounts with 1 each
duration median 19.9s, range 8.0-79.9s
```

**Account concentration got worse, not better.** BL-988 flagged 6 of the top 30 from one page;
it is now **10 of 30 from `moviezar`, and 22 of 30 from just three accounts**. The gate removed
low-quality clips without any per-account cap, so the accounts that survive best now dominate
more. That is handoff item 3 and this round did not touch it — but it is worth knowing that
landing the gate *sharpened* it.

---

## 4. The plants — 7 of 7, each naming the check that fired

```
plant                                    passes  reason(s) the gate gave
clean clip                               True    (none)
static infographic                       False   static_non_clip
third-party watermark                    False   third_party_watermark
CJK caption                              False   caption script unrenderable: Han; non_english_caption
Devanagari caption                       False   caption script unrenderable: Devanagari; non_english_caption
Hangul caption                           False   caption script unrenderable: Hangul; non_english_caption
Cyrillic caption (must NOT trip script)  False   non_english_caption
```

Every plant differs from the clean base in **exactly one field**, so the reason cannot come
from elsewhere in the record.

**The two controls matter more than the three refusals.** A gate that refused *everything*
would satisfy all three refusal plants; the **clean clip** catches that. And a term that
refused every non-ASCII caption would satisfy all three script plants; the **Cyrillic
control** catches that — Montserrat draws Cyrillic, so it must *not* trip the script term,
and it doesn't. It still trips `non_english_caption`, which is also correct.

11 tests in `tests/test_selection_gate_wired.py`, including one that monkeypatches
`clip_postable.classify` and asserts the gate's answer changes with it — **testing the
classifier again would have passed with the wiring removed.**

### Three things only the real path showed

- **The script reason is ordered before `non_english_caption`.** The `gating` stage attributes
  a clip to `bad[0]`, and of the two only the script one is a refusal the renderer will
  repeat — "non-English" is a taste term a future round could switch off; a glyph no font can
  draw is a fact. Naming the weaker reason would send a reader looking for a language policy
  when the answer is a missing font.
- **The reason names the SCRIPT, not the codepoint.** It first read `"Katakana (U+30AB)"`, and
  the gating stage's digit-normaliser — which exists so reasons group — rendered that
  **`"Katakana (UNAN)"`**. Exempting it would have made every codepoint its own bucket.
- **`_SCRIPT_NAMES` was ordered wrong.** The renderer's broad CJK range (0x2E80–0x9FFF)
  *contains* Hiragana (0x3040–0x309F), so a first-match scan named `こ` as **"Han"**. The
  refusal was correct and the diagnosis inside it was wrong — the more expensive half.
  `test_every_renderer_range_has_a_NAME_here` caught it and now fails if the renderer learns
  a range the message map does not.

**The gate fails OPEN.** A raising or missing `clip_postable` returns no reasons rather than
refusing everything: a missing quality filter must cost a worse selection, never an empty
pool. Tested.

---

## 5. Handoffs — noted, not fixed

BL-988's four open items are other rounds'. Two updates from this round:

| # | item | status after this round |
|---|---|---|
| 1 | **OCR coverage** is the binding limit on two of three terms | Unowned, unchanged. Still the highest-leverage unowned item — it would do more than any new rule |
| 2 | **Dead canvas / unreadable footage** — no term, largest surviving defect class | **Now owned: BL-1004**, claimed 22:32:56, adding terms to `clip_postable.py`. I did not write that file |
| 3 | **Account concentration ungated** — 6 of top 30 from one page | **Worse: 10 of 30**, and 22 of 30 from three accounts. Landing the gate sharpened it |
| 4 | **Rule-only drift risk** — every term reads the fields it was validated on | Unchanged, and the script term is the one exception: it reads a *font*, not a model output, so it cannot drift with the vision model |

---

## Verification

| check | result |
|---|---|
| gate live in the pipeline | `run_batch` → `gating` stage, **in 2,728 → out 1,592, unaccounted 0** |
| paid calls | **0** — stub fetcher raises on any call; `calls=0, cost=$0.0000` |
| pool | 2,061 → **1,723**, 338 removed (**16.4%** vs BL-988's 16.0%) |
| plants | **7 of 7**, incl. a clean control that passes and a Cyrillic control that must not trip |
| wiring tests | **11 of 11** green, incl. a monkeypatch proving the gate *asks* `clip_postable` |
| gate consumers | `test_clip_pipeline`, `test_clip_pipeline_gate`, `test_clip_postable`, `test_clip_pipeline_entrypoint` — all green |
| campaigns | **5, unchanged** — ZHUS 216, PANICBABY 1811, STRAENGE 113, DAYLIGHT 95, ANIME15K 5 |
| config | parses, 161 keys, `spend_cap_usd` 50.0 |
| suite | **163 of 166 green** (683.3s, `HEAD=7f6aaf4`, 8–13 rounds in flight) |
| the three red | **none are mine** — see below |

### The three reds, attributed

| suite | standalone, right after | verdict |
|---|---|---|
| `tests/test_clip_pipeline.py` | **OK** | transient — and the one I checked hardest, since I edited that module |
| `tests/test_no_unchecked_stdout.py` | **OK** | transient |
| `tests/test_atomic_io.py` | **FAILS** | **real, and not mine** |

`test_atomic_io` names it exactly: `UNGUARDED clippershq/audit_labels.py:189 os.replace`.
That file is **unheld, committed by another round at 23:09:15 — two minutes before my run
finished** — and appears in neither of my commits. On Windows a bare `os.replace` fails while
another process holds the file open, measured at up to 85% of `master_leads.csv` finalises
(BL-927); the fix is `clippershq/atomic_io.replace`. **Handoff, unowned.**

## Limits and advisories

- **`clippershq/clip_pipeline.py` was taken from BL-899 on the stale-claim advisory.** Its
  claim is ~25 h old with its own files untouched for as long, and the file has been committed
  **four times by other rounds since** (`69f1b6c`, `0e27912`, `49e216e`, `0731766`).
  `git status --porcelain` showed it **clean**. Taken on INFRA-019's precedent, committed with
  `--foreign BL-899` so the override is in the message. **The commit hook refused the first
  attempt** because the two paths spanned two rounds; they were committed separately, which is
  what it was asking for and better history anyway.
- **`clip_postable.py` is held by BL-1004** — claimed 90 seconds after my preconditions read
  it FREE, for the dead-canvas work that is handoff item 2. **I did not write it, only imported
  it.** If BL-1004 adds terms, they appear in this gate automatically, because the gate asks
  `classify()` rather than naming terms.
- **The 16.4% is one library snapshot at one moment**, with 12 rounds in flight and
  `clip_library` itself growing (2,661 → 2,728 since BL-988). The rate is the comparable
  figure, not the count.
- **This round measured no frames.** Whether the surviving 1,723 are *better* to watch is
  MEMEBOT-098/074's question, not this one — the gate's precision figures are BL-988's and are
  inherited, not re-measured here.
- **`static_non_clip` came in at 21 against BL-988's 57**, a larger gap than the other two
  terms. Not chased. It reads `vision_scene`, whose fill has changed with the library, and
  BL-988 itself flags that term as RULE-ONLY with 100% precision "treated as an upper bound".
- **I polluted my own first full-suite run** by editing `clip_pipeline.py` while it executed —
  the same trap as two rounds ago. That run was discarded and re-run on a stable, committed
  tree.
