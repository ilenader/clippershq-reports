# BL-1535 — Every Spotify lead with no email: 5,670 of 13,513

**5,670 Spotify-sourced leads in `master_leads.csv` carry no email address. That is 42.0% of the
13,513 Spotify-sourced rows in the store** (13,513 is itself 18.5% of the 72,971 rows in
`master_leads.csv`). The file is at:

```
%USERPROFILE%\OneDrive\Desktop\spotify_leads_no_email.csv
```

5,670 rows, 78 columns, UTF-8 with a BOM, sorted by Spotify monthly listeners descending —
largest audience first, because the question underneath the request is who is worth chasing.
Nothing was sampled, truncated or capped. **The spreadsheet is not in the repo and is not
published; this report carries counts and shapes only.**

---

## The four counts, with the denominator named

| | count | of what |
|---|---:|---|
| rows in `master_leads.csv` | **72,971** | the denominator |
| rows that are Spotify-sourced | **13,513** | 18.5% of 72,971 |
| of those, carrying an email | **7,843** | 58.0% of 13,513 |
| of those, carrying **no** email | **5,670** | **42.0% of 13,513 — this is the export** |

### How the Spotify rows were identified — and why the obvious column is wrong

**`platform == 'spotify'` matches 2 rows.** Had I trusted it, this round would have published a
two-row spreadsheet and a clean, silent, wrong answer. `platform` records the platform of the
**resolved handle**, not the discovery source: on the Spotify population it reads `instagram`
13,489 times and `tiktok` 22 times.

I censused the distinct values of every one of the 72 columns rather than guessing. Seven columns
carry a Spotify signal, and they do not agree:

| signal | rows |
|---|---:|
| `email_source` begins `spotify:` | **13,513** |
| `qualified_by` begins `spotify:` | 12,763 |
| `spotify_monthly_listeners` non-empty | 12,763 |
| `spotify_followers` non-empty | 12,763 |
| `run_id` begins `spotify`/`BL1288` | 4,065 |
| `platform == 'spotify'` | 2 |
| **union of all signals** | **13,513** |

I used `email_source` — it is the widest, it is stamped by the Spotify funnel itself, and it is a
strict superset of every other signal. **The choice does not move the answer:** the 750 rows that
carry `email_source` and nothing else all have an email (750 of 750), so they are absent from the
export either way. On the narrower 12,763 definition the no-email count is still 5,670.

### The headline re-derived a second way

| method | no-email count |
|---|---:|
| the `email` cell is empty | **5,670** |
| `email_source == 'spotify:none'` | **5,670** |

Cross-tabulated, the two disagree on **zero** rows in **either** direction: 0 rows are
`spotify:none` with an address present, and 0 rows are non-`none` with an address absent.

### The "no email" shapes, censused

The brief is right that "no email" has more than one shape. In this store it turns out to have
exactly **one**. Every value in the `email` column that is not an address is the empty string:

| shape | whole store | Spotify rows |
|---|---:|---:|
| empty string | 59,994 | 5,670 |
| null / `None` | 0 | 0 |
| whitespace-only | 0 | 0 |
| a literal sentinel (`none`, `N/A`, `<absent>`, …) | 0 | 0 |

So a truthiness test and an `is None` test do not disagree here — but that is a **measured**
result, not an assumption. I treated the empty string, and only the empty string, as empty.

### Structurally short addresses — flagged, not moved

**117** of the 7,843 Spotify rows with an email have a local part of two characters or fewer.
**0 of 117 are on free webmail.** These count as **having an email** and are correctly **absent**
from the export. They were not silently moved into it.

### Positive controls

Both directions were proved on a known row before any count was trusted: a row the filter calls
`HAS EMAIL` holds a 20-character value containing an `@`; a row it calls `NO EMAIL` holds the
empty string with `email_source='spotify:none'`. The hash verifier was proved by a corruption
control — one byte flipped in a copy, size unchanged, and sha256 refused it. **The control fired.**

---

## Both stores were checked, and why master won

