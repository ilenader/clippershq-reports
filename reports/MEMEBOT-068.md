# MEMEBOT-068 — The comedy and meme song routes: a ranked shopping list

**Round:** MEMEBOT-068 · **Date:** 2026-08-02 · **Paid calls:** none
**Status:** PROPOSAL. Read-only on the matcher and on `scratch/songs.json`. Nothing here is installed.

---

## THE SHOPPING LIST

Ranked by **clips unlocked per song bought**, measured — not by cluster size. Each row is the
*marginal* gain given everything above it, because `_vision_match` is first-hit-wins and two
overlapping rules cannot both be paid for the overlap.

| # | Song | Brief (buy this) | Unlocked | Park after | Drop-in? |
|---|------|------------------|---------:|-----------:|----------|
| 1 | **A — the meme song** | *"The caption is the joke. Bouncy, dumb, loopable — the sound that makes a still face funny. Sitcom-outro energy, a bassline that struts. Nothing sincere."* | **+129** | 79.3% | ✅ yes |
| 2 | **F — the wholesome song** | *"Dad meets the baby. The dog comes home. Soft guitar or piano, no drums, sounds like a memory you're already nostalgic for."* | **+40** | 77.3% | needs 1 token |
| 3 | **D — the grief song** | *"Someone's gone. Slow piano, lots of air, no beat. Not a breakup — a funeral. The song you'd hear over a hospital corridor."* | **+35** | 75.5% | needs 1 token |
| 4 | **C — the pressure song** | *"Someone is about to get caught. Ticking clock, tight low strings, builds and never releases. Interrogation room, not a fight."* | **+29** | 74.1% | ✅ yes |
| 5 | **E — the money song** | *"Slow-motion walk into the room and everyone looks. Expensive, smug, unbothered. Red carpet, not the match."* | **+29** | 72.6% | needs 1 token |
| 6 | **B — the horror song** | *"Something is wrong in this house. Creeping, high strings, silence that gets louder. The bit before it happens, not the jump."* | **+18** | 71.7% | ✅ yes |

**Buy A first and it is not close.** It alone is 129 of the 280 clips on this entire list —
more than the other five combined. It is also drop-in.

---

## THE CEILING, PER PURCHASE

| After buying | Matched | % of labelled | Park |
|---|---:|---:|---:|
| *(today — 4 songs)* | 286 | 14.4% | **85.7%** |
| + A meme | 415 | 20.9% | 79.3% |
| + F wholesome | 455 | 22.9% | 77.3% |
| + D grief | 490 | 24.7% | 75.5% |
| + C pressure | 519 | 26.1% | 74.1% |
| + E money | 548 | 27.6% | 72.6% |
| + B horror | **566** | **28.5%** | **71.7%** |

Corpus: 2,003 rows, 1,985 vision-labelled (99.1%). Today's 286 matches reconcile exactly with
the briefed figure; the 14.4% vs the briefed 13.2% is the same numerator over a larger
labelled denominator, as the library has grown.

**Six songs roughly double the reach and still leave 71.7% parked.** That is the honest
shape of this: the park is a long tail, not a few big blocks. Nobody buys their way to a
mostly-unparked library.

---

## WHAT THE PARK ACTUALLY CONTAINS

1,699 parked clips carry vision text. Clustered on `vision_text` — the *same* string the
matcher reads — because a cluster measured on a richer signal is a cluster whose count
evaporates the day someone writes the rule.

| Cluster | Clips | Song? |
|---|---:|---|
| *(unclustered)* | 212 | — |
| **textoverlay_reaction** (form) | 177 | → **A** |
| superhero_comic | 163 | ✗ see below |
| family_parenting | 143 | → F |
| distress_grief | 132 | → D |
| music_performance | 113 | ✗ see below |
| celebrity_press | 102 | → E |
| captioned_other | 96 | partly A |
| comedy_residual | 77 | partly A |
| crime_police | 75 | → C |
| animation_cartoon | 74 | — |
| food_cooking | 56 | — |
| cars_driving | 52 | — |
| horror_supernatural | 51 | → B |
| workplace_school | 49 | — |
| romance | 46 | — |
| animals_pets | 33 | → F |
| sitcom_series | 19 | — |
| sports_nonfootball | 18 | — |
| no_vision_text | 18 | unreachable |
| scifi_space | 11 | — |

