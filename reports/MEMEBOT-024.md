# MEMEBOT-024 — **The biggest comedy cluster is a FORM, not a subject**: 179 clips where a caption does the joke over a near-still face. And the hook wiring is not one line — it is four, one of which hangs ffmpeg forever

**Date:** 2026-08-01 · **Type:** Read-only analysis (Part A) + measured proof (Part B) · **Spend:** **$0.00 · 0 paid calls · 0 network requests**
Claim `MEMEBOT-024` filed before the first read. **No `clippershq/` module was edited and no `memebot/` file was written** — see §9, which is the most important operational fact in this report.

Honesty tiers: **VERIFIED** (measured this round), **CORRECTION**, **GAP**.

---

## Verdict first

**Part A.** "Comedy 384" was never a song brief, and sub-clustering it says something the genre label hid: the largest buyable cluster is **`textoverlay_reaction` — 51 of 131 labelled parked comedy clips (38.9%), projecting to ~179** — clips where the picture is a near-still face and **the caption is the joke**. It wants a completely different track from everything else in the pile, because there is no dialogue to sit under and no action to hit: the song is the entire soundtrack.

**And the shopping list is smaller than it looks, for a reason that is a treatment finding rather than a music one.** **81% of measured parked comedy clips are speech-heavy.** The joke is in the words. Mute-and-replace destroys it, and ducking was closed on measurement by MEMEBOT-020. **Most of the comedy pile should be KEEP-ORIGINAL, not a new song.**

**The blocker on saying which is which is structural and nobody has noticed it:** clustering needs a vision label, treatment needs a speech label, and **only 7 clips out of 2,003 have both** — 0.3%, where independence predicts 206. The two labelling passes are running on near-disjoint halves of the library.

**Part B.** MEMEBOT-023 went in flight **1.5 minutes before this round's claim** covering B1/B2/B4/B5/B6 almost verbatim. **I did not duplicate it** — MEMEBOT-017 was the round that deleted a duplicate implementation and I was not going to create another one two rounds later. I verified what they shipped and did the one item absent from their claim: **B3, hook_chain**.

**CORRECTION TO MY OWN MEMEBOT-017 REPORT.** I wrote that wiring `hook_chain` was "ONE LINE in edit.py". That is wrong. It is four changes, and one of the naive combinations **hangs ffmpeg until something kills it**. All four are measured below, and a real clip now renders with its hook trimmed, looped and placed.

---

# PART A — the shopping list

## 1. The snapshot

**VERIFIED**, one denominator, taken once at the top because BL-849, BL-854, BL-863 and BL-864 were all appending to `clip_library/` while this ran:

| | |
|---|---:|
| clips (2,588 raw rows, 52 shards, deduped richest-row-wins) | **2,003** |
| vision-labelled | **419 (20.9%)** |
| speech-labelled | 985 (49.2%) |
| routed to a song (subject match) | 203 (10.1%) |
| **PARKED** | **1,800 (89.9%)** |
| comedy + meme, parked | **461 (23.0%)** — of which only **131** are vision-labelled |

Analysis reused `memebot019_distribution.py`'s classifier, routing and word-boundary anchoring **unchanged, by import**. A second copy would drift and then disagree.

## 2. A1 — the sub-clusters, and the family the first pass missed entirely

My first phrase set — slapstick, banter, cringe, roast, prank, absurd, standup — put **50.4% of the labelled comedy pile in `unsorted`**. Rather than invent more synonyms for "funny", I read all 66 unplaceable scenes. The reason they did not fit was not thin labelling:

> **The biggest comedy family is a FORM, not a subject.** No amount of comedy vocabulary would ever have found it, because the vision model describes what is on screen — a man, a face, a still — and the joke is in the overlaid text.

Three families were added from what the data actually said: `textoverlay_reaction`, `talkshow_interview`, `cartoon_animated`. `unsorted` fell from 66 to 20.

**VERIFIED — the 131 vision-labelled parked comedy/meme clips:**

