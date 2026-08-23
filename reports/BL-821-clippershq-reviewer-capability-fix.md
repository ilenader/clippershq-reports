# BL-821 — the granted reviewer capability was working. The silence around it was not.

**2026-08-23 · DB `now()` = `2026-08-23 21:28:38.467929+00` (first read) to `22:33:48.654601+00` (last) · INVESTIGATE, BUILD AND MERGE.**
Base `origin/main` @ `b9a288cc`. Branch `checkpoint/BL-821` @ `e5bd62ef`. **Merged and verified pushed: `origin/main == local == 4ea1c139`.** Tags `pre-BL-821`, `post-BL-821`, `pre-BL-821-merge`, `post-BL-821-merge`, all on origin. Isolated worktree `C:/w821`, a short path, `node_modules` never junctioned, **removed at the end**. Every read through `scripts/run-select.js`, every timestamp cast `::text` against DB `now()`. Handles redacted where they are not the subject; no wallet address read or printed.

**A REDEPLOY ON RAILWAY IS REQUIRED BEFORE ANY OF THIS IS LIVE.**

> ## THE ANSWER, FIRST
> **THERE IS NO BUG IN THE CAPABILITY GATE, AND THAT IS THE FINDING.** The capability is saved. The build is live. He has 27 invitees. Asked as **him**, his own invitee's clip returned **HTTP 200 with a working picker**.
> **WHAT HE CANNOT DO IS FIND A CLIP HE IS ALLOWED TO MOVE.** All **463** of his invitees' clips are already APPROVED or REJECTED — **none PENDING** — and **461 of them sit in three campaigns he is not assigned to**. Every clip waiting in his queue belongs to a clipper he did not invite.
> **IT IS NOT JUST HIM.** `movable_if_granted` is **0 for every reviewer on the platform**. Whoever had been granted this would have seen the same nothing.
> **WHAT WAS ACTUALLY DEFECTIVE IS THE SILENCE**, in BL-814's exact shape: a clip his own queue had just listed to him answered the generic **404 "Clip not found"** while he was looking at it, and no screen anywhere said why the control was missing. That is what this round fixes.
> **NO REAL CLIPPER'S CLIP WAS MOVED.** Every move was on a synthetic fixture that lived for 39 minutes and was removed.

---

## PART 0 — THIS USER'S ACTUAL STATE, AND THE FOUR PLAIN EXPLANATIONS, RULED OUT ONE BY ONE

Handle `jdb001`, id `cmoagb7e…`. Read live at `2026-08-23 21:28:38.467929+00`.

| question the brief asked | measured answer |
|---|---|
| his role | **REVIEWER** |
| does he hold the reviewer role | **yes**, since `2026-04-22 19:34:04.602` |
| does he hold the campaign-change capability | **YES** — `reviewerCapabilities = {ANALYTICS_VIEW, CLIP_REASSIGN_CAMPAIGN}` |
| when was it granted | **`2026-08-20 19:14:12.441`** |
| invitee scope flag `reviewerScopeInvitedOnly` | **false** (he is one of the three the owner deliberately left unscoped) |
| TRIAL or LIVE | **LIVE** |
| clippers he personally invited | **27** |
| their clips, by status | **APPROVED 321 · REJECTED 142 · PENDING 0** · 0 deleted |
| campaigns he is assigned to | **3** — Zhus Meme (0.20 CPM), Zhus Edit (0.50 CPM), SomeSome App, all ACTIVE |
| `reviewerCanSeeDecided` | true |
| last login | **`2026-08-23 19:59:51.539`**, ~90 minutes before this round began |

### 1. WAS THE CAPABILITY ACTUALLY SAVED? — **YES. Ruled out.**

Not read off a screen. Read out of the column, and corroborated by the audit row that wrote it:

```
users.reviewerCapabilities   {ANALYTICS_VIEW,CLIP_REASSIGN_CAMPAIGN}
audit_logs REVIEWER_CONFIG_UPDATED  2026-08-20 19:14:12.441
  before {"reviewerCapabilities":["ANALYTICS_VIEW"], …}
  after  {"reviewerCapabilities":["ANALYTICS_VIEW","CLIP_REASSIGN_CAMPAIGN"],"sessionVersion":{"increment":1}}
```

BL-790's six phantom checkboxes and BL-794's unset flag are both absent here. The stored value is correct.

**And it is not silently ignored either.** `hasCapability` auto-grants the Basic set (`CLIP_VIEW`, `CLIP_APPROVE`, `CLIP_REJECT`) to every non-referral-only reviewer, so the route's `if (!holdsMove || !holdsView)` gate passes for him. Verified by request, not by reading: the GET on his invitee's clip returned **200**, which it cannot do if either half of that gate fires.

