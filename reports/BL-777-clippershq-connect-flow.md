# BL-777 — the connect-TikTok flow, which did not exist

**THE FLOW CANNOT BE EXERCISED END TO END TODAY, AND NO PILOT IS CLAIMED. The bundle.social
organisation has NO TEAM and NO SUBSCRIPTION.** Probed live this round against the owner's real key:
`GET /api/v1/team` returns `200 {"items":[],"total":0}`. So no TikTok account can be connected by
anybody yet, and not one analytics field has ever been observed. What IS proven live is the connect
contract itself, below. Three prior rounds on this topic were confidently wrong from documentation;
this one separates what was measured from what was read.

**2026-08-11 · DB `now()` = `2026-08-11 17:38:56.659465+00` · BUILD.**
Base `origin/main` @ `3e96698b`, branch `checkpoint/BL-777` @ `d0caa37a`, **verified pushed**
(`origin/checkpoint/BL-777 == local HEAD`). Tags `pre-BL-777` and `post-BL-777` on origin. **Not
merged to main**, per the round's own ship instruction. Isolated worktree `C:/m777`, short path,
`node_modules` never junctioned, removed at the end. **This round wrote nothing to the database and
created nothing on the vendor side.** No key or token was logged, printed or committed.

---

## PART 0 — WHAT THE OWNER MUST DO, AND WHAT THE CLIPPER MUST DO

### Probed live this round, not read

| call | result | what it proves |
|---|---|---|
| `GET /api/v1/organization` | **200** | org "ClipperHQ", created `2026-08-11T11:28:36.818Z` |
| `apiAccess` | **true** | **API access is already on with `subscription: null`** |
| `subscription` | **null** | no paid plan |
| `teams` | **`[]`**, `GET /api/v1/team` → `total: 0` | **the actual blocker** |
| `POST /api/v1/social-account/connect` with a bogus `teamId` | **404 `{"message":"No team found"}`** | the route EXISTS and the body PARSED |
| the same call with the body omitted | **400**, `issues` naming exactly `teamId` and `redirectUrl` | the request contract is confirmed |
| `GET /api/v1/social-account/by-type?type=TIKTOK&teamId=…` | **404 "No team found"** | the verification route exists |

**The blocker is not the key, and it is not the plan. It is that there is no team.**

### The owner's steps, in order

1. **Create a team** in bundle.social. Every connect and analytics call takes a `teamId` and there are
   zero teams. This is the only hard blocker.
2. **Set `BUNDLE_SOCIAL_TEAM_ID`** in Railway to that team's id. The feature reads it at call time and
   renders "not switched on yet" until it is present, so nothing breaks in the meantime.
3. **Run two SQL files by hand** in the Supabase editor, both additive and both safe to re-run:
   `scripts/migrations/BL-777-clip-account-provider-links.sql` (new, this round) and
   `scripts/migrations/BL-773-clip-analytics-snapshots.sql` (**still unrun**: `information_schema`
   reports the snapshot table does not exist in production).
4. **Then ask a clipper.** BL-772 measured five voluntary connections covering 71.0% of TikTok
   earnings.

**A plan is NOT required to connect.** `apiAccess` is already `true` with no subscription, and the
vendor's own FAQ confirms a free tier exists. A plan governs **import volume**, which is the real
constraint: **Free 5 posts/month, Pro 100, Business 500**, against roughly 308 TikTok clips a month.

### What the clipper must do inside TikTok itself

**This cannot be done for them, and without it the analytics fields are empty however well the link
works.** TikTok's own wording on both insights endpoints: account owners must *"first publish at least
one video, then tap the 'Turn On' button on the Analytics page of their mobile TikTok app"*.

The path: **Profile, then the menu (top right), then TikTok Studio or Creator Tools, then Analytics,
then "Turn On".** Exact wording varies by app version, so the owner should screenshot his own before
writing instructions. Two further facts worth putting in the message: `profile_views` is
Business-account-only, and audience demographics need 100+ followers, so **a smaller clipper will
connect successfully and correctly see no demographics.** That is normal, not a fault.

---

## PART 1 — THE CLIPPER-FACING FLOW

