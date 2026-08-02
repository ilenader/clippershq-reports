# MEMEBOT-062 — the ledger had eight copies and no backup; and a correction to my own last report

> **Published as MEMEBOT-062.** The work ran under claim `MEMEBOT-061`, but that report id
> was published by another round while this one was in flight. `publish_report.py`'s collision
> check is what makes that visible instead of silent; MEMEBOT-063 is claimed, so this takes
> the next genuinely free id.

Registry read with `tools/claims_read.py --holders` **and** `git status --porcelain`:
`BACKUP_THESE_6_FILES.md` and `memebot/runs.jsonl` both **FREE**; `clip_pipeline.py` still
held by BL-899 and only *called* here, never written. No paid calls.

---

## 0. A CORRECTION TO MEMEBOT-060, FIRST

MEMEBOT-060 reported *"a fresh render proves it resolves"*. **The render failed.** It exited
`rc=1` at `edit.py` and produced no video file; what was written was a `failed:render`
record carrying the correct key.

That distinction is the whole point of the round that preceded it, so it should not have been
blurred:

| what was actually proven | what was claimed |
|---|---|
| the **record's** join key is built correctly, normalised, and resolves in the store | *"a fresh render whose key resolves"* |

The join-key fix is real and is now proven twice. **No end-to-end video with a joinable record
exists**, because every render is currently failing at `edit.py` on audio treatment
(`audio_treat keep (routed on class dialogue-only)`, `rc=1`) — a separate, live problem in a
file this round does not hold.

I would rather flag this than let a second report inherit it.

---

## 1. THE LEDGER'S STATUS — the decision was already made, and it was not being honoured

**Three corrections to the brief's premise, all in the same direction: the paperwork was
further along than stated, and the protection was further behind.**

- The backup list has **nine** entries, not eight.
- **`memebot/runs.jsonl` is already entry 8**, added by BL-888, and is already in the copy
  script's file loop.
- `memebot/.gitignore:52` carried the deliberate rationale: *"the render LEDGER — data, and
  entry 8 on the backup list."*

So the decision existed. It rested on one thing: **the copy script being run.**

### It never has been

```
E:\clippershq-backup   absent
D:\clippershq-backup   absent
F:\clippershq-backup   absent
```

And every copy of the ledger on this machine is on the same device:

| copy | bytes | device |
|---|---:|---|
| `memebot/runs.jsonl` (live) | 471,412 | **C:** |
| `scratch/mb060/runs.jsonl.pre_mb060.bak` | 435,494 | **C:** |
| `scratch/mb046h/tree/memebot/runs.jsonl` | 175,608 | **C:** |
| 4 × worktree copies under `scratch/` | 58,219 each | **C:** |
| `scratch/memebot017_backup/runs.jsonl.bak` | 8,175 | **C:** |

**Eight copies, one device.** They die in the same event — exactly what
`BACKUP_THESE_6_FILES.md` already says about `backups/`.

> Count of copies is not redundancy. Count of **devices** is.

That answers item 2 directly: the `mb060` backup is **not** the only copy, and that fact is
worth nothing, because none of the eight would survive the event they exist for.

### So it is now committed to memebot's own remote

`memebot@fecc21f`, pushed. That is the only off-disk copy that currently exists.

| | |
|---|---|
| cost | 471 KB of JSONL → **25 KB** compressed, against a 7.4 MB `.git` |
| growth | ~400 bytes per rendered video |
| what it buys beyond a copy | **history** — MEMEBOT-060's 22 `joinable`/`join_reason` annotations could not be committed at all, so *"when did this record become unjoinable"* had no answer |

**It stays on the backup list.** Git is a second *device*, not a backup strategy: the copy
script is still the only thing that survives losing the GitHub account as well as the disk.

### The list's own figure was 8× stale

Entry 8 read **57 KB**; the file is **460 KB**. It grew from 8 KB to 471 KB in eight hours on
2026-08-01. A size in a backup list ages even when the entry is correct — the table now says
so.

