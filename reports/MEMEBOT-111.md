# MEMEBOT-111 — The vision guard moves into the matcher, and the narrowed marker lands

**Round:** MEMEBOT-111 · **Date:** 2026-08-02 · **Spend:** **$0.00**, no paid calls
**Claim:** `MEMEBOT-111`, repeated `--write` flags, amended once with `--force-reason` on the
record. `claims_read.py --holders` per target; `git status --porcelain` read by column.
`scratch/songs.json` is the **operator's file**: only the drafted change was applied and the
consent is recorded inside the rule.

Acts on [BL-1002](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1002.md)
and [MEMEBOT-109](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-109.md).

---

## 1. (b) FIRST — and the hole was wider than reported

`require_vision` was a parameter of `clip_pipeline.pick_song`, checked once before
`render_plan`. BL-1002 called it "guards `pick_song`, not the title tier". An AST sweep for
callers of the matcher found the shape is worse: **two other entry points reach the matcher
directly and neither had the guard.**

| Bypass | What it decides |
|---|---|
| `clip_pipeline.py:583` — `_servable()` | the **ordering predicate**. A clip nobody had looked at counted as servable and was re-ordered to the **front** of the queue. |
| `dashboard/server.py:1319` | the dashboard's **`renderable`** count — so the number on screen **overstated** how much of the library can actually be rendered. |

Both are read-only decisions, which is exactly why neither was noticed.

**The fix is in the matcher, not at a call site.** `require_vision` is now a parameter of
`song_library.match` / `match_detail` / `render_plan`, default **on**, so every caller
inherits it. That is MEMEBOT-057's rule — put the check in the tool rather than in the one
caller somebody remembered — and it is the only version that closes all three entry points at
once.

### Measured, on identical code, guard off vs on

| | |
|---|---:|
| matched, guard **off** | 481 |
| matched, guard **on** | 448 |
| **removed** | **33 (6.9%)** |
| …via `TRACK_TITLE_MOOD` | 29 |
| …via `FRANCHISE_MOOD` | 4 |

Neither of those tiers reads a description: `franchise` says which **film** a clip is from and
`track_title` says what the **poster** called the audio. On a clip nothing has seen, a quiet
dialogue scene and a decapitation route to the same song.

> **A number I withdraw.** My first pass reported **37**. It does not reproduce under a
> controlled before/after on one code state, and **33** is confirmed by two independent
> predicates. The 37 was taken across a code change and is not trustworthy; 33 is the figure.

### The test asserts it per tier, and asserts the skip

`tests/test_vision_required_every_tier.py` drives **every** tier with a store that would make
it fire and a clip with no vision evidence, and requires each to park — so a tier added later
inherits the refusal instead of becoming the next bypass. It also asserts the other half of
`docs/TESTING.md` rule 2: each tier **still fires** once any vision field carries content.

`VISION_RULE` is skipped in the no-evidence loop, and **the skip is itself a test**: that tier
reads `vision_text()` to match at all, so there is no case to construct — asserted rather than
assumed.

### The contract change was absorbed, not worked around

20 checks across `test_song_library.py` and `test_track_title_tier.py` built **vision-less**
synthetic clips to exercise franchise / fallback / track-title in isolation. Each gained a
vision field where it was testing **tier routing**. The one test genuinely *about* an unseen
clip resolving — `test_fallback_NEVER_returns_none`, "an empty clip still resolves" — is
updated to the new truth and now asserts **both** that an unseen clip parks **and** that a
seen one still falls back. Weakening the guard to keep them green would have undone the fix.

---

## 2. THE NARROWED MARKER — applied, with four-bucket accounting

MEMEBOT-104 drafted `reacting to a video`, `reacting to a montage`, `split screen`,
`gaming chair` and explicitly did **not** apply it. This brief is the consent; it is recorded
in the rule as `_why_narrowed_reacting_to`, the way 104 and 109 recorded theirs.

**One implementation note, stated because it is a judgement:** 104's draft says `split screen`;
the corpus writes it **81 times spaced and 28 hyphenated**, and `_compile_terms` joins words
with `\s+`, so a hyphen does not match. Both spellings are included as the **same drafted
marker**, not a new one. `reacting to a montage` fires on **0** clips today and is kept anyway
— it is part of what was consented to, and a marker that never fires costs nothing.

### Four buckets, per clip, summing to the library

| Bucket | Count |
|---|---:|
| **KEPT** (state unchanged, *including parked-in-both*) | 2,716 |
| **MOVED** (matched before and after, different mood) | 0 |
| **PARKED** (matched → nothing) | 12 |
| **GAINED** (nothing → matched) | 0 |
| **TOTAL** | **2,728 = the library** ✅ |

`KEPT` means **state unchanged**. Defining it as "matched in both" is what made MEMEBOT-109's
first run fail to sum — the clips parked before *and* after fall into no bucket at all. And a
set difference would have reported `MOVED 0` as "harmless" without ever being able to see a
move; the buckets are the instrument that can.

hype **285 → 273**.

### The three named clips

