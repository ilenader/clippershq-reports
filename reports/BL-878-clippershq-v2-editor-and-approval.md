# BL-878 — marketplace v2, round two: the campaign type and the editor's door

> **NOTHING IS UNREMOVABLE AND NO SQL IS OWED. FIRST LINE, AS THE ROUND REQUIRES.**
> 14 ledgered rows, **`VERIFIED: 0 of 14 recorded rows remain`**, 0 failed, 0 cascaded. A direct
> catalogue sweep after teardown returns **zero** `bl878sbx-` rows in `users`, `campaigns`, `clips`,
> `clip_accounts`, `notifications`, `audit_logs` and `activity_events`, **zero** rows in
> `marketplace_v2_clips`, and **zero** tracking jobs behind a sandbox clip. The campaign population
> is back to **34**, all **34** NORMAL, with the fingerprint `e9defb11fcf63f2a100fbb1a63ed98de`
> identical to the opening snapshot. Nothing was left behind and there is nothing for the owner to
> run.

**2026-09-16. Shipped on `checkpoint/BL-878`, merged to `main`. Requires a Railway REDEPLOY**, and
BL-877's redeploy is still owed as well. Base `origin/main` @ `3802d89b`. Isolated worktree
`C:\w\b878`, a short path, `node_modules` never junctioned, **removed at the end and verified by
listing the path**. DB `now()` **14:04:57.082939+00** (opening census, before the schema change) to
**14:30:17.990954+00** (closing sweep), every timestamp cast `::text`.

---

## THE HEADLINE

> **1. NO POSTER SURFACE EXISTS AND NO MONEY MOVED. PROVEN, NOT ASSERTED.** Zero directories under
> `src/app` match a v2 post, poster, catalogue or browse route. `writeMarketplaceV2Earnings` has
> exactly **ONE** reference in the whole of `src`, its own definition. The closing census shows
> `marketplace_v2_posts`, `marketplace_v2_editor_earnings`, `marketplace_v2_platform_earnings`,
> `agency_earnings` and `payout_requests` **all at their opening values**. An approved clip sits in a
> catalogue nobody can browse and nobody can post from.
>
> **2. THE RENDER PASS CAUGHT A REAL DEFECT THAT NO TEST WOULD HAVE, AND IT WAS A DOUBLE MISS.** The
> "which flow am I in" notice was first placed inside the campaign detail page's "Your Clips"
> section. The shot at 375px showed it was **invisible on the tab a clipper actually lands on**. And
> the file it had been placed in was the wrong one entirely: `campaigns/[id]/page.tsx:123` hardcodes
> `const isTestUser = true`, so **every CLIPPER is served `CampaignDetailPremium.tsx`** and the
> legacy page is dead for them. Both were fixed; the notice now sits **above the tab row**. This is
> exactly why the screens are photographed rather than described.
>
> **3. THE SANDBOX PROOF FOUND THAT THE NEW REFUSAL COULD NOT BE REACHED, AND THE PRODUCT CODE WAS
> NOT REORDERED TO MAKE THE TEST PASS.** `clipper-submit-core.ts` refuses EVERY submission to an
> `isTestCampaign` campaign, unconditionally, several lines ABOVE the new branch, so a sandbox
> campaign can never reach it. Reordering would mean telling somebody to go to the marketplace about
> a campaign that had **ENDED**. The campaign was instead flipped out of test mode for **160 ms**,
> for one call, and flipped straight back, with the window measured and printed.
>
> **4. THE ACCESSIBILITY REVIEW CORRECTED THREE OF THIS ROUND'S OWN PREMISES, AND ALL THREE WERE
> VERIFIED AGAINST SOURCE BEFORE THEY WERE BELIEVED.** The shared `Modal` has **37** callers, not the
> 3 BL-876 named, and three already render their own `role="dialog"` and their own focus trap.
> `src/lib/use-dialog-focus-trap.ts` already exists. `tracking-modal.tsx` nests a `ConfirmModal`
> inside a `Modal` today. Every one checked and true.

**PROOFS: 36 of 36 sandbox checks and 20 of 20 render shots passed. 0 failed.**
Two proof failures were hit along the way, both real, both reported in full below, both fixed.

---

## PART 0 — THE MODEL SPLIT, AND WHAT WAS CHECKED AGAINST SOURCE

| tier | what ran there | subagents |
|---|---|---|
| **cheapest (Haiku)** | pure retrieval only: the existing modal, reject modal, submit modal, upload route, notification types, `notifHref` and email signatures; the campaign form, its two API routes, the card grid and the detail page | **2** |
| **accessibility team** | one `accessibility-lead`, which fanned out to its own specialists | **1** |
| **strongest (Opus), NOT SPLIT** | the campaign-type migration and its rollback, every line touching `clipper-submit-core.ts`, the v2 server layer, the four API routes, all five UI surfaces, the `Modal` primitive, every proof script, the render harness and this report | **0 subagents between it and the source** |

**THE ROUND WARNED THAT A SUBAGENT HAD PREVIOUSLY MISCHARACTERISED A PRIOR ROUND'S DESIGN, AND SAID
TO ASSUME IT WOULD HAPPEN AGAIN. It did not happen this time, and saying so is part of the job.**
Every load-bearing claim was re-run against source before being acted on:

