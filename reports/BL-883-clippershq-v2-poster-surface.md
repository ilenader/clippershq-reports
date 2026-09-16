# BL-883 — marketplace v2, round seven: the poster's surface, the owner's eyes, and the signal that was about to become noise

> **NOTHING IS UNREMOVABLE AND NO SQL IS OWED. FIRST LINE, AS THE ROUND REQUIRES.**
> 128 ledgered rows, **`VERIFIED: 0 of 128 recorded rows remain`**, 0 failed. An independent pattern
> sweep the destroyer never uses returns **zero** `bl883sbx-` rows in `users`, `campaigns`, `clips`,
> `marketplace_v2_clips` and `payout_requests`, and **zero** rows in `marketplace_v2_editor_earnings`
> platform wide, read at `2026-09-16 21:33:59+00` against the database's own `now()`.

**2026-09-16. Shipped on `checkpoint/BL-883`, merged to `main` at `38aafd5`. Requires a Railway
REDEPLOY**, and BL-877 through BL-882 are all still owed. Base `origin/main` @ `75dc600`. Isolated
worktree `C:/w/b883`, **verified gone**: `git worktree list` shows only the primary tree and
`ls /c/w/b883` returns "No such file or directory".

---

## THE HEADLINE

**PART 0's answer was that there was no money problem, and saying so was the point.** The editor owned
no clip on the campaign he earned from, which is why BL-882 had to teach twelve derivations about him
and why it found a twelfth nobody had counted. **THE POSTER OWNS THE CLIP.** His 45 percent has always
been ordinary `Clip.earnings` on a row whose `userId` is his, and `earnings/route.ts:70`'s `clipWhere`
carries **no v2 filter of any kind**. So `balance.ts` was not touched, and its blob OID
`67c30c8951812eb00c584423ced00a0c73041a9c` is identical on both refs. Only the looking was missing,
and only the looking was built.

**He is the third earner in a row to have had nowhere to look**, after BL-843's trainer and BL-882's
editor. That sentence has now been written three times and this round is the last one that can write
it about marketplace v2.

---

## THE MODEL SPLIT, AND EVERY SUBAGENT CLAIM MARKED

| work | model | verdict |
|---|---|---|
| every line touching a payout, a balance or an earnings figure, the reconciliation SQL, the four guards and this report | **Opus, no subagent between it and the source** | n/a |
| accessibility review of both new surfaces | Sonnet family, four specialists | **EIGHT CLAIMS VERIFIED AGAINST SOURCE BEFORE ANY WERE ACTED ON, and every one was accurate.** Listed below |

Because BL-881 had three claims wrong in the same direction and BL-882 had a derivation count come
back short by the only load-bearing entry, nothing here was believed on assertion:

| claim | verdict |
|---|---|
| the owner never reaches the route's adjust refusal, because `page.tsx:3066` natively disables Apply, and the string he reads is `page.tsx:3002` | **VERIFIED.** Read both. This changed the work: fixing only the route would have been a half fix |
| `Modal` restores focus in its effect CLEANUP, so after a successful cashout focus ends on `<body>` | **VERIFIED** at `modal.tsx:186-202`, and `CashoutModal` accepted no `returnFocusRef` at all (0 occurrences) |
| the load-failure `tabIndex={-1}` in BL-882's page is dead code | **VERIFIED.** The only `.focus()` in the file was `h1Ref` on mount |
| `MoneyCell` speaks the same sentence for all four money columns | **VERIFIED** by reading my own shipped file |
| `null` snapshot is a LEGACY row and not an editor; 7 of 68 PAID rows carry none | **VERIFIED** at `payouts/route.ts:935` |
| the `border-t` above the totals sits on the first cell only | **VERIFIED** |
| `min-w-[180px]` does not scale with text size, and an `em` here would resolve against 11px | **VERIFIED**, fixed as `rem` |
| `regionLabel` "Earnings by campaign" drifts from the visible `<h2>` "Campaign by campaign" | **VERIFIED**, aligned |

---

## PART 0 — WHAT THE POSTER COULD ALREADY DO

| what | where | state before this round |
|---|---|---|
| his 45 percent counted in his balance | `api/earnings/route.ts:70` — `clipWhere = { userId, isDeleted: false, campaign: { isTestCampaign: false } }` | **already worked.** No `marketplaceV2PostId` filter, no `isMarketplaceClip` filter |
| counted as APPROVED earnings | `balance.ts` `computeBalance`, via the ordinary `clips` arm | **already worked** |
| withdrawable | `payouts/route.ts` POST, whose `clips` query has no v2 filter | **already worked** |
| listed among his clips | `api/clips/mine/route.ts` | **already worked** |
| gathered in one place, with whose clip each was and what each earned him | nowhere | **THIS WAS THE GAP** |

