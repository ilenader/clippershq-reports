# MEMEBOT-026: CI was skipping 637 test functions, and the caption fitter was only one of them

**Date:** 2026-08-01 · **Class:** Fix + audit · **Spend:** **$0.00**, no paid calls.
**Claim:** `MEMEBOT-026`, filed at start, declaring the files and the three conflicts it would route around.
**Files changed:** `tests/run_all.py`, `memebot/scraper/templates.yaml`, and two new files — `tests/test_memebot_config_contract.py`, `docs/CORRECTIONS.md`. Backed up (`*.20260801_17*.mb026.bak`). **No file held by another round was written.**

| | before | after |
|---|---|---|
| suites in CI | 65 | **81** |
| checks | 2,824 | **3,556** |
| tests/ directories searched | 1 | **3** |
| test files in the tree that CI ignored | 15 | **0** |

**Final run: ALL GREEN — 81/81, 3,556 checks, 448.7s.** Campaign hash `8e02f8d6f6307ae8` **MATCH**. Both YAMLs parse.

---

## 1 & 2. The gap was five times bigger than the caption tests

I expected to move 15 caption tests. The sweep found **80 test files, of which 65 ran** — and the 15 outside the runner's path held **637 test functions**:

| directory | files | test fns | in CI before |
|---|---|---|---|
| `tests/` | 65 | — | yes |
| `memebot/meme/tests/` | **10** | **565** | **no** |
| `memebot/scraper/tests/` | 4 | 72 | **no** |
| `scratch/` | 1 | 0 | no (correctly) |

`memebot/meme/` is not dead code — 25 modules, `cli.py` at 74 KB and `ocr.py` at 79 KB, all edited within the last two weeks. Its ten suites had **never once run in CI**, and they cover 565 test functions.

**The cause was one line.** `discover_suites()` was `os.listdir(HERE)` — flat, `tests/` only. It is now a walk that enrols any `test_*.py` under any `tests/` directory, so adding a suite anywhere is enough. `scratch/` is explicitly skipped: a throwaway probe must never be able to turn the suite red.

**Two of the fourteen needed a path, not a fix.** `memebot/meme/tests/test_text.py` and `test_transforms.py` do `from meme.text import ...` and died with `ModuleNotFoundError: No module named 'meme'`. Suites run with `cwd=ROOT` because data paths depend on it, so the runner now supplies the package parent on `PYTHONPATH` instead — for `<root>/<pkg>/<sub>/tests/` that is `<root>/<pkg>`. Both went from import error to 7 and 20 passing tests.

**I trial-ran all fourteen before wiring them,** because enrolling a rotted suite silently would just move the lie. Eleven passed immediately. Two were the path problem above. One — `test_duck.py` — was genuinely red with 8 failures, and it belonged to MEMEBOT-023, which was mid-flight on exactly those files. I left it alone; it landed its fix during my round and now reports **57 checks, green**. Had it still been red at the end I would have wired it anyway and reported the red, because that is the point.

**One honest caveat about a red I caused indirectly.** On the first full run `tests/test_filelock.py` failed at 44.3s; it passes alone in 17.4s and passed at 13.8s on the confirming run. It is a cross-process locking test with timeouts, and **my change grew the suite from 340s to ~450–570s**, which makes a load-sensitive lock test likelier to trip. I did not touch `filelock.py` or its test — but I am not going to call it "just a flake and not mine" when I plausibly increased the odds. If it recurs, the fix is a longer timeout in that test, not a shorter suite.

## 3. Config keys that look live and do nothing

`tests/test_memebot_config_contract.py` is BL-801's AST contract extended to memebot's YAML, which had no equivalent. It walks every leaf key in `config.yaml` and `templates.yaml`, collects every string literal memebot's Python uses as a lookup, and fails on the difference.

**Raw scan: 134 leaf keys, 10 unreferenced. Six of those were my own false positives.**

The vignette keys (`angle_min/max`, `x0_min/max`, `y0_min/max`) are read through a naming convention, not a literal:

