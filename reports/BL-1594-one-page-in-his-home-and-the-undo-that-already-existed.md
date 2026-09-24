# BL-1594: his home now holds one openable grading page; the re-render is held because his clicks cannot be counted; and the config "undo" I said was missing was there all along

**IS THE FUNNEL SAFE TO RUN? YES.** No gate, cut or store write was added. Master, his workbook and MARK
were never touched. Two old copies of the grading page were moved into an archive folder in his home, and
nothing was deleted.

**Round:** BL-1594 · **$0.00, no vendor call** · 35 store files byte-identical across every snapshot taken ·
MARK never opened · accounts never named.

**Whose judgement.** No rate in this round rests on anyone's labels; every figure is a count or a test.

## The paragraph

**Step 1 stopped the re-render, as the brief says it must.**
- **No results file exists anywhere:** not in Downloads, either Desktop, Documents or his home.
- **His clicks cannot be counted.** They live in the browser storage of his real browser profile, and
  reading that means opening his profile, which this project refuses (BL-1578) and the machine's rules
  forbid for automation. So the number of the 323 cards carrying a click is **unknown, not zero**.
- **Consequence:** the brief continues only on zero, so **step 2 (re-render) and step 4 (the real-page
  loop) are held** for his answer.

**Step 3 is done.**
- His home held **3** openable grading pages sharing one storage key, including the BL-1587 page with the
  old key order. It now holds **one**, `review_CURRENT.html`.
- The other two pages and their two manifests were moved to `archive\` as `DO_NOT_OPEN_*.archived`. The
  file count is 8 → 8, every byte is still there, and `review_CURRENT` and the workbook are byte-identical.
- Both Start Menu shortcuts still resolve.
- `operator_home.install` now archives on every future render, so the second page cannot come back. The
  test was written first; it failed on his real home and now passes 5/5.

**Step 5's premise came from my own mistake.**
- BL-1583's tag disable **did** leave its undo: `config.backups/config_20260922_173221_bl1583.json` holds
  the exact pre-change campaigns (`8e02f8d6…`).
- My BL-1593 report said it left none. I had looked for a generation matching the *after* state, and
  backups are *before* copies by design.
- The audit of every tracked config writer (AST and grep) found that each already leaves a pre-write
  generation. A test now locks that in, with a positive control that proves it can fail.

## 1. What it was asked to do

**The aim:** make the page he is about to grade ingestible, and make it impossible to grade into a dead end.

1. **Report the current click state before touching anything.** If any clicks exist, stop before step 2.
2. **Re-render `review_CURRENT` with the BL-1593 template** and assert the BL-1592 set of checks.
3. **End the old-page hazard:** archive and rename the old page (never delete it), verify the shortcuts,
   and add a test that fails when more than one openable page exists. Test first.
4. **Prove the whole loop on the real page:** 3 real clicks, a real download, a real ingest into a temp
   store, then clean up his state.
5. **Make every config write leave a `config.backups` generation.** Test first.

## 2. What shipped, and how each was proved

| change | where | proved by |
|---|---|---|
| `openable_pages(home)`: every .html/.htm at any depth | `clippershq/operator_home.py` | `test_bl1594_one_page` |
| `archive_stale_pages(home)`: every page but `review_CURRENT` (plus its manifest) moved to `archive\DO_NOT_OPEN_<name>.archived`; never overwrites, never deletes, re-hash checked | `clippershq/operator_home.py` | unit tests on a temp home: bytes preserved, workbook untouched, no overwrite |
| `install()` archives after every render, so a second page cannot reappear | `clippershq/operator_home.py` | `test_install_itself_leaves_one_page` |
| a live test: his real home holds exactly one openable page | `tests/test_bl1594_one_page.py` | **failed before** (3 pages, §3b); passes after |
| his home archived | `scratch/bl1594/archive_live.py` | the verdict in §3b |
| config writers audited | `scratch/bl1594/config_writers.py` | §3c |
| every tracked config writer leaves a pre-write generation | `tests/test_bl1594_config_generations.py` | 5/5, including a positive control (a raw write with no backup is caught) |

Commit `3759db05`. No `--no-verify`. **The re-render (step 2) and the real-page loop (step 4) were not
run** (§4).

## 3. What was measured

### 3a. Step 1: the click state

**Downloaded results files** (Downloads, OneDrive and plain Desktops, Documents, OneDrive Documents, his
home, `output/`): **none**. So **nothing he has graded has left his browser**.

**Grades held in his browser: unknown.** The page saves each click in the browser storage of whichever
browser he uses, keyed by the page's storage key. Two ways to count them:
- **Read his browser's storage:** that means opening his real browser profile. It is refused here
  (BL-1578) and forbidden for automation on this machine.
- **Ask him:** the page shows "N graded" at the bottom.

Neither was done. **Not deleted, not overwritten, not migrated: no click was touched.**

### 3b. Step 3: the page hazard, test first

**Before the fix**, the live test on his real home failed:

```
AssertionError: ... his home holds 3 openable grading pages: ['clipper_review_20260923_181934.html',
'clipper_review_20260923_181934.r20260924_141438.html', 'review_CURRENT.html'] -- they share one storage key,
so a click on the wrong one writes a wrong label
```

**The archive** (`scratch/bl1594/archive_live.out`):

```
before: 8 files; openable pages 3
moved:
   -> archive\DO_NOT_OPEN_clipper_review_20260923_181934.html.archived
   -> archive\DO_NOT_OPEN_clipper_review_20260923_181934.manifest.json.archived
   -> archive\DO_NOT_OPEN_clipper_review_20260923_181934.r20260924_141438.html.archived
   -> archive\DO_NOT_OPEN_clipper_review_20260923_181934.r20260924_141438.manifest.json.archived
   review_CURRENT.html                in place, byte-identical
   review_CURRENT.manifest.json       in place, byte-identical
   clipper_emails_ALL.xlsx            in place, byte-identical
