# BL-870 — the platform recorded what worked, so nobody who gave up was ever visible

**TEARDOWN FIRST, AS THE ROUND REQUIRES: NOTHING IS UNREMOVABLE. NO SQL IS OWED.**
20 ledgered rows, `VERIFIED: 0 of 20 recorded rows remain`. Two video hash rows and two
audit rows escaped the ledger's patterns because the real routes mint cuids; both sets
were removed by explicit id with the SQL printed first, and both verified at zero. A
direct catalogue sweep confirms **zero** `bl870sbx-` rows survive anywhere, and
`activity_events` is back to **0**, `marketplace_video_hashes` to its opening **9**.

**2026-09-09. Shipped on `checkpoint/BL-870`. Requires a Railway REDEPLOY.**

---

## PART 0 — WHAT WAS ALREADY RECORDED, CHECKED BEFORE ANYTHING WAS BUILT

Two prior rounds found features already built and merely invisible, so this was measured
first. **It is not a display round. The data does not exist.**

**`audit_logs` records only what SUCCEEDED.** Every `logAudit` call in the five
marketplace routes writes a completed act: `MARKETPLACE_SUBMISSION_CREATE`
(`submissions/route.ts:873`), `_POSTED` (`post/route.ts:1367`), `_APPROVE`
(`approve/route.ts:177`), `_REJECT` (`reject/route.ts:278`), `_LISTING_CREATE`
(`listings/route.ts:614`). **Not one of the refusal returns calls it.**

Measured across all **27,799** audit rows on the platform, the only attempt-shaped action
that exists anywhere is `ACCOUNT_VERIFY_ATTEMPT` (1,062 rows), which is account
verification and not the marketplace. The only refusal-shaped one is
`TRAINER_APPEAL_REFUSED`, with **three** rows. The marketplace's own history is 16
`SUBMISSION_CREATE`, 5 `LISTING_CREATE`, 5 `APPROVE`, 4 `POSTED`, 3 `REJECT`, and nothing
about anybody who tried and could not.

**Sentry does not fill the gap, and that was confirmed from the code rather than assumed.**
`instrumentation.ts:38-63` wires `onRequestError`, which fires only when a handler THROWS.
Every refusal in these routes is an explicit `return NextResponse.json({error}, {status})`,
a successfully returned response. **A 4xx refusal never reaches Sentry or
`captureServerError`.**

**How many refusals were invisible:** across the five handlers, **119** returns with a
literal 4xx and **15** with a literal 5xx. Across the whole `src/app/api/marketplace/`
tree, **326** and **62**. Every one of them was silent.

### What tomorrow could and could not have been answered with today's data

| Question | Before this round |
|---|---|
| How many clips were submitted | **Answerable.** `audit_logs` has it. |
| How many were approved, rejected, posted | **Answerable.** |
| Did anyone open the marketplace at all | **NOT answerable.** Nothing records a page view. |
| Did anyone try and fail | **NOT answerable.** No refusal is recorded anywhere. |
| Which rule stopped people | **NOT answerable.** |
| Was this reporter refused two minutes earlier | **NOT answerable.** No refusal existed to join to. |

---

## PART 1 — RECORDING EVERY REFUSAL WITHOUT TOUCHING ONE OF THEM

### A wrapper, not fifty edits, and that is the safety argument

Editing 134 `return NextResponse.json({error}, {status})` sites to add a logging line would
be a large diff through the exact code that decides whether a clipper may earn, and every
edit would be a chance to change a status or a message by accident.

`src/lib/with-activity.ts` wraps the handler instead. It calls the handler, looks at
whatever response the handler decided to return, records it, and **returns the same object
by reference**. There is no line in that file that constructs a response, sets a status or
alters a header. The body is read from `res.clone()`, so the original stream is never
consumed.

**The diff per route is one import, one signature rename and one export at the tail. Zero
lines inside any handler body changed.** That is checkable rather than argued, and it was
independently confirmed: a mapping subagent reading these files mid-round, without being
told what to expect, reported "Every handler body is byte-identical to before, just renamed
to an internal `xHandler` function and exported as `withRefusalRecording(surface, xHandler)`.
All refusal strings/conditions are unchanged."

