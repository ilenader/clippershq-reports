UNREMOVABLE: none. All 86 ledgered sandbox rows were removed, 684 text columns were swept, and 0 values still carry bl941sbx-.

# BL-941: the owner's marketplace answers, built and proven (ClippersHQ)

**Status:** shipped. Merge `68286e83` went live at 21:46:49 UTC on 2026-10-08 (`/api/version` returned that sha). BACKLOG entry is `91f3613`. Tags: pre-BL-941, post-BL-941, pre-merge-BL-941, post-merge-BL-941.
**Rollback, in this order:** `git reset --hard pre-merge-BL-941` with a verified push, then `C:/bl941-sandbox/BL-941-ROLLBACK-20261008214206.sql`, then `C:/bl941-sandbox/BL-941-ANGIE-ROLLBACK-20261008214706.sql`.
**Limits held:** every read-only script used one connection. The real tick and the local server used two to four, because of the BL-901 committed read. The render subagent opened none of its own; it went through the server, capped at 4. No paid vendor call and no Apify actor: in the sandbox every fetch was stubbed and refused, and every job was parked.

## 1. Rates (Part 1)
**ANGIE BROWN** was changed through `PATCH /api/campaigns/[id]`, the route the owner's edit form uses, signed in as the owner, with apply to existing OFF. The snapshot and printed rollback came first (21:47:06). The route answered 200.
• Instagram clipper rate: $0.20 to $0.10.
• TikTok clipper rate: none to $0.20, with owner rate $0.0985. The form requires an owner rate for every platform that has a clipper rate.
• Minimum payout: $25 to $20.
• Unchanged: the platform ("Instagram", so TikTok is not enabled), the Instagram and legacy owner rates ($0.0985), the locked share 0.32998325 with its guarantee, the $150 max per clip, and the $2,700 budget.
• All 105 clips are byte-identical in stamp and earnings. The 103 stamped $0.20 keep that rate; 2 carry $0.09 (BL-941e). No existing post's money fell.

**Owner's cut.** Before and after, the guarantee pays $49.25 per $100 paid to a poster, 33.0 percent of the total. The edit form does not touch the Instagram owner rate, so neither did I, and the legacy ownerCpm is unchanged. On the real route in the sandbox, an existing post kept $0.20 ($10.86 to $12.25 as views rose), a new post was stamped $0.10, and the owner received 49.22 and 49.18 per $100 on the two.

**Tennis Bracelet (REBOUNDER)** already matched, so it was NOT changed: Instagram $0.10 (owner $0.0493), TikTok $0.20 (owner $0.0986), minimum $20, max per clip $150. It is a NORMAL campaign: not in the marketplace, so its posts are ordinary clips.

**Bug found and fixed.** A v2 post was stamped with the campaign's single highest rate, so after this edit Instagram posts on ANGIE would have been paid $0.20. `createV2Post` now stamps the posting account's platform rate, clipper and owner, exactly as an ordinary submit does. Poster screens read the per-platform rates: "about $10.00 to $20.00 per 100,000 views", or $10.00 on ANGIE.

## 2. No 45/45/10 anywhere (Part 2)
`v2SplitForMaker` never answers SHARED; a former maker's clip is TEAM with makerKind FORMER. The writer, `deriveV2LegTargets` and the tick hold every maker leg that is not the owner's: the row is never written, so it neither falls nor accrues. The platform leg closes and is recorded as MKT2_TEAM_LEG_CLOSED. Everything goes through `recomputeV2PostEarnings` and the chokepoint; there is no parallel writer.

**Transition.** Snapshot and rollback were printed before the push; the transition ran after the deploy and before the next tick. Of 73 posts, 10 moved and were verified: posters $2.26 to $5.07, platform legs $0.50 to $0.00 (10 closures recorded), maker legs $2.20 held with rows unwritten. Payout fingerprint unchanged.

**The 7 former makers** (hash prefixes). Before and after, their legs, earned amount and withdrawable amount are identical:

| Maker | Legs | Held | Withdrawable |
|---|---|---|---|
| a92aea47 | 8 | $0.14 | $0.00 (video gone) |
| a58138aa | 6 | $0.87 | $0.87 |
| b4b68026 | 44 | $1.08 | $0.81 |
| ac0e3f4d | 7 | $0.28 | $0.28 |
| 0f4fe5b1 | 8 | $0.32 | $0.24 |
| 29961807 | 0 | $0.00 | $0.00 |
| 17985027 | 0 | $0.00 | $0.00 |

**Notice.** Each got one in-app notice (`MKT_V2_MAKER_SHARE_ENDED`, bell and push, 0 emails). It is sent once per person; a second send is refused.
• Title: "A change to your marketplace clips".
• Body: "From now on, people who post your clips are paid in full, so your clips no longer earn you a share. Everything you already earned is still yours and you can still withdraw it."
• Their page says: "The Clippers HQ team sends new clips now. Your clips stay up and the people who post them are paid in full. Everything you already earned is yours and is right here."

## 3. The team's clips go live; clippers stay in review (Part 3)
`goesLiveOnSubmit` is true for the owner and an EDITOR, through the form and the token. It still goes through `approveV2Clip`, so the thumbnail and frame pipeline runs as for a reviewed clip, with no second approval writer (guard S12). In the sandbox, owner form, editor form, editor token and owner token were each APPROVED on arrival and recorded with how they came in; a clipper's post still lands PENDING. The Send form takes up to 20 lines and reports each line. New: paste many lines at once, link then title; lines without a link are counted and left out.

