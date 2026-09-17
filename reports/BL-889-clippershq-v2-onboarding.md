# BL-889: make marketplace v2 usable by fifty people who have never seen it

**NOTHING IS UNREMOVABLE. 36 of 36 recorded rows deleted, 0 remain, and the platform reconciles to the row: users 1,756 and campaigns 34, both exactly what they were before the round, clips 10,226 before and 10,226 after, payouts 249, and the payout fingerprint byte identical. Zero rows match `bl889sbx-`, zero carry the sandbox marker, zero `mkt2.` activity rows survive, and zero of the 1,756 people carry a marketplace role.** Three arrival rows the RENDER pass created after the ledger had been enumerated were found by their sandbox owned column, appended to the ledger and deleted in a second teardown rather than declared as leftovers.

**NOTHING HAS EVER RUN IN PRODUCTION AND EVERY PROOF BELOW IS A SANDBOX PROOF.** All four v2 tables hold zero rows. Measured this round and it shapes step one of the checklist: **there is not a single campaign on the platform with a marketplace type**, so a poster opening the marketplace today sees an empty campaign list until the owner changes one.

## The model split, and what is verified

The strongest model wrote every money path, every gate, every guard and this report, with no subagent between it and the source. Four retrieval subagents ran on a cheaper model: the role and capability inventory, BL-870's refusal recording, the BL-876 PART 4 and 5 journeys, and the accessibility brief. **Every load-bearing claim they returned was re-checked against source before it was used**, and the four that decided the design are marked VERIFIED below. One subagent claim was taken as READ and is flagged as such.

## PART 0: what a role would even mean here

- VERIFIED, `prisma/schema.prisma:74-81` and `:361-363`. **`users.posterStatus` already exists and is the trap.** `NONE / PENDING / APPROVED / REJECTED`, driven by an application flow with an owner review and a scheduled call: a permission somebody was GRANTED, not an activity somebody CHOSE. Writing a v2 choice into it would move a v1 permission silently.
- VERIFIED, `src/lib/auth.ts:952-975`. **The session carries exactly ten fields** and `posterStatus` is not one of them, so no existing field reaches a page without its own database read.
- VERIFIED by grep. **Nothing distinguishes the two activities today.** `submitV2Clip` takes an `editorId` parameter and `createV2Post` a `posterId`, neither checks anything about the caller, and the schema has called an editor posting his own clip deliberate since BL-877.
- READ, not independently re-derived: the subagent reports `User.trainerPromotedById` written once and never read anywhere. It is consistent with the five prior rounds and I did not re-verify it.

**A NEW FIELD IS GENUINELY NEEDED, AND IT IS A SIGNPOST.** `marketplaceV2Role`, nullable, no default, so all 1,756 existing users keep NULL and nothing about them changes. It decides which screen somebody lands on and nothing else. **RECOMMENDED AND IMPLEMENTED AS A SIGNPOST, NOT A GATE**, for three reasons: the owner's own words are that a person may switch at any time, and a thing you may switch at any time enforces nothing; a gate on the wrong person locks a real earner out on day one, refusing him over a choice he barely remembers making; and nothing in the product needs it, because the editor leg is keyed to the CLIP and the poster leg to the POST. `npm run check:v2-role-is-signpost` asserts it as **zero mentions across 13 route files and exactly one writer**, so it is a counted property rather than a promise.

## PART 1: the choice, explained before it is made

Quoted from `src/lib/marketplace-v2-copy.ts`, which imports nothing so Prisma cannot reach the browser bundle. On the way in: *"Some people are good at making clips and some people are good at getting them seen. The marketplace lets those two people work together and split the money."* and *"One person makes a clip. Other people post that clip to their own accounts. Both of them get paid every time one of those posts gets views."*

The two options read **"I make clips"** and **"I post clips"**, each with four numbered steps and the money said out loud: *"You earn 45 percent of what EVERY post of your clip makes. If ten people post it, you earn 45 percent from all ten, and that keeps going for as long as the campaign runs."* and *"You earn 45 percent of what YOUR OWN post makes. What other people's posts make does not change yours, and there is no limit on how many people can post the same clip."* Before the choice: *"Pick the one that sounds like you. You can change it any time from the menu in the top right, and changing it never affects money you have already earned."* and *"You are allowed to do both. Picking one just decides which screen you land on first, and nothing stops you doing the other thing as well."*

