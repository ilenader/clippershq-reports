# BL-919 — three real frames from inside the video at 25, 50 and 75 percent, the owner picks, and the video is deleted the moment they exist

> **NOTHING IS UNREMOVABLE AND NO SQL IS OWED. FIRST LINE, AS THE ROUND REQUIRES.** Two sandboxes.
> `bl919sbx-` (the pipeline proof): 25 ledgered rows, **`VERIFIED: 0 of 25 remain`**, 0 failed; one
> earlier run crashed on a real bug and its 18 rows were destroyed first (`0 of 18 remain`).
> `bl919rsbx-` (the renders): 10 ledgered rows plus 13 activity rows the product wrote for the
> sandbox people, **`0 of 10` and `0 of 13 remain`**. Zero `bl919%sbx-` traces across users,
> campaigns, v2 clips, audit, activity and notifications. No real row was written by this round
> from this machine: every real v2 clip's picture columns (thumbnail AND frame) and every money
> fingerprint are byte-identical before and after (PART 4). **The only real rows this fix will
> write are the twelve `frame*` columns of `marketplace_v2_clips` and one `V2_FRAMES_JOB` audit
> row per attempt, and it has not written any yet: nothing runs on deploy, and at merge time
> production is UNOBSERVED (PART 4, said plainly).** No provider key was used in any proof; the
> render server ran with every provider variable unset and the dev bypass off. No paid vendor
> call, no Apify actor. Downloads made from this machine, all of them maker files already on the
> platform: 322.9 MB + 139.8 MB + 23.6 MB + 36.1 MB (PART 1), 23.6 MB twice more and about 30 MB of
> partial downloads in the proof (PART 4). Sixteen ranged GETs of 64 bytes each.

**2026-09-21. Shipped on `checkpoint/BL-919` (`2fab9d4b`, backlog `3b81b5c`), merged to `main` as
`21e7c660`, pushed and verified (`origin/main == local HEAD`). Tags `pre-BL-919`, `post-BL-919`,
`pre-merge-BL-919`, `post-merge-BL-919`. Branch and merge trees identical by OID, so the branch
build IS the merge build; main was then re-installed and built as well. Worktree `C:\w\b919`
removed and verified gone. `checkpoint/BL-723` not merged. Every one of the six protected money
files byte-identical by blob OID (`git rev-parse HEAD:<path>`), `tracking.ts` in no diff.**

**Model split.** Opus designed the pipeline, wrote every line that runs on the server or touches
approval, every proof, and this report. Two Haiku readers were used for reading only: the first
read the WRONG files (same-numbered reports from other projects in the same directory) and its
summary was discarded (VERIFIED wrong, disclosed); the second read the five ClippersHQ reports
and its summary was used for orientation only (READ). The accessibility lead (an agent, plus six
specialists it ran) reviewed the UI plan BEFORE any UI line was written; its hard requirements
are followed and named in PART 3 (READ, then VERIFIED in the renders). Subagents opened no
database connection. Connection cap: this session's scripts hold one Prisma client each, one at a
time, disconnected at exit; the render server held its own pool for eleven minutes and was killed
by PID.

---

## THE HEADLINE

1. **THE BOX CAN CARRY IT, MEASURED ON THE BIGGEST REAL CLIP.** 322.9 MB, 27.86 s of video:
   downloaded in 34.7 s from this machine, probed in 70 ms, three frames in 0.57 s each, 36.7 s
   end to end, 21 to 38 KB per frame, the video unlinked. The smallest (23.6 MB) in 4.8 s.
2. **FFMPEG WAS NOT IN THE DEPLOYED IMAGE AND NOW IS PART OF THE CHANGE.** `railway.json` names
   NIXPACKS with no `nixpacks.toml`, and the node provider installs node and npm and nothing else.
   The binaries now ship as npm platform packages pinned in the lockfile (`@ffmpeg-installer/
   linux-x64` 4.1.0, `@ffprobe-installer/linux-x64` 5.2.0), installed by the same `npm ci` the
   image already runs, kept external to the server bundle, and **their presence in the deployed
   image is written into every trace row**. Read back at 12:50:32 UTC, thirteen minutes after the
   push, from the cron service's container built from this commit: `frameTooling.present: true`,
   `ffmpeg version N-47683-g0e8eb07980-static`, `ffprobe version N-66595-gc2b38619c0-static`.
   The binaries install and run in Railway's image.
3. **IT RUNS IN THE WEB SERVICE, WHICH HOLDS THE KEY.** BL-918 measured the cron service has no
   storage credentials and that HTTP cron routes never run; the web service stored twenty
   previews in nine seconds. Approval kicks the job there, fire and forget; the owner's backfill
   button drains the rest there. A process without storage asks Google for nothing.