every file's bytes still in the home: True; file count 8 -> 8
openable pages now: ['review_CURRENT.html']
VERDICT: ONE OPENABLE PAGE; NOTHING DELETED; CURRENT AND WORKBOOK UNTOUCHED
```

**Start Menu shortcuts, after the move:**
- `Grade cards` → `review_CURRENT.html`, resolves.
- `Lead workbook` → `clipper_emails_ALL.xlsx`, resolves.

**After:** `Ran 5 tests … OK`.

**Why `.archived` and not just the prefix.** A `DO_NOT_OPEN_…html` file still opens in a browser on
double-click. Without an .html extension it does not. The vault still holds the originals under their
real names.

### 3c. Step 5: every tracked config writer

**The audit** (`config_writers.out`) covered 225 tracked .py files, with AST plus grep:

| writer | sites | backs up first? |
|---|---|---|
| `control._backup_and_save` → `main.safe_write_json` | 4 (`control.py:1434, 4330, 4371, 4495`) | yes: a timestamped generation first |
| `main.save_config` → `safe_write_json` | 3 (`main.py:4730, 4760, 4778`) | yes |
| dashboard save routes | `server.py:2398, 2780` | yes: `control._make_backup` first (`:2387`, `:2770`); `:2412` is a restore *from* a backup |
| `clip_pipeline.py:4553`, `paste_batch.py:2813` | 2 | **not the live config**: throwaway render `config_<render_id>.yaml` files in a run's work folder (false positives of my pattern) |

**BL-1583's write, the premise of step 5:** `scratch/bl1583/disable_tags.py` wrote two sha-verified
backups before it wrote.

```
config.backups/config_20260922_173221_bl1583.json   campaigns 8e02f8d6f6307ae8   (the PRE-change state = the undo)
backups_bl1583/config.json                          campaigns 8e02f8d6f6307ae8
live config.json                                    campaigns 5f8d53f6d0acaa08
```

**Every writer already backs up, so the test could not be shown to fail first.** It locks the behaviour in
instead: each writer is driven on a temp config, and a generation holding the pre-write bytes is required.
The **positive control** is a raw `json.dump` with no backup, which the same check catches. `Ran 5 tests …
OK`.

**Observation, not changed** (outside this brief):
- **Different retention:** generations written through `main` (`config.json.<stamp>.bak`) are capped at
  the newest **5** (`BACKUP_KEEP`). Generations through `control` (`config_<stamp>.json`) are not capped.
  That is why there are 1,169 of one kind and 5 of the other.
- **The consequence:** an undo point written by `main` disappears after five later saves.

### 3d. Suites (named exactly; snapshot around the run)

**8 suites run: 7 green, 1 red:**
- **Green:** `test_bl1594_one_page`, `test_bl1594_config_generations`, `test_operator_home`,
  `test_bl1592_buttons_and_rank`, `test_bl1579_review_loop`, `test_bl1593_keymap` and
  `test_governance_rules`.
- **Red: `test_dashboard`, which is red at HEAD too** (`run_all --head`: `FAILED -- 1 red of 1 suite(s)`).
  This round did not touch the dashboard.

**Pre-existing and left alone, per the brief:** `test_atomic_io` and `test_silent_zero_shape`.
`test_dashboard` joins them as a third.

0 of 35 store files moved.

## 4. What was refused and why

- **Step 2 (re-render `review_CURRENT`): held.** Step 1 could not establish zero clicks, and the brief
  continues only on zero.
  - **Why it is safe to run once he answers:** the re-render keeps the storage key, so any clicks he has
    made stay on the page.
  - **What those clicks will cost him:** they carry no key-map stamp, so ingest will refuse them. He would
    re-grade those cards.
- **Step 4 (the real-page loop): held**, because it depends on step 2.
  - **How it will run, and why his clicks are never touched:** in a **throwaway browser profile** (a temp
    `--user-data-dir`), never his. Browser storage lives inside the profile, so the 3 test clicks would
    never reach his page state, and "deleting them" is just discarding the temp profile.
  - **Why that is safer than the brief's literal instruction:** the brief says delete the 3 test clicks
    from his page state, which would mean writing into his real profile.
- **Reading his browser profile to count clicks:** refused.
- **Deleting anything:** refused. The archive only moves files.
- **Fixing `test_atomic_io`, `test_silent_zero_shape` or `test_dashboard`:** not done, per the brief.

## 5. What I got wrong

1. **BL-1593 §3a stated that BL-1583's config write "left NO config.backups generation".** It was false.
   The pre-write generation `config_20260922_173221_bl1583.json` exists, and it is the undo. I compared
   generations against the post-change hash, which a backup can never have. This round's step 5 was built
   on that error; the report corrects it rather than "fixing" a gap that was not there.
2. **The brief asked me to prove the config test fails first. It could not fail**, because the behaviour
   already existed. I used a positive control instead and say so, rather than breaking a writer to
   manufacture a red.
3. **My config-writer audit pattern over-matched.** It flagged two throwaway render-YAML writers as live
   config writes. Both were read and cleared.
4. **The first store snapshot was taken mid-round**, just before the suites, not at the very start. Before
   it, the round only read files and moved four files inside his home, which is not one of the 35 stores.
5. **Stopping at step 1 means the round's stated point**, a page he can grade into ingest, **is not
   delivered yet.** That is the rule working, but it is the headline, so it is stated here as well as in the
   paragraph.

## 6. Money, stores, disk

```
money: $0.00; vendor calls: 0; network: the publish and its signed-out check only
store files (35: master, spend.json, config.json, the tag ledger, his workbook, every ground_truth/ file):
  pre-suite -> end 35 vs 35, 0 moved
