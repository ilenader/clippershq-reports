# BL-808 — the report form is a heading, ONE sentence, the box and the send button

**Merged to main in the same round and verified pushed. `origin/main` == local at `609417f4`.** Branch `checkpoint/BL-808` @ `cf8ff923`, base `3a1b6a34`, tags `pre-BL-808` / `post-BL-808` on origin. Isolated worktree `C:/b808`, short path, `node_modules` never junctioned, **removed at the end**. DB `now()` from `2026-08-14 20:08:25.707+00` to `20:39:17.709+00`, every timestamp cast `::text`. Handles redacted, no wallet address read or printed.

**A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE.**

## PART 1 — the deletion

**123 visible words to 18.** Both numbers are measured out of the live DOM, not estimated: `scripts/bl808-wordcount-before.ts` was run against the unedited tree first, and the render harness measures the same thing after, with `sr-only` nodes stripped so hidden text cannot flatter the count.

**The entire on-screen copy of the form, quoted in full and in order:**

> ### Report a problem
> Tell the team what went wrong, but you will not get a reply here.
> *[the box]*
> 0/2000
> Send report

That is everything. **One visible paragraph, asserted at all five widths.** Deleted: the `This form goes one way. It reaches the team, and no reply comes back here. For anything that needs an answer, ask on Discord.` paragraph; the visible `What went wrong?` label; and the ~80 word paragraph beginning `Say what you were doing`, which is where the character limit was stated in words.

**The behaviour is untouched, which was the point.** BL-797's context capture still runs at submit and a real row from this round reads `pagePath=/earnings, viewportWidth=320, displayMode=browser-tab, roleAtReport=CLIPPER, clientVersion=0.1.1, serverVersion=0.1.1, pendingClipCount=0, recentRejectionCount=0, blockedBalanceCents=null`. The 2,000 character limit is still enforced on the client **and** the server (`/api/problem-reports` still 400s over the limit). BL-804's reply-free confirmation still shows.

**The counter is a small number, not a sentence.** It already existed under the box as `0/2000` and it stays exactly as it was, `aria-hidden`, `tabular-nums`, right-aligned. Deleting the paragraph is what made it the only on-screen statement of the limit. Nothing was added on screen to replace the sentence.

## PART 2 — the two things BL-806 put there on purpose

### The no-reply line: yes, removing it would mislead, so it went inside the sentence

**Stated plainly: removing the pre-send line entirely WOULD leave a clipper misled before they send, and the confirmation does not cover it.** The confirmation arrives after the message is written and sent. The cost of learning late is not "waits forever" — the confirmation prevents that — it is that somebody writes *"can you email me back at…"* or phrases a question, under an assumption this screen never corrected. A box, a Send button and a heading reading "Report a problem" carry the ordinary expectation that a person may answer. BL-806's review was right and I did not dismiss it.

**So the meaning survives inside the one sentence, and no second block was added:**

> Tell the team what went wrong, but you will not get a reply here.

**`here` is load-bearing and must never be trimmed.** Scoped, it says only that this box does not answer. Unscoped it would assert the product never answers anybody, which is false. **`but` rather than `and`,** because the meaning is a contrast; `and` reads as *"do this, and as a result nothing happens"*. My first draft used `and` and the accessibility lead rejected it on exactly that ground.

**On the Discord pointer, and the dead-end question: not a dead end.** The form no longer names Discord, but the alternative is not gone, it moved to where it is actionable. The confirmation carries a **real link** (`Discord (opens in a new tab)`) rather than the form's plain text, the desktop sidebar carries **Join our Discord** at every width above the phone breakpoint (`sidebar.tsx:820`), and the phone tab bar's fifth tab is still Discord Support. **One correction to the brief's premise, which I checked rather than assumed:** that tab bar is `md:hidden`, so it is a phone-only route, not "every width". The desktop route is the sidebar, and it is always there.

### The capture disclosure: not required in the form, moved to Help, and corrected on the way

**Stated plainly: deleting it from the form creates no conformance failure.** The accessibility lead's verdict was unambiguous — no WCAG criterion governs data collection; 3.3.2 covers input the user must supply, 3.3.4 covers legal, financial and data-deletion transactions, and 3.3.7 Redundant Entry is actively *helped* by capture that spares the user typing. It is a transparency question, not a conformance one.

**Two facts that made the panic unwarranted.** The paragraph was **already incomplete** — it never named the screen width, the installed-app-versus-browser-tab flag or the app version, all three of which were being sent. And the capture is conservative in code: the query string and hash are stripped in the browser, the raw user-agent is never stored, and nothing about another clipper is ever attached.

