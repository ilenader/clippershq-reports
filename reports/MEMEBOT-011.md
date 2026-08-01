# MEMEBOT-011: The bed is audible, and grain has a price list

**Date:** 2026-08-01 · **Class:** Fix + measurement · **Spend:** $0.00, no paid calls. `memebot/` only — `memebot/scraper/edit.py` and `config.yaml`, both backed up (`*.20260801_152229.mb011.bak`).
**Claim:** `MEMEBOT-011` filed at start, ended at close. Eight rounds were in flight; none touched these two files.

Tested on the **real retrieved clip** from MEMEBOT-007 (`3903533101225116852_80578444437`, VP9, video-only), not a synthetic.

---

## 1. The −49.4 dB bed: fixed, and the diagnosis was slightly wrong

The defect was structural as described — but "switch to absolute" would only have half-fixed it. A source with no audio has no level to sit *under*, and in that case the track is not a background bed at all: **it is the entire soundtrack**. Putting it in the absolute bed range (−38…−28 dB) would have moved it from inaudible to merely too quiet.

So the fix adds a third mode. When `source_has_audio()` is false, volume comes from a new **`solo_volume_db_min/max`, defaulting to −14…−6 dB** — a listening level, not a bed level. Relative mode's −22 dB placeholder is bypassed entirely.

**Proof on the retrieved clip:**

```
before  ambient_bed  song01.mp3 @ -39.2dB [relative (src -22.0dB -17.2dB)]
        output mean -49.4 dB   max -37.3 dB

after   ambient_bed  song01.mp3 @ -10.6dB [solo (source has no audio track)]
        output mean -23.0 dB   max  -8.7 dB
```

**+26.4 dB.** The output mean sits at −23 dB with peaks near −9 dB, which is a normal music level — the mean is pulled down by the song's own outro inside the chosen 120–162 s window, not by the mixer.

The log line names the mode (`[solo (source has no audio track)]`), so this can never again be mistaken for a working relative computation.

## 2. Grain: a price list, and the shipped range straddles a cliff

Same clip, preset pinned to `fast`, every other transform held, only grain varying:

| strength | size | bitrate | vs off |
|---|---|---|---|
| off | 3,610,457 | 0.76 Mbps | 1.00× |
| 2 | 4,055,550 | 0.84 Mbps | **1.12×** |
| 4 | 4,539,229 | 0.91 Mbps | **1.26×** |
| 6 | 10,342,356 | 2.05 Mbps | **2.86×** |
| 8 | 17,172,444 | 3.49 Mbps | 4.76× |
| 12 | 35,785,092 | 7.18 Mbps | **9.91×** |

**The cost is sharply non-linear and the cliff is between 4 and 6.** Going 2→4 costs 14 percentage points; 4→6 more than doubles the file; 12 costs ten times.

The shipped range is **4–12, which straddles the cliff** — so identical input renders anywhere between 0.9 and 7.2 Mbps depending on the roll. That is the real defect: not that grain is expensive, but that its price is a lottery.

**Recommendation, written into the config beside the setting: `strength_min: 2, strength_max: 4`.** Grain and its per-frame reseeding are retained for fingerprint evasion at ~1.1–1.3× instead of up to ~10×. **I did not change the values** — it is a deliberate evasion feature and the trade is yours. The table is now in `config.yaml` where the choice is made.

**And the cost is now printed at render time**, so a roll of 11 announces itself:

```
frame_noise  7    (range 4-12) ~~3.5x bitrate vs no grain
```

**Honest caveat:** the absolute Mbps here (0.76 off) is lower than MEMEBOT-007's (3.35 off) because sharpening, zoom and speed also roll per render and were free to vary between those two runs. **The ratios are the finding** — those were measured with everything but grain held fixed.

## 3. VP9 — noted, not fixed

A comment now sits at the encoder branch in `edit.py`, immediately where the dangerous optimisation would be added:

> The "best" DASH video rendition is **VP9, not h264**, and carries **no audio stream**. Harmless because everything re-encodes with libx264 and takes audio from the ambient input. It stops being harmless the moment someone adds `-c:v copy` for speed — that silently produces VP9-in-mp4 which players and platforms reject — or assumes `-c:a copy` has something to copy, which fails outright on a video-only source. Probe, do not assume.

## 4. Fades: verified, both directions

Rendered at 3.0 s in / 4.0 s out on the video-only clip, so the bed is the only audio and the envelope is unambiguous. Measured per half-second:

**Fade-in** — ramps and then plateaus exactly at the configured 3.0 s:

```
t=0.0 -46.3   t=0.5 -39.6   t=1.0 -36.5   t=1.5 -34.6   t=2.0 -31.5
t=2.5 -22.3   t=3.0 -20.8   t=3.5 -19.6   t=4.0 -19.9   t=4.5 -19.9   (plateau)
mid  t=19.6 -21.2
```

**Fade-out** — monotonic decline through the last ~4 s to silence (output ends 39.13 s):

```
t=34.1 -33.8   t=35.1 -37.6   t=36.1 -41.9   t=37.1 -45.7
t=38.1 -53.7   t=38.6 -71.9
```

Part of that slope is the song's own outro (the window runs into it), but the terminal **−71.9 dB** is the fade: the song at the corresponding point is −28 dB. Both fades work as configured.

---

## State on exit

`config.yaml` back to shipped defaults — `ambient_bed.enabled: false`, no `file`/`start_sec`/`end_sec`, fades 0.4/0.8, grain 4–12 unchanged, preset options unpinned, CRF still pinned at 20. New keys `solo_volume_db_min/max` (−14/−6) are additive and inert until a video-only source is rendered. `edit.py` parses; `config.yaml` parses.

## Limits

One clip, one song, one template. The grain table is a single clip's content — a static talking-head would show a smaller absolute spread than this fast-cutting comedy edit, though the shape of the curve should hold. "Normal listening level" is judged from measured dB, not by ear. The solo range (−14…−6) is a reasonable default I chose, not an optimum. Fade timing was verified in 0.5 s steps, so the ramp is located to ±0.5 s. I did not test a source that *has* audio through the new branch — that path is unchanged code, but it is untested by this round.