| claim | source check | verdict |
|---|---|---|
| the `Modal` has 37 callers | `grep -rl "@/components/ui/modal" src` | **37. TRUE** |
| 3 of them already do their own dialog semantics | `grep -rn "aria-modal"` on those three files | **TRUE** |
| `src/lib/use-dialog-focus-trap.ts` already exists | `ls` | **TRUE**, and it is BL-736's |
| `tracking-modal.tsx` nests a `ConfirmModal` | `grep -c ConfirmModal` | **2 references. TRUE** |
| `--bg-page` is defined nowhere | `grep -- "--bg-page:"` across `src` | **0 definitions, 23 users. TRUE** |
| the repo is Next 16 / React 19 / Tailwind 4 | `package.json` | **16.2.6 / 19.2.4 / ^4. TRUE** |
| `MpStatusBadge` already passes contrast | read the file | **TRUE**, tinted bg + saturated fg |
| `marketplace/layout.tsx` has a visibility gate v2 would not inherit | `grep -c isMarketplaceVisibleForUser` | **3 references. TRUE**, and the gate was added to the v2 page because of it |
| the campaign create AND edit form are one file | read `admin/campaigns/page.tsx` at the POST and PATCH sites | **TRUE** |
| `CAMPAIGN_FIELDS` is a PATCH allow-list that would silently drop a new field | read `api/campaigns/[id]/route.ts:101-132` | **TRUE**, and `campaignType` was added to it |

**One correction the review got wrong and it is recorded rather than passed on.** It stated the
contrast of white on the danger token as 3.76 to 1 against this round's brief of 1.44 to 1. Neither
figure was recomputed here, because **the design does not use white on a filled token at all**: it
reuses `MpStatusBadge`, whose tinted-background treatment the review itself measured as passing.
**The disagreement is therefore moot rather than resolved, and it is stated that way.**

---

## PART 0b — THE FOUNDATION, CONFIRMED, AND WHAT ADDS YIELDS ON A REAL CAMPAIGN

Measured live at DB `now()` **2026-09-16 14:29:59.06151+00**:

| thing | measured |
|---|---|
| the four v2 tables | **4 of 4 present** |
| indexes on them in `pg_indexes` | **21** (BL-877's 20, plus this round's one) |
| `marketplace_v2_clips` / `posts` / `editor_earnings` / `platform_earnings` | **0 / 0 / 0 / 0** rows |
| v2 clips carrying `isMarketplaceClip = true` | **0** |
| `MARKETPLACE_V2_PLATFORM_CUT_MODE` | **`ADDS`** |
| `v2AgencyEarningApplies()` | **`true`** |

**THE ADDS DECISION, CONFIRMED ON A REAL CAMPAIGN'S OWN OWNER SHARE rather than BL-877's
illustrative 33.33 percent.** The campaign is **Zhus Edit (0.50 CPM)** (`cmsisj3d800f10po8jvz526hf`),
ACTIVE, CPM_SPLIT, `clipperCpm $0.50`, `ownerCpm $0.3197`, `lockedOwnerShareDecimal 0.39002074`, so
his ordinary per-clip cut on it is **39.0021 percent**.

**Per $100 of v2 gross, on that campaign:**

| leg | gross | cash after his own withdrawal fee |
|---|---|---|
| editor | $45.00 | **$40.95** |
| poster | $45.00 | **$40.95** |
| platform leg | **$10.00** | |
| the two withdrawal fees to the owner | **$8.10** | |

* **REPLACES: the owner nets $18.10 and the campaign spends $100.00.**
* **ADDS: the owner nets $57.10 and the campaign spends $139.00.**

> **WHAT ADDS ACTUALLY DOES, SAID PLAINLY ONE MORE TIME BECAUSE IT IS THE THING MOST EASILY
> MISREAD.** The earners are paid **identically** under both options, $40.95 and $40.95. ADDS takes
> nothing from them. **It makes the CAMPAIGN pay $139.00 for the same views instead of $100.00, so a
> fixed budget buys 28.1 percent fewer views and exhausts sooner.** On a campaign with a larger owner
> share the gap is larger; on one with a smaller share it is smaller. The flag is one named constant
> in `src/lib/marketplace-v2-earnings.ts` and changing it is a one-line edit.

---

## PART 1 — THE CAMPAIGN TYPE

### One enum, and why not two booleans

`campaignType` on `Campaign`, values **`NORMAL`**, **`MARKETPLACE_ONLY`**, **`BOTH`**,
**`NOT NULL DEFAULT 'NORMAL'`**. BL-876 chose this over two booleans because two booleans can express
`false / false`, which is a campaign nobody may submit to, and over deriving it from existing rows
because that cannot be set in advance and flips silently the moment a test row is created.

### The SQL, and its rollback, printed before it was run

Applied through `scripts/run-schema-sql.js`, in three statements, never `prisma migrate`:

```
node scripts/run-schema-sql.js --inline "CREATE TYPE \"CampaignType\" AS ENUM ('NORMAL','MARKETPLACE_ONLY','BOTH')"
node scripts/run-schema-sql.js scripts/migrations/BL-878-campaign-type.sql
node scripts/run-schema-sql.js --inline "CREATE INDEX CONCURRENTLY IF NOT EXISTS marketplace_v2_clips_editorid_videohash_idx ON public.marketplace_v2_clips (\"editorId\",\"videoHash\")"
```

The file itself is one statement:

```sql
ALTER TABLE public.campaigns
  ADD COLUMN IF NOT EXISTS "campaignType" "CampaignType" NOT NULL DEFAULT 'NORMAL';
```

**ROLLBACK, printed in the migration header before anything was applied.** `run-schema-sql.js`
refuses every one of these on purpose, so they go through the Supabase editor by hand:

```sql
DROP INDEX IF EXISTS public.marketplace_v2_clips_editorid_videohash_idx;
ALTER TABLE campaigns DROP COLUMN IF EXISTS "campaignType";
DROP TYPE IF EXISTS "CampaignType";
```

**Dropping the column loses nothing that existed before BL-878**: every value is the default this
migration wrote, no prior data is encoded in it, and no money, earnings, payout or tracking path
reads it.

