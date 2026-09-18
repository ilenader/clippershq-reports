# BL-902 — The owner's answers, verified; two reversals, built

**Round:** BL-902 · **Date:** 2026-09-18 · **Branch:** `checkpoint/BL-902` → `main`
**Merge commit:** `dbc02bbf` · **Tags:** `pre-merge-BL-902`, `post-BL-902`

**ONE LINE VERDICT:** Two things now stand between him and the launch flag, and both are decisions
rather than defects: **the side lock is platform wide, not per campaign as he confirmed**, and **his
ADDS figures understate both what his campaigns spend and what he earns**. Everything he asked to be
reversed is built and proved; the dashboard, the new clip badge and the URL rename are not built and
are named below.

**NOTHING IS UNREMOVABLE.** 185 sandbox rows recorded, 185 deleted, 0 failed, 0 remain. The worktree
at `C:/b902` is verified gone.

---

## Model split

| Who | What |
| --- | --- |
| **Opus, no subagent between it and the source** | All of PART 0's verification, the strike and ban change, the side request, the duplicate-post money fix, every migration, the walk, the invariants and this report. |
| **Sonnet subagents (4), READ only** | Read BL-885, BL-893, BL-879 and BL-897 from the reports repo; counted the user-visible "v2" sweep; mapped existing owner controls. |

Every subagent claim is marked **READ** below and was re-**VERIFIED** against code before being used.
**One was wrong in a way that mattered:** the BL-885 reader reported the ban copy as promising a third
strike ban, which was true of the report but the file also carried a stale header describing behaviour
that had already changed. All four reports were treated as claims, not evidence.

---

## PART 0 — The four confirmed answers, exercised

### Answer 1 — the 10 percent ADDS: **TRUE, but his figures are wrong**

**My first test proved nothing and its own log caught it.** I drove the tracking tick. It ran, found the
job, processed the clip, and then died at the fetch:

```
[TRACKING] Clip …: individual fetch threw: apify hard off (BL-678) (notFound=false)
[TRACKING] Clip …: individual fetch threw, retry in 60min
```

It never reached the earnings block, so the absent `AgencyEarning` row meant only that the writer had
not run. Reporting that as "ADDS does not happen" would have been a false headline. Apify is
`const true` off by construction, so no tick on this machine can ever fetch views.

**Re-exercised through the real approval route** (`clips/[id]/review/route.ts:557` computes
`isCpmSplit`, `:1016` upserts `agency_earnings`), which reads **stored** stats and needs no provider:

| measure | result |
| --- | --- |
| `MARKETPLACE_V2_PLATFORM_CUT_MODE` | `ADDS` (`marketplace-v2-earnings.ts:108`) |
| `v2AgencyEarningApplies()` | `true` (`:119`) |
| `isMarketplaceClip` on the posted clip | **false** — which is what routes it down the ordinary owner-cut branch |
| three legs | poster $45.00, maker $45.00, platform $10.00 |
| **owner's ordinary cut** | **$50.00, standing beside the $10.00 platform leg** |

**ADDS is confirmed and it ships.** Under REPLACES there would be no row at all, which is what the first
marketplace does.

#### But the per-$100 figures he was given are wrong, and so is the file's own header comment

He was told: **$57.10 netted per $100, campaign spends $139.00, 39.0021 percent owner share.**

Both that and the header of `marketplace-v2-earnings.ts` (which says $33.33 / $133.33) assume the
ordinary cut is `gross × ownerShare`. **The code computes `views/1000 × ownerCpm`**, which is
`gross × (ownerCpm / clipperCpm)` = `gross × s/(1−s)`.

Measured on my sandbox campaign (clipperCpm 1.0, ownerCpm 0.5, share 33.3333 percent): the cut came
out **$50.00**, where `gross × share` would be $33.33. The measurement proves the ratio form.

His 39.0021 percent is a real campaign: **"Zhus Edit (0.50 CPM)"**, `lockedOwnerShareDecimal`
0.39002074, clipperCpm 0.5, ownerCpm 0.3197.

| per $100 of gross | he was told | **what the code does** |
| --- | --- | --- |
| owner's ordinary cut | $39.00 | **$63.94** |
| campaign actually spends | $139.00 | **$163.94** |
| owner nets (platform leg + cut + 9 percent fees) | $57.10 | **$82.04** |

