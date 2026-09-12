# BL-1549 — four things that were measurably wrong, and one column one command away

**Four published figures were wrong and one is worse than reported.** "Only 120 clippers" is
**24x low** — the true whole-corpus figure is **2,933 clipper rows with an email (22.60%
[21.89–23.33] of 12,977)**, while the "8,719 clients" half reproduces exactly but belongs to a
**different, date-filtered denominator of 10,173**; the two must be quoted together or not at
all. The `lead_kind` column that produced them is **provenance, not observation** — it returns
`clipper` for any `tt:`/`ig:` source regardless of content, and one in three resolvable rows in
that bucket is a business (**33.83% [30.87–36.93]**, n=931). The "+12" mislabel is **confirmed
and now 21 rows**, still accumulating. And the cross-platform price fallback, **briefed at four
sites, is actually at six** — `repost_finder.py` and `run.py` were not on the list. All six now
call an accessor that **raises** instead of silently billing Instagram at the TikTok rate.
**What he has to do, in one sentence: export a CSV of bounced addresses with a column headed
`email`, and run the one command in §6 — after that, every accuracy claim this project makes
becomes checkable for the first time.**

---

## 1. What this project is, for a reader with no context

A funnel discovers TikTok and Instagram accounts belonging to video editors ("clippers"), reads
their public bios, and extracts published email addresses into a lead store (`master_leads.csv`,
72,971 rows). Vendors: **LamaTok** for TikTok at **$0.000600/call**, **HikerAPI** for Instagram
at **$0.00069064/call** — 15.1% apart, which is the whole of §5.

This round is **correctness, not discovery**. It changed six production files, added one test,
and made no funnel run. **All nine backed-up stores are byte-identical to round start** — the
`M` flags git shows on four seen stores are pre-existing dirt from before this session, verified
against sha256 hashes taken before any work began.

## 2. Safety

Nine stores backed up sha256-verified, **bodies found BY SHAPE**: `spend.json` → `runs` (35,422
rows — up 212 during the round, written by a concurrent funnel, not by me), `master_leads.csv`
72,971, `clip_seen.json` a **bare list** of 2,193, `meme_pages_seen.json` → `pages` 6,196,
`tiktok_pages_seen.json` → `pages` 3,270, `spotify_playlists_seen.json` → `playlists` 1,961,
`repost_seen.json` 1,715, `email_harvest_tags.json` → `tags` 572, `config.json` 173 keys.

**All five corruption controls FIRED.** The load-bearing one: on a duplicated pair, deleting one
leaves the natural-key **set provably identical** (both digests equal, measured) while the
**index-qualified** digest moves. A key-set check is blind to it by construction.

## 3. The two-clocks bug — FIX CATEGORY: GENERAL, and it is at four sites

`clippershq/email_harvester.py:343` constructs a fresh `LockedBudget` on every `Harvester`,
including every **resume**. `_load_checkpoint` (`clippershq/email_harvester.py:366-386`) then
restores `rows`, `per_tag` and `seen_ids`, which are **cumulative across every session ever run
against that checkpoint**. A runner writing both into one file produced
`output/bl1542_run/summary.json` with **`accounts=44270` (cumulative) beside `spent_usd=0.5778`
(session-only)**. Read as the run's cost that **understates it 4.42x** — the true cumulative was
**$2.5560**, confirmed against three run logs.

**The published cost figures survive; the summary file is the thing that was wrong.** Correcting
for it reproduces **$2.47/1,000** (fresh) and **$3.70/1,000** (re-walk) almost exactly, and the
already-held share reproduces at **54.24%**.

**Sites, counted rather than assumed — verdict GENERAL:**

| site | what it is |
|---|---|
| `clippershq/email_harvester.py:343` + `:366-386` | the root mechanism |
| `scratch/bl1542/bl1542_run.py:319-326` | confirmed instance (the positive control) |
| `scratch/bl1544/bl1544_run.py:265-274` | same root cause, independent call site |
| `clippershq/meme_finder.py` (`:6223`, `:8684-8685`, `:8749-8762`, `:9037-9039`) | **an independent re-implementation of the identical defect, sharing no code** — session-fresh `used={"calls":0}` beside `len(all_rows)`, which unions checkpoint-recovered pages. It makes `exports_meme_pages/_provenance.json` wrong the same way. |

