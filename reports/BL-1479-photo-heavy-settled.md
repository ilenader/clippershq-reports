# BL-1479 — photo_heavy settled: it is a 10% photo cut, it is live and free, and it kills none of his best pages

> ## IS THE FUNNEL SAFE TO RUN? — **NO**, and not for any reason to do with this rule.
>
> `photo_heavy` itself comes out of this round **clean**: measured on his own marks it kills
> **0 of his 11 pages scored 8-10, at every threshold tested**. The reason the funnel is not
> safe to run is separate and larger, and another round measured it while this one ran:
> **51.9% of pages in the Instagram store have no grid image, and a page with no image never
> reaches the model judge at all.** On those pages the free rules — this one included — are the
> only thing judging, with nothing able to disagree.
>
> **Nothing in this round changed a judging rule.** No production file was written, because the
> setting it was asked to ship **already exists and was proved to work**.

> ## WHAT THIS DOCUMENT COULD NOT CONFIRM
>
> - **The "97.5% precision" figure that three production files quote does not record which posts
>   endpoint produced it**, and it is unrecoverable. Two figures from the same day, same marks and
>   same rule differ by everything (85.0% against 0 of 192) purely on that variable.
> - **One recent run reports the rule firing AND a second-fetch counter that should be
>   impossible together.** That single run's endpoint is **UNRESOLVED**; nothing here depends on
>   it.
> - **Every line number here is a working-tree read at commit `ab060d0`.** Two peer rounds
>   committed to these files during the audit; every anchor was re-derived by text afterwards,
>   and they will move again.
> - **The TikTok facts block was reconstructed from source, not spied on a live run.** The
>   *mechanism* of the 360-to-5 defect is proved by a driven control; the specific fallback value
>   is a reconstruction.
> - **`aweme_type` evidence is a convenience sample clustered by author**, so its rate is not a
>   population estimate.

---

## 1. WHAT THIS ROUND WAS ASKED TO DO

**Round BL-1479 · 2026-09-01 · read-mostly · vendor spend $0.00, zero vendor calls.**

The operator said this, and it is clearer than anything in the code:

> *"If the profile has like 70% photos, I don't want it. If it at least has 30-40% videos,
> that's okay with me. But I don't understand the photo_heavy argument."*

The round was asked to find out what the rule actually does, settle whether it really kills
28.6% of the pages he wants, score his stated 70% rule against the shipped one on his own marks,
and ship the threshold as a setting defaulted to today's behaviour.

**The short answers:**

1. **It is a genuine photo-share threshold — set at 10%, not 70%.**
2. **It is live, and on today's configuration it costs nothing extra.**
3. **It kills none of his best pages.** The 28.6% figure is real but was measured against
   approvals he has since withdrawn.
4. **The setting already exists**, so nothing was shipped.

---

## 2. WHAT SHIPPED

**Nothing. Deliberately, and that is the finding.**

The round was told to make the threshold configurable and default it to current behaviour.
**It already is configurable, and the existing implementation is better than a new one would
be.** Shipping a second setting beside it would have duplicated a working one — which is this
project's most-repeated mistake in a new costume.

**How that was proved — a runtime spy driven from his real configuration, not a reading:**

```
PROOF 1  THE CHAIN, BY AST
  config.json -> config["meme_finder"]           meme_finder.py:4990
              -> max_photo_share                 meme_finder.py:5176  (explicit `in` test)
              -> judge_page(max_photo_share=)    meme_finder.py:6956  (the ONLY call site)
              -> the rule                        meme_finder.py:2548
  call sites passing the threshold: 1     UNBROKEN SINGLE PATH: True

PROOF 2  DOES HIS REAL CONFIG SELECT?
  his real config       -> 0.1
  CONTROL A  set 0.70   -> 0.7    CHANGED: True
  CONTROL B  key absent -> 0.1    (falls to the CODE default, not to his value)
  CONTROL C  value 0    -> 0.0    (an `or` chain would have silently given 0.1)
  CONTROL C  value None -> None   (means: rule OFF, reachable without a code change)
  campaigns defined: 5 ; overriding this key: NONE

PROOF 3  THE RULE HONOURS THE VALUE   (driven on post lists of known composition)
  a 10% photo page dies at a 0.10 cut and survives every higher cut; a 70% photo page
  dies at 0.10 through 0.70 and survives 0.80. Abstention holds: with fewer than
  MIN_VIDEO_JUDGED = 3 typed posts the share is None and the rule does not fire.
```

