# BL-859 — the app bonus is for using the app

**Nothing was left behind. 7 rows created, 5 deleted and 2 taken by a cascade, 0 of 7 remaining, verified by a separate tool. No removal SQL is needed and none is owed.**

**Merged to main `3b3c48cc`. Branch `checkpoint/BL-859` at `a302fff1`. Requires a Railway REDEPLOY.**

---

## The headline, and it is not what you asked me to build

**The rule was already live, at two days, and it was stripping the bonus from nine of the thirty-seven clippers who are actively submitting clips.**

`gamification.ts` has been setting `isPWAUser = false` on anyone whose last app open was more than two days old since long before this round, with the same `<= 2` literal copied into five other files. **Nobody had written it down. No screen mentioned it. The sidebar was promising the 2 percent unconditionally.** So your policy was not built this round. It was found, measured, widened, made forward only, and given one home.

**And it was worse than that: losing it reached backwards.** The self-heal recomputed every approved unpaid clip without the bonus and wrote the lower figure, so a clipper who went quiet for two days had **already-earned money reduced**. That is the defect this round actually fixes.

---

## PART 0 — what the signal can carry

**`lastPWAOpenAt` is written by one place**, when the app shell mounts in a standalone context, at most once an hour. No service worker, no background sync, no push.

**So a daily rule is not safe, and I am saying so rather than shipping one.** Three reasons: the shell must remount, so a clipper who leaves the app backgrounded for days and switches back to it may write nothing; the hourly gate can lag a real open by an hour; and the measured tail is already past two days.

**BL-854 is not overruled, and its reasoning is why the number is seven.** It said the signal cannot tell an uninstall from a quiet week. That is right, and under the old framing (a reward for having the app installed) it is fatal. **Under your new framing it dissolves**, because the question is no longer whether the app is on the phone. It is whether the person opened it, and that is exactly what the column records.

**BL-854 had one factual error and it matters:** it called the flag permanent, having looked only at the unused door and missed the self-heal. **The loaded gun it declined to build was already firing.**

### The distribution, anchored before the outage

Of the **37** clippers holding the bonus who submitted a clip in the previous fortnight, average time since last app open **1.35 days**, worst case **11.92 days**:

| threshold | actively clipping people who lose it |
| --- | --- |
| 1 day | **11 of 37** |
| **2 days, the rule live today** | **9 of 37** |
| 3 days | 7 of 37 |
| **7 days, shipped** | **1 of 37** |
| 14 days | 0 of 37 |

Across all **397** holders: 35 within a day, 42 within two, 47 within three, **74 within seven**, 99 within fourteen, 166 within thirty.

---

## PART 1 — seven days, and why not fourteen

**Seven ships.** Fourteen strips nobody, so it enforces nothing, and you changed the rule because you wanted it to mean something. The one clipper seven strips **had not opened the app for 11.92 days**, nearly twice the window, which under your policy is the correct outcome rather than an error.

**The accessibility review argued for fourteen and I am recording the disagreement rather than hiding it.** Its case: at seven days I am writing a message to someone who "did nothing wrong", a clipper who posted six days ago. **I think that applies the old framing.** Posting a clip is not opening the app; a clipper can submit from a browser tab. Under "open the app to hold it", not opening it for over a week is precisely the condition not being met. **The cost of choosing fourteen over seven is about six cents a month, so if you disagree, the change is one constant and the reasoning is written beside it.**

**Restoration is immediate and proven.** One second after reopening, the bonus is active, and a second dashboard load does not undo it. The grant route refreshes both columns on the first standalone mount, so it is seconds, not an hour. The hour is a ceiling on how often the sync repeats, not a wait.

### What it saves

On clips approved in the 30 days before the outage:

| last app open | clippers | clips | base earned | 2% ceiling a month |
| --- | --- | --- | --- | --- |
| within 7 days | 74 | 2,596 | $4,764.58 | **$95.29** |
| 7 to 30 days | 92 | 33 | $10.99 | **$0.22** |
| over 30 days | 231 | 1 | $4.30 | **$0.09** |

**The whole policy saves about 31 cents a month.** The $95.29 belongs to the people who open the app and are clipping, which is the bonus doing its job. **The value here is that the rule becomes truthful and comprehensible, which is what you said you wanted. It is not money.**

**Your "$2 per $100 across 357 people" could not be reconciled**, exactly as BL-854 already reported. The real population is **397**.

---

## PART 2 — forward only, and this is the part that was broken

**The self-heal called `recalculateUnpaidEarnings`.** That recomputed every approved unpaid clip without the bonus and wrote the lower figure through `writeClipEarnings`. The never-below-stored guard in that writer covers only the budget-headroom clamp, so **nothing floored the drop**.

**That call is gone.** The flag flip stays, because that is what stops future clips carrying the bonus, which is the whole of your policy. What is removed is the reaching backwards.

**Proven on a real clip in the sandbox:**

| | before | after |
| --- | --- | --- |
| the flag | `true` | **`false`** |
| the clip's earnings | $102.00 | **$102.00** |
| its base | $100.00 | **$100.00** |
| its bonus amount | $2.00 | **$2.00** |
| its stamped bonus percent | 2% | **2%** |

