# BL-1494 — Packaging the Spotify lead system for a second machine

## IS THIS FOLDER SAFE TO HAND OVER, AND DOES PART C CONTAIN REAL PEOPLE?

**Yes, it is safe to hand over — and YES, Part C contains 7,618 real people's email
addresses.** That is deliberate and it is his to share. Parts A and B contain **zero** real
contact data and **zero** live credentials, both proved rather than assumed: 0 files in
A or B hold an address that exists in the live lead store, and 0 files anywhere in the package
hold a live API key. **He can hand over A and B alone and the system still works completely.**
Getting there required removing 21 real addresses that were sitting in five *production source
files* as docstring examples, and dropping six test files built from real lead rows.

---

## 1. Round ID, date, and what it was asked to do

**BL-1494**, 2026-09-03. Copy-only: no file in the project was modified, moved, or renamed.

The ask, in his words: *"Everything to do with Spotify lead generation goes in one folder so I
can hand it to a friend. He has full access. Everything he needs to run it on his own PC,
smoothly, plus a README for his Claude Code so he sets it up right. Make it easy to edit and
upgrade. And do not break anything of mine — copy."*

**Conditions at start**, checked before anything was claimed: no listener on the dashboard or
sheet-server ports (read from the listening-port table, never a command-line filter — a
process filter here once matched its own command line), 3 Python processes, 388 GiB free, and
one 272-hour-stale claim in flight. Round number verified free three ways.

Three sub-agents ran in parallel: the dependency trace, the data dictionary and provenance
audit, and the secret scanner.

**Spend: $0.00.** No vendor call was made.

---

## 2. What actually shipped

**One folder, three parts, on his Desktop.** The path is on his machine and is deliberately
not written into this public report.

```
SPOTIFY_LEAD_SYSTEM/          147 files, 10 MB
├── README.md                 for a person: install, run, what each folder is
├── CLAUDE.md                 for his friend's AI: architecture, traps, known defects
├── DATA_DICTIONARY.md        all 72 columns, what fills them, what empty means
├── A_system/       140 files, 4.8 MB   NO real contact data, NO keys
├── B_sample_data/    2 files,  20 KB   41 invented rows
└── C_live_leads/     2 files, 5.2 MB   REAL PEOPLE — has its own README
```

**Nothing was modified in the project.** All 8 protected files — `config.json`, `spend.json`,
`master_leads.csv` and the five seen stores — are **byte-identical to their pre-round
sha256**, verified at the start, during, and again at publication: **0 of 8 changed**.

---

## 3. What was measured

### 3.1 Finding everything — three instruments, reconciled, then PROVEN

The file list was traced, not guessed. That mattered: the runner dispatches funnels by
importing module names **out of string literals in a table**, and the first import graph ever
built in this project orphaned the two live finders — the most important modules in the tree.

**The control ran first.** The walker had to see a known-live edge (the Spotify finder's
import of the email finder, and its call to `ef._detect`) before any absence was trusted. It
did. It only works because the package directory has **no `__init__.py`** — it is a namespace
directory whose modules import their siblings *bare*, so the resolver indexes four separate
path roots with `os.walk`. **A dotted resolver orphans the entire tree.**

| instrument | found | what only it found |
|---|---:|---|
| AST import walk | 63 | lazy edges never executed by a drive — the rejection store, the send guard, process identity |
| runtime import trace (network hard-blocked) | 37 local | the call-time-only layers: resume, playlist harvest, the ledger, cross-dedup, preflight. **The module-level closure alone would not start a run.** |
| grep for string literals and dynamic loads | — | the dispatch table itself, a bare cross-directory import, and a prior round's stale package |

**The runtime instrument refuted the AST walk on 14 files.** The AST pulled a meme/vision tail
through the judging module; driving it showed that stage adds **two modules**, neither of which
touches the vision code. **Excluding it is what removes opencv, onnxruntime, faster-whisper and
the OCR runtime from the dependency list.**

**Reconciled: 196 files.** Then *proved*: the non-test files were copied into an isolated tree
containing no other repo file and the funnel was driven there in a subprocess with
`PYTHONPATH=""` and the network blocked. **Exit 0, end to end.** A forgotten module would have
been a `ModuleNotFoundError`. There was none.

**Every copy was verified**: 196 of 196 copied, sha256 equal at source and destination, and the
**source re-hashed after the copy** to catch a peer writing underneath us. 0 mismatched, 0
moved under us, 0 missing. Free space was re-read before the copy and every 25 files; it never
moved below 387 GiB against a 5 GiB abort floor.

### 3.2 Secrets: none travel

`config.json` was **not copied**. A `config.template.json` was generated from it using the
project's **own** secrets guard rather than a re-derived rule — a second definition of "what
is a secret" would be free to drift from the first.

