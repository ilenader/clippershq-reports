UNREMOVABLE: no database row. On disk, C:/b944lf2 (a plain extraction of the merge, used to run the guards on Linux line endings) is left for you to delete: the safety check refuses rm -rf at the C: root without a person, so I did not try. Four sandbox runs were removed and verified; 709 text columns were swept and 0 values still carry bl944sbx-.

# BL-944: the exclusive marketplace engine, one clip, one poster (ClippersHQ)

**Status:** merged as `c212f868` and pushed with verification (origin == local). The first web deploy (c212f868) FAILED on Railway, while the tracking-cron service on the same commit succeeded. The logs need a Railway sign-in. Every guard, every import case and the LF bytes checked clean, and the next push (the BACKLOG, 1c233f90) deployed with "success": the live /api/version reports 1c233f90 since 22:06 UTC on 2026-10-09.
**Tags:** pre-BL-944, post-BL-944, pre-merge-BL-944, post-merge-BL-944.
**Rollback:** `git reset --hard pre-merge-BL-944` with a verified push, then the ROLLBACK lines in `scripts/migrations/BL-944-exclusive-reservations.sql` and `BL-944-unique-indexes.sql`, run in the SQL editor (additive only, so the old code ignores the new tables).
**Limits held:** • Each read-only query held one connection, and subagents opened none. • The sandbox engine proof peaked at 4 connections and the local server was capped at 4, because a tick and the post need the BL-901 lock on a second connection. • No paid vendor call and no Apify actor: keys were blank, fetch was stubbed in the library proofs, and every sandbox job was parked.

## 1. Measured first
**Per-account rule:** `createV2Post` gate three (2 hits of `accountAlreadyPosted`), plus `marketplace_v2_posts_v2clipid_clipaccountid_key` in pg_indexes. It is retired in code (now 0 hits). The index stays, since it can never fire on an exclusive post.
**The limit of 20:** found with grep -c. • Family one, the server clamps, 2 sites: campaign create (`OWNER ? 20 : 10`) and campaign edit (`Math.min(20)`). • Family two, the form, 1 site: its dropdown of 20 options and the sentence "Max 20 per user per day". • All three now say 100 (the admin ceiling of 10 is unchanged). The per-user overrides already allowed 1,000. Other 20s (batch line caps, page sizes) are not this limit and were left alone.
**Rate limits:** • Post route: 40 an hour, now replaced. • Unchanged: state 120 an hour, submit 60 an hour, upload token 60 an hour per token and 120 per IP.
**Freshness:** a post must be at most 30 minutes old, measured against the platform's own publish time, which a vendor reads (HikerAPI for Instagram, failing open; Apify for TikTok; the YouTube API). It is independent of anything on our site.
**Strikes:** one creation site (`marketplaceV2Strike.create` in `marketplace-v2-strikes.ts`), and 0 strike rows. The S checks in check:v2-strike-sites forbid any cron from mentioning the strike table.
**Clips with posts today:** all 31 approved clips. They have all left the open marketplace.

## 2. Exclusivity that cannot race
**Two partial unique indexes,** each applied as its own statement through `run-schema-sql.js` and read back from pg_indexes: • `uq_v2_reservation_active_per_clip` on ("v2ClipId") WHERE status = 'ACTIVE' • `uq_v2_post_exclusive_per_clip` on ("v2ClipId") WHERE "isExclusive" Every post from BL-944 on is exclusive. Older posts keep `isExclusive = false`; a clip holding any post is refused under the lock.

**One transaction under BL-901's campaign row lock.** Reserving and posting run in one transaction that takes BL-901's lock, `SELECT id FROM campaigns WHERE id = $1 FOR UPDATE`, and then the clip row lock.

**Proven:** • Two reserves at the same instant: one 201, one 409, one hold, both in the library and over HTTP. • Two posts of one open clip at the same instant: one 201, one 409, one post. • Somebody else's live URL is still refused.

## 3. Reservation lifecycle
**The four outcomes:** • Reserve, from an open clip only. • Let go: free in the first 10 minutes, a warning after. • Satisfied by an accepted link. • Expired: the window passed on the database clock, `"expiresAt" <= now()`, never a vendor fetch. Holds are settled when somebody touches the marketplace, never by a cron.

