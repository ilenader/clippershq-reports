# BL-893 — the marketplace side becomes a real gate that locks on the first action

**MODEL SPLIT.** The strongest model wrote every line of the gate, the lock, the owner override, all
three action route gates, the replacement guard, its demonstration, both proof scripts and this report,
with no subagent between it and the source. Cheaper models read: a role and guard inventory, a shell
measurement, counted sweeps, an accessibility review. Claims are marked **VERIFIED** where I re-derived
them myself and **READ** where they are a subagent's measurement I did not re-run.

## The reversal, both arguments side by side

**BL-889 BUILT THIS AS A SIGNPOST AND ARGUED IT**, and its three reasons are preserved verbatim in
`marketplace-v2-role.ts`: a thing you may switch at any time enforces nothing; a gate on the wrong person
locks a real earner out on day one for a choice he barely remembers; and five rounds (BL-790, 794, 821,
825, 833) each found a role flag stored and never read, read backwards, or granting nothing. It then
wrote a guard asserting **zero** route reads.

**YOU HAVE ASKED FOR THE OPPOSITE**: they cannot be both, not both on the same campaign, and the lock
falls on the first clip sent or posted. Both texts now sit together in the file, so the next round sees a
decision rather than a drift. **THE GUARD WAS REPLACED, NOT DELETED**: S2, S3 and S4 survive as R2, R7
and R8; S1's job inverts into R1, R3 and R4. Deleting it would leave the column unwatched in the very
round that gave it power.

**BL-889's STRONGEST OBJECTION IS ANSWERED: THE LOCK IS DERIVED, NEVER STORED.** No `roleLocked` column
exists and **R5 fails the build if one ever appears**. A derived lock cannot go stale, be written
backwards, or be left behind by a migration, which is exactly what those five rounds found.

## The lock, defined exactly

**FIRST ACTION**: for a maker, sending a clip; for a poster, posting one. **A PENDING CLIP LOCKS HIM**,
because your rule is that SENDING is the action, not approval. **A REJECTED OR WITHDRAWN CLIP DOES NOT.**
So if the only thing somebody ever did was send a clip you said no to, **the lock releases on its own**,
with no owner and no migration. Locking a person into a side after a rejection would be cruel; this is
the mechanism, not a promise. RETIRED still holds, since pulling an approved clip does not undo posts
made from it. **VERIFIED end to end**: unlocked with nothing, locked by a PENDING clip, switch refused,
**released by the rejection**, free again after.

**PLATFORM WIDE, AND BOTH YOUR SENTENCES ARE BUILT.** Rule one, the side deciding which action routes
answer, is what your first complaint requires: a per campaign rule still shows both tiles to everybody.
Rule two, not both on the same campaign, is unreachable under rule one and **becomes reachable the moment
you override somebody**, since a maker you move to poster could otherwise post his own clip on the
campaign he made it for. **What it costs, plainly: a maker on one campaign can never post on a different
campaign without asking you.** The override is the release valve and it is built, not promised.

**THE WARNING COMES BEFORE THE LOCK FALLS**, above the button that spends it, only while still true:
> **This is the last moment you can change sides.** Sending this clip sets you as somebody who makes
> clips. After this you cannot switch to posting yourself, and only the owner can change it for you.

**YOUR OVERRIDE** is a panel on the person's admin profile, OWNER only, showing their side and what holds
it in counts. The reason is **required and refused server side**, and the audit row keeps you, them, the
side before and after, what was holding the lock, and the **database's own `now()` cast to text**. BL-732
found a cascade that wrote no audit row and went unnoticed for three days.

## What each side sees, and why the tile row is not the rule

A maker sees **Send a clip / Your money / Change what you do**; a poster sees **Post a clip / Your money
/ Change what you do**. Neither sees the other's action. Somebody who has not chosen sees **no tiles at
all**, because the screen he is on is the chooser and a row of destinations competes with the question.

**ENFORCED SERVER SIDE.** BL-888 measured nine of eleven v2 routes with no gate while every page had one,
and the post route answered 201 to an ordinary clipper and minted three money legs. A hidden tile over a
live route is that defect in a new hat. **VERIFIED by request in both directions**: the maker account
refused **403 WRONG_SIDE** on all three poster action routes, the poster account on the maker's, with:
> You are set up to post clips, so this side is not open to you. You cannot switch yourself any more,
> because you have already started working. Ask the owner and he can change it for you.

**AND THE ORDERING HOLDS**: an ordinary clipper still answered **404 and never 403** on those same
routes. A 403 to a stranger confirms a route he must not know exists and would void three rounds of
containment proof. R4 asserts it statically, the proof asserts it by request.

**THE SWITCH STAYS REACHABLE AND SAYS SO IN WORDS**, since all three text tokens render white: the tile
reads "Locked. Open this to see why, and how to ask the owner." **No dead controls** — when locked, the
choice buttons are not rendered at all rather than rendered inert.

## The shell, matched as measurements (READ)

Sixteen properties read off `MpChrome`, `MpNav`, `MpPageShell` and `MpEmptyState` and closed: chrome
inset **0 to 16/24/32px**, chrome top padding **0 to 24px**, width cap **none to 1536px**, page vertical
padding **8 to 32px**, tile gap **12 to 8px**, tile padding **16 to 12px**, icon **24 to 20px**, title
**14px bold to 13px semibold**, subtitle **12 to 11px**, inner gap **6 to 4px**, alignment **left to
centred**, the **104px height floor removed**, the active tile **neutral to a 10 percent accent tint**,
both colour tokens, and the empty state **from a left aligned card with no icon to centred with a 40px
icon, 48px of room and an 18px title**. **The cap does not undo BL-891**: 1536px binds at none of the
five widths, and the measured result is **95 percent content to viewport**.