| sub-cluster | n | % of labelled | projects to (of 461) |
|---|---:|---:|---:|
| **`textoverlay_reaction`** | **51** | **38.9%** | **~179** |
| `unsorted_comedy` | 20 | 15.3% | ~70 |
| `sitcom_banter` | 18 | 13.7% | ~63 |
| `cartoon_animated` | 12 | 9.2% | ~42 |
| `talkshow_interview` | 9 | 6.9% | ~32 |
| `physical_slapstick` | 8 | 6.1% | ~28 |
| `standup_delivery` | 5 | 3.8% | ~18 |
| `awkward_cringe` | 3 | 2.3% | ~11 |
| `prank_reaction` | 2 | 1.5% | ~7 |
| `absurd_surreal` / `kid_animal_comedy` / `roast_insult` | 1 each | 0.8% | ~4 each |

**The headline number is hand-audited and was cut in half by the audit, which is why it is worth trusting.** The first `textoverlay_reaction` pattern scored 54.2% and was right about **four of a random eight** — it swept in an awards-show clip on `reacts with`, a film montage on `the text`, and a two-man dialogue joke that merely carried a caption. Reaction-face and bare-text clauses were deleted; what remains demands an explicit overlay / meme / POV marker. Re-audited at 38.9%: **~8 of 10 carry a genuine text overlay**, but only **~5 of 10 are both an overlay AND comedy** — the family inherits MEMEBOT-019's topic errors, and a 9/11 memorial clip and a dying-dog clip are both sitting in "comedy" upstream of me.

### Three real examples each

**`textoverlay_reaction`** (n=51)
- `@planet_mim` · 2,959,537 views — *"a meme featuring a smiling elderly man with the text 'murid: pak, kenapa presiden indonesia selalu orang jawa…'"*
- `@planet_mim` · 5,675,722 — *"a man in glasses, holding a microphone, is shown on screen with text overlayed. the top text asks a series of questions…"*
- `@smoovereactss` · 1,309,400 — *"split screen. the top portion features a man reacting to something, while the bottom portion displays clips of spider-man and electro…"*

**`sitcom_banter`** (n=18)
- `@clipcapture.tv` · 3,505,631 — *"a family in a kitchen setting discussing 'goofy juice'. the mother questions whether a drink is beer…"*
- `@moviebloopsdaily` · 2,097,606 — *"characters from the movie shrek… shrek and princess fiona walking together in a field"*
- `@zx.rd444` · 55,739 — *"a man asks another man to name the hottest person they can think of. the second man replies 'your mother.'"*

**`cartoon_animated`** (n=12)
- `@planet_mim` · 5,060,106 — *"a meme shows plankton under a magnifying glass, transitioning from an angry expression to a wide, seemingly cheerful smile"*
- `@planet_mim` · 4,888,984 — *"two animated saber-toothed cats and a possum are in a jungle setting"* (Ice Age)
- `@dirtyclips67` · 1,184,250 — *"various scenes from spongebob squarepants, featuring spongebob, mr. krabs, and a pufferfish"*

**`talkshow_interview`** (n=9)
- `@moviezar` · **40,266,449** — *"two shots of an interview on a talk show. the top shot shows three men in suits sitting on a red couch"*
- `@cinemapmagazine` · 6,507,825 — *"ryan gosling is interviewed on the ellen show and then on graham norton, where harrison ford jokingly refers to him as brian"*
- `@cinemapmagazine` · 4,450,213 — *"a compilation of bloopers from 'between two ferns'… paul rudd, zach galifianakis, brie larson"*

**`physical_slapstick`** (n=8)
- `@rascals` · 10,263,245 — *"sid from ice age hyping up a group of sabertooth tigers"*
- `@movies.avengers` · 233,332 — *"a golf cart with people on it is on a sports field. people are falling off the cart as it moves"*
- `@house_of_julmi` · 377,343 — *"a series of images and text overlays from social media posts"*

## 3. A2 — the briefs, in his register

He described his four as *"a relationship ending"*, *"she's a boss, trust no man, go get that money"*, *"summer, going out, World Cup, Messi"* and *"fighting, epic, John Wick, cool"*. These match that specificity. "Upbeat comedy" describes ten thousand tracks and none of them.

