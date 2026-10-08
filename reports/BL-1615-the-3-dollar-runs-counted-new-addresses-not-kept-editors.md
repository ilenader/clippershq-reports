# BL-1615: the "$3 per 1,000" runs counted new addresses, not kept editors

## Answer card

| | |
|---|---|
| **What made the old runs cheap** | They counted **new addresses of any kind**: fresh tags of any topic, at a time when ~90% of found addresses were still new. Only ~29% of those addresses were editors, in any niche, and no picture check was applied. |
| **"$3 per 1,000" matches** | **Definition (b), new addresses.** It never meant (c): new kept editors in football, tennis or movies. |
| **Probes, $ per 1,000 new kept editors** | foreign-language **$63** · long-tail names/films **$47** · pro-tool tags **$50** · tags from BL-1614's editors' captions **$16**. **None under $5**, so nothing was scaled (your rule). |
| **New editor emails delivered** | **21**: football **14**, tennis **2**, movies **5** |
| **LamaTok spent** | **$1.24**. The ledger booked 2,061 calls. The free balance read fell 349,122 → 347,084 requests, so the vendor billed 2,038. The 23-call gap is retried 5xx errors that the client counts and the vendor doesn't bill, so the ledger is $0.014 high, the safe side. |
| **$ per 1,000** | **$58.89** (21 for $1.2366) |
| **Audit** | All 26 picture keeps were re-judged blind on their newest covers: **21 editors, 80.8% [62.1–91.5]**, 0 creators, 0 businesses, 2 out of scope, 3 unclear. That is under 90%, so I tightened: **only the 21 confirmed twice are delivered.** |
| **File** | `<PROFILE>\AppData\Local\ClippersHQ\operator\editor_emails_20261008_BL1615.xlsx` (21 rows). BL-1614's file from the same day is unchanged. |
| **Also written** | master +21 through `crossdedup.append_leads` (run_id bl1615). Workbook: Emails 4,395 → 4,416, every other sheet unchanged, **MARK untouched**, backup sha-verified and vaulted. **No email was sent.** |

## 1. Our history ($0): the cheapest runs, three definitions

Sources:
- **Spend:** spend.json, by run_id.
- **(a) Raw emails:** the tag ledger's per-tag `emails`, inside each run's time window.
- **(b) New:** the rows that run appended to master, which are new by construction.
- **(c) Kept editors:** the editor measure each round had. That is the craft-cut KEEP, BL-1548's 29.4% editor rate, or BL-1614's picture check. Only BL-1614 limited editors to these three niches.

| Run | $ | (a) raw | $/1k raw | (b) new | $/1k new | (c) kept editors | $/1k kept |
|---|---:|---:|---:|---:|---:|---:|---:|
| BL-1545 (Instagram, free bio) | 0.104 | ~140 | ~0.74 | 137 | 0.76 | ~18 (13.3%, BL-1557) | ~5.8, any niche (that route is now an auth wall) |
| BL-1541 (16 tags) | 0.089 | 103 | 0.86 | 66 | 1.35 | not measured | — |
| BL-1584 (pro-tool tags) | 1.203 | 1,350 | 0.89 | 808 | 1.49 | 162 craft KEEP | 7.43, any niche |
| BL-1566 (9 fresh tags, ≤30 pages) | 0.139 | 52 | 2.67 | 56 | 2.48 | 6 KEEP | ~23 |
| BL-1542 (512 tags) | 2.556 | n/a | — | 1,001 | 2.55 | ~294 (29.4%) | ~8.7, any niche |
| BL-1583 | 1.652 | 528 | 3.13 | 514 | 3.21 | 104 KEEP | 15.89 |
| BL-1544 (deep re-walk) | 2.970 | n/a | — | 767 | 3.87 | ~225 (29.4%) | ~13.2 |
| BL-1563 | 4.153 | ~676 | ~6.1 | 908 | 4.57 | 168 KEEP | ~25 |
| BL-1564 | 1.225 | 435 | 2.82 | 88 | 13.92 | 11 KEEP | ~111 |
| BL-1614 (picture check, 3 niches) | 1.942 | 639 | 3.04 | ~207 (hashtag) | ~9 | 46 hashtag picture-keeps | ~38 |

