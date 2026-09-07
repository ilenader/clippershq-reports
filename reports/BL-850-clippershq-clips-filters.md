# BL-850 — the clips page filters and sorts

**Merged to main `f6a418ad`. Branch `checkpoint/BL-850` at `908080fe`. Requires a Railway REDEPLOY.**

## The short version

You said you select two campaigns, ask for most views, and nothing changes. **Both of those controls were
already working.** What was broken is that **you could only name 5 of your 34 campaigns**, and **4,760 of your
9,496 clips, 50.1 percent, sat on campaigns the picker would not show you.** That is fixed. On your own two
campaigns the count went **2,777 to 3,824**, so **1,047 clips became reachable that were not.**

## PART 0 — the inventory, and a correction to my own first answer

Every control on `/admin/clips`, with a verdict proven by direct request against the running server rather
than read off the source.

| Control | Where | Before | After |
| --- | --- | --- | --- |
| Campaign picker | `page.tsx:1771` → `route.ts:243` | SERVER, correct | unchanged |
| Sort (Newest / Most views) | `page.tsx:1818` → `route.ts:728` | SERVER, correct | unchanged |
| Search box | `page.tsx:1765` → BL-160 | SERVER, correct | unchanged |
| Date range | BL-‑OWNER-CLIPS-FILTERS-SERVER | SERVER, correct | unchanged |
| Real status chips | `page.tsx:727` → `route.ts:257` | SERVER, BL-837 | unchanged |
| **Help requested** | `page.tsx:1068` | **CLIENT, over 30 rows** | **SERVER, union** |
| **Client flagged** | `page.tsx:1069` | **CLIENT, over 30 rows** | **SERVER, union** |
| **Bot suspected** | `page.tsx:1072` | **CLIENT, over 30 rows** | **SERVER, union** |
| **The campaign LIST itself** | `campaigns/route.ts:110,125` | **hid 29 of 34** | **all 34 for the owner** |
| **Archived campaigns' clips** | `clips/route.ts:460` | **excluded for everyone** | **admitted for the owner** |
| **ADMIN pagination** | `page.tsx` param gate | **capped at newest 500** | **pages like the owner** |

**I got the diagnosis wrong the first time and the accessibility review caught it.** I reported that you had
selected an archived campaign and its clips were being dropped. You could not have: `scope=manage` forces
`isArchived = false` and `status != "PAST"`, so an archived campaign was never in the list to select. I
verified that independently before changing anything, and the fix is the wider list rather than the narrower
one I first proposed.

**Reproduced against the real server, as you, on a production build.** Both named controls answered correctly:
the platform's single highest-view clip at **12,758,532 views** leads page 1, and every row of a two-campaign
request belonged to those two campaigns.

## PART 1 — every wrong control, fixed

**The campaign list.** The picker now also fetches `archived=true&includePast=true`, **for the OWNER only**,
and merges it live-campaigns-first, de-duplicated by id. Nothing changes for any other role.

**Archived clips are admitted.** `clips/route.ts:460` used to force `campaign: { isArchived: false }` for every
caller, so even a hand-typed id returned nothing. The OWNER now sees them; everyone else is exactly as before.

**The three virtual chips.** They are OR-combined with the real statuses on screen. BL-837 sent the status
narrowing **only when no chip was ticked** and wrote that limit down honestly, so ticking one threw the whole
server narrowing away and fell back to filtering the 30 loaded rows. `clientFlagged=1` and `botSuspected=1`
already existed but both **AND** into the query, which answers a different question. **Measured before the
change: `statuses=PENDING&botSuspected=1` returned 748, identical to `botSuspected=1` alone**, because
`botSuspected` overwrites the status clause and the PENDING narrowing simply vanished.

`orMode=1` now asks the route for the page's real meaning: a **union** over the full set. It is sent only when
a chip is on, so every existing caller keeps the exact AND behaviour it has today. **Measured after: Pending
union Bot suspected is 909, which is exactly 82 + 827 and larger than either branch alone.**

**Counts match lists.** 11 checks, **11 passed, 0 failed**, with every expected number read from the database
**immediately before** its assertion. The first draft hardcoded 3,810 and 76; both had moved within the hour.