**And coming back does not retroactively raise it either**, which would be the same defect mirrored.

**One honest limit on that proof:** the fixture clip carried no view snapshots, so the recompute that still runs from the streak path had no views to work from. The strongest claim I can make is the combination of the two facts: the clip did not move by one cent, and the PWA path no longer calls the recompute at all.

---

## PART 3 — the outage does not count against anyone

**A seven day window absorbs a one day outage for any active clipper**, but that is not all of the protection, and I measured rather than assumed: **nine flagged clippers currently sit between seven days and seven days plus the outage length**, so a plain cut would strip them for a day that was ours.

**So the outage is recorded as data.** `PLATFORM_OUTAGES` holds `2026-09-07T19:37Z` to `2026-09-08T19:48Z`, and the rule adds overlapping downtime back to each clipper's own grace window. Proven: a clipper **7.5 days idle across it keeps the bonus with exactly 24 hours forgiven**, and somebody 40 days idle is still paused, so it is not a loophole.

**Future outages are not handled automatically and cannot be today.** Nothing on the platform records its own downtime as data; the cron heartbeat gap is a gap rather than a record, and reading it would mean mistaking a paused cron for a dead database. **The list is hand-maintained. After the next outage, it must be added, or clippers who could not open the app during it may lose the bonus.**

### The seven, dated

There was **no audit trail of the old flip**, so they were identified from `users.updatedAt`. **14 clippers have been granted and then revoked. Five flipped after recovery on 2026-09-08 between 21:00 and 21:30 UTC**, as they came back and loaded their dashboards. **Two of those were only 3.20 and 3.23 days idle** and crossed two days only because we were down for 24 hours.

**Under seven days neither would have lost it.** Nothing in this round lowers anything of theirs, and they regain the bonus the moment they open the app. **This round adds the audit row that was missing, so the next time you ask this question the database can answer it.**

---

## PART 4 — telling them, and the day-one count

**Four states, not three.** Widening the window restores nobody by itself, because the old rule has already written the flag false. So a clipper stripped at day three now sits **inside** the new window, and telling them "it has been longer than 7 days" would be a false statement they could disprove from memory.

**No date is ever printed.** `lastPWAOpenAt` records a POST that survived four gates, any of which can drop a real open, so the stored moment is a **floor** on the last real open rather than the open itself. Printing it asserts what the data cannot support, and a clipper who opened the app on the 14th and is told "since the 12th" is right and the screen is wrong.

### The copy, quoted

**Holding it**, on `/progress`:
> **Your app bonus is on**
> The app adds an extra 2% to what your new clips earn.
> Open it from your home screen every 7 days and it stays on.

**Paused**, when the gap really is longer than the window:
> **Your app bonus is paused**
> The extra 2% stays on while you open the app every 7 days.
> It has been longer than 7 days, so new clips are earning without the bonus.
> Clips you already earned on keep their 2%.
> Open Clippers HQ from your home screen to turn it back on.

**Paused, but the last open is inside the window** (the cohort the two day rule stripped):
> **Your app bonus is paused**
> The extra 2% stays on while you open the app every 7 days.
> The bonus is off right now, so new clips are earning without it.
> Clips you already earned on keep their 2%.
> Open Clippers HQ from your home screen to turn it back on.

**Never had it:**
> **Get an extra 2% with the app**
> Add Clippers HQ to your home screen and new clips earn an extra 2%.
> Open it every 7 days and the bonus stays on.

**And the rule itself on `/help`**, under Bonuses, which is where the streak and level rules already live:
> **What is the app bonus?**
> Add Clippers HQ to your home screen and your new clips earn an extra 2%.
> Open the app at least once every 7 days and the bonus stays on.
> Go longer than 7 days and the bonus pauses. New clips then earn without it.
> Clips you already earned on keep their 2%. Nothing is taken back.
> Open the app again from your home screen and the bonus turns back on.

**Why it is worded that way.** The person is never the subject of a negative sentence: not "you have not opened it", which accuses, and not "your account has not opened it", which is worse because accounts do not open apps. **The upkeep rule is stated to people who still hold it**, so a holder can never be surprised. The survival promise is nine words, scoped to this rule, because BL-854's absolute version contradicts what the platform tells clippers elsewhere about unavailable clips and fake views. Measured at **Flesch-Kincaid 4.8 or below** against a ceiling of 6.0, longest sentence 15 words.

**The sidebar's `+2%` badge keeps its pixels and its accessible name now carries the condition**: *", +2% earnings bonus while you use the app"*. And the POST behind that badge gained the header it was missing, so **the button carrying the promise now actually grants the bonus when pressed**, which BL-854 reported and left.

### The day-one count is zero, and that is a finding

**No clipper's rate changes at deploy.** Widening a threshold restores nobody automatically. **The nine the old rule wrongly stripped stay stripped until they next open the app.**

**The SQL to restore them is yours to run, not mine.** It writes to real clippers' money-adjacent flags, so it is printed rather than executed:

```sql
-- Restores the app bonus to clippers whose last app open is inside the NEW
-- seven day window but whose flag the OLD two day rule already cleared.
-- Forward only: it sets the flag and recomputes nothing.
UPDATE users
   SET "isPWAUser" = true
 WHERE role = 'CLIPPER'
   AND "isPWAUser" = false
   AND "pwaGrantedAt" IS NOT NULL
   AND "lastPWAOpenAt" > now() - interval '7 days';
```

**No announcement is sent, on two grounds.** Without the backfill it would have zero recipients. And `STREAK_LOST` is declared, routed, iconed and tiered in this codebase **while never being fired anywhere**, so the streak bonus, whose loss is five times larger, is silent. Making a 2 percent loss the platform's first bonus-loss notification would be inconsistent and disproportionate. **If you want bonus-loss notifications, that is one decision covering both bonuses and it is not this round.**

---

## PART 5 — proven in the sandbox

**36 checks, 36 passed, 0 failed.** The rule is a pure function, so the threshold, the immediate return and the outage allowance are proven exactly with no fixture. Forward-only is proven on real rows against the shipped `getGamificationState`, not a copy of its logic.

**Nothing real was touched.** 7 rows created, **5 deleted and 2 taken by a cascade, 0 of 7 remaining.**

**50 teardown checks, 47 passed and 3 failed, and all three failures are one fact the tool itself attributes: one real person signed up mid-round.** Users went 1,683 to 1,684 and the user fingerprint moved with the id set. **The payout fingerprint is byte-identical, the invariant is 0 both sides, and 0 payouts were created.** Also named rather than smoothed: 3 clips from 2 real clippers, 75 cron view snapshots, approved earnings up $2.65.

**The bonus arithmetic still holds:** 100,000 views at $1.00 CPM is $100.00 without the bonus and $102.00 with it, and the difference is the bonus and nothing else.

---

## PART 6 — render and merge

**30 shots, 290 assertions, 0 failures** at 320, 375, 414, 1280 and 1440, with `window.innerWidth` printed beside every shot: **0 at the wrong width, 0 with horizontal overflow.** All three states on `/progress` plus the `/help` entry, as a sandbox clipper on a real minted session against a production build with the dev bypass off. The three states were reached by flipping the fixture's own two columns, because **a real clipper is in exactly one state and changing a real person's bonus flag to take a screenshot would be indefensible.**

**Nothing I could not render.** Every changed clipper-facing surface was photographed at every width.

**The merge.** Main was at `fd960fec` and had not moved, so there were no conflicts and no unions were needed. **The merge tree OID equals the branch tree OID exactly at `212cde19`, so the branch's green build is the merge's build.** **BACKLOG 185 to 186**, counted with `grep -c`. `checkpoint/BL-723` confirmed **not** an ancestor. Worktree `C:/w859` removed and verified gone. **No live claim existed:** `git worktree list` showed only the shared tree when this round started.

### The build caught what the typechecker could not

**`npx tsc --noEmit` returned exit 0 with zero errors on a tree that `next build` then refused.** The rule module reached a client bundle and `logAudit` dragged `node:module` in with it. Split along the server boundary into `pwa-bonus-window.ts` and `pwa-bonus-audit.ts`. **Recorded rather than quietly retried, and exactly why the house rule says never to trust `tsc` alone.**

| gate | result |
| --- | --- |
| clean tsc baseline, untouched worktree, before any edit | exit 0, 0 errors |
| `npm run build`, first attempt | **exit 1**, the client-bundle failure above |
| `npm run build` pre-commit and post-commit | **exit 0** both |
| `npx tsc --noEmit` final | exit 0, 0 errors |
| hooks gate | **0 errors, 10 warnings** against a ceiling of 11, zero added |
| eslint | v9.39.4 confirmed present, so the gate is a real check |

---

## Reported, not changed

- **`tracking.ts:2155` and `:2162` still read the raw flag with no freshness check.** That file is one of the six protected money files, and the error direction here is the generous one, which BL-854 argued is the preferable error. Left deliberately.
- **`pwa-status/route.ts` still calls `recalculateUnpaidEarnings` on GRANT**, so a return still moves already-earned money **upward**. That is the mirror of the defect fixed here and it deserves its own decision.
- **The notification bell button has no accessible name**, and a type missing from `notifHref` renders as a non-focusable div. Both pre-existing, and only reachable if a notification ships, which it does not.

## Safety

The 6 money files plus `tracking.ts`, `campaign-era.ts`, `earnings-never-decrease.ts`, `payout-calc.ts`, `apify.ts` and `prisma/schema.prisma` are **byte-identical by blob OID on both refs**. No schema change, no `prisma migrate`, no index, **no Apify actor run**, the **11 BL-678 guards intact**, **0 Supabase pool errors**, every timestamp cast `::text` against the database's own `now()`. No handle, wallet address or key appears anywhere above. **BL-627's no-overpayment and BL-696's no-double-pay are untouched: this round writes no earnings, no balance and no payout row.**

**Rollback:** `git revert -m 1 3b3c48cc`. Nothing in the database needs undoing.
