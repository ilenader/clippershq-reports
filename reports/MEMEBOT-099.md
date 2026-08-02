# MEMEBOT-099: the duck.py orphan is at HEAD, and the refusal works from a clean clone

**Date:** 2026-08-02 · **Type:** Rescue + verify · **Spend:** **$0.00** (no paid calls) · memebot HEAD `b28f521`, parent `81979e3`

---

## SUMMARY

- **Shipped:** MEMEBOT-066's `AudioClassRequired` refusal committed **unedited** and attributed (`memebot b28f521`, pushed, both blobs confirmed on the remote); two orphaned prose corrections rescued (`parent 81979e3`).
- **The one number:** **178 lines** that existed only on this machine are now at HEAD — and the refusal fires from a `git archive` extract, which is the first time it has been proven to exist outside this working tree.
- **Off-brief:** the sweep found `memebot/scraper/edit.py` mid-edit, but it is **claimed and live** (MEMEBOT-102, written 4 minutes into this round) — not an orphan, left alone.
- **Got wrong:** my first extract harness reported the guard as **not firing while it was firing**, and the classed arm as not rendering when it had. Two harness faults, no code faults.
- **Still broken:** `docs/claims/MEMEBOT-094.claims` is staged (`A `) by another round mid-commit; `memebot/scraper/edit.py` + `test_font_scripts.py` belong to live MEMEBOT-102.
- **Suites:** memebot **242 tests OK** at `b28f521`; parent **159/159 suites, 5,173 checks** at `81979e3`, 3 rounds in flight. Spend $0.00.

---

## 1. What the orphan was

`memebot/scraper/duck.py` carried 98 uncommitted lines and `scraper/tests/test_duck.py` 92 — **178 insertions, 12 deletions** — with **no claim holder**, sitting in the working tree of one machine.

It is MEMEBOT-066's work. `resolve_treatment` had four branches: an operator's `--treatment`, a fixed word in config, a measured `audio_class`, and — when none of those spoke — a **guess** of `keep` with a warning on stderr. The rescued code turns that guess into an exception.

**Why the guess is not survivable, in the words of the round that wrote it.** The two failure directions are not symmetric:

- guess `keep` on a **music-only** clip → the original copyrighted song stays under the new one. Music-only is the *majority* class here (~51.9% BL-853, 80.3% measured locally by MEMEBOT-020).
- guess `keep` on a **DASH rendition** with no audio stream → nothing to keep, and the file ships silent. BL-950 watched 25 finished videos and found **0** carrying their configured song, 12 with no audio at all.

Both outcomes are a healthy-looking mp4 that exits 0.

**Why it mattered that it was uncommitted.** It is live in the render path — `edit.py:2268` calls `duck.resolve_treatment` — so every clean clone has been running *different audio behaviour* than the machine that produced the last several rounds of measurements. Three rounds independently flagged it (MEMEBOT-097, MEMEBOT-098, BL-995) and none owned it. `docs/ORPHAN_RULE.md` records that an orphan of this shape became a live HEAD break within an hour once.

---

## 2. Coherence, checked before committing