**Control B and C matter more than Control A.** The newest failure class in this project is a
correct fix on a branch the configuration never takes — a garbage-cutting switch is `true` at
the top level, four campaigns override it `false`, the fifth omits it, and an omitted value
falls through to a code default of `false`, so his `true` selects nothing anywhere. **This key
does not have that defect:** no campaign overrides it, and the explicit `in` test expresses `0`
and `None`, which an `or` chain cannot. The comment at `:5176` records that as deliberate.

**So the honest deliverable is: the lever he wants already exists, it is one number in one
file, and this report tells him what each value costs.**

---

## 3. WHAT WAS MEASURED

### 3.1 What the rule actually is — MEASURED by reading and driving it

At `meme_finder.py:2548`:

```
photo_heavy =  (max_photo_share is not None and pho_share is not None
                and pho_share >= max_photo_share)
            or (min_video_share is not None and vid_share is not None
                and vid_share < min_video_share)
```

| property | value | where |
|---|---|---|
| what it measures | share of a page's recent posts that are photos | `:2548` |
| the sample | the same post slice every other share uses; **albums count by their CHILDREN**, so a 12-still carousel weighs twelve, not one | `:2541` |
| threshold, photo arm | **0.10** — ten per cent | `config.json` `meme_finder.max_photo_share` |
| threshold, video arm | 0.70 | `meme_finder.min_video_share` |
| missing value | **abstains.** Below 3 typed posts the share is `None` and the rule cannot fire | `MIN_VIDEO_JUDGED = 3`, `:1463` |

**ANSWERING HIS ACTUAL QUESTION.** Yes — it is a photo-share threshold, exactly the kind of
rule he described. **It is set seven times stricter than the number he gave.** He said 70%; it
cuts at 10%.

**That is very likely the whole reason the argument does not make sense to him.** A page that
is one-tenth photos is not "photo heavy" by any ordinary reading of those words — he would call
it a video page. The rule's name describes his rule; the rule's threshold does not.

**⚠️ AND HIS CONFIGURATION RECORDS HIM CHOOSING THE 10%.** The note stored beside the value
says he was shown that it catches 35 of 70 rejections (50.0% recall) and **kills 7 of his 28
wanted pages (25.0%)**, that he shipped it anyway, that he called three of his own approvals
"HIS MISTAKE", and it instructs: *"do not soften this."*

**So two recorded statements of his conflict, seven-fold apart.** The standing rule is that his
latest word wins — but this is his call, not this round's, and section 7 gives him the price of
each choice rather than making it for him.

### 3.2 THE THRESHOLD SWEEP — MEASURED, n=95, cut declared

**Denominator:** 95 pages that carry **both** a hand mark from his 22 August sheet **and** a
real photo share measured through the photo-capable endpoint. Of 99 marked pages, 95 were
computable and **4 abstained** (three where the call failed and one with 2 typed posts).

**The cut is stated, because a figure whose threshold is not stated is not a figure.** Scored on
want / not-want at **≥6**, and repeated at ≥7. Never on his 1-to-10 score, which he reproduces
only 18.5% of the time against 77.2% [69.8, 83.2] for his decision.

| cut T | kills | catches his 1-3s | **KILLS his 8-10s** | kills wants ≥6 | precision | recall |
|---|---|---|---|---|---|---|
| **0.10 shipped** | 41/95 = 43.2% | 37/67 = 55.2% | **0 of 11 — upper bound 25.9%** | 1/19 = 5.3% [0.9, 24.6] | 40/41 = 97.6% | 40/76 = 52.6% |
| 0.50 | 27/95 = 28.4% | 25/67 = 37.3% | **0 of 11** | 0/19 = 0.0% [0, 16.8] | 27/27 = 100% | 27/76 = 35.5% |
| 0.60 | 20/95 = 21.1% | 19/67 = 28.4% | **0 of 11** | 0/19 | 20/20 = 100% | 20/76 = 26.3% |
| **0.70 his stated** | 14/95 = 14.7% | 14/67 = 20.9% | **0 of 11** | 0/19 | 14/14 = 100% | 14/76 = 18.4% |
| 0.80 | 12/95 = 12.6% | 12/67 = 17.9% | **0 of 11** | 0/19 | 12/12 = 100% | 12/76 = 15.8% |
| 0.90 | 6/95 = 6.3% | 6/67 = 9.0% | **0 of 11** | 0/19 | 6/6 = 100% | 6/76 = 7.9% |

