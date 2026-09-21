# BL-1579 — His grades are in: 17 of 100 survivors are not editors, no learned rule may cut, and the loop now measures recall

**Round:** BL-1579 · **Spent: $0.00** — `spend.json` sha256 `4edc0802cd…` / 16,043,805 bytes at
start and at close, byte-identical; no vendor call. · Paths redacted: `<PROFILE>` is the user
folder; `<Desktop>` is the OneDrive Desktop the shell names. · The results file, the review
pages, the label rows and the sheets are **not committed and not published**; only code, scripts
and this report are.

## The paragraph

**He graded all 100 cards: 83 EDITOR, 17 NOT, no "why" on any row.** The craft cut's false-pass
rate on what it *keeps* is **8.0% [3.2–18.8] on TikTok (4 of 50)** and **26.0% [15.9–39.6] on
Instagram (13 of 50)**; the intervals overlap, so 50 rows per platform cannot yet separate "Instagram
has few editors" from "the rule does not transfer" — the point estimate is 3× worse and the answer is
**(c), hold**. Every candidate rule learned from his 17 NOT rows fails his own standard: business
words fire on **29 of 83 of his editors** (35%), fan-page words on 3 of 37 Instagram editors, custom
domains on 10 of 83 — **no rule costs ≤5% of labelled editors on both label sets, so nothing ships
as a CUT.** What shipped is a **HOLD** column, `review_hold`, stamped on master (74,218 rows, now
76 columns, written under the file lock after a sha-verified backup) and on the workbook (3,028
rows, MARK 0 → 0, column by header name, two new sheets, "Would remove (BL-1579)" empty by design):
530 TikTok and 4,673 Instagram addressed rows are parked for his eye, none deleted. His 100 grades
are permanent in `ground_truth/` (append-only, no address, vaulted to both roots and re-hashed) and a
standing loop exists: `tools/review_loop.py generate | ingest | evaluate`. Its first real page —
**87 cards, 60/20/20 survivors/held/cut, stratum hidden** — is on the Desktop; its first real
evaluation, over all 347 editor labels to date, **flags the live craft cut itself: it fails
23 of 155 labelled TikTok editors, 14.8% [10.1–21.3]**, three times his 5% line. That number
comes from the 247 masked labels (23 of 109), not from his 50 — his 50 were all drawn from survivors
and *cannot* measure recall, which is exactly why the new page draws 20 of every 100 cards from
rows the rules removed. The tool recommends; it changed nothing.

## 1. What this project is, for a reader with no context

ClippersHQ finds video editors on TikTok and Instagram and delivers their addresses to one
operator. A "craft cut" (`editor_gate.bio_rule`) removes addressed rows whose bio carries no
editing vocabulary. BL-1572 built a 100-card page of rows that *survived* that cut, 50 per
platform, for him to grade by hand. This round reads those grades, learns from them under his two
standing rules — **never wrongly cut a real editor; unknown is a hold, never a cut** — acts on
what survives, and builds the mechanism that makes every future delivery teach the system.

## 2. Part 0 — the file, its copies, and where the cards came from

| copy | bytes | mtime | sha256 |
|---|---|---|---|
| `output/bl1572_review_results.csv` (repo root) — **used** | 6,532 | 2026-09-21 14:54:01 | `bcf0bd9c8ebdd597…` |
| `<PROFILE>/Downloads/bl1572_review_results.csv` | 6,532 | same second | identical |

First action once found: copied (never moved) into both vault roots
(`<PROFILE>/AppData/Local/ClippersHQ/vault_bl1574/bl1579_his_grades/` and
`D:/clippershq_vault_bl1574/bl1579_his_grades/`), re-hashed equal; both vaults report
`VERDICT: VAULT VERIFIED` at close. Read with the address mask on from the first command
(`email` and `handle` deleted after deriving the domain). Header `platform, handle, verdict, why,
email, tag`; 100 rows, 50/50 by platform; **100 of 100 match a card on the page, 0 ungraded**.

The draw was **post-cut**, by file:line: `scratch/bl1572/bl1572_review_page.py:65-70` excludes
every row whose `craft_cut` is not `KEEP`; `:251-258` is the seeded random draw per platform;
`:293` records the selection rule in the page. So the sample measures **false passes, not recall**.

## 3. Part 1 — what the grades say

