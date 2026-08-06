# BL-724 — The privacy policy stops lying, and the TikTok submission gets a map

**2026-08-06 · Base:** `main @ de0169bd` · **Branch:** `checkpoint/BL-724`
**Nothing was registered. Nothing was submitted. No credential was stored. BL-723 was NOT merged and NOT deployed.**
**DB access this round: `run-select.js` only (refuses every write keyword). No clip's earnings or status changed.**

---

## THE HEADLINE, BEFORE ANYTHING ELSE

**The app you are submitting and the code BL-723 wrote are for two different TikTok platforms.**

BL-723's code calls `business-api.tiktok.com/open_api/v1.3` with scopes `video.list` + `video.insights`.
That is the **TikTok API for Business (Accounts API)**, and TikTok's own documentation says its apps are
created at `ads.tiktok.com/marketing_api/apps/` after registering a TikTok For Business account. You are
submitting a **Login Kit** app at `developers.tiktok.com` with `user.info.basic` + `video.list`. Different
portal, different endpoint host, different auth header, different scope namespace. **The Login Kit app you
are submitting will not work with BL-723's code as it stands.**

**That is fine, and you should still submit the Login Kit app.** TikTok's own Video Object documentation
lists `view_count`, `like_count`, `comment_count`, `share_count`, `create_time`, `share_url`, `duration`
and `id` as fields you can request on the Display API's `/v2/video/list/` under the `video.list` scope.
That is the entire earnings requirement. **One app is enough.** Details and citations in PART 2.

**And the likeliest single cause of rejection is not a scope or a policy. It is your website URL.** TikTok
requires the Privacy Policy and Terms of Service links to be visible on the registered website URL without
opening a menu, and requires that the URL not be a landing or login page. `https://clipershq.com/` sends a
logged-out visitor to `/preview`, which has **no legal links at all**. PART 2.7 and PART 4 step 2.

---

# PART 1 — THE PRIVACY POLICY

## 1.1 What was false

| Claim in the live policy | Reality | How it was verified |
|---|---|---|
| "Apify (public clip stat tracking)" | Apify is off by construction | `src/lib/apify-hard-off.ts` exports `APIFY_HARD_OFF: true` as a `const` that reads **no** environment variable, so no value in Railway or a `.env` can re-enable it (BL-678). Confirmed against the production DB: the last `apify_usage_entries` row from any `actor:apify/*` provider is **2026-07-29**; nothing since. |
| "Vercel (application hosting)" | Railway is the host | Live response headers on `https://clipershq.com/preview`: `Server: railway-hikari`, `x-railway-request-id: nNc9AQxkQ8mZ7UJu5nX1uw`, `x-railway-edge: ams1`. Zero Vercel headers, zero occurrences of the string `vercel` in the served page. |

I did not take BL-678 or BL-654 on trust. Both were re-verified from the code and from live evidence.

## 1.2 What the processor list is now, and the evidence for each line

Every entry below is a measurement, not an inference.

| Processor | What it is used for | Evidence |
|---|---|---|
| Discord | Sign in, plus server roles and campaign announcements | `next-auth/providers/discord` in `src/lib/auth.ts`; `DISCORD_BOT_TOKEN` read by `src/lib/discord-bot.ts`, the role-reconcile cron and marketplace broadcast |
| Railway | Application hosting | Live response headers, above |
| Supabase | Database hosting and file storage | `DATABASE_URL` points at Supabase; the live page serves `supabase.co/storage/v1/object/public/uploads/...` image URLs |
| Resend | Transactional email | `resend` dependency, `EMAIL_API_KEY`, `RESEND_WEBHOOK_SECRET`, `EmailSuppression` fed by the Resend bounce webhook |
| Sentry | Error and performance monitoring | Live page source carries `sentry-environment=production` and a `sentry-release` equal to the deployed commit `de0169bd` |
| HikerAPI | Public Instagram post statistics | `apify_usage_entries`, provider `hikerapi-v2`, **20,909 rows** in 14 days, latest **2026-08-06 13:01:15** |
| LamaTok | Public TikTok post statistics | Same table, providers `lamatok-tiktok-only` (660) + `lamatok-tiktok` (265), latest **2026-08-06 13:01:12** |
| Google, via the YouTube Data API | Public YouTube post statistics | Same table, provider `youtube-api-batch`, **534 rows**, latest **2026-08-06 13:01:12** |
| ScrapeBadger | Public TikTok and YouTube profile info for account verification | `creator_scans` rows for provider `scrapebadger`, latest **2026-08-05 08:21** |
| TikHub | Public Instagram profile info for account verification | `creator_scans` rows for provider `tikhub`, latest **2026-08-06 05:42** |

**The one entry I could not settle from outside: Ably.** `/api/ably-token` is auth-gated, so I cannot probe it,
and the public pages do not load it. It is imported on every logged-in page and `src/lib/ably.ts` no-ops
silently when `ABLY_API_KEY` is unset. I listed it, because over-disclosing a processor is harmless and
omitting a live one is not. **Settle it yourself in one command: `railway variables | grep ABLY_API_KEY`.**
If it is unset, delete that one line from the policy.

