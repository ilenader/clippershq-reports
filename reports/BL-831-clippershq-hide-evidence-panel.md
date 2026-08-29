# BL-831 — the measurements panel is off his clip screen, hidden behind one switch, and it stopped fetching too

**2026-08-29 · DB `now()` = `2026-08-29 18:57:24.154075+00` (first read) to `19:30:01.743608+00` (last) · BUILD AND MERGE.**
Base `origin/main` @ `96853d49`. Branch `checkpoint/BL-831` @ `f6b54c9f`. **Merged and verified pushed: `origin/main == local == c54b2d60`.** Tags `pre-BL-831`, `post-BL-831`, `pre-merge-BL-831`, `post-merge-BL-831`, all on origin. Isolated worktree `C:/w831`, a short path, `node_modules` never junctioned, **removed at the end**. Every database read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted, no wallet address read or printed.

**A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE.**

> **IT IS OFF, IT IS NOT DELETED, AND IT NO LONGER FETCHES. The switch is `SHOW_REVIEW_EVIDENCE_PANEL` in `src/lib/review-surface.ts`.**
> **AND THE BRIEF'S PREMISE NEEDED CORRECTING: 100 requests and 300 queries was the figure BEFORE BL-816 batched it. Measured today, the panel cost ONE request and FOUR queries.**

---

## PART 0 — WHAT HE IS LOOKING AT, NAMED BEFORE ANYTHING WAS HIDDEN

**It is TWO components, not one, and only one of them is what he described.**

**BLOCK A, HIDDEN.** `ReviewEvidencePanelMount` at `admin/clips/page.tsx:2375`, rendering BL-775's `ReviewEvidencePanel`, fed by BL-816's `ReviewEvidenceBatchProvider` wrapping the list at `:1750`. On **every** row, every status. It renders, in this fixed order: a `role="group"` headed **"Measurements for this clip"**; a paragraph disclaiming the order; **"Other clips by this clipper"** with X-of-Y rejection counts, the bought-views mention count, its most recent date, and the caveat that the count comes from matching words because rejection reasons are free text; a disclosure **"Show N past rejection notes you wrote (unedited, may be blunt)"** quoting his own wording in `figure`/`blockquote`; **"When the views arrived"** with the 6h figure bound into one sentence with its platform-specific caveat clause, then the 24h and 72h marks and the snapshot count; **"Platform analytics"**; a disclosure **"Background counts from past clips. Not a test for this clip."** holding methodology only; and a closing line saying it recommends nothing.

**BLOCK B, LEFT IN PLACE AND NAMED.** BL-666's **"Bot note"** card, `ReviewerNoteCard` at `admin/clips/page.tsx:2444`, a **different** component, **PENDING rows only**, inside the actions grid, with its own two endpoints and its own batch provider. It renders a suggestion pill, a confidence, a headline, metadata health, machine checks, "for your eyes", "what I could not see", "my thinking" and a draft reply.

**The ambiguity is real and it is resolved the way the brief says to resolve it.** Two of the three things he named are Block A's own section labels word for word. The third, "the bot notes", matches Block B's literal name as readily as it matches Block A's quoted "botted views" notes. So the clearly-named parts are hidden and **Block B is left in place**, because sweeping away a second component he did not name cannot be undone by reading. **If he meant the Bot note card as well, that is one line and I will do it on a word.**

---

## PART 1 — HIDDEN, NOT CSS-HIDDEN, AND THE MEASUREMENT CORRECTS THE BRIEF

### The diff, in full

`src/lib/review-surface.ts` is new and holds the switch and the record of what the panel measured. The two readers:

```
ReviewEvidenceBatch.tsx
+ import { SHOW_REVIEW_EVIDENCE_PANEL } from "@/lib/review-surface";
- export const ReviewEvidenceBatchProvider = evidence.Provider;
+ const NO_CLIPS: string[] = [];
+ export function ReviewEvidenceBatchProvider({ clipIds, children }: { clipIds: string[]; children: React.ReactNode }) {
+   return (
+     <evidence.Provider clipIds={SHOW_REVIEW_EVIDENCE_PANEL ? clipIds : NO_CLIPS}>{children}</evidence.Provider>
+   );
+ }

ReviewEvidencePanelMount.tsx
+ import { SHOW_REVIEW_EVIDENCE_PANEL } from "@/lib/review-surface";
  useEffect(() => {
+   if (!SHOW_REVIEW_EVIDENCE_PANEL) return;      // the single-clip fallback never fires either
    if (batched) return;
+ if (!SHOW_REVIEW_EVIDENCE_PANEL) return null;   // after the hooks, so the hooks gate still passes
```

