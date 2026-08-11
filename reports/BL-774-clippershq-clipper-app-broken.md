# BL-774 — "my app is not working", diagnosed

**THE PLATFORM IS NOT BROKEN, AND ACTIVITY IS ABOVE NORMAL. This is one clipper, and it is not a
defect: every one of Clipper F's 22 clips and his $52.08 payout request were rejected by the OWNER
himself on 2026-08-03 with the reason "botted views buddy". He has $0.00 because everything he
submitted was refused, and the app already tells him why on every clip.**

**2026-08-11 · DB `now()` = `2026-08-11 14:06:49.386609+00` · AUDIT ONLY, READ ONLY.**
No code, data or config changed. **Nothing about this clipper's account, session, clips, balance or
status was altered.** Base `origin/main` @ `9d285c8c`, isolated worktree `C:/m774`, removed at exit,
`node_modules` never junctioned. A markdown-only diff cannot change tsc or build, so neither was run
and neither is claimed. Handle redacted throughout as **Clipper F**; no wallet address was selected.

---

## PART 0 — IS IT EVERYONE? NO, AND THE PLATFORM IS BUSIER THAN USUAL

Measured before looking at any single account, last 24 hours against the prior 7 days' daily average:

| Signal | Last 24h | Prior 7-day daily average | Direction |
|---|---|---|---|
| Clips submitted | **107** | 77.1 | **+39%** |
| Distinct clippers submitting | **19** | 6.6 | **+188%** |
| Payout requests | 1 | 2.4 | lower, see note |

**There is no outage and no collapse.** Submissions are up by nearly 40% and nearly three times as many
distinct people submitted in the last day as on an average day of the prior week. **Whatever is
happening to Clipper F is happening while the rest of the platform is having an unusually good day.**

The single payout request against a 2.4 average is not a signal: payout volume is low-count and lumpy,
BL-770 measured only 33 distinct requesters in 30 days, and one day's count carries no information.

### The deploy cross-reference, which excludes every recent change

**Clipper F's last interaction of any kind was submitting a clip at `2026-07-31 09:15:54.589`.**

The earliest merge in the recent window is **BL-713 at 2026-08-05 13:14**. Every round the brief names
landed later still: BL-736 and BL-739 and BL-740 on 08-08, BL-744 and BL-746 and BL-748 on 08-09,
BL-755 on 08-09, BL-756 on 08-10 14:21, BL-762 on 08-10 19:49, BL-765 on 08-10 22:14.

**He stopped using the platform five days before the earliest of them shipped.** No change to the
earnings display, the payout messaging, per-clip CPM overrides, YouTube view handling, the Instagram
submit path, the mobile drawer or the reassignment picker can have broken anything for him, because he
was already gone. **This is not a judgement about those rounds; it is a timestamp comparison and it is
conclusive.**

---

## PART 1 — CLIPPER F, EVERY DIMENSION

| | |
|---|---|
| Account | `cms7miow`, role **CLIPPER** |
| Created | `2026-07-30 14:43:22.396` |
| Last updated | `2026-08-03 17:17:32.459` |
| **Last active date** | **`2026-07-31 00:00:00`** |
| **Last clip submitted** | **`2026-07-31 09:15:54.589`** |
| Banned / restricted | **No.** `marketplaceBannedUntil` null, not a test user |
| Discord linked | Yes |
| Referred by | No |
| Connected accounts | **2, both Instagram, both APPROVED and verified.** One self-deleted by him on the day he joined, one active |
| **Clips** | **22, and every single one REJECTED** |
| Approved earnings | **$0.00** |
| Payout requests | **1, REJECTED** |

### What actually happened, from the audit trail

**All 22 clips carry the identical rejection reason: "botted views buddy".** They were rejected in a
single sweep between `2026-08-03 17:15:10.457` and `2026-08-03 17:17:11.819`, roughly two minutes, one
clip at a time.

**The actor on every one of those `REJECTED_CLIP` audit rows is `cmn4m6lh`, whose role is OWNER.**

**His payout request was rejected with the same words:** payout `cms98o8q`, requested
`2026-07-31 17:51:19.101` for **$52.08** gross (**$45.31** net), status **REJECTED**, reason
**"botted views buddy"**, `paidAt` null so no money ever moved.

