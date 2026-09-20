# BL-1576 — The code has a second copy now; the remote is private but the history is dirty, so do not push

**Round:** BL-1576 · **Spent: $0.00** — `spend.json` sha256 `4edc0802cd…` / 16,043,805 bytes at
start and at close, byte-identical; no vendor call. · **Nothing pushed.** · One code change (the
three pruners + their test), driven on a synthetic tree, dry against the disk, **nothing moved**.
· Paths redacted: `<PROFILE>` is the user folder, everything else repo-relative. The 581 sheet
is not committed and not published.

## The paragraph

**His code has a second copy: a `git bundle` of all 10 refs (816.4 MB, every reachable object,
HEAD `efa706e9`) plus the 734 tracked files of `clippershq/`, `tools/`, `tests/` and
`dashboard/`, 834.8 MB in all, added as the label `bl1576_code` beside BL-1574's labels in
BOTH vault roots — the local NTFS vault outside OneDrive and the USB stick — verified on both by
re-reading and re-hashing every copy (0 mismatches, 0 missing), by `git bundle verify` (exit 0),
and by cloning the bundle to a temp dir and asserting its HEAD equals the manifest's (14,549
tracked files in the clone). BL-1574's vault re-verified untouched. D: has 13,606 MB free.**
**The remote is PRIVATE by three independent signals** (unauthenticated web 404,
unauthenticated API 404 against a public-repo control that answers 200/`private: false`, and the
authenticated API `isPrivate: true`) — **but the unpushed history is dirty**: 7,777 blobs scanned,
and real corpus addresses sit in 7 blob versions (5 of them `clippershq/writer.py`'s own
docstring), real handles in 971 files (257 outside `scratch/`, including shipped modules), his
user folder in 843. **Recommendation: (c) — do not push; the bundle in the vault is the second
copy.** The three pruners are fixed and driven — `outputs_gc` can see `output/`, `backup_prune`
scans `backups/`, `scratch_gc` quarantines outside the repo and only derived files — and on the
real disk today they would move **0.34 GB** (BL-1574 already took the 54 GB; the value is that
the next 40 GB never accumulates). **The 581 never-delivered addresses are on his Desktop as
`BL-1576_never_delivered_581.xlsx`**, source file and capture date in columns, craft-KEEP first.
Master 74,218 × 75, the workbook 3,028 / MARK 0 and `spend.json` are unchanged.

## 1. What this project is, for a reader with no context

ClippersHQ finds video editors on TikTok and Instagram and delivers their addresses to one
operator. BL-1575 found the project's source code existed in exactly one place: one NVMe, 686
commits ahead of a remote nobody had pushed to since July, with a scheduled daily off-device backup
that has never succeeded. BL-1574 vaulted the data; this round vaults the code, decides whether
the push is safe by evidence, fixes the three retention rules that let 70 GB accumulate, and
hands over the 581 addresses BL-1575 found sitting unused in files the project already owns.

## 2. Part 1 — the code vault

`scratch/bl1576/vault_code.py build` ran under a PID lock (`copy.lock`); a second instance
started while the holder lived answered `REFUSED: copy.lock is held by live PID 3552 … A second
copier does not start.` (exit 3) and the lock vanished when the holder exited.

| | |
|---|---|
| bundle | `repo.bundle`, `git bundle create --all`: 10 refs, 816.4 MB, 11 s |
| tree | 734 tracked files of `clippershq/`, `tools/`, `tests/`, `dashboard/` (from `git ls-files`, so nothing gitignored) |
| total added | **735 files, 834.8 MB** per root; own manifest `bl1576_code_manifest.json` (path, size, sha256, HEAD, refs) |
| local root | `<PROFILE>/AppData/Local/ClippersHQ/vault_bl1574/bl1576_code/` — added beside BL-1574's 22 labels; theirs untouched |
| USB root | `D:/clippershq_vault_bl1574/bl1576_code/` — FAT32, largest file 816.4 MB (< 4 GiB); **13,606 MB free after** |

Verification, both roots, verdict lines quoted:

