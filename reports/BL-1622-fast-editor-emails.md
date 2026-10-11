# BL-1622: fast editor emails: 62 delivered, not 1,000; every paid source is above $10 per 1,000

## Card

| | |
|---|---|
| **1. Emails delivered / 1,000** | **62 / 1,000.** By niche: celebrities **28**, UFC/boxing **10**, movies **8**, NBA **8**, other sport **4**, anime **2**, F1 **2**. Football, tennis, WWE and cars: **0**. |
| **2. Minutes from paid start to delivered** | **35 minutes**: paid start 16:14:29, workbook written 16:49:26. |
| **3. $ total, $ per 1,000 emails** | **$1.52 of $10.00** (LamaTok $0.94 + OpenRouter $0.58, of which $0.52 was judge calibration). **$24.59 per 1,000** delivered emails ($16.20 without the calibration). |
| **4. Each source's $ per 1,000 delivered** | **Free:** edit-app stored bios **$2.04** (33 emails) · earlier rounds' pool **$33.8** (3) · old paid payloads on disk: 0 emails. **His 3 niches:** movies names **$29.9** (2) · football names: 0 emails · tennis names: 0 emails. **New niches:** celebrities **$17.5** (21) · UFC/boxing $33.8 (1) · NBA $36.3 (1) · F1 $129 (1) · WWE, anime, cars: 0 emails. |
| **5. Audit pass rate** | **The AI judge failed the audit.** 40 random AI keeps: **26 real edit pages (65%)**. After a stricter second AI look: 28 of 40 (70%). So **I delivered only the 62 rows I checked by eye** (90 looked at). |
| **6. Exact file** | `<PROFILE>\AppData\Local\ClippersHQ\operator\editor_emails_20261011_BL1622.xlsx` (62 rows, read back) |

**Why it stopped at 62.** Your stop rule fired by 16:31: every source was above $10 per 1,000. The only source under the line, the edit app's stored bios, ran out at 245 accounts. Running faster would not have helped: the money goes on hashtag pages that rarely carry a new address (140 new addresses from 6,475 new authors).

**Also written.** master +62 through `crossdedup.append_leads` (run_id bl1622, backup made). His workbook: Emails 4,592 → 4,654; every other sheet unchanged, MARK untouched, backup sha-verified and vaulted to both roots. **No email was sent.**

## Your decisions

| | Question | My recommendation |
|---|---|---|
| A | The edit app's stored bios were the only cheap source ($2 per 1,000, 33 delivered). The app adds accounts every day. | Re-mine them **daily, for free**: about 2 minutes, no vendor call for accounts whose stored covers and views are fresh. |
| B | Celebrities is the only paid niche anywhere near the line: $10.86 per 1,000 estimated during the run, **$17.5 per 1,000 delivered** after the eye audit. | Only if you accept about $18 per 1,000. Expect K-pop and singer fan pages, not sports. |
| C | The AI judge cannot hold 90% on these new niches (65–70%). | Keep the eye audit on every delivered row, or go back to his 3 niches, where the judge was measured (94%). |

## 1. Asked

Two briefs, one round:

1. **Build** hashtag → free email check → feed views/recency check → cheap AI picture judge → spreadsheet. Copy BL-1619's parts, calibrate the judge on our own verdicts, and wait for BL-1619.
2. **"GO"** for 1,000 new editor emails delivered within 60 minutes, $10 cap. Free sources first (edit-app bios not skipped, re-mined payloads, the pool). Then a $1.00 pilot across his 3 niches (name lists only) plus 7 new edit niches. Then a detached full run where money goes only to sources under $10 per 1,000, with lanes 16 → 24 → 32 and the judge at 32 lanes. Then audit 40, deliver like BL-1619, commit and publish.

## 2. Shipped and proved