**What I chose, and why.** No link and no disclosure in the form: the order enumerates four elements and a link is a fifth. The disclosure moved to `/help` as a new FAQ entry, **What gets sent with a problem report?**, collapsed by default and reachable through the page's own search — proven: present, findable by typing `report`, opens, and names what is never included. It is the corrected list, so the platform now discloses more than it did, in a place that does not shout. I also widened the confirmation's one narrow line from *"along with the page you were on"* to *"along with the page you were on and a short summary of your account"*, because with the paragraph gone it was the only place the account summary was named at all, and naming one of six things reads as a complete list.

## PART 3 — rendered at five widths

BL-793's method: real Chromium, **CSS viewport set through `browser.newContext({ viewport })`**, `next dev --webpack` because Turbopack was the blocker, `window.innerWidth` read back and asserted every time. **161 assertions, run twice — once on the branch and again on the merged main tree — with identical results.**

| measured at every width | 320 | 375 | 414 | 1280 | 1440 |
|---|---|---|---|---|---|
| CSS viewport really is the asked width | yes | yes | yes | yes | yes |
| visible words in the whole form stage | **18** | **18** | **18** | **18** | **18** |
| visible paragraphs in the form | **1** | **1** | **1** | **1** | **1** |
| the sentence, lines rendered / last-line ratio | 2 / 1.00 | 2 / 1.00 | 2 / 1.00 | 1 / — | 1 / — |
| **no scrolling: the whole form reads at a glance** | **yes** | **yes** | **yes** | n/a | n/a |
| send button on screen without scrolling | yes | yes | yes | yes | yes |
| report entry reachable, fully on screen, ≥44px | `167.5 x 44` | same | same | same | same |
| every deleted string absent from the panel | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 |
| the box still has an accessible name | `What went wrong?` at all five |

**Confirmed: the whole form reads at a glance with no scrolling on a phone.** At 320, 375 and 414 the form's scroll container measures `705/705` — content and viewport identical, nothing to scroll. Before the deletion the same container measured `705/705` at 375 but **`639/585` at 1280**, i.e. the old form scrolled on a desktop panel; it no longer does at any width.

**375 with the software keyboard raised: I could NOT verify it, and I am not claiming it.** Headless Chromium does not raise a software keyboard. I rendered the geometry instead, at 375x340, and report the real result: the sentence and the box are fine, but **the send button falls below the fold and is reachable only by scrolling**. The accessibility lead's finding is that this is worse than the brief assumed and also pre-existing: `layout.tsx` sets no `interactive-widget=resizes-content`, so `100dvh` does not shrink when the keyboard opens and the keyboard **overlays** the panel. The deletion improves that state by roughly two lines and does not cause it. The fix is a pinned footer outside the scroll region and belongs to its own round.

## PART 4 — merged and pushed in this round

`609417f4` merges `cf8ff923` into `3a1b6a34`. **Clean tsc baseline recorded on the untouched worktree BEFORE any edit: exit 0, 0 errors, with `npm ci` exit 0 and `npx prisma generate` exit 0 first.** **Zero conflicts, so no union resolution was needed; 0 conflict markers.** The merge tree OID equals the branch tree OID (`2f8d35c4…`), so the branch's build IS the merge's build, and it was rebuilt on main anyway. **BACKLOG counted with `grep -c`, never piped to `head`: 151 to 152 sections, 21,848 to 21,862 lines — one entry added, none lost.** **`checkpoint/BL-723` is NOT an ancestor of this branch or of main.**

| gate | result |
|---|---|
| `npx tsc --noEmit`, baseline then after then on merged main | **exit 0, 0 errors** at all three |
| `npm run build` on the branch | **`REAL_BUILD_EXIT=0`**, echoed from the log, never piped through `tail` |
| `npm run build` on merged main | **`REAL_BUILD_EXIT=0`**, compiled in 35.4s |
| prisma-bypass / removed-fields | 0 violations / OK across 724 files |
| **hooks gate** | **0 errors, 11 warnings** at the ceiling, with **eslint v9.39.4 confirmed present** so it did not silently no-op |

**Confirmed on the merged result, by asking the running server rather than reading code:**