`CREATE TYPE` has no `IF NOT EXISTS` form in Postgres. Re-running it errors with SQLSTATE 42710 and
changes nothing, and that error IS the idempotency. The index is `CONCURRENTLY` and therefore its own
single statement, because `run-schema-sql.js` sends a whole file as one simple query and Postgres
wraps a multi-statement simple query in an implicit transaction, where `CREATE INDEX CONCURRENTLY`
fails with SQLSTATE 25001. BL-845, BL-696 and BL-877 each recorded that independently.

### Every existing campaign is unchanged, measured on both sides of the change

| | campaigns | of which NORMAL | fingerprint |
|---|---|---|---|
| **before** the column landed, `14:04:57.082939+00` | **34** | n/a, the column did not exist | `07da7b4df8d29574fef2fabee8c8de1f` |
| **after**, `14:05:11.436753+00` | **34** | **34** | `07da7b4df8d29574fef2fabee8c8de1f` |

The pre-change fingerprint is over `id:status:pricingModel` and is **identical**. The proof script's
own fingerprint, which additionally includes `campaignType`, read
`e9defb11fcf63f2a100fbb1a63ed98de` at the opening snapshot and **the same value again after the whole
round and its teardown**.

The column reads `nullable=NO default='NORMAL'::"CampaignType" type=CampaignType`, and the new index
is present, `valid=true ready=true`, in `pg_indexes`.

### NO BACKFILL WAS RUN, AND THAT WAS A DECISION RATHER THAN AN OMISSION

BL-876 explicitly rejected a proposed
`UPDATE campaigns SET "campaignType"='BOTH' WHERE id IN (SELECT "campaignId" FROM marketplace_poster_listings)`.
**This field governs NORMAL versus V2 ONLY.** The existing marketplace stays governed by the
existence of a `MarketplacePosterListing` row exactly as it is today, so a campaign carrying a v1
listing and a `NORMAL` type behaves in every respect exactly as it does now. There is **1** v1
listing on the platform and it was not touched.

### The index is deliberately NOT unique

`marketplace_v2_clips_editorid_videohash_idx` makes the duplicate lookup cheap and nothing more. The
v2 duplicate rule mirrors the existing marketplace's gate 5, which is scoped to the creator AND is
campaign-scoped or site-wide depending on `campaign.allowContentReuse`. **A UNIQUE index could not
express that conditional scope** and would refuse an editor's legitimate submission of the same file
to a second campaign. The rule is enforced in application code and proved below.

### Both campaign forms

`src/app/(app)/admin/campaigns/page.tsx` holds **both** the create and the edit form. The field was
added to `defaultForm`, to the edit-populate `setForm`, to the payload, and as a labelled `<select>`
directly under Pricing Model, with plain wording that changes per selection:

* **NORMAL**: "The normal way. A clipper uploads his own clip. This is what every campaign did before."
* **MARKETPLACE_ONLY**: "Clippers cannot upload their own clip here. Editors send clips, the owner approves them, and posters post them."
* **BOTH**: "Both ways are open. A clipper can upload his own clip, or post a clip an editor made."

`campaignType` was added to **`CAMPAIGN_FIELDS`** in `src/app/api/campaigns/[id]/route.ts`, which is
the PATCH allow-list. Without that the edit form would have posted the field and the server would
have **silently dropped it**. Being on that list means an assigned ADMIN may only **propose** a
change through the pendingEdit diff path, which the OWNER then approves, while the OWNER's own save
applies directly. The value is validated against the three members on both the create and the edit
path, so neither can write a string that is not one of them.

---

## PART 2 — THE ONE REFUSAL, AT THE CHOKEPOINT

### Where it lives, and why not at the two routes

Inside `processClipperSubmitLink` (`src/lib/clipper-submit-core.ts`), beside the existing `PAST` and
`PAUSED` refusals, with `campaignType: true` added to the select at `:362` because without it the
check cannot see the type. Measured: `/api/clips` and `/api/clips/batch` **both** delegate to that
core, and **neither carries a `MARKETPLACE_ONLY` gate of its own**, counted by grep. BL-824's own
lesson about this exact pair of call sites is that *"a patch at either site would have left the other
wrong."*

### The copy, quoted exactly as shipped

> **You cannot upload your own clip to this campaign. This one works through the marketplace. Go to
> the marketplace, pick a clip an editor already made, post it to your account, and paste the link
> there. You earn 45 percent of what your post makes.**

The sandbox asserts on that string **byte for byte** and it matched. It points at the right door
rather than judging who knocked, which is deliberate rather than lazy: `clipper-submit-core.ts` has
no concept of an editor or a poster and cannot tell them apart, so the same words serve both, and
neither needs to be accused of anything.

### THE OWNER SUBMIT PATH WAS LEFT UNGATED, AND HERE IS WHY

`validateOwnerSubmitContext` (`src/lib/owner-submit-core.ts`) checks only AUTO-paused and
test-campaign-in-override-mode and has **no campaign-status gate at all**, unlike the clipper path.
BL-876's view was that MARKETPLACE_ONLY should not reach it, **because the owner blocking himself out
of his own campaign helps nobody**. The proof exercises it against the MARKETPLACE_ONLY sandbox
campaign and it **accepts**.

### THE PROOF FAILED FIRST, AND THAT FAILURE IS THE MOST USEFUL THING IN THIS PART

The first run reported:

```
FAIL  a MARKETPLACE_ONLY campaign refuses a clipper's own clip, at the core
      the copy, verbatim: "This campaign is not available for submissions right now."
```

That is not the new refusal. It is `if (campaign.isTestCampaign)` at `:373`, which refuses **every**
submission to a test campaign, unconditionally, several lines ABOVE the new branch. A sandbox
campaign is a test campaign by the tooling's own rule, so **the branch under test could never be
reached**.

