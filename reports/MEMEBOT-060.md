# MEMEBOT-060 — the join key is fixed at the source, and a fresh render proves it resolves

Budget $0.05; **spent $0.00** by the ledger (one render, 55.5 s wall). Ledger backed up
before any write.

**A fresh render's key now resolves in the store.** That is the only proof that counts — 48
records looked correct and none joined.

---

## THE CLAIM CHECK — a claim with no work behind it

`tools/claims_read.py --holders clippershq/clip_pipeline.py` → **BL-899**.
`git status --porcelain clippershq/clip_pipeline.py` → **empty**.

The file is clean: not staged, not modified, identical to HEAD. Weighing that against the
claim, as instructed:

| evidence | reading |
|---|---|
| BL-899 claim age | **149 min** |
| its last artefact (`bl899_maps.py`, `test_clip_pipeline_gate.py`) | **21:40** — then 2h25m of silence |
| `clip_pipeline.py` worktree state | clean, **identical to HEAD** |
| its recorded pid | `None` — liveness not checkable |
| BL-899's actual fix | already **committed at 23:37** by another round, explicitly to stop it living only in a working tree |

A staged file is stronger than a claim, and there is no staged file. I proceeded and said so
in my own claim. BL-899's work is safe — it is in HEAD, and I did not revert or reformat any
of it.

---

## 1. THE PATH IS NORMALISED AT THE SOURCE

`ledger_song_path()` already existed and was already correct. It was applied to the **wrong
branch**:

```python
"song": (song.get("store_path")            # <-- used verbatim
         or ledger_song_path(song.get("file")) or None)   # <-- only this normalised
```

`store_path` is the value actually used, so an absolute Windows path went straight into the
join key. **MEMEBOT-014's original bug, reported twice, surviving a fix that only ever
covered the fallback.** Now:

```python
"song": ledger_song_path(song.get("store_path") or song.get("file")),
```

`ledger_song_path` is idempotent on an already-relative path, so wrapping the whole
expression costs nothing and closes the open branch.

`tests/test_join_key.py` — **11 tests, green** — including one that reads the record-builder's
source and fails if `store_path` ever bypasses the normaliser again. A fix that covers one
branch of an `or` is exactly what it exists to catch.

---

## 2. A KEY THAT RESOLVES TO NOTHING IS NOW LOUD AT WRITE TIME

`check_joinable()` runs **before `append_record`**, while the run is still on screen:

```
!! this record will NOT join the song store: absolute song path; the store holds a
   repo-relative one; key 'C:/…/song01.mp3@20.0-25.0' matches none of the 21 store key(s).
   The video is fine -- its outcome is recorded but can never earn rotation.
```

**Warns, never blocks.** A clip that cannot join is still a finished video worth keeping, and
refusing to record it would lose the render as well as the evidence. The record now carries
`joinable` and `join_reason`, so the state is a fact in the ledger rather than something a
reader re-derives.

It distinguishes four cases, and one of them is not a mismatch at all:

| condition | reported as |
|---|---|
| key in the store | `joinable: true` — silent |
| absolute path | *"absolute song path; the store holds a repo-relative one"* |
| song absent from the store | *"song is not in the store at all"* |
| song present, window not a marked hook | *"this window is not one of its marked hooks"* |
| **store unreadable** | `joinable: null`, *"join not evaluated"* |

That last row matters: *"no key matched"* and *"there were no keys to match against"* are
different facts, and only the second is a tooling failure. Collapsing them is the same defect
as a scanner passing on zero files.

---

## 3–4. THE HISTORICAL RECORDS — MARKED, NOT BACKFILLED

**All 22 are now `joinable: false` with a reason.** Nothing was invented.

| reason | records |
|---|---:|
| song is not in the store at all (`bl691_audio` corpus tracks) | 17 |
| window is not a marked hook (pre-hand-marking placeholders) | 5 |

### Two corrections to MEMEBOT-059's arithmetic

**"48 records" was 48 ledger LINES — there are 22 distinct records.** `record_id_for()` keys
on the output path, and several lines share one output. 48/22 is a real distinction: the 25
outcomes-per-arm bar counts records, not lines.

**The 7 absolute-path records are not separately recoverable.** Normalising their path yields
`memebot/scratch/song01.mp3@20.0-25.0` — a **placeholder window**. The path was never their
only problem, so the brief's "41 historical records" is really **all 22**, and no backfill of
any kind recovers one of them.

### Why nothing was backfilled