**Entry point:** inside the account detail dialog on `/accounts`, for a **TikTok** account with status
**APPROVED** only. That is the right scope because the link is per clip account, which is exactly the
key the capture uses, and because pairing it with a named `@handle` is what makes a wrong-account link
detectable at all.

It sits **between the rejection-reason block and the Actions row**. Remove (irreversible account
deletion) is the last tab stop and the focus trap's wrap target; putting an optional control after it
would make that control reachable only by tabbing **through** Remove.

**The copy, verbatim, before they click:**

> **TikTok stats**
> You can let us read the stats TikTok already shows you for clips you have posted, like how long
> people watched and where your views came from.
> We can only read stats for clips you have already posted. We cannot post anything, we cannot read
> your messages, and we cannot change anything on your account. You can unlink whenever you want, from
> right here.
> This is optional. Your clips, your earnings and your withdrawals work exactly the same if you never
> link it.
> **[ Link TikTok stats ]**

**The handoff:** the button posts to our API, which asks the vendor for an OAuth URL and returns it;
the browser then navigates in the same tab. `disableAutoLogin: true` is set deliberately, because
without it a clipper who has authorised before is bounced straight through and never sees what they
are agreeing to.

**The destination is deliberately not named** in the button's screen-reader text. Whether the first
screen is `tiktok.com` or an intermediate vendor page could not be observed without a team, and naming
the wrong one is its own defect. The hidden text says only *"you leave Clippers HQ in this tab to
approve, then come back here"*.

**The return** lands on `/accounts` with a short outcome, rendered as a heading that receives focus.
It does **not** auto-open the dialog: this page removed an auto-navigation in BL-326 for exactly that
reason, and a focus-trapped dialog engaging on page load repeats it. Reachability is an explicit
**"Open account"** button instead.

### It is optional, and that is enforced rather than promised

BL-772 measured that **76 of the 146 clippers holding a balance have no TikTok account at all**, and
that **59.7% of unwithdrawn money ($1,673.12 across 94 clippers) was earned with zero TikTok
involvement**. Proven by grep, not asserted:

- The whole feature imports exactly three shared modules: `@/lib/db`, `@/lib/auth-guards`,
  `@/lib/get-session`. **No money module, no eligibility module, no payout module.**
- **0 files** under `api/payouts`, `api/clips`, `api/earnings`, `payout-minimum-shared.ts` or
  `clipper-access.ts` reference any part of it.
- `/api/accounts/mine` is **byte-unchanged**. The card indicator reads a **separate** endpoint that
  returns an empty array for every clipper today, so an unconnected clipper's page renders exactly as
  it does now.

---

## PART 2 — THE CONNECTED STATE, AND DISCONNECTING

Six states, one **stable** heading across all of them, no icon and no colour on any of them.

| state | what the clipper sees |
|---|---|
| not switched on | "This is not switched on yet. There is nothing for you to do." **And no button at all**, because a permanently disabled control with no reachable reason is a dead end. |
| not linked | the invitation copy above |
| linked | "Linked on {date} to @{handle}." plus **Unlink** |
| linked to a different account | both handles in a labelled `<dl>`, no icon, no warning colour |
| a failure came back | one plain sentence naming what happened |
| linking in flight | the button stays, name unchanged, `aria-busy` |

**The mismatch state is the one that had to be got right.** The vendor's handle and the Clippers HQ
handle are shown as two labelled facts, in full `--text-primary` weight, with `<bdi>` around each so a
right-to-left handle does not render scrambled. **No `role="alert"`** on three independent grounds: it
fires on insertion so it would announce nothing on a page load, `assertive` interrupts, and the role
literally means *error*, which is the accusation the wording is avoiding. The copy closes with
*"Nothing is wrong with your clips either way."*

### Disconnecting, and what happens to captured analytics

**They are KEPT. The copy says so, and the code does exactly that.**

> We will stop reading new stats straight away. The stats we already saved stay saved, because they
> are the record of clips that were already checked and paid.

`revokeLink` flips the link row's `status` and stamps `revokedAt`. **It references
`clipAnalyticsSnapshot` nowhere at all** (harness-asserted), so it cannot delete a snapshot.