At the stricter ≥7 cut the rule kills **0 of 14** of his wants at **every** threshold.

**⚠️ WHY THE THRESHOLD BARELY MATTERS, AND THIS IS THE HEADLINE.** All 11 of his pages scored
8-10 are **0.000 photo / 1.000 video**, over 12 counted children each. **There is nothing on his
best pages for a photo rule to hit at any threshold.** The single casualty at 0.10 is one page
at 16.7% photos that he scored 6.

### 3.3 THREE ARMS ON THE SAME 95 PAGES — MEASURED

| arm | kills | catches lows | kills his 8-10s | kills wants ≥6 | precision |
|---|---|---|---|---|---|
| today, 0.10 | 41 | 37 of 67 | **0 of 11** | 1 of 19 | 40/41 |
| his stated, 0.70 | 14 | 14 of 67 | **0 of 11** | 0 of 19 | 14/14 |
| no rule at all | 0 | 0 of 67 | 0 | 0 | — |

**The legacy video arm is not his rule.** At 0.10 it is subsumed entirely; at 0.70 it
contributes 10 of the 24 kills. Anyone moving the photo cut should know the video arm keeps
firing on its own terms.

### 3.4 THE BASELINE, WITH ITS SCOPE NAMED — MEASURED

**Always-reject scores 80.0% [70.9, 86.8] at ≥6** and 85.3% [76.8, 91.0] at ≥7, **on this pool:
the 95 pages carrying both a hand mark and a real mixed-endpoint share — a delivered-sheet pool,
not a sample of Instagram.**

**It beats every arm above on raw accuracy, and that is expected, not damning:** any reject-only
rule on an 80%-reject pool loses to "reject everything" on accuracy. Accuracy is the wrong
scoreboard here; the right ones are the two columns that matter to him — what it catches, and
what it destroys.

### 3.5 PRECISION PER ENDPOINT, NEVER POOLED — and the numbers everyone quotes are two different things

**⚠️ THE MOST-QUOTED FIGURES IN THIS RULE'S HISTORY ARE NOT PRECISIONS.** The widely-cited
"97.4% versus 30.0%, disjoint intervals" comes from a row explicitly labelled **`photo_heavy`
fires** — they are **FIRE RATES** on two hashtag surfaces (38/39 and 12/40), not precisions. The
"97.5% precision" that sits in the same table cell is a **different quantity** that got welded
onto it in quotation. **This document's own author repeated that error in a published report the
day before and is correcting it here.**

The real precision measurements, each with the endpoint that produced it:

| precision | k/n | posts endpoint | note |
|---|---|---|---|
| 85.0% | 17/20 | `/v2/user/medias` — photo-capable, second fetch ON | describes an older configuration |
| 97.0% [84.7, 99.5] | 32/33 | mixed, ≥4 filter versions | |
| **97.5% [87.1, 99.6]** | **39/40** | **NOT STATED — unrecoverable** | **the number three production files quote** |
| 97.6% [87.4, 99.6] | 40/41 | stored corpus, $0.00 | |
| **0 of 192 — "dead by endpoint"** | 0/192 | `/v2/user/clips` — reels only | the rule could not fire |

**The confound that matters is the POSTS endpoint, not the discovery surface.** Figures 1 and 5
are the same round, the same day and the same marks, differing **only** by which endpoint
supplied the posts: 85.0% on the photo-capable one, **0 of 192** on the reels one. **That
confound makes a rule vanish rather than merely mis-fire, which is far harder to notice.**

On this round's own 95 pages the per-endpoint split is: 31 suggested, 27 seed, 11 known-repost,
2 hashtag, 1 crawl, **23 unknown (24.2%)**. Precision runs 87.5–100% across buckets, the largest
holds 10 kills, **nothing separates, and the pool cannot detect a surface gap.** Reported rather
than pooled.

### 3.6 IS THE RULE LIVE TODAY? — MEASURED, and the answer reversed twice

His configuration sets `photos_endpoint` to the **empty string**, and one docstring says that
turns the second fetch off and makes the gate dead. **A different comment says the opposite**,
and the comment is right:

> *"`photos_endpoint` empty used to mean ONE thing — no second fetch, so nothing can see photos
> and the rule is dead. After the gql merge it means the OPPOSITE: the primary posts call
> already returns photos, so the rule works AND costs nothing extra."*

