# BL-803 — the merged code IS live. The deploy worked. The owner is looking at surfaces his own account cannot show him.

**2026-08-13 · DB `now()` = `2026-08-13 12:10:36.371016+00` (first read) to `12:11:47.167467+00` (last) · AUDIT, READ ONLY.**
Nothing was deployed, pushed, changed or written. `origin/main` was not moved. Worktree `C:/b803`, short path, `node_modules` never junctioned, removed at the end. Every database read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted, no wallet address read or printed.

## THE VERDICT, IN ONE LINE

> **The live site IS running the merged code.** Proven from the live site itself, not from the repository: the production CSS bundle carries the `--border-strong` token that exists only in the merged chain, the production JavaScript carries eight strings that exist only in the merged chain, the three routes BL-797 added answer as routes that exist, and the live build artifact was compiled **six minutes and twenty-seven seconds after main's tip commit**. **There is no deploy problem, no failing build and no missing table.** What is missing is a place to look: **almost everything shipped is clipper-facing or reviewer-only, and the owner's own account cannot render it.**

## PART 1 — WHAT IS DEPLOYED VERSUS WHAT IS ON MAIN

**`origin/main` tip: `d004b396199b7f1c22b8498e44ea845f3832ff7c`**, committed **`2026-08-13T00:31:40+02:00`**, which is **`2026-08-12 22:31:40` UTC**. It is a documentation-only commit: `git diff --name-only 5f6fbd62 d004b396 -- src prisma package.json` returns **0 files**, so it compiles to exactly the same output as `5f6fbd62`, the BL-797 merge and the last source-bearing commit on main. **Nothing has been pushed since.**

**The live build's identity, taken from the live site.** A production JavaScript chunk answers with a real file timestamp:

```
GET https://clipershq.com/_next/static/chunks/06eodeuyp85sp.js
  last-modified: Wed, 12 Aug 2026 22:38:07 GMT
  cache-control: public, max-age=31536000, immutable
  server: railway-hikari   x-railway-edge: ams1
```

**22:38:07 UTC is 6 minutes 27 seconds after main's tip commit at 22:31:40 UTC.** That alone dates the build to the tip, and the content confirms it.

**The decisive content proof, public and unauthenticated.** BL-797 added an additive CSS token that does not exist anywhere before the chain (`git show 72f05cec:src/app/globals.css | grep -c border-strong` returns **0**; on main it returns **3**). The live stylesheet carries it:

```
GET https://clipershq.com/_next/static/chunks/0.~t6qwwc-_a8.css   HTTP 200, 235,386 bytes
  --border-strong:#6b6b73        (dark theme)
  --border-strong:#8a8a93        (light theme)
```

**So live is main's current tip.** The one honest caveat, stated rather than glossed: because `d004b396` and `5f6fbd62` produce byte-identical build input, the live artifact cannot be told apart from either, and it does not matter, since they differ only by a markdown file. **What would settle the exact SHA is the Railway dashboard: Deployments, the active deployment's commit hash.** I did not have dashboard access and did not guess.

## PART 2 — EACH SHIPPED CHANGE, CHECKED INDIVIDUALLY ON THE LIVE SITE

Method: every string below was verified **absent from `72f05cec`** (main before the chain) and **present on `d004b396`**, then searched inside the JavaScript and CSS bundles **downloaded from clipershq.com**. A string that exists only in the chain and is present in the live bundle can only have got there from a build of the chain.

| change | live evidence, fetched from clipershq.com | verdict |
|---|---|---|
| **BL-797** problem report inside the chat widget | `"Report a problem"`, `"One message, no reply. Use the chat if you need an answer."`, `"This goes one way"` all present in the live client bundle. `GET /api/problem-reports` returns **405** (route exists, POST-only), `GET /api/admin/problem-reports` returns **401**, `GET /admin/problem-reports` returns **200** | **LIVE** |
| **BL-797** owner side | `"Problem Reports"` present in the live bundle, in `ownerNav` | **LIVE** |
| **BL-799** reviewer navigation fix | `"Review queue"` present in the live bundle. It is BL-799's relabel of the reviewer clip link and exists nowhere before the chain | **LIVE** |
| **BL-793** fix 1, Discord and app links on one line | the live bundle renders `<span className="whitespace-nowrap">Join our Discord</span>` and carries `gap-2.5 px-2.5` on the footer rows | **LIVE** |
| **BL-793** fix 2, the labelled progress figure | `"in percent added to what you earn"`, BL-793's new screen-reader summary on the milestone grid, present in the live bundle | **LIVE** |
| **BL-793** fix 3, top earners | **BL-793 changed nothing about how it updates**, because it was already live. Seeing no change here is the correct outcome, not a failure | **LIVE, and deliberately unchanged** |
| **BL-793** fix 4, reviewer controls on the profile page | `"This is not zero, it is unknown"`, BL-793's new invitee-reach copy, present in the live bundle served for `/admin/users/[id]` | **LIVE** |
| **BL-788** partner review queue, grant screen | `"What this person will be able to do"`, `"Only clippers they invited"` and the typed phrase `"FULL AUTHORITY"` all present in the live bundle, all absent before the chain | **LIVE** |
| **BL-788** partner review queue, server-side scope | not directly observable from outside, because the `where` clause runs on the server behind authentication. **It is in the same build**: Next.js compiles server and client from one commit, and that commit is proven above. **The column it reads exists in production** and BL-802 wrote to it yesterday | **LIVE by construction, not by direct observation, and I say so** |