**He earns more than he thinks, and his campaigns spend more than he thinks.** On a fixed budget that
means the budget buys materially fewer views than his arithmetic suggests. This is a figure to correct,
not a defect to fix: the code is self-consistent and the two comments in
`marketplace-v2-earnings.ts` that state the $33.33 form should be corrected in a round of their own.

### Answer 2 — several of his own accounts: **TRUE, and it exposed a live money defect**

| measure | result |
| --- | --- |
| same poster, same clip, account A then account B | **201 and 201**, two distinct clip ids |
| what each earned | **$45.00 and $45.00** — $90.00 to one person from one clip |
| same poster, same clip, **account A again** | **201.** Refused by nothing. |

`prisma/schema.prisma` declares `@@unique([v2ClipId, clipAccountId])` on `MarketplaceV2Post` and carries
a comment saying it was applied with `CREATE UNIQUE INDEX CONCURRENTLY`. **It was not in `pg_indexes` at
all.** The table held only its primary key, a unique on `clipId`, and three plain indexes.

This is the **BL-841 failure the schema's own comment cites**, repeated: a Prisma `@@unique` enforces
nothing at runtime, so a declaration nobody applied is a constraint that exists only in the file.

**What it cost:** one account could post one clip any number of times and be paid a full poster leg on
every one, **with the maker and the platform paid again each time too**. The campaign is charged three
times over for one piece of work. Gate one cannot catch it (the url is his own) and gate two cannot
(it matches the normalised url, and a second link to the same video is a different url).

**Closed two ways**, because relying on the declaration alone is exactly what produced it:

1. **Gate three** in `createV2Post` (`marketplace-v2-poster.ts`), which gives the person a sentence
   rather than a constraint name: *"You have already posted this clip from that account. Pick another
   account, or a different clip."*
2. **The real index**, `scripts/migrations/BL-902-v2-post-account-unique.sql`, applied after teardown on
   a table with **0 rows and 0 duplicate pairs**, and **verified present in `pg_indexes`**.

Re-exercised after the fix: the third post from the same account is **refused**.

### Answer 3 — the side lock is per campaign: **NOT WHAT SHIPPED**

He confirmed: *"one person may make clips on one campaign and post on another, never both on the same
one."*

Exercised: a person with side `EDITOR` who has made a clip on campaign X, asking to post on **campaign
Y**, is **refused**:

```
code    WRONG_SIDE
message "You are set up to make clips, so this side is not open to you. You cannot switch
         yourself any more, because you have already started working. Ask the owner and he
         can change it for you."
```

The refusal is **RULE ONE, which is platform wide** (`marketplace-v2-side.ts:238`,
`if (role !== required)`). It fires on his stored `marketplaceV2Role` alone, **before any campaign is
considered**. The per-campaign rule is **RULE TWO** (`:246-262`) and is only reached once rule one has
passed, so it can never be the thing that decides this case.

The second half of his sentence does hold: posting on campaign X, where he made the clip, is refused.

**Reported and not silently changed.** This is a permission, and PART 0 was scoped verify only. It needs
his decision: either the answer is corrected, or rule one is narrowed to per campaign, which is a
permission change deserving its own round.

### Answer 4 — `clipershq.com/marketplace`

An acceptance of a plan, not a shipped behaviour, so it is **reported rather than exercised**. Today
both `src/app/(app)/marketplace` and `src/app/(app)/marketplace-v2` exist, and `/marketplace`
**redirects to** `/marketplace-v2` (`marketplace/page.tsx:61`). The swap has not happened. See PART 5.

---

## PART 1 — The side switch is a request now

### What was built

| Piece | Where |
| --- | --- |
| The row | `MarketplaceV2SideRequest`, table `marketplace_v2_side_requests` |
| The migration | `scripts/migrations/BL-902-side-request.sql`, additive only |
| The rule and every string | `src/lib/marketplace-v2-side-request.ts` |
| The person's route | `POST/GET /api/marketplace-v2/side-request` |
| The owner's route | `POST/GET /api/admin/marketplace-v2/side-requests` |