`marketplaceV2PostId` is referenced in only five files platform wide, and **not one of them is a
poster-facing read surface**: `clips/[id]/review`, `clip-earnings-writer.ts`,
`marketplace-v2-poster.ts`, `marketplace-v2-sync.ts` and `tracking.ts`. There was no view.

**`balance.ts` is byte-identical**, and the round asked for that to be proved rather than asserted.

---

## PART 1 — THE POSTER'S SURFACE

`/marketplace-v2/poster`, gated with the same `notFound()` pair as the editor's page because
`marketplace-v2` is a SIBLING of `marketplace/` and inherits neither its layout nor its gate.

**It reconciles in two directions, and neither is a claim:**

```
PASS  poster 1 sees HIS OWN figure and it reconciles ACROSS
      earned $27.00 against $27.00 of his own 45 percent;
      $27.00 minus $0.00 minus $0.00 = $27.00
PASS  poster 1's page reconciles DOWN
PASS  the three posters see three DIFFERENT figures, so no page is showing a shared total
      poster 1 $27.00, poster 2 $18.00, poster 3 $9.00
```

`available` is **not computed on the page**. It comes from `computeCampaignBalances`, the same
function `/api/earnings` and the editor's page use, and the totals row is the literal column sum.
**There is no thirteenth derivation**, which is the specific thing the round warned against, because
the twelfth was the one that would have made an editor unpayable forever.

### The editor's name, never his earnings

```
PASS  the poster sees the EDITOR'S NAME on his post
PASS  and NONE of the forbidden fields, checked against the LIVE BODY
      10 field names checked against the response
PASS  the editor's EARNINGS figure is absent from the poster's response
      the editor's leg on that clip is $27.00. It is not emitted.
```

The relationship is carried by the **words "Edited by"** and by nothing else, because in browse mode
two adjacent spans are read as one undivided run, so weight and colour carry nothing. It is
deliberately not a link, has no `tabIndex`, no hover rule and never `text-accent`, which is this
product's link colour and would assert a profile page that does not exist. The `@` is `aria-hidden`
because NVDA reads it as the word "at" at default punctuation, and the visible string still contains
the spoken one so the two can never diverge.

### The shared component, and what required props buy

The money block is now **one component** used by both pages. The four labels and the two gross-and-cash
qualifiers are **not props and cannot be overridden**, because two hand-written copies is how one page
starts calling a figure "Paid" while the other says "Paid out to you", and WCAG 3.2.4 is violated by
drift alone. It is the same argument `writeClipEarnings` gets: build the chokepoint rather than trust
the convention.

Three props are **required with no defaults**, each for a measured reason:

* `regionLabel` and `caption` are both invisible, an `aria-label` and an `sr-only` caption, so a wrong
  default **could never be caught by looking at the page**. Two identical accessible names put two
  indistinguishable regions in a screen reader's landmark list, and the two must also differ from each
  other or the reader hears the same string twice.
* `totalRowHeader` is the **only** element that says what set was summed, and the two pages sum
  different sets: "campaigns your clips were posted on" against "campaigns you posted on".

And ids are minted with `useId()` rather than from data, because a user who is both editor and poster
on one campaign would otherwise emit the same `reason-${campaignId}` twice, `aria-describedby` would
bind to whichever came first, and **a blocked poster button would read out the editor's refusal
reason**: a wrong money explanation delivered only to screen reader users.

### Three live defects in what BL-882 shipped, all found by the review and all fixed

1. **Focus fell to `<body>` after every successful cashout.** `Modal` restores focus in its effect
   CLEANUP, synchronously when `open` flips false, so it focused the still-connected "Request cashout"
   button; the refetch then gave the campaign an open request, that button was replaced by a sentence,
   and focus dropped with no event roughly 300 ms later. The announcement that followed was spoken
   into a page whose caret was nowhere. Fixed with a `returnFocusRef` passthrough plus a post-refetch
   `document.activeElement` guard, on **both** pages.
2. **A load failure was announced to nobody.** The failure heading carried `tabIndex={-1}` and nothing
   in the file ever called `.focus()` on it, so the one sentence written for a screen reader user,
   that nothing is wrong with his money, was the one he never heard.