| platform | graded | EDITOR | NOT | false-pass rate (Wilson 95%) |
|---|---|---|---|---|
| TikTok | 50 | 46 | 4 | **8.0% [3.2–18.8]** |
| Instagram | 50 | 37 | 13 | **26.0% [15.9–39.6]** |
| both | 100 | 83 | 17 | 17.0% [10.9–25.5] |

Re-derived a second way (17 of 100 = 17.0% from the raw verdict column; per-platform sums 4 + 13 = 17).
**The Instagram question:** the intervals overlap ([15.9–39.6] vs [3.2–18.8]), so the answer is
**(c): fifty rows cannot tell few-editors from rule-does-not-transfer.** The point estimate is 3.25×
worse; a further 100 Instagram grades would narrow each interval to about ±8 points.

**Why-text:** 0 of 17 NOT rows carry a reason. His instruction was "remove content creators and
businesses"; without a word from him, **which of the 17 are creators and which are businesses cannot
be said** — that is what the three-button page (EDITOR / CREATOR / BUSINESS) fixes.

## 4. Part 2 — learning: every candidate rule, tested three ways

Signals on his 100 (NOT 17 vs EDITOR 83), and the rule tests. "247" = the masked hand labels of
BL-1568/69 (109 E, 138 non-E; **0 Instagram rows; 14 carry an address**; labelled by the model
under masking, not by him). The line is his: **>5% of labelled editors lost ⇒ HOLD, never CUT.**

| rule | his 100: NOT caught / editors lost | split-half A / B (lost of editors) | 247: editors lost (Wilson) | verdict |
|---|---|---|---|---|
| R1 business words in bio | 0/17 · **29/83 (34.9%)** | 14/40 · 15/43 | 3/109 = 2.8% [0.9–7.8] | HOLD |
| R2 fan/meme-page words | 5/17 · 5/83 (6.0%) | 1/40 · 4/43 | 2/109 = 1.8% [0.5–6.4] | HOLD |
| R3 custom (non-free) domain | 6/17 · 10/83 (12.0%) | 5/40 · 5/43 | unmeasurable (14 addresses) | HOLD |
| R4 followers ≥ 100k | 5/17 · 13/83 (15.7%) | 6/40 · 7/43 | 5/109 = 4.6% [2.0–10.3] | HOLD |
| R5 creator first-person words | 2/17 · 19/83 (22.9%) | 10/40 · 9/43 | 18/109 = 16.5% [10.7–24.6] | HOLD |
| R6 link hub in bio | 0/17 · 1/83 | 1/40 · 0/43 | 0/109 | DEAD (catches nothing) |
| R1+R2 | 5/17 · 32/83 (38.6%) | 15/40 · 17/43 | 5/109 = 4.6% | HOLD |

Two things the table says plainly. **Business vocabulary is editor vocabulary here** ("studio",
"agency", "booking", "clients") — R1 catches none of his 17 and would remove a third of his editors.
And the only rule that separates at all on Instagram (R2, 5 of 13 NOT vs 3 of 37 editors) was learned
from Instagram rows only, so **it is applied on Instagram only**, as a HOLD.

## 5. Part 3 — what was acted on (flag and separate, never delete)

`review_hold` entered `writer.FULL_COLUMNS` first (`clippershq/writer.py`, 75 → 76 columns; a key
outside that list is silently dropped by the row comprehension). Values: `fanpage-words` (Instagram
only), `custom-domain` (either platform), both joined by `;`, blank on rows without an address.

| store | before | after | how |
|---|---|---|---|
| `master_leads.csv` | 74,218 × 75, sha `ede73c71…` | 74,218 × 76, sha `0d69689b…`, header == `FULL_COLUMNS` | backup `backups_bl1579/master_leads.csv` sha-VERIFIED; rewrite under `filelock.file_lock(master)`, tmp + fsync + `os.replace`; PID lock `scratch/bl1579/write.lock` held |
| workbook `Emails` | 3,028 rows, MARK 0 | 3,028 rows, MARK 0, `review_hold` at column 27 by header name | backup `backups_bl1579/clipper_emails_ALL.xlsx` sha-VERIFIED; re-read after save |

| platform | addressed | HELD | of which fanpage-words | custom-domain | CUT |
|---|---|---|---|---|---|
| master TikTok | 4,158 | 530 | — | 530 | **0** |
| master Instagram | 9,739 | 4,673 | 238 | 4,529 | **0** |
| workbook TikTok | 2,690 | 332 | | | 0 |
| workbook Instagram | 338 | 84 | | | 0 |

