# BL-930: every external service ClippersHQ uses, what it costs, and how close each is to a limit

> **URGENT, FIRST LINE: THE INSTAGRAM DATA PROVIDER (HikerAPI) HAS $8.65 LEFT and runs out in about 2 to 6 days, between 2026-09-26 and 2026-09-30.**
> * **Read from HikerAPI's own billing page today.** No top-up since 2026-06-25.
> * **When it empties,** every Instagram clip's view count stops updating. That is almost the whole platform, including the marketplace campaign.
> * **Why no fallback:** the fallback provider (Apify) is switched off in code by a constant, `APIFY_HARD_OFF = true`.
> * **The only alarm is a bell, not an email,** and a separate round measured 0 of 24 bells ever read.
> * **What the owner would do** (not done here): top up the HikerAPI balance.

**AUDIT ONLY. NOTHING WAS CHANGED OR BOUGHT.** No code, schema, data, config, environment variable, flag or plan change.
* **Clock:** DB `now()` read from 2026-09-24 12:16 UTC onward.
* **Repo:** branch `checkpoint/BL-930` carries this file only.
* **Worktree:** `C:\w\b930`, removed at the end and verified gone.

**Model split:** Opus did everything, **0 subagents**. The brief allowed a cheaper model for enumeration. I kept it in-house because the dashboards overturned two of my own estimates mid-round (sections 3.4 and 5).

**Caps:**
* **Database:** ONE connection at a time, about 30 sequential `run-select.js` reads.
* **Vendors:** **no vendor API call and no Apify actor.** HikerAPI's and LamaTok's own balance endpoints were deliberately NOT called; balances were read from their dashboards instead.

**Browser: available, and used READ ONLY.** A Chrome session with some of the owner's sign-ins was available.

| site | page read | what it held |
|---|---|---|
| Railway | usage | yes, signed in |
| HikerAPI | billing, dashboard | yes, signed in |
| LamaTok | billing | yes, signed in |
| Resend | usage | **NOT signed in** (redirected to the marketing site) |
| Supabase | dashboard | **NOT signed in** (sign-in page; I did not sign in) |

**Controls seen and NOT touched:**
* Railway: "Update limits", "Manage your plan".
* HikerAPI: "Top up your balance", "Earn free credits", "Download this report as csv".
* LamaTok: "Top up your balance".

**One disclosure.** Opening HikerAPI's tokens page displayed the access key in full. It is written nowhere: not in this report, a file or a log. I left the page at once and opened no other key page.

**Prior reports, all read through the authenticated API** (the repository is private): the handoff, BL-838, BL-855, BL-856, BL-872, BL-780, BL-920. None failed to read.

---

## PART 1: EVERY SERVICE, FROM THE CODE

**How they were found:**
* **97 distinct environment variable names** are read by `src`, the cron script and the config files (`grep -rhoE "process\.env\.[A-Z0-9_]+"`).
* **The second family is outbound hosts called with no key at all**, which a variable census never sees: 21 hostnames in server code (`grep -rhoE "https?://…"` over `src/lib`, `src/app/api` and the cron script).
* **A third family names no URL at all**: SDK clients (Prisma, Supabase JS, Ably, Sentry, the auth providers).

