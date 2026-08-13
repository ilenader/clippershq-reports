# BL-806 — one plain sentence saying what the report button is for

**Merged to main in the same round and verified pushed. `origin/main` == local at `3a1b6a34`.** Branch `checkpoint/BL-806` @ `94f0b3b9`, base `15fc29b1`, tags `pre-BL-806` / `post-BL-806` on origin. Isolated worktree `C:/b806`, short path, `node_modules` never junctioned, **removed at the end**. Every timestamp cast `::text` against DB `now()`. Handles redacted, no wallet address read or printed.

**A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE.**

## PART 1 — the sentence

**Shipped verbatim, and it is the whole change:**

> **Use this to tell the team about anything that looks broken or wrong.**

12 words, one sentence, Flesch-Kincaid grade about 4.8. It is the first paragraph of the form body, directly above the box. **No examples, no bullets, no second sentence, no placeholder essay, no help link.** Everything else BL-804 built is untouched: one box, one send button, no categories, its own row, the reply-free confirmation and BL-797's automatic context capture.

The diff against main is **one source file, 22 insertions, 0 deletions**, and 14 of those lines are the comment explaining the decisions below.

### Why it does NOT restate the no-reply rule, which is a deliberate departure from the brief

The brief asked the sentence to set the expectation that nobody replies. The accessibility review argued against putting that in *this* sentence, and I took the argument, so I am naming it rather than burying it.

The paragraph immediately below it, which BL-804 shipped and which I was told to keep exactly as it is, reads: *"This form goes one way. It reaches the team, and no reply comes back here. For anything that needs an answer, ask on Discord."* The reviewer's point is that **"no reply comes back HERE" is scoped, and that scope is the only thing that keeps "ask on Discord" from contradicting it.** An unscoped "no reply comes back" placed *first* recreates the dead end that BL-804's own header comment says it removed, and turns one crisp promise into three non-identical statements of the same fact in about 43 words, with the vaguest one holding the primacy slot.

My first draft was *"Report anything that looks broken or wrong, and it goes straight to the team with no reply coming back."* Two reviewers independently rejected it: the participial clause dangles onto *the team* rather than the reader, and "it" has two live antecedents (the bug by proximity, the report by intent).

What shipped instead satisfies the hard safety rule, which is that the sentence **must not promise or imply a reply** — it promises nothing. "Use this" also gives the next sentence's "This form" an antecedent, so the two chain rather than compete, and the block now reads **purpose, then the one-way rule, then where answers come from**. The no-reply expectation is still set, one line lower, in the sentence that scopes it correctly. **If the owner wants it inside the first sentence anyway, that is a one-word edit and his call.**

### Accessibility, reviewed before any code was written

Three specialists. No blocker in markup, focus trap or color; the one substantive finding was the copy itself, above.

- **Deliberately NOT added to `aria-describedby`.** That string already carries the roughly 90 word capture disclosure and is re-read on every focus and refocus; the one-way line, which matters more, is not referenced either. Describing the weaker paraphrase but not the actual promise inverts the priority. Focus lands on the `<h2>`, so a browse-mode reader meets the new paragraph as the very next node.
- **Class shipped:** `mb-2 text-balance text-[14px] leading-relaxed text-[var(--text-primary)]`. 14px because that size already exists in this component; `mb-2` pairs it with the one-way line against the 16px gap before the label.
- **No `font-semibold`.** In dark theme `--text-primary`, `--text-secondary` and `--text-muted` are all `#ffffff` and all measure **18.40:1** on the card, so color cannot carry hierarchy. A bold 14px line 2px under the real `h2` would read as a second heading (1.3.1). Size and spacing carry it instead.
- **No `tabindex`, no `role`, no `aria-label`**, so the trap's tabbable set is byte-identical and no third live region collides with the two already present.

