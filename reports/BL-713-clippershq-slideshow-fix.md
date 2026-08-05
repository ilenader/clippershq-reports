# BL-713 — TikTok photo slideshows now resolve their view counts

Date 2026-08-05. Base `origin/main` 8b5aaf57. Branch `checkpoint/BL-713` @ `7221a737`, VERIFIED PUSHED
(origin == local). Tags `pre-BL-713` (8b5aaf57) / `post-BL-713`. ONE file on the tracking path,
187 insertions / 7 deletions. No schema change, no `prisma migrate`, no Apify actor run, no bulk backfill.

**Gates, honestly.** `npm ci` exit 0 (wipes the generated client) → `npx prisma generate` exit 0 BEFORE tsc →
`npx tsc --noEmit` **TSC_EXIT=0**, log 0 lines → `npm run build` **BUILD_EXIT=0**, exit code echoed from a log
file, never piped through `tail`. eslint **v9.39.4 genuinely present** in the worktree, so the hooks gate is
real and not a silent no-op: **0 errors / 11 warnings** (cap 11, all pre-existing `react-hooks/exhaustive-deps`;
no React file was touched). `check:prisma-bypass` 0 violations, `check:removed-fields` OK,
`✓ Generating static pages (61/61)`. Post-commit build re-run clean on the committed tree.

## PART 1 — THE FIX, AND WHY THIS SHAPE

BL-712 measured it: production only ever calls LamaTok `by/url`, which returns HTTP 500 `AppException` on a
canonical `/photo/` slideshow and times out on a short link hiding one, while `by/id` returns HTTP 200 with a
real `playCount`. Apify is hard-off (BL-678), so nothing caught the miss and 8 APPROVED TikTok clips in the
ACTIVE "SomeSome" campaign had **zero ClipStat rows ever**.

**Decision: `by/id` becomes the path for `/photo/` slideshows ONLY, as a RESCUE. Normal `/video/` clips are
not touched.** Two reasons, both load-bearing.
• Normal videos work today. The rescue is gated on `by/url` having already produced **no stats** AND the
  verdict not being `"gone"`, so a clip that resolves returns above the new code and runs the byte-identical
  path it ran yesterday. Nothing that works can be disturbed by code it never reaches.
• BL-604 proved `by/id` is **display-rounded** (25,700 against a true 25,835). Promoting it wholesale would
  move every TikTok earning ~0.3 to 0.9% under the true count, silently. For a slideshow the choice is not
  rounded-versus-exact, it is **rounded versus no count at all and $0**, which is why the rescue is correct
  here and would be wrong everywhere else.

**Ambiguous links are handled, not assumed.** BL-668 put short links at ~70% of TikTok clips, and a short link
HIDES its `/photo/` nature until resolved (all 8 stranded clips are `vm.`/`vt.` links; BL-712 resolved 3 of 3
to `/photo/`). So:
• canonical `/photo/<id>` → the id is in the URL, zero extra cost;
• short link (`vm.`, `vt.`, `tiktok.com/t/`) → **one free 3s HEAD-follow**, and only after `by/url` already
  failed, with the same cheap SSRF guard `apify.ts` uses (the regex matches the STRING, `fetch` hits the real
  HOST, so only an allow-listed social host is ever contacted);
• canonical `/video/` → never resolved, never probed. It is a video, not a slideshow.
If the HEAD fails, or the canonical form is not `/photo/`, the function returns null and the caller's
behaviour is completely unchanged.

**Kill switch.** `LAMATOK_SLIDESHOW_BYID="false"` restores the exact pre-BL-713 behaviour in one env flip, read
at call time, no redeploy. Proven in SECTION E below.

## THE FULL DIFF (one file, `src/lib/scraper-providers/lamatok.ts`)

```diff
@@ import block @@
 import type { ClipStats } from "@/lib/apify";
 import { classifyTiktokUrl } from "@/lib/scraper-providers/hikerapi";
+import { isAllowedSocialHost } from "@/lib/social-hosts";
```
JUSTIFY: the SSRF guard for the HEAD-follow. `social-hosts` imports nothing (leaf module), so this cannot
create a cycle. The equivalent helper inside `apify.ts` is module-private and `apify.ts` imports THIS file, so
importing from there would be a real runtime cycle on the money path.