### 2. HAS THE DEPLOY HAPPENED? — **YES. Ruled out.**

BL-815 stated a redeploy was required. It happened. Determined by probing routes that exist only in builds **after** BL-815's merge (`7f97dd0f`) — the two BL-816 added — against a control that exists nowhere:

```
GET  https://clipershq.com/api/admin/review-evidence/batch   -> 405   (route exists, no GET handler)
POST https://clipershq.com/api/admin/review-evidence/batch   -> 401   (route exists, auth gate)
GET  https://clipershq.com/api/admin/reviewer-note/batch     -> 405
POST https://clipershq.com/api/admin/reviewer-note/batch     -> 401
GET  https://clipershq.com/api/admin/definitely-not-a-route-bl821 -> 404   (control)
```

BL-816 merged after BL-815 and strictly contains it, so the live build carries the feature.

### 3. DOES HE HAVE ANY INVITEES AT ALL? — **27. Ruled out.**

BL-802's other partner had zero. This one does not. 27 invitees, 463 clips between them.

### 4. ARE THE CLIPS HE CAN SEE PENDING WITH ZERO EARNINGS? — **THIS IS IT, and it is worse than the brief guessed.**

The question splits in two, and both halves fail:

* **His invitees' clips are not PENDING.** 321 APPROVED, 142 REJECTED, **0 PENDING**. BL-736's clip-side blocks refuse every one of them outright.
* **The PENDING clips he CAN see are not his invitees'.** 17 clips were waiting for his decision at `21:29`. **Zero** belonged to a clipper he invited.

**Where his invitees actually post — the number that explains everything:**

| campaign | his invitees' clips | PENDING | in his assigned set? |
|---|---|---|---|
| bees.n.honey | 270 | 0 | **no** |
| somesome | 100 | 0 | **no** |
| WinGram | 91 | 0 | **no** |
| Zhus Meme (0.20 CPM) | **2** | 0 | yes |

Newest invitee clip anywhere: **`2026-08-04 15:48:37.319`**, nineteen days before the grant.

**And the audit log shows the owner narrowed him to those three campaigns 2 h 19 min BEFORE granting the capability.** At `2026-08-20 16:55:21` to `16:55:35` his scope was rewritten from `{bees.n.honey, somesome, WinGram, …}` to `{Zhus Meme, Zhus Edit, SomeSome App}`. The capability landed at `19:14:12` on a scope his invitees had never posted into. Neither decision was wrong on its own; together they left nothing to move.

> **PLAINLY: none of the four plain explanations is an unsaved capability, an undeployed build or a missing invitee. It is the fourth, in both of its halves at once.**

---

## PART 1 — REPRODUCED BY DIRECT REQUEST, NOT INFERRED

**Method.** A real Auth.js session was minted for **his id only** (`scripts/bl821-mint-session.mjs`) and every request below was made as him against `next dev --webpack`, pointed at the production database. **The mint writes nothing:** the token carries only `sub` and a `lastLoginDay` marker set to today, which suppresses the `lastLoginAt` stamp the auth callback would otherwise make on his row. BL-802 established the technique; BL-740 is why it is used at all.

Identity confirmed before anything else:

```
GET /api/auth/session -> 200
{"user":{"name":"jdb001","id":"cmoagb7ei00300pqvfgr5tp92","role":"REVIEWER",
 "reviewerCapabilities":["ANALYTICS_VIEW","CLIP_REASSIGN_CAMPAIGN"],"reviewerMode":"LIVE", …}}
```

### THE FAILURE, AS HE MEETS IT

```
GET /api/clips?status=PENDING            -> 200, 7 rows      canReassignCampaign TRUE on 0 of 7
GET /api/clips                           -> 200, 500 rows    canReassignCampaign TRUE on 0 of 500
```

**500 clips readable, 0 movable.** The campaign name becomes a button only when the server marks the row, so **the control renders on nothing at all**. There is no error, no message, no greyed-out option. Nothing.

**He cannot ever have seen it.** Since the grant he has reviewed **55** clips (`reviewer_audit_log`, `2026-08-21 03:32:33.565` to `2026-08-22 15:45:38.275`) and **0** belonged to one of his invitees. His `reviewer_audit_log` contains **no** `CAPABILITY_DENIED_403` and **no** `INVITEE_SCOPE_VIOLATION_404` before this round — he never reached the route, because there was no button to press.

### AND IF HE CRAFTS THE REQUEST ANYWAY — the part that made this unanswerable

