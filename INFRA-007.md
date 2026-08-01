# INFRA-007: Everything runs. One video came out. It is not postable.

> **CORRECTED 2026-08-01 by MEMEBOT-026 — two claims below are wrong.**
>
> **1. "32% duplicate rows" / "the library is 664 clips" is WRONG.** That was a raw row
> count of an append-only log presented as corruption. Every row carries a `rev`; the
> surplus rows are revisions written by the vision-labelling rounds, not copies. The
> canonical reader `clip_library.read_all()` is documented LAST-WINS by (clip_id, rev)
> and already resolves them. Nothing was double-counted and **nothing should dedup it**.
>
> **2. "62/62 suites green" describes the runner, not the tree.** `run_all.py` searched
> `tests/` only. Fifteen further test files existed holding **637 test functions** —
> including the caption fitter this very report caught shipping broken. CI now discovers
> nested `tests/` directories: 81 suites, 3,556 checks.
>
> Full detail and how to re-derive both: `docs/CORRECTIONS.md` and MEMEBOT-026.md.

**Date:** 2026-08-01 · **Class:** Integration check, read-only · **Spend:** **$0.0024** of the $0.05 budget (4 paid calls at $0.0006).
**Claim:** `INFRA-007`, READ-ONLY, filed at start. I changed no pipeline code, no config and no committed file.
**Eleven other rounds were in flight the whole time** and several were writing the files I was measuring. Where that changed a result under me, I say so inline — it is a finding, not a footnote.

---

## The headline: yes, a video came out. No, you cannot post it.

```
python scratch/memebot010_run.py --n 1
  library 664 clips -> 3 candidates for 1 video(s)
  [1/1] 3949591972384081465_60028400938 @borcellae_
      window fitted: marked window 20.0-25.0s is shorter than the 43.0s clip
                     -> widened to 20.0-64.0s
      1280p, 2016.8 KB -> song song01 [matched] 20.0-64.0s
      ok -> .../final/white_frame/3949591972384081465_60028400938.mp4 (81968.1 KB)
RESULT memebot010: made=1 attempted=1 calls=1 cost=$0.0006 wall=52.1s
```

Every stage of the real path fired: pick → match → retrieve → render → record. One paid call, $0.0006, 52 seconds, no crash. **The plumbing is connected end to end and it works.**

Three things stop the file being postable, in order of severity:

**1. The caption is cut off mid-sentence.** I pulled frames at t=12 s and t=30 s. The overlay reads:

> `Brad Pitt ruined Tarantino's original script in the best way possible… Aldo Raine was`

— and runs off the right edge of the 1080-px frame, clipped at both ends, on every frame. It is rendered as one unwrapped line. This is the single most visible defect and nothing in the round that built the caption path measured it. **Not previously reported by any round.**

**2. 82 MB for 41.6 seconds — 16.15 Mbps.** This is the grain lottery from MEMEBOT-011 landing on a bad roll. The shipped range is `strength 4-12` and it straddles the cost cliff I measured between 4 and 6. I recommended `2-4` in `config.yaml` and deliberately did not change it; this render is what the un-narrowed range costs in practice. Instagram will re-encode it, but 82 MB is a slow upload and a wasteful master.

**3. About 40% of the frame is dead black.** The source clip carries its own letterboxing, and the template pads on top of it. Vertically the actual picture occupies roughly the middle 55% of a 1920-px canvas.

The video is *technically* correct — it plays, it has sound, the codecs are right. It is not *publishable* output.

### The hook window is a placeholder, and it visibly drove this render

Stated plainly, because the run log makes it easy to miss: `song01`'s window `20.0-25.0s` was **never marked by ear**. `scratch/songs.json` says so in its own header — *"Every start_s/end_s below is a PLACEHOLDER put here so the plumbing has something to run against… they were NOT chosen by listening and they are NOT drop positions."* MEMEBOT-008 refused to fabricate them and the operator has not marked them since.

The consequence is in the log: the 5-second placeholder was **widened to a 44-second window** to cover the clip. So the audio in this video is not a hook, not a drop, and not a chosen section — it is 44 seconds of `song01.mp3` starting from an arbitrary 20-second mark. The matcher ran and reported `[matched]`, which is true of the *tier logic* and says nothing about the window being any good. **Treat the audio in this deliverable as unchosen.** The other two songs in the library are templates with no file behind them.

---

## 1. The suite, and the marker side effect

**62/62 suites, 2,633 checks, all green.** Run with `PYTHONUTF8=1`.

**The marker side effect still reproduces.** After the suite, three files carry `"status": "running"`:

| file | pid | stamped |
|---|---|---|
| `scratch/spotify_finder.status.json` | 15600 | 15:45:40 |
| `scratch/twitch_finder.status.json` | 15600 | 15:45:42 |
| `scratch/youtube_finder.status.json` | 15600 | 15:45:42 |

