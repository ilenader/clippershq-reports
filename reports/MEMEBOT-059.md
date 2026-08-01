# MEMEBOT-059 — the loop is wired, the sheet is ready, and not one record joins the store

> **Published as MEMEBOT-059.** The work ran under claim `MEMEBOT-057`, but that report id
> was taken by another round mid-flight. `publish_report.py`'s collision check refused the
> overwrite — correctly, and it is the reason this is not the fifth silent replacement after
> BL-649, BL-675, BL-677 and MEMEBOT-055. MEMEBOT-058 is claimed by a live round, so this
> takes the next genuinely free id.

Registry read with `tools/claims_read.py` **and** `git status --porcelain`: **10 live claims**,
`outcome_loop.py` and `memebot/runs.jsonl` unheld, `clip_pipeline.py` held by BL-899 and
read-only here. One advisory accepted — BL-928 claims `scratch/` broadly; my files are
`scratch/mb057_*`. No paid calls.

**The headline: bias is correctly inert, the export works, and the join key that carries every
future outcome matches the store on 0 of 48 records.** The loop will record faithfully and
learn nothing until that is fixed.

---

## 1. ONE LEDGER, AND outcome_loop READS IT

| | |
|---|---|
| Live ledgers | **1** — `memebot/runs.jsonl` |
| Worktree copies ignored | 5 — `scratch/mb029/tree*`, `mb034`, `mb041`, `mb046h` |
| `clip_pipeline` writes | `memebot/runs.jsonl` (`DEFAULT_RECORD_PATH`) |
| `outcome_loop` reads | the path it is **given** — no module-level constant |

MEMEBOT-017's consolidation held: there is exactly one. The five extra `runs.jsonl` files are
git worktree copies under `scratch/`, the same artefact that turned 4 guard findings into 14
in BL-878 — counting them would report five ledgers where there is one.

`outcome_loop` takes the path as an argument rather than hard-coding it, so "does the reader
read the writer's file" is a property of the **caller**, not of either module. Verified by
calling `OL.load_runs(CP.DEFAULT_RECORD_PATH)` — 132 lines, 48 with an output that exists on
disk.

### Field completeness

**29 of 48** rendered records carry all nine fields the loop needs. Missing:

| field | absent on |
|---|---:|
| `treatment` | 19 records |
| `cost_usd` | 9 records |

Both are older records; `clip_id`, `permalink`, `song`, the hook window, `output` and `ts` are
present on all 48.

---

## 2. THE EXPORT — 64 rows, ready to fill

`export_csv` writes **64 rows** (every video with no outcome yet), columns
`record_id, ts, clip_id, account, song, template, posted_to, posted_at, views, likes,
comments, saves, shares, note`.

→ `scratch/mb057/outcomes_to_fill.csv`

---

## 3. THE JOIN KEY — 0 of 48 match. This is MEMEBOT-014 recurring.

`song_library.bias_map` groups outcomes on `"%s@%s-%s" % (song, start_sec, end_sec)` built
from the **record**; `hook_key` builds the same string from the **store**. Evidence only
accumulates where those agree byte for byte.

| | |
|---|---|
| distinct keys in the store | 21 |
| distinct keys in the records | 14 |
| **matching exactly** | **0** |

Three distinct causes, not one:

| class | records | example |
|---|---:|---|
| **B.** song path absent from the store | **30** | `scratch/bl691_audio/1227570025460968.m4a@18.0-38.0` |
| **C.** window is not a marked hook | **11** | `memebot/scratch/song01.mp3@20.0-25.0` |
| **A.** absolute song path (store is relative) | **7** | `C:\Users\…\clipper finder\memebot\…` |

- **B** — those renders used tracks from the old `bl691_audio` corpus, which is not the song
  store at all. Nothing in the store can ever match them.
- **C** — the path is right; the window is the **old placeholder** (`20.0-25.0`,
  `60.0-65.0`, `110.0-116.0`). The operator has since hand-marked the real windows
  (`13.572-28.392`, `0.427-18.701`, …), so these records point at windows that no longer
  exist.
- **A** — MEMEBOT-014's original bug, still live: the record stores an absolute Windows path
  where the store holds `memebot/scratch/song01.mp3`.

**None of this is lost data** — the outcomes will still be recorded against `record_id`. What
is lost is the *grouping*: every one of these lands in a bucket `bias_map` will never look up.
Only videos rendered **after** the hand-marking, with a store-relative path, will join.

I did not fix it: the key is built in `clip_pipeline.py` (BL-899) and `song_library.py`.

---

## 4. BIAS IS CORRECTLY INERT

| check | result |
|---|---|
| `bias_map(store, runs)` entries | **0** — empty |
| `should_bias([], [])` | `False` — *"need >= 25 per arm; have 0 and 0. Any gap here is noise."* |
| `should_bias(n=3 vs n=3)` | `False` — same reason |
| `MIN_N_PER_ARM` | **25** |

Rotation stays least-used-first. **This is the intended behaviour, not a failure.**

*My first harness called `should_bias(key, bias_map)` and got
`ValueError: could not convert string to float: 'm'` — it takes `(hook_values,
pooled_values)`, and it was iterating the characters of my key string. A harness bug that
would have read as a crash inside `should_bias`.*

---