```
GET  /api/admin/clips/<a PENDING clip in HIS OWN QUEUE>/reassign-campaign -> 404 {"error":"Clip not found"}
GET  /api/admin/clips/cmZZZZdoesnotexistatall/reassign-campaign           -> 404 {"error":"Clip not found"}
```

**A clip he is looking at, on his own screen, told him it does not exist.** That is BL-814's defect shape precisely: a refusal that names nothing is why the owner has to ask.

### THE PICKER DOES OPEN — for the two invitee clips inside his campaign scope

```
GET /api/admin/clips/<his invitee's APPROVED clip, Zhus Meme>/reassign-campaign -> 200
```

**So the capability gate is NOT the culprit.** The campaign-by-block matrix for that clip, from the live response:

| destination | verdict |
|---|---|
| SomeSome App | **BLOCKED** `CLIP_NOT_PENDING` + `CLIP_HAS_EARNINGS` + `CLIP_HAS_MONEY_ROWS` |
| Zhus Edit (0.50 CPM) | **BLOCKED** same three |
| Zhus Meme (0.20 CPM) | **BLOCKED** same three + `SAME_CAMPAIGN` |
| 11 further campaigns | not shown — outside his assigned set |
| 19 further campaigns | not shown — archived |

`reason: "Only a PENDING clip can be moved. This clip is APPROVED."` and `"This clip has already earned money (earnings 0.60)."`

### WHICH OF THE FIVE IT IS

Of the five the brief listed — the capability gate refusing, the scope filter finding nothing, all destinations blocked, a server error, or the UI not showing the control — **it is the second and the fifth, and they are the same fact seen from two sides.** The invitee scope filter finds nothing, so the UI shows no control. Not the capability gate (proven passing by a 200). Not a server error (no 500 anywhere in the round). Not the seven destination blocks (they never get consulted, because no clip reaches them).

---

## PART 2 — THE FIX: NAME THE BOUNDARY. WEAKEN NOTHING.

**Diff: 8 files changed, 368 insertions, 45 deletions, plus 2 new source files. No schema change. No block touched. No scope widened.**

### 1. `reassign-campaign/route.ts` — the 404 becomes a 403 **only when he is already looking at the clip**

BL-788's rule is that a clip a reviewer cannot see must never be confirmed to exist, and that rule is **kept intact**. What changes is the case it was never meant to cover: a clip his own queue **had just listed to him**.

```ts
const visibleInHisQueue =
  !isHisOwnClip &&
  inReadScope &&                       // clips/route.ts:340  campaign-list scope
  cutoff.inScope &&                    // clips/route.ts:410  BL-89 date cutoff
  statusReadable &&                    // clips/route.ts:398  BL-132 readable statuses
  isClipperInReviewerInviteeScope(…);  // clips/route.ts:357  BL-788 invitee read flag
```

Every clause mirrors one filter in `/api/clips`, in the same order, **through the same exported functions** — not a paraphrase. If all pass, the clip is on his screen and naming the reason tells him nothing he does not already hold. If any fails, the generic 404 stands, byte-identical.

```diff
-  return NextResponse.json({ error: "Clip not found" }, { status: 404 });
+  const named = isHisOwnClip
+    ? "Nothing was changed. You cannot move your own clip to another campaign."
+    : visibleInHisQueue
+      ? "Nothing was changed. You can move a clip to another campaign only for a clipper you invited, and this one was not invited by you."
+      : null;
+  return named
+    ? NextResponse.json({ error: named }, { status: 403 })
+    : NextResponse.json({ error: "Clip not found" }, { status: 404 });
```

**`"Nothing was changed."` leads both sentences.** The a11y review caught that the named 403 displaces the dialog's own fallback (`"The move failed and nothing was changed."`), so without it he would hear a rule where he used to hear an outcome.

**The audit row now carries the status it actually returned.** A new `INVITEE_SCOPE_VIOLATION_403` action sits beside the existing `…_404` (one additive line; the column is `text`, no schema change), so the owner's log can never record a 403 under a name ending in 404, and the two cases stay countable apart. Metadata gains `visibleInHisQueue`, `isHisOwnClip` and `httpStatus`.

### 2. `reviewer-capabilities.ts` — one shared `REVIEWER_READABLE_STATUSES`, replacing two copies

The whole safety claim above rests on the two rule sets agreeing. It was enforced by a comment. `["PENDING","FLAGGED"]` now lives once, in a file with no database import, imported by both. **The a11y review found this and it is the most load-bearing three lines in the diff:** a future edit to one copy would have caused either a leak or the unhelpful 404's return.

### 3. `/api/reviewer/move-scope` (new, read-only) + `lib/reviewer-move-scope.ts`

Two integers: how many clips are waiting for his decision, and how many of those are his invitees'.

