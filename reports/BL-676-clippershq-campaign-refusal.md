# BL-676 (ClippersHQ) — the silent blank screen on a completed campaign is now an explanation with a way out

> **Filename note.** The SHIP step asked for `reports/BL-676.md`, but that path was **already taken** by a different project: `reports/BL-676.md` in this repo is *"the view-count decoy: which field actually carries reach, per platform"*, an audit of the **clipper-finder** Python funnel pipeline, published as commit `9dbffbf`. Two separate repos are numbering BL items independently and have collided on 676. That file was **not** overwritten and was **not** modified. This ClippersHQ report is published beside it under a disambiguated name.

**Branch** `checkpoint/BL-676` @ `d169d7db` (pushed; `origin/checkpoint/BL-676 == local HEAD`, verified by `scripts/safe-push.mjs`).
**Base** `0a69fcc4` (`post-merge-BL-672`). **Tags** `pre-BL-676` (0a69fcc4) and `post-BL-676` (d169d7db), both pushed.
**Worktree** `C:/b676`, short path, `node_modules` never junctioned.
**Rollback** `git revert d169d7db`, or `git reset --hard pre-BL-676`. Reverting restores the blank screen, so revert only if the panel itself misbehaves.

**Note on the base.** `origin/main` moved to `d6373647` (BL-673) while this round was building. This is a parallel-safe round shipping a BRANCH, so it stayed on `0a69fcc4` and the merge round will union it. Its own diff against its base is exactly 4 files and nothing else.

| file | change |
| --- | --- |
| `src/components/campaigns/CampaignUnavailable.tsx` | NEW, +129, the panel |
| `src/app/(app)/campaigns/[id]/page.tsx` | +41 / −6, the status capture and the branch |
| `scripts/test-bl-676-campaign-refusal.ts` | NEW, +170, the proof harness |
| `BACKLOG.md` | +12, the BL-676 entry |

---

## PART 1 — the blank screen is replaced

**What was wrong.** `src/app/(app)/campaigns/[id]/page.tsx:264` read `if (!campaign || campaign.error || !campaign.id) return null;`. `return null` renders **absolutely nothing**: no heading, no message, no route out. The API had already said, in words, `{ error: "This campaign has ended" }` with a 403, and the page threw those words away, because the fetch at `:132` ran `r.json()` unconditionally and discarded `r.status`.

**It was worse on a phone than BL-674 recorded.** The a11y review found that `app-layout.tsx:982` suppresses the mobile topbar on this exact route and `BottomNav.tsx:332` returns `null` on it. So on a phone the blank page carried **no navigation whatsoever**. The only way out was the browser's own back button.

**Two changes, both small.** The fetch keeps the status beside the parsed body (same URL, same method, same headers, still exactly one call to the endpoint), and the **unchanged** guard condition now renders a panel instead of nothing.

```tsx
fetch(`/api/campaigns/${id}`).then(async (r) => ({
  __httpStatus: r.status,
  body: await r.json().catch(() => ({})),
})),
```

The `.catch` on the parse is deliberate: without it, a non JSON refusal body would reject the whole `Promise.all` and hit `.catch(() => router.push("/campaigns"))`, silently bouncing the user away, which would have swapped one invisible failure for another.

### The three cases, told apart

The API produces three distinct refusals and this round distinguishes all three. **Role is checked before the prose**, so a copy edit on the API can never silently downgrade "finished" into the wrong message. Reading a machine code instead would be cleaner, but the route returns no code and PART 2 forbids touching that file.

| API result | who gets it | panel |
| --- | --- | --- |
| `403 { error: "This campaign has ended" }` | any non OWNER, non CLIENT opening a **PAST** campaign | **ended** |
| `403 { error: "Forbidden" }` | a **CLIENT** (they must use `/api/client/campaigns/[id]`) | **no access** |
| `404 { error: "Not found" }` | campaign does not exist, **or** exists and is invisible (test campaign, DRAFT seen by a clipper) | **not found** |

**Honest limits, stated rather than guessed at:**

* **"A campaign they were never part of" is not a case this API has.** There is no membership gate anywhere in the GET handler. Any authenticated non CLIENT can open any ACTIVE campaign whether they joined it or not, so no refusal ever means "you were not part of this". Inventing that message would have been a lie about the system.
* **"Does not exist" and "exists but is hidden from you" are deliberately merged into one 404**, by the API, so that the existence of a campaign is never leaked. This page does not undo that: both get the identical wording, `This campaign either does not exist or is not available to your account`.

