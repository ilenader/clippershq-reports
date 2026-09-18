# BL-907 — your clipper account is an ordinary clipper now, the extra was TWO lines not one, and the marketplace launched for real while this round was running

**2026-09-18. Zero database writes. No product behaviour changed except the two grants below. Merged `12414433`, tagged `pre-BL-907` / `post-BL-907`, pushed and verified from origin.**

## THE HEADLINE: YOU LOSE NOTHING, AND THE REASON IS SOMETHING YOU DID AT 19:08 TONIGHT
At **19:08 UTC** `ANGIE BROWN THE REAL ME` became `campaignType MARKETPLACE_ONLY`, ACTIVE, not a test campaign. At **20:37:39 UTC** a real CLIPPER (handle `sam***`, `isTestUser` **false**, on no allow list) chose the EDITOR side and submitted **the platform's first ever marketplace v2 clip**. BL-905's standing blocker, the one it said no round could fix, is closed, and you closed it.

That single row settles the question this round could not otherwise answer. `isMarketplaceV2VisibleForUser` has exactly four ways to return true: the v2 flag, the v1 flag, `role === "OWNER"`, `isTestUser === true`, or the preview list. That person is a plain CLIPPER, not a test user, and was never on the list. **So one of `NEXT_PUBLIC_MARKETPLACE_V2_ENABLED` or `NEXT_PUBLIC_MARKETPLACE_ENABLED` is `"true"` in Railway right now.** Measured by consequence, not guessed.

**Which means removing your preview line is a NO-OP. You keep the marketplace, exactly like everybody else.**

## MODEL SPLIT
**100% Opus, zero subagents.** The cheap-model half of the brief was not taken, and that is deliberate: every step here either decided a deletion from live product code on an account holding $991.11 of payouts, or read a raw query I had to see myself. BL-899 gave the reasoning and BL-896 gave the evidence, a subagent returning three claims that were false on reading the files. Enumeration was shell and SQL, which costs the same at any tier.

## PART 0 — EVERYTHING THE ACCOUNT CARRIED
**The handle and the email are ONE account**, counted four ways: 1 row by handle, 1 by email, **1 carrying both**, 1 distinct id across the union, and that id is the one already on the preview list. Nothing to guess, nothing to stop for.

Compared field by field against the 1,690 active clippers and against one real clipper carrying 392 clips:

| what it carries | an ordinary clipper | this account | verdict |
| --- | --- | --- | --- |
| `role` / `status` / `isDeleted` | CLIPPER / ACTIVE / false | CLIPPER / ACTIVE / false | same |
| `isTestUser` | false (only 2 of 1,690 are true) | **false** | same. BL-905's correction stands |
| `reviewerCapabilities` / scope / mode | empty, TRIAL (0 of 1,690 hold any) | empty, TRIAL | same |
| `reviewerCanSeeDecided` | false (**0 of 1,690**) | **false** | same, and three code comments still claim otherwise |
| `canActAsClipper`, `bulkAddBypass`, `clipSubmitBypass` | false | false, false, false | same |
| `isTrainer`, `posterStatus`, bans, strikes, `manualBonusOverride` | none | none | same |
| `marketplaceV2Role` | null for most; 5 people have chosen | **EDITOR, chosen 2026-09-17 19:33:35.869** | **a CHOICE, not a privilege. NOT reset** |
| `lastClientSeenAt` | null (**he is the only clipper with it**) | 2026-06-23 10:05:00.163 | residue of the fortnight BL-226 had him as CLIENT. Read only by the owner's clients screen, which he is absent from (0 `campaign_clients` rows). Grants nothing. Left alone |
| `sessionVersion` | 0 for most, 29 are above it | 37 | a JWT invalidation counter. Grants nothing |
| **`MARKETPLACE_V2_PREVIEW_USER_IDS`** | not listed | **listed (BL-890)** | **PRIVILEGE. Removed** |
| **`FRESHNESS_EXEMPT_USER_IDS`** | not listed | **listed (BL-709)** | **PRIVILEGE. Removed** |

**THE SECOND ONE IS THE FINDING, AND THE BRIEF IS WHY IT WAS FOUND.** `src/lib/clipper-submit-core.ts` carried this account as the only id on the platform exempt from the **30 minute posting window**, and reading the call site rather than the comment shows it is broader than BL-709's header says: the branch covers **TikTok, Instagram AND YouTube**, not Instagram alone. Its only effect is that an already-measured `too_old` **skips the refusal**. An ordinary clipper submitting a clip posted 31 minutes ago is told no; this account was not.