```python
v_x0 = _rand_in_range_dict(vig_cfg, "x0", 0.5, rng)   # reads x0_min / x0_max
```

A scan that only looks for literal key strings calls all six dead. The shipped test understands that pattern — a literal `"x0"` licenses `x0_min` and `x0_max`. **I am flagging this because the detector's own blind spot is the same class of bug it exists to catch**, and a contract test that cries wolf gets disabled.

**Four are genuinely dead, hand-verified:**

| key | why it does nothing |
|---|---|
| `edit.templates_path` | `edit.py` resolves templates from the `--templates` flag, default `ROOT/'templates.yaml'`. The key is never consulted. |
| `edit.default_template` | `--template` is `required=True`, so there is no default to supply — and `clip_pipeline.py` hardcodes `DEFAULT_TEMPLATE = "white_frame"`. |
| `ambient_bed.auto_threshold_db` | MEMEBOT-021 replaced the loudness gate with audio-class routing. Survives only inside a comment explaining its own removal. |
| `gainzalgo.caption.max_chars_per_line` | Superseded by the measured auto-fit. Counting characters cannot size proportional type. |

The first three are in `config.yaml`, held by MEMEBOT-023 — I did not edit it. They sit in the test's `KNOWN_DEAD` allowlist, each with a written reason, so the suite is green today and **fails the moment a new dead key appears**. A further test asserts the allowlist itself stays honest: remove a key and the entry must go with it.

The fourth is in `templates.yaml`, which I own, and is now marked dead in place with its reason.

**And the specific regression is pinned:** a test asserts `max_lines=max_lines` is still forwarded to `compute_caption_layout` and still read from the caption block. If it ever goes back to being "informational", CI says so.

## 4. The correction is recorded — `docs/CORRECTIONS.md`

New file, because a report on GitHub is a snapshot and a wrong number needs a current home.

**The clip library is NOT 32% duplicates.** I said that in INFRA-007 and it was a raw row count of an append-only log presented as corruption. What is true: every row carries a `rev` (2,580/2,580); of 558 repeated clip_ids only 3 were byte-identical, and the differing fields were `provenance`, `rev` and the `vision_*` columns; all duplication was within a single shard. And the canonical reader already resolves it — `read_all()` is documented **LAST-WINS by (clip_id, rev)**. **2,003 was the true count and nothing should dedup it.**

The file records how to re-derive it, and the general lesson: **in this repo, rows are not records** — count through `read_all()` or say plainly that you are counting rows. It also notes that INFRA-007's "65/65 green" was true of the runner and false of the tree, with the rule that a suite count should be quoted together with its discovery rule.

## 5 & 6. Both notes recorded in `templates.yaml`, beside the settings they concern

**Hashtag stripping stays,** documented as a deliberate choice with the measurement next to it: median caption across 1,058 library captions is **922 characters**, because the stored caption carries the poster's whole tag block. Fitting that yields a caption that wraps correctly, never overflows, and reads as a wall of `#fyp`. The note says exactly how to undo it.

**The crop/composition trade is noted, not fixed,** on `video.scale_width` where the lever is: cropping the source letterbox took dead black from 48.0% to 11.3%, but the picture is a 655px band instead of 1536px and the white pad grew. `864 → 1080` buys about 25% more picture at the cost of the side margins that make `white_frame` look like itself. Left to you.

---

## Limits

The dead-key scan reasons about `memebot/scraper/*.py` only; a key read from somewhere else in the tree would read as dead, which is why every one of the four was hand-verified against a whole-tree grep before being called dead. **Reference is necessary, not sufficient** — the test cannot catch a key that is read into a variable nobody uses, which is a real remaining class of dead knob.

Enrolling 16 suites raised runtime from 340s to ~450s, and one suite (`test_band.py`) alone takes 100–126s. Nobody has looked at whether the newly-visible `memebot/meme` suites are *good* tests — only that they run and assert. 565 test functions arriving in CI in one commit is a lot of unaudited green.

I did not run a render this round, so the caption and crop behaviour is covered by the tests rather than re-proven on video; MEMEBOT-016 has those frames.