| check | result |
|---|---|
| `import duck` | clean |
| `AudioClassRequired` | subclasses `RuntimeError` |
| `REQUIRE_AUDIO_CLASS_DEFAULT` | `True` |
| `require_audio_class({})` | `True` — a missing key cannot weaken the guard |
| `require_audio_class({...: False})` | `False` — the opt-out works |
| reachable from shipping code | `edit.py:2268` → `duck.resolve_treatment` → `raise` at `duck.py:605` |
| memebot suite | **229/229 OK** (matching BL-995's count at the time) |
| `test_duck.py` alone | **67 tests OK** |

The tests are part of the same orphan and cover the refusal, the message naming its own opt-out, an explicit decision never being refused, and a missing config key not weakening the guard.

Committed **unedited**, in its own round id with `Claim-Override: MEMEBOT-066`, matching the precedent MEMEBOT-094 set when it rescued the `_floor_trim_budget` half of the same orphan (`1ee7dc7`). Authorship stays with the round that did the work.

---

## 3. Pushed, and confirmed on the remote by blob

```
scraper/duck.py             remote=e49a44f5dc3a  local=e49a44f5dc3a   match
scraper/tests/test_duck.py  remote=c0326530a8de  local=c0326530a8de   match
```

`fbeb1ec..b28f521  main -> main`.

*(Blob hashes abbreviated to 12 characters on purpose: the report scanner refused the
publish with `credential-shaped literal` on the full 40-character forms, and it is right
to — a long high-entropy hex run is exactly the shape it exists to catch. The prefixes
still verify with `git rev-parse origin/main:scraper/duck.py`.)*

---

## 4. It works from a clean extract — and naming which check fired

`git -C memebot archive HEAD` extracted to a separate tree, `edit.py` invoked **there**, so what runs is what a fresh clone gets. The extract is byte-identical to the worktree modulo line endings (`git archive` normalises to LF).

Two arms, **same source clip, same config**, differing only in `--audio-class`:

| arm | rc | file on disk | names the firing check |
|---|---|---|---|
| `--audio-class music-only` | **0** | **yes** | — |
| no `--audio-class` | **1** | **no** | **yes** |

**The firing check is `duck.py:605`**, and the marker is the string `"Refusing to render"`, which occurs **exactly once** in `duck.py` — at the raise site — and *not* in the opt-out warning path below it, which says "could not be routed" where the refusal says "cannot be routed". So the marker identifies this check and no other failure.

That distinction is the whole point: `edit.py` exits non-zero for a missing font, an unreadable source, a bad filter graph and half a dozen other reasons. A refusal on its own would only have shown that *this clip cannot render*. The classed arm succeeding on the *same* input is what makes it evidence about the guard rather than about the clip.

---

## 5. The orphan sweep

| path | state | verdict |
|---|---|---|
| `memebot/scraper/duck.py` + `tests/test_duck.py` | ` M`, no holder | **rescued** (§1–3) |
| `memebot/scraper/edit.py` | ` M`, **holder MEMEBOT-102** | **left alone** — live round, written 21:37 (4 min into this one) |
| `memebot/scraper/tests/test_font_scripts.py` | `??` | MEMEBOT-102's, untracked, live |
| `docs/CORRECTIONS.md` | ` M`, no holder | **rescued** — MEMEBOT-078's correction of MEMEBOT-077 §7 |
| `scratch/BL-963.md` | ` M`, no holder | **rescued** — already published on origin; local copy was behind |
| `docs/claims/MEMEBOT-094.claims` | **`A ` staged** | **left alone** — a commit is in progress |
| `dashboard/static/runs.json` | ` M` | generated artifact, rewritten every run |
| `scratch/bl864_run.json` | ` M`, mtime 10s ago | **actively being written** |
| `scratch/bl974_extract.json`, `bl986_stamp.json`, `mb075_sweep.json` | ` M` | scratch data from finished rounds |
| `memebot/runs.jsonl` | ` M` | append-only ledger |

Two prose orphans were whole (both end on complete sentences) and were rescued with `Claim-Override: MEMEBOT-078, BL-963`. `scratch/BL-963.md`'s text was verified against `origin/main` first — it is **already published**, so committing it only brings the local copy level with the public record rather than publishing anything new.

**`edit.py` is the one I want to be explicit about.** It was clean when this round started and dirty four minutes later. It is claimed. Committing it would have taken a live round's mid-edit work — exactly the landmine MEMEBOT-094 recorded after committing a test marker into the renderer twice.

---

## 6. What I got wrong

My first extract harness printed:

```
classed   rc=0  file=False  names AudioClassRequired=False
unclassed rc=1  file=False  names AudioClassRequired=False
  and the FIRING CHECK is named : False
```

Both columns were wrong, and both would have led me to report that the rescued guard does not work:

1. **`names AudioClassRequired=False` while the guard was firing.** `edit.py` catches the exception and prints its *message*; the class name never appears in the output. I was grepping for the identifier instead of for anything the code actually emits. Fixed by grepping the raise site's own unique sentence.
2. **`file=False` on an arm that had rendered.** The stdout said `rendered=1 status=ok`. The copied config carries a **top-level** `output_dir` as well as one under `edit:`, and the top-level one wins — so the render wrote into the work directory of the round the config came from. I asserted on a path the render was never going to use.

Neither was a code fault. Both were caught by reading the output instead of the exit code — which is the same discipline the brief asked for and which I had to apply to my own harness first.

---

## 7. Still broken, and whose

| what | where | status |
|---|---|---|
| `edit.py` font-coverage work uncommitted | `memebot/scraper/edit.py` + `test_font_scripts.py` | **MEMEBOT-102, live and claimed** — theirs to land |
| A commit in progress | `docs/claims/MEMEBOT-094.claims` (`A `) | staged by another round; untouched |
| Suite count moved under me | memebot 229 → **242**, parent 154 → **159** | other rounds added suites mid-round; a count is a moment, not a property |

**Both suites green at the rescued HEAD.** memebot 242 tests OK at `b28f521`; parent
159/159 suites / 5,173 checks at `81979e3` in 459.0s, with 3 rounds in flight. The parent
commit touched only two markdown files, so the parent suite is a regression check on the
repo rather than on this change — worth stating so the green is not read as evidence about
the rescue itself. The evidence about the rescue is §4.

---

## Files

- `memebot/scraper/duck.py`, `scraper/tests/test_duck.py` — rescued unedited (`b28f521`, pushed)
- `docs/CORRECTIONS.md`, `scratch/BL-963.md` — prose orphans rescued (`81979e3`)
- `scratch/mb099_extract.py` — the clean-extract two-arm proof
- `scratch/mb099_extract_proof.json` — its recorded result