**8 of 8 credential fields redacted, 0 leaked**, and the leak test was itself proved by
planting a real secret in the blob and confirming it fired. The template keeps `base_url`, the
endpoint paths, the campaign block and the measured cost notes, so it still runs once he
pastes his own keys.

> **A first attempt over-redacted and produced a template that was safe and useless.** It used
> the guard's `is_secret_field()`, which is the Control Panel's *edit-lock* rule ("may he type
> here?"), not the redaction rule ("is this value a secret?"). It returns true for every leaf
> in a credential block, so it blanked `base_url` and the endpoints — and a template with no
> base URL cannot make a call. Two different questions, one function.

**The scanner and its 21 planted controls.** Every shape it claims to detect was planted
first, including one **inside a nested subdirectory** (to prove the walk descends) and one with
a **leading-dot filename** (to prove it is not glob-blind), plus a negative control of ordinary
code that must produce zero hits.

**All 21 positive controls PASS. The negative control PASS. Nested and leading-dot both
found.**

The control table earned its place immediately — **it caught three defects in the scanner
itself** before anything was reported about the real tree:

| # | what failed | why |
|---|---|---|
| 1 | the email detector fired **0** times on a planted email | its pattern demanded **two** dots in the domain, so it could not see an ordinary address at all |
| 2 | one key format fired 1 of 2 | the word-boundary reproduced the underscore bug it was built to avoid |
| 3 | a wallet detector fired 0 | **the control body was wrong** — base58 has no zero and the plant contained one. The detector was fine |

Number 3 is worth keeping: **a failing control does not always mean a failing detector.** The
table's job is to make the disagreement visible.

**Final scan of the package**, decisive tests rather than shape counts:

- **live credential values anywhere in the package: 0** (control fired on a planted secret)
- **real lead addresses in Part A: 0** · **in Part B: 0**
- absolute paths carrying his Windows username: **0** (three were found and scrubbed from the
  copies; the survivors are a genericised `Firstname` example and two ellipsis placeholders)
- `.git` directories, `.env` files, credential stores, cached tokens: **0**
- C0 control bytes in any text file: **0**

### 3.3 The leak I did not expect, in production source

The scanner found **803 email-shaped strings inside Part A**, which is supposed to hold no
contact data. Shape is not proof, so each was tested against the live store — the only
authority on whether an address belongs to a real person.

**11 files held 32 distinct REAL addresses**: five *production source* files
(`role_policy.py`, `bio_parser.py`, `crossdedup.py`, `email_finder.py`, `send_suppress.py`)
and six test files. They are docstring examples and fixtures written years of rounds ago using
real rows.

Classified by context before touching anything: **28 of 31 occurrences in the production files
are comments or docstrings**; the other 3 sit in module self-tests. **They were redacted with a
deterministic, shape-preserving mapping** — the same real address always yields the same fake,
so duplicate-folding still folds, and role prefixes survive so role classification still
classifies. **All five modules' own self-tests still pass.**

**The six test files were removed instead**, because they assert relationships between an
address and the handle and artist name beside it; rewriting the address alone breaks the
assertion, and rewriting all three is a different job. Named in `CLAUDE.md` so nothing is
silent.

> **The original project still contains those addresses.** That is a defect in the source
> repository. It is named and left alone — this was a packaging round, and fixing it needs a
> history rewrite rather than an edit.

### 3.4 The clean-machine rehearsal — four failures, all fixed

A fresh directory outside the repo, a new virtual environment, install from the shipped
requirements, run as a stranger. **Every failure below was found by the rehearsal and by
nothing else.**

**Failure 1 — the minimal requirements file was silently clobbered.** I wrote a 7-package
requirements file, and then the 196-file copy overwrote it with the project's own 19-package
one, because `requirements.txt` was in the traced manifest. **Installing it pulled the entire
video/OCR stack** — a tokenizer, a 4 MB binary, an ML runtime — into what is a lead-generation
tool. Fixed: the minimal file is written *after* the copy, and the original is preserved
beside it as `requirements-full-original.txt` so nothing is lost.

**Failure 2 — pip could not read my requirements file at all.** It contained a warning emoji
and em-dashes. **pip decodes a requirements file using the console codepage**, which is cp1252
on a default Windows install, and one non-ASCII byte makes the whole file unreadable:
`UnicodeDecodeError: 'charmap' codec can't decode byte 0x8f`. The file looked perfect in every
editor. Fixed: the shipped file is pure ASCII and says so at the top, with the reason.

**Failure 3 — my redaction broke four tests.** The first fake addresses used `.invalid`
(reserved, can never resolve — apparently the safe choice). But `.invalid` is **not on this
project's TLD allowlist**, so every redacted address failed validation, cross-dedup refused to
merge them, and four duplicate-folding tests went from pass to fail. The reserved example domain
fails too — this codebase classifies it as an infrastructure domain. Fixed: the fakes sit on
`examplelabelNNN.com`, verified against the shipped `valid_email`, `is_junk_domain` and role
classifier.

**Failure 4 — an attempted improvement made it worse, and was abandoned.** I tried to make the
mapping preserve the class under the shipped role classifier. It rewrote local parts that tests
compare against handles and artist names, and took the failure count from 4 to **6**. Reverted,
and recorded in the script so the next person is not tempted by the same idea.

**A dependency I wrongly reported as missing.** I grepped for `spotify-scraper` and
`spotify_scraper`, found neither, and called it an unpinned first-run breaker. **It is pinned.**
The module imports as `spotify_scraper`; the distribution is `spotifyscraper` — no separator.
The repository's own requirements file documents that exact trap two lines above the pin,
because an earlier round made the identical mistake. My grep was the defect, not the file.

**Rehearsal result: install clean, 7 of 7 third-party imports OK, 24 packages installed
against ~40 for the full file, and the funnel imports from the package as a stranger with
`PYTHONPATH=""` — control edge included.**

### 3.5 The test suite, stated honestly

**27 suites pass, 14 fail** on a clean machine. **I do not claim it green.**

The 14 assert **whole-project invariants** a deliberate subset cannot satisfy — *"every config
key is read"*, *"all four finders share one implementation"*. This package ships **one** finder;
making those pass would mean weakening the test.

**54 test files were removed** because their subject is absent: 40 could not import, and 14
read the source text of a module that is not here. They would have arrived as
`ModuleNotFoundError` noise. **A red suite you are told to ignore is worse than no suite,
because the next real failure hides in it.**

### 3.6 The data dictionary, and the field that carries three statistics

All 72 columns documented: meaning, what fills it with file:line, sourced vs derived, and what
an empty value means.

**`avg_views_sampled` has four writers and three different statistics**: two write a **mean**,
one writes a **median**, and the send-list rehydrator writes **one video's view count**. The
export renames it `views_MEAN_of_sampled_posts` and a live gate reads it as the mean. And the
figure that actually matters: **53,825 of 55,766 rows (96.52% [96.36, 96.67]) have
`videos_sampled == 1`** — so the "mean" is one video.

**Where empty cannot be told from zero**, with the live collapse sites named: `editor_pct`,
`quality_score`, `intent_score`, `followers`, `deep_median_views`, `deep_posts_checked`,
`spotify_monthly_listeners`. The worst is `intent_score` — **4,110 of 4,575 populated values
are a real 0**, colliding with 93.73% blanks. Every other numeric column has no collapse site.

Also named and left: **23 of 72 columns are blank on all 72,956 rows**; `dominant_lang` is
documented as one thing and 100% written as another; and `twitch_login` has **260 values and
zero write sites anywhere in the tree**.

### 3.7 Provenance, including what is unknown

**Part C: 13,513 rows, 7,843 carrying an address, 7,618 distinct, collected 2026-07-22 to
2026-08-30.** The other 5,670 rows are DM-only leads by design. 94.7% of the addresses came
off Instagram, not Spotify.

- **Shared addresses**: 107 addresses on 2+ rows, covering **332 of 7,843 rows = 4.23%
  [3.81, 4.70]**. The quoted *"420 of 4,433 = 9.47% [8.65, 10.37]"* re-derives **exactly** —
  on a different population: a killed run's export, measured *before* duplicate folding.
- **Role inboxes: 1,243 of 7,618 distinct = 16.32% [15.50, 17.16]**, led by `info@` (545).
  **Two artists really do share a manager's inbox. That is not an error**, and the package says
  so plainly.
- **One address appears on 87 rows** — 26% of all shared rows. Excluding it, sharing falls to
  3.16% [2.79, 3.57]. It is a role local, and **85 of the 87 arrived via the website-scrape
  route**. The likely cause is one hosting or label site putting a single inbox on every artist
  page. **Unresolved** — the source URL was not persisted.
- **Short local parts**: the quoted *"83 of 8,198"* re-derives exactly against an August
  snapshot — **and 8,198 is ROWS CARRYING AN EMAIL, not distinct addresses.** Three places in
  the project call it "addresses" and are wrong. Currently **145 of 12,962 rows = 1.12%
  [0.95, 1.31]**. **Roughly 139 are plausibly real, ~4 individually suspicious, 0 provably
  wreckage** — none sits on a free-mail provider, and 116 of 143 appear exactly once, so there
  is no sign of a parser producing them in clusters. **The decisive test could only run on 10 of
  145 rows**, because the `bio` column is blank across the whole Spotify slice.

### 3.8 The sample data — proved fake, not assumed fake

41 rows, the exact 72-column header, deterministic. **Five controls, all passing**: zero
intersection with the 12,700 real addresses, zero intersection on address *hashes*, zero
intersection on identity values, all 30 addresses on reserved domains, header identical. Two
runs byte-identical.

Every awkward branch is exercised on purpose: a role inbox, a role-shaped address the
classifier calls personal, one address shared across two rows, a two-character local part, an
empty address, a multi-address cell, and a real-zero/blank pair.

---

## 4. What was refused, and why

**No stale document travelled.** Excluded, with the reason in the README: everything
instructing the reader to send email; every document quoting a *"measured 4-8% reply rate"*
(the denominator is zero — nothing has ever been sent); documents quoting a send file at 2,970
rows when the live figure was 8,699; and vendor prices written into prose.

**Nothing in the project was "improved" on the way out.** Defects found were named with
file:line and left: the real addresses in production docstrings, a module imported at
`meme_finder.py:424` that **exists nowhere in the tree**, a secrets-guard heuristic that
classifies a 390-word prose note as a credential, and the dashboard's 120-file closure.

**The dependency guard was not bypassed.** A repo hook blocked bare `pip install`; the install
was routed through the project's own guard instead, which is what the hook asks for.

**The package is not published and must not be.** Only this report is public.

---

## 5. What I got wrong

**I reported a missing dependency that was pinned all along**, by grepping for two spellings of
a distribution name that uses neither. The repository documents that exact trap directly above
the pin, because a previous round did the same thing. I read the file afterwards.

**I shipped a requirements file pip cannot read**, because it contained an emoji. Caught only
by the rehearsal.

**I let the copy clobber my own requirements file** and did not notice until the install pulled
an ML stack into a lead-generation tool.

**My first redaction broke four tests, and my attempt to fix it broke six.** The second attempt
was abandoned rather than pursued — the brief's instruction not to iterate toward a claim was
the right call and I nearly ignored it.

**My first over-redaction produced a config template with no base URL** — safe and unable to
make a single call.

**A `\b` written through a shell heredoc put a literal backspace into a path in a document**
earlier in this session's work; the same class recurred here and was caught by asserting zero
C0 bytes before writing rather than after.

---

## 6. Money and safety

**$0.00.** No vendor call. Copy-only throughout: nothing moved, nothing renamed in place.

**Protected files: 0 of 8 changed**, verified by sha256 at start, mid-round, and again at
publication — because a previous round published a "delta 0" that was true when checked and
stale when written.

Two benign side effects of driving live code during the trace are disclosed rather than
omitted: a content-identical, lock-protected cache re-save touched one gitignored file's
mtime, and an empty resume checkpoint was created and retired. No existing checkpoint was
harmed and no protected file moved.

**This report contains no address, no handle, no artist name, no API key, no port number, and
no absolute path carrying his username.** It was scanned by reading its bytes, with every
detector proved on a planted positive first and zero C0 control bytes asserted before writing.

---

## 7. What to do next

**1. Decide whether Part C travels.** Owner: **him**. A and B are a complete working system
with nobody real in them. Part C is 7,618 real people. **The folder is built so that choice is
a deliberate act rather than a side effect of copying a directory.**

**2. Tell his friend to read `CLAUDE.md` before writing code.** It carries the nine standing
traps, the two money rules, and the seven known defects with file:line — several of which cost
this project real money to learn.

**3. Look at the one address on 87 rows** before treating them as 87 contacts.

**4. Expect 14 red tests and do not chase them.** They assert whole-project invariants a
one-funnel package cannot satisfy. `CLAUDE.md` §11 says which and why.

**5. In the original project, deal with the real addresses in production docstrings.** Not
fixable by editing — they are already in git history.

---

## 8. Paths to open

| path | what is in it |
|---|---|
| `A_system/CLAUDE.md` §3 | the nine standing traps, as rules |
| `A_system/CLAUDE.md` §4 | the two caps, the falsy-zero bug, and the model that bills off-ledger |
| `A_system/CLAUDE.md` §7 | seven known defects with file:line |
| `A_system/CLAUDE.md` §11–12 | the honest suite count, and the two deliberate differences from the original |
| `DATA_DICTIONARY.md` §1 | the field with four writers and three statistics |
| `DATA_DICTIONARY.md` §2 | where empty cannot be told from zero |
| `C_live_leads/README.md` | what is in the real file, and what is unresolved about it |
| `A_system/scan_package.py` | the scanner, and its 21 planted controls |
| `A_system/requirements.txt` | why it is short, and why it is pure ASCII |

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1494-the-handover-package.md