**THE DELIBERATE CONFIRMATION**, titled *"Set you up to post clips?"*, saying *"You will see a screen of campaigns, and inside each one the clips you can post."* and *"You can change this any time from the menu in the top right. Changing it does not affect any money you have already earned."* The buttons are *"Yes, I post clips"* and *"Not yet, let me read again"*. Initial focus is deliberately NOT on the confirm button, so nobody commits by reflex before reading the reversibility sentence.

**CHANGEABLE FROM THE TOP RIGHT**, in the account menu beside BL-852's entry, reading **"Marketplace: make clips or post clips"**, which says what it does rather than naming a setting. **SWITCHING COSTS NOTHING, AND IT IS MEASURED.** A person earned $45.00 as a poster, switched to editor, and his poster total, his editor total and **the whole platform's clip fingerprint** were identical before and after.

## PART 2: the campaign comes first

A poster now lands on campaigns, each row showing what it pays as his own 45 percent already applied, and **BL-879's three states carried up**: *"3 clips you have not posted, 1 clip you posted, 0 clips you skipped."* The campaign name is the link, so twenty rows do not read "Open" twenty times, and every number carries its own spoken unit.

**WHICH CAMPAIGNS APPEAR IS SAID ON THE SCREEN**: *"Every campaign the owner has opened to the marketplace shows up here, whether you have joined it or not. Posting a clip from a campaign adds you to that campaign automatically, so there is nothing to join first."*

**BL-876 PART 4.5 ARGUED THE OPPOSITE AND THIS ROUND OVERRULES IT DELIBERATELY.** Its words: *"platform or campaign filters as the primary axis do not address the goal at all. The question is 'what have I not posted', not 'what is on TikTok'."* That reasoning is about ordering ONE LIST of clips and it is still right; this is about navigation for fifty newcomers. **Both answers survive**: the campaign is the way in, BL-879's status tabs are untouched inside it and still default to "Not posted", and the three counts are carried up so "what have I not posted" is answerable without opening anything. The overrule is written into the code, not just here.

**AND A THIRD SILENT DIVERGENCE, THE SAME SHAPE AS BL-888's TWO.** `clipper-submit-core.ts` refuses an ordinary clip with *"You must join this campaign before submitting clips."* as its RULE 0, and **marketplace v2 contained zero references to `campaignAccount` anywhere**. A v2 poster could always earn on a campaign whose member list did not contain him and whose notifications would never reach him. **Repaired with a row and not a refusal**: posting joins him inside the same transaction, because a gate there would refuse him after he had already made and posted the video.

The editor side takes the same shape: his submissions are grouped by campaign, each group saying *"2 waiting for review, 1 reviewed."* in words.

## PART 3: the guidance, where the decision is

Four numbered steps beside the clips, not on a help page: *"Pick a clip and open it in Google Drive."*, *"Post it to one of your own approved accounts."*, *"Come straight back here and paste the link to your post."*, *"You have thirty minutes from the moment it goes live. After that the link is refused."* The editor's four sit above his own submissions. What a rejection means is next to them: *"Nothing bad. The owner writes you a reason in plain words and you can send a fixed version as a new clip. A clip that is not approved is not a mark against you and nobody else ever sees it."* Where the money shows up is stated for both. The empty campaign list says *"The owner has not opened any campaign to the marketplace yet. When he does, it will appear here. Nothing is wrong and there is nothing for you to fix."*

## PART 4: watchable

**THE TABLE ALREADY EXISTED AND WAS ALREADY GENERIC**, so this round wrapped 13 v2 handlers into BL-870's `activity_events` rather than building a second recorder: a dotted surface key, the VERBATIM sentence, no relation to `User`, fire and forget. 13 surfaces declared, all 13 wired, asserted as a count.

