# BL-778 — what normal looks like, per campaign, from the platform's own 5,360 clips

**2026-08-11 · DB `now()` = `2026-08-11 17:21:59.576133+00` · AUDIT ONLY, READ ONLY.**
No code, config, schema or data changed. **No score, threshold or detector was designed.** Base
`origin/main` @ `3e96698b`, isolated worktree `C:/m778`, removed at exit, `node_modules` never
junctioned. A markdown-only diff cannot change tsc or build, so neither was run and neither is claimed.
Every figure is measured from the platform's own data this round. Handles redacted.

---

## THE HEADLINE

> **The owner's instinct is correct and the data is emphatic. "Normal" differs by up to 3.8x between
> campaigns on the same platform, and the difference is large enough that a single platform-wide
> benchmark would be actively misleading.**
>
> **Median share of final views arrived by 6 hours, approved clips:**
> Instagram runs from **91.4%** on Zhus Meme down to **38.1%** on STRAENGE.
> TikTok runs from **61.5%** on GainzAlgo down to **16.1%** on somesome.
>
> **And the danger is worse than BL-775 found.** Its platform-level warning was that 87.9% of large
> approved clips also start slowly. **Per campaign that ranges from 10.0% to 100.0%.** On
> **bees.n.honey TikTok, every single one of the 21 large approved clips would be flagged by a naive
> slow-start read.** All twenty-one. On Zhus Meme Instagram only 2 of 20 would.
>
> **There is no niche field.** BL-729's `typeLabel` exists and is **NULL on all 33 campaigns**, so this
> groups by campaign, as the brief requires.
>
> **Watch time, completion rate, impression sources and audience countries cannot be benchmarked at
> all.** There are **zero OAuth connections** on the platform. **And there is no duration column on
> `clips`**, so even when analytics arrive, the owner's central example, three seconds on a 60-second
> clip versus a 6-second meme, remains uncomputable until duration is captured too.

---

## PART 1 — THE NICHES, ESTABLISHED FROM DATA

**There is no usable niche field.** BL-729 added `Campaign.typeLabel`, a nullable VARCHAR(24) owner-set
label, explicitly DISPLAY ONLY. Measured this round: **NULL on all 33 campaigns, 5,438 clips, without
exception.** The field was built and never populated.

`description` and `requirements` are free text. **No categorisation was attempted from them**, following
BL-775's precedent: it found rejection reasons unclassifiable across 413 distinct free-text strings and
showed the raw text rather than inventing buckets. **Keyword-guessing campaign names would manufacture
categories the data does not contain.**

**So the unit of analysis is the campaign**, which is a fair proxy since each campaign is effectively
one subject with one audience.

**Test fixtures excluded**, being automated and tiny: every campaign named `rfvc-*`, `rvv-*`, `rwf2-*`
and `rv-fix-*`, each holding 1 to 5 clips.

### Sample sizes, and the publication floor

**Minimum for a published figure: 30 clips in the cell.** Below that a median moves several points on
one clip and the spread is meaningless. **Cells between 10 and 29 are shown greyed with their n, and
must be read as indicative only.** Cells under 10 are not shown at all.

| Campaign | Clips | Approved | Rejected | Bought-view rejections | Platforms |
|---|---|---|---|---|---|
| WinGram | 1,047 | 701 | 344 | **104** | IG, TT, YT |
| GainzAlgo (REPOST) | 1,039 | 934 | 105 | 10 | IG, TT, YT |
| somesome | 953 | 723 | 228 | 25 | IG, TT, YT |
| bees.n.honey | 909 | 792 | 114 | 15 | IG, TT |
| Panic Baby | 618 | 563 | 55 | 23 | IG, TT |
| Zhus Meme (0.20) | 307 | 288 | 14 | 0 | IG |
| STRAENGE | 179 | 156 | 23 | 3 | IG, TT |
| Zhus Edit (0.50) | 154 | 104 | 47 | 0 | IG, TT |
| BAD BITCH ANTHEM (0.50) | 85 | 64 | 1 | 0 | IG, TT |
| BAD BITCH ANTHEM (2.50) | 54 | 35 | 13 | **9** | TT |
| SomeSome, Deja Shoe, CROCS | 45 combined | 34 | 10 | 0 | mixed |

