# BL-682 (ClippersHQ) — Instagram captions and sound ids reach the reviewer note again, sourced from HikerAPI

## FIXED, AND THE SOUND ID CAME BACK TOO. On three real live Instagram clips the caption now reaches the evaluator 3 of 3 (1,347 chars each), along with the sound id, the hashtags, the post timestamp and the duration, and none of the three notes reports the pipeline-gap message any more. Contrary to this round's own expectation, **HikerAPI does expose a usable Instagram sound id**; the extractor was already reading the right key, the payload simply never arrived. TikTok is unbroken at 3 of 3. One file changed, `apify.ts` and `campaign-rules.ts` are both byte-identical, and no organic Instagram submit has landed since the branch was built, so the owner's confirmation query is in PART 3.

> **Filename note, per CONVENTION.md.** `reports/BL-682.md` was already taken by a different project (clipper-finder, *"Mood from text, not audio"*). The collision check was run against `origin/main` before pushing and that file was **not** touched. This report is published beside it under the `-<project>-<slug>` suffix the convention prescribes.

**Branch** `checkpoint/BL-682` @ `7e1bef5` (pushed, `origin/checkpoint/BL-682 == local HEAD`, verified by `scripts/safe-push.mjs`).
**Base** `fdde504f`. **Tags** `pre-BL-682` (fdde504f) and `post-BL-682` (7e1bef5), both pushed.
**Worktree** `C:/b682`, short path, `node_modules` never junctioned. **DB `now()` at query time: 2026-07-29 18:27:04.486188+00.**
**Rollback** `git revert 7e1bef5`, or `git reset --hard pre-BL-682`. Reverting restores the blind Instagram note and changes nothing else.

| file | change |
| --- | --- |
| `src/lib/clipper-submit-core.ts` | the only production file: one harvest helper plus one call site |
| `scripts/test-bl-682-instagram-caption.ts` | NEW, the proof harness |
| `scripts/bl682-hiker-probe.ts` | NEW, the diagnostic probe that found the unwrap |
| `BACKLOG.md` | +13 |

---

## PART 0 — the diagnosis, before anything was changed

### The root cause, with file and line

**The Instagram caption arrived on `stats.raw` from APIFY, and it died when Apify died.** The chain, read from the code on `fdde504f`:

| step | file:line | what happens |
| --- | --- | --- |
| 1 | `src/lib/clipper-submit-core.ts:138` | the submit path calls `fetchClipFreshnessWithRetry(clipUrl, platform)` |
| 2 | `src/lib/apify.ts:2497` | which calls `fetchClipStats(url, { skipHikerOverlay: true, includeRawMeta: true })`. `skipHikerOverlay` is BL-137's deliberate choice, so Instagram could read a parseable `createdAt` for the 30 minute window |
| 3 | `src/lib/apify.ts:2383` | `if (!options?.skipHikerOverlay)` is therefore **FALSE**, so the **HikerAPI overlay is skipped entirely** on this path |
| 4 | `src/lib/apify.ts:740` | control falls to `fetchInstagramStats`, whose **three tiers are all Apify** |
| 5 | `src/lib/apify.ts:796` | tier 1 `fetchInstagramStatsApiScraperSingle` returns `null` behind **BL-678 GUARD 3**; tier 2 (apidojo) and tier 3 (legacy) are guarded too |
| 6 | `src/lib/apify.ts` | the chain yields `{ stats: null, provider: "none" }` |
| 7 | `src/lib/clipper-submit-core.ts:158` | `fetchedRawMeta = (stats as any)?.raw ?? null` → **null**, every time |

**This is the identical failure shape BL-673 fixed for the Instagram cover frame:** a path that forces `skipHikerOverlay: true` and therefore depends on an Apify chain that has been dead since the 2026-07-22 cutover and impossible since the BL-678 guard.

### Reconciling BL-665 against BL-680

The hypothesis the brief asked to test first was correct, and here is the evidence rather than the assertion.