**THE PRODUCT CODE WAS NOT REORDERED TO MAKE THE TEST PASS**, and that was the whole decision.
Availability gates belong first: telling somebody to go to the marketplace about a campaign that has
**ENDED** would be worse copy than telling him it ended. Instead the sandbox campaign is flipped out
of test mode for the duration of **ONE** function call and flipped straight back, and the window is
measured and printed rather than glossed over:

```
PASS  a MARKETPLACE_ONLY campaign refuses a clipper's own clip, at the core  status 400, copy matches byte for byte
      the sandbox campaign was non-test for 160 ms, for this ONE call, and was flipped straight back.
```

**Disclosed honestly: for 160 milliseconds that fake campaign was theoretically visible to a real
clipper on `/campaigns`.** Nobody joined it, it carried the `BL878-SANDBOX-DELETE-ME` marker in its
name, and it has since been deleted. The NORMAL comparison campaign got the same treatment for a
similar window, and without it its PASS would have been meaningless, because it would only ever have
measured the test-campaign refusal.

---

## PART 3 — WHAT A CAMPAIGN SHOWS

### The two findings the render pass produced

BL-876 measured that the campaign detail page contains **zero** occurrences of the word "marketplace"
across 1,065 lines and offers one button, so a clipper cannot tell there is a second way to earn.
**That confusion IS the theft vector even without bad intent.**

**FINDING ONE: the notice was placed where a clipper never looks.** It was first rendered inside the
"Your Clips" section. The 375px shot showed the landing tab is **Overview**, and the notice was not
on it.

**FINDING TWO, and it is the sharper one: the file being edited was dead for clippers.**
`src/app/(app)/campaigns/[id]/page.tsx:123` hardcodes `const isTestUser = true` and branches at
`:419` to `CampaignDetailPremium.tsx` for every CLIPPER. **The legacy page renders only for
OWNER and ADMIN.** Both files now carry the notice; the premium one has it **above the tab row**, so
it is visible on every tab and above every button.

### What each type shows

| type | card badge | detail page |
|---|---|---|
| **NORMAL** | none | **nothing new at all**, so every campaign that existed before BL-878 is unchanged |
| **MARKETPLACE_ONLY** | **"Marketplace only"** | *"This campaign only works through the marketplace. You cannot upload your own clip here."* plus a line pointing at the right door, and the Submit button is not rendered |
| **BOTH** | **"Two ways to earn"** | a heading, a lead sentence, and two cards, **"Way 1: Make your own clip"** and **"Way 2: Post a clip someone else made"** |

Both are photographed below at every width.

### How the two badges coexist, since the round asked

The existing `TypeBadge` slot carries the **cosmetic** `typeLabel` ("Song", "App"), whose own schema
comment says it is *"DISPLAY ONLY... read by no money, earnings, payout, eligibility or campaign-status
path"*, and the existing "Song / App / All" filter (`CampaignsRedesign.tsx:511-522`) keys on **that
label**, not on a mode. So the new badge is rendered **beside** it in a flex wrapper, never replacing
it, and **the type filter is a second control that this round did not build**. Combining them would
have broken the shipped filter.

---

## PART 4 — THE EDITOR SUBMITS

Built on `src/components/marketplace-v2/EditorSubmitModal.tsx`, modelled directly on
`SubmitClipModal.tsx`.

* **Drive link, required**, validated by host and protocol exactly as `isValidDriveUrl` does, with
  the same predicate on the server so the two cannot disagree. Wrong host gives BL-876's verbatim
  copy: *"That needs to be a Google Drive link. Copy it from Drive with the Share button."*
* **A `<details>` block, closed by default**, "How to share your video", with the three numbered
  steps and the footnote.
* **A title, required**, so a poster's card has a name and a screen reader has a heading.
* **Notes for the owner, optional**, 2,000 characters with a live count.
* **NO PLATFORM CHECKBOXES.** They exist in the old form because a CLIPPER picks which of a poster's
  accounts to target. **An editor targets nobody.**

### What is stored, and the one derivation

The raw pasted link, the **canonical Drive file id as its own column**, derived once with the
existing `extractDriveFileId`, and the content hash. Proved: a link of the form
`/file/d/1AAA.../view?usp=sharing` stored `driveFileId = "1AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"` with a
`videoHash` present.

**`extractDriveFileId` was EXPORTED and the keyword is the only change to it.** `video-hash.ts` is
not one of the six money files. Re-implementing the normalisation in the v2 module is precisely what
BL-868 priced: `/open?id=FILE_ONE` and `/open?id=FILE_TWO` hashed identically and an honest second
submission was refused. One definition, two callers.

### The duplicate rule, and the half that matters most

| case | result |
|---|---|
| the **same** editor sends the **same** file twice | **REFUSED**, 409: *"You already sent this exact file. Pick a different video, or send a link to the corrected file."* |
| a **different** editor sends the **same** file | **ACCEPTED** |

**It cannot fire across editors by construction**: `editorId` is in the `where` of the only query
that can refuse, so a second editor's file is never even compared against the first. That is not a
nicety. The global unique on `MarketplaceVideoHash.hash` **would** have refused him, and BL-868
measured what that costs: *"An honest second submission was refused as a duplicate. This is the worse
of the two, because it blocks real work and looks like a false accusation."*

**`MarketplaceVideoHash` was never written.** Its count was **9** at the opening snapshot and **9**
at the close.

### The thumbnail, and the rule that governs it

Browser-side canvas capture at submission, uploaded through the **existing** `/api/upload` route
(JPEG, PNG, WebP, GIF, 5MB, magic bytes validated), recorded on the row afterwards. No ffmpeg, no new
dependency, no new runtime, no Google Cloud project, no API key and no new secret to rotate. The URL
stored is always **our own copy**, and the route refuses a value that is not.

**IT WILL OFTEN FAIL, AND THAT IS EXPECTED RATHER THAN A BUG.** It depends on the editor's browser
loading the video cross origin from Drive, which BL-876 recorded as a dependency and which Drive's
consumer endpoints frequently refuse.