### What actually renders now

Rendered from the shipped component through `react-dom/server`, text extracted, all three cases:

```
### 403 ended (clipper on a PAST campaign)
  This campaign has finished
  The campaign page closes once a campaign is completed, so it cannot be opened
  anymore. Nothing you did on it is lost. Every clip you posted, everything you
  earned and every payout is still on your own pages.
  Where to go next
  Browse campaigns    See everything open right now
  Your clips          Every clip you have posted, including on this campaign
  Your earnings       What you earned, with a filter for each campaign
  hrefs: href="/campaigns" href="/clips" href="/earnings"

### 403 no access (CLIENT)
  You cannot open this campaign
  Your account does not have access to this campaign page. If you posted clips on
  it, that work is still yours and is still on your own pages.
  Where to go next
  Browse campaigns / Your clips / Your earnings
  hrefs: href="/campaigns" href="/clips" href="/earnings"

### 404 not found
  We could not find this campaign
  This campaign either does not exist or is not available to your account. If you
  had clips on it, they are still on your own pages.
  Where to go next
  Browse campaigns / Your clips / Your earnings
  hrefs: href="/campaigns" href="/clips" href="/earnings"
```

**Why those three links and not a generic "go home".** BL-674 proved live that a clipper is not locked out of anything they earned. Re grepped on this branch as the brief demanded rather than inherited: `src/app/api/clips/mine/route.ts`, `src/app/api/earnings/route.ts` and `src/app/api/payouts/route.ts` contain **zero** campaign status references. A finished campaign's clips, money and payout history are all still reachable, so the panel takes the clipper straight to them instead of leaving them at a dead end.

---

## PART 2 — the permission was NOT weakened

`src/app/api/campaigns/[id]/route.ts` is **byte identical by blob OID**, `8542fc04ec27a750cbf1c548c2971f6623188cba`, on both `0a69fcc4` and the branch head. Not one byte of the authorisation chain moved. The harness additionally asserts the three guards are still literally present in the shipped file:

* `if (campaign.status === "PAST" && role !== "OWNER")` still returns 403.
* The invisible test campaign still returns **404**, not 403, so existence is not leaked.
* `shapeCampaignForClipper` still strips the owner and agency fields for a CLIPPER.

**No campaign internal can reach this panel, structurally rather than by review.** `CampaignUnavailable` takes exactly three props and there is no campaign object in its scope at all:

```
({ httpStatus, errorText, role, }: { httpStatus: number | null; errorText: unknown; role: string; })
```

The harness asserts that signature contains no occurrence of the word "campaign", that the module never mentions `ownerCpm`, `agencyFee`, `clientName`, `aiKnowledge`, `lockedOwnerShareDecimal`, `budget` or `clipperCpm`, and that no rendered case emits any dollar figure.

---

## PART 3 — would making completed cards clickable just lead here?

**Yes, and that is why they were left alone.** `CampaignsRedesign.tsx:198` returns a plain `<div>` for a past card. Giving it a `<Link href={"/campaigns/" + c.id}>` would send the clipper to this very route, which for a PAST campaign returns the 403 at `route.ts:67`, which now renders the **"This campaign has finished"** panel. That is a real improvement on a blank screen, but it is still a refusal, not a brief: the card would advertise a destination and deliver an apology.

**They stay non clickable this round.** `src/app/(app)/campaigns/CampaignsRedesign.tsx` is **byte identical by blob OID**, `1c1fc6f0e9d6901454bebb7bf8b9db30e8c546d1`, and the harness asserts the exact line `if (isPast) return <div className="block">{inner}</div>;` is still there. They should stay non clickable until the endpoint permits a clipper view, which is BL-674's Answer B and an owner policy call, not this round's.

BL-674's Answer A, pointing the card at the clipper's own money instead, was also **not** taken here: the brief ring fenced the card, and BL-674 already recorded the blocker, that `earnings/page.tsx:36` does not read the URL, so a deep link would need query param seeding first.

---

## PART 4 — the evidence

### 4.1 A 403 renders a clear message with working links instead of a blank screen

`scripts/test-bl-676-campaign-refusal.ts` imports the **real shipped component** the page imports and renders it through `react-dom/server`, then asserts on the actual HTML. **44 passed, 0 failed.**

