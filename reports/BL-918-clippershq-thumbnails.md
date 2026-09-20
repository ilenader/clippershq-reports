# BL-918 — every marketplace preview had failed, the cause was the site's own CSP, and the picture now comes from Google on the server

> **NOTHING IS UNREMOVABLE AND NO SQL IS OWED. FIRST LINE, AS THE ROUND REQUIRES.** 15 ledgered
> rows, **`VERIFIED: 0 of 15 remain`**, 0 failed; two partial runs before the real one were each
> destroyed to zero first. Three owner bell rows my sandbox submission created on the REAL owner
> accounts (about a clip named `BL918-SANDBOX-DELETE-ME`) were deleted by a scoped statement,
> `rowCount=3`, verified `0` left. Closing census against the opening one: every count and every
> fingerprint identical, including the fingerprint of every real marketplace clip's thumbnail
> columns, so **no real row was written by this round from this machine**; the rows the fix
> legitimately writes are written by the production cron and are read back in the ADDENDUM.
> **One thing cannot be undone and is disclosed:** the first sandbox submission ran the real
> owner notification and Resend accepted ONE email to the owner's own address (the other two
> owner addresses are refused by Resend, as BL-910 recorded); the subject line names the sandbox
> marker. The proof deleted the provider keys before loading `.env.local`, which loads after, so
> the deletion did nothing; disclosed in PART 5.