**Deliberately NOT listed, with reasons.** Anthropic (`SUPPORT_AI_ENABLED` defaults off, and the code
requires the literal string `"true"`); OCR.space, Browserless (optional, key-gated, absent from the env);
Google sign-in (registered only when `GOOGLE_CLIENT_ID` is set, and gated to pre-existing CLIENT users, a
role CLAUDE.md records as not yet built). **If you ever set `SUPPORT_AI_ENABLED=true`, Anthropic must be
added to Section 3 before you do it.**

## 1.3 The new Section 4 describes BL-723's code, not its intentions

I read all nine BL-723 files before writing a word of it. Each promise below is anchored to code.

| The policy says | The code that makes it true |
|---|---|
| "We never post, upload, edit, delete or schedule anything… We do not ask for the permission that would let us." | `TIKTOK_BUSINESS_REQUIRED_SCOPES = ["video.list", "video.insights"]` in `config.ts`. No publish or upload scope exists anywhere in the feature. This is structural, not a policy promise. |
| "We do not receive your TikTok password" | OAuth authorization-code flow only; `oauth.ts` exchanges an `auth_code` at `/tt_user/oauth2/token/`. No credential of the user's ever reaches us. |
| "only created after you… approve it on TikTok's own authorization screen" | `start/route.ts` redirects to TikTok's portal-generated authorize URL; `callback/route.ts` refuses without a valid HMAC-signed `state` and an `auth_code`. |
| "We store the access credential… encrypted" | `scripts/migrations/BL-723-clip-account-connections.sql` has **no plaintext token column**; both are AES-256-GCM ciphertext under `OAUTH_TOKEN_ENC_KEY`. `saveConnection` refuses to write at all when the key is missing. |
| "We ask TikTok to revoke the credential and we delete our stored copy" | `disconnect()` calls `revokeAccessToken` (best effort, hence "ask"), then sets `accessTokenEnc = ""` and `refreshTokenEnc = ""` and stamps `revokedAt`. |
| "We never share, sell or license TikTok data to any third party" | `fetch/route.ts` is `requireOwner` and returns to the caller only. Grep-verified in BL-723: zero imports of the feature outside itself. |

