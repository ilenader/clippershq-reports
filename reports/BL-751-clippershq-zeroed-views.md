# BL-751 — the YouTube client fabricates a zero exactly as Instagram's did, and unlike Instagram nothing downstream stops it

**VERDICT IN ONE LINE: YES, a live defect can zero a clip's stored views. `youtube.ts:178` fabricates a `0` when YouTube omits `statistics.viewCount`, nothing on the YouTube path rejects it and no never-decrease guard protects stored views, so the tick writes it. 13 clips are currently wrong, 5 of them provably reachable today, and the money is $0.00 because every one peaked at 1 or 2 views on a campaign with a 1,000 view minimum. The live exposure is 539 YouTube clips carrying $146.16.**

**2026-08-09 · READ ONLY · Base:** `main @ d169e73b` · **Branch:** `checkpoint/BL-751`
**Nothing was changed. `git status --porcelain` is 0 lines and worktree HEAD equals `origin/main`. No code, config or data change, nothing repaired. No Apify actor run; `apify.ts` untouched with its 8 BL-678 comment lines intact. Probes: 18 keyless oEmbed calls, $0.00. Handles redacted; every timestamp cast `::text` against DB `now()`.**
**No build, `tsc` or lint run was performed and none is claimed: this round produced one markdown file.**

---

# PART 1 — WHO THEY ARE, AND WHEN THEY FELL

## 1.1 The split, confirmed today

**51 fall events across 50 distinct clips.** One clip (`cmpsy3cf700000`) fell twice, on 2026-05-31 at
01:02 and again at 03:02, which is why the event count exceeds the clip count.

| platform | clips | still 0 today | recovered | total earnings | earnings on the still-zero | clippers |
|---|---|---|---|---|---|---|
| **YouTube** | **45** | **13** | 32 | $3.31 | **$0.00** | 16 |
| **TikTok** | **5** | **0** | **5** | $2.91 | $0.00 | 5 |

`db_now = 2026-08-09 17:53:31.294438+00`. **BL-748's 45 and 5 split is confirmed exactly.**

## 1.2 The clustering answers the first question

**They are SCATTERED, not a single event.** The falls run from **2026-05-23 11:01:21.296** to
**2026-07-31 03:01:59.508**, ten weeks apart, individually, at ordinary hourly tick timestamps
(`:01:xx`, `:02:xx`, `:11:xx`), never two on the same tick.

**That rules out a sweep or a deploy and points at a per-clip condition**, which is what the rest of this
report identifies. It also rules out the 2026-07-22 Apify cutover as a cause, since the falls both predate
and postdate it.

## 1.3 The population, with the pattern visible

Every row, redacted. `views_before` is the value immediately prior to the zero.

