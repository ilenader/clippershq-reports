# BL-1574 — The vault, then the reclaim: 4,802 files on two devices, then 54 GB back

**Round:** BL-1574 · **Spent: $0.00** — `spend.json` sha256 `4edc0802cd…` / 16,043,805 bytes at
start and at close, byte-identical; no vendor call. · **No code change.** No module, tool, test or
pruner edited. · Paths redacted: `<PROFILE>` is the user folder; everything else repo-relative.

## The paragraph

**The vault holds 4,802 files / 1,165.00 MB — master (74,218 × 75), the workbook (3,028, MARK
untouched), every seen store by shape, the 1,532-bio checkpoint, `config.json` and all 1,189
`config.backups/` generations, `spend.json`, FACTS, the claim registry, the memory files, the
reports clone, and 251 lead/bio files a content sweep found (60,000+ paid bios sitting inside
`output/`, the directory he said he does not need) — copied, sha256-manifested, then verified by
re-reading every copy and re-deriving every row count from the copy, on the local NTFS volume AND
on the USB stick, a second physical device (D:, FAT32, 15 GB free).** Neither copy is under
OneDrive. Then three tiers deleted **76,719 files = 55.22 GB by the log; free space moved 26.67 →
79.97 GB across the tiers, 54.06 GB measured** (gap 2.1%). **Skipped, with reasons:** the paste
render root (9.39 GB — the dashboard serves it), 16.9 GB of `output/` children that a test names in
a real string literal, every record file (json/jsonl/csv/xlsx) anywhere, every config generation
not proven superseded, and the root `master_leads.csv.*.bak` the daily pruner already governs.
**After deletion, every live store re-verified identical to its start-of-round shape, with the
checker proven on a planted absent path and a planted wrong hash.** Leads, bios, seen-sets, the
learning in the reports repo (1,232 published, HEAD = remote) — all intact. One thing to say out
loud: the project repo's branch is **684 commits ahead of its remote**; the vault holds `docs/`,
`reports/` and the claims, not the git history — that history is still one-volume until someone
pushes.

## 1. What this project is, for a reader with no context

ClippersHQ finds video editors on TikTok and Instagram and delivers their addresses to one
operator who reads one workbook. BL-1573 measured the disk: 79.9 GB in the repo folder, 39 GB of
it page-grid renders under `output/`, 29.6 GB of byte-identical copies, 28 GB free on the only
volume — and an off-device backup that has never once succeeded. The operator's instruction for
this round: *renders are disposable; leads, bios, seen-sets and written learning are not.* This
round vaulted the second set first, verified it twice, and only then deleted the first.

## 2. Phase 1 — the vault

**Enumerated from disk, not memory** (`scratch/bl1574/vault.py enumerate`): every regular file at
the repo root except lock files and the rotated master copies; `config.backups/`; `.claims/`;
`docs/`; `reports/`; `ground_truth/`, `clip_library/`, `_probe_samples/`, the `exports_*` dirs;
`memebot/runs.jsonl`; `scratch/songs.json`; the quarantine manifests; the workbook, his two review
files and the two BL-1541 CSVs on the local Desktop; the memory directory; the reports clone.

**The sweep for the only copy of paid data** (`bio_sweep.py`): every JSON/JSONL under `scratch/`,
`output/`, `quarantine/`, the backup piles and the root — 199 files carry bios whose handle master
either lacks a bio for (1,281) or does not hold at all (142,514). The biggest are **inside
`output/`**: `output/bl1542_run/checkpoint.json` (39,003 bios, 34,624 for handles master has never
seen), `bl1544_run` (23,690), `bl1545_run` (1,551), `bl1541_run` (1,614); then
`scratch/bl1569/fetch_ckpt.json` (2,552 bios, **1,532 for handles master lacks** — re-derived
against live master, not inherited). All 199, plus every `walk_rows` / `checkpoint` / `rows.jsonl`
under `scratch/` and `output/`, went into the vault (label `bio_and_lead_files`, 251 files,
484 MB) **and stayed in place** — the deletion rule never touches a record extension.

