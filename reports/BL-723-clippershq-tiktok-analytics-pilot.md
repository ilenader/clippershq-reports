# BL-723 — TikTok creator-authorized analytics: the pipe is BUILT, the proof is BLOCKED on the owner

**THE FIRST LINE, BECAUSE IT IS THE ONE THAT MATTERS: the live fetch was NOT run and is NOT claimed.** There is no TikTok developer app, `TIKTOK_BUSINESS_CLIENT_ID` / `TIKTOK_BUSINESS_CLIENT_SECRET` / `TIKTOK_BUSINESS_REDIRECT_URI` / `TIKTOK_BUSINESS_AUTHORIZE_URL` are all unset, and this round was forbidden from registering one. So `/business/video/list/` was never called, not once, and **PART 2's "which of the eleven documented fields actually arrive" is UNVERIFIED.** What this round did instead is build the entire pipe so that the moment the owner finishes the checklist below, the proof is two URLs and about ninety seconds.

**2026-08-06 · BUILD.** Base `origin/main` `de0169bd` (Merge BL-720) · branch `checkpoint/BL-723` @ `cb5e633d`, **verified pushed** · tags `pre-BL-723` / `post-BL-723`. Isolated worktree at the short path `C:/b723`, `node_modules` never junctioned. **No developer app was registered, no API access was requested, and no credential was stored by this round. Zero calls were made to any TikTok endpoint.**

---

## WHAT THE OWNER MUST DO HIMSELF, AS A CHECKLIST

Nothing below can be delegated to an agent. Steps 1 to 4 are queues at TikTok; start them and walk away.