**BL-665 measured the Instagram caption arriving 5 of 5 on the submit path on 2026-07-24. BL-680 measured 0 of 11 organic rows on 2026-07-29. Both are correct about their own day.** BL-665 ran **five days before the BL-678 guard shipped**, from a local environment whose Apify key still worked. Its five successes are not a coincidence: `apify_usage_entries` records exactly **five `success = true` rows on 2026-07-24 and zero on every other day since the cutover**, and BL-677 independently attributed those five to BL-665's own probe. So BL-665 measured a world in which Apify still answered. **That world no longer exists**, which is precisely why its conclusion no longer holds and why repeating it would have been wrong.

### The second discovery: the unwrap

A first probe pass unwrapped the HikerAPI response as `body.media ?? body.data ?? body` and reported **"CAPTION: none of the probed keys held a string"** and **"SOUND: none of the probed keys were present"**. That would have supported a conclusion of "HikerAPI does not carry it", and it would have been **wrong**.

The response's top level holds only two keys: **`media_or_ad`** and `status`. The real media object is nested one level down. Re-probing with `body.media_or_ad` first changed the answer completely. This is recorded because the near-miss matters: BL-673's note that HikerAPI's summarised `raw` is thin is true of the **summary blob**, not of `rawBody`.

---

## PART 1 — the fix

**One HikerAPI read, on the submit path only, harvested in `clipper-submit-core.ts` rather than in `apify.ts`.** That placement is the design, not a convenience:

* **`src/lib/apify.ts` is BYTE-IDENTICAL** by blob OID, `656bf4c0c408e955676c95d14bbbb764eecde1ef`. The tracking poll, the thumbnail path and **all 11 BL-678 Apify guards** are therefore untouched by construction, not by review. The harness re-counts the five `if (APIFY_HARD_OFF)` guards in `apify.ts` and asserts on it.
* **`stats` is never modified.** Freshness, the 30 minute posting window, status, earnings and payout cannot move. This round makes DATA arrive and decides nothing.
* **`src/lib/campaign-rules.ts` is BYTE-IDENTICAL too**, `fc91216fdf1b248cdeb6fd2d0b863763e6fedc85`. `extractClipMetadata` already read `caption.text` and `clips_metadata.music_info.music_asset_info.{id,audio_cluster_id}`, added by BL-668. **The keys were never wrong. The payload never arrived.**
* **Exactly one call**, and only when the payload did not already carry metadata (`fetchedRawMeta == null`).
* **TikTok is not routed through it at all**, so its BL-668 path is provably unaffected.

### Fail open, on every shape

The helper never throws: no key, a cooldown, a 404 on a deleted or private post, a non-JSON body, a timeout and any exception all return `null`. A `null` records `captionPresent = false`, and the reviewer note then reports a gap in **our** pipeline, never a mark against the clip. Proven, not asserted:

```
--- 3. fail open ---
PASS  a provider miss (null): captionPresent false, never a throw, never a fabricated value
PASS  a post with no caption: captionPresent false, never a throw, never a fabricated value
PASS  an image-only carousel: captionPresent false, never a throw, never a fabricated value
PASS  a deleted or private post body: captionPresent false, never a throw, never a fabricated value
PASS  a total miss composes a note that blames OUR pipeline, not the clip
```

---

## PART 2 — the Instagram sound id: HikerAPI DOES expose one

**Stated plainly, and it is the opposite of what this round was set up to expect.** The brief anticipated that HikerAPI might not expose a usable Instagram sound id and asked for a plain "no" rather than a fake. The live probe says otherwise. On two real Instagram clips, under `media_or_ad`:

| key | present | note |
| --- | --- | --- |
| `clips_metadata.music_info.music_asset_info.id` | **yes** | the stable asset id |
| `clips_metadata.music_info.music_asset_info.audio_cluster_id` | **yes** | what the extractor reads FIRST |
| `clips_metadata.music_canonical_id` | **yes**, 17 chars | |
| `clips_metadata.audio_ranking_info.best_audio_cluster_id` | **yes**, 15 chars | **a ranking cluster, and the wrong key for licensed music** |
| `clips_metadata.audio_type` | **yes**, 14 chars | |

