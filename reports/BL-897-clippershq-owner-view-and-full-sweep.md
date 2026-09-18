# BL-897 — the owner's own view, and a budget gate that sees 45 percent of what it is guarding

**MODEL SPLIT.** The strongest model read every money path, wrote the overview loader, the four-figure
route, the budget proof and this report, with no subagent between it and the source. Cheap models did
two read-only retrievals. Claims are **VERIFIED** where I re-derived them myself and **READ** where
they are a subagent's and I did not. **Two subagent claims were false on reading the files** and both
are named below.

## The headline: the budget gate projects the poster's 45 percent and nothing else

**MEASURED, NOT REASONED ABOUT.** A $1,000 campaign, bonuses on, 90 posts of 20,000 views:

| | |
|---|---|
| per post | gross $20.00, maker $11.25 (25% bonus), poster $9.90 (10% bonus), platform $2.00 |
| posts created | **90 of 90** |
| money writes that landed | **48** |
| refused by the L1 hard lock | **42**, the first naming the campaign over budget |
| final legs | poster $475.20 + maker $432.00 + platform $96.00 |
| `getCampaignBudgetStatus().spent` | **$1,003.20 against a $1,000.00 budget** |

**IT WENT $3.20 OVER, and the mechanism is exact.** `clip-earnings-writer.ts:206` computes
`delta = rounded.earnings − current.earnings`. On a v2 clip `Clip.earnings` is **the poster's 45
percent only**, so `projected = spent + delta` prices a write at 45 percent of what it will actually
cost. The same write syncs the maker's leg and the platform's leg, and `balance.ts:585` counts all
three. **The aggregate sees three legs; the projection sees one.**

The second mechanism has the same blind spot, verified by grep: **`src/lib/proportional-cut.ts`
contains ZERO references to `marketplaceV2`, `v2Editor` or `v2Platform`**, and its pre-scan uses
`proposedClipper = breakdown.clipperEarnings`.

**THIS IS BL-877 HALF-FIXED.** That round made `spent` count all three legs and never widened what
the gate projects. **The overshoot is BOUNDED**, which is why it is a defect and not an emergency:
once committed spend reaches the budget the `isOverBudget` branch refuses everything, so the most a
campaign can exceed by is one write's other two legs.

**I DID NOT FIX IT, AND THAT IS A DECISION RATHER THAN AN OMISSION.** The fix is in
`clip-earnings-writer.ts`, the platform's number one guardrail, hours before launch. A wrong change
there is worse than a bounded 0.32 percent overshoot. **The one-line shape of the fix**: when
`marketplaceV2PostId` is set, the projected delta must add the maker and platform deltas the same
write will cause.

## What the owner could reach before this round: one link, in the wrong menu

**HE IS EXACTLY RIGHT THAT HE SEES ONLY THE OLD MARKETPLACE, AND IT IS A MISSING LINK.** VERIFIED by
reading `sidebar.tsx`:

* `marketplaceV2NavItem` (`:153`) is referenced at **exactly two places, `:218` and `:222`, both
  inside `buildClipperNav`**.
* For an OWNER, `:524` runs `sections = ownerNav;` and **discards that entirely**. `ownerNav` carries
  `marketplaceNavItem` at `:293`, whose href is `/marketplace`.
* The phone bar is the same story: `TABS_OWNER` has **no `/marketplace` tab at all**, and BL-891's
  repoint is guarded by `t.href !== "/marketplace"`, so it can never fire for him.
* The approval queue was linked from **one place in the whole product**, `V2Nav.tsx:105`, which
  renders only inside `marketplace-v2/layout.tsx` — he had to already be inside to find it.

**BL-891 IS THE ROUND THAT PUT THE MARKETPLACE IN THE LEFT NAVIGATION "WHERE THE OWNER ASKED FOR IT".**
It built that for clippers only, so the one person who asked is the one who never got it. His only
door was an account-menu entry reading "Make clips or post clips" — two earner roles, nothing about
reviewing. **A subagent reported the v2 item was in `ownerNav`. It is not; line 293 is the v1 item.**

Fixed first, before anything was built: three entries for him, gated on the same call every v2 page
makes — **Marketplace**, **Marketplace review**, and the old one kept and relabelled **Marketplace
(first version)**, which is BL-891's own rule for somebody who can reach both.

## What was built

**ONE OVERVIEW, NOT FIVE**, at `/marketplace-v2/admin/overview`, OWNER only. Per clip: who made it,
its state, when, how many posters took it, and its three legs. Per post: who posted it, **the live
link**, views and earnings. Per campaign: clips live, posts, spent and left. Gross and cash carried
separately on every field. **It links to BL-896's approval queue and reimplements nothing.**

**IT COMPUTES NO MONEY.** Every figure is read from the row its writer put there or from a named
function: the maker's leg through `loadV2EditorEarnings`, the poster's from `Clip.earnings`, the
platform's from `MarketplaceV2PlatformEarning`, spend from `getCampaignBudgetStatus`, cash from
`projectPayoutCash`. No fourteenth derivation.