Justified in order of weight. First, **a snapshot is the record of what was true when a clip was
reviewed and paid**; deleting it on request would let the record of a decision be erased after the
money moved. Second, **the vendor deletes its own analytics after 30 days**, so this platform's copy is
the only durable one. Third, nothing in the store identifies a person beyond the clip it belongs to.

**What unlinking does stop is immediate:** `isAccountConnected` reads exactly the row that is revoked,
so the next capture tick skips that account with no other coordination.

### Every failure path

| what happens | what the clipper sees | does it block anything? |
|---|---|---|
| cancels on TikTok's screen | "Nothing was linked. If you closed the TikTok screen or pressed cancel, that is fine, you can try again whenever you want." **No red, no warning word**, button returns enabled | no |
| does not grant all permissions | "TikTok did not pass on all the permissions we asked for" | no |
| vendor errors, times out, or is unreachable | one sentence per case, all offering a retry | no |
| the token expires or they revoke in TikTok's own app | the vendor stops reporting a connected account, the next status read returns not-linked, and capture stops | no |
| links the wrong account | both handles shown, unlink and try again | no |
| not configured yet | "This is not switched on yet. There is nothing for you to do." | no |
| signed out during the round trip | "You were signed out on the way back, so nothing was linked." | no |

**None of them can block earning, submitting or withdrawing**, structurally rather than by promise: no
code on any of those paths can reach this feature (PART 5).

**The return leg trusts nothing in the query string.** The vendor documents `tiktok-callback` as the
parameter name for **both** its success and its error case, so a returning URL cannot prove a
connection happened. The route asks the vendor what it actually holds instead. A cancelled
authorisation therefore resolves to `no_account` with no interpretation at all.

---

## PART 3 — WIRED TO THE CAPTURE

**How a connected clipper's clips are recognised:** a clip carries `clipAccountId`; a row in
`clip_account_provider_links` on that same clip account with `status = 'active'` and
`revokedAt IS NULL` is what makes it eligible. That is the only marker, and it is the column
`isAccountConnected` already keyed on, so BL-773's capture needed one added check rather than a
rewrite. BL-723's unmerged token table is still consulted after it, so that branch keeps working if it
ever lands.

**When capture fires:** a new scheduled route, `/api/cron/tiktok-analytics-capture`, requiring
`CRON_SECRET` regardless of `NODE_ENV`. **Not on the submit path**, so submission never waits for a
vendor and cannot fail because of one. The cadence is BL-773's `shouldCapture`, unchanged and
unforked: first at 48h, refresh every 24h, stop after 7 flat days.

### Two findings, both real defects, both fixed here

**FINDING 1 — BL-773's capture called the analytics endpoint wrongly.** The vendor's own OpenAPI for
`GET /api/v1/analytics/post` takes **`postId` WITH `platformType`**, or **`importedPostId` alone**, and
documents the two as mutually exclusive. `teamId` **is not a parameter of that route at all**, so
BL-773's `teamId` query argument was inert and its bare `postId` was the wrong identifier. Clippers
post natively, so a clip reaches the vendor through a **history import** and `importedPostId` is
correct. Fixed with an explicit `idKind`.

**FINDING 2 — ongoing refresh for imported posts is OFF by default.** The vendor: imported posts join
the regular refresh cycle only when *"controlled by an organization-level setting"*, enabled by
contacting them, where *"Additional platform usage fees may apply"*. **So even on a paid plan, ongoing
analytics for natively-posted clips is not something the price includes by default.** This was not
known to BL-770, BL-772 or BL-773.

### Staying inside the cap, and how the owner knows

`MONTHLY_CAPTURE_BUDGET` defaults to **100** and is overridable by env, which matters now that the
free tier is known to be **5**. The count is read from our own stored rows and checked **before** any
vendor call.

Measured fresh this round rather than carried forward: **301 TikTok clips in the last 30 days from 42
clippers**, so the average clipper posts about 7 a month and the concentration curve puts the top few
far above that.