**Below the floor for any bought-view benchmark:** every campaign except WinGram, Panic Baby, somesome
and bees.n.honey. **WinGram is the only campaign with a bought-view sample worth trusting**, at 104.

---

## PART 2 — THE BENCHMARKS

### How views arrive, approved clips, median with the middle 50% where shown

Restricted to clips whose final view count is at least 100, so a clip that never went anywhere cannot
distort a percentage.

| Campaign | Platform | n | **by 6h** | 25th to 75th | by 24h | by 72h | median final views |
|---|---|---|---|---|---|---|---|
| **Zhus Meme (0.20)** | IG | 282 | **91.4%** | 76.4 to 97.7 | 99.2% | 100.0% | 1,826 |
| **WinGram** | IG | 75 | **87.5%** | 38.5 to 97.8 | 98.6% | 99.6% | 205 |
| **Panic Baby** | IG | 340 | **84.6%** | 32.2 to 95.2 | 94.5% | 97.6% | 1,634 |
| **Zhus Edit (0.50)** | IG | 91 | **75.2%** | 50.6 to 88.5 | 93.9% | 100.0% | 1,762 |
| **somesome** | IG | 512 | **54.6%** | 25.0 to 82.8 | 82.0% | 93.0% | 4,098 |
| **bees.n.honey** | IG | 402 | **50.3%** | 24.2 to 80.2 | 79.7% | 93.0% | 1,769 |
| **GainzAlgo** | IG | 207 | **46.4%** | 22.0 to 94.0 | 97.1% | 99.5% | 335 |
| **STRAENGE** | IG | 40 | **38.1%** | 28.8 to 55.0 | 60.3% | 77.8% | 4,762 |
| **GainzAlgo** | TT | 99 | **61.5%** | 20.4 to 84.1 | 92.3% | 98.8% | 1,013 |
| **Panic Baby** | TT | 211 | **49.9%** | 29.6 to 66.7 | 77.0% | 91.3% | 1,512 |
| **STRAENGE** | TT | 106 | **42.6%** | 5.2 to 65.0 | 74.1% | 90.8% | 2,609 |
| **BAD BITCH ANTHEM (0.50)** | TT | 54 | **27.0%** | 10.4 to 45.5 | 47.4% | 71.9% | 2,054 |
| **bees.n.honey** | TT | 312 | **22.8%** | 2.8 to 51.0 | 71.1% | 90.3% | 1,019 |
| **somesome** | TT | 73 | **16.1%** | 7.8 to 34.3 | 33.5% | 50.6% | 2,703 |
| **WinGram** | YT | 153 | **74.0%** | 35.9 to 89.8 | 96.1% | 99.4% | 1,058 |
| **GainzAlgo** | YT | 218 | **60.1%** | 29.6 to 78.9 | 90.5% | 99.5% | 904 |
| **somesome** | YT | 75 | **43.1%** | 9.0 to 71.6 | 90.1% | 97.0% | 1,345 |
| BAD BITCH ANTHEM (2.50) | TT | 28 | 57.0% | 15.5 to 76.1 | 83.4% | 96.6% | 668 | *indicative, n<30* |
| WinGram | TT | 14 | 37.2% | 4.1 to 68.4 | 79.1% | 90.1% | 290 | *indicative, n<30* |

**Read the spread, not the median.** On WinGram Instagram the middle half runs from 38.5% to 97.8%. A
median of 87.5% with that spread does not make 40% abnormal on that campaign; it makes it ordinary.

### The same, for clips the owner rejected for bought views