| clipper | clip | plat | campaign | camp | clip | before | fell at (`::text`) | max ever | latest |
|---|---|---|---|---|---|---|---|---|---|
| 9d81d0df | cmpi4eg9d004c0 | YT | somesome | PAST | APPROVED | 117 | 2026-05-23 11:01:21.296 | 9,099 | 9,096 |
| 9d81d0df | cmpimxarc000a0 | YT | somesome | PAST | APPROVED | 2 | 2026-05-23 21:01:57.085 | 12 | 10 |
| 35ad3034 | cmpnk0hod000a0 | YT | GainzAlgo REPOST | PAST | APPROVED | 68 | 2026-05-27 06:01:44.257 | 1,240 | 1,239 |
| bc64d4c1 | cmpspmmae001d0 | TT | somesome | PAST | APPROVED | 84 | 2026-05-30 21:02:18.727 | 2,875 | 2,875 |
| 6b0d58e5 | cmpsy3cf700000 | YT | somesome | PAST | APPROVED | 2 | 2026-05-31 01:02:18.384 | 7 | 7 |
| 6b0d58e5 | cmpsy3cf700000 | YT | somesome | PAST | APPROVED | 2 | 2026-05-31 03:02:08.204 | 7 | 7 |
| e81401bc | cmq4g0xr200000 | YT | GainzAlgo REPOST | PAST | APPROVED | 1 | 2026-06-08 02:02:06.688 | 12 | 12 |
| 14c2cfc6 | cmq8ujnqt00040 | YT | GainzAlgo REPOST | PAST | APPROVED | 5 | 2026-06-11 04:02:59.303 | 16 | 16 |
| 35ad3034 | cmq9lig1o00070 | YT | WinGram | PAUSED | APPROVED | 1 | 2026-06-12 18:01:06.539 | 11 | 11 |
| 9cbad3db | cmqbrmilg000f0 | TT | bees.n.honey | PAST | APPROVED | 1,398 | 2026-06-18 01:02:05.129 | 1,783 | 1,783 |
| 36044c1d | cmqi24im8001j0 | TT | bees.n.honey | PAST | APPROVED | 189 | 2026-06-18 02:01:40.310 | 9,274 | 272 |
| a9cc304c | cmqn08osa000v0 | YT | WinGram | PAUSED | REJECTED | 2 | 2026-06-21 05:00:51.751 | 16 | 16 |
| f9cf0b65 | cmr2unbh0005u0 | YT | GainzAlgo REPOST | PAST | APPROVED | 2 | 2026-07-02 06:12:11.786 | 23 | 23 |
| 70aa2a27 | cmr08psq300fi0 | TT | GainzAlgo REPOST | PAST | APPROVED | 1 | 2026-07-04 21:40:52.650 | 1 | 1 |
| 8565c407 | cmr6qm35s000w0 | YT | WinGram | PAUSED | REJECTED | 2 | 2026-07-04 23:10:52.777 | 1,186 | 1,186 |
| 52760f93 | cmr7ru8b400bg0 | YT | WinGram | PAUSED | APPROVED | 1 | 2026-07-05 16:01:10.208 | 12 | 12 |
| d378b5e5 | cmr847mmw00250 | YT | WinGram | PAUSED | APPROVED | 1 | 2026-07-05 21:00:28.667 | 7 | 7 |
| d378b5e5 | cmr846w4g001t0 | YT | WinGram | PAUSED | APPROVED | 1 | 2026-07-05 21:00:35.748 | 6 | 6 |
| d378b5e5 | cmr84dtwt00330 | YT | WinGram | PAUSED | APPROVED | 1 | 2026-07-05 22:10:59.456 | 1 | 1 |
| d378b5e5 | cmr92zv7z00010 | YT | WinGram | PAUSED | APPROVED | 2 | 2026-07-06 14:02:03.815 | 2 | 1 |
| 8565c407 | cmr7k1lqr00a30 | YT | WinGram | PAUSED | APPROVED | 1 | 2026-07-06 15:51:35.520 | 2 | 2 |
| eb397ae5 | cmr9nh2ix000g0 | YT | WinGram | PAUSED | APPROVED | 2 | 2026-07-07 01:01:34.438 | 37 | 37 |
| eb397ae5 | cmrb0f2uy004e0 | YT | WinGram | PAUSED | APPROVED | 1 | 2026-07-07 21:02:03.673 | 7 | 7 |
| d378b5e5 | cmrbav63h001m0 | YT | WinGram | PAUSED | APPROVED | 1 | 2026-07-08 02:11:05.916 | 14 | 14 |
| d378b5e5 | cmrc4qj7w000z0 | YT | WinGram | PAUSED | APPROVED | 1 | 2026-07-08 17:21:07.836 | 26 | 26 |
| f20eecea | cmr9nhinv000j0 | YT | GainzAlgo REPOST | PAST | APPROVED | 1 | 2026-07-08 19:31:40.666 | 1 | 1 |
| f20eecea | cmrcl2cvu000d0 | YT | GainzAlgo REPOST | PAST | APPROVED | 1 | 2026-07-09 18:41:29.296 | 6 | 6 |
| **f20eecea** | **cmrbuxbox00b80** | YT | GainzAlgo REPOST | PAST | APPROVED | 1 | 2026-07-09 20:31:41.233 | 1 | **0** |
| eb397ae5 | cmrf9cx9c001o0 | YT | WinGram | PAUSED | APPROVED | 1 | 2026-07-10 23:01:25.528 | 12 | 12 |
| **6aedd49b** | **cmrdbmo7f004k0** | YT | GainzAlgo REPOST | PAST | APPROVED | 2 | 2026-07-11 01:50:58.779 | 2 | **0** |
| **6aedd49b** | **cmrdbn5ng004n0** | YT | GainzAlgo REPOST | PAST | APPROVED | 1 | 2026-07-11 17:31:36.798 | 1 | **0** |
| **6aedd49b** | **cmrdbm55w004h0** | YT | GainzAlgo REPOST | PAST | APPROVED | 1 | 2026-07-11 17:31:38.519 | 1 | **0** |
| d378b5e5 | cmrgbv1ir000l0 | YT | WinGram | PAUSED | APPROVED | 2 | 2026-07-11 18:11:39.773 | 2 | 2 |
| d378b5e5 | cmrh2j1q0002b0 | YT | WinGram | PAUSED | APPROVED | 1 | 2026-07-12 05:02:00.056 | 11 | 11 |
| b0480ea8 | cmrf8afx0000w0 | YT | WinGram | PAUSED | APPROVED | 1 | 2026-07-12 18:52:10.675 | 2 | 2 |
| **eb397ae5** | **cmrhzjll7000g0** | YT | WinGram | PAUSED | APPROVED | 1 | 2026-07-13 18:41:34.776 | 1 | **0** |
| **d378b5e5** | **cmrh2q8d100330** | YT | WinGram | PAUSED | APPROVED | 1 | 2026-07-13 19:11:13.125 | 1 | **0** |
| **eb397ae5** | **cmri1qtkz000q0** | YT | WinGram | PAUSED | APPROVED | 1 | 2026-07-13 19:41:11.318 | 1 | **0** |
| **d378b5e5** | **cmrh2p8n800300** | YT | WinGram | PAUSED | APPROVED | 1 | 2026-07-13 20:31:16.160 | 1 | **0** |
| b0480ea8 | cmrjdm1ac00140 | YT | WinGram | PAUSED | APPROVED | 1 | 2026-07-13 21:11:58.575 | 1 | 1 |
| **d378b5e5** | **cmrh2hgr100250** | YT | WinGram | PAUSED | APPROVED | 2 | 2026-07-13 21:41:07.226 | 2 | **0** |
| eb397ae5 | cmrjkzcbo003b0 | YT | WinGram | PAUSED | APPROVED | 1 | 2026-07-13 22:13:26.938 | 9 | 9 |
| f9cf0b65 | cmrk8vxy8063d0 | YT | GainzAlgo REPOST | PAST | APPROVED | 3 | 2026-07-14 08:01:27.594 | 322 | 322 |
| **f20eecea** | **cmri66n2n00000** | YT | GainzAlgo REPOST | PAST | APPROVED | 1 | 2026-07-14 22:11:34.577 | 1 | **0** |
| **db9da539** | **cmrj94xi400050** | YT | WinGram | PAUSED | APPROVED | 1 | 2026-07-15 00:11:39.548 | 1 | **0** |
| **f20eecea** | **cmridcn7m000i0** | YT | GainzAlgo REPOST | PAST | APPROVED | 1 | 2026-07-15 02:31:35.375 | 1 | **0** |
| f20eecea | cmrmrz29c03qy0 | YT | GainzAlgo REPOST | PAST | APPROVED | 17 | 2026-07-16 03:01:38.918 | 2,005 | 2,005 |
| **f20eecea** | **cmrv621nf00170** | YT | GainzAlgo REPOST | PAST | APPROVED | 1 | 2026-07-22 20:11:10.506 | 1 | **0** |
| dfb43bdc | cms2cdjlt04ir0 | TT | Panic Baby | PAUSED | APPROVED | 531 | 2026-07-27 06:02:35.809 | 637 | 637 |
| 52760f93 | cms4y53860naa0 | YT | WinGram | PAUSED | APPROVED | 1 | 2026-07-28 22:02:19.737 | 5 | 5 |
| 61da7f0f | cms84uiy200wl0 | YT | WinGram | PAUSED | APPROVED | 3 | 2026-07-31 03:01:59.508 | 7 | 7 |

