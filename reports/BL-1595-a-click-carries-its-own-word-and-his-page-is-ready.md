# BL-1595: a click carries its own word, so nothing he graded is lost; his page is re-rendered, proven end to end, and now saves his work to a file every 25 grades

**CAN HE GRADE STRAIGHT AWAY? YES. DOES ANY CARD NEED RE-GRADING? NO.** Every grade ingests: stamped ones
from the new page, and unstamped ones (from before) inferred from their own verdict words, with a tag that
lets them be separated later.

**IS THE FUNNEL SAFE TO RUN? YES.** No cut, no gate beyond step 2's, no store write. Master, his workbook,
MARK and his browser profile were never opened.

**Round:** BL-1595 · **$0.00, no vendor call** · 35 store files byte-identical start to end · the live label
store byte-identical through the real-page loop · accounts never named.

**Whose judgement.** No rate in this round rests on anyone's labels; every figure is a count, a test or a
driven browser.

## The paragraph

**I answered the question from the code, as asked.**
- **What each page stores per click:** in all three templates, the **verdict word**
  (`ans[r.id]={v:v,…}`, where `v` is `EDITOR`, `NOT_FOR_HIRE`, `CREATOR` or `BUSINESS`), never the key
  digit.
- **The vocabulary is shared:** the old and new pages store the same four words.
- **The storage key is the same:** it is byte-identical across the old and installed pages, and the new
  template fills its one key slot from the page it replaces.

**So an unstamped click already says what it means, and BL-1593's blanket refusal was over-strict.**
- **The corrected rule:** ingest accepts an unstamped row when **every** verdict in the file is one of the
  four words. It stores the row as `keymap=2` with `keymap_provenance=INFERRED_FROM_VOCABULARY`.
- **What is still refused:** a row stamped with an old key map, and any file holding a word the new page
  cannot produce.
- **Testing:** the test was written first and failed; it now passes, with a positive control proving the
  refusal still fires.

**His page is re-rendered and proven.**
- The same 323 cards, order, storage key and results file, now stamping key map v2. It is vaulted to both
  roots, and it is the only openable page in his home.
- The whole loop was run **on his real page in a throwaway browser profile**: 3 clicks, the real download,
  the real ingest into a temp store, 3 of 3 stored, and `NOT_FOR_HIRE` kept raw and scored NOT.

**The page now keeps his work visible and on disk.**
- A large tally is always visible: "N of 323 graded · key map v2 · last download: N".
- A download starts by itself every 25 new grades, so his work reaches a file while he works.
- The accessibility lead reviewed that design **before** any edit, and caught a must-fix in it.

## 1. What it was asked to do

1. **Is an unstamped click actually ambiguous?** Answer from the three templates' JavaScript, with grep and
   a parse, quoting the lines: what storage holds per click, when the stamp is written, and whether the
   storage keys are identical.
2. **The decision that follows.** Word stored → accept unstamped rows only on a closed vocabulary, tagged
   with provenance. Digit stored → keep the refusal and build a quarantine store. Test first, with a
   positive control.
3. **Re-render `review_CURRENT`**, with the full set of assertions, and prove from the template that his
   clicks survive.
4. **Prove the whole loop on the real page** in a throwaway profile, then run the step-2 branch on a
   synthetic unstamped file. The live label store must stay byte-identical.
5. **Make it unable to happen again:** an always-visible count with the key-map version, an automatic
   download every 25 cards, and the unfilled-placeholder refusal kept. Accessibility review **before** the
   edit.

**Not asked of him, per the brief:** the click count. It was not needed. The code answers the question.

## 2. What shipped, and how each was proved