**`admin/clips/page.tsx` was not edited at all.** Blob OID `cf1e55c3e80f` on both refs. 9 files changed, 3 of them source, 735 insertions and 1 deletion.

### Before and after, production build, real owner session, same machine, same database, back to back

main's tree was built and measured first, then the branch's. Median of three warm loads each, at 1440px, `/admin/clips`.

| | BEFORE | AFTER |
|---|---|---|
| `/api/admin/review-evidence/batch` requests | **1** | **0** |
| bytes it carried | **35.3 KB** | **0** |
| total bytes on the wire | **210.4 KB** | **176.6 KB** |
| **DOM nodes** | **5,745** | **4,229** |
| database queries for the panel, per page load | **4** | **0** |
| database time for the panel, per page load | **429.9 ms** | **0 ms** |
| settle, every request answered | 2,960 ms | 2,867 ms |
| total requests | 51 | 51 |

**THE BRIEF'S 100 REQUESTS AND 300 QUERIES IS A PRE-BL-816 FIGURE AND I AM SAYING SO RATHER THAN CLAIMING IT.** BL-816 already batched the storm into one request. `scripts/bl831-probe-queries.ts` measured what remained on a real page of 30: **4 queries and 429.9 ms**, reading 176,027 bytes of rows, against **4 queries and 128.3 ms for a single clip** on the unbatched path. So this round removes the last request, not the storm.

**Settle time and the total request count are NOT claimed as a win.** They are dominated by the polling shell BL-816 named as the next round: `/api/notifications`, `/api/profile/avatar`, `/api/admin/sidebar-counts` and `/monitoring` vary by several requests between identical loads. The honest figures are the ones that do not move: the request census, the bytes and the DOM count.

**Two endpoints now have no caller in the app, named rather than orphaned silently:** `POST /api/admin/review-evidence/batch` and `GET /api/admin/review-evidence/[clipId]`. Both are kept, both still answer the owner, and **the two still agree byte for byte**, which is the proof the hidden logic is intact.

---

## PART 2 — THE SWITCH, AND WHAT THE PANEL MEASURED

**One boolean: `SHOW_REVIEW_EVIDENCE_PANEL` in `src/lib/review-surface.ts`. Set it to `true` and the panel is back exactly as it was.** It is read in exactly two places, both named in the file's own comment. Nothing was deleted: `ReviewEvidencePanel.tsx` `dd97601ec401`, `ClipAnalyticsCard.tsx` `412eabe6635a`, `review-evidence.ts` `4a5d45ff2d34` and both route files are **byte-identical by blob OID on both refs**.

The file also carries the measurements, so their value does not leave with their visibility: **BL-775's six-hour separation** across 4,496 clips, Instagram 66.4% approved against 7.8% rejected by 6 hours where 24 hours separates nothing at 91 against 81, TikTok 40.6 against 6.3, **YouTube 35.2 against 37.5 which is no separation at all**; **the 87.9 percent viral trap**, that 87.9% of 58 approved clips above 100,000 views were also under 10% at six hours, so a reviewer reading a slow start as buying would flag the platform's best clips first; and **BL-820's measured-snapshots-only fix**, which stopped rule #9 reading one unmeasured tick's stored 0 as a 100% fall and accusing a real person of buying engagement. BL-820's fix lives in the fraud rule and the tracking write, not in this panel, and this switch does not touch it.

---

## PART 3 — EVERYTHING ELSE, PROVEN ON A ROW THAT ARRIVES BY SCROLLING

`scripts/bl831-verify.mjs`, production build, real minted sessions, **22 passed, 0 failed**. Nothing mutated.