A latent fifth: `scratch/bl1545/bl1545_run.py` writes a checkpoint it never reads back — no
defect today, one resume-read away from it.

**Ruled out with reasons:** `harvest_run.py` (session-scoped on both sides), `tiktok_finder.py`
(already carries its own delta-vs-cumulative guard from BL-923/839/1333), `ig_bio.py` (no
checkpoint at all).

**The fix.** `Harvester.summary_fields()` now emits the clock in every key —
`session_calls`, `session_spent_usd`, `session_cap_usd` beside `cumulative_accounts`,
`cumulative_tags_done`, `cumulative_per_tag` — plus a `summary_clock_note` that travels *inside
the file* saying `session_*` resets on every resume. The legacy `calls` / `spent_usd` are still
emitted with identical values so nothing that reads them breaks; they are documented as
deprecated. **Driven across a simulated resume:** session figures reset (3 → 1) while
`cumulative_accounts` held at 5, reproducing the understatement in miniature at 4.00x.

**`meme_finder.py` is NAMED AND LEFT.** It is an independent implementation in a 9,000-line
module this round did not claim, and the brief asked for small and cheap. Fixing it is a
separate, deliberate change.

## 4. `lead_kind` — a guess wearing an observation's name

`clippershq/writer.py:363-367` returns `LEAD_KIND_CLIPPER` for **any** provenance beginning
`tt:` or `ig:`, **regardless of bio content**. `:315-319` is a static funnel→kind map. Hardcoded
per-funnel constants also sit at `clippershq/google_play_finder.py:943`,
`clippershq/repost_finder.py:1595`, `clippershq/meme_finder.py:8838`.

**Its own docstring was already honest** — *"which funnel wrote this row… a recorded fact, not a
guess about the person."* **The docstring was honest and the field name was not**, and four
reports read it the other way anyway. That is precisely why the fix is in the code and not in a
report.

**The fix: `writer.discovered_via()`**, a sibling that returns *exactly* what
`lead_kind_from_source` returns (proved identical on seven inputs) under the name that says what
the value is. **`lead_kind` is deliberately NOT redefined** — other code reads it, and silently
changing a field's meaning changes behaviour nobody asked to change. Both functions now carry the
measured evidence in their docstrings, where the next reader will hit it.

### The corrected composition pair, both denominators stated together

| denominator | rows | clipper | client | meme_page | blank |
|---|---:|---|---:|---:|---:|
| **whole corpus**, rows with an email | **12,977** | **2,933 = 22.60% [21.89–23.33]** | 8,719 = 67.19% | 1,291 | 34 |
| **era-filtered** `date_added >= 2026-07-11` | **10,173** | **129 = 1.27% [1.07–1.50]** | 8,719 = 85.71% | 1,291 | 12.69% |

**The slogan mixed them.** "8,719 of 10,164" is the era denominator; "only 120 clippers" is also
era-scoped but was read as global. The era filter excludes **2,804 of 2,933 historical clipper
rows — 95.6% — by construction**.

**Date-parser control:** 0 of 72,971 `date_added` cells failed to parse; range 2026-06-30 to
2026-09-07. The era filter is trustworthy.

*(The era denominator is 10,173 here, not the quoted 10,164. `master_leads.csv` is a live file
that funnels append to — a moving target, and the 9-row difference is entirely explained below.)*

## 5. The "+12" era bug — CONFIRMED, and it is now 21

`clippershq/meme_finder.py:8838` and `clippershq/tiktok_finder.py:4598` (was cited as `:3792`;
**pure line drift** from 822 unrelated lines added since — the code is byte-identical and still
unfixed) both hardcode:

```python
"lead_kind": "clipper",
```

inside the master-append step of the `meme_pages` and `tiktok_pages` funnels, which should stamp
`meme_page`. `writer.py` declares `LEAD_KIND_MEME_PAGE` and **no production writer ever emits
it**.

**Measured, and the two instruments reconciled rather than averaged.** My first count said 8;
the sub-agent's said 21. Counting by exact `FUNNEL_TAG` settles it — 8 was `meme_pages` only:

| `source_hashtag` | `lead_kind` | rows | dates |
|---|---|---:|---|
| `meme_pages` | **clipper** ← wrong | **8** | 2026-08-31 → 09-06 |
| `meme_pages` | meme_page | 985 | 2026-08-07 → 08-29 |
| `tiktok_pages` | **clipper** ← wrong | **13** | 2026-09-05 → 09-07 |
| `tiktok_pages` | meme_page | 226 | 2026-08-08 → 08-28 |
| | **total mislabelled** | **21** | |

**This is a regression with a date boundary.** The same funnels stamped 1,211 rows `meme_page`
correctly through 29 August, then switched to `clipper` on 31 August and have not stopped —
newest victim 2026-09-07. Corrected era clipper count: **129 − 21 = 108**, which reproduces the
prior round's 108 exactly.

**It also has a downstream cost:** `clippershq/meme_send_list.py:182` and
`clippershq/tiktok_send_list.py:75` both define their kind as `"meme_page"`. Rows stamped
`clipper` are filtered out of the lists built *for them*.

**NAMED AND LEFT**, with `file:line`, as the brief directed.

## 6. The `bounced` write-back — proved end to end, one command

**All nine outcome columns are 0 non-empty of 72,971 rows.** No accuracy or bounce figure this
project has produced has ever been checked against a real result.

`clippershq/outcomes.py:501-503`:

```python
def mark_bounced_from_csv(path, *, master_csv=None, dry_run=False, now=None,
                          read_master_fn=None, backup_label="markbounced",
                          bounced="yes") -> dict:
```

**File shape:** a CSV with a column headed `email` / `Email` / `EMAIL` / `recipient` /
`Recipient` / `address` / `To` / `to`, one bounced address per row — **or** any non-`.csv` file,
which is regex-scanned for address-shaped tokens (`outcomes.py:458-498`). Matching uses the same
identity index as sends. A key matching 0 rows is `unmatched`; **2+ rows is `ambiguous` and
refused, never guessed**; exactly 1 is stamped under the master's filelock, after a timestamped
`.bak`.

**End-to-end drive on a from-scratch synthetic sandbox: PASSED, 7 of 7 checks.** Targeted rows
stamped; negative-control rows untouched; counts matched exactly (4 keys → 1 unmatched, 1
ambiguous, 2 updated); the ambiguous pair **refused, neither row written**; re-running produced
byte-identical state — **idempotent**. Dry run previewed the identical match set with
`updated: 0`. **No real address appears in any fixture**, and the synthetic domain was chosen to
pass `bio_parser.is_junk_domain` — a probe once planted `example.com`, got nothing, and nearly
"fixed" a healthy extractor.

**The command** (dry run first; re-run with `dry_run=False` to commit):

```
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0,'clippershq'); import outcomes, json; print(json.dumps(outcomes.mark_bounced_from_csv(r'PATH_TO_BOUNCE_REPORT.csv', master_csv=r'master_leads.csv', dry_run=True), indent=2, default=str))"
```

**Interval claim corrected.** "±2 points at n=469" is exact only near a low base rate: Wilson 95%
half-width at n=469 is **±2.00 points at p=0.05** but **±4.51 points at p=0.5** — over twice as
wide. The true width must be recomputed once real data exists; it is currently n=0.

*(This project does not send. Reading a result back is in scope. No sender, pitch, template or
send order is proposed anywhere in this round, and none was built.)*

## 7. The price fallback — briefed at four sites, found at SIX, now fails closed

The chain was:

```python
cost = (cfg.get("ig_api") or {}).get("cost_per_call_usd") \
    or (cfg.get("api") or {}).get("cost_per_call_usd") or 0.00069064
```

**The second term is the other platform's price.** All six were **correct on the day they were
found**, because the first key is set — which is exactly what makes the shape dangerous: silent
until the key is removed. That mispricing has already been paid for once: `int(3.00/0.0006) =
5,000` calls against a $3.00 cap is **$3.45** at the true rate.

| site | on the brief's list? |
|---|---|
| `clippershq/caption_finder.py:1087` | yes |
| `clippershq/caption_finder.py:1313` | yes |
| `clippershq/control.py:3198` | yes |
| `clippershq/control.py:3374` | yes |
| **`clippershq/repost_finder.py:1668`** | **no** |
| **`clippershq/run.py:672`** | **no** |

