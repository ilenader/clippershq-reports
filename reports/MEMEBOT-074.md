# MEMEBOT-074 — I watched all 30. **A 100k repost page would post 3.** The music landed on 27 of 30 (BL-950 had 0 of 25), and the fix that stopped captions being cut mid-word now deletes the last word of every caption that does not end in a full stop — which is **5 of the 5 captions in this batch that read like a hook at all.**

**Date:** 2026-08-02 · **Type:** Viewer audit, first since BL-950 · **Spend:** **$0.0210** of a $0.30 budget
**Wrote:** `scratch/mb074_*.py|json`, `scratch/mb074_frames/`, `scratch/MEMEBOT-074.md`, this report.
**Read but never wrote:** `clippershq/clip_pipeline.py`, `clippershq/song_library.py`,
`memebot/scraper/edit.py`, `scratch/songs.json`, `scratch/mb066_corr.py`.

---

## 1. The per-video judgement

Rendered unattended through the real path — `python -m clippershq.run --funnel clip_render`,
no `explicit_song`, the real 2,003-clip library, the real ranker, the real song store.
**Post** = a 100k repost page posts it as it stands. **Fix** = one specific change away.
**No** = would not go out.

| # | account | what it is | dur | song | dead canvas | verdict — first disqualifier |
|---|---|---|---:|---|---:|---|
| 1 | movyclipz | Final Destination compilation | 23.9s | song04 h2 | 27% | **Fix** — caption is a plot synopsis; source's own "No monster. No killer." is the better line |
| 2 | ashoraif | POW drama, RIVEN-EDITS watermark | 57.8s | song04 h3 | 44% | **No** — 58s; caption opens `":-"`; another page's watermark |
| 3 | primecuttv | Persian psych-analysis of Tokyo | 61.5s | song04 h4 | 49% | **No** — **caption renders as □□□□ boxes**; 62s; hype music on a therapy post |
| 4 | thomasabg | Last Samurai | 54.7s | song04 h5 | 49% | **No** — nested letterbox, 28% black; source's headline top-sliced; 55s |
| 5 | clipcapture.tv | Two and a Half Men | 74.6s | song01 h1 | 26% | **No** — **74.6s**; caption is a *streaming availability listing* |
| 6 | randomly_curious | FIFA semi-finalists graphic | 8.3s | song03 h5 | 24% | **Post** — right length, right song, static but that is the format |
| 7 | smoovereactss | Bleach reaction | 58.9s | song04 h1 | 26% | **No** — 59s; caption lost its last word (below) |
| 8 | thomasabg | Unthinkable | 59.0s | song04 h2 | 45% | **No** — 59s; source's headline top-sliced; nested letterbox |
| 9 | primecuttv | Persian psych-analysis of The Hound | 58.2s | song04 h3 | 51% | **No** — **caption is boxes**; 58s; square source, 33% white |
| 10 | random_shyt0 | The Boys edit | 15.8s | song04 h5 | **61%** | **No** — **61% dead canvas**; caption's last line sliced by the video |
| 11 | screenjunkiebe | Troy | 40.3s | song04 h2 | 26% | **Fix** — good song, good source hook; 40s is the problem |
| 12 | matheuxmendex | PT-BR talking head, Globoplay promo | **88.5s** | song04 h4 | 27% | **No** — 88s of a review; hype music over speech |
| 13 | smoovereactss | Dragon Ball reaction | 68.3s | song04 h1 | 26% | **No** — 68s; caption "Hype is real" shipped as "Hype is…" |
| 14 | zackrawrrshorts | Asmongold reaction | **80.0s** | song04 h2 | 27% | **No** — 80s; "people actually believed this" → "people actually believed…" |
| 15 | thomasabg | Jojo Rabbit | 55.7s | song04 h3 | 53% | **No** — 56s; hype music on a tender scene; source headline top-sliced |
| 16 | solidshampooz | LEGO Batman friendship meme | 20.1s | song04 h4 | 58% | **No** — 58% dead; "I knew you in another life" → "…in another…"; hype on a goofy meme |
| 17 | memes_literallyme | "good taste in video games" list | 16.8s | song04 h5 | 57% | **No** — **our whole caption is the word "Real"**; 57% dead |
| 18 | zackrawrrshorts | Asmongold gym reaction | 72.5s | song04 h1 | 26% | **No** — 72s; "lil bro pulled an ELITE" → "lil bro pulled an…" |
| 19 | cinemavault.01 | Jackie Chan, CINEMAVAULT brand bar | 63.6s | song04 h2 | 41% | **No** — 64s; republishes a rival page's logo + verified tick |
| 20 | thomasabg | Jojo Rabbit (2nd scene, same account) | 56.2s | song04 h3 | 50% | **No** — 56s; hype music on a Holocaust-adjacent scene |
| 21 | randomly_curious | FIFA finals graphic | 8.0s | song03 h1 | 26% | **Post** — 8s, football song on football content |
| 22 | matheuxmendex | PT-BR Sandman explainer | 55.0s | song04 h4 | 26% | **No** — 55s; caption ends `"? . . ."`; hype over speech |
| 23 | randomly_curious | FIFA semi-finalists, blue variant | 8.2s | song03 h2 | 26% | **Post** — same as 21; source title top-sliced to "rIFA" |
| 24 | superhero_moviesupdate | Avengers Doomsday rumour collage | 8.2s | song04 h5 | 54% | **No** — 54% dead, very dark, nothing moves; song not attributable |
| 25 | screenjunkiebe | Madea | 36.1s | song04 h1 | 37% | **No** — **hype battle music on a comedy**; 36s; black rotation wedges |
| 26 | matheuxmendex | PT-BR Game of Thrones lore | **91.6s** | song04 h2 | 26% | **No** — **91.6s**, the longest; hype over a talking head |
| 27 | thomasabg | Yellowstone | 25.7s | song04 h3 | 54% | **Fix** — right length, right song; 54% dead canvas is the problem |
| 28 | loste1980 | Small Soldiers | 50.3s | song04 h4 | 50% | **No** — 50s; caption says "Small Soldiers" twice; headline top-sliced |
| 29 | clipsvaultex | Avengers Endgame | 31.2s | song04 h5 | **62%** | **No** — **62% dead canvas**, the worst; caption is a *cast list* |
| 30 | randomly_curious | FIFA semi-finalists — **duplicate of #6** | 9.2s | song03 h3 | 24% | **No** — the ranker picked the same creative twice |