**Same pid, two seconds apart** — the signature of one import, not three runs. Pid 15600 is long dead.

**But the user-visible symptom is already contained.** `/api/now` returns `"running":[]` and files all three under `idle`. INFRA-004's pid-liveness check catches the stale markers and does not report phantom funnels. So this is now a dirty-scratch-directory problem, not a lying-dashboard problem. INFRA-006 is in flight on the root cause.

## 2. Dashboard

Server on **127.0.0.1:8787** (not 8000). Measured at 16:02.

| route | result |
|---|---|
| `GET /` | **404 — the static frontend is not mounted** |
| `/api/health` `/api/files` `/api/history` `/api/now` `/api/settings` `/api/spend` `/api/videos` | 200 |
| `GET /api/start` | 405 (POST-only, by design) |

**Every endpoint `app.js` calls exists and answers.** The backend/frontend contract holds — there is no mismatch left in the six data routes.

**The one contract bug I found was fixed underneath me during the round.** `app.js` was probing `/api/start` with the tolerant `get()` helper, which turns a 405 into `null`, so the Start button shipped permanently disabled against a working backend. When I re-read the file it had been rewritten (`app.js:463-471`) to probe by method and treat anything other than 404/502 as present, with a comment explaining exactly that. I did not do this. Someone else did, mid-round.

**`GET /` returning 404 is the remaining blocker** — there is no way to reach the UI from a browser. Whether the running server matches the 16:00 on-disk `server.py` is unknown; I did not restart it.

**Settings count: `/api/health` reports `settings_exposed: 44`, not the spec's 16.** INFRA-006 holds the curation task.

`/api/videos` returns *"Nothing yet — memebot is not wired."* — literally true of the dashboard, and now false of the pipeline: a video exists, the dashboard just cannot see it. `/api/history`: `total_ledger_rows: 151, rows_with_run_id: 0` — no run is traceable end to end yet.

## 3. The three render fixes — all hold, verified on this output

| fix | expected | measured | verdict |
|---|---|---|---|
| yuv420p (MEMEBOT-005) | `yuv420p` | `h264 High, 1080x1920, pix_fmt=yuv420p` | **holds** |
| solo audio (MEMEBOT-011) | −14…−6 dB when source is video-only | source probes `vp9, video` — no audio stream; output **mean −25.8 dB, max −10.9 dB** | **holds** |
| grain (MEMEBOT-011) | configured 4–12 | 16.15 Mbps / 82 MB | **applied — at the top of the range** |

The solo branch fired correctly: the retrieved DASH rendition is VP9 video-only, so the bed became the whole soundtrack at a listening level rather than the −49 dB it produced before the fix. `blackdetect` found no black segments; both sampled frames are real picture.

**Honest limit on "play the output":** I verified this by measurement and by extracting and looking at frames. I cannot listen to it. The levels are right and the stream decodes; whether the music actually suits the clip is a judgement only you can make — and per the placeholder window above, there is good reason to think it does not.

## 4. Library — grew a lot, and two fields went backwards

**Count everything by distinct `clip_id`.** The raw files disagree with themselves:

```
rows on disk          977
distinct clip_id      664     <- what the orchestrator reports
duplicate rows        313     (32.0% of rows re-write a clip already present)
```

**Nearly a third of `clip_library/*.jsonl` is duplicate rows.** `loste1980` has 244 rows for 122 clips — exactly 2×. Any tool that counts rows overstates the library by half. MEMEBOT-007's "772 clips" was almost certainly a row count, which makes a direct clip-to-clip comparison against it unsafe; the fill percentages below are still comparable because both are ratios.

| metric | now (deduped) | MEMEBOT-007 |
|---|---|---|
| distinct clips | **664** | 772 (row count) |
| distinct accounts | **68** | 67 |
| top-2 share | **31.2%** (loste1980 122, movies.avengers 85) | — |

**Fill, and which way it moved:**

| field | now | MB-007 | move |
|---|---|---|---|
| engagement_per_follower | 69.1% | 55.6% | **+13.5 up** |
| layout | 69.1% | 55.6% | **+13.5 up** |
| duration_s | 63.7% | 55.4% | +8.3 up |
| save_count | 22.3% | 17.5% | +4.8 up |
| play_count / permalink | 100.0% | 100.0% | flat |
| track_title | 34.5% | 42.9% | **−8.4 DOWN** |
| content_genre | 27.4% | 37.7% | **−10.3 DOWN** |

**The drift MEMEBOT-007 flagged is still happening and still runs both ways.** The structural fields the pipeline computes itself (layout, engagement, duration) are climbing. The two fields that depend on what Instagram chose to return — `track_title` and `content_genre` — are falling, by 8 and 10 points. New clips arrive with those fields emptier than the old ones. That is a supply property, not a bug, but it means genre- and track-based matching tiers cover less of the library every week.