- **The chat is gone and no route is reachable.** `/api/chat/conversations`, `/unread`, `/sse`, `/campaign-chats`, `/messageable-users` all **404**, against a live control (`/api/campaigns` **200**). **0** `/api/chat/` routes in the production build manifest, **0** files under `src/app/api/chat`.
- **The report entry works at 320.** Measured `167.5 x 44`, fully on screen, panel opens, form usable, no sideways scroll.
- **The archive is still owner-only.** OWNER reads it with **no composer**; **CLIPPER, REVIEWER and ADMIN cannot** (BL-531 holds).
- **The owner's report list still functions.** Rendered at 320 and 1440 with the proof rows and all real rows, grouped by page, unread badge, mark-read and resolve intact; `GET /api/admin/problem-reports` **200 for OWNER, 403 for CLIPPER**.

## PART 5 — the evidence

| claim | evidence |
|---|---|
| the exact final copy | `Report a problem` / `Tell the team what went wrong, but you will not get a reply here.` / the box / `0/2000` / `Send report`, and nothing else |
| rendered at all five widths | 161 assertions at 320/375/414/1280/1440, twice (branch and merged main), same numbers |
| a report still sends with context still captured | **4 real rows created and confirmed** (2 on the branch, 2 on main), one reading `pagePath=/earnings, viewportWidth=320, displayMode=browser-tab, roleAtReport=CLIPPER, clientVersion=0.1.1, serverVersion=0.1.1, pendingClipCount=0, recentRejectionCount=0, blockedBalanceCents=null`. **No wallet, token, password or another clipper's data** |
| the reply-free confirmation still shows | `Thanks for reporting this` present, `This form does not send replies` present, the Discord link present, **no match** for `we will / we'll / get back / shortly / soon as`, focus moved to the confirmation heading, at **320 and 1440** |
| the character limit is still enforced | at 2,001 characters the submit is `aria-disabled=true`, the box is `aria-invalid=true`, the counter reads `2001/2000` and the reason is shown; the server still rejects over-limit bodies |
| no clip's earnings or status changed | **0 clips written by this round.** 15 clips were credited by the production tracking batch inside one 4.5 second window, `20:10:54.034` to `20:10:58.552`, and one real clipper submitted a PENDING clip at `20:27:32.133`. Neither is mine: this round made no clip request of any kind |
| no payout touched | **169**, last write `2026-08-14 17:58:03.747`, which is **two hours and ten minutes before this round's first read**. Payouts created, modified, approved or cancelled: **0** |
| the earnings invariant | **0 violations**, before and after |
| money files byte-identical by blob OID on BOTH refs | all 7 **IDENTICAL**: `clip-earnings-writer ac5be7de`, `earnings-calc 797e2098`, `balance e887f80a`, `tracking 83ce4bab`, `invariant-middleware 61cef393`, `money-decimal ef5cdae7`, `campaign-era 106e16ad`. Also identical: `apify-hard-off 29258a5d` and BL-776's `admin/clips/page.tsx d1ebebe5`, with `ReviewEvidencePanelMount` still present |
| BL-678 guards | untouched, **no Apify actor run** |
| schema | **no change, no `prisma migrate`** |

**Rows I created and how they were removed.** Four `problem_reports` rows on the synthetic `dev-clipper-001` seed account, sent so the confirmation, the limit and the context capture could be proven against real rows. **All four deleted** by `scripts/migrations/BL-808-remove-proof-rows.sql` (`rowCount=2` on each run, idempotent, scoped to that account and that body prefix). `problem_reports` now holds **4** rows and **every one of them is a real user's, untouched.**

**Two false failures, reported rather than hidden.** The render harness first died on `__name is not defined` — esbuild's keep-names helper does not exist inside `page.evaluate`, so a named helper function cannot be declared there; it was inlined. Then the owner's report list reported the sent rows missing at both widths, twice. It was my wait, not a defect: the list is a client fetch and my check ran after a flat 1.2s settle. Re-run with a wait on the row text it **passes at 320 and 1440**, and a 20 second settle at 1440 photographed the full list. BL-806 left this check unclosed at 320; **it is closed now at both widths.**

## ACCESSIBILITY — reviewed before any code, six blocking items implemented