`textoverlay_reaction` lands at **177** against the briefed ~179 — an independent
reconstruction of that cluster agreeing to within two clips.

### The two clusters that look big and are not purchases

**superhero_comic — 163 clips, and I propose no song for it.** Of 180 park hits on superhero
vocabulary, only **18 are action-bearing**. The fight scenes are not here; song 4 already took
them. What is parked is *fandom talk* — unboxing a Captain America shield, fan-art
compilations, casting-discourse commentary, a narrator explaining the Red Goblin's origin.
Those want a voice, not a drop. Buying an "epic superhero" song would buy 18 clips.

**music_performance — 113 clips.** These clips already have music in them. Scoring a stage
performance with a different track fights the source audio. Flagged, not proposed.

---

## THE VISION RULES

Written in the store's exact `vision_rules` schema, in `scratch/memebot068_rules.py`. All six
are plain-phrase only — `validate()` rejects any phrase containing `()[]|\*+?^$`, because
those are phrases, not patterns, and a stray regex character is silently escaped rather than
honoured. Each carries an `excludes_any` built from false friends **observed in this corpus**,
not imagined.

**The form rule is the interesting one.** `textoverlay_reaction` is a FORM — a near-still face
with a caption doing the joke — and a form is a *conjunction*, which `strong` cannot express.
The engine already has the mechanism: `requires_any` is a hard gate and `weak` needs TWO
distinct phrases. So the caption markers go in `requires_any` (no caption, no fire) and the
reaction markers go in `weak` (two distinct ones needed). The conjunction falls out of the
engine's own semantics — no new code path.

Spot-check of rule A's 129 clips: 102 fire on `strong`, 27 on a weak pair; 13 of 14 sampled
are unambiguously caption-driven memes. That is a **spot-check, not a hand-labelled
precision measurement**, and MEMEBOT-032's 57%-false-alarm figure for `pov:`/`when you` does
**not** transfer here — it was measured answering *"is this comedic?"*, where those phrases
were a proxy. Here they are the subject itself. Sample 20 by hand before paying for the song.

---

## THE MOOD-TOKEN CEILING — read before buying song #2

`mood_vocabulary` holds seven tokens. Four are spoken for: `melancholy`=song 1, `triumphant`=2,
`warm`=3, `hype`=4. **Three are free** — `goofy`, `eerie`, `tense` — which is exactly why A, C
and B are drop-in and F, D, E are not.

This is not cosmetic. `pick(store, mood)` finds a song **by mood token**:

> A "sad but not a breakup" rule cannot reuse `melancholy`, because `melancholy` **is** the
> breakup song. Every grief clip it matched would be handed the breakup ballad — the exact
> failure the brief forbids, arriving *silently*, because `pick()` would succeed.

F, D and E each need **one new token** added to `mood_vocabulary` in the *same edit* as the
song, or `validate()` will correctly refuse the rule. Suggested: `tender`, `sombre`, `lavish`.

A rule whose mood has no enabled song parks every clip it matches. Install a rule only
together with the song it routes to.

---

## THE VALENCE MAP — do not fill it, and here is the measurement

The brief's figures reproduce exactly: the full map takes park from 85.7% to **1.9%**. Two
things that number hides:

**Song 2 gets nothing.** Under the full map the split is `hype` 850, `warm` 786, `melancholy`
329, **`triumphant` 0**. It does not spread 1,965 clips over four songs — it dumps **850 clips
(42% of the corpus) onto the fast aggressive fighting song** on the strength of a `neutral`
label, and leaves the female-rap anthem at zero.

**And `negative -> melancholy` alone is worse than it looks.** It is 326 clips, one reversible
entry, as briefed — but `melancholy` **is song 1, the breakup ballad**. That entry routes 326
clips onto the breakup song on a bare negative-sentiment signal. It is the dead-dog case,
industrialised.

