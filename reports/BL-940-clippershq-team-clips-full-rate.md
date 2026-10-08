Unremovable rows: none. Every sandbox id was recorded and only those were deleted; 684 text columns searched afterwards, 0 values still carry `bl940sbx-`.

# BL-940: a clip the team made pays its poster exactly like an ordinary clip

**In one line:** on ANGIE BROWN a poster of a team clip now earns **$0.20 per 1,000 views on Instagram** (the full clipper rate, was $0.09); ANGIE BROWN takes **Instagram only and has no TikTok rate**, so there is no TikTok figure (see finding BL-940d). Of the existing legs, the 14 team posts that held money moved: every poster leg **rose** ($29.20 to $64.94), the owner's own maker legs (**$29.17**) and the platform legs (**$6.37**) **closed to $0.00, each with a recorded reason**; no editor leg existed; the 73 posts on former clipper makers' clips and every payout are **unchanged**.

Merged to main at `f59080c9` (branch `checkpoint/BL-940`, tip `5a35ba8d`). Tags `pre-BL-940`, `post-BL-940`, `pre-merge-BL-940`, `post-merge-BL-940`. Both pushes verified by safe-push (origin equals local). Production's cron ran the new build at 18:52:02 UTC before any real row was moved. Clips are named by the first 8 characters of an md5 of their id; no handle and no key appears here.

**Rollback:** `git reset --hard pre-merge-BL-940` with a verified push, THEN run `BL-940-ROLLBACK.sql` (committed at the repo root): 55 UPDATEs and one DELETE inside one transaction, written from the snapshot at 18:41:02 UTC before any real row changed. Code first, or the next tick reapplies the rule.

## Part 0: how the round ran

• Clean worktree `C:/b940` on a fresh `checkpoint/BL-940` from main `ece55cc2` (BL-939 included). No other session held the branch or a worktree; the main tree had 0 modified tracked files.
• No paid vendor call and no Apify actor: every vendor, email, storage and Discord key was deleted from every process I ran, `fetch` was stubbed to refuse and count in the proof (0 calls), and the render server ran with all of them blank.
• **Connections, measured, not assumed.** Every process ran with a preload that caps each Postgres pool and records the peak open at once. Every read only script: **peak 1**. The real transition: **peak 2**. The proof that drives the real tracking tick: **peak 8** (two pools of four). I could not hold the tick to one: its budget lock (BL-901) reads committed spend on a second connection while the tick's own transaction holds the first, so a cap of one deadlocked it (run 1) and two per pool timed out behind 78 ms round trips (runs 2 to 4). Disclosed rather than hidden; one process at a time throughout.
• Timestamps are the database's own `now()`. Sandbox prefix `bl940sbx-`; every tracking job parked after every step that could make one (11 of 11 parked at the end).

## Part 1: measured before anything changed (DB now 2026-10-08 16:33 UTC)