1. **`sr-only` `<label for>` keeps `What went wrong?`** as the box's accessible name (4.1.2). The alternative, promoting the sentence to the label, was rejected: a 14 word accessible name is re-spoken in full on every refocus and is unscannable in the NVDA elements list and the VoiceOver rotor. **2.5.3 Label in Name cannot fail here** — with no visible label text the criterion is out of scope. Speech input still reaches the box because "what went wrong" appears verbatim inside the visible sentence.
2. **`reportHintId` renamed `reportIntroId` and re-pointed** at the surviving sentence. Left alone it would have been an `aria-describedby` aimed at an id nothing renders — a silent 1.3.1 failure that TypeScript cannot catch, because the constant is still referenced.
3. **The sentence is now referenced by the box.** Focus lands on the `h2`, and Tab goes heading → close → box, so it never crosses the paragraph; without the reference the only instruction on the surface, and the only pre-send carrier of the no-reply rule, was reachable solely by deliberate browse-mode reading.
4. **A new `sr-only` `Up to 2,000 characters.`** derived from `PROBLEM_REPORT_MAX_CHARS` (3.3.2). The on-screen counter is `aria-hidden` because it changes every keystroke, and the band announcements fire at 200 remaining, which is 1,800 characters too late. Static text, not a live region, and derived from the constant so it cannot drift from what the server enforces.
5. **`reportStatusId` dropped from `aria-describedby`** (4.1.3). It is already a live region spoken by `announce()`; describing the field with it re-reads a rate-limit refusal on every refocus for the rest of the session. Error id kept, and placed **first**, because a blocked submit returns focus to the box by hand and the reason must be heard before the standing instructions.
6. **The stale rationale comments were rewritten.** Lines that instructed the next maintainer to keep the sentence *out* of `aria-describedby`, on a premise this round deletes, would have got item 3 reverted on their own authority.

Also taken: `mt-3` on the box, because `mb-2` plus `mt-2` collapse to 8px and not 16px; the band timer cancelled at the top of `submit()`, so two polite regions cannot change in the same frame; and `announce()`'s timeout held in a ref so it is cancelled with the others. Contrast tokens, target sizes (all ≥44px), `motion-reduce`, heading nesting and the 320px header math all passed unchanged. **No dashes as bullets, no emojis, no hardcoded colours.**

**Reported, NOT fixed, all pre-existing and out of scope:** zoom is disabled app-wide (`layout.tsx:130`, `maximum-scale=1, user-scalable=no`, 1.4.4), which also invalidates any 400% reflow claim anyone makes about this app; Shift+Tab from the opening focus position walks out of the modal onto the launcher (`use-dialog-focus-trap.ts`, a shared file used by every dialog, needs its own round); the send button is obscured at 375 with the keyboard up (PART 3); the background is not `inert`, only `aria-modal`; and `/help`'s Discord link opens in a new tab with no warning, inconsistent with the widget's own wording.

## WHAT THE OWNER DOES NOW

1. **REDEPLOY ON RAILWAY.** Main carries the trimmed form; production does not. Production is still older than BL-804 — the chat is still live there, which is how a new conversation was opened yesterday. Nothing above is live until the redeploy.
2. **A clipper has been waiting since `2026-08-13 15:05:31.300`,** and wrote their message at `15:06:04.572`. It is still the last word in that conversation and nothing has answered it. **Three more real problem reports arrived today** — `11:49:38`, `12:13:13` and `15:07:38`, all from phones at 360 to 363px — about a rejected clip, a clip not approved yet, and music on a rejected clip. None has been answered either.
3. **The 18 never-answered people are now 19, and 7 of them explicitly asked for a person.** The 15:05 clipper is the 19th. They are readable at `/admin/chat-archive` once the redeploy lands, and answering them means reaching outside the platform.

**Rollback:** `git revert -m 1 609417f4` or `git reset --hard pre-BL-808`. **Nothing in the database needs undoing.**

---

## APPENDIX — the full diff