**It is a separate route because measurement forced it.** The values were first put on `/api/clips`'s rich-mode envelope — and rich mode is gated on `isOwner` at `admin/clips/page.tsx:633`, so a **reviewer's** fetch takes the legacy path and returns a **bare array** with nowhere to hang a page-level field. Widening rich mode to reviewers would change how their whole list paginates. That is a different round, and the first attempt is recorded here rather than quietly deleted.

The counts are built from the **scope rules alone** — the self-authored exclusion, the campaign scope, the BL-788 invitee flag, the BL-89 cutoff — never from the loaded page and never narrowed by the search box or the filters. They are **`null`, never `0`**, when they cannot be taken.

### 4. `admin/clips/page.tsx` — one plain sentence, outside the list

Rendered as `<p>` with **no ARIA at all**, placed after the filters and **before** the loading/empty/list ternary so it survives the empty state, which is exactly when he needs it.

> You can move a clip to another campaign only for a clipper you invited. **None of the 23 clips waiting for your decision are theirs**, so there is nothing for you to move.

Four branches: check unavailable → *"We could not check which of these clips you can move. That is not the same as none."*; nothing pending; none of them his; and *n* of them his — and only that last one adds *"On those, the campaign name is a button."*, and only when a row on the page **actually carries the flag**, so the sentence and the DOM cannot disagree if the row-flag lookup failed.

### 5. `ReviewerCapabilityChecklist.tsx` — the owner learns it at grant time

A sibling paragraph under the existing state line — **not** an extension of it, for reasons in the a11y section:

> Right now they can move their own invitees' clips into the 3 campaigns you ticked above, and nowhere else.
> **Nothing of theirs is waiting to be moved today. That can change as soon as one of their clippers posts.**

`reach` gains `moveCandidates`, and the whole computation moved into one function called by **both** the GET and the PATCH, because the owner changes the tick list and the capability on this very card and a figure fetched once at mount would go stale on the exact action the card exists for.

**Two ticked campaigns are required for a non-zero count.** With one ticked, the only permitted destination is the campaign the clip is already on, and `SAME_CAMPAIGN` refuses it. One ticked campaign is a measured zero, not a small number.

**"could be moved", never "can move".** It is a necessary condition and BL-736's blocks can still refuse any of them.

### 6. `reassign-campaign-dialog.tsx` — two defects the a11y review found in the neighbourhood

The dialog's `aria-describedby` promised *"Pick the campaign this clip should have been submitted to"* even on a refused GET where no campaign will ever render; it now reads *"This clip cannot be moved. The reason is below."* And the GET path never bumped `errorSeq`, so a **second identical** refusal on the same mount was announced to nobody; it now bumps it exactly as the POST path does.

### WHAT WAS DELIBERATELY NOT DONE

* **No block was weakened.** `campaign-reassign.ts` is **byte-identical by blob OID `3e513702` on both refs**.
* **The invitee scope was not widened.** `isClipInReviewerMoveScope` still ignores `reviewerScopeInvitedOnly`; the two new reads of that flag decide only what he can already SEE.
* **The generic 404 was not removed** — only narrowed to the cases it was written for, proven by request in PART 4.
* **B12, a page-wide gap, was reported and NOT fixed.** `/admin/clips` calls `setLoading(true)` nowhere — the skeleton renders once and never again — so every search, filter, SSE refresh and Force Now replaces the entire list silently. It is a real WCAG 4.1.3 defect, it is pre-existing, and it is page-wide live-region work rather than this round's scope. This round is required only not to make it worse, which the no-ARIA sentence guarantees.

---

## PART 3 — IT IS NOT JUST HIM

**Every reviewer holding `CLIP_REASSIGN_CAMPAIGN` today: exactly one, `jdb001`.** Nobody else has been granted it.

**But the wall is not personal to him.** Every live reviewer, measured, with the count each would see the moment the capability was granted:

| reviewer | mode | ticked campaigns | invitee-only | invitees | **movable today** |
|---|---|---|---|---|---|
| `cmoagb7e` (jdb001) | LIVE | 3 | false | 27 | **0** |
| `cmp9d0xu` | TRIAL | 1 | **true** | 2 | **0** |
| `cmpod0dh` | LIVE | 1 | false | 1 | **0** |
| 10 `bl89-*` dev/test seeds | TRIAL | 0 | false | 0 | **0** |

**Zero for all of them.** Granting this to anyone on the platform today produces exactly the same silence, and the two remaining real reviewers would additionally be stopped by having only **one** ticked campaign.

**The three LIVE-mode reviewers BL-802 deliberately left unscoped, verified untouched by this round:**