| | Team made (owner) | Former clipper made |
| --- | --- | --- |
| Catalogue clips | 9 (one maker, the OWNER) | 33 (7 makers, all CLIPPER) |
| Posts | 32 | 73 |
| Approved, live | 28 | 48 |
| Poster legs | $29.20 | $2.78 |
| Maker legs | $29.17 (all the owner's) | $2.69 |
| Platform legs | $6.37 | $0.61 |
| Owner cut (AgencyEarning) | $5.07 | $2.97 |

• **EDITOR grants:** 0 grant or removal events ever, 0 people hold the grant. So no editor money exists to protect today; the code protects it anyway (Part 3).
• **Paid floors:** 0 payout rows for any maker or poster of a v2 clip on any campaign that holds one. No floor bound anywhere.
• The 45 percent was computed in **two families and written in a third**, counted with `grep -c` over `src` on main:
  ◦ the arithmetic: `MARKETPLACE_V2_POSTER_SHARE` 12 lines in 4 files, `MARKETPLACE_V2_EDITOR_SHARE` 10 in 4, `calculateMarketplaceV2Earnings(` 5 in 4 (the calculator, the tick's v2 fork, the post, the recompute, the conversion), and the poster rate helpers `posterRateUnrounded`, `posterRatePer1k`, `posterRatePer100k` (3, 4, 4 lines in one file, all at a flat 45 percent);
  ◦ **the second family, a hidden copy:** the chokepoint's budget lock carried its OWN six line copy of the sync's 45/45 arithmetic (`clip-earnings-writer.ts`), checked only to match. A rule change made in one place would have priced the other;
  ◦ **the words:** 32 non comment lines on main name 45 percent or 45%; 13 of them are sentences a person reads (catalogue, campaign notice, submit refusal, three strike notices, two editor lines, the send dialog line, the approval notice, the conversion refusal, the maker card line, the retired maker line), plus the owner's clip review labels and the overview's four figures.

## Part 2: the rule, at one point

`src/lib/marketplace-v2-split.ts` is the only place it is written:

• `v2SplitForMaker`: TEAM when the maker was an OWNER, or held the EDITOR grant at the time the clip was made (the latest MKT2_EDITOR_GRANTED or MKT2_EDITOR_REMOVED row at or before the clip's `createdAt`; the grant writer records both in its own transaction). Anything the record cannot prove is SHARED, because calling a former clipper's clip TEAM would close his money and the reverse takes nothing from anybody.
• `deriveV2LegTargets`: the legs a write leaves. SHARED is BL-881's six lines unchanged; TEAM closes the owner's maker leg, holds an editor's, and has no platform leg. **Called by both the chokepoint's sync and its budget lock**, so the gate prices exactly the write the sync makes. The copy is gone.
• `V2_TEAM_MADE_SQL`: the same rule for the reconciliation, kept beside it.
• Decisions are remembered per process (a clip's split never changes once made), so the reads happen before the tick's Serializable transaction opens and none inside it.

**How every writer reaches it.** The tick sends a team clip down the **ordinary branch**: `newEarnings` stays `breakdown.clipperEarnings` and the owner cut stays the ordinary cut, computed by the calls every ordinary clip is paid by, then written through `writeClipEarnings`, whose v2 sync settles the other two legs. The recompute, the post route and the conversion name the split; `calculateMarketplaceV2Earnings` with TEAM calls `calculateClipperEarnings` itself. **The v2 writer asks the rule of the record and refuses a breakdown on the other split**, so a caller that forgot cannot pay a team poster 45 percent or close a former maker's leg. No parallel writer was built.

**Equal to an ordinary clip, to the cent:**
• Arithmetic: **67,584 of 67,584** combinations identical in base, bonus percent, bonus and total (22 view counts including 13, 1,025 and 594,565; 8 rates including $0.0985 and $0.333; 64 bonus profiles; three caps; two minimums). Worst difference $0.00. SHARED identical to the calculator before BL-940 on all 67,584, and the leg targets identical to the old six lines on 384 of 384.
• The real tick (production code, fetch stubbed): a team post and an ordinary clip, same poster, same stamped $0.20, same views: **6,173 views $1.32 and $1.32, owner cut $0.65 and $0.65; 41,113 views $8.80 and $8.80, $4.33 and $4.33; 594,565 views $127.23 and $127.23, $62.66 and $62.66.** No maker row and no platform row was created for the team post.

## Part 3: the existing posts, without taking anybody's money

Rule for each leg on a team clip: the poster rises to the full rate; **the owner's maker leg closes through the same paid floor every maker leg has** (any part already paid is held); **an editor's maker leg is held at exactly its value and never written**; the platform leg closes. Every closure writes an MKT2_TEAM_LEG_CLOSED audit row in the same transaction, with before, after and the reason.

Snapshot of every affected row and the exact rollback were written at 18:41:02 UTC, before the merge; the transition ran at 18:53 UTC on the live build, one Serializable transaction per post through `recomputeV2PostEarnings` at each post's newest ClipStat views:

| Clip | Views | Poster | Owner's maker leg | Platform leg | Closures |
| --- | --- | --- | --- | --- | --- |
| 24cdb475 | 5,121 | $0.48 to $1.04 | $0.47 to $0.00 | $0.10 to $0.00 | 2 |
| 73e85d36 | 5,203 | $0.48 to $1.06 | $0.48 to $0.00 | $0.10 to $0.00 | 2 |
| a977a9ef | 4,127 | $0.38 to $0.85 | $0.38 to $0.00 | $0.09 to $0.00 | 2 |
| 087ef4f1 | 4,214 | $0.39 to $0.86 | $0.39 to $0.00 | $0.08 to $0.00 | 2 |
| e13048fc | 5,486 | $0.50 to $1.12 | $0.50 to $0.00 | $0.12 to $0.00 | 2 |
| dde8317c | 994 | $0.09 to $0.20 | $0.09 to $0.00 | $0.02 to $0.00 | 2 |
| eaf3a02d | 2,321 | $0.23 to $0.50 | $0.21 to $0.00 | $0.04 to $0.00 | 2 |
| be1cdb92 | 1,032 | $0.09 to $0.22 | $0.09 to $0.00 | $0.03 to $0.00 | 2 |
| 3f1c1da4 | 1,442 | $0.13 to $0.30 | $0.13 to $0.00 | $0.03 to $0.00 | 2 |
| f4e82a20 | 1,501 | $0.14 to $0.31 | $0.14 to $0.00 | $0.02 to $0.00 | 2 |
| 085936c5 | 7,600 | $0.69 to $1.55 | $0.69 to $0.00 | $0.16 to $0.00 | 2 |
| 72162f46 | 8,148 | $0.74 to $1.66 | $0.74 to $0.00 | $0.17 to $0.00 | 2 |
| 5816ffea | 7,592 | $0.32 to $0.69 | $0.32 to $0.00 | $0.06 to $0.00 | 2 |
| 0ac1b22b (pending) | 594,565 | $24.54 to $54.58 | $24.54 to $0.00 | $5.35 to $0.00 | 2 |
| **14 posts** | | **$29.20 to $64.94** | **$29.17 to $0.00** | **$6.37 to $0.00** | **28** |

• Read back: **14 of 14 equal the plan to the cent**, every poster leg sums to base plus bonus, 28 closures recorded.
• The other 18 team posts held $0.00 in every leg (views under the 500 minimum, or the video is gone) and were not touched.
• **No one's money fell:** every poster leg rose or stayed; there was no editor leg; the only money that closed is the owner's own maker leg and the platform leg, which nobody is paid; the payout fingerprint over all 255 payout rows is identical before and after.
• The owner's cut on these posts is written by the tick; it moves to the ordinary cut on each post's next check (the sandbox showed it equal to an ordinary clip's).
• ANGIE BROWN's recorded spend: **$23.31 before, $23.36 after**, of $2,700.

## Part 4: every screen tells the truth

A poster's rate is now taken at **each clip's split**, from the unrounded source: `posterRateUnrounded(campaign, split)` is `gross x v2PosterShareFor(split)` (1 on a team clip, 0.45 on a former clipper's), and the 100,000 figure is one multiplication of that. At $0.19 the 45 percent shows $8.55, never 100 x $0.09; at $0.0985 a team clip shows $9.85 and a former clip $4.43.

| Where | Before | After |
| --- | --- | --- |
| Catalogue, under the heading | "You earn 45 percent of what your post makes." | "Each clip shows what you earn on it." |
| Clip cards and the clip's page, team clip, ANGIE BROWN's terms | "$9.00 per 100,000 views" | "$20.00 per 100,000 views" (a former clipper's clip still "$9.00") |
| Campaign card, campaign holding both kinds | "You earn about $9.00 per 100,000 views" | "You earn about $9.00 to $20.00 per 100,000 views" (team only: "$20.00") |
| Campaign page notice, marketplace only | "...paste the link there. You earn 45 percent of what your post makes." | "...paste the link there. Each clip in the marketplace shows what you earn on it." |
| Campaign page notice, two ways | "You earn 45 percent and the editor earns 45 percent." | "Each clip in the marketplace shows what you earn on it." |
| Refusal when uploading to a marketplace only campaign | "...You earn 45 percent of what your post makes." | "...Each clip in the marketplace shows what you earn on it." |
| First strike notice | "...so the editor gets paid too, and you still earn 45 percent for posting it." | "...so it is paid the right way. Each clip there shows what you earn for posting it." |
| Second and later strike notices | "Marketplace clips belong to the editor who made them, and you still earn 45 percent when you post them through the marketplace." | "Marketplace clips belong to the person who made them, and you are paid for posting them through the marketplace, where each clip shows what you earn." |
| Owner's send page | "...You earn 45 percent of every post of your own clips." | "...Posters of team clips earn the full clipper rate." |
| Editor's send page | "...any poster can post it. You earn 45 percent of every post." | "...any poster can post it and earn the full clipper rate." |
| Send dialog | "You earn 45% of what every post of your clip makes, for as long as the campaign runs." | "Posters of your clip earn the full clipper rate. Team clips have no maker share." |
| Maker's approved card, team clip | "Posters can post it now. You earn 45 percent of every post." | "Posters can post it now and earn the full clipper rate. Team clips have no maker share." (former clipper's clip unchanged) |
| Approval notice, team clip | "...and you earn 45 percent of every post." | "...and earn the full clipper rate on it." (former clipper's clip unchanged) |
| Conversion refusal | "...converting it would pay him 45 percent twice and take 10 percent off him." | "...they cannot also be named as the person who made it." |
| Owner clip review, team post | "Maker, 45 percent, gross", "Poster, 45 percent, gross", "only because it went through the marketplace" | "Maker, gross" (or "Maker, held from before, gross" for an editor's held leg), "Poster, full rate, gross", "none on a team clip" |
| Owner overview, team clip | "cash $X after 9 percent", "the extra 10 percent", "All three legs, gross" | "no maker share on a team clip", "none on a team clip", "All legs, gross" |

Kept on purpose: "Your clips stay up, keep earning you 45 percent of every post" (former makers; still true). After the change, 0 poster screens name 45 percent (guard S8).

**Rendered** on a local production build as real minted sessions (the sandbox poster and the sandbox owner), at 320, 375, 414, 1280 and 1440: 8 screens, 40 shots, **180 of 180 checks**, `innerWidth` read back equal to the width on every shot, **0 px of pan on every shot**, and the URL read back on each (`/market/campaigns`, `/market/campaigns/<campaign>`, `/market/catalogue/<clip>`, `/campaigns/<campaign>`, `/market/admin/overview`, `/market/editor` with the Approved tab and with the send dialog open, `/admin/clips`). The range card at 320 reads "You earn about $9.00 to $20.00 per 100,000 views" on two lines. An accessibility review of the changed markup found one real defect (a Maker label saying "no share" beside an editor's held figure) and one repetition; both fixed before the final build.

## Part 5: proof and merge

**Sandbox proof, 52 of 52** (`scripts/sandbox/bl940-prove.ts`), opening snapshot first, 15 people one per path:
• the rule: owner made TEAM, editor made TEAM, former clipper SHARED, granted AFTER his clip SHARED, grant removed after the clip still TEAM, unknown SHARED;
• an existing owner made post written 45/45/10, ticked: poster $0.48 to $1.07 (the ordinary calculator's figure), maker $0.46 and platform $0.10 to $0.00, both recorded, owner cut $0.51 to $0.53 = the ordinary cut; the next tick changes nothing;
• an editor made post: his leg **$0.73 held to the cent through two ticks** with its row's `updatedAt` unchanged; poster $0.77 to $12.86 (ordinary $12.86); only the platform closure recorded; owner cut $6.33 = the ordinary cut on $12.86;
• a former clipper's post: poster, maker and platform exactly the 45/45/10 calculator ($5.23, $4.89, $1.08 on a $10.86 gross);
• **paid floors, each earner's own:** the owner PAID $3.70 on his maker leg: held at $3.70 while the platform still closed; a PAID poster ($5.23) held by his floor on a recompute at fewer views while the unpaid maker fell $4.89 to $1.80;
• **the budget cap:** a team post worth $4.20 to its poster alone on a $1.37 campaign settled at exactly $1.37; a campaign set exactly at its spend took the transition and stayed at $12.55, the poster rising $3.89 to $8.41 and never falling;
• the conversion: preview TEAM, poster keeps $5.90, maker $0.00, platform $0.00, extra cost $0.00; write equals preview equals the next tick;
• refusals, each its own clip and person, none a 429: the poster named as maker refused 400 in the new words; a 45/45/10 breakdown for a team clip and a team breakdown for a former clipper's clip both refused with SPLIT MISMATCH and nothing moved;
• screens: catalogue $20 on team clips and $9 on former ones, the clip page the same, the campaign card "about $9.00 to $20.00"; the owner overview shows a team clip's real legs; the owner cut monitor finds 0 drift; both reconciliation forms explain every sandbox row.

**Invariants across the full population**, before (18:39 UTC) and after (18:54 UTC), 0 violations each time: no sandbox row counted; ANGIE BROWN under $2,700; both declared uniques present in `pg_indexes`; BL-627 no campaign over budget (23 budgeted); BL-696 no double leg in four tables; earnings equal base plus bonus on all 10,347 live clips and all 105 maker legs, none negative; BL-824 no maker leg negative; the owner's test campaign unchanged. After only: all 255 payout rows identical; 32 of 32 team posts as the rule requires; 73 of 73 former clipper posts byte identical; every former maker holds every leg and cent ($0.28, $0.87, $0.32, $0.14 and the rest unchanged).

**Both reconciliation forms**, leaks only and every row with its verdict:

| When | Definition | Leaks only | Every row |
| --- | --- | --- | --- |
| Before | main's | 0 | 0 |
| Before | BL-940's | 14 | 14: the same 14 posts, each "team clip still carries a platform leg", the pending transition |
| After | BL-940's | 0 | 0 |

**The protected money files.** By blob OID, main to branch: `earnings-calc.ts` 0041063, `balance.ts` 67c30c8, `clip-earnings-invariant-middleware.ts` 61cef39 and `money-decimal.ts` ef5cdae **byte identical**. Two changed deliberately, every line below:

`src/lib/clip-earnings-writer.ts` (18 added, 13 removed), inside the v2 budget pricing only. Removed:

```ts
          const {
            MARKETPLACE_V2_POSTER_SHARE,
            MARKETPLACE_V2_EDITOR_SHARE,
          } = await import("@/lib/marketplace-v2-earnings");

          const grossAfter =
            MARKETPLACE_V2_POSTER_SHARE > 0 ? r2(posterBaseAfter / MARKETPLACE_V2_POSTER_SHARE) : 0;
          const editorBaseTarget = r2(grossAfter * MARKETPLACE_V2_EDITOR_SHARE);
          const editorBonusTarget = r2((editorBaseTarget * editorBonusPct) / 100);
          const editorTarget = r2(editorBaseTarget + editorBonusTarget);
          const totalGross = r2(grossAfter + (posterAfter - posterBaseAfter) + editorBonusTarget);
          const platformTarget = Math.max(0, r2(totalGross - posterAfter - editorTarget));
```

Added (plus an eight line comment saying why):

```ts
          const { resolveV2SplitByPostId, deriveV2LegTargets } = await import("@/lib/marketplace-v2-split");
          const v2Decision = await resolveV2SplitByPostId(tx, (current as any).marketplaceV2PostId as string);
          const { editorTarget, platformTarget } = deriveV2LegTargets({
            decision: v2Decision,
            posterAfter,
            posterBaseAfter,
            editorBonusPct,
            editorBefore,
          });
```

Justification: the removed lines were a copy of the sync's arithmetic. A team clip pays no maker or platform leg, and a copy that did not know it would price the closed legs as growing and refuse writes that fit. The replacement is the sync's own function (384 of 384 identical to the removed lines on SHARED clips), so the lock and the write cannot disagree. Nothing else in the chokepoint moved: the invariant, the L1 lock, the row lock and BL-901's floor pricing below are byte for byte as they were.

`src/lib/tracking.ts` (43 added, 2 removed): a `let v2SplitDecision` beside `v2Breakdown`; at the v2 fork, `if ((clip as any).marketplaceV2PostId) {` became an ask of `resolveV2SplitByPostId(db, postId)` followed by a TEAM branch that sets the projected maker leg to an editor's held figure or zero and the platform leg to zero and does NOT compute the 45/45/10 breakdown, then `} else if ((clip as any).marketplaceV2PostId) {` around the unchanged fork; `split: "SHARED"` named in that fork's call; and the ordinary write's reason reads `tracking-tick:marketplace-v2-team` for a team clip (every other clip's string unchanged). The rest is comment. Justification: a team clip stays on the ordinary branch, so its poster leg and owner cut ARE the ordinary clip's. Every other path through the tick is unchanged.

**Guards.** New `check:v2-split-one-rule`, S1 to S9: the rule written once and the grant history read nowhere else; every calculator call names its split; the writer asks and refuses; TEAM pays through the ordinary calculator with no maker or platform leg; the tick's team branch; every rate at the clip's split with every call naming it; the SQL form beside the rule; no poster screen saying 45 percent; closures recorded and an editor's held leg never written. Updated: budget lock B4 and B5 (the shares live in the split file; the chokepoint and sync must CALL the derivation and hold no copy), rules gate R4, lists L5 (**tightened**: BL-940's own second `groupBy` let the old count pass when the counting one was removed, which the demo caught) and L7 (the three grant history reads named with their bound), and the single share writers guard's message. **Each shown failing alone, never sampled:** `scripts/bl940-guard-demo.mjs` 16 of 16 (S1 to S9, B4, B5, R4, L5, L7, W3, and a prose only negative), each restored byte for byte by sha256 and green again; the earlier demos cover the rest of those guards' checks (BL-898 B1 to B4 and B6 to B9, BL-896 L1 to L4 and L6 and L7, BL-923 R1 to R3, R5, R6, BL-894 W1, W2, W4 and S4); their three stale anchors (B5, L5, R4, and W3's count) are the checks the BL-940 demo covers. The 11 BL-678 guards: 0 lines changed.

**Builds.** Three production builds from logs with the real exit code: the first failed on a type error in my own proof script (exit 1, fixed); the second and third exit 0, all 23 prebuild guards passing and the hooks gate 0 errors and 10 warnings (limit 11). tsc clean on the worktree before the change and after (0 errors), and on the merged main tree (0 errors, after regenerating that tree's stale local Prisma client, which is gitignored). The merge tree equals the branch tree (`698c03df`). `checkpoint/BL-723` was not merged.

## Found, not changed (BACKLOG BL-940a to e)

1. **BL-940a.** The owner's re-pricing tools (cpm restamp, freeze undo, force recalc, fix earnings, the override route, fix budget, payout adjust) still exclude every v2 post, team ones included: a campaign rate edit restamps ordinary clips and not team posts.
2. **BL-940b.** A level change re-prices a poster's ordinary clips at once and his team posts only at their next tick (sandbox: $160.50 against $162.00 until the tick). On a past campaign where ticks stop, the difference would stay.
3. **BL-940c, pre-existing.** On a 45/45/10 post the tick writes the poster's leg before calling the v2 writer, so BL-885's poster paid floor compares against the value just lowered and never binds when views fall (sandbox: paid $5.23, views 54,321 to 20,000, written to $1.93). An ordinary clip has no floor on falling views either, so a team post behaves as one.
4. **BL-940d.** The v2 post route does not check a post's platform against the campaign's: ANGIE BROWN is Instagram only with no TikTok rate, yet a TikTok post there would be stamped and paid at the campaign's $0.20.
5. **BL-940e.** The real tick cannot run on one database connection (see Part 0).

## Disclosures

• **I reverted my own work once.** While demonstrating guard W3 I restored `tracking.ts` with `git checkout`, which put it back to main and threw away my uncommitted BL-940 edits to that file. Nothing had been pushed or deployed and no row was touched. I re-applied the three edits, checked the diff (43 added, 2 removed), the line endings and five guards, committed immediately, and every later proof, build and render ran on the restored file.
• Proof runs 1 to 5 failed on my harness, not the code: the one connection deadlock, then timeouts at two per pool, then a shared $333.33 budget between my comparison clips, then a poster level reset by the tick (sandbox levels are now what their earnings make them), then a check that expected the 45/45/10 tick path to hold a paid poster (it does not; finding c). Each run was torn down before the next; teardowns found 0 real notices and 0 unremovable rows every time.
• Screenshots stay on this machine (`C:/bl940-sandbox/renders`): the owner's clip review shows real production clips beside the sandbox ones.