| Check | Result |
| --- | --- |
| Two campaigns, one archived, count against DB truth | 3,824 = 3,824 |
| Archived campaign alone, which used to return nothing | 1,047 = 1,047 |
| Highest-view clip on the platform leads page 1 | yes, 12,758,532 views |
| Two campaigns AND a status AND the sort | 62 = 62, every row PENDING or FLAGGED |
| The chip union is the true sum of its branches | 909 = 82 + 827 |
| Page 1 and page 2 share no clip | 0 overlapping, both full at 30 |
| The oldest pending clip is reachable by filter | found on page 1 |

## PART 2 — sorting orders the whole set

`ORDER BY ls.views DESC NULLS LAST, c."createdAt" DESC, c.id DESC`, applied to every matching row **before**
the page slice. **The tie break is total**, because `c.id` is unique, so no two pages can disagree and paging
cannot duplicate or skip a clip. Proven rather than argued: page 1 and page 2 share 0 clips and both are full.

## PART 3 — the cost, measured

Measured on a production build against the live database, warm, both sides on the same machine.

| | Requests | Queries | DB time | Payload | Matched set |
| --- | --- | --- | --- | --- | --- |
| Your case, before | 1 | 6 | 343 ms | 21.6 KB | 2,777 |
| Your case, after | 1 | 6 | 293 ms | 21.6 KB | **3,824** |
| Chip union, before | 1 | 6 | 453 ms | — | 8,404 rows, then filtered in the browser |
| Chip union, after | 1 | 6 | 312 ms | — | **909, filtered in the database** |

**No index was added, and none is needed today.** Your campaign case already uses `clips_campaignId_idx`:
**3.1 ms for 3,824 rows.** The chip union is a sequential scan, **4.6 ms over 9,575 rows, 776 buffers**, which
is cheaper than the page's own render. If the clips table ever grows enough to want one, this is the SQL, for
you to run in the Supabase editor as a deliberate step:

```sql
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_clips_bot_suspected_open
  ON clips (status)
  WHERE "lastBotAlertScore" IS NOT NULL AND "fraudDismissedAt" IS NULL AND "isDeleted" = false;
```

**Accuracy was taken over speed wherever they met.** The archived-campaign fix makes the query match more rows,
not fewer, and that is the point.

## PART 4 — every other paginated list

**The same shape exists in six more places. None is fixed here**, because each needs its own measurement and
render proof, and a round that changed a payout query without measuring it would repeat the mistake this one
exists to correct. Each figure below is a direct count against your live database.

| Surface | Cap | Reality | Live severity |
| --- | --- | --- | --- |
| **`/admin/payouts`** | `take:200`, no `where` at all | **221 payout rows, already over** | **Highest.** Every status chip filters whatever happened to be newest. The 21 rows currently pushed out are 2 REJECTED and 19 VOIDED, so nothing actionable is hidden **today**, but the window is full. |
| **`/admin/users/[id]`** | `take:50` clips | **top clipper holds 870** | **High, and money-facing.** The approved/pending counts, the all-time earnings tile, the **unpaid balance tile** and the campaign dropdown are all computed from the newest 50 clips. For anyone above 50 those figures are wrong. The per-clip list itself is correctly paginated. |
| Referral override | `take:1000` | **1,627 clippers** | High. The search box is silently blind to the oldest 627, with no disclosure. |
| Agency earnings | `take:1000` per campaign | one campaign holds **2,026** | Medium. Dollar totals are safe (aggregated by BL-837); the expandable per-clip list is half missing. |
| Community `TicketPanel` | 30 per fetch | largest campaign has **exactly 30** | Medium. Filters and counts run over the loaded page; the API already supports `status=` server-side. |
| Marketplace admin, Submissions tab | 100 per fetch | table is empty today | Low. The cursor is set and the "Load more" button is never rendered, so the "+" in the counter promises a control that does not exist. |

**Checked and correct:** `/admin/audit-log` (keyset cursor, all filters server-side), `/admin/team`,
`/admin/growth`, `/client/clips` (raw SQL with a matching COUNT), `/marketplace/browse`, `/marketplace/incoming`,
`/admin/watch`, `/marketplace/strikes`, the clipper's own `/clips`.

## PART 5 — proven, including your exact case