**Settled from a probe that was already on disk and had never been read back** — no vendor call
was needed, and a prior round had recorded this as unresolved pending a live call:

```
  v2_clips  (the old reels catalogue)   media_types {2: 12}           ALL VIDEO
  v2_medias (the old second fetch)      media_types {1:8, 8:2, 2:2}   photos + albums
  gql_flat  (WHAT SHIPS TODAY)          media_types {1:8, 8:2, 2:2}   photos + albums
```

Two high-volume public accounts, 12 items each, `carousel_media` present on the albums. The
client sets the flattening flag from the path, so the merged route returns the same mix the
dedicated photo endpoint did.

**CONCLUSION: `photo_heavy` is LIVE, and on today's configuration it costs no extra request.**

**AND IT HAS NOW BEEN OBSERVED END TO END.** An earlier draft of this report called that the
honest residual. It is no longer, on four independent grounds:

1. **One run kept a log, and the log says so in its own words.** A run of 2026-08-28 emitted, at
   start-up and computed from the live value: *"media mix read from the PRIMARY posts call
   (/gql/user/medias) — merged, so NO second request; empty `photos_endpoint` means MERGED, not
   disabled."* **That same run's resume file records a firing** — photo share 0.4167 over 12
   items, reason *"42% … the cut is 10%"*. **No second-fetch line appears anywhere in that log.**
2. **27 dated configuration snapshots.** 20 of them, spanning 2026-08-25 to 08-31, show
   `photos_endpoint` empty **and** the merged primary endpoint together — and firings continue
   right through that window (8, 25, 180, 354, 15 on successive days).
3. **The distribution is impossible under the old reading.** Across 1,079 recorded firings the
   photo share ranges 0.10 to 1.00 with **zero rows at 0.0** — which could not happen if the mix
   were the all-video reels catalogue.
4. The live configuration has not been modified since 2026-08-30.

**One contradiction flagged and NOT resolved:** the most recent run reports `photo_heavy: 15`
**and** a second-fetch success counter of 31, whose only increment site is guarded by the
endpoint being non-empty. That could not be explained without running the funnel. **That single
run's endpoint is UNRESOLVED; nothing above depends on it.**

### 3.7 THE 588-versus-439 DISCREPANCY — **RESOLVED, and not the way anyone expected**

**It is not per-run versus cumulative.** That was the standing hypothesis, including in this
round's own brief, and it is wrong.

**Both figures are cumulative. They come from different files covering disjoint time windows:**

```
  a walk file                ends   2026-08-23     439 of 2,042 rows, 12 named runs
  the rejection log          starts 2026-08-24     611 of 2,935 rows
```

**They are additive, not competing.** The resemblance that made them look like rivals is a
coincidence: the true **per-run maximum is 429**, which is 97.7% of 439.

**And "588" was never wrong — it was earlier.** Reading the same live file today gives **611**,
exactly 23 appended rows later. **Any count taken from that file is a timestamp, not a
constant**, and quoting one without its read-time is how two correct measurements become an
apparent contradiction.

**⚠️ AND A SEPARATE DEFECT FELL OUT OF IT: A TEST HARNESS IS WRITING INTO THE PRODUCTION
REJECTION LOG.** The "four firings on 2026-08-31" that this round was sent to investigate are
**synthetic**. They are two fabricated handles walked twice, and the reason string states its own
threshold: **"the cut is 0%"** — not 10%. At a zero cut the rule fires on everything, which is
why those rows carry a photo share of 0.0 and satisfy neither shipped arm. The same fabricated
handles fire the view floor against a 1,000,000 threshold and the staleness rule against a
one-day cut in the same twelve minutes, and neither handle appears in either resume file covering
that window. **Something is appending probe traffic to the file that records real rejections**,
and anyone counting rule firings from it is counting test fixtures as production events. The
genuine recent firings are 23 rows from 08-31 to 09-01, all real pages, 10 of 23 on the photo arm
alone.

**⚠️ WHAT WAS PROVED, AND WHAT WAS NOT.** Proved: the rows are fabricated handles, at thresholds
no shipped configuration holds, absent from the run records for their own window. **Not proved:
which script wrote them.** The obvious reading is a rule-reachability harness, and that is an
inference about purpose, not an observation — **the writer was never identified.** A tree-wide
trace for it timed out on a 5.58 GB directory and was abandoned rather than guessed at.

### 3.8 WHICH ARM FIRES — MEASURED, and the video arm is effectively dead