| | master_leads.csv | the run checkpoint |
|---|---:|---:|
| records | 72,971 rows | **43,717** (folded by key, last-wins; **0 torn** lines) |
| Spotify records | 13,513 | 43,717 (all of it) |
| passed the filter | — | **18,187** |
| **failed** the filter | — | **25,530** |
| with an email | 7,843 | 4,449 |
| without an email | **5,670** | 39,268 (13,738 among passing) |

**I exported from `master_leads.csv`.** He asked for "every single lead that is good, that we have
in our spreadsheet". The checkpoint's 25,530 non-passing records were never leads — 18,134 were
rejected for `low_listeners` alone, plus 4,477 non-target country, 1,676 too many listeners, 510
non-target language, 456 timeouts, 252 unknown listeners, 25 hard errors. Exporting those would
have answered a different question with 30,000 extra rows. The checkpoint is also **one run**
(26 Aug); master spans every Spotify run.

**Overlap:** 10,911 of the checkpoint's 43,261 distinct artist names appear among master's 12,731
distinct Spotify display names. `passed_filter` is a real **boolean** — a truthiness test would
have silently folded its 25,530 `False` values into the same bucket as a missing field.

### One gap, measured and flagged, not chased

**7,390 artists that passed the filter in the 26 Aug run do not appear in `master_leads.csv` at
all** — 7,116 of them had no email in the checkpoint. Separately, **0 rows in master carry that
run's `run_id`**, though 10,561 of its names are present (9,447 Spotify rows have a blank
`run_id`, so most of the run landed unstamped). **This round did not investigate further** — it is
read-only and out of scope. Recording the number so it is not lost.

---

## The question underneath: are these people reachable another way?

Denominator: the **5,670** exported rows, read back off the delivered file.

| | count | share |
|---|---:|---:|
| a handle on another platform | **5,654** | 99.7% |
| a website or external link (`link_in_bio`) | **4,194** | 74.0% |
| a bio on file | **0** | 0.0% |
| both a handle and a link | 4,189 | 73.9% |
| **neither** a handle nor a link | **11** | 0.2% |

Monthly listeners across the export: min 50,009 · median 367,038 · max 5,096,564.

### The bio answer is "fetched but not retained" — not "never fetched"

`bio` is empty on all 5,670. That is **not** the same claim as "no bio was ever fetched", and the
control settles which one is true: **`bio` is also empty on all 7,843 Spotify rows that DID yield
an email** — including the 328 whose `email_source` is literally `spotify:bio-link`. An address
cannot be extracted from a bio that was never read. So the bio **was** fetched during the run and
this store simply does not retain it for the Spotify route; the run checkpoint does not carry it
either. Every row in the spreadsheet says so in its own `bio_status` cell rather than reporting a
measurement that was never taken.

---

## What I got wrong

1. **My first instrument would have returned 2 rows.** `platform == 'spotify'` is the obvious
   filter, the column is named exactly right, and it is wrong by a factor of 6,756. Only a census
   of all 72 columns caught it. This is the third one-word field-name failure on record here.
2. **My discovery script hid the 44 MB store from itself.** I filtered candidate files by
   extension (`.csv/.json/.jsonl/.pkl`); the checkpoint is named
   `spotify.<run>.jsonl.<stamp>.done` and ends in `.done`. My own filter excluded the largest
   Spotify file in the repo. I found it only by reading `run_resume.py` for where checkpoints live.
3. **I first read "bio filled on 0 rows" as "no bio was ever fetched".** That was an inference,
   not a measurement, and the control refuted it. Had it reached the spreadsheet it would have
   told him 5,670 times that a lookup failed when the lookup had in fact succeeded and been
   discarded.

## Safety

Read-only, as required. `master_leads.csv` and the run checkpoint were sha256-hashed before any
read, backed up with the copies hash-verified, and **re-hashed afterwards: both byte-identical,
sizes unchanged.** The corruption control fired. No backup was restored, no production file was
written, no store was modified, no funnel module was touched, and **zero vendor calls were made —
this round spent $0.00.** Routed entirely to local Python scripts; **no sub-agents were spawned.**
The export was written once, read back, and re-counted from the file on disk.