**NOT MATCHED, deliberately**: the panel's two CTA buttons, which would put both sides back on screen;
the chevron-only affordance, because the text label is what makes the control readable; and the four-up
card grid, because a row here carries a disclosure panel and a verbatim rejection reason a card cannot
hold. No messaging tile, no account-listing tiles, no KPI strip, which you said yourself.

**PERCENTAGES, RE-PROVED NOT INHERITED (VERIFIED):** **2** occurrences of 60 or 30 as a percentage across
every v2 surface, both on lines 13 and 14 of `V2Explainer.tsx`, **inside that file's own comment saying
those are the other feature's numbers**. Zero rendered; every number a person reads is 45.
**USER-VISIBLE "MARKETPLACE V2" (VERIFIED): 49 in source, ZERO on screen.**

## The empty state you saw was never borrowed

**BORROWED STRINGS: ZERO (VERIFIED).** Both sentences you quoted live in **exactly one file**,
`marketplace/browse/browse-client.tsx`, and appear **zero times** under marketplace-v2. **You were being
sent to the old marketplace.** `BottomNav.tsx:166` read `repointToV2 = v2Visible && !mpVisible`, so an
account that can see BOTH for real — every OWNER and every test user — failed `&& !mpVisible` and kept
its phone tab on `/marketplace/browse`. It is now simply `v2Visible`. **Nobody else is affected**: that
flag is false for the 1,748 people not on the allow-list. The three v1 components v2 imports take all
their text as props.

## What the guards and reviews caught, including my own

• **TWO OF MY OWN CHECKS FAILED TO FAIL.** R6 and R8 were presence tests where you asked for counts, and
both **passed while the demonstration was breaking them**, because those routes export two handlers and
breaking one left the other to satisfy the test. Both count per handler now. **9 of 9 cases, nothing
sampled**, each naming itself, every file restored byte for byte.
• **A CONTAINMENT CHECK FAILED AND IT WAS STALE, NOT THE PRODUCT.** It asserted zero v2 rows created,
true of three previous rounds; proving a lock requires creating one. It now asserts every v2 row created
belongs to a **sandbox** id, which is tighter.
• **THE ACCESSIBILITY REVIEW FOUND THE PREMISE FAILING AT THE MOMENT IT MATTERS.** The lock state is a
server prop and the tile row's comes from the segment layout, which the App Router does not re-render
between children. Without `router.refresh()`, a person who had just sent his first clip would still read
*this is the last moment*, and the tile would stay unlocked all session, then lead him to a locked screen
underneath a row saying he could still change. **Fixed both sides. I would not have shipped without it.**
• **THE RENDER FOUND A LEAK I HAD NOT**: "Post a clip" reached the maker account on the poster money
screen at all five widths, and chasing it found a second defect — **the money tile pointed both sides at
the MAKER's earnings page**, so a poster pressing his own money tile landed somewhere scoped to
`editorId` showing him nothing. Both fixed.
• **THE CHOOSER HAS NEVER FOCUSED ITS OWN HEADING** since BL-891: the ref was attached and the file had
no `useEffect` at all. It does now, and focuses the locked heading when locked.
• **THE "CONTINUE" BUTTON WAS DEAD** and is gone: pressing a side opens the confirmation immediately, so
it sat behind an open dialog and, when reachable, did nothing at all, silently.

## The numbers

**36 of 36 containment checks. 40 of 40 renders** as both accounts in both sides at 320, 375, 414, 1280
and 1440, URL, `innerWidth` and pan read back, **0px pan, 95 percent content to viewport**. **60 of 60
route requests refused** for four strangers, every one a 404, **zero 429**; **36 of 36 neutral titles**;
**28 of 28 page walks refused in a real browser**. **14 of 14 guards. Hooks gate 0 errors, 11 warnings.
Twelve protected money files byte-identical by blob OID**, including `marketplace-flag.ts` and
`marketplace-v2-poster.ts`. Clip and payout fingerprints identical, earnings invariant 0 violations, both
reconciliation forms clean, the BL-678 apify guard byte-identical with no actor run, sandbox torn down to
zero.

## Your walk, in order, on campaign `cmu5yeax20000h4w7yv5n387y`

1. **Account A already makes clips.** Open the marketplace from the left nav: Send a clip, Your money,
   Change what you do, and **Review clips** because you are the owner. No Post a clip tile.
2. Press **Send a clip**, pick **Marketplace test campaign**. Above the button you read *This is the last
   moment you can change sides*. Send it. **The lock falls on that press.**
3. The switch tile reads **Locked** immediately, not next session. Follow it: *You cannot change sides any
   more*, the sentence naming that you have already sent a clip in, and no choice controls at all.
4. Try the poster's side by URL: a **403** with the sentence, not a 404 and not a blank screen.
5. As owner, press **Review clips** and approve it.
6. **Account B posts clips.** Its row is Post a clip, Your money, Change what you do, with no Send a clip
   tile. Open the campaign, open the clip, read the same warning, paste the post link. **Its lock falls.**
7. **To unlock account A**: your owner account, that person's admin profile, the **Marketplace side**
   panel. It says they make clips and that 1 clip sent holds them. Write a reason, press *Set them to
   posts clips*. The audit row keeps both names, both sides, the reason and the database's own timestamp.

**ROLLBACK:** `git revert` the merge commit. The lock is derived, so there is no column to migrate back.