**Post: 3 (#6, #21, #23). Fix: 4 (#1, #11, #27, and #30 if the duplicate is dropped). No: 23.**

All three postable ones are static infographics from **one account**, `randomly_curious.official`,
which supplied 4 of the 30. **Not one of the 26 video clips is postable as it stands.**

---

## 2. Verified by measurement, never by exit code

`scratch/mb074_verify.py`. Four checks per video; a render is PASS only if all four hold.

| check | method | result |
|---|---|---|
| audio stream present | `ffprobe -select_streams a` | **30 / 30** |
| duration clears the 8.0s floor | video-stream duration on the artefact | **30 / 30** (min 8.00s) |
| ledger record joins the store | `"%s@%s-%s" % (song, start_sec, end_sec)` ∈ `store_hook_keys` | **30 / 30** |
| carries the configured track | 40–250 Hz signed envelope correlation vs the applied window, every other track as the null | **27 / 30** |

**27 of 30 PASS all four.** The three that miss are attribution, not silence: #3 (r=0.28, margin
0.09), #24 (r=0.58, margin 0.05), #30 (r=0.51, margin 0.01) — the bed is audible, it just does not
beat the null by the 0.10 bar. Median r on the other 27 is **0.93**.

**A method error I made and corrected.** My first null gave each competing track its whole file
as a reference. That scored **0.94 against a track the render never touched**, and 5 of 12 videos
"failed". The cause is in `mb066_corr.best_corr`: the lag search runs to
`min(len(reference), len(video))`, so a 162-second reference slides across its whole duration and
keeps the best of thousands of alignments. A marked hook is 10–27s, which bounds the search — which
is what mb066's own docstring says it is doing. Hooks-only nulls restored the method. The unbounded
number is kept per row as `noise_floor_unbounded`, because it is the honest noise floor of this
measurement and any r has to be read against it rather than against zero.