**The sequence is coherent and deliberate.** He joined on 30 July, submitted 22 clips across two days,
accrued enough to request $52.08 on 31 July, and on 3 August the owner reviewed the account, rejected
the payout and then rejected every clip. **This is enforcement working, recorded, and attributable.**

### The one genuine anomaly found, and why it is not the cause

**Clipper F has no row in `auth_accounts` and no row in `auth_sessions`.** He is not unique:
**68 of 1,379 users have no `auth_accounts` row, 31 of them CLIPPERs**, and **23 of the 68 have
submitted a clip at some point**, so they demonstrably authenticated successfully once. They span
`2026-03-24` to `2026-08-07`, so it is not a single migration artifact.

**It is very probably harmless, and I checked rather than assumed.** `src/lib/auth.ts:91` sets
`strategy: "jwt"`, so sessions live in a cookie and an empty `auth_sessions` is expected for everyone.
And the Discord provider sets **`allowDangerousEmailAccountLinking: true`** (`auth.ts:65`), so on the
next sign-in the PrismaAdapter re-attaches an Account row to the existing user by verified email rather
than failing with `OAuthAccountNotLinked` or minting a duplicate. **A missing row self-heals at next
login.**

**Reported because it is real and unexplained, not because it explains this.** The honest position is
that 23 users lost a row they once had, nobody knows how, and it is worth a separate look. It does not
account for Clipper F, whose situation is fully explained by 22 rejections.

---

## PART 2 — EVERY SCREEN HE WOULD TOUCH

Traced against his actual data rather than guessed.

| Screen | What it does for him | Throws? |
|---|---|---|
| **Login** | Works. Not banned, Discord linked, JWT strategy, 30-day `maxAge` so an 11-day-old session would still be valid, and a fresh login re-links cleanly | **No** |
| **Clips page** | Renders 22 clips, every one marked REJECTED, **each showing "Reason: botted views buddy"** | **No** |
| **Submit modal** | Works. He has one active APPROVED verified Instagram account, so submission is available | **No** |
| **Earnings page** | Renders $0.00. He has no APPROVED clips, so `campaignBalances` is empty | **No** |
| **Payout screen** | Renders and correctly offers nothing | **No** |
| **Campaigns list** | Normal | **No** |
| **Mobile drawer** | Normal | **No** |

**Nothing errors, and no line throws.** There is no stack trace to name because there is no exception
to name.

### Against the specific recent changes the brief flagged

* **BL-762 and BL-766, the per-campaign minimum explanation and the global clamp.** BL-766's own report
  warned that `/api/earnings` clamps per-campaign figures to the global balance, so campaigns can be
  dropped entirely for a clipper at $0.00, which had already hidden money from two clippers.
  **Clipper F is at $0.00, so he is exactly the shape that concerned BL-766.** But the failure mode
  there was *money being hidden*, and **he has no money to hide**: no approved clips, no balance, no
  unwithdrawn cents. The clamp has nothing to clamp. **The path is inert for him.**
* **BL-757, per-clip CPM overrides.** Requires an approved clip with earnings. He has neither. Inert.
* **BL-747 and BL-746, the Instagram submit path.** He is an Instagram clipper, so this is the one
  change that could touch him. **But it shipped 2026-08-09, nine days after his last submission.** He
  has never executed that code.
* **BL-741 and BL-739, the mobile drawer.** Shipped 2026-08-08. Same exclusion.
* **BL-750 and BL-755, YouTube view handling.** He has no YouTube account. Inert.

**His data takes no untested path, because his data reaches almost none of the new code at all.**

---

## PART 3 — WHAT "NOT WORKING" MOST LIKELY MEANS, RANKED

1. **He sees $0.00 and 22 rejected clips, and calls that "not working". Most likely by a wide
   margin.** It fits every fact: the balance is zero because the earnings were refused, the payout was
   refused, and there is nothing to withdraw. **From inside, an account that yields nothing can feel
   identical to an account that is broken.**
2. **He disagrees with the rejection and is raising it obliquely.** Also plausible. "My app is not
   working" is a low-cost opening that does not concede the botting finding. **Not an accusation, just
   a reading the owner should hold alongside the first.**