Ten handlers are wrapped: submit, post, approve, reject, listing-create, trainer join and
trainer dispute for refusals; browse, my-submissions and listings for arrivals.

### It stores what happened, never a category

`ActivityEvent.message` holds **the exact sentence the person was shown**. BL-775 measured
413 distinct free-text rejection reasons on this platform and concluded raw text beat every
attempt to classify them. A category can always be derived later by reading; a sentence
replaced by a category at the call site is gone.

### Proven by direct request, per path

`scripts/sandbox/bl870-prove.ts` drives the real route over HTTP against a **production
build with `DEV_AUTH_BYPASS=false`** and real minted cookies. **16 assertions, 0 failed.**

| Path | Status and message returned | Rows written |
|---|---|---|
| missing `listingId` | 400 `"listingId is required."` | **exactly 1** |
| a marketplace-banned clipper | 403 `"You're temporarily banned from marketplace submissions due to missed deadlines. Ban lifts in 72 hours."` | **exactly 1** |
| the daily quota, third of two slots | 409 `"This listing has reached its daily submission limit. It resets at midnight UTC."` | **exactly 1** |
| the duplicate Drive link | 409 `"You already have a pending submission with this Drive link."` | **exactly 1** |
| **two ACCEPTED submissions (201, 201)** | unchanged | **zero refusal rows** |

Each recorded row was checked to carry the message **verbatim**, plus the surface and the
status. Not one behaviour changed: every status and every sentence is the route's own.

### IT FAILS OPEN, PROVEN BY BREAKING IT

Reading a try/catch proves nothing, so the writer was broken where it actually runs. **The
`activity_events` table was renamed out from under the running server**, a request was
made, and the table was renamed back:

```
5. with the table GONE          -> 400 "listingId is required."
PASS  case 5 THE REQUEST STILL WORKED with the recording table missing
```

The refusal is byte-identical to the same case with the table present. **A recording
failure changed nothing a person could see.**

---

## PART 2 — WHAT PEOPLE REACHED, AND WHAT IT COSTS

Arrivals are recorded on the successful GETs behind browse, my-submissions and the poster's
own listings. Proven live: three GETs produced exactly three rows, one per surface.

**IT IS DEDUPED PER PERSON PER SURFACE PER HOUR, and that is what keeps it cheap.** The
owner's question is "did anyone even open it", which one row an hour answers exactly as well
as forty rows a minute. Proven: **six browse calls in a row produced one row, not six.**

### The cost, stated three ways

- **Row size** about 250 bytes including index overhead.
- **The pilot**, one poster and a handful of clippers: on the order of **300 rows a day, so
  about 75 KB a day**, and under **2.5 MB** held at any time.
- **The ceiling, which is what matters.** The dedup makes arrivals bounded by
  `people x surfaces x 24` a day, not by time. At the platform's current 1,698 users that
  ceiling is about 245,000 rows a day, roughly 60 MB a day, which is the honest worst case
  and would never be approached in practice. **The point is that it is a ceiling at all:
  it does not grow with elapsed time the way `clip_stats` does.**

### Retention: 30 days, and it ships in the same commit as the table

BL-856 measured that `notifications` is the **only** table on this platform with a working
retention policy, and that `clip_stats`, `email_events`, `user_events` and
`apify_usage_entries` all grow without limit. A new table would have been the fifth, so its
cleanup is not a follow-up: it is added to the daily `notifications-cleanup` cron, the one
job that already exists to do exactly this.

**Thirty days, not the sixty notifications get.** A notification is something the owner may
want to scroll back to; an activity row exists to answer "what happened during the pilot"
and stops being useful once that question has been asked. It also bounds how long a deleted
person's id can linger in a table that deliberately has no cascade.

### It holds nothing new about anybody

