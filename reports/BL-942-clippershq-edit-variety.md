# BL-942: stopping one clip being posted by too many accounts, with genuinely different edits (ClippersHQ)

**AUDIT ONLY.** Nothing changed: no code, schema, data or config. • Every query ran in a READ ONLY transaction on ONE connection, closed after each run; no two runs overlapped. The helper subagent opened none. • No paid vendor call and no Apify actor. • Worktree C:/b942 at main `91f36137`, removed and verified after. • Timestamps read as ::text against DB now() 2026-10-09 19:03:50 UTC. Handles are redacted to hash prefixes.

**What this report does NOT design.** It designs no way to alter a video or its file so that one edit looks like several to a platform. BL-871 established that the platforms re-encode every upload ("not one byte survives") and match duplicates perceptually, so file or metadata tricks would not work. It would also deceive the platforms. The only fix designed here is genuine variety: the team makes several truly different edits of one moment, and the site spreads posters across them.

## 1. How many posters take one clip today
**Clips.** 42 real v2 clips: 31 APPROVED, 4 PENDING, 7 REJECTED. All are on one campaign, ANGIE BROWN.
**Posts.** 105 posts. 4 of them are owner clips converted on 2026-10-07 and have no account, so 101 are real posts, on 27 clips, by 10 posters, all on Instagram.

| Posts on one approved clip | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Clips | 7 | 4 | 8 | 3 | 3 | 4 | 1 | 1 |

• The largest is 8 posts on one clip (723241cd), on 8 distinct accounts, over 12 days. • The busiest 24 hours on one clip had 5 posts. The mean is 3.39 posts per approved clip. • Every post of a clip is on a different account, and no poster has posted the same clip from two accounts (0 pairs). • **The concern is live now:** 6 clips already carry 6 to 8 posts of the same video. The platforms publish no threshold, so nobody can say where limiting starts.

**A weak signal, not proof.** By post order, approved posts have these median views:

| Post on its clip | 1st | 2nd | 3rd | 4th | 5th and later |
|---|---|---|---|---|---|
| Posts | 25 | 21 | 18 | 11 | 14 |
| Median views | 534 | 158 | 24 | 23 | 26 |

This is confounded by account size and by when the post was made: • In the week of 2026-09-14, first and later posts were equal (485 and 500). • In the week of 2026-09-21, first posts had a median of 189 and later posts 43. • Of 7 posters with both kinds of post, 5 got fewer views when they were not the first to post a clip, and 2 got more.

The direction matches the owner's worry. The sample cannot separate the cause.

**Why the posts pile up.** The catalogue lists clips newest first (`orderBy: { approvedAt: "desc" }` in `src/lib/marketplace-v2-poster.ts`). The 6 clips approved together on 2026-09-23 took 4 to 7 posts each within days.

## 2. Variant groups, designed
**The model.** A group is several genuinely different edits of ONE moment, for example a different cut, crop, opening, length, text or music bed, made by the team. Each edit stays its own `MarketplaceV2Clip`, approved on arrival through `approveV2Clip`, so the thumbnail and frame pipeline runs for each edit. A clip outside any group behaves as a group of one, so nothing changes for it.

**Schema.** These need owner-run SQL; never prisma migrate. • New table `marketplace_v2_clip_groups`: id, campaignId, label, createdById, capPerEdit (nullable), createdAt. • New nullable column `groupId` on `marketplace_v2_clips`, with an index on (groupId, status). • New column `v2PostCapPerEdit` (Int, nullable) on `campaigns`. The owner sets it; the group's capPerEdit overrides it; null means no cap. • New nullable column `reservedUntil` on `marketplace_v2_poster_states`, the per-poster row that already exists.

**Sending one group.** • *Send several clips:* a tick, "These are different edits of the same moment", files every line of that send into one new group. • *Single send:* gains "Add as another edit of" with a picker of the campaign's groups. • *Upload token:* the JSON body takes an optional `groupKey`, the tool's own name for the moment. The same campaign plus the same key always lands in the same group, which is created on first use. No other field changes.

