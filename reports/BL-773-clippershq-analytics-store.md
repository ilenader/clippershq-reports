# BL-773 — the analytics store, and the clip card that shows the owner the real numbers

> **THE PIPELINE IS UNVERIFIED END TO END. A real `BUNDLE_SOCIAL_API_KEY` is present and I proved it authenticates, but not one analytics field was ever observed, because the bundle.social organisation has no team, no subscription and no connected TikTok account. It was created `2026-08-11T11:28:36.818Z`, about half an hour before this round began. The store and the display are built against the documented shape with every field nullable. I am not claiming a working integration.**

**2026-08-11 · DB now() = `2026-08-11 13:49:01.632852+00` · BUILD.**
Base `origin/main` @ `9d285c8c`. Branch `checkpoint/BL-773` @ `4298f9a`, **verified pushed**. Tags `pre-BL-773` and `post-BL-773` on origin. Worktree `C:/b773`, short path, no junctioned `node_modules`, removed at the end. **This round wrote nothing to the database.** No key, token or credential was logged, printed or committed.

---

## PART 0 — THE PREREQUISITE, HONESTLY

### What exists, measured against the live API

BL-770 could not run because no key was supplied. A key exists now, so I used it rather than reasoning from documentation, and the result is genuinely further than three prior rounds reached.

| check | result |
|---|---|
| `BUNDLE_SOCIAL_API_KEY` in `.env.local` | **present**, 36 characters, not a placeholder |
| Does it authenticate? | **YES.** `GET /api/v1/organization` returns **200** |
| `apiAccess` | **true** |
| `analyticsDisabled` / `analyticsPostsDisabled` | **false / false** |
| `subscription` | **null. No paid plan.** |
| `teams` | **0** |
| `GET /api/v1/team` | 200, `total: 0` |
| Organisation created | **`2026-08-11T11:28:36.818Z`** |
| `clip_account_connections` rows | **0** |
| Import limit fields | all `null`, because there is no subscription to carry them |

### Three endpoint facts nobody had confirmed

| endpoint | result | meaning |
|---|---|---|
| `GET /api/v1/analytics/social-account/raw?teamId=…&platformType=TIKTOK` | **404 "No team found"** | The route **exists** and both parameters **parsed**. BL-769's documented path and contract are **correct**. |
| `GET /api/v1/analytics/post` | **400 Request Validation Error** | The route **exists**; `id` is **not** its parameter name. The correct name is still unknown. |
| `GET /api/v1/analytics/posts/bulk` | **404** | **Does not exist**, despite being advertised in the vendor's own `llms.txt`. |
| `GET /api/v1/social-accounts`, `/teams` (plural) | **404** | The vendor's `llms.txt` is **unreliable**; the singular forms are the real ones. |

**So the blocker is not the key. It is that there is nothing to fetch analytics for.** No team, no plan, no connected account.

### What the owner must supply, in order

1. **Create a team** in bundle.social. Every analytics call takes a `teamId` and there are zero teams.
2. **Take a paid plan.** `subscription` is null.
3. **Connect at least one TikTok account**, which is BL-772's "ask five people personally" step. Five connections cover **71.0% of TikTok earnings**.
4. **Run the additive SQL** in `scripts/migrations/BL-773-clip-analytics-snapshots.sql`.

Only then can a single number appear, and only then can the four questions BL-770 left open be answered: what the payload actually looks like, whether `video_view_retention` hides in the untyped `raw` object, what counts as an import, and whether a refresh recounts.

---

## PART 1 — THE STORE

`ClipAnalyticsSnapshot`, mapped to `clip_analytics_snapshots`. I kept **the name BL-772 planned** rather than inventing a parallel one.

**Applied with `npx prisma generate` only. `prisma migrate` was never run and the table does not exist in production** (`information_schema` returns 0). The additive `CREATE TABLE IF NOT EXISTS` sits in `scripts/migrations/` for the owner to run by hand.

### All nine fields, nullable

`averageTimeWatchedSec`, `fullVideoWatchedRate`, `totalTimeWatchedSec`, `reach`, `videoViews`, `profileViews`, `impressionSources`, `audienceCountries`, `audienceGenders`, `audienceAges`. Plus `capturedAt`, `provider`, `platform`, `externalPostId`, `ok`, `errorCode`.

