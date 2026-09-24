# BL-1593: both reds fixed where they were actually wrong, a grade now says which key order made it, and ingest is proven ready, but the page he has open cannot feed it yet

**IS THE FUNNEL SAFE TO RUN? YES.** No gate, cut or row removal was added, and no production store was
written. The only behaviour change on his path is that `review_loop.py ingest` now **refuses** grades
that do not say which key order produced them. That is the point of item 2, and it has one consequence he
must decide about (below).

**Round:** BL-1593 · **$0.00, no vendor call** · 35 store files byte-identical start to end · MARK never
opened · his old page and `review_CURRENT` untouched (the old page's hash is `93216e78…`, the same as
BL-1592's "before" hash) · accounts never named.

**Whose judgement.** No rate in this round rests on anyone's labels; every figure is a test or a count.

## The paragraph

**All three are done. One thing needs his decision before he grades.**

- **The two reds.** Each was traced to what was actually wrong, not edited green:
  - **The governance fingerprint: the test's baseline was stale.** 1,169 of 1,170 config generations
    hash to the recorded pair. The single change is BL-1583's deliberate disabling of 13 PANICBABY tags.
    The new baseline now lives in one place, `health_check.py`, with that provenance.
  - **The writer self-test: three things, and one was a real code bug.** The no-drop guard misread
    mixed-width legacy files and refused a migration that would lose nothing. The drift fixture predated
    that guard. And **a lead had fallen out of `BOT_READY` because of the `.invalid` placeholder I put
    in BL-1592.** Now `ALL PASS`, 95 checks.
- **The key-map gate.** Every page now stamps the key order (`KEYMAP_VERSION = 2`) into each stored grade
  and into the results file. Ingest refuses any row whose version is missing or old, loudly, naming the
  file, and never reinterprets it. The test was written first and failed before the fix; after it, 5/5 pass.
- **Ingest readiness.** A synthetic file with all four buttons, driven through the real command line into
  a temp store: ingested 4/4. `NOT_FOR_HIRE` is stored raw and scored NOT. The live label store is
  byte-identical afterwards.

**The consequence he must decide about.** The page he opens today (`review_CURRENT`, BL-1592 template)
does not stamp a key map. So **anything he downloads from it now will be refused**. The same dry run proved
it: exit 3, 0 stored, the file named.
- Making it ingestible means re-rendering `review_CURRENT` with this template. The BL-1592 method keeps
  the cards, the order, the storage key and the results file.
- This round was told not to touch that page, so it has not been re-rendered.
- Any grade he has already clicked stays unversioned and will be refused. Nobody can know which page
  produced it.

## 1. What it was asked to do

1. **Fix the two reds at HEAD** (BL-1592 §7.4): `test_governance_rules` and the `writer.py` self-test.
   Paste the real failure, decide whether the test is stale or the code is wrong, and fix what is wrong.
   Never edit a test just to make it green.
2. **Guard the key-order hazard** (BL-1592 §7.1).
   - Stamp the key-map version into the stored record.
   - Ingest refuses missing or old versions loudly, naming the file.
   - Write the test first and prove it fails.
   - Do not delete the old page. Do not touch `review_CURRENT` or anything he has clicked.
3. **Ingest-readiness dry run.** Push a synthetic file through the real ingest into a temp store, prove
   `NOT_FOR_HIRE` is stored as NOT with the raw verdict kept, and keep the live store byte-identical.

## 2. What shipped, and how each was proved

| change | where | proved by |
|---|---|---|
| campaigns baseline: ONE copy, with its history | `tools/health_check.py` `CAMPAIGNS_SHA_*`, now `5f8d53f6d0acaa08` / `c09c936d0bdf5d7a`; the test reads it instead of a private copy | `test_governance_rules`: 26 OK, including a new control that the pair is two distinct 16-hex values |
| no-drop guard reads each row through the layout migration will use | `clippershq/writer.py` `extra_master_columns` | the self-test's mixed-width drift file migrates, and a new check requires 0 on the mixed file and 1 on a populated one |
| drift fixture: `faceless_score` emptied; a populated retired column is tested as a REFUSAL, file byte-identical | `writer._selftest` | `[OK] a populated retired column (faceless_score) is REFUSED, file byte-identical` |
| the `dropped_faceless` counter labelled unreachable | `writer.migrate_master_csv` (comment only) | read: the guard raises before any row is counted |
| the fixture lead I broke in BL-1592 ships again | `writer._selftest`: a synthetic address on the sibling fixtures' domain, absent from both lead stores | `[OK] reach-first … ['90', '40', '70']`; `write_point_guard`: 0 lead addresses in the file |
| `KEYMAP_VERSION = 2`; every answer carries `km`; the results CSV has a `keymap` column | `tools/review_loop.py` template and constant | `test_bl1593_keymap` |
| ingest refuses a row whose key map is missing or old, naming the file, exit 3; accepted rows carry `keymap` into the store | `tools/review_loop.py` `cmd_ingest` | `test_bl1593_keymap`; the dry run |
| one renderer, which refuses an unfilled placeholder instead of writing a blank page | `tools/review_loop.py` `render_page`, now used by `generate` too | `test_bl1593_keymap` (the accessibility reviewer's catch) |
| guarded replace in `atomic_write_text` | `tools/review_loop.py` | `test_atomic_io` drops that site (3 → 2 unguarded) |
| the bl1579 results fixture carries `keymap` (it models a current-page download) | `tests/test_bl1579_review_loop.py` | the suite is green again |

Commit `881dc4c4`. No `--no-verify`. **The accessibility lead reviewed the template change *before* it was
made** (it is non-visual: a stored field and a CSV column). Verdict: "No WCAG concern". It flagged the
unfilled-placeholder risk, which is now enforced.

## 3. What was measured

### 3a. The governance red, pasted

```
AssertionError: Items in the first set but not the second: '5f8d53f6d0acaa08' 'c09c936d0bdf5d7a'
Items in the second set but not the first: '7a029ee5447cddd8' '8e02f8d6f6307ae8'
```

**The test was stale, and the code was right.** Traced through every config generation
(`scratch/bl1593/campaign_fp_history.out`):

```
generations read: 1170; generations hashing to the RECORDED pair: 1169
campaign-block changes across the history: 1
config.json: 8e02f8d6f6307ae8 -> 5f8d53f6d0acaa08  (OUT OF the recorded pair)
  + campaigns.PANICBABY._default_hashtags_disabled_bl1583 (added)
  ~ campaigns.PANICBABY.default_hashtags: list 1811 -> 1798 items (+0 / -13)
re-encoding check: the live block re-serialised and re-parsed hashes the same: True
```

That is BL-1583's published decision, not a re-encoding.
- **Two copies of the baseline existed:** the tripwire in `health_check.py` and the test. They now share
  one.
- **The history is recorded beside the value.**
- **Side finding:** BL-1583's config write left **no** `config.backups` generation, so the change is
  visible only by diffing the last backup against the live file.
- **About 250 older reports quote the old pair** as their own campaigns fingerprint. Those were true when
  written and are not edited.

### 3b. The writer self-test red, pasted, and what it turned out to be

```
ValueError: …drift_master.csv: refusing to migrate — it has column(s) this version does not know that
CONTAIN DATA: faceless_score (2 rows). …
```

**Three separate things, found one at a time:**
1. **The fixture was stale.** It put `"42"` in the retired `faceless_score` column from the era when a
   migration silently discarded it. The newer no-drop guard, and his standing rule, refuse that. The
   fixture now leaves it empty, and a **new** check proves a populated value is refused and the file left
   byte-identical.
2. **The code was wrong.** After step 1 the guard still refused the fixture, for "faceless_score (1
   rows)". The file's 18-column row has no `faceless_score`. `extra_master_columns` read every row by the
   14-column header's positions, so it took that row's `videos_sampled` value for `faceless_score`. On any
   mixed-width legacy file, the guard refused a migration that would lose nothing. Each row is now mapped
   by its own layout, exactly as the migration maps it.
3. **A regression of mine.** The run went on to show `[FAIL] reach-first … ['90', '70']`: a lead missing
   from `BOT_READY`. That lead's address was the `.invalid` placeholder I put there in BL-1592 when
   removing a real address. `bio_parser.valid_email` correctly rejects every reserved domain (`.invalid`,
   `example.com/org`, `.example`, `.test` were all probed: all rejected). **The version before my BL-1592
   commit passes this check** (`['90', '40', '70']`). The fixture now uses a synthetic address on the
   sibling fixtures' domain, which is absent from both lead stores.

After all three: `ALL PASS`, 95 checks. The red run had stopped after 60.

### 3c. The key-map gate: test first

Before the fix (`keymap_test_BEFORE_fix.out`), `FAILED (failures=2, errors=2)`:
- `KEYMAP_VERSION` did not exist;
- a synthetic old-map row and an unversioned row were ingested with exit 0: `AssertionError: 0 == 0 : a
  refusal is a non-zero exit, never a quiet success`.

After: `Ran 5 tests … OK`. The fifth test is the reviewer's blank-page guard.

### 3d. Ingest readiness (`scratch/bl1593/ingest_dry_run.out`, the real command line in a subprocess)

```
A) current-template file, all four buttons, keymap=2, REAL CLI ingest into a TEMP store
   exit 0; stored 4/4; raw verdicts ['BUSINESS', 'CREATOR', 'EDITOR', 'NOT_FOR_HIRE']
   NOT_FOR_HIRE stored raw as 'NOT_FOR_HIRE', scored by all_labels as 'NOT'
   scored: EDITOR->EDITOR CREATOR->NOT BUSINESS->NOT
   every stored row carries keymap=2: True; copied to both TEMP vault roots: True   -> PASS
B) the SAME four grades as the INSTALLED review_CURRENT (BL-1592 template, no keymap column) downloads them
   exit 3; stored 0; refusal names the file: True
   REFUSED: 4 of 4 row(s) in review_dryrun_installed_results.csv do not carry key map v2 (missing: 4) --
   the file has NO keymap column: it was written by a page older than BL-1593. …   -> PASS (refused, as designed)
live label store + real vault review_loop_labels: 29 files, hash 7a7063d59f900e77 -> 7a7063d59f900e77: BYTE-IDENTICAL
VERDICT: INGEST READY for a current-template download; the installed page's download is REFUSED
```

**How "stored as NOT" works:**
- **The store keeps the raw verdict** (`NOT_FOR_HIRE`), plus `keymap: 2`.
- **Scoring reads it as NOT** in `all_labels`, the function every evaluation uses.
- **No stored field is literally `NOT`.** The raw value is what makes "edits, not for hire" separable
  later.

### 3e. Suites (named exactly, snapshot around every run)

The final run covered 17 suites: **15 green, 2 red, both red at HEAD, and neither is a file this round
touched:**
- **`test_atomic_io`:** unguarded `os.replace` / `os.remove` sites. It was 3 and is now 2, after this
  round guarded the one in `review_loop.py`. The remaining two are `clippershq/proxy_pool.py:290` and
  `tools/backup.py:170`, outside this claim.
- **`test_silent_zero_shape`:** flags `main.py` (`_cap_backups`, `delivered_projection`),
  `free_judge.py`, `meme_finder.py` and `mark_reader.py`, all untouched here.
  `run_all --head`: `FAILED -- 1 red of 1 suite(s)`.

0 of 35 store files moved in any run.

## 4. What was refused and why

- **Re-rendering `review_CURRENT` so it stamps the key map:** not done, because the brief forbids touching
  it. It is the one step between him and an ingestible download (§7).
- **Any override to accept unversioned grades:** not built. "Never silently reinterpret" was the
  instruction, and a flag that assumes the key order would be exactly that.
- **Deleting or editing the old page:** not done. Its downloads are refused by the gate instead.
- **Editing the ~250 historical reports** that quote the old campaigns pair: refused. Each was true when
  written.
- **Fixing the three other pre-existing reds** outside the brief (`test_atomic_io`'s two remaining sites,
  `test_silent_zero_shape`): reported, not fixed. The one `atomic_io` site in a claimed file was fixed.
- **Nothing on the refuted list** was touched.

## 5. What I got wrong

1. **In BL-1592 I broke the writer self-test and called the red "pre-existing".** My redaction put a
   `.invalid` address on a fixture lead that must ship; the send-list filter correctly dropped it, and the
   reach-first check failed. I read only the tail of the output (the drift crash), compared it with HEAD's
   tail, and reported "red at HEAD as well". The version before my commit passes that check. Found this
   round; fixed.
2. **I first told you both reds were "test stale, code right".** For the writer, that was wrong. Emptying
   the fixture exposed a real code bug in the no-drop guard (§3b.2). I had concluded before I had run the
   fix.
3. **The fixture address departs from the `.invalid`-only rule.** A fixture whose purpose is "this lead
   ships" cannot use any reserved domain, because production correctly rejects all of them. It uses a
   synthetic address on the domain the sibling fixtures already use, checked absent from both lead stores.
   I am stating it rather than bending production to accept `.invalid`.
4. **The gate I was asked to build blocks the page he has open today.** That is correct behaviour, but it
   means a round that has "ingest ready" as its headline also leaves his current download un-ingestible.
   It is stated at the top, not buried.
5. **My first governance plan was simply "update the constant".** I traced the history before writing it,
   which is what showed there were two copies of the baseline and a config write with no backup.

## 6. Money, stores, disk

```
money: $0.00; vendor calls: 0; network: the publish and its signed-out check only
store files (35 incl. master, spend.json, config.json, the tag ledger, his workbook, every ground_truth/ file,
             the label store): start -> end 35 vs 35, 0 moved
live label store + real vault review_loop_labels (29 files): byte-identical across the ingest dry run
MARK: never opened
his home: untouched (review_CURRENT.* and the old page keep their BL-1592 timestamps; old page sha 93216e78…)
suites: 17 in the final run, 15 green, 2 red at HEAD (reported); writer self-test ALL PASS (95)
processes killed: none
```

## 7. Ranked next steps

1. **His decision: make the page he opens ingestible.** Re-render `review_CURRENT` with the BL-1593
   template (`python tools/review_loop.py rerender`). It keeps the same cards, order, storage key and
   results file, as BL-1592 proved.
   - **What happens to grades already clicked:** anything clicked before the re-render has no key-map
     stamp and will be refused.
   - **How much re-grading that means:** he re-grades those cards, which is 0 cards if he has not started.
     There is no way to recover which page produced an unstamped grade.
2. **After that, he grades and downloads.** Ingest then works end to end, as §3d proves. His grades from the
   old page are refused with the card ids listed, never guessed.
3. **Separate, small:** guard `proxy_pool.py:290` and `backup.py:170` (`test_atomic_io`), and settle
   `test_silent_zero_shape`'s five sites.
4. **Make config edits leave a backup.** BL-1583's tag disable left no `config.backups` generation.

## 8. Paths

Everything below is under `%USERPROFILE%\OneDrive\Desktop\clipper finder\`.

**Code:**
- `tools\health_check.py`
- `clippershq\writer.py`
- `tools\review_loop.py`

**Tests:**
- `tests\test_governance_rules.py`
- `tests\test_bl1579_review_loop.py`
- `tests\test_bl1593_keymap.py`

**Proof files**, under `scratch\bl1593\`:
- `campaign_fp_history.py` / `.out`
- `governance_before.out` / `governance_after.out`
- `writer_selftest_before.out`, `writer_selftest_after.out`, `writer_selftest_final.out` and `writer_selftest_HEAD.out`
- `keymap_test_BEFORE_fix.out` / `keymap_test_AFTER_fix.out`
- `ingest_dry_run.py` / `.out`
- `suites.out` and `suites_final.out`
- `atomic_head.out` and `silent_zero_head.out`
- `snap_stores.py` and `stores_*.json`

**His home (untouched):** `%LOCALAPPDATA%\ClippersHQ\operator\`

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1593-two-reds-fixed-keymap-gate-and-ingest-ready.md