| Clip | Before | After | |
|---|---|---|---|
| `3425885556908830479_971774209` | hype | **park** | ✅ `reacting to a video` + `gaming chair` |
| `3397600688332666046_971774209` | hype | **park** | ✅ `split-screen` |
| `3931285888038729468_15165051384` | hype | hype | ❌ **matches none of the drafted markers** |

The third is a Bowser dialogue scene — *"a lumalee, dressed as a police officer, is in a cage
and speaks to them"*. No reaction register, no split screen, no gaming chair. It is a
**commentary** match, defect (a), and inventing a fifth marker to force it would be applying
something nobody consented to. Left alone deliberately.

---

## 3. (a) THE AUDIT — my bar, stated first, and my number

> **The bar.** Does the **matched phrase** sit in a description of something **happening on
> screen** (ACTION), or of someone **talking** / a **still artefact** (COMMENTARY)? The
> verdict is about the phrase's context, not whether the clip is "actiony" overall — a lore
> explainer over battle B-roll is COMMENTARY, because the phrase that fired was in narration.

30 of the 297 current `VISION_RULE` matches, sampled deterministically (sorted by `clip_id`,
every 9th, so it re-runs identically).

| Verdict | Count |
|---|---:|
| ACTION | 21 |
| **COMMENTARY** | **9** |
| UNCLEAR | 0 |

**9 of 30 — 30.0% — of vision-tier matches are commentary rather than action.**

The nine: on-screen text saying what clones *can* do; a montage of game **title screens**
(`katana` as a logo); *"a man and a woman are **talking** on a soccer field"*; a news anchor
**reporting** on a football game; *"madea **boasts about** her ability to fight"*; *"displays
a **graphic** that lists the FIFA semi-finalists"*; a quoted line of **dialogue** (*"you don't
pull a boner in a battle"*); narration of aftermath (*"he **realized** a gunfight **had**
erupted"*); and *"the **interviewer asks** why the soldier wants to fight"*.

**No comparison to 56.1% or 68.8%.** BL-1002 measured one sample at 35.0% strict and 82.5%
lenient — two numbers that **straddle** the published figure. Comparing across bars is
arithmetic dressed as evidence, so this reports its bar and its number and compares to nothing.

### A methodological finding that matters for any fix

I also ran an automatic speech-marker over the sentence carrying each phrase. Against the hand
read it caught **3 of 9** (missed 6) and **false-alarmed on 4 of the 7 it flagged**. A
phrase-list fix for (a) would inherit exactly that unreliability — which is the second reason
the next section proposes rather than applies.

---

## 4. PROPOSED, NOT APPLIED

Beyond the drafted marker, nothing was changed. Two candidates, both for a round that is given
consent:

1. **Route the vision rules on a speech-scoped exclusion** — suppress a match when the
   carrying sentence is a description of speech or of a still artefact. The audit says the
   population is ~30%; the marker experiment above says a naive keyword version will be
   unreliable, so this wants the *carrying sentence*, not the whole blob.
2. **`reaction video` and the six never-fired register markers** are untouched and should stay
   — 104 measured them 9/9 at zero cost.

**And the measured reason to be sceptical of all of it:** dropping **every** strong phrase
moved the hype default **2.4 points**, where the track-title **tier** moved it **28**.
Phrase-level work is worth little; tier-level work is where the movement is.

---

## 5. FINAL DISTRIBUTION

| | |
|---|---:|
| Library | **2,728** |
| Matched | **442 (16.2%)** |
| Parked | **2,286 (83.8%)** |

| Mood | | Tier | |
|---|---:|---|---:|
| hype | 277 | `PARK` | 2,286 |
| warm | 87 | `VISION_RULE` | 298 |
| melancholy | 67 | `TRACK_TITLE_MOOD` | 135 |
| triumphant | 11 | `FRANCHISE_MOOD` | 9 |

Park rose from 82.2% to 83.8%: **33 clips** were parked by the vision guard (they should never
have matched) and **12** by the narrowed marker. The library also grew from 2,661 to 2,728
between MEMEBOT-109 and this round, so the *counts* are not directly comparable — the
*proportions* are.

## VERIFICATION

| Check | Result |
|---|---|
| `test_song_library.py` | **ALL PASS** |
| `test_track_title_tier.py` | **OK** (1 skipped — a pre-existing BL-899 deferral) |
| `test_comedy_register.py` | **OK** |
| `test_matcher_boundary.py` | **OK** |
| `test_vision_required_every_tier.py` | **9/9** |
| `songs.json` `validate()` | **CLEAN** |
| Four buckets | **sum to 2,728**, asserted in code |
| `config.json` | unmodified, parses, **5 campaigns** |

## STILL OPEN

- **Defect (a) is measured, not fixed** — 30.0% of vision-tier matches are commentary. A fix
  needs consent and should work on the carrying sentence, not a keyword list.
- **`3931285888038729468_15165051384`** still matches hype and is one of the 30%.
- `clip_pipeline.py:583` and `dashboard/server.py:1319` now inherit the guard through the
  matcher; **neither file was edited** — both are other rounds' territory.