*(A note on the count: BL-769 and BL-770 both say "nine fields" and both list **ten** names. BL-772's schema resolves it by dropping `audience_cities`, which is what I followed. The disputed tenth is `audience_cities`.)*

### ABSENT is not NULL is not ZERO

`fieldStatus` is the only **NOT NULL** analytic column, and it is the reason the store has this shape:

> **`"present"`** — a usable value arrived. **This includes a genuine zero.**
> **`"null"`** — the key arrived and was explicitly null.
> **`"absent"`** — the key was not in the response at all, which is what an expired field looks like.

Six fields stop being returned once a clip has had no engagement for seven days. Without per-field provenance an expired field renders as **"0 seconds watched"**, which is an accusation wearing the costume of a measurement. **The display refuses to print a number for anything not `"present"`.**

### Every capture is kept

New row every time, never an update. A clip that was quiet on day one and viral on day four keeps both readings, and the difference between them is the only thing here that approaches evidence. Failed captures are stored too, with a machine `errorCode` only and never a provider message, so a reviewer can tell **"we asked and got nothing"** from **"we never asked"**.

`rawPayload` exists and is **deliberately not written**. The column is there so the first round that sees a real response can vet it and start writing without another schema change. **Writing an unseen payload to the database is storing something nobody has read.**

### The cadence, and why

| rule | value | reason |
|---|---|---|
| First capture | **48h** after the clip | TikTok's analytics carry a documented 24 to 48 hour delay; asking sooner spends an import to learn nothing |
| Refresh | every **24h** while views climb | The vendor recomputes daily, so asking more often returns the same numbers |
| Stop | after **7 flat days** | The same moment TikTok's six perishable fields begin disappearing |
| Payout time | **never fetch** | A vendor outage must never sit between a clipper and his money |

There is a second clock: the vendor **deletes its analytics after 30 days**. Two independent expiries are why this is a store and not a live read.

**One thing the platform must never do.** TikTok's documented remedy for an expired field is to view, like or comment on the video. The platform must not: manufacturing engagement on content it pays for is the behaviour it is trying to detect.

---

## PART 2 — THE CAPTURE, FAILING OPEN

`captureClipAnalytics` **never throws**. Every path returns an outcome object, and the caller may ignore it entirely.

| failure | outcome | clip |
|---|---|---|
| No key | `{attempted:false, reason:"no_api_key"}` | untouched |
| Clipper not connected | `{attempted:false, reason:"not_connected"}` | untouched |
| Not TikTok | `{attempted:false, reason:"not_tiktok"}` | untouched |
| Monthly cap reached | `{attempted:false, reason:"import_cap"}` | untouched, **no vendor call made** |
| HTTP 429 | stored row, `errorCode:"rate_limited"` | untouched |
| HTTP 401/403 | stored row, `errorCode:"unauthorized"` | untouched |
| Any other non-2xx | stored row, `errorCode:"http_<n>"` | untouched |
| Empty or unparseable body | stored row, `errorCode:"empty"` | untouched |
| 10s timeout | stored row, `errorCode:"timeout"` | untouched |
| Network error | stored row, `errorCode:"network"` | untouched |
| Even the store write fails | `{attempted:true, ok:false, errorCode:"capture_failed"}` | untouched |

The outermost `try` wraps everything including the database write, so there is no path out of this function that is an exception. **It is structurally incapable of blocking, slowing or breaking a clip**, and it is not called from any existing clip path in this round.

### The import cap

A self-imposed ceiling of **100 captures per calendar month**, counted from our own stored rows and checked **before** the vendor call, matching BL-772's finding that the plan caps imports at 100 posts against roughly 308 TikTok clips a month. At the cap the function returns `import_cap` without calling the vendor. The owner sees how close he is by counting rows in one table.

**Honest caveat, carried from BL-772 verbatim:** *"What counts as an import, whether a refresh recounts, and whether analytics-only reads count at all are UNVERIFIED."* So this is a ceiling on **our** calls, not a mirror of the vendor's accounting, and it is probably stricter than it needs to be, which is the safe direction to be wrong in.

**Unconnected clippers are skipped before anything is spent.** There is nothing to capture and a certain miss must not cost quota.

---

## PART 3 — THE DISPLAY

`ClipAnalyticsCard`, rendered in the admin clip queue beside BL-666's `ReviewerNoteCard`.

### Facts, and nothing else

> Average time watched 1.2 seconds. Clip duration 14 seconds.
> Watched to the end by 8% of viewers.
> Total time watched 57,600 seconds.
> Reached 41,200 people. Views 48,000. Profile views from this post 12.
>
> **Where views came from** — For You 11%, Search 2%, Others 87%
> **Where viewers were. Campaign target: United States.** — United States 91%, Canada 4%
> **Change between captures, {first} and {latest}** — Reach 12,400 → 31,900, **up 19,500**
>
> *Numbers as captured from TikTok for this clip. No score, no rating, nothing judged. No status, earnings or payout touched. The clipper sees none of this.*

*(Those figures are illustrative of the layout. No real capture exists, and the card renders nothing at all until one does.)*

### What is deliberately absent

**No score, no rating, no badge, no verdict pill, no threshold, no cutoff, no colour meaning good or bad, no bold-on-high.** BL-771 measured why rather than assuming it: against 206 clips a human had labelled bought, the best computable signal reached **20.2% precision** where beating the reviewer needs **99.2%**.

**The campaign's target country is a stated fact in a caption**, never a highlighted row, a match/mismatch cell, a sort key or a percentage-in-target. The accessibility lead flagged this as blocking and the reasoning is exactly right: **layout emphasis is a verdict without words.**

**No comparative or normative vocabulary.** Not "only", "just", "low", "unusually", "despite", "expected". The card says "Average time watched 1.2 seconds. Clip duration 14 seconds." and stops.

**Change is carried by a direction word**, `up` / `down` / `unchanged`, never green, red or an arrow. Up and down are facts about arithmetic; green and red are the judgement this card refuses to make.

### Absence, which most clips will show for a long time

Three states, never merged, and **no icon on any of them**, because an `AlertTriangle` or a dashed amber border reads as a defect in the clip:

> **Not connected** — "Analytics are captured only when a clipper connects their TikTok account. This clipper has not connected one, so there is nothing to show."
> **Connected, nothing captured yet** — "Connected on {date}. No capture has run for this clip yet."
> **Capture returned nothing** — "The last capture did not return data on {timestamp}."

The wording states the mechanism and stops. It never negates a suspicion, because *"this does not mean anything is wrong"* plants the idea it denies.

---

## PART 4 — WHAT DOES NOT LEAK

**Nothing reaches a clipper.** `grep -c` for `ClipAnalyticsCard`, `clip-analytics`, `clipAnalyticsSnapshot` and `clip_analytics_snapshots` across `api/clips`, `api/earnings`, `api/payouts`, `(app)/clips`, `(app)/earnings` and `(app)/payouts` returns **0 files with any match**.

**The gate is server-side.** The read route calls `requireOwnerOrCapability("CLIP_VIEW")` and returns before a byte otherwise. A render-only gate leaks through the network tab. `rawPayload` is not even selected, so an unvetted payload cannot leave the database.

**Nothing aggregates creators.** Every query is `where: { clipId }` for one clip belonging to one creator. There is no group-by, no percentile, no peer band and no cross-creator read anywhere in the diff. TikTok's prohibition is verbatim:

> "Extract reports of TikTok profiles and posts from authorized creators' accounts, and use the aggregated data to develop a self-built affiliate influencer marketing program (such as creator discovery and ranking)"

**BL-599's peer bands are not rebuilt on this data**, and must not be.

*(A correction: the brief cited BL-531 for the clipper-facing strip. **BL-531 does not exist** — this reports archive begins at BL-539. The live equivalent is CLAUDE.md's select-allowlist posture and `clip-sanitize.ts`, which this round matches by never selecting the field into a clipper response in the first place.)*

---

## PART 5 — THE EVIDENCE, AND WHAT IS ONLY STRUCTURAL

**Proven with real data:**

• The key authenticates and the organisation config was read live (PART 0 table).
• Three endpoint paths verified and one documented path disproved.
• `clip_analytics_snapshots` does **not** exist in production: `information_schema` returns **0**. The round wrote nothing.
• **Earnings invariant: 0 violations** across live approved clips.
• 5,353 live clips and 166 payout rows unchanged; newest payout `updatedAt` is `2026-08-10 23:45:53.265`, the day before this round.
• **0 active account connections**, which is why no capture could run.
• Money files byte-identical by blob OID: `clip-earnings-writer.ts` `ac5be7de`, `earnings-calc.ts` `797e2098`, `balance.ts` `e887f80a`, `tracking.ts` `83ce4bab`, `clip-earnings-invariant-middleware.ts` `61cef393`, `money-decimal.ts` `ef5cdae7`, `campaign-era.ts` `106e16ad`.
• No secret in the diff: `grep -c` for key assignments, `pk_live` and inline `x-api-key` values returns **0**.
• Gates, from logs with exit codes echoed directly: **`TSC_EXIT=0`, 0 errors**; **`BUILD_EXIT=0`**, compiled in 44s, and again at 88s after the BACKLOG commit; hooks gate **0 errors, 11 warnings**, at the ceiling and unchanged; **eslint confirmed present**, so the gate is real.
• Diff is real and non-empty: 5 files, **+883**.

**Proven only structurally, because no key-holding team exists:**

• That a capture stores a row with fields correctly marked present, absent or null. The classifier `buildSnapshotFields` and `classifyField` are pure and exported for exactly this reason, but **no real payload has ever been classified**.
• That a second capture is preserved rather than overwriting. The code path is `create`, never `update`, and the schema has no unique constraint on `clipId` that could force an upsert. **Not demonstrated on real rows.**
• That a fetch failure leaves the clip untouched. Guaranteed by construction (the function has no throw path and touches no Clip field), **not observed against a real outage**.
• That the card renders real numbers. It has never rendered one.
• **No browser render.** The admin queue needs an owner login I do not have, so the card's layout is unverified visually. Same honest limit as BL-762 and BL-765.

**Not wired into any clip path.** `captureClipAnalytics` is exported and called from nowhere in this round. That is deliberate: wiring a capture into the submit or tracking path before a single real response has been seen would be the fourth confidently-wrong round on this topic.

### Accessibility

Reviewed **before** any UI was written; all eight blocking items satisfied. `role="group"` with `aria-labelledby` rather than an N-times-repeated landmark; one `h4`; real `<table>` with `<caption>` and `scope` on both axes; **no `aria-live`, `role="status"` or `role="alert"` anywhere**; direction words instead of colour; and only `--text-primary`, `--text-muted` and `--text-secondary`, never `text-accent` (3.40:1 on the card in the live light theme) and never the emerald/amber/red clip-status palette, whose reuse would be a verdict in the reviewer's existing colour vocabulary.

**Two pre-existing defects disclosed, not fixed.** `admin/clips/page.tsx` carries exactly one heading (`h1` at line 1231) and no row `h3`, so this card and `ReviewerNoteCard` both sit at `h4` under an `h1`. Matching the existing sibling was chosen over half-fixing a 2,807-line file. Separately `ReviewerNoteCard` references `--bg-page`, which is defined nowhere and resolves to transparent.

---

## WHAT THIS ROUND DID NOT DO

• **It captured nothing**, because there is no team, no plan and no connected account.
• **It created no table in production.** The SQL is written and waiting.
• **It wired capture into no existing path.** One real response should be seen first.
• **It built no score, threshold, ranking or verdict**, and it must stay that way.
• **It changed no clipper-facing surface**, no money file, no status and no payout.

---

## VERIFICATION

The pipeline is declared UNVERIFIED in the first line, with the key's presence, its successful authentication and the exact missing prerequisites named. The store holds all nine fields nullable plus capture timestamp and per-field presence, applied via `generate` not `migrate`, storing every capture rather than overwriting, recording ABSENT distinctly from NULL and zero. Capture fails open on every enumerated path with the clip untouched, states its cap behaviour before spending a call, and skips unconnected clippers. The display shows watch time against duration, completion, impression-source mix, audience countries with the campaign target as a stated fact, and change between captures, with no score, rating or verdict, and three non-suspicious absence states. `grep` proves nothing reaches a clipper route and nothing aggregates creators. The 6 money files plus `tracking.ts` and `campaign-era.ts` are byte-identical by blob OID. No key was logged, printed or committed. The worktree is removed. What is proven with real data and what is only structural are separated above rather than blended. No dashes as bullets.
