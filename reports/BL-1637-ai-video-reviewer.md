# BL-1637: the AI video reviewer -- built, measured on 1,400 fresh videos, live in SHADOW; v4 never wrong on what it decides alone, but it decides only ~15 %

2 APP order `2026-10-14_0140_OVERNIGHT-AI-REVIEWER` (P1) + P0 `2026-10-14_0830_RESUME-after-power-off`.
2026-10-14 01:40 - 03:44, then 08:30 - 10:30 (the PC was restarted by Windows Update at 03:44; nothing was lost).
Money: **OpenRouter $2.26 research + ~$0.01 live shadow reviews** of the $3.00 night cap (own stop $2.40). $0 LamaTok,
$0 HikerAPI. The OpenRouter account has **$0.38 left**.

## Card

| # | Item | Result |
|---|---|---|
| 1 | **Accuracy on what it decides alone** | **v4 (live now): 66 / 66 on a fresh, never-tuned set of 450 videos** (95 % interval 94.5-100 %). Over all three fresh sets (1,400 videos): **174 / 174** where the eye labels are settled. It also decided **2 + 0 + 2 = 4** videos that three human looks could not settle; counted as wrong, **97.1 %** on the clean set. |
| 2 | **Coverage (share it decides alone)** | **15.1 %** on the clean set (10.7-18.8 % across sets). Everything else stays for the friend. |
| 3 | **The 99.5 % target** | **Not proven.** The point estimate is 100 %, but the order asks for >= 400 auto-decisions on held-out videos; v4 has **174** on fresh sets (+94 on the tuning half). At 15 % coverage, 400 needs ~2,700 more labelled videos. |
| 4 | **The higher-coverage option (v3.1)** | 277 / 279 right (**99.3 %**) on two fresh sets, deciding **~30 %** alone. Its misses were all "plain" videos every cheap look called an edit -- that is what v4's extra look removes. |
| 5 | **Speed** | Live: **~8.6 videos a minute** with 3 lanes (12 videos in 84 s at the app's start). Per video: one decode ~4.3 s (median) + ~2.9 model calls of ~2.6 s. |
| 6 | **$ per 1,000 videos** | **$0.53** (v4, measured on 450: 2.93 calls a video). |
| 7 | **In the app** | Reviews every waiting video as soon as it lands, after any restart too. **SHADOW**: own table `ai_reviews`, nothing moved, the friend's queue untouched. Live since 08:23; v4 since 10:10. Settings > **AI reviewer > "AI decides for me"** (OFF; owner only). |
| 8 | **The day's job** | `python tools\edits.py job --football 100 --basketball 100` -- built; **proved only in a fake world ($0)**: `job --fake` ends DONE. |
| 9 | **Audit** | Blind audit #1 (240 of the 270 v4 auto-decisions) **sent to 3 FIXER at 10:05; result pending.** |

## Ground truth (2,963 videos, eye-labelled)

- **Sources:** 817 approved-library videos (his / the friend's YES), 2,041 videos the friend said NO to, 105 from the review
  queue. The friend's NOs are noisy (out-of-scope days), so a NO was never taken as "not an edit": **every video was
  labelled by eye**.
- **Two independent Claude labellers** (A = Sonnet, B = Opus sub-agents) on a 12-frame contact sheet (5 %..95 % of the
  whole video), with the owner's spec as the guide (`scratch/bl1637/LABEL_GUIDE.md`). They agreed on **78.4 %**; every
  disagreement (**639**) got a third, careful look (C = Opus) on the 12-frame **and** a 24-frame sheet. No majority -> UNSURE.
- **Result:** YES 1,995 / NO 779 / UNSURE 189. YES by niche: football 1,018, superhero + film 547, UFC 288,
  basketball 113, **tennis 3**.
- Side findings (counts only):
  - **61 % of the friend's NO folder are YES by eye** (1,197 of 2,041: tennis on out-of-scope days, good edits).
  - **6.4 % of the approved library is not an edit by eye** (52 of 817).
- **Splits:** tune (502), test (1,061: used while building v2 / v3, so no longer clean), and three **fresh** held-out
  sets added one at a time, each graded **once**, by the version frozen before it was labelled:

| fresh set | videos | graded version | AI alone right / settled | accuracy | coverage | strict (unsettled counted wrong) |
|---|---|---|---|---|---|---|
| 1 | 500 | v3 | 161 / 162 | 99.38 % | 32.8 % | 98.17 % |
| 2 | 450 | v3.1 | 116 / 117 | 99.15 % | 26.4 % | 97.48 % |
| 3 | 450 | **v4** | **66 / 66** | **100 %** | **15.1 %** | 97.06 % |

v4 on the earlier sets (not clean: the v4 rule was built from their misses): tune 94 / 94 (18.8 %), fresh 1 60 / 60
(12.0 %), fresh 2 48 / 48 (10.7 %).

## How it decides (`clippershq/edits_ai_review.py`, VERSION v4)

1. **The picture ($0):** one streamed decode of the whole video -> a 12-frame sheet + free signals (cuts per second,
   static / frozen / black share, motion, colour, audio level, beat, speech rhythm, cuts on the beat).
   **Free signals alone separate edits only moderately:** cuts per second AUC 0.82, motion 0.81, the rest 0.40-0.69
   (on 1,969 YES vs 695 not-edits). They are used as vetoes, never as the judge.
2. **Four cheap looks in a cascade** (it stops paying at the first answer that already sends the video to a person):
   Claude Haiku 5.5, GPT-6 Luna, Qwen 3.7 Flash, Haiku again with a second wording. Stronger cheap models (Gemini 3.5
   Flash Lite, GPT-5 mini, Qwen Plus) were tried on 120 and did not beat Haiku.
3. **The route:** decide alone only when every look is sure and gives the same decision (and the same niche for a YES)
   and nothing vetoes it:
   - a NO whose kind includes "raw" -> person (light highlight edits get called raw);
   - a "creator / podcast" cut faster than 0.4 cuts a second -> person;
   - **v3.1:** a YES needs a cut at least every 10 s;
   - **v4:** a YES also needs a **strict 5th look** (Haiku, "is this real editing craft or only plain clips with a
     caption?") to answer CRAFT and be sure. It only ever turns a YES into "person", never adds a decision.
4. **Broken / frozen -> NO; black -> person** (2 of 4 "black" videos were dark-graded edits).

## Good sides and bad sides (v4, all three fresh sets: 1,400 videos)

| class (eye label) | videos | AI alone, right | AI alone, wrong / unsettled | to a person |
|---|---|---|---|---|
| football edits | 456 | 45 | 0 | 411 |
| superhero edits | 164 | 31 | 0 | 133 |
| UFC edits | 134 | 19 | 0 | 115 |
| film edits (part of "superhero") | 68 | 5 | 0 | 63 |
| basketball edits | 35 | 3 | 0 | 32 |
| tennis edits | 3 | 0 | 0 | 3 |
| raw footage / plain highlights | 198 | 0 | 0 | 198 |
| creator / talking head | 47 | **33** | 0 | 14 |
| podcast / interview | 22 | 12 | 0 | 10 |
| slideshow | 30 | 9 | 0 | 21 |
| ads / news | 24 | 3 | 0 | 21 |
| other not-edits | 83 | 6 | 0 | 77 |
| pure AI video | 12 | 1 | 0 | 11 |
| other niche (NFL, anime, music...) | 22 | 7 | 0 | 15 |
| humans could not settle | 101 | -- | **2** | 99 |

**Good:**
- No wrong decision on a settled video in any v4 run (268 auto-decisions incl. tune).
- Best at **creators / talking heads** (33 of 47 alone) and podcasts.
- When it says YES, the niche was right every time.
- Cheap ($0.53 / 1,000) and it never moves a file in shadow.

**Bad:**
- **Coverage.** Only ~10 % of real football edits are decided alone. The strict look sends many real edits to the
  friend: of 167 true YES on tune it keeps 65.
- **Raw / plain highlights are never decided** (by design: that is where light edits hide).
- **Tennis is untested** (3 tennis edits in 2,963 videos).
- The few videos it decides that humans cannot settle: 2 per 450.
- **Every v3 / v3.1 miss** was a "plain" video all four cheap looks called an edit (a highlight with a caption, a photo
  slideshow with slow zooms, a voice-over trivia video, film clips with one lyric line).
- **A failed call (network) sends the video to a person.** It was 8.6 % of videos today; the internet upload was
  saturated by another program. The worker now retries a failed review after 1 hour, never in a loop.

## In the app (SHADOW)

- `edits_swipe_server.start_ai_reviewer` starts `edits_ai_review.Worker` with the live server.
  - It polls every 20 s with 3 lanes, oldest video first.
  - Its table `ai_reviews` is the resume point after any restart / power cut. A file that changed, or a review whose
    call failed (after `RETRY_S` = 1 h), is reviewed again.
  - Spend stops at **`ai_cap_day_usd`** ($1 a day; Settings > money).
  - Every call is booked to `spend.json`, campaign `ai_review`.
- **"AI decides for me"** (Settings > AI reviewer, owner only, default OFF, only a real `true` turns it on):
  - Sure YES / NO go through the **same decision journal as a click**, as reviewer `ai` (YES -> library, NO -> rejected).
  - **BACK works** on an AI decision. A decision is never applied twice; "person" videos stay for the friend.
  - The Settings block shows today's counts and cost.
  - Accessibility review (accessibility-lead): no blocking issues; its 3 wording fixes are applied in English and Serbian.
- Today, live in shadow: 12 waiting videos reviewed; the app was restarted twice through its own `restart_app` job
  (the friend's last click was 100 min earlier).
- **Bug found and fixed live:** a cascade that stopped on purpose (an unsure answer) was labelled as a failed call.
  With the new 1-hour retry it would have re-paid for those videos every hour. Fixed + tested before the second restart.

## The day's job

- `python tools\edits.py job --football 100 --basketball 100 [--ufc N --tennis N --superhero N] [--budget 3]`, plus
  `--status` and `--fake`.
- Only a person starts it; nothing schedules it (daily_on stays OFF). It refuses to start when downloads are OFF.
- Each round runs one paid discovery per short niche (through `cmd_discover`: his caps, the run lock and the balance
  floor all apply; the job budget is split over the short niches).
- It then waits until the AI reviewer and the decision journal have caught up.
- It ends DONE when every niche has its N, or STOPPED on budget, no progress twice, a refused run, or 6 rounds.
- **Approvals counted are library rows since the job started**: the friend's clicks, plus the AI's when "AI decides"
  is on.
- **Proved only in a throwaway world ($0):** `job --fake --football 5 --basketball 3` and `--football 4 --ufc 2` both
  ended DONE.
- **Never run against the real vendor.** With v4's ~15 % coverage, most approvals still need the friend.

## Tests

- `tests/test_bl1637_ai_review.py`: **16 tests, green**.
  - parse; every route rule (v3.1 cuts veto, v4 strict look: plain / unsure / missing / failed); the strict look is
    asked only after four sure YES.
  - The cascade stops paying early. A stopped cascade is not a failed call; a failed call is retried after RETRY_S and
    not before.
  - Shadow moves nothing. AI-decides goes through the real journal, BACK works, nothing is applied twice.
  - The daily cap stops the worker; a fake model books nothing.
  - The job: DONE / no progress / refused; the fake world never touches his home.
  - Settings: default OFF; every new word in both languages.
- `run_all -k test_bl16*`: **60/60 suites green, 636 checks** (before the v4 edits; the BL-1637 suite was re-run green
  after each change).

## Not done

- Research spend ($2.26, 12,164 calls) is booked in spend.json as campaign `ai_review`, label `bl1637_research`.
- **BL-1636's library check (642 rows left):** not run. It needs OpenRouter credit, and the account has $0.38.
- 3 FIXER's suggestion to split `pc_off` into restart vs. waiting-for-sign-in in `edits_outages.py`: not in this round.

## What the owner can do

1. **Top up OpenRouter** (it has $0.38; the live reviewer spends ~$0.53 per 1,000 videos, at most $1 a day).
2. **Choose:** leave "AI decides" OFF until 3 FIXER's blind audit is back. Then turn it on in Settings > AI reviewer:
   it takes the ~15 % it is sure about and leaves the rest for the friend. If you would rather have ~30 % decided at
   ~99.3 %, say so (that is v3.1: one line in POLICY).

Code: `clippershq/edits_ai_review.py`, `clippershq/edits_ai_job.py`, `tools/edits.py` (job), `tools/edits_job_fake.py`,
app / db / i18n / server wiring, `tests/test_bl1637_ai_review.py`. Research scripts: `scratch/bl1637/`.
Data (private, never the repo): `%LOCALAPPDATA%\ClippersHQ\edits\ai_review\`.