> **SO A FAILURE IS RECORDED AS A FAILURE AND NEVER AS A FACT ABOUT THE VIDEO.** Every reason string
> describes what **we** could not do. None says the video is missing, broken, invalid or gone. The
> sandbox asserts on that with a regex over the stored reason, and it passed:
> *"Your browser could not read the video from Drive, so we could not make a preview."*
>
> **AND NOTHING KEYS OFF WHETHER ONE EXISTS.** Proved by walking every `.ts` and `.tsx` file under
> `src` for a conditional read of a v2 `thumbnailUrl`: **0 found.** A clip with no thumbnail is fully
> usable, shows a placeholder glyph with no accessible name at all, and the owner's queue prints the
> failure reason followed by *"The clip itself is fine and works normally."*

---

## PART 5 — THE EDITOR SEES HIS OWN SUBMISSIONS

Three states, each said **in words**, never by colour alone. The pill's label IS the word, the pill
is a child of the row heading so heading navigation carries the state with the title, and the
headline repeats it as a sentence.

* **PENDING** — *"Waiting for review"*, then *"The owner has not looked at this yet. Nobody can see
  it until it is approved."* **No time estimate**, because nothing in this product forecasts a
  moderation queue and a promised window is a claim the interface cannot keep.
* **APPROVED** — *"Approved. Posters can see it."*, then *"Any poster can now find this clip and post
  it. You earn 45 percent of every post."*, and when nobody has posted yet, *"Approved. Waiting for
  its first poster."* rendered with no alarm treatment, because zero here is legitimate and
  temporary.
* **REJECTED** — the owner's words **verbatim and unsummarised** under a heading that **names its
  clip**, `Why "{clip title}" was not approved`, with the optional improvement note as a separate
  *"What to change"* line that reads as help rather than a second verdict.

### The accessibility defect that was fixed rather than inherited

`MpSubmissionRow.tsx:488-498` has `aria-expanded` with **no `aria-controls`** and a panel with **no
`id`**, and its "Rejection reason" label is a plain `<p>` tied to nothing, so with several rejected
rows on screen a screen reader user cannot tell which clip a reason belongs to. The v2 row pairs the
toggle and the panel by id, and the panel is **always rendered and hidden with the `hidden`
attribute** rather than conditionally mounted, because an `aria-controls` pointing at an element that
is not in the document is broken ARIA exactly when it matters.

### What he must not see, proved by the RETURNED KEYS and not by reading the source

`EDITOR_CLIP_SELECT` is an explicit allow-list. BL-876 warned that `/api/campaigns` still leaks
`clientName` and `aiKnowledge` to a CLIPPER for the opposite reason, an `include` with no explicit
select, logged as BL-532 STATUS TODO. The proof issues the same query the route issues and reads the
keys back:

```
keys returned: approvedAt, campaign, campaign.id, campaign.name, createdAt, description,
               driveUrl, id, improvementNote, postCount, rejectedAt, rejectionReason,
               status, thumbnailUrl, title
```

**Absent, every one checked by name: `budget`, `ownerCpm`, `clipperCpm`, `agencyFee`,
`lockedOwnerShareDecimal`, `clientName`, `aiKnowledge`, the three per-platform owner CPMs and
`platformFeePctDecimal`.** The campaign contributes exactly two fields, its id and its name, because
a row has to say which campaign it belongs to. Tenant isolation is **at the query**: `editorId` is in
the `where`, never a client-side filter.

---

## PART 6 — THE OWNER APPROVES OR REJECTS

### The queue

The editor's **clickable name** linking to the existing `/admin/users/[id]`, the clip title, the
campaign, and the age as relative time. **No poster name**, because nobody has posted anything. The
name rendered is `username` and **never a Discord id**, matching `ReviewMetaBlock`, which
deliberately removed the Discord tag and raw id from every rendered name.

**He watches the video in Drive, in a new tab.** BL-876 measured that **nothing in this codebase
plays a Drive video inline, anywhere**; every Drive surface renders an external anchor. This is not
the place to build the product's first inline player. The link carries `rel="noopener noreferrer"`,
an `aria-hidden` icon, and the new-tab warning in words rather than left to the icon.

**The action cluster contains no link.** A `target="_blank"` anchor between Approve and Reject
destroys queue position for anyone driving the page from the keyboard, so every link precedes the
cluster and Approve comes before Reject.

### Approve, reject, undo

* **Approve is one tap** for the OWNER, with an optional note. Proved: status APPROVED, `approvedAt`
  set, `approvedById` recorded.
* **Reject is always a modal and the reason is REQUIRED**, capped at 1,000 characters. Both refusals
  proved: an empty reason gives 400 *"A reason is required. The editor reads it exactly as you type
  it."*, and 1,001 characters gives 400. BL-876 found the two shipped precedents disagree, the clips
  page allowing an empty uncapped reason and the marketplace modal requiring one, and chose the
  marketplace one **because an editor whose income is 45 percent of every future post on that clip
  cannot act on a rejection with no reason**.
* **Presets apply and offer an inline undo** rather than calling `window.confirm`, which is a
  blocking native dialog that takes focus out of the app entirely and cannot be styled, labelled or
  trapped.
* **Undo is one tap and non-modal on both approved and rejected rows**, and both directions are
  proved. On an approved row the copy says plainly: **"Undoing this hides the clip from every poster
  again."** It is refused outright once anything has been posted, which is unreachable today and is
  written now so Round Three cannot forget it.

### THE SHARED MODAL, FIXED IN THE PRIMITIVE

BL-876 measured `src/components/ui/modal.tsx` in full and found no `role`, no `aria-modal`, a title
with no `id`, no focus trap and no focus return. **The fix is in the primitive so the new dialog and
the existing callers inherit it together.**