**85 render assertions, 0 failures, 15 shots** at 320, 375, 414, 1280 and 1440, with `window.innerWidth`
printed beside every one. **0 at the wrong width, 0 with horizontal overflow.** Rendered as you, on a real
minted session with the dev bypass off. The run **presses the two controls you press** rather than
photographing a default queue. **Nothing that moves money was pressed:** Approve, Reject, Flag, Undo and the
campaign-move button were never touched.

**One test was wrong and it is recorded rather than quietly fixed.** Its first version asserted the archived
marker on your exact case and read **0 markers at four widths of five**. That was the test, not the page:
sorted by Most views across both campaigns, **all thirty top rows belong to the live campaign**, so there was
no archived row on screen to mark. The marker is now proven on the archived campaign alone: **30 markers on 30
rows at every width.**

**A row whose campaign is archived now says so.** Before this round your list could not contain one, so nothing
needed to say it and nothing did. It reads **"Campaign archived"** and not a bare "Archived", because it sits
beside the clip's status badge where a bare word would read as a fifth clip status.

**No money and no status changed.**

| Fingerprint | Before | After |
| --- | --- | --- |
| Clip statuses, all 9,579 | `9a45d3f9` | `9a45d3f9` **same** |
| Payout rows and states | `9c311f1b` | `9c311f1b` **same** |
| Campaign money | `c7a9a4a9` | `c7a9a4a9` **same** |
| Money out | $7,003.89 | $7,003.89 **same** |
| Invariant violations | 0 | 0 |
| Payouts created / changed | — | **0 / 0** |

**One fingerprint did move and it is attributed rather than smoothed.** `clip_money_fp` changed. **97 clips
were updated in the window and all 97 took a tracking snapshot inside it. 0 were updated without one, 0 manual
snapshots, 0 clips reviewed, 0 audit rows.** That is your production tracking cron running against the same
database. **This round issued GETs and wrote nothing.**

## PART 6 — the merge

Merged to main at **`f6a418ad`**, pushed and verified with `safe-push`. **The merge tree OID equals the branch
tree OID exactly at `3e33f355`, so the branch's green build is the merge's build.** Main had not moved, so
there were no conflicts and no unions were needed. **BACKLOG 180 to 181**, counted with `grep -c`.
`checkpoint/BL-723` confirmed **not** an ancestor of main. Worktree `C:/w850` removed.

**Build honesty.** eslint v9 confirmed present, so the hooks gate is a real check. Clean tsc baseline on the
untouched worktree before any edit. **tsc exit 0 with `grep -c "error TS"` = 0; `npm run build` exit 0
pre-commit and exit 0 post-commit**, each written to a log with the exit code echoed by hand and never piped
through `tail`. **Hooks gate: 0 errors, 10 warnings, zero added.** One intermediate build **did** fail, exit 1,
on a measurement script importing `PrismaClient` from the wrong path; it is reported rather than hidden, and
the two greens above were taken after it was fixed.

**Safety.** The 6 money files plus `tracking.ts`, `campaign-era.ts`, `payout-calc.ts`, `apify.ts` and
`prisma/schema.prisma` are **byte-identical by blob OID on both refs**. No schema change, no `prisma migrate`,
no index created, no Apify actor run, the 11 BL-678 guards untouched, 0 Supabase pool errors, every timestamp
cast to `::text` against the database's own `now()`. No wallet address printed and no handle named.

## The accessibility review

It ran before any UI was written and every blocking item was implemented.

- It **caught my diagnosis error**, which is the round's most valuable correction.
- It caught that `campaign.isArchived` had been dropped from the API select, which would have made every
  row-level marker dead code.
- It caught that the end-of-list sentence still read *"The server found N before the filters on this page were
  applied"*, naming a cause that stops existing at the exact moment this lands. It now states the total and
  what to do, and claims nothing about why.
- It caught that the legacy list branch never cleared the failure notice, so a REVIEWER kept a stale "could
  not load" line above a list that had just loaded, with no way to dismiss it short of a reload.
- It caught that the page's only live region carried `empty:hidden`, which prunes it from the accessibility
  tree and defeats the persistent mount it exists for.

**Rollback:** `git revert -m 1 f6a418ad`.
