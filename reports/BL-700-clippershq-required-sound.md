# BL-700 (ClippersHQ) — the first REQUIRED_SOUND rules, at enforcement rank, added as a data operation

## THREE RULES LANDED, ALL AT `rank`, AND INSTAGRAM IS COVERED. Production went from **0** REQUIRED_SOUND rules to **3**, across two campaigns, every one confirmed `enforcement: "rank"` by reading the saved rows back. The owner asked for Instagram to be checked as well as TikTok, and the ids turn out **not to be comparable**, so each platform got its own rule with its own id rather than one rule that would have flagged every Instagram clip. **Zero source files changed.** One rule was deliberately **held**: Panic Baby's Instagram agreement is 84.6 percent, below the 95 percent threshold, and shipping it would flag about one in seven legitimate clips.

> **Filename note, per CONVENTION.md.** Published at the path the round specified. The collision check was run against `origin/main` before pushing.

**Branch** `checkpoint/BL-700` @ `5670345` (pushed, `origin/checkpoint/BL-700 == local HEAD`, verified by `scripts/safe-push.mjs`).
**Base** `f7a1a344`. **Tags** `pre-BL-700` and `post-BL-700`, both pushed. **Worktree** `C:/b700`, short path, `node_modules` never junctioned.
**DB `now()` at query time: 2026-07-31 10:40:12.410894+00.**
**Rollback** id-targeted SQL in the migration footer; verify `md5("rulesJson"::text)` returns to `6923c0eb0e82eda4cee16546d8af9309` (Panic Baby) and `3b637d44229a832c0c0fe121d0eb8960` (bees.n.honey).

| file | change |
| --- | --- |
| `scripts/migrations/BL-700-REQUIRED-SOUND-RULES.sql` | NEW, the data operation plus its rollback |
| `scripts/test-bl-700-required-sound.ts` | NEW, the proof harness |
| `scripts/bl700-ig-sound-probe.ts` | NEW, the comparability probe |
| `BACKLOG.md` | +11 |
| **`src/`** | **nothing. `campaign-rules.ts` `fc91216f` and `reviewer-note.ts` `a33f4bda` byte-identical** |

---

## PART 1 — a data operation, and the form defect that made it necessary

**Written through `scripts/run-mutation-once.js`, never the admin form.** Three `UPDATE` statements, each idempotent behind `NOT ("rulesJson" @> '[{"id":"rN"}]'::jsonb)`, each returning `rowCount=1`.

**Read back from the saved rows, not asserted from the file:**

| campaign | rule id | type | **enforcement** | soundId | platforms |
| --- | --- | --- | --- | --- | --- |
| bees.n.honey | `r7` | REQUIRED_SOUND | **rank** | `7641624164701259777` | `["tiktok"]` |
| bees.n.honey | `r8` | REQUIRED_SOUND | **rank** | `954083907432874` | `["instagram"]` |
| Panic Baby | `r9` | REQUIRED_SOUND | **rank** | `7644917591970039809` | `["tiktok"]` |

### The admin form silently writes `auto_reject`. REPORTED, NOT FIXED.

`src/app/(app)/admin/campaigns/page.tsx:329` writes `enforcement: defaultEnforcementForType(r.type)`, and `defaultEnforcementForType("REQUIRED_SOUND")` returns **`auto_reject`** (`campaign-rules.ts:60`). The form exposes **no enforcement picker at all** and sets no `params.soundId`, so choosing "Required sound" in the UI produces an `auto_reject` rule that can never evaluate.

**It has already happened, nine times.** Counted across every campaign's `rulesJson`:

| enforcement | rules in production |
| --- | --- |
| `human_only` | 88 |
| **`auto_reject`** | **9** |
| `rank` | 3 (all added by this round) |

All nine are `REQUIRED_CAPTION_TOKENS`, spread over seven campaigns: BAD BITCH ANTHEM (0.50) x2, BAD BITCH ANTHEM (2.50) x2, CROCS, Deja Shoe, GainzAlgo, SomeSome, STRAENGE. **They are harmless today** because no reject code path exists (BL-659) and `RULES_AUTO_REJECT_LIVE` gates nothing, confirmed live: **0 of 328** shadow rows have ever recorded `autoRejectLive`. But they are exactly the thing that becomes dangerous the day a reject path is built.

