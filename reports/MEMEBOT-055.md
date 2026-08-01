# MEMEBOT-055 — the valence map would take park to 1.9%, and that is the argument against filling it

READ-ONLY on the matcher. `scratch/songs.json`, `song_library.py` and `clip_library.py` were
not written. No paid calls. Every library figure read through a frozen snapshot — thirteen
rounds are in flight and three of them are writing `clip_library/`.

Registry read with `tools/claims_read.py` as instructed: **13 live claims**. One advisory
accepted — BL-895 claims `scratch/` broadly; my files are `scratch/mb055_*`.

The full operator-facing proposal is `scratch/mb055_proposal.md`. This is the measurement
behind it.

---

## 1. THE VALENCE MAP — counts first

| valence | clips | % library | parked today | accounts | top account share |
|---|---:|---:|---:|---:|---:|
| positive | 866 | 43.2% | 752 | 135 | 7% |
| neutral | 680 | 33.9% | 601 | 135 | 3% |
| negative | 418 | 20.9% | 326 | 109 | 11% |
| *(absent)* | 39 | 1.9% | 38 | 11 | — |

**1,679 parked clips carry a valence value — 83.8% of the library.** That is the most a
complete valence map could reach.

**No concentration problem**, unlike genre: 109–135 accounts per value, top account 3–11%.

### Proposed mapping

```json
"valence_mood_map": { "positive": "hype", "neutral": "warm", "negative": "melancholy" }
```

Three real examples per value are in the proposal. Only four moods are routable at all —
your songs carry **hype, melancholy, triumphant, warm**; the vocabulary also lists **eerie,
goofy, tense**, which have no song.

---

## 2. THE CEILING — and the correction that makes it meaningful

Simulated against the real matcher on a copy of the store:

| scenario | clips with a song | unusable |
|---|---:|---:|
| today | 286 | **85.7%** |
| + valence map (3 entries) | **1,965** | **1.9%** |
| + genre map only (25 entries) | 557 | 72.2% |
| + both maps | 1,965 | 1.9% |
| + both + a house set | 2,003 | 0.0% |
| + valence map pointing at moods with **no song** | 286 | 85.7% |

That last row is the control, and it is why the table can be trusted.

**My first version of this measurement was wrong and would have been believed.** It counted
`match()` tiers, and reported an identical **1.9%** for a map pointing at moods that have a
song and one pointing only at moods that do not. `match()` answers *"which rule fired"* from
the map lookup; `pick()` is what enforces that an enabled song actually carries that mood.
**A tier is not a song.** Reading one as the other makes an empty song library look fully
covered. The table above calls `render_plan()` and counts a clip only when a `song_id` comes
back — and the control row now correctly reads 286, identical to today.

### Reconciling with MEMEBOT-032's 19.5%

The brief asked whether filling the maps only moves 86.2% → 80%. It does not — it moves it to
**1.9%**. But that number and MEMEBOT-032's ceiling are not in conflict, because they answer
different questions:

> **1.9% park** — how many clips *get* a song.
> **19.5%** — how many get the *right* one.

Filling valence closes the first gap and leaves the second exactly where it was.

---

## 3. WHY I AM NOT RECOMMENDING THE OBVIOUS MAPPING

Three values spread over four songs is **~491 clips per song**, assigned on a signal with the
resolution of positive / neutral / negative.

That converts a **visible** failure — clips park, nothing renders — into an **invisible** one:
everything renders, and four-fifths of it carries music chosen by a three-way flag.
MEMEBOT-019 deleted the old fallback for precisely this reason (*"it produced a breakup ballad
over a football clip"*), and a blunt valence map rebuilds it under a different name. The park
rate would look solved on every dashboard.

**The least-bad version, if you want it:** fill `negative → melancholy` only. 326 parked
clips, the tightest of the three, one entry, reversible, and you can hear the result before
deciding about the other two.

---

## 4. THE GENRE MAP — two corrections to the brief

**Fill is 17.7%, not 28%** — 355 of 2,003 clips.

**BL-847's "70.8% from two accounts" no longer holds library-wide.** Only **5 of 25** values
exceed it, and four of those five have ≤29 clips. The nine largest genres run top‑2 of
29–46%, across 14–26 accounts each. The warning now applies to **`satire` (79%),
`dark-comedy` (76%) and `sci-fi` (64%)** specifically — three values to map last or not at
all — rather than to the genre signal as a whole.

**The binding limit is coverage, not concentration: 84.2% of parked clips carry no genre.**
A complete 25-entry genre map reaches 621 clips and moves park 85.7% → **72.2%**. It is a
sixth of the problem at eight times the number of decisions.

---

## 5. WHERE THE HEADROOM ACTUALLY IS

**98.7% of parked clips already carry a vision label.** Only **1.0%** have neither genre nor
vision.

The parked pile is not short of signal. The four vision rules are each written for one song's
subject and deliberately narrow — the store's own note says *"a sad clip about a dead dog must
NOT get this song"* — so they convert 267 clips out of 1,695 that carry vision text. That
precision is a feature; it is also the whole gap.

So the ranking that matters is songs:

| buy a song for | parked clips unlocked (via genre) | % of parked |
|---|---:|---:|
| **goofy** — comedy / sitcom / satire / family | **151** | 8.8% |
| **eerie** — horror / sci-fi / fantasy / mystery | 91 | 5.3% |
| **tense** — thriller / crime / mystery / war | 68 | 4.0% |

**Buy goofy first.** Comedy (105 parked) and sitcom (50 parked) are the two largest parked
genres and there is no song a comedy clip can route to today except by calling it *warm*.

These are floors — counted via genre, which covers only 15.8% of the parked pile. With a
vision rule written for the new song, each would reach considerably further into the 98.7%
that carry vision labels.

---

## PROOF

| Required | Result |
|---|---|
| Valence proposal with counts | 3 values, 866 / 680 / 418, 83.8% of library parked-and-routable |
| Genre with counts and account spread | 27 values, 17.7% fill, 5 flagged concentrated |
| Three real examples per entry | in `scratch/mb055_proposal.md` |
| Projected park-rate change | 85.7% → **1.9%** (valence), → 72.2% (genre only) |
| Ceiling reported honestly | 1.9% *matched* vs MEMEBOT-032's 19.5% *correct* — reconciled, not conflated |
| Missing songs ranked | goofy 151 > eerie 91 > tense 68 parked clips |
| Live maps not written | `scratch/songs.json` untouched; simulated on deep copies |

---

### Method / limits

- The mood assignments in the proposal are **illustrative groupings for costing**, not
  recommendations. Which feeling a genre carries is the operator's call, and this round does
  not make it.
- The ceiling simulation uses one plausible genre→mood grouping. A different grouping changes
  *which* song a clip gets, not how many clips get one, so the park-rate figures hold; the
  precision figures would move.
- `render_plan(count=False)` was used so the simulation cannot mutate rotation counters. On a
  store copy regardless.
- The song-unlock counts are **via `content_genre` only**. They are floors, not estimates of
  what a new song plus a vision rule would actually reach.
- MEMEBOT-032's 19.5% is quoted from that report, not re-measured here.