| service | what ClippersHQ uses it for | who calls it | how often | if it stops |
|---|---|---|---|---|
| **Railway** | hosting: the web service and the cron service | the whole app | always | **the site is down** |
| **Supabase Postgres** (`DATABASE_URL`) | every row of the platform | Prisma, everywhere | always | **the site is down** (it happened on 7 September) |
| **Supabase Storage** (`NEXT_PUBLIC_SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`) | clip covers, avatars, marketplace thumbnails and frames, screenshots | 11 files | on upload and approval | pictures stop saving; the pages still work |
| **HikerAPI** (`HIKERAPI_KEY`) | **Instagram view tracking**, clip liveness, verification, covers | `scraper-providers/hikerapi.ts`, `clip-liveness-recheck.ts` | every tracking tick; **about 2,256 requests a day** by its own meter | **every Instagram view count freezes** (no fallback, section 4) |
| **LamaTok** (`LAMATOK_KEY`) | TikTok view tracking | `scraper-providers/lamatok.ts`, the tracking route | every tick; about 20 calls a day by the ledger | TikTok counts freeze |
| **Apify** (`APIFY_API_KEY`, `APIFY_TOKEN`, 4 actor variables) | the old tracking and fallback | `apify.ts`, `apidojo.ts`, `account-profile.ts` | **never**: `APIFY_HARD_OFF` is a constant `true` (`apify-hard-off.ts:62`) | nothing; **it is on the list but the code no longer calls it** |
| **Resend** (`EMAIL_API_KEY`, `EMAIL_FROM`, `EMAIL_API_URL`, `RESEND_WEBHOOK_SECRET`) | all email: owner alerts, payout reminders, marketing, clipper mail | `email.ts` and 8 files | **about 145 sends a day** | **every email stops**, including every owner alert |
| **YouTube Data API** (`YOUTUBE_API_KEY`, `YT_DAILY_QUOTA`) | YouTube view tracking, verification | `youtube.ts`, `account-profile.ts`, `clip-freshness.ts`, `verify-cascade.ts` | **0 units in 14 days** | YouTube counts freeze |
| **Browserless** (`BROWSERLESS_URL`, `_TOKEN`, `_API_KEY`) | a headless browser for account verification, last tier | `verify-cascade.ts` | only when cheaper tiers fail | verification falls back to manual |
| **Sentry** (`NEXT_PUBLIC_SENTRY_DSN`, `SENTRY_AUTH_TOKEN`) | error tracking | `capture-server-error.ts`, the Sentry configs, the browser | on errors | errors go unseen; nothing breaks |
| **Ably** (`ABLY_API_KEY`) | realtime push: live counts, community | `ably.ts`, `/api/ably-token`, `tracking-post-steps.ts` | every page load mints a token | live updates stop; pages still load |
| **Discord** (bot: `DISCORD_BOT_TOKEN`, `DISCORD_GUILD_ID`; OAuth: `AUTH_DISCORD_ID`, `AUTH_DISCORD_SECRET`) | **sign-in** (the main login) and server roles | `auth.ts`, `discord-bot.ts`, the role reconcile cron | every sign-in | **nobody can sign in with Discord** |
| **Google sign-in** (`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`) | a second sign-in option | `auth.ts` | at sign-in | Google sign-in stops |
| **Google Drive** (no key) | marketplace previews (`drive.google.com/thumbnail`) and the video download behind the three frames (`drive.usercontent.google.com`) | `marketplace-v2-thumbnail.ts`, `marketplace-v2-frames.ts` | per marketplace clip | previews and frames stop; the clip still works |
| **Instagram, TikTok, YouTube public pages and oEmbed** (no key) | link checks and fallbacks | several files | occasional | small |
| **bundle.social** (`BUNDLE_SOCIAL_API_KEY`, `BUNDLE_SOCIAL_TEAM_ID`, `BUNDLE_SOCIAL_MONTHLY_CAPTURES`) | TikTok analytics capture through a linked account | `social-connect/bundle-social.ts`, `clip-analytics-capture.ts`, the TikTok analytics cron | **0 captures ever** | nothing today |
| **TikHub** (`TIKHUB_API_KEY`) | owner creator-scan tool (Instagram) | `creator-scan/providers.ts` via `scan.ts` | **187 creator scans in 30 days** (all three scan vendors) | the owner's scan tool fails |
| **ScrapeBadger** (`SCRAPEBADGER_API_KEY`) | creator-scan (TikTok, YouTube), account profiles | `creator-scan/providers.ts`, `account-profile.ts` | as above | the same |
| **OCR.space** (`OCR_SPACE_API_KEY`) | reading screenshots in creator-scan | `creator-scan/screenshot-ocr.ts` | as above | screenshot reading fails |
| **Anthropic** (`ANTHROPIC_API_KEY`) | a support chatbot | `chatbot.ts` | **never**: `chatbot.ts` has **0 importers** | nothing; **dead code** |
| **GitHub** | the code host, pushes, the private reports repository | git, `gh` | every round | deploys stop (Railway builds from `main`) |

