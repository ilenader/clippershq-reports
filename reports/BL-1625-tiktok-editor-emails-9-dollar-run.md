# BL-1625: the $9 TikTok editor run: 95 faceless editors for $8.66, not 450–650

## Card

| | |
|---|---|
| **1. Editors delivered** | **95 faceless edit pages** → master + his workbook + the BL1625 file. Separately: **12 freelance editors** and **11 anime edit pages**, each in its own file only (not master). 12 video-game edit pages were found and dropped. |
| **2. Spent (both balances)** | **$8.662 of $9.00**: LamaTok $8.4252 (14,042 requests) + OpenRouter $0.2368. Never over $9. Paid calls stopped at $8.75 by my counter; the ledger is reconciled to the balances. |
| **3. $ per 1,000** | **$91 per 1,000 faceless delivered** ($81 counting the freelancers too). |
| **4. Each source's $ per 1,000 eye-checked faceless** | **K-pop names $32** · kept-editor captions $33 · Asian actors / idols $40 · caption-id tags $71 · singers $96 · caption tags with idol names $107 · NBA $110–214 · influencers $148 · UFC, movies, Western actors: 0 delivered. (From the run counters, which cover $6.27 of the $8.66; see §3.) |
| **5. Fixed along the way** | Free tag ids from captions (**4,843 lookups saved** vs 1,454 paid; **0 id mismatches in 30,592 checks**). Four stalls: the shared spend ledger and the tag ledger were rewritten **while holding the interpreter lock**, and fsync ran inside the stream's global lock. Throttled lookups dropped tags. **Video-game edit pages fooled the AI judge and the first eye agents**: caught by my spot-check, every sheet re-audited. |
| **6. Files** | `<PROFILE>\AppData\Local\ClippersHQ\operator\editor_emails_20261011_BL1625.xlsx` (95) · `…_BL1625_freelancers.xlsx` (12) · `…_BL1625_anime.xlsx` (11) |

**Why 95 and not 450–650.** Three things went wrong, in order of cost:
1. **The stream froze four times** in its first 50 minutes, at 10–100 calls a minute instead of 250–790. The money spent then still bought pages, but slowly, and every restart re-paid the start-up.
2. **Every source paid $0.30 to prove itself** (your rule). 18 sources × up to $0.30 is about **$3.3**, and most of them proved bad.
3. **The cheap pools ran dry.** K-pop names ($32 per 1,000) and kept-editor captions ($33) were used up by 01:36. After that every live source cost $70–110 per 1,000, and the rule was to keep spending on the cheapest one.

**No email was sent.**

## Your decisions

| | Question | My recommendation |
|---|---|---|
| A | 12 freelance editors and 11 anime edit pages sit in their own files. | Your call: add them to master and the workbook, or leave them. |
| B | TikTok faceless editors cost **$91 per 1,000** this round and about $32 at best (K-pop names). The cheap name pools are now walked. | **Stop paid TikTok editor runs.** Use BL-1623's YouTube faceless route (about $0.16 per 1,000 on the free quota) instead. |
| C | The $0.30 trial per source cost about $3.3 of $8.66 here. | If you run again, give a source $0.10, or let similar lists share one trial. |

## 1. Asked

$9 hard cap (stop paid calls at $8.75), reusing BL-1622/1623's stream, gates, judge5 and delivery:

0. **Fixes ($0, test first):** free tag ids from captions, routing by $ per eye-real editor (re-rank every 200 calls, $0.30 trial per source), save each hashtag item's plays and date, Normal priority, detached, PROGRESS every 25 calls.
1. **Free first:** mine the rest of the edit app's 963 stored email bios.
2. **Paid walk:** celebrities first, then movies / UFC / NBA, then new tags from kept editors' captions.
3. **Eye-check every judge keep** (sub-agents in parallel, I spot-check 1 sheet in 10) and **deliver in waves of 100**.

Plus: balances every 15 minutes, a status line every 15 minutes, and naming any other LamaTok spender.

## 2. Shipped