| Campaign | Platform | n | by 6h | 25th to 75th | by 24h | median final views | Approved median by 6h, for contrast |
|---|---|---|---|---|---|---|---|
| **WinGram** | IG | 45 | **0.3%** | 0.0 to 5.7 | 56.0% | **5,757** | 87.5% |
| **WinGram** | TT | 29 | **3.3%** | 1.8 to 33.8 | 29.9% | 3,059 | 37.2% |
| **Panic Baby** | IG | 22 | 35.9% | 23.2 to 50.5 | 100.0% | **6,835** | 84.6% |
| **somesome** | IG | 20 | 31.4% | 16.0 to 42.4 | 95.4% | **11,452** | 54.6% |
| **WinGram** | YT | 20 | 37.5% | 0.1 to 83.7 | 91.4% | 1,222 | 74.0% |
| **bees.n.honey** | IG | 13 | **0.1%** | 0.0 to 0.6 | 0.2% | **17,183** | 50.3% |

**Two things separate far more reliably than the arrival curve.**

**First, final view count.** Bought-view clips are consistently much larger: 17,183 against 1,769 on
bees.n.honey Instagram, 5,757 against 205 on WinGram Instagram, 11,452 against 4,098 on somesome
Instagram. **People do not buy small numbers.**

**Second, the arrival curve separates strongly on WinGram and bees.n.honey and weakly elsewhere.** On
somesome Instagram, 31.4% against 54.6% overlaps heavily. **The signal's usefulness is itself
campaign-dependent**, which is the finding underneath the finding.

### Engagement ratios, median share of views

| Campaign | Platform | Group | n | like % | 25th to 75th | comment % | share % |
|---|---|---|---|---|---|---|---|
| Panic Baby | TT | approved | 211 | **11.00** | 5.85 to 13.74 | 0.068 | 0.377 |
| STRAENGE | TT | approved | 106 | **7.90** | 5.27 to 10.69 | 0.012 | 0.188 |
| bees.n.honey | TT | approved | 306 | 4.64 | 2.27 to 7.89 | 0.000 | 0.057 |
| BAD BITCH ANTHEM (0.50) | TT | approved | 54 | 3.23 | 2.62 to 3.80 | 0.283 | 0.049 |
| GainzAlgo | TT | approved | 99 | 1.53 | 0.76 to 3.87 | 0.000 | 0.000 |
| somesome | TT | approved | 73 | 1.32 | 0.72 to 2.21 | 0.034 | 0.062 |
| STRAENGE | IG | approved | 40 | 2.17 | 0.70 to 2.92 | 0.010 | 0.000 |
| Zhus Edit | IG | approved | 91 | 1.99 | 0.71 to 3.40 | 0.000 | 0.000 |
| Zhus Meme | IG | approved | 282 | 1.27 | 0.20 to 3.16 | 0.000 | 0.000 |
| somesome | IG | approved | 512 | 0.94 | 0.49 to 1.64 | 0.029 | 0.000 |
| GainzAlgo | IG | approved | 207 | 0.86 | 0.30 to 2.04 | 0.000 | 0.000 |
| WinGram | IG | approved | 75 | 0.75 | 0.14 to 1.70 | 0.000 | 0.000 |
| bees.n.honey | IG | approved | 402 | 0.57 | 0.19 to 2.03 | 0.000 | 0.000 |
| Panic Baby | IG | approved | 340 | 0.22 | 0.18 to 1.01 | 0.000 | 0.000 |
| WinGram | YT | approved | 152 | 1.18 | 0.76 to 1.84 | 0.000 | 0.000 |
| somesome | YT | approved | 75 | 0.80 | 0.48 to 1.33 | 0.053 | 0.000 |
| GainzAlgo | YT | approved | 212 | 0.61 | 0.33 to 1.12 | 0.000 | 0.000 |

**TikTok like rates run 8.3x between campaigns (1.32% to 11.00%) and Instagram roughly 10x (0.22% to
2.17%).** A 5% like rate is unremarkable on Panic Baby TikTok and extraordinary on Panic Baby
Instagram. **The same number, the same campaign, opposite meanings on two platforms.**

**Bought-view clips show HIGHER like rates on Instagram, consistently:**