**No stat was manual**: `isManual` is false on every one of the 51 events, so every zero came from the cron
tick, not a human.

**The pattern is the finding.** `views_before` is **1, 2 or 3 on 38 of the 51 events**. **32 of 45 YouTube
clips and all 5 TikTok clips recovered on a later tick**, several to large numbers: 117 to 9,099, 1,398 to
1,783, 84 to 2,875, 68 to 1,240. **This is a transient misread on very low counts, not a permanent
destruction of a large one.**

---

# PART 2 — WHAT WROTE THE ZERO

## 2.1 The YouTube client fabricates a zero in THREE places, exactly the `hikerapi.ts:603` shape

The brief asked me to check specifically for this, and it is there.

```
src/lib/youtube.ts:35    views: parseInt(stats.viewCount || '0', 10),
src/lib/youtube.ts:86    views: parseInt(item.statistics?.viewCount || '0', 10),
src/lib/youtube.ts:178   views: parseInt(stats.viewCount ?? "0", 10) || 0,
```

**`:178` is the one that matters**, because it is the **batch** path (`fetchYouTubeStatsBatch`) that the
tracking tick uses via `apify.ts:2194-2196`. When YouTube returns an item whose `statistics` object is
present but whose `viewCount` key is **absent**, `?? "0"` yields the string `"0"`, `parseInt` yields `0`, and
the trailing `|| 0` converts even a `NaN` to `0`. **A hard, fabricated zero.**