**Nothing else on the platform depends on the account being special.** Its id appears in 14 more files; every one is either a **protection** (the purge and sentinel scripts refuse to run if this id is in their target set), a comment, or your Discord handle shown on the payouts screen. No product code branches on it anywhere else.

## PART 1 — WHAT WAS REMOVED, AND WHAT THAT DOES
**Both rollbacks were printed before either change was made, and neither writes to your user row**, which is the property BL-890 designed for and BL-709 chose an immutable constant for.

| removed | file | to put it back in ONE action |
| --- | --- | --- |
| marketplace v2 preview | `src/lib/marketplace-flag.ts` | restore the one id line to `MARKETPLACE_V2_PREVIEW_USER_IDS` and redeploy |
| posting window exemption | `src/lib/clipper-submit-core.ts` | restore the one id line to `FRESHNESS_EXEMPT_USER_IDS` and redeploy |

**No SQL. No row. `git revert 12414433` undoes both at once. BOTH OUTCOMES OF THE MARKETPLACE LINE, because no round can read Railway:** with `NEXT_PUBLIC_MARKETPLACE_V2_ENABLED=true` (or the v1 flag) it is a **no-op** and you keep v2 like everybody; with both unset you **lose v2 entirely**, since you are a CLIPPER and not a test user. **The evidence above says the first case is the live one.**

**Your money and your work are untouched, by fingerprint and not by assertion.** Measured at 20:41 before any edit, again at 20:53, and again at 21:00 after the merge: **clip fingerprint `98d567e3…`, payout fingerprint `d20bc887…`, clip-account fingerprint `6d83bb41…`, identical all three times.** 203 clips, 187 approved, **$260.45**, 13 payouts totalling **$991.11**, 8 clip accounts (6 approved), 6 campaign memberships, EDITOR side and its 2026-09-17 timestamp unchanged.

**A correction to the brief's numbers, and it is good news.** It quoted BL-890's 194 clips / 178 approved / $248.60. The account is at **203 / 187 / $260.45** because **you submitted 9 Instagram clips at 12:18 today**, all nine approved. That is your own work, hours before this round opened, not drift I caused. Those nine had `postedAt` equal to `createdAt`, age **0.0 minutes**, so **none of them used the exemption I removed**.

## PART 2 — PROVED ORDINARY BY REQUEST, NOT BY READING
Production build, `DEV_AUTH_BYPASS=false`, both flags unset locally so the strict case is the one tested. Both sessions minted from the **real database rows**, never invented, which is the BL-904 mistake BL-905 named.

| request | your clipper account | a genuinely ordinary clipper | same? |
| --- | --- | --- | --- |
| `/api/marketplace-v2/campaigns` | 404 | 404 | yes |
| `/api/marketplace-v2/poster/campaigns` | 404 | 404 | yes |
| `/api/marketplace-v2/catalogue` | 404 | 404 | yes |
| `/api/marketplace-v2/role` | 404 | 404 | yes |
| `/api/marketplace-v2/earnings` | 404 | 404 | yes |
| `/api/campaigns` | 200, **3 campaigns, test campaign absent** | 200, 3, absent | yes |
| `/api/earnings` | 200, 5 campaign balances | 200, 4 | yes (his own money, correctly different) |
| `/api/campaigns/spend` | 200, identical 14-campaign map | 200, identical map | yes |
| `/api/admin/users` | **403** | 403 | yes |
| `/api/admin/clips`, `/api/admin/payouts`, `/api/admin/campaigns` | **404** | 404 | yes |
| `/api/marketplace-v2/catalogue/<test campaign id>` | **404** | 404 | yes |

**14 of 14 identical.** He sees **0** marketplace campaigns and **404** on the test campaign by direct id, which is exactly what BL-905 measured for an ordinary clipper, so `filterTestCampaigns` is doing what it was measured doing. **No admin or owner surface answers him.**

**And the pages refuse him server side, not in the browser.** BL-890 proved a refused clipper gets the bare brand where a granted one gets the real title, resolved per request. Measured now: **5 of 5 v2 page titles identical** between the two accounts, `Clippers HQ` on three and a hard `404` on two. No `.tsx` of mine changed, so **no render pass was run and none is claimed**.

**MY OWN CHECK WAS WRONG BEFORE THE PRODUCT WAS.** My first version demanded `/api/campaigns/spend` refuse a clipper and reported a failure. The route's own header says it is global by design and "clippers need it for progress bars"; CLAUDE.md's rule is about the **full** map, and BL-840 is what made it not-full. Both accounts get the byte-identical map with the test campaign filtered out. The check was rewritten to ask the right question.