```
VERIFY <local>/bl1576_code: 735 copies re-read, 834.8 MB, sha256 mismatches 0, missing 0
git bundle verify: exit 0 -- The bundle uses this hash algorithm: sha1
clone of the bundle: HEAD efa706e98be6 == manifest efa706e98be6: True; 14549 tracked files in the clone
positive control: planted absent path reported missing = 1 of 1; planted wrong hash reported mismatch = 1 of 1 -> OK
VERDICT: CODE VAULT VERIFIED
VERIFY D:/clippershq_vault_bl1574/bl1576_code: 735 copies re-read, 834.8 MB, sha256 mismatches 0, missing 0
… VERDICT: CODE VAULT VERIFIED
```

BL-1574's vault on D: re-verified afterwards: `VERDICT: VAULT VERIFIED`. What the bundle carries
that the file copy does not: the history — every commit, including the 6,750 scratch files the
tree copy deliberately leaves out. Scratch is therefore protected in the bundle, not as files.

## 3. Part 2 — the push decision (evidence; nothing pushed)

**Visibility.** Three signals, all agreeing, high confidence:

| signal | project remote | control (the public reports repo) |
|---|---|---|
| unauthenticated `GET github.com/<owner>/<repo>` | **404** | 200 |
| unauthenticated API `GET /repos/<owner>/<repo>` | **404 "Not Found"** | `"private": false` |
| authenticated `gh repo view --json isPrivate` | **`PRIVATE`, `isPrivate: true`** | — |

**The scan of the history, not the tree** (`scratch/bl1576/history_scan.py`): every object in
`origin/<branch>..HEAD` — 9,951 objects, **7,777 distinct blobs** (7,213 text, 564 binary
skipped) — read with `git cat-file` and scanned once. Detectors built from both corpora (15,639
addresses, 77,167 handles) with a vocabulary of 10,653 tokens (any word in ≥5 published
reports) to keep ordinary words from reading as handles. Positive control (planted `.invalid`
address, planted handle, 40-hex, user folder, host:port) fired 5 of 5; negative control 0 of 5.

| top-level | files | ADDR | HANDLE | USERPATH | KEYLIT | HOSTPORT |
|---|---|---|---|---|---|---|
| scratch | 6,529 | 2 | 848 | 811 | 2,465 | 31 |
| reports | 208 | 0 | 57 | 28 | 84 | 6 |
| tests | 164 | 0 | 14 | 2 | 162 | 0 |
| clippershq | 97 | **1** | 34 | 0 | 72 | 0 |
| docs | 68 | 0 | 8 | 0 | 54 | 1 |
| tools | 23 | 0 | 3 | 2 | 11 | 0 |
| dashboard | 7 | 0 | 2 | 0 | 4 | 0 |
| ground_truth + 9 root files | 11 | 0 | 5 | 0 | 5 | 0 |
| **total** | **7,107** | **3** | **971** | **843** | **2,857** | **38** |

Adjudicated without printing a token: the ADDR hits are `clippershq/writer.py` (a real corpus
address in its docstring, present in 5 historical versions of the file — the same docstring
that once matched the lead corpus when copied into a control) and two scratch data files (6
hits). HANDLE hits outside `scratch/` are 257 files — shipped modules such as `free_judge.py`
(12 tokens; it names his own pack pages), `crawl_suggested.py`, `edits_rubric.py`, tests and
reports — real handles as string literals. KEYLIT (≥32-char opaque or 40-hex) is dominated by
sha256/sha1 strings in reports and scratch; it was not adjudicated further because the
address and handle classes already decide the outcome. USERPATH: 843 files carry the user
folder, as BL-1573 found 1,465 tracked files do.

**Three options, with the trade-off:**

- **(a) push as-is** — only if private **and** clean. Private: yes. Clean: **no** — the history
  carries corpus addresses and handles in `scratch/` and in shipped code. Not recommended.
- **(b) push code but not scratch** — would need a history rewrite, not a `.gitignore`:
  `scratch/` is already committed in 686 commits, so excluding it means `git filter-repo
  --path scratch --invert-paths` (or a fresh orphan branch) and a force-push, and even then
  `writer.py`'s docstring and `free_judge.py`'s literals go up. Still unprotected afterwards:
  the addresses in code history, and a rewritten history that no longer matches the remote's
  existing 3ad2e752.
- **(c) do not push; rely on the vault bundle** — costs him: no off-site copy (the bundle is on
  two local devices, one of them a stick that leaves the house), no remote to clone from on a
  new machine without the stick, and a remote that stays 686 commits stale.