**What a poster sees.** One card per moment, exactly like today. • The edit offered is the one in the group with the FEWEST posts that is under its cap. Ties go to the oldest approval. • The choice is fixed for that poster when he first opens the card, so the card never changes under him. • Opening "Post this" reserves one slot on that edit for 2 hours (`reservedUntil`). The cap counts posts plus live reservations. • Posting again from another connected account (BL-941) offers him a DIFFERENT edit of the group, chosen the same way.

**When every edit is at its cap.** • The moment leaves the "to post" list for posters who have not reserved it. • Its page says plainly: "This moment is full. Every edit of it has been posted as many times as the owner allows. Pick another clip." • A poster holding a live reservation can always submit. This is what protects a poster who has already posted on the platform. • The owner's overview shows each group's fill, so he knows to add an edit.

**How the existing rules interact.** • **One post per clip per account:** unchanged; the unique key on (v2ClipId, clipAccountId) stays. Proposed addition: one post per GROUP per account, because an account posting two edits of one moment is itself repetitive. • **30 minute window:** unchanged, measured per post from when the post goes live. • **Max per clip:** unchanged. Each post is its own Clip, capped on its base exactly as now. • **Budget:** unchanged. Each post goes through the same L1 lock; a group carries no money. • **BL-940/941 full rate:** unchanged. Every edit is team made, so it pays its poster in full.

**No parallel writer.** The cap is enforced inside `createV2Post`'s existing transaction. The current `postCount: { increment: 1 }` update becomes a conditional `updateMany` with `postCount < cap` (or a live reservation), and a 0-row result refuses with a 409. There is no new post path and no new money path.

**Files that would change.** • Schema and SQL: `prisma/schema.prisma`. • Library: `src/lib/marketplace-submit.ts`, `src/lib/marketplace-v2-poster.ts` (`listCatalogueForPoster`, `listCampaignsForPoster`, `getCatalogueClipForPoster`, `createV2Post`), `src/lib/marketplace-v2-copy.ts`, `src/lib/marketplace-v2-owner-overview.ts`. • Routes: `src/app/api/marketplace-v2/upload/route.ts`, `src/app/api/marketplace-v2/clips/route.ts`, `src/app/api/marketplace-v2/catalogue/[id]/post/route.ts`, `src/app/api/marketplace-v2/catalogue/[id]/state/route.ts`, `src/app/api/campaigns/[id]/route.ts`. • Screens: `src/components/marketplace-v2/EditorSendManyModal.tsx`, `src/components/admin/OwnerMarketplaceSubmit.tsx`, `src/components/marketplace-v2/CatalogueCard.tsx`, `src/app/(app)/marketplace-v2/catalogue/catalogue-client.tsx`, `src/app/(app)/marketplace-v2/catalogue/[id]/detail-client.tsx`, `src/app/(app)/marketplace-v2/admin/setup/setup-client.tsx`, `src/app/(app)/admin/campaigns/page.tsx`. • Guards: `scripts/check-v2-lists-are-queries.js` (the group query), plus one new guard that the cap lives only in `createV2Post`.

## 3. Hosting the files on the site instead of Drive
**What Drive costs today.** It costs the platform no money. It costs fragility and friction: • BL-918: 27 of 27 browser previews failed, because of the site's own CSP, no CORS on Drive, a virus-scan page on 13 of 26 files over about 25 MB, and 4 files not shared. This was fixed by fetching Google's thumbnail on the server. • Today: 31 of 35 approved or pending clips have a Drive picture. • 4 have no file id; all are converted owner clips, not Drive. • 2 rejected clips were never shared. • Rejections: 1 of 7 was "cannot open this link". 1 folder link was refused (BL-908). • The frame pipeline depends on an undocumented Drive download URL (`confirm=t`, BL-919). Google answered a bogus id three different ways in one day.

**Real sizes.** The frame pipeline measured all 27 approved clips (`frameVideoBytes`): • 5.9 MB to 307.9 MB; median 97.0 MB, mean 114.9 MB; 3,103 MB in all. • 19.5 s to 35.3 s long, at 2.5 to 92.7 Mbps. This matches BL-919's 23.6 to 322.9 MB, which was 2,715 MB for 16 clips.

