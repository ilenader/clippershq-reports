# BL-1597: Spotify client leads, emails only — $1.16 per 1,000 now, about half the hours with one reorder, and the money is not where the waste is

## ANSWER CARD

**A) Current settings:** 1,000 new emails = **$1.16, 4.8 hours** (MEASURED, last full run, same settings as today)
  *Confidence high on $ (ledger rows, 4,003 emails); medium on hours (one run, and MusicBrainz speed varies by day).*

**B) Emails-only settings:** 1,000 new emails = **$1.15, about 2.1 hours** (DERIVED)
  *Confidence medium. Dollars barely move. Hours come from a model (57% fewer MusicBrainz lookups at 2.97 s each), not from a run.*

**C) Everything left in the current seeds:** about **14,000 emails** (range 4,000–31,000), **about $16**, **about 68 hours now / 30 hours emails-only** (DERIVED)
  *Confidence low. It rests on 120 search queries that have never run, priced from the 94 that have.*

**D) Is it working today:** **yes, the free half.** BL-1596's smoke test 5 days ago (2026-09-27) looked at 14 artists, kept 8, spent $0.
  *Confidence medium. The paid Instagram lookup (the step that finds the emails) was off in that test. That vendor last answered on 2026-09-18, in another round.*

**E) The one change:** check the artist's Instagram link, and our master, **before** the MusicBrainz country lookup.
  *Confidence high that it loses 0 emails (0 of 10,329 artists with no link ever gave one). It saves hours, not dollars. Emails per dollar is already flat: every paid group costs $1.08–$1.32 per 1,000.*

**Round:** BL-1597 · read-only · **$0.00, 0 vendor calls** · 87 protected files hashed at start and end, **0 moved** (master, spend.json, spotify_playlists_seen.json, resolve_cache.json, config.json, every Spotify checkpoint and run card, your workbooks) · no config change · MARK not opened · no address, handle or artist name in this report.

## 1. Is it alive?

The smoke test ran 5 days ago, inside your 7-day rule, so I cited it instead of re-running: `scratch/bl1596/p2_smoke.out`, BL-1596, 2026-09-27 09:26.
- Exit 0. 14 artists looked at, 8 kept, all 8 with monthly listeners, 7 with a country.
- $0.000000 in its temporary ledger, and the live files were byte-identical afterwards.
- One caveat: it looked at 14 artists, more than your limit of 10.

The last paid run ended at 11:00 on 2026-08-27 on an Instagram-vendor outage: 362 server errors (500 and 503) in one hour. The same vendor answered other rounds through 2026-09-18 (MEASURED, last `ig_usd` row in spend.json).

## 2. How it works

1. Read artists from playlists: 24 seeds, about 400 playlists found by free Spotify search per run, related-artist hops, and one day of ListenBrainz. **Free.**
2. Read each artist on Spotify: listeners, links. Keep 100k–5.1M listeners. **Free.**
3. Look up the country on MusicBrainz (only US/GB/CA/AU/IE/NZ kept), then check the song language. **Free; this is the slow step.**
4. Take the Instagram (or TikTok) link Spotify lists, and skip it if master already holds that handle. Try the artist's website or link page first. **Free.**
5. **The only step that costs money:** the paid Instagram lookup, $0.000613–$0.000705 each (ledger), then a free read of the bio link.

## 3. What it did before (all MEASURED)

**7,608 new unique emails for $9.4884** = **$1.25 per 1,000**.
- Each address is counted once. 224 rows share an address with another Spotify row (usually a manager), and 3 were already held by another funnel.
- Hours are recorded from 2026-08-01 on: **31.2 h for 6,739 emails = 4.6 h per 1,000**.

| where the email came from | new emails |
|---|---:|
| Instagram (paid lookup) | 7,283 |
| link-in-bio (free, read after the paid lookup) | 319 |
| website (free) | 2 |
| TikTok (paid lookup) | 4 |

ListenBrainz is a way of *finding* artists, not an email source. Artists it found gave **80** emails. By how the artist was found: related hops 4,179 · playlists 2,605 · not recorded (July rows) 744 · ListenBrainz 80.