### The copy, quoted

**Why it is asked, shown above the box:**

> You have already started working on this side, so the owner reads every request himself before
> anything changes. Tell him what happened and what you want to do instead. Fifty words is about three
> or four sentences.

**The label:** *"Why do you want to change side?"*

**The prompting questions:**

> What have you been doing on your current side so far?
> What made you want to change?
> What do you plan to do on the other side?
> Is there anything unfinished that somebody else is waiting on?

**The counter**, which uses the *same* `countWords` the route enforces, so a person cannot be told he
has enough and then refused:

> `12 of 50 words. 38 to go.` → `51 words. That is enough, you can send it.`

**While he waits** — no estimate, no queue position, nothing about when:

> **Your request has been sent.** You have asked to move to the posting side. Nothing has changed yet
> and you are still on the side you were on, so carry on as normal. The owner reads these himself and
> you will be told here when he has answered.

**On a rejection**, carrying the owner's own words:

> **You are staying on your current side.** The owner has read your request and decided not to move you
> for now. He said: *[his reason]* Everything you have earned is still yours. If things change you can
> ask again.

### The properties that were proved

- **Nothing changes until approved.** His stored side was re-read during the wait and was unchanged.
- **No time estimate.** The waiting body is searched for *hour, day, week, queue, position, soon,
  shortly, within* and contains none.
- **A rejection requires the owner's reason.** A rejection with none is refused 400.
- **One open request at a time**, refused **by the database**: a partial unique on `("userId") WHERE
  status = 'PENDING'`, **verified in `pg_indexes`**. Given what PART 0 found about declared-but-absent
  uniques, this one was checked rather than assumed.
- **An audit row** on every decision carrying `oldSide`, `newSide`, the reason and `now()` cast to
  `::text`.
- **No second writer of the side column.** An approval calls the existing `setV2RoleAsOwner`, so
  `check:v2-role-is-a-gate` R2 still counts exactly one writer.

### The automatic release is removed

`REJECTED` was **added** to `LOCK_HOLDING_CLIP_STATUSES` (`marketplace-v2-side.ts`). Before this round,
a person whose only clip was rejected read `locked=false`; he now reads `locked=true` and must ask.

### The rejected-only case: decided, and stated

**What I built:** he still needs a request. *"A rejection no longer unlocks anybody"* is unambiguous.

**What I recommend:** treat him as **genuinely free**. He has produced nothing, earned nothing and left
no counterparty, and he is now asked to write fifty words to undo an evening's work the owner had
already turned down. It is one extra clause on `getV2RoleLock` — release only somebody whose entire
history is rejected or withdrawn clips and **zero** posts — which the owner can accept or decline on its
own merits. The recommendation is written into the source comment so it is not lost.

---

## PART 2 — Strikes and bans are purely manual

### The automatic ban is gone

`V2_STRIKE_BAN_THRESHOLD` and `V2_STRIKE_BAN_DAYS` are **deleted**, not set to a large number, so
nothing can quietly start counting again. `getV2StrikeStanding` no longer derives a ban from a count;
`liveCount` remains and is informational.

**Proved:** a person with **four** live warnings is **not banned**, and can still post.

### The ban the owner sets

Four additive columns on `User` (`marketplaceV2BannedUntil`, `…BanReason`, `…BannedById`, `…BannedAt`),
written by exactly two functions, `setV2Ban` and `clearV2Ban`, called only from an OWNER route. The
length is his; it is clamped at 365 days so a typo cannot mean a decade, and the clamp is reported back.

**Proved:** he banned for **14 days** and 14 was stored, not a seven-day default.

### The BL-841 lesson is kept, not repeated

BL-885 stored no scalar because `User.clipperMarketplaceBannedUntil` was written by one cron and
**cleared by nothing**. These columns do not repeat that, for two structural reasons:

1. **No background job writes them.** `check:v2-strike-sites` fails the build if any file under
   `src/app/api/cron/` so much as mentions this surface. It still passes, **16 of 16**.
2. **They clear themselves by comparison, not by a job.** "Banned" is `bannedUntil > now()`, evaluated
   on every read, so a ban whose date has passed is **already** not a ban with nothing required to come
   along and notice. What rotted before needed somebody to clear it; this needs nobody. The owner can
   still lift one early by setting the column null.