The safe version is `negative -> sombre` **after** buying song D. I measured that too, and it
still fails. It adds 298 clips *that D's rule had already seen and rejected* — and **19% of
them (58 clips) carry an explicit comedy or meme marker**. Concretely, the grief piano would
be placed over:

- *"farting into grandma's oxygen machine"*
- a karaoke clip in a dimly lit room
- a cartoon character whose ears wiggle at the end
- an office comedy scene

That is a measured 1-in-5 visible mismatch, and the remaining 4-in-5 were rejected by a rule
built to find exactly this content — so they are not endorsements, they are unknowns.

**Recommendation: fill no valence entry, including the single one.** The park is a visible,
countable failure. This trades it for an invisible one.

---

## GOTCHA — `_RULE_CACHE` is unsound for measurement harnesses

`song_library._RULE_CACHE` is keyed on `(id(rule), idx)`. That is fine in production, where
the store loads once and rule dicts live as long as the process. It is **not** fine in an A/B
harness that builds a trial store, measures it, and discards it: the freed dicts' addresses
are handed straight back to the next `deepcopy`, and a later rule collides with an earlier
rule's cache entry and is matched **with somebody else's compiled regexes**.

It was caught by an invariant, not by reading code. Under first-hit-wins a rule's marginal
gain can only *shrink* as rules are installed above it. The uncorrupted run had
`B_eerie_horror`'s gain **grow from 19 to 47** between rounds while `C_tense_crime` collapsed
to 0 — B was matching C's crime phrases.

**The part worth remembering:** the corrupted run and the clean run reach the **same final
total, 566**. The bug was invisible in the headline number and wrong only in the per-song
attribution — which was the entire deliverable. The first ranking I produced was
A, B, C, D, E, F; the true one is A, F, D, C, E, B. A total that reconciles is not evidence
that the breakdown does.

`measure()` now clears the cache on entry and asserts monotonicity every round.

---

## GOTCHA — `claim.py` will hand you an id that already has a published report

This round was filed as **MEMEBOT-058** and got a clean `"no path conflicts"`. That id already
has a published report on origin — an unrelated governance audit from 2026-08-01, landed under
BL-956's commit. `claim.py` did not warn, and it is not wrong to: it checks *in-flight* claims,
and that round had long since ended.

So the live claim registry and the published-report namespace are **two different namespaces**,
and only one of them is checked when an id is chosen. The collision surfaced only because
`publish_report.py` refuses on `exists_on_remote` — the last gate before the overwrite that has
already destroyed four reports here (BL-649, BL-675, BL-677, MEMEBOT-055).

Re-filed as **MEMEBOT-068** (first id free in both namespaces; origin reaches MEMEBOT-064,
local claims MEMEBOT-067) and every artefact renamed to match. **Check `git ls-tree origin/main
reports/<id>.md` when you pick a round id, not when you publish.**

---

## VERIFICATION

- **Order-independence asserted:** with all six candidate rules installed, **0** clips lost
  the song they have today. New rules append after the existing four, and first-hit-wins means
  they can only ever see what those four rejected. No purchase can disturb the current 286.
- Corpus read through `clip_pipeline.dict_of`, never off raw rows (MEMEBOT-043).
- Nothing written to `scratch/songs.json`, the live maps, or the matcher.

## FILES

| Path | What |
|---|---|
| `scratch/memebot068_cluster.py` | the clustering pass |
| `scratch/memebot068_clusters.json` | cluster counts, samples, members |
| `scratch/memebot068_rules.py` | the six drop-in rules |
| `scratch/memebot068_ceiling.py` | greedy marginal ranking + assertions |
| `scratch/memebot068_ceiling.json` | the ranked numbers |

## IF YOU ONLY DO ONE THING

Buy the meme song. It is +129 clips, it is drop-in against the free `goofy` token, and the
cluster behind it was found by matching the *shape* of a description rather than any comedy
vocabulary — which is why every previous round looking for "comedy" walked straight past it.
