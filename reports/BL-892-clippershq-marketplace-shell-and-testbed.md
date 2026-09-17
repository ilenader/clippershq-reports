# BL-892 — the marketplace takes the first marketplace's shape, and you get a campaign to test on

**YOU CAN WALK THE WHOLE LOOP TONIGHT.** One campaign is open to the marketplace now, id
`cmu5yeax20000h4w7yv5n387y`, and it is a TEST campaign from the instant it existed: `isTestCampaign:
true` is in the CREATE and never a later update, so the window in which a real clipper could have seen
it is **zero seconds**. One row, nothing else: **0 clips, 0 memberships, 0 marketplace clips, 0 agency
rows**, and neither of your accounts was written to. It takes TikTok, Instagram and YouTube, the three
both accounts hold approved accounts on. Remove it with one statement,
`DELETE FROM campaigns WHERE id = 'cmu5yeax20000h4w7yv5n387y';` — every table holding a `campaignId`
either cascades from that or nulls its reference, so no foreign key can block it.

**YOU CANNOT WITHDRAW FROM IT, AND THAT IS CORRECT.** `api/payouts/route.ts:601` answers a typed
`CAMPAIGN_IS_TEST`. **The second half would have looked like a bug**: the marketplace earnings screen
ALSO excludes test campaigns entirely, so the number stays at **$0.00** however many views land. That
is the rule the ordinary earnings page has followed for rounds. The submit form says both now, at the
moment you pick the campaign.

## The shell you asked for

You put the first marketplace's landing page on screen and asked for that shape. It is a **segment
layout** there, not a page, so the panel and tiles persist across every tab; ours does the same. A
**collapsible "What the marketplace is" panel** that remembers being folded, a **row of four large
tiles** (five for an OWNER), then the work, a filter, and listings with an honest empty state per
filter. **THE STRUCTURE WAS COPIED AND NOT ONE STRING WAS.** Their panel says sixty and thirty percent because
those are ITS numbers; ours is forty five and forty five. `V2Explainer.tsx` **contains no percentage
literal at all** — every sentence comes from the copy file, where it has said forty five since BL-889,
so there is no path by which the wrong number could reach that screen. The platform's own cut is not
on the panel, for the same reason the first marketplace never shows a clipper its ten percent.

**THE MONEY IS A TILE ON EVERY SCREEN NOW.** It used to be an underlined sentence on one screen, so a poster reading his own page had no route to it. The render pass asserts the tile's words are on all five screens at all five widths, as both accounts.

## The URL swap: costed, not done, and here is the bill

**About 45 files need a real edit**, on top of the 94 that merely relocate. Three items make it a round
of its own. **Both v2 guard scripts hardcode the directory names and run in `prebuild`**, so a rename
without them fails the BL-348 hooks gate on the next commit. **`bl890-containment.ts` and
`bl891-containment.ts` carry 52 hardcoded route literals** encoding the last two rounds' entire
containment proof, and a rename would **silently invalidate that proof** rather than break a build,
which is the worse of the two. And **`app-layout.tsx` matches `startsWith("/marketplace")` with no
boundary check**, the only reason these routes get the full viewport today; the first marketplace has
an `error.tsx` and this one does not, so whichever tree lands at `/marketplace` needs one written.

**You lose nothing by waiting**: you reach it from the left navigation, not by typing a URL. Swept and
counted again: **49 occurrences of "marketplace v2" across 34 files, ZERO in text a person can see.**

## The rest of what you named

