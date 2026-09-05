# BL-839 — the bypass was working. It was reading the wrong route.

Round of 2026-09-05. Branch `checkpoint/BL-839`, merged to `main` at `7075e6a`. **Requires a Railway
REDEPLOY.** Handles redacted. Timestamps are the database's own `now()`.

## The answer, first

Your clipper's "Clip-submit rate-limit bypass" was **saved, read and honoured**. It just was not read
by the screen he was using.

There are two ways to submit. The single form posts to one place; the **"Add another clip"** form,
where anyone posting many clips ends up, posts to a **different** place. Your toggle only ever reached
the first. The second had its own limit of 12 an hour written into it and had never heard of the
toggle, so he was stopped after 12 presses and told "You're doing that too fast" by a message that
named no limit. You reasonably pulled the rate-limit lever, and it did not cover that route.

## It was NOT the 30-minute posting rule, and I checked that first

The two messages share nothing but the number thirty. The posting rule says *"This Instagram clip was
posted more than 30 minutes ago and cannot be submitted."* He saw *"You're doing that too fast."* The
file holding every submit rule contains "too fast", "please wait" and "slow down" **zero times**, and
"about 30 minutes" is what the speed limiter prints when its one-hour window is half spent. That rule
is untouched by this round.

## Every limit on the submit path

| limit | where | covered by your toggle? |
|---|---|---|
| 12 submissions an hour, single form | `api/clips/route.ts:1022` | **yes**, raised to 120 |
| **12 sends an hour, Add-another-clip form** | `api/clips/batch/route.ts:57` | **NO. This is the bug.** |
| daily clips per campaign, and the 30-minute posting window | `clipper-submit-core.ts:389`, `:458`, `:614` | no, and neither should be |
| campaign paused, ended, archived, over budget, account not approved, wrong platform, duplicate link | `clipper-submit-core.ts:350` to `:639` | no |

**Proof he was on the untouched route:** one internal record is written only by the single form, and
of his 50 clips that day **45 have no such record and 5 do**, same campaign, same day.

I built your current live code and made real requests. **14 checks, 0 failures:** the single form with
the toggle off refused the 13th; I then turned the toggle on through your own screen's endpoint and
**the very next submission went through** with the counter still at twelve, so the toggle works; and
with the toggle still on the **Add-another-clip form refused the 13th send with the identical
message**. Then the fixed code, **16 checks, 0 failures**: 120 sends allowed, refused at 121, naming
the limit. **No clip was created by any of it.**

## The second half of the problem, and the new wording

A submission that is **turned away still spends a slot**: the counter is touched before the clip is
looked at. So a clipper refused for a completely different reason can reach the speed limit having
submitted nothing, and then be told he is going too fast. That is how one problem disguises itself as
another. The new message says he "tried to send", never "sent".

> You have tried to send clips 120 times in the last hour. That is the limit for one hour. This is a
> speed limit, not your daily clip limit. Nothing is wrong with your clips, and none of them were sent
> just now. Wait about 25 minutes, then send them again.

The number is the one in force, never typed. The old shared sentence is **untouched**, because those
same words are used by logins and admin screens across the app.

## Your daily cap was the real first wall, and you had already fixed it

Zhus Meme allows 20 a day. He submitted **exactly 20** between 00:20 and 01:19, then nothing for
fourteen hours. That is the daily cap, not a speed limit. You granted him **150 a day** on two
campaigns at 13:47:57 and 13:48:04. **Today he has 100 left on Zhus Meme and 150 on Zhus Edit.** One test request as him on the fixed
build was not refused, and nothing was submitted for him: 50 clips before, 50 after. **You need to do
nothing else.** After the redeploy he can send 120 times an hour on either form, and his real ceiling
is your 150 a day.

## Nothing else changed

A clipper **without** the toggle is still refused on exactly the 13th send, proven on a second test
account, and his message says 12, not 120. **Three of 1,664** users hold the toggle. The daily cap,
the 30-minute window and the one-person window exemption are **byte-identical to before**, so they
cannot have moved. The 30-minute rule's own test returns **37 passed, 1 failed**, and that failure is
the test's live sample rather than the rule: it expects two real clips to be old and one was 18
minutes old, correctly treated as fresh. The rule still accepts 29, 30 and 34 minutes, refuses 36, and
refused a real 52-minute post. No payout touched, no clip's status or earnings changed, invariant **0
violations**, twelve protected files identical on both branches, no Apify actor ran.

**Every other toggle was checked for the same defect.** All nine on/off switches on a user are **stored, read by the server, and enforced**: act-as-clipper,
see-decided-clips, invited-clippers-only, trainer, PWA user, test user, deleted, bulk account-add
bypass (which has no second route to drift onto), and clip-submit bypass. **The batch route was the
only one of its kind, and it is fixed.**

## Named, not fixed, what I could not do, and how to undo it

**A refusal still writes no record.** There is a function for it and neither submit route calls it, so
a refused clipper left no trace in the log, the audit table or any column, which is why this had to be
reproduced from scratch. A log line is added now; a stored record is a separate change. **The main
submit button is white on the blue accent**, 3.40:1, which fails the contrast standard on both submit
screens: one colour token affecting every button in the app.

The **owner's toggle** is rendered at 320, 375, 414, 1280 and 1440 pixels, 55 checks, 0 failures, no
sideways scrolling, and now reads: *"Lets this person submit clips faster. It raises the hourly speed
limit from 12 to 120, on the one clip form and on the Add another clip form. It does not change their
daily clip limit for a campaign. They still have 30 minutes to paste a link after posting."*

The **clipper's refusal was not rendered in a browser**: reaching that screen needs a test clipper
joined to a live campaign and none is, so its wording above is quoted from the real response instead.

**To undo it:** `git revert -m 1 <merge>` or `git reset --hard pre-BL-839`. Reverting puts the hardcoded 12 back on
the second form and restores the old wording. There is nothing in the database to undo.