**Follow-up for a later round, deliberately not done here:** give the form an enforcement picker, or change `defaultEnforcementForType` to return `rank`, and decide what to do with the nine existing rows. **Until then the owner must not add a rule through the UI.**

### Why `rank` is structurally safe, not merely a label

`evaluateRulesShadow` (`campaign-rules.ts:333`) sets `wouldReject` **only** for `enforcement === "auto_reject" && verdict === "would_reject"`. A `rank` rule therefore cannot contribute to an auto-reject **even if the live flag were switched on**. The harness asserts this directly rather than trusting the reading: on a deliberate mismatch, `summary.wouldReject === false` and `wouldRejectRuleIds` is empty, while the per-rule verdict is still recorded so the disagreement rate accrues.

---

## PART 2 — resolving each sound, and the Instagram finding

### TikTok, by free redirect follow, one call per campaign

BL-681 found LamaTok cannot resolve a sound **share** link (0 of 3, because it calls the media endpoint and a `soundLink` points at a sound page). Re-resolved this round by plain redirect, no API key and no cost:

| campaign | resolved to | **stable music id** | corroboration |
| --- | --- | --- | --- |
| bees.n.honey | `www.tiktok.com/music/daylight-7641624164701259777` | **`7641624164701259777`** | slug `daylight` is the track title, and the same redirect carries `share_music_id=7641624164701259777` |
| Panic Baby | `www.tiktok.com/music/glitter-in-the-night-7644917591970039809` | **`7644917591970039809`** | slug matches the requirement text *"glitter in the night"*, and `share_music_id=7644917591970039809` |

**Two independent signals per campaign**, the slug and the query parameter, and neither slug says `original-sound`.

### Instagram: the ids are NOT comparable, and there is a third identifier

BL-682 established that HikerAPI does expose an Instagram sound id. The question this round had to settle is whether it is the **same** id, and the answer is no, twice over. One HikerAPI call per campaign on a real APPROVED clip:

| campaign | TikTok music id | Instagram id **stored in the campaign's audio URL** | Instagram id **HikerAPI actually reports** | `audio_type` |
| --- | --- | --- | --- | --- |
| bees.n.honey | `7641624164701259777` | `27608619482065252` | **`954083907432874`** | `licensed_music` |
| Panic Baby | `7644917591970039809` | `35557449013901392` | **`1286427376475817`** | `licensed_music` |

**Three separate namespaces, and the trap is the middle column.** The campaigns each store an `instagram.com/reels/audio/<id>/` link, and that id **appears nowhere in the media payload**: not as `audio_cluster_id`, not as `music_asset_info.id`, not as `music_canonical_id`. A rule keyed on the stored URL would have flagged **100 percent** of Instagram clips while looking entirely reasonable in the JSON. The rule uses the id the extractor actually reads, `clips_metadata.music_info.music_asset_info.audio_cluster_id`.

**The consequence for rule shape.** `evaluateRuleShadow` reads a **single** `params.soundId` and gates on `rule.platforms`, returning `cannot_evaluate` with *"rule not scoped to this platform"* when the clip's platform is not listed. So the correct shape is **one rule per platform, each carrying that platform's own id**, which needs no code change at all. A single rule scoped `["tiktok","instagram"]` would have been the wrong answer.

### YouTube reads `cannot_evaluate`, and here is the precise reason

Confirmed by the harness: a YouTube clip returns `cannot_evaluate`, never a pass and never a flag, and `rankRuleIds` stays empty.

**Stated precisely rather than loosely:** the reason string is *"rule not scoped to this platform"*, **not** BL-668's YouTube-specific wording. That is because the platform gate at `campaign-rules.ts:270` fires **before** the YouTube branch at `:297`, and these rules are scoped to a single platform that is never `youtube`. The required outcome is met exactly; the sentence a reviewer would read is the platform-scope one. If the owner ever wants the "YouTube exposes no sound id on any API" wording to surface, a rule would have to list `youtube` in `platforms`, which would be worse, not better.

---

## PART 3 — would the rules be right? The agreement test, and the one that was held

**Threshold applied: 95 percent agreement against already human-APPROVED clips.** Below that, a rule flags more than one legitimate clip in twenty and the reviewer note becomes noise. R-2's caption finding, where humans approved 85 percent of clips breaking the hashtag rule, is the failure this threshold exists to avoid.

**Measured for free from `rule_shadow_decisions`, joined to real clip status, no provider call:**