**1. Create a TikTok for Business account.** Go to `https://business-api.tiktok.com/portal` and register with an email (TikTok's own advice: use an alias such as `developers+tiktok@company.com` so the login is shareable) and a password, then confirm the emailed code.
Source: [Create a TikTok For Business account](https://business-api.tiktok.com/portal/docs?id=1738855099573250)

**2. Register as a developer.** Your developer profile must be APPROVED before an app can be created, or app creation errors out.
Source: [Register as a developer](https://business-api.tiktok.com/portal/docs?id=1738855176671234)

**3. Complete the Accounts API Access Application Form. This is mandatory and it is the real gate.** TikTok's own note, repeated on the Accounts API overview, the API reference, the FAQs and both insights endpoints: "starting **March 20, 2026** at 00:00 (GMT+0), developers must complete the Accounts API Access Application Form before submitting a new developer app or requesting a scope increase that includes the 'TikTok Accounts' permission scope."
**How the use case must be described, and this is not cosmetic.** TikTok's Accounts API overview lists as a **Prohibited Use**: "Extract reports of TikTok profiles and posts from authorized creators' accounts, and use the aggregated data to develop a self-built affiliate influencer marketing program (such as creator discovery and ranking), instead of using the TikTok One platform or API." TikTok also "reserves the right to revoke a developer's Accounts API access at any time without prior notice". So describe the use as **verifying the view count and post time of a video the creator themselves submitted, on their own account, at their own request, in order to pay them**, and do not use the words discovery, ranking, marketplace or leaderboard anywhere in the description.
Source: [Accounts API overview](https://business-api.tiktok.com/portal/docs?id=1737944384433218)

**4. Create the developer app.** Fields TikTok asks for, in its order:
• **App name.** Something descriptive, for example "Clippers HQ payout verification".
• **App description.** TikTok asks for two things explicitly: **Intended Uses** ("Describe the key intended functions and usage scenarios ... Explain what core permissions are technically required") and **Developer App Access Controls** ("Clarify whether the developer App access is limited only to internal organizational use, or shared with other external accounts"). Answer the second honestly: it is used by creators outside your organization who opt in.
• **Advertiser redirect URL.** Required by the form even though this pilot does not use the advertiser flow. Any valid URL you control.
• **TikTok account holder redirect URL.** **This is the one that matters.** Set it to exactly `https://clipershq.com/api/admin/tiktok-connect/callback/` (with the trailing slash). TikTok's six formatting rules, all enforced locally by `validateRedirectUri` in this round's code so a bad value is caught before a live authorization: absolute and ending with `/`; no query parameters; no `#` anchor; must start with `https://`; no port; 10 to 512 characters.
• **Scope of permission.** Tick **"TikTok Accounts"**, and within it the scopes this pilot needs: **`video.list`** (gives `item_id`, `create_time`, `caption`, `share_url`, `embed_url`, `thumbnail_url`, `video_duration`, `likes`, `comments`, `shares`, `favorites`, `reach`, `video_views`, `media_type`, `is_ad`) and **`video.insights`** (gives `full_video_watched_rate`, `total_time_watched`, `average_time_watched`, `impression_sources`, `audience_countries`, `audience_genders`, `audience_cities`, `audience_types`, `video_view_retention`, `engagement_likes`, `new_followers`, `profile_views`). Do not tick more than you need: narrowest-scope is a stated review criterion on every platform.
• **App logo.** A JPG, JPEG or PNG no larger than 512 x 512. **Not optional in practice:** TikTok's Authorization doc states that if you skip it, "users will see an error page when they try to authorize the app."
**Review time: "The review may take 2 to 3 business days."** Each developer may hold up to five apps.
Source: [Create a developer app](https://business-api.tiktok.com/portal/docs?id=1738855242728450) · [Accounts API Authorization](https://business-api.tiktok.com/portal/docs?id=1738083939371009)

**5. Copy four values out of the portal** (My Apps > App Detail > Basic Information): the **App ID**, the **Secret**, and the **TikTok account holder authorization URL** (a ready-made `https://www.tiktok.com/v2/auth/authorize?...` link that TikTok generates; if it is missing, go to Authorization > Scope of permission and confirm "TikTok Accounts" is enabled). Then set five Railway variables:

| Variable | Value |
|---|---|
| `TIKTOK_BUSINESS_CLIENT_ID` | the App ID |
| `TIKTOK_BUSINESS_CLIENT_SECRET` | the Secret |
| `TIKTOK_BUSINESS_REDIRECT_URI` | `https://clipershq.com/api/admin/tiktok-connect/callback/` |
| `TIKTOK_BUSINESS_AUTHORIZE_URL` | the portal's TikTok account holder authorization URL, pasted verbatim |
| `OAUTH_TOKEN_ENC_KEY` | a NEW 64-hex-character random value. **Not `WALLET_ENC_KEY`.** Generate with `node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"` |

**6. On the phone, on the TikTok account being connected:** publish at least one video, then open the Analytics page and tap **"Turn On"**. TikTok's own words on both insights endpoints: "To view insights and analytics data, TikTok account owners need to first publish at least one video, then tap the 'Turn On' button on the Analytics page of their mobile TikTok app." **You do NOT need to switch to a Business account** (BL-722 established that every field this platform needs is TikTok-Studio-sourced, and only the Business-Analytics-sourced fields carry the Business-only note).

**7. Then run the pilot** (PART 2 below): open `/api/admin/tiktok-connect/start?force=1`, approve, and open `/api/admin/tiktok-connect/fetch?id=<the id the callback prints>`.

### Sandbox versus production, said plainly

TikTok publishes **Sandbox accounts** for the API for Business, but the pilot cannot usefully run there and this round will not pretend otherwise. A sandbox account is a synthetic advertiser environment; **the thing this pilot must prove is that a REAL creator's REAL analytics arrive for a REAL video posted minutes ago**, and a synthetic account has no TikTok Studio history, no `reach`, no `full_video_watched_rate` and no `impression_sources` to return. **Nothing about the 24-to-48-hour delay, the 7-day-inactive hole, or the real-time-ness of `create_time` can be tested in a sandbox.** So the honest position is: this pilot requires an approved production app, and until step 4 clears review there is no partial result to report. If the Accounts API access form is refused, the TikTok branch of BL-722's plan stops entirely; there is no second route to these fields, because the Display API at `open.tiktokapis.com` returns counter metrics only.

---

## PART 1 — THE CONNECT FLOW, BUILT

Nine files, four routes, all OWNER-only, all new. No existing file was edited except `prisma/schema.prisma`.

| File | What it is |
|---|---|
| `src/lib/tiktok-business/config.ts` | env read at CALL TIME, the kill switch, the field list, TikTok's six redirect-URL rules enforced locally |
| `src/lib/tiktok-business/token-crypto.ts` | AES-256-GCM under `OAUTH_TOKEN_ENC_KEY`, fails closed |
| `src/lib/tiktok-business/oauth.ts` | HMAC-signed CSRF state, `auth_code` exchange, refresh, revoke |
| `src/lib/tiktok-business/client.ts` | the `/business/video/list/` call, the field classifier, the redactor |
| `src/lib/tiktok-business/connection-store.ts` | storage, refresh-on-use, failure counting, disconnect |
| `src/app/api/admin/tiktok-connect/route.ts` | GET status, DELETE disconnect |
| `src/app/api/admin/tiktok-connect/start/route.ts` | redirect to consent |
| `src/app/api/admin/tiktok-connect/callback/route.ts` | consent return, exchange, store |
| `src/app/api/admin/tiktok-connect/fetch/route.ts` | the single fetch, redacted by default |

**The flow.** `GET /api/admin/tiktok-connect/start?force=1` verifies OWNER, refuses with a 503 and a list of MISSING ENV NAMES (never values) if anything is unset, then redirects to the portal-generated authorize URL with a signed `state` appended. TikTok returns to the registered redirect with `auth_code` (**valid 10 minutes, single use**) and the echoed `state`. The callback verifies OWNER, verifies the state's HMAC and its age, exchanges the code at `POST /open_api/v1.3/tt_user/oauth2/token/`, encrypts both tokens, upserts one row, and returns a summary that contains **no token and not even the raw `open_id`** (it is replaced by a stable opaque `acct_*` reference).

**Why the authorize URL is an env var rather than a URL this code builds.** TikTok does not document a parameter set for the account-holder authorize URL. Its Authorization guide says the developer takes the ready-made "TikTok account holder authorization URL" from the portal and shares it. Synthesising a query string here would be a guess printed as a fact, so the owner pastes TikTok's URL verbatim and this code appends only `state` (which TikTok documents as supported: "you can add a unique `state` query parameter ... It will be echoed back to your application") and, on `force=1`, `disable_auto_auth=1`.

**A detail worth knowing before the first attempt, and it is why `force=1` exists.** TikTok: "By default, if the TikTok account user has previously authorized the developer app for the same permissions, the permission scope review and approval page in Step 2 will be skipped. Instead, the TikTok account user will be directly redirected to the redirect URL." A second run would therefore silently skip the very screen the pilot is meant to read.

**A second detail, flagged rather than glossed.** TikTok requires the registered redirect URL to end in `/`. This app runs with Next's default `trailingSlash: false`, so Next answers `/api/admin/tiktok-connect/callback/` with a 308 to the slash-less form, and a 308 preserves the query string, so `auth_code` arrives intact. That is standard behaviour and the handler reads `auth_code` from the query either way, but **the end-to-end redirect is UNVERIFIED until the owner runs it once**, because no app exists to run it against. If it ever failed, the one-line fix is a `redirects()` entry in `next.config.ts`.

### What the clipper sees on the consent screen

**UNVERIFIED, and it will not be invented here.** The real flow could not be run. TikTok's Authorization documentation shows the screen only as a screenshot, so its literal wording is not extractable from the docs either. What IS documented, and is quoted: the account user "reviews and approves the authorization request"; the page is a "permission scope review and approval page"; on approval they "are redirected to the application's specified redirect URL, with an authorization code included"; and "The TikTok account user can revoke the authorization at any time from within the TikTok app."
**What would settle it:** the owner running step 7 with `force=1` and screenshotting the screen. That is the first thing the next round should capture.

### Token storage, and a correction to the premise

**The brief says BL-656 recorded the owner declining wallet encryption. That is not what BL-656 says, and the difference changes the design.** BL-656's own words: the scheme is "AES-256-GCM (`src/lib/wallet-crypto.ts:33-38`), which is reversible encryption, not a hash", the key `WALLET_ENC_KEY` is "live in production (81 rows are already encrypted, which is only possible with the key set)", and what was deferred is **dropping the plaintext column**: "Key loss is only catastrophic AFTER the plaintext column is dropped. That is precisely why the plaintext net must stay until the key is proven backed up." Encryption was not declined. A one-way step was postponed.

**And that reasoning does not transfer to a token, which is the whole point.**

| | Wallet address | OAuth token |
|---|---|---|
| Replaceable? | **No.** It is the only route to a person's money. | **Yes.** One re-authorization regenerates it. |
| Cost of key loss | The owner cannot pay someone. | One reconnect prompt per account. |
| Correct posture | Keep a plaintext net until the key is proven backed up (BL-656). | **No plaintext, ever.** |

So `token-crypto.ts` uses the same algorithm as `wallet-crypto.ts` and inverts its failure mode: **`encryptToken` THROWS when `OAUTH_TOKEN_ENC_KEY` is missing or malformed**, `saveConnection` refuses the connection rather than storing a credential in the clear, and **there is no plaintext token column in the schema and there never will be** (proven: `information_schema` reports **0** columns named `accessToken` or `refreshToken` on the new table). For a credential, a plaintext fallback is not a safety net, it is the leak the encryption exists to prevent.
**If the key is lost or rotated:** every stored token stops decrypting, `decryptToken` returns null rather than garbage (harness-proven under a deliberately wrong key), the connection reports itself unusable, and each affected account reconnects once. Nothing is destroyed, no money moves, and nobody is blocked from anything while it happens. A separate key from `WALLET_ENC_KEY` is deliberate: different blast radius, different rotation cadence, and rotating one must not touch the other.
**No token is ever logged.** The feature contains **0** `console.*` statements of any kind (asserted by the harness, not by inspection), the token travels in an `Access-Token` header and never in a URL, error objects carry a code and a reason and never a value, and the connection summary strips both the ciphertext and the raw `open_id`.

### Refresh, revocation, expiry, and the promise that none of it can hurt a clipper

Lifetimes are TikTok's, verified in BL-722: `auth_code` **10 minutes** single use, access token **1 day** (`expires_in: 86400`), refresh token **1 year** (`refresh_token_expires_in: 31536000`) and **rolling**, since a refresh returns a new refresh token.

`getUsableAccessToken` refreshes when the access token is within **one hour** of expiry, via `POST /tt_user/oauth2/refresh_token/`, and re-encrypts both new tokens. Every failure path returns a value rather than throwing:

| Situation | What happens |
|---|---|
| Refresh call fails | `lastRefreshError` records a REASON (never a token), `consecutiveRefreshFailures` increments, the caller gets `ok:false` |
| 3 consecutive failures | the row stays but reports `usable:false`, which in a later round becomes exactly ONE reconnect prompt, worded as a reconnection request and never as suspicion (BL-521) |
| Refresh token expired (1 year unused) | stamped and reported; the account authorizes again |
| Token undecryptable (key lost or rotated) | reported as needing a reconnect, with the explicit note that nothing is lost |
| Clipper revokes in the TikTok app | the next refresh fails and the row parks itself; the clipper needed no prompt from us to do it |
| Owner disconnects | TikTok is told via `POST /tt_user/oauth2/revoke/` (best effort), **both ciphertext columns are emptied**, `revokedAt` is stamped, and nothing retries it |

**The promise, and it is structural rather than a policy sentence: a token failure cannot block a clipper from earning, tracking, submitting or withdrawing, because no code on any of those paths can call into this feature at all.** PART 4 proves that by grep. The `fetch` route answers a dead connection with **HTTP 200 and a verdict**, never a 5xx, the same discipline BL-689 built for typed payout refusals after three clippers holding $52.86 were told to retry a permanent condition.

---

## PART 2 — THE FETCH, AND THE PROOF THAT COULD NOT BE PRODUCED

**BLOCKED. No raw response is pasted here, because none exists.** Pasting an invented response, or a sample from TikTok's documentation dressed up as a live capture, would be exactly the failure this round was warned against.

**What was built and is ready to run:**

```
GET /api/admin/tiktok-connect/fetch?id=<connectionId>&max=<1..20>&cursorMs=<epochMs>
```

It requests, in one call: `item_id`, `create_time`, `caption`, `share_url`, `video_duration`, `video_views`, `likes`, `comments`, `shares`, `reach`, `full_video_watched_rate`, `total_time_watched`, `average_time_watched`, `impression_sources`, `audience_countries`. It returns `httpStatus`, TikTok's `code`, `latencyMs`, the `X-Tt-Logid` request id, `returnedPosts`, `hasMore`, `nextCursor`, a per-post `fieldReport`, and the response **redacted by default** (captions, share URLs, embed URLs, thumbnail URLs and post ids become `[REDACTED len=N refXXXX]`; every number, percentage and distribution survives untouched, because those are the evidence). `raw=1` returns the unredacted body for the owner's own screen and is not what goes in a report.

**The classifier is three-valued on purpose, and this is the part that makes the eventual answer trustworthy:**
• **present** the key exists and carries a usable value (`0` counts as present: zero comments is data)
• **null** the key exists and TikTok returned null or an empty array, which is the 24-to-48-hour case or the 7-day-inactive case
• **absent** the key is not in the object at all, which means the scope was not granted or the field is not supported
Merging null and absent would turn "we were not granted `video.insights`" into "TikTok has no data yet", and those need completely different fixes. The harness proves all three cases plus the empty-array-is-null and zero-is-present edges.

**The three experiments, written out so the owner can run them in order the day the app is approved:**

**Experiment A, the eleven fields.** `fetch?id=<id>&max=5`. Read `fieldReport`. **What BL-722 predicted from the documentation:** all eleven return, with `video_views`, `likes`, `comments`, `shares`, `reach`, `video_duration`, `full_video_watched_rate`, `total_time_watched`, `average_time_watched`, `impression_sources` and `audience_countries` on a T+24-to-48-hour delay. **The result to record: for each field, present / null / absent, plus the post's age.** If any field is `absent` rather than `null`, the cause is a scope, not a delay.

**Experiment B, is `create_time` genuinely real-time.** Post a video, wait long enough to submit it in the app, then call `fetch?id=<id>&max=1` within minutes. The route already computes `ageSeconds` per post. **The whole 30-minute freshness design rests on this**: TikTok's latency table puts `item_id`, `create_time`, `thumbnail_url`, `share_url`, `embed_url` and `caption` in the "No" latency row, which is what would let submit-time prove ownership, existence and exact post time with zero delay while the view count arrives later. **Expected: the minutes-old post appears, `create_time` matches the real post time, `ageSeconds` is in the hundreds, and every metric field is null.** If the post does not appear at all within the freshness window, the design in BL-722 PART 1.7 is wrong and the product plan changes.

**Experiment C, the 7-day-inactive hole.** `fetch?id=<id>&max=20&cursorMs=<a timestamp ~30 days ago>` to page back to an old, quiet post. TikTok: "If the data for the fields `reach`, `full_video_watched_rate`, `total_time_watched`, `average_time_watched`, `impression_sources`, and `audience_countries` are unavailable, the reason is usually that the video has not been active ... for more than 7 days." **`video_views` is deliberately NOT on that list**, so the money metric should survive while the quality detail goes null. **The result to record: which of those six are null on an old post, and whether `video_views` is still present.**

**Every one of the three is UNVERIFIED today.** What settles all three: the owner completing the checklist. Nothing else.

---

## PART 3 — RATE LIMITS, QUOTA, AND THE PROJECTION

**Observed rate limits: NONE. Zero calls were made, so nothing was observed.** What follows is TikTok's documented ceiling and this round's own arithmetic, labelled as such.

**Documented ceilings** ([Accounts API rate limits](https://business-api.tiktok.com/portal/docs?id=1738084416214017), [global rate limits](https://business-api.tiktok.com/portal/docs?id=1740029171730433)): **40 QPM per authorized TikTok account per endpoint**; **600 QPM across all Accounts API endpoints combined** at the default Basic app level (1,000 at every higher level); global Basic **10 QPS / 600 QPM / 864,000 QPD**. Throttling returns `"code": 40100`; a QPM throttle needs a 5-minute pause, a QPD throttle waits until 00:00 UTC.

**Quota consumed by one account fetch: exactly ONE call**, returning up to `max_count` posts (**maximum 20**, default 10). Because `cursor` is a UTC millisecond timestamp that pages backwards, a specific clip is reachable by passing its submit time rather than by walking the back catalogue, so the normal cost of checking one clip is **one call, not one call per page**.

**The projection. First, a correction to the brief's numbers**, measured read-only on prod at DB `now()` = `2026-08-06 13:40:39.724906+00`:

| The brief says | Measured today |
|---|---|
| about 2,300 clips a month | **1,659** clips in the last 30 days |
| about 1,240 clippers | **101** clippers submitted in 30 days; **1,321** registered users; **528** hold any account |
| TikTok share | **361** TikTok clips / 30d from **51** clippers; **305** APPROVED TikTok accounts across **266** users |

**"100 percent adoption" therefore means 305 connected accounts, not 1,240.** Against the ceiling:

| Design | Calls/day | Even QPM | Share of 864,000 QPD (Basic) | Share of 600 QPM |
|---|---|---|---|---|
| 305 accounts, one page, hourly | **7,320** | ~5 | **0.85%** | **0.85%** |
| 305 accounts, one page, every 15 min | **29,280** | ~20 | **3.4%** | **3.4%** |
| Plus one same-hour recheck per new TikTok clip (~12/day) | +12 | negligible | negligible | negligible |
| **The brief's hypothetical 1,240 accounts, hourly** | **29,760** | ~21 | **3.4%** | **3.4%** |

**Where the ceiling actually is, and what happens at it.** The binding limit is **600 QPM app-wide, which is 864,000 calls a day**; hourly polling of every TikTok account on the platform uses under one percent of it, and even the brief's inflated 1,240-account case uses 3.4%. The per-account 40 QPM limit is never approached because a given account is touched once an hour. **At the ceiling TikTok returns `code: 40100` and the correct response is to stop for five minutes, not to retry**, which is why the client returns a typed failure carrying `apiCode` rather than throwing. The realistic constraint on this integration is **adoption, review and clipper friction, not quota.**

**Cost: $0.** TikTok publishes no per-call price for the Accounts API. This round spent nothing because it called nothing.

---

## PART 4 — WIRED INTO NOTHING, PROVEN BY GREP

| Proof | Command shape | Result |
|---|---|---|
| Nothing outside the feature imports it | `grep -rlE 'from "[^"]*tiktok-(business\|connect)' src` minus the feature dirs and the gitignored generated client | **0** |
| Nothing outside the feature even MENTIONS it | same, any mention | **0** |
| No clipper-facing UI exists | `find src/lib/tiktok-business src/app/api/admin/tiktok-connect -name '*.tsx'` | **0** |
| No token can be logged | `grep -rE 'console\.(log\|error\|warn\|info\|debug)'` across the feature | **0** |
| Every route is OWNER gated | route files containing `requireOwner(` / total route files | **4 / 4** |
| The feature imports no money, tracking, submit, fraud, bot-alert or reviewer-note module | harness guard G2 over 16 forbidden module names | **0 violations** |
| Money files in the diff | `git diff --name-only de0169bd..HEAD` filtered to the 6 money files + `tracking.ts` + `campaign-era.ts` | **0** |

The single match anywhere in `src/` for the string `tiktok-business` outside the feature is `src/generated/prisma/internal/class.ts`, which is **gitignored** (confirmed with `git check-ignore`) and merely embeds the schema text, including my model's comment. It is a generated artifact, not an import.

**Money files, byte-identical by blob OID on BOTH refs** (`git rev-parse de0169bd:<f>` vs `git rev-parse HEAD:<f>`):

| File | Blob OID (identical on both refs) |
|---|---|
| `clip-earnings-writer.ts` | `ac5be7deb061768fec800aa89aae512a56a9e065` |
| `earnings-calc.ts` | `797e20985ad57475ef321afcf3cb1ea7b0d6ab84` |
| `balance.ts` | `e887f80acfc70fee438e719a32a60025eda22749` |
| `tracking.ts` | `83ce4babfd39a6261114465639f2eac4e23bfceb` |
| `clip-earnings-invariant-middleware.ts` | `61cef39395363c31f0c902dd4c64e8c06b3e6449` |
| `money-decimal.ts` | `ef5cdae757b9ad3c23380ee8b63e279f98d0b6ac` |
| `campaign-era.ts` | `106e16ad75125c3b10b6949a2981d33614c69ab9` |

**Exactly ONE tracked file was modified in this round: `prisma/schema.prisma`.** Everything else is new. No Apify actor ran and the 11 BL-678 guards are untouched.

**Prod money census after the schema apply** (read-only, `::text` against DB `now()`): **4,915** clips, **3,886** approved, **$11,449.53** total earnings, **0 invariant violations**, **155** payout requests, newest clip write `2026-08-06 13:18:50.449` which **predates** the schema apply at `13:40:39`, so the last write to a clip was the tracking cron and not this round. **No clip status, earning or payout changed.**

**Schema.** One new table `clip_account_connections`: **17 columns, 0 rows, 0 foreign keys, 0 plaintext token columns**, applied with `CREATE TABLE IF NOT EXISTS` via `scripts/run-schema-sql.js` (4 statements) and `npx prisma generate` only, **never `prisma migrate`**. `clipAccountId` is a plain nullable indexed key, not a Prisma relation, so `ClipAccount`, `Clip` and `User` were not edited (harness guard G5d).

**Gates, honestly.** `npm ci` exit 0. `npx prisma generate` run BEFORE tsc because `npm ci` wipes the generated client. `npx tsc --noEmit` **exit 0, 0 lines of output**. `npm run build` **exit 0**, read from a redirected log with the exit code echoed by hand and never piped through `tail`, 61/61 pages, "Compiled successfully in 31.8s". prebuild gates: prisma-bypass **0 violations**, removed-fields **OK across 703 files**, **lint:hooks 0 errors / 11 warnings** at the cap, with **eslint v9.39.4 confirmed executing** so the gate is not a silent no-op. Offline harness `scripts/bl723-verify.ts`: **73 passed, 0 failed**, exit 0, covering crypto round-trip, random-IV divergence, tamper rejection, wrong-key nulling, refusal-to-encrypt-without-a-key, state signing and expiry and future-dating, all six TikTok redirect-URL rules including both length bounds, three-valued field classification, redaction with numeric preservation and reference stability, summary-carries-no-token, and the five static guards. **The `.ts` diff is genuinely non-empty (9 new source files plus a schema edit), so this is a real code change and not a document.**

**No accessibility review was needed and none is claimed: this round added zero `.tsx` files and zero markup.** Every surface is a JSON API route. The moment a clipper-facing connect button is designed (BL-722's step 5), it goes to the accessibility lead first.

---

## PART 5 — THE VERDICT AND THE NEXT STEP

**ONE LINE: it is UNKNOWN whether real analytics arrive with real values, because no TikTok developer app exists, so not a single call was made, and this round refuses to report a pilot it could not run.**

**Which fields are trustworthy, delayed, or absent: UNVERIFIED, all of them.** What can be said is the shape of the answer the next run will produce and what BL-722's documentation reading predicts:

| Class | Fields | Predicted from docs | Status |
|---|---|---|---|
| Real-time, no latency | `item_id`, `create_time`, `caption`, `share_url`, `embed_url`, `thumbnail_url` | present immediately, which is what makes the 30-minute freshness window survivable | **UNVERIFIED** |
| T + 24 to 48 hours | `video_views`, `likes`, `comments`, `shares`, `reach`, `video_duration`, `full_video_watched_rate`, `total_time_watched`, `average_time_watched`, `impression_sources`, `audience_countries` | null at first, populated within two days | **UNVERIFIED** |
| Lost after 7 days of inactivity | `reach`, `full_video_watched_rate`, `total_time_watched`, `average_time_watched`, `impression_sources`, `audience_countries`, but **NOT `video_views`** | quality detail goes null, the money metric survives | **UNVERIFIED** |

**Is reality narrower than the documentation promised? Unknown, and that is the honest answer.** BL-722 verified what TikTok SAYS. This round was meant to verify what TikTok DOES, and it could not, so the gap between the two remains exactly where BL-722 left it. **Everything downstream in BL-722's plan still depends on this being measured, and no product surface should be built until it is.**

**What this round did prove, and it is not nothing:** the pipe compiles, the crypto is correct under rotation and tampering, the CSRF state cannot be forged or replayed past 10 minutes, TikTok's six redirect-URL rules are enforced before a live authorization rather than after a failed one, a redacted response is safe to publish while keeping every number intact, and the whole feature is provably unreachable from any clipper-facing surface and from every money path.

### The next round, precisely

**BL-724 does not exist until the owner has done steps 1 to 6.** It is not an engineering round, it is a queue. When the app is approved:

1. **Run the three experiments** in PART 2, in order A, B, C, and paste the redacted `fieldReport` for each. One round, mostly waiting, no code.
2. **Screenshot the consent screen** on the `force=1` run, so PART 1's UNVERIFIED line closes.
3. **Only if Experiment B confirms `create_time` is real-time:** design the clip-to-`item_id` match. This is the first real engineering problem and it is not trivial, because **69% of stored TikTok clip URLs are `/t/` short links** (BL-662) which carry no `item_id`. The likely answer is to match on `create_time` within the submission window plus `video_duration`, rather than resolving the short link, but that is a design decision that needs Experiment B's data first.
4. **Then, and only then**, BL-722's step 4: shadow read, owner-only, comparing the official `video_views` against what LamaTok reports for the same clip, for a measured period, with nothing deciding anything.

**Where this stops:** if the Accounts API Access Application Form is refused, the TikTok branch ends here and the code shipped in this round becomes dead weight to be reverted. That is a real possibility given the prohibited-use clause, which is why step 3 of the owner checklist matters more than any line of code in this round.

---

## Disclosure

**API calls to any platform: ZERO.** No TikTok, Meta or Google endpoint was called, no documentation was re-fetched (BL-722's citations are reused), no Apify actor ran, no HikerAPI or LamaTok call was made. **Cost of this round: $0.** Database: one schema apply (4 statements, `CREATE TABLE IF NOT EXISTS` plus 3 `CREATE INDEX IF NOT EXISTS`) and three read-only `SELECT`s via `scripts/run-select.js`, all timestamps cast `::text` against DB `now()`. **No developer app was registered, no API access was requested, and no credential was created or stored.** No token exists anywhere in this repository, this report, this round's commits, or the database. No handle, caption, wallet address, email or personal string appears above. `.env` and `.env.local` were copied into the worktree for the build and the read-only SELECT runner and are confirmed gitignored, so they cannot be committed. Nothing a live round holds was touched (the `main` working tree is held by worktree `C:/b575`; this round never checked out `main`). **No dashes as bullets.**

**Rollback:** `git revert -m 1 <merge>` once merged, or `git reset --hard pre-BL-723`. The new table is additive, empty, and read by nothing else, so nothing needs dropping; `DROP TABLE IF EXISTS clip_account_connections;` afterwards if wanted.
