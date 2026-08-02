# MEMEBOT-078 — the track-title tier, measured; and the claim.py finding I got wrong

**Headline:** the TRACK_TITLE tier takes matched clips **286 → 438** (+152), park **85.7% →
78.1%**, and the hype default **87.1% → 58.9%** — with **0 clips losing or changing a song**,
no purchase, and no vision rule touched.

**It is NOT landed, and the story of why is the most useful thing in this report.** BL-972
released `song_library.py` mid-round, the deferral registry went RED, I took it — and
`tests/test_matcher_boundary.py` refused the result within one suite run. That guard exists to
catch *a field the matcher reads that `dict_of` does not pass*, which is precisely what half
this change is. The tier was reverted; it ships as a verified patch and **one** deferral entry.
§0 and §7.

**And a correction that matters more than the tier.** MEMEBOT-077 §7 reported that
`claim.py start` silently overwrites a live claim. **That is false.** The guard has existed
since BL-839, refuses, exits 2, and leaves the victim's file intact. Item 6 of the brief is
built on my own bad diagnosis. §6 below.

---

## 0. What is landed, and what is not

| | state |
|---|---|
| `tests/test_claim_collision.py` (5 checks) | **landed** — pins a guard nothing tested |
| `tests/test_variant_preconditions.py` (4 checks) | **landed** — variants closed, as assertions |
| `tests/test_track_title_tier.py` (12 checks) | **landed**, skips until the tier does |
| `tests/test_deferrals.py` — its first real entry | **landed** |
| `docs/CORRECTIONS.md` — the claim.py correction | **landed** |
| the TRACK_TITLE tier (two files, one change) | **DEFERRED** — `scratch/mb078_patch.diff` |

`clippershq/song_library.py` is free; `clippershq/clip_pipeline.py` is held by **BL-899**. The
change needs both, so it waits for both. `tests/test_song_library.py` is BL-972's file, so the
tier's tests went in a new file of my own — split ownership by file.

Every number below was produced by the **real patch**, applied to the live matcher and run over
all 2,003 clips, then reverted. Verified `0` clips differ between the patch and the scratch
simulation, and `scratch/songs.json` is byte-identical to where it started.

## 1. The tier, and where it goes

**After VISION, before FRANCHISE.** Three things decide it and they do not all point one way:

1. **It beats franchise, so it goes above.** A franchise name says what *film* this is;
   MEMEBOT-028 audited all 15 franchise matches and **twelve routed clips carrying no vision
   label at all**. A track title says what *mood a human chose for this footage*.
2. **It does not beat vision, so it goes below.** Not because a model outranks a person — the
   vision *rules* carry three guards tuned over four rounds (`excludes_any`, `requires_any`,
   `outcome_contradicts_any`) and a title lookup carries none. Guarded vs unguarded, not
   machine vs human.
3. **A title can be counter-textual and nothing catches that.** "hidden sorrow" over a comedy
   clip is a poster using a library bed as neutral background. So the tier ships
   `needs_review: True`.

Placing it below vision also makes zero-regression **structural**: vision matches first, so no
clip that has a vision match can be moved. The per-clip check still ran, because "structural"
is an argument and the brief asked for a measurement.

The map is **exactly** MEMEBOT-077's 21 hand-read titles. Exact match, case-folded. No
stemming, no substring test — "contains sorrow" would fire on titles nobody has read.

## 2. Before and after

| song | before | after | |
|---|---|---|---|
| song01 melancholy | 3 | **73** | +70 |
| song02 triumphant | **0** | **24** | +24 — its first clips ever |
| song03 warm | 34 | **83** | +49 |
| song04 hype | 249 | 258 | +9 |
| **total matched** | **286** | **438** | **+152** |

Park **1,717 → 1,565** (85.7% → 78.1%). Tier counts: VISION 276 (unchanged), TRACK_TITLE 154,
FRANCHISE 10 → 8.

### Per-clip zero-regression

Measured per clip, because **a set difference cannot see a move** — a clip that changes song
appears in both the before and after sets and cancels out:

```
clips that LOST a song   : 0
clips that CHANGED song  : 0     <- invisible to a set difference
clips that GAINED a song : 152
```

**Two clips changed TIER without changing song** — franchise 10 → 8 — and this is exactly what
the per-item check is for. Both are Dark Knight / Endgame clips whose posters declared *FUNK
CRIMINAL (ULTRA/MEGA SLOWED)*. They were hype before because the *film* was in the franchise
map; they are hype now because a human picked a phonk track. Same song, better reason. A
set-difference audit would have reported "nothing changed" and been right about the total
while missing that the evidence under two records was replaced.

## 3. Hand-audit of 30 new matches

