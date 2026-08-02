# MEMEBOT-109 — one marker out, nineteen clips back, sixteen of them right

**Brief:** remove the single marker carrying 100% of the comedy-register exclusion's cost;
keep the other nine; account per clip in four buckets; verify the ten wrongly-parked clips
return; hand-audit anything whose song changes; re-state the matcher numbers for Group B.

**The marker is `reacting to`.** MEMEBOT-104's audit: 24 fires, 14 RIGHT, **10 WRONG —
every wrong displacement in the whole change**, 58.3% precision. The other nine are 9/9.

**Removed, with this brief recorded as consent inside the rule.** Suites green, config
valid, campaigns unchanged. **$0.00, no paid calls.**

**The one number that matters: 19 clips returned, not 10** — and I hand-audited all
nineteen: **16 RIGHT, 3 WRONG.**

---

## Gate

```
git status --porcelain -- scratch/songs.json clippershq/song_library.py   -> clean
claims_read --holders  scratch/songs.json          -> FREE
                       clippershq/song_library.py  -> FREE   (BL-999 live, holds neither)
```

Both stop conditions checked and clear. `clippershq/song_library.py` was never written —
the marker lives in the operator's `scratch/songs.json`, in the hype rule's `excludes_any`.

---

## 1–2. The marker, named and removed

```
hype rule excludes_any:  20 markers -> 19
removed:                 "reacting to"
kept (the sibling):      "reaction video"   <- a DIFFERENT marker, one of the six that never fired
```

The consent is recorded inside `_why_register_excludes`, appended to MEMEBOT-104's own note
rather than replacing it, so the rule now carries both decisions and the evidence for each.

**Not narrowed — removed.** MEMEBOT-104 proposed narrowing this marker and explicitly did
not apply it, because narrowing was not what had been consented to. The same reasoning runs
here in the other direction: removal is what this brief consented to, so removal is what was
done, and the narrowing stays available to a round that is given consent for it.

---

## 3. Four buckets, per clip, summing to the library

| bucket | count |
|---|---:|
| **KEPT** state unchanged | 2,642 |
| **MOVED** different mood | 1 |
| **PARKED** matched → nothing | **0** |
| **GAINED** nothing → matched | 18 |
| **TOTAL** | **2,661** = library ✓ |

The one MOVED clip is MEMEBOT-104's move running backwards:
`3947016901880248224_4043186953`, **melancholy → hype** — the O.K. Corral gunfight from
*Tombstone*. 104 recorded it going hype → melancholy via `track_title` when the marker
displaced it; removing the marker returns it.

**My first version of these buckets did not sum** — it required a clip to be matched in
*both* snapshots to count as KEPT, so the 2,188 clips parked before *and* after landed in no
bucket at all and the four totalled 473 against a library of 2,661. Four buckets that do not
sum are not an accounting. KEPT now means *state unchanged*, which includes staying parked.

---

## The correction the brief needs: it is 19, not 10

The brief says *"the ten wrongly-parked clips should return to hype; verify each by id."*
**Nineteen returned.** That is not a defect — it is what removing a 24-fire marker does. The
ten WRONG were never a separable population; they were 10 of the 24 clips this marker
displaced, and dropping it gives back all of them that no *other* marker also catches.

```
24  clips 'reacting to' displaced   (MEMEBOT-104)
-5  also caught by one of the nine markers that stay  -> remain parked
19  returned  (18 GAINED + 1 MOVED)
```

The nine surviving markers independently hold five of the twenty-four. That is the clearest
evidence in this round that keeping them was right.

---

## 4. Hand-audit of all nineteen — definition stated first

> **RIGHT** — the clip's own vision/caption text describes **action happening on screen**
> (a fight, a chase, a stunt, a match). Hype is about the footage.
> **WRONG** — the text describes **someone talking about** something: a reaction, a
> commentary, a face-cam over gameplay. The action words are in the *subject*, not the
> *footage*.

**16 RIGHT / 3 WRONG.** The three:

| clip | why it should have stayed parked |
|---|---|
| `3425885556908830479_971774209` | *"A man is shown **reacting to** a video montage"* — a reaction video, exactly what the marker was for |
| `3397600688332666046_971774209` | *"split-screen… man playing a video game on the bottom and himself on the top… **reacting to** the gameplay"* — face-cam over gameplay |
| `3931285888038729468_15165051384` | Bowser and Bowser Jr. in a dimly lit room; a caged Lumalee *speaks*. Dialogue, no action |

The sixteen RIGHT are unambiguous footage: an energy attack in *Regular Show*, Darkseid's
armies, *The Flash* vehicle chase with explosions, Kung Fu Panda combat, a warehouse fight
sequence, Cyclops' optic blasts, Lego Batman action, Galactus subdued by Ghost Rider,
Jackie Chan's kitchen chaos, Doctor Strange's magic duel, the O.K. Corral gunfight.

**The trade, stated plainly.** Before: 10 clips wrongly parked. After: 3 clips wrongly
matched to hype. **Net −7 wrong**, and the direction of the remaining error changed from
"a good clip gets no song" to "a talking-head clip gets a hype song" — which is the cheaper
failure, because a parked clip produces nothing at all.

---

## 5. Matcher numbers after — for the Group B audit

| | before | after |
|---|---:|---:|
| library | 2,661 | 2,661 |
| **matched** | 455 (17.1%) | **473 (17.8%)** |
| **park %** | 82.9% | **82.2%** |
| hype | 268 | **287** (+19) |
| melancholy | 78 | 77 (−1) |
| warm | 96 | 96 |
| triumphant | 13 | 13 |

> **Group B: measure THIS state, not MEMEBOT-104's.** 104 published 448 matched / 16.8% /
> hype 262. This round's baseline reads 455 / 17.1% / hype 268 *before* my change — the
> library moved underneath us (BL-979 was writing `clip_library/` during the same window),
> so 104's figures are a snapshot of a smaller library, not a disagreement. **473 / 17.8% /
> hype 287 is the final state.**

---

## 6. Suites, against the applied store

| suite | result |
|---|---|
| `test_comedy_register` | **11 OK** (was 9, +2) |
| `test_song_library` | ALL PASS |
| `test_track_title_tier` | 15 OK (1 skipped) |
| `test_matcher_boundary` | 9 OK |
| `test_config_contract` | ALL OK |
| `test_governance_rules` | 25 OK — campaigns fingerprints unchanged |

`test_comedy_register` **went red first, and it was right to.**
`test_every_proposed_marker_is_on_the_hype_rule` pins MEMEBOT-104's ten-marker state, so
removing one broke it — that is the guard doing its job. It was **narrowed, not loosened**:
it still asserts every other proposed marker is live, and it now also asserts the removed one
is **absent** and that the sibling `reaction video` **survived**. Silently re-adding
`reacting to`, silently dropping a tenth marker, or quietly taking `reaction video` with it
all fail here now.

---

## What I got wrong

- **The four buckets did not sum on the first run** (473 vs 2,661) because KEPT excluded
  parked-in-both. Caught by the sum check I had written into the harness, which is the only
  reason it did not reach the report.
- **Three wrong API guesses before the accounting ran**: `song_library.reload_library()`
  (does not exist), `pick(clip)` (the signature is `pick(store, mood, …)` — mood is decided
  by `match()`), and `read_all()` returning a list (it returns a dict keyed by clip id).
- I extended my claim mid-round for `tests/test_comedy_register.py` once it went red, with
  the reason on the record rather than editing an unclaimed file.

## What is still broken, and whose file

- **3 clips now match hype that should not** — all three are genuine reaction/commentary
  formats. A narrowed `reacting to` (anchored to a face-cam or split-screen signal rather
  than the bare phrase) would catch them; MEMEBOT-104 drafted it and it needs its own
  consent. **`scratch/songs.json`, the operator's file.**
- **`park %` is still 82.2%.** Nothing in this round addresses the ~1,700 clips parked for
  want of a matching route; that is a song-purchase question, not a marker question.

---

## Verification

```
python scratch/mb109_account.py --before     # snapshot (run against the pre-change store)
python scratch/mb109_account.py --after      # four buckets + per-mood
python tests/test_comedy_register.py         # 11 OK
python tests/test_song_library.py            # ALL PASS
```