```diff
+export function slideshowByIdEnabled(envValue = process.env.LAMATOK_SLIDESHOW_BYID): boolean {
+  return String(envValue ?? "").trim().toLowerCase() !== "false";
+}
```
JUSTIFY: the rollback lever. Read at call time so a Railway env change needs no redeploy. Default ON because
the pre-fix state is a live defect; only the literal string "false" turns it off (mirrors `areCarouselsDisabled`).

```diff
+const TIKTOK_SHORT_LINK_RE = /(?:^|\/\/)(?:(?:vm|vt)\.tiktok\.com\/|(?:www\.)?tiktok\.com\/t\/)/i;
+async function resolveTiktokShortLink(url: string): Promise<string | null> {
+  if (!TIKTOK_SHORT_LINK_RE.test(url)) return null;
+  let host: string | null = null;
+  try { host = new URL(url).hostname; } catch { return null; }
+  if (!host || !isAllowedSocialHost(host)) return null;
+  try {
+    const res = await fetch(url, { method: "HEAD", redirect: "follow", signal: AbortSignal.timeout(3_000) });
+    return res.url || null;
+  } catch { return null; }
+}
```
JUSTIFY line by line. The regex is the same set of short shapes `apify.ts` resolves, so no new URL family is
opened. The hostname is re-derived and allow-list checked because the regex matches a STRING and `fetch` hits
a HOST (this is what blocks `https://127.0.0.1//vt.tiktok.com/`). `HEAD` + `redirect:"follow"` + a **3s**
`AbortSignal` is exactly the bound BL-255 settled on after a slower resolver blew the cron budget. Both
`try` blocks return null rather than throwing: this function can never break tracking for anyone.

```diff
+async function fetchLamatokTiktokById(id: string, origUrl: string): Promise<LamatokResult> { ... }
```
JUSTIFY the whole function. It GETs `/v1/media/by/id?id=<id>` with the same `x-access-key` header, the same
`fetchWithTimeout`, and the same 20s bound as the existing reader.
• `if (!res.ok || parsed == null)` → `stats: null`, `verdict: "transient"`. **Never `"gone"`.** Only a `"gone"`
  verdict can advance `gone-counter.ts`, so this function is structurally incapable of striking a live slideshow.
• The id check refuses any response whose top-level id is not the exact id requested and logs
  `[LAMATOK-BYID] ID MISMATCH`. That closes BL-550's trap at the source rather than in a probe script.
• `viewsPick == null` → `stats: null`, never 0 (BL-543). A `playCount` the provider genuinely REPORTS as 0 is
  a real reading and is returned as 0, exactly as BL-605 decided for a readable carousel sum.
• The field probes DUPLICATE the `by/url` mapper instead of being refactored into a shared helper. That is
  deliberate: `by/url` is the working money path for every normal TikTok clip, and the narrowest safe change
  is one that leaves it literally untouched. Verified against a live `by/id` payload, whose response is the
  TikTok itemStruct at top level, so `stats.playCount`, `createTime`, `desc` and `music` all sit where these
  same probes already look. `raw` is the parsed payload, so BL-668's `includeRawMeta` caption passthrough
  keeps working on the rescue path too.

```diff
+async function resolveSlideshowId(url: string): Promise<string | null> {
+  const direct = extractTiktokPhotoId(url);
+  if (direct) return direct;
+  if (classifyTiktokUrl(url) !== "unknown") return null; // canonical /video/ — not a slideshow
+  const canonical = await resolveTiktokShortLink(url);
+  if (!canonical) return null;
+  return extractTiktokPhotoId(canonical);
+}
```
JUSTIFY: the three-way decision in one place. Canonical `/photo/` costs nothing. The middle line is the guard
that keeps normal canonical videos out of the HEAD entirely. Only `"unknown"` (a short link) pays the HEAD.