**What I deliberately did NOT promise, and why.** An in-app disconnect button. The only disconnect route
today is `DELETE /api/admin/tiktok-connect`, guarded by `requireOwner`, and BL-723 states plainly that the
feature has **zero `.tsx` files** — there is no clipper UI. Promising a button a clipper cannot see would be
exactly the aspirational overpromise you asked me to avoid. The policy therefore names TikTok's own
app-permissions screen first (always true, and TikTok's own documented revoke path) and email second.

## 1.4 Two code gaps, flagged and NOT fixed this round

1. **The connection row survives disconnect.** `disconnect()` clears the two ciphertext columns but the
   `clip_account_connections` row remains, still carrying `providerAccountId` — the TikTok `open_id`.
   The policy states this honestly rather than claiming erasure, and commits to removing it on an
   account-deletion request under Section 7. **That deletion is manual, so whoever runs it must now also
   delete this row.**
2. **No cascade.** `clipAccountId` is a plain nullable non-FK column (deliberately, mirroring BL-659), so
   deleting a user or a clip account will **not** remove the connection row automatically. If the feature
   ever ships to clippers, that becomes a real deletion-completeness gap and needs its own round.

## 1.5 One accessibility fix, disclosed

The `.updated` line was `#5a6a7a` on `#080c10` = **3.53:1**, a genuine WCAG 2.2 SC 1.4.3 failure for normal
text. It is now `#7a8a9a` = **5.54:1**. I was editing that exact line anyway. An accessibility review of the
page was run before the edit (the repo hook requires it) and its other required changes are applied: the `h3`
rule ships with the `h3` markup (without it, the browser default `1.17em` would have rendered h3 **larger**
than h2 because of the `*{margin:0}` reset), the back link is now visibly a link, and the `&larr;` is
`aria-hidden` so its accessible name is exactly "Back to Clippers HQ". The new Section 4 has `id="tiktok"`,
so you can point TikTok at `https://clipershq.com/privacy.html#tiktok` if a reviewer asks.

## 1.6 `TOS_VERSION` bumped v1 → v2

`src/lib/legal-version.ts` carries its own instruction: "Bump when public/terms.html or public/privacy.html
changes meaningfully." This qualifies. Both login pages write the cookie **from** the constant and both
signup paths compare **against** it, so the two sides move together. No existing user is re-prompted —
nothing compares `User.tosVersion` to the constant after `createUser` / `verify-magic-link`.

**Known 24-hour window, stated plainly:** a visitor who loaded `/login` before the deploy holds a `tos_accepted=v1`
cookie (max-age 86400). If they complete signup after the deploy, `createUser` sees `v1 !== v2` and stores no
`tosAcceptedAt`. **Signup is not blocked** and nothing else is affected. Not bumping was the worse option: it
would record new users as having accepted "v1" of a policy that materially changed.

## 1.7 Terms of Service — NO CHANGE NEEDED. Confirmed.

You were right. `public/terms.html` contains no processor list and no statement the TikTok integration
falsifies. §4 ("Earnings are calculated based on verified view counts") stays accurate. §10 already routes
data handling to the privacy policy, and the privacy policy is where TikTok's Developer Terms of Service put
the obligation: *"make a complete and accurate disclosure to your End Users of the privacy practices and
policies applicable to the Application."*
([TikTok Developer Terms of Service](https://www.tiktok.com/legal/page/global/tik-tok-developer-terms-of-service/en))

**One thing the ToS does need, and it is not a wording change: verification.** See PART 2.5.

## 1.8 Also found, REPORTED not changed

`vercel.json` still sits in the repo root with five cron entries. It is vestigial after BL-654 moved the
crons to Railway and BL-658 removed the `x-vercel-cron` auth. Harmless, but a reviewer who reads your repo
would find it confusing. Out of scope for this round.

---

# PART 2 — THE REVIEW REQUIREMENTS, FROM TIKTOK'S OWN DOCUMENTATION

Every citation below is a TikTok-owned page. No blog post, no third party, is used for any requirement.

## 2.1 Documented rejection reasons, each checked against your submission

TikTok publishes no single list titled "reasons we reject." I read the two pages that carry the criteria —
the [App Review Guidelines](https://developers.tiktok.com/doc/app-review-guidelines) and the
[Developer Guidelines](https://developers.tiktok.com/doc/our-guidelines-developer-guidelines) — and turned
every stated requirement into a check. The FAQ confirms there is no published list: *"Apps are not approved
for various reasons. Please review the application feedback."*
([App Review FAQ](https://developers.tiktok.com/doc/getting-started-faq))

| # | TikTok's requirement (verbatim) | Source | Your status |
|---|---|---|---|
| 1 | *"The app must have a custom name"* and *"The app name should match the app or website name and not describe your app"* | App Review Guidelines | **ACTION.** Use exactly `Clippers HQ`. Not "Clip tracker", not "Clippers HQ Analytics". |
| 2 | App names *"cannot reference social media companies"* | App Review Guidelines | **PASS.** "Clippers HQ" references none. Do not add "for TikTok". |
| 3 | Icon must be *"clear, appropriate, and consistent with the app brand"* | App Review Guidelines | **ACTION.** 1024×1024 px, JPEG/JPG/PNG, max 5 MB ([Create an app](https://developers.tiktok.com/doc/getting-started-create-an-app)). Use `public/icon-512.png` upscaled, or `public/landing/logo/logo.png`. |
| 4 | Description must explain *"what the app does and how it works"*; cannot be for *"private/personal use, adult content, or development/testing phases"* | App Review Guidelines | **RISK.** Never describe this as a pilot, test, or experiment. It is a live platform with real campaigns and real payouts. Say so. |
| 5 | *"A valid official website that houses information about your web and services"* and *"Your website URL cannot be a landing page or login page."* | App Review Guidelines | **FAIL AS THINGS STAND.** See 2.7. |
| 6 | *"Your Privacy Policy and Terms of Service links must be visible on the website URL without having to open a menu to view them, and the links must be active."* | App Review Guidelines | **FAIL AS THINGS STAND.** See 2.7. This is your biggest risk. |
| 7 | Web platform: *"Valid redirect URI required"* | App Review Guidelines | **ACTION.** See 2.6. |
| 8 | *"Only request permissions and features that your app needs."* | App Review Guidelines | **PASS** with the minimal set in 2.3. |
| 9 | *"At least one demo video that shows the complete end-to-end flow of the up-to-date integrations."* | App Review Guidelines | **BLOCKED** until BL-723 (or its Login Kit replacement) is deployed. PART 3. |
| 10 | *"All selected products and scopes must be clearly demonstrated in the video."* | App Review Guidelines | **TRAP.** Every scope you tick must appear on screen. Tick a scope you cannot film and you delay yourself. |
| 11 | *"If your app has not been approved before, you are required to use a sandbox environment on the Developer Portal to demonstrate the integration."* | App Review Guidelines | **APPLIES TO YOU.** You have never been approved. See 2.8. |
| 12 | Domain in the demo must match the submitted website URL | App Review Guidelines | **TRAP.** The browser address bar in your video must read `clipershq.com`. Not localhost, not a Railway preview URL. |
| 13 | *"Verify ownership of all configurations with a URL, including your Privacy Policy, Terms of Service"* | Developer Guidelines | **ACTION.** See 2.5. |
| 14 | *"Providing fake or incomplete data may lead to the rejection of your app and delays in your integration."* | Developer Guidelines | **PASS**, provided the policy is true — which is what PART 1 was for. |
| 15 | App must remain *"functioning during our review process"* | Developer Guidelines | **RISK.** Do not deploy anything that breaks the connect flow while review is open. |
| 16 | *"provide demo accounts and capabilities to our approvers free of charge, if requested"* | Developer Guidelines | **PREPARE.** Have a clipper login ready to hand over. |
| 17 | *"If you have access to a user's PII… never share it with anyone without their consent."* | Developer Guidelines | **PASS.** Section 4 of the policy commits to exactly this. |
| 18 | *"Never misguide users into thinking that you are part of the TikTok app"* | Developer Guidelines | **PASS.** Check your consent-screen copy uses no TikTok logo as your own branding. |
| 19 | *"Apps with complaints of frequent outages, timeouts, or poor performance can be rejected"* | Developer Guidelines | **PASS.** |

**UNVERIFIED:** whether TikTok weights any of these more heavily, and whether an Individual-owner account
faces stricter scrutiny than a Business-owner one. TikTok's documentation does not distinguish them — the
Create an App page lists the registration fields without defining the owner types at all.

## 2.2 Are `user.info.basic` and `video.list` the correct and minimal scopes? **YES.**

The Display API overview names exactly these two as its scopes, and the Login Kit overview names
`user.info.basic` as the baseline scope requested at authentication
([Display API overview](https://developers.tiktok.com/doc/display-api-overview),
[Login Kit overview](https://developers.tiktok.com/doc/login-kit-overview)).

* `user.info.basic` — *"Read a user's profile info (open id, avatar, display name …)"*. You need `open_id`
  to bind the grant to a creator. Not optional.
* `video.list` — *"Read a user's public videos on TikTok"*. This is what carries the view count.

([TikTok API scopes](https://developers.tiktok.com/doc/tiktok-api-scopes))

**Do not add these**, however tempting:

* `user.info.stats` (follower/like/video counts) — you do not price on followers. Adding it forces you to
  demonstrate it in the video.
* `user.info.profile` (bio, verified status) — same.
* `video.publish` / `video.upload` — you do not post. Requesting these would also contradict the privacy
  policy you just published, which is the worst possible combination in front of a reviewer.

**Does requesting extra delay review? Yes, structurally.** *"All selected products and scopes must be
clearly demonstrated in the video"* (App Review Guidelines) means every extra scope is another thing you
must film. Combined with *"Only request permissions and features that your app needs"*, an unused scope is
both extra work and a guidelines violation.

## 2.3 The minimal set to submit

**Product:** Login Kit. **Scopes:** `user.info.basic`, `video.list`. **Nothing else.**

## 2.4 One app or two? **ONE. Definitively.**

This is the question you flagged as most important, so here is the full chain of evidence.

**They are genuinely two separate platforms.** TikTok's own Accounts API Authorization documentation states
the prerequisites: *"You've created a TikTok For Business account"*, *"You've registered as a developer"*,
and *"You've created a developer app with the required scope of permissions which includes 'TikTok Accounts'"* —
each linking to `ads.tiktok.com/marketing_api/docs`, and the app itself created at
`ads.tiktok.com/marketing_api/apps/`. The authorize URL is not one you construct; it is a
*"TikTok account holder authorization URL"* copied from **My Apps > App Detail > Basic Information**.
(business-api.tiktok.com, doc id `1738083939371009`.) That is a different portal, a different account type,
and a different registration from `developers.tiktok.com`.

**But the Login Kit path already returns the money field.** TikTok's Video Object documentation lists the
complete queryable field set for the Display API:

| Field | Type | TikTok's description |
|---|---|---|
| `id` | string | *"Unique identifier for the TikTok video. Also called 'item_id'"* |
| `create_time` | int64 | *"UTC Unix epoch (in seconds) of when the TikTok video was posted."* |
| `share_url` | string | *"A shareable link for this TikTok video."* |
| `duration` | int32 | *"The duration of the TikTok video in seconds."* |
| `view_count` | int64 | *"Number of views of the video"* |
| `like_count` | int32 | *"Number of likes for the video"* |
| `comment_count` | int32 | *"Number of comments on the video"* |
| `share_count` | int32 | *"Number of shares of the video"* |

([Video Object](https://developers.tiktok.com/doc/tiktok-api-v2-video-object)) Endpoint:
`POST https://open.tiktokapis.com/v2/video/list/`, scope `video.list`, returning *"a paginated list for the
given user's public TikTok video posts, sorted by `create_time` in descending order"*, `max_count` default
10 and *"Maximum is 20"* ([List Videos](https://developers.tiktok.com/doc/tiktok-api-v2-video-list)).
Rate limit **600 requests per minute** on `/v2/video/list/`
([Rate Limits](https://developers.tiktok.com/doc/tiktok-api-v2-rate-limit)).

`view_count` + `create_time` is the entire earnings requirement. Earnings are `(views / 1000) × cpm`.

**What the second app would buy you, and why it is not worth it now.** The business-api `/business/video/list/`
adds `reach`, `full_video_watched_rate`, `total_time_watched`, `average_time_watched`, `impression_sources`
and `audience_countries`. TikTok's own note on that endpoint says: *"If the data for the fields `reach`,
`full_video_watched_rate`, `total_time_watched`, `average_time_watched`, `impression_sources`, and
`audience_countries` are unavailable, the reason is usually that the video has not been active
(viewed/liked/commented/shared) for more than 7 days."* It also warns *"There is a 24-48 hour delay for some
profile level metrics"*, that *"Post data will stop updating 365 days after the post is published"*, and that
the account owner must *"first publish at least one video, then tap the 'Turn On' button on the Analytics
page of their mobile TikTok app."* (business-api.tiktok.com, doc id `1762228421622786`.)

And since **March 20, 2026**, that path has an extra gate: *"developers must complete the Accounts API Access
Application Form before submitting a new developer app or requesting a scope increase that includes the
'TikTok Accounts' permission scope."* (same doc.)

**Verdict: submit the ONE Login Kit app. Do not open a business-api application now.** Ship earnings
verification on `view_count`, and treat the richer insights as a separate, later decision with its own form,
its own account type and its own approval.

**Consequence you must plan for: BL-723's client code needs a Login Kit variant.** Different host
(`open.tiktokapis.com` not `business-api.tiktok.com`), different auth (`Authorization: Bearer` not an
`Access-Token` header), different token endpoint (`/v2/oauth/token/` not `/tt_user/oauth2/token/`), different
response shape. The **OAuth state machine, the AES-256-GCM token encryption, the connection store, the
refresh logic and the disconnect path all carry over unchanged** — the rewrite is the client and the config,
not the architecture. Token lifetimes even match what BL-723 already assumes: access token *"valid for 24
hours"*, refresh token *"valid for 365 days"*, and *"The returned `refresh_token` may be different than the
one passed in the payload. You must use the newly-returned token if the value is different"*
([Token management](https://developers.tiktok.com/doc/oauth-user-access-token-management)).

## 2.5 Domain verification: use **Domain**, not URL prefix

TikTok's Create an App page documents both: for **Domain**, *"enter your domain and subdomain name, then
click Verify"*; for **URL prefix**, *"enter your complete URL, then click Verify. Download the provided
signature file, then upload it to your URL."*
([Create an app](https://developers.tiktok.com/doc/getting-started-create-an-app))

**Domain is correct for you, for a concrete reason.** The same page states that for apps created after
**September 9, 2024**, three URLs need verification: Terms of Service URL, Privacy Policy URL, and Web or
Desktop URL. All three of yours sit under `clipershq.com`. TikTok's Content Posting API guide states
*"Once the ownership of a domain is verified, all paths under that domain or its subdomains are considered
owned by the developer application"*, versus URL prefix where *"all URLs with the exact prefix are considered
owned"* ([Media transfer guide](https://developers.tiktok.com/doc/content-posting-api-media-transfer-guide)).
One TXT record covers all three URLs. URL prefix would mean three separate signature files.

**Exactly what to do:**

1. Developer portal, Production mode, click **URL properties**, then **Verify properties**.
2. Choose **Domain**. Enter `clipershq.com` (**one P** — `clippershq.com` is not your domain).
3. The portal shows a signature string. Add it as a **TXT record on the apex of `clipershq.com`** at your DNS
   provider — host `@`, type `TXT`, value = the string the portal gave you.
4. Wait for DNS propagation, then click **Verify** in the portal.

**UNVERIFIED, honestly:** TikTok does not publish the TXT record's name or exact format. Its guide says only
*"it is recommended that you add a signature string to the domain's DNS records."* The portal generates the
value and will tell you where it goes. Do not guess it in advance — read it off the screen. The same applies
to the URL-prefix signature file: TikTok does not publish its filename or path, only *"Download the provided
signature file, then upload it to your URL."* If you ever need that route, the file would go in `public/` and
be served from the site root, but take the name from the download, not from me.

## 2.6 Redirect URI rules, and the exact URI

**Login Kit's registration rules, verbatim** ([Login Kit for web](https://developers.tiktok.com/doc/login-kit-web)):

* *"A maximum of 10 URIs is supported."*
* *"The length of each URI must be less than 512 characters."*
* *"URIs must be absolute and begin with `https`."*
* *"URIs must be static. Parameters will be denied."*
* *"URIs cannot include a fragment, or hash character (#)"*
* Example given: `https://dev.example.com/auth/callback/`
* On the authorize call, `redirect_uri` *"must match one of the redirect URIs you registered for the app."*

**The URI in BL-723's code, quoted character for character.** The value is read from the env var
`TIKTOK_BUSINESS_REDIRECT_URI`; the code fixes the exact string it expects in the doc comment at the top of
`src/app/api/admin/tiktok-connect/callback/route.ts`:

```
https://clipershq.com/api/admin/tiktok-connect/callback/
```

**With the trailing slash. One P in `clipershq`.** The code's own validator in
`src/lib/tiktok-business/config.ts` enforces `https://` start, trailing slash, no `?`, no `#`, length 10–512,
and no port — which is the business-api rule set. Login Kit's rules are the same minus the mandatory trailing
slash, so **this exact string is valid under both**, and TikTok's own Login Kit example also ends in a slash.
Register it verbatim.

**One thing to watch, from BL-723's own comment:** the app runs with Next's default `trailingSlash: false`,
so Next answers the slashed path with a 308 to the slash-less form. A 308 preserves the query string, so the
auth code arrives intact. BL-723 marks the end-to-end behaviour **UNVERIFIED** because nobody has ever run
it. **Confirm it the first time you click through**, before you start filming.

## 2.7 The website URL problem — read this twice

TikTok requires, verbatim: *"Your website URL cannot be a landing page or login page"* and *"Your Privacy
Policy and Terms of Service links must be visible on the website URL without having to open a menu to view
them, and the links must be active."*

**What your site actually does.** `src/app/page.tsx` redirects a logged-out visitor from `/` to `/preview`.
I fetched `https://clipershq.com/` and `https://clipershq.com/preview` and found **no Privacy Policy, Terms
of Service or Cookie links on either**. The footer that has all three exists in `public/clipper.html`
(line 746: `<a href="/privacy.html">Privacy Policy</a>`, `/terms.html`, `/cookies.html`), and `/clippers`
embeds that file in an **iframe**.

**Two honest readings.** A human reviewer opening `clipershq.com/clippers` in a browser would see the footer,
because the iframe renders. A reviewer opening `clipershq.com` would see `/preview` and no links at all.
You should not gamble on which one they do.

**Two options, in order of preference:**

* **A (recommended) — a build round.** Add a small footer with Privacy Policy, Terms of Service and Cookie
  Policy links to `/preview`, so the bare domain satisfies the rule. Then register the Website URL as
  `https://clipershq.com`. This is the answer that holds regardless of which page a reviewer lands on.
* **B (no code) — register `https://clipershq.com/clippers` as the Website URL.** It is an informational
  page about the service, not a login page, and the embedded footer carries live legal links. Weaker,
  because the links are inside an iframe and a strict reviewer may not accept that.

**Do A. It is a small round and it removes the single most likely rejection.**

## 2.8 Sandbox — yes, it applies to you, and here is what it means

*"If your app has not been approved before, you are required to use a sandbox environment on the Developer
Portal to demonstrate the integration."* (App Review Guidelines) You have never been approved, so this is you.

What a sandbox is, from TikTok's own page ([Add a sandbox](https://developers.tiktok.com/doc/add-a-sandbox/)):
*"A restricted environment that allows you to try out integrations without having to submit your app for
review."* Up to **5 sandboxes** per app. You add target users by clicking **Add account** and logging into a
TikTok account you own, up to **10 accounts**. *"Sandbox mode does not offer access to Content Posting API
for public videos or Data Portability API"* — irrelevant to you, since you use neither.

**What this means in practice, plainly.** A sandbox is a *credential context*, not a mock website. It gives
you a working client key and secret that authorize only your listed target TikTok accounts, so you can run
the real OAuth flow and make real Display API calls against your own account **before** anyone approves you.
Your **website stays your real website**. You film your real UI on `clipershq.com` while the app is running
in sandbox mode. When you are happy, TikTok lets you *"import a sandbox's configuration to a Draft of your
app in production"* — note that this **overwrites existing draft settings** — and then submit.

**So the answer to "does sandbox suffice?": sandbox is how you get the credentials, and the live domain is
where you film.** You need both. Sandbox does not let you skip deploying — the video must show real UI at
`clipershq.com`, and that UI has to exist and work.

## 2.9 Timeline and what happens on rejection

*"App review may take several days to two weeks after submission."*
([App Review FAQ](https://developers.tiktok.com/doc/getting-started-faq))

On rejection you get written feedback: *"Click the history icon button at the top of the app page to access
Review comments."* You fix what they raised and **resubmit**; the cycle repeats until approved. There is no
documented penalty for a rejection and no documented limit on resubmissions.

**Plan for two weeks, not two days.** Read once and pass beats read twice and fail, which is the entire
reason for this round.

---

# PART 3 — THE DEMO VIDEO, SHOT BY SHOT

## 3.0 What must be true before you can press record

**BL-723 is a prerequisite for filming. It is currently on an unmerged branch and is not deployed.** There is
nothing to film. Specifically, before you can record:

1. BL-723's connect flow must be **merged to main and deployed to Railway** so that
   `https://clipershq.com/api/admin/tiktok-connect/*` actually responds. (Not this round. It is also written
   against the wrong API — see 2.4 — so it needs a Login Kit variant first.)
2. The five environment variables must be set in Railway, or every route returns 503 with `missingEnv`.
3. **There must be a visible page with a Connect button.** BL-723 shipped **zero `.tsx` files**. Today the
   flow is four JSON API routes with no UI at all. TikTok requires *"The video should clearly show the user
   interface and user interactions"* — a JSON response in a browser tab is **not a user interface** and will
   read as an incomplete integration. **A minimal connect page is not optional. It is the video.**

**Sandbox does not remove any of this.** Sandbox gives you credentials that work pre-approval; it does not
give you a website. The domain in the video must be `clipershq.com`.

## 3.1 Tools, free, on Windows 11

* **Xbox Game Bar** — press `Win + G`, then the record button. Built into Windows 11, zero install, outputs
  MP4. **Use this one.**
* **Windows Steps Recorder** — do not use; it captures screenshots, not video.
* **OBS Studio** (obsproject.com) — free, more control, MP4 output. Use if Game Bar refuses to record the
  browser window.
* **Your phone's screen recorder** — for the TikTok mobile shots, if you include them. iOS: Control Centre.
  Android: quick settings tile. Both output MP4 or MOV.

**Format and limits, from the App Review Guidelines:** **MP4 or MOV**, **maximum 5 files**, **up to 50 MB
each**. A 90-second 1080p screen recording is comfortably under 50 MB. If it is not, record at 720p.

## 3.2 The shot list

Aim for **90 to 150 seconds**. One continuous take is better than cuts, because it proves the flow is real.
Nothing may be a mockup, a slide, or a Figma frame.

| # | Shot | What must be visible on screen | Duration |
|---|---|---|---|
| 1 | Open a fresh browser window. Type `clipershq.com` into the address bar and press Enter. | **The address bar reading `clipershq.com`.** This is the domain-match requirement. Show it for a full 2 seconds before doing anything. | 5s |
| 2 | Log in as a clipper. | The Clippers HQ login screen, then the dashboard. Proves it is a real product, not a demo page. | 10s |
| 3 | Scroll to the footer, or open the privacy policy in a new tab. | **The Privacy Policy and Terms of Service links, and then the privacy policy page itself, scrolled to Section 4 "Connecting Your TikTok Account".** This pre-answers the reviewer's compliance check. Use `clipershq.com/privacy.html#tiktok`. | 10s |
| 4 | Navigate to the page with the TikTok connect button. | The real page, real styling, the button labelled clearly (for example "Connect TikTok account"). Move the mouse to it slowly. | 8s |
| 5 | Click Connect. | **TikTok's own authorization screen**, in full, unedited. The scope list must be legible. Do not speed this up or cut it — **this is the shot that demonstrates your scopes**, and *"All selected products and scopes must be clearly demonstrated in the video."* | 15s |
| 6 | Read the scope list aloud or pause on it. | Both `user.info.basic` and `video.list` visible as TikTok words them: *"Read your profile info (avatar, display name)"* and *"Read your public videos on TikTok"*. | 5s |
| 7 | Click Authorize. | The redirect back to `clipershq.com`. **The address bar must be visible on the return trip.** | 5s |
| 8 | The connected state. | Your page showing the account is connected: the TikTok handle or avatar, and a connected status. This demonstrates `user.info.basic`. | 8s |
| 9 | Trigger the video fetch. | **A list of the creator's own videos with real view counts, rendered in your UI.** This demonstrates `video.list`. Not raw JSON — a rendered list. | 15s |
| 10 | Show the link back to earnings. | The clip's view count next to what it earned, so the reviewer sees the *purpose* stated in your privacy policy actually happening. | 10s |
| 11 | Click Disconnect. | The disconnect control and a confirmation that the account is disconnected. Demonstrates user control, which the Developer Guidelines ask for. | 10s |

Shots 3, 10 and 11 are not strictly required. Include them anyway: they make the reviewer's compliance check
trivial, and a reviewer who has to hunt is a reviewer who asks questions.

## 3.3 Every trap, in one place

1. **The address bar must read `clipershq.com`** in shots 1 and 7. Not `localhost:3000`, not a
   `*.up.railway.app` preview host. The domain in the video must match the registered Website URL.
2. **`clipershq.com` has one P.** `clippershq.com` is not your domain. Check it on screen before you record.
3. **Every scope you ticked must appear on screen.** If you tick `user.info.stats` and never show follower
   counts in your UI, you have given the reviewer a reason to come back. Tick exactly two.
4. **Real UI only.** JSON in a browser tab, a Postman window, a terminal, a slide, or a Figma mockup will all
   read as "not integrated." *"The demo video should showcase the website or app where the features will
   actually be integrated."*
5. **Do not cut TikTok's consent screen.** It is the single most important frame in the video.
6. **No dev tools open, no console visible, no other tabs with anything private.** Close everything else.
7. **MP4 or MOV. Maximum 5 files. 50 MB each.** Check the file size before uploading.
8. **Do not deploy anything that breaks the flow while review is open.** *"Your app must be functioning
   during our review process."*
9. **No audio narration is required.** If you add it, do not claim anything the video does not show.

---

# PART 4 — THE ORDERED CHECKLIST, FROM HERE TO SUBMITTED

Follow it top to bottom. **[YOU]** = your action. **[BUILD]** = a round to hand to Claude Code.

| # | Who | Step | Blocks |
|---|---|---|---|
| 1 | **[BUILD]** | Merge this round (BL-724) and deploy. The corrected privacy policy must be live at `clipershq.com/privacy.html` before a reviewer reads it. | 12 |
| 2 | **[BUILD]** | Add a footer with Privacy Policy, Terms of Service and Cookie Policy links to `/preview`, so the bare `clipershq.com` satisfies the "visible without a menu" rule. **The highest-value step in this list.** See 2.7. | 12 |
| 3 | **[YOU]** | Confirm Ably: `railway variables \| grep ABLY_API_KEY`. If unset, tell Claude Code to delete that line from Section 3. | — |
| 4 | **[BUILD]** | **Port BL-723 to Login Kit.** New host `open.tiktokapis.com`, `Authorization: Bearer`, `/v2/oauth/token/`, `POST /v2/video/list/`, fields `id,create_time,share_url,duration,view_count,like_count,comment_count,share_count`. Keep the OAuth state machine, token encryption, connection store, refresh and disconnect **unchanged**. See 2.4. | 8, 10 |
| 5 | **[BUILD]** | **Build the connect UI.** BL-723 has zero `.tsx` files, and without a visible page there is nothing to film. Needs: a Connect button, a connected state showing the TikTok handle, a rendered list of the creator's videos with view counts, and a Disconnect button. Gate behind `isTestUser` per CLAUDE.md. See 3.0. | 10 |
| 6 | **[YOU]** | Create the app at `developers.tiktok.com`. Name **exactly** `Clippers HQ`. Icon 1024×1024. Description: a live platform connecting clippers with brand campaigns that pays per view, which needs to read a creator's own public video view counts to calculate what they are owed. Category: Business. | 7 |
| 7 | **[YOU]** | Add product **Login Kit**. Add scopes **`user.info.basic`** and **`video.list`**. Nothing else. See 2.2. | 11 |
| 8 | **[YOU]** | Register the redirect URI, exactly: `https://clipershq.com/api/admin/tiktok-connect/callback/` — or whatever path step 4 settles on. Trailing slash. One P. See 2.6. | 10 |
| 9 | **[YOU]** | **Verify the domain.** URL properties → Verify properties → **Domain** → `clipershq.com` → add the portal's TXT string to your apex DNS → Verify. Also register the ToS URL (`/terms.html`), the Privacy Policy URL (`/privacy.html`) and the Web URL. See 2.5. | 12 |
| 10 | **[YOU]** | **Create a sandbox.** Add your own TikTok account as a target user. Copy the sandbox client key and secret into Railway with the other env vars. Then click through the real flow once end to end and confirm the 308 trailing-slash redirect delivers the auth code (BL-723 marks this UNVERIFIED). See 2.8. | 11 |
| 11 | **[YOU]** | On your phone: publish at least one video, then open TikTok Analytics and tap **Turn On**. Needed so there is real data to show. | 12 |
| 12 | **[YOU]** | **Film the demo video.** Win + G. Follow the shot list in 3.2. Check every trap in 3.3. MP4, under 50 MB. Watch it back once, in full, before uploading. | 13 |
| 13 | **[YOU]** | Import the sandbox configuration into the production Draft (**it overwrites the draft**), attach the video, write the per-scope justification: `user.info.basic` binds the connection to the right creator; `video.list` reads the creator's own view count so their payout is calculated from an accurate figure. Submit. | — |
| 14 | **[YOU]** | Wait. Several days to two weeks. Do not deploy anything that breaks the connect flow while it is open. | — |
| 15 | **[YOU]** | If rejected: history icon → **Review comments**. Fix exactly what they name, resubmit. No penalty, no limit. | — |
| 16 | **[BUILD]** | Once approved and before the feature reaches clippers: close the two gaps in 1.4 — account deletion must remove the `clip_account_connections` row, and the policy should be updated to name the in-app disconnect button once it exists. | — |

**Steps 1, 2, 4 and 5 are build rounds and are prerequisites for step 12.** You cannot film a flow that is
not deployed and has no user interface.

---

# VERIFICATION

**Safety**

* 6 money files + `tracking.ts` + `campaign-era.ts` **BYTE-IDENTICAL by blob OID** on both refs, checked
  with `git show` against `origin/main` and `checkpoint/BL-724`. Table in the appendix below.
* No schema change. No `prisma migrate`. **No DB write of any kind** — the only database access this round
  was `scripts/run-select.js`, which refuses every write keyword.
* No clip's earnings, status, views or payout changed.
* Nothing registered, nothing submitted, no credential stored, no TikTok API call made.
* BL-723 **not merged, not deployed**. Its branch was read only.
* No dashes used as bullets anywhere in the shipped policy copy.

**Build honesty**

* `eslint` confirmed present: `npx eslint --version` → `v9.39.4`. The hooks gate is not silently no-opping.
* `npm ci` → exit **0**. `npx prisma generate` run afterwards → exit **0** (npm ci regenerates it, and it
  was re-run explicitly before typecheck).
* `npx tsc --noEmit` → exit **0**, `grep -c "error TS"` = **0**.
* `npm run build` → **BUILD_EXIT=0**, read from `$?` written to a log, never piped through `tail`.
  `✓ Compiled successfully in 21.4s`.
* **BL-348 hooks gate: `11 problems (0 errors, 11 warnings)`** against `--max-warnings 11`. It passes, and it
  passes **at the limit** — all 11 are pre-existing `react-hooks/exhaustive-deps` warnings in files this
  round did not touch. Stated plainly because one new warning from any round would break the gate.
* Both `tsc` and `next build` actually ran. Neither was inferred from the other.

**Files changed:** `public/privacy.html`, `src/lib/legal-version.ts`, `BACKLOG.md`, and this report.

**Rollback:** `git revert -m 1 <merge>`. The policy returns to the Apify/Vercel wording and `TOS_VERSION`
returns to `v1`. Nothing else moves.

## Appendix — money-file blob OIDs

`git rev-parse origin/main:<path>` compared against `git rev-parse checkpoint/BL-724:<path>`. All seven
matched exactly (blob OID compared on **both** refs, not a working-tree hash — a working-tree sha256 on
Windows fakes a mismatch through CRLF).

| File | Blob OID on both refs |
|---|---|
| `src/lib/clip-earnings-writer.ts` | `ac5be7deb061768fec800aa89aae512a56a9e065` |
| `src/lib/earnings-calc.ts` | `797e20985ad57475ef321afcf3cb1ea7b0d6ab84` |
| `src/lib/balance.ts` | `e887f80acfc70fee438e719a32a60025eda22749` |
| `src/lib/tracking.ts` | `83ce4babfd39a6261114465639f2eac4e23bfceb` |
| `src/lib/clip-earnings-invariant-middleware.ts` | `61cef39395363c31f0c902dd4c64e8c06b3e6449` |
| `src/lib/money-decimal.ts` | `ef5cdae757b9ad3c23380ee8b63e279f98d0b6ac` |
| `src/lib/campaign-era.ts` | `106e16ad75125c3b10b6949a2981d33614c69ab9` |

The full branch diff against `origin/main` is exactly four files: `BACKLOG.md`, `public/privacy.html`,
`src/lib/legal-version.ts`, and this report.
