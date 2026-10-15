# BL-1647: Claude looks at what the AI script is unsure about -- 263 waiting videos became 50; 3 tennis edits sent

2 APP order `2026-10-14_2320_P1-CLAUDE-plus-AI-review-the-unsure` (owner 23:15: "AI script + Claude Code review hand in
hand ... one picture with 30 pictures inside ... least usage ... I don't want my guy to do anything").
Money: **$0 OpenRouter / $0 LamaTok for the lane** (Claude Code sub-agents; the send's own gate check is a few cents).
The order arrived at 23:20; my order watcher had been stopped by low memory, so the work started at 12:58.

## Card

| # | Item | Result |
|---|---|---|
| 1 | **Waiting before** | 263 videos the script left for a person (252 "tennis"-tagged) |
| 2 | **Claude first look (Sonnet)** | 161 decided: 46 YES, 115 NO; 102 unsure |
| 3 | **Claude second look (Opus), only on those 102** | 53 more decided: 21 YES, 32 NO; 49 unsure |
| 4 | **Left for the friend** | **50 of 263 (19 %)** -- the 49 both looks were unsure about + 1 older AI case |
| 5 | **Approved, by niche** | football 35, superhero / films 21, UFC 5, basketball 2, **tennis 3**. Most "tennis" pages post football and film edits; real tennis edits are rare (3 of 252) |
| 6 | **Sent** | **3 tennis edits** (all 3 passed the send gates) -> Drive "ClippersHQ Sends / Tennis 2026-10-15 (3)". The link is in 2 APP's reply |
| 7 | **Checked before sending** | I looked at all 4 tennis YES myself. **1 was wrong** (broadcast rallies with a caption, name labels and one red circle = plain, not an edit). It was taken back (BACK, then NO as reviewer "claude") and never sent |
| 8 | **How decisions are made** | Every Claude decision goes through the app's own decision journal as reviewer **"claude"** -- the same path as a click, so BACK works. 214 done, 0 failed |
| 9 | **3 FIXER** | Checks a fixed 10 % of "claude" decisions in its own file (claude_checks.jsonl), scored apart from the script. 0 checked yet |

## The picture (his idea, measured)
One image per video: **30 frames evenly across the whole video, 6 x 5, the second on each frame**, and the script's verdict
and reason on top. A video over 60 s gets two images (first half / second half).

Two sizes were tried on **40 eye-labelled videos the script itself leaves for a person** (the hard ones):

| sheet | Claude decided | right | unsure | sub-agent tokens per video |
|---|---|---|---|---|
| **small (576 x 872, ~670 image tokens)** -- chosen | 26 | **26** | 14 | ~4,400 |
| large (864 x 1302, ~1,500 image tokens) | 21 | 21 | 19 | ~5,400 |
| small, Haiku instead of Sonnet | 18 | 16 | 22 | ~4,700 -- **rejected** (2 wrong) |
| + Opus second look on the 14 Sonnet-unsure | 6 more | **6** | 8 | ~5,900 (only on the unsure) |

The bigger picture did not help (more unsure, never more right), so the small sheet is the default.
Live cost: **~7,900 sub-agent tokens per waiting video** on average (Sonnet on all, Opus on the 39 % it was unsure about).
Caveat: the 40 labels came partly from Opus looks (BL-1637), so the Opus second look's 6 of 6 is not a fully independent
grade. 3 FIXER's blind checks are the independent one.

## The script learns from Claude
- Every Claude YES / NO is now a **labelled example** for the script's daily learner (214 so far). A learned change still
  goes live only when it is not worse on the 1,901 frozen eye-labelled videos AND on these examples.
- Today's learner run: **no change** -- no setting of the existing knobs decides more without a new error somewhere.
- Idea tested and **rejected**: "all four cheap looks say raw + few cuts -> NO". Claude agreed on 21 of 22 live videos, but
  on the frozen set 8 of 77 such videos were real edits (10 % wrong). The frozen set did its job.
- A Claude YES does **not** count as the page's human-approved history (the v5 waiver), so a Claude mistake cannot let
  later videos skip the strict look.

## Mistake types fixed today
| mistake | fix | so it cannot pass again |
|---|---|---|
| Claude (first look) called a broadcast rally compilation with a caption / name labels / one circle an edit | Reversed; the rule is now written into the spec every Claude look reads: such a compilation is raw | Test `test_the_mistake_fixed_today_is_in_the_spec` |

## Scores now
- **Script:** 117 of the last 118 checked decisions right (no new script decisions since 14 Oct 17:50 -- nothing new arrived).
- **Claude lane:** waiting for 3 FIXER's first checks; my own check found 1 wrong of 4 tennis YES (the one above).
- **Coverage now (script alone):** 23.4 % on the frozen set (unchanged today). Together with the Claude lane: 81 % of what
  waited today was decided without the friend.

## How to run it again
`python tools\edits.py claude-lane prep` -> Claude Code looks at the batch folders (SPEC.txt inside) and writes
answers.jsonl -> `claude-lane ingest <folders> --by claude-sonnet` -> `claude-lane second` -> Opus look ->
`ingest --by claude-opus` -> `claude-lane status`.

Code: `clippershq/edits_claude_lane.py` (new), `clippershq/edits_ai_learn.py` (Claude examples feed the learner),
`clippershq/edits_ai_review.py` (Claude YES is not page history), `tools/edits.py` (`claude-lane`). Tests:
`tests/test_bl1647_claude_lane.py` (9); `run_all -k test_bl1631*,1636*,1637*,1641*,1642*,1647*`: 6/6 green, 61 checks.
Research: `scratch/bl1647/`.

- 13:20 FINDER BL-1647 Claude lane: 263 waiting -> 50 for the friend; 3 tennis edits sent; small 30-frame sheet chosen (26/26 on the hard set); 1 Claude mistake reversed + spec fix (DONE)
