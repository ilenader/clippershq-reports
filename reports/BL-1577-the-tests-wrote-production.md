# BL-1577 — Two writers resolved `config.backups` against the CWD; one resolver fixes both; the five generations were sandbox ledgers and went back anyway

**Round:** BL-1577 · **Small.** · **Spent: $0.00** — `spend.json` sha256 `4edc0802cd…` / 16,043,805
bytes at start and at close, byte-identical; no vendor call. · Paths redacted: `<PROFILE>` is the
user folder, everything else repo-relative.

## The paragraph

**Two writers reached the production `config.backups/`, for one reason:** `main._timestamped_backup`
defaulted to the *relative* name `config.backups` (`main.py:146`) and `control._make_backup`
joined the same relative name (`control.py:414`), and both resolved it against the current
working directory — which the runner sets to the repo root for every suite while sandboxing only
the spend *file*, the log dir and the status dir. So a sandboxed `spend.json` in a temp dir got
its pre-write copy in production (the 5 `spend.json.20260920_*.bak`, from the ledger writers at
`main.py:953` / `:1074`), and `test_dashboard`'s config-save routes put 38 `config_*.json` copies
there through `control._make_backup`. **The fix is GENERAL, one site:** `main.backup_dir_for(path,
backup_dir)` resolves a relative backup directory *beside the file being backed up*, and both
writers now go through it (one call-site edit in `control.py`). Driven: seven suites, including
the two that caused the drift, with `config.backups/` (1,227 → 1,227), `config.json`, `spend.json`
and the spotify seen store sha256-snapshotted around the run — no drift — and a positive control
that shows the checker moving when a write is aimed at a stand-in production directory.
**The five rotated generations were restored** (1,227 → 1,232, copied from the vault under a PID
lock, never overwriting, every copy sha256-verified against BL-1574's manifest) because the
arithmetic on a scratch copy of the directory says the cap evicts nothing newer on the next
write that it would not have evicted anyway — but they are worth saying plainly: **all five are
0.7–2.1 KB sandbox ledgers of one TikTok-finder test fixture (1–4 rows, $0.015 steps), not
production generations, and the production ledger has zero pre-write copies in
`config.backups/` today** because the cap of five has been full of test copies. **Other live
stores the suites can still reach:** every one that is a bare relative name — `master_leads.csv`,
`config.json`, `state.json`, `clip_seen.json`, `review_marks.jsonl`, the seen stores,
`memebot/runs.jsonl` — none is sandboxed by the runner; the proven writer is
`test_funnel_wiring.py` → `spotify_playlists_seen.json`, left as it is (63111d43… unchanged).

## 1. What this project is, for a reader with no context

ClippersHQ finds video editors and delivers their addresses to one operator. Its test runner
gives every suite a throwaway money ledger so a test can never book real spend — and BL-1574
found that the same suites were nonetheless writing copies of *their* throwaway files into the
real `config.backups/`, pushing out real generations. This round finds the path, closes it at one
place, and decides the restore by arithmetic rather than by hope.

## 2. Part 1 — the path that wrote production

**Grep** (`config.backups` / `CONFIG_BACKUP_DIR` / `backup_dir` in code): 4 files in `clippershq/`
and `tools/`; **AST** (every call of `safe_write_json` / `_timestamped_backup` / `_cap_backups`,
`scratch/bl1577/callers.py`): 15 call sites in 5 files — `main.py` 5 (1 explicit dir),
`control.py` 1 (explicit, but relative), `test_bl1460_backup_cap.py` 6, `test_write_point_redaction.py`
2 (no dir), `test_resilience.py` 1. **AST answered the count; grep found the second writer**
(`control._make_backup` calls neither function — it joins `BACKUP_DIR` itself).

| writer | before | what it produced in production | callers |
|---|---|---|---|
| `main._timestamped_backup` | `backup_dir = backup_dir or CONFIG_BACKUP_DIR` (`main.py:146`), relative → CWD | `spend.json.<stamp>.bak` × 5 (2026-09-20 13:39, and the identical set of 2026-09-18 23:46) | `save_config` `:284`, `_record_spend_locked` `:953`, `_record_aux_spend_locked` `:1074` — none passes a dir |
| `control._make_backup` | `os.path.join(BACKUP_DIR, f"config_{stamp}.json")` (`control.py:414`), `BACKUP_DIR = "config.backups"` relative → CWD | `config_<stamp>.json` × 38 | `dashboard/server.py:2382`, `:2765` (the config-save routes `test_dashboard` drives) |

The runner (`tests/run_all.py:150-161`) sets `CLIPPERSHQ_SPEND_FILE`, `CLIPPERSHQ_LOG_DIR` and
`CLIPPERSHQ_STATUS_DIR` — the ledger file, not its backup directory — and runs every suite with
`cwd=ROOT`. Two writers, one cause.

**The fix — GENERAL, 1 site, plus 1 call-site edit:** `main.backup_dir_for(path, backup_dir)`: a
relative backup directory is resolved against `dirname(abspath(path))` — beside the file being
backed up — and an absolute one is used as given. `_timestamped_backup` calls it (covering
`save_config`, both ledger writers and `control._backup_and_save`, which passes the relative
`BACKUP_DIR`); `control._make_backup` calls it for its own name scheme. A sandboxed
`<tmp>/spend.json` now backs up to `<tmp>/config.backups/` by construction; the production
`config.json` and `spend.json` live in the repo root, so their backups land exactly where they
always did. A future writer cannot reach production by adding one line, because the only line
to add is a call to the resolver.

**Driven** (`tests/test_bl1577_backup_dir_sandbox.py`, 8 tests: the resolver's three cases; the
four writers on temp files with the production directory's file count asserted unchanged across
each; a positive control that aims the old behaviour at a stand-in production directory inside
the fixture and asserts the count moves), then the suites that caused the drift, through the
runner's own `run_suite` and sandbox:

```
BEFORE: config.backups 1227 | config 82e65b78b5b1 spotify 63111d43e6fc spend 4edc0802cd59
PASS  4.4s tests/test_bl1577_backup_dir_sandbox.py | OK
FAIL 55.2s tests/test_dashboard.py | FAILED (failures=2, errors=1, skipped=1)   <- the same three as BL-1574's run, pre-existing
PASS  4.6s tests/test_write_point_redaction.py | OK
PASS  3.1s tests/test_bl1460_backup_cap.py | OK
PASS  2.7s tests/test_funnel_filter_editor.py | OK
FAIL  2.1s tests/test_resilience.py | NameError: name 'spend_cap_declared' is not defined   <- BL-1569 baseline
PASS  6.8s tests/test_bl1401_launcher….py | OK
AFTER : config.backups 1227 | config 82e65b78b5b1 spotify 63111d43e6fc spend 4edc0802cd59
```

`test_dashboard` — the suite that produced 38 config copies in BL-1574's run — produced none.
The two reds are the pre-existing ones (identical failure names to BL-1574's captured output).

## 3. Part 2 — the restore, decided on a copy

`_cap_backups` (`main.py:166`; `BACKUP_KEEP = 5` at `:186`): *keep the newest `keep` copies of
`base` in `backup_dir` (by mtime, names starting `base + "."`); delete the rest* — run by
`_timestamped_backup` after every copy it takes.

**The arithmetic, on a scratch copy** (`scratch/bl1577/restore.py decide`; production untouched):
copy the five `spend.json.*` entries now in production plus the five vaulted ones (copy2, so they
keep their 2026-09-18 mtime) into a scratch directory, add one newer copy to stand for the next
production write, run the cap; then the counterfactual without the five.

```
simulated_next_write_evicts: the five 2026-09-18 copies + spend.json.20260920_133915_3.bak
evicted that are newer than the five: [spend.json.20260920_133915_3.bak]
evicted anyway without the restore:   [spend.json.20260920_133915_3.bak]
newer evictions CAUSED by the restore: []        DECISION: NO-EVICTION
```

So: restore. `config.backups/` was first backed up whole to scratch (1,227 files, sha256
manifest); a PID lock was taken (a second `apply` while a holder lived: `REFUSED: restore.lock is
held by live PID 22044. A second writer does not start.`, exit 3); each of the five was copied
from the local vault only if absent, hashed against BL-1574's manifest before and after the
copy. Verdict line:

```
restored 5 of 5 (skipped as already present: []); config.backups/ 1227 -> 1232 files; every copy sha256-verified against BL-1574's manifest
```

**What they are.** Read from the vault: 1,660 / 2,137 / 702 / 1,179 / 1,660 bytes; 3 / 4 / 1 / 2 / 3
ledger rows; `total_spent_usd` 0.045 / 0.06 / 0.015 / 0.03 / 0.045; one campaign label, a test's.
The five now in production from 2026-09-20 13:39 are the same fixture's ledger at the same four
stages. They are test artefacts that the old resolution parked in production, and restoring them
restores nothing of value — the brief's condition was met, so they went back, and this is the
honest description. The consequence that matters: **the 16 MB production ledger has zero
pre-write generations in `config.backups/` today**, because five sandbox copies newer than the
last real one fill the cap; from the next real ledger write onward, only real copies arrive.
`config.backups/` also carries `bl1502_agentB_spend.json.*.bak`, `spend2.json.*` and `spend3.json.*`
— the same defect class from earlier rounds, left where they are.

`spotify_playlists_seen.json` was not touched: sha256 `63111d43…` at close, the one playlist
`test_funnel_wiring.py` added on 2026-09-20 13:43:14 (1,994 → 1,995) recorded as a known,
accepted artefact — removing a seen entry is how a future run re-pays. The Part 1 fix does **not**
cover that writer: `playlist_harvest.DEFAULT_SEEN_PATH` is its own bare relative name.

## 4. Part 3 — what else the suites can reach

Every store the runner does not sandbox is a bare relative name resolved against the CWD, which
is the repo root for every suite. By AST (a store's basename inside a real string literal of a
test) / grep (any mention): `master_leads.csv` 27 / 34 tests, `config.json` 53 / 59,
`memebot/runs.jsonl` 16 / 16, `state.json` 6 / 6, `clip_seen.json` 5 / 8, `review_marks.jsonl`
4 / 5, `meme_pages_seen.json` 2 / 3, `tiktok_pages_seen.json` 2 / 2, `resolve_cache.json` 2 / 2,
`suppress_mx.json` 2 / 2, `repost_seen.json` 1 / 1, `repost_rejections.jsonl` 1 / 1;
`spotify_playlists_seen.json` 0 / 0 by name — it is reached through `playlist_harvest`'s default
(`DEFAULT_SEEN_PATH = "spotify_playlists_seen.json"`, `playlist_harvest.py:59`), the writer that
fired. Reachable is not the same as written; the proven writers are the two fixed here and that
one. The module defaults are the same shape everywhere: `config_defaults.py:193`
`"master_file": "./master_leads.csv"`, `tiktok_finder.py:2812/:4536` `master_csv="master_leads.csv"`,
`meme_finder.py:8857`. Fixed nothing else this round; the general remedy is the same one applied
here — one resolver, beside-the-file or an explicit sandbox root — and it is a round of its own.

## 5. Assertions at close

```
master_leads.csv 74,218 x 75 (sha256 ede73c71… unchanged) · workbook Emails 3,028 rows, MARK non-empty 0
config.json sha256 82e65b78… unchanged · spend.json 4edc0802cd… / 16,043,805 bytes == start of round
spotify_playlists_seen.json 63111d43… unchanged · config.backups/ 1,227 before -> 1,232 after: +5, the restored generations, nothing else
BL-1574 vault re-verified by re-reading and re-hashing:  local  VERDICT: VAULT VERIFIED   ·   D:  VERDICT: VAULT VERIFIED
reports clone: main == origin/main
```

## 6. Fix category and sites, stated

GENERAL: 1 site (`main.backup_dir_for`). Call-site edits: 1 (`control._make_backup`). Suites
run: 7, named above. Broad suite: not run.

## 7. Scope check

One defect (the resolver), one restore (five files), one new suite. The Part 3 stores were named,
not fixed. Nothing grew past the brief.

## 8. What I got wrong

- **I first wrote the AST caller scan through a shell heredoc and it died on a backslash** — the
  trap the brief names, for the third round running. Redone with a file tool before anything
  else happened; the failed attempt changed nothing.
- **I expected the five vaulted generations to be production ledger copies.** They are 0.7–2.1 KB
  test ledgers. The brief's condition (no newer eviction) was still met and they were restored;
  the report says what they are rather than what I assumed.
- **Leak scan of this report:** built from both corpora, every detector proven on planted
  `.invalid` controls; 0 leaks, 0 C0 bytes, asserted before writing.