```diff
diff --git a/src/components/support/ReportProblemWidget.tsx b/src/components/support/ReportProblemWidget.tsx
index b6b5e193..c426cc97 100644
--- a/src/components/support/ReportProblemWidget.tsx
+++ b/src/components/support/ReportProblemWidget.tsx
@@ -35,6 +35,11 @@ import { useDialogFocusTrap } from "@/lib/use-dialog-focus-trap";
  *     is where an answer actually comes from and is already the tab bar's
  *     Support tab and the Help page's link. Saying "no reply comes back"
  *     while offering no alternative would be a dead end.
+ *     BL-808 UPDATE: the form itself no longer names Discord. The pointer is
+ *     made where it is actionable instead, in the confirmation, which carries
+ *     a real link rather than the form's plain text. The form's one sentence
+ *     keeps the scoped "here" precisely so it cannot be read as "this product
+ *     never answers anyone".
  *
  *  3. IT IS A REAL DIALOG. Below md this panel is the whole screen, so the
  *     bare `inert`-only div BL-797 could get away with as a corner card is
@@ -53,6 +58,23 @@ import { useDialogFocusTrap } from "@/lib/use-dialog-focus-trap";
  * `tabbableWithin` correctly keeps as a tab stop; and there is no
  * `maxLength`, because a silent paste truncation on a one-way form can never
  * be discovered by the person who sent it.
+ *
+ * BL-808 (2026-08-14) — THE FORM IS CUT TO FOUR THINGS: the heading, ONE
+ * sentence, the box, the send button. Measured, the form stage carried 123
+ * visible words across three paragraphs and a visible label; the owner asked
+ * for one sentence. Deleted: the "This form goes one way" paragraph, the
+ * visible "What went wrong?" label, and the ~80 word paragraph listing what is
+ * captured automatically, including the sentence that stated the character
+ * limit in words.
+ *
+ * NOTHING BEHIND THE WORDS CHANGED. The context capture still runs at submit
+ * exactly as BL-797 built it, the 2,000 character limit is still enforced on
+ * both the client and the server, and the reply-free confirmation is
+ * unchanged apart from naming the account summary it was already sending.
+ * What the deleted paragraphs said is now carried by: the one sentence (the
+ * no-reply rule, scoped), the small number under the box (the limit), an
+ * sr-only line (the limit, for a screen reader, since that number is
+ * aria-hidden), and the Help page (the capture list, in full and corrected).
  */
 
 const DISCORD_SUPPORT_URL = "https://discord.gg/JVC3JMrxGf";
@@ -74,7 +96,12 @@ export function ReportProblemWidget({ userId, drawerOpen = false }: ReportProble
   const panelId = `report-panel-${ids}`;
   const panelTitleId = `report-title-${ids}`;
   const reportTextId = `report-text-${ids}`;
-  const reportHintId = `report-hint-${ids}`;
+  // BL-808 — was `reportHintId`, and it pointed at the ~90 word capture
+  // paragraph that this round deletes. Renamed rather than left dangling: an
+  // aria-describedby aimed at an id nothing renders fails silently, and
+  // TypeScript cannot catch it because the constant is still referenced.
+  const reportIntroId = `report-intro-${ids}`;
+  const reportLimitId = `report-limit-${ids}`;
   const reportStatusId = `report-status-${ids}`;
   const reportErrorId = `report-error-${ids}`;
 
@@ -94,6 +121,7 @@ export function ReportProblemWidget({ userId, drawerOpen = false }: ReportProble
   const sentHeadingRef = useRef<HTMLHeadingElement>(null);
   const countBandRef = useRef<string>("ok");
   const countTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
+  const announceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
 
   const overBy = Math.max(0, text.length - PROBLEM_REPORT_MAX_CHARS);
   const isOver = overBy > 0;
@@ -108,8 +136,10 @@ export function ReportProblemWidget({ userId, drawerOpen = false }: ReportProble
     setStatus("");
     // 130ms, not a single animation frame: both commits inside one frame are
     // collapsed into a net diff of msg -> msg at the frame boundary, which is
-    // no change at all, which is silence.
-    setTimeout(() => setStatus(msg), 130);
+    // no change at all, which is silence. Held in a ref so closing the panel
+    // and unmounting can cancel it, the same way the band timer is cancelled.
+    if (announceTimerRef.current) clearTimeout(announceTimerRef.current);
+    announceTimerRef.current = setTimeout(() => setStatus(msg), 130);
   }, []);
 
   const openPanel = useCallback(() => {
@@ -126,6 +156,7 @@ export function ReportProblemWidget({ userId, drawerOpen = false }: ReportProble
 
   const closePanel = useCallback(() => {
     if (countTimerRef.current) clearTimeout(countTimerRef.current);
+    if (announceTimerRef.current) clearTimeout(announceTimerRef.current);
     setOpen(false);
   }, []);
 
@@ -155,6 +186,10 @@ export function ReportProblemWidget({ userId, drawerOpen = false }: ReportProble
   const submit = useCallback(async (e: React.FormEvent) => {
     e.preventDefault();
     if (sending) return;
+    // Kill any band announcement still in flight. Typing past the limit and
+    // pressing Send inside the 700ms debounce would otherwise change both
+    // polite regions in the same tick, and one of the two is then dropped.
+    if (countTimerRef.current) clearTimeout(countTimerRef.current);
     if (isOver) {
       // Announce it as well as showing it. Relying on the textarea's
       // description would read 2,000+ characters of value first, so in
@@ -211,9 +246,10 @@ export function ReportProblemWidget({ userId, drawerOpen = false }: ReportProble
     }
   }, [announce, isOver, overBy, sending, text]);
 
-  // Opening: focus the HEADING, not the textarea. Focusing the box on a phone
-  // raises the keyboard immediately and scrolls the "no reply comes back" line
-  // out of view before it is read, which would defeat the whole surface.
+  // Opening: focus the HEADING, not the textarea. The one sentence sits
+  // between the heading and the box in DOM order, so a browse-mode reader
+  // meets it as the very next node; focusing the box instead would skip past
+  // it AND raise the phone keyboard, which pushes the send button under it.
   useEffect(() => {
     if (!open || stage !== "form") return;
     const raf = requestAnimationFrame(() => headingRef.current?.focus());
@@ -245,6 +281,7 @@ export function ReportProblemWidget({ userId, drawerOpen = false }: ReportProble
 
   useEffect(() => () => {
     if (countTimerRef.current) clearTimeout(countTimerRef.current);
+    if (announceTimerRef.current) clearTimeout(announceTimerRef.current);
   }, []);
 
   if (!userId) return null;
@@ -327,8 +364,7 @@ export function ReportProblemWidget({ userId, drawerOpen = false }: ReportProble
         <div className="flex items-center gap-3 border-b border-[var(--border-color)] px-5 py-3.5">
           {/* tabIndex -1 so opening the panel can land focus here rather than
               in the textarea: auto-focusing the box on a phone raises the
-              keyboard and scrolls the "no reply comes back" line out of sight
-              before it is read. */}
+              keyboard and pushes the send button underneath it. */}
           <h2
             id={panelTitleId}
             ref={headingRef}
@@ -350,54 +386,62 @@ export function ReportProblemWidget({ userId, drawerOpen = false }: ReportProble
         {stage === "form" ? (
           <form onSubmit={submit} noValidate className="flex flex-1 flex-col overflow-hidden">
             <div className="flex-1 overflow-y-auto px-5 py-4">
-              {/* BL-806 — what this is FOR, in one sentence, before any rule
-                  about it. Opening on "This form goes one way" told somebody
-                  the postage before telling them the purpose. Deliberately NOT
-                  in aria-describedby: that string already carries the ~90 word
-                  capture disclosure and is re-read on every focus, and the
-                  one-way line below it, which matters more, is not referenced
-                  either. "Use this" also gives the next sentence's "This form"
-                  an antecedent, so the two chain instead of competing.
-                  It does NOT restate the no-reply rule: unscoped, it would
-                  contradict the scoped "no reply comes back HERE" below, which
-                  is what keeps "ask on Discord" coherent rather than a dead
-                  end. Regular weight, not semibold: in dark theme every text
-                  token is the same white, so a bold 14px line 2px under the
-                  real h2 reads as a second heading (1.3.1).
-                  `text-balance` because measured wrapping put a single word
-                  alone on the second line in the md and lg panels (last line
-                  11 to 16 percent of the widest); balancing evens the two
-                  lines and degrades to ordinary wrapping where unsupported. */}
-              <p className="mb-2 text-balance text-[14px] leading-relaxed text-[var(--text-primary)]">
-                Use this to tell the team about anything that looks broken or wrong.
+              {/*
+                BL-808 — THE ONLY SENTENCE ON THIS SCREEN.
+
+                The owner asked BL-806 for one sentence and the form had grown
+                to 123 measured words across three paragraphs and a label. The
+                one-way paragraph, the visible label and the capture disclosure
+                are all deleted. Nothing replaces them: the behaviour they
+                described is untouched, only the words are gone.
+
+                It carries the no-reply meaning INSIDE itself rather than in a
+                second block, because BL-806's review was right that somebody
+                who writes a question here and expects an answer has been let
+                down by this screen and not by the team, and the confirmation
+                only tells them AFTER they have already written it.
+
+                "here" is load-bearing and must not be trimmed. Without it the
+                sentence asserts the product never answers anybody, which is
+                false and has no counterweight left on this surface: the
+                Discord pointer now lives in the confirmation and on /help.
+
+                "but" rather than "and": the meaning is a contrast, and "and"
+                reads as "do this, and as a result nothing happens". The
+                subject shifts across the conjunction either way, so the
+                connective has to carry the turn.
+
+                Regular weight, not semibold: in dark theme every text token is
+                the same white, so a bold 14px line under the real h2 reads as
+                a second heading (1.3.1). `text-balance` because measured
+                wrapping otherwise leaves one word alone on the last line in
+                the md and lg panels. No bottom margin here: the gap is owned
+                by the textarea's `mt-3`, since adjacent margins collapse and
+                two half-gaps would silently become one.
+              */}
+              <p id={reportIntroId} className="text-balance text-[14px] leading-relaxed text-[var(--text-primary)]">
+                Tell the team what went wrong, but you will not get a reply here.
               </p>
 
-              {/* The one-way promise is made BEFORE sending, not only after.
-                  Somebody who expects a reply and does not get one has been
-                  let down by this screen, not by the team. */}
-              <p className="text-[13px] leading-relaxed text-[var(--text-secondary)]">
-                This form goes one way. It reaches the team, and no reply comes
-                back here. For anything that needs an answer, ask on Discord.
-              </p>
-
-              <label htmlFor={reportTextId}
-                className="mt-4 block text-[13px] font-semibold text-[var(--text-primary)]">
-                What went wrong?
-              </label>
-              {/* The disclosure names EVERYTHING that rides along, including
-                  the account state. Telling somebody their browser is
-                  attached while quietly attaching their rejection count and
-                  their blocked balance is not consent. */}
-              <p id={reportHintId} className="mt-1.5 text-xs leading-relaxed text-[var(--text-muted)]">
-                Say what you were doing and what you expected to happen. Up to{" "}
-                {PROBLEM_REPORT_MAX_CHARS.toLocaleString()} characters. Sent
-                automatically with it: the page you are on, your device and
-                browser, and a short summary of your account right now, which is
-                how many clips are waiting for a decision, how many were
-                rejected in the last 30 days, and any balance you are holding
-                below a campaign minimum. Your wallet address, your password and
-                anybody else&apos;s information are never included.
-              </p>
+              {/* The label is kept and hidden, not deleted. A textarea with no
+                  accessible name is a 4.1.2 failure, and "What went wrong?" is
+                  a short scannable name in the NVDA elements list and the
+                  VoiceOver rotor, where the 14 word sentence above would not
+                  be. It also appears verbatim inside that sentence, so speech
+                  input still reaches the box by substring. Tailwind `sr-only`
+                  ONLY: `hidden` would remove it from the accessibility tree. */}
+              <label htmlFor={reportTextId} className="sr-only">What went wrong?</label>
+
+              {/* The limit is now shown on screen ONLY as the small number
+                  under the box, which is aria-hidden because it changes on
+                  every keystroke. Without this line a screen reader user would
+                  learn the limit exists only at 200 characters remaining,
+                  which is 1,800 characters too late (3.3.2). Static text, not
+                  a live region, and derived from the constant so it can never
+                  drift from what the server enforces. */}
+              <span id={reportLimitId} className="sr-only">
+                Up to {PROBLEM_REPORT_MAX_CHARS.toLocaleString()} characters.
+              </span>
               <textarea
                 id={reportTextId}
                 ref={textRef}
@@ -405,17 +449,26 @@ export function ReportProblemWidget({ userId, drawerOpen = false }: ReportProble
                 onChange={(e) => onChange(e.target.value)}
                 rows={8}
                 spellCheck
-                aria-describedby={`${reportHintId} ${reportStatusId}${isOver ? ` ${reportErrorId}` : ""}`}
+                /* Error FIRST: a blocked submit returns focus here by hand, and
+                   the reason has to be heard before the standing instructions.
+                   `reportStatusId` is deliberately NOT here: it is already a
+                   live region spoken by announce(), and describing the field
+                   with it would re-read a rate-limit refusal on every refocus
+                   for the rest of the session (4.1.3). */
+                aria-describedby={`${isOver ? `${reportErrorId} ` : ""}${reportIntroId} ${reportLimitId}`}
                 aria-invalid={isOver || undefined}
-                className="mt-2 w-full resize-y rounded-xl border border-[var(--border-strong)] bg-[var(--bg-input)] px-4 py-3 text-[14.5px] leading-relaxed text-[var(--text-primary)] focus:border-accent focus:ring-1 focus:ring-accent focus:outline-none"
+                className="mt-3 w-full resize-y rounded-xl border border-[var(--border-strong)] bg-[var(--bg-input)] px-4 py-3 text-[14.5px] leading-relaxed text-[var(--text-primary)] focus:border-accent focus:ring-1 focus:ring-accent focus:outline-none"
                 style={{ minHeight: 160, maxHeight: 320 }}
               />
 
               {/* No maxLength. A silent paste truncation on a one-way form can
                   never be discovered by the person who sent it, so the
-                  overflow is shown and named instead. The visible count is
-                  aria-hidden; the band-crossing region below is the only
-                  spoken one, so there is no unreferenced sr-only duplicate. */}
+                  overflow is shown and named instead. BL-808: this small
+                  number is now the ONLY on-screen statement of the limit, in
+                  place of the sentence that used to say it in words. It stays
+                  aria-hidden because it changes on every keystroke; the sr-only
+                  line above the box carries the limit for a screen reader and
+                  the band-crossing region below is the only spoken counter. */}
               <div className="mt-1.5 flex items-center justify-end">
                 <span aria-hidden="true" className="text-xs tabular-nums text-[var(--text-muted)]">
                   {text.length}/{PROBLEM_REPORT_MAX_CHARS}
@@ -474,8 +527,13 @@ export function ReportProblemWidget({ userId, drawerOpen = false }: ReportProble
               className="text-base font-semibold text-[var(--text-primary)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-accent)]">
               Thanks for reporting this
             </h3>
+            {/* BL-808 — this used to name the page and nothing else, which read
+                as the complete list. With the capture paragraph gone from the
+                form it is the only place the account summary is named at all,
+                so it names it. The full list lives on the Help page. */}
             <p className="mt-2 text-[14px] leading-relaxed text-[var(--text-secondary)]">
-              Your message is with the team, along with the page you were on.
+              Your message is with the team, along with the page you were on and
+              a short summary of your account.
             </p>
             <p className="mt-2 text-[14px] leading-relaxed text-[var(--text-secondary)]">
               This form does not send replies. For anything that needs an
diff --git a/src/app/(app)/help/help-redesigned.tsx b/src/app/(app)/help/help-redesigned.tsx
index 8b797dec..9c648a37 100644
--- a/src/app/(app)/help/help-redesigned.tsx
+++ b/src/app/(app)/help/help-redesigned.tsx
@@ -29,7 +29,7 @@ import { useMemo, useState, useEffect, useRef } from "react";
 import {
   LifeBuoy, Search, ChevronDown, MessageCircle, ArrowUpRight, Rocket, DollarSign,
   Flame, Star, Wallet, ShieldCheck, XCircle, Eye, ShoppingBag, Users, HelpCircle, Sparkles,
-  Megaphone, Globe, Ticket, TrendingUp,
+  Megaphone, Globe, Ticket, TrendingUp, Flag,
 } from "lucide-react";
 
 const DISCORD_URL = "https://discord.gg/JVC3JMrxGf";
@@ -106,6 +106,18 @@ const FAQS: Faq[] = [
     "They get a reduced platform fee too: 4% instead of 9%.",
     "There's no limit on referrals. The more active clippers you invite, the more passive income you earn.",
   ]},
+  // BL-808 — the report form used to carry this list as an ~80 word paragraph
+  // above the box. The owner cut the form to one sentence, so the disclosure
+  // moved here, where it is searchable and does not shout, rather than being
+  // dropped. It is also CORRECTED: the paragraph in the form never named the
+  // screen width, the app-versus-browser flag or the app version, all three of
+  // which were being sent. Keep this in step with `collectClientContext` in
+  // `src/lib/problem-report-context.ts`.
+  { id: "report-data", Icon: Flag, tag: "Help", q: "What gets sent with a problem report?", a: [
+    "When you send a problem report, your message goes to the team along with a few details that help us find the problem without asking you for them.",
+    "Those details are: the page you were on (without anything after the ? in the address), how wide your screen is, whether you are in the app or a browser tab, roughly which device and browser you use, the app version, your role, the time, how many of your clips are waiting for a decision, how many were rejected in the last 30 days, and any balance you are holding below a campaign minimum.",
+    "Your wallet address, your password, your email and anybody else's information are never included. Nothing about another clipper is ever attached.",
+  ]},
   { id: "issues", Icon: Sparkles, tag: "Help", q: "Something's not working? What do I do?", a: [
     "Views not updating? We recheck on a schedule. Give it a little time before worrying.",
     "Clip URL won't submit? Make sure it's the direct post link and that you're within 30 minutes of posting.",
```

Also in the commit, none of it shipping code: `scripts/bl808-render.ts`, `scripts/bl808-owner-list.ts`, `scripts/bl808-help-check.ts`, `scripts/bl808-wordcount-before.ts`, `scripts/migrations/BL-808-remove-proof-rows.sql`, and the `BACKLOG.md` entry.