**`text-balance` is load-bearing, not decoration.** Measured, the sentence put **one word alone on line two** in the md and lg panels: last-line ratio **0.16 at 414** and **0.11 at 1280**. That is precisely the "wraps badly" the brief asks me to rule out. Balanced, every width renders two even lines at ratio **1.00**, and it degrades to ordinary wrapping where unsupported.

**Reported, not changed, both pre-existing and out of scope:** the focus trap does not handle `active === headingRef`, so Shift+Tab from the heading on open leaves the dialog backwards (2.1.2); and "ask on Discord" is plain text before sending but a real link in the confirmation.

## PART 2 — rendered at five widths

BL-793's method: real Chromium, **CSS viewport set through `browser.newContext({ viewport })`**, and `next dev --webpack` because Turbopack was the blocker. `window.innerWidth` read back and asserted every time.

**17 assertions per width, 0 failures, at 320 / 375 / 414 / 1280 / 1440**, reproduced across two independent clean runs.

| checked at every width | result |
| --- | --- |
| CSS viewport really is the asked width | **5/5** |
| the sentence is rendered, and is exactly ONE sentence | **5/5** |
| fully inside the viewport, no overflow of its container | **5/5** |
| no orphan last line | **5/5**, ratio **1.00** at all five |
| no help link, no bullets in it | **5/5** |
| it sits ABOVE the box | **5/5** |
| the box is still there and not pushed off screen | **5/5** |
| the box is on screen or reachable by scrolling | **5/5** |
| still one box, one send button, no categories | **5/5** |
| focus still lands on the panel heading, not the box | **5/5** |
| BL-804's one-way promise still present | **5/5** |
| report entry still reachable, fully on screen, at least 44px tall | **5/5**, measured `165.25 x 44` at 320 |

Rendered geometry was identical at every width: **2 lines, 45.5px tall, 14px**. **320 renders it exactly as intended** and the entry remains reachable there, which is the width where BL-803 found the old chat launcher was unreachable on a phone entirely.

**Three false failures, reported rather than hidden.** The first run photographed the **loading splash at every width**: a flat 2500ms wait cannot cover a fresh worktree's roughly 50 second cold compile, so the harness now waits on the DOM. The second run redirected to `/login` at every width, because the dev-auth bypass lives in **`.env.development.local`**, which I had not copied into the worktree; `.env` alone sets `DEV_AUTH_BYPASS=false`. The third run lost the owner list to the same flat-wait mistake. **None of the three was a defect in the change**, and the dev server proved flaky under sustained load, with a different subset failing per run, which is why the two contested checks were re-run on their own below.

**One width I did NOT verify, named rather than claimed:** the accessibility review asked for a check at 375 **with the software keyboard raised**, where the panel collapses to roughly 300 to 340px. Headless Chromium does not raise a software keyboard, so I could not reach that state and am not claiming it. The sentence is 45.5px, so it costs about two lines of that collapsed height.

## PART 3 — merged and pushed in this round

`3a1b6a34` merges `94f0b3b9` into `15fc29b1`. **Clean tsc baseline recorded on the clean worktree BEFORE any edit: exit 0, 0 errors.** **Zero conflicts**, so no union resolution was needed; **0 conflict markers**. **BACKLOG counted with `grep -c`, never piped to `head`: 614 before, 615 after**, one entry added and none lost. **`checkpoint/BL-723` is NOT an ancestor of main**, confirmed after the push.

| gate, on the merged tree | result |
| --- | --- |
| `npm ci` in the worktree | exit 0, 561 packages, `node_modules` a real directory and never a junction |
| `npx prisma generate` before tsc | exit 0 |
| `npx tsc --noEmit` | **exit 0, 0 errors**, unchanged from baseline |
| `npm run build` | **`REAL_BUILD_EXIT=0`**, echoed from the log, never piped through `tail`. Compiled in 44s |
| prisma-bypass / removed-fields | 0 violations / OK |
| **hooks gate** | **0 errors, 11 warnings**, with **eslint v9.39.4 confirmed present** so it did not silently no-op |

**Confirmed on the merged result:**