| Piece | What it does | Proof |
|---|---|---|
| `scratch/bl1625/stream25.py` | BL-1622's stream + judge5, plus the changes below | `smoke25.py` offline (fake vendor, judge, balances): **PASS** after every change |
| …free tag ids | Every caption hashtag on a bought page or feed carries its challenge id; a known id skips the lookup | **4,843 tags walked with no lookup** (1,454 paid lookups); self-check **0 mismatches in 30,592** caption-vs-lookup comparisons |
| …routing | Re-rank every 200 calls by $ per eye-real editor (eyes.json; prior 80.3% until 10 checks); $0.30 trial per source; no kill line | `rank`, `per_1000_real` and `precision` in every status file |
| …plays + date | Every hashtag item's play count and post date → `items.jsonl` | **156,103 items saved** for next round's free pre-check |
| …balance guard | Both balances read free (start + every 15 min, 5 min in the last run); if the balance-measured spend is above the counter, the counter is raised | Smoke: a $1.00 balance raised the counter and stopped the walk with 0 paid calls |
| …stall fixes | Spend booking in its own process (`book25.py`); tag ledger saved once a minute; fsync off the global lock; checkpoint writes retried; lane / monitor errors counted, never fatal; stack dump on any 2-minute stall | go3 onward: 240–790 calls a minute (was 10–100) |
| …game filter | Game words in tag names; and the judge's own reason naming a game → a GAME drop | Measured offline on 128 eye-checked rows: the reason names a game on 7 of 11 game pages and **0 of 62** real faceless pages. Live in go7 (the last $1.32) it fired 0 times |
| `free25.py` | Step 1 (the edit app's stored bios) | Result in §3 |
| `gen25.py`, `more25.py`, `capids25.py`, `snoweye25.py` | One tag per name; ledger-filtered; caption tags with known ids | Speculative name+group variants I typed were caught and removed before walking (63) |
| `eyes25.py`, `reaudit25.py` | Numbered 8-row sheets + bios; verdicts F / R / A / G / N; a re-audit where the stricter verdict wins | 218 of 218 judge keeps eye-checked |
| `deliver25.py` | Wave-safe delivery (delivered.json); master via `crossdedup.append_leads`; workbook via `tools/deliver_workbook.py`; three files | 95 / 12 / 11 read back; workbook skips all 95 on a re-run (already present) |

## 3. Measured

**Step 1, free source: 0 new.** The edit app holds 963 accounts with an email in the bio:

| Already | Accounts |
|---|---:|
| Mined by BL-1622 / 1623 | 245 |
| Picture-judged in BL-1614–1619 | 263 |
| Address already his | 419 |
| Account already his lead (different address) | 36 |
| **New** | **0** |

**The paid funnel, all runs:**

| Step | Count |
|---|---:|
| Tags walked (ledger) | 6,068 |
| Hashtag pages | 11,284 |
| Authors on them | 155,501 |
| New authors | 79,573 |
| …with a new email | 1,270 (1.6%) |
| Fed (views / recency / photos gate) | 1,267 |
| Judged | 996 |
| Judge keeps | 218 |
| **Eye-checked faceless** | **95** (44% of keeps) |
| Freelancer / anime / game / not | 12 / 11 / 12 / 88 |

**By source** (run counters; eye verdicts on every keep):

| Source | $ (counters) | Tags | Keeps | Faceless | $ per 1,000 faceless |
|---|---:|---:|---:|---:|---:|
| K-pop names | 0.84 | 488 | 34 | 26 | **32** |
| Kept-editor captions | 0.40 | 274 | 40 | 12 (+10 game) | **33** |
| Asian actors / idols | 0.25 | 135 | 7 | 5 | 40 |
| Caption-id tags (free ids) | 2.48 | 1,954 | 102 | 35 | 71 |
| Singers | 0.48 | 228 | 8 | 5 | 96 |
| Caption tags with idol names | 0.85 | 757 | 13 | 8 | 107 |
| NBA names / BL-1622 leftovers | 0.32 | 210 | 3 | 2 | 110–214 |
| Influencers | 0.15 | 64 | 6 | 1 | 148 |
| UFC names / leftovers, movies, Western actors | 0.46 | 298 | 2 | 0 | — |

- **The counters cover $6.27 of the $8.66 billed.** The other $2.39 is billing that no source counter caught:
  - lookups that errored and were re-queued
  - calls in flight when four runs were stopped
  - go4's frozen last minutes
  - feeds for re-queued candidates across restarts
- **So the per-source figures are floors.** The honest whole-round number is the balance one: **$91 per 1,000**.

**The eye check.**

| | |
|---|---|
| First-pass agents | Passed three sheets of video-game character edits (Genshin / Honkai / Love and Deepspace) as 8/8 faceless |
| My spot-check | Caught it on s0013 |
| Fix | All 11 agent-checked sheets re-audited with a stricter rubric (G for game, A for anime); a row stays faceless only if both passes said so |
| Change | First-pass faceless 73 of 96 → after re-audit **52** of 112 at that point |
| Sheets I checked myself | s0001, s0006, s0011, s0012, s0013, s0023 (6 of 28) |

**Speed.**

| Runs | Calls per minute | Notes |
|---|---|---|
| go / go2 / go4 (before the fixes) | 10–130 | Then frozen |
| go3, go5–go7 | 240–790 | Unbilled 427 throttles counted by the meter (~500 in go5 alone) |

## 4. What I got wrong

- **Four stalls before I found the cause.**
  - I first blamed CPU (other sessions pin it at 100%), then spend.json lock contention.
  - py-spy showed the truth: spend.json (19 MB) re-encoded in pure-Python json **while holding the GIL**. Then the 2.4 MB tag ledger and a 1.4 MB tag-id dump did the same, and fsync ran inside the global lock.
  - I should have taken a stack dump at the first stall instead of restarting twice.
- **go4 froze with its memory paged out.** I stopped it **by its own PID** (two PIDs, both mine, checked by command line). Its spend was then set from the balance.
- **I trusted the first-pass eye agents for 10 sheets.**
  - Game-character edits look like anime edits, and my first prompt counted anime characters as faceless.
  - The spot-check caught it. Nothing wrong was delivered, but the routing ran on inflated precision for about 10 minutes and sent money to caption tags.
- **I typed speculative "name + group" tags** (e.g. a member name + group name). I removed 63 before they were walked.
- **Throttled lookups dropped tags in go3:** a tag that hit 3 throttles (427) was recorded as walked with 0 pages. 74 of this round's 6,068 ledger tags have 0 pages; most are tags that don't exist, an unknown few are throttle losses. Fixed in go4: a 427 now re-queues without using a try (164 re-queued since).
- **The 100-editor wave never filled.** Everything went in one final wave at 02:53. The eye verdicts were on disk all along, so a crash would have lost nothing.
- **Target missed:** 95 delivered vs 450–650 expected.

## 5. Money and stores

| | Start (23:42) | End (02:24) | Spent |
|---|---|---|---|
| LamaTok requests (free balance read) | 315,288 | 301,246 | **14,042 = $8.4252** |
| OpenRouter usage (free read) | 16.8310 | 17.0678 | **$0.2368** |
| **Round** | | | **$8.662 of $9.00** |

- **Counter vs balance.** My counter (the client's own request count) ran ahead of the bill by the unbilled 427 throttles. After each run stopped, its status total was set to the balance-measured amount, so each next run got the true remainder. go4 was frozen, so its total was set the same way.
- **Ledger.** spend.json campaign bl1625 had booked 15,343 requests (427s included) and $0.11 of judge cost. Two `bl1625_reconcile` rows (−1,301 requests, +$0.1262) bring it to **$8.4252 + $0.2368 = $8.662**, matching the balances.
- **Other LamaTok spender: none during the round.**
  - No other campaign booked in the window, and no other walker was running.
  - The tag ledger was last written at 19:07 before I started.
  - The balance had drifted by 10 requests between BL-1623's last read (19:11) and my start (23:42). That was before this round, so it is not in the $8.662.
- **Stores written:**
  - master_leads.csv +95 (run_id bl1625, backup made)
  - his workbook: +95 to Emails; every other sheet unchanged, MARK untouched, backup vaulted to both roots
  - three operator files
  - the tag ledger (walked tags)
  - `bl1625_work\memory.jsonl` (seeded with BL-1622/1623, so nothing is paid for twice)
- **Work data stays outside the repo**, in `%LOCALAPPDATA%\ClippersHQ\bl1625_work\` (bios, handles, strips, eye sheets, tag ids, items).

## 6. Leak scan

| Scan | Result |
|---|---|
| Secret scan (publish_report) | Run at publish |
| Two-corpus scan (`scratch/bl1604/leak_adjudicate.py`, edit and lead corpora, all 25 committed files + this report) | 251 hits. 169 are explained by the public vocabulary. The other 82 are all inside the name and word lists I typed: `gen25.py` 64 and `more25.py` 11 (public idol, singer, actor, athlete names), `stream25.py` 5 and `capids25.py` 2 (tool / game words). **0 hits in any status, balance, per-source or PROGRESS file or in this report. 0 leaks.** |
| Also | FACTS.md lifetime spend re-stamped (commit a4614a00): the pre-commit guard refused at a $10.01 TikTok drift (limit $7.40) after this run. |

## 7. Next

1. **Don't buy more TikTok editor emails at this price.** The cheap pools (K-pop names, kept-editor captions) are walked; what is left costs $70+ per 1,000.
2. **YouTube faceless** (BL-1623): about $0.16 per 1,000 on the free quota, with the same eye check.
3. If TikTok runs again:
   - a $0.10 trial per source
   - snowball only from eye-confirmed editors
   - the game filter on from the start
   - `items.jsonl` (plays + date) used as a free pre-check before any feed call
4. The stream fixes apply to BL-1622's original too: book spend.json out of process, and never fsync or dump big JSON inside the global lock.

## 8. Paths

- Code and counts: `scratch/bl1625/`
  - stream25.py · smoke25.py · balances.py · book25.py · free25.py · gen25.py · more25.py · capids25.py · snoweye25.py · eyes25.py · reaudit25.py · deliver25.py · status25.py · common.py
  - PROGRESS.md · status_go*.json · balances.jsonl · per_source.json · free_sources.json
- Work data: `%LOCALAPPDATA%\ClippersHQ\bl1625_work\`
- Files: `<PROFILE>\AppData\Local\ClippersHQ\operator\editor_emails_20261011_BL1625.xlsx` · `…_freelancers.xlsx` · `…_anime.xlsx`