## 5. THE SHEET NOW STATES WHAT ITS OWN NUMBERS CAN DECIDE

```
# CLIPPERSHQ OUTCOME SHEET -- 64 video(s) awaiting numbers
# Fill in views/likes/comments/saves/shares from the post. Leave a metric BLANK
#   if you do not have it: blank means 'not filled in', 0 means 'zero views',
#   and conflating them poisons every median downstream.
# WHAT THESE NUMBERS CAN DECIDE, honestly:
#   25 outcomes per window is the bar before the loop will bias rotation at all.
#   That bar clears only a LARGE effect. A MEDIUM one needs ~128 posts per arm
#   for a two-arm question. Until then the loop RECORDS; it does not DECIDE.
# Lines starting with # are ignored on import.
record_id,ts,clip_id,account,song,template,…
```

### This changed a contract, and it broke two things before it was right

A `#` preamble means **line 0 is no longer the header**. That cost two separate breakages in
one existing test, and both are worth recording because any future consumer will hit them:

1. **`import_csv` would have imported nothing.** `csv.DictReader` takes the first line it is
   given as the header, so the preamble would have become the column names — returning `0`,
   which reads exactly like *"the operator filled nothing in"*. Fixed on both sides together.
2. **`read().splitlines()` destroyed multi-line fields.** My first skip-the-comments
   implementation split the file into lines, which breaks any quoted `note` containing a
   newline: the surplus columns landed under DictReader's `None` restkey and writing them
   back raised `dict contains fields not in fieldnames: None`. The csv module handles
   embedded newlines by pulling further lines from its iterator, so it now gets a **filtered
   generator**; pre-splitting cannot work.

`tests/test_outcome_loop.py` assumed `rows[0]` was the header in two places. It now *locates*
the header rather than assuming it. Round trip re-verified end to end, including a note
containing a newline. **All three outcome suites green** — `test_outcome_loop`,
`test_outcome_loop_wiring` (8 new tests), `test_outcomes`.

---

## 6. WHAT THE OPERATOR ACTUALLY HAS TO DO

Post the videos, then **once per batch**:

1. Open `scratch/mb057/outcomes_to_fill.csv` in any spreadsheet.
2. Fill `views`, `likes`, `comments`, `saves`, `shares` for the rows you posted.
   **Leave a metric blank if you don't have it** — blank ≠ 0.
3. Save it as CSV.
4. `python -c "import sys; sys.path.insert(0,'clippershq'); import outcome_loop as O;
   print(O.import_csv('scratch/mb057/outcomes_to_fill.csv','memebot/runs.jsonl'))"`

That is the whole manual step. You never edit the ledger, and a row you skip is simply not
recorded rather than recorded as zero.

**And the honest expectation:** at 25 per arm and four songs, the loop needs on the order of
**100 posted videos before it changes a single rotation decision** — and that only if an
effect is large. Until then it is a record, not an advisor.

---

## PROOF

| Required | Result |
|---|---|
| One ledger, outcome_loop reading it | 1 live (`memebot/runs.jsonl`); 5 worktree copies correctly excluded; reader takes the writer's path |
| Ten records exported | **64 rows** exported, all columns present |
| Join keys matching the store | **0 of 48** — three causes, classified |
| Bias inert at n=0 | `bias_map` empty; `should_bias` False at n=0 and n=3; bar = 25 |
| Statistics in the export header | 9-line preamble, round trip re-verified |
| Suites | **107 of 112 green** — see below |
| Campaigns byte-identical | **yes**, and the cited hash explained below |
| config.json | parses, 161 keys, 5 campaigns |

### The campaigns hash — the block is unchanged, the formula moved

The brief cites `7a029ee5447cddd8`; the value every round has verified today is
`8e02f8d6f6307ae8`. **Both are the same campaigns block.**

| serialization | hash |
|---|---|
| `json.dumps(camps, sort_keys=True)` — `gp_verify_config.py` | `8e02f8d6f6307ae8` |
| `json.dumps(camps, sort_keys=True, separators=(',',':'))` | **`7a029ee5447cddd8`** |

Compact separators reproduce the cited value exactly. The five campaigns
(ANIME15K, DAYLIGHT, PANICBABY, STRAENGE, ZHUS) are byte-identical either way — this is a
formula change, not a config change.

### The five red suites — none of them this round's

`test_caps`, `test_clip_pipeline`, `test_secrets_guard`, `test_tools_tracked` all **pass
standalone**; they went red in a 569 s parallel run with **11 rounds in flight**.
`test_config_contract` is genuinely red, on `google_play_max_run_usd` being undocumented —
zero references to `outcome_loop`, and nothing this round touched. None of the three outcome
suites appear in the red list.

---

### Method / limits

- `clip_pipeline.py` was imported and read, never written (held by BL-899).
- The join-key classification is over **48 rendered records**, which is every record whose
  output still exists on disk — not only the most recent ten.
- I checked a prior round's claim that the secret scanner misses planted credentials in the
  `api` and `ig_api` blocks. Against the real credential leaves both are **caught** (exit 1),
  so that alarm does not reproduce here; BL-931 now holds that file.
- The operator's import command is written against `scratch/mb057/outcomes_to_fill.csv`. If
  the sheet is regenerated elsewhere, the path changes; nothing else does.