**A MARKETPLACE CLIP IS UNMISTAKABLE IN HIS CLIPS LIST**: the badge fires for a v2 clip (which carries
`isMarketplaceClip` FALSE on purpose), both people are named, and his two slices are broken out
**separately** — ordinary cut and the extra 10 percent — because they come from different tables and
mean different things. On the real campaign `Zhus Edit (0.50 CPM)` at a 39.0021 percent owner share,
read back from `computeV2CampaignCostPer100`: maker $45.00 gross / $40.95 cash, poster the same,
platform leg **$10.00**, ordinary cut **$39.00**, fees $8.10, **ADDS owner nets $57.10** while the
campaign spends $139.00, against $18.10 under REPLACES. *(The round attributed these to BL-884; they
are in BL-878, BL-880 and BL-881. The figures are right, the citation was not.)*

**THE FOUR FIGURES LIVE ON ONE ROUTE**, OWNER only, proven against the live body: the maker, the
poster and an ordinary clipper each get **403**, and all six field names are absent.

**THE MAKER NOW SEES WHERE HIS CLIP WENT**: every post, who posted it, the link, that post's views and
**what that post earned HIM**. The poster's earnings are absent by construction — there is no field
that could be subtracted to recover them.

## What the guards caught, including my own

* **BL-882's S3 refused my first overview and my first route**, both for querying the editor earnings
  table directly. It was right: the owner reading a maker's leg that disagrees with the maker's own
  balance page is the failure that guard exists to prevent. Both now go through `loadV2EditorEarnings`.
* **BL-896's own list guard refused my overview** for a `take: 1000` where a grouped sum belonged.
* **My budget proof hardcoded `true` for the bonus-ceiling check and ran with every bonus at zero.**
  The legs came back exactly 45/45/10, which is what exposed it. The check now reads the percentages
  back off the breakdown: maker 25, poster 10.
* **I read `Clip.views`, which is not a column** — views live on `ClipStat`. The build could not catch
  it (untyped client); the render prep did, at runtime, in two files.
* **My render reported five false failures** on a page that was rendering perfectly: `innerText`
  applies CSS `text-transform`, so uppercase headings never matched. The screenshot settled it.
* **The accessibility review found eight real defects in this round's code**, including two `<dd>`
  elements under one `<dt>` asserting "maker gross = cash $40.95" — a figure beside a label that did
  not produce it, which is the rule this round was built on. Also fixed: a missing `role="list"` that
  made an iPhone report the nested lists inside-out, links to `/admin/users/` with no id, a live
  region re-reading five numbers and a microsecond timestamp on every page, and "Show more" dropping
  focus to the body.

## Proof, and what is not proved

**18 of 18 renders**: both accounts at 320, 375, 414, 1280 and 1440, production build,
`DEV_AUTH_BYPASS=false`, real minted cookies. **Zero pan at every width**, measured by scrolling.
Containment held for a stranger and a signed-out visitor on both owner URLs.

**Twelve protected money files byte-identical by blob OID**, including `clip-earnings-writer.ts`,
`balance.ts`, `tracking.ts`, `earnings-calc.ts` and `proportional-cut.ts`. **One money file changed**:
`marketplace-v2-editor-balance.ts`, twenty additive lines adding a `clipIds` scope option and one
`if` — no arithmetic, and every existing caller omits it. That is the documented path this file's own
header records for exactly this situation.

**Invariants across the full population: 10,181 clips, 0 violations, 0 negatives, 0 clips carrying
both marketplace flags.** Sandbox: 424 rows under `bl897sbx-`, **0 remain, nothing unremovable**. The
platform is back to 35 campaigns and 0 v2 clips, and **the test campaign `cmu5yeax20000h4w7yv5n387y`
is untouched**.

**NOT PROVED, AND NAMED RATHER THAN IMPLIED.** The full people-shaped sweep of PART 5 and its second
cycle were not run: the round's budget went into finding and characterising the gate defect above.
What that leaves unproven is the combination matrix — trainer cuts, express, devaluation, retire and
revive, conversion and undo — each of which BL-894 and BL-885 proved separately and none of which
this round changed. **The maker's per-post list is built and rendered but not photographed with
data**, because `buildV2EditorDashboard` excludes test campaigns by design and the only alternative
was a non-test campaign touching real money.

## What he must decide

1. The budget gate prices a v2 write at 45 percent of its cost, so a campaign can end up to one
   clip's other two legs over its cap. Fix it in the chokepoint now, or after launch?
2. Money written at post time sits on a PENDING clip and does not count toward spend until the clip
   is approved. Intended?
3. `recomputeV2PostEarnings` nulls the bonus config, so a conversion writes legs with no bonus until
   the next tick rewrites them. Harmless because the tick recomputes from total views. Leave it?
4. While `NEXT_PUBLIC_MARKETPLACE_V2_ENABLED` is true the first marketplace has no URL. Still right?

**ONE LINE VERDICT:** nothing stands between him and opening it except the budget gate's 45 percent
projection, which is bounded and his to weigh; the variable is
`NEXT_PUBLIC_MARKETPLACE_V2_ENABLED=true`.
