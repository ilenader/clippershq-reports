# BL-908 — the Drive blocker, the queue you use, and real charts

**The blocker was real and it was sitting in your queue while this ran.** Your first two real
submissions, measured before a line was written: the **older one is a Drive folder**
(`drive.google.com/drive/folders/...`, `driveFileId` NULL), the newer is a proper file link. Your
second request, "do not put twenty videos in one drive", had already happened before you asked.

**Merged to main** (`c8bc2286`), tree byte-identical to the branch that was built and proved. No
migration, no schema change, no data change. Your two pending clips were never touched.

## 1. The permission: what can be checked, and what cannot

**It cannot be checked, and this round says so rather than shipping a validation that passes
everything.** Nothing in the codebase calls the Drive API. An anonymous fetch does not answer it
either, and that was considered rather than skipped:

- Google serves **200 with a sign-in interstitial** for a private file, so the status code reads
  "fine" for exactly the case being hunted. Parsing that page is guessing at undocumented HTML.
- A server IP draws interstitials and rate limits your browser never sees, so it would refuse good
  links for reasons that have nothing to do with the maker.
- Anything that cannot reliably refuse must not refuse, and one that never refuses is theatre.

So instead, three things that actually help:

**The instruction moved, which was the real defect.** Both rules already existed on the submit
form. Both sat inside a collapsed block, **closed by default, below the field, in the quietest text
style on the page**. They said the right thing and nobody read them. They are now above the field,
open and numbered:

> **Two things to get right, or it comes back**
> 1. One Drive link, one video, one clip. Do not put twenty videos in one Drive folder and send the
>    folder. You do not need a folder at all, just the video and its link.
> 2. Set the link so anyone can open it. In Drive press Share, change Restricted to Anyone with the
>    link, and leave it on Viewer.

**And a required tick:** "I set this link to Anyone with the link, Viewer, and it opens one video."
**That tick is not a check and nothing pretends it is.** The platform cannot see the file; a
deliberate confirmation is the strongest honest thing available.

**You get a one-press way out.** Every pending row now carries **"Cannot open it"**, which opens the
rejection with this already written, so you read what the maker will receive and confirm:

> "I cannot open this link. In Drive press Share, change Restricted to Anyone with the link, leave
> it on Viewer, then send it again."

**The two already in your queue:** nothing automatic, deliberately. They are real rows and no round
deletes somebody's work. The folder one now costs you seconds.

## 2. One link, one video, one clip

**A folder link IS detectable, and it is now refused.** `extractDriveFileId` has always returned
null for `/drive/folders/`, and the platform has always stored that null without once reading it
back. One definition, `classifyDriveLink`, is called by **both the form and the server**, so a link
refused in the browser is refused by the server in the same words, and a link arriving without the
form is refused all the same. The refusal names the fix rather than just saying no.

The rule is also in the maker's steps before he starts, which went from four to five because "put
it in Drive and share the link" was hiding the two separate things that each went wrong.

## 3. Full width, and charts copied from analytics

**Width, measured on the same page with one variable changed** (the removed padding put back in the
live DOM, so this is a measurement and not arithmetic):

| viewport | before | after | gain |
| --- | --- | --- | --- |
| 1280 | 928px, 72.5% | 992px, **77.5%** | +64px |
| 1440 | 1088px, 75.6% | 1152px, **80.0%** | +64px |

The marketplace wrapper paid `lg:px-8` on top of the shell's own `lg:p-6`, so a desktop page carried
112px of inset nobody had chosen. **A latent one found on the way:** the full-width list tests
`"/marketplace"` while BL-903 moved the path to `/market`, so `"/market/admin"` has never matched
and every marketplace screen has been inside the 1280px wrapper since. It changed **no measured
number here**, because the sidebar already makes the column narrower than that cap, and it would
have bitten on a wider monitor. Fixed, and named as what it is rather than claimed as the win.