New sheets: **"Would remove (BL-1579)"** — one note row, empty by design; **"Held for review
(BL-1579)"** — every held row with its reason. The Instagram domain mix explains the 4,529: 3,704
distinct domains on 9,739 addressed rows, gmail 4,817, then talent agencies and management
companies; 4,098 rows sit on domains seen fewer than five times. A custom domain on Instagram is as
likely an agency as an editor with a website — which is why it is a hold and not a cut.

**Instagram decision (recommend only; no campaign config was changed):** hold Instagram buying
until 100 more Instagram grades exist. If the false-pass interval then still excludes TikTok's, the
rule does not transfer and Instagram needs its own gate; if the survivor pile stays at ~50 rows
(see §6), the platform is thin regardless. Two facts that would change the recommendation: an
Instagram false-pass rate under 12% on the next 100, or a CUT-stratum recall above 90%.

## 6. Part 4 — the standing loop, driven end to end

`tools/review_loop.py` (stdlib only, no handle or address ever printed):

- **`generate`** draws 100 cards from the current post-rule pile, **60% survivors / 20% HELD /
  20% CUT per platform** — stated because a sample drawn only from survivors can never discover
  that a rule throws editors away. The stratum is written to a sidecar manifest keyed by an opaque
  card id (`sha256(seed:platform:handle)[:12]`); the page never shows it. One self-contained dark
  offline page, three buttons EDITOR / CREATOR / BUSINESS on keys 1/2/3, an optional why box,
  Back / Next, autosave, Download results — built to the accessibility checklist the lead returned
  (skip link, landmarks, `aria-pressed` toggles named by their visible word, a single-key-shortcut
  off switch, one polite status region, focus moved to the card heading, 3 px white focus ring with
  2 px offset, palette with stated contrast ratios, 44 px targets).
- **`ingest <results.csv>`** appends to `ground_truth/review_marks_<page>.jsonl`, de-duplicated by
  (platform, handle), no address stored, copies to both vault roots and re-hashes, then runs
  `evaluate`.
- **`evaluate`** re-runs **every live rule** (craft cut; fanpage-words on Instagram; custom-domain)
  against **all editor labels to date** — his 100, every ingested page, the 247 as E / non-E —
  per platform, with Wilson intervals, and flags a CUT whose editor loss crossed 5%. **It only
  recommends.** Marks that answer a different question (BL-1298 WANT/REJECT, BL-1210 GOOD/BAD) are
  excluded by `mark_kind` — see §8.

**Synthetic drive** (`tests/test_bl1579_review_loop.py`, 6 tests, `.invalid` addresses, planted
handles, temp master, temp label dir, temp vault roots): generate → page + manifest with exactly
12/4/4 per platform and no stratum word in the page; ingest twice → 6 rows, "6 duplicate(s)
skipped", no `@` in the store, both vault copies re-hash equal; **negative control**: editors graded
only among survivors → custom-domain loses 0/20, nothing flagged; **positive control**: three
planted EDITOR grades on held rows → 3/23 = 13.0% > 5% → that one rule flagged, the craft rule not.
Verdict line: `Ran 6 tests … OK`.