```
cmoagb7e  REVIEWER · LIVE · reviewerScopeInvitedOnly false · ACTIVE   (unchanged)
cmpod0dh  REVIEWER · LIVE · reviewerScopeInvitedOnly false · ACTIVE   updatedAt 2026-08-02 08:52:24.264, unchanged
cmovb0q6  CLIPPER  · BANNED — demoted and banned BY THE OWNER at 2026-08-20 18:20:27.702, disclosed by BL-815. Not this round.
```

---

## PART 4 — PROVED END TO END, BY DIRECT REQUEST

**The clip that was moved, named: `bl821-fixture-clip`.** Wholly synthetic, created `2026-08-23 21:48:28.567`, removed `22:27:41.234`. Its clipper, `bl821-fixture-clipper`, is `isTestUser = true` and was invited by jdb001 for those 39 minutes.

**Why a fixture and not a real clip.** The feature needs a clip whose clipper was invited by the acting reviewer. Measured: **there is not one in production.** Manufacturing one would mean writing `users.referredById` on a live account — the column deciding the 9%-versus-4% platform fee and the 5% referral mint. That is a money write and it was not made.

```
=== A. THE WALL AS THE OWNER FOUND IT — a PENDING clip on his own screen ===
REVIEWER GET  /api/admin/clips/cmt67p5y30…/reassign-campaign  -> 403
  "Nothing was changed. You can move a clip to another campaign only for a clipper you invited,
   and this one was not invited by you."
REVIEWER POST …                                                -> 403  (same sentence)

=== B. A CLIP HE CANNOT SEE, AND AN ID THAT DOES NOT EXIST — byte-identical ===
REVIEWER GET  /api/admin/clips/cmsgfdnwo0…/reassign-campaign  -> 404 {"error":"Clip not found"}
REVIEWER GET  /api/admin/clips/cmZZZZdoesnotexistatall/…      -> 404 {"error":"Clip not found"}
REVIEWER POST /api/admin/clips/cmsgfdnwo0…/reassign-campaign  -> 404 {"error":"Clip not found"}

=== C. A DESTINATION HE WAS NEVER ASSIGNED TO ===
REVIEWER POST destinationCampaignId=<not in his set>  -> 403 DEST_OUTSIDE_REVIEWER_SCOPE
  "You are not assigned to that campaign, so you cannot move a clip into it."

=== D. HIS OWN INVITEE'S PENDING CLIP — the picker opens ===
REVIEWER GET  /api/admin/clips/bl821-fixture-clip/reassign-campaign -> 200
  currentCampaign "Zhus Edit (0.50 CPM)"  currentClipperCpm 0.5  currentOwnerCpm null  ownerRatesVisible false
  outsideScopeHiddenCount 11   archivedHiddenCount 19   clipSideBlocks []
  OFFERED  SomeSome App             $0.50
  BLOCKED  Zhus Edit (0.50 CPM)     SAME_CAMPAIGN
  OFFERED  Zhus Meme (0.20 CPM)     $0.20

=== E. THE MOVE ===
REVIEWER POST destinationCampaignId=<Zhus Meme>  -> 200 {"success":true, from Zhus Edit 0.5, to Zhus Meme 0.2}
```

**The restamp, read out of the row afterwards:**

```
BEFORE  campaign Zhus Edit (0.50 CPM)   clipper stamp 0.5000   owner stamp 0.3197   PENDING   earnings 0
AFTER   campaign Zhus Meme (0.20 CPM)   clipper stamp 0.2000   owner stamp 0.1279   PENDING   earnings 0
```

Both stamps written inside the **same** `clip.update`, in the **same** single transaction, so the rates agree by construction. Everything under the gate is the code BL-736 and BL-740 shipped, unchanged.

**Every surface agrees:** the clip row, the `campaign_accounts` membership created inside the transaction, both audit tables and the clipper notification all read the destination.

### THE AUDIT ROW, AND WHERE THE OWNER SEES IT

```
reviewer_audit_log  CLIP_CAMPAIGN_REASSIGNED  reviewerUserId=cmoagb7e…  firedAt 2026-08-23 21:49:17.46+00
  clipId bl821-fixture-clip
  {"platform":"Instagram","fromCampaignName":"Zhus Edit (0.50 CPM)","toCampaignName":"Zhus Meme (0.20 CPM)",
   "oldClipperCpm":0.5,"newClipperCpm":0.2,"oldOwnerCpm":0.3197,"newOwnerCpm":0.1279,
   "clipperUserId":"bl821-fixture-clipper","requestRoute":"POST /api/admin/clips/[id]/reassign-campaign"}
```