| run day | new emails | $ (ledger) | hours |
|---|---:|---:|---:|
| Jul 22–31 | 869 | 0.6696 | not recorded |
| Aug 1 | 0 | 0.0006 | 0.36 |
| Aug 6 | 1,160 | 1.3212 | 2.56 |
| Aug 15 | 345 | 0.6936 | 1.59 |
| Aug 18 | 713 | 1.5570 | 2.26 |
| Aug 19 (six small test runs) | 6 | 0.0132 | 1.76 |
| Aug 24 | 513 | 0.6060 | 3.57 |
| **Aug 26–27 (today's settings)** | **4,002** | **4.6272** | **19.11** |
| **total** | **7,608** | **9.4884** | 31.22 |

## 4. Emails only: where the money goes (MEASURED unless marked)

This is over 12,507 paid lookups recorded in checkpoints, which cover $8.8128 of the $9.4884.

| question | answer |
|---|---|
| Paid lookups that returned no email | **5,201 of 12,507 = 41.58% [40.72–42.45]**, about **$3.66** (DERIVED: × $0.000705) |
| Paid, found an email, but not a new one | 561, about $0.40 |
| Paid for an artist with **no** link on Spotify | **0 of 12,507** |
| Paid when a free email was already found | **0 of 12,507**. The free routes run first, and found only 2 emails all-time |
| Same handle paid in two runs | 19 |

**Email rate by link** (qualified artists we did not already hold):
- Instagram link on Spotify: **57.84% [56.99–58.70] of 12,767**.
- **No link at all: 0 of 10,329 [0.00–0.04%]**. These cost $0 but still went through the slow country lookup.

**New-email rate per paid lookup.** It is flat across everything known before paying:

| group | new email rate (denominator = paid lookups) |
|---|---|
| 100–150k listeners | 54.47% [52.28–56.64] of 2,003 |
| 150–250k | 56.86% [54.93–58.77] of 2,557 |
| 250–500k | 54.68% [52.87–56.48] of 2,906 |
| 500k–1M | 54.45% [52.32–56.57] of 2,110 |
| 1–2.5M | 49.06% [46.69–51.43] of 1,704 |
| 2.5M+ | 46.54% [43.22–49.90] of 853 |
| country known (MusicBrainz) | 54.17% [52.90–55.44] of 5,933 |
| country unknown | 53.51% [52.26–54.76] of 6,126 |
| found by playlist / related hop / ListenBrainz | 53.32% of 4,901 / 54.35% of 7,455 / 52.98% of 151 |

**Seeds are where the yield differs.** Measured as new emails per artist looked at (the cost there is time):
- related hops: **11.83% [11.49–12.18] of 34,246**
- genre-search playlists: 8.01% of 20,402
- ListenBrainz: 7.37% of 1,086
- **9 of the 24 config seeds: 27 emails from 8,761 artists looked at = 0.31%**
  - These are `37i9dQZF1DWUFAJPVM3HTX`, `…DX4OR8pnFkwhR`, `…DWYUfsq4hxHWP`, `…DX9be6QR3XeJp`, `…DWYIJ3HxqIxIJ`, `7Ge1SJnlEQ08lgpAGS7xX2`, `…DWW4igXXl2Qkp`, `…DWT0upuUFtT7o` and `…DXcWL5K0oNHcG`.
  - In the last run's first hour, 2,821 artists were looked at for **1** email.

**PROPOSED "EMAILS-ONLY" SETTINGS** (I changed nothing):
1. **Code:** read the links and check master **before** MusicBrainz. No Instagram/TikTok link, or a handle already held → stop. 0 emails lost.
2. **Config, existing option:** turn on `spotify_skip_ids_file` with the **52,187** artist IDs already looked at. This loses 78 of 4,011 last-run emails (1.9%). It also covers the 9 dead seeds, whose old artists get skipped.
3. **Do not cut any paid group.** The worst (2.5M+) costs $1.32 per 1,000 at the margin and the best $1.08. Cutting it saves cents and costs emails, while supply is the limit.

**Projected (DERIVED, applied to the last run's work):**
- MusicBrainz lookups: 23,174 → **10,010**.
- Hours: 19.1 → **8.3**. The floor is 4.6 h, because Spotify reads are capped at 2 per second.
- Emails: 4,003 → 3,925.
- Dollars: $4.63 → $4.53.
- **= $1.15 and 2.1 h per 1,000.**

## 5. Speed: where the hours go

**The bottleneck is MusicBrainz.**
- Last run: **19.11 h for 23,174 lookups = 2.97 s of wall clock per lookup**. Earlier runs ran at 1.9–2.5 s per lookup.
- MusicBrainz handles one request at a time, paced at 1.1 s. Its own answers are slow: **9,698 lookups took over 5 s**, 117,405 s in total.
- Other slow steps, same log: Instagram 168 slow calls / 7,284 s (mostly the Aug 27 outage); link pages 824 / 6,550 s; Spotify reads 92 / 550 s.

**Time per step, estimated by regression** (DERIVED: worker-seconds in 111 ten-minute windows against the steps done in each):

| step | share of worker time |
|---|---:|
| MusicBrainz | **72%** (6.44 s per lookup) |
| Spotify reads | 15% (0.72 s per artist) |
| Instagram lookups | 7% (1.86 s each) |
| link pages | about 0% |

**What the MusicBrainz lookups were for** (last run, MEASURED):
- 32.6% went to paid lookups.
- **27.9% were artists with no link.**
- **17.2% were handles we already held.**
- 19.3% were dropped as wrong country, 2.2% as wrong language.

**Proposals, with no rate limit raised:**
1. The reorder above (−57% MusicBrainz).
2. The skip list (−10,333 Spotify reads, −24%).
3. Do **not** add workers. Going from 3 to 6 was measured at 1.02× faster.
4. **Your call:** dropping the country lookup entirely. Set `spotify_allowed_countries` to empty.
   - Country does **not** change the email rate (54.17% vs 53.51%). But the lookup is what drops wrong-country artists.
   - Dropping it means about 2,040 more paid lookups and about 1,080 extra emails from non-target countries per run like the last, about +$1.25 (DERIVED).
   - Hours would fall to the Spotify floor.
5. Fetching link pages in parallel is not worth building: they take about 0% of the time, and the free routes found 2 emails ever.

## 6. How many are left

**Supply used so far (MEASURED):**
- **1,995 playlists walked.**
- **94 of 214** search queries run. **120 have never run**: region 62, size 26, mood 18, decade 11, genre 3.
- **52,187** artists looked at.

**Duplicates across runs are not rising** (artists already looked at in an earlier run):

| run | duplicates |
|---|---|
| Aug 15 | 57.7% of 4,176 |
| Aug 18 | 45.4% of 6,224 |
| Aug 24 | 46.1% of 8,846 |
| **Aug 26** | **23.6% [23.24–24.04] of 43,717** |

- New artists per walked playlist stayed flat: 36.5 (Aug 6) → 40.1 (Aug 24) → 37.6 (Aug 26).
- The last run found **184–353 new emails every hour for 17 hours**. It stopped on the vendor outage, not on supply.
- Its $4.63 was also close to the **$5.00 per-run cap**, which stops a run near 4,300 emails.

**Supply leak (MEASURED):** the Aug 24 run met its target with **up to 8,822 of its 17,668 pooled artists never looked at**, and their playlists are now marked walked.

**Estimate (DERIVED)** = playlists left × new artists per playlist × overlap discount × new emails per new artist:
- Playlists left: 120 unused queries × 12–20 each, plus 500–900 found but unwalked.
- New artists per playlist: **34.0**, from the unused query groups.
- New emails per new artist: **0.079 direct to 0.277 with related hops**, from the Aug 26 run.
- **Result: about 14,000 (3,900–31,000).**

**The best new seeds** are the kinds that bring the most **new artists per playlist**: genre (48.1) and size (45.6), over region (28.5) and decade (30.6). The email rate per paid lookup is the same whatever found the artist, so choose seeds by fresh artists, not by email rate. Genre is nearly used up (47 of 50), so the next win is more genre-style queries plus the 26 unused size queries.

## 7. What I got wrong

- **I printed artist names and handles to my terminal three times.** None of them are in any file.
  - The first probe's shape mask left short name fragments in place.
  - A log scan showed Instagram vendor log lines that carry handles.
  - A run-card listing printed its free-text `stage` field.
- After that, every read went through scripts that print counts only.
- **I used a heredoc, which your brief bans.** While checking one leak-scan hit, I sent a malformed shell command that held an empty heredoc. It ran nothing, wrote nothing, and I stopped it. I redid the check through a script file.

## Paths

- **Scripts and outputs:** `scratch/bl1597/`: `analyze.py`/`.out`, `analyze2.py`/`.out`, `analyze3.py`/`.out`, `derived.py`/`.out`, `snap_start.json`, `snap_end.json`.
- **Claim:** `.claims/BL-1597.json`.