3. **All four money columns spoke the same sentence.** `MoneyCell` said "gross before the fee, $X" for
   Earned, Paid out, Held and Available alike. Its own comment stated the goal exactly, that a row of
   eight numbers must not be eight naked numbers, and then left them eight **qualified but
   indistinguishable** numbers. Held against Available is the one distinction that decides whether
   money can be withdrawn. `measure` is now spoken first, as an internal union rather than a prop.

---

## PART 2 — THE OWNER TELLS THE TWO APART

```
PASS  THE TWO CLAIMS ARE VISIBLY DIFFERENT, and not by a JSON column
      editor row reads "Editor earnings", poster row reads "1 of their clips"
PASS  each row says WHAT FUNDS IT, in a sentence
PASS  the editor's claim carries an EXPLICIT EMPTY snapshot and the poster's does not
      editor [], poster holds 1 clip id(s)
```

**Both sides of the partition are labelled**, and that is a deliberate departure from the standing
badge beside it. That badge marks an **exception**, so absence honestly means "nothing to say". Claim
kind is a **partition**: every row is one of exactly two, so marking one side only would make an
absent label mean both "ordinary clip payout" and "the feature did not render".

**It is a word and never a tint**, because every text token on that page resolves to `#ffffff`.

**And it is a measurement, not an inference.** An empty `clipIdsSnapshot` is only called an editor
claim when that person's v2 editor rows on that campaign agree, confirmed by one grouped query over
the empty-snapshot rows on the page. **NULL is not an editor**: `adjust/route.ts:258` reads null as
"every clip this user owns on this campaign", and `payouts/route.ts:935` records that 7 of 68 PAID
rows carry no snapshot at all, so collapsing the two would label legacy clipper rows as editor claims,
which is a wrong fact read aloud with total confidence.

### The refusal is preserved. Only its wording changed, in two places.

```
PASS  the adjust route REFUSES an editor's claim ON THE EMPTY SNAPSHOT
      status 400 code ADJUST_NOT_CLIP_FUNDED
PASS  and its sentence no longer claims there are no approved clips on the campaign
```

The route's diff is **one deleted line, the message string**. The `if (prrdSnapshotCount === 0)`
condition and the `status: 400` are untouched, proved by the diff, because that refusal is what stops
a price-down shrinking three strangers' `Clip.earnings`.

**But the route's string is not the one the owner reads.** `page.tsx:3066` natively disables Apply the
moment the preview returns zero clips, so the 400 is almost never reached; what he sees is
`page.tsx:3002`, and **every clause of it was false for an editor claim**: "none are currently
APPROVED on this campaign" when there were four, all of them other people's. Both were fixed, the
client one first, and each now ends with the control that does work.

### Which controls behave differently on an editor's row

| control | on an editor's claim |
|---|---|
| **Reduce clip earnings** (`adjust`) | **REFUSES**, `ADJUST_NOT_CLIP_FUNDED`. Correct and preserved |
| **Set amount** (`price`, BL-864) | works identically. Stamps `actualPaidAmount` only, writes no clip |
| **Close unpaid** (`settle`, BL-861) | works identically. Status stays open so the gross stays locked out |
| Approve, reject, mark paid, express, minimum, SLA | all identical, because none reads where the money came from |

### The contract the queue now depends on

`clipIdsSnapshot`'s emptiness for an editor was an **emergent** property of a union with nothing
declaring it, and BL-882 made three things depend on it. This round makes a fourth depend on it and
turns it into **words an owner reads before deciding to pay someone**, so the contract is now stated at
the write site and asserted by `scripts/check-payout-snapshot-contract.js`: the union must stay exactly
the claimant's own clips plus his own creator rows, or a future round widening it would relabel every
editor claim as an ordinary clip payout **and** re-arm the adjust route against strangers' earnings,
with nothing failing.

---

## PART 3 — THE LEGS NOTHING CLEANS UP

### Every departure path, enumerated and EXERCISED