**The extractor is already reading the right one.** `extractClipMetadata` reads `music_asset_info.audio_cluster_id` then `music_asset_info.id`, and **never** `best_audio_cluster_id`. That matters because a sibling audit of the same Instagram API found `best_audio_cluster_id` is the wrong key for licensed music, so a sound rule keyed on it would compare the wrong identifier. No change was needed and none was made.

Confirmed end to end: **3 of 3** live Instagram clips now resolve a sound id through the shipped extractor. So a REQUIRED_SOUND rule on Instagram is now machine-checkable rather than permanently `cannot_evaluate`, and nothing was faked to get there.

---

## PART 3 — proof on real data

`scripts/test-bl-682-instagram-caption.ts`, run against live production data through the real shipped extraction and note-composition code: **16 passed, 0 failed.**

```
--- 2. real Instagram clips, through the real extractor ---
  clip cms6dpxxy00890pnmy6y1fc2p status=PENDING
    rawMetaPresent=true captionPresent=true captionLen=1347 soundIdPresent=true hashtags=1
    postedAtPresent=true durationSec=22
    rules=6 evaluated=0 failedOpen=6 confidence=low containsPipelineGap=false
  clip cms6dpvt600840pnmeehy3jnu status=PENDING
    rawMetaPresent=true captionPresent=true captionLen=1347 soundIdPresent=true hashtags=1
    postedAtPresent=true durationSec=18
    rules=6 evaluated=0 failedOpen=6 confidence=low containsPipelineGap=false
  clip cms6dptnj007z0pnmf51dl9ru status=PENDING
    rawMetaPresent=true captionPresent=true captionLen=1347 soundIdPresent=true hashtags=1
    postedAtPresent=true durationSec=18
    rules=6 evaluated=0 failedOpen=6 confidence=low containsPipelineGap=false

PASS  Instagram captions now reach the evaluator  3/3
PASS  Instagram sound ids now reach the evaluator  3/3
PASS  no Instagram note reports the pipeline-gap message  3/3
```

**Read `evaluated=0 failedOpen=6` honestly.** The metadata now arrives, and the note no longer blames our pipeline. Those particular six rules on that campaign are still not machine-checkable, which is why confidence reads `low`. That is a property of how those rules are written, not of this fix, and it is why `confidence` did not jump to `high`. The gap this round was asked to close is closed: the evaluator is no longer blind.

**Also recovered, for free, on the same payload:** `postedAt` is now present on all three (BL-662 measured it populated on only 2 percent of clips) and `durationSec` resolves at 18 to 22 seconds, which makes VIDEO_LENGTH rules evaluable on Instagram for the first time.

### What is NOT proven, stated plainly

**No organic Instagram submit has landed since this branch was built**, so no `rule_shadow_decisions` row yet shows `captionPresent = true` for Instagram. The pre-deploy baseline is unchanged and is the thing to watch:

| platform | organic rows since BL-668 merged | captionPresent true | soundIdPresent true |
| --- | --- | --- | --- |
| instagram | 11 | **0** | **0** |
| tiktok | 8 | 7 | 7 |
| youtube | 3 | 0 | 0 |

**The owner's check query, to run after this merges and deploys:**

```sql
SELECT platform,
       COUNT(*)                                            AS rows,
       SUM(CASE WHEN "captionPresent" THEN 1 ELSE 0 END)   AS caption_true,
       SUM(CASE WHEN "soundIdPresent" THEN 1 ELSE 0 END)   AS sound_true,
       SUM(CASE WHEN array_length(hashtags,1) > 0 THEN 1 ELSE 0 END) AS with_hashtags,
       MAX("createdAt")::text                              AS newest
FROM rule_shadow_decisions
WHERE source IS NULL              -- organic submits only, never a proof row
  AND "createdAt" > '<the deploy timestamp>'
GROUP BY 1 ORDER BY 1;
```