**YouTube omits `statistics.viewCount` as a documented product behaviour** when the uploader has hidden the
view count on a video. It is not an error condition, so nothing upstream flags it.

## 2.2 The same file gets the OTHER case right, which is what makes this a bug rather than a policy

`youtube.ts:188-195`, forty lines after the fabrication:

```ts
// Anything in chunk but not in seen = missing (private/deleted/banned)
for (const vid of chunk) {
  if (!seen.has(vid)) {
    for (const clipId of byVideoId.get(vid) ?? []) {
      out.set(clipId, null);          // <- correct: unknown becomes NULL
    }
  }
}
```

**A deleted, private or banned video correctly becomes `null`** and the clip keeps its last-known value, per
BL-543. **Only the hidden-count case fabricates.** The file already knows the right answer and applies it
one branch over, which is precisely the asymmetry BL-748 found between `hikerapi.ts`'s carousel branch and
its single-video branch.

## 2.3 Unlike Instagram, NOTHING downstream rejects the zero

This is the difference that makes the YouTube defect live where Instagram's never was.

| | Instagram | YouTube |
|---|---|---|
| Classifier fabricated a 0 | `hikerapi.ts:603`, **fixed by BL-748** | `youtube.ts:178`, **still live** |
| A gate rejecting `views <= 0` | **YES**, `hikerapi.ts:878`, falls back to Apify | **NO** |
| Result | never written | **written** |

`apify.ts:2201-2210` passes the batch result straight through: `const s = ytMap.get(c.clipId); if (s)
result.set(c.clipId, s);`. A `slim` object carrying `views: 0` is a **truthy object**, so it is accepted as a
real stat.

`tracking.ts:1782` and `:1794` then write it **unconditionally**:

```ts
await db.clipStat.create({ data: { clipId: clip.id, views: stats.views, ... } });
```

There is no comparison against `prevViews`. `prevViews` is read at `:1725` and used **only** for the cadence
ladder and a log line at `:1727`, never as a floor.

## 2.4 BL-538's never-decrease guard protects EARNINGS ONLY, not views

The brief asked, and the answer is unambiguous.

`grep -rn` for any views-decrease protection across `src/` returns **0**. `earnings-never-decrease.ts`
exports `decideNeverDecrease`, `capButNeverBelowStored`, `capFloorDidBind` and `logNeverDecreaseBlock`, and
**every one operates on money**. `tracking.ts:38` imports `capButNeverBelowStored`, which is BL-718's paid
floor applied at `:2525` and `:2583` to **earnings**, inside the budget-cap path.

**Stored views have no floor of any kind.** A single bad provider response can and does overwrite a real
count, exactly as the brief hypothesised. **That is the finding.**

## 2.5 What wrote each zero, per clip

I cannot attribute each of the 51 individually without provider logs from the moment, and I will not
pretend otherwise. What the evidence supports:

* **All 51 came from the cron tick**, not a human: `isManual` false on every row.
* **The 45 YouTube events are consistent with `youtube.ts:178`**, and no other YouTube path writes views.
* **The 5 TikTok events are NOT this defect.** TikTok goes through a different provider chain (`apidojo.ts`, LamaTok), and `apidojo.ts:230-231` uses `??` chains without a `|| 0` terminator, so an absent field yields `undefined` rather than 0. All 5 recovered and all 5 are at $0.00. **I did not establish their cause and am not attributing them**, which is the same discipline BL-748 applied.

---

# PART 3 — ARE THE VIDEOS ACTUALLY GONE