4. **DRIVE SERVES THE VIDEO BYTES, NO INTERSTITIAL, FOR ALL 16 APPROVED FILES.** Measured with a
   64 byte ranged GET each: `206`, `application/octet-stream`, `Content-Range` with the real size,
   magic bytes `ftyp` (QuickTime `qt` for 14, `isom` for 2), from `drive.usercontent.google.com`.
   The population: 16 approved clips, 23.6 MB to 322.9 MB, **2,715 MB in all**. The 4
   `ABSENT_NOT_SHARED` clips are PENDING or REJECTED and are never downloaded; the one that was
   put through the video path anyway answered the sign-in page and was recorded as
   `ABSENT_NOT_SHARED`, the same way it failed the thumbnail.
5. **THE VIDEO IS NEVER KEPT.** Unlinked the moment the third frame exists on disk, before the
   first upload (`videoDeletedBeforeUpload: true` in the trace); the temp directory removed in a
   `finally` on every path; a killed process's leftover (reproduced: 9.4 MB of partial video)
   removed by the next job once older than 20 minutes, a fresh one kept.
6. **APPROVAL NEVER WAITS AND NEVER FAILS FOR THIS.** Approval of a clip with an unreadable file:
   200 in 70 ms, the clip APPROVED before, during and after the job failed in the background, the
   Drive thumbnail still on it.
7. **NO CLIP REGRESSES.** The card's order is the owner's choice, then the platform's default,
   then BL-918's Drive thumbnail, then the honest absent state. Every real row's picture columns
   are byte-identical after the round, and the fallback is a pure function proved on six cases.

**PROOFS: 37 of 37 pipeline checks, 30 of 30 HTTP and render checks (12 failure paths each its
own person, 3 success paths, 15 renders at 320, 375, 414, 1280 and 1440 in four states), all 18
prebuild guards, hooks gate 0 errors 10 warnings against a cap of 11, tsc 0 errors, build exit 0.**

**THE COUNT, IN ONE LINE:** at merge, **0 of 16 approved marketplace clips show a frame extracted
from inside the video** (nothing runs on deploy and the owner has not yet pressed the button),
against BL-918's 20 of 27 Drive thumbnails, all of which still show; the first press of "Take
pictures for 16 approved clips without them" or the next approval changes that, and the trace rows
say what happened.

---

## PART 1 — WHAT THE BOX CAN DO, ESTABLISHED BEFORE A LINE WAS DESIGNED

**Is ffmpeg in the deployed image.** No. Established from the build configuration rather than
from this machine: `railway.json` declares one service, builder NIXPACKS, `npm start`, and the
repository holds no `nixpacks.toml`, no `Dockerfile`, no `apt` or `nix` package list; the NIXPACKS
node provider installs node and npm. This machine had ffmpeg nowhere either until the packages
below were added, which is the point: a developer binary is not a container binary. **How it is
added:** `@ffmpeg-installer/ffmpeg` and `@ffprobe-installer/ffprobe` in `package.json`; each
resolves a platform package from the npm registry at install time (`linux-x64` for the image,
`win32-x64` here), both now in `package-lock.json` as optional dependencies, so the Railway
build's `npm ci` fetches the Linux static binaries from the registry with no GitHub download and
no postinstall script. `next.config.ts` lists both under `serverExternalPackages` so the bundle
requires them from `node_modules` at runtime and their `__dirname` lookup survives. The
alternative (`nixPkgs = ["ffmpeg"]` in a new `nixpacks.toml`) was not chosen because it could not
be exercised here at all; the npm route runs the identical code path on this machine (VERIFIED:
`ffmpeg version N-92722` and `ffprobe version 2023-02-13` answered `-version` under the module's
own `probeFrameTooling`). **Confirmed in the deployed image after the push:** the trace rows
(`V2_THUMB_SWEEP`, which the cron writes every ten minutes, and `V2_FRAMES_JOB`) carry
`frameTooling: { present, ffmpegVersionLine, ffprobeVersionLine }` measured in the deployed
process, and the cron's 12:50:32 UTC row reads `present: true` with the Linux static builds
(`N-47683-g0e8eb07980-static`, `N-66595-gc2b38619c0-static`). That is the cron service's
container, built by the same NIXPACKS build from the same commit as the web service's; the web
service's own row appears with its first frame job.