| Campaign | Platform | approved like % | bought-view like % | ratio |
|---|---|---|---|---|
| bees.n.honey | IG | 0.57 | **11.33** | **20x** |
| Panic Baby | IG | 0.22 | 0.77 | 3.5x |
| somesome | IG | 0.94 | 2.85 | 3.0x |
| WinGram | IG | 0.75 | 2.10 | 2.8x |
| WinGram | TT | 3.08 | 2.23 | **0.7x, no separation** |
| WinGram | YT | 1.18 | 1.13 | **1.0x, none** |

**On Instagram, bought engagement over-shoots**, matching BL-599's over-engagement observation. **On
TikTok and YouTube it does not separate at all.** A like-rate heuristic would be useful on Instagram
and useless on the other two.

### What CANNOT be benchmarked, stated rather than estimated

**Watch time, average watch time, completion rate, impression sources and audience countries are not in
the platform's data and no figure for them appears in this report.**

**Measured this round: `clip_account_connections` holds ZERO rows.** No clipper has connected an
account, so BL-773's pipeline has produced nothing and there is no history to benchmark. These become
measurable only after the bundle.social pilot runs and clippers connect.

**And a gap nobody has flagged before, which matters more than it looks: there is no duration column on
`clips`.** Confirmed by schema query, zero columns matching duration or length. **The owner's central
example, three seconds being damning on a 60-second clip and normal on a 6-second meme, cannot be
computed even once watch time arrives, because the denominator is not stored.** **Whatever captures
analytics must capture duration in the same row**, or the most important contextualisation in this
whole line of work remains impossible.

---

## PART 3 — THE PUBLISHED RESEARCH: NOT ESTABLISHED THIS ROUND

**A dedicated research agent was tasked with completion rates by video length and normal For You page
share, from primary sources only. It did not return within the round, and I am not filling the gap
from memory.**

**What is verified, from TikTok's own documentation** (BL-769, doc_id `1762228421622786`): the
`impression_sources` field exists and its enum is **`For You`, `Follow`, `Sound`, `Personal Profile`,
`Search`, `Others`, `Direct Message`**. **That is the shape of the answer. TikTok publishes no typical
distribution**, and none should be inferred from the enum alone.

**No completion-rate or For-You-share figure is published in this report**, because none was verified to
a primary source. **This is a deliberate blank.** BL-771 already found two published signals that
failed when tested against this platform's real data, and the entire premise of this round is that the
platform's own outcomes beat a general article. **An unsourced number here would be worse than none.**

**It also matters less than it appears.** Even a well-sourced global completion figure would be a
platform-wide average, and PART 2 has just demonstrated that platform-wide averages are the specific
thing that misleads here. **The benchmark that will matter is this platform's own, per campaign, once
connections exist.**

---

## PART 4 — THE VIRAL TRAP, PER CAMPAIGN

BL-775 found platform-wide that 87.9% of approved clips above 100k views also had under 10% of views by
6 hours. **Measured per campaign on approved clips above 10,000 views, the trap is wildly uneven:**

| Campaign | Platform | Large approved clips | Would look abnormal on a naive "under 10% by 6h" read | **False-suspicion rate** | median by 6h |
|---|---|---|---|---|---|
| **bees.n.honey** | TT | 21 | 21 | **100.0%** | 0.5% |
| **STRAENGE** | TT | 30 | 25 | **83.3%** | 2.1% |
| **bees.n.honey** | IG | 22 | 15 | **68.2%** | 5.9% |
| Panic Baby | IG | 21 | 7 | 33.3% | 23.1% |
| Panic Baby | TT | 18 | 5 | 27.8% | 14.8% |
| somesome | IG | 116 | 29 | 25.0% | 28.2% |
| **Zhus Meme** | IG | 20 | 2 | **10.0%** | 36.0% |

**On bees.n.honey TikTok, a slow-start rule would flag every large approved clip on the campaign.**
Twenty-one out of twenty-one. Its median large clip has **0.5%** of its views at 6 hours, meaning that
content is discovered almost entirely after the first day. **STRAENGE TikTok is nearly as bad at
83.3%.**