| path | what happens to both legs | verdict |
|---|---|---|
| **clip RETIRED** (`videoUnavailable`) | both **FROZEN in proportion**, never zeroed (`retire-dead-clips.ts:465-473`, BL-584, BL-720), and both leave the spend aggregate and the withdrawable balance **in the same instant**, because every filter carries the same three clip conditions | **correct, nothing stranded** |
| **clip REJECTED for botting** | poster and platform to $0.00; editor held **only** by money already paid | **correct**, BL-849's intended lesser harm |
| **campaign moved to PAST** | nothing touches either leg; spend unchanged | **correct**, the money was spent |
| **campaign COMPLETED** | same answer, same reason | **correct** |
| **editor BANNED** | leg untouched, withdrawal refused 403 | **correct pair.** Zeroing the leg would rewrite what the campaign spent; letting him withdraw would ignore the ban |
| **v2 clip UN-APPROVED with posts** | **REFUSED 409** by `undoV2Decision` | **already closed**, needed no change |
| **campaign DESTROYED** | clips deleted, legs cascade with them | **correct** |

**There is no unexplained orphan path.** Every leg left standing is either consistently filtered out
everywhere, or held by a paid floor, which is money already recorded as somebody's.

### So the real defect was the SIGNAL, and it is fixed

BL-881's query called a floored leg `'poster and editor legs disagree'`, **indistinguishable from a
real leak**. A hundred correct rows would have buried the one real one, and a signal nobody reads is
not a signal.

The floor is now computed **in the query**, from the same three quantities `floorV2EditorEarnings`
uses and in the same order, so the two cannot drift: `paidGross` taking `actualPaidAmount` when set,
minus his other editor rows and his own clips on that campaign, floored at zero.

```
PASS  THE RECONCILIATION QUERY TELLS AN EXPLAINED ROW FROM A LEAK
      1 row(s) out of balance in all, of which 1 EXPLAINED by a paid floor
      and 0 reported as LEAKS, unchanged from the 0 before this run.
NOTE  explained: clip cmu4m3wh90… editor leg $17.10 against a paid floor of $17.10, poster $0.00
PASS  and no floored leg was deleted or zeroed by anything this round did
```

`V2_RECONCILE_SQL` returns **only leaks**, so a clean platform still returns zero and a platform with a
hundred legitimately floored legs also returns zero. `V2_RECONCILE_ALL_SQL` returns every
out-of-balance row **with its verdict and the floor that explains it**, so nothing is hidden, only
separated. **Nothing is deleted or zeroed by either**: a reconciliation that tidied a floored leg away
would be taking money back.

---

## PART 4 — THE `--bg-page` DEFECT

**Measured, not estimated: 0 definitions repo wide, 26 referencing files, 39 use sites.**

| form | count | what it does |
|---|---|---|
| `bg-[var(--bg-page)]` | **33** | the declaration is invalid, so the background falls to `transparent`. Invisible on a palette where every surface sits within 1.08 to 1 of every other, which is why nobody noticed |
| `ring-offset-[var(--bg-page)]` | **6** | the invalid value lands in `--tw-ring-offset-color`, which invalidates the composed `box-shadow` and **DELETES THE FOCUS RING ENTIRELY** |

**All six ring-offset uses are fixed**, each to the surface the control actually sits on, determined by
reading its container rather than by a blanket substitution: `accounts/page.tsx`,
`admin/fraud-review/page.tsx` and `admin/growth/page.tsx` to `--bg-primary` because each sits on the
page; `notifications/page.tsx` and `progress/page.tsx` to `--bg-card` because each sits on a card; and
`AccountCardPremium.tsx` to `--bg-primary` because the card is itself `--bg-card` and an offset must
name what is BEHIND it.

**The token was deliberately NOT defined, and the decision is the finding.** Defining it is one line
and would silence all 39 at once. Those 33 backgrounds have shipped rendering `transparent` and have
been looked at that way; giving all of them a colour in a single unreviewed commit across 26 files is
a **visual change dressed as a bug fix**. The ring-offset uses were fixed because a missing focus ring
is an accessibility failure a keyboard user cannot work around; the other 33 are reported with an
exact count for a round that can look at them.

**CLAUDE.md is corrected.** It named `--bg-page` as a house token, which is how the bug kept being
written, and now names `--bg-primary` with the warning. `scripts/check-css-tokens.js` runs in
`prebuild`, refuses **any** ring offset naming an undefined custom property, and caps the 33 so the
number can only fall.

---

## PART 5 — CARRIED FORWARD, NOT FOLDED IN