**The library grew while I measured it** — 969 → 972 → 974 → 977 rows across four reads in about twenty minutes. BL-851 is in flight growing it to 2,000.

**Fields declared by recent rounds but absent from stored data:** `run_id` 0/664, `vision_verdict` 0/664, `vision_labels` 0/664, `ocr_text` 0/664, `speech_frac` 16 (2.4%), `format` 20 (3.0%), `subtitle_text` 3. BL-849 (vision labelling) and BL-852 (speech) are both still in flight, so these are expected-empty rather than broken — but nothing downstream can rely on them today.

## 5. Built but not connected

| piece | exists | wired to | state |
|---|---|---|---|
| `clippershq/song_library.py` | yes | `clip_pipeline.py`, tests | **wired** |
| `clippershq/clip_pipeline.py` | yes | `scratch/memebot010_run.py`, tests | **wired — but only from `scratch/`** |
| `clippershq/clip_media.py` | yes | `clip_pipeline.py`, `clip_runner.py` | **wired** |
| `clippershq/ocr_features.py` | yes | `frame_pipeline.py`, tests | wired |
| `memebot/scraper/run_record.py` | yes | **nobody** | **orphaned** |
| hook-window marker | **no** | — | placeholders only; MEMEBOT-012 building the UI now |
| feedback loop (posted → performance → ranking) | **no** | — | nothing exists |

**Two ledgers are competing.** `memebot/runs.jsonl` (1 row, written by MEMEBOT-007's `run_record.py`) and `scratch/renders.jsonl` (13 rows, written by `clip_pipeline.append_record`). Nothing imports `run_record` any more — MEMEBOT-010 wrote a second recorder rather than adopting the first. One of them should be deleted before a third appears.

`renders.jsonl` holds **8 `pending` rows and 5 `ok`**. The pending ones are dry-run residue.

**Shortest path to a working loop, in order:**
1. **Mark hook windows by hand** — the only step nothing can automate, and the one that decides whether output is worth posting. MEMEBOT-012's UI is in flight; the marking itself is yours.
2. **Fix caption wrapping** — one-line change in the render path, currently the most visible defect.
3. **Narrow grain to 2–4** — one config edit, ~8× smaller files.
4. **Mount the dashboard frontend** (`GET /` → 404) and point `/api/videos` at `renders.jsonl`.
5. **Pick one ledger**, delete the other, and stamp `run_id` so `/api/history` can trace a run.

Steps 2–5 are hours. Step 1 is the gate, and it is a listening task.

## 6. Regressions from twelve concurrent rounds

**Nothing regressed in the test suite** — 62/62, 2,633 checks green, and the campaign hash is unchanged.

Four real problems, none of them a broken test:

1. **`--dry-run` spends money.** `memebot010_run.py:4` documents it as *"no paid call, no render"*. It is only "no render": the `dry_run` check sits at `clip_pipeline.py:1037`, **after** retrieval has already fetched bytes and counted pages. My dry run made **3 paid calls and cost $0.0018**. That is most of what I spent this round.
2. **`--dry-run` exits 1.** `memebot010_run.py:116` is `return 0 if summary["made"] else 1`, and a dry run always has `made == 0`. Any CI or wrapper treating exit code as truth will read a clean dry run as a failure.
3. **32% duplicate rows in `clip_library/`**, and consumers disagree about what "clip count" means depending on whether they dedupe.
4. **The orphaned recorder / two-ledger split** above.

**Live-edit evidence.** These files changed *while this check was running*: `dashboard/server.py` 16:00:54, `dashboard/static/app.js` 16:00:06, `clippershq/clip_pipeline.py` 15:59:14, `memebot/scraper/edit.py` 15:49:11, `song_library.py` 15:48:20. One of them now contains a comment reading *"Found by INFRA-007 running this module during the round"* (`clip_pipeline.py:1038`) — a fix attributed to my round that I did not write, describing a dry-run bug my dry run had exposed twenty minutes earlier. Rounds are reacting to each other's side effects in real time.

---

## Limits

One video, one clip, one song, one template — the render findings are a single sample, and grain in particular is a per-render dice roll, so a second run would produce a different bitrate. Fill comparisons are against MEMEBOT-007's numbers as published; I could not re-derive its 772 on today's data and believe it counted rows. I probed the dashboard against a server process started before the 16:00 edits, so its behaviour may not match `server.py` on disk. I did not restart it, did not test the UI in a browser (`GET /` is 404), and did not listen to the audio. Eleven rounds were writing throughout; every number here is a snapshot with a timestamp, not a stable state.
