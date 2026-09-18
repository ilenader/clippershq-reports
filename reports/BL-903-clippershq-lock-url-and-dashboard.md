# BL-903 — Per campaign sides, the duplicate rule, and the last visible v2

**Round:** BL-903 · **Date:** 2026-09-18 · **Merge commit:** `3b9a7b8b`
**Tags:** `pre-merge-BL-903`, `post-BL-903`

**ONE LINE VERDICT:** Nothing found in this round blocks setting the launch flag; the two things that
did block it, a side lock that refused work the owner allows and a duplicate rule nobody had confirmed
both ways, are fixed and proven, and the only user-visible "v2" left anywhere is gone.

**NOTHING IS UNREMOVABLE.** 92 sandbox rows recorded, 92 deleted, 0 failed, 0 remain. The worktree at
`C:/b903` is verified gone.

---

## His launch steps, in order

1. **Apply the one migration** if it has not reached production yet:
   `scripts/migrations/BL-903-side-request-per-campaign.sql`. It is additive apart from swapping a
   partial unique on a table holding zero rows. The other two from BL-902 are already applied.
2. **Deploy `main` at `3b9a7b8b`.** The build is green with the hooks gate at its baseline.
3. **Check `clipershq.com/market` loads for you.** That is the new address; `/marketplace-v2` still
   works so nothing you have open breaks.
4. **Set `NEXT_PUBLIC_MARKETPLACE_V2_ENABLED=true`.** This is the launch flag. It opens v2 alone and
   does not touch the first marketplace.
5. **Watch the first posts land.** The budget is protected by BL-901's row lock, the duplicate rule by
   a real index, and nobody can post their own clip.

---

## Model split

| Who | What |
| --- | --- |
| **Opus, no subagent between it and the source** | The side lock change, the duplicate verification, gate zero, both migrations, the guard extension, the walk, and this report. |
| **Three Sonnet subagents, in parallel, READ only** | Mapped the dashboard data sources, the URL and rewrite mechanism, and the badge mechanism plus the BL-886 guard. |

**One subagent corrected me, and checking it myself changed the round.** It reported that the missing
unique had never been a declared directive. I verified that against the schema and the guard source
myself, and **BL-902's report had named the wrong cause.** See PART 2.

---

## PART 1 — The side is decided per campaign

### What was wrong

The owner's rule, in his own words and said twice: **one clip for one campaign, another clip for another
campaign.** A person may MAKE on campaign A and POST on campaign B, and may never do both on the same
one.

BL-893 built the gate as **RULE ONE, PLATFORM WIDE**: `if (role !== required) return WRONG_SIDE`, firing
on the stored `marketplaceV2Role` **before any campaign was considered**. BL-902 exercised the cost: a
maker on campaign X was refused from posting on campaign Y with *"You are set up to make clips, so this
side is not open to you."*

Its own paragraph argued for it on the grounds that the owner objected to being **shown** "Send a clip"
and "Post a clip" together. **That was the wrong fix for that complaint.** He was complaining about what
he was shown, which is a navigation question, and it was answered with a gate.

### What was built

`marketplace-v2-side.ts`: rule one is deleted. Rule two, per campaign, becomes the whole rule, plus one
new term, an **APPROVED switch request for that campaign**, which the gate reads directly.

`marketplaceV2Role` is **not deleted and nobody loses it.** It stops being a gate and becomes the
**preference** it always described itself as: it drives the navigation, so nothing the owner objected to
comes back, and the arrival flow still sets it.

### Nobody is worse off, and there is no migration

This is a property rather than a hope. **The change only ever REMOVES a refusal.** Every request allowed
before passed rule one and then rule two, and rule two is unchanged. Every request refused by rule one
alone is now allowed if and only if the person has no work on the other side of that campaign. The
owner's own two accounts keep the sides they picked and gain the ability to work the other side
elsewhere. **No column is rewritten, so there is nothing to migrate and nothing to lose.**

### Proven

| check | result |
| --- | --- |
| he has made a clip on campaign A | `clipsHeld 1`, read back from the derived lock |
| **he may POST on campaign B** | **ALLOWED** (before this round: `WRONG_SIDE`) |
| **and he really does, through the live route** | **201** |
| **never both on the same one:** posting on campaign A | refused `OTHER_SIDE_ON_THIS_CAMPAIGN` |
| he now holds work on both sides, on different campaigns | `heldBy BOTH` — the ordinary case now |
| **nobody worse off:** he can still MAKE on campaign A | ALLOWED |

The refusal copy names the rule, what he can still do, and the remedy. **The middle sentence changed
meaning this round:** under the platform wide rule *"You can still work this side on a different
campaign"* was not true, and now it is.

