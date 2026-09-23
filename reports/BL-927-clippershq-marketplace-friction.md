# BL-927: where a clipper or a poster gets stuck between arriving and being paid

**AUDIT ONLY. NOTHING CHANGED.** No code, schema, data, config or flag. Clock: DB `now()` **2026-09-23 20:20 to 20:28 UTC**. Branch `checkpoint/BL-927` carries this file only. The worktree `C:\w\b927` was removed after publishing (verified at the end).

**Model split, stated honestly.** Opus ran every query, read every raw result and wrote this report. **0 subagents**; no cheaper model ran anything. The brief allowed a cheaper model for queries and counts. I didn't use one because the population kept needing judgment mid-count:
* two sandbox ids hiding among "real" refusals;
* the owner's own accounts stocking the catalogue;
* a gate whose refusals the recorder cannot see.

A retrieval summary would have carried those errors forward.

**Caps and constraints:**
* **Database:** ONE connection at a time: about 40 short read-only `run-select.js` queries, run sequentially.
* **Other network calls:** one `GET /api/version` to our own site. No vendor call, no Apify actor.
* **Rows touched:** none.

**How test traffic was told from real, by evidence, not assumption.** 59 accounts have ever touched the marketplace. Excluded, with the rule that excluded each:
1. **4 accounts whose role is not CLIPPER** (3 OWNER, 1 REVIEWER), plus **1 test clipper** (`isTestUser`).
2. **The owner's own clipper account.** It is matched in SQL by the exact fingerprint BL-907 recorded (203 clips, 13 payouts totalling $991.11), and the rule matches **exactly 1** account.
3. **BL-926's named test account** (handle ending "test", 0 clips, a side chosen): the rule matches **exactly 1**.
4. **BL-907's scripted rows** on its real control clipper (392 clips): 4 refusal rows at 20:50 on the 18th, 30 ms apart twice, as BL-910 established.
5. **Two sandbox ids** (`bl898sbx…`, `bl908sbx…`) whose users no longer exist. They carry the pre-launch `mkt2.post` and `mkt2.choose-role` refusals and the owner-only `mkt2.decision` refusals, exactly the rows BL-910 attributed to prior rounds.
6. **42 signed-out rows** (401 containment probes, 17th to 21st).

**52 real people remain.** No id was hardcoded: every exclusion is a rule whose match count is printed (`q-exclusions.sql`).

---

## THE HEADLINE

**Nobody in the marketplace can be paid, and at today's rates nobody will be for about two months at the earliest.**
* ANGIE BROWN THE REAL ME, the only real marketplace campaign, sets a **payout minimum of $25.00** (`campaigns.minPayoutAmountDecimal`); the platform default is $10.00.
* Eight real people have earned anything. The best has **$1.66** (a poster); the best maker has **$1.03**.
* At each person's own measured rate, the fastest reaches $25 in **59 days**, the rest in **100 to 390 days**, and five posters holding $0.00 never do.
* **0 marketplace payouts have ever been requested and $0.00 has ever been paid.** The drop from "earned something" to "requested a payout" is **100 percent on both sides**, and it is arithmetic, not a bug.

**And the people who ARE owed money are waiting too.** Ten real clippers hold **REQUESTED payouts past their deadline**: **$1,797.71 in total**, the oldest **23.0 days late**. Five of those ten are marketplace posters, including the single most active one, who is owed **$908.70**. These payouts generated **219 of the 249 owner alert emails in the last 48 hours (88 percent)**, which buries every other alert.

---

## PART 1: THE WHOLE FUNNEL, EVERY STAGE, SPLIT BY SIDE

52 real people, all-time since the first real arrival on 2026-09-18. "Seen in 48 h" is anyone with any marketplace row, post, submission or Drive tap since 2026-09-21 20:20 UTC. Those people have not dropped out; they are still going.

**Everyone**

| stage | people | seen in 48 h | drop |
|---|---|---|---|
| arrived | 52 | 24 | |
| chose a side | 35 (24 poster, 11 maker) | 18 | **17 (33 percent)** |
| chose nothing | 17 | 6 still around, **11 gone** | |

**Poster side (24 people)**

| stage | people | seen in 48 h | drop |
|---|---|---|---|
| chose poster | 24 | 15 | |
| opened the campaign list | 24 | 15 | 0 |
| opened a campaign's clips | 20 | 13 | 4 (17 percent) |
| opened a clip | 17 | 11 | 3 (15 percent) |
| opened the Drive link (server in-progress row) | 17 | 11 | 0 |
| **came back and tried to post** | **9** | 6 | **8 (47 percent)** |
| submitted a post link | 9 | 6 | 0 |
| has a post the owner approved | 9 | 6 | 0 |
| earned anything above $0.00 | 4 | 3 | **5 (56 percent)** |
| requested a payout | 0 | 0 | **4 (100 percent)** |
| was paid | 0 | 0 | |