| source | photo arm only | both arms | **video arm only** |
|---|---|---|---|
| rejection log, n=611 | 272 | 335 | **0** |
| resume corpus, n=1,079 | 373 | 704 | **1** |
| walk file, n=439 | 83 | 354 | **1** |

**Across 2,129 firings the video arm was the sole cause 2 times — 0.09%.** `photo_heavy` is, in
practice, the photo-share rule and nothing else. The legacy video clause is very nearly
decorative on today's data.

### 3.9 IS THE INPUT EVEN RIGHT? — one defect MANUFACTURES rejections

A rule can be correct and still fire wrongly if what it reads is wrong. Driven against a real
captured profile payload, with a control:

**A TikTok page with 360 videos reaches the judge as 5.** The profile writer stores the true
count under one key; the funnel reads a different key, gets nothing, then falls through to a
fallback that reports **how many videos our own crawl happened to fetch**.

```
  true value in the payload      360
  delivered to the judge           5
  display name delivered          ''   (structurally always empty)
```

**The display name is not merely missing — its documented fallback has ZERO writers.** A runtime
dump shows the author record carries exactly six keys, none of them a display name.

**⚠️ THE CONTROL IS THE FINDING.** Substituting the correct two keys and changing nothing else:
the display-name line returns, and his own numeric floor flips from
**`('BAD', 'only 5 video(s) posted…')`** to **`('PASS', '')`**.

**So the defect does not merely lose information — it MANUFACTURES A REJECTION out of our own
crawl depth.** A page is rejected for posting five videos when it posted 360. **A search would
have found both key names present in the file and concluded nothing was wrong**; only driving it
against a real payload shows it.

**And a free fix already sits one field away:** the grouped author record carries a video count
on 4 of 4 authors, before anything is bought.

### 3.10 HIS OWN NUMERIC FLOORS — CONFIRMED not running on Instagram, and worse than reported

His stated floors — **500 views, 10 videos** — live in one function whose only production caller
is on the TikTok path. Instagram's reject path goes somewhere else entirely and never touches
it. **Proved by a runtime control with call counters and no network:** identical facts
(`views=100, video_count=2`) give TikTok a rejection with the floor function called **once**, and
Instagram no rejection with it called **zero** times.

**Worse than the brief stated: the 10-video rule fires on NEITHER platform.** Instagram's facts
block packs no view count and no video count at all — and the shipped TikTok facts block has no
video-count key either, so the 5-versus-360 value above is invisible to the floor in the normal
path.

### 3.11 `aweme_type == 150` — the free TikTok photo signal, with a corrected denominator

**MEASURED: 70 of 1,099 = 6.37%, Wilson 95% [5.07, 7.97]**, over every captured record on disk.

**The 7.16% in this round's brief is 70/978 — the same 70 hits against one file's denominator
rather than the whole corpus.** Same numerator, narrower base.

It is a clean signal where it appears: `aweme_type == 150` coincides with a photo payload on
**978 of 978 = 100%**. It has **zero readers** in production. Of 100 typeable pages, **28 carry
at least one photo post [20.1, 37.5]**, and two are 100% photos.

**⚠️ But "one dict lookup" holds only on one endpoint.** The web-style payload carries no
`aweme_type` at all (0 of 5); only the app-style listing does. **So TikTok cannot have this rule
for free everywhere — only where that endpoint is already in use.**

### 3.12 CAN THE ENDPOINT CONFOUND RECUR? — **YES. MEASURED.**

A hashtag call once returned photos instead of clips and `photo_heavy` fired on **86 of 86**
accounts, killing the whole channel. **That can happen again.**

The hardening added afterwards went into a discovery module **that the funnel's hashtag path
does not call.** The shipped path uses a second, unhardened dispatcher at
`meme_finder.py:3359-3362`, and it has **two different fallbacks for two flavours of "no valid
value"**:

```
  str(kind or "clips")                    empty / None / 0  ->  clips    the good surface
  .get(..., client.hashtag_medias_recent) a MISSPELLING     ->  recent   the surface that
                                                                          killed the channel
```

A typo in one configuration key silently routes the funnel onto the photo surface. **The cost is
measured:** `/recent` returns **0.7% video** — 225 photos, 50 carousels, 2 videos out of 277 —
against 98.7% for `/clips`, and **0 of 37** accounts passed on it.

