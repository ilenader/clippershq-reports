# BL-891: the marketplace moves to the left navigation, loses the word v2, and uses the screen

**HE USED IT HIMSELF DURING THIS ROUND, AND THAT IS THE HEADLINE.** At **18:57:08** the allow-listed account chose **"I make clips"**. That is before this round's server existed and in a window when nothing automated was running against production as him, so it is his own hand: **the first human use of marketplace v2 in its history**, and proof BL-890's grant works end to end. Everything below is built on a feature that a real person has now actually opened.

**NOTHING IS UNREMOVABLE.** 90 of 90 ledger rows deleted and 0 remain; the lock then refused 18 more because their owner column held a REAL id, which is it working as designed, and those were removed by an explicit list of 20 ids. **The three activity rows from his own 18:57 visit were deliberately left alone: they are his.** Zero rows match `bl891sbx-`, the payout fingerprint is identical, the earnings invariant is 0 across 10,227 clips, and all 14 prebuild guards pass with the hooks gate at 0 errors and 11 warnings.

**THE MODEL SPLIT.** Six design reviews ran in parallel on a cheaper model, **one per surface rather than one shared aesthetic opinion**: the door and role chooser, the campaign list with the clip catalogue, the editor's submit form, the editor's list with both money screens, and the owner's queue with the compare screen. Two more cheap agents did the navigation and naming inventory and the width inventory. **The strongest model decided the placement, wrote every line touching the gate, wrote both guard changes, verified every gate afterwards and wrote this report.** Their findings were RECONCILED, not averaged: where two reviewers disagreed about the Drive disclosure being open or closed, one flagged the conflict with the round that specified it and I kept it closed. Every load-bearing number below was re-measured by me; claims I took on trust are marked READ.

## PART 1: the left navigation

**IT IS UNDER CLIPS, WHERE HE ASKED FOR IT**, and on the phone bar too, because a desktop-only entry is invisible to half the people. VERIFIED by rendering, not by reading: **the allow-listed account sees 2 marketplace links on an ordinary page; an ordinary clipper, a reviewer and a non-owner admin each see 0.**

**BOTH ENTRIES ASK THE SAME HELPER EVERY PAGE AND ROUTE ASKS.** VERIFIED at `sidebar.tsx` and `BottomNav.tsx`: each already carried a hand-written copy of the FIRST marketplace's rule (the second and third such copies), and this round added **no fourth**. The user id is plumbed from the shell exactly as `isTestUser` already was, so the navigation can ask the allow-list question instead of guessing at it.

**THE NAME COLLIDED WITH THE FIRST MARKETPLACE AND NOTHING WAS RENAMED TO SOLVE IT.** For an ordinary clipper the existing "Marketplace" entry is a **coming soon teaser** pointing at a page the first marketplace will not open for him, so there was nothing to collide with and the entry simply becomes the real destination. For the handful who can reach both for real (three OWNER accounts and test users) the first marketplace keeps its href, icon, position and behaviour and is told apart **in words** as "Marketplace (first version)". Two identical labels in one list is its own confusion and gives a screen reader two indistinguishable landmarks.

**THE ACCOUNT MENU ENTRY STAYS, and here is why it is not a second door to one room.** They go to different places and say so: the navigation entry reads **"Marketplace"** and lands him where he belongs; the menu entry reads **"Marketplace: make clips or post clips"** and carries `?change=1`, which is the documented way back to the chooser. One is "go there", the other is "change what you are", which is the thing he asked to be able to do from the top right.

**THE PHONE BAR HAS FIVE SLOTS AND A SIXTH CROWDS 320 PIXELS**, so the existing Marketplace tab is repointed rather than a tab added. Test users and owners, who can reach the first marketplace for real, keep their tab exactly as it was and reach the new marketplace from the sidebar, which the mobile drawer renders in full.

## PART 2: the name

**NOTHING A PERSON CAN SEE SAYS v2.** A counted sweep found **nine user-visible occurrences**, every one on an OWNER-only screen (`/admin/liability` and `/admin/payouts`), which is exactly why they survived the discipline BL-889 and BL-890 applied everywhere a clipper can reach. All nine changed to "marketplace editor". The final count of user-visible occurrences across all of `src`, excluding comments and generated Prisma code, is **zero**; the two remaining hits are a JSX comment and a block comment, neither of which renders.

**URLS AND FILE NAMES ARE DELIBERATELY UNTOUCHED.** `/marketplace-v2` stays. Changing a route would break BL-890's containment proof, every link into the feature and the gate's own path matching, and a path is not a label. **Comments still say v2 on purpose**, because that is how the next reader knows which of the two marketplaces a line is about.