**PROVED TO FAIL OPEN THE WAY BL-870 PROVED IT.** The table was renamed out from under the running server for one request. With it present: `400 "Pick one of the two. Say whether you make clips or post clips."` With it gone: the same status and the same sentence, byte identical. **THE NEVER EVIDENCE RULE IS NOW IN THE DATABASE**, not only in a report. `COMMENT ON TABLE activity_events` states that no row may become evidence against anybody, reach a strike, a ban, a score, a flag, a queue or any screen implying suspicion, and that the only permitted ranking is of REASONS by distinct people, never of people. The owner's screen has no per-person column.

**ONE SCREEN, BESIDE BL-870's, on the problem reports page he already opens**: eleven funnel rows, refusal reasons ranked by distinct people with the rank as a COLUMN rather than as row order, and below a floor of five arrivals it says in words that an order between the rows means nothing at that size.

## PART 5: the guards, and what they caught

**14 prebuild guards, 15 steps in the chain, all passing**, plus the hooks gate at 0 errors and 11 warnings, at its ceiling: prisma-bypass, removed-fields, event-wiring, v2-leg-sync, v2-editor-balance, paid-is-final, payout-snapshot, css-tokens, liability-rules, v2-strike-sites, schema-drift, page-titles, v2-flag-gate, **v2-role-is-signpost (new)**.

- **BL-888's `check:v2-flag-gate` COULD BE SILENCED BY AN ORDINARY REFACTOR.** It matched only `export async function GET(`; wrapping the handlers changed the shape and it reported **thirteen routes with no handler** rather than failing on anything real. Widened: 15 handlers, 15 gate calls, 9 of 9 pages.
- **BL-888's DEMONSTRATION did not restore byte for byte** in a fresh worktree, because it read text and wrote it back, normalising CRLF to LF. It said so honestly. The new one reads and writes binary.
- **The new guard failed on its FIRST RUN against this round's own work**: `mkt2.arrive` declared and wired to nothing.
- **One of my own demonstration cases was bad and the guard was right to pass it**: S2's first version added a comment inside the one writer's own file, which creates no second writer.

All 8 checks across both guards then failed one at a time, never sampled, each naming itself in its FAILURE list rather than anywhere in its output, every file restored byte for byte and re-verified clean.

## PART 6: what was run and what it said

- **THE PROOF: 49 passed, 0 failed.** Run 1 crashed on a missing `profileLink` in my own fixture, which was my script and not the product.
- **THE RENDERS: 25 of 25, first pass**, five surfaces at 320, 375, 414, 1280 and 1440 against a production build with `DEV_AUTH_BYPASS=false` and a real minted cookie. **Pan measured, not `scrollWidth`: 0 pixels at every width.** URL read back, one `h1` each, 5 distinct titles, 0 dangling `aria-controls`, 0 duplicate ids, 0 controls white on accent, 0 unscoped table headers, 0 `var(--bg-page)`, and a real clipper refused on every one.
- **THE MONEY:** all three legs paid and summing to the cent, $45.00 + $45.00 + $10.00 against a $100.00 gross with 100,000 views actually landed. All nine protected money files **byte identical by blob OID**. Earnings invariant 0 violations across the full population, no negative money, one editor leg per clip, every v2 clip stamped, none wrongly flagged. Both reconciliation forms 0 leaks and 0 out of balance, before and after.
- **THE BUILD:** one failure first, a type error in my own sandbox script, and **the task runner reported exit 0 while the log said the build worker exited 1**. The log is the truth and that is why the exit code is echoed from a file rather than trusted from a pipe.

## What is NOT in this round

**THE REFERRAL PERCENTAGE IS RECORDED AND NOT BUILT.** It is a new money flow between a third party and an earner, which is the trainer system's exact shape, and that needed a design round, a build round and a third round to add a cashout nobody had noticed was missing. It needs its own design round answering at minimum whether the share comes out of the earner's 45 percent or is additional, whether it applies to both legs or one, whether it is forever, what happens when the referrer is banned or is himself the editor, and where he withdraws it. Hours before launch is the wrong time.

Also still open from BL-888, unchanged: the L1 budget lock sees only the poster's 45 percent on non tick writers; a conversion prices both parties with zero bonuses; the clipper is never told he was warned; the theft comparison surface has no door; the editor is invisible on the owner's clips list; 11 serious accessibility items with line numbers in BACKLOG.md.

---