`userId` the platform already holds. `surface` is a fixed dotted key chosen in code, never a
URL, so it can never carry an id or a search term. `message` is the product's own error copy,
written by us and shown to that same person a moment earlier. **The only reader is the
owner's own admin screen**, behind the same three gates as the problem-report stream, which
is the rule `api/admin/problem-reports/route.ts:6-7` states as BL-531's.

*One honesty note: BL-531 has no report in the reports repo. Its rule is quoted here from
the code comment that cites it, not from a document I was able to read.*

---

## PART 3 — CONNECTING THE REPORTS TO THE REFUSALS

**The form already captures everything needed, and NOTHING had to be added to it.**

`ProblemReport` (`prisma/schema.prisma:3652-3710`) already records `userId` and `createdAt`,
which is exactly and only what a join by person and time requires. It also carries
`pagePath`, coarse `platform` and `browser`, `displayMode`, `viewportWidth`,
`clientVersion` and `serverVersion`, `roleAtReport`, `pendingClipCount`,
`recentRejectionCount`, `recentRejectionAt`, `blockedBalanceCents` and
`blockedCampaignName`.

**So the link is a read, not a write.** The activity endpoint runs a correlated subquery
that finds the most recent refusal by the same person within **30 minutes before** the
report, and the screen prints it in words: *"7 minutes earlier this person was refused on
marketplace.submit: This listing has reached its daily submission limit."* When there is
none it says so, rather than leaving a blank the owner has to interpret.

---

## PART 4 — THE ONE SCREEN, WHERE HE ALREADY LOOKS

**It is a section on `/admin/problem-reports`, not a new page.** BL-797 built that surface
for this exact habit, the sidebar already badges it unread, and a report and the refusal
that caused it belong on one screen rather than two. `/admin/command-center` and
`/admin/health` were both considered and both rejected: the first is spend and activity
charts, the second is cron and defence-stack health, and neither is where the owner goes to
read what a person did.

It answers the four questions and nothing else: **how many opened it, how many started
something, how many finished, and where the rest stopped.**

**Every headline is a count of PEOPLE, with the event count beside it.** One person refused
nine times is one person with a problem, not nine problems.

**The refusal reasons are ranked by how many people hit them**, grouped by the exact
sentence, never by a category. Two sentences that mean the same thing appear as two rows,
which is the honest failure mode: the owner reads them and decides.

**IT IS HONEST ABOUT SMALL NUMBERS.** Below five people the panel says, in words:
*"This is 3 people. That is too few to read a pattern into. Every row below is shown in full
so you can look at each one, but an order between them means nothing at this size."* The
rows are still shown. Nothing is hidden; the reader is simply told not to draw a trend from
three events.

---

## PART 5 — THE TRAINER, IN THE SAME VIEW

No second screen. `trainer.join` and `trainer.dispute` are wrapped by the same wrapper and
land in the same table, so a code that did not exist, a second code, a revoked trainer and
every dispute raised all appear in the same ranked list under their own verbatim sentences.
BL-869's own refusal wording carries through unchanged: *"That is your own trainer code. You
cannot be your own trainer."*, *"You already have a trainer. Ask the owner to let you leave
before you join someone else."*, *"This code is not open to new clippers at the moment."*

---

## PART 6 — THE PROOFS

**The sandbox**, BL-842's tooling, `SANDBOX_ROUND=bl870`, opening snapshot taken **before**
anything was created. **`verify-gone.ts`: 50 checks, 50 passed, 0 failed.**

**No money moved and nothing was touched.** Every fingerprint is byte-identical either side:
real payout `d8f515ecf352a93e8e109a628d7c977d`, real user `d4d7b1621a90ea666c62acbd256363fe`,
real clip status `38dcd11665ebe1d52e9cd9ebc675866d`. Clips 9,832 to 9,832. `clip_stats`
359,693 to 359,693. `agency_earnings` 4,652 to 4,652. Approved earnings $14,269.32
unchanged to the cent. **INVARIANT VIOLATIONS: 0.** Zero payouts created.