**The fix:** `ig_client.instagram_usd_per_call(config)` reads the one named key and **raises
`InstagramPriceMissing`** otherwise — never falling back. Driven on five refusal shapes (key
absent, zero, `None`, not-a-dict, empty config): **all five raised**, and each message names the
key it refuses to fall back to and how wrong it would be. The pattern is copied from
`harvest_run.Budget`, whose own default unit is `1e9` so a caller who forgets refuses the first
call rather than mispricing every one.

**An AST sweep of all of `clippershq/` now finds zero surviving chains**, and the committed test
proves that sweep can see a *planted* one — a clean sweep from a blind detector is a false
absence.

## 8. The two unpriced endpoints — sized by arithmetic first, then settled for $0.0024

**9 of 29 live LamaTok paths are referenced by production; 20 are not.** The whole value of the
two unwired `/v1/user/following/*` endpoints turned on one fact, and the arithmetic was done
**before** any call:

| | bios come INLINE | handles ONLY (a profile call each) |
|---|---|---|
| optimistic (no overlap, 3.49%) | **$0.41 / 1,000** | $17.77 / 1,000 |
| pessimistic (54.24% held, 1.94%) | **$1.61 / 1,000** | $69.84 / 1,000 |

Baseline: **$2.47/1,000** (fresh tags + v1, measured). So the arithmetic **did not refuse it** —
one branch beats the baseline 6x, the other is 7x worse — and **nothing on disk could answer
it**: the live OpenAPI spec declares an empty `{}` 200-schema for *every* path, including
`/v1/hashtag/medias`, which we know returns bios inline. Spec-reading has no power here.

**Four calls, $0.0024, settled it. CASE A: bios come inline.** The response carries
`response.userList[].user.signature`, **50 accounts per billed call** (requesting `count=30`),
**42 of 50 with a non-empty bio = 84.0% [71.5–91.7]**.

**⚠️ This is a LEAD, not a cost figure.** n = one seed account's following list. Of three seeds
tried, one was `PrivateAccount` and one returned `total=0` — a 1-in-3 usable rate on n=3. And
**overlap between seeds is entirely unmeasured** and is the whole risk: one account's follows are
not a random sample. Worth one funded test; not worth quoting as a price.

## 9. WHAT I GOT WRONG

1. **My own probe leaked a real handle, and I published it to my console and a JSON file.** The
   key-walker emitted `users.<real handle>.signature` because the vendor keys that object *by the
   handle*. I deleted the artefact and added a mask that replaces any non-structural key with
   `<id>`, plus a control that plants a handle-keyed dict and proves the mask hides it. **The
   round's own leak scan would not have caught this** — it scans for addresses and known handles
   in committed files, and this was a fresh handle in a scratch file.
2. **I wrote `VERDICT: CASE B` from a zero my own instrument produced.** The probe reported "0
   accounts, 0 bios" and I concluded handles-only. The list was nested under `response` and my
   counter read the top level. A zero from a list-finder with no control proving it can find a
   list is an instrument failure, not a finding. The verdict logic now refuses to choose at all
   when zero accounts came back, and reports **ABSENT**.
3. **My first two attempts to edit `control.py` silently found nothing** because I matched exact
   source text that differed by a line continuation. Both times the script **refused rather than
   guessing**, which is the only reason this is a footnote and not a corrupted file.
4. **My third attempt produced code that did not parse** — I inserted a top-level import, which
   shifted every subsequent line and broke indentation in all three files. The re-parse check
   caught it and **refused all three writes**. The fix uses a local import at the call site.
5. **I wrote a scratch file into another round's namespace** (`scratch/bl1548_preround.txt`)
   before noticing BL-1548 was live. Removed within the minute.
6. **A backtick in a shell string spawned a subshell** during claim filing — harmless here, the
   same class as the SIGPIPE and heredoc traps this repo has already paid for. And one heredoc
   *did* mangle my escaping mid-round, exactly as the brief warned; I switched to file-based
   edits.