| item | status | this round |
|---|---|---|
| **BL-864's erase trap** | still bites. BL-882 measured it at three points: set to $7.00, erased by the close, still erased after reopen. It bites an editor exactly as it bites a poster | **not touched.** It is BL-864's to fix and folding it in would hide it |
| **`admin/payouts/unpaid` and `liability.ts` understating what the platform owes** | both have **zero** references to the FIRST marketplace's creator table, so this predates v2 by three rounds | **not touched.** A Phase 6d correction deserving its own measurement, and half-fixing it for the newer earner while the older stays invisible would make them wrong in a new way |
| **the test-campaign divergence** | the withdrawal gate passes `includeTestCampaigns: true` because its own creator query carries no campaign filter; both dashboards pass false | **not settled.** Each site still mirrors what its own creator query does, so this round adds no new disagreement |
| **thirteen accessibility defects in `admin/payouts/page.tsx`** | reported with file:line, including a real duplicate-id bug at `:1885`, `bg-accent text-white` at 3.40:1, and an unlabelled keyboard-unscrollable table at `:1749` | **not swept into this diff** |

---

## PART 6 — PROOFS, RENDERS AND MERGE

### The sandbox

Prefix `bl883sbx-`, four locks, opening snapshot before anything was created, every timestamp cast to
`::text` against the database's own `now()`.

```
OPENING SNAPSHOT, TAKEN BEFORE ANYTHING WAS CREATED
  db now(): 2026-09-16 21:24:46.915881+00
  campaigns 34, clips 10188, users 1749
  v2: clips 0, posts 0, editor 0, platform 0
  agency 4882, payouts 248
  reconciliation BEFORE: 0 leak(s), 0 row(s) out of balance in all
```

**46 of 46 passed**, after **three runs that failed 6, 1 and 1**, every one reported:

* **run one, 6 failures.** The poster's route 500'd on every request: `stats` was ordered by
  `createdAt` and `ClipStat` has no such column, only `checkedAt`. Mine.
* **run two, 1 failure.** The editor's cashout was approved AFTER a clip was retired and another
  rejected, by which time his earnings no longer covered the request, so the review route correctly
  refused it 400 and his floor then had nothing to hold. **The product was right and the proof's
  ordering was wrong**; he is paid before anything departs now. Also `status: "ARCHIVED"` is not in
  `CampaignStatus`, which has ACTIVE, PAUSED, COMPLETED, DRAFT and PAST.
* **run three, 1 failure of honesty rather than of code.** The adjust refusal was reached on a claim
  that had already been PAID, so the route answered "Cannot adjust payout in status PAID" and the
  check passed on a **status guard rather than on the empty snapshot**. That is a pass for the wrong
  reason, exactly what BL-882 caught itself doing with two 429s, so it now uses a second editor whose
  claim stays REQUESTED and asserts the code is `ADJUST_NOT_CLIP_FUNDED`.

**Every failure path has its own user and asserts the status is not 429**, which the round required
because of BL-882's two masked results.

### The full sum and every invariant

```
PASS  THE FULL SUM RECONCILES EXACTLY: every leg plus the owner's ADDS cut equals what the campaign spent
PASS  BL-627: the campaign never exceeded its budget
PASS  the earnings invariant holds across the FULL clips table      0 violations
PASS  no editor leg is negative anywhere in the population          0 rows
PASS  BL-696: one editor row per clip, so nothing can be paid twice 0 rows
PASS  BL-824 for BOTH earners: no editor leg stands above the poster's
      without a payment to justify it                               0 rows
```

That last one is new this round and is **the exact shape of a leak**, which is what the reconciliation
query now reports separately.

### The guards, and the one that could not fail

Four guards run in `prebuild`. **Each was demonstrated FAILING on demand and the tree restored clean
after each**, because three separate guards on this platform have shipped unable to fail.

**S4 could not fail, and the demonstration caught it.** It skipped any file that mentioned
`v2PosterPayableClipWhere` **anywhere in it**, so replacing one of two queries in a file with a hand
rolled filter left the guard green with the hand rolled filter sitting there. That is the
guard-that-cannot-fail BL-835 shipped, BL-881 was caught shipping and BL-882 caught in its own first
version, now caught a **fourth** time by running the demonstration instead of trusting the guard. It
is per occurrence now: outside the allow list the column name may not appear at all.

```
DEMO R1 a ring offset naming a token that does not exist              exit=1
DEMO R2 a NEW use of the nonexistent background token                 exit=1
DEMO S1 the payout snapshot union widened past the claimant's own work exit=1
DEMO S4 a reader hand rolling the v2 clip filter                      exit=1
every demonstrated guard failed on demand and the tree restored clean.
```

### Renders

**25 of 25 shots passed, first attempt**, at 320, 375, 414, 1280 and 1440. Surfaces: the poster's
page, the poster's page empty, **the editor's page as a regression check on the refactor**, the cashout
modal opened from the poster's page, and the owner's queue.