```
PASS  BL-816: the list still pages at 30                       30 rows at offset 60
PASS  BL-816: totalCount is still the TRUE total               7,167
PASS  BL-816: the appended row is byte-identical fetched alone at its own offset
PASS  BL-736: the picker answers for an appended clip          14 destinations
PASS  BL-736: its hard blocks still refuse, by code            CLIP_HAS_EARNINGS, CLIP_HAS_MONEY_ROWS,
      CLIP_NOT_PENDING, DEST_PAST, DEST_PAUSED, DEST_PLATFORM_NOT_ACCEPTED, SAME_CAMPAIGN
PASS  BL-736: every refused destination still carries a REASON, not just a code
PASS  BL-744: the four labelled rates are still on the OWNER's response   clipper 0.20 · owner 0.1279
PASS  BL-815: a REVIEWER without the capability is still refused          HTTP 403
PASS  BL-815: and his POST is refused too, so nothing moved               HTTP 403
PASS  BL-814: the review route is reachable and refuses an invalid ACTION rather than the caller
                                                                          HTTP 400 {"error":"Invalid action"}
PASS  the single-clip and batch evidence routes are both still present and still agree byte for byte
PASS  BL-666: the Bot note card's routes are untouched and still answer   HTTP 200 / HTTP 200
```

**Approve, Reject, Undo and Flag were proven present and reachable, never pressed.** Pressing one on a real clipper's clip moves money. The undo path is proven by the route refusing an invalid ACTION with a 400 rather than refusing the CALLER, and Approve and Reject are photographed on a PENDING row.

**The reviewer used for the capability checks is a real one.** My first attempt used two soft-deleted fixtures and got a 401, which is auth working correctly and my test being wrong; the suite now asserts the reviewer is live and authenticated before drawing any conclusion from a refusal.

---

## PART 4 — WHO ELSE LOSES SOMETHING, STATED PLAINLY

**A REVIEWER'S VIEW IS AFFECTED, AND I THINK IT SHOULD BE, BUT HE SHOULD KNOW IT.** `CLIP_VIEW` is a **basic** reviewer capability (`reviewer-capabilities.ts:141`), so every reviewer could see this panel and **none can now**. Rendered as a real reviewer and confirmed: the panel is gone from his queue and his page does not fetch it either. The **endpoint gate is unchanged** and still allows him with a 200; the page simply no longer asks. I judged a global switch right because reviewers work the owner's queue under his judgement, and because the fetch only truly stops when nobody fetches. **If he wants reviewers to keep it, the constant becomes a function of the viewer's role and its two readers pass it in.** That is a small, named change.

**No clipper-facing surface changed and nothing previously hidden became visible.** A CLIPPER is still refused both evidence routes with 403, and none of eight forbidden field names (`ownerCpm`, `agencyFee`, `clientName`, `aiKnowledge`, `rejectionsMentioningBoughtViews`, `pctBy6h`, `rawReasons`, `mostRecentBoughtViewRejectionAt`) appears in his own clips payload.

---

## PART 5 — RENDERED, AND MERGED

`scripts/bl831-render.mjs`, production build, `window.innerWidth` printed beside every shot. **8 shots, 0 at the wrong width, 0 with horizontal overflow. 29 assertions, 0 failures.**

```
queue-top   320 · 375 · 414 · 1280 · 1440    measured == asked, every one, overflow 0
  at every width: 0 of 5 panel strings on screen, 0 review-evidence requests, controls present
after-load-more 1440   30 rows then 60, the panel absent on the APPENDED rows, still 0 requests
pending-filter  1440   BL-666's card renders: "BOT NOTE - BAD BITCH ANTHEM (0.50 CPM)", 1 note request,
                       Approve / Reject / Flag on the row, the panel still absent, still 0 requests
reviewer-queue  1440   a REVIEWER sees no panel and fetches none
```

**The layout holds where the panel used to sit.** The row now ends at the actions row and the reviewer meta, with no gap and no empty container, at all five widths. Observed and **pre-existing, not caused here**: at 375px BL-744's rates line clips its "Set a custom rate" link inside its own scroll container; `page.tsx` is byte-identical on both refs, so this round cannot have caused it.

### The accessibility review ran before the change and found 0 blocking items

It also **corrected one of my premises**: the removed `role="group"` boundaries are **4 per row and not 7**, because `ClipAnalyticsCard`'s own three have never rendered in production, the mount having always withheld `analyticsConnected` so the card's absence sentence prints instead. It found no ARIA regression and no id crossing out of the panel, **no heading change at all** (the panel emits none), and that the BL-816 "Load more" focus path is untouched and now measures geometry that does not grow underneath the pointer. At most two tab stops are removed and focus cannot be stranded, because the panel never mounts rather than unmounting under a focused element. It ruled **silent removal correct**: no WCAG criterion applies, and a per-row notice would be the announcement stampede BL-776 exists to prevent. **Lost with no equivalent anywhere:** the rejection rate, the bought-views mention count and its date, and the 6h/24h/72h arrival shares. **Survives elsewhere:** verbatim rejection reasons through `ReviewMetaBlock`, and the raw snapshot series through the Live button on every row. `ReviewerNoteCard` stands alone correctly and in fact reads better, since a PENDING row used to carry two consecutive absence sentences and now carries one. **Its one implementation warning was the trap this change could have walked into and did not: wrap the exported evidence provider, never the shared factory, or the bot note dies with it.**