| Piece | What it does | Proof |
|---|---|---|
| `scratch/bl1622/gates.py` | The pure gates: a new address in the bio, the account dedupe, 1 post in 180 days, mostly videos, **average** views of the returned videos ≥ 2,000 | `tests/test_bl1622_gates.py` **20/20** |
| `judge.py` | One 6-cover strip plus the bio (addresses masked). qwen3.7-flash first; anything that isn't EDITOR goes to claude-haiku-5.5 once. Cost is OpenRouter's own `usage.cost`. | Calibration below |
| `calib_build.py`, `calib_run.py`, `combo.py` | 839 calibration strips cut from BL-1614/15/17/19's sheets. **10 of 10** sheet numbers checked against the crop. | `calib_score_v1.json`, `calib_score.json` |
| `free_sources.py`, `known.py` | Free sources. Being in edits.db no longer counts as "known" (your correction). | 605 new-address accounts found before spending |
| `gen_niches.py` | 1,299 unwalked singular `<name>edit` tags | Ledger-checked: every tag already walked was dropped |
| `stream.py` | Every stage runs at once, with the hard cap, the $1 pilot, the $10 cutoff per source, lanes 16 → 32 on the 503 rate, a log every 5 minutes, and power-loss-proof rows | Offline smoke with a fake vendor and judge (`smoke_stream.py`): funnel adds up, cap holds, a resume pays nothing twice |
| `tighten.py`, `audit.py`, `deliver.py` | Strict re-judge, audit sheets, delivery | 62 rows written and read back |

## 3. Measured

**Free sources** (counted before any spend):

| Source | New-address accounts | Path |
|---|---:|---|
| Edit-app stored bios | 245 | 150 stored PASS → judge with no feed call · 76 needed a feed call · 19 failed on stored data ($0) |
| Old paid payloads (123 files) | 6 | feed call |
| Earlier rounds' pool | 354 | feed call. Cut by the $10 rule after 147 feed calls (5 AI keeps) |

**Funnel (both runs):**

| Step | Count |
|---|---:|
| Hashtag pages read | 783 |
| Authors on them | 11,397 |
| New authors (not his) | 6,475 |
| …with a new address in the bio | **140 (2.2%)** |
| Feed calls (hashtag + free) | 368 |
| Passed views / recency / mostly videos | 282 (+150 free stored PASS) |
| Judged | 430 |
| AI KEEP | 113 (316 NOT, 2 out of scope) |
| Delivered after the eye audit | **62** |

**Pilot ($1.00 reached at 16:31), $ per 1,000 kept as the run measured it:**

| Niche | Calls | Raw new | AI keeps | $ / 1,000 (est.) |
|---|---:|---:|---:|---:|
| Free (all three) | 229 feed calls | 605 | 70 | 2.47 |
| Celebrities | 495 | 103 | 34 | 10.83 |
| Movies (names) | 87 | 11 | 3 | 19.9 |
| Cars | 50 | 4 | 1 | 32.8 |
| UFC/boxing | 54 | 2 | 1 | 33.8 |
| NBA | 57 | 3 | 1 | 36.3 |
| F1 | 211 | 13 | 2 | 67.4 |
| Football names / tennis names / WWE / anime | 56 / 61 / 55 / 71 | 1 / 3 / 0 / 0 | 0 | none kept |

**Judge calibration** on 238 past editor verdicts and 421 non-editor verdicts:

| Model / setup | Editors right | Non-editors right | $ / 1,000 checks |
|---|---:|---:|---:|
| ling-3.0-flash-vl | 98.7% | 76.0% | 0.015 |
| nex-n2.5-mini | 92.4% | 91.0% | 0.015 |
| qwen3.7-flash | 87.4% | 99.05% | 0.021 |
| claude-haiku-5.5 | 89.1% | 95.0% | 0.11 |
| gemma-4-31b **:free** | 5 of 113 calls answered (108 rate-limited, HTTP 429) | | 0 |
| **Chosen: qwen → haiku, his 3 niches (v3)** | **93.7%** | **98.1%** | 0.094 |
| **Chosen, new niches in scope (v4)** | **94.1%** | **99.05%** | 0.10 |

- No model, prompt or vote rule reached 95% on the editor side. Some old "editor" verdicts break this brief's own NOT rules (news pages, non-English text).
- **The calibration did not carry over to the new niches:** live, the judge's keeps were only 65% real edit pages.

**Speed:**

| | |
|---|---|
| Paid calls per minute | 72–205, never 280 |
| Overload 5xx | 0% |
| Lanes | 16 → 24 → 32 (raised as you asked) |
| CPU | 100% at every 1-minute reading |
| Free RAM | 2.05–5.8 GB |

**The PC was the bottleneck.** Largest processes by memory (read with `tasklist`, none killed): chrome.exe 5.8–6.3 GB, claude.exe 4.5–4.9 GB, python.exe 1.4–2.8 GB (this run plus others), msedgewebview2.exe 1.9–2.1 GB, svchost.exe 1.5 GB, ffmpeg.exe 1.0–1.4 GB, Discord.exe 0.9 GB. CPU per process was not measured.