**Nothing notices.** No assertion checks the media kind of what came back; validation is
list-length only. The rule discovers the problem one paid profile fetch later, as mass
rejection, after the money is spent. A real instrument for this exists and **no production code
reads it.** And the two tests covering the dispatcher assert on **call signatures against stubs
returning `None`** — one of them actively **pins the fallback-to-`recent` behaviour** without
requiring so much as a log line.

**The docstring defends the design — *"a bad config value must cost supply quality, never the
run"* — and that intent is right. The chosen fallback is simply the worst available surface,
and it disagrees with the same function's own default two lines above.**

---

## 4. WHAT WAS REFUSED, AND WHY

- **No new setting was shipped.** The threshold is already configurable through a correct
  implementation, proved above. Adding a second lever would duplicate a working one.
- **No threshold was changed.** The round measures; he decides. Section 7 prices each option.
- **The one-identifier fix to the hashtag fallback was NOT applied.** It is small and its cost
  is measured, so it qualifies — but `meme_finder.py` is held by a live peer round that
  committed to it twice during this audit. **A handover was requested and the peer's answer was
  that nothing was needed from them for the setting question; changing a rule dispatcher is a
  different ask and there was no time to negotiate it without racing a dirty file.** It is
  written up here in full so whoever holds that file next can apply it in ten minutes.
- **The stale note in his configuration was NOT edited.** It still describes the old reels
  endpoint as shipped and has already caused one retraction — **this round's own.** That file is
  held by another peer round.
- **The TikTok photo-type field was NOT wired as a rule.** It is a clean free signal
  (coincides with a photo payload on 978 of 978) but **nobody has scored it against his marks**,
  and it is absent from one of the two payload shapes in use. Extracting it onto the row so a
  future sweep is free costs nothing; gating on it unscored would repeat the mistake this round
  was sent to investigate.
- **His 500-view / 10-video floors were NOT switched on for Instagram.** They are small to plumb
  and **unscored on Instagram marks** — nobody has observed what they would kill. Count first,
  gate second.
- **No production file was written at all**, so his dashboard was never restarted.

---

## 5. WHAT I GOT WRONG

The most useful section, and this round produced four.

### 5.1 I published "the rule is inert" and had to retract it before it reached him

I read `photos_endpoint = ""`, found a docstring saying that disables the second fetch, drove
the shipped predicate against an all-video post list, and concluded the rule could not fire.
**Wrong.** A comment further down says the empty string now means *merged, not disabled*, and
his primary endpoint had been changed to the photo-capable one.

**The supporting measurement was worse than the reasoning.** I reported 3,748 of 3,749 typed
posts as video — then split that sample by capture date and found **all of it is older than 14
days, with the last 14 days giving n=1.** I had a confident conclusion resting entirely on a
pre-merge corpus.

**What saved it was a comment that named the wrong inference instead of restating the code.**
Its author had already watched this rule get "fixed twice and measured never" and wrote down
*why* the obvious reading would be wrong. Every other comment in that file told me what the code
does, which I could already see.

### 5.2 My own regex silently answered a different question

Checking a colleague's finding, I searched a probe file for `"media_type": <n>` and got
`{12: 6}` — which contradicted their report. **My pattern was matching a field-presence counter**
(`"media_type": 12` meaning *twelve items carried this field*) **rather than the histogram
`media_types`.** Printing the file showed they were right and I was wrong. A silent, plausible,
confidently-wrong answer that nearly caused me to correct a correct colleague.

### 5.3 I repeated the fire-rate-as-precision error in a published report

In a document published the day before, I wrote that this rule's 97.5% precision is
"endpoint-dependent: 97.4% against 30.0%, disjoint intervals." **Those two numbers are FIRE
RATES, not precisions.** The source row is labelled "`photo_heavy` fires". **That published
report is being corrected alongside this one.**

### 5.4 I gave a colleague a stale line number

Handing over anchors after the file moved, I supplied nine post-move numbers and one pre-move
number, and the stale one now points into an unrelated block. **Caught by the colleague, not by
me.** My tooling re-derives anchors by AST and self-corrected; my prose did not, and prose is
what people read.

### 5.5 I carried a wrong explanation for the firing discrepancy and nearly published it

I wrote that 588-versus-439 was "likeliest per-run versus cumulative", and was careful to mark it
unverified — which was right, because **it is wrong.** Both counts are cumulative; they come from
different files covering **disjoint windows**, and are additive rather than competing. The
resemblance that made them look like rival counts of one thing is a coincidence with a third
number (a per-run maximum of 429). **Marking it unverified saved the report; it did not make the
guess any less wrong, and a reader who skimmed the hedge would have carried the error away.**