| change | where | proved by |
|---|---|---|
| ingest: an unstamped row is accepted only when every verdict in the file is in `KEYMAP_V2_VOCAB`; stored `keymap=2`, `keymap_provenance=INFERRED_FROM_VOCABULARY` (stamped rows: `STAMPED`) | `tools/review_loop.py` `cmd_ingest`, `KEYMAP_V2_VOCAB` | `test_bl1595_inference`: **2 of 4 failed before**, 4/4 after; the positive control (a file holding `NOT`) is refused before and after |
| the refusal message no longer claims rows hold "digits" | same | read |
| BL-1593's two over-strict assertions corrected; every refusal they checked still asserted (old stamp; the file named; out-of-vocabulary) | `tests/test_bl1593_keymap.py` | 5/5 |
| an always-visible tally: a direct child of `body`, sticky only with room (`min-width:40em` and `min-height:30em`), `html` scroll-padding measured from its height, `z-index` 5 (below the skip link's 9), separator dots hidden from screen readers | the `review_loop.py` template | `test_bl1595_page_features`; driven in §3c |
| a download every 25 NEW grades, inside his own gesture; ONE status message reading "Started…", never "Saved"; a warning sentence under the Download button | same | driven in §3c: the 25th fires, the 26th does not |
| `review_CURRENT` re-rendered | his home, via `review_loop.py rerender` | §3b |

Commit `efdd51b3`. No `--no-verify`.

**The accessibility lead reviewed the design before the template was touched.** It found a must-fix in my
plan: a sticky bar plus `scroll-padding` on `main` (which does nothing) would have hidden the focused card
heading on every card (2.4.11), and filled half the screen at 400% zoom (1.4.10). I applied its corrected
design exactly: the one-message rule, the "started, not saved" wording, and the warning sentence.

## 3. What was measured

### 3a. Step 1, from the source (`scratch/bl1595/template_facts.out`)

| | A: pre-BL-1592 (archived) | B: BL-1592 (was `review_CURRENT`) | C: BL-1593 (template) |
|---|---|---|---|
| **grep: the click store** | `ans[r.id]={v:v,why:why,at:new Date().toISOString()};save();` | the same line | `ans[r.id]={v:v,why:why,at:new Date().toISOString(),km:KM};save();` |
| **parse: fields stored per click** | `v, why, at` | `v, why, at` | `v, why, at, km` |
| **parse: digit → value stored** | `1 EDITOR, 2 CREATOR, 3 BUSINESS, 4 NOT_FOR_HIRE` | `1 EDITOR, 2 NOT_FOR_HIRE, 3 CREATOR, 4 BUSINESS` | same as B |
| **a) stores the verdict WORD, not the digit** | yes | yes | yes |
| **b) key-map stamp** | none | none | **per click** (`km:KM`); the download only *reads* it (`(a.km\|\|'')`) |
| **c) storage key** | `var KEY="clippershq_review_20260923_181934";` | **byte-identical to A** | `var KEY="__KEY__";`, filled by `rerender` from the page it replaces |

**What the table shows:**
- **Vocabulary:** A and B store the same four words.
- **Key maps:** digits `2`, `3` and `4` mean different words on A and B.

**The instruments:**
- **Grep** answered the store line, the download lines and the key lines.
- **The parse** answered the digit→word maps and the stored field set, by extracting the literals and
  parsing them as data.
- There is no JavaScript AST parser installed here, so this is a literal parse, not a full AST. The two
  instruments agree on every item.

**The one limit no rule can remove.** A digit pressed out of habit on the old page (where `2` =
`CREATOR`) stored `CREATOR`: true to what that page showed, perhaps not to what he meant.
- **The key-map stamp could never detect that either;** it only notes which page.
- **How exposed he was:** the old page was the grading page until BL-1592 (so its order was then the
  intended one), and it has been archived and un-openable since BL-1594.
- **The mitigation:** the provenance tag keeps every inferred row separable if that ever matters.

### 3b. Step 3: the re-render (`page_check_after.out`)

```
card count SAME (323) · card content SAME · card ORDER SAME · storage key SAME · results filename SAME
manifest card set SAME · page bytes CHANGED, as intended · C0 control bytes: 0
page stamps KEYMAP_VERSION = 2 ('var KM=2;' present): True
vault, both roots, page + manifest: re-hash equal (4 of 4); review_CURRENT.* == the vaulted stamped pair: True
openable grading pages in his home: ['review_CURRENT.html']
template holds ONE storage-key slot ('var KEY="__KEY__";'): True; filled from the old page's own KEY: True
his 100 graded accounts on the page: 0 (control: the join finds 100 of his 100 as keys)
ClippersHQ files on the Desktop (2 desktop folders checked): 1
```

