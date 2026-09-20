# BL-1575 — The re-buy surface: 77,353 accounts' bios owned and unused, $47 to re-buy, 26 usable

**Round:** BL-1575 · **Read-only census.** · **Spent: $0.00** — `spend.json` sha256 `4edc0802cd…` /
16,043,805 bytes at start and at close, byte-identical; no vendor call. · Nothing built, merged,
written or deleted; **no test suite was run** (BL-1574 §5: running them writes live stores). ·
Paths redacted: `<PROFILE>` is the user folder, everything else repo-relative.

## The paragraph

**This system owns bios for 77,353 accounts that master does not hold — 66,147 of them real
bios (85.51% [85.26–85.76]) — and has never used one of them.** The brief's 142,514 was not
wrong on the join key (casing and `@` move zero rows; secUid and normalised handle agree to the
row); it was a *sum over files* — the same account sits in `checkpoint.json` and `rows.jsonl` of
the same run, and across runs — and the **union is 77,353** (sum 159,008, overlap 81,655).
Re-buying them all would cost **$46.63** (68,001 TikTok × $0.00060000 = $40.80; 2,393 Instagram
× $0.00069064 = $1.65; 6,959 platform-unevidenced at the TikTok unit = $4.18) — **a ceiling,
not a refund**: the buy paths only ever fetch bios for *addressed* rows, and the addressed
orphans are 3,676, of which 3,095 are already on his workbook (their bios were bought back for
$1.51 in BL-1569 while sitting free in these files — that is the real avoided cost, ~$1.9) and
**581 are in neither store**. Of those 581, **26 pass the craft cut** (4.48% [3.07–6.48],
extrapolating a rule measured on 247 editor-enriched TikTok labels, 0 Instagram) and 329 cannot
be niche-judged at all. **The leak bleeding most per month is not a leak: Instagram's second
fetch, $7.35 of the last 30 days' $44.00, is inherent to the vendor** — the hashtag payload
carries no biography and HikerAPI's 154 stored paths have no bulk-user route; the fixable ones
are the tag-resolve re-pay ($0.10 to date, LOCAL, 1 site) and the bio buy-back ($1.51 to date,
GENERAL, 2 sites). **The merge should NOT go into master.** These are 74,248 unqualified,
unaddressed accounts; master is what the workbook and every send list derive from, and its write
path is an unlocked scratch append. They belong in an append-only `known_bios` store keyed by
(platform, secUid|handle) that every profile-buy site consults before spending — designed in §6,
not run.

## 1. What this project is, for a reader with no context

ClippersHQ walks TikTok and Instagram hashtags, reads creators' bios, and delivers the ones
carrying an email to one operator's workbook. TikTok's bio rides free in the hashtag payload;
Instagram's costs a profile call. Every walk keeps a checkpoint of every account it saw — bio
included — but only the addressed rows go anywhere; the rest stay in the checkpoint. BL-1574's
sweep found those checkpoints hold bios for tens of thousands of accounts master has never seen.
This round asks what that is, what it is worth, and whether it should be merged.

## 2. The census

**The join key, proved by value** (`scratch/bl1575/join_key.py`). Candidates were scored on the
same rows: (a) secUid — checkpoint `account_id` (`email_harvester.py:421` `account_id` takes
`secUid` first) against master `secuid` (filled on 56,801 rows, i.e. the TikTok rows); (b) the
handle — checkpoint `handle` (`email_harvester.py:454`, already lower-cased and `@`-stripped)
against master `tiktok_handle`, which is filled on **all 74,218 rows including the 17,210
Instagram ones** (it is "the handle", not "the TikTok handle"), and the `instagram` column.

| file | rows | secUid hits | handle raw | handle normalised | both | renames | secUid-only | handle-only |
|---|---|---|---|---|---|---|---|---|
| `output/bl1542_run/checkpoint.json` | 44,270 | 4,828 | 4,592 | 4,594 | 4,556 | 1 | 272 | 38 |
| `output/bl1544_run/checkpoint.json` | 26,897 | 1,269 | 1,253 | 1,253 | 1,215 | 0 | 54 | 38 |
| `output/bl1545_run/checkpoint.json` (Instagram) | 2,125 | 13 | 87 | 87 | 12 | 0 | 1 | 75 |
| `output/bl1541_run/rows.jsonl` | 1,842 | 320 | 314 | 314 | 307 | 0 | 13 | 7 |
| `scratch/bl1569/fetch_ckpt.json` (no secUid) | 2,722 | 0 | 1,111 | 1,111 | — | — | — | 1,111 |