- The corpus-track records name a track **the operator never chose**. Mapping them to a store
  song would fabricate evidence that then counts toward the bar deciding rotation. A wrong
  number in an evidence base is worse than no number, because nothing downstream can tell it
  apart.
- The placeholder-window records are **honestly stale**: the audio actually rendered *was*
  the placeholder window. Re-pointing them at a hand-marked hook would attribute a real
  outcome to a window that was never played.

**The historical 22 are permanently outside the loop.** Only videos rendered after the
hand-marking can ever join.

*I got the annotation wrong once and restored from backup rather than leave it.* My first
pass keyed on `record_id`/`render_id`, which are `None` on most rows, so 29 of 39 annotations
attached to ids nothing else used and created orphan groups. The ledger is append-only, so I
restored the 132-line backup (verified the delta was exactly my own 39 — nothing else had
appended) and redid it with `record_id_for()`. Result: 22 of 22 marked, **0 orphans, 0
unevaluated**.

---

## 5. THE FRESH RENDER — THE KEY RESOLVES

```
TARGET KEY : memebot/scratch/song01.mp3@13.572-28.392

song      : memebot/scratch/song01.mp3
absolute? : False
window    : 13.572-28.392
key       : memebot/scratch/song01.mp3@13.572-28.392
RESOLVES  : YES
joinable  : True   reason=None
```

One render, 55.5 s. The song was named explicitly against a real hand-marked hook — 86.2% of
the library parks, so a plain draw would very likely have produced a songless record and
proved nothing about the key. The key is still built by the production record-writer through
the production normaliser, which is the code path that was broken.

**`joinable: True` is written into the record by the new check** — the loop can now see, from
the ledger alone, which records are eligible.

---

## 6. THE TWO CSV TRAPS (MEMEBOT-059), RECORDED

Any future consumer of the outcome sheet will hit both.

**1. A `#` preamble means line 0 is no longer the header.** `csv.DictReader` takes the first
line it is given as the header, so a naive reader makes `"# CLIPPERSHQ …"` the column names
and imports **nothing while returning 0** — indistinguishable from an empty sheet.
`import_csv` filters comments; any other consumer must too.

**2. `read().splitlines()` destroys any field containing a newline.** A quoted `note`
spanning two lines becomes two malformed rows; the surplus columns land under DictReader's
`None` restkey and writing them back raises `dict contains fields not in fieldnames: None`.
The csv module handles embedded newlines by pulling further lines from its iterator, so a
**filtered generator** preserves that behaviour and pre-splitting cannot.

---

## PROOF

| Required | Result |
|---|---|
| Paths normalised, test on an absolute path | `ledger_song_path` wraps both branches; **11/11** tests, incl. a source check that `store_path` cannot bypass it |
| A non-resolving key warns at write time | `check_joinable` before `append_record`; warns, never blocks; 4 distinguished reasons + "store unreadable" |
| Historical records marked unjoinable with reasons | **22/22**, 0 orphans, 0 unevaluated, nothing backfilled |
| One fresh render whose key resolves | **YES** — `memebot/scratch/song01.mp3@13.572-28.392`, `joinable: True` |
| Suites | **116 of 118 green.** Both reds (`test_claims_manifest`, `test_secrets_guard`) **pass standalone** — live-writer artefacts in a 525 s run with many rounds in flight. `test_join_key` 11/11 and `test_outcome_loop` both green. |
| Campaigns unchanged | `8e02f8d6f6307ae8` (sort_keys) **and** `7a029ee5447cddd8` (compact) — both baselines match |
| config.json | parses, 161 keys, 5 campaigns |
| Budget | $0.05 allowed; ledger delta **$0.0000** |

---

### Method / limits

- BL-899's claim on `clip_pipeline.py` was live but unbacked by any worktree or staged change;
  I proceeded on that evidence and recorded it in my own claim. Its committed work is intact.
- The fresh render names its song explicitly. That proves the KEY path end to end; it does not
  prove the matcher would have picked that song on its own.
- The historical records are annotated, not repaired. They stay in the ledger and stay outside
  the loop by design.
- `check_joinable` is wired at the record-writing site in `run_batch`. Any other caller that
  writes a record directly bypasses it — there is one such site (`append_record` at the
  reconcile path) which writes status transitions, not new join keys.
- One render is one render. It proves the key resolves for a store song with a marked window;
  it does not exercise the corpus-track or placeholder paths, which are covered by unit tests.