**Start Menu shortcuts:** `Grade cards` → `review_CURRENT.html` and `Lead workbook` →
`clipper_emails_ALL.xlsx`. Both resolve.

**Desktops:** the plain Desktop holds **1** ClippersHQ file, `clipper_emails_BL1541.csv`. That is
pre-existing, his, and untouched, as reported since BL-1592. The OneDrive Desktop holds **0**. The
checker's verdict line reads FAILED for that one file alone. It is reported, not waved through.

**His clicks survive, proven from the template rather than asserted.**
- The template has exactly one storage-key slot.
- `rerender` fills it with the key read out of the page it replaces (`extract_page` → `render_page`).
- The key is unchanged (SAME above).
- Browser storage is keyed by that string, so every click he made reads back on the new page.

### 3c. Steps 4 and 5, driven

**The real-page loop** (`real_loop.out`): Playwright's own Chromium, a fresh temp `--user-data-dir`, and
his real `review_CURRENT.html` opened read-only.

```
throwaway profile opened his page: '0 of 323 graded · key map v2 · last download: none'
after 3 real clicks: '3 of 323 graded · key map v2 · last download: none'
downloaded: review_20260923_181934_results.csv -- 3 row(s), columns [... 'keymap']
   verdicts ['CREATOR', 'EDITOR', 'NOT_FOR_HIRE']; keymap on every row: ['2', '2', '2']
REAL ingest (CLI) into a TEMP store: exit 0; stored 3/3; keymap=2 STAMPED on every row: True;
   NOT_FOR_HIRE stored raw 'NOT_FOR_HIRE', scored 'NOT' -> PASS
UNSTAMPED synthetic file (the BL-1592 page's format): exit 0; stored 4/4 with provenance
   ['INFERRED_FROM_VOCABULARY'] -> PASS
throwaway profile deleted: True; downloaded file deleted: True
a FRESH throwaway profile opens the page at: '0 of 323 graded ...' -> 0 clicks
his review_CURRENT.html unchanged by the loop: True
LIVE label store + real vault review_loop_labels: 7a7063d59f900e77 -> 7a7063d59f900e77: BYTE-IDENTICAL
```

The three test clicks existed only inside the throwaway profile, so there was nothing of his to clean up.

**The auto-download** (`auto_download.out`): a throwaway profile on a **synthetic** 30-card page
(`.invalid` data only).

```
tally position=sticky, height 54px, html scroll-padding-top=62px
downloads: before the 25th 0; after the 25th 1; after the 26th 1 -> fires on the 25th only
status after the 25th: 'Saved Business. Started a download of 25 grades. Your browser may ask to allow it.'
tally after the 25th:  '25 of 30 graded · key map v2 · last download: 25'
```

**The unfilled-placeholder refusal** (BL-1593) still holds: `test_bl1595_page_features`.

### 3d. Suites

The final run covered 9 affected suites (named exactly, under a snapshot): **ALL GREEN, 76 checks**. They
are `test_bl1595_inference`, `test_bl1595_page_features`, `test_bl1593_keymap`,
`test_bl1592_buttons_and_rank`, `test_operator_home`, `test_bl1579_review_loop`, `test_bl1594_one_page`,
`test_bl1594_config_generations` and `test_governance_rules`.

The three pre-existing reds, `test_atomic_io`, `test_silent_zero_shape` and `test_dashboard`, were not
touched, per the brief.

## 4. What was refused and why

- **Asking him for the click count:** not done, per the brief. The source code answers the question.
- **The quarantine branch:** not built. Step 1 found the word branch, not the digit branch.
- **Opening his browser profile:** refused. Every browser in this round was a throwaway Playwright
  Chromium, deleted afterwards.