**Controls, so these are not false positives.** `GET /api/definitely-not-a-route-bl803` returns **404** and `GET /definitely-not-a-page-bl803` returns **404**, against **405 / 401 / 200** for the three surfaces BL-797 added. **No change is on main but absent from live, and no change is absent from both.** Every branch the reports claim was merged is present in the running build.

## PART 3 — THE DEPLOY PIPELINE, AND WHETHER ANYTHING IS FAILING SILENTLY

**What triggers a deploy, as far as the repository can say.** `railway.json` declares one service, `web`, builder **NIXPACKS**, start command **`npm start`**. There is **no `.github/workflows` directory at all**, so no GitHub Action deploys this project. The repository therefore carries **no deploy trigger of its own**: the trigger lives in the Railway service settings, which are a dashboard setting and not readable from here. **What would settle it: Railway, service `web`, Settings, Source, which shows the connected repository and branch and whether "auto deploy" is on.** I did not guess.

**What the evidence shows regardless of the setting: the deploy happened and it succeeded.** The running artifact was compiled 6.5 minutes after the tip commit and contains the merged code. **A silently failing build would leave the OLD bundle serving, and the old bundle would not contain `--border-strong` or `"Review queue"`.** It does. And because **nothing has been pushed since `d004b396`**, there is no later build that could have failed after this one.

**Could anything fail at runtime while building cleanly? No. Checked directly against the production database.** Every model in `prisma/schema.prisma` was parsed and compared, table by table and column by column, against `information_schema` on production:

```
DB_NOW=2026-08-13 12:11:47.167467+00
MODELS_IN_SCHEMA=83     TABLES_IN_PROD_PUBLIC=91
MISSING_TABLES=0        MISSING_COLUMNS=0
```

**Not one table and not one column that the deployed Prisma client can query is missing from production.** Specifically:

• **`problem_reports` exists** with all **21** columns exactly as BL-797 specified, and holds **0 rows**. BL-797's warning that the running server's generated client had no `problemReport` model was true **of the old deploy only**; `package.json` runs `prisma generate && next build`, so the new build regenerated the client. The table is there, the routes are there, the model is there.
• **`users."reviewerScopeInvitedOnly"` exists** and BL-802 set it on one row yesterday, so the deployed code reads a column that is present.
• **BL-780's two tables are present**; production `public` is at **91 tables**, above the 90 BL-780 recorded, the extra being `problem_reports`.
• **BL-799's 1,039 referral codes were a data write, not a schema change**, and need nothing from a deploy.

**No build error exists to quote, because no build failed.** I am not paraphrasing an error; there is none to report.

## PART 4 — WHERE TO LOOK, AND AS WHOM

This is the actual answer to "I see nothing new". Of the eight items above, **exactly three can be seen from an owner account**, and two of those are small.