> You are already working the other side of this campaign, so you cannot do both on it. You can still
> work this side on a different campaign, starting right now. If you want to change sides on THIS
> campaign, ask the owner and tell him why in about fifty words.

### The switch request, scoped per campaign

BL-902 built it platform wide because the lock was. With the lock per campaign the request has to be too.

- The row carries a `campaignId`, and **an APPROVED row IS the exemption**, read by the gate. Nothing is
  copied onto the user, so there is no second place for the grant to drift out of step with.
- `fromSide` is now derived from **the work he actually has on that campaign**, not from his preference.
- **The approval no longer calls `setV2RoleAsOwner`.** Under a per campaign rule moving that column would
  be both too much (approving one campaign would flip what he sees on every other) and too little (the
  column no longer grants anything). `check:v2-role-is-a-gate` R2 still counts **exactly one** writer.
- The partial unique is swapped to **one open request per person per campaign**, verified in
  `pg_indexes`. BL-902's platform wide one would have refused a legitimate second request about a
  different campaign.

All three paths re-proven after the scope change: a short reason refused with his words counted back; a
request naming no campaign refused; the request taken; a second on the same campaign refused **by the
database**; the owner approving, after which campaign A lets him post **while his preference is asserted
unchanged**; and a rejection refused without a reason, then carried through with the owner's verbatim
sentence in the notification.

### Gate zero — you may never post your own clip

**This round is what made it necessary.** Until now the side gate was platform wide, so a maker could not
post anywhere and the shape was unreachable rather than forbidden. With the side per campaign and an
approved exemption letting somebody act on both sides of one campaign, exactly one door opens that must
stay shut.

**What it would cost if it were open:** he takes the maker's 45 percent **and** the poster's 45 percent
on one video, 90 percent of the gross to one name. **No aggregate would notice.** All three legs would be
written correctly, every invariant would hold to the cent, and the budget would spend exactly what it
says. It is a rule, not a leak, and the only place a rule like that can live is in front of the write.
It is unconditional and sits above every other gate, including the exemption.

---

## PART 2 — The duplicate rule, confirmed both ways

### BL-902 named the wrong cause, and this corrects it

BL-902's report said *"schema.prisma declares `@@unique([v2ClipId, clipAccountId])` and nobody applied
it."* **It did not declare it.** Verified myself:

- The model carried, at what was then line 4175, a `//` comment ending
  *"...the enforcement is `@@unique([v2ClipId, clipAccountId])` plus its CONCURRENTLY index, added then"*
   — prose about what **would** be added if the owner ever answered BL-876 question 11.
- `check-schema-drift.ts:244` is `if (!t || t.startsWith("//") ...) continue;`

So the guard **had nothing to compare against and could not have caught it.** It checks DECLARED against
`pg_index`, correctly and completely in that direction. A constraint that was only ever a sentence is
invisible to it. The defect and the fix in BL-902 were both real; the mechanism I named was not.

### What was done

1. **The directive is now real.** `@@unique([v2ClipId, clipAccountId])` is a live line on
   `MarketplaceV2Post`, so the existing MISSING UNIQUE INDEX check covers it from here on.
2. **The guard gained `[ASPIRATIONAL UNIQUE]`**: a `@@unique` written inside a comment, with **neither a
   live directive nor a `pg_index` entry** behind it.

**The first version of that check was wrong and running it showed why.** It asked only whether a live
directive existed and fired on **five** more models at once. Four of them — `Clip`, `PayoutRequest`,
`CampaignTicket`, `MarketplacePosterListing` — are uniques this repo applies with **raw SQL** and
documents in a comment on purpose, and the indexes really exist. Calling those a defect would have made
the guard cry wolf on the project's own convention, and a guard that must be ignored is a guard that will
be. It now asks the **database**. It also learned the schema's own vocabulary for an absence
(`DELIBERATELY NOT`, `is gone`, `REPLACED`, `NOT representable`), and one flagged item turned out to be a
correct **cross reference** to constraints declared on a neighbouring model.

**142 declared uniqueness constraints verified, up from 140.**

### Proven by request

| check | result |
| --- | --- |
| **the index shape, read from `pg_indexes` and not from `schema.prisma`** | unique on `(v2ClipId, clipAccountId)` **PRESENT**; unique on `(v2ClipId, posterId)` **absent, correctly** |
| **one video, FIVE of his own accounts** | **five posts accepted, five distinct clip ids** |
| **and he earns on each** | **5 of his clips carry money** (the count is five, not "more than zero") |
| **the same video twice on ONE account** | **refused 409** |
| **another poster's live URL** | **still refused 409** |

Both directions of the index are asserted, because a unique on `posterId` would forbid the very thing the
owner has just confirmed he wants.