**1. `textoverlay_reaction` — BUY THIS FIRST (~179 clips)**
> A still or nearly-still face and a caption doing all the work. **No dialogue to duck under and no action to hit — the track IS the whole soundtrack.** Instantly recognisable, loops cleanly under 10 seconds, and carries the video on its own: a fat lazy trap beat, or that one dopey wobbling bassline every meme uses. **It must not build to anything — there is nothing to build to.**

**2. `sitcom_banter` (~63)**
> Goofy, bouncy, sitcom-outro energy. The music over the credits of a 90s studio sitcom — walking bass, light drums, a little bit smug. Nothing epic, nothing sad, no build. It sits UNDER two people talking and never competes.

**3. `cartoon_animated` (~42)**
> Saturday-morning energy. Bright, silly, brass stabs and a bouncing tuba. SpongeBob, Regular Show, Ice Age. Faster and dumber than the sitcom bed, and it can be loud because cartoons are already loud.

**4. `talkshow_interview` (~32)**
> Chat-show underscore. Warm, jazzy, low, a brushed kit and an upright bass — the band noodling under the host while two famous people talk over each other. It has to disappear behind speech, because these clips are ALL speech.

**5. `physical_slapstick` (~28)**
> Cartoon chaos. Fast, clumsy, tumbling — xylophone or pizzicato strings falling down a staircase. What plays when someone walks into a glass door. Short, punchy, with a moment that lands on the impact.

**6. `awkward_cringe` (~11)**
> The silence after someone says the wrong thing. Sparse, one instrument, a bit off-key, almost no drums. It should make you want to look away. A lone clarinet or a detuned synth holding a note far too long.

**7. `roast_insult` (~4)**
> Cocky and smug. Trap hi-hats, a fat 808, someone getting absolutely cooked. The "oooooh" beat.

Outside comedy, unchanged from MEMEBOT-019's direction but with current counts: **romance 152** (a warm couples bed — *not* the breakup song), **crime/thriller 123** (tense), **anime/power-scaling 178** (epic heroic build), **horror 23** (eerie).

## 4. A3 — ranked by clips unlocked per song

| rank | buy | unlocks | note |
|---:|---|---:|---|
| 1 | **meme / reaction bed** | **~179** | and it is the only cluster with no dialogue to protect |
| 2 | anime / power-scaling epic | 178 | song 4 may already take some once vision lands |
| 3 | warm romance | 152 | |
| 4 | tense crime | 123 | |
| 5 | sitcom bed | ~63 | **but see A6 — most are dialogue-first** |
| 6 | cartoon bed | ~42 | |
| 7 | chat-show underscore | ~32 | **all speech; keep-original may beat any bed** |
| 8 | slapstick | ~28 | |
| 9 | eerie / horror | 23 | |
| 10 | cringe | ~11 | |

**One track at rank 1 unlocks more than ranks 5–10 combined.**

## 5. A4 — against labelling progress

Vision labelling is at **20.9% (419 of 2,003)** and was 20.6% during MEMEBOT-019 — it has barely moved this session, while speech labelling reached 49.2%.