```diff
 export async function fetchLamatokTiktokByUrl(url: string): Promise<LamatokResult> {
   const first = await fetchLamatokTiktokByUrlOnce(url);
+  if (first.stats == null && first.verdict !== "gone" && slideshowByIdEnabled()) {
+    const photoId = await resolveSlideshowId(url);
+    if (photoId) {
+      const byId = await fetchLamatokTiktokById(photoId, url);
+      if (byId.stats != null) return byId;
+      console.log(`[LAMATOK-BYID] rescue miss ...`);
+    }
+  }
   const isRetryable = ...
```
JUSTIFY the gate, which is the single most important line in this round. `first.stats == null` means a clip
that RESOLVED is returned before the rescue can see it, so no working clip changes. `verdict !== "gone"` means
a definitively deleted post is never resurrected and the gone path is untouched. `slideshowByIdEnabled()` is
the off switch. `if (byId.stats != null)` means only a REAL count short-circuits; a `by/id` miss falls through
to the retry block below, which is unchanged, so the fail-safe is exactly the pre-BL-713 behaviour.

```diff
-  if (urlClass === "photo") void shadowProbeSlideshowById(url);
+  // (comment: the shadow is superseded by the rescue)
```
JUSTIFY LOUDLY, because this is the only removal. BL-580 fired a **billed** `by/id` call here on every
`/photo/` poll and threw the answer away. The rescue now makes the same request and USES it. Keeping both
would bill LamaTok twice per slideshow poll for one number. Nothing is lost: the shadow's proof is what
BL-712 built this fix on, the rescue emits the equivalent `[LAMATOK-BYID]` line, and
`shadowProbeSlideshowById` stays exported as a manual diagnostic. Nothing in production calls it now.

## PART 2 — FAIL SAFE, PROVEN

• **NULL never 0.** A well-formed but non-existent `/photo/` id (`7000000000000000001`) returned
  `stats=null`, `http=500` on `by/url`, `by/id` HTTP 404 `MediaNotFound`, and **no fabricated 0**.
• **No `consecutiveGone` strike.** `verdict=carousel`, NOT `"gone"`. `fetchLamatokTiktokById` cannot emit
  `"gone"` at all, and `gone-counter.ts` increments ONLY on a definitive gone verdict, never on a transient
  5xx. The 8 stranded clips sit at `consecutiveGone=0` today and the rescue cannot move them.
• **Cannot be auto-retired.** `retire-dead-clips.ts:74` still filters candidates to
  `clipUrl contains "instagram"` and still demands a fresh HTTP 404 at `:111`. TikTok is excluded entirely,
  and that file is byte-identical to `origin/main`.
• Apify genuinely no longer exists as a fallback: `apify.ts` is byte-identical, the 6 `APIFY_HARD_OFF` sites
  and 5 `logApifySkip` sites are untouched, and the diff adds **0** actor URLs.

## PART 3 — THE 13 STRANDED CLIPS