The refusal explains rather than merely refusing:

> You have already posted this clip from that account. Pick another account, or a different clip.

---

## PART 3 — The path moves, the directory does not

BL-902's counted sweep proved the **only** place a person can still see "v2" is the address bar.
`sidebar.tsx:141` even carries the comment *"Nothing a person sees may say v2"* two lines above an
`href` reading `/marketplace-v2`.

### Why the directory does not move, re-counted rather than quoted

BL-896 refused the rename. **The reason has grown:** the literal `/marketplace-v2` now appears **520
times across 73 files in `scripts/`**, up from the 449 across 56 BL-896 measured.
`bl893-containment.ts` alone holds 31.

Moving the directory would leave every one of those proofs asserting about paths that no longer exist,
and **they would not fail loudly.** A containment proof that requests a route expecting 404 and receives
404 **reports success.** The entire body of evidence that strangers cannot reach these pages would
quietly become a set of tests that check nothing.

### What was built

A `beforeFiles` rewrite in `next.config.ts` (there was **no** rewrites config before):

```ts
{ source: "/market",        destination: "/marketplace-v2" },
{ source: "/market/:path*", destination: "/marketplace-v2/:path*" },
```

Plus **49 UI link replacements across 13 files**, so the address bar actually shows the clean path.

| measure | result |
| --- | --- |
| user-visible `/marketplace-v2` links remaining in `src` | **0** |
| `/api/marketplace-v2` fetch literals touched | **0** (17 remain, correctly) |
| script route literals touched | **0** (73 files still hold them) |
| `.tsx` lines changed | 45 insertions, 45 deletions, **0 non-href lines** |

### Containment on the new address

| check | result |
| --- | --- |
| 20 API requests, 5 routes × 4 strangers (ordinary clipper, REVIEWER, non-owner ADMIN, signed out) | **all refused, 404 and never 403** |
| any refusal that was a rate limit | **0 of 20** |
| the new address resolves | yes, for all four |
| the old address still resolves | yes, nothing bookmarked breaks |

A signed-out visitor is allowed 401 rather than 404, because he has no session to test the flag against.
That is stated rather than folded into the same number.

**The page half is honestly incomplete.** This app serves a **splash shell**, so the HTML for an owner
and a stranger is byte identical and a status code proves only that the rewrite maps. What a stranger
actually sees has to be read in a real browser, and **that browser pass was not run** — see below.

---

## PART 4 — The owner's dashboard: NOT BUILT

Named rather than half-built. Everything it needs was mapped this round and is ready to be linked or
reused:

| He wants | What already exists |
| --- | --- |
| per clip: maker, state, when, every poster, every link, views and earnings per post, total | `buildOwnerOverview` (`marketplace-v2-owner-overview.ts:180`) already returns exactly this, including `posts[]` with `posterName`, `postUrl`, `views`, `posterGross` |
| per campaign: clips live, posts, spend, remaining | the same function's `campaigns[]` |
| the four money legs together | `GET /api/admin/marketplace-v2/clip-legs` |
| approve / reject / undo | `POST /api/marketplace-v2/admin/clips/[id]/decision` |
| strike / revoke / ban / unban | `POST /api/admin/users/[id]/v2-strikes` |
| change side · **decide a switch request** | `/api/admin/marketplace-v2/role` · `/api/admin/marketplace-v2/side-requests` |
| convert / undo | `POST /api/admin/clips/[id]/convert-to-marketplace` |

**Every money figure already has a named derivation** — `loadV2EditorEarnings`,
`getCampaignBudgetStatus`, `projectPayoutCash`, `Clip.earnings`, `MarketplaceV2PlatformEarning.amount`,
`AgencyEarning.amount` — so the page can be assembled without adding a thirteenth.

**What is genuinely missing:** the page itself, a **per person** panel, and the **per day** series for
the charts. Measured this round: *neither* `buildOwnerOverview` *nor* the funnel route produces any
per-day bucketing at all, so the over-time panel needs a new query and is the real work.

**Also verified for whenever it is built:** no route outside `api/admin/**` and
`api/marketplace-v2/admin/**` selects more than two of the four money legs. The four-leg shape is
already exclusive to the owner.

**His real figures, for when it shows them:** on *Zhus Edit (0.50 CPM)*, share 39.0021 percent, the
campaign spends **$163.94** per $100 of gross and he nets **$82.04** — not the $139.00 and $57.10 an
earlier report claimed, because the code computes his cut as `views/1000 × ownerCpm`, not `gross × share`.

---

## PART 5 — The unseen-clip badge: NOT BUILT