**Not on the brief's list, and so the interesting ones:**
* **Ably**: live in every page load.
* **TikHub, ScrapeBadger, OCR.space**: live, via the owner's creator-scan tool.
* **Google Drive**: live, keyless.
* **Anthropic**: present but dead.

**On the list but no longer called:** Apify.

---

## PART 2: COST AND PLAN, AND HOW EACH IS KNOWN

| service | paid? | plan and cost | how I know |
|---|---|---|---|
| **Railway** | paid | **Pro Plan, usage-based: $20.00 plan fee including $20.00 of usage.** This cycle (Sep 20 to Oct 20): **$3.21 used** (memory $2.87, CPU $0.08, egress 5.16 GB $0.26, volume $0.003). Plan includes up to 24 GB RAM, 24 vCPU, 100 GB shared disk. "Agent Usage Limit $0.00 / $50.00" | **read from Railway's usage page today** |
| **HikerAPI** | paid, **prepaid balance** | **Balance $8.65.** Page text: "Funds are debited hourly according to your chosen plan". Top-ups: ₮5.2 (2026-06-04), ₮104.2 (2026-06-07), ₮213 (2026-06-25), none since. Per-request price $0.00069214 | balance and top-ups **read from HikerAPI's billing page today**; price from **BL-838 (2026-09-05)**, from the vendor's own meter |
| **LamaTok** | paid, **prepaid balance** | **Balance $236.03**, the same hourly debit text. Top-ups: ₮21.5 and ₮280 (both 2026-06-25). Per-request price $0.00060007 | balance **read from LamaTok's billing page today**; price from **BL-838 (2026-09-05)** |
| **Supabase** | paid (see note) | the plan could NOT be read (not signed in) | **structural only:** `shared_buffers` = 512 MB, the Small compute BL-872 (2026-09-09) described as "the Small upgrade" after the Nano outage. Small compute is a paid add-on; its price was not read |
| **Resend** | **could not be established** | not read (not signed in) | **measured evidence only (PART 3):** 145 sends accepted in one day with 0 refusals and 0 HTTP 429, so this account is not held to 145 a day or less |
| **YouTube Data API** | free quota | 10,000 units a day by the code's default (`operational-monitor.ts`, `YT_DEFAULT_DAILY_QUOTA`) | the code; the real quota lives in Google Cloud and was not read |
| **Apify** | unknown | not called | the code |
| **Sentry, Ably, Browserless, TikHub, ScrapeBadger, OCR.space, bundle.social, GitHub** | **could not be established** | not read | none of their dashboards was opened; no prior report prices them |
| **Discord, Google sign-in, Google Drive** | free to use | | the code (OAuth and keyless fetches) |
| **Anthropic** | none | dead code | the code |

**Prior measured costs, with dates:**
* **BL-838 (2026-09-05):** Instagram about $139 a month, since its $9.75 saving was 7.0 percent of the Instagram bill.
* **BL-872 (2026-09-09):** vendor spend $146.73 a month.

---

## PART 3: HOW MUCH OF EACH LIMIT IS USED, MEASURED

### 3.1 Email, first as the brief asked

**The ledger only goes back 2.7 days.** `email_send_outcomes` has recorded every send only since 2026-09-21 19:10 UTC (BL-920). Earlier days exist only for the growth engine (`email_events`), which sends 2 to 15 a day. **Fourteen full days of owner alerts cannot be reconstructed; they were not recorded before BL-920.**