| change | who can see it | where, exactly |
|---|---|---|
| **BL-797 report a problem** | **every role, the owner included** | Open the chat launcher, the round accent button at the **bottom right** of any signed-in page. The first row in the list, above every conversation, is a square-tiled row reading **"Report a problem"** with a chevron. **On a phone the launcher is `hidden md:flex`, so it does not exist below 768px**; on a phone it opens from the **Chat tab in the bottom navigation** instead. **If he looked on his phone for a floating button, there was never one to find.** |
| **BL-797 owner inbox** | **OWNER only** | Sidebar entry **"Problem Reports"**, in the owner group near Reviewer Audit, with an unread badge. The list is **empty today, 0 rows**, so it will look like nothing happened. That is correct: nobody has sent one yet. |
| **BL-793 fix 1, sidebar footer** | **every role** | Bottom left of the sidebar. **"Join our Discord"** and **"Download App"** each sit on one line instead of wrapping to two. It is a one-line-versus-two-line difference and easy to miss unless he remembers the wrap. |
| **BL-793 fix 4, reviewer controls** | **OWNER only** | `/admin/users/<someone>`, the **Reviewer Permissions** panel, **collapsed by default and last on a very long page**. Expand it: it now states how many people that person invited and how many clips that covers, in words, and never as a bare zero. |
| **BL-793 fix 2, the +1% figure** | **CLIPPER surface** | `/progress`, the streak milestone squares, now reading **+1% +2% +3% +5% +7%**. **"Progress" is in the clipper navigation only**, so it is not in the owner's sidebar at all; he must type the URL, and he will still see it as a clipper page. |
| **BL-793 fix 3, top earners** | **CLIPPER surface** | `/progress`. **Nothing changed here on purpose.** BL-793 proved it was already reading live from the database. |
| **BL-799 reviewer navigation** | **REVIEWER role ONLY** | **Invisible from an owner account by design.** An owner already has every page. It only shows for a signed-in user whose role is REVIEWER, who now sees the whole clipper navigation plus a **Review** section. |
| **BL-788 partner review queue** | **REVIEWER role ONLY** | Same. The owner-facing half of BL-788 is the grant screen in PART 4's row above. |

**So five of the eight are either invisible to an owner account by design, or a deliberate no-change.** The owner's impression is honest and the software is fine.

## PART 5 — THE VERDICT AND WHAT TO DO

**The live site is running the merged code. There is nothing to fix in the deploy.**

**To see it with his own eyes, in this order, takes about two minutes:**

1. **On a desktop browser, not a phone**, open any signed-in page and click the round accent button at the bottom right. **"Report a problem" is the first row.** On a phone, use the **Chat** tab in the bottom bar instead.
2. **Sidebar, "Problem Reports".** It exists and it is empty. Empty is correct.
3. **`/admin/users/<any user>`, expand Reviewer Permissions.** The invitee-reach sentence is the new part.
4. **Look at the bottom left of the sidebar.** Two single-line rows where there used to be two double-line rows.
5. **To see the reviewer navigation at all he must be signed in as a reviewer.** He cannot see it as the owner, and that is by design, not a bug.

**One thing genuinely still pending, and it is not a deploy problem.** `/admin/problem-reports` holds **0 rows** because no clipper has sent a report yet. Nothing will appear there until one does.

**Two pre-existing findings from earlier rounds that are still true and still unactioned**, repeated once so they are not lost: the stale hand-typed leaderboard blob in `gamification_config` that silently substitutes old money figures if the live query ever returns empty (BL-793 recommended clearing it), and `scripts/test-bl-129-recruiter-access.ts:106`, which still asserts the pre-BL-799 navigation behaviour and will fail (BL-799 reported it rather than quietly editing it). **Neither was touched by this round.**

## WHAT THIS ROUND DID NOT DO, AND WHY

**No authenticated request was made against production.** Proving BL-799's navigation and BL-788's read scope on the live site by observation, rather than by build identity, would mean signing in as a real reviewer on the live product. That is impersonation of a live account and it is outside a read-only audit, so it was not done and nothing is claimed from it. **Everything asserted above came from unauthenticated fetches of clipershq.com, from git, or from read-only SELECTs.**

**No report was created to test the problem-report endpoint end to end**, because that is a write to production.

## GATES AND SAFETY

**No build was run and none is claimed:** this round produced no source change, so tsc and `npm run build` would prove nothing about it. `npm ci` in the worktree exited **0**, used only so a read-only schema-comparison script could import `pg`. **Nothing was deployed, pushed to the product repository, or written.** `origin/main` is still `d004b396`. The working tree and `origin/main` were not moved. No schema change, no `prisma migrate`, **no Apify actor run**, no data mutation. Handles redacted, no wallet address read or printed. Worktree `C:/b803` **removed**.

**One deliberate deviation, stated plainly.** The SHIP line asked for branch `checkpoint/BL-803`; the ABSOLUTE RULE said do not push. **The branch exists locally with the BACKLOG entry committed, and it was NOT pushed**, because the read-only instruction is the stronger one. To publish it: `node scripts/safe-push.mjs checkpoint/BL-803`. It contains one markdown file and cannot affect anything running.