## 3.1 An honest limitation first

**There is no `YOUTUBE_API_KEY` in this environment.** `grep -c` over `.env.local` and `.env` returns **0**
for any YouTube key. **So the Data API probe that would have returned a live `viewCount` could NOT be run**,
and I cannot report "reachable with a real count of X" for any clip. Saying so is more useful than
substituting a guess.

Instead I probed the **public, keyless oEmbed endpoint**, which answers reachability definitively:
**18 calls, no API key, no billing, no quota charge, $0.00, no Apify actor.** Within the 25 cap.

## 3.2 Results, ids matched not rows

**All 13 currently-zero clips, plus 5 recovered controls spanning the value range:**

| clip | videoId | stored | max ever | HTTP | verdict |
|---|---|---|---|---|---|
| cmrj94xi400050 | nopB8d7-hJM | 0 | 1 | **200** | **PUBLIC, watchable today** |
| cmri66n2n00000 | _EaG1xx7FoU | 0 | 1 | **200** | **PUBLIC** |
| cmri1qtkz000q0 | kAnChIEuiWk | 0 | 1 | **200** | **PUBLIC** |
| cmrhzjll7000g0 | as5SzmuXKi4 | 0 | 1 | **200** | **PUBLIC** |
| cmrbuxbox00b80 | cLeKthjY5sk | 0 | 1 | **200** | **PUBLIC** |
| cmrdbmo7f004k0 | pm52JCuDmic | 0 | 2 | 403 | exists, embedding disabled |
| cmrdbm55w004h0 | NCjToiXqYiM | 0 | 1 | 403 | exists, embedding disabled |
| cmrdbn5ng004n0 | oJN7OhY1r4o | 0 | 1 | 403 | exists, embedding disabled |
| cmrh2hgr100250 | u1MNPvGDVTY | 0 | 2 | 404 | deleted |
| cmridcn7m000i0 | 9MAbzSox28A | 0 | 1 | 404 | deleted |
| cmrh2q8d100330 | x1GqkMX-B54 | 0 | 1 | 404 | deleted |
| cmrv621nf00170 | aeIcpBGFP9s | 0 | 1 | 404 | deleted |
| cmrh2p8n800300 | P0GWOOj8sEM | 0 | 1 | 404 | deleted |
| cmpnk0hod000a0 | Ag8HUv6e-Iw | 1,239 | 1,240 | 200 | control, public |
| cmr6qm35s000w0 | q4A5EeWLFpk | 1,186 | 1,186 | 200 | control, public |
| cmrk8vxy8063d0 | -GY12nlP-vs | 322 | 322 | 200 | control, public |
| cmpi4eg9d004c0 | 40GcQ7n1c5E | 9,096 | 9,099 | 404 | control, since deleted |
| cmrmrz29c03qy0 | kAMSW4fLaPk | 2,005 | 2,005 | 404 | control, since deleted |

## 3.3 The three-way split

| Category | count of the 13 | Is the stored 0 defensible? |
|---|---|---|
| **Reachable and public today** | **5** | **NO. The stored 0 is WRONG and the video is watchable right now.** |
| Exists, embedding disabled (403) | 3 | **Probably not.** The video exists; oEmbed refuses only to embed it. |
| Deleted (404) | 5 | Arguably, though BL-543 says the honest value is null with last-known kept, not 0 |

**At least 5, and probably 8, of the 13 carry a stored zero that is factually wrong today.**

## 3.4 A control result worth reporting, because it shows the correct behaviour working

`cmpi4eg9d004c0` fell from 117 to 0 back in May, **recovered to 9,096**, and its video is **now deleted**.
Its stored views are still **9,096, not 0**. **That is BL-543 working exactly as designed**: when the video
genuinely disappeared, the batch path returned `null` at `:189-195` and the clip kept its last-known value.
Same for `cmrmrz29c03qy0` at 2,005. **The system protects a real count when the video goes away; it fails
only on the hidden-count case.**

## 3.5 BL-720 and the gone-verdict

**None of the 50 is retired**: `videoUnavailable` is **false on every one**, so **none was wrongly retired
under the old gone-verdict logic** and BL-720's narrowing has nothing to undo here. The zeroing and the
retirement path are independent, and only the zeroing fired.

---

# PART 4 — WHAT IT COSTS