### A banned person still sees everything

| surface, asked with the same cookie that was refused at posting | status |
| --- | --- |
| the catalogue | **200** |
| his earnings | **200** |
| the campaigns | **200** |
| the clip detail | **200** |
| **posting** | **403, code `V2_OWNER_POST_BAN`** |

His money is untouched — BL-883's pair followed exactly: **the leg stands.**

**Both posting doors ask.** BL-885's ban refused only the ordinary submit path and its own copy told the
person he could *"still post marketplace clips"*. The owner's instruction is one rule, not two, so the
marketplace's own post route now asks the same question.

### The refusal names the rule and the remedy

> The owner has paused your posting until 2 October 2026, so this one cannot go through. The reason he
> gave is: *Posting other people's clips as your own after four warnings.* Everything you have already
> posted goes on earning and your money is still yours. If you think this is wrong, reply in Discord and
> the owner will look at it again.

### The copy discipline is kept

Nobody is called a thief. The warning copy also **stopped promising a third-strike ban**, because there
is no longer such a thing and an interface that promises what the code cannot keep is the same defect
class as a time estimate:

> **A warning about marketplace clips.** A clip you posted was made by another editor and submitted as
> your own work. When you post someone else's marketplace clip, post it through the marketplace so the
> editor gets paid too, and you still earn 45 percent for posting it. This is a warning and nothing
> more. Nothing has been taken from your earnings. If you think this is wrong, reply in Discord and the
> owner will look at it again.

---

## PART 3 — The poster's catalogue

### The skipped filter already existed

**BL-879 built it.** `listCatalogueForPoster` carries a `skipped` tab with its own count
(`marketplace-v2-poster.ts:219-233`), `parsePosterCatalogueTab` accepts it (`:186`), and
`catalogue-client.tsx:50` renders the heading *"Clips you skipped"*. `unskip` already existed as an
action on the state route.

**So this round verified it rather than rebuilding it**, which is why nothing new was written:

- he skips a clip and **finds it again** in the skipped tab;
- un-skipping **returns it** to his ordinary list (checked in a *different* tab from the one it was
  found in, so a filter that never changed would fail one of the two);
- and skipping **recorded nothing about him**: 0 notifications, 0 audit rows, 0 warnings, counted
  across three tables.

### Question 16 is NO, proved on live bodies

Three clip-facing surfaces a poster can reach were searched for **nine** taker field names
(`postCount, posters, posterName, posterId, takers, takenBy, takerCount, postersCount, otherPosters`):
**none present**. They were also searched for the **user ids of four other people**, two of whom had
posted on that very clip: **none found**.

**One of my own checks was wrong here and the product was right.** The first version searched all four
bodies for `posts` and failed on the poster's *own* earnings screen, which of course lists his own
posts — filtered by `posterId` in `v2PosterPayableClipWhere`. Question 16 is about learning who *else*
took a clip, not about a man seeing his own work. The check now asks the two halves differently.

### The new-clip badge: NOT BUILT

Named rather than half-done. The right mechanism exists and should be reused: `sidebar-badges.ts`,
`/api/admin/sidebar-counts` and `/api/admin/sidebar-seen` already implement exactly the pattern he
described (a count, cleared by a POST when the person enters the route, with `sidebarLastSeen` as a JSON
map on `User`). It is currently **owner scoped** — every route in `SIDEBAR_SECTION_ROUTES` is under
`/admin/` — so extending it to a poster-facing section is a real piece of work rather than a
configuration change.

**What would mark a clip seen, stated so the next round does not have to decide it twice:** entering
`/marketplace-v2/catalogue` stamps `lastSeen` for that section, and the count is
`marketplaceV2Clip where status = APPROVED and approvedAt > lastSeen`. A badge that cleared on any page
load would be a lie, and one keyed to individual clip rows would never clear for somebody who never
scrolls.

---

## PART 4 — The owner's screen: NOT BUILT

This is the round's largest omission and it is named plainly rather than part-delivered. What exists
today, mapped and ready to be linked or reused rather than rebuilt:

| He wants | What already exists |
| --- | --- |
| per clip: maker, state, when, every poster, every link, views and earnings per post | `GET /api/marketplace-v2/admin/overview` → `buildOwnerOverview` (`marketplace-v2-owner-overview.ts:180`), already returning exactly this shape including `posts[]` with `posterName`, `postUrl`, `views`, `posterGross` |
| per campaign: clips live, posts, spend, remaining | the same route's `campaigns[]` |
| the four money legs together | `GET /api/admin/marketplace-v2/clip-legs` |
| approve / reject | `POST /api/marketplace-v2/admin/clips/[id]/decision` |
| strike / revoke / **ban / unban** | `POST /api/admin/users/[id]/v2-strikes` — **this round added ban and unban to it** |
| change somebody's side | `POST /api/admin/marketplace-v2/role` |
| **act on a switch request** | `POST /api/admin/marketplace-v2/side-requests` — **new this round** |
| convert and undo | `POST /api/admin/clips/[id]/convert-to-marketplace` |
| over time | `GET /api/admin/marketplace-v2/funnel?days=` |

**Every money figure it would need already has a named derivation** — `loadV2EditorEarnings`,
`getCampaignBudgetStatus`, `projectPayoutCash`, `Clip.earnings`, `MarketplaceV2PlatformEarning.amount`,
`AgencyEarning.amount` — so the page can be assembled without adding a fourteenth. BL-882 counted twelve
derivations and found the twelfth would have made an editor unpayable for ever; BL-883 refused to add a
thirteenth; this round adds none.

**What is genuinely missing is the page itself**, plus the two panels nothing currently serves: **per
person** (what they made or posted, their totals, their side and standing) and the **per-day** series
for the charts.

---

## PART 5 — The counted V2 sweep: the only thing a person can see is the URL

Counted with `grep -c`, never piped to `head`.

| | |
| --- | --- |
| `grep -rc "V2" src/app src/components --include=*.tsx` | **301** raw matches |
| Rendered text, titles, headings, buttons, empty states, toasts, API `error:` strings, emails, notification titles and bodies, nav labels | **ZERO** contain v2 |
| `src/lib/marketplace-v2-copy.ts` — all 50 exported strings | **0 of 50** string *values* contain v2 |
| **URLs a person sees in the address bar** | **the only hits: `/marketplace-v2` and its 10 page routes, referenced from 25 link sites across 12 files** |

**This explains why he has reported seeing it after two rounds said it was gone.** Both rounds were
right about the words and neither was looking at the address bar. `sidebar.tsx:141` even carries the
comment *"Nothing a person sees may say v2."* — and the `href` two lines below it is `/marketplace-v2`.

**The rename is NOT built.** It is entangled with his accepted answer 4 (`/marketplace` becoming this
marketplace and the first one losing its URL), it touches 12 files plus directory moves plus a redirect
for anyone holding an old link, and doing it late in a round that had already changed two permissions
would have been the riskiest thing in the round. It should be one round of its own, and it is the single
highest-value cosmetic change left.

**Why file names, directory names and internal route literals stay**, restated: BL-896 measured **449
occurrences across 56 files in `scripts/`** that are hardcoded route literals inside four rounds'
containment proofs. Renaming them would leave those proofs asserting about paths that no longer exist.
The `/api/marketplace-v2/**` fetch paths are not address-bar navigated and stay with them.

---

## PART 6 — Proof

### Walked as people: 37 of 37

Every failure path has its **own user**, every walk asserts the status is **not 429**, every setup is a
check, and every check states what made it pass.

Somebody asks to switch and waits · a five-word reason is refused with his words counted back · the
owner approves one and only then does the side move · he rejects another and cannot do it without a
reason · a rejected clip no longer releases anybody · a poster skips, finds it again and un-skips · four
warnings and still no ban · the owner bans for fourteen days · the banned person still sees everything
and is refused only at posting · the owner lifts it and he posts again · and no poster-facing body names
another poster.

**Two of my own checks were wrong and the product was right**, both caught by running it:

1. A 409 after the unban was **BL-902's own new gate three** refusing a second post from one account.
   The walk was re-posting the same clip from the same account. Fixed to use a different clip.