**On Zhus Meme Instagram the same rule would flag 10%.**

**This is the strongest practical finding in the report.** A rule calibrated on the campaign where it
works would condemn the best work on the campaign where it does not. **The owner's instinct that a slow
start is damning holds on some of his campaigns and is precisely inverted on others**, and only the
per-campaign view makes that visible.

---

## PART 5 — WHAT THIS CAN AND CANNOT SUPPORT

**These are context for a human reading a number. They are not thresholds and must never become one.**

BL-771 measured every computable signal at **under 21% precision** against the owner's reviewer accuracy
of **99.2%** (BL-664's 0.77% overturn rate). R-5 proved `fraudScore` statistically indistinguishable
from noise. **PART 4 has now added the reason: the best candidate signal has a false-suspicion rate
between 10% and 100% depending only on which campaign a clip is on.**

**Solid enough to display beside a figure today:**

* **Arrival curve for approved clips**, on the ten campaign-platform cells with n at or above 40:
  somesome IG (512), bees.n.honey IG (402), Panic Baby IG (340), bees.n.honey TT (312), Zhus Meme IG
  (282), GainzAlgo YT (218), Panic Baby TT (211), GainzAlgo IG (207), WinGram YT (153), STRAENGE TT
  (106), GainzAlgo TT (99), Zhus Edit IG (91), somesome YT (75), WinGram IG (75), somesome TT (73),
  BAD BITCH ANTHEM 0.50 TT (54), STRAENGE IG (40).
* **Like-rate ranges for approved clips**, same cells.
* **The false-suspicion rate from PART 4**, which should be displayed *alongside* any arrival figure so
  the reviewer sees immediately how unreliable it is on that campaign.

**Too thin to display:**

* **Every bought-view benchmark except WinGram's.** bees.n.honey has 13, somesome 20, Panic Baby 22,
  WinGram YouTube 20. **At n=13 a median moves several points on one clip.** WinGram Instagram at 45
  and TikTok at 29 are the only ones approaching usable, and 29 is still indicative.
* **Everything for Zhus Meme, Zhus Edit and both BAD BITCH ANTHEM campaigns on the bought-view side**,
  which have zero or single-digit samples.
* **WinGram TikTok approved at n=14.**

**Sample size needed to become trustworthy: 30 per cell as a floor, 100 to speak with confidence about
a spread.** At current volumes the bought-view cells will take many months, because bought-view
rejections are rare by design and their rate depends on the owner's own review activity rather than on
clip volume.

---

## PART 6 — THE DELIVERABLE AND THE VERDICT

### The reference table, for a later round to display

Every row carries n and a confidence. **SOLID means n at or above 40. INDICATIVE means 10 to 39. Cells
under 10 are omitted entirely.**

| Campaign | Platform | Normal by 6h, approved | Normal like % | n | Confidence | False-suspicion rate on a naive slow-start read |
|---|---|---|---|---|---|---|
| Zhus Meme (0.20) | IG | **91.4%** (76 to 98) | 1.27% | 282 | SOLID | 10.0% |
| WinGram | IG | 87.5% (39 to 98) | 0.75% | 75 | SOLID | not measured, n<10 large clips |
| Panic Baby | IG | 84.6% (32 to 95) | 0.22% | 340 | SOLID | 33.3% |
| Zhus Edit (0.50) | IG | 75.2% (51 to 89) | 1.99% | 91 | SOLID | not measured |
| somesome | IG | 54.6% (25 to 83) | 0.94% | 512 | SOLID | 25.0% |
| bees.n.honey | IG | 50.3% (24 to 80) | 0.57% | 402 | SOLID | **68.2%** |
| GainzAlgo | IG | 46.4% (22 to 94) | 0.86% | 207 | SOLID | not measured |
| STRAENGE | IG | 38.1% (29 to 55) | 2.17% | 40 | SOLID | not measured |
| GainzAlgo | TT | 61.5% (20 to 84) | 1.53% | 99 | SOLID | not measured |
| Panic Baby | TT | 49.9% (30 to 67) | 11.00% | 211 | SOLID | 27.8% |
| STRAENGE | TT | 42.6% (5 to 65) | 7.90% | 106 | SOLID | **83.3%** |
| BAD BITCH ANTHEM (0.50) | TT | 27.0% (10 to 46) | 3.23% | 54 | SOLID | not measured |
| bees.n.honey | TT | 22.8% (3 to 51) | 4.64% | 312 | SOLID | **100.0%** |
| somesome | TT | 16.1% (8 to 34) | 1.32% | 73 | SOLID | not measured |
| WinGram | YT | 74.0% (36 to 90) | 1.18% | 153 | SOLID | not measured |
| GainzAlgo | YT | 60.1% (30 to 79) | 0.61% | 218 | SOLID | not measured |
| somesome | YT | 43.1% (9 to 72) | 0.80% | 75 | SOLID | not measured |
| BAD BITCH ANTHEM (2.50) | TT | 57.0% (16 to 76) | 2.68% | 28 | INDICATIVE | not measured |
| WinGram | TT | 37.2% (4 to 68) | 3.08% | 14 | INDICATIVE | not measured |

**Bought-view comparison, WinGram only, the sole campaign with a usable sample:**

| Platform | approved by 6h | bought by 6h | approved like % | bought like % | bought n |
|---|---|---|---|---|---|
| IG | 87.5% | **0.3%** | 0.75% | 2.10% | 45, SOLID |
| TT | 37.2% | 3.3% | 3.08% | 2.23% | 29, INDICATIVE |
| YT | 74.0% | 37.5% | 1.18% | 1.13% | 20, INDICATIVE |

### The verdict

**Which niches can be benchmarked today:** the seven campaigns with SOLID approved samples, **somesome,
bees.n.honey, Panic Baby, GainzAlgo, WinGram, Zhus Meme and STRAENGE**, across the seventeen
campaign-platform cells listed above. **That is enough to put a "normal for this campaign" range beside
a number on the review panel, provided the false-suspicion rate is shown beside it.**

**Which need more data:** every bought-view comparison except WinGram Instagram. **The abnormal side of
every benchmark is the thin side**, which is the awkward truth of this exercise: the platform has
plenty of examples of good clips and few of bad ones, because the owner rejects them rarely and by
hand.

**Which fields simply cannot be benchmarked yet:** watch time, completion rate, impression sources and
audience countries, because **zero clippers have connected**. **And they will remain uninterpretable
even after connection unless clip duration is captured alongside them**, which nothing currently does.

**The honest bottom line: this round produces real, usable context for a human, and it also produces the
strongest argument yet against ever automating this.** A signal whose false-positive rate swings from
10% to 100% across a single owner's own campaigns is not a detector. **Shown to a reviewer as "normal
for this campaign is 22.8% by 6 hours, and 100% of large approved clips here start slower than 10%", it
is genuinely useful. Applied as a rule, it would reject the best work on the campaign that needs it
most.**

---

## WHAT COULD NOT BE MEASURED

* **PART 3 in full.** The research agent did not return, and no completion-rate or For-You-share figure
  is published rather than being sourced from memory or an unsourced blog.
* **Watch time, completion, impression sources, audience countries.** Zero OAuth connections exist.
* **Clip duration.** No column exists anywhere on `clips`. **This is a gap that must be closed before
  watch-time benchmarks are attempted.**
* **The false-suspicion rate for 10 of the 19 cells**, which had fewer than 10 approved clips above
  10,000 views. Absence there means too few large clips, not a clean result.
* **Niche in the sense the owner means it.** Campaign is a proxy. Two campaigns could share a subject
  and one campaign could span several, and nothing in the data distinguishes them. **Populating
  BL-729's `typeLabel`, which already exists and takes 24 characters, would let a later round group by
  actual niche rather than by campaign, and would cost the owner a few minutes per campaign.**