**2026-09-20. Shipped on `checkpoint/BL-918` (`0d7f8566`), merged to `main` as `7efe3702`, pushed
and verified (`origin/main == local HEAD`). Tags `pre-BL-918`, `post-BL-918`, `pre-merge-BL-918`,
`post-merge-BL-918`. Worktree `C:\w\b918` removed and verified gone. `checkpoint/BL-723` not
merged. Every one of the six protected money files byte-identical by blob OID (PART 5). **Then three more merges the same evening, each with its own pre/post tags and
read back from production in the ADDENDUM: `c0da7d74` (trace), `8e173936` (the sweep runs from the cron
script Railway actually executes), `aa449775` (the sweep runs where the storage key lives, kicked by the
poster's own request). Final count at 20:36 UTC: 20 of 27 real clips show a real picture, 5 say why
they cannot, 2 wait for the next poster request.**

---

## THE HEADLINE

1. **THE BROWSER CAPTURE COULD NEVER HAVE WORKED, AND THE WALL IS OURS.** `next.config.ts:76` sends
   `media-src 'self' blob: data:`. A `<video>` whose `src` is drive.google.com is refused by the
   browser before a single request leaves it: real Chromium against four real file ids, with and
   without `crossOrigin`, eight runs, every one `MEDIA_ELEMENT_ERROR: Media load rejected by URL
   safety check` in **0 to 4 ms** with an EMPTY network log and the console line "Loading media from
   'https://drive.google.com/uc?export=download&id=…' violates the following Content Security Policy
   directive". That is why all 27 failure rows are stamped 0.1 to 2.3 s after their submission.
2. **BEHIND THAT WALL IT WOULD STILL HAVE FAILED, THREE MORE WAYS, MEASURED WITH CURL.** Drive
   answers `uc?export=download` with **no `Access-Control-Allow-Origin` on any of the 26 file ids**
   (so `crossOrigin="anonymous"` fails and a tainted canvas would follow), with a **2.4 KB virus scan
   interstitial page for 13 files** (those above about 25 MB), with a **1.24 MB sign-in page for 4
   files** not shared to anyone with the link, and with video bytes for 9. The owner's hypothesis
   was right in every part and still not the first cause.
3. **GOOGLE ALREADY HAS THE PICTURE.** `https://drive.google.com/thumbnail?id=<id>&sz=w640`
   answered a real frame (JPEG or PNG, 640 px wide, 2.7 KB to 140 KB, looked at, not assumed) for
   **22 of 26** ids, unauthenticated, no video downloaded, no credential; the 4 unshared ids answer
   the sign-in page. The fix asks for that picture on the server at submission, sniffs the bytes,
   stores **our own copy** in the uploads bucket, and records a **status** and a **sentence** when
   there is no picture. Nothing is fabricated.
4. **STORAGE IS CONFIGURED AND REACHABLE IN PRODUCTION**, measured rather than assumed: 7,349
   ordinary clip covers live in the `uploads` bucket at `wfnzotxaeuqbammdccwx.supabase.co`, the
   latest written **16:02:56 today**, and a fetch of one returns `200 image/jpeg`. It is NOT
   configured on this machine (no `SUPABASE_SERVICE_ROLE_KEY` among the 29 variable names), which
   bounded what the sandbox could prove and is said so in PART 5.
5. **THE CARD NEVER LIES IN A GREY BOX AGAIN.** Present: the frame behind a skeleton until it paints.
   Absent: "No preview", the reason in the poster's words, and the submitted date. The maker is told
   at submission and on his list, in the words that fix it. Rendered in all three states at 320,
   375, 414, 1280 and 1440, pan 0 px everywhere.

6. **THEN PRODUCTION TAUGHT TWO THINGS (ADDENDUM).** The sweep was wired into an HTTP route production
   never calls, so three ticks did nothing; moved into the cron script Railway runs. That script's
   service has no storage key, so its first sweep fetched 17 pictures and stored none; the sweep now
   refuses to start without storage and is kicked from the web service by the poster's own request.
   Nine minutes after that deploy a real poster opened a clip and **20 real pictures were stored in
   nine seconds**, one fetched back and looked at.

**PROOFS: 21 of 21 sandbox checks, 5 of 5 HTTP failure paths (two re-run with corrected
expectations, PART 5), 10 of 10 renders, all 18 prebuild guards, hooks gate 0 errors 10 warnings.** **Storage round: 14 of 14, sandbox destroyed 6 of 6.**

---

## PART 0 — THE MODEL SPLIT

| tier | what ran there | subagents |
|---|---|---|
| **accessibility-lead** | the review of the preview component and the fallback, BEFORE it was written; its findings were applied and are listed in PART 4 | **1** (84,950 tokens) |
| cheapest | nothing this round: the census, the probes and the reproduction were each one command, cheaper to run than to delegate and read back | **0** |
| **strongest (Opus), NOT SPLIT** | every figure, every probe, the reproduction, the approach, every line of the fix, every proof, this report | **0 subagents between it and the row, the file or the browser** |

**Connections:** one at a time, `run-select.js` or one `$queryRawUnsafe` per statement; the cap was
one. No Apify actor, no vendor call, no paid API: the only outside requests were to Google's public
thumbnail and download endpoints, unauthenticated, the same request the product now makes. No
credential was invented. No real maker's link is printed anywhere in this report; the 26 ids were
read into a local file for the probes and that file was deleted at teardown.

---

## PART 1 — THE FAILURE AS IT STANDS TODAY

**The population, cast to `::text`, db now `2026-09-20 16:08:46.240938+00`.** 27 marketplace clips
ever submitted, `2026-09-18 20:37:39.698` to `2026-09-20 12:43:44.241`. Link shape, counted:

| shape | count | file id stored |
|---|---|---|
| Drive file link (`/file/d/<id>/view?usp=…`) | **25** | yes, 33 characters, all 25 |
| Drive folder link (`/drive/folders/…`) | 1 (the oldest, REJECTED) | no |
| docs.google.com file link | 1 | yes |

**Thumbnail stored: 0 of 27. Failure recorded: 27 of 27** (`thumbnailFailedAt` set on every row, 0.1
to 2.3 s after `createdAt`), `thumbnailSource` null on all. Reasons, verbatim: "Your browser could not
read the video from Drive, so we could not make a preview." (**26**) and "We could not read a file id
from that link, so we could not make a preview." (**1**, the folder). **The failure rate is 27 of 27**;
BL-910 measured 15 of 15 and twelve more clips landed since, every one of them the same.

**Did the capture run? Yes, every time, in the maker's browser, at submit time**, from
`EditorSubmitModal.tsx:207` (`void captureDriveThumbnail(...)`, fire and forget after the 201) into
`capture-thumbnail.ts`, which built a `<video>` on `uc?export=download`, and on the `error` event
posted the sentence to `/api/marketplace-v2/clips/[id]/thumbnail`, which wrote it through
`recordV2Thumbnail`. **So the failure was recorded, honestly, every time**, which is the one thing
BL-878 got right; what it could not record was WHY, because the browser never told it.

**Where a thumbnail lives when it exists:** `marketplace_v2_clips.thumbnailUrl`, a public URL in the
Supabase `uploads` bucket, written through the service role key, exactly where 7,349 ordinary clip
covers already live (`clips.thumbnailUrl LIKE '%/storage/v1/object/public/uploads/%'`, latest
`16:02:56` today, one fetched: `200 image/jpeg`). Configured and reachable in production.

**What swallows.** `capture-thumbnail.ts:46-56` (`report`): the POST that records the failure is
itself wrapped in `try {} catch {}` "silent on purpose"; `capture-thumbnail.ts:70-75`: the video's
`error` event is mapped to one sentence with the `MediaError` code and message discarded, which is
precisely the piece of evidence that would have named the CSP on the first day. Both files are
deleted by this round.

---

## PART 2 — THE FAILURE, WATCHED

**Method.** Playwright Chromium, a page on the real origin `https://clipershq.com/login` so the
request is cross origin exactly as in production, the capture code's own element construction
(`crossOrigin`, `muted`, `playsInline`, `preload="metadata"`, `src = uc?export=download&id=…`),
against four real ids chosen for their shapes: a >25 MB file (interstitial), a 23 MB mp4 (bytes), an
unshared file (sign-in), a 97 MB octet-stream. Console and network read back.

**The real error, verbatim, all eight runs (four ids, `crossOrigin` set and not set):**
`{"outcome":"error event","mediaError":{"code":4,"message":"MEDIA_ELEMENT_ERROR: Media load rejected
by URL safety check"},"ms":0..4,"readyState":0,"networkState":3}`, network `[]`, console `error:
Loading media from 'https://drive.google.com/uc?export=download&id=<redacted>' violates the following
Content Security Policy directive`. The production header, read with curl: `media-src 'self' blob:
data:`; `img-src 'self' data: blob: https://cdn.discordapp.com https://*.supabase.co
https://*.ytimg.com https://img.youtube.com` (so a hotlinked googleusercontent thumbnail would be
refused too, which is why the copy must be ours).

| hypothesis | evidence | verdict |
|---|---|---|
| the Drive link is an HTML page, not a decodable video | true for 13 of 26 (interstitial, 2.4 KB) and 4 of 26 (sign-in, 1.24 MB); 9 of 26 return real bytes (`video/mp4` or `application/octet-stream`, 1.8 to 102 MB) | **in, second cause**, partial |
| cross origin taints the canvas, `toBlob` returns null | never reached; but no Drive response carries `Access-Control-Allow-Origin` (0 of 26 with `Origin: https://clipershq.com`), so it would have | in, third cause, never reached |
| `crossOrigin` never set, or Drive does not answer the header | it IS set (`capture-thumbnail.ts:63`); Drive does NOT answer the header | in, same as above |
| the file is not shared to anyone with the link | 4 of 26 (sign-in page on `uc`, `401` on `/file/d/<id>/preview`, sign-in page on `thumbnail?id`) | in, for 4 |
| capture before enough data | never reached: `readyState 0` at the error | ruled out |
| capture works, upload fails or lands nowhere | never reached; storage is configured and reachable (PART 1) | ruled out |
| mobile only | identical on a desktop context and an iPhone 12 context; the refusal is the CSP, not a gesture rule | ruled out |
| the code is never reached on the real path | it is reached: 27 failure rows exist, each written by its POST | ruled out |
| **the site's own `media-src` refuses the element before any request** | 8 of 8 runs, 0 to 4 ms, empty network log, the CSP named in the console; the header read from production | **the first cause, ruled in** |

**What the evidence supports:** a chain of four, the first of which is ours. Opening `media-src` would
expose the other three; none of them is fixable from a browser without Google's cooperation, and the
capture was the wrong instrument for the job.

---

## PART 3 — THE APPROACH, CHOSEN BEFORE IT WAS WRITTEN

| approach | cost | failure mode | verdict |
|---|---|---|---|
| **ask Google for the thumbnail it already has** (`thumbnail?id=<id>&sz=w640`), server side, store our copy | one HTTPS request per clip at submission, 3 to 140 KB, no video, no credential, no new dependency, no new runtime | 4 of 26 today answer the sign-in page (unshared, or a wrong id); Google may change the endpoint | **chosen** |
| embed Drive's own preview iframe on the card | none server side | `frame-src` is not in the CSP either, a 16:9 iframe per card on a phone, and a card that cannot be looked at without loading Google's viewer | rejected |
| fetch the file and extract a frame with ffmpeg | 1.8 to 102 MB per clip through Railway, ffmpeg in the image, seconds of CPU, and the >25 MB interstitial still has to be clicked through by a script | a media pipeline for a picture Google already made | rejected |
| capture in the maker's browser from a decodable source | needs a same-origin or CORS-enabled video source, which Drive is not | the chain in PART 2 | rejected |
| a combination with ordered fallback | the chosen route with an honest recorded status for the remainder IS the fallback | | as chosen |

**Clips already submitted:** filled in retroactively by the tracking cron, which now sweeps up to 20
absent previews per hourly tick whose last attempt is older than six hours or never happened, newest
first; the 27 existing rows take two ticks. Cost: 27 requests of a few KB each, once, then one request
per new submission and one per absent clip per six hours. **A maker who fixes his sharing gets a
picture within the hour without asking anybody.**

---

## PART 4 — WHAT SHIPPED

**`src/lib/marketplace-v2-thumbnail.ts` (new, 250 lines).** `fetchDriveThumbnail(fileId)`: GET the
endpoint with redirects followed and a 10 s timeout; classify by MAGIC BYTES (BL-366's lesson) as
`image`, else by the final URL or the body as `not-shared` (accounts.google.com sign-in),
`no-file` (a true 404), or `unavailable`. `captureV2Thumbnail({v2ClipId, driveFileId})`: never throws;
stores the copy through `uploadImageToBucket` at `marketplace-v2-thumbnails/<id>.<ext>`; writes
`thumbnailUrl` + `thumbnailSource = "drive-thumbnail"`, or `thumbnailUrl null`, `thumbnailSource` one
of `ABSENT_NOT_SHARED | ABSENT_NO_FILE_ID | ABSENT_NO_FILE | ABSENT_UNAVAILABLE | ABSENT_STORAGE`,
`thumbnailFailedAt`, and the maker's sentence in `thumbnailFailedReason`. `sweepV2Thumbnails({limit,
campaignId?})` for the cron and the proof. **No column was added:** `thumbnailSource` carries the
status the way `ClipStat.sharesSource` carries ABSENT.

**The sentences, verbatim.** Maker, not shared: "Google asked us to sign in instead of giving us a
preview, which usually means the Drive file is not shared with anyone with the link, or the link is
wrong. In Drive, choose Share, then Anyone with the link." Poster, not shared: "Google asked us to sign
in instead of giving us a preview, which usually means the maker has not shared the file with anyone
with the link, or the link is wrong." No file id: "We could not read a file id from that link, so we
could not ask Google for a preview." Unavailable: "Google did not give us a preview this time. The
clip itself works normally." Storage: "We got a preview from Google but could not save our copy. The
clip itself works normally." "Or the link is wrong" is there because a bogus id lands on the same
sign-in page as an unshared file (measured), and BL-908's rule holds: the sentence refuses nothing.

**`clip-thumbnail.ts`:** the bucket write extracted verbatim into `uploadImageToBucket` and
`sniffImage` exported as `sniffImageBytes`; `rehostImage` calls the former and is unchanged in
behaviour. **`marketplace-v2-catalogue.ts`:** `submitV2Clip` awaits `captureV2Thumbnail` after the
row exists and returns `{ thumbnail: { status, reason } }`; `EDITOR_CLIP_SELECT` carries
`thumbnailFailedReason`. **`clips/route.ts`:** the 201 carries it. **`marketplace-v2-poster.ts`:**
the poster catalogue carries `thumbnailStatus`, `thumbnailReason` and `submittedAt`, still no CPM.
**`EditorSubmitModal.tsx`:** the browser capture call is gone; on a 201 with an absent status the
maker sees a 12 s toast "Submitted, but there is no preview yet. <the maker's sentence>".
**`editor-client.tsx`:** under the submitted date, "No preview. <sentence>" when absent.
**`cron/tracking/route.ts`:** the sweep, isolated, after the agency monitor. **`activity-record.ts`:**
the `mkt2.thumbnail` surface retired, because `check:v2-role-is-a-gate` R7 refused the build the
moment its route was gone, which is that guard working. **Deleted:** `capture-thumbnail.ts` and
`clips/[id]/thumbnail/route.ts`.

**`v2-ui.tsx`, `V2Preview`, and what the accessibility review changed before it was written:**
`alt=""` (the frame's content cannot be put into words the server has, and "Preview frame of X" would
read the title a fourth time; the absent state carries the information in text); the absent block
names the clip sr-only ("No preview for <title>") because it sits before the card's heading in the
DOM; `motion-reduce:animate-none` on the skeleton and `motion-reduce:transition-none` on the fade; an
image already `complete` before hydration is detected through `naturalWidth` or it would stay at
opacity 0 on a cached hit; the icon uses `--mp-text-muted` (6.00 to 1 on `--mp-surface-1` in both
themes) rather than `--text-muted`, which flips to near-black in light; the absent box is NOT
`overflow-hidden`, so an `aspect-ratio` box grows to its min-content height at 200 percent zoom
instead of clipping the sentence, and the detail page's outer `overflow-hidden` was dropped for the
same reason; dates are formatted in UTC on both sides so hydration agrees. **`CatalogueCard.tsx` and
`detail-client.tsx`** mount it. **`--bg-page`: 0 uses in the changed area** (the only mentions in
`v2-ui.tsx` are comments recording that it does not exist). No money figure is computed anywhere;
nothing else on the catalogue was redesigned.

---

## PART 5 — THE PROOF, THE TEARDOWN, THE MERGE

**Sandbox `bl918sbx-`**, opening census before anything was created (`16:35:11.471276+00`), five test
people (owner, three makers, a poster), one test campaign with a maker door. `server-only` shimmed
the way `backfill-clip-thumbnails.ts:47-60` does, so the EXACT live modules ran.

| check | result | what made it pass |
|---|---|---|
| A1 a shared real file | `image/jpeg 76147 bytes` | Google answered bytes whose first three are `FF D8 FF` |
| A2 an unshared real file | `{"kind":"not-shared","status":200}` | the final URL was accounts.google.com |
| A3 a nonexistent id | `not-shared` and the sentence says "or the link is wrong" | same page, so the words say both |
| B1 `submitV2Clip`, shared file | 201; `thumbnail.status = ABSENT_STORAGE`; row `ABSENT_STORAGE`, sentence "could not save our copy" | Google gave the picture; this machine has no service role key, and the row says exactly that rather than nothing |
| B2 `submitV2Clip`, unshared file | 201, NOT refused; row `ABSENT_NOT_SHARED` with the maker's sentence | the sentence written equals `V2_THUMB_WORDS.ABSENT_NOT_SHARED` character for character |
| B3 a folder link | 400, not 429 | BL-908's `classifyDriveLink`, unchanged |
| B4 a row with no file id | `ABSENT_NO_FILE_ID` with its sentence | the recorder's null branch |
| C1 the sweep leaves a fresh failure alone | attempted 0 of 2 | `thumbnailFailedAt` under six hours |
| C2 the sweep retries an old failure | the row aged to 7 h was re-classified from Google (`storage-not-configured` here) | the `lt: cutoff` clause; scoped to the sandbox campaign so no real row was written from this machine |
| D1, D2 the sentences | every absent status has a maker and a poster sentence, no dash bullets, no emoji; the poster is never told to change sharing | read from the two modules |
| F the full population | 10,219 live clips 0 invariant breaches 0 negative; 20 maker rows 0 breaches; no double pay; **22 budgeted campaigns 0 over** (both v2 aggregates and the owner's cut counted); paid is final, maker 0 and v2 poster 0; **ANGIE BROWN $2,700 ACTIVE**; both reconciliation forms 0 and 0; **the four money fingerprints identical before and after** | one statement each |

**HTTP failure paths against the worktree's build on port 3918, each its own person:** nobody signed
in **401**; a signed-in person who has chosen no side **403** "Choose whether you make clips or post
clips first…"; the sandbox maker sending a folder **400** with BL-908's sentence; the poster catalogue
**200** carrying `thumbnailStatus` and `submittedAt` for both sandbox clips and no CPM field; none 429.
**Two of my own checks were wrong and the product was right, disclosed:** the first run expected the
sandbox POSTER to be refused as a maker and got **201**, because the side lock is per campaign
(BL-903) and he held no side on the sandbox campaign; and it expected the sandbox maker's folder link
to be refused with 400 and got **403**, because that person had never chosen a side (the library
call in the proof bypasses the route's gate). Both re-run with the right expectation; the clip the
first run created was ledgered and destroyed.

**Renders**, as the sandbox poster, `/market/catalogue`, three states (present with a real frame from
our own bucket staged on the sandbox clip, loading with the image request stalled, absent with
`ABSENT_NOT_SHARED`):

| width | innerWidth | URL | pan | present | loading | absent |
|---|---|---|---|---|---|---|
| 320 | 320 | /market/catalogue | 0 px | `alt=""`, loaded, opacity 1, no skeleton, 254x143 | skeleton on, opacity 0 | "No preview", the sentence, "Submitted 20 Sept 2026", 254x149 |
| 375 | 375 | same | 0 px | 309x174 | same | 309x174 |
| 414 | 414 | same | 0 px | 348x196 | same | 348x196 |
| 1280 | 1280 | same | 0 px | 318x179 | same | 318x179 |
| 1440 | 1440 | same | 0 px | 371x209 | same | 371x209 |

The absent card at 375, as rendered: "No preview for BL918-SANDBOX-DELETE-ME unshared. Google asked us
to sign in instead of giving us a preview, which usually means the maker has not shared the file with
anyone with the link, or the link is wrong. Submitted 20 Sept 2026". `--bg-page` uses in the DOM: 0.
The real clips on the same page, not yet swept, read "No preview. No preview has been made for this
clip yet. Submitted 19 Sept 2026", which is true.

**Money, byte for byte.** `git rev-parse main:<path>` against the branch: `clip-earnings-writer.ts
5b40d49e`, `earnings-calc.ts 00410634`, `balance.ts 67c30c89`, `tracking.ts 672d2ab3`,
`clip-earnings-invariant-middleware.ts 61cef393`, `money-decimal.ts ef5cdae7`, **all six identical**.

**Guards and builds.** All 18 prebuild guards pass; none was touched, so none was demonstrated;
`check:v2-role-is-a-gate` R7 refused the first build over the retired surface and passed once the
declaration was removed. Hooks gate **0 errors, 10 warnings** against the cap of 11; eslint present,
three binaries. tsc **exit 0** after every edit; `npm run build` on the branch **`BUILD_EXIT=0`**;
merge tree OID `44a4caa08455` equals the branch tree; `npm run build` on merged `main`
**`BUILD_MERGE_EXIT=0`**.

**What went wrong in the round, disclosed.** The provider keys were deleted before `.env.local` was
loaded, which loads after, so a real notification email reached the owner about a sandbox clip
(one; Resend refuses the other two owner addresses). The first proof run crashed on `server-only`
twice before the shim was copied in. Two HTTP expectations were mine and wrong (above). Three real
owner bell rows were created by the sandbox and deleted by a scoped statement. The phone screenshots
are covered by the install prompt even after "Maybe later" is pressed; the assertions are on the DOM
and passed, the desktop screenshot shows all three states side by side.

**Teardown.** 15 ledgered (including the extra clip, four activity rows and one bell row the product
wrote), **15 deleted, 0 already gone, 0 failed, 0 of 15 remain**; 0 `bl918sbx-` traces across users,
campaigns, v2 clips, notifications, audit and activity. Closing census (`16:46:39`) identical to the
opening one on every count and every fingerprint, the real v2 thumbnail fingerprint included.

---

## WHAT COULD NOT BE DETERMINED FROM THIS MACHINE

* **The PRESENT branch end to end.** No service role key here, so no picture could be stored from
  this machine; the branch is proved in production by the cron sweep and read back below.
* **Whether the four sign-in files are unshared or mislinked.** Indistinguishable from outside.

---

## ADDENDUM — WHAT PRODUCTION DID, READ BACK, AND THE TWO THINGS IT TAUGHT

Everything above shipped as `7efe3702`. This section is what happened after, in the order it
happened, every number read from `audit_logs` (`V2_THUMB_SWEEP`) and `marketplace_v2_clips`, none
inferred.

**1. Three ticks, nothing moved, and no trace of why (17:41, 17:50, 18:01 UTC).** 0 of 27 rows
changed, 0 trace rows. The trace commit (`c0da7d74`, "every attempt, failure and top-of-hour run
writes a `V2_THUMB_SWEEP` row") went out and the next tick wrote nothing either, which is the
answer: **the code was not running at all.** The sweep had been wired into the post-steps of the
HTTP route `/api/cron/tracking`, and production does not call that route. Railway's cron service
runs `scripts/run-tracking-cron.ts`, which calls `runDueTrackingJobs` directly; the script's own
comment says the route's post-steps "live in the HTTP route, which this script does not call".
Measured, not assumed: one `cron_runs` row per tick for the last three hours, every one written by
the script (`isBatchTick=true` at every minute, BL-200's shape), and none of the route's
`isBatchTick=false` heartbeats. **This means the L5 agency-earning monitor and the payout reminder
sweep, which live only in the route, have never run in production either.** Logged as a finding in
the BACKLOG entry (item 5); it wants its own round because the L5 monitor is a money guard.

Fixed as `8e173936` (branch `checkpoint/BL-918-cron-script`, tags `pre-BL-918-cron` /
`post-BL-918-cron` / `pre-merge-BL-918-cron` / `post-merge-BL-918-cron`): the script calls the sweep
after the batch, with the same `server-only` shim the ordinary cover backfill uses, and writes the
trace row itself. Proof `scripts/sandbox/bl918-cron-import-check.ts` (the shimmed import resolves
under tsx; a sweep of a nonexistent campaign attempts 0). Build clean, money files identical by
blob OID, worktree removed.

**2. The first sweep that ran (19:51:04 to 19:51:11 UTC) fetched 17 real pictures and stored none
of them.** Trace: `attempted 20, present 0, ABSENT_NOT_SHARED=3, ABSENT_STORAGE=17`, every storage
outcome `storage-not-configured`. The second (20:00:35): `attempted 7, ABSENT_STORAGE=5,
ABSENT_NOT_SHARED=1, ABSENT_NO_FILE_ID=1`. So Google answered exactly as PART 2 measured (22 of 26
real ids give a frame) and **the cron service has no storage credentials.** It never needed any:
ordinary covers are stored by the web service at `POST /api/clips/[id]/thumbnail` (the 7,349 covers
in the headline), and nothing in the tracking path writes to the bucket. Neither `railway.json`
nor anything on this machine can add a variable to that service (`railway whoami`: not logged in),
so the fix went where the key already lives.

Fixed as `aa449775` (branch `checkpoint/BL-918-storage`, tags `pre-BL-918-storage` /
`post-BL-918-storage` / `pre-merge-BL-918-storage` / `post-merge-BL-918-storage`), three moves in
`src/lib/marketplace-v2-thumbnail.ts`:

* **A process without storage asks Google for nothing.** `isV2ThumbnailStorageConfigured()` reads
  the same two variables `clip-thumbnail.ts` reads; the sweep checks it before reading a row and
  returns `skipped: "storage-not-configured"`, stamping nothing. The cron's traces since then read
  exactly that (20:20:48, 20:30:05).
* **Our own failure is retried at once.** A row whose `thumbnailSource` is `ABSENT_STORAGE` is
  eligible immediately (Google already answered; only our copy is missing); a Google failure still
  rests six hours.
* **The web service runs the sweep from the poster's own request.** `kickV2ThumbnailSweep(caller)`
  is fire-and-forget (the catalogue answers as it always did), single-flight, at most once every ten
  minutes per process, never without storage, and is called at the top of `listCatalogueForPoster`
  and `getCatalogueClipForPoster` in `marketplace-v2-poster.ts`. `sweepV2ThumbnailsTraced` carries
  the sweep and its trace row (caller named) for the script, the route and the kick alike, so the
  script and the route each shrank to one call and keep working the day the cron service is given
  the two variables.

Proof `scripts/sandbox/bl918-storage-prove.ts`, **14 of 14**, sandbox `bl918ssbx-` (one owner, one
maker, one campaign, one v2 clip written directly so no notification could fire; the two trace rows
the kicks wrote were pointed at the sandbox owner and ledgered): without storage the UNSCOPED sweep
skips before reading a row and the kick returns false; with fake storage variables scoped to the
sandbox campaign, an `ABSENT_STORAGE` row stamped seconds earlier is retried at once, then rests once
Google has answered; first kick true, second false (in flight), third false (spacing), a kick past
the window true; each kick wrote one trace naming its caller. Every real thumbnail column and every
money fingerprint byte-identical before and after. Destroyed: **6 of 6, 0 remain**; 0 `bl918ssbx-`
traces across users, campaigns, v2 clips, audit. One detail worth recording: the bogus file id that
answered Google's sign-in page this morning answered `http-400` this evening, so the sweep recorded
`ABSENT_UNAVAILABLE` for it; the classification is by what Google says, and Google changed its mind.
Build clean (0 errors, hooks gate 10 warnings, all 18 guards), branch and merge trees identical by
OID, money files identical by blob OID against `pre-merge-BL-918`, worktree removed and verified gone.

**3. What a real poster then did, unprompted (20:19:39 to 20:19:48 UTC).** Nine minutes after the
deploy, a poster opened a clip's detail page. The web service kicked the sweep: trace
`caller=poster-detail, attempted 20, present 20, drive-thumbnail=20`. **Twenty real pictures stored
in nine seconds**, at `<bucket>/marketplace-v2-thumbnails/<clipId>.jpg`, the latest of them fetched
back from this machine: `200 image/jpeg`, 6,302 bytes, JPEG magic bytes, 640 by 640, looked at (a
dark first frame of a person in profile, which is the frame Google chose, not a sign-in page and not
a placeholder). The four `ABSENT_NOT_SHARED` rows and the folder link were not attempted again (they
rest six hours, and the folder has no id to ask for), exactly as designed.

**4. What this machine could and could not do to finish it.** Two rows remain `ABSENT_STORAGE` (the
20:00 tick stamped seven, the poster's kick took twenty rows newest first, and two from 2026-09-18
fell outside the twenty). They are eligible at once and the next poster request on the site fills
them, no cron tick and no owner action needed. I tried to be that request: `scripts/sandbox/
bl918-kick-prod.ts` created one test person (`bl918ksbx-`), minted a session cookie for that person
alone, and sent one GET to the live catalogue; production answered **401** (a cookie minted here
does not carry into production, which is right), nothing was written, the person was destroyed
(**1 of 1, 0 remain**, 0 traces). I did not try a second way in. So the count below is the count as
read at the end of the round, not a projection.

**5. The count, read back at 20:36 UTC.** Of the 27 real marketplace clips ever submitted:

| state | rows | what the poster sees |
| --- | --- | --- |
| `drive-thumbnail` | **20** | a real frame from the file, our own copy, behind a skeleton until it paints |
| `ABSENT_NOT_SHARED` | 4 | "No preview", the sign-in sentence, the submitted date; the maker is told what fixes it |
| `ABSENT_NO_FILE_ID` | 1 | "No preview", the folder-link sentence, the submitted date |
| `ABSENT_STORAGE` | 2 | "No preview" until the next poster request, which retries them at once |

**Every file Google can answer for now has a picture except the two that fell outside one sweep,
and the five without one say why in the poster's words.** BL-910 measured 15 of 15 failures; this
round measured 27 of 27 failures at its start.

**Production commit chain:** `0d7f8566` (branch) → `7efe3702` (merge) → `c0da7d74` (trace) →
`1c68a50d` / `8e173936` (cron script) → `870bb049` (backlog note) → `de60a58f` / `aa449775`
(storage precondition and the web-service kick). Every push verified `origin/main == local HEAD`.
Tags for a one-step rollback of each: `pre-merge-BL-918`, `pre-merge-BL-918-trace`,
`pre-merge-BL-918-cron`, `pre-merge-BL-918-storage`. `checkpoint/BL-723` not merged. Teardown sweep
(`sweep-round-leftovers.mjs`, dry run) reclaimed nothing: every leftover directory is under the
three-day floor or is another repository's worktree.

**Two lessons, written down.** Read the trace before the code: three "nothing happened" ticks were
not a bug in the sweep but a sweep that was never called, and the fourth was a process that could
never have finished what it started. And a process must check what it cannot do BEFORE it starts:
the first sweep asked Google twenty times for pictures it had nowhere to put.
