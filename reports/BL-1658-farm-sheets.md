# BL-1658: the tennis review's sheets can now be made on a Flashcut farm PC -- built and tested ($0); it needs Flashcut to add one job type first

3 FIXER order `2026-10-16_1657_MOVE-THE-TENNIS-VIDEO-REVIEW-BL-1654-TO` (ALFRED for Dusan 16:57): move the tennis video
review (BL-1654) to the pod or a farm PC instead of pausing it; restart the 1 LEADS order watcher. Money: **$0**.

## Card

| # | Item | Result |
|---|---|---|
| 1 | **Where the review runs now** | Still parked on this PC: **not moved yet**. The farm can run it once Flashcut adds one job type (`sheets`, row 4). |
| 2 | **What was built** | `clippershq/farm_sheets.py prep NAME` packs the waiting videos into zips, sends them to a farm PC, and writes the same batch folders `claude-lane prep` writes (SPEC.txt, batch.json, `<key>.jpg`). The Sonnet look and the ingest do not change. |
| 3 | **Farm job script** | `tools/farm_jobs/clipper_sheets_job.py` runs OUR `edits_claude_lane.sheets()` on the farm PC. It ships `edits_claude_lane.py` as an input and lifts it, the same way `first_look_job.py` lifts `page_judge.py`, so the sheet code has one source. **Byte-identical sheets on 3 of 3 real waiting videos** vs `sheets()` here. |
| 4 | **Blocked on** | Flashcut 1 BOSS: their `farm_dispatch` only runs a script inside `neuraltrack`. Needed: copy the job script into `neuraltrack/tools/farm/jobs/` and add a `sheets` kind to `tools/farm/submit_job.py` (about 6 lines, written out in `tools/farm_jobs/FLASHCUT_ASK.md`). Flashcut's files were only read, never changed. |
| 5 | **Size of the job** | 540 waiting videos, 4.3 GB (8.1 MB each) -> **14 farm jobs** of <= 40 videos, each under 1.2 GB (Flashcut's whole-file limit is 1.5 GB). |
| 6 | **When this PC still makes sheets** | Only with `--local`, or for a job no farm PC took within 20 min. That job is then retired with the lane's `cancel/<job id>` marker so it is never done twice, the same rule as BL-1653. Every reason goes to `<lane>/farm_sheets.log`. |
| 7 | **The pod** | Not used. The videos (4.3 GB) and `edits.db` live on this PC; the farm is on the office LAN (BL-1653: 57 MB moved in minutes), while the pod is over the internet. ALFRED 13:36: work that needs edits.db/the app cannot move to the pod. |
| 8 | **1 LEADS order watcher** | Running: the 1 LEADS window was restarted by the launcher at ~18:27 and took both 18:29 orders (BL-1656 and BL-1657 claimed 18:31). Nothing for 3 FIXER to restart. |

## Tests
- `tests/test_farm_sheets.py` (9, synthetic: fake lane, fake farm, no ffmpeg) checks four things:
  - jobs split by count and by bytes; the zip carries `keys.json` with the header;
  - batch folders match the prep format, and an unreadable video is counted and skipped;
  - farm first: 2 jobs, 0 on this PC, zips deleted. An untaken job falls back here with the reason logged. `--local` never touches the farm. Videos already in a batch are skipped;
  - a job nobody takes leaves the cancel marker after 20 min, and a done job comes home.
- **9/9 pass. Control: `clippershq/farm_sheets.py` does not exist at HEAD, so every test fails on the old code.**
- Parity: `scratch/bl1658/parity.py`, job script vs `edits_claude_lane.sheets()` on 3 real pending videos: 3/3 identical.
- `tests/run_all.py` not run: two new files and their own test; no existing file changed.

## Next
1. Flashcut 1 BOSS applies `tools/farm_jobs/FLASHCUT_ASK.md` (route: ALFRED).
2. 2 APP (owner of BL-1654) runs `Python311 clippershq/farm_sheets.py prep bl1654_farm` instead of `scratch/bl1654/prep_par.py`, then runs the Sonnet look and ingest as before.