Same rubric as MEMEBOT-077 so the two are comparable. Stratified 12/8/7/3 across
melancholy/warm/triumphant/hype against a population of 70/49/24/9 — triumphant and hype
over-sampled because triumphant had **never matched a clip before this tier**.

| | RIGHT | WEAK | WRONG |
|---|---|---|---|
| **new track-title matches (n=30)** | **53.3%** | 26.7% | **20.0%** |
| existing matcher (MEMEBOT-077, n=40) | 56.1% | 23.9% | 20.0% |

**The tier doubles coverage at the same precision. It does not improve precision** — the WRONG
rate is identical at 20% and the RIGHT rate is indistinguishable at these n. That is the honest
result, and it is still worth landing: +152 clips at no quality cost, for zero purchase.

By mood: warm 62% right, triumphant 43%, melancholy 42%, hype 100% (n=3).

**The counter-textual risk the brief named is real and I found it.** The six WRONG:

- *Young Sheldon* algorithm gag → "Whisper Walk" → melancholy. The poster used a calm library
  bed as **neutral background**, not as emotion.
- *The Rookie* — Officer Chen **fights back** → "Hidden Sorrow" → melancholy over an action beat.
- *The Simpsons* — Todd Flanders doubts God **after his mother's death** → "Milk and Cookies" →
  warm. The worst call in the set: a wholesome track over a child's grief.
- *Futurama* Bender gag, *Rick and Morty* black comedy, *Friends* haircut anecdote → all
  "Forest Knight" → triumphant.

**"Forest Knight" is the single worst entry: 1 RIGHT / 3 WRONG.** It routes 13 clips. It is a
generic library bed whose *name* reads epic while the footage is comedy. Dropping it costs 13
clips (152 → 139) and removes half of triumphant. Recommended, and left in the map for the
operator to decide because the brief said not to generalise beyond what was read.

## 4. The hype default — and what actually fixes it

The brief asked what the vision rules would match if hype required stronger evidence. Measured
by rebuilding the rule three ways:

| variant | matched | hype share |
|---|---|---|
| shipping | 286 | **87.1%** |
| drop `strong:explosion` | 264 | 86.0% |
| drop **every** strong phrase (hype needs two weak) | 242 | 84.7% |
| **+ TRACK_TITLE tier (no rule change at all)** | **438** | **58.9%** |

**Weakening the hype rule barely moves the default.** Removing every strong phrase costs 44
matches and buys 2.4 points. The tier costs nothing and buys **28.2 points**. So the 87% was
never a threshold problem — it is that **only one of four songs has a broad subject rule**, and
it happens to match what this corpus mostly is. Adding a second broad route is the fix; tuning
the first one is not.

### `strong:explosion` precision

It fires on **34 clips** — the most of any strong phrase — and the scene description confirms
an explosion on **13. Precision 38.2%**, far the worst in the rule:

| phrase | fired | scene confirms |
|---|---|---|
| **explosion** | **34** | **13 (38.2%)** |
| fight sequence | 7 | 4 (57.1%) |
| action sequence | 9 | 6 (66.7%) |
| martial arts | 9 | 6 (66.7%) |
| fight scene | 9 | 7 (77.8%) |
| shootout | 6 | 5 (83.3%) |
| fifa / soccer / assassin / boxing | 2–4 each | 100% |

Unconfirmed hits include a Spider-Man stunt **behind-the-scenes** reel, a My Hero Academia
**character-ranking** post, and a Regular Show **Christmas** episode.

**Honest limit:** "scene confirms" measures whether the phrase describes the *footage* or
something else in the fused text — it is not a correctness measure, and MEMEBOT-077 found
scene-confirmation does *not* separate RIGHT from WRONG overall (57.9% vs 50.0%). For
`explosion` specifically it corroborates the hand audit, where three explosion-fired clips had
no explosion and two were WRONG. Treat 38.2% as "this phrase is the loosest in the rule",
not as "62% of these clips are wrong."

## 5b. Multi-song variants stay closed — now as assertions

Not built, as instructed. Both facts are recorded in `tests/test_variant_preconditions.py` so
the idea is refused by a test rather than by whoever remembers the report:

- **0 of 2,003 clips match more than one rule.** `requires_any` blocks 450 of 812 cross-rule
  evaluations; "no phrase at all" accounts for 360 more.
- **`bias_map` keys on `song@start-end` with no clip dimension**, so an A/B is confounded by
  clip quality — the strongest clip's song wins regardless of song.

The tests go RED if either becomes false, which is the point: a closed result that cannot
notice it has been reopened is a stale opinion. Both carry a self-test that fires on a
synthetic fixture, so an all-zero result is a measured fact rather than a vacuous pass.

## 6. Item 6 — I was wrong, and there was nothing to fix

MEMEBOT-077 §7 reported `claim.py start` silently overwriting a live claim and recommended
adding a guard. Checking before building:

- The guard has been in `start()` since **BL-839**, present in **all eight** most recent
  commits of the file, first appearing **2026-08-01 13:13** — a day before the collision.
- Run live against BL-972's real claim it **REFUSES**, **exits 2**, and leaves their `started`
  and `intent` byte-identical.

So `.claims/MEMEBOT-072.json` cannot have existed at 13:42. The other round was working under
that id **without a live claim**. I inferred a tool bug from a collision whose cause I had not
checked. Corrected in `docs/CORRECTIONS.md`; `tools/claim.py` **not modified**, which also
dissolved an advisory conflict with BL-973, who is editing that file for path resolution.

**The real gap was a missing test.** `grep -rn DuplicateClaim tests/` returned nothing: a guard
three rounds depend on had no coverage. `tests/test_claim_collision.py` now pins the refusal,
the victim's file surviving byte for byte, `--force` still reclaiming, and the CLI exiting
non-zero.

**Writing that test found a live hazard.** My first draft redirected the registry by setting
`claim.CLAIM_DIR` — which does nothing, because `claims_dir()` resolves per call from
`$CLIPPERSHQ_CLAIMS_DIR` then the git common dir. The test wrote `ROUND-1.json`, `ROUND-2.json`
and `R1.json` into the **live registry** while 13 rounds were in flight. Detected, removed,
and the test now asserts the redirect took effect before it writes anything. Same shape as
INFRA-012's rule for the dashboard config: *point at a temp copy, and "I patched the constant"
is not the same as "I redirected the resolver".*

## 7. Traps this round hit

**I landed half a change and the repo caught me.** `dict_of()` carries only `MATCHER_FIELDS`,
and `track_title` is not in it — so the tier alone matches **nothing** on all 575 clips that
have a title, while passing every unit test fed a hand-built dict. I knew this, wrote it into
the patch as "part 2, required" — and then landed part 1 anyway the moment BL-972 freed the
file, because `test_deferrals` told me to take it. `tests/test_matcher_boundary.py` failed on
the next run with *"dict_of() drops ['track_title'], which song_library reads … this is the
ninth instance of a value computed correctly and discarded at a boundary"*. Reverted.

**The deferral registry entry was the actual bug.** I filed the change as **two** entries, one
per file. That is wrong: a deferral is keyed on a file but its unit is a **change**. Split one
change in two and each half independently invites you to take it. It is now one entry, keyed
on the file still held, naming both halves — so a partial release cannot green-light a partial
landing. The registry note records this, because the next round will hit the same shape.

**My first landed-marker was the bug's fingerprint, not the fix's.** I keyed the
clip_pipeline deferral on `"track_title",` — which **already appears** in `_RANK_FORBIDDEN`,
so the registry reported the work landed before anyone had done it. Caught by the test on its
first run. This is the precise mistake `test_deferrals.py`'s own docstring warns about, made
by the round that read it.

**And a third, smaller:** the patch is generated against a CRLF file. My first pass used `\n`
patterns, so every **multi-line** replacement silently failed while single-line ones succeeded
— producing a patch that reproduced all 152 matches and then raised `KeyError` in
`match_detail()`. Caught only because the verification ran `match_detail` rather than `match`.
A patch that gets the headline number right can still be broken.

## 8. Suites, campaigns, config

**144 of 146 suites green.** The two red are not mine:

| red suite | attribution |
|---|---|
| `tests/test_render_argv.py` | `edit.py` gained `--force-caption`, which `clip_pipeline` neither passes nor records. `edit.py` is held by **MEMEBOT-082**; I never touched it. |
| `memebot/scraper/tests/test_caption_fit.py` | same `edit.py` work (green on the final run) |

`tests/test_matcher_boundary.py` was red for one run **because of me** and is green again after
the revert — recorded here rather than quietly fixed, because it is the finding in §7.

My five suites: `test_track_title_tier` 15 (12 skipped while deferred, 3 asserting the deferral
is real), `test_claim_collision` 5, `test_variant_preconditions` 4, `test_deferrals` 7,
`test_matcher_boundary` 9 — all green. BL-972's `test_song_library.py` also green: the tier
broke none of their work while it was applied.

**A skipped suite is a red suite.** `run_all.py` marked `test_track_title_tier` red for
"asserted NOTHING" when every class skipped — the same vacuous-proof rule `test_deferrals`
applies to an empty registry. Fixed by adding three checks that always run and assert the
DEFERRAL is real: the patch exists, it carries both halves, and the registry still names it.

Campaigns unchanged (10, `run.py` untouched). `config.json` (161 keys),
`memebot/scraper/config.yaml` and `scratch/songs.json` all parse. **`scratch/songs.json` and
`clippershq/song_library.py` are byte-identical to where they started** — verified with
`git status --porcelain`, both clean.

**Spend: $0.00.** No paid calls.