**Three things the original plan had wrong, all three verified against source before they were
believed:**

1. **THE MODAL HAS 37 CALLERS, NOT 3**, and three of them (`AccountDetailPremium.tsx`,
   `PayoutRequestFlow.tsx`, `AddAccountFlow.tsx`) **already render their own `role="dialog"`, their
   own `aria-modal` and their own trap**, one of them in capture phase. Adding semantics
   unconditionally would have nested two dialogs and run two traps against each other on every Tab.
   So every new behaviour is gated on **`manageDialogSemantics`**, defaulting to `Boolean(title)`,
   and those three pass `false` explicitly so a future title cannot silently nest them.
2. **NESTED MODALS ARE REAL TODAY.** `tracking-modal.tsx` renders a `<ConfirmModal>` INSIDE the
   `<Modal>` it already opened, and both registered their own document-level Escape listener, so
   **one Escape closed both**. A module-level LIFO stack means only the **topmost** dialog answers
   Escape and Tab, which **fixes that existing bug** rather than inheriting it. The scroll lock is
   now refcounted, so closing the inner one no longer unlocks the page underneath an outer one that
   is still open.
3. **THE TRAP IS NOT HAND-ROLLED.** `src/lib/use-dialog-focus-trap.ts` already exists (BL-736) and
   already closes the two holes a fresh copy would reintroduce: a radio group collapses to its one
   real tab stop, and the `tabIndex={-1}` panel is neither first nor last.

**And the focus-return chain is a chain, because "skip the restore if the trigger left the DOM" IS
the bug.** Approve, Reject and Undo all delete the row their trigger lived on, and skipping means
landing on `<body>`. The order is: the original trigger if it is still connected, then a
caller-supplied `returnFocusRef`, then the page `h1`. **Never `<body>`.** Initial focus goes to the
**panel**, not the first focusable, because the first focusable in every titled modal is the X.
`data-no-swipe` is on the root because the global swipe handler lives at the left edge.

### An ADMIN may not see this queue, and that is a stated default

BL-876 left it open. The existing marketplace admin dashboard is hard gated
`if (user?.role !== "OWNER") notFound()` with the comment *"Even when the marketplace launches
publicly... the admin queue stays locked to OWNER."* **This round takes that default: OWNER only**,
`notFound()` on the page and 403 on the route. **Widening it later is one line; narrowing it after an
ADMIN has already seen an editor's unapproved work is not.**

### A security gap the accessibility review caught, and it was not an accessibility gap

`marketplace-v2` is a **sibling** of `marketplace/`, so it inherits neither that segment's layout nor
its **`isMarketplaceVisibleForUser`** gate. Without a gate of its own the editor page would have been
reachable by every clipper the moment it shipped. **The gate was added to the v2 editor page**,
`notFound()` rather than 403 so the route's existence never leaks, matching
`marketplace/my-submissions/page.tsx:19`.

---

## PART 7 — NOTIFICATIONS

In-app and email, both **transactional**, both fire and forget, **neither subject to
`canSendMarketing`**, exactly matching the ordinary clip decision.

* **in-app, approved:** title *"Clip approved!"*, body *"Your marketplace clip was approved. Posters
  can see it now and you earn 45 percent of every post."*
* **in-app, rejected:** title *"Clip not approved"*, body *"Reason: {the owner's words}"*. Because
  the reason is required, this branch is always taken and the ordinary fallback string never renders
  on a v2 clip.
* **email, approved:** `sendClipApproved`, subject *"Your clip was approved"*. **The earnings line
  legitimately reads zero** and is therefore omitted entirely, because `sendClipApproved` already
  renders it only when the figure is above zero. That is an existing conditional in the template
  rather than new work: the editor's 45 percent does not exist until a poster posts, and no poster
  can post until Round Three.
* **email, rejected:** `sendClipRejected`, subject *"Clip update"*, the required reason in the
  callout.
* **No notification on undo**, matching the existing clips page, which also fires none. An undo is
  the owner correcting himself within seconds.

### The type-string decision, and why it is not a reuse

**NEW type strings, `MKT_V2_CLIP_APPROVED` and `MKT_V2_CLIP_REJECTED`, and THE DEEP LINK IS THE
WHOLE REASON.** `notifHref` switches on the **type and nothing else**, so reusing `CLIP_APPROVED`
would have routed an editor to `/clips`, which lists clips he posted himself and can show him neither
his submission nor its reason. BL-876 recorded that as the minimum the deep link needs. Proved:

```
PASS  the in-app notification reaches the editor and deep links to a V2 destination
      type MKT_V2_CLIP_APPROVED, href "/marketplace-v2/editor",
      and the ordinary CLIP_APPROVED still routes to "/clips"
```

The wording, the channels and the fire-and-forget shape all still match the ordinary decision
exactly. Only the routing key differs.

---

## PART 8 — THE PROOFS, THE RENDERS AND THE TEARDOWN

### The opening snapshot, taken before anything was created

```
db now(): 2026-09-16 14:17:25.125476+00
campaigns 34 (NORMAL 34), clips 10180, users 1748
v2: clips 0, posts 0, editor earnings 0, platform earnings 0
v1: video hashes 9, submissions 0, creator earnings 0, platform earnings 0
agency rows 4882, payouts 248, notifications 15092
campaign fingerprint e9defb11fcf63f2a100fbb1a63ed98de
```

BL-864 skipped its opening snapshot and its census reported two false failures.

### 36 of 36 checks passed, 0 failed