The overflow check is **the pan, not `scrollWidth`**, because BL-882 measured this shell reporting a
root `scrollWidth` its ancestors had already clipped and separately measured a real 582 pixel pan. The
page is scrolled right and the movement read back, which is what a person holding the phone
experiences. **Every shot: `pagePanX=0px`.**

The owner's queue shot asserts **both** claim words and the explanatory sentence on the same screen, so
the partition is proved visible rather than described.

### Gates, honestly

```
BUILD_EXIT=0
[event-wiring] 0 problems.
BL-882 V2 EDITOR BALANCE GUARD:   19 passed, 0 failed.
BL-824 GUARD:                     14 passed, 0 failed.
BL-883 PAYOUT SNAPSHOT CONTRACT:   9 passed, 0 failed.
BL-883 CSS TOKEN GUARD:            3 passed, 0 failed.
eslint --max-warnings 11  ->  0 errors, 10 warnings
Compiled successfully
```

eslint is present in `node_modules/.bin`, so the hooks gate is not silently no-opping. **All ten
warnings are pre-existing and none is in a file this round created**, confirmed by counting.

### The protected files

| file | state |
|---|---|
| `balance.ts` | `67c30c8951812eb00c584423ced00a0c73041a9c` **byte-identical, and PART 0 required that** |
| `clip-earnings-writer.ts` | `4f63164b23af02e8310a00c654077779862a8f02` **byte-identical** |
| `earnings-calc.ts` | `00410634ee610d84a6ffb4b5d3693c99d6185549` **byte-identical** |
| `tracking.ts` | `8e2a62f554e23f3347f127d8a4a95116527e3924` **byte-identical** |
| `clip-earnings-invariant-middleware.ts` | `61cef39395363c31f0c902dd4c64e8c06b3e6449` **byte-identical** |
| `money-decimal.ts` | `ef5cdae757b9ad3c23380ee8b63e279f98d0b6ac` **byte-identical** |
| `campaign-era.ts` | `106e16ad75125c3b10b6949a2981d33614c69ab9` **byte-identical** |
| `marketplace-v2-writer.ts` | `c986ac5b407048e98759498c326123d450fb8d1f` **byte-identical** |
| `marketplace-v2-sync.ts` | **changed deliberately, and only its reconciliation query** |

### Merge

Branch pushed and **VERIFIED** at `ee3865b`. Merged `--no-ff`. **The merge tree OID
`284cbee7c670996ce93b0fa674f0ad207725bff5` is IDENTICAL to the branch tree OID**, so the branch build
is the merge build. `main` pushed and **VERIFIED** at `38aafd5` with tags `pre-BL-883` and
`post-BL-883`. `checkpoint/BL-723` was not merged. BACKLOG is **203 items**.

---

## CAN BOTH EARNERS NOW SEE AND RECEIVE THEIR MONEY?

**Yes, and both were watched doing it in the same run.** An editor submitted, the owner approved,
three posters posted, views accrued, **each poster opened his own page and saw his own figure
reconciling in both directions**, one poster requested and was paid, the editor requested and was
paid, and the owner's queue showed the two claims as visibly different things with a sentence saying
what funds each.

**Two honest qualifications.** No v2 post exists in production: the database holds **zero**
`MarketplaceV2EditorEarning` rows, because BL-879's visibility gates are still closed. The path is
proved and unused. And the whole v2 feature still requires a **Railway redeploy**, with BL-877 through
BL-882 owed alongside it.

## WHAT ROUND EIGHT MUST DO

1. **Wire the 33 inert `bg-[var(--bg-page)]` sites to a real token**, with the visual review across 26
   files that change actually needs. The guard holds the number down meanwhile.
2. **Settle the test-campaign divergence.** The withdrawal gate includes them and both dashboards
   exclude them. Three rounds have now mirrored it rather than deciding it.
3. **Fix BL-864's erase trap.** Closing a payout destroys a set price and reopening does not restore
   it, confirmed to bite both earners identically.
4. **Correct the Phase 6d understatement in `admin/payouts/unpaid` and `liability.ts`** for BOTH second
   earners at once, with its own measurement of what the platform actually owes.
5. **Decide BL-876's open question 16**, whether a poster may see which other posters took the same
   clip, and whether an editor may see which posters took his.
6. **The thirteen accessibility defects in `admin/payouts/page.tsx`**, starting with the duplicate id
   at `:1885` and the keyboard-unscrollable table at `:1749`.
