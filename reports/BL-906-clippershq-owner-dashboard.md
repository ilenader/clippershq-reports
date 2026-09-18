# BL-906 — the owner's dashboard, and the notification that makes it matter

**Four rounds said the dashboard was not built. It was half built, and you were looking at the
wrong page.** BL-897 shipped a real owner overview at `/market/admin/overview` carrying PER CLIP
and PER CAMPAIGN. "Waiting for you" and "already decided" are not on it: they are the two tab
labels of BL-896's **approval queue** (`admin-client.tsx:88-89`), a different screen. So this
round added the three panels that genuinely did not exist, **to that same page** rather than to a
second one you would also have to find.

**Merged to main** (`a932b073`), whose tree is byte-identical to the branch that was built and
proved. No migration, no schema change, no data change.

## What you can now see, and what you can now do

**PER PERSON** what each person made and posted, their maker and poster totals in gross and cash,
their side **on each campaign**, and their standing. **WHAT YOU EARNED** your ordinary cut and the
platform ten percent per campaign, side by side, because under ADDS they stand beside each other
rather than replacing one another. **OVER THE LAST 30 DAYS** four charts, each stating the
question it answers: are makers still arriving, are you keeping up, are approved clips actually
being posted, what did it cost.

**Five of the seven controls already existed and had no screen anywhere in the codebase.** Not a
stub, not behind a flag: no `.tsx` file referenced them.

| control | before | now |
| --- | --- | --- |
| approve / reject a clip | BL-896's queue | **linked**, not rebuilt |
| strike a person | route only, no screen | wired to that route |
| ban / unban | route only, no screen | wired to that route |
| decide a side request | route only, no screen | wired to that route |
| convert a clip | route only, no screen | **linked**, because it needs a clip and an editor chosen together |

**No money is computed on this page and there is no thirteenth derivation.** Every figure is
summed from a row a named writer wrote or returned by a named function: `loadV2EditorEarningsByUser`,
`v2PosterPayableClipWhere` over `Clip.earnings`, `MarketplaceV2PlatformEarning`, `AgencyEarning`,
`projectPayoutCash`. The screen shows BL-902's **real** figures: on Zhus Edit the campaign spends
**$163.94** per $100 of gross and you keep **$82.04**, because your cut is views over 1,000 times
your own CPM and not a share of the gross. It is the only place all four legs appear together,
which is why it is OWNER only behind the 404-before-403 gate.

## The notification

`submitV2Clip` wrote a PENDING row and returned. It now tells you, through `createNotification`,
which is the bell, the Ably push and the owner email leg. Not a second system, and not subject to
marketing consent. It deep-links to `/market/admin`, the screen you act on.

**It cannot break a submission, and that was proved by breaking it mid-request.** With the
notifications table renamed out from under the running process, the submission still returned 201
and still created the clip; the table was restored by a retrying `finally` and then asserted
present. **One correction to the inherited account:** BL-870 renamed `activity_events`, not the
notification table. The method transfers, but this is the first time it has been run there.

**Thirty makers do not produce thirty emails.** The message is about the **queue** and carries the
pending count, so a burst produces one message that says the number. A 15-minute dedup sits under
it. That half is **new, not borrowed**: every existing dedup bounds a repeated *same* event, none
bounds many *distinct* subjects. Proved twice on independent runs, three submissions and one
message each time.

**The pending-clip alert needs no external step, and is specced rather than built.** The watchdog
already fires every 30 minutes in production, measured at 96 runs in 48 hours. Adding an age check
to it is pure code. Left unbuilt deliberately: it touches cron logic mid-launch, and the submit
notification already covers the arrival case.

## The three cheap fixes

**`setPosterState` now filters test campaigns**, closing the single gap in BL-905's whole sweep. It
is a **gap, not a leak**: it writes one state row, returns no campaign data and moves no money, so
nobody could have learned anything through it.

**The poster's empty state** said "New clips show up here as soon as the owner approves them",
naming approval as the only missing step when today no maker can make one either. It now reads
"Two things happen before a clip lands here. A maker sends one in, then the owner approves it."

**The hooks gate went from 11 of 11 to 10 of 11 by fixing, not by raising the cap.** `announce` is
`useCallback(...,[])`, so adding it changes nothing at runtime. **The other ten are not fixed and
that is a decision:** none is a stable callback, they sit on live payout, campaign, team and user
surfaces, and refactoring them mid-launch for a lint cap is the wrong risk. Headroom is 1. Thin,
and honest. Worth its own round.

## What caught me

**Two guards failed my build and both were right.** BL-882's S4 refused my `agencyEarning` scope
for naming `marketplaceV2PostId` directly; the scope now comes from `marketplace_v2_posts`, which
is the authority on which clips are v2 posts. BL-893's R1 refused me for reading
`marketplaceV2Role`, a permission-shaped column I had selected and never rendered. Neither was
fixed by an allow-list edit.

**The sandbox caught a control that would have failed every press.** `issueV2Strike` refuses a
strike with no evidence clips; my first dashboard posted an empty array. The walk found it because
it called the real function instead of looking at the button.

**The accessibility review found nine major defects in my own work, all fixed.** A blocked
destructive button returned silently. The shared busy guard was a silent no-op. Approving a side
request dropped focus to the body. The success message was thrown away, because closing the modal
restores focus in the same tick and focus preempts speech. `--mp-danger` is declared only inside
`.dark` and would have rendered **transparent** in the light theme, and the blocked state dimmed to
2.08:1, which is the state the modal opens in. `loadDash` swallowed every failure and left stale
rows on screen. `hasMorePeople` was sent and never rendered, so the rest of the people were
unreachable. Ban and Unban shared one DOM node.

## Proved

29 of 29 checks, exit 0, every setup a check. **Full population, not the sandbox:** 0 out of
balance, 0 negative, 0 double paid on either leg, 0 campaigns over budget counting both v2
aggregates, paid-is-final moved by exactly zero. Both reconciliation forms run before and after,
unchanged. All 18 prebuild guards pass; build exit 0, 0 TypeScript errors. **Renders 10 of 10**
across 320, 375, 414, 1280 and 1440, **empty and populated**, with `innerWidth` and the URL read
back, state asserted in words and the pan measured at **0px everywhere**. Fourteen protected money
files byte-identical by blob OID. Teardown by recorded id only: every count and fingerprint
identical, zero residue.

## Disclosed, and one finding worth a round

**I disturbed you three times.** Three real emails reached your own address during the proof runs,
because the fan-out finds every OWNER row and not only the sandbox one. The rows were removed; the
emails cannot be.

**The Resend account has no verified domain.** Owner alerts to both non-`digitalzentro` owner
addresses returned `403 validation_error` on every attempt. The bell always works; the email leg
does not, for them. That is not caused by this round and it is worth fixing before you rely on
being emailed.

**Still not built:** the unseen-clip badge.

**The one thing no round can do** is opt a real campaign into the marketplace. `ANGIE BROWN THE
REAL ME` at $3,000 and ACTIVE is still `campaignType NORMAL`.