# THE OWNER'S OPENING CHECKLIST, REWRITTEN FOR WHAT THIS ROUND CHANGED

**What is different from BL-888's briefing: there is a door now, the role choice exists, campaigns come before clips, every screen explains itself, and you can watch all of it.**

**HOW TO OPEN IT, IN ORDER, WITH WHAT YOU SHOULD SEE AFTER EACH STEP.**

1. **Set one campaign's type to "Two ways to earn".** Measured today: **you have zero campaigns with a marketplace type**, so until you do this the marketplace is an empty room. After: the campaign card on the campaigns page carries the badge "Two ways to earn".
2. **Open `/marketplace-v2` as yourself.** You should see "What the marketplace is", then "Which one are you?", then the two options with 45 percent stated on each. Pick one, read the confirmation, confirm. After: you land on that role's screen, and the account menu in the top right now reads "Marketplace: make clips or post clips".
3. **As a poster, check the campaign list.** You should see your campaign, what it pays you per 1,000 views, and "0 clips you have not posted" because nothing is approved yet. If you see "No campaigns yet", step 1 did not take.
4. **Mark ONE editor and TWO posters as test users and send them the link.** Two posters, not one, because two people earning from the same clip at once is the thing most worth watching. They will see exactly what you saw at step 2.
5. **Watch for a full day before widening.** Then set `NEXT_PUBLIC_MARKETPLACE_ENABLED` to true when you want everybody in. That one switch is the whole opening.

**WHAT TO WATCH ON DAY ONE, AND WHERE.** Open **`/admin/problem-reports`** and scroll to "The marketplace, and where people stopped". It tells you how many arrived, how many chose and which, how many editors sent a clip, how many were approved or not, and how many posters posted. Underneath, **"Which rules refused people", ranked by how many different people hit each one**. A rule refusing many people is a design problem, not many mistakes. Below five arrivals the screen tells you itself that an order between the rows means nothing. Separately, watch that **every post produces three legs** and watch **the campaign budget** rather than the clip count, because one popular clip with fifty posters spends quickly.

**WHAT TO SEND YOUR FIRST EDITORS.** "Go to the marketplace and pick 'I make clips'. You make a clip, put it in Google Drive, and send me the link through the site. If I approve it, anybody on that campaign can post it, and **you earn 45 percent of what every one of those posts makes, from all of them, for as long as the campaign runs**. You do not post it yourself and you do not need any accounts. If I do not approve one you get a reason in writing and you can send a fixed version."

**WHAT TO SEND YOUR FIRST POSTERS.** "Go to the marketplace and pick 'I post clips'. You will see campaigns; open one and you will see clips other people made. Pick one, open it in Drive, post it to your own account, then come straight back and paste the link. **You earn 45 percent of what your own post makes**, and what other people's posts make does not change yours. **You have thirty minutes from the moment your post goes live to paste the link.** Post it to your own account only."

**HOW TO CLOSE IT AGAIN, FASTEST FIRST, AND WHAT HAPPENS TO MONEY.**

1. **Everybody at once:** set `NEXT_PUBLIC_MARKETPLACE_ENABLED` back to false. Every v2 screen and every v2 route answers "not found" for everyone except you and test users. **No data is touched and every cent already earned stays exactly where it is.**
2. **One campaign:** change its type back to "Normal". Nobody can start a new post on it from that moment, and **everything already posted keeps earning to the end of the campaign**. That was BL-888's answer to the open question and it is unchanged.
3. **One person:** issue a strike. Three inside ninety days bans him from ordinary posting for seven days, it is reversible, and **his money stays his**. Be aware of the standing gap: **he is not currently told**, so tell him yourself.
4. **The code:** `git revert` the merge commit. The two new columns and the table comments stay behind harmlessly; the rollback SQL is printed at the top of `scripts/migrations/BL-889-marketplace-v2-role.sql`.

**THE ONE THING I WOULD NOT DO, unchanged from BL-888 and now with a third example behind it.** Do not open this to everybody on the same day you open it to anybody. Three silent divergences have now been found in three rounds, all the same shape: a rule that existed on one path and not on the other, invisible from the screens. Let three people find the fourth before three hundred do.