**They need NO nudge.** Measured at `now() = 2026-08-05 10:41:58.43972+00`: all 13 are `isActive=true`,
`checkIntervalMin=360`, `cadenceReason=INFRA_DEFER`, `videoUnavailable=false`, `consecutiveGone=0`,
`consecutiveFailures=0`, and every `nextCheckAt` falls between `2026-08-05 11:00:00` and `16:00:00`, i.e.
inside 6 hours. The ordinary tick collects them (short cadence sorts first under BL-200's ordering). **No bulk
backfill was run, by instruction: the fix landing and one tick proving itself comes first.**

**Only 8 of the 13 are fixed, and that is correct.** The 8 TikTok short-link clips will resolve on the next
tick after deploy. The **5 Instagram `/p/` clips are NOT fixed and must not be**: BL-712 probed all 3 sampled
and found `carousel_image_only`, `media_type=8`, 4 children, **0 video children**, `play_count=null` and
`view_count=null`. There is no count to fetch from any endpoint, so BL-610's quarantine is the right answer
and this round leaves `hikerapi.ts` byte-identical.

**Earnings from here.** Once a stat lands, these clips earn normally at their stamped CPM through the
unchanged earnings path. **Past views are not lost:** TikTok's `playCount` is CUMULATIVE, so the first stat
captures every view since posting as a level, and earnings are computed from the current count, not from a
delta. What genuinely cannot be reconstructed is the **day-by-day history** — there is no source for it and
none was invented. Be plain about the money: the campaign's `minViews` is 1,000 and
`earnings-calc.ts:100` returns 0 below it, so at 151 and 1 views these clips still pay **$0.00** until they
cross 1,000. The defect is real and now fixed; the money it was costing today was $0.00.

## PART 4 — NOTHING THAT WORKS WAS TOUCHED

Byte-identical by blob OID, `git rev-parse origin/main:<f>` == `git hash-object <f>`:
`clip-earnings-writer.ts` 7aa6be48, `earnings-calc.ts` 797e2098, `balance.ts` e887f80a,
**`tracking.ts` 847dcf70**, `clip-earnings-invariant-middleware.ts` 61cef393, `money-decimal.ts` ef5cdae7,
`campaign-era.ts` 106e16ad, **`apify.ts` 656bf4c0**, **`hikerapi.ts` 80508fe3**.
So Instagram carousels (including the correctly-quarantined image-only ones), YouTube, and the 11 BL-678
Apify guards are untouched **as a matter of file identity**, not opinion. The diff contains **0** DB writes
(`.update(` / `.create(` / `.upsert(` / `.delete(` / `$executeRaw` / `writeClipEarnings`) and **0** Apify
actor URLs. No Apify actor was invoked at any point in this round.

## PART 5 — THE EVIDENCE (harness 27 passed, 0 failed, exit 0)

`scripts/test-bl713-slideshow.ts` runs the REAL production reader `fetchLamatokTiktokByUrl` (the exact
function `apify.ts:463` and the batch at `apify.ts:1181` call). It writes no Clip, ClipStat, TrackingJob or
earning. Population drawn from the live DB, never invented.

**A real slideshow resolves, id-matched not row-matched:**
```
[LAMATOK-BYID] RESOLVED id=7668823960754113799 idMatch=true http=200 views=151 viewSource=playCount imagePost=true
  clip=cms9j26hl002t0po2djtinkhi url=https://vt.tiktok.com/ZS4rP4cvn/  verdict=ok views=151 viewSource=byId:playCount ms=23193
  clip=cms5y1dmi008q0pmrjqlbv8vr url=https://vm.tiktok.com/ZGdx8bJPc/  verdict=ok views=1   viewSource=byId:playCount ms=24008
  canonical /photo/ verdict=ok views=1 wantId=7667894322632592672 respId=7667894322632592672  (EXACT MATCH)
```
**A normal TikTok video is unchanged, and no stored view moved down:**
```
  clip=cmsdhm33u0bu10po2wpv35f88 verdict=ok views=537  stored=537  viewSource=playCount ms=1792   (rescue never fired)
  clip=cmscp257n072l0po2fy8zcdke verdict=ok views=2842 stored=2822 viewSource=playCount ms=3026   (rescue never fired)
```
**An unresolvable slideshow fails safe:** `verdict=carousel stats=null http=500`, `by/id` 404 MediaNotFound,
no 0, **verdict NOT gone**. **Kill switch OFF:** `stats=null verdict=carousel` — the exact pre-BL-713 result.

**Tick budget at CLIPS_PER_TICK 90.** The change makes slideshows FASTER, measured: 23.2s and 24.0s wall
clock versus ~41s before (a 20s `by/url` timeout plus a 20s retry that is now skipped once `by/id` answers).
Normal videos are unchanged at 1.8s and 3.0s. At `LAMATOK_BATCH_CONCURRENCY = 3` the whole 8-clip cohort drops
from ~123s to ~72s, inside `TRACKING_LOOP_BUDGET_MS` (210s). Stated honestly, the ONE path that got slower is
a short-link clip that already failed `by/url` and turns out NOT to be a slideshow: it pays one bounded 3s HEAD.

**Probes and cost, all disclosed.** 1 recon `by/id` (200, billed) to establish the response shape, then the
harness: 3 slideshow `by/url` (2 timeouts + 1 HTTP 500, none billed), 2 free HEAD-follows, 4 `by/id` (3×200
billed, 1×404 free), 2 normal-video `by/url` (200, billed), 1 bogus `by/url` (500, free), and 1 `by/url` with
the kill switch off (500, free). **~14 LamaTok requests, 6 billed 200s**, under the ~20 cap. All per-post
calls, never profile scans, so ONE CALL PER PROFILE is not engaged. **0 Apify actor runs. 0 HikerAPI calls.**

## ROLLBACK

Three levers, cheapest first: set `LAMATOK_SLIDESHOW_BYID=false` (env only, no redeploy, proven to restore the
exact prior behaviour); or `git revert 7221a737`; or `reset --hard pre-BL-713`. Nothing to undo in the
database: this round wrote nothing, changed no clip status, no stored view and no earning.