| connected clippers | est. TikTok clips/month | inside 100? | inside 5 (free)? |
|---|---|---|---|
| 1 (a top clipper) | roughly 19 | yes | **no** |
| 5 | roughly 93 | **yes, just** | no |
| 10 | roughly 143 | **no, 43% over** | no |

**With one connected clipper the Pro cap is not close.** On the **free** tier even one clipper exceeds
it, so the owner should set `BUNDLE_SOCIAL_MONTHLY_CAPTURES=5` until he takes a plan.

**At the cap the run stops before spending anything** and returns
`{"ran":false,"reason":"import_cap","budgetUsed":…,"budgetTotal":…,"remaining":0}`. Every successful
run returns the same three numbers, so **one request tells the owner exactly how close he is**, and
`clip_analytics_snapshots` is a single-table row count if he prefers SQL.

**Fails open, and never fabricates.** Each clip is captured inside its own try, so one bad clip cannot
end the run; the route answers 200 with a summary even when every capture failed. It writes **no clip
field** (harness-asserted: no `clip.update`, no `writeClipEarnings`). An absent field is stored as
`fieldStatus: "absent"` rather than a zero, which is BL-773's design and is why an expired field can
never render as *"0 seconds watched"*.

---

## PART 4 — WHAT COULD BE PROVEN, AND WHAT COULD NOT

**No account could be connected, so no raw response is pasted. Pasting a documentation sample dressed
up as a live capture is precisely the failure this line of rounds keeps being warned about.**

**All ten analytic fields remain UNTESTED**, at every clip age: `averageTimeWatchedSec`,
`fullVideoWatchedRate`, `totalTimeWatchedSec`, `reach`, `videoViews`, `profileViews`,
`impressionSources`, `audienceCountries`, `audienceGenders`, `audienceAges`.

**Proven with real calls:**

- The key authenticates; the organisation config was read live.
- **`POST /api/v1/social-account/connect` exists**, its body schema parses, and it names exactly
  `teamId` and `redirectUrl` as required. The connect contract in the code matches the API's own
  validator, not a documentation reading.
- **`GET /api/v1/social-account/by-type` exists.**
- `clip_account_connections` exists in production with **17 columns**, `accessTokenEnc` and
  `refreshTokenEnc` both **NOT NULL** — which is why this round added a separate table rather than
  reusing it.
- `clip_analytics_snapshots` **does not exist** in production yet.

**Proven only structurally:** that a real connect returns a URL; that the return leg classifies a real
cancellation; that the mismatch state fires against a real vendor handle; that a capture stores a real
field. **No browser render either** — the accounts page needs a clipper login, the same honest limit
BL-762 and BL-765 recorded.

**What the owner must supply for any of it to become verified:** the team, then
`BUNDLE_SOCIAL_TEAM_ID`, then the two SQL files, then one clipper who taps "Turn On".

---

## PART 5 — NOTHING ELSE MOVES

| proof | result |
|---|---|
| files in the diff touching money, submission, payout or eligibility | **0** |
| money/payout/eligibility files referencing this feature | **0** |
| shared modules the feature imports | **3**: `db`, `auth-guards`, `get-session` |
| clip status written anywhere in the feature | **0** |
| `clip.update` / `writeClipEarnings` in the cron | **0** |
| `console.*` statements across all new files | **0** |
| `/api/accounts/mine` response | **byte-unchanged** |
| BL-678 markers | **27, unchanged.** No Apify actor run |

**Byte-identical by blob OID, on `origin/main` and on this ref:** `clip-earnings-writer.ts`
`ac5be7de`, `earnings-calc.ts` `797e2098`, `balance.ts` `e887f80a`, `tracking.ts` `83ce4bab`,
`clip-earnings-invariant-middleware.ts` `61cef393`, `money-decimal.ts` `ef5cdae7`, `campaign-era.ts`
`106e16ad`, `apify.ts` `656bf4c0`.

**No owner economics and no machine suspicion reach a clipper.** The feature surfaces exactly two
things to a clipper: whether their own account is linked, and to which handle. It shows no analytics
figure, no score, no flag and nothing about review (BL-518, BL-521). *(BL-531 does not exist; this
reports archive begins at BL-539. The live equivalent is the select-allowlist posture, which this
round matches by never selecting anything owner-only into a clipper response.)*