Two renders of 30 attempted **failed on purpose**, and correctly:
`ERROR ... no audio class supplied, so the treatment cannot be routed, and guessing it is how
BL-950 got 0 of 25` — rc=1. MEMEBOT-066's refusal moves the exit code, exactly as intended.

---

## 3. What reading the frames found

30 contact sheets read, plus 2 caption bands and 1 stacked band at full 1080-px resolution, plus a
staged source frame. Every defect below came from looking, not from a counter.

### 3a. The caption fix now deletes the payoff word — **5 of the 5 hook-shaped captions**

The ledger says the caption was complete. The burned-in caption is not:

```
ledger                                   rendered
"lil bro pulled an ELITE"          ->    "lil bro pulled an…"
"Hype is real"                     ->    "Hype is…"
"I knew you in another life"       ->    "I knew you in another…"
"people actually believed this"    ->    "people actually believed…"
"Might have to rewatch bleach      ->    "Might have to rewatch bleach…"
 honestly"
```

`edit.caption_hook` (edit.py:793–798):

```python
if not ends and s and s[-1] not in ".!?…)]\"'”’":
    head = s.rsplit(" ", 1)[0] if " " in s else ""
    if head:
        s = head.rstrip(" ,;:—–-") + "…"
```

**When a caption contains no sentence terminator anywhere, its last word is dropped and an
ellipsis added — at any length.** The comment names the trade and accepts it: *"That costs a
legitimate list caption its last word; it costs a severed one its severed half. Given that 25 of 25
shipped videos were severed, that trade is the right way round."*

It is now the wrong way round, for a reason that did not exist when it was written. The severed
half it was defending against came from a caller slicing to 90 characters, and **that caller is
gone** — `clip_pipeline.clean_caption` cuts only above 120 chars and appends its own `"..."` at a
word boundary when it does. So a caption arriving under 120 characters is provably intact, and this
rule still eats its last word. One full stop is the whole difference:

```
'lil bro pulled an ELITE'   -> 'lil bro pulled an…'
'lil bro pulled an ELITE.'  -> 'lil bro pulled an ELITE.'
```

Instagram captions do not end in full stops. **All five losses are short, human-written,
hook-shaped lines — the only five in the batch that were worth burning in at all.** The other 25
are scraped synopses that get ellipsised anyway, so the rule protects exactly the captions that
did not need protecting and destroys exactly the ones that did.

### 3b. Non-Latin captions render as empty boxes — 2 of 30

`#3` and `#9` (primecuttv) carry Persian captions. Montserrat-Bold has no Arabic glyphs, so the
finished frame shows three lines of `□□□□ □□□□□`, with only the parenthesised Latin — `(Tokyo)`,
`(The Hound)`, `(Emotional Dysregulation)` — legible. `clean_caption` strips emoji for exactly this
reason (`_EMOJI` → "they render as blank boxes on a finished deliverable") and does not check any
other script. **BL-950 never saw this class; both of these are unshippable, not merely weak.**

### 3c. The source's own headline is still being sliced — vertically now

MEMEBOT-071 fixed the horizontal half of `detect_content_crop` (`x, w = 0, w0`) because a
caption bar's outer pixels read as letterbox. The vertical half still crops, and it lands *inside*
the source's own text. Measured on `#8`'s staged 720×1280 source:

```
source caption ink begins at row 197   (unchanged at every luma threshold 24..160)
detect_content_crop returns            crop=720:798:0:200
```

Three rows of the ascenders are discarded, then the frame is scaled up ~1.43×. Read off the
finished frames: `#8` "Interrogator threatens to torture" with the tops gone; `#27` "Rip Wheeler"
reading as "Kip"; `#23`/`#30` "FIFA WORLD CUP" reading as "rIFA WORLD CUr". **Still live** — I
re-ran `detect_content_crop` against the current working tree after MEMEBOT-071's latest edit
(edit.py `b20ced6c`, 15:27) and it returns `crop=720:798:0:200` unchanged.