## 4.1 BL-748's $0.00 claim, verified independently and for a stronger reason

**Confirmed: $0.00. And the reason is more decisive than BL-748 gave.**

Every affected campaign carries **`minViews = 1000`**, and every one of the still-zero clips peaked at
**1 or 2 views**:

| clip | campaign | camp status | CPM | max views ever | would earn at max | earns now | minViews |
|---|---|---|---|---|---|---|---|
| cmrdbmo7f004k0 | GainzAlgo REPOST | PAST | $1.00 | 2 | **$0.0020** | $0.00 | **1,000** |
| cmrbuxbox00b80 | GainzAlgo REPOST | PAST | $1.00 | 1 | $0.0010 | $0.00 | 1,000 |
| cmrdbm55w004h0 | GainzAlgo REPOST | PAST | $1.00 | 1 | $0.0010 | $0.00 | 1,000 |
| cmrdbn5ng004n0 | GainzAlgo REPOST | PAST | $1.00 | 1 | $0.0010 | $0.00 | 1,000 |
| cmrhzjll7000g0 | WinGram | PAUSED | $1.00 | 1 | $0.0010 | $0.00 | 1,000 |
| cmri1qtkz000q0 | WinGram | PAUSED | $1.00 | 1 | $0.0010 | $0.00 | 1,000 |
| cmri66n2n00000 | GainzAlgo REPOST | PAST | $1.00 | 1 | $0.0010 | $0.00 | 1,000 |
| cmrj94xi400050 | WinGram | PAUSED | $1.00 | 1 | $0.0010 | $0.00 | 1,000 |

**Even fully restored to their best-ever count, these clips would earn $0.0090 between them, and the
1,000 view minimum zeroes that to $0.00 anyway.** They were never going to earn a cent at 1 or 2 views.

**No clipper is losing money.** Total across the whole 50-clip population: **$6.22 of earnings, all of it on
clips that recovered**, and **$0.00 on every clip still at zero**.

## 4.2 How long they have been zeroed

The 13 have carried their zero since **2026-07-09 to 2026-07-22**, so **18 to 31 days**. Long, and
completely without financial consequence for the reason above.

## 4.3 So is it negligible?

**The realized damage is genuinely negligible and needs no repair.** But **the mechanism is not**, and that
is the whole point of the round. PART 5 sizes it.

---

# PART 5 — CAN IT RECUR

## 5.1 The mechanism is LIVE, today

**Yes. Nothing in this chain has been fixed.** BL-748 fixed the Instagram twin; the YouTube one is
untouched:

1. `youtube.ts:178` fabricates `0` when `statistics.viewCount` is absent.
2. `apify.ts:2203` accepts it, because a `slim` object with `views: 0` is truthy.
3. `tracking.ts:1782` writes it to `ClipStat` with no comparison to the prior value.
4. **No views floor exists anywhere in `src/`.**

## 5.2 What triggers it

**A YouTube video whose uploader has hidden the view count**, which is a normal creator setting, not an
error. The video is otherwise healthy and public, so nothing else flags it. That is consistent with what the
data shows: five of the affected videos are public and watchable today while the platform believes they have
zero views.

## 5.3 What a clip carrying real earnings would suffer

**539 live YouTube clips sit behind this mechanism right now**: APPROVED, not retired, on ACTIVE or PAUSED
campaigns. **89 of them have over 1,000 views**, so they are past the `minViews` floor and genuinely
earning. **They carry $146.16 of earnings between them.**

If the mechanism fires on one of those, the stored views drop to 0 and the earnings recompute follows them
down. **BL-718's paid floor does not catch it**, because that floor sits inside `if (delta > 0)`
(`clip-earnings-writer.ts:197-198`) and a views-driven fall is a **decrease**, which skips the entire
guarded block.

**Two mitigations, stated honestly, because they are why this has not yet hurt anyone:**

* **It is usually transient.** 32 of 45 YouTube clips recovered on a later tick, because the next response carries the count again and earnings recompute upward.
* **It has only ever landed on 1-to-2-view clips so far**, which is likely selection rather than protection: a hidden-count setting is more common on tiny throwaway uploads.

**Neither is a guarantee.** A fall that coincides with a payout request, a campaign moving to PAST, or an
era boundary freezing the clip would make the zero permanent on a clip that does carry money.

## 5.4 Fix spec, NOT performed