Where both keys hit, the handles agree in 6,079 of 6,080 (one rename). **Casing and `@` change
nothing:** master's 74,200 distinct raw handles are 74,200 distinct normalised ones, and
normalised-but-not-raw hits are 0 on every file. So the key is **secUid for TikTok with the
normalised handle as fallback; normalised handle (+platform) for Instagram**, and it is not
case- or `@`-sensitive on this data — the code normalises anyway. The orphan count does **not**
collapse on the key; it collapses on the *union* (below). Master itself carries 18 duplicate
handles (74,218 rows, 74,200 distinct).

**Per file** (the five principal ones of 197; `scratch/bl1575/census.py`, checkpointed per
file; platform from the source's own evidence — a `MS4w…` secUid / TikTok author fields, or
the row's own `platform` field on the BL-1545 walk; `lead_kind` and `verdict` were not used —
`writer.py:335-435` `lead_kind_of` returns CLIPPER for any `tt:`/`ig:` provenance and says so at
`:388`):

| file | written | rows | bio present / empty / unknown | orphans vs master | orphan bios | addressable | master holds, no bio | platform |
|---|---|---|---|---|---|---|---|---|
| `output/bl1542_run/checkpoint.json` | 2026-09-10, BL-1542 | 44,270 | 39,003 / 5,267 / 0 | 39,404 | 34,378 | 836 | 220 | TikTok |
| `output/bl1544_run/checkpoint.json` | 2026-09-11, BL-1544 | 26,897 | 23,690 / 3,207 / 0 | 25,590 | 22,438 | 649 | 33 | TikTok |
| `output/bl1545_run/checkpoint.json` | 2026-09-11, BL-1545 | 2,125 | 1,551 / 126 / **448** | 2,035 | 1,473 | 88 | 25 | Instagram |
| `output/bl1541_run/rows.jsonl` | 2026-09-10, BL-1541 | 1,842 | 1,614 / 228 / 0 | 1,515 | 1,310 | 56 | 25 | TikTok |
| `scratch/bl1569/fetch_ckpt.json` | 2026-09-17, BL-1569 | 2,722 | 2,552 / 31 / **139** | 1,610 | 1,532 | 1,502 | 0 | TikTok |
| 192 other files (August judge/corpus files, probes) | 2026-08-08..09-12 | — | — | — | 5,016 | — | — | mostly unevidenced |

**The failed-fetch distinction.** The harvest checkpoints carry `bio_state` from
`email_harvester.classify_bio:430` — `present` / `empty` (served, genuinely blank) / `unknown`
(field absent: torn or unserved) — and the BL-1569 buy-back carries `kind` = bio / empty_bio /
fetch_failed. On the two TikTok walks the unknown count is **0** (the bio rides in the payload,
so a served item always has the field); BL-1545's Instagram walk has 448 unknown (21.1%) and the
buy-back 139 (5.1%, its own "fetch_failed"). An orphan with `bio_state != present` is **not**
"no bio" and was not counted as one anywhere below.

**Sum versus union.** Per-file orphans sum to **159,008**; deduplicated by the proven key the
union is **77,353**; overlap **81,655**. Most of the overlap is trivial — every run wrote both a
`rows.jsonl` and a `checkpoint.json` with the same rows — and the rest is the same account
seen by more than one run (the buy-back's 86 already-in-union rows, for instance). The
**sweep's 142,514 was this sum**, re-run this round against live master and unchanged (199
files, 1,281 bio-less, 142,514 unheld — identical to BL-1574, so master did not move).

**Against both stores.** 3,105 of the 77,353 are on his workbook (Profile-link + Instagram
handles, 2,955 distinct); **74,248 are in neither master nor the workbook**.

## 3. What it is worth, and what is usable

**Units, by named key:** `config.json` → `api.cost_per_call_usd` = **$0.00060000** (TikTok,
LamaTok) and `ig_api.cost_per_call_usd` = **$0.00069064** (Instagram, HikerAPI; 15.1% above
TikTok, TikTok 13.1% below). The re-buy route is one profile call per handle
(`api_client.py:519` `user_by_username` / `ig_client.py:974`).