## 4. Post screen (Part 4)
It shows "30 minutes from the moment your post goes live", and: "You can post each clip once per account. To post it again it must be a different account you have connected, and you pick which one below. We check." After posting it says how many other accounts are left and offers "Post from another account", which reopens the form with only the unused accounts and moves focus to the account select. Proven: the same account twice is refused 409 (not 429), a different connected account succeeds 201, and the page knows both. The submit path accepts nothing new.

## 5. Max per clip (Part 5)
A v2 post pays through the ordinary branch: `tracking.ts` `campaignForCalc` sets `maxPayoutPerClip: econ.maxPayoutPerClip`, and `calculateClipperEarnings` caps the base, with any bonus on top exactly as on an ordinary clip. Proven on a $150 cap: views worth $177.78 stopped at $150.00, and the budget counted exactly $150.00 plus the owner's cut.

## 6. Upload token (Parts 6 and 9)
`POST /api/marketplace-v2/upload` with `Authorization: Bearer <token>` and a JSON body: `campaignId`, `title`, `driveUrl` (a Google Drive link, not the file) and an optional `description`. One clip per request; 60 an hour per token, 120 per IP; answers 201 `{ok, clipId, state:"LIVE"}`.
• The owner's tool can use it as it stands, if it sends that JSON.
• A tool holding local files must, for each file: upload it to Drive (`files.create`), share it (`permissions.create`, anyone with the link, reader), then send its link.
• Sandbox: a token send answered 201 LIVE and the clip was APPROVED; a wrong token got 401 TOKEN_INVALID. No token value was printed.
• Guide and tokens now carries a ready curl example with `<your token>` as the placeholder.
• Direct file upload was NOT built. It needs a multipart route with magic-byte and size checks plus object storage. At about 75 MB per one-minute 1080p clip, 1,000 clips is about 75 GB, about $1.10 a month on R2.

## 7. Proof
**Sandbox** (prefix bl941sbx-, opening snapshot): library proof 32 of 32, HTTP proof on a production build 9 of 9. Every failure path ran as its own user, never 429, on views that do not divide evenly.
**Invariants, full population:** 11 of 11 before, 15 of 15 after. 23 budgeted campaigns, 0 over. No double pay; earnings = base + bonus everywhere; no negative maker leg. ANGIE BROWN under $2,700 ($23.38 spent before, $25.69 after; getCampaignBudgetStatus agrees). 76 of 76 live posts correct, 29 frozen posts untouched, every non-owner maker's legs identical, payouts untouched.
**Reconciliation** (new rule, both forms, every row classified). Before, 14 rows: the 10 live former-maker posts the transition moved plus 4 frozen. After, 4 rows: e2e9d428, d7c2fe32, dafe34f4, 15473e60. Their video is gone, so they are never re-priced and are excluded from every budget and balance sum ($0.11 of platform legs). The tick re-prices one at the full rate if its video returns (BL-941b).
**Money files:** 5 byte-identical by blob OID (clip-earnings-writer, earnings-calc, balance, clip-earnings-invariant-middleware, money-decimal). `tracking.ts` changed one line:
```
-          newV2EditorAmt = v2SplitDecision.makerKind === "EDITOR"
+          // BL-941 — an editor's leg and a former clipper maker's leg are both
+          // held where they stand; only the owner's own leg closes to zero.
+          newV2EditorAmt = v2SplitDecision.makerKind !== "OWNER"
```
Why: the tick's projection of a former maker's leg must be the held amount, not zero, or the budget lock would price a write the sync never makes. The 45/45/10 fork beside it is now unreachable (BL-941a).
**Guards:** check:v2-split-one-rule runs S1 to S12. S7 to S9 were rewritten; S10 (never SHARED), S11 (per-platform stamp) and S12 (live only via approveV2Clip) are new. Wording was updated in the rules gate and the single-share guard; the lists allowance is now 2. `bl941-guard-demo.mjs`: 26 of 26, each edit failing only its named check, sha256 restored, guard green again (including a negative case and B4, B5, R4, L5, L7, W3). The 11 BL-678 guards are intact.
**Builds** (from logs, real exit codes): build 1 failed on a type error in a script written while it ran (fixed). Builds 2 to 5 passed with 0 TS errors and a hooks gate of 0 errors, 10 warnings (limit 11). The merge tree equals the branch tree (c080b08d).
**Renders:** 9 surfaces at 320, 375, 414, 1280 and 1440, as real minted sessions on a production build: 45 shots, each with window.innerWidth equal to its width and a pan of 0px; 215 of 215 checks with every state in words. The accessibility review found 2 major issues (focus after "Post from another account"; the no-links paste note only spoken); both were fixed and confirmed.
**Found, not changed:**
• BL-941c: ANGIE's Instagram owner rate is $0.0985 against a $0.10 clipper rate, which the agency monitor reads as ambiguous. The calculator would give $0.0493.
• BL-941d: no platform check on posts (BL-940d), so a TikTok post on ANGIE would now be stamped $0.20.
• BL-941e: 2 odd $0.09 rows on ANGIE, one PENDING holding $54.58.
• BL-941f: the edit's audit row logged only the minimum payout, and logged it "from null".
**Worktree:** C:/b941 removed and verified.

**One line:** A new post earns $0.10 per 1,000 views on ANGIE BROWN Instagram; its $0.20 TikTok rate is set but TikTok stays off. Tennis Bracelet pays $0.10 on Instagram and $0.20 on TikTok as ordinary clips, since it is not a marketplace campaign. ANGIE's existing posts kept their stamped $0.20. The minimum payout is $20 on both. Each former maker holds exactly what they held before, $2.69 in all: a92aea47 $0.14, a58138aa $0.87, b4b68026 $1.08, ac0e3f4d $0.28, 0f4fe5b1 $0.32, 29961807 $0.00, 17985027 $0.00.