**No credential is stored at all.** Under bundle.social the vendor completes the OAuth and holds the
token; the new table has **no token column** and must never gain one. There is nothing on this
platform to leak, rotate or lose.

---

## GATES, HONESTLY

`NPMCI_EXIT=0`. `npx prisma generate` run before tsc because `npm ci` wipes the generated client:
`PRISMA_EXIT=0`. **eslint v9.39.4 confirmed present**, so the hooks gate is not a silent no-op.
`npx tsc --noEmit` **exit 0, 0 errors**. `npm run build` **exit 0**, read from a redirected log with
the exit code echoed by hand and never piped through `tail`. Hooks gate **0 errors, 11 warnings**, at
the ceiling of 11 and unchanged. Offline harness `scripts/bl777-verify.ts`: **24 passed, 0 failed**.

**Two harness assertions failed on first run and both were harness bugs, not code defects**, recorded
rather than quietly fixed: one looked for a literal ownership string that the status route expresses
inside a helper, and one compared positions in the import list instead of the function body. Both were
corrected to measure the thing they claimed to measure.

### Accessibility ran twice, and the second pass said NO-SHIP

The design was reviewed **before any UI existed**: nine blocking items, all applied. The written code
was then reviewed again, which is what caught the two that mattered.

| new issue | what it would have done |
|---|---|
| the generalised focus trap wrapped to the **ends** of the dialog rather than the next tab stop | with the unlink confirm open, **Tab skipped both its buttons** and landed on Close; **Shift+Tab landed on Remove**, making irreversible account deletion the immediate neighbour of a confirm heading |
| the section focused its heading synchronously | child effects run before parent ones, so the dialog recorded that heading as its focus-restore target; the jump never landed AND closing dropped focus to the grid instead of the button that opened it |
| a failed unlink closed the confirm and moved focus in the same beat as the message | the announcement was swallowed and the reappearing Unlink button **read as success** |
| the link button cleared its busy state under the outgoing navigation | `return` does not skip `finally`; the spinner reverted and a second press could start a second authorisation |
| the open-at-section intent was never reset | every later manual open of that account would steal focus into an optional section |

All five fixed, then rebuilt and re-harnessed. Two premise corrections from the same review, recorded
because they are repo-wide rather than this round's: `text-accent` is **5.42:1** on card and passes (the
3.40:1 figure is white **on** accent, i.e. the primary button fill, which fails); and `--bg-page` is
**defined nowhere**, so the 41 existing `ring-offset-[var(--bg-page)]` usages paint a white halo. No
new control here uses either.

**Database untouched, and the drift is accounted for rather than hidden.** At the start: 5,360 live
clips, 4,394 approved, **0 invariant violations**, $8,644.36 approved earnings, 166 payout rows. After
the push: **5,372 live clips** and newest clip write `2026-08-11 18:14:51`. **That +12 is ordinary
clipper submissions and the tracking cron, not this round**, and the decisive proof is that
`clip_account_provider_links` **still does not exist in production** (`information_schema` returns 0):
this round has no table to write to and wrote nothing. **Invariant violations 0** and **166 payout
rows**, both unchanged.

322 approved TikTok accounts across 272 clippers, and **301 TikTok clips in the last 30 days from 42
clippers**, which is the population that could eventually link.

---

## WHAT THIS ROUND DID NOT DO

- **It connected nothing**, because there is no team. No pilot is claimed.
- **It created nothing on the vendor side.** Creating the team would have changed the owner's vendor
  account without his say, and PART 0 states it as his step precisely because it is his to take.
- **It created no table in production.** Both SQL files are written and waiting.
- **It built no score, threshold or verdict**, and nothing here can reject a clip.
- **It changed no money file, no clip status and no payout.**

**Rollback:** `git revert -m 1 <merge>`, or `reset --hard pre-merge-BL-777`. The new table is additive,
empty, and read by nothing else; `DROP TABLE IF EXISTS clip_account_provider_links;` afterwards if
wanted.