### 5.6 One of this round's own counters returned a confident zero across 40,834 rows

A sweep of the resume corpus initially found **zero** firings in 40,834 rows. The field it read
is a comma-separated **string** in that store, not a list, so every membership test failed
silently. **The positive control caught it** and the true count is 1,079. A zero across forty
thousand rows is exactly the kind of result that reads as a finding.

### 5.7 The shell silently deleted a phrase from this report while I was writing it

Editing this file through a shell command, I wrapped a field name in backticks inside a
double-quoted string. **The shell executed it as a command substitution and replaced it with
nothing**, leaving the sentence *"** was NOT wired as a rule"* — a grammatical sentence missing
its subject. The command reported success. It was caught by reading the result back, not by any
error.

**Recorded because it is the same shape as everything else in this section, and because it
happened inside the document describing the pattern.**

### 5.8 And the same shell edit silently converted the whole file to Windows line endings

The publication gate **refused to write this report**: 647 carriage-return bytes, introduced when
a scripted edit re-wrote the file using the platform's default newline translation. Nothing
warned; the file looked identical.

**This is the failure mode that once rewrote 3,633 lines for a 66-line change**, and the only
reason it did not reach the repository is that the byte assertion runs **before** the write and
abandons it on failure rather than repairing afterwards. Normalised, verified byte-for-byte
identical apart from line endings, and re-scanned.

**The pattern in all eight: every one was silent and plausible.** None raised an error. Six of
the eight were caught by something outside my own reasoning — a colleague, a control, a
read-back, a pre-write assertion, or a comment written by someone who had seen the trap before.
**Two were caught by the safeguards in this round's own publication process**, which is the
argument for having them.

---

## 6. MONEY AND SAFETY

```
  vendor calls made by this round        0
  vendor dollars spent                   $0.00      (cap was $0.75)
  production files written               0
  config files written                   0
  seen stores written                    0
  processes killed                       0
```

Everything measured here came from data already on disk. The probe that settled the endpoint
question had been sitting unread — a prior round recorded that question as needing a live call,
and it did not.

**Backups taken before any work, and verified by re-hashing from disk, because there is no
backup drive** — the scheduled backup returns error 2 and nothing deleted is recoverable:

```
  config.json  spend.json  master_leads.csv  and all four seen stores
  7 of 7 copies verified byte-identical by SHA-256 re-read
```

**Seen stores re-verified AT PUBLICATION, not only at check time.** The Instagram store moved
during this round — **not this round's write**, which wrote nothing; peers are active in it.
Disk was re-read before every phase and never approached any floor.

His four servers were confirmed listening **through the operating system's port table, never a
command-line search** — a process filter once matched its own command line and reported two live
where there were none. All four were left alone.

**Files held by other rounds were read and never written.** The rule's file was committed to
twice by its owner during this audit; every line number here was re-derived by text afterwards.

---

## 7. WHAT HE SHOULD DO NEXT — RANKED, WITH THE ARITHMETIC

### 1. KEEP THE PHOTO CUT AT 10%. It is not costing him what he was told it costs.

**The arithmetic, on 95 of his marked pages:**

| if he sets it to | he catches | he loses from his 8-10s | he loses from everything he wants |
|---|---|---|---|
| **0.10 — today** | **37 of 67 bad pages** | **0 of 11** | 1 of 19 (a page he scored 6, 16.7% photos) |
| 0.70 — as he described | 14 of 67 | 0 of 11 | 0 of 19 |

**Moving from 10% to 70% would save him one page he scored 6, and cost him 23 bad pages he is
currently not seeing.** That is the whole trade.

**And the reason he was told otherwise:** the "kills a quarter of his approvals" warning is real,
but it was measured against his 15 August marks. Re-scored there the rule does kill 8 of 28 —
**and he re-marked those same eight pages seven days later at 1, 1, 1, 5, 4, 3, 2 and 6.** Seven
of the eight are now rejections. **The rule was scored against approvals he has since
withdrawn** — the same trap that made a correct filter look like a failure on the car and gym
reversal.

**If he still dislikes the rule, the honest lever is not the threshold** — all his best pages are
100% video, so no threshold reaches them. The lever is to switch it off entirely by setting the
value to `null`, which the code supports without an edit.

### 2. Rename it, or he will keep not understanding it.