**Maker side (11 people)**

| stage | people | seen in 48 h | drop |
|---|---|---|---|
| chose maker | 11 | 3 | |
| submitted a clip | 6 | 3 | **5 (45 percent), and none of the 5 has been seen in 48 h: stopped** |
| had a clip approved | 4 | 3 | 2 |
| earned anything above $0.00 | 4 | 3 | 0 |
| requested a payout | 0 | 0 | **4 (100 percent)** |
| was paid | 0 | 0 | |

**The biggest drops, named:**
1. **Earned to requested: 100 percent on both sides**, explained in full by the $25 minimum (headline).
2. **In people: 17 of 52 arrived and chose nothing (33 percent)**, of whom 11 are gone.
3. **After committing: 8 of 17 posters opened the Drive link and never posted (47 percent), and not one of the 8 hit a single refusal.** The recorder has nothing on them. What is known:
   * **One (`cmsotu9m`) holds no clip account of any kind**, so he could never have posted. The page says so in words and sends no request, so nothing is recorded.
   * **Four of the 24 posters in total hold no clip account at all** (0 pending either), and none has posted.
   * Of the other seven, two were seen today and may still post. **The data cannot say why the rest stopped, and I will not invent a reason.**

---

## PART 2: EVERY REFUSAL, RANKED BY DISTINCT PEOPLE

**The recorder is writing.**
* 964 marketplace rows in `activity_events`; **the most recent at 2026-09-23 19:48:53.803, 32 minutes before `now()`**.
* Real arrivals and posts today confirm it is live.

**Real refusals in the marketplace's entire life: 3 events from 2 people.**

| sentence the person saw (verbatim) | surface | people | events | first and last (UTC) | reading |
|---|---|---|---|---|---|
| "You have already submitted this exact post." | `mkt2.post` 409 | 1 | 1 | 2026-09-22 04:58:47 | **working as intended.** The poster posted a clip at 04:57:08, opened the next clip at 04:57:18 and 99 s later pasted the same link, one post for two clips |
| "You already sent this exact file. Pick a different video, or send a link to the corrected file." | `mkt2.submit` 409 | 1 | 1 | 2026-09-21 16:18:28 | **working as intended, but look at why.** A maker resent a file while BOTH his clips were still pending. They were approved **53 hours** after he sent them (2026-09-22 17:58). A resend is the shape of someone who did not know his first one arrived |
| "Invalid request." | `mkt2.state` 400 | 1 | 1 | 2026-09-20 15:29:37 | a request body that did not parse (`state/route.ts`, the `req.json()` catch). One event, no pattern |

**Honest about small numbers.** BL-870's floor is five people. **Nothing reaches two.** There is no trend here, and I am not making one.

**The new rules gate (BL-923, live since about 09:10 UTC today, `2f87742c` in the tick log):**
* **6 real people have read a campaign's rules**: 5 in the marketplace, 1 on an ordinary campaign page. A seventh row belongs to the owner's own clipper account.
* **0 refusals recorded with `CAMPAIGN_RULES_NOT_SEEN`. That zero does NOT mean nobody was stopped.** BL-923's client stops an unread poster before any request is sent ("0 post requests sent", its own proof). So a poster the gate held is invisible to the recorder.
* **Measured directly instead:** every real poster who opened a clip since the gate went live **read the rules**. The three who posted did so **6 seconds, 8 seconds and 17 minutes** after reading. **Nobody opened a clip and left unread.**
* The only sign of friction: one poster opened a clip at 13:52:12 and read the rules at 14:05:06. A 13-minute gap cannot be told apart from browsing.
* **Refused and never came back: 0 people, as far as the data can see.**

---

## PART 3: THE THREE THINGS NOBODY HAD SEEN WORK

**1. A maker reading a rejection and resubmitting: YES, it has happened, three times out of three.**

| maker | rejected (reason, verbatim) | waited | resubmitted | outcome |
|---|---|---|---|---|
| `cmu5sqhc` | "There is no video here." | 11.9 h | 7 h later | went on to **16 approved clips**, the platform's main supplier |
| `cmu7zdkg` | "its needs to be an edit" | 2.1 h | 4 h later | one approved; then rejected twice more ("Does not match the campaign", "no story or meaning"); **not seen since 2026-09-20** |
| `cmt08bz7` | "this is not the right part of the song. Go read the requirements to fi…" | 11.7 h | about 21 h later | rejected again: **"You submitted requierments"**. He sent the REQUIREMENTS link instead of a video. **Not seen since 2026-09-20.** 0 approved |

So rejection-and-resubmit works for someone who understands the job. The one maker told to "go read the requirements" appears to have submitted the requirements themselves. **One person, so no pattern**, but it is the clearest sign of confusion in the data.