| campaign | platform | expected id | approved MATCHING | approved MISMATCHING | agreement | decision |
| --- | --- | --- | --- | --- | --- | --- |
| Panic Baby | tiktok | `7644917591970039809` | **34** | 1 (`7641616442413090833`) | **97.1%** (n=35) | **ADDED** |
| bees.n.honey | instagram | `954083907432874` | **17** | 0 | **100%** (n=17) | **ADDED** |
| bees.n.honey | tiktok | `7641624164701259777` | **1** | 0 | 100% (n=1) | **ADDED**, see below |
| **Panic Baby** | **instagram** | `1286427376475817` | 11 | **2** (`35557449013901390`) | **84.6%** (n=13) | **HELD** |

**bees.n.honey TikTok is added on n=1, and that is defensible for a specific reason:** its expected id was resolved from the campaign's **own stored `soundLink`** with two independent corroborations, so the rule's value does not depend on that single observation. The one observed clip agreeing is a check, not the source. Instagram's id, by contrast, could only be established empirically, which is why 17 of 17 mattered there.

**Panic Baby Instagram is held, and the two dissenters are interesting.** Their id `35557449013901390` differs from the campaign's stored URL id `35557449013901392` by a single final digit, which looks like an id that has passed through a 64-bit float somewhere and lost precision, since both exceed `Number.MAX_SAFE_INTEGER`. Whatever the cause, 2 of 13 approved clips would be flagged and the rule is not ready. **It should be revisited once more Instagram rows accumulate.**

### The original-sound hold is respected

**BAD BITCH ANTHEM (2.50 CPM) got no rule.** Its sound resolves to `original-sound-7621960336325446431` and BL-681 held it because a per-post original-sound id would flag re-uploads correctly but cannot be validated until a human has ruled on one. Nothing was added.

**Both added campaigns re-confirmed as library tracks, not original sounds:** slugs `daylight` and `glitter-in-the-night`, and `audio_type = "licensed_music"` on the live probe of each.

---

## PART 4 — snapshot, dry run and rollback, all before the write

**Pre-state, captured before any change:**

| campaign | rules before | `md5("rulesJson"::text)` | requirements length | requirements md5 |
| --- | --- | --- | --- | --- |
| bees.n.honey | 6 (all HUMAN_ONLY) | `3b637d44229a832c0c0fe121d0eb8960` | 483 | `6e049b0d2385c3b139b969eb128fb903` |
| Panic Baby | 8 (all HUMAN_ONLY) | `6923c0eb0e82eda4cee16546d8af9309` | 414 | `ea93b1109e05428d05171c027932f830` |

**Dry run, computed with a `SELECT` that wrote nothing:** bees.n.honey 6 → 8, Panic Baby 8 → 9. The appended JSON was rendered through `jsonb_pretty` first so the escaping in `Use the official \"glitter in the night\" sound.` could be eyeballed before it was committed.

**Rollback, exact and id-targeted**, in the migration footer:

```sql
UPDATE campaigns
   SET "rulesJson" = (SELECT COALESCE(jsonb_agg(e), '[]'::jsonb)
                        FROM jsonb_array_elements("rulesJson") e
                       WHERE e->>'id' <> 'r9')
 WHERE id = 'cmqcnzpzk00370pqjov9d6tlc';

UPDATE campaigns
   SET "rulesJson" = (SELECT COALESCE(jsonb_agg(e), '[]'::jsonb)
                        FROM jsonb_array_elements("rulesJson") e
                       WHERE e->>'id' NOT IN ('r7','r8'))
 WHERE id = 'cmppnmhb3000g0po2gih2jt75';
```

**The clipper-facing text is byte-identical.** Re-read after the write: bees.n.honey still length 483 md5 `6e049b0d2385c3b139b969eb128fb903`, Panic Baby still length 414 md5 `ea93b1109e05428d05171c027932f830`. **Clippers see no change whatsoever.**

---

## PART 5 — the proof

`scripts/test-bl-700-required-sound.ts` reads the rules **back from the database** and drives them through the real evaluator and note composer, using sound ids already stored on real clips so it makes **no provider call at all**. **16 passed, 0 failed.**