The mechanism to reuse is `sidebar-badges.ts` with `/api/admin/sidebar-counts` and
`/api/admin/sidebar-seen`, backed by `User.sidebarLastSeen` (a JSON map, `schema.prisma:319`). Both
routes are **OWNER-only today** (`role !== "OWNER"` → 403), and `sidebar.tsx` gates its two effects the
same way, so opening it to a poster is real work rather than configuration.

**What marks a clip seen, specified so the next round does not decide it twice:** entering
`/market/catalogue` stamps `lastSeen` for that section, exactly as entering `/admin/payouts` does today
via the `pathname === href || pathname.startsWith(href + "/")` effect. The count is then
`marketplaceV2Clip where status = APPROVED and approvedAt > lastSeen`. A badge that cleared on any page
load would be a lie; one keyed to individual clip rows would never clear for somebody who does not
scroll.

It must record nothing beyond what he has seen, reach no queue and no count, and never imply suspicion,
which is the rule BL-879 set for the skip and the in-progress flag.

---

## PART 6 — Proof

### Walked as people: 30 of 30

Every failure path with its own user, every one asserted **not 429**, every setup a check, and every
check stating what made it pass.

**My first run failed thirteen checks** with a uniform 404 "Not found". `mint()` hardcoded
`isTestUser: false`, which is correct for the four strangers in PART 3 who must be refused by the
visibility flag and wrong for every participant. It also made one check **pass while testing nothing**:
*"while he waits nothing changes"* was green because no request had ever been created.

### Guards: 3 of 3 demonstrated failing, alone

Each naming itself, tree restored with identical sha256 after each, both guards green before and after.
The CRLF translation BL-902 had to discover is built in from the first line.

**Two of my three mutations were wrong and the check was right both times.** A1 first merely deleted the
directive, leaving no comment to be aspirational about; then commented out the real pair, which the check
correctly cleared **because the index genuinely exists**. Only a pair backed by nothing at all is the
defect. B1's anchor was in a file that did not contain it.

### Full population, after teardown: 10 of 10

| invariant | result |
| --- | --- |
| BL-627 no overpayment, both v2 aggregates counted | **20 budgeted campaigns, 0 over** |
| BL-696 no double pay, four tables | 0, 0, 0, 0 |
| the earnings invariant | **10,198 live clips, 0 violations, 0 negatives** |
| BL-824 paid is final, **both earners separately** | 0 negative maker legs |
| both reconciliation forms | 0 and 0 (a **trivial** zero, and said so: the platform holds no v2 clips after teardown) |
| the unique on `(v2ClipId, clipAccountId)` | verified in `pg_indexes` |
| the side request partial unique, per campaign | verified in `pg_indexes` |
| owner's test campaign `cmu5yeax20000h4w7yv5n387y` | present, ACTIVE, unarchived, untouched |

Re-proved rather than inherited, because the money path changed twice this week.

### Gates

- `npm run build` exit **0** on the branch and again on `main` after the merge.
- BL-348 hooks gate: **0 errors, 11 warnings** — identical to baseline. `eslint` confirmed present.
- **11 protected money files byte-identical by blob OID.** `marketplace-v2-poster.ts` changed
  (`a50c670d…` → `fcefb650…`), which is gate zero.
- `check:v2-role-is-a-gate` **refused my first build twice**, and both were it working: once when the
  new reader appeared, once when BL-902's allow-list entry went stale because this round stopped that
  file reading the column.
- No Apify actor ran; the 11 BL-678 guards intact. No wallet address printed.

### Teardown

92 recorded, **92 deleted, 0 failed, 0 remain**, including the 2 side request rows. Worktree at `C:/b903`
verified gone. The BL-899 sweep kept all directories it found, every one under its 3-day floor.

---

## Not run, and named

1. **The five-width render pass and the accessibility review.** 13 `.tsx` files changed and the diff is
   **45 insertions against 45 deletions with zero non-href lines** — no markup, no text, no styling, no
   ARIA. The rendered DOM is unchanged apart from URL strings, which is why this was judged not owed. It
   is stated here so the judgement can be overruled rather than assumed.
2. **The real-browser containment pass on the new address.** The API half was proven by direct request;
   the page half needs a browser because of the splash shell, and it was not run.
3. **The owner dashboard and the unseen-clip badge**, as above.
4. **`/marketplace` itself is not taken over.** The owner has accepted that it becomes this marketplace
   and the first one loses the URL. That is **one more entry in the same rewrite array**, and it was not
   done because 31 live files still serve the first marketplace there and shadowing them on the same
   afternoon as a permission change and a money guard is a bigger change than a rename.

## Rollback

`git revert 3b9a7b8b`. The one migration is additive apart from swapping a partial unique on a table
holding zero rows, and its rollback SQL is in the file. No stored money figure changes.