| set | TikTok | Instagram | unevidenced (at TikTok unit) | total |
|---|---|---|---|---|
| every orphan handle (77,353) | 68,001 × $0.0006 = **$40.8006** | 2,393 × $0.00069064 = **$1.6527** | 6,959 × $0.0006 = $4.1754 | **$46.63** (at the IG unit for the unevidenced: $47.26) |
| orphans with a real bio (66,147) | 59,658 × $0.0006 = $35.7948 | 1,473 × $0.00069064 = $1.0173 | 5,016 × $0.0006 = $3.0096 | **$39.82** |

Second derivation in integer 1e-8 units: 68,001 × 60,000 = 4,080,060,000 → $40.8006; 2,393 ×
69,064 = 165,270,152 → $1.65270152. **This is a ceiling, not a refund** — it is what fetching
these bios again would cost, and it is only real for handles a future run would actually fetch.
The buy paths fetch bios for *addressed* rows only (`bl1572_buy.py:78` skips a row that already
has a bio; the target set is rows with an email and no bio). So the part of the ceiling that has
ever been spent is the buy-back of bios the walks had already received: BL-1569's 2,522 calls,
**$1.51**, against 3,095 addressed orphans that are on the workbook — **~$1.9 at most is the
real avoided cost**, and $1.51 of it has already been paid.

**The funnel, over the union** (denominator named at every step; craft = `editor_gate.bio_rule`
(`editor_gate.py:158`), the rule `bl1572_cut.py:137-143` applies; addressable =
`bio_parser.extract_emails` (`bio_parser.py:483`, with `valid_email` at `:245`) re-run on the
stored bio, agreeing with the stored `has_email` on 1,629 of 1,629 harvest rows; on-niche =
`quality_gate._free_niche` (`quality_gate.py:1181`) against every campaign's `ig_niche_keywords`
/ `off_niche_keywords`, true if any campaign reaches its `ig_niche_min_pct` with no dominating
off-niche hit):

| step | count | rate | denominator |
|---|---|---|---|
| orphans (union, vs master) | 77,353 | — | — |
| with a real bio | 66,147 | 85.51% [85.26–85.76] | 77,353 |
| on-niche by any campaign | 50,835 true / 534 false / 14,778 unknown | 76.85% [76.53–77.17] true | 66,147 |
| craft-cut KEEP (bio says the craft) | 20,693 | 31.28% [30.93–31.64] | 66,147 |
| **addressable** (bio carries a valid address) | **3,676** | 5.56% [5.39–5.73] | 66,147 |
| addressable and craft-KEEP | 685 | 1.04% [0.96–1.12] | 66,147 |
| addressable, craft-KEEP, on-niche | 630 | 0.95% [0.88–1.03] | 66,147 |
| addressable and **already on the workbook** | 3,095 | 84.19% [82.98–85.34] | 3,676 |
| addressable and in **neither store** | **581** | 15.81% [14.66–17.02] | 3,676 |
| of those, craft-KEEP | **26** | 4.48% [3.07–6.48] | 581 |
| of those, niche-unknown (bio too thin to judge) | 329 | 56.6% | 581 |