### Gates, honestly

`eslint` is present in the worktree, so the hooks gate is real. `npm ci` exit 0, `npx prisma generate` exit 0.

| gate | before any edit | after |
|---|---|---|
| `npx tsc --noEmit` | **exit 0, `grep -c "error TS"` = 0** | **exit 0, 0** |
| `npm run build` | **exit 0**, compiled in 53s | **exit 0**, compiled in 62s |
| `lint:hooks` | 0 errors, **11 warnings** | 0 errors, **11 warnings**, at the ceiling, unchanged |

Exit codes were echoed from `$?` into a log and never read through `tail`.

### Merged

| | |
|---|---|
| branch | `checkpoint/BL-831` @ **`f6b54c9f`**, verified on origin by `safe-push` |
| merge commit | **`c54b2d60`**, `origin/main == local` verified by `safe-push` |
| conflicts | **none.** main never moved from `96853d49`, and the **merged tree OID equals the branch tree OID exactly** (`a12c2f65`) |
| BACKLOG | **167 sections before, 168 after**, `BL-831` x1, **0 conflict markers**, counted with `grep -c`, never piped to `head` |
| **`checkpoint/BL-723`** | **confirmed NOT an ancestor of main** |

---

## SAFETY

| | |
|---|---|
| the 6 money files plus `tracking.ts`, `campaign-era.ts` and `apify.ts` | **byte-identical by blob OID on BOTH refs**: `ac5be7de`, `797e2098`, `81a683c1`, `359bcbbe`, `61cef393`, `ef5cdae7`, `106e16ad`, `d66d4534` |
| `admin/clips/page.tsx`, `ReviewEvidencePanel.tsx`, `ClipAnalyticsCard.tsx`, `ReviewerNoteCard.tsx`, `review-evidence.ts`, both evidence routes | **byte-identical on both refs** |
| schema | **no change**, no `prisma migrate`; `prisma generate` only. No index created |
| Apify | **no actor run**; the 27 BL-678 guard comments across 7 files untouched |
| payouts | **204 rows before and after, 0 with an `updatedAt` inside the round window** |
| earnings invariant | **0 violations** before and after |

**MOVED IN THE WINDOW AND NOT MINE, NAMED RATHER THAN SMOOTHED.** Clips 8,337 to 8,338, approved 6,966 to 6,975, pending 20 to 12, approved earnings $15,066.57 to $15,076.08. Every one of the **10 `APPROVED_CLIP` audit rows** in the window is the **owner's own account**, between `18:57:24.949` and `18:59:39.312`, at human pace, and **before this round's server was ever started**. My scripts never pressed Approve. The only other two audit rows in the window are one Discord guild join and one Discord role assign from live traffic. **No `SERVER_ERROR` and no `BUDGET_PROBE_BYPASS` row appeared at all**, unlike BL-816's window: a production build holds one pool and the measuring window was minutes rather than an hour.

## WHAT COULD NOT BE MEASURED, AND WHAT I WOULD SAY NEXT

* **Production timings.** Everything was measured against a local production build pointed at the production database. The request census, the payload sizes, the DOM counts and the query counts are exact; the wall-clock settle times are not production numbers and are not claimed as any kind of win.
* **A real screen reader.** DOM order, roles, focus behaviour and the group boundaries are all measured; NVDA, JAWS and VoiceOver were not run.
* **The panel on a PENDING row before the change.** The queue is newest-first and every PENDING clip on the platform is old, so the BEFORE shots show APPROVED and REJECTED rows. The BEFORE request census proves the panel was fetched for the whole page regardless of status.
* **Next, if he wants it:** the shell is now comfortably the most expensive thing on this page, exactly as BL-816 predicted, and `/api/accounts` still returns every column of every account to the Accounts page at 27.7 MB.