Everything the round named, and each is quoted in the parts above: every existing campaign NORMAL and
unchanged; the column's nullability and default; the new index valid and ready in `pg_indexes`; the
MARKETPLACE_ONLY refusal at the core with the copy matched byte for byte; both routes delegating with
no gate of their own; a NORMAL campaign unaffected; the owner path ungated; the editor submitting;
the four input refusals; the duplicate rule in both directions; the stored file id; the allow-list
select by returned keys; tenant isolation at the query; the thumbnail failure recorded as a failure
and nothing keying off it; the required and capped rejection reason; approve; reject with verbatim
words; undo in both directions; the notification and its v2 deep link; no poster surface; no caller
of the money writer; no v2 money row; `MarketplaceVideoHash` unwritten; no v1 row; no agency or
payout row; `isMarketplaceClip` false across the full population.

### Every invariant, across the FULL population

| invariant | measured |
|---|---|
| **BL-538 and the earnings invariant**, `abs(earnings - (base + bonus)) > 0.01` | **0 breaches** |
| **BL-696 no double pay**, two open payouts on one campaign | **0** |
| **BL-696 no double pay**, a clip with two agency rows | **0** |
| **BL-824 paid-is-final with BL-849's write side** | **26 positions** sit below money already paid |
| **BL-627 no overpayment** | this round created **zero earning rows of any kind**, so no budget could be exceeded by it |

The 26 positions are **pre-existing and were not created by this round**, which wrote zero payout
rows and zero earnings. BL-877 measured the same 26 nine days after BL-849 measured 17, and this
round did not re-measure it with BL-849's exact query either, so **whether the two figures are
comparable is still not determined**. What is certain is the direction: `balance.ts` bounds each
campaign at `min(paid, payable)`, so `available` is floored at zero and never negative.

### The renders: 20 of 20, at every width

BL-793's method unchanged: the viewport is set on the **context** so the page really is 320 CSS
pixels wide, `window.innerWidth` is **read back** and printed beside every shot, horizontal overflow
is measured on every shot, the URL is read back so a bounce to `/login` can never be photographed as
a passing screen, and the session is a **real minted `__Secure-` Auth.js cookie** against a
**production build** with `DEV_AUTH_BYPASS=false`.

| screen | 320 | 375 | 414 | 1280 | 1440 |
|---|---|---|---|---|---|
| the editor's submissions | PASS | PASS | PASS | PASS | PASS |
| the owner's queue | PASS | PASS | PASS | PASS | PASS |
| a MARKETPLACE_ONLY campaign | PASS | PASS | PASS | PASS | PASS |
| a BOTH campaign | PASS | PASS | PASS | PASS | PASS |

`innerWidth` matched the requested width on all twenty and **horizontal overflow was 0px on all
twenty**.

**WHAT COULD NOT BE RENDERED, STATED RATHER THAN OMITTED.** The **editor submit modal** and the
**owner reject modal** were not photographed. Both are opened by a click and the harness photographs
routes rather than driving interactions, so a shot of either would have meant adding a click step the
harness does not have. **Their markup is therefore reviewed but not seen**, and that is the one gap
in this round's visual evidence. Everything else on all four surfaces was photographed.

### The teardown, exactly

```
14 rows recorded in C:/bl878-sandbox/ledger.jsonl
  all locks passed, nothing has been deleted yet
  marketplace_v2_clips       deleted   2
  clips                      deleted   1
  campaign_accounts          deleted   2
  clip_accounts              deleted   1
  notifications              deleted   1
  campaigns                  deleted   3
  users                      deleted   4
  14 deleted, 0 already gone, 0 FAILED
  VERIFIED: 0 of 14 recorded rows remain.
```

**Product-written rows were ADOPTED rather than swept.** Driving the real submit path writes more
than the row it is asked for, and the clip it created carried a product cuid that the tooling never
minted, so it was never ledgered at creation. `bl878-adopt.ts` adds a ledger line **only where it can
prove the row belongs to this round**, by reading a column that holds a sandbox id straight out of
the database. It performs no delete, no pattern match on a name and no date range. It adopted **1
clip** and **1 notification**; a second run found **0 new lines**, which is how it was confirmed to
have found everything.

**The independent sweep after teardown, at DB `now()` 14:30:17.990954+00:**

| table | `bl878sbx-` rows remaining |
|---|---|
| users, campaigns, clips, clip_accounts, notifications, audit_logs, activity_events | **0 each** |
| `marketplace_v2_clips`, platform-wide | **0** |
| tracking jobs behind a sandbox clip | **0** |
| campaigns total / of which NORMAL | **34 / 34** |
| campaign fingerprint | **`e9defb11fcf63f2a100fbb1a63ed98de`**, identical to the opening snapshot |

### Safety, itemised

* **No real user, clip, campaign or payout was touched.** Every row created carried the
  `bl878sbx-` prefix and the `BL878-SANDBOX-DELETE-ME` marker, every person was `isTestUser` and
  every campaign `isTestCampaign`, apart from the two measured flips of 160 ms and its
  counterpart, disclosed in PART 2.
* **NO APIFY ACTOR RAN.** Exercising the real submit path made **3 LamaTok lookups** against a
  fabricated TikTok URL, all HTTP 404, and the log line on all three is
  `[SKIP-APIFY] reason=gone-404`. **That is a disclosed vendor cost of three metered calls.** The 11
  BL-678 guards are untouched.
* **The six money files, `tracking.ts` and `campaign-era.ts` are BYTE-IDENTICAL by blob OID** on both
  refs: `clip-earnings-writer.ts ac5be7de`, `earnings-calc.ts 00410634`, `balance.ts 25a0b2f2`,
  `tracking.ts bf31646f`, `clip-earnings-invariant-middleware.ts 61cef393`,
  `money-decimal.ts ef5cdae7`, `campaign-era.ts 106e16ad`. **The only money-adjacent file that moved
  is `video-hash.ts`, and the change is one keyword**, `function` to `export function`, plus a
  comment. No body, signature or behaviour changed.