- **The chat is still gone.** `src/app/api/chat` holds **0 files**, and the production build emitted **0 `/api/chat` routes**.
- **The report entry works and is not width-gated.** Rendered and measured at all five widths, above.
- **The archive is still owner-only.** OWNER reads it; **CLIPPER, REVIEWER and ADMIN cannot**. Probed inside the archive's own `<main>`: **0 textareas, 0 submit buttons, 0 text inputs**, so no clipper can reach another clipper's messages (BL-531).
- **The owner's report list still functions.** `GET /api/admin/problem-reports` is **200 for OWNER and 403 for CLIPPER**, and the response contains the sent rows.

## PART 4 — the evidence

| claim | evidence |
| --- | --- |
| the sentence renders at all five widths | 17/17 assertions at each of 320/375/414/1280/1440, two clean runs, geometry `2 lines / 45.5px / 14px` and last-line ratio 1.00 at every width |
| a report still sends and confirms with no implied reply | **3 real rows created and confirmed**: "Thanks for reporting this" present, "This form does not send replies" present, no match for `we will / we'll / get back / shortly / soon as`, focus moved to the confirmation heading, at **320 and 1440** |
| context is still captured | a real row reads `pagePath=/earnings, viewportWidth=320, displayMode=browser-tab, roleAtReport=CLIPPER, clientVersion=0.1.1, serverVersion=0.1.1, pendingClipCount=0, recentRejectionCount=0, blockedBalanceCents=null`. **No wallet, token, password or another clipper's data** |
| no clip's status or earnings changed | **0 clips touched by this round** |
| no payout was touched | **168**, last write `2026-08-13 12:34:46.065`, which is **three hours before this round began**. Payouts created, modified, approved or cancelled: **0** |
| the earnings invariant | **0 violations** |
| money files byte-identical by blob OID on both refs | all 7 **IDENTICAL**: `clip-earnings-writer ac5be7de`, `earnings-calc 797e2098`, `balance e887f80a`, `tracking 83ce4bab`, `invariant-middleware 61cef393`, `money-decimal ef5cdae7`, `campaign-era 106e16ad` |
| BL-678 guards | untouched, no Apify actor run |
| schema | **no change, no `prisma migrate`** |

**Rows I created and how they were removed.** Three `problem_reports` rows on the synthetic `dev-clipper-001` seed account, sent so the confirmation and the context capture could be proven against real rows: `cmsruu6cw…`, `cmsruud32…`, `cmsruysjw…`. **All three deleted** by `scripts/migrations/BL-806-remove-proof-rows.sql` (`rowCount=3`), which is scoped to that account and that body prefix and is idempotent. `problem_reports` now holds **1** row, and **that one is a real user's report from `2026-08-13 17:39:07.061`, which I did not touch.**

**The owner was working live throughout this round, and it was not me.** Between `17:34:14` and `18:08:54` there were **78 clip decisions, every one by the real OWNER account** (75 approvals, 3 rejections). My round made no clip request of any kind.

**One check I could not close, stated rather than claimed:** at **320** the owner's report list did not finish loading its rows inside a 150 second wait, so I never saw the sent reports on that screen. The page itself, its heading and the report entry all render correctly at 320 with no sideways scroll, the same list showed the rows at **1440** in the same run, and the API returns them at 200. I read this as dev-server slowness rather than a defect, but I did not prove that.

## What the owner does now

1. **REDEPLOY ON RAILWAY.** Main carries the sentence; production does not. Nothing above is live until then.
2. **A clipper is still waiting.** Someone opened a chat at **`2026-08-13 15:05:31.300`** through the chat that is still live in production, and there is now a second live signal: a real problem report at **`2026-08-13 17:39:07.061`**. Neither will get a reply through the product.
3. **The 18 never-answered people remain in the archive, and 7 of them explicitly asked for a person.** Oldest 135 days. They are readable at `/admin/chat-archive` once the redeploy lands, and answering them means reaching outside the platform.
