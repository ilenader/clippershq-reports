# BL-1642: the AI reviewer keeps learning -- mistake book, rolling score on Home, a daily learner with rollback; v6 decides ~23 % alone (was ~15 %) with 0 wrong on the eye-labelled sets

2 APP order `2026-10-14_1608_P1-AI-learns-until-990-of-1000` (owner 16:05: "always be learning on its mistakes ...
monitored by Claude until it does 1,000 and gets 990 correct ... think outside the box").
Money: **OpenRouter $2.04 research** (the Claude Sonnet strict-look trials, 534 calls; booked `ai_review / bl1642_research`)
**+ ~$0.33 live AI reviews today**, of the $5 cap. $0 LamaTok.

## Card

| # | Item | Result |
|---|---|---|
| 1 | **Score now** | **114 of the last 115 checked AI decisions right (99.1 %)**. 3 FIXER checks every one by eye. Target: 990 of 1,000. |
| 2 | **The one mistake** | A YES on a slideshow of still photos over mostly black frames (35 % black). Undone (back in review, unsent). Fixed the same day by the learner, which added a veto: a YES needs < 30 % near-black frames. |
| 3 | **Coverage now** | On the 1,901 eye-labelled videos: **444 decided alone (23.4 %), 0 wrong, 1 the humans could not settle.** It was 15.1 % (v4). Live today: 21 of 284 (7 %). The queue is 90 % tennis, where the looks rarely agree. |
| 4 | **Mistake book** | Table `ai_checks`: every check, right or wrong, from 3 FIXER's monitor (synced in) or from a **person who takes back an AI decision** and decides again. Wrong ones = the book: video, AI said, right answer, why, who. `python tools\edits.py ai-score --book`. |
| 5 | **Home** | New card **"AI reviewer: X of the last N were correct"**, with "Claude double-checks every AI decision / about 5 of every 100. Mistakes found: M." English + Serbian; accessibility review: no blockers, wording applied. |
| 6 | **Checking mode** | Every AI decision is checked until the last 1,000 hold >= 990 right. Then a fixed 5 % by video id (never chosen after seeing the answer). It goes back to checking every decision by itself if the score falls below 990 of 1,000. |
| 7 | **Daily learner** | Once a day in the app (and `tools\edits.py ai-learn`), $0: it re-tunes the route's knobs (strict-look waiver, creator cut rate, cut veto, raw rule, black-frames veto). Inputs: the frozen eye-labelled sets, the mistake book, and the friend's YES on videos the AI left for him. **A change goes live only if it is not worse anywhere.** Either it removes book mistakes (at most 5 % fewer decided, no new frozen errors), or it decides more with no new error anywhere. Every version is kept in `ai_policy.json`. One that scores < 99 % on >= 50 live checks is **rolled back** and never chosen again. Waiting videos are re-routed from stored answers (no model call). |

## What changed, and why (each measured before it went live)

| version | change | measured on the 1,901 eye-labelled videos | why |
|---|---|---|---|
| v5 | A page with >= 1 earlier **human-approved** edit (his / the friend's; never the AI's own) skips the strict look on a sure 4-look YES | +146 decided alone, **0 new errors** | Labelled videos from pages with 3+ approved edits are 95-100 % edits; pages with none, 63 % |
| v6 | The strict look is **Claude Sonnet 5.5** instead of Haiku | 448 alone (was 416), 0 wrong, 1 unsettled instead of 2; on tune it keeps 95 of 167 real edits (Haiku 65) and passes none of the 5 known misses | ~$0.0036 a look, asked only after four sure YES on a page with no history |
| L-20261014 (learner) | Veto a YES over >= 30 % near-black frames (+ creator cut rate 0.5) | 444 alone (-4), 0 wrong; removes the book's one mistake | 3 FIXER's live mistake; adopted by the learner's own gate |

## Thinking outside the box -- tested, kept what won

| idea | result |
|---|---|
| **Account history** (the page's earlier approved edits) | **Kept (v5)**: the biggest lever, +146 decided alone with 0 new errors |
| **Two different models must agree** | Already the core: 4 looks from 3 vendors + a strict look by a 4th model. A stronger strict look (Sonnet) **kept (v6)** |
| **Cut rhythm vs the beat**, motion strength | Measured as free signals: cuts per second AUC 0.82, motion 0.81, cuts-on-beat 0.69. Useful only as vetoes (cut veto kept); not strong enough to decide alone |
| **Audio type** (speech rhythm = creator / podcast) | Speech rhythm does not separate edits from talking videos here (overlapping distributions). Not used |
| **Mostly black frames + stills** | **Kept** (learner, after 3 FIXER's mistake) |
| **Per-niche thresholds** | Tennis is the clear case: 0 sure tennis decisions on ~400 tennis videos, because tennis tags carry mostly raw match clips and the looks disagree. A per-niche knob is not added: there are no settled tennis examples to tune it on (3 in 2,963) |
| **Frames every ~0.5 s around cuts; on-screen text / OCR** | **Not tested this round.** Both need new pictures and new model calls on every labelled video (~$2-4); left for the next round |

## The mistake types left
One: a YES on a stills-over-black slideshow (fixed by the veto). No NO has been found wrong yet (98 checked).

## What the owner can do
Nothing is needed; the reviewer and 3 FIXER keep going. To see it: Home > "AI reviewer". To read the book:
`python tools\edits.py ai-score --book`.

Code: `clippershq/edits_ai_learn.py` (new), `clippershq/edits_ai_review.py` (v6, policy file, history waiver, black
veto, daily learn), `clippershq/edits_review.py` (a person's reversal = a check), Home card (`edits_app.py`,
`edits_app.js`, `edits_i18n.json`), `tools/edits.py` (`ai-score`, `ai-learn`). Tests: `tests/test_bl1642_ai_learns.py`
(11) + `tests/test_bl1637_ai_review.py` (19). Research: `scratch/bl1642/`.

- 17:55 FINDER BL-1642 AI keeps learning: score 114/115, coverage 23.4 % on labelled sets (was 15 %), book + daily learner + rollback live (DONE)