**Projection.** 42 clips were uploaded in the last 30 days, and posts per clip are 3.39.

| Per month | Today's rate | Ten times |
|---|---|---|
| New storage | 4.8 GB | 48 GB |
| Download egress | 16 GB | 164 GB |
| Storage and egress with a 100 MB cap | 2.1 GB, 7 GB | 21 GB, 71 GB |

The 100 MB cap row assumes clips above the cap are re-exported to about 60 MB. That brings the mean to 50 MB, a 57 percent cut. Previews already use the stored JPEG frames, so only the poster's download moves video.

**Against the plan.** BL-930 could not read the Supabase plan. The owner reads it at supabase.com, then the project, then Settings, then Billing and Usage; the per-file upload limit is under Storage settings. The bucket holds 487 MB today (BL-930).

Supabase's PUBLIC list prices, which I did not read from the account: • *Free:* 1 GB storage, 5 GB egress, 50 MB per file. 17 of 27 measured clips are over 50 MB, so on Free on-site hosting is NOT possible. • *Pro:* $25 a month, 100 GB storage and 250 GB egress included, then about $0.021 per GB-month and $0.09 per GB. • At today's rate it fits inside the allowance with no retention for about 20 months. • At ten times, with no retention, it passes 100 GB in month 3. After a year it would be about 580 GB, roughly $10 a month extra.

**Size limit and retention.** • A 100 MB per-file limit roughly halves both storage and egress, and loses nothing: the platforms re-encode every upload anyway. • A retention of 30 days after approval holds storage flat at one month of uploads: 4.8 GB, or 48 GB at ten times. That is safe because posts are tracked by their URL, not the file.

**Recommendation: keep Drive now.** Variant groups need nothing from on-site hosting, since each edit is its own Drive link. Add on-site hosting, with a 100 MB limit and 30-day retention, only once the owner confirms the plan is Pro. On Pro it is affordable at today's rate and at ten times.

## 4. What else protects the posters' accounts, legitimately
**Catalogue order: fewest posts first.** Measured effect: 105 posts on 31 clips can be spread at no more than 4 per clip, where today one clip has 8 and 6 clips have 6 or more. No schema and no owner input are needed. Do it first.

**Cap per edit.** Posts over the cap would have gone to another edit: • Cap 3: 30 of 105 (29 percent), needing 45 edits for 31 moments, 14 more than today. • Cap 4: 18 posts (17 percent). • Cap 5: 9 posts (9 percent), needing 37 edits.

**Own captions.** Posts store no caption today, so the effect cannot be measured. The platforms match the video, not the caption, so a caption alone does not stop limiting. A line on the post screen, "write your own caption; do not copy another poster's", costs nothing and adds genuine variety.

**More clips per campaign.** 10 posters on 31 clips today. Each extra edit of a busy moment lowers the per-edit count directly. This is owner work, so it is the lever the cap makes visible.

**Order:** catalogue order, then caption line, then variant groups with the cap, then on-site hosting if wanted.

## 5. The plan, ranked

| Round | What | Owner input | Size and cost |
|---|---|---|---|
| 1 | Catalogue shows fewest-posted clips first (newest breaks ties); post screen asks for an own caption | None | 1 small round, no schema |
| 2 | Variant groups: schema, send form tick, token `groupKey`, one-edit-per-group catalogue, reservations, the cap in `createV2Post` | Run the printed SQL; choose the cap | 2 rounds: data and posting, then screens and token |
| 3 | 100 MB size guidance on Drive sends, warned from `frameVideoBytes` at approval | None | 1 small round |
| 4 | On-site hosting, if wanted | Confirm the Supabase plan and the allowance | 2 rounds: upload route with magic byte and size checks, retention sweep. About $0 extra on Pro at today's rate |

**One line:** Cap each edit at 3 posts, adjustable per campaign. On-site hosting is affordable only on Supabase Pro, inside its allowance at today's rate and about $10 a month extra at ten times with no retention; it is not possible on Free, where 17 of 27 clips exceed the 50 MB file limit. The first round to run is catalogue order, fewest posts first.
