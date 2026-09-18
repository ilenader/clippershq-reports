# BL-896 — the approval queue, its whole class, and the URL

**The blocker is fixed and proved at 2,000 pending clips by creating them. The same shape was found
twice more on the poster's earning screen. The URL moves on one environment variable.**

## The blocker, and it was worse than BL-895 reported

`/api/marketplace-v2/admin/queue` ran `findMany({ orderBy: createdAt asc, take: 500 })` with **no
`where`**. The failure does not wait for 500 PENDING clips, it waits for **500 v2 clips of any
kind**: with 600 decided clips older than the pending ones the old query returned **0 pending of 30,
0 of 500 and 0 of 2,000**, and the queue would have said "Nothing to review" while editors waited.

Proved on real rows, 20 of 20 checks:

| pending | old query showed | new: page one | true count | every row reachable |
|---|---|---|---|---|
| 30 | 0 of 30 | 248 ms | 30 | 30 of 30, 1 page |
| 500 | 0 of 500 | 235 ms | 500 | 500 of 500, 10 pages |
| 2,000 | 0 of 2,000 | 235 ms | 2,000 | 2,000 of 2,000, 40 pages |

Page one is flat and the **last** page costs the same (242 ms at skip 1,950). "Reachable" means the
pages were walked to the end and the ids compared against the full id set from raw SQL.

**The plan was read, not assumed.** Page one was a Seq Scan of the whole table plus a Sort every
load: fine at 0.977 ms, linear for ever. A composite index on `(status, createdAt)` made it an Index
Scan reading 50 rows instead of 2,601, **0.977 ms to 0.108 ms** (`bl896-v2-queue-index.sql`, applied;
rollback is one DROP INDEX).

## The sweep: this is the fifth instance, and two of them are on the poster's screen

I parsed every `findMany` in `src` rather than grepping, after a subagent enumeration returned three
claims that were false on reading the files. **509 list queries; 155 carry a literal cap with no way
past it.** The two that matter are new, and both are in v2:

* **The poster's campaign cards.** `totalClips`, `notPosted`, `posted` and `skipped` were counted by
  looping a `take: 2000` array **with no `orderBy` at all**: past 2,000 approved clips the numbers
  were wrong, wrong DOWNWARD, and not reproducible between two page loads. Now a `groupBy`, with the
  per-poster parts bounded by his own rows rather than by the platform.
* **The poster's catalogue pills.** All four counts were `loadedArray.filter(...).length` over a
  `take: 500`. His state is a real database filter now and each count is its own `count()`.

Re-verified the three earlier fixes myself: BL-836's status filter, BL-850's campaign picker (the
subagent said it was missing; it is not) and BL-833's pagination are all present. **BL-892's deferral
list is stale**: the dead "Continue" button it named was removed by BL-893.

**The guard.** `check:v2-lists-are-queries` runs in `prebuild`, 7 checks, each demonstrated failing
**alone** by reintroducing the defect it catches. It caught two things in my own work and one in
itself: a `[^)]*` that could not match the very line it forbids, the third guard in three rounds to
ship a check that could not fail. The 17 pre-existing v2 caps are allow-listed **by name, with a
reason and a measured bound**, so anything new fails the build.

## The URL, and the launch flag underneath it

**There was ONE flag for BOTH marketplaces**, so the single act that launches v2 to fifty people
would have opened the **first** marketplace to all 1,714 clippers in the same instant. That
marketplace holds **0 submissions, 0 creator earnings, 0 clip posts and 0 clips**; it has never
carried a cent. v2 now has its own flag: additive, so nobody loses access, and **both flags are
unset, so nothing changes until he sets one.** 21 of 21 checks, five personas, four flag states.

**The rename is still not done, and the reason got worse.** Re-measured: **449 occurrences of
`marketplace-v2` across 56 files in `scripts/`**, and they are the hardcoded route literals inside
the BL-890 to BL-893 containment proofs. A rename would leave those proofs asserting things about
paths that no longer exist, hours before fifty people arrive, rather than failing loudly. **So the
path moves without the directory moving.** `/marketplace` sends anybody who can see v2 to it, gated
on v2's own flag: one file, four lines, zero route literals touched, zero proofs invalidated.
Setting `NEXT_PUBLIC_MARKETPLACE_V2_ENABLED=true` opens v2 **and** points clippershq.com/marketplace
at it in one act. While it is on, the first marketplace has no URL: a real trade, and his to make.

## The accessibility review found a defect of mine

**A failed queue load said "Loading the queue." for ever.** Written this round, one branch below a
header about silent lies: `reload` returned without setting `clips` and the render tested
`clips === null` before `failed`, so the error branch was unreachable. No error, no retry, no
announcement. Fixed, and **proved in a real browser by aborting the request**: it now says the
request did not arrive, says plainly this is not an empty queue, moves focus to the error heading,
and recovers the true queue on "Try again". 5 of 5.

Also fixed: a doubled announcement, silence when a tab emptied, a tablist cycling under key repeat, a
skip that double-posted then said it failed, and a race that could label PENDING rows "Already decided".

## Proof

16 of 16 renders: both accounts, five widths each, against a production build with
`DEV_AUTH_BYPASS=false` and a real minted session cookie. Zero pan at every width, measured by
scrolling right. The tab read **120** while the page held **50 rows**, which is the whole point;
"Show more" moved it to 100 of 120 with the total unchanged. A stranger and a signed-out visitor saw
nothing on the same URLs.

**No arithmetic changed: twelve protected money files byte-identical by blob OID on both refs.**
Sandbox: 2,973 rows created under `bl896sbx-`, **0 remain**. The platform is back to 35 campaigns,
1,765 users and 0 v2 clips. One ordinary clip arrived at 11:11:54 from a real clipper; not mine, and
nothing here touched it. **No referral percentage was built.**

## What he must decide

1. Set `NEXT_PUBLIC_MARKETPLACE_V2_ENABLED=true` at launch, opening v2, pointing
   clippershq.com/marketplace at it, and leaving the first marketplace with no URL?
2. Rename the directory properly after launch, as a round of its own with the proofs re-pointed?
3. The 17 allow-listed v2 caps are each bounded by one person's own rows. Paginate them too?
4. The catalogue card knows each clip's approval date and hides it. Should it show it?
5. `--text-primary`, `--text-secondary` and `--text-muted` all render white, so the three-step
   hierarchy these screens imply is one flat tone. Platform-wide. Worth a round?