```
  bees.n.honey  id=r7 enforcement=rank soundId=7641624164701259777 platforms=["tiktok"]
  bees.n.honey  id=r8 enforcement=rank soundId=954083907432874 platforms=["instagram"]
  Panic Baby    id=r9 enforcement=rank soundId=7644917591970039809 platforms=["tiktok"]

PASS  EVERY saved sound rule reads enforcement rank, never auto_reject
PASS  every saved sound rule is scoped to exactly one platform
PASS  a TikTok clip on the required sound reads would_pass  sound id matches
PASS  a TikTok clip on a DIFFERENT sound reads would_reject  sound id mismatch (got 7641616442413090833, want 7644917591970039809)
PASS  even on a mismatch, the summary wouldReject stays FALSE (rank can never auto-reject)
PASS  the mismatch still ranks the clip for a human
PASS  an Instagram clip is NOT judged by the TikTok rule  rule not scoped to this platform
PASS  an Instagram clip on the required Instagram audio reads would_pass  sound id matches
PASS  a TikTok clip is NOT judged by the Instagram rule  rule not scoped to this platform
PASS  a YouTube clip reads cannot_evaluate, never a pass  rule not scoped to this platform
PASS  a YouTube clip is never flagged by the sound rule
PASS  the note carries a real SOUND finding  confidence=high suggestion=look_closer
PASS  the note mentions the sound id mismatch in words
PASS  a matching clip's note does NOT claim a violation  confidence=high suggestion=nothing_flagged
```

**The note now says something a reviewer can act on.** On a mismatching TikTok clip it reads `confidence=high, suggestion=look_closer` and names the mismatch in words; on a matching clip it reads `confidence=high, suggestion=nothing_flagged`. Before this round, with zero REQUIRED_SOUND rules in production, the only machine-certain check generated nothing at all.

**Nothing moved that should not have.** Measured after the write:

| check | result |
| --- | --- |
| clip statuses | PENDING 7, APPROVED 3675, REJECTED 871, FLAGGED 6 |
| earnings invariant | **0 violations** across all four statuses |
| REJECTED earnings | **$0.00**, BL-683's cleanup still holding |
| payouts | no row updated by this round; newest update predates it |
| auto-reject | **0 of 328** shadow rows have ever recorded `autoRejectLive` |
| clipper visibility | none: `requirements` byte-identical, and the note is OWNER and CLIP_VIEW only |

---

## Gates, honestly

| gate | result |
| --- | --- |
| `npm ci` | **exit 0** |
| `npx prisma generate` | **exit 0**, after `npm ci` and before `tsc` |
| `npx tsc --noEmit` | **exit 0**, log 0 lines |
| `npm run build` | **BUILD_EXIT=0**, echoed from `$?`, never piped through `tail`; "Compiled successfully in 16.7s" |
| hooks gate `lint:hooks` | **eslint present and executed** (`node_modules/.bin/eslint`, eslint **9.39.4**); `--max-warnings 11` → **11 problems, 0 errors, 11 warnings**, at the cap |

## Safety and probe disclosure

**Money files, blob OID against `f7a1a344`, all IDENTICAL:** `clip-earnings-writer.ts`, `earnings-calc.ts`, `balance.ts`, `tracking.ts`, `clip-earnings-invariant-middleware.ts`, `money-decimal.ts`, `campaign-era.ts`, and **`campaign-rules.ts` `fc91216f`** and **`reviewer-note.ts` `a33f4bda`**. No source file changed at all.

**Every probe, disclosed with its cost:**

| probe | calls | cost |
| --- | --- | --- |
| redirect follow of each campaign's TikTok `soundLink` | 2 | **free**, no API key, one per campaign |
| HikerAPI media read on one approved Instagram clip per campaign | 2 | one call per campaign, **never per clip** |
| agreement test | 0 | read entirely from stored `rule_shadow_decisions` rows |
| read-only DB `SELECT`s via `scripts/run-select.js` | ~12 | free |

**NO Apify actor was run and no Apify endpoint was contacted.** All **5** `if (APIFY_HARD_OFF)` guards in `apify.ts` are intact, and the file is untouched. No `prisma migrate`; the only write was three idempotent `UPDATE`s to `campaigns."rulesJson"` through the sanctioned `run-mutation-once.js`, each echoed to the log before running. No clip was rejected, flagged to a clipper or status-changed, and nothing renders machine suspicion to any clipper. No clipper handle, caption or wallet address appears anywhere. Counting was done with `grep -c` and `wc -l`, never through `head`. Nothing held by BL-698 or BL-699 was touched; this round worked only in `C:/b700`. NO dashes used as bullets.