**Him, the clip, both campaigns and both rate pairs.** Asked as the OWNER: `GET /api/admin/users/cmoagb7e…/reviewer-activity` → **200**, the move at the top of the list, and it is visible on his profile page under "Recent reviewer activity" in the 1440 render.

**Both refusal shapes are audited too**, so an attempt leaves a trace rather than vanishing:

```
INVITEE_SCOPE_VIOLATION_403  clip cmt67p5y30…  {"campaignScope":true,  "visibleInHisQueue":true,  "httpStatus":403}
INVITEE_SCOPE_VIOLATION_404  clip cmsgfdnwo0…  {"campaignScope":false, "visibleInHisQueue":false, "httpStatus":404}
```

### THE BLOCKS, EACH SEEN REFUSING ON THIS BUILD

Ten codes observed refusing a live POST, plus two more:

```
409 CLIP_NOT_PENDING + CLIP_HAS_EARNINGS + CLIP_HAS_MONEY_ROWS   (his invitee's real APPROVED clip)
409 SAME_CAMPAIGN                    "The clip is already on this campaign."
409 DEST_PAST                        "Hapday has ended. A clip moved there can never earn."
409 DEST_PAUSED + DEST_PLATFORM_NOT_ACCEPTED   (BAD BITCH ANTHEM 2.50, TikTok-only, Instagram clip)
409 DEST_ARCHIVED                    "…is archived. A clip moved there could never be approved or earn."
409 CLIPPER_ACCOUNT_NOT_APPROVED + DUPLICATE_URL_IN_DEST   (fixture put into both states)
409 DEST_DAILY_LIMIT_REACHED         "This clipper has already used their 0 clip limit on SomeSome App today."
404 DEST_NOT_FOUND                   "That campaign could not be found."
403 DEST_OUTSIDE_REVIEWER_SCOPE      (as the REVIEWER, checked BEFORE the campaign lookup)
```

`DEST_ARCHIVED` is the one showing the list filter is not a relaxation: archived campaigns are hidden from the picker and the POST still refuses one by name. `DEST_OUTSIDE_REVIEWER_SCOPE` firing **before** the lookup is why an unknown campaign id and an out-of-scope one cannot be told apart.

**THREE BLOCKS WERE NOT DEMONSTRATED AND ARE NOT CLAIMED.** `DEST_ERA_WOULD_FREEZE`, `DEST_OVER_BUDGET` and `DEST_NO_CPM_FOR_PLATFORM` fire on no live campaign today, and manufacturing any of them would mean editing a real campaign's boundary, budget or rates. They are asserted against the untouched rule set, and BL-740 measured them firing. BL-815 hit the same wall on two of the three.

### THE MONEY, BEFORE AND AFTER

| | `21:42:03` (before) | `22:33:48` (after) |
|---|---|---|
| earnings-invariant violations | **0** | **0** |
| payout_requests rows | **189** | **189** |
| newest payout `updatedAt` | `2026-08-23 13:54:54.914` | **identical** |

**No payout was created, modified, approved or cancelled.** No clipper's earnings fell. No real clip changed status, campaign or earnings.

### THE FIXTURE'S REMOVAL, AND ONE PROTECTION WORKING

```
users        bl821-fixture-clipper   isDeleted true,  referredById NULL
clips        bl821-fixture-clip      isDeleted true
clip_accounts bl821-fixture-acct     REJECTED
campaign_accounts / notifications / clip_limit_overrides   0 rows
jdb001's invitees                    27   (back to his true count)
reviewer_audit_log rows for the fixture  5  — KEPT
```

**A hard delete is impossible, and that is a protection working.** `reviewer_audit_log` is append-only (BL-87 immutability trigger) and the reviewer's moves wrote rows into it that a cascade would have removed. The trigger was **not** defeated to tidy a test fixture. `referredById` is cleared explicitly, because it is the only field on the fixture pointing at a real account and leaving it would have shown jdb001 28 invitees forever.

**Two of the five moves were made in the reverse rate direction** (Zhus Meme 0.20 → SomeSome App 0.50, owner 0.1279 → 0.25), so the restamp is proven both up and down.

---

## PART 5 — RENDERED, AND MERGED

### The render pass, with the viewport MEASURED

**The reviewer's screens are rendered as the REAL jdb001**, not as a dev stand-in. That is not a nicety: `use-effective-session.ts` says in its own header that a dev-bypass session carries `reviewerCapabilities` as `[]` on purpose, so a capability-gated surface can **never** render under dev auth — the trap BL-793 recorded.