Affects at least **6 of 30** (#4, #8, #15, #20, #23, #27, #28, #30 — 8 by eye, 6 unambiguous).

### 3d. Our caption's last line is sliced by the video — 3 of 30

Confirmed by eye at full resolution on `#3`, `#10`, `#16`. On `#10` the last line measures 41 px
against 47 px for the two identical-size lines above it, and its ink stops on the row immediately
above the video's top edge.

**A hypothesis I had and killed:** I assumed the rolled `position_shift_y ∈ [-8, +8]` walked the
picture up into the caption. It does not — `edit.py:1859` adds `tx_shift_y` to the caption's `y`
as well, so the template's 5-px clearance is preserved at every shift. What is left is that the
rendered ink overshoots the bottom implied by `y="275-text_h"`, and the overshoot exceeds 5 px at
the larger auto-fit sizes: on `#10` the lines are 47 px tall, on `#1` (not clipped) they are 38–41.

**My automated detector is not trustworthy and I am not quoting its count.** It flagged 7; four
were false positives where it read the source's own dark band edge as a caption line. The three
above are the ones I read.

### 3e. Dead canvas — **median 39.2%, worst 61.8%**, essentially unchanged from BL-950

Measured from the pixels (bounding box of non-canvas content below the caption band), not from
template arithmetic, because MEMEBOT-071 made the zoom enlarge the video into the margin.

```
>= 45% dead canvas : 12 / 30      worst: #29 61.8%, #10 61.4%, #16 58.4%
>= 20% near-black  : 15 / 30      worst: #6 38%, #21/#23/#30 31-32%, #3 30%
```

The shape is always the same and it is a template/source mismatch, not a bug: `white_frame` scales
to 864 px wide on a 1080×1920 canvas and drops the video at y=280. A 9:16 source fills the height
and dead canvas lands near 26%. A **square or landscape** source cannot — `#29`'s 16:9 picture
occupies rows 280–1100 and everything below is flat white. The five `thomasabg`-style clips are
worse again: the source is *itself* a letterboxed black canvas, so the finished frame is white →
our caption → black band → their caption → a small picture → black → white.

### 3f. Nothing happens on screen at the drop, and that is measured

The drop is located on the artefact (largest positive step in the 40–250 Hz envelope), then
compared to the source's own scene cuts:

```
videos with both a bass onset and detectable cuts : 17
drop within 0.25s of a cut                        :  2 / 17
median distance to nearest cut                    : 6.87s
median distance from a RANDOM instant             : 6.25s   <- chance
beats chance                                      :  8 / 17
```

**Indistinguishable from picking a moment at random**, and slightly worse than chance. Worse, on
**17 of 30 the drop arrives after 10 seconds** — `#26` at 91.1s, `#14` at 78.3s, `#13` at 55.0s.
Nobody is still watching.

### 3g. Two other things that read as amateur

- **Rotation leaves visible wedges.** The rolled `rotation_deg ∈ [-0.8, 0.8]` on a source with
  rounded corners leaves black or white arcs biting into the picture's corners — obvious on
  `#1`, `#2`, `#11`, `#12`, `#25`, `#26`.
- **We republish other pages' branding.** `#19` carries CINEMAVAULT's logo *and a verified tick*;
  `#2` RIVEN-EDITS; `#3`/`#9` PRIMECUTTV MOVIE SERIES; `#17` memes_literallyme; `#10` @random_shyt0.

---

## 4. Song fit, all 30 — and yes, it reads as lazy

The store holds **4 tracks and 21 hand-marked windows**. This batch used **25 song04, 4 song03,
1 song01 — 83% one track**, and **`song_repeat_forced` fired on 22 of 24** logged picks: after
`avoid=recent_track_ids(k=3)` there was nothing left to choose from, so the no-repeat guard was
overridden. Rotation *within* song04 is healthy — h1..h5 all used, **10 of 21 windows reached**,
which is MEMEBOT-072's fix working. The concentration is one layer up.

The cause is legible in the ledger: **25 of 30 matched via a `-> mood:hype` rule**, and hype has
exactly one track.

| fit | n | videos |
|---|---:|---|
| **Right** | 8 | #6 #21 #23 (football graphic → football song), #11 Troy, #13 DBZ, #19 Jackie Chan, #27 Yellowstone, #29 Endgame |
| **Defensible but generic** | 9 | #1 #2 #4 #7 #8 #9 #24 #28 — action footage, hype music, nothing wrong and nothing chosen |
| **Wrong** | 13 | #25 Madea **comedy** → battle music · #15 #20 Jojo Rabbit, tender/sombre → battle music · #16 LEGO Batman friendship meme → battle music · #3 a Persian therapy post → battle music · #12 #22 #26 Portuguese talking heads → battle music over speech · #14 #18 Asmongold reactions → same · #5 a breakup clip got song01 melancholy, which is right, over **74.6 seconds** · #10 #17 list-format memes → battle music |
| **Not attributable** | 3 | #3 #24 #30 (see §2) |

**It reads as lazy, and the honest version is that it is not laziness, it is arithmetic.** With
one hype track and a `franchise_mood_map` whose 15 entries all point at `hype`, a repost page
posting this daily publishes the same song 5 days out of 6. A viewer who follows the page hears it
before the video loads. The three that land — the football graphics — land because `fifa` and
`world cup` are the only strong vision tokens in the batch routing anywhere other than hype.

`#25` is the sharpest case and it confirms BL-894 from the deliverable side: **the system cannot
see comedy.** Madea, in a dress, matched `weak-pair:fight,fighting` and got battle music.

---

## 5. The verdict, and the problems ranked

**A 100k repost page posts 3 of 30 — all three static football infographics from one account.
Zero of the 26 actual video clips.**

That is up from BL-950's 0 of 25, and the reason is real: the music now lands. It is not up much,
because the two defects that replaced BL-950's are just as visible.

| rank | problem | videos | why it ranks here |
|---|---|---:|---|
| **1** | **Over 30 seconds** | **20 / 30** | up to **91.6s**. A repost page's norm is 7–15s. This alone kills two thirds of the batch |
| **2** | Caption is scraped reference text — synopsis, cast list, streaming availability | 25 / 30 | nobody stops scrolling for "Original Network: CBS" |
| **3** | ≥45% dead canvas | 12 / 30 | template assumes 9:16; square and landscape sources leave half the frame flat white |
| **4** | ≥20% near-black inside the frame | 15 / 30 | nested letterbox on the reposted-repost sources |
| **5** | Hype music on content that is not hype | 13 / 30 | comedy, tenderness, talking heads |
| **6** | The source's own headline top-sliced by the vertical content crop | ≥6 / 30 | "rIFA WORLD CUr" |
| **7** | **Last word of the caption deleted** | **5 / 30** | but it is **5 of the 5 captions worth having** |
| **8** | Two competing captions, ours the weaker | ≥12 / 30 | the source's burned-in hook is better on every one I read |
| **9** | Non-Latin caption renders as boxes | 2 / 30 | unshippable outright |
| **10** | Our caption's last line sliced by the video | 3 / 30 | confirmed by eye |
| **11** | Another page's watermark or brand bar republished | ≥5 / 30 | `#19` carries a rival's verified tick |
| **12** | Duplicate creative in the same batch | 1 / 30 | `#30` is `#6` |

**Ranks 1 and 2 are the product not working.** Both are one decision away and neither needs new
measurement: a maximum duration (the gate's `MAX_DURATION_S` is 90.0, and 90 seconds is not a
repost), and a caption source that is not the poster's SEO blurb — the source's own burned-in hook
is already better on every video I read.

---

## 6. Against BL-950 specifically

| BL-950's finding | now |
|---|---|
| **"not one video has the song"** — 0/25, 12 silent | **FIXED.** 30/30 have an audio stream, **27/30 carry the configured track**, median r 0.93 against a hook-bounded null. `audio_class` reaches `edit.py` on all 30, and two renders **refused** rather than guessing |
| **"caption truncated mid-word on every one"** — "It bec", "the San" | **FIXED as stated, and replaced.** Zero mid-word cuts in 30. Every long caption now ends on a whole word with an ellipsis. But the fix that did it **deletes the last word of any caption with no sentence terminator**, which hit 5 of 30 — and all 5 were the short human hooks |
| **"~45% dead canvas"**, "the bottom ~45% is blank white"; ≥20% black on 3/25 | **SURVIVES.** Median **39.2%**, 12/30 at ≥45%, worst **61.8%**. ≥20% near-black is **15/30**, up from 3/25 — this batch drew more reposted-reposts |
| **"the source's own better hook clipped"** by the crop | **HALF FIXED.** The horizontal crop that produced "essed up" is gone (`x, w = 0, w0`). The **vertical** crop still shaves the top of the source's headline on ≥6 of 30, and is live in the current working tree |
| items 3 & 4 "unanswerable — none has the song" | **ANSWERABLE NOW, AND THE ANSWER IS BAD.** The drop lands no closer to a scene cut than a random instant (2/17 on a cut; 6.87s median vs 6.25s chance), and on 17/30 it arrives after 10 seconds |
| "7 run over 30 seconds, up to 79.6s" | **WORSE.** **20/30** over 30s, up to **91.6s** |
| "the captions are scraped reference text" | **UNCHANGED.** 25/30 |
| the duration floor trimmed clips below the bar it enforced | **FIXED.** 30/30 clear 8.0s, minimum 8.00s, zero `edit:under-floor` |

Two of BL-950's four are fixed, one is half fixed, one survives intact — and the caption fix
introduced a new defect in the same place.

---

## 7. Verification

| check | result |
|---|---|
| videos rendered | **30** (2 + 28, one process each, `--funnel clip_render`) |
| render path | `clippershq.run` → `control._render_clips` → `clip_pipeline.run_batch`; no `explicit_song`, real library, real ranker, real fetchers |
| attempted / made | 30 attempted, 28 made in the second batch; 2 **refused** for a missing audio class (rc=1, by design) |
| paid calls | 33 re-fetches, **$0.0198** + $0.0012 smoke = **$0.0210** |
| sheets read | **30 / 30** composition sheets, + 2 caption bands + 1 stacked band at full 1080-px, + 1 staged source frame |
| all four measurements pass | **27 / 30** |
| code state at render time | `edit.py` sha256 `0d6369e0…`, `templates.yaml` `85fa20d3…`, `config.yaml` `311f29c1…`, `clip_pipeline.py` `fd1fd698…`, `songs.json` `1e4b28a3…` |
| suite | **142 of 143 green** (469.8s, `PYTHONUTF8=1 python tests/run_all.py`, nested-dirs discovery) |
| the one red | `tests/test_funnel.py` → `merge columns appended LAST` — **not mine**, see below |
| shipped code changed | **none** |

**The red is BL-964's, named.** `all_bot_ready.BOT_READY_COLUMNS[9:]` now ends
`… rank_median_views, date_sent, touch_number`; the test asserts it ends at `rank_median_views`.
The two columns were added by BL-964 (commit `3230380`, "MX table covers 100% of the send file")
without updating the contract test. **Owner: BL-964, `clippershq/all_bot_ready.py` +
`tests/test_funnel.py`.** I wrote no shipped code this round and nothing in that path.

## Limits

- **`edit.py` moved during the session, but not during the renders.** It was
  `0d6369e0` when I snapshotted it and `b20ced6c` afterwards (mtime 15:27:31); my last render
  finished at **15:04:01**. All 30 used one build. MEMEBOT-071 holds that file and committed
  `b7eca8b` mid-session; I read it and wrote nothing.
- **I cannot hear them.** "Carries the track" is a correlation on a loudness contour. Whether the
  mix is *pleasant* — the bed level, the ducking — is not measured here.
- **"Would a page post this" is judgement.** The 20 over 30 seconds and the 2 rendering as boxes
  need none. The rest is taste, informed by the format.
- **My caption-clip detector is unreliable** (§3d) and its count is not quoted. Three cases were
  adjudicated by eye at full resolution; there may be more I did not catch, or fewer.
- **The song-fit column is one person's taste on 30 clips**, not a measurement. The 83%-one-track
  concentration and the 25/30 `-> mood:hype` routing behind it *are* measured.
- **The three attribution misses are not "no song".** The bed is audible on all three; it fails to
  beat the null. Two of the three (#24, #30) are short clips where the bed loops.
- **`randomly_curious.official` supplied 4 of 30 and all 3 postables.** A batch drawn on a different
  day would rank differently; this is 30 clips, not a survey of the 2,003.
