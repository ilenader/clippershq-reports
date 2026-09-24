# BL-931 — the locked "Change what you do" tile: its second line is gone, the lock is not

**Shipped 2026-09-24.** Branch `checkpoint/BL-931` (4e045633), merged to main as a5e26b20.
Rollback: `git reset --hard pre-merge-BL-931`, or `git revert -m 1 a5e26b20`.

**Tile heights (tile 1 / 2 / 3), maker and poster alike.** Before, locked: 69.5 / 69.5 / 103.8 at 320, 69.5 / 69.5 / 88.6 at 375 and 414, all three 88.6 at 1280 and 1440. After: 69.5 / 69.5 / 69.5 at every width. Unlocked people were already 69.5 everywhere.

## 1. What was removed, counted

The sentence "Locked. Open this to see why, and how to ask the owner." came from ONE source and had ONE emission point:
* **Family 1, the text.** The constant `V2_SWITCH_LOCKED_LINE` in `src/lib/marketplace-v2-copy.ts`.
* **Family 2, the renderer.** The ternary in `src/components/marketplace-v2/V2Nav.tsx` that printed it in the tile's second line when `locked` was true.
* `grep -c` over `src` before: 1 definition, 1 import and 1 use of the constant, and the sentence in 1 file. After: **0 files** with the sentence and **0** with `V2_SWITCH_LOCKED_LINE`.
* No other surface printed it. The phone and desktop layouts share the same component, so one removal covers both.

## 2. The lock stays, and where the explanation lives

* The lock is decided by `getV2RoleLock` (`src/lib/marketplace-v2-side.ts`) from real rows: held clips for a maker, posts for a poster. This round did not touch it.
* The tile is still a working link to `/market?change=1`. That screen (`src/app/(app)/marketplace-v2/arrive-client.tsx`, section `#v2-locked`) shows:
  * the heading "You cannot change sides any more";
  * the reason in words;
  * "If you need it changed, ask the owner: he can change it for you, and he records why."
* Focus moves to that heading when the screen opens.
* **Proven as a maker AND as a poster, locked, at all five widths (20 of 20).** Pressing the tile landed on `/market?change=1` with that heading, the "ask the owner" text present and focus on the heading.

## 3. Render (BL-793 method; production builds, before = main, after = branch)

* **Method.** Four sandbox people: maker locked, maker free, poster locked, poster free. Each was checked at 320, 375, 414, 1280 and 1440.
* **Readback.** `innerWidth` read back equals the width every time. The URL is `/market/editor` for makers and `/market/campaigns` for posters. Pan measured by scrolling the document and `<main>` sideways: 0 in all 40 renders. No install sheet appeared.
* **Level alignment.** After the change, the icon top sits at 13 px and the label top at 37 px in every tile of every render.
* **Before.** Only the locked tile was different: it grew to 103.8 px at 320 and 88.6 px elsewhere. On desktop the grid stretched its neighbours to match, so the whole row was 88.6 px.

| person | 320 | 375 | 414 | 1280 | 1440 |
|---|---|---|---|---|---|
| maker locked, before | 69.5/69.5/103.8 | 69.5/69.5/88.6 | 69.5/69.5/88.6 | 88.6 x3 | 88.6 x3 |
| poster locked, before | 69.5/69.5/103.8 | 69.5/69.5/88.6 | 69.5/69.5/88.6 | 88.6 x3 | 88.6 x3 |
| every person, after | 69.5 x3 | 69.5 x3 | 69.5 x3 | 69.5 x3 | 69.5 x3 |

**Finding.** Maker and poster behave the same. The tall tile follows the LOCK, not the side. A poster who holds a post has the same row as a locked maker, so the owner's "as a poster too" was a locked poster.

## 4. Accessibility

* **Name.** The locked state is carried in the link's name: an sr-only ", locked" follows the visible label.
  * Chrome's tree reads "Change what you do , locked". The sr-only span is absolutely positioned, which puts a space before the comma. Screen readers do not speak that space.
  * The visible label comes first, so voice control by "Change what you do" still works (2.5.3).
  * A description was not used, because VoiceOver on iOS drops descriptions when swiping.
  * An unlocked tile's name stays exactly "Change what you do" (match 1 in all 10 renders).
* **Keyboard.** The locked tile is reachable by Tab in every render. Its focus ring is a solid 2 px outline plus a shadow.
* **Target size.** The tile is 256 to 379 px wide and 70 px tall, so every target is at least 44 px.
* **Tab order.** Nothing was removed from it. The removed span was never focusable, and the tile count is 3 before and after.
  * The Tab count to reach the tile was identical in 18 of 20 cases.
  * At 320 the locked maker went 16 to 15 and the locked poster 12 to 13. The two moved in opposite directions, so this is page timing, not this change.
* **Review.** The accessibility-lead review found nothing blocking. 1.3.1 passes (the state is available to software), and 1.4.1 and 3.3.2 do not apply.

## 5. Found, not built (BACKLOG BL-931)

1. **The request form does not exist.** The BL-902 route `/api/marketplace-v2/side-request` has zero callers in any `.tsx`. The locked screen says "ask the owner", but there is no in-app way to ask. Decide whether to build the form or drop the route.
2. **The owner's own row is uneven.** Overview and Review still carry a visible second line, so the owner's five tiles are uneven in the same way.
3. **Optional (a11y review).** When locked, show lucide `Lock` as the switch tile's icon (aria-hidden). Sighted people would then get a cue before pressing, with no added height. This is a design call for the owner.

## 6. Safety

* **Money files.** The 6 files are byte-identical by blob OID (`git rev-parse pre-BL-931:<path>` equals `git hash-object`):
  * `clip-earnings-writer` 80418a18
  * `earnings-calc` 00410634
  * `balance` 67c30c89
  * `tracking` 672d2ab3
  * `clip-earnings-invariant-middleware` 61cef393
  * `money-decimal` ef5cdae7

  `tracking.ts` is not in the diff. The diff is 2 source files, BACKLOG and 4 sandbox scripts.
* **Guards.** All 22 prebuild guards pass. The hooks gate reports 0 errors and 10 warnings (limit 11).
* **tsc and builds.** The tsc baseline was clean (exit 0) before and after. `BUILD_EXIT=0` on the before build, the after build and build 2. The merge tree OID (a7ea220e) equals the branch tree OID, so build 2 is the merge build.
* **Sandbox.** Every row was prefixed `bl931sbx-` and ledgered, and all were torn down: 4 users, 1 test campaign, 1 v2 clip, 1 account, 1 clip, 1 post, 24 activity rows and 4 lifecycle rows.
  * A sweep of 341 id columns found 0 remaining.
  * The closing snapshot equals the opening one: users 1794, campaigns 37, v2 clips 33, v2 posts 53, clip accounts 1547, rules seen 7, with identical id and status fingerprints. No real row was written.
* **Vendors.** No vendor call was made and no Apify actor was run. The visited marketplace pages mount no thumbnail or vendor component, and the server logs show no vendor lines. At most one DB connection was held at a time.
* **Git.**
  * Push: branch and main pushed with `safe-push`, VERIFIED (origin equals local).
  * Tags: `pre-BL-931`, `post-BL-931`, `pre-merge-BL-931`, `post-merge-BL-931`.
  * `checkpoint/BL-723` is not an ancestor of main before or after.
  * BACKLOG went from 237 to 238 entries.
* **Cleanup.** The worktree `C:\w\b931` was removed and pruned, and `ls` confirms it is gone. The leftover sweep dry run found 0 MB to reclaim. Servers were stopped by PID.