**No warning when the platform or the owner caused it:** • A clip withdrawn or since sent to somebody. • A campaign paused or ended. • An owner cancellation. • A link pasted in time and refused for a reason on our side: a vendor that could not answer, our own gate, or an error. His own mistake (a bad link, the wrong account, somebody else's link, a post over 30 minutes old) protects nothing. The words say: "This does not add time to your reservation."

**The two clocks.** The post route stamps the paste FIRST, on the database clock. A link pasted inside the window is then in flight for 3 minutes, so no settle can expire it and a post landing in that gap counts as in time. So a poster who reserves, posts at minute 25 and pastes at minute 28 passes both clocks: • His post is 3 minutes old. • His paste was stamped at 28. If the owner sets a window over 30 minutes, the freshness rule still applies: a post must be pasted within 30 minutes of going live. The rule and the campaign form both say so.

## 4. Warnings and the block
**Their own record.** Warnings live in `marketplace_v2_reservation_warnings`, separate from BL-885's strikes, written at ONE site (`issueWarning`, called only by `endReservation`). There is no block column. The block is computed at read time from the warnings that are not cleared and that came after the owner's last lift: 3 within 30 days block reserving for 7 days, measured from the third. The owner clears a warning or lifts a block in one press, and it takes effect on the next read.

**check:v2-strike-sites, updated deliberately with W1 to W7:** • W1: one warning site. • W2: no cron mentions reservations. • W3: no block column. • W4: no vendor import, and expiry runs on our own clock. • W5: warnings never touch strikes. • W6: only a lapsed window or a late release warns. • W7: holds are created only in the library.
**New guard check:v2-exclusive, X1 to X6:** • X1: the claim runs inside the transaction, every post is exclusive, and gate three is gone. • X2: the lock is taken first. • X3: both indexes are their own statements. • X4: every poster read hides clips sent to others or posted by others. • X5: the paste is stamped before freshness, and the bucket is 100. • X6: clipper routes use the session only.
**Demonstration:** `scripts/bl944-guard-demo.mjs` passes 15 of 15. Each edit fails only its named check (L7 included), the bytes are restored from a copy (sha256 identical), and the guard is green again. A comment-only case does not trip W2.

**The messages, verbatim.** • **Before reserving:** "Reserving makes this clip yours alone for 30 minutes. Post it on your account, then paste the link here before the time runs out. Paste it within 30 minutes of your post going live, and before your reservation ends. If the time runs out without a link, the clip goes back to everyone and you get a warning. 3 warnings in 30 days stop you reserving for 7 days. You can let it go in the first 10 minutes with no warning." • **Each warning:** "Your reservation of "<title>" ran out before a link was pasted, so the clip went back to the marketplace. This is warning 1 of 3 in the last 30 days. At 3, you cannot reserve clips for 7 days." • **The block:** "You have 3 warnings in the last 30 days, so you cannot reserve clips until <day month, hh:mm> UTC. Clips sent to you still work. If you think this is wrong, contact the admins." • **Cool-off:** "You have done more than 100 posting actions in the last hour, so we have paused you for about 10 minutes. If this seems unfair, contact the admins."

## 5. Assignment, niches, limits and rate
**Assignment.** The owner, an editor (on clips he made) or the upload token (`assignTo`) can send a clip to a named person, at submission or later through `POST /api/marketplace-v2/admin/assign`. • Shapes: one person per line, or one person for many clips. Each line is reported and audited. • A send naming an unknown person is refused before any clip exists. The clip is assigned BEFORE approval, so it is never live and open even for a moment. • An assigned clip is invisible and unpostable to everybody else: the list, the page (404), the reserve (404) and the post (404). It has no timer and no warning.

**Niches.** The owner or the clip's maker sets them through `PATCH /api/marketplace-v2/admin/clips/[id]/niches`, or at submission. A poster tags his account through `PATCH /api/marketplace-v2/poster/accounts/[id]/niche` (the existing `contentNiche`). The catalogue pages across database-counted tiers: his own clips first, then his niches, then the rest, so page two follows page one.

**Limits and rate.** • Window: 30 minutes by default, 10 to 180. • Holds: 20 by default, up to 100. • Daily clips: up to 100. • Values out of range are refused in a sentence, never clamped. • One bucket of 100 posting actions an hour (reserve, let go, post) with no "too fast" refusal below it, then a 10-minute cool-off.

**Clipper routes, each proven by direct request to reach only his own data:** • His reservations list. • Letting go of another poster's hold: 404, and the hold stands. • Another poster's assigned clip: 404. • His own account's niche: 200; another poster's account: 404. • Every owner and team route: 403.

## 6. Owner control
**`/market/admin/reservations`** has an owner tile and is OWNER-only on both the page and every route. It shows: • Every reservation by status, with person and clip. • Every assignment. • Every warning and every block.
**One press actions,** each with a reason, an audit row and the time as `::text`: • Cancel a reservation. • Take back, reassign or bulk-send clips. • Clear a warning. • Lift a block. • Move a mistaken post: same campaign, through `recomputeV2PostEarnings` in a Serializable transaction under the lock. It is refused for a post carrying a pre-BL-940 maker or platform leg.

## 7. Proof
**Sandbox** (prefix bl944sbx-, opening snapshot): the engine proof passes 41 of 41 on the final code. • 20 holds, then the 21st refused with 409. • All 20 posted with no refusal. • Three lapses, then a block until +7.0000 days; reserving and a one-step post are both refused (403); the lift works at once. • Every no-warning path, the in-flight paste, and his own mistake warning. • Both races. • Assignment. • A legacy clip closed off. • Niches first, across pages. • Moving a post. • The cool-off.
**HTTP walk on a production build:** 11 of 11. • 20 reserves and 20 posts, 40 actions with no refusal. • The rule is required first. • Scoping. • The race. • The owner's routes. • The settings refused out of range and accepted in range. • 100 actions, then 429 for about 10 minutes. Every failure path ran as its own user, never 429 except the cool-off.
**Invariants across the full population:** BEFORE 13 of 13, AFTER 16 of 16 on the live deploy at 22:06:37 UTC. No real reservation, warning, lift, assignment, niche or exclusive post exists. Every real post is identical or moved by a tick, every maker's legs are identical, and payouts are unchanged.
**Reconciliation, both forms:** the 4 frozen BL-941b rows only (e2e9d428, d7c2fe32, dafe34f4, 15473e60), each explained.
**Money files:** all 6 are byte-identical by `git rev-parse HEAD:<path>`: clip-earnings-writer, earnings-calc, balance, tracking, the invariant middleware and money-decimal.
**Builds** (from logs, real exit codes): baseline and builds 1 to 4 all BUILD_EXIT=0, with 0 TS errors and a hooks gate of 0 errors and 10 warnings. The merge tree equals the branch tree (61f4645d). The 11 BL-678 guards and every prebuild guard are green.
**Renders:** 5 states at 320, 375 and 1280 (open, held, sent to you, held by someone else, the owner page): 15 shots, each at its width with a pan of 0px, and 69 of 69 checks.
**Accessibility review:** it found 1 blocker and 4 major issues. All 4 majors and the minors were fixed and confirmed.

## Open, for the owner
**BL-944a: ACCESSIBILITY CONFLICT, WCAG 2.2.1 Timing Adjustable (Level A).** It is OPEN: a poster cannot extend a hold. • The per-campaign window does not satisfy 2.2.1, because the poster must be able to adjust it himself. • Option A, which fixes it: an "Add N minutes" control, offered 20 seconds before the end, at least 10 times. It changes your strict rule. • Option B, which leaves it failing: you record an essential exception in writing. • Mitigations in place now: visible and spoken warnings at five and one minute, "Let it go", and the free time left.

**Other open items:** • BL-944b: `clip_accounts.niche` was added and then found redundant with `contentNiche`. It is empty and unused. Drop it in the SQL editor: `ALTER TABLE clip_accounts DROP COLUMN IF EXISTS "niche";`. • BL-944c: the open marketplace is empty until the team sends new clips, because all 31 approved clips already have posts. • BL-944d: the cool-off is in memory per server process, like every limit here.

**What BL-945 must build on top:** • The catalogue's reserve-first cards with the time left. • A "my reservations" page (the route exists: `GET /api/marketplace-v2/poster/reservations`). • The niche controls for posters and the owner. • "Send to a person" fields on the Send form. • The owner page's design. • The 2.2.1 decision.

**One line:** The reservation window is 30 minutes by default (10 to 180). One warning per lapsed window; 3 in 30 days block reserving for 7 days. At most 20 holds at once (owner sets up to 100), up to 100 clips a day, and 100 posting actions an hour before a 10-minute cool-off. All 31 existing approved clips left the open marketplace because they already had posts.