It cuts at 10%. "Photo heavy" describes a page that is mostly photos. **The name and the number
disagree by a factor of seven**, and he said in as many words that the argument does not make
sense to him. `any_photos` or `photo_share_over_10pct` would end the confusion permanently.
Costs nothing and changes no behaviour.

### 3. Fix the hashtag fallback — one identifier, and the cost of not fixing it is already paid once.

A misspelled endpoint key silently routes the funnel to the surface that returns **0.7% video**
and once killed an entire channel at **0 of 86**. The same function already defaults to the good
surface when the value is empty; it should do the same when the value is wrong. **The arithmetic:
one identifier, versus a repeat of a failure that has already cost one channel and 86 wasted
profile fetches.** Add an assertion on the media kind of what comes back, so the next occurrence
is loud instead of silent.

### 4. Fix the TikTok video count — it is currently manufacturing rejections.

A page with **360 videos reaches the judge as 5**, because two keys are read that are never
written, and the fallback reports how deep our own crawl went. **The arithmetic: with the correct
keys substituted and nothing else changed, his own floor flips from "BAD — only 5 videos posted"
to "PASS".** Pages are being rejected for our crawl depth, not for their content. The correct
value is already in the payload, and a second free copy sits on the grouped author record.

This is **small and scored** — the two corrected reads were measured on 66 pages he wants, with
harm bounded near zero (4.6% [1.6, 12.7], p=0.500). **Wiring the video count so the 10-video
floor actually fires is a SEPARATE and UNSCORED change** and should not be bundled with it: that
floor currently fires on neither platform, and switching on a reject gate with zero observations
of what it kills is how this project has hurt itself repeatedly.

### 5. Find what is writing probe rows into the production rejection log, and give it its own file.

Two fabricated handles appear in the live rejection log with a stated cut of **0%**, alongside a
view floor of 1,000,000 and a one-day staleness cut. **The arithmetic: this round was
commissioned partly to explain "four firings on 2026-08-31", and all four are fixtures.** Anyone
counting rule behaviour from that file is counting test data as production events — and a future
round will spend real time on them again, exactly as this one did.

**The first step is identifying the writer, which this round did not manage.** Searching for the
two handles across the whole tree timed out. The cheap route is the reverse one: add the writing
process's own name to each row at the point of append, so the next anomaly identifies itself
instead of costing a search.

### 6. Record the posts endpoint beside every rule measurement, permanently.

The precision figure that three production files quote **cannot be attributed to an endpoint and
is therefore uninterpretable** — and two figures from the same day, same marks and same rule
differ by everything (85.0% versus 0 of 192) purely on that variable. **The arithmetic:** one
extra field per measurement, against a history in which the single most-quoted number about this
rule is unusable.

### 7. Then look at the grid gap, which is bigger than everything above.

**51.9% of Instagram pages have no grid image and can never reach the model judge.** On those
pages the free rules are the only opinion, with nothing able to overrule them. Every accuracy
argument in this project — including this one — concerns a stage that half the traffic never
reaches.

---

## 8. WHERE THE FILES ARE

Paste into File Explorer. `%USERPROFILE%` expands on its own, so no username is written here.
**No port numbers appear anywhere in this report** — they are not stable across runs and a
grading session was lost to a bookmarked one. Start any server from its own launcher and use the
address it prints at that moment.

```
  the project
    %USERPROFILE%/OneDrive/Desktop/clipper finder

  THE ONE NUMBER HE MIGHT CHANGE
    %USERPROFILE%/OneDrive/Desktop/clipper finder/config.json
      the key is  meme_finder.max_photo_share   (currently 0.1)
      set it to null to switch the rule off entirely, with no code change

  the rule itself, and the dispatcher with the bad fallback
    %USERPROFILE%/OneDrive/Desktop/clipper finder/clippershq/meme_finder.py

  this round's own evidence
    %USERPROFILE%/OneDrive/Desktop/clipper finder/scratch
      bl1479_spy_out.txt        the four proofs that the setting selects
      bl1479_sweep.md           the threshold sweep, three arms, baseline
      bl1479_endpoint.md        the endpoint confound and the precision table
      bl1479_backups_*          the verified copies taken before any work
```

---

*Every rate carries its denominator and a Wilson 95% interval. Every figure is marked MEASURED,
DERIVED, REFUTED, RETRACTED or UNRESOLVED. Where two sources disagree and neither is settled,
both are named and neither is chosen.*