| label | MB | files |
|---|---|---|
| bio_and_lead_files | 484.00 | 251 |
| config_backups (real keys) | 294.63 | 1,189 |
| repo_root (master 40 MB, spend 16 MB, every seen store, config, FACTS…) | 89.18 | 145 |
| reports_clone (the published learning, working copy) | 80.68 | 1,342 |
| clip_library (paid vision labels) | 67.44 | 111 |
| _probe_samples (raw vendor payloads) | 61.97 | 199 |
| exports_meme_pages / spotify / repost | 38.68 | 46 |
| ground_truth (hand labels) | 21.69 | 134 |
| memebot/runs.jsonl | 10.09 | 1 |
| reports_repo, docs, claims_registry, memory (693 files) | 12.16 | 1,360 |
| operator_desktop (workbook, review page, BL-1541 CSVs, BL900 set) | 2.91 | 10 |
| **total** | **1,165.00** | **4,802** |

**Copied, never moved**, to `<PROFILE>/AppData/Local/ClippersHQ/vault_bl1574/` — outside the
OneDrive sync root — with `vault_manifest.json` (source path, size, mtime, sha256). **Verified by
re-reading the copies:** 4,802 re-hashed, **0 mismatches, 0 missing**, and the shapes re-derived
from the copies equal the shapes derived from the sources:

```
master 74,218 x 75 · workbook Emails 3,028 rows, MARK non-empty 0, 5 sheets · clip_seen list len 2,193
tiktok_pages_seen dict, 3 top keys, pages 3,270 · fetch_ckpt done 2,722, with_bio 2,552
config campaigns [ANIME15K, DAYLIGHT, PANICBABY, STRAENGE, ZHUS] · meme 5 · repost 1,715 · spotify 3
positive control: planted missing entry reported missing = 1 of 1 -> OK    VERDICT: VAULT VERIFIED
```