| day (UTC) | all sends | owner alerts | of which "Payout overdue" | marketing | other | refused or 429 |
|---|---|---|---|---|---|---|
| 09-21 (from 19:10) | 33 | 33 | 27 | 0 | 0 | 0 |
| 09-22 | 144 | 123 | 111 | 2 | 19 | 0 |
| **09-23 (peak)** | **145** | 129 | 114 | 1 | 15 | 0 |
| 09-24 (to 12:16) | 66 | 60 | 60 | 0 | 6 | 0 |

* **388 sends, 388 accepted, 0 refused, 0 HTTP 429.**
* The reminder flood is **77 to 79 percent of all email**.

**Could the flood exhaust an allowance?**
* **Not a daily one:** the peak of 145 in a day went through with zero rate-limit answers.
* **A monthly one cannot be ruled out,** because the plan is unknown. At about 145 a day the account sends roughly 4,300 a month.
* Resend's public pricing lists a free tier of 100 a day and 3,000 a month. That is from their public pricing page, **not this account**, and the 145-a-day evidence says this account is not on a 100-a-day limit.
* **If a monthly cap exists and is hit, every email stops at once:** owner alerts, payout reminders, the maker-submitted alert, clipper mail. Each failed send would write a `refused` row, **but no alert can say so**, because the alerts themselves travel by email (PART 4).
* **The owner can settle it** at resend.com, Settings, Usage.

### 3.2 The database

**Measured at 2026-09-24 12:16:46 UTC:**
* **777 MB** (814,779,539 bytes).
* **Growth:** BL-872 measured 725 MB on 2026-09-09, so +52 MB in 15 days, **about 3.5 MB a day**.
* **Connections: 24 of 90** (1 active, 0 idle in transaction). BL-872 measured 26.
* **Cache hit: 99.99 percent.**
* **Largest tables:** `email_events` 200 MB, `user_events` 166 MB, `clip_stats` 155 MB, `apify_usage_entries` 106 MB.

**The disk allowance cannot be read over SQL**, and the dashboard was not signed in. For scale: 1 GB would be reached in about 70 days at this rate, and 8 GB in about 6 years. Which of those is the real limit is not known. **Connections are fine for months.**

### 3.3 Storage

* **One bucket, `uploads`: 8,095 objects, 487 MB** (510,273,814 bytes).
* **Clip covers are 459 MB of it.** Marketplace frames are **2.2 MB (78 objects, three per approved clip)**; marketplace thumbnails are 0.8 MB.
* **Growth: 1.32 MB a day over 7 days, 4.43 MB a day over 30.**
* The allowance was not read. At these rates, storage grows about 0.05 to 0.13 GB a month: **months to years on any paid plan.**

### 3.4 The data providers