• **THE RETURN IS THE EASY PART NOW.** A returning poster gets "You already opened this one" first,
with one button that puts the cursor in the paste field. The flag is **server side**,
`marketplace_v2_poster_states.inProgressAt`, not `localStorage`, so it survives a cold load on another
device. It had been in that screen's payload since BL-879 and **never once read**.
• **WHICH PLATFORMS A CAMPAIGN ACCEPTS is said before you leave for Drive.** It was enforced silently,
so a poster could download, post, come back, and find his account simply absent from the dropdown.
• **THE THIRTY MINUTES RUNS FROM THE POST GOING LIVE**, not from the Drive tap. `clip-freshness.ts`
compares `Date.now()` against the timestamp the platform itself reports and **never reads
`inProgressAt`** (0 references). The screen now also says what missing it does not cost.
• **WHAT SWITCHING DOES is answered on screen.** Not an assertion: `check:v2-role-is-signpost` asserts
**zero** route files read the role, so nothing can be hidden by it.
• **THE MENU ENTRY IS ONE LINE, MEASURED.** "Make clips or post clips" at `innerWidth=320`, menu
**224px** (it is `w-56`, fixed at every width, so the wrap was never about the viewport), box
**222×36px**, line height 19.5px, padding 8px. The old string was 37 characters and could not fit the
176px the menu leaves for text.
• **"ONLY CAMPAIGNS YOU ARE IN" IS NOT WHAT THE CODE DOES**, and the shipped copy says so. BL-889
decided joining happens at POST time, and filtering to joined campaigns would show **every one of your
fifty newcomers an empty marketplace**. Left as built.

## What the guards caught, including this round's own

• **G5 COULD NOT SEE A TEMPLATE LITERAL.** BL-891 widened it to `href[=:]` and stopped; the class after
it cannot cross a backtick, so ``href={`/marketplace-v2/...`}`` never matched.
• **AND ITS SKIP RULE WAS A SUBSTRING THAT SWALLOWED A DIRECTORY.** `includes("/marketplace-v2/")` was
written to mean "a v2 screen" and also matched `src/components/marketplace-v2/`, where this round put a
tile row rendering **five links and calling no gate**. It is correct only because the gated layout is
the one thing that renders it, so **G8 now checks that claim** rather than assuming it.
• **15 of 15 demonstration cases passed**, each naming itself in its failure list, every file restored
byte for byte, all three link shapes broken separately rather than inferred from the first.
• **MY OWN CHECK FAILED FIRST AND THE PRODUCT WAS RIGHT.** The containment proof asserted ZERO
campaigns were open to the marketplace, true last round and exactly what this round was asked to
change. Corrected to something tighter: exactly one, and it must be a TEST campaign. **27 of 27 after.**
• **MPFILTERPILLS WAS SHIPPING A MEASURED AA FAILURE** and this round was about to put it on a new
screen: white on the accent fill is **3.40:1** against a 4.5 requirement, its count **2.72:1** while
carrying real information. BL-891 measured this exact pair and fixed it in one file while the shared
component kept shipping it. One token, selected state only: **5.86:1**, four other call sites improved.
• **THE DESTROYER REFUSED, AND THAT IS THE LOCK WORKING.** It will not delete from a real account by
pattern, so those rows went by explicit list, and the cutoff earned its keep: thirteen ids were in the
ledger and only **six** were mine, because arrivals dedupe per hour. **Seven were refused as yours**,
including your 18:57:08 visit and a second at 19:31.

## The numbers

**50 of 50 renders** as BOTH accounts at 320, 375, 414, 1280 and 1440, URL, `innerWidth` and the pan
read back, **0px pan everywhere**, **95% content to viewport** at 1280 and 1440. **60 of 60 route
requests refused** for four kinds of stranger, every one a 404, **zero 429**. **36 of 36 neutral tab
titles. 28 of 28 page walks refused in a real browser**, now checking the shell's words too, because a
layout drawing chrome around a 404 leaks everything the page refused. **27 of 27 containment checks.
14 of 14 guards. Hooks gate 0 errors, 11 warnings. Eleven protected money files byte-identical,
including `marketplace-flag.ts` itself**: no gate, no permission and no arithmetic moved. Clip
fingerprint identical across 10,227 clips, payouts 249 to 249, earnings invariant 0 violations, both
reconciliation forms clean, the BL-678 apify guard file byte-identical with no actor run, and the
sandbox torn down at **48 of 48 rows deleted, 0 remaining, 0 rows matching `bl892sbx-`**.

**ROLLBACK:** `git revert` the merge commit, then
`DELETE FROM campaigns WHERE id = 'cmu5yeax20000h4w7yv5n387y';`