**Expected: the Instagram row's `caption_true` and `sound_true` climb with `rows` instead of sitting at 0.** If Instagram is still 0 after several organic submits, the fix did not take and the first thing to check is whether HikerAPI is configured in the production environment, since the harvest returns null without a key.

---

## PART 4 — TikTok is unbroken

Both platforms share the extraction layer, so TikTok was driven through its own untouched BL-668 path in the same run:

```
--- 4. TikTok, untouched, through the real submit fetcher ---
  clip cms64pqww00140pnmus5scfsu rawPresent=true captionPresent=true captionLen=56 soundIdPresent=true hashtags=1
  clip cms64pg7i000x0pnmfxaapjvp rawPresent=true captionPresent=true captionLen=56 soundIdPresent=true hashtags=1
  clip cms64p6hi000r0pnmhdd63k8g rawPresent=true captionPresent=true captionLen=56 soundIdPresent=true hashtags=1
PASS  TikTok caption arrival is unbroken  3/3
```

Structurally it could not have broken: the new branch is gated on `platform === "instagram"`, and `apify.ts` and `campaign-rules.ts` are both byte-identical.

---

## Gates, honestly

| gate | result |
| --- | --- |
| `npm ci` | **exit 0** |
| `npx prisma generate` | **exit 0**, run after `npm ci` and **before** `tsc` |
| `npx tsc --noEmit` | **exit 0**, log 0 lines |
| `npm run build` | **BUILD_EXIT=0**, echoed from `$?`, never piped through `tail`; "Compiled successfully in 22.5s" |
| hooks gate `lint:hooks` | **eslint present and actually executed** (`node_modules/.bin/eslint`, eslint **9.39.4**); `--max-warnings 11` → **11 problems, 0 errors, 11 warnings**, at the cap, passing |
| `check:prisma-bypass`, `check:removed-fields` | ran (prebuild) |

The `.ts` diff is real and non-empty: `src/lib/clipper-submit-core.ts` plus two new scripts, verified with `git status` before the claim was written.

## Safety and probe disclosure

**Money files, blob OID against `fdde504f`, all IDENTICAL:** `clip-earnings-writer.ts`, `earnings-calc.ts`, `balance.ts`, **`tracking.ts`**, `clip-earnings-invariant-middleware.ts`, `money-decimal.ts`, `campaign-era.ts`. **`apify.ts` `656bf4c0` and `campaign-rules.ts` `fc91216f` are byte-identical too.**

Nothing changes a clip's status, earnings or payout. Nothing renders to a clipper. Auto-reject stays OFF and this round does not touch `isAutoRejectLive`. **The BL-678 guard is not weakened on any of its 11 paths**, asserted mechanically by the harness. No schema change, no `prisma migrate`, no data mutation.

**Every probe, disclosed with its cost:**

| probe | calls | cost |
| --- | --- | --- |
| HikerAPI media read, diagnostic probe pass 1 | 2 | one call per clip |
| HikerAPI media read, diagnostic probe pass 2 (after the `media_or_ad` fix) | 2 | one call per clip, same two clips |
| HikerAPI media read, proof harness | 3 | one call per clip |
| LamaTok TikTok read, proof harness PART 4 | 3 | one call per clip, the existing submit path |
| read-only DB `SELECT`s via `scripts/run-select.js` | 3 | free |

**NO Apify actor was run, and no Apify endpoint was contacted.** No key was read, set or printed. **ONE CALL PER PROFILE was respected**; the four Instagram diagnostic calls are two clips probed twice, once before and once after the unwrap was corrected, and that is stated rather than hidden.

**Caption retention and redaction.** The caption is the clipper's own public post text, already fetched at submit time, so storing it costs no new vendor call. It is persisted only on `rule_shadow_decisions`, retained only as long as needed to validate the rule engine before auto-reject could ever be considered, read by OWNER-side tooling only, never rendered to a clipper, and **redacted to a character count in this report and in every log line**. No caption text, no sound id value and no clipper handle appears anywhere in this document.

Nothing held by BL-683 was touched: it has no branch and no worktree on this machine, and this round worked only in `C:/b682`. No dashes used as bullets.