- **Any change to his cards:** refused. The re-render lifts the page's own cards and key.
- **Deleting anything:** refused. The re-render's stamped pair went to `archive\` through `install()`.
- **The three pre-existing reds:** left alone, per the brief.
- **The accessibility review's optional note about a "Save as" dialog** in his browser: not testable
  without his browser. It is in §7.

## 5. What I got wrong

1. **BL-1593's refusal was over-strict, and its message was false.** I built a gate that refused every
   unstamped row, and wrote into its refusal message that such rows' "digits may mean something else". The
   rows hold words, not digits. I had not read what the page stores before designing the gate; this round
   re-derived it from the source.
2. **My tally design had a 2.4.11 must-fix in it.** I planned `scroll-padding-top` on `main`, which cannot
   work because `main` does not scroll. The review caught it before any code existed. This time the order
   was right.
3. **The in-browser focus check was weaker than it looks.** On the 30-card test page, the heading was
   already far below the bar (344px against a 54px bar), so the page never scrolled a heading under it. The
   run shows the scroll padding is set to the bar's height plus 8. It does not exercise the worst case.
4. **The stamped filenames stack a suffix per re-render.** The name now reads
   `….r20260924_141438.r20260925_115213.html`. That is cosmetic, but it will keep growing.
5. **The page checker I copied from BL-1592 looked for stamped files in his home.** They have been archived
   since BL-1594. I fixed the copy before running it, not after a false failure.

## 6. Money, stores, disk

```
money: $0.00; vendor calls: 0; network: the publish and its signed-out check only
store files (35 incl. master, spend.json, config.json, the tag ledger, his workbook, every ground_truth/ file):
  start -> end 35 vs 35, 0 moved
live label store + real vaults' review_loop_labels: byte-identical across the real-page loop
his home: review_CURRENT.* replaced by the re-render; the new stamped pair archived (DO_NOT_OPEN_*.archived);
  one openable page; workbook untouched
browsers: Playwright's own Chromium only, three throwaway profiles, all deleted; his Chrome and profile never opened
MARK: never opened
processes killed: none (each browser context closed by the script that launched it)
```

## 7. Ranked next steps

1. **He grades.** Start Menu → ClippersHQ → Grade cards.
   - **At the top of the page:** it shows how many cards are graded, the key map, and the last download.
   - **Every 25 grades:** a download starts. His browser may ask to allow multiple downloads; he should
     allow it.
   - **When he wants it ingested:** hand over the newest results file. Each file holds everything graded
     so far, so the latest one is enough.
2. **If his browser asks where to save each file,** a native Save dialog will take the keyboard focus every
   25 grades. Switching that browser setting off avoids it (the accessibility lead's optional note).
3. **Ingest the file when it arrives:** `python tools/review_loop.py ingest <file>`.
   - Stamped rows go in as `STAMPED`.
   - Any grade made before today goes in as `INFERRED_FROM_VOCABULARY`.
   - Nothing needs re-grading.
4. **Separate:** the three pre-existing reds (`test_atomic_io`, `test_silent_zero_shape`,
   `test_dashboard`), and the stacking stamped filenames.

## 8. Paths

Everything below is under `%USERPROFILE%\OneDrive\Desktop\clipper finder\`.

**Code:** `tools\review_loop.py`

**Tests:**
- `tests\test_bl1595_inference.py`
- `tests\test_bl1595_page_features.py`
- `tests\test_bl1593_keymap.py`

**Proof files**, under `scratch\bl1595\`:
- `template_facts.py`, `template_facts.out` and `template_facts.json`
- `inference_BEFORE_fix.out` / `inference_AFTER_fix.out`
- `auto_download.py` / `.out`
- `real_loop.py` / `.out`
- `page_check.py`, `page_before.json` and `page_check_after.out`
- `rerender.out`
- `suites_template.out` and `suites_final.out`
- `snap_stores.py` and `stores_*.json`

**His home:**
- `%LOCALAPPDATA%\ClippersHQ\operator\review_CURRENT.html`, the only openable page.
- `%LOCALAPPDATA%\ClippersHQ\operator\archive\`, which holds the archived stamped pairs.

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1595-a-click-carries-its-own-word-and-his-page-is-ready.md