his home: 8 files -> 8 files; 4 moved into archive\ (renamed DO_NOT_OPEN_*.archived), 0 deleted;
  review_CURRENT.html, review_CURRENT.manifest.json, clipper_emails_ALL.xlsx byte-identical
MARK: never opened (the workbook was hashed as bytes, never parsed)
his browser profile: never opened
processes killed: none
```

## 7. Ranked next steps

1. **He answers one question: has he clicked any cards yet?** The page shows "N graded" at the bottom.
   - **If 0:** run step 2 (`python tools/review_loop.py rerender`) and step 4 (three clicks in a throwaway
     profile, the real download, a real ingest into a temp store). Then he grades, and every grade is
     ingestible.
   - **If more than 0:** the same re-render keeps them visible, but they carry no key-map stamp, so ingest
     refuses them. He re-grades those cards; nothing is guessed.
2. **Separate:** decide whether `main`'s 5-generation cap on config backups is short enough to lose an
   undo.
3. **Separate, pre-existing reds:** `test_atomic_io`, `test_silent_zero_shape` and `test_dashboard`.

## 8. Paths

Everything below is under `%USERPROFILE%\OneDrive\Desktop\clipper finder\` unless shown otherwise.

**Code:** `clippershq\operator_home.py`

**Tests:**
- `tests\test_bl1594_one_page.py`
- `tests\test_bl1594_config_generations.py`

**Proof files**, under `scratch\bl1594\`:
- `archive_live.py` / `.out`
- `one_page_BEFORE_fix.out`, `one_page_MID.out` and `one_page_AFTER_fix.out`
- `config_writers.py` / `.out`
- `config_generations.out`
- `suites.out`
- `dashboard_head.out`
- `snap_stores.py` and `stores_*.json`

**His home:**
- `%LOCALAPPDATA%\ClippersHQ\operator\review_CURRENT.html`, the only openable page.
- `%LOCALAPPDATA%\ClippersHQ\operator\archive\`, which holds the four `DO_NOT_OPEN_*.archived` files.

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1594-one-page-in-his-home-and-the-undo-that-already-existed.md