**Where the job runs, and does that service hold the key.** The WEB service. BL-918 measured
(read back from `audit_logs`, not assumed) that the cron service's sweep fetched 17 pictures and
stored zero because it has no `SUPABASE_SERVICE_ROLE_KEY`, that Railway runs
`scripts/run-tracking-cron.ts` directly so nothing in an HTTP cron route runs, and that the web
service stored twenty previews in nine seconds from a poster's request. So: `approveV2Clip`
(`src/lib/marketplace-v2-catalogue.ts`) calls `kickV2FrameJob("approval", id)` after the approval
is committed, fire and forget; the owner's backfill route drains up to fifty in the background of
his request; both run in the web process that already writes the bucket. The job's first line
checks `isV2ThumbnailStorageConfigured()` and, without the two variables, skips before claiming a
row (PART 4, B1). **Owner action, only if he wants the cron service to run it too:** give that
service `NEXT_PUBLIC_SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`; nothing here depends on it.

**The container's limits.** Not readable from this machine: `railway whoami` answers
"Unauthorized" and no Railway token is present. What is known: the job never holds the video in
memory (it streams to disk through a counting transform), the biggest real file needs 323 MB of
temp disk for under a minute, and no work runs inside a request (the approval returns before the
job starts, the backfill returns 202 with the count and drains behind it). The trace row records
`totalMemMB`, `freeMemMB`, `rssMB`, `tmpFreeMB` and `tmpTotalMB` of the deployed container on
every job, so the real numbers are read back after the first run rather than guessed here.