**Recommendation: (c).** The rule was fixed in advance — a dirty scan means (c) — and the scan
is dirty. The code is protected by the bundle on two devices as of this round; the push waits
for a scrub of the history, which is a round of its own.

## 4. Part 3 — retention, the one code change

| pruner | the defect (file:line, before) | the rule (after) | category / sites |
|---|---|---|---|
| `tools/outputs_gc.py` | `plan()` listed only `n.startswith(PREFIX)` at the repo root; `PREFIX = "outputs_"` cannot match `output/` | `plan_output()` (folded into `plan()`): every CHILD of `output/` is a workspace; skipped whole when its name is in `OUTPUT_AST_READ` (the 39 children a `.py` names in a real string literal, from BL-1573's AST table), when a live claim names it, or when it is younger than `--hours`; only `classify() == 'derived'` moves; records, tracked files and `never_touch()` paths stay; loose files in `output/` are never listed. Plus `--expire`: the age rule that empties the quarantine — derived files of batches older than `--purge-days` whose manifest is in HEAD, per file, never a record | LOCAL, 1 site (`plan`) + 1 new command |
| `tools/backup_prune.py` | `plan()` is `os.listdir(root)` and `NAME_RE` matches only `master_leads.csv.<stamp>…bak`; `backups/` and `backups_bl*/` were never scanned (`:106`) | `plan_backups_dir()` + `--backups-dir`: junction-safe walk of `backups/` and `backups_bl*/`, grouped by basename; the NEWEST generation per store and EVERY config generation are kept; older generations are MOVED to the quarantine through `outputs_gc.do_apply` (manifest first), never deleted here | LOCAL, 1 site |
| `tools/scratch_gc.py` | data moved to `<repo>/quarantine/<batch>/` — inside OneDrive (`:104`) — whole directories, records included, and `:77` promised never to empty it | `quarantine_dest()` = `outputs_gc.default_dest()` (outside OneDrive; manifests stay in `quarantine/` so `--restore` still works, and it now reads the destination from the manifest header); `movable_files()` lists only derived files, so **every record file stays in place by construction**; a directory left empty is `rmdir`'d, which refuses a non-empty one | LOCAL, 1 site |
| by construction, all three | — | `classify()` names json/jsonl/csv/xlsx/md/txt/html as `record` explicitly; `never_touch()` refuses the render root the dashboard serves, both vault roots, and any name starting with `config` | GENERAL, 1 site (`outputs_gc`), consulted by all three |

**Driven on a synthetic tree** — `tests/test_bl1576_retention.py`, 13 tests, each rule paired
with a positive control (a records-only fixture must plan 0, then a planted png must be
listed, or the rule is dead, not quiet):

```
PASS  3.9s tests/test_bl1576_retention.py | OK
PASS  3.8s tests/test_outputs_gc.py | OK
PASS 46.1s tests/test_scratch_gc.py | (fixture updated: a derived .png, and the data destination pointed at the fixture)
PASS  0.3s tests/test_bl1308_scratch_quarantine.py | OK      (no rmtree; manifest before move; MANIFEST_DIR unchanged)
PASS  0.8s tests/test_bl1316_quarantine_excluded.py | 10 check(s), 0 failed
PASS  1.4s tests/test_bl1460_backup_cap.py | OK
```

Six suites, named, run through `run_all.run_suite` with its ledger sandbox; `config.backups/`
(1,227 files), `config.json` and `spotify_playlists_seen.json` sha256-snapshotted before and
after: **no drift**. `test_atomic_io` and `test_silent_zero_shape` were also run because they
scan `tools/`: both red in BL-1569's baseline, and the sites they name (`proxy_pool.py:290`,
`free_judge.py`, `meme_finder.py`, `mark_reader.py`, `main.py:217`) are not this round's. One
side effect of the first suite pass, before the fixture pointed the destination at the temp
dir: `test_scratch_gc`'s apply test created one **empty** batch directory in the real
quarantine (0 files); removed, and the fixture fixed so it cannot recur.

**Dry against the real disk, moving nothing:**

