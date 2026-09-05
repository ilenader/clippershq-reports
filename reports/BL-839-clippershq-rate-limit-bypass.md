# BL-839 — the bypass was working. It was reading the wrong route.

Round of 2026-09-05. Branch `checkpoint/BL-839`, merged to `main` at `7075e6a`.
**Requires a Railway REDEPLOY.** Handles redacted. Timestamps are the database's own `now()`, `::text`.

## The answer, first

Your clipper's "Clip-submit rate-limit bypass" was **saved, read and honoured**. It just was not read
by the screen he was using.

There are two ways to submit a clip. The single form posts to one place. The **"Add another clip"**
form, which is what anyone posting many clips ends up on, posts to a **different** place. Your toggle
only ever reached the first one. The second had its own limit of 12 an hour written into it, and it
had never heard of the toggle.

So he was stopped after 12 presses, told "You're doing that too fast", and the message named no
limit. You reasonably reached for the rate-limit lever, and it did not cover that route.

## It was NOT the 30-minute posting rule, and I checked that first

The two messages share nothing but the number thirty.

- The posting rule says: *"This Instagram clip was posted more than 30 minutes ago and cannot be
  submitted."*
- He saw: *"You're doing that too fast. Please wait about 30 minutes and try again."*

The file holding every submit rule contains the words "too fast", "please wait" and "slow down" **zero
times**. And "about 30 minutes" is exactly what the speed limiter prints when its one-hour window is
half spent. That rule is untouched by this round.

## Every limit on the submit path

| # | limit | where | what it says | covered by your toggle? |
|---|---|---|---|---|
| 1 | 12 submissions an hour, single form | `api/clips/route.ts:1022` | the speed message | **yes**, raised to 120 |
| 2 | **12 sends an hour, Add-another-clip form** | `api/clips/batch/route.ts:57` | the same message | **NO. This is the bug.** |
| 3 | daily clips per campaign | `clipper-submit-core.ts:389` | "You reached the maximum ... today" | no, and it should not be |
| 4 | 30-minute posting window | `clipper-submit-core.ts:458` and `:614` | "posted more than 30 minutes ago" | no, and it should not be |
| 5 | campaign paused, ended, archived, over budget | `clipper-submit-core.ts:368` to `:377` | names the campaign state | no |
| 6 | account not approved, wrong platform, duplicate link | `:350`, `:394`, `:639` | names the reason | no |

## Proof he was on the untouched route

An earlier round established that one internal record is written **only** by the single form. Of his
50 clips that day, **45 have no such record and 5 do**, on the same campaign on the same day. He was
using the form your toggle did not reach.

## Reproduced, not guessed

I built your current live code and made real requests. **14 checks, 0 failures:**

- Single form, toggle off: refused on the 13th, `429`, *"You're doing that too fast. Please wait
  about 1 hour and try again."*
- I turned the toggle on through your own screen's endpoint. **The very next submission went
  through**, with the counter still sitting at twelve. The toggle works.
- With the toggle still on, the **Add-another-clip form refused the 13th send with the identical
  message**.

Then the fixed code, **16 checks, 0 failures**: 120 sends allowed, refused at 121, with a message that
says which limit it is.

**No clip was created by any of this.** The probes are shaped so they die immediately after the
counter is touched and long before anything is written.

## The second half of the problem

A submission that is **turned away still spends a slot**. The counter is touched at the top, before
the clip is even looked at. So a clipper being refused for some completely different reason can reach
the speed limit having submitted nothing, and then be told he is going too fast. That is how one
problem disguises itself as another. The new message says he "tried to send" clips, never "sent".

## What the refusal says now

> You have tried to send clips 120 times in the last hour. That is the limit for one hour. This is a
> speed limit, not your daily clip limit. Nothing is wrong with your clips, and none of them were sent
> just now. Wait about 25 minutes, then send them again.

The number is the number actually in force, never a typed one. The old shared sentence is
**untouched**, because the same words are used by logins and admin screens across the app.

## Your daily cap was the real first wall, and you had already fixed it

Zhus Meme allows 20 clips a day. He submitted **exactly 20** between 00:20 and 01:19, then nothing for
fourteen hours. That is the daily cap, not a speed limit. You then granted him **150 a day** on two
campaigns at 13:47:57 and 13:48:04.

**Today he has 100 left on Zhus Meme and 150 on Zhus Edit.** One test request as him on the fixed
build was **not** refused by the speed limit. Nothing was submitted for him: his count was 50 before
and 50 after.

**You need to do nothing else.** After the redeploy he can send up to 120 times an hour on either
form, and his real ceiling is your 150 a day.

## Nothing else changed

- A clipper **without** your toggle is still refused on exactly the 13th send, proven on a second
  test account, and his message says 12, not 120.
- **Three of 1,664** users hold the toggle.
- The daily cap, the 30-minute window and the one-person posting-window exemption are **byte-identical
  to before** by file fingerprint, so they cannot have moved.
- The 30-minute rule's own test returns **37 passed, 1 failed**, and that one failure is the test's
  live sample, not the rule: it grabs two real clips and expects both to be old, and one was 18
  minutes old, which is correctly treated as fresh. The rule itself still accepts 29, 30 and 34
  minutes and refuses 36, and correctly refused a real 52-minute post.
- No payout touched, no clip's status or earnings changed by this round, earnings invariant **0
  violations**. Twelve protected files identical on both branches. No Apify actor ran.

## Every other toggle, checked for the same defect

All nine on/off switches on a user are **stored, read by the server, and enforced**: act-as-clipper,
see-decided-clips, invited-clippers-only, trainer, PWA user, test user, deleted, bulk account-add
bypass, and clip-submit bypass. The bulk account-add bypass has no second route to drift onto. **The
batch route was the only one of its kind, and it is fixed.**

## Named, not fixed

- **A refusal still writes no record.** There is a function for it and neither submit route calls it,
  so before this round a refused clipper left no trace in the log, the audit table or any column,
  which is why this had to be reproduced from scratch. A log line is added now. A stored record is a
  separate change.
- **The main submit button is white on the blue accent**, which measures 3.40:1 and fails the contrast
  standard, on both submit screens. It is one colour token affecting every button in the app.

## What I could not do

The **owner's toggle** is rendered at 320, 375, 414, 1280 and 1440 pixels, 55 checks, 0 failures, no
sideways scrolling, and it now reads: *"Lets this person submit clips faster. It raises the hourly
speed limit from 12 to 120, on the one clip form and on the Add another clip form. It does not change
their daily clip limit for a campaign. They still have 30 minutes to paste a link after posting."*

The **clipper's refusal message was not rendered in a browser**. Reaching that screen needs a test
clipper joined to a live campaign, and none is; joining one is a write this round declined to make.
Its exact wording above is quoted from the real response instead.

## To undo it

`git revert -m 1 <merge>` or `git reset --hard pre-BL-839`. Reverting puts the hardcoded 12 back on
the second form and restores the old wording. There is nothing in the database to undo.