**The render**, BL-793's method: **35 assertions, 0 failed**, at 320, 375, 414, 1280 and
1440, against a production build with the dev auth bypass off. Each shot read
`window.innerWidth` back, measured **0** horizontal overflow, confirmed the splash lifted,
confirmed the page did not bounce to `/login`, confirmed the panel and the funnel were on
screen, and **confirmed a real recorded refusal sentence was readable on the page**. The
owner reviews from his phone, which is why 320 is first.

**The owner used for the render cannot be emailed.** BL-868 refused to create a sandbox
OWNER because owner email fan-out has no `isTestUser` filter. That reasoning was right and
its conclusion one step too strong: the fan-out sends to `recipient.email`
(`notifications.ts:619`) and the gate is "OWNER and has an email", and `User.email` is
nullable (`schema.prisma:100`). An owner row with `email: null` is **structurally
unemailable**. Asserted in the fixture output: `email is null: true`.

**Accessibility: two MUST FIX items, both found and both fixed.** The panel declared its own
polite live region while the page already had one, which is how an announcement gets dropped
when two regions update in the same tick; it now calls the page's single announcer through
an `onAnnounce` prop. And it was mounted **above** the page's `h1`, putting an `h2` and three
`h3`s before the only `h1` and inverting the outline for anyone navigating by heading; it now
sits after it. The review found no hardcoded colour, no emoji, no dash used as a bullet, and
confirmed the `aria-pressed` period selector and the `role="list"` ranked rows as correct.

**Builds, from a log, exit codes echoed rather than inferred.** Clean baseline **before any
edit**: `TSC_BASELINE_EXIT=0`, 0 errors, eslint present with 3 binaries so the hooks gate is
not a silent no-op. Build #1 `BUILD1_EXIT=0`, 0 TS errors. Build #2, after the accessibility
fixes: **`BUILD2_EXIT=0`, 0 TS errors**. Hooks gate **0 errors, 10 warnings** against a limit of 11, every
warning in a file this round did not touch.

**The schema change is additive and isolated.** One new table, no foreign key, no column
added to any existing model, applied with `run-schema-sql.js` and never `prisma migrate`.
Verified in the catalogue: 8 columns with every optional one nullable, 4 indexes plus the
primary key. Rollback is printed in the migration file itself and is a single
`DROP TABLE IF EXISTS public.activity_events;`, which loses no money, no status and no clip.

**The 6 money files, `tracking.ts` and `campaign-era.ts` are byte-identical by blob OID on
both refs.** No Apify actor, 11 BL-678 guards intact, no Prisma in a browser bundle, no
Supabase pool errors.

### A tooling gap this round hit and closed

Driving real routes mints product rows the ledger cannot know. The sweep learned to adopt
`activity_events` by their sandbox `userId`, which satisfies LOCK 2 directly. Two video hash
rows and two audit rows still could not be adopted, because neither table has a column
holding a sandbox id; both were removed by explicit id through scripts that print the exact
SQL first and refuse any row that is not the shape this round created.

---

## THE MODEL SPLIT

**Opus** decided everything about what gets written and where: the wrapper architecture over
fifty call-site edits, the verbatim-message rule, the table shape, the 30 day retention and
where it lives, the decision to put the screen on an existing page, the unemailable-owner
reasoning, and this report.

**Sonnet** did three jobs, all retrieval or review: distilling eight prior reports, mapping
every refusal path to file:line, and the accessibility review whose two MUST FIX items are
fixed above.

**Nothing money-touching was split, and nothing money-touching was changed.** This round
writes to exactly one new table and reads from three. It computes no money, and the proof
shows every money fingerprint identical either side.

---

## WHAT THE OWNER SHOULD DO

1. **Redeploy.** Recording does nothing until it is deployed. The table is already created,
   so the screen will render empty rather than error in the meantime.
2. **Open `/admin/problem-reports` tomorrow.** The activity panel is at the top, under the
   heading. Set it to "Today".
3. **Read the refusal list first, then the reports.** If one sentence has more people beside
   it than the others, that is the rule to look at, provided the count is above the floor the
   screen names.