| pruner | would move today |
|---|---|
| `outputs_gc` (`output/` rule) | 25 files, 469 KB — `output/` is 30,823 files / 16.71 GB now, of which 28,782 files are AST-read children and 1,901 are records; BL-1574 already took the renders |
| `outputs_gc --expire` | 0 B — the outputs_gc batch's destination is gone (BL-1574), and the two scratch_gc batches of 2026-08-16 have manifests **not in HEAD** |
| `backup_prune --backups-dir` | 0 files of 281 (1.20 GB) — exactly the newest-per-store + config set BL-1574 left |
| `scratch_gc` | 80 directories qualify, 0.72 GB, **0.34 GB derived would move; records stay** |
| **total** | **≈ 0.34 GB** |

The zeros have controls: the synthetic tree's planted files fired for every rule.

## 5. Part 4 — the 581

`scratch/bl1576/deliver_581.py` re-derives BL-1575's union with the same key and collision
rule (a bio-less sighting may be replaced by a later one with a bio — 3 rows depend on it),
keeps only addressable accounts in neither master nor the workbook, and writes one workbook to
the Desktop **the shell named** (`[Environment]::GetFolderPath('Desktop')`, the OneDrive one):

```
rows written: 581 | craft KEEP: 26 | niche: {'true': 199, 'unknown': 329, 'false': 53} | platform: {'unknown': 533, 'tiktok': 46, 'instagram': 2} | from bl1232: 429
```

Columns: handle · platform · bio · email · craft_cut verdict · niche verdict · **source file ·
file date** · profile link (clickable). Sorted craft-KEEP first, then niche true → unknown →
false. A READ ME sheet carries the caveat: 429 of the 581 (446 per file, before the union) come
from one August meme-page corpus, not editor hashtags; the craft verdict is an extrapolation
from 247 editor-enriched TikTok labels. Nothing was written to master or the workbook.

## 6. Part 5 — the vision flag, described, not changed

The warning already exists in code: `main.py:5488-5497` prints a boxed **"THUMBNAIL-VISION IS ON
BUT NOT INSTALLED — it will do NOTHING"** in the run banner of the campaign funnel (the only
funnel that uses vision, via `make_vision_fn`), from `thumbnail_vision.status_line`
(`thumbnail_vision.py:117-134`), and `main.py:1597-1610` surfaces the same line under `--health`.
So the flag is not silently fake-on where vision is used. What is true: that banner goes to
stdout and appears in **0 of 18** `logs/runs/*.log` and 0 lines of `logs/run.log` — the
dashboard-launched funnels (`tiktok_finder`, `meme_finder`) do not print it and do not use
vision either. The kind of zero: **untestable from the logs** (stdout is not captured), so
whether a human has seen the box since August cannot be established. A 1-line LOCAL change
would add `status_line` to `--health`'s summary in the dashboard; it is not covered by any suite
this round ran, so it is left for the next round.

## 7. Assertions at close

```
master_leads.csv  74,218 rows x 75 cols  (sha256 ede73c71… unchanged)   workbook Emails 3,028 rows, MARK non-empty 0
spend.json  sha256 4edc0802cd… 16,043,805 bytes == start of round      config.json sha256 82e65b78… unchanged
config.backups/ 1,227 files before and after the suites; spotify_playlists_seen.json sha256 63111d43… unchanged
BL-1574 vault on D:  VAULT VERIFIED  (untouched)                         reports clone: main == origin/main, 1,233 reports
```

## 8. What I got wrong

- **The first suite pass wrote one empty directory into the real quarantine** — `test_scratch_gc`'s
  apply test ran before its fixture pointed the data destination at the temp dir. 0 files; the
  directory was removed and the fixture now sets `CLIPPERSHQ_QUARANTINE_DIR`. A retention
  change's test must be sandboxed before it is run, not after.
- **My first 581 was 578**: first-sighting-wins is not the census's rule; three accounts were
  first seen bio-less and later with a bio. The sheet now applies the same collision rule.
- **The brief's "69 AST-read children" is 39 names in the constant**: the 69 in BL-1573's table
  include 30 loose files directly in `output/`, which the rule never lists at all.
- **The pruners would reclaim 0.34 GB today, not tens of GB** — because BL-1574 already deleted
  by hand what the rules would have moved. That is the honest number; the fix is for the next
  40 GB.
- **Leak scan of this report:** built from both corpora, detectors proven on planted `.invalid`
  controls; 0 leaks, 0 C0 bytes, asserted before writing.