**THE FIRST MARKETPLACE IS NOT BROKEN AND NOT RENAMED.** VERIFIED by grep and by rendering: `sidebar.tsx`'s `marketplaceNavItem` and `BottomNav.tsx`'s `TABS_CLIPPER` entry are byte-identical to what shipped, both still labelled "Marketplace", both still pointing at `/marketplace`, and the 35 files reading the shared gate for v1 are untouched. The one and only change visible to a v1 user is that somebody who can reach BOTH sees the older one qualified in words.

## PART 3: the role chooser

**309 WORDS TO ABOUT 105 ON THE DECIDING SCREEN.** The measured before is 309 words for a first-time visitor, of which the two supporting cards were 176, or 64 percent of everything between the question and the answer. **Those 176 words were not deleted**: they moved into the confirmation dialog, where "what happens next" is worth reading, instead of sitting between the buttons and the button that commits. Individually: what the marketplace is, 56 words to 22; the reassurance, 30 to 13; the both-note, 26 to 13.

**THE TWO CHOICES ARE THE SCREEN NOW.** The reason he read it twice was structural, not verbal: the two buttons and the two paragraphs explaining them were **the same kind of object**, bordered cards of similar height, so nothing said which to press. Now: a 180 pixel minimum height rising to 220, a 40 pixel icon, a `text-2xl` label, a two pixel border at rest and a full accent fill when chosen, in their own band with `gap-6` and nothing between the question and the answer.

**PROMINENCE COMES FROM SIZE, FILL, SPACING AND POSITION, NOT COLOUR**, because all three text tokens on this platform render white and the marketplace's own focus rings were once measured at 1.54 and 1.69 to 1. **The number is on the button**: "Earn 45% of every post of your clip." It used to live in a paragraph below, so a person had to leave the control to find the reason to press it. **Text on the accent fill is `--bg-primary`, measured at 5.72:1**; white on the same fill is 3.43:1 and fails. The render asserts **zero** controls anywhere painting white on accent.

**THE DELIBERATE CONFIRMATION AND THE CHANGEABLE LINE BOTH STAY.** The reassurance is now the first thing in the dialog, which matters because `initialFocusRef` is omitted on purpose so focus lands on the panel and a person reads that this is reversible before he can commit by reflex.

## PART 4: the width

**MEASURED FIRST.** At a 1440 viewport the shell gives a page **1152 pixels**: 1440 minus the fixed 240 pixel sidebar minus 24 pixels of padding each side. Marketplace routes are **already exempt** from the platform's own `max-w-7xl` fallback, so the only thing narrowing them was each screen's own wrapper, and there were **seven different caps across eight screens**. Every other area of this platform (payouts, clips, campaigns, liability) uses a bare `space-y-6` with **no cap at all**.

| screen | before | of 1152 | after |
| --- | --- | --- | --- |
| the door and role chooser | 768 | 67% | 1024, and the width spent on bigger buttons |
| campaign list | 896 | 78% | house width, no cap |
| clip catalogue | 1024 | 89% | house width, no cap, plus a fourth column at 2xl |
| editor's list | 896 | 78% | house width, no cap |
| owner's queue | 1024 | 89% | house width, no cap |
| the post form | 672 | 58% | 896, a measure kept and widened |
| both money screens | 1152 | 100% | unchanged, already exact |

**IT IS NOT A max-width DELETION.** Lists and grids took the house treatment; the two reading surfaces kept a measure and were widened, because a 1152 pixel line of prose is scanned and lost rather than read. **The clip grid gained a fourth column at 2xl** rather than wider cards, matching the platform's own campaign grid, because a clip card carries a thumbnail, a title, a rate and one action and gains nothing from extra width. **The money tables stay tables everywhere**: a card carries the across reconciliation and cannot carry the down one, and reading down a column is the act of checking the sum.

**MEASURED AFTER, ACROSS TEN SHOTS AT 1280 AND 1440: 94 percent content-to-viewport**, with the door itself at 95 and 96 percent against 67 before. **The pan was measured, never `scrollWidth`: 0 pixels on all 25 shots**, because BL-883 measured a real 582 pixel pan this shell's own clipping had hidden.

## PART 5: the other screens