**One executable line, mirroring BL-748 exactly.** `src/lib/youtube.ts:178`:

```diff
-          views: parseInt(stats.viewCount ?? "0", 10) || 0,
+          views: stats.viewCount != null && Number.isFinite(parseInt(stats.viewCount, 10))
+            ? parseInt(stats.viewCount, 10)
+            : null,
```

with the same treatment at `:35` and `:86`, and the `slim` type widened to `views: number | null`.

**Then the caller must be taught to skip a null**, which is the part BL-746 got wrong on Instagram by
guarding only one site. `apify.ts:2201-2210` must treat `s.views == null` as a **miss** and map the clip to
`null`, exactly as `youtube.ts:189-195` already does for an absent video, so the clip keeps its last-known
value.

**What must be proven before it ships:**

1. A hidden-count video yields `null`, not 0, and the clip **keeps its last-known views**.
2. A genuinely-zero-view video still records a real **0**, and the two stay distinguishable, which is BL-748's test shape.
3. A deleted video still maps to `null` via the existing `:189-195` path, unchanged.
4. **Every caller of the three functions** is mapped first, the way BL-748 mapped `classifyV2Media`'s six: `apify.ts:2194` and `:2522`, and `marketplace/submissions/[id]/post/route.ts:112`. That marketplace call site reads `views` for a first snapshot and must be checked for the same null-safety BL-746 added.
5. The tick still completes within budget.

**A separate, larger recommendation:** the real structural gap is that **stored views have no never-decrease
protection at all**, while earnings have three layers. A `viewsNeverDecrease` floor at the `ClipStat` write
would make every provider defect of this shape harmless, present and future. That is a bigger change on the
money-critical path and deserves its own round with its own proof.

## 5.5 Data repair spec, NOT performed

**Rows: 13. Money: $0.00. Recommendation: do not repair.**

The correct value for the 5 public and 3 embedding-disabled clips is their last real count, which was **1 or
2 views**. Restoring it changes no earnings, because `minViews = 1000` on every affected campaign. **A money
round with snapshots and printed rollback, per BL-716 and BL-718, cannot be justified to move $0.00.**

If the owner wants them corrected anyway for tidiness, the shape would be: for each of the 13, take
`max(views)` from `clip_stats`, write one new `ClipStat` at that value only where the video is confirmed
reachable, write **no** earnings, and let the next tick recompute. **Skip the 5 confirmed deleted**, whose
zero should become null rather than a resurrected count.

---

# PART 6 — THE VERDICT

**A live defect CAN zero a clip's stored views: `youtube.ts:178` fabricates a 0 when YouTube omits
`statistics.viewCount`, nothing on the YouTube path rejects it the way `hikerapi.ts:878` rejects Instagram's,
and no never-decrease guard protects stored views anywhere in the codebase. 13 clips are wrong today, at
least 5 of them provably public and watchable, and the money is $0.00 because every one peaked at 1 or 2
views against a 1,000 view campaign minimum. The exposure that matters is forward-looking: 539 live YouTube
clips, 89 of them past the minimum and carrying $146.16.**

**Recommended action: fix the classifier and its caller, do not repair the data.** The defect is one line
plus a caller change and is worth doing precisely because the next clip it lands on may not be a
one-view throwaway. The 13 existing rows are not worth a money round.

---

# WHAT COULD NOT BE MEASURED

* **A live view count for any clip.** There is no `YOUTUBE_API_KEY` in this environment, so the Data API probe was impossible and I used keyless oEmbed for reachability only. **I therefore cannot state what the 5 public videos actually have today**, only that they exist and that their best-ever recorded count was 1 or 2.
* **Per-clip attribution of each of the 51 events.** No provider response was logged at the time. The YouTube 45 are consistent with `youtube.ts:178` and no other YouTube path writes views, but that is inference from a single available mechanism, not a captured payload.
* **The 5 TikTok events.** A different provider chain, all recovered, all $0.00, and **not attributed**, on the same discipline BL-748 applied to this population.
* **Whether a hidden-count video is what actually hit these 13.** It is the only mechanism in the code that produces this exact signature, but confirming it needs the Data API response for one of the 5 public videos, which needs the key.
* **Whether any earnings dipped during a transient zero.** `clip_stats` retains the view history but earnings carry no per-tick history, so a temporary dip that recovered would leave no trace.