## PART 3 — NOTHING ELSE MOVED
**Twelve protected money files byte-identical by blob OID** against current `origin/main`: the six, plus `marketplace-v2-earnings/writer/sync/poster`, `proportional-cut` and `marketplace-v2-catalogue`. **Zero database writes this round**; every access was a SELECT or a GET, **one pooled connection at a time**, no Apify actor and no vendor call. No sandbox row was created, so there is nothing to tear down and nothing unremovable.

**Full population:** 10,285 clips (10,202 live), **0 invariant violations**, 0 negative clip money, 0 negative payouts, 1,766 users, 36 campaigns, 250 payout requests. **21 budgeted campaigns, 0 over budget, closest $300.00 under**, matching BL-905 exactly. v2 tables: 1 clip (the real one above), 0 posts, 0 editor legs, 0 platform legs, 0 strikes. The **first** marketplace is still at 0 submissions and 0 clips, so whichever flag is set has not pulled anybody into v1.

**Reconciliation, including where my own form was wrong.** Form A, the earnings invariant per clip: **0 violations**. Form B, my naive SQL comparing lifetime paid against lifetime clip earnings, flagged 23 and then 14 users. It is **my form that is incomplete**, not a leak: switching to `actualPaidAmount`, what was really sent, collapses the lifetime gap from **$1,201.09 to $101.84** across 14 accounts, and clip earnings are not the only thing a payout draws on (9 `payout_adjustments` rows exist). The authoritative statement is the platform's own `check:paid-is-final`, which passed **all 14 of its assertions** in prebuild including no-double-pay, no-overpayment and no-negative-balance. I changed nothing on that path.

**Guards: 18 of 18 prebuild steps pass, build exit 0, 0 TypeScript errors.** `check:v2-flag-gate` OK at 19 handlers and 10 pages, reporting **"0 ids on the preview allow-list. An empty list means nobody, which is the safe default."** Hooks gate **0 errors, 10 warnings against a cap of 11**, so BL-906 bought back the headroom BL-905 warned had run out. `eslint` is present at v9.39.4, so the gate is not silently no-opping.

**AN INHERITED CHECK WAS TESTING ITS OWN FIXTURE, AND THAT IS THE SECOND FINDING.** `scripts/test-bl-709-freshness-exempt.ts` asserted **"EXACTLY ONE account platform-wide satisfies the exemption"** while querying `WHERE id = ANY($1)` with the literal id **the test file itself declares**. It never read the real list. It would have passed with the list **empty** and it would have passed with a **second id secretly added**, which are the only two ways that list can go wrong. Same shape as BL-904 minting the flag its own check read. It now drives the **real exported predicate across all 1,766 users** and reports **0 exempt**; restoring the id was demonstrated turning **five checks red**, and the old version turned none.

**Stale and named, not fixed:** `prisma/schema.prisma:135` and `src/app/api/clips/route.ts:534` still say this account holds `reviewerCanSeeDecided = true` (the row says false, and **0 of 1,690** clippers hold it); `src/app/api/admin/users/route.ts:147` still calls it a test account. `scripts/test-bl-132-*` asserts the same falsehood and **was already failing before this round touched anything**. None is code and none was in scope.

**THE ROUND WAS MARKED RUN ALONE AND IT WAS NOT.** BL-906 was live in `C:/b906` with 17 dirty files when this started, writing render output at 22:32 local. Nothing of mine touched its tree; I worked in my own worktree at `C:/b907`, waited for it to merge, then merged on top. **The worktree is gone, verified by listing the path**, and `git worktree list` shows only the primary checkout on `main` with the same 19 untracked entries it had at session start.

## PART 4 — IN PLAIN WORDS
**What you had:** a private preview of the new marketplace that nobody else could see, and a quiet exemption letting you submit a clip posted more than 30 minutes ago when every other clipper would be refused.

**What you have now:** neither. Your account is an ordinary clipper account, and 14 of 14 requests prove it answers exactly like one.

**Can you still reach the marketplace? Almost certainly yes, and here is the one sentence:** the marketplace flag is on in Railway (a real clipper who was never on any list submitted the first v2 clip tonight at 20:37), so you keep the marketplace like everybody else; **if it is ever switched off, you will lose it, because you are now an ordinary clipper.**

**What you will notice:** if you submit a clip posted more than 30 minutes ago, you will now be told no, like anybody else. That is the only change to what you can DO. Your 203 clips, $260.45 of earnings, $991.11 of payouts, 8 accounts, 6 campaigns and your EDITOR side are all exactly as they were.

**To put either back, in one action:** say the word and one line goes back into one file. `git revert 12414433` restores both.

**And the one thing that is no longer true:** every round since BL-904 has closed by saying no round can opt a real campaign into the marketplace, only you can. **You did it tonight**, and the first real clip arrived twenty nine minutes later.