**2. A poster returning from Drive on a DIFFERENT device: CANNOT BE MEASURED.**
* No device or user agent is recorded anywhere.
* What is measured: 43 of 47 real posts had a Drive tap first. The median tap-to-post time is **343 s**; 11 took over 10 minutes, and **one took 33,790 s (9.4 hours)**. That one is the only post where the server-side place was demonstrably kept across a long gap, whatever the device.
* 4 posts had no Drive tap at all.

**3. A real person hitting the 30-minute window: NO RECORDED CASE, AND WHETHER THE CHECK EVER RAN IS NOT KNOWABLE FROM THE DATABASE.**
* No refusal carrying the window's sentence exists.
* **None of the 47 real posts stores a platform publish time** (`Clip.postedAt` is null on all 47).
* The check logs its verdict, including every fail-open, **to the Railway console only** (`clip-freshness.ts`, the `[FRESHNESS-MP5]` lines).
* Instagram, the campaign's only platform, is checked through HikerAPI. The cron service's credential census does not list it, and the web service's own variables cannot be read from here.
* **So the largest untested assumption is still untested, and now it is also unobservable.** Reading the Railway log for `[FRESHNESS-MP5]` would settle it.

---

## PART 4: SUPPLY, MEASURED

**Every maker submission (33 in total), by maker class:**
* **Real makers: 27 submissions from 6 people**, 2026-09-18 20:37 to **2026-09-20 12:43:44**. The **last real submission was 79.7 hours ago**.
* **Owner-controlled accounts: 6 submissions today**: 1 from the owner's clipper account (12:03) and 5 from an OWNER-role account (13:36 to 13:42), each approved within about 3.5 minutes. **The owner is stocking the catalogue himself.**
* **Daily flow (UTC):**

| day | submitted | approved | posts | people posting |
|---|---|---|---|---|
| 09-18 | 14 | 0 | 0 | 0 |
| 09-19 | 7 | 12 | 14 | 6 |
| 09-20 | 6 | 4 | 9 | 6 |
| 09-21 | 0 | 2 | 8 | 4 |
| 09-22 | 0 | 2 | 7 | 3 |
| 09-23 | 6 (all owner-controlled) | 6 | 9 | 4 |

* **One real maker supplies 16 of the 20 real approved clips (80 percent).**

**The catalogue is NOT running dry.**
* 26 approved clips are visible to posters.
* The poster nearest the bottom still has **15** he has neither posted nor skipped.
* The heaviest poster has posted 10 in about five days, so his 16 remaining last **about 8 days** at that pace; everyone else has 17 to 26.
* Each clip can be posted by every poster, so posting does not consume a clip for anyone else.
* **On today's numbers the first poster runs out in roughly a week to ten days, and only if no new clip is approved.** The owner's six today already bought that time.

**What would report it:** nothing does today. The owner's funnel screen shows counts in a window, never "days since the last real maker submission" or "clips left for the busiest poster". Both are one query each over tables that already exist. **Code, small, no owner action.**

---

## PART 5: THE QUEUE AND THE OWNER'S OWN LATENCY

**Pending maker submissions: 1.**
* `cmu8ieea`, from a real maker, sent **2026-09-19 14:55:14**, waiting **101.5 hours**.
* **It can never be approved as it stands.** Google answered its preview request with a sign-in page ("usually means the Drive file is not shared"), so the owner cannot open it.
* **12 later clips were decided while it waited.**
* The maker has not been seen since 2026-09-21 and does not know his sharing setting is the problem.
* Nobody else is blocked behind it: posters have 26 approved clips.