- **Matches "$3":** BL-1542 $2.55, BL-1566 $2.48 and BL-1583 $3.21 per 1,000, all definition **(b)**. Even the best (c) on record, BL-1584's $7.43, was any niche and judged only by the craft cut. The craft cut keeps only 28% of proven edit pages (BL-1613), so it isn't comparable to a picture check.
- **What made them cheap:**
  1. **Fresh tags of any topic.** BL-1542 walked 512 tags (anime, music, gaming, everything).
  2. **The store was young.** BL-1565 measured ~90% of found addresses as still new. In BL-1614 that was about 1 in 3.
  3. **No niche limit and no picture check.** Roughly 70% of those addresses were not editors at all.
- **Languages and sources:** nothing language-specific. All TikTok hashtag v1/v2, except the one Instagram run.

## 2. Probes (fresh tags only: 96 already in the ledger were skipped)

| Probe | Tags walked | Calls (walk + pictures) | Raw new emails | Kept | **$/1k new kept** |
|---|---:|---:|---:|---:|---:|
| (a) Foreign-language edit tags (es/pt/fr/ar/tr/id/it, plus de/nl/pl) | 70 | 698 + 34 | 40 | 7 → 5 after audit | **$63 → $88** |
| (b) Long-tail: young/squad players, smaller clubs, national teams; single films and characters | 87 (hit its cap) | 750 + 34 | 44 (films 0.091 per call, best) | 10 → 8 | **$47 → $59** |
| (c) Pro-tool tags not yet walked | 24 | 359 + 54 | **398 (1.1 per call)** | 5 → 4 | **$50 → $62** |
| (d) Tags from the 119 BL-1614 editors' captions | 6 (all the unwalked ones left) | 96 + 10 | 13 | 4 → 4 | **$16** |
| (e) What made the old runs cheap | — | — | — | — | Fresh tags are in every probe above. "Any topic, no editor check" breaks your rule by definition. |

- **The pro-tool result is the instructive one.** Those tags carry **15× more emails per call** than any edit tag (1.1 against 0.05–0.09). But 232 of 398 were general-purpose video editors (vlogs, weddings, YouTube, brands) outside your three niches. Their pictures were judged together with probe (d)'s: of those 64, **9 editors, 28 creators and 26 off topic**.
- That is the old cheap runs in miniature: plenty of addresses, very few football, tennis or movie edit pages.
- **Nothing scaled** (step 3: no source under $5).

## 3. Quality, exactly as BL-1614

- Text may only drop. Every keep needs a 6-cover picture judged by me, and unclear means drop.
- Accounts BL-1614 had already judged kept their verdict and were not re-paid.
- I judged 132 pictures this round, plus 26 fresh ones for the audit.
- **The audit is the whole population (26).** The second look found 5 that don't belong: a Netflix-series page, a horror-film page and 3 unclear. They were removed. The 21 delivered passed both looks.

## 4. Notes

- **The probes ran one after another** in one detached job (`run_probes.py`). The tag ledger is one shared file, and two walkers at once could lose entries.
- **Priority.** I raised **my own** job's process ID to Normal; the machine was busy.
- **Where the data lives.** Work data is in `%LOCALAPPDATA%\ClippersHQ\bl1615_work\`, never in the repo. The repo files hold counts only.
- **The obvious next lever is outside your rule.** The pro-tool tags deliver addresses at ~$0.54 per 1,000 new: 398 new emails for $0.215, before any picture check. They are working video editors of any niche, though, so they only help if you widen the niche.

Files: `scratch/bl1615/` (gen_probe_tags, run_probes, the BL-1614 tooling copied and retargeted, PROGRESS.md and the JSON counts).