**Population caveat, stated where it applies:** the craft cut's 97.5%/22.0% figures come from
247 labels, 41.9% EDITOR, drawn from editor-targeted TikTok hashtags — editor-enriched by
construction, 0 Instagram — and measure separation, not his lead mix. Every "craft-KEEP" number
above is that rule applied to an unlabelled pile; it is an extrapolation. On the 581 net-new
addressable rows it keeps 4.48%, not 31%, which is itself evidence the pile is not the labels'
population: 446 of the 581 come from one August page corpus (`quarantine/…/bl1232/sized.jsonl`,
BL-1232's meme-page material), not from editor hashtags.

**Staleness.** The rows carry no capture timestamp; the file is the clock. 61,131 of the 66,147
orphan bios (92.4%) sit in the five principal files written 2026-09-10..17 — **3 to 10 days
old**; the other 5,016 are in August files (2026-08-08..08-30), 3–6 weeks old. Master's own bios
were captured the same way, at harvest, so the pile is no staler than the store.

**What "usable" actually is.** After the funnel: **581 addresses the operator has never
received, sitting in files this system already owns, 26 of them craft-KEEP** — and 20,008
craft-KEEP accounts with a bio but no address, which this project's delivery cannot use without
a second fetch (Instagram) or a DM route (neither exists).

## 4. The other re-buy leaks — confirmed or killed, by file:line

| leak | live today? | evidence | fix | $/month at the current run rate (last 30 days: $44.00 across 34,868 ledger rows) |
|---|---|---|---|---|
| **a. tag resolve re-paid on every re-walk** | **LIVE** | `email_harvester.py:648-659` `_resolve` bills one `hashtag_info` per call and returns the id to a local; `TagLedger.record` (`:379`) stores pages/authors/emails/note, **no id** (0 of 669 ledger entries carry one); `cache_hashtags.json` has 9 entries and `hashtag_resolver.resolve_hashtag` (`hashtag_resolver.py:81`) is imported nowhere in the harvester. Re-paid to date: 174 of 495 tags resolved on both endpoints = **174 calls = $0.1044** (an undercount: a re-walk on the same endpoint overwrites its ledger entry) | **LOCAL, 1 site**: `_resolve` calls `resolve_hashtag(client, tag)` and the cache is the one place | $0.10 over the ledger's 10 days ≈ **$0.31/mo** |
| **b. bio buy-back of bios already received free** | **LIVE** | five shipped profile-buy sites — `email_finder.py:249`, `harvest_run.py:452`, `ig_discovery.py:347`, `meme_finder.py:4310`, `exemplar_sheet.py:267` — and every scratch buy; none consults a checkpoint or any "known bios" set before calling (`ig_discovery.py:347`'s own comment: "no response cache … BL-1230's harvest paid it 281 times"). `bl1572_buy.py:78` skips only rows whose *master* row has a bio | **GENERAL, 2 sites**: the two vendor clients' `user_by_username` consult a `known_bios` store (§6) before the request | BL-1569: 2,522 calls = **$1.51** in the window ≈ $1.51/mo at one buy-back per month |
| **c. Instagram's second fetch** | inherent | `_probe_samples/` hashtag payload: 130 author blocks, 30 keys, **no biography**; HikerAPI's stored spec (`scratch/bl1459_hiker_spec.json`, 154 paths) has **no bulk-user route** (`user` ∩ {bulk, batch, many, ids} = ∅); the only bio carriers are `/v2/user/by/username` (`ig_client.py:974`) and the free profile page (`ig_bio.py:104`, walled) | none at the vendor; the free route is the only lever | 13,364 profile/bio calls in 30 days: **ig $7.35** (BL-1572's 10,209-call buy, BL-1560/1561 refetches) + tt $1.63 (BL-1569) — the largest line, and not avoidable by code |
| **d. wrong-kind booking** | latent (0 wrong today) | `record_aux_spend(…, ig_calls=0, tt_calls=0, cost_per_call=0.0006, ig_cost_per_call=None, …)` at `main.py:957`; **24 call sites** (22 in `clippershq/`, 2 in `tools/`; BL-1573's "20" was a truncated listing) and nothing ties a count to a vendor. The headers are still off by exactly the incident: rows sum ig **$53.983663** / tt **$16.060624**, headers ig **$55.864276** / tt **$14.426824**, Δ = +$1.880613 = 2,723 × $0.00069064 and −$1.633800 = 2,723 × $0.00060000, total $81.567744 both ways | **GENERAL, 1 site** (a vendor-typed argument in the booker); the header correction is a one-time ledger edit | $0/mo spend; a permanent $1.88 / $1.63 reporting error |

**Ranked by $/month:** c ($7.35, inherent) > b ($1.51, GENERAL 2 sites) > a ($0.31, LOCAL 1 site)
> d ($0, GENERAL 1 site). Category counts state what the code says, not that a fix works — "the
module imports" is not proof, and none of these was driven this round.

## 5. Two small truths

- **Vision is fake-on.** `clip_enabled=True` on ZHUS, PANICBABY, STRAENGE, DAYLIGHT (15
  `clip_*` keys each; ANIME15K none), `thumbnail_vision.probe()` → `False`. Turning it on today:
  `.venv\Scripts\python.exe -m pip install open_clip_torch pillow && … pip install torch
  --index-url https://download.pytorch.org/whl/cpu` (`thumbnail_vision.INSTALL_HINT`), through
  `SAFE_PIP.bat` because `requirements.txt:30` refuses an install that moves torch/numpy — about
  250 MB of wheels and 5–10 minutes; **the SigLIP weights are already on disk (778 MiB in the HF
  cache), so no model download**; nothing else changes. Not installed.
- **The unpushed commits: 686** now (684 at BL-1574 plus its two). `git diff --stat` against the
  remote branch: 7,328 files — `scratch/` 6,750, `reports/` 207, `tests/` 165, `clippershq/` 98,
  `docs/` 67, `tools/` 23, `dashboard/` 7. **At risk, existing nowhere in the vault:** the 98
  `clippershq/`, 23 `tools/`, 165 `tests/` and 7 `dashboard/` source files' current versions, and
  6,750 scratch scripts — the vault holds docs, reports, claims and the lead/bio files, not code.
  Not pushed (his call).

## 6. The merge — proposed, not run

**Does it belong in master? No.** For: master is the one store every guard, dedup and export
reads, so bios there are consulted for free by `DedupGuard.build` and the buy paths. Against:
these are 74,248 accounts with no address, no qualification and no delivery path; master is what
`all_bot_ready`, the DM lists and the workbook derive from (`writer.py:1934` onward), every
send-list stat counts `master_rows`, `backup_prune` copies the whole file before every write
(a 120 MB master means 120 MB per copy), and the write path a scratch round would use is an
**unlocked append** (`scratch/bl1564_deliver.py:159`; the locked path is
`crossdedup.append_leads` at `crossdedup.py:548` under `filelock.file_lock` at `:572`). Doubling
master with rows that fail every filter is the wrong shape. **Recommendation: an append-only
`known_bios.jsonl` store** — one record per (platform, secUid or handle, bio, bio_state,
source file, captured-at) — that the two vendor clients consult before a profile call, and that
`DedupGuard.build` can load as `extra_accounts`. Master gains rows only when an account is
addressed, through `append_leads`.

**What breaks if it went into master anyway:** the workbook (3,028 rows born from
`scratch/merge_email_files.py`, appended by hand per round, no rule in code — it would not
change, which is the divergence widening); every `master_rows` stamp — `all_bot_ready.py:444`
`count_records`, `control.py:4049`, `meme_send_list.py:257`, `tiktok_send_list.py:133` — and
`tests/test_send_list_rebuild.py:140`, already red on a stale meta `master_rows` of 72,950 against
74,218; no test hard-codes 74,218 (grep and AST: 0 hits), `docs/FACTS.md:245` stamps 72,971 as
prose; the daily `backup_prune` and the vault size.

**Collision rule.** Never overwrite an existing bio (`bl1572_buy.py` and BL-1572's guard: 0
overwrites). When two checkpoints disagree about one key: keep both records in `known_bios`
with their source and file date; the *consulting* side prefers `bio_state == present`, then the
newest file date; `empty` never replaces `present`, and `unknown` (torn/failed) never replaces
either — the census applied exactly this rule when building its union.

**Write discipline:** by header name, never position (the workbook carries `Bio source`,
`Staleness`, `Email quality` three times); any key stamped into a rec but absent from
`writer.FULL_COLUMNS` (`writer.py:39`) is silently dropped, so a new field is a column change
first; the MARK column and every MARK file untouched.

**Before anyone runs it:** the vault at `<PROFILE>/AppData/Local/ClippersHQ/vault_bl1574/` and on
D: re-verified by re-reading (`scratch/bl1574/vault.py verify`, both roots) *the same day*; a fresh
pre-write copy of any store touched; `filelock.file_lock` held around the write; a PID lock so a
phantom "killed" notice cannot start a second writer; a dry run that prints the exact row deltas
first. **How it proves itself:** master 74,218 × 75 before and after (unchanged, if the store is
separate); `known_bios` row count = union orphans (77,353) with 0 duplicate keys; every
`present` bio in the source files present in the store by sha256 of the text; workbook 3,028 /
MARK 0 unchanged; `spend.json` byte-identical; the two vendor clients driven against the store
with a planted `.invalid` handle that must be refused and a planted known handle that must not
be fetched.

## 7. Recommendation for BL-1576

**Build the `known_bios` store as a read-only derivation of these 197 files (77,353 keys, the
collision rule above), wire the two vendor clients' `user_by_username` to consult it, drive both
with planted controls, and deliver the 581 never-received addresses to him as a separate sheet
with their 26 craft-KEEP flags — no master write.**

## 8. What I got wrong

- **I patched the census through a shell heredoc once and it failed on a `\U` escape before it
  could corrupt anything** — the same trap the brief names. The edits were redone with a file
  tool; the failed patch changed nothing.
- **My first workbook path was one directory too high** (`FileNotFoundError` on the first census
  run); fixed and re-run.
- **BL-1573's "20 call sites" was a truncated listing** — the real count is 24. Corrected here.
- **The "142,514 unseen" needed no join-key rescue, but it did need a union**: I reported it as a
  count last round; it was a sum over files that each carry the same rows twice.
- **Leak scan of this report:** built from both corpora, every detector proven on planted
  `.invalid` controls, 0 leaks, 0 C0 bytes asserted before writing.