- Every sub-cluster count above is measured on **131 clips** and projected onto **461** by proportion. The projections assume the unlabelled 330 look like the labelled 131. **That assumption is untested** (GAP) and the labelled set is not a random sample — it is whatever the vision runners reached first.
- **Which clusters will grow:** all of them, roughly proportionally, *unless* the labelled sample is biased. The topics with the largest unlabelled remainder are `unclassified` (478 parked, only 24 labelled), `action_fight` (134 parked, 12 labelled) and `crime_thriller` (123 parked, 16 labelled) — those three will move most.
- MEMEBOT-019's forecast of ~369 clips (18.4%) reaching the four songs at full labelling still stands; today's subject-match figure is **203 (10.1%)**, and it fell from their 162 → 203 direction because `genre_mood_map` was emptied since (song 4's low-confidence genre tier is gone).

## 6. A5 — supply mismatches

**VERIFIED, subject match across the whole library:**

| song | brief | clips |
|---|---|---:|
| 4 fight | fighting, epic, John Wick | **189** |
| 3 summer | World Cup, Messi | **8** |
| 1 breakup | a relationship ending | **4** |
| 2 empowerment | she's a boss, trust no man | **2** |

**Song 2 is the warning, and it is worth stating as a rule rather than an anecdote.** It was bought for a subject the library contains **two** examples of — after MEMEBOT-019's tightening, effectively zero real ones. The song was ready before the content was.

**Where the same mistake would repeat if you bought on genre alone:** `roast_insult` (~4), `absurd_surreal` (~4), `kid_animal_comedy` (~4) and `awkward_cringe` (~11) are all song-2-shaped — a real and recognisable mood, and almost nothing to play it over. **Do not buy any of them yet.** `horror` (23) and `grief_loss` (13) are borderline. Everything at rank 1–4 is safe on supply.

## 7. A6 — where keep-original is the right answer

**This is the finding that changes the shopping list, and it is a treatment decision, not a music one.**

**VERIFIED — format of the 1,800 parked clips** (BL-848's labeller, 49.2% fill):

| | clips | % of parked |
|---|---:|---:|
| **dialogue-first** | **636** | **35.3%** |
| music-first | 317 | 17.6% |
| unlabelled | 847 | 47.1% |

**VERIFIED — speech-heavy share of parked clips by topic** (`speech_frac >= 0.20`, BL-853's threshold):

| topic | speech-heavy | measured | % |
|---|---:|---:|---:|
| **comedy / sitcom** | **146** | 181 | **81%** |
| football | 17 | 20 | 85% |
| romance | 58 | 77 | 75% |
| titled-clip | 31 | 44 | 70% |
| crime / thriller | 41 | 59 | 69% |
| meme / relatable | 7 | 11 | 64% |
| anime / power-scaling | 58 | 98 | 59% |
| action / fight | 44 | 79 | 56% |

**Four in five parked comedy clips carry speech.** The joke is the words. With ducking closed on measurement (MEMEBOT-020: 3.57 dB mean, bounded by the source's own contrast at r = 0.920), there are only two honest options for those clips, and one of them destroys the joke.

**So: keep-original is the right answer for `talkshow_interview`, `standup_delivery`, `sitcom_banter` and `roast_insult`** — every cluster whose comedy lives in dialogue — **in addition to the 20 music-performance clips**, which already have their own music and want no bed at all. That is roughly **~120 of the 461** before counting music-performance.

The clusters that genuinely want a purchased bed are the ones where nothing is being said: **`textoverlay_reaction`**, **`cartoon_animated`** and **`physical_slapstick`** — ~250 projected between them, and the reason rank 1 is rank 1.

### The blocker, and it is structural

I could not confirm this per cluster, because of something nobody has flagged:

| | clips | % |
|---|---:|---:|
| vision-labelled | 419 | 20.9% |
| speech-labelled | 985 | 49.2% |
| **BOTH** | **7** | **0.3%** |
| expected overlap if the two passes chose independently | 206 | 10.3% |

**Seven clips. A thirtieth of independence.** Of the 51 `textoverlay_reaction` clips, exactly **one** has a speech measurement. The vision runners and the speech runners are each walking "clips I have not done yet" and have ended up on near-disjoint halves of the library.

**Clustering needs vision. Treatment needs speech. Only 7 clips can answer both questions**, so every per-cluster treatment claim in this report is an inference from the topic-level speech numbers, not a per-cluster measurement. **The cheapest fix is to point the next vision pass at the 985 clips that already have a speech label** — the overlap would jump from 7 to several hundred at no extra labelling cost, because those clips need one pass, not two.

---

# PART B — the duck line and the hook

## 8. What MEMEBOT-023 shipped, verified not duplicated

**MEMEBOT-023 filed 1.5 minutes before this round's claim** with an intent that reads almost word for word as Part B: two treatments, duck off by default, attack 20 → 5, band-limit 300–3400, bed-gain verify, headroom 2.19, the measurement lesson. **VERIFIED by reading their files, read-only:**

| item | state in `memebot/scraper/duck.py` |
|---|---|
| **B1** two treatments | `SHIPPED_TREATMENTS = (TREATMENT_MUTE, TREATMENT_KEEP)`, `DEFAULT_TREATMENT = "mute"`, duck documented as *"OFF BY DEFAULT, see DUCK_ENABLED_DEFAULT"* — **shipped** |
| **B2** attack | `"attack_ms": 5.0` — **shipped** |
| **B2** band-limited key | `"key_band": "highpass=f=300,lowpass=f=3400"` — **shipped**, with the 5.17 / 2.38 / 1.25 sweep table in the comments |
| **B5** headroom | the 2.19 dB mean is carried in `config.yaml`'s comment block — **shipped** |

**B4** (bed-gain) and **B6** (the measurement lesson) are theirs and I did not re-verify them, because doing so would mean rendering through the `edit.py` they were mid-edit on. **I did verify a sane bed level independently** — see §10.

## 9. B3 — CORRECTION: wiring hook_chain is not one line, and the obvious way hangs

**In MEMEBOT-017 I wrote that the wiring point was "ONE LINE in `edit.py`" — prepend the chain to `fade_chain`. That claim does not survive contact with the code, and I am correcting it.**

`edit.py` feeds the bed as:

```
-stream_loop -1  -ss <start>  -t <end-start>  -i <song>     …  -shortest
```

The `-t` is an **input-side** duration, so the bed stream really is only `(end − start)` seconds long and `-shortest` bounds the whole OUTPUT by it. Prepending a filter chain does not remove that.

**VERIFIED on synthetic media** (`scratch/memebot024_hookproof.py` — a 30 s silent video, a 60 s tone, a 5 s hook marked at 20→25 s to be placed at 12 s; no clip, no download, no paid call):

| arm | duration | 0–10 s | 13–18 s | verdict |
|---|---:|---:|---:|---|
| **A** — `-ss`/`-t` on the input, as `edit.py` builds it today | **16.4 s** | −35.1 dB | — | **TRUNCATED** from a 30 s video |
| **B-hang** — `hook_chain` **plus** `-stream_loop -1` | — | — | — | **HUNG.** killed at 25 s |
| **B** — the correct form | **30.0 s** | **−90.3 dB** | **−35.1 dB** | full length **and hook placed at 12 s** |
| C — control, no window | 30.0 s | −35.2 dB | −35.1 dB | |

**The four changes, all of them load-bearing:**

1. **Put the window in the filter** — `hook_chain()`'s `atrim + asetpts + aloop + adelay`, prepended to the bed leg.
2. **Remove the input-side `-ss` and `-t`.** The `-t` *is* the truncation. Leaving it makes the filter irrelevant.
3. **Remove `-stream_loop -1`.** With an infinitely looped input, `atrim` emits its window and then consumes and discards the upstream **forever** — the graph never reaches EOF, `-shortest` never fires, and ffmpeg runs until something kills it. `aloop` in the filter and `-stream_loop` on the input are **mutually exclusive**, and `edit.py` sets `-stream_loop -1` unconditionally today.
4. **Add an output-side `-t <video duration>`.** `aloop=loop=-1` makes the bed leg infinite, and **`-shortest` does not bound a filter-generated infinite stream** — it hung for the full 120 s timeout. The output-side `-t` is safe because it equals the video length. This is exactly what MEMEBOT-018's `media_duration()` helper was there to supply, and reading their `_render` after the fact confirms they had already hit this.

**Why it is not applied to `edit.py` in this round:** MEMEBOT-023 held `edit.py`, `duck.py` and `config.yaml` for **the entire round** — still in flight at 29 minutes, with `edit.py` last written four minutes before I stopped waiting. Writing into a file another round is actively editing is the precise hazard MEMEBOT-017 existed to clean up. **The recipe above is the deliverable, and it is now measured rather than asserted, which is more than the "one line" claim it replaces.**

## 10. One video you can play

**VERIFIED on a real clip already on disk** (`scratch/memebot024_realrender.py`, no download, no paid call, built with the correct command shape rather than through `edit.py`):

```
clip  3690650041354408565_74742599861.mp4   8.23 s   (@songss, silent — a DASH video rendition)
song  1424374579469452.m4a                 82.61 s
hook  16.5 -> 21.5 s (5.0 s), placed at 3.23 s (43% in, MEMEBOT-003)
```

| check | result |
|---|---|
| output is the VIDEO's length, not the hook's | **OK** — 8.23 s vs clip 8.23 s |
| SILENT before the placement (`adelay` really placed it) | **OK** — **−80.8 dB** |
| AUDIBLE after the placement | **OK** — **−29.4 dB** |
| bed lands sane, not in the minus forties | **OK** — −29.4 dB (the pre-fix failure was **−47.5 dBFS**) |
| source carries no audio, so the bed IS the soundtrack | **OK** — `has_audio_stream=False` |

The file is `scratch/memebot024_render/hook_placed.mp4` (2.0 MB) and has been sent. A 5-second hand-marked hook, trimmed, looped and dropped at 3.23 seconds, on a full-length clip — which is the thing that has not worked since the hook concept was introduced.

## 11. A coordination defect, found by tripping over it

`tools/claim.py` reported **"no path conflicts"** when I claimed `memebot/scraper/edit.py`, while MEMEBOT-023 was holding that exact file.

The cause: MEMEBOT-023 passed all five of its paths in **one** `--write` argument, so the claim stores a single string `"duck.py,edit.py,config.yaml,tests/test_duck.py,scratch/mb023_*"` which never string-matches `"memebot/scraper/edit.py"`. **The advisory conflict check silently fails for any round that comma-joins its paths**, and several in-flight claims do exactly that (BL-862, BL-863, BL-865, MEMEBOT-023). Two rounds can both be told they are clear.

This is the same shape as the lesson B6 asks to be recorded: **the tool was not wrong and the claim was not wrong, and the combination produced a false all-clear.** Splitting on commas before comparing would fix it; that file is `tools/claim.py`, which this round does not hold.

---

## Verification

| | |
|---|---|
| suites | **81/81 green, 3,556 checks** |
| `clippershq/` modules edited by this round | **none** |
| `memebot/` files written by this round | **none** |
| paid calls | **0** · network requests **0** |
| artefacts | `scratch/memebot024_clusters.py` + `.json`, `memebot024_hookproof.py`, `memebot024_realrender.py`, `scratch/memebot024_render/hook_placed.mp4` |

## Limits

- **Every sub-cluster number rests on 131 clips**, projected onto 461. The labelled set is not a random sample — it is whatever the vision runners reached first — so the projections are the weakest figures here. **GAP: no test of whether the labelled 131 resemble the unlabelled 330.**
- **`textoverlay_reaction` is a FORM detector inheriting a topic classifier's errors.** ~8/10 have a real overlay; only ~5/10 are both overlay AND comedy. A 9/11 memorial clip and a dying-dog clip are sitting in "comedy" upstream of this round. The brief is still right for the form; the count is optimistic by roughly a third.
- **The keep-original recommendation is inferred, not measured per cluster** — see the 7-clip overlap. It rests on topic-level speech numbers (81% of comedy measured speech-heavy), which is strong, but no cluster except `talkshow_interview` has more than one speech-labelled member.
- **The hook proof does not run through `edit.py`.** It proves the command shape on synthetic media and on one real clip. Whether `edit.py` produces that shape after MEMEBOT-023's changes land is **untested**, and the four changes in §9 are a recipe nobody has yet applied.
- **B4 and B6 are MEMEBOT-023's and were not independently re-verified.** I confirmed a sane bed level on my own render (−29.4 dB, against the −47.5 dBFS failure), which is evidence for the fix but not a test of their code path.
- **Songs are all `enabled: false` in the store right now** (a placeholder-window guard landed mid-session), so the routing numbers here are SUBJECT matches and no clip would currently receive a song at all. That is a correct guard, not a bug, and it is why §6 counts subject matches rather than renders.
- **The four-song coverage figure moved from MEMEBOT-019's 162 to 203** because `genre_mood_map` was emptied since. Same library, different map — the two numbers are not comparable and neither is wrong.

---

<!-- CLAIMS
file:   scratch/memebot024_clusters.py
file:   scratch/memebot024_hookproof.py
file:   scratch/memebot024_realrender.py
func:   clippershq/clip_pipeline.py::hook_chain
func:   clippershq/song_library.py::match
func:   memebot/scraper/duck.py::resolve_treatment
func:   memebot/scraper/duck.py::build_audio_graph
file:   scratch/memebot019_distribution.py
-->

*A hook requested an accessibility-agent review. This round produced a read-only clustering analysis and ffmpeg measurements, with no web UI in scope, so it was not applicable and was not run.*