**And it forced a two-server pass, which is worth recording.** `app-layout.tsx:314` reads `isAuthenticated = isDevMode ? !!devRole : status`, so while `DEV_AUTH_BYPASS` is on the shell ignores a real session entirely and bounces to `/dev-login`. The reviewer's screens were therefore rendered against a server with the bypass **off**; only the owner's card used the dev-auth server. Next allows one dev server per directory, so the two passes ran in sequence.

```
reviewer-clips-note / trigger / picker / confirm   320 375 414 1280 1440   20 shots
owner-move-card (fixture present, "1 could be moved")               5 shots
owner-move-card (fixture gone, the TRUE state)                      5 shots
reviewer-clips-note (fixture gone, the TRUE state)                  5 shots
ALL 35 SHOTS AT THE ASKED WIDTH (measured == asked, every one). No horizontal overflow anywhere.
```

**Read at 320:** the disclosure wraps to three lines, sits above an empty list, and still says *"1 of the 24 clips waiting for your decision is theirs"* — surviving the empty state is the whole reason it lives outside the ternary. **Read at 375:** the reviewer's confirmation with Clipper / Account / Currently on / Current clipper rate `$0.20` / Current owner rate **Not shown to you**, "Move to (2 available)", the exclusion sentence naming 11 campaigns, all four labelled rates, the immediacy warning and *"The clipper is told about this move either way."* **Read at 1280 as jdb001 himself:** *"You can move a clip to another campaign only for a clipper you invited. **None of the 23 clips waiting for your decision are theirs**, so there is nothing for you to move."* **Read at 1440 as the owner:** the move block ending *"Nothing of theirs is waiting to be moved today. That can change as soon as one of their clippers posts."*, with five `CLIP_CAMPAIGN_REASSIGNED` rows below it under "Recent reviewer activity".

The PNGs are deliberately not committed (35 files); the harness that regenerates them is.

### Merged and pushed

| | |
|---|---|
| clean `tsc` baseline on the untouched worktree, **before any edit** | `npm ci` exit **0**, `npx prisma generate` exit **0** (before tsc, because `npm ci` wipes the client), `npx tsc --noEmit` exit **0**, `grep -c "error TS"` = **0** |
| branch | `checkpoint/BL-821` @ **`e5bd62ef`**, VERIFIED on origin by `safe-push` |
| merge commit | **`4ea1c139`**, `origin/main` verified by `safe-push` |
| conflicts | **none**; main never moved from `b9a288cc`, and the **merged tree OID equals the branch tree OID exactly** (`ecb4b94e`), so the branch's green build IS the merge's build |
| BACKLOG | **162 sections before, 163 after**, `BL-821` ×2, **0 conflict markers**, counted with `grep -c` and never piped to `head` |
| **`checkpoint/BL-723`** | **confirmed NOT an ancestor of main** |
| files | 8 modified, 2 new source files, 6 fixture SQL files, 4 harness scripts |
| worktree `C:/w821` | **removed**, 0 node processes left behind |

> **A REDEPLOY ON RAILWAY IS REQUIRED.** Main carries the fix; production still shows him nothing.

---

## THE ACCESSIBILITY REVIEW, RUN BEFORE ANY UI WAS WRITTEN

The lead and two specialists reviewed the **design**. **Twelve blocking items. Every one was implemented rather than argued with.** The ones that changed the work:

**Two of them were CORRECTNESS defects, not styling.** The disclosure count was going to be derived from `filteredClips`, a client post-filter over one page — so it would have rewritten itself on every scroll and stated a different claim each time. And it was going to be derived from `canReassignCampaign`, where *"not yours"*, *"no capability"* and *"the lookup threw"* all collapse into one falsy value, so **an unmeasured input would have rendered as a measured refusal** — telling a reviewer he can move nothing when the truth is that nobody checked. Zero is the finding this entire round is about. Both now come from the server with an explicit `UNAVAILABLE` state and a `null`-not-`0` contract.

**A third: the row flag tests ONE gate but the route requires THREE.** Naming the invitee rule as the reason would have been a guess whenever campaign scope or the date cutoff was the real refusal. The count is now built from a query that already contains the other two gates, so the invitee rule is provably the only one left that can separate the two numbers.

**The owner's sentence was NOT allowed to extend `moveStateId`.** That paragraph is the grant button's `aria-describedby` and is re-spoken on every deliberate focus return; doubling its length would bury the destination rule in an interruptible tail. **This file states the principle itself at `:508-513`** — *"carrying NO ARIA at all: a description would re-read 70 words on every focus… The heading is what makes it findable"* — and the review quoted it back. A sibling paragraph with no ARIA, findable through the existing `h4`.

**And it must not restate the invitee count.** That number already renders once on the card, over a **different** set. A second "27" would be two figures about the same 27 people that can disagree.