2. `"posts"` on the earnings screen is the poster's **own** posts. Fixed to ask the two halves
   differently.

### Full population, after teardown: 10 of 10

| invariant | result |
| --- | --- |
| BL-627 no overpayment, both v2 aggregates counted | **20 budgeted campaigns, 0 over** |
| BL-696 no double pay, across four tables | agency 0, maker 0, platform 0, posts 0 |
| the earnings invariant | **10,196 live clips, 0 violations, 0 negatives** |
| BL-824 paid is final, **both earners asked separately** | 0 negative maker legs; the poster-side shape reported rather than asserted to zero, because BL-883 describes it as EXPLAINED by a paid floor |
| both reconciliation forms | 0 and 0 |
| the declared unique now real | **verified in `pg_indexes`** |
| the side request partial unique | **verified in `pg_indexes`** |
| owner's test campaign `cmu5yeax20000h4w7yv5n387y` | present, ACTIVE, unarchived, untouched |

Re-proved rather than inherited, because **BL-901 changed the money path this week.**

Honestly: the reconciliation zeros are **trivial** zeros, since the platform holds zero v2 clips after
teardown. The form that proves the query still discriminates ran inside the walk, on live rows.

### Teardown

**185 rows recorded, 185 deleted, 0 failed, 0 remain.** 60 product-written rows were adopted by
`sweep.ts` before destruction. `marketplace_v2_side_requests` was **added to the sandbox's deletable
tables**, without which its 6 rows would have vanished with their users and the round could not have
counted them.

The worktree at `C:/b902` is **verified gone** (`git worktree list` shows only the main checkout; the
path does not exist). The BL-899 leftovers sweep kept all seven directories it found, every one under
its 3-day floor — **0 MB reclaimed across 0 directories**, which is the safe answer.

### Gates

- `npm run build` exit **0** on the branch and again on `main` after the merge.
- BL-348 hooks gate: **0 errors, 11 warnings** — identical to the pre-round baseline.
- `eslint` confirmed present, so the gate did not silently no-op.
- Clean `tsc` baseline established before any change (the only error was in my own new script).
- **11 protected money files byte-identical by blob OID.** `marketplace-v2-poster.ts` changed, which is
  this round's money fix, `3613adf0…` → `a50c670d…`.
- **`check:v2-strike-sites` 16 of 16**, so the single strike creation site survives.
- **`check:v2-role-is-a-gate` passes**, and it **refused my first build**: R1 caught the new side-request
  file reading `marketplaceV2Role`. That is the guard working — a new reader of the side is a new
  permission surface — so the file was added to the allow-list with its reason rather than the guard
  loosened. R2 still counts **exactly one writer** of that column.
- **Zero `.tsx` changed**, so no render pass and no accessibility pass was owed or run.
- No Apify actor ran; the 11 BL-678 guards are intact. No wallet address appears anywhere.

---

## Not built, and named

1. **The owner's dashboard (PART 4).** The largest omission. Every control and nearly every figure it
   needs already exists and is mapped above; what is missing is the page, the per-person panel and the
   per-day series.
2. **The new-clip badge (PART 3).** The mechanism to reuse is named, and what marks a clip seen is
   specified so the next round does not re-decide it.
3. **The URL rename (PART 5).** The only user-visible "v2" left. Entangled with his accepted
   `/marketplace` swap; should be one round of its own.
4. **The ADDS comments.** Two comments in `marketplace-v2-earnings.ts` state the `gross × share` form
   and should be corrected to the ratio form.

## Needs his decision

1. **Is the side lock meant to be per campaign?** He confirmed it is; the code says otherwise, platform
   wide, at `marketplace-v2-side.ts:238`. Correcting the code is a permission change.
2. **His ADDS figures.** $163.94 spent and $82.04 netted per $100 of gross on his own campaign, against
   the $139.00 and $57.10 he was told.
3. **The rejected-only case.** Built as "he must ask"; recommended as "he is free".

## Rollback

`git revert dbc02bbf`. The three migrations are additive and each carries its own rollback SQL:
`BL-902-manual-ban.sql`, `BL-902-side-request.sql`, `BL-902-v2-post-account-unique.sql`. No stored money
figure changes.