Six reviews, one per surface. **The editor's submit form, which he named, was missing four things and none was decoration**: what a good clip is, what happens after he presses send, how long that takes, and what he earns. All four ship. **The approval time is deliberately not promised**: the platform measures a real review time but measures it over the ORDINARY clip table, which a marketplace clip is not in, so no measurement of this queue exists. Copying the twenty four to forty eight hours promised elsewhere would be inventing a number, so it says "There is no fixed clock. He reviews these by hand, so it takes as long as it takes." **The closed-by-default Drive disclosure was confirmed present, closed and correct, and one reviewer's proposal to open it was declined** because an earlier round specified it closed; the conflict was flagged rather than silently overridden. Elsewhere: the poster's four steps became three with every promise kept, and the empty states were shortened while keeping the "Nothing is wrong" reassurance, because he has already been frustrated once by an empty marketplace reading as a broken one.

**WHAT WAS DELIBERATELY NOT TAKEN**, with reasons, all named in BACKLOG.md: the queue's list-beside-detail split and the compare screen's two-column layout, which change how a decision is made rather than how it looks; the editor list's guidance behind a disclosure, which trades his "explain everything" instruction against his "too much text" one and is his call; and moving the money screens' tiles beside their tables.

## PART 6: no gate and no money moved

- **CONTAINMENT RE-PROVED BY DIRECT REQUEST**, exactly as BL-890 did it: an ordinary clipper, a REVIEWER, a non-owner ADMIN and a signed-out visitor, each with his own account, **refused on 15 of 15 v2 API routes, 60 of 60 requests, zero answered 429**, every refusal a 404 and never a 403. **25 of 25 containment checks passed.**
- **AND IN A REAL BROWSER**, because a page cannot be judged over plain fetch on this app: **all four strangers refused on 7 of 7 pages**, seeing none of the screens' words and **no title naming the feature**.
- **THE ALLOW-LIST IS UNCHANGED**: one id, and nine malformed, missing and near-miss shapes still all refused.
- **Every protected money file byte-identical by blob OID**, ten of them, against the pre-round commit. Schema untouched. **No clip, payout or earning row touched**; payout fingerprint identical; earnings invariant 0 violations across the full population; no negative money; one editor leg per clip; **both reconciliation forms clean before and after**.
- **14 prebuild guards, 15 chain steps, all passing.** Hooks gate 0 errors, 11 warnings, at its ceiling.
- **G5 COULD NOT SEE A NAVIGATION ENTRY, and that is the guard finding of this round.** The check BL-890 wrote to catch exactly this defect matched only an href ATTRIBUTE. The navigation declares entries as DATA, `href: "/marketplace-v2"`, so when this round put the marketplace into the sidebar and the phone bar it still reported ONE linking file and **passed**. It matches both shapes now: 3 linking files, 3 gated. A twelfth demonstration case covers that shape, and **all twelve checks across both guards were demonstrated failing one at a time**, each naming itself, every file restored byte for byte.
- **TWO OF MY OWN CHECKS WERE WRONG AND THE PRODUCT WAS RIGHT.** The containment asserted he had no marketplace role, which was a stale snapshot of the previous round rather than a defect. The render asked for `/marketplace-v2` and found it redirecting to his editor screen on all five widths, which is **his own requirement met**, and the chooser had to be photographed through `?change=1`.

---

# WHAT TO DO AND WHAT YOU WILL SEE

1. **Redeploy.** Nothing else needs flipping. Leave `NEXT_PUBLIC_MARKETPLACE_ENABLED` alone.
2. **Sign in as your clipper account.** Look at the **left navigation**: there is now a **Marketplace** entry directly under Clips. Nobody else on the platform can see it. On a phone it is the Marketplace tab in the bottom bar.
3. **Click it.** Because you have already chosen "I make clips", it takes you straight to **Clips you sent**, which is what you asked for: the chooser if you have not chosen, the marketplace if you have.
4. **To see the chooser again**, use the account menu entry in the top right, "Marketplace: make clips or post clips". Two big buttons, each saying what you do and what you earn, and a confirmation that says you can change it any time.
5. **Expect the screens to be empty, because they still are.** **All 34 campaigns are still "Normal"** and there is nothing marketplace can show until that changes. The campaign list will say "Nothing is wrong. The owner has not opened a campaign to the marketplace yet."
6. **To make it show something:** open one of the two campaigns that are actually live, set its type to **"Two ways to earn"**, and reload. It appears in the campaign list with what it pays.
7. **Then send a clip.** Press "Send a clip" on Clips you sent. The form now tells you what a good clip is, what you earn, what happens after you send it, and honestly that there is no fixed clock on approval. Approve it from your **owner** account, then post it from your clipper account.
8. **If anything still looks wrong, it is worth saying so:** six separate design reviews ran on these screens and each proposed more than shipped, so there is a queue of named, reasoned improvements waiting rather than a blank page.