## 4. What I got wrong

- **The AI judge passed calibration and failed the audit.** It kept music and lyrics pages, gaming, manga, sports-highlight pages with meme captions, and fans posting their own concert photos. These hardly exist in his 3 niches, so the calibration never tested them. Fix used here: a strict re-judge, then only eye-checked rows delivered.
- **Two bugs in the paid run, both fixed:**
  1. A status write read the counters while lanes changed them. Run `go` exited with "dictionary changed size during iteration" when I stopped it at 16:24. Its data was all on disk.
  2. When every source fell over the line, the walking lanes ended without saying "walk over". The feed lanes then waited forever. I stopped it by **its own PID** at 16:44; it had spent nothing since 16:31.
- **The pool sat first in the feed queue** and delayed the hashtag finds for about 8 minutes. I restarted with hashtag finds first. The restart lost nothing: run `go2` carried `go`'s counters.
- **The 60-minute and 1,000 targets were not met.** 62 delivered in 35 minutes.

## 5. Money and stores

| | Before | After | Spent |
|---|---|---|---|
| LamaTok (free balance read) | 317,946 requests (16:14) | 316,372 (16:44, unchanged at 16:50) | **1,574 requests = $0.9444** |
| OpenRouter (free credits read) | usage 16.0951 (start of round) | 16.6754 | **$0.5803** (calibration $0.5201, live judge $0.0485, strict re-judge $0.0117) |
| **Round total** | | | **$1.5247 of $10.00** |

- **Ledger:** spend.json campaign bl1622 now books LamaTok $0.9444 and OpenRouter $0.5801, the same as the balances to within $0.0002.
  - The meter had over-booked 34 LamaTok calls: 5xx answers not yet booked back when I stopped the stuck process.
  - The judge had under-booked $0.012 of OpenRouter: it books in batches of 100 calls.
  - Both are fixed by two `bl1622_reconcile` rows. No other campaign spent LamaTok in the window.
- **Stores written:** master_leads.csv (+62, backup made) · operator file (62 rows) · his workbook (Emails +62, vaulted) · the tag ledger (walked tags) · `bl1622_work\memory.jsonl` (every account paid for is never paid for again).
- Work data (bios, handles, covers) stays in `%LOCALAPPDATA%\ClippersHQ\bl1622_work\`. The repo holds counts only.

## 6. Leak scan

| Scan | Result |
|---|---|
| Secret scan (publish_report) | **PASS**: 0 config leaves, 0 emails, 0 credentials |
| Two-corpus scan (`scratch/bl1604/leak_adjudicate.py`, edit and lead corpora, 31 committed files) | 304 hits. 237 are explained by the public vocabulary. The other 67 were adjudicated by value, without printing them: public athlete, celebrity, club and competition names in the tag lists I typed (gen_niches 56, tags_build 5), plus 4 ordinary English words in code and comments. **0 leaks. This report: 0 unexplained hits.** |

## 7. Next

1. **A daily free job:** re-mine the edit app's stored bios with the same judge and the eye audit ($0 LamaTok).
2. If he wants paid volume, **celebrities only**, at about $18 per 1,000 delivered.
3. Before any AI-only delivery in a new niche, calibrate on **that niche's** pages. The 65% audit shows the his-3-niches calibration does not transfer.
4. Run long paid jobs when Chrome, ffmpeg and other sessions are idle. The CPU was pinned the whole time.

## 8. Paths

- Code and counts: `scratch/bl1622/`
  - PROGRESS.md · stream.py · judge.py · gates.py · known.py · free_sources.py · gen_niches.py · calib_*.py · combo.py · tighten.py · audit.py · deliver.py · smoke_stream.py
  - status_go.json · status_go2.json · pilot_snapshot.json · per_source.json · calib_score*.json · strict_score.json · audit_score*.json · free_sources.json · models.json
- Test: `tests/test_bl1622_gates.py`
- Work data: `%LOCALAPPDATA%\ClippersHQ\bl1622_work\` (keeps, memory, strips, audit sheets, rate logs)
- Delivered file: `<PROFILE>\AppData\Local\ClippersHQ\operator\editor_emails_20261011_BL1622.xlsx`
