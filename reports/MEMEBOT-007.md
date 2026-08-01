# MEMEBOT-007: The first video exists — and it cost $0.0006

**Date:** 2026-08-01 · **Class:** End-to-end delivery · **Spend:** **$0.0006 of $0.05** — one paid call. `clippershq` modules untouched; changes confined to `memebot/` and the session scratchpad.
**Claim:** `MEMEBOT-007` filed at start, ended at close.

**Watch it:**
`memebot/scraper/clips/tiktok/cultureh0f/final/gainzalgo/3903533101225116852_80578444437.mp4`
**16.5 MB · 39.3 s · h264 High · yuv420p · 1080×1920 · 3.35 Mbps · aac 44.1 kHz stereo.**

**Its record:** `memebot/runs.jsonl`

```json
{"ts": "2026-08-01T15:15:28", "clip_id": "3903533101225116852_80578444437",
 "account": "cultureh0f", "permalink": "https://www.instagram.com/reel/DYsIqx7gIS0/",
 "play_count": 42468237, "song": "scratch/song01.mp3", "start_sec": 120.0,
 "end_sec": 162.0, "template": "gainzalgo",
 "output": "clips/tiktok/cultureh0f/final/gainzalgo/3903533101225116852_80578444437.mp4",
 "source_bytes": 4541383, "pages_fetched": 1, "cost_usd": 0.0006}
```

---

## 1. Picking, on fields that hold

Ranked on `play_count` and `engagement_per_follower` only. `save_count` excluded — its absence correlates with the account, so ranking on it ranks accounts.

Measured fill on the library **as it stands now (772 clips, 67 accounts)** — and it has moved since BL-847:

| field | now | BL-847 |
|---|---|---|
| play_count / permalink / clip_id | **100%** | 100% |
| engagement_per_follower | 55.6% | — |
| layout | **55.6%** | 67.4% |
| track_title | 42.9% | 58.8% |
| content_genre | **37.7%** | 28.3% |
| save_count | 17.5% | 21% |

The library grew 755 → 772 between the two measurements and every inferred field moved by 5–16 points, in both directions. That is worth knowing before anyone hard-codes a threshold against one of them. The two fields I ranked on did not move: they are 100%.

Top 5 came from **5 distinct accounts**, so no account dominated the shortlist:

| # | account | play_count | epf | clip_id |
|---|---|---|---|---|
| 1 | cultureh0f | 42,468,237 | 46.6 | `3903533101225116852_80578444437` |
| 2 | self_respect_club | 23,643,085 | 16.5 | `3430176313047013174_65975240301` |
| 3 | rascals | 22,868,432 | 25.5 | `3712056345639094481_333045814` |
| 4 | clipcapture.tv | 21,875,298 | 13.8 | `3915146003363721805_80072930752` |
| 5 | solidshampooz | 19,061,115 | 197.2 | `3704370692815734839_6686166013` |

## 2. Retrieval — one call, first page, first candidate

`clip_media.retrieve(clip_id, fetch_clips_page=…, http_get=…, max_pages=2)`, with the fetcher from `ig_client.make_clip_fetch_page()`. The `clip_id` from the library was used as-is; nothing was reconstructed.

```
[1/5] 3903533101225116852_80578444437  (cultureh0f, 42,468,237 plays)
      pages=1  ok=True  err=None  (3.9s)
      rendition: height 1920, width 1080, bandwidth 853509, mime video/mp4
      wrote 4.54 MB
```

**Cost: 1 call, $0.0006.** The remaining four candidates were never fetched.

Worth noting: the retrieved DASH rendition is **VP9**, not h264. Harmless here because the pipeline re-encodes to libx264, but anything that assumes h264 on the retrieved file will be wrong.

## 3. Song and window — explicit, not inferred

`song01.mp3` was where you said (162.5 s, 128 kb/s). I used **`ambient_bed.file`** from MEMEBOT-005 rather than the one-file-folder trick — an explicit path is cleaner than making randomness deterministic by starving it.

The window was **hand-marked from an energy map**, not from `_find_loudest_window_start`:

```
t= 60- 90s  peak RMS -8.6 .. -9.7 dB      <- first sustained loud section
t= 90-120s  peak RMS -11.6 .. -13.4 dB    <- dip
t=120-150s  peak RMS -8.5 .. -9.3 dB      <- loudest sustained section
t=150-162s  peak RMS -20.2 .. -30.9 dB    <- outro
```

Marked **120.0 → 162.0**. The render log confirms it took the explicit path:

```
ambient_bed  song01.mp3 @ -39.2dB [relative (src -22.0dB -17.2dB)],
             start=120.0s [explicit-window] (always)
```

## 4. Proof the hook landed where it was asked to

The output's energy contour is the song's own contour from 120 s, shifted down by the applied bed volume — including the outro decay after 150 s, which is a signature no fade would produce:

| output t | song t | output mean | song mean | delta |
|---|---|---|---|---|
| 0–5 s | 120–125 | −51.0 dB | −11.5 dB | −39.5 |
| 5–10 s | 125–130 | −48.8 | −9.4 | −39.4 |
| 10–15 s | 130–135 | −48.4 | −9.1 | −39.3 |
| 15–20 s | 135–140 | −48.6 | −9.3 | −39.3 |
| 20–25 s | 140–145 | −53.4 | −14.1 | −39.3 |
| 25–30 s | 145–150 | −58.2 | −18.9 | −39.3 |
| 30–35 s | 150–155 | −62.3 | −23.0 | −39.3 |

A constant −39.3 dB offset against the logged −39.2 dB bed. The start offset landed on 120.0 s exactly.

Audio and video durations match to 13 ms (39.333 s video / 39.346 s audio), so it is in sync.

---

## What broke

**1. The first render was 120 MB at 25 Mbps — unpostable.** The cause is `frame_noise`, and it is the whole cause:

| grain | size | bitrate |
|---|---|---|
| enabled (shipped default) | **120,176,283 b** | **25.1 Mbps** |
| disabled | **16,474,406 b** | **3.35 Mbps** |

**7.3×.** Random grain is expensive to encode and x264 at CRF 20 faithfully spends bits on it. The delivered file is the grain-off render. I restored `frame_noise: true` because it is a deliberate fingerprint-evasion feature and turning it off is your call — but **as shipped, every output is ~25 Mbps**, and that needs either lower grain strength, a `-maxrate`/`-bufsize` cap, or a higher CRF.

**2. The bed is too quiet, and it will be on every retrieved clip.** The output sits at −49.4 dB mean. The retrieved DASH video rendition is **video-only** — no audio stream — so relative volume mode fell back to its `-22.0 dB` placeholder basis and computed a bed level for a source that has no level. MEMEBOT-005 flagged this exact defect on a synthetic silent clip; here it bit a real deliverable, and **it will bite every clip retrieved this way**, because the video rendition never carries audio. The fix stands as written there: fall back to absolute volume when the source has no audio track.

**3. Library fill rates have drifted** 5–16 points from BL-847 in both directions, as tabulated above.

## The record — the missing piece

`memebot/scraper/run_record.py`, 40 lines including the reasoning. `record(**fields)` appends one JSON line to `memebot/runs.jsonl`; `rows()` reads them back; `already_used(clip_id)` answers the question that makes this a loop rather than a one-off. Verified live: `already_used(<this clip>) -> True`, `already_used('123_456') -> False`, ledger holds 1 row.

It is append-only JSONL at the repo root — no schema, no database, and a torn final line is skipped rather than poisoning the file.

## State on exit

`config.yaml` restored to shipped defaults: `ambient_bed.enabled: false`, no `file`/`start_sec`/`end_sec`, `frame_noise: true`, CRF still pinned at 20 from MEMEBOT-005. The retrieved source clip and the finished render are left in place. `runs.jsonl` has its first row.

## Limits

One clip, one song, one template (`gainzalgo`, full-bleed). The window is my judgement from an RMS map, not yours — if 120–162 s is the wrong hook, the pipeline will place the wrong one just as precisely. Sync was confirmed by stream durations and by the energy contour matching, not by watching the video. The four unfetched candidates were never validated as retrievable.