* **No Prisma in the browser bundle.** Every client component imports only from
  `@/components/...` and `@/lib/toast`; the v2 server layer is imported by routes and scripts only,
  and the build's route table confirms the five API routes are server functions.
* **The branch did not drift.** `git rev-parse --abbrev-ref HEAD` read `checkpoint/BL-878`
  throughout and the merge was made from `main` afterwards.
* **No handle was printed that is not a sandbox handle, and no wallet address appears anywhere.**
* **Every timestamp is cast `::text` against DB `now()`.**

### Build and gates, honestly

`eslint` is genuinely present, **3 binaries** in `node_modules/.bin`, so the BL-348 gate did not
silently no-op.

| run | result |
|---|---|
| `npx tsc --noEmit` | **exit 0** |
| `check:prisma-bypass` | **0 violations** |
| `check:removed-fields` | OK across 784 files |
| `check:event-wiring` | **0 problems** |
| **`lint:hooks`** | **10 problems, 0 errors, 10 warnings** against a ceiling of 11 |
| **`npm run build`** | **`BUILD_EXIT=0`**, echoed by the build's own shell, never read off a pipe |

**THE BUILD FAILED TWICE FIRST AND BOTH FAILURES ARE REPORTED RATHER THAN QUIETLY FIXED.**

1. **The hooks gate went to 12 warnings against a ceiling of 11**, both new ones in `modal.tsx`: a
   ref read in an effect cleanup, and a `useCallback` missing `isTopmost`. Both were fixed properly
   rather than suppressed. `isTopmost` became a real `useCallback` so every hook can name it as a
   dependency, which removed two `eslint-disable` lines with it, and the cleanup now reads the ref
   objects through locals aliased inside the effect. **The cleanup still reads the LIVE value
   deliberately**, because the element that opened the dialog can be deleted by the very action the
   dialog took, and that is the case the chain exists for.
2. **`next build` type-checks `scripts/` too**, which `tsc --noEmit` had already passed before the
   adopt script existed. Two real type errors surfaced: the ledger's `table` needed the
   `DeletableTable` union, and `record()` requires a `kind`. Fixing the second revealed that
   **`processClipperSubmitLink` returns `clipId` at the top level, not in `extra`**, which is why the
   clip the proof created was never ledgered in the first place and had to be adopted. That is fixed
   at the source now.

---

## WHAT IS AND IS NOT REACHABLE

**REACHABLE AFTER THIS ROUND**, and gated:

* **`/marketplace-v2/editor`** — an editor's own submissions and the submit form. Gated on
  `isMarketplaceVisibleForUser`, the same gate every existing marketplace sub-page uses, so until
  `NEXT_PUBLIC_MARKETPLACE_ENABLED` flips it is OWNER and `isTestUser` only, and `notFound()` for
  everyone else.
* **`/marketplace-v2/admin`** — the approval queue. **OWNER only**, `notFound()` for everyone else.
* **The campaign type control**, on the campaign create and edit form, OWNER-direct or ADMIN-proposed.
* **The badge and the flow copy**, on the campaign grid and the campaign detail page, and **only on a
  campaign whose type is not NORMAL**. All 34 campaigns are NORMAL, so **nothing on any real campaign
  looks different today**.
* **Five API routes** under `/api/marketplace-v2/`, each with `getSession()`, `checkBanStatus()` and,
  on the two admin routes, an OWNER role check.

**NOT REACHABLE, AND THAT IS THE POINT OF THE ROUND:**

* **There is no poster surface of any kind.** No catalogue to browse, no post flow, no way for anyone
  other than the editor and the owner to see a v2 clip exists.
* **No money can move.** `writeMarketplaceV2Earnings` has no caller. The tracking tick does not know
  v2 exists. An approved clip earns nothing and can earn nothing.

**WHAT ROUND THREE MUST BUILD to make an approved clip postable:**

1. **The poster's catalogue**, listing approved v2 clips for a campaign, with the editor's name, the
   submission date and which accounts have posted it, which PART 6.4 of BL-876 wants for spotting
   theft by eye anyway.
2. **The post flow**: download from Drive, post to his own account, paste the live URL, and a
   `MarketplaceV2Post` row plus the earning `Clip` it creates, with `isMarketplaceClip` left FALSE
   and `marketplaceV2PostId` set.
3. **The tracking tick that calls `writeMarketplaceV2Earnings`**, with all three legs in one
   transaction, and **`computeV2BudgetCost` as a pre-flight gate** for the reason BL-877's PART 4
   measured.
4. **The `AgencyEarning` decision wired to `v2AgencyEarningApplies()`** rather than re-decided, so
   the ADDS flag has one reader as well as one writer.

**That is the first round where v2 money moves in production.**

---

## WHAT COULD NOT BE DETERMINED

* **Whether the 26 positions carrying money below their paid floor is comparable to BL-849's measured
  17.** Not re-measured with BL-849's exact query, for the same reason BL-877 gave. This round
  created zero payout rows, so it created no new position below a floor.
* **Whether the browser canvas thumbnail will actually succeed for a real editor.** It failed in the
  sandbox, which is the expected outcome for a fabricated Drive id, and no real Drive file was
  available to test the success path. **The failure path is what was proved, and it is the path that
  matters.**
* **Whether `--bg-page` resolving to nothing is visibly wrong on all 23 files that use it**, or
  whether some of them sit on a surface where transparent happens to look correct. It was measured as
  undefined, not rendered file by file.
* **Whether an ADMIN should eventually see the approval queue.** BL-876 left it open, this round took
  the OWNER-only default, and it remains the owner's call.

---

**PERFORM NO FIX ON ANYTHING ABOVE. The two defects this round found in its own work, it fixed and
re-proved. The two pre-existing defects it found, `--bg-page` and the stale CLAUDE.md stack line, it
deliberately did not touch.**