---

## 2. THE JOIN HOLDS ON A SECOND RENDER — on a different window

MEMEBOT-060 used `hooks[0]`. This used **`hooks[1]`**, deliberately: re-proving the same key
would only show the first result was repeatable, not that the normaliser works for a window it
has not seen.

```
TARGET KEY : memebot/scratch/song01.mp3@0.427-18.701

song      : memebot/scratch/song01.mp3
absolute? : False
window    : 0.427-18.701
key       : memebot/scratch/song01.mp3@0.427-18.701
RESOLVES  : YES
joinable  : True   reason=None
```

**12 of 12 records across both rounds carry `joinable: True`** with a relative path and a
hand-marked window. One resolving key proved the fix; two different windows prove it is not
the first one's luck.

With the honest caveat from §0 attached: these are **records**, not shipped videos.

---

## 3. THE ARITHMETIC CORRECTION, RE-CONFIRMED

Re-measured this round, on the live ledger:

```
ledger LINES with an output : 48
distinct RECORDS            : 22
joinable = False            : 22
joinable = True             :  0   (of the historical set)
```

**48 ledger lines are 22 distinct records**, because `record_id_for()` keys on the output path
and several lines share one. **The 25-outcomes-per-arm bar counts records.** Any figure
quoting 48 is counting the wrong unit — including MEMEBOT-059, which introduced it.

---

## 4. THE RECOVERY FINDING, CARRIED

The 7 absolute-path records are **not separately recoverable**. Normalising their path yields
`memebot/scratch/song01.mp3@20.0-25.0` — a **placeholder window**. The path was never their
only problem.

**All 22 historical records are permanently unjoinable and no backfill recovers any of them.**
Both remaining causes are refusals on principle, not gaps:

- the corpus-track records name a song **the operator never chose** — mapping them would
  fabricate evidence that then counts toward the bar deciding rotation;
- the placeholder-window records are **honestly stale** — the audio actually rendered *was*
  the placeholder window, so re-pointing them would attribute a real outcome to a window
  nobody heard.

---

## PROOF

| Required | Result |
|---|---|
| Ledger status decided, committed **or** in the backup list | **both** — committed to memebot's remote (`fecc21f`) *and* kept as entry 8 |
| The `mb060` backup is not the only copy | correct — **8 copies**, and all 8 on `C:`, so the count is worth nothing |
| `backups/` is same-session undo, not DR | already documented; the same test applied to the ledger and it failed the same way |
| A second fresh render joining | **YES** — `…song01.mp3@0.427-18.701`, `joinable: True`, a *different* window |
| 48 lines = 22 records | re-confirmed on the live ledger |
| 7 absolute-path records unrecoverable | re-confirmed — they normalise to a placeholder window |
| Suites | **ALL GREEN — 118/118 suites, 4,370 checks** (463 s) |
| Campaigns unchanged | `8e02f8d6f6307ae8` (sort_keys) **and** `7a029ee5447cddd8` (compact) — both match |
| config.json | parses, 161 keys, 5 campaigns |

---

### Method / limits

- `clip_pipeline.py` was imported and called, never written — BL-899 still holds it.
- **Neither render produced a video.** Both exited `rc=1` at `edit.py` on audio treatment.
  What is proven is the record-writing path, which is where the join key is built; the render
  failure is in `memebot/scraper/edit.py` and belongs to whichever round holds it.
- The off-disk check probes `E:`, `D:` and `F:` for `clippershq-backup`. A copy made to a
  different path or a NAS would not be seen — the finding is "no copy at the documented
  destinations", not a proof that none exists anywhere.
- Committing the ledger makes GitHub a second device. It is not a substitute for the copy
  script, and the doc now says so rather than implying the problem is closed.
- The ledger is now tracked, so every future render dirties it in `git status`. That is the
  intended cost and worth naming: a noisy status is cheaper than an unrecoverable evidence
  base.
