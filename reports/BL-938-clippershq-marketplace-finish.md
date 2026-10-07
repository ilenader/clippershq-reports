Unremovable: none. Teardown removed every ledgered and prefixed row; a sweep of 684 text columns found 0 values still carrying the sandbox prefix.

# BL-938 — the marketplace finished for the owner

Merged to main at e074aef (branch checkpoint/BL-938, tip bbd53ec). Tags: pre-BL-938 (04bc5f5f), post-BL-938, pre-merge-BL-938, post-merge-BL-938. Rollback: `git reset --hard pre-merge-BL-938`. Both pushes verified by safe-push (origin == local). Handles are redacted; people appear as the first 8 characters of an md5 of their id.

## The end line

• **Former makers who can now post: 7 of 7.** All 7 are active clippers and none holds the EDITOR grant, so rule two no longer binds them. 4 of them hold an approved account today and can post at once; the other 3 need an approved account first, as anyone does. 0 open payouts among the 7 (2 have historical PAID payouts from 2026-07-30 to 2026-08-29, which nothing here touches).
• **Old clips converted: 4**, each to a marketplace post made by the owner's own maker account, priced at the clip's own rate. What each party holds now (DB, after production's 21:01 tick re-priced two of them as posts):

| Clip | Status | Poster | Maker (owner) | Platform | Owner's ordinary cut (agency) |
|---|---|---|---|---|---|
| wgurtb | APPROVED | $0.69 | $0.69 | $0.16 | $0.76 |
| ah6th8 | APPROVED | $0.74 | $0.74 | $0.17 | $0.81 (was $0.82, see finding 4) |
| slho1c | APPROVED | $0.32 | $0.32 | $0.06 | $0.34 |
| wrh6hf | **PENDING** | $24.54 | $24.54 | $5.35 | none |

• **wrh6hf is converted and still PENDING.** Nothing already paid was clawed back; none of the four was on any payout of any kind. ANGIE BROWN has spent $45.76 of its $2,700 budget.
• **From the owner's home, in one press:**
  ◦ review the clips waiting for review
  ◦ convert an ordinary clip
  ◦ set the page guide or make a token
  ◦ jump to the editors list (add or remove an editor with a reason)
  ◦ open the day's refusals
  ◦ see the token uploads refused
  ◦ see the approved clips that have no preview
  Every item is a count. No money is computed on the home.

## Part 1 — rule two lifted for people without the EDITOR grant

• `hasOtherSideOnCampaign` (src/lib/marketplace-v2-side.ts) now asks the team gate first when the person is posting: someone who is not on the team (not OWNER, no EDITOR grant, read fresh from the database) is exempt. Editors are still refused on a campaign they made clips for. Gate zero in `createV2Post` (nobody posts their own clip) is unchanged.
• Guard `check:v2-submit-is-team-only` gained **T10**: exactly one exemption block before the count, and gate zero present exactly once and before the post is written. Demonstrated failing one mutation at a time: exemption removed, exemption widened to everybody, gate zero removed, gate zero moved after the write. Each failed with its own words; the clean copy passed. Demo run: 20 of 20 (T1 to T10).
• Proven by direct request against a local production build (sandbox people, real sessions):
  ◦ a former maker posting somebody else's clip on the campaign they made clips for: **201**
  ◦ the same person posting their own clip: **409** "This is your own clip, so you cannot post it yourself. Somebody else posts it and you earn the maker's share of everything they make with it."
  ◦ an editor with a clip on that campaign: **403** OTHER_SIDE_ON_THIS_CAMPAIGN, "You have clips of your own on this campaign, so you cannot also post on it."
  None of these was a 429.

## Part 2 — the conversion priced at the clip's own rate, then the four real conversions

• New `src/lib/marketplace-v2-pricing.ts` loads exactly what the tracking tick uses: the clip's stamped rate first (BL-756 overrides included), the snapshot economic fields, and both parties' bonus inputs. The preview, the write (`recomputeV2PostEarnings` into the one chokepoint) and the undo all use it. No second writer was built.
• Proof on a sandbox clip stamped at $0.09 against a $0.20 campaign: the old formula gave $10.86 gross, the fixed one **$4.89**, split $2.20 poster, $2.20 maker, $0.49 platform. Preview equals write equals tick, 11 of 11 checks. The poster's paid floor held at $5.23 while the maker kept $2.48; undo restored the poster to $4.89.
• Scope was re-measured: exactly 4 ordinary clips on marketplace campaigns, 0 on any payout, so no STOP.
• The owner's maker account was established by evidence: the owner account 471193bd made 5 v2 clips on 2026-09-23 between 13:36:57 and 13:42:46, all posted by the same poster b0616ed6 between 13:55:34 and 13:58:11.
• Converted one at a time by explicit id, each with a before snapshot, a preview and its undo command printed first, each 7 of 7 checks, between 19:56:50 and 19:57:39 UTC. Snapshots: before.json and after.json per clip.
• The Convert button (owner only):
  ◦ It sits on the clip review row, for ordinary clips on MARKETPLACE_ONLY or BOTH campaigns only, and on a new "Clips you can convert" page.
  ◦ The overview's "Convert a clip" link now opens that page.
  ◦ The dialog shows the route's own preview in plain words, including "this clip's own rate", and asks for a maker and a required reason.
  ◦ After converting it offers Undo.
  ◦ The route is the existing one; the preview gained `rate` and `rateSource`.

## Part 3 — the owner side

• **Send several clips** (owner and editors), up to 20 lines. The team gate runs once, then every line goes through `submitMarketplaceClip`, the same path as the form and the token. Each line is reported on its own, never all or nothing: 201 if any line was created. Proven:
  ◦ three lines sent at once, three created and live
  ◦ a folder link refused with the single form's exact words while the next line was sent and an empty link was refused
  ◦ a clipper's multi-line send refused whole (403, nothing written)
• **Owner home** at /market/admin/home. /market sends the owner there, and the Home tile was added to the owner's nav.
• **Editors list** with add (search by username) and remove, both through the audited grant with a required reason.
• **Guide and tokens:** the tokens section now explains in two lines what a token is and that its value is shown once. The integration example and the shown-once reveal from BL-937 are kept.
• The home answers counts only, with no money field. A clipper and an editor are refused the home, the convert list and the editor search (403).

## Part 4

• **BL-785 re-applied by hand.** It did NOT apply cleanly: it conflicted with BL-820's `sharesSource`, and the resolution keeps both. The owner submit path no longer stores a fabricated zero first snapshot when no provider answers. Harness 41 of 41. Proven live: a bulk owner clip with every provider key blank got 0 clip_stats rows.
• **TikTok photo lines** on the bulk owner route are refused with the single route's exact words, and the rest of the batch still goes through. Proven: photo line refused, reel line created. The owner override path refuses test campaigns, so the sandbox campaign was moved to "real and COMPLETED" for a 20 second window (20:32:18.76 to 20:32:38.91 UTC) and back.
• **Pans at 320px fixed:**
  ◦ the overview campaign filter
  ◦ the profile time range toggle
  ◦ the profile account row, where a 26 character handle still panned 114px
  ◦ the clip review money lines, which were pre-existing since 2026-05-06 and panned 106px at 320
  All four measure 0 at 320, 375 and 414.
• **Campaigns heading focus ring removed.** Tailwind v4 layers its utilities, so no class can beat the global `*:focus-visible` rule. An opt-in `[data-focus-target]` rule in globals.css does it, on this round's focus targets only. Rendered with no visible ring at all 5 widths.
• **Stale comment at MpFilterPills.tsx:83** fixed.
• **Owner notices skip sandbox data** (`createNotification`, `notifyOwnersOfPendingV2Clip`). Proven: an editor submission, three owner sends and a token upload produced **0** notices on real owner accounts. The cleanup script found 0 to remove.

## Part 5 — polish

The polish covered every surface this round changed: the home, the convert list and dialog, the clip review row, Send several, the editor screen, the campaigns heading, the overview and the profile. Each was rendered per surface in parallel. The accessibility lead reviewed the built code and found 6 major and 8 minor items; all 14 were applied and re-rendered.

The marketplace surfaces this round did not change (catalogue, post page, money pages) were not re-rendered. BL-923's simple tiles, BL-931's even tiles and BL-937's job rail are unchanged.

## Part 6 — the record

**Renders.** Playwright with a throwaway profile, at 320, 375, 414, 1280 and 1440, with `innerWidth`, the URL and the sideways pan read back beside every shot. Three browser processes ran in parallel (cap 3). Every run is listed:

| Run | What happened |
|---|---|
| Run 1 | 94 passed, 34 failed. Script faults: Playwright will not click an `aria-disabled` button; the form opens with two lines; the modal close and the problem-report dialog were counted. Plus the two real pans and timeouts under load. |
| Run 2 | 136 passed, 8 failed: the heading ring, and the clip review pan. |
| Run 3 | 144 passed, 15 failed: `focus:outline-none` also loses in Tailwind v4. |
| Run 4 | **159 passed, 0 failed**, 51 screenshots. |

• **Walk.**

| Run | What happened |
|---|---|
| Run 1 | Every call 401: my server script set an http AUTH_URL, which renames the session cookie. 11 anonymous refusal rows resulted; they were ledgered and removed. |
| Run 2 | 21 of 23. The 2 failures were the bulk route refusing a test campaign. |
| Bulk check | Re-run in the flip window: passed. |

• **Builds:** 5 production builds, each exit 0, hooks gate 0 errors and 10 warnings (limit 11). tsc clean on every pass. The final prebuild ran 22 guards plus the hooks gate, exit 0, on the tip whose tree equals the merge (82135119), so no rebuild on main was needed.
• **Guard demo:** run 1 was a syntax error in my script; run 2 had 3 mutations that did not apply because of CRLF; run 3 was 20 of 20.
• **Money files:** all 6 byte identical to main by blob OID; tracking.ts is not in the diff. BL-678's 11 guards are untouched (0 lines changed) and its hard-off test passes 28 of 28.
• **Invariants and both reconciliation forms** (leaks only, and every row with a verdict):
  ◦ opening snapshot 19:52:12 UTC: 13 of 13
  ◦ after the four conversions: 13 of 13
  ◦ final, after teardown at 21:40:49: 13 of 13
  Both reconciliation forms returned 0 rows each time.
• **Sandbox:** prefix bl938sbx-, opening snapshot first, values that do not divide evenly (budgets $333.33, $211.17, $123.45; 41,113 views). Every tracking job was parked after every step that could create one; the final count was 4 of 4 parked, and none was ever checked by production.
• **Vendors:** sandbox vendor rows 0, cost $0. The one sandbox reel the bulk route tried was stopped by the BL-678 hard off and a blank HikerAPI key; no request left the machine.
• **Real rows touched:** the four conversions and their audit rows only. No owner setting was changed.

## Found, not changed (BACKLOG BL-938a to BL-938e)

1. **First ever CRON_DID_NOTHING** at 20:31:53 UTC: a batch tick saw 7,395 due clips and processed 0. 7,380 jobs are more than a day overdue, the oldest from 2026-05-14. Ticks either side processed clips (34 checks in the 20:00 hour, 46 by 21:06). Nothing this round wrote touches the queue. Needs its own review.
2. Tailwind v4's layers make all 32 existing `outline-none` focus targets show a ring.
3. The shared Modal close button is 36px (the house rule is 44). The time range toggle has no `aria-pressed`, and white on accent at 12px is about 3.4:1.
4. Agency on a converted clip can move a cent on its first tick: ah6th8 went from $0.82 to $0.81 at the same 8,148 views. The conversion never writes agency; the tick does.
5. A sandbox OWNER receives real production owner alerts. The 20:31 alert sent one email to the sandbox owner's example.invalid address, and the provider accepted it. The record was removed at teardown.

## Disclosures

• While the walk ran, two processes held one database connection each (the server and the walk script, both connection_limit=1). Never more than two.
• Every process I started was stopped by its own PID taken from netstat on port 3938. The worktree and C:/bl938-sandbox are removed after this report.