**Can the server fetch a Drive VIDEO.** Yes, and the real response is printed. For each of the
16 approved clips' file ids, one GET of `https://drive.usercontent.google.com/download?id=<id>
&export=download&confirm=t` with `Range: bytes=0-63`:

| clip | status | content type | size from Content-Range | magic bytes |
| --- | --- | --- | --- | --- |
| cmu7hifb… | 206 | application/octet-stream | 127.4 MB | `ftyp qt` |
| cmu7hja5… | 206 | application/octet-stream | 245.2 MB | `ftyp qt` |
| cmu7hjth… | 206 | application/octet-stream | 306.9 MB | `ftyp qt` |
| cmu7hkds… | 206 | application/octet-stream | **322.9 MB** | `ftyp qt` |
| cmu7hl45… | 206 | application/octet-stream | 191.4 MB | `ftyp qt` |
| cmu7hmvd… | 206 | application/octet-stream | 139.8 MB | `ftyp qt` |
| cmu7hnck… | 206 | application/octet-stream | 127.5 MB | `ftyp qt` |
| cmu7hnpo… | 206 | application/octet-stream | 251.4 MB | `ftyp qt` |
| cmu7ho3o… | 206 | application/octet-stream | 97.6 MB | `ftyp qt` |
| cmu7hohw… | 206 | application/octet-stream | 101.7 MB | `ftyp qt` |
| cmu7hosx… | 206 | application/octet-stream | 91.1 MB | `ftyp qt` |
| cmu7hp74… | 206 | application/octet-stream | 229.2 MB | `ftyp qt` |
| cmu8dp97… | 206 | video/mp4 | 23.6 MB | `ftyp isom` |
| cmu8f2ry… | 206 | video/mp4 | 36.1 MB | `ftyp isom` |
| cmu8kh7h… | 206 | application/octet-stream | 292.9 MB | `ftyp qt` |
| cmu9iki0… | 206 | application/octet-stream | 130.2 MB | `ftyp qt` |

No confirmation interstitial for any of the 16 (the `confirm=t` form of the URL, on the
`usercontent` host, answers bytes for files above 25 MB where the old `uc?export=download` form
answered BL-918's 2.4 KB virus-scan page). `Content-Disposition: attachment` with the maker's
file name, not printed. **For a file that is not shared** (a real one, put through the video
path in the sandbox): the final URL is Google's sign-in page, `text/html`, classified by its
first 16 KB as `not-shared` and recorded as `ABSENT_NOT_SHARED` (PART 4, C4). **For a bogus id:**
Google answered the sign-in page in the morning, `400` in the evening and `404` at night; each
was recorded as what it was (`ABSENT_VIDEO_DOWNLOAD` with `http-404` on the last run), which is
why the code differs by run and the classifier is by bytes, never by URL.

**The measurement, real code on real clips, no database write** (`scripts/sandbox/
bl919-measure.ts` calls the module's own functions):

| clip | bytes | download | duration | frames at | frame ms | frame bytes | luminance mean 25 / 50 / 75 | differences 25:50 / 50:75 / 25:75 | default |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cmu7hkds… (biggest) | 322,857,875 | 34,677 ms | 27.862 s | 6.966 / 13.931 / 20.897 s | 567 / 576 / 559 | 21,789 / 20,913 / 37,585 | 136.8 / 89.8 / 61.5 | 71.0 / 45.2 / 84.2 | 50 |
| cmu7hmvd… | 139,813,763 | 14,443 ms | 27.867 s | 6.967 / 13.933 / 20.900 s | 362 / 448 / 376 | 31,994 / 35,329 / 30,379 | 135.6 / 63.4 / 108.4 | 72.6 / 46.2 / 53.9 | 50 |
| cmu8f2ry… | 36,142,368 | 6,407 ms | 27.121 s | 6.780 / 13.560 / 20.341 s | 218 / 289 / 157 | 22,724 / 14,906 / 17,893 | 28.8 / **9.9** / 37.1 | 22.4 / 30.0 / 33.1 | **25** |
| cmu8dp97… (smallest) | 23,648,818 | 3,982 ms | 21.419 s | 5.355 / 10.709 / 16.064 s | 130 / 168 / 184 | 46,165 / 27,476 / 15,903 | 105.0 / **21.2** / 33.8 | 85.8 / 24.7 / 79.3 | **25** |

Probe 66 to 77 ms each. The frames at 25, 50 and 75 percent ARE at 25, 50 and 75 percent of the
probed duration (the instants are `round(duration × pct / 100, 3)`, printed above). They differ
from each other by measurement: the mean absolute difference of their 16 by 16 luminance vectors
is 22.4 to 85.8 on a 0 to 255 scale, and their SHA-256 prefixes differ in every case. Two real
clips' 50 percent frames are near solid black (means 9.9 and 21.2 against the threshold of 24)
and the default fell to 25 on both, which is the rule working on real material rather than on a
staged example. The biggest clip's 50 percent frame was looked at: a footballer laughing, the
kind of frame Google's early-frame thumbnail (a dark first frame of the same clip in BL-918) never
gives.

**The population and its cost.** 16 approved clips, 2,715 MB to download once, at this machine's
9 to 10 MB/s about 5 minutes of download in all; Railway's link to Google will be faster. One job
at a time, so a full backfill is 16 sequential downloads. The 4 `ABSENT_NOT_SHARED` clips (3
PENDING, 1 REJECTED) and the 1 `ABSENT_NO_FILE_ID` (REJECTED) are never downloaded because the
claim requires APPROVED; if any is later approved, its video download fails the same way its
thumbnail did and the row says so.

---

## PART 2 — THE PIPELINE, EVERY LIMIT IN NUMBERS

`src/lib/marketplace-v2-frames.ts` (new, about 480 lines, every constant exported):

| limit | value | what happens at the edge |
| --- | --- | --- |
| `V2_FRAME_MAX_VIDEO_BYTES` | 600 MB | `Content-Length` above it: `ABSENT_VIDEO_TOO_LARGE`, no body stored; a stream that passes it regardless of the header is aborted and the partial file unlinked |
| `V2_FRAME_DOWNLOAD_TIMEOUT_MS` | 180 s | `ABSENT_VIDEO_TIMEOUT` with the bytes so far, the partial file unlinked |
| `V2_FRAME_PROBE_TIMEOUT_MS` | 30 s | `ABSENT_VIDEO_TIMEOUT` |
| `V2_FRAME_FFMPEG_TIMEOUT_MS` | 60 s per frame | `ABSENT_VIDEO_TIMEOUT`, three frames or none |
| `V2_FRAME_MEASURE_TIMEOUT_MS` | 15 s per frame | the frame is kept, its luminance unknown, the default rule treats it as fine |
| concurrency | 1 job per process | `drainV2FrameJobs` is single-flight; a second drain returns null and the rows stay claimable |
| output | JPEG, 640 px wide, `-q:v 4` | 15 to 46 KB measured |
| `V2_FRAME_MAX_ATTEMPTS` | 3 | then `not-claimable`, the reason stays on the row; the owner's re-extraction resets it |
| `V2_FRAME_LOCK_TTL_MS` | 15 min | a claim older than this belongs to a dead process and is taken over |
| `V2_FRAME_TMP_MAX_AGE_MS` | 20 min | a `v2frames-*` directory older than this is removed by the next job before it starts |
| near solid | mean ≤ 24 black, ≥ 231 white | on a 16 by 16 grey downscale; the default moves 50 → 25 → 75 → 50 |

**The shape.** `runV2FrameJob({v2ClipId, caller})`: storage check → THE CLAIM → sweep stale temp
→ container facts and tooling probe into the trace → `mkdtemp(v2frames-)` → `downloadDriveVideo`
(head classified by magic bytes before the body is kept) → `probeDurationSec` → `extractFrames`
at `frameInstants(duration)` → **`unlink(video)`** → `measureFrameLuma` × 3 → `chooseDefaultPct`
→ `uploadImageToBucket` × 3 at `marketplace-v2-frames/<clipId>-<pct>.jpg` → the row → `finally`
removes the directory and writes the `V2_FRAMES_JOB` trace (bytes, seconds, per-frame stats,
differences, default, `videoDeletedBeforeUpload`, `tempDirRemoved`, container facts, tooling).
It never throws: a throw anywhere is caught, recorded as `ABSENT_VIDEO_TOOLING` and released.

**Deletion is not at the end of the job.** The unlink sits between extraction and measurement,
before any upload, and runs whether extraction succeeded or not; the `finally` then removes the
directory on success, failure, timeout and throw. The killed-process path (nothing runs) is
covered by the sweep the NEXT job performs on any `v2frames-*` directory older than 20 minutes.

**Approval never blocks or fails.** `approveV2Clip` commits the status first, then calls
`kickV2FrameJob` inside its own try/catch; the kick returns a boolean and starts an un-awaited
promise; the job never throws. Proved by making it fail (PART 4, C13).

**The idempotency key** is the row: `UPDATE marketplace_v2_clips SET frameLockedAt = now(),
frameAttempts = frameAttempts + 1 WHERE id = ? AND status = 'APPROVED' AND (frameStatus IS NULL OR
frameStatus <> 'video-frames') AND frameAttempts < 3 AND (frameLockedAt IS NULL OR frameLockedAt <
now() − 15 min)`. One row updated means this process owns the job; zero means somebody else does
or there is nothing to do. Approving twice, undoing and re-approving, two processes racing, the
owner clicking twice: all resolve on that one statement (PART 4, C9, C9b, C10, C11).

**Retries** are bounded at three attempts, each re-downloads (the file is gone by design and no
code assumes it), and the last reason stays on the row. A storage failure (`ABSENT_STORAGE`, ours)
is retried at once by the next drain; a Google failure rests until the owner asks or the opt-in
cron pass runs. The opt-in pass: `/api/cron/marketplace-v2-frames` (CRON_SECRET, three clips,
synchronous so the caller reads the outcomes) registered as `marketplace-v2-frames` in the
in-process scheduler at :05 and :35, fired only if the owner writes its name into
`RAILWAY_NATIVE_CRON`, and deliberately absent from the watchdog's kind map so it can never
false-alarm CRON_DOWN.

**One vocabulary, not two.** `V2_THUMB_STATUS` gains `FRAMES: "video-frames"`,
`VIDEO_TOO_LARGE: "ABSENT_VIDEO_TOO_LARGE"`, `VIDEO_DOWNLOAD: "ABSENT_VIDEO_DOWNLOAD"`,
`VIDEO_TIMEOUT: "ABSENT_VIDEO_TIMEOUT"`, `NOT_A_VIDEO: "ABSENT_NOT_A_VIDEO"`,
`VIDEO_TOOLING: "ABSENT_VIDEO_TOOLING"`; `ABSENT_NOT_SHARED`, `ABSENT_NO_FILE_ID` and
`ABSENT_STORAGE` are reused as they are; `V2_THUMB_WORDS` carries one maker sentence for each.
The job writes them into `frameStatus`, a second COLUMN in the same vocabulary rather than a
second status system, because the round's rule is that the Drive thumbnail must survive a frame
failure: `thumbnailSource` keeps saying what the placeholder is while `frameStatus` says what the
job did, and `resolveV2Picture` reads both in the fallback order.

**Schema.** `scripts/migrations/BL-919-v2-video-frames.sql`, twelve `ADD COLUMN IF NOT EXISTS`
on `marketplace_v2_clips` (`frame25Url`, `frame50Url`, `frame75Url`, `frameDefaultPct`,
`frameChosenPct`, `frameStatus`, `frameFailedReason`, `frameAttempts` default 0,
`frameAttemptedAt`, `frameLockedAt`, `frameDurationSec`, `frameVideoBytes`), all nullable or
defaulted, applied through `run-schema-sql.js` (12 statements, all applied, read back from
`information_schema`), rollback inside the file, `npx prisma generate` after.

---

## PART 3 — WHAT SHIPPED, AND THE CARD THAT NEVER SHOWS A SILENT GREY BOX

**Server.** `marketplace-v2-frames.ts` (above). `approveV2Clip` kicks. `OWNER_QUEUE_SELECT` and
the poster's `CATALOGUE_SELECT` carry the frame columns; both poster mapping sites resolve ONE
url and ONE status through `resolveV2Picture` (owner's choice → default → Drive thumbnail →
absent) and add `frameExtracting`, `durationSec` and `makerUsername`; the poster response still
carries no CPM field and no raw frame column (checked in S3). `railway-cron-scheduler.ts` gains
the opt-in job. `activity-record.ts` declares `mkt2.frames` and `mkt2.frames-backfill` so the R7
guard holds them to a route.

**Routes (OWNER only, the decision route's four gates in the same order, every refusal
recorded).** `POST /api/marketplace-v2/admin/clips/[id]/frames` with `{action:"choose", pct:
25|50|75|null}` (400 on any other number, 409 when that frame does not exist) or
`{action:"extract"}` (409 unless APPROVED, 409 while the job holds the row, 503 without storage;
resets attempts and kicks). `GET`/`POST /api/marketplace-v2/admin/frames/backfill`: the counts,
and a drain of up to fifty in the background (202 with `willTake`, 409 while one runs, 503
without storage). `GET /api/cron/marketplace-v2-frames` (CRON_SECRET).

**The owner's queue, decided tab** (`admin-client.tsx`, `FrameChooser`). Built to the
accessibility lead's hard requirements, each verified in the renders: a `fieldset` with the
legend "Picture the posters see" (sr-only clip title), one plain sentence "Picking one saves it
at once. Posters see it right away.", three NATIVE radios (`name` unique per row, `sr-only peer`,
the ring on the label, offset against `--bg-primary`, never `--bg-page`), each label wrapping the
frame image (`alt=""`, the label text is the name) and the text "Frame at 25 percent", "Frame at
50 percent, the platform's choice", "Frame at 75 percent" (the default keeps its suffix when
overridden); checked is `border-accent` plus an `aria-hidden` `CheckCircle2`, never colour alone;
rest is `border-[var(--border-strong)]`; every label at least 44 px tall; `data-no-swipe` on the
fieldset; optimistic choice with coalesced POSTs (the last frame asked for wins, at most two
requests while holding an arrow); a server refusal reverts the dot, writes the sentence into a
per-row node every radio describes, and is spoken by ONE page-level `role="status"` live region
(added to the file with `useAnnouncer`); "Use the platform's choice" exists only while an override
does and focuses the default radio before it unmounts; "Take the three pictures again" stays in
the DOM, `aria-disabled` while the job runs; the running row carries `aria-busy` and "Taking
pictures now"; a failed row shows the stored reason and "Tried three times; it will not try again
on its own"; while any row runs the list re-fetches every fifteen seconds and says once, per
clip, "Pictures are ready for {title}" or "Pictures could not be taken for {title}", without
moving focus. A broken frame image keeps its radio and shows "Picture could not be shown".

**The deliberate backfill**, at the top of the queue: one sentence and one button, no heading;
"Counting approved clips without pictures" until the GET answers, then "Take pictures for N
approved clips without them" (or "Every approved clip has its pictures", with the number stopped
for good after three tries when there is one); `aria-disabled` during the POST, focus stays,
the outcome announced. Nothing runs on deploy.

**The poster's card** (`V2Preview`). The order above, resolved server side, so the component
still takes one url and one status. NEW LOADING STATE when there is no picture and the job holds
the row: a pulse (`motion-reduce:animate-none`) with the sentence "Making a preview from the
video" as real text stacked above it (a sibling, never a child, so it never dims), sr-only
"for {title}", a border for forced-colours mode. ABSENT STATE additions, one paragraph each,
identity before date: the reason, "Made by @username", "27 seconds long" as
`<time dateTime="PT27S">` (floored, never rounded up, minutes and seconds in words above sixty),
"Submitted 19 Sep 2026". `alt=""` stays (BL-918's decision: the text carries the information).
BL-918's maker warning at submission is untouched; a maker's list line now also reads the frame
job's sentence when it failed for a reason he can fix, through the same words table.

**Not done, in the BACKLOG with its measurement:** nothing beyond the picture, its chooser, its
loading state and its fallback was touched on the catalogue.

---

## PART 4 — THE PROOF, THE TEARDOWN, THE MERGE

**`scripts/sandbox/bl919-prove.ts`, 37 of 37**, sandbox `bl919sbx-`: an owner (the trace rows'
`OWNER_USER_ID` pointed at him so they could be ledgered), one campaign, and EIGHT makers with one
clip each, one per path (pending, rejected, bogus id, no file id, unshared, small real file,
race, approve). Opening snapshot before anything was created (users 1783, campaigns 36, clips
10318, v2 clips 27, posts 23, maker legs 23, platform legs 23, agency 4951, payouts 251,
notifications 15326, frame traces 0, seven fingerprints). What made each pass:

* **A1** ffmpeg and ffprobe resolve from their packages and answer `-version` (exit 0 both).
* **B0, B1, B2** with the two storage variables deleted in-process: the job returns `skipped:
  storage-not-configured` with NO lock, NO attempt and NO temp directory; the kick returns false.
* **C1** a PENDING and a REJECTED clip: `not-claimable`, attempts 0, zero traces (never downloaded).
* **C2** a folder link: `ABSENT_NO_FILE_ID`, attempt 1, lock cleared, the maker's sentence stored.
* **C3** a bogus id: Google's real answer (`http-404` this run) recorded as
  `ABSENT_VIDEO_DOWNLOAD`, attempt 1, lock cleared, temp directory removed.
* **C4** a real unshared file through the VIDEO path: `signin-200` → `ABSENT_NOT_SHARED`.
* **C5** the 322.9 MB clip against a 1 MB cap: `too-large` from `Content-Length` in 999 ms with
  no `video.bin` on disk. **C6** the same clip with a 2.5 s limit: `timeout` after 10,725,429
  bytes, the partial file unlinked. **C7** the classifier: a JPEG is `other`, HTML is `html`, an
  `ftyp` head is `mp4`.
* **C8** the real 23.6 MB file, fake storage variables: downloaded in 4,719 ms, probed at
  21.419 s, three frames at 5.355 / 10.709 / 16.064 s (46,165 / 27,476 / 15,903 bytes),
  **`videoDeletedBeforeUpload: true`**, the fake key refused the first upload,
  `ABSENT_STORAGE` recorded, `tempDirRemoved: true`, the trace row written with the luminance
  (105.0 / 21.2 / 33.8), the differences (85.8 / 24.7 / 79.3) and the default 25 (**C8c**, the
  fifty percent frame near solid black on a real clip); **C8e** a storage failure is ours so the
  row is claimable again at once.
* **C9** two jobs started at once for one clip: exactly one claimed, one `not-claimable`,
  attempts 1, **downloads 1** (counted from the traces' `download.kind`). **C9b** `approveV2Clip`
  twice on the already approved clip: 200 both times, attempts unchanged.
* **C10** at three attempts: `not-claimable` and not a candidate. **C11** a fresh lock respected;
  a lock aged sixteen minutes taken over.
* **C12a** a child process killed with SIGKILL 2.5 s into the 322.9 MB download left
  `v2frames-JHYhf1/video.bin` with 9,365,533 bytes (the hazard, reproduced). **C12b** aged past
  twenty minutes, the next job removed it (`staleTempRemoved: ["v2frames-JHYhf1"]`) and kept a
  fresh directory.
* **C13** approval of a PENDING clip with an unreadable file: **200 in 70 ms**, status PENDING →
  APPROVED → APPROVED while the job failed behind it (`ABSENT_VIDEO_DOWNLOAD`), the Drive
  thumbnail still present. **C14** the default rule on five cases. **C15** the fallback order on
  six cases.
* **F1 to F6, the full population**: 10,226 live clips, 0 invariant breaches, 0 negative; every
  maker leg's invariant holds; no double pay across agency, maker, platform and posts; 22
  budgeted campaigns, 0 over budget counting both v2 aggregates and the owner's cut; paid is
  final for the MAKER and for the V2 POSTER asked separately; ANGIE BROWN's budget $2700.00,
  ACTIVE, spent $4.70. **G1** both reconciliation forms across the full population: 0 rows each.
* **H1** every REAL v2 clip's picture columns byte-identical (fingerprint over thumbnail and
  frame columns of the 27 real rows). **H2** every money fingerprint identical, so "never
  decrease" holds by identity. **H3** no `v2frames-*` directory survives.

A first run crashed on two real defects, both fixed and disclosed: the claim's `frameStatus <>
'video-frames'` never matched a NULL (SQL three-valued logic; C2, C3, C4 all `not-claimable`),
and a `ReadableStream.cancel()` rejected unhandled on abort and took the process down. The
timeout path (C6) is what found the second.

**`scripts/sandbox/bl919-render.mjs`, 30 of 30**, against a PRODUCTION build on port 3919 with
`DEV_AUTH_BYPASS=false` and every provider variable unset, sandbox `bl919rsbx-` (an owner, a
poster, a maker, a person with no side, a test campaign, five clips staged by hand into the four
states with public images from our own bucket as the frame urls, since this machine cannot store
any). Failure paths, each its own person, every status asserted not 429: nobody signed in 401;
the POSTER choosing 403; the MAKER reading the backfill count 403; the person with no side
starting it 403; the owner picking 33 percent 400 with the sentence; picking a frame on a clip
without frames 409; asking for pictures on a PENDING clip 409 ("approve it first"); asking while
the job holds the row 409; asking on a server without storage 503 and the row untouched; the
backfill without storage 503; an unknown action 400; the cron route without the secret 500 here
(401 in production). Success paths: the owner reads the counts (200, `storageConfigured:
false`); the owner's choice reaches the poster's card at once (25 then 75, the card's url followed
each time, status `video-frames`); the other three cards carry `frameExtracting`, the Drive
fallback and the absent state with duration and maker, and no CPM or raw frame field.

Renders at 320, 375, 414, 1280 and 1440, innerWidth and URL read back, pan measured by scrolling
to 99999 (0 px everywhere), `--bg-page` uses 0 on every page: **the poster's catalogue** with all
four states on one page (the owner's 75 shown with `alt=""` and painted; the pulse plus "Making
a preview from the video" and no image; the Drive thumbnail painted; "No preview", the
not-shared sentence, "27 seconds long", "Made by @…", "Submitted 19 Sep 2026"); **the poster's
detail page** with the chosen frame painted; **the owner's queue** with three native radios in a
`data-no-swipe` fieldset under the legend, the same `name`, 75 checked, "Frame at 50 percent,
the platform's choice", both buttons, `alt=""` on the three frames, every label at least 44 px
tall, the running row `aria-busy="true"` with its sentence, the failed row with its reason and
"Tried three times" and its retake button, the backfill sentence, and exactly one sr-only polite
live region. Phone screenshots are covered by the install prompt even after "Maybe later" (the
BL-918 note); the assertions are on the DOM, and the 1280 screenshot shows the chooser as built.

**Guards.** All 18 prebuild guards pass on the branch (`PREBUILD_EXIT=0`); the flag-gate guard
G2 failed once on the backfill route ("2 handlers, 1 gate call") and the gate was written into
each handler, which is the guard doing its job; no guard script was touched, so none is
demonstrated failing here. Hooks gate 0 errors, 10 warnings against a cap of 11 (one of
headroom, not zero). `eslint` present (`> eslint --config eslint.hooks.mjs` in the build log).
`tsc --noEmit` 0 errors before and after. `npm run build` exit 0 on the branch, read from the log
with the exit code echoed, not through `tail`.

**Teardown.** `bl919sbx-`: 25 ledgered (owner, campaign, eight makers, eight clips, seven trace
rows), **25 deleted, 0 already gone, 0 failed, 0 of 25 remain**; the crashed first run's 18
destroyed the same way first. `bl919rsbx-`: 10 rows, **0 of 10 remain**, then the 13 activity
rows the product wrote for those people, ledgered by the same gate and **0 of 13 remain**. Counted
afterwards across users, campaigns, v2 clips, audit, activity and notifications: 0 `bl919%sbx-`
rows. The render server (PID 6140, read from the port) killed by PID. No `video.bin` anywhere
under the round's directories, no `v2frames-*` in the temp directory. `sweep-round-leftovers`
dry run then `--apply`: one three-day-old sandbox directory removed (2 MB), twelve kept by its
refusals. Worktree `C:\w\b919` removed, `git worktree list` shows main only, the path gone.

**The merge.** `pre-merge-BL-919` → `git merge --no-ff` → `21e7c660` → `post-merge-BL-919`,
`safe-push` verified. Branch and merge trees identical by OID (`2716394b…`), so the branch build
is the merge build; main re-installed (`npm ci`, `prisma generate`) and built afterwards. Money
files by blob OID against `pre-BL-919` and against `pre-merge-BL-919`: six of six SAME.
`checkpoint/BL-723` untouched. BACKLOG 228 → 229 entries.

---

## WHAT COULD NOT BE DETERMINED FROM THIS MACHINE, SAID PLAINLY

* **The job running in the deployed shape.** Nothing runs on deploy by design, this machine holds
  no production session (a minted cookie is refused there, BL-918), no CRON_SECRET and no Railway
  token, so no production extraction was triggered or observed. **Confirmed after the push:** the
  Linux ffmpeg and ffprobe binaries are present and run in the deployed image (the cron's
  12:50:32 UTC `V2_THUMB_SWEEP` row, PART 1). **Still unconfirmed:** a full extraction in the web
  service, the container's memory and disk, and the download speed from Railway to Google. **How
  it becomes confirmed:** the first `V2_FRAMES_JOB` row (after the owner approves a clip or
  presses the backfill button) carries `tooling`, `container.totalMemMB`, `container.tmpFreeMB`,
  `download.ms`, `download.bytes` and the three frames' stats.
* **The bucket write for frames.** `uploadImageToBucket` is the same function that stored 7,349
  covers and twenty previews; the frame path differs only in the key prefix. Not exercised here
  (no key) beyond the fake-key refusal, which is what proved the video is unlinked before it.
* **The exact fraction after the backfill.** 16 approved clips, all shared and all served as
  video bytes by Google today; the four unshared and one folder-link clips are not approved. The
  honest expectation is 16 of 16 with three frames each, and it is an expectation, not a count.

**Rollback:** `git reset --hard pre-merge-BL-919` (one step); the twelve columns stay, unused, and
their `DROP` is written in the migration file for the day it is wanted.