**HikerAPI (Instagram). THE ONE THAT IS CLOSE.**
* **Balance $8.65 today**, against $76.91 that BL-838 read on 2026-09-05.
* **$68.26 gone in about 19 days = about $3.60 a day**, with no top-up in between (the transactions list shows none since June).
* **Its own meter** counted **2,256 requests on 2026-09-23** (the dashboard's hourly table, browser-local day), about $1.56 at the per-request price. The balance fell faster than that, consistent with its "debited hourly according to your chosen plan" text.
* **At $3.60 a day the balance lasts about 2.4 days (to about 2026-09-26); at $1.56 a day about 5.5 days (to about 2026-09-30).**
* **My own earlier estimate was wrong, disclosed.** Before opening the dashboard I estimated about 48,500 requests left and a run-out near 2026-10-27, by subtracting the ledger's calls from BL-838's request counter. The dashboard shows the ledger misses most calls (next bullet), so that estimate is withdrawn.
* **The platform's own ledger UNDERCOUNTS HikerAPI about 2.5 times:** 897 ledger calls on 2026-09-23 (UTC) against the vendor's 2,256 (browser-local day). BL-838 measured 12.6 percent on 2026-09-05; the gap has grown.
* **`HIKERAPI_DAILY_BUDGET_USD` is an ALARM, not a cap, re-confirmed:**
  * `hikerapi.ts:828` calls it a "PURE ALERT THRESHOLD, not a cap";
  * `notifications.ts:359` calls it a "PURE FIRE ALARM";
  * it defaults to $10 a day;
  * it sums `estimatedCostUsd` from the same ledger (`hikerapi-budget.ts`), so it measures a spend the ledger undercounts, and **it never looks at the balance at all**.

**LamaTok (TikTok):**
* **Balance $236.03**, against $257.79 on 2026-09-05: **about $1.15 a day, so about 205 days (to about April 2027).**
* The ledger records about 20 calls a day.

**Apify:** 0 calls; hard off.

**The owner's creator-scan tool (TikHub, ScrapeBadger, OCR.space):** 187 scans in 30 days, the last at 03:44 today. Unpriced; no record of its spend exists anywhere in the platform.

### 3.5 YouTube

* **0 units in 14 days** (`apify_usage_entries`, platform `youtube`), against 10,000 a day: **0 percent used.**
* **668 YouTube clips hold active tracking jobs and none was fetched in 14 days.** Nothing is near a limit. Whether those clips should be tracked is a separate question, noted and not examined.

### 3.6 Hosting

* **$3.21 of the $20.00 included usage**, 4.5 days into a 30-day cycle.
* **Projected about $21 for the cycle**, so at most a dollar or two over the included $20. Fine.

### 3.7 Error tracking

Sentry's own counts could not be read. **The platform's proxy, `audit_logs` `SERVER_ERROR`:** **2 in 14 days**, the last 2026-09-18 18:20 UTC. Fine.

### 3.8 Every service, used and limit

| service | used | limit | headroom | runs out |
|---|---|---|---|---|
| **HikerAPI** | about $3.60 a day | **$8.65 balance** | **about 2 to 6 days** | **about 2026-09-26 to 2026-09-30** |
| LamaTok | about $1.15 a day | $236.03 balance | about 205 days | about April 2027 |
| Resend | about 145 a day, about 4,300 a month | **unknown** | unknown | unknown (not daily-capped at 145) |
| Railway | $3.21 of $20 included, 4.5 days in | $20 included, then pay-as-you-go | fine | never (it bills, it does not stop) |
| Supabase DB | 777 MB, 24 of 90 connections | disk allowance unknown; 90 connections | connections 3.75x | disk: 1 GB in about 70 days; the real limit unknown |
| Supabase Storage | 487 MB | unknown | | months to years |
| YouTube | 0 units a day | 10,000 a day | 100 percent | never at this rate |
| bundle.social | 0 captures | 100 a month in code | 100 percent | never |
| Sentry, Ably, Browserless, TikHub, ScrapeBadger, OCR.space, GitHub | not measurable here | unknown | | unknown |

---

## PART 4: WHAT HAPPENS AT EACH LIMIT, AND WHETHER ANYONE WOULD KNOW

**HikerAPI at $0: fails silently for users.**
* The vendor answers HTTP 402. The code sets a 10-minute cooldown and "falls back" to Apify (`hikerapi.ts:853-860`), but **Apify is hard off**, so Instagram views simply stop updating.
* Earnings on Instagram clips stop moving.
* **The alert** `HIKER_BALANCE_LOW` is a **bell only**. It is NOT in the owner email list (`notifications.ts`, the owner email set), unlike the daily budget alarm `HIKER_BUDGET_THRESHOLD`, which is emailed.
* **Evidence it has happened before:** `HIKER_BALANCE_LOW` fired 4 times on 2026-06-06 and 07, just before the ₮104.2 top-up on 06-07.
* **Would the owner know? Probably not quickly:** BL-927 measured 0 of 24 marketplace bells ever read. The frozen counts are the visible symptom, and they look like slow videos rather than an outage.

**Resend at a limit: fails silently, and cannot report itself.**
* Each refused send writes an `email_send_outcomes` row, **but every owner alert that would report it travels by email.**
* Bells would still arrive, and a person reading `/admin` would see them.

**Supabase database full or overloaded: fails loudly for users, silently for alerts.**
* The site stops (7 September, 24 h 11 min).
* **BL-872 established that the watchdog reads its heartbeats from the database**, so no operational alert can fire while it is down. Nothing external watches it; BL-872's minimum recommendation of an external uptime monitor is still the owner's step.

**Railway over the included $20: starts charging.** It keeps running; the bill rises by usage. No outage.

**LamaTok at $0:** TikTok counts freeze, the same shape as HikerAPI. It is 205 days away.

**YouTube quota:** a hard block that freezes YouTube counts. The alert fires at 80 percent (`YOUTUBE_QUOTA_HIGH`, emailed). It is not near.

**Discord sign-in failure: fails loudly** (nobody can log in). Google sign-in remains.

**Ably, Sentry, Browserless, creator-scan vendors: degrade quietly.** Live counts stop updating, errors go unseen, verification falls back to manual, and the owner's scan tool errors. Nothing user-facing breaks.

---

## PART 5: THE VERDICT, CLOSEST FIRST

**URGENT THIS WEEK:**
1. **HikerAPI, $8.65 left, about 2 to 6 days to zero (2026-09-26 to 2026-09-30).**
   * **What breaks:** every Instagram view count and every Instagram earning update, silently.
   * **Who would know:** a bell nobody reads.
   * **What the owner would do (not done here):** top up at hikerapi.com, Billing.
   * **Worth knowing before choosing an amount:** the balance has been falling about $3.60 a day, roughly $108 a month at this pace.

**FINE FOR NOW, BUT UNKNOWN AND WORTH ONE LOOK:**

2. **Resend's plan.** It is not capped at 145 a day, but a monthly allowance cannot be ruled out at about 4,300 a month, 77 to 79 percent of which is payout-overdue reminders. **Owner action:** open resend.com, Settings, Usage. Paying the ten overdue payouts BL-927 named would also remove most of this volume.
3. **Supabase's plan and disk allowance.** 777 MB, growing about 3.5 MB a day; not readable without signing in. **Owner action:** supabase.com, the project, Settings, Billing and Usage.

**FINE FOR MONTHS:**

4. LamaTok, about 205 days.
5. Railway, about $21 this cycle against $20 included, then pay-as-you-go.
6. Database connections, 24 of 90.
7. Storage, 487 MB growing 1.3 to 4.4 MB a day.
8. YouTube, 0 of 10,000.
9. bundle.social, 0 of 100.

**STRUCTURAL FINDINGS, NO LIMIT INVOLVED:**
* The HikerAPI ledger undercounts about 2.5 times, so the platform's own spend figures and its $10 daily alarm under-read the real spend.
* The balance-exhausted alert is bell-only.
* Apify, Anthropic and the chatbot are dead code carrying live keys.
* 668 YouTube clips hold tracking jobs with 0 fetches.

**Is everything fine?** Everything except one thing, which is not fine and is days away: the Instagram provider's balance.

**Known monthly spend, from pages read today and prior measured rates:**

| item | per month | source |
|---|---|---|
| Railway | about $20 to $21 | read today |
| HikerAPI | about $108 at the current balance burn | measured from two vendor readings 19 days apart |
| LamaTok | about $35 | the same method |
| **Known total** | **about $163 to $164 a month** | |

**Costs that could not be established:** Supabase (the Small compute and any plan fee), Resend, Sentry, Ably, Browserless, TikHub, ScrapeBadger, OCR.space, bundle.social and GitHub.

**Where the owner can look, for each unknown (read only, nothing to press):**

| service | page |
|---|---|
| Supabase | the project's Billing and Usage |
| Resend | Settings, Usage |
| Sentry | Settings, Subscription |
| Ably | Account, Usage |
| Browserless | Account, Usage |
| TikHub, ScrapeBadger, OCR.space | each account's Balance or Usage page |
| GitHub | Settings, Billing and plans |