**First real page:** `<Desktop>/clipper_review_20260921_152635.html` (35,748 bytes) with its
manifest beside it. **87 cards, not 100:** TikTok 30/10/10, Instagram **17**/10/10 — master holds
only **51 unheld Instagram survivors in total** (75 KEEP of 9,739 addressed; BL-1572's "keeps 22×
less on Instagram"), he has already graded 34 of them, and the 17 drawn are every one that is left.

**First real evaluation** (347 labels: TikTok 155 E / 142 non-E, Instagram 37 / 13):

| rule | kind | platform | false passes caught | editors lost (cut) / held (hold) | flag |
|---|---|---|---|---|---|
| craft_cut (bio_rule says no) | cut | TikTok | 137/142 = 96.5% [92.0–98.5] | **23/155 = 14.8% [10.1–21.3]** | **FLAG** |
| craft_cut | cut | Instagram | 0/13 | 0/37 | — (all his IG rows were survivors) |
| review_hold: fanpage-words | hold | Instagram | 5/13 = 38.5% | 3/37 = 8.1% [2.8–21.3] | note: a hold, his time not a loss |
| review_hold: custom-domain | hold | TikTok | 1/142 | 4/155 = 2.6% [1.0–6.4] | |
| review_hold: custom-domain | hold | Instagram | 5/13 = 38.5% | 5/37 = 13.5% [5.9–28.0] | note |

The craft-cut number re-derived a second way, straight from the 247 with `editor_gate.bio_rule` on
the masked bios: E fail 23 of 109 (the stored `bio_hit` flag agrees on 106 of 109 rows). **It
recommends: review the craft cut.** It was shipped in BL-1572 against a different criterion; by his
5% line it is over. The next page's 10 TikTok CUT cards measure this on his own grades.

## 7. Suites, and what they did to the stores

Only suites covering changed code, named: `tests/test_bl1579_review_loop.py` (new, PASS) and the
four that read `FULL_COLUMNS` in a way a new column could break — `test_funnel.py`,
`test_outcomes.py`, `test_bl1569_general_gate.py`, `test_gp_keyless_dedup.py` — with `config.json`,
`config.backups/` (every file), every `*seen*.json`, `spend.json`, master and the label store
sha-snapshotted before and after (1,269 files, `scratch/bl1579/snap.py`).

- `test_outcomes.py`, `test_bl1569_general_gate.py`, `test_gp_keyless_dedup.py`: **PASS** (40, 17, 19 checks).
- `test_funnel.py`: **FAIL, and red at HEAD too** (`run_all.py --head`, a clean `git archive`
  extract: FAIL, 394 checks). `clippershq/main.py:1165` reads `ig_budget_declared`, which is only
  bound at `:5597` in another function — a `NameError` present since BL-1566 (2026-09-16). Not this
  round's; not touched; recorded.
- **One store moved:** `spotify_playlists_seen.json` grew 665 bytes. `run_all.py -k test_funnel`
  matched **`test_funnel_wiring.py` by substring** (prefix-disjoint is not substring-disjoint — my
  own BL-1571 note), and that suite walked three real playlists into the live store at 15:20:51–58.
  Restored by removing exactly those three entries and re-serialising the way the harvester does
  (text-mode handle → CRLF): **sha256 equals the pre-suite snapshot**; the restore script refuses
  any candidate that does not re-hash to it. Diff after: **0 of 1,269 files moved.** Spotify is
  token-free; `spend.json` unchanged.

## 8. What I got wrong

1. **The first `evaluate` pooled answers to three different questions.** It read every
   `review_marks_*.jsonl` in `ground_truth/` and mapped BL-1298's WANT/REJECT and BL-1210's GOOD/BAD
   onto EDITOR/NOT — 1,170 "labels", 623 with no platform, and the craft cut's Instagram loss read
   12.3%. A REJECT is "I do not want to contact this account", which a real editor can earn. Fixed
   by admitting only `mark_kind == "operator_grade"` with the four verdicts; a negative-control test
   plants a REJECT and a GOOD file and asserts both are ignored. A label is a claim; the question it
   answered is part of the claim.
2. **`-k test_funnel` ran a suite I had not named**, and it wrote a live store. I knew this failure
   mode by name and repeated it. The snapshot caught it; the restore is proven by hash, not by
   eyeballing.
3. **The first vault-count assertion in the suite was wrong** (expected 2 "vault OK" lines, got 4:
   two ingests × two roots). The test was fixed, not the tool — the second copy re-hashing is the
   behaviour wanted.
4. **The page is timestamped, not `clipper_review_next.html`** as the claim said: each page owns
   its results filename and manifest, so two pages can never be graded into one file. The claim was
   updated to the real name.
5. **His 50 Instagram grades exhausted the Instagram survivor pile.** I planned 100 cards; there
   are 17 Instagram survivors left to draw. The page states 87.

## 9. Assertions at close

```
master_leads.csv 74,218 x 76, header == FULL_COLUMNS (76)   · workbook Emails 3,028 rows, MARK non-empty 0, review_hold present
spend.json sha256 4edc0802cd… / 16,043,805 bytes == start    · label store 100 rows (0 before + 100 graded), 0 addresses
results file + label store re-hash equal in both vault roots · vault verify: VAULT VERIFIED (both roots)
store snapshot diff before_suites -> after_all: 0 of 1,269 files moved
```

Not committed, not published: the results file, `ground_truth/review_marks_BL-1572_his_grades.jsonl`,
the review page and its manifest, `backups_bl1579/`, the workbook.
