# BL-1653: the free first look (page_judge) now runs on a farm PC first -- tennis 588 pages: farm 20.5 min vs this PC 52.5 min, verdicts identical 588/588

3 FIXER order `2026-10-16_1426_FARM-FIRST-LOOK-HOOKUP` (ALFRED for Dusan; Dusan's yes 16 Oct 13:27 and his FOREVER rule
"When there is work and a farm PC or the pod is free, use it before Dusan's PC"). Money: **$0** (no vendor call).

## Card

| # | Item | Result |
|---|---|---|
| 1 | **What changed** | `python clippershq/raw_pages.py judge --run <run> --out-name <pictures>` sends the pages to the Flashcut render farm FIRST, through Flashcut's own `tools/farm/submit_job.py first-look` (farm_only: it never runs on this PC) |
| 2 | **When this PC judges** | Only when no farm PC took the job within **20 min** (the queued job is then retired with the lane's own `cancel/<job id>` marker, so it is never judged twice), when the farm job fails / is cancelled / runs over 35 min after it started, or with **`--local`**. Every reason is written to `raw_emails\<run>\judge_where.log` |
| 3 | **Output** | The same `raw_emails\<run>\judge.json`, same four fields per page (`account_id`, `script`, `confidence`, `why`): nothing downstream changes. A page the farm did not return is judged here. `--out <name>` writes another file name (used for this test) |
| 4 | **Real run** | tennis, 588 pages (`tennis_pages_20261014`): **588 on the farm, 0 here** |
| 5 | **Farm time** | **20.5 min** end to end: 4.8 min in the queue (ASR jobs ahead), 15.4 min on the farm PC (the judge itself 543 s = 0.9 s a page, the rest = moving the 57 MB of pictures) |
| 6 | **This PC time** | **52.5 min** for the same 588 pages with `--local` (detached, below-normal priority); a foreground try did not finish in 9.7 min; 10 pages timed in the foreground took 4.4-37 s each |
| 7 | **Identical?** | **Yes: 588/588 records identical** (verdict, confidence and reasons) between the farm and this PC on the same pictures today. EDITOR 494, UNSURE 79, CREATOR 15 |

## How it works (clippershq/raw_pages.py)
- `farm_first_look()`: zips the run's pictures as `<n>.jpg` + a `bios.json` (the judge reads the bio too) into the run's own work folder, calls `submit_job.py first-look <zip>`, then polls the lane queue (`render_queue.json`) every 15 s. `running` or `done` = taken. On `done` it reads `farmjobs/<job id>/out/first_look.jsonl`. The zip is deleted on every way out.
- Flashcut's and the Video Downloader's files were only read, never changed (`submit_job.py`, `first_look_job.py`, `page_judge.py`). The only thing written on their side is what their tools are for: the job (by `submit_job.py`) and, on a give-up, a `cancel/<job id>` marker for our own job.

## Tests
- `tests/test_bl1644_raw_pages.py`, class `FarmFirst` (5 new, synthetic, fake clock + fake lane): a job queued 5 min then running 40 min is waited for and its verdicts come home, zip + bios sent, nothing cancelled; nobody takes it -> gives up just after 20 min and leaves the cancel marker; a failed job / a failed submit -> falls back with the reason; farm verdicts land in the same `judge.json` shape and a page the farm skipped is judged here; `--local` never touches the farm. **15/15 pass; control: the 5 new tests fail against HEAD's raw_pages.py** (no `farm_first_look`).
- `tests/run_all.py` not run: the change is one file plus its own test file.

## Found on the way
- The live `raw_emails\tennis\judge.json` is from 14 Oct 21:51; all 631 tennis pictures were redrawn after it. Against that old file the farm differs on 2 of 588 verdicts (pages 1 and 5) -- both are identical to today's local run, so the old file is simply older than the pictures. It was not overwritten (this test wrote `judge_farm_bl1653.json` and `judge_local_bl1653.json` next to it). Rule: check a farm port against a fresh local run on the same files, never against an old output.