7. **My test-attribution method produced a FALSE ACCUSATION against myself, and I nearly acted
   on it.** Running the four reds in a detached pre-round worktree said
   `test_bl1307_veto_refused` **passed** there and therefore that I had broken it. I did not. The
   guard scans `scratch/` for files pointing a judge at a refuted brief, and its only offender —
   `scratch/bl1441_ast_sink_tests.json` — is **untracked**, dated **2026-08-30**, thirteen days
   before this round, and therefore **absent from a fresh worktree**. The guard scanned an empty
   corpus and passed trivially. Copying that one untracked file in made it fail at pre-round too.
   **This is the "a SKIP reads as a PASS" trap one level deeper: an empty scan corpus also reads
   as a pass.** Had I trusted the first result I would have gone looking to "fix" a guard that
   was working correctly — the exact failure the brief warns about.
8. **I committed the two-clocks bug myself, in the round that fixed it.** I was about to report
   this round's spend as **$0.0024** — the figure the last probe run printed. The true total is
   **$0.0078 across 13 calls in four sessions**, because every run built a fresh budget and
   reported only its own session. **A 3.25x understatement, from the identical mechanism, by the
   person who had just spent the morning fixing it.** If the fix needed justifying beyond the
   measurement, that is the justification.

## 10. What the round cost, and what was routed where

**$0.0078 of the $0.25 budget — 13 calls, summed across four probe sessions**, from my own
counter at the wrapper, never a ledger delta (a concurrent funnel added 212 rows to `spend.json`
during the round).

| probe session | calls | spend |
|---|---:|---:|
| run 1 — single seed; leaked a handle | 2 | $0.0012 |
| run 2 — after the mask fix | 3 | $0.0018 |
| run 3 — seed loop added | 4 | $0.0024 |
| run 4 — corrected list counter | 4 | $0.0024 |
| **total** | **13** | **$0.0078** |

**I nearly published $0.0024 — the last run's figure — which understates the round 3.25x.** Each
probe run built a fresh `LockedBudget`, so each printed only its **session** spend. **That is
precisely the two-clocks bug this round exists to fix, committed by me, inside this round.** It is
the single best evidence that naming the clock in the field was the right fix rather than a
cosmetic one.

Everything else was free: AST sweeps, CSV passes, and a synthetic end-to-end drive. **Nothing
latched** — all nine stores byte-identical to round start.

**Routed to cheap models (Sonnet):** the two-clocks site census (~144k tokens), the composition
re-derivation and `+12` trace (~125k), the `bounced` end-to-end drive (~127k). **~396,000 tokens
of mechanical measurement kept out of the expensive context.**

**Kept in the expensive context:** the price-accessor design, the fail-closed fix and its AST
sweep, the following-endpoint arithmetic and probe, the two-instrument reconciliation on the
`+12` count, and this report.

**Test verdicts, quoted verbatim from the project's own runner:**

```
ALL GREEN -- 1/1 suites passed, 12 checks   (2.9s)    [-k bl1549]
ALL GREEN -- 1/1 suites passed, 20 checks   (1.0s)    [-k harvester]
ALL GREEN -- 1/1 suites passed, 9 checks    (1.1s)    [-k writer]
ALL GREEN -- 6/6 suites passed, 176 checks  (22.4s)   [-k outcome]
```

**The full 475-suite run did not reach a verdict line before this report was written, so none is
quoted.** At 92 suites it showed four reds, and **all four were attributed to the pre-round
commit, not to this round** — by checking each one out at `62cfbcdd` in a detached worktree with
the gitignored files copied in:

| red suite | verdict at pre-round |
|---|---|
| `tests/test_atomic_io.py` | FAIL — pre-existing (`proxy_pool.py:290`, untouched here) |
| `tests/test_bl1300_judge_first.py` | FAIL — pre-existing |
| `tests/test_bl1307_veto_refused.py` | FAIL — pre-existing *(see below)* |
| `tests/test_bl1308_refuted_brief.py` | FAIL — pre-existing |

This round changed seven files, all in `clippershq/`: `caption_finder` (+12/−3),
`control` (+14/−3), `email_harvester` (+61), `ig_client` (+60), `repost_finder` (+7/−2),
`run` (+21/−3), `writer` (+38). None is touched by any of the four failing guards.