**No live region on the disclosure.** Six things reset that list — a 300 ms search debounce, the campaign checkboxes (both a post-filter and a fetch dependency, so one tick fires it twice), an SSE refresh and Force Now — two of them unprompted. A live region would speak on mid-word typing pauses and would reach the reviewer **before** BL-816's append announcement that caused it, and could coalesce with it and drop a measured count that was built on purpose.

**Two live defects in neighbouring code**, both fixed here: the dialog's description promised a picker on a refused GET, and a repeated identical GET refusal was announced to nobody.

**`moveCandidates` was going to go stale** on the exact control the card exists for, and *"so they can move those"* would have promised something the server can still refuse. Re-read from the PATCH; the words are *"could be moved"*.

**Reported, NOT fixed:** the page-wide silent list replacement (B12, its own round); `role="alert"` doubling as an `aria-describedby` target in both confirmation panels; `aria-expanded` being removed rather than changed on a successful grant; two near-duplicate button names in the move section; and a dead `phraseMatchId`.

---

## GATES, HONESTLY

* **eslint confirmed present**, `v9.39.4`, so the hooks gate is a real check and not a silent no-op.
* `npx tsc --noEmit` exit **0**, `grep -c "error TS"` = **0**, run eight times across the round, the first on the **untouched** worktree so no error could be misattributed.
* `npm run build` **three times**, each written to a log with the exit code echoed by hand and **never piped through `tail`**: **`BUILD1_EXIT=0`**, **`BUILD2_EXIT=0`**, **`BUILD3_EXIT=0`** (the last post-commit). Prebuild clean every time: `check:prisma-bypass` **0 violations**, `check:removed-fields` **OK across 734 files**, hooks gate **11 problems (0 errors, 11 warnings)** — at the ceiling of 11 with **zero added**.
* `scripts/bl815-verify.ts`: **112 passed, 0 failed** against the changed tree. `scripts/test-reviewer-permissions.ts`: **55 passed, 0 failed**.
* Counted with `grep -c`, **never piped through `head`**. **No heredocs** were used to write any file. One shell at a time.
* **No Apify actor was run.** Nothing in `apify.ts` or the 11 BL-678 guards was touched.
* **`safe-push` refused once and was right to.** The first attempt ran from the main repo, whose HEAD was `b9a288c`, and it reported `COMMITS ARE STUCK LOCALLY`. Re-run from the worktree it verified `e5bd62e`. The guard did its job; the operator error is on the record.
* **Zero Supabase pool errors across all seven dev-server runs** (`grep -ci "Too many database connections"` = 0 on every log). BL-815 caused four such errors on the owner's live session; this round caused none, and each server was stopped between phases.

---

## WHAT COULD NOT BE PROVEN, AND WHY

* **jdb001 himself has not pressed the button.** The flow is proven end to end against a synthetic clipper he really did invite, by real HTTP requests through the real route as his real session — not by a person clicking in production.
* **Nothing was verified against production over HTTP** beyond the five unauthenticated deploy probes in PART 0. Every other request ran locally against the merged tree, pointed at the production database.
* **`DEST_ERA_WOULD_FREEZE`, `DEST_OVER_BUDGET` and `DEST_NO_CPM_FOR_PLATFORM` were not observed refusing**, for the reasons in PART 4.
* **A real screen reader was not run.** DOM order, roles, live regions and focus behaviour are reasoned and measured; NVDA, JAWS and VoiceOver were not.
* **The owner's card renders under the dev-auth session**, so it is `Dev Owner`'s view of jdb001's profile, not the owner's own login.

---

## WHAT THE OWNER SHOULD DECIDE NEXT

1. **The feature is dormant, not broken, and one tick fixes it.** His 27 invitees post into **bees.n.honey (270 clips)**, **somesome (100)** and **WinGram (91)** — none of which he is assigned to. Tick one of those and he can move his invitees' clips there the moment one goes pending. Leave it as it is and the feature waits for one of his 27 to post into Zhus Meme, Zhus Edit or SomeSome App.
2. **Two ticked campaigns are the floor.** With one, the only permitted destination is the campaign the clip is already on, and `SAME_CAMPAIGN` refuses it. The card now says so.
3. **His read scope is much wider than his move scope, and that is deliberate.** 500 clips readable against 0 movable today. Turning on *"Only clippers they invited"* for him would make the two match — and would shrink his review queue from 23 pending clips to 0, which is almost certainly not what you want.
4. **The other two real reviewers would hit the same wall**, and both additionally have only one ticked campaign. Fix that before granting either of them this capability.
5. **The page-wide silent list replacement (B12) deserves its own round.** Every search, filter and refresh on `/admin/clips` swaps the whole list with no announcement at all.