**Pending POST links: 7** (the owner reviews posters' links too).

| waiting | 28.4 h | 27.5 h | 26.6 h | 19.8 h | 6.5 h | 4.1 h | 1.8 h |
|---|---|---|---|---|---|---|---|

* **No alert of any kind exists for a pending post link.** "Marketplace clips are waiting" covers maker clips only.
* The reviews measured here (the 8 rejected posts and the 4 approved-but-unavailable ones) took **2.7 to 25.2 hours**.

**Did the maker-submitted notification fire and reach him?**
* **It fires:** 24 `MKT_V2_CLIP_SUBMITTED` bells to 3 owner accounts since 2026-09-19, including one at 14:55:14.463 for the clip above, the same second it arrived.
* **None of the 24 bells has ever been read.**
* **Email:** 6 "Marketplace clips are waiting" emails in 48 hours, all accepted. **0 of 316 email rows have ever been refused.**

**The reminder flood, last 48 hours:**
* **249 owner alert emails, 219 of them "Payout overdue" (88 percent).**
* They concern **11 distinct payouts** (10 still REQUESTED and past deadline, 88 reminders across them).
* The other 30: "Marketplace clips are waiting" 6, "Campaign at 90% budget" 6, and 18 standard-payout countdowns.

---

## PART 6: EVERYTHING ELSE THAT COULD BE QUIETLY FAILING

| check | number now | changed? | would anyone notice? |
|---|---|---|---|
| thumbnail sweep on the cron service | skipped on **144 of the last 24 hours' ticks** (storage credentials absent) | unchanged since BL-918 | no, and it does not matter: the web service fills pictures; **26 of 26 approved clips have pictures and frames** |
| approved clips carrying the three frames | **26 of 26**, including the owner's 6 from today | up from 20 | n/a |
| tracking reaching every v2 post | **47 of 47** posts have an active job; **43** checked in the last 24 h; **0** never checked, 0 with no job | healthy | the 4 not checked in 24 h are the 4 flagged video-unavailable |
| share recording (BL-914: Instagram 53.9 percent over 30 days) | Instagram **60.5 percent** of 7,792 snapshots in 7 days, TikTok **100 percent** of 347 | not a regression | **one** Instagram snapshot has shares above 0 with no source (BL-914 said none since BL-820); one row, logged |
| L5 agency monitor | **92** violations across 7,286 rows | unchanged (BL-921's frozen legacy) | it repeats every tick; nobody acts on it |
| `TRACKING_RECALC_FAIL` since BL-924 deployed (10:50 UTC today) | **0**; 9 ever; the last 2026-09-22 20:00:58 | fixed | yes: the tick writes the row |

---

## PART 7: THE RANKED LIST, WORST FIRST, WITH EVIDENCE

**Costing somebody money or time right now:**
1. **Ten real clippers are owed $1,797.71 past deadline, up to 23 days late.** Five are marketplace posters; one is owed $908.70. **Owner action** (pay them). It also removes 88 percent of his alert email.
2. **Nobody in the marketplace can ever request money at today's rates: ANGIE BROWN's minimum is $25.00, the best earner has $1.66.** Every person who earned anything (8 people) is 59 to 390 days away. **Owner decision / config** (the campaign's minimum payout).
3. **Posters lose work to rule breaks: 8 of 47 real posts (17 percent) were rejected, all for campaign rules.** Four were for the original sound and four for the caption, from 4 people, each post paying $0. All 8 predate the rules gate; its effect is **not yet measurable** (the 9 posts since are all pending). **Watch, then copy.**
4. **Post links wait up to 28.4 hours for the owner, with no alert that they exist**; 7 are pending now. **Code** (an alert like the maker one) **plus owner action**.
5. **A maker's unshared clip has waited 101.5 hours and can never be approved.** One person, who has not been back since the 21st. **Owner action**: the "cannot open it" rejection.
6. **Half of all approved posts earn nothing: 16 of 32 sit under the campaign's 500-view minimum** (median 485 views). This is the rule working as written, and it is the owner's design. One poster has 7 posts and $0.00 (4 flagged video-unavailable, 1 rejected) and stopped on the 20th. **Owner decision.**

**Should merely be better:**

7. **The biggest committed drop is invisible**: 8 of 17 posters opened Drive and never posted, with **zero refusals**. The client-side stops (no approved account; rules unread) send no request, so the recorder cannot see them. 4 of 24 posters hold no clip account at all. **Code**: record those client-side stops.
8. **The 30-minute window is unobservable**: its verdict lives only in the Railway console, and no post stores a publish time. **Code** (record the verdict) **or read the Railway log once**.
9. **Supply rests on one real maker (80 percent of real approved clips)**, with no real submission in 79.7 hours, and nothing reports it. **Code**, small (PART 4). Two of the three rejected makers stopped after their second rejection; one sent the requirements link instead of a video. One person each; no pattern.
10. **24 marketplace bells, 0 read.** Email carries every alert, and 88 percent of email is reminders. **Owner habit / a digest**, BL-920's standing suggestion.
11. The cron's thumbnail skip, and one shares row without a source: harmless and logged.

**THE SINGLE MOST VALUABLE THING TO DO: pay the ten overdue payouts.** It is $1,797.71 to ten real people who asked for their money, the oldest 23 days ago. Half of them are the marketplace's own posters, and doing it silences 88 percent of the owner's alert email.

**The next decision after that is ANGIE BROWN's $25 minimum**, because until it comes down or earnings go up, the marketplace cannot pay anybody.

**Is the honest answer that nothing is wrong and the marketplace just needs more clips?** Partly:
* **Nothing is broken:**
  * 3 real refusals in its whole life, all rules working;
  * the recorder is writing;
  * every post is tracked and every clip has frames;
  * no new conflict rows;
  * the new rules gate has turned away nobody it could see.
* **Supply is thin, not dry.**
* **The friction is not a defect but three settings and a queue:**
  * the money the owner has not yet paid;
  * the $25 minimum;
  * the 500-view minimum;
  * reviews that take a day.