```
--- 1. the 403 that used to render NOTHING ---
PASS  a 403 renders actual HTML, not an empty string  5945 chars
PASS  it renders a level-1 heading
PASS  the heading SAYS the campaign finished
PASS  it tells the clipper their work is not lost
PASS  it uses NO dash as a bullet
PASS  it contains no emoji

--- 2. the way out ---
PASS  link to /campaigns is present and labelled "Browse campaigns"
PASS  link to /clips is present and labelled "Your clips"
PASS  link to /earnings is present and labelled "Your earnings"
PASS  a clipper can reach their own CLIPS from the refusal
PASS  a clipper can reach their own EARNINGS from the refusal
PASS  the ways out are a real list
PASS  every link carries visible text, so none is an icon-only mystery link
PASS  decorative icons are hidden from assistive tech

--- 3. the API's cases, told apart ---
PASS  403 + the finished-campaign body classifies as ENDED
PASS  403 for a CLIENT classifies as NO ACCESS (role, not prose)
PASS  403 + Forbidden classifies as NO ACCESS even for a CLIPPER
PASS  404 classifies as NOT FOUND
PASS  a reworded finished-campaign body still classifies as ENDED (role is the stable signal)
PASS  an unknown status falls back to NOT FOUND rather than guessing
PASS  the NOT FOUND wording differs from the ENDED wording
PASS  the NO ACCESS wording differs from both
PASS  NOT FOUND never leaks whether the campaign exists
PASS  every case still offers the same three ways out
```

### 4.2 The API's authorisation is unchanged

```
--- 6. ring-fenced, and left alone ---
PASS  the API still refuses a PAST campaign to every non-OWNER
PASS  the API still 404s an invisible test campaign rather than leaking it
PASS  the API still strips the owner fields for a CLIPPER
PASS  completed campaign cards are STILL not clickable
```
plus the blob OID above, `8542fc04`, identical on both refs.

### 4.3 A clipper can reach their own clips and earnings from that page

The panel emits `href="/clips"` and `href="/earnings"` in **every** refusal case, asserted on the rendered HTML. Those destinations work for a finished campaign because none of their routes reads campaign status, re grepped on this branch:

| route | campaign status references |
| --- | --- |
| `src/app/api/clips/mine/route.ts` | **0** |
| `src/app/api/earnings/route.ts` | **0** |
| `src/app/api/payouts/route.ts` | **0** |

### 4.4 No campaign's displayed numbers changed

`scripts/test-bl-641-finished-campaign-display.ts` re run **live against prod** on this branch: **19 passed, 0 failed**.

```
somesome status=PAST budget=$9750.00 clipperSide=$1967.14 total=$5370.12
LIVE  (status PAST) clipper sees $9750.00 of $9750.00 = 100%
PASS  LIVE somesome is FINISHED, so a clipper sees the full $9750.00
PASS  LIVE progress bar reads 100%
PASS  AS PAST clipper sees the FULL budget $9750.00
PASS  AS PAST the progress bar reads 100%
PASS  ZERO unfinished campaigns change display (BL-535 control property intact)
PASS  OWNER headroom is real and non-zero: $4379.88
PASS  control displays its REAL spend $841.00 while not finished
19 passed, 0 failed
```

Structurally this could not have changed: nothing this round touches reads or renders a campaign figure.

### 4.5 The page still works for an authorised owner

The **guard condition is byte for byte the same**, `if (!campaign || campaign.error || !campaign.id)`. Only the body of that branch changed, from `return null` to the panel. A response that rendered before still satisfies the same condition the same way and takes the same path, and `campaignHttpStatus` is never read on the success path. Asserted directly:

```
PASS  the GUARD CONDITION is unchanged, so an authorised render is untouched
PASS  that branch no longer returns null
PASS  the fetch still makes exactly ONE call to the campaign endpoint
PASS  no money route was added to this page
```

An OWNER is exempt at `route.ts:67`, so an owner opening a PAST campaign still receives a 200 and the full brief, exactly as before. The panel is unreachable for them unless the campaign genuinely does not exist.

---

## a11y review

Run by `accessibility-agents:accessibility-lead` on the shipped markup, before the file was written. **Verdict: no blocking WCAG A or AA failure.** Its findings were applied:

* **Applied.** The row **label** now carries the accent (`#2596be` on `--bg-card-hover` = 5.11:1), matching `ResourceCard` in the same file, because the row fill measures only **1.06:1** against the card and the row border **1.18:1**, so neither can be what identifies the row as a link (SC 1.4.11). Hover border lifted from `accent/45` (2.03:1) to `accent/70` (about 3.2:1).
* **Applied.** The `outline-none` plus `focus-visible:ring-*` cluster was **deleted as dead code**. `globals.css:202` declares an **unlayered** `*:focus-visible { outline: 2px solid #2596be; outline-offset: 2px }`, and Tailwind utilities sit inside `@layer utilities`, so the unlayered rule wins and `outline-none` is inert. Keeping the ring would have misled the next reader into thinking focus was suppressed. Focus is visible at 5.4:1 against the card.
* **Applied.** `motion-reduce:transition-none motion-reduce:active:translate-y-0`, for consistency with the three existing reduced motion blocks in `globals.css`. The lead noted the 1px press could not fail AA anyway, since SC 2.3.3 is AAA.
* **Applied.** Used the house `<Card>` component rather than hand rolling the container, and matched the sibling `h2` size (`text-xs`, not `text-[11px]`). Copy fixed: "any more" to "anymore", and "brief" replaced with "campaign page", which is plainer for a new clipper.
* **Ruled and kept as written, not both options.** **No live region and no focus move.** The panel **is** the route's entire main content replacing a spinner after a navigation the user initiated, so SC 4.1.3 does not apply; `role="alert"` would be actively harmful because its implicit `aria-atomic` flattens the heading, the list and the three links into one unstructured string, and a focus move would race the App Router's own route change reset. **`h1` is correct**: the shell renders no `h1` on this route and the success branch's own `h1` is mutually exclusive with this early return, so there is exactly one either way.
* **Confirmed passing.** Contrast everywhere (all three text vars resolve to `#ffffff` in the dark theme, 17.4:1 to 18.4:1; accent 5.1 to 5.4:1 against every surface used). Touch targets are **60px** tall and full width, clearing SC 2.5.8 AA and SC 2.5.5 AAA even at 375px. Link text passes SC 2.4.4 and SC 2.4.9; SC 2.5.3 Label in Name passes. `aria-hidden` sits on the icon wrappers, which contain no focusable descendants.
* **Flagged, not fixed, both pre existing and app wide.** The loading spinner at `page.tsx:246` has no `role="status"` and no accessible text, so a screen reader user hears silence during load on **both** branches; and the app has no SPA route change title or focus announcer.

---

## Safety and gates

| check | result |
| --- | --- |
| `npm ci` | **exit 0** |
| `npx prisma generate` | **exit 0**, Prisma Client 7.8.0, run **after** `npm ci` and **before** `tsc` |
| `npx tsc --noEmit` | **exit 0**, log 0 lines |
| `npm run build` | **BUILD_EXIT=0**, echoed from `$?`, never piped through `tail`; "Compiled successfully in 27.1s" |
| hooks gate `lint:hooks` | **eslint present and actually executed** (`node_modules/.bin/eslint`, eslint **9.39.4**); `--max-warnings 11` → **11 problems, 0 errors, 11 warnings**, at the cap, passing |
| `check:prisma-bypass`, `check:removed-fields` | ran (prebuild) |

Money files, blob OID against the base `0a69fcc4`, all **IDENTICAL**: `clip-earnings-writer.ts` `7aa6be48`, `earnings-calc.ts` `797e2098`, `balance.ts` `e887f80a`, `tracking.ts` `847dcf70`, `clip-earnings-invariant-middleware.ts` `61cef393`, `money-decimal.ts` `ef5cdae7`, `campaign-era.ts` `106e16ad`.

No API change, no schema change, no `prisma migrate`, no data mutation, no clip's earnings or status touched. The only live database access this round was the read only `test-bl-641` display test. Nothing held by another round was touched: BL-675 and BL-677 have no branch and no worktree on this machine, and this round worked only inside `C:/b676`. No dashes used as bullets, in the code, the UI copy or this report.

## Flagged for the owner, not fixed

* `src/lib/email.ts:761` still embeds `https://clipershq.com/campaigns/<id>` in every campaign alert, so old emails still point at a campaign that will eventually finish. This round makes that landing honest rather than blank, which is as far as it can go without a policy decision.
* `favorites/page.tsx:87` links every favourite to `/campaigns/[id]` unconditionally, but its source `/api/campaigns` is fetched without `includePast`, so a favourited campaign silently **vanishes** from Favorites when it turns PAST rather than dead linking. BL-674 found this; it is untouched here and is a separate defect.
* Whether a completed campaign should open read only for a clipper at all is BL-674's Answer B and remains the owner's call.
* The `reports/BL-676.md` filename collision above means two repos are numbering BL items independently against one shared reports repo. Worth a naming convention before the next collision.