3. **A stale installed PWA serving old code. UNVERIFIED and untestable from here.** BL-649 established
   iOS snapshots a PWA at install time, so an old install can run weeks-old JavaScript. **No user agent
   and no client version is stored anywhere**, because the JWT strategy writes no session rows, so
   there is no signal to check. **How the owner would tell:** ask him to open the site in Safari or
   Chrome directly rather than the installed icon. If it works in the browser and not the icon, it is a
   stale install, and deleting and re-adding the icon fixes it.
4. **He cannot log in.** Unlikely. Not banned, and the missing `auth_accounts` row self-heals via email
   linking. **Cannot be fully excluded without him trying**, which is why the question in PART 5 is
   phrased to catch it.
5. **A genuine defect in code he has never run.** Effectively excluded by the timeline.

---

## PART 4 — HOW MANY OTHERS ARE LIKE HIM

| | |
|---|---|
| Clippers with **every** clip rejected | **49** |
| Of those, with 5 or more clips | **8** |
| **Of those, with 20 or more clips** | **1, which is Clipper F** |
| Clips rejected with a bot-related reason | **132**, across **35 distinct clippers** |
| Payout requests rejected for bot reasons | **7**, across **7 distinct clippers** |

**Bot enforcement is routine here, not exceptional.** 35 clippers have had clips rejected for it and 7
have had payouts refused. **Clipper F is the most extreme single case on the platform**: nobody else
has had 20 or more clips rejected outright.

**On silent drop-off:** none of the 68 users lacking an `auth_accounts` row has been active in the last
7 days, and the most recent clip from any of them is `2026-08-03 07:13:53`. **That looks alarming and
probably is not.** The group is defined partly by inactivity, so the correlation is expected: people
who stopped using the platform are over-represented among people whose rows went stale. **Stated as an
open question rather than a finding**, because the direction of causation was not established and
23 of them did once submit clips successfully.

---

## PART 5 — THE VERDICT AND THE REPLY

> ## **The app is not broken, for him or for anyone. Clipper F has $0.00 and nothing to withdraw because the owner personally rejected all 22 of his clips and his $52.08 payout on 2026-08-03 for botted views, and the app already displays that reason on every clip.**

**This is the BL-762 pattern in reverse.** There, a clipper opened a ticket because a screen showed
$0.00 with no explanation and the platform was working correctly. **Here the screen does explain
itself**, on all 22 clips, and the complaint arrived anyway.

### The reply the owner can send

> Hey, I had a look at your account and everything on our side is working normally.
>
> Your clips were all reviewed on 3 August and were not approved. If you open the Clips page you will
> see the reason on each one. Because none of them were approved, your balance is $0.00 and there is
> nothing available to withdraw, which is probably what you are seeing.
>
> If you think a screen is genuinely failing to load, tell me which page you are on and what you see,
> and I will check it.

**Plain, factual, no accusation, and it does not re-litigate the decision.** It states the position,
points him at the reason he can already read, and leaves the door open for a real bug.

### The single most useful question, if the data cannot settle it

> **"Are you asking about the clips that were not approved, or is a page actually failing to load for
> you? If a page is failing, which one, and what do you see?"**

**One question, and it splits the two remaining possibilities cleanly.** If he names a page, there is
something to investigate. If he talks about the rejections, the matter is a decision rather than a
defect.

### Fix spec

**There is no defect to fix, and none should be invented.** Two optional items, neither urgent, neither
performed:

1. **The 23 users who lost an `auth_accounts` row they once had.** Cause unknown, effect probably
   nil given email re-linking. **Worth one round to establish how a row disappears**, because "unknown
   deletions in the auth table" is not a sentence anyone wants to leave standing.
2. **Nothing on the clips or payouts pages.** Both already state their position correctly for a
   zero-balance rejected clipper.

---

## WHAT COULD NOT BE MEASURED

* **Whether he can currently log in.** No session or user-agent rows exist to inspect, because the JWT
  strategy stores nothing server-side. **Only he can answer it by trying.**
* **Whether he is running a stale installed PWA.** No client version or user agent is recorded
  anywhere. UNVERIFIED, with the browser-versus-icon test given above.
* **Page-level error telemetry.** There is no client error log to query, so "no errors recorded" is
  not evidence of no errors. The screen-by-screen conclusions in PART 2 come from reading his data
  against the code, not from observed renders.
* **How 23 users lost an `auth_accounts` row.** Found, characterised, not explained.
* **What he actually means.** He gave no page, no error and no step, and no amount of database work
  substitutes for the one question in PART 5.