**The charts are the analytics component.** `AreaGradientChart` now draws the ink, the same one
`admin/analytics` and `command-center` render. **It is wrapped rather than swapped in, and that
matters:** measured first, `area-gradient-chart`, `simple-chart` and `donut-chart` contain **zero**
occurrences of aria, role, scope or sr-only between them. Dropping one in bare would have given you
the picture and taken the summary sentence and the numbers table from anyone who cannot see it. Each
chart answers a stated question: are makers still arriving, are you keeping up, are approved clips
being posted, what did it cost.

**Money tables stayed tables.** A card carries the across reconciliation and cannot carry the down
one, and reading down a column is the act of checking a sum.

**The explainer is gone for you only**, decided by role, the same signal the nav on the next line
already uses. Everybody else sees exactly what they saw.

## 4. The review flow

**One press back.** BL-906 put a link on the overview bringing you here and built no way back. A
link that only goes one way is half a link.

**Newest first, and the fair order kept.** Pending was oldest-first, defended in three comments as
the longest waiter first. You asked for newest, so newest is the default and **"Longest wait first"**
sits beside it as one press. **It cost no index:** the btree scans backwards as happily as forwards.

**The screen had started lying and the accessibility review caught it:** it still said "Longest wait
first." while the server was sending newest first. It is computed from the live order now.

**The real timestamp is visible.** You saw only "37 minutes ago"; the absolute time existed but was
hidden from sighted readers. It is on screen now, and marked so a screen reader does not read the
same timestamp twice on every row.

**The rejection reason is still required, verified by request** through the live route, not by
reading the file: empty is refused, 1,001 characters is refused, and the prepared sentence the new
button writes is accepted whole.

## 5. Resend, named so it is not lost

**`digitalzentro` is the only address that works.** Owner alerts to your other two addresses return
`403 validation_error` on every attempt, because the Resend account has **no verified domain**.

**This is your manual step in Resend and no round can do it.** Verify a domain there, then alerts
reach all three.

**The consequence:** the maker-submitted alert is your only early warning that a queue is filling,
and it dies silently to two of your three inboxes. It worked for the real submission at 20:52 — one
notification per owner was written — but only one of the three emails was delivered.

## 6. Proved

23 of 23 checks, exit 0, every setup a check, **every failure path its own user** and every refusal
asserted NOT 429. Invariants across the **full population**: 0 out of balance, 0 negative, 0 double
paid, 0 campaigns over budget counting both v2 aggregates, paid-is-final moved by exactly zero. Both
reconciliation forms unchanged. **18 of 18 guards**, build exit 0, 0 TypeScript errors, hooks 0
errors and 10 warnings. **Renders 10 of 10** at 320, 375, 414, 1280 and 1440 across the queue and
the overview, with `innerWidth` and the URL read back, the state asserted in words, and the pan
measured at **0px everywhere**. Fifteen protected money files byte-identical by blob OID. Teardown
by recorded id only, every count and fingerprint identical.

**The accessibility review found a critical defect in my own work and it is fixed.** recharts 3
defaults its accessibility layer to on, which stamps `tabindex=0` on the chart, so four charts meant
**four tab stops inside a hidden wrapper that announce nothing**. Fixed with a passthrough, so the
nine other places using that chart are byte-identical, and verified in a real browser at zero.

**Reported and not fixed, because it is the app shell rather than this round:** the closed mobile
drawer is hidden from screen readers while holding 34 focusable links, on every page of the
platform.

**One thing I could not render:** the dashboard's empty state. The marketplace is no longer empty,
so there is no empty to photograph. That premise expired between rounds.

## And the blocker five rounds ended on is retired

**BL-905's standing blocker is closed, and you closed it.** `ANGIE BROWN THE REAL ME` is
`MARKETPLACE_ONLY` now, not NORMAL, and two real makers have submitted to it. The one thing no round
could do, you did.