(75 columns, not 74: BL-1572 appended `craft_cut`; the brief's figure predates it.)

**Off-device.** `Get-Disk` shows two physical devices: the 932 GB NVMe that holds everything, and
a 29 GB USB stick (FAT32, 15.2 GB free). The vault was copied to `D:/clippershq_vault_bl1574/`
(`copyfile`, since FAT32 cannot carry NTFS attributes) and **verified there by the same
re-read: 4,802 copies, 0 mismatches, 0 missing, identical shapes, control fired.** Neither vault
sits under OneDrive, so the placeholder question does not arise; for the record, `OneDrive.exe`
was not running and every source file was fully hydrated. **The stick is his footage stick — the
vault is one folder on it; if it leaves the machine, the vault leaves with it, which is the point.**

**The learning is off-machine, with one exception.** The reports clone exists, its remote is
reachable, local HEAD = `origin/main` = `ls-remote` (`5c4c9d65`), **1,232 reports published**. The
project repo itself: local branch `967bef15`, remote `3ad2e752`, **684 commits ahead** — the code,
`docs/claims/` and the reports' repo copies have no second copy in git. The vault carries the files;
it does not carry the history. Not pushed this round (an outward action, his call).

## 3. Phase 2 — the reclaim, tier by tier, measured

**Before any deletion:** `reclaim.py apply` refuses without `--really-delete` *and*
`BL1574_ALLOW_DELETE=1`, refuses unless `vault_verified.flag` carries `VAULT VERIFIED` (written
only from a fresh verify verdict, local and USB), and refuses while `reclaim.lock` names a live
PID. **The lock was driven:** a holder took it (PID 2436), a second `apply` with flag and
environment set answered `REFUSED: reclaim.lock is held by live PID 2436 … A second deleter does
not start.` exit 3, and the lock vanished when the holder exited. No "killed for low memory"
notice arrived during any tier; had one arrived, the lock is what would have stopped a phantom
second deleter, not the notice's accuracy.

**Per-pile proof before each tier** (`readers.py`, grep and AST, which one answered):

| pile | grep (code) | AST | answered by | content proof | verdict |
|---|---|---|---|---|---|
| `quarantine/20260816_113647` | 0 | 0 | neither | 1.406 GB byte-identical to `…_113854` (re-hashed live) | delete dups |
| `.git/lost-found` | 1 (RECOVERY.md recipe) | 0 | grep-only prose | 1.039 GB identical elsewhere; repo `fsck` clean, HEAD resolves, 41/41 manifest verifies | delete dups, then renders |
| backup piles (`backups_bl*`, `backups/`) | `backups/`: 13 code / 3 AST (`backup.py`, `backup_prune.py`, `wip_commit.py` — none opens a specific copy); `backups_bl`: 0 | — | AST | 947 copies identical to another copy; 49 identical to a vaulted file; 165 older generations with a newer copy kept | delete; keep newest per store + every config generation |
| `<PROFILE>/AppData/Local/ClippersHQ/quarantine/20260815_153917` | 0 code (1 manifest) | 0 | grep-only | class `derived` by `outputs_gc`'s own manifest | delete whole |
| weights: CLAP, OmniShotCut, torch-hub wav2vec2/beat_this/resnet18 | 0 | 0 | neither | `clip_model` is the only selecting key; **15 `clip_*` keys on 4 of 5 campaigns** (ANIME15K has none), and `MODEL_PRESETS` resolves exactly `siglip-base`, `vit-b-32`, `vit-l-14` | delete |
| `output/` (media only) | 83 code / 35 AST name `output/` — the funnel's export root | AST | the 251 lead files inside it are vaulted and are RECORD files, never deleted | delete media except AST-read children |
| `output/` children with an AST reader (`bl1350_grids` 8.08 GB, `bl1425_grids` 2.36, `bl1372_sheet` 1.40, `bl1424_grids` 1.38, `tiktok_sheets` 0.83, `bl1436_tt` 0.67, `bl1257_fresh100` 0.41, `bl1081` 0.26, and 60 smaller) | — | 1–3 tests each, or `tiktok_finder.py` | AST | — | **SKIP, 16.9 GB** — a pile with a reader fails the proof |
| `quarantine/20260816_113854` (BL-1573's KEEP) | 0 | 0 | neither | BL-1573 kept it because 170 mp4 renders were the only copy after git lost them — *unproven*, not paid or hand-made. Its paid content is the `_batch.json`/corpus records (vaulted, kept in place) | delete media, keep records |
| `C:/ClippersHQ_renders` | 8 code / 1 AST (`paste_batch.py:1179`), plus `dashboard/server.py:3361` builds its media roots from it and the paste routes serve playback | AST | — | **SKIP, 9.39 GB** — the dashboard reads it |

**Tier 1** — proven duplicates, derived renders, unselectable weights:

```
   5.483 GB     947 files  T1-backup-dup-copy
   4.732 GB    6213 files  T1-outputs_gc-derived
   1.958 GB      25 files  T1-weight-unselectable
   1.406 GB     203 files  T1-quarantine-113647-dup
   1.039 GB     285 files  T1-lostfound-dup
TIER 1 DONE: deleted 7673 file(s) = 14.617 GB (predicted 14.617 GB); free space 26.669 GB -> 41.298 GB = 14.629 GB measured
```

BL-1573's dry-run set also listed 13.4 GB of `output/` duplicate copies; that unit was not run
separately because Tier 2 deletes the whole render set, keeper and copy alike.

**Tier 2** — `output/` renders (57,354 media files across 239 children; the 69 AST-read children
and every record file untouched; checkpointed every 2,000 unlinks):

```
TIER 2 DONE: deleted 57354 file(s) = 21.539 GB (predicted 21.539 GB); free space 41.298 GB -> 61.901 GB = 20.603 GB measured; 1376 empty dirs removed; 132s
```

The 0.94 GB gap (4.3%) is logical size versus allocation slack on 57,354 small PNGs plus whatever
other processes wrote in those 132 seconds; under the 5% line.

**Tier 3** — quarantine renders, lost-found renders, backup generations:

```
  17.577 GB   11430 files  T3-quarantine-113854-render
   1.118 GB     165 files  T3-backup-older-generation
   0.221 GB      49 files  T3-backup-dup-of-vaulted
   0.087 GB      14 files  T3-lostfound-render
   0.058 GB      34 files  T3-quarantine-113647-render
TIER 3 DONE: deleted 11692 file(s) = 19.060 GB (predicted 19.060 GB); free space 61.145 GB -> 79.973 GB = 18.828 GB measured; 584 empty dirs removed; 53s
```

**Backup generations kept, by name:** 281 files. One `master_leads.csv` (the newest, 2026-09-17,
31.8 MB — the pre-BL-1572 generation; the live one and its vault copies are the current
generation), one `spend.json` (2026-09-17), one each of `spotify_playlists_seen.json`,
`email_harvest_tags.json`, the workbook copy, `clip_library.…pre_bl863.tar.gz`, and **every
`config.json` generation** (5 plain copies + 9 named `.bak` generations, 2026-07-01 → 2026-09-13)
because "superseded" could not be proven by content for a config. Seven `backups_bl*` directories
survive with 0.05 GB; `backups/` holds 1.25 GB. The root `master_leads.csv.*.bak` files (1.1 GB,
47) were not touched: `backup_prune.py` governs them daily.

**Totals, measured.** Log: 76,719 files, 55.216 GB. Free space across the three tiers:
+14.629 + 20.603 + 18.828 = **54.060 GB**, gap 2.1%. Between tiers 2 and 3 the volume lost 0.76 GB
to other writers (session logs, the suites' own backups — see section 5). Free space at the end of
the round, after the suites and this round's own scratch: **77.79 GB** against 26.66 at the start.

**Re-measured after deletion:** `output/` 17.63 GB / 30,973 files (16.9 skipped + 0.7 records);
`quarantine/` 0.84 GB / 7,010 records; `backups/` 1.25 GB; `.git/lost-found` 4 MB / 555 non-media
blobs; the outputs_gc quarantine 0 files; `C:/ClippersHQ_renders` 9.39 GB untouched.

## 4. Phase 3 — nothing broke

**Live stores, re-verified from the live files, not the vault** (`verify_live.py`):

```
OK  master             expected {'rows': 74218, 'cols': 75}
OK  workbook           expected {'emails_rows': 3028, 'mark_nonempty': 0}
OK  clip_seen          list len 2193 · OK tiktok_pages_seen dict, pages 3270 · OK config 5 campaigns
OK  fetch_ckpt         done 2722, with_bio 2552 · OK bios whose handle master lacks: 1532
OK  spend.json sha256 4edc0802cd5999d5... == start-of-round: True
positive control: planted absent path reported missing = 1 of 1; planted wrong sha reported mismatch = 1 of 1 -> OK
```

The same script found **5 vaulted sources missing live and 1 changed** — and none of the six was
touched by this round (0 deletion-log entries under `config.backups/`, none under the seen stores).
Section 5 says who did.

**Suites.** The runner's own discovery lists 485 suites; the readers table names 78 test files;
**77 exist in the runner's list and all 77 were run through `run_all.run_suite` with its ledger
sandbox** (the 78th is `run_all.py` itself). **66 green, 11 red.** Eight of the eleven are in
BL-1569's settled fail-at-both baseline (`test_atomic_io`, `test_bl1359_ig_cost_fixes`,
`test_bl1407_free_first`, `test_bl1528_absent_never…`, `test_brief_leakcheck`,
`test_dashboard`, `test_resilience`, `test_silent_zero_shape`); `test_send_list_rebuild` was
already failing at HEAD in that adjudication (its assertion: a stale `master_rows` of 72,950 in a
meta file against 74,218 live — the meta file is a record, present, unchanged). The two uncompared
reds went to the decisive control: **`test_bl1503_his_own_packs` FAILS at a clean `git archive
HEAD` extract** (`state: FAIL, checks 16`), which contains no `output/` at all — not this round's.
**`test_bl1461_video_strip` passes at HEAD (2 checks, engine test skipped for lack of a fixture)**
and fails in the working tree on `Error splitting the argument list: Option not found` from
ffmpeg; its fixture directory (`output/bl1081`, 40 files) is AST-read, protected, and has 0
deletion-log entries — the red is the engine's command line, not a missing file. Full suite not
attempted: the last three full runs were killed for memory against the 24 GB this machine has. The
two `--head` extracts this round created were removed by this round.

## 5. Two things the suites did to live stores, found by the vault check

1. **Tests write to the real `config.backups/`.** During the 77-suite run, 38
   `config_20260920_*.json` copies and 5 `spend.json.20260920_*.bak` copies landed in the
   production `config.backups/` (1,189 → 1,227 files), and `_cap_backups` rotated out the five
   oldest `spend.json` copies — the ones the vault had just captured. The vault still holds them;
   the live tree does not. BL-1460 built a `tests/config.backups/` for exactly this and some path
   still writes the real one.
2. **`tests/test_funnel_wiring.py` wrote one playlist record into the live
   `spotify_playlists_seen.json`** at 13:43:14 (1,994 → 1,995 playlists, `updated` re-stamped;
   the runner was inside that suite from 13:43:10 for 4.0 s). No money moved — `spend.json` is
   byte-identical — but a seen-store write from a test is the same defect class as the suite that
   once booked $0.038 into the ledger. Neither store was reverted: this round writes no store.

## 6. Skips, each with its reason

| skipped | GB | why |
|---|---|---|
| `C:/ClippersHQ_renders` | 9.39 | read: `dashboard/server.py:3361` (media roots) and the paste routes serve playback from it; `paste_batch.py:1179` writes it |
| 69 `output/` children with an AST reader | 16.94 | a test (or `tiktok_finder.py`) names them in a real string literal; a pile with a reader fails proof (a) |
| every RECORD file under every pile (json/jsonl/csv/xlsx/md/txt/html) | ~1.5 | leads, bios, manifests, judge results — his "keep the leads" |
| 14 `config.json` generations in the backup piles | <0.01 | "superseded" not provable by content |
| `.git/lost-found` non-media (555 blobs, 4 MB) and 0.79 GB of unreachable packed objects | 0.79 | KEEP-UNPROVEN |
| root `master_leads.csv.*.bak` (47 files) | 1.15 | governed by the daily `backup_prune`; not a tier |
| `scratch/` (6.6 GB) | 6.6 | not in scope; `scratch/bl1569/fetch_ckpt.json` inside it is IRREPLACEABLE |

## 7. The retention fix for next round — described, not done

`output/` is invisible to every pruner: `tools/outputs_gc.py` walks the repo root for
directories whose name starts with `PREFIX = "outputs_"`, which cannot match `output/`;
`tools/backup_prune.py:106` is `os.listdir(root)` at the repo root, so `backups/` one level down is
never scanned; `tools/scratch_gc.py:104` puts its quarantine inside the repo and `:77` promises
never to empty it. The scope of the fix is one directory rule per tool — an `output/` rule in
`outputs_gc` that keeps records and AST-read children (the list is in
`scratch/bl1573/candidates.json`) and moves media; a recursive `backups/` pass in `backup_prune`;
an age rule for `quarantine/`. Separately: sandbox `config.backups` and the seen-store path in the
test runner (section 5). And the 684 unpushed commits.

## 8. What I got wrong

- **My first shape check took the last file that shared a basename** and reported master as
  72,971 × 72 — a scratch copy visited after the live one. Caught by reading the printout against
  the brief before trusting the verdict; the check is now pinned to the repo-root path. The vault
  was copied twice because of it.
- **The brief's "74 columns" is 75**, and its "nine `clip_*` keys on four campaigns" is fifteen keys
  on four of five campaigns; BL-1573 had counted fourteen because it left out `clip_enabled`
  itself. Reported as counted.
- **The tiers in the brief overlap** (BL-1573's dry-run set already contained the outputs_gc
  quarantine and the lost-found duplicates that Tier 3 lists again); I ran each unit once, in the
  earliest tier that names it, and said so rather than counting it twice.
- **I did not foresee that running the suites would write into `config.backups/` and a live seen
  store.** The vault check caught both; nothing was lost, but "run the suites covering these paths"
  is itself a store-writing act in this repo and the next round should know that before it runs
  them.
- **Leak scan of this report:** built from both corpora (15,639 addresses, 77,149 handles), every
  detector proven on a planted `.invalid` address, a planted handle, a 40-hex literal, a user-folder
  path, a host:port and a C0 byte; the report: 0 leaks, 0 C0 bytes, asserted before writing.
