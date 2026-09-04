# BL-1496 — the ruler was wrong four ways, and one of his six thresholds can kill

> **Reading this cold?** This project runs an automated funnel that finds social-media pages
> worth contacting. It spends real money with three vendors, and records every cent in a ledger
> (`spend.json`). That ledger is also what the spending **caps** read, so an inaccurate ledger
> does not just misreport — it mis-authorises. This round was asked to fix the ledger *before*
> measuring anything with it.
>
> Creator handles are redacted. Paths are relative to the repository or use `%USERPROFILE%`.
> No port numbers appear.

---

## THE LEDGER BILLED EVERY FAILED ATTEMPT. The booking ran **before** the request was sent, at **three** sites — the brief named one. A run that never opened a socket still wrote real rows. Fixed at a single chokepoint, and driven across **eight failure modes**.

## INSTAGRAM WAS PRICED AT TIKTOK'S RATE. Re-derived from his live ledger: **6,642 of 7,688 rows — 53,313 calls — booked at $0.000600 instead of $0.00069064. $4.83 of real spend was never recorded**, leaving the Instagram ledger **9.60% low**. It also mis-sized every cap: `max_calls = int(cap / cost)` let a $3.00 cap authorise **$3.45**.

## A MODEL THAT BILLS WAS COUNTED AS FREE. "Paid" was `model == PAID_FALLBACK`. `glm-5.3-flash` is asked on every page, **holds cutting authority at 90**, bills per token — and booked **nothing**, while eating a free-tier quota it is not subject to.

## THE JUDGE'S DOLLARS WERE INVISIBLE TO THE RUN THAT SPENT THEM — **17,124 rows, $1.5240, 2.48% of the whole ledger**, sitting outside every run record. A measured window read **7.99% low**.

## ⚠️ AND ON HIS SIX THRESHOLDS: two were already his value, three are **loosenings that cannot kill anything**, and **one is a brand-new floor whose cost I could not measure** — because `media_count` is empty on **72,757 of 72,956** lead-store rows. It ships UNKNOWN-SAFE and says so; §3.6 has the one-line off switch.

## ⚠️ AND THE PROFILE PURCHASE MUST NOT MOVE YET. The brief's own precondition fires: moving it strips **four rendered lines** from the judge's prompt — display name, followers, verified, exact post count. 266 bytes → 202. That is a verdict change, not a saving. §3.7.

**Money: $0.00, 0 vendor calls**, counted by this round's own counter. ⚠️ **But I did write five real ledger rows by accident and removed them — §5.1.**

---

# 1. ROUND ID, DATE, AND WHAT I WAS ASKED TO DO

**BL-1496**, 2026-09-04. Fix four ledger defects; set his six thresholds and prove each selects;
three free savings; a before/after per brain.

**Before touching anything.** The port table (never a command-line grep) showed **one** listening
Python process — his sheet/review server. **No dashboard listener**, re-checked immediately
before *every* write under `clippershq/`, six times. Nothing was killed. Backups of config, the
ledger, the lead store and all five seen stores: **9 of 9 verified by sha256 against the source**,
with a control proving a corrupted copy is detected.

**Round number.** BL-1493, 1494 and 1495 already exist as reports, so this is **BL-1496**.

---

# 2. THE TABLE

| # | The thing | Before | After | Proof |
|---|---|---|---|---|
| 0a | Booking happens before the send | **3 sites** | after, 1 chokepoint | 8 failure modes driven |
| 0a | A failure that never reached the vendor | **billed** | not billed | real ledger watched |
| 0b | Instagram price | $0.000600 | **$0.00069064** | 3 writers driven |
| 0b | …and TikTok | $0.000600 | unchanged | the control |
| 0c | Judge dollars in the run record | **never** | yes, in-window | 7.99% measured |
| 0c | Another funnel's dollars | excluded | still excluded | the control |
| 0d | Models recognised as billing | **1** | **2** | prices differ 3.00× |
| 0d | A derived price | — | flagged `estimated` | ledger column |
| 1 | IG min posts | 13 | **10** | loosening |
| 1 | IG recency | 152 *(one campaign)* | **180** | loosening |
| 1 | TT min avg views | 3,000 | **1,000** | selects, control fires |
| 1 | TT min posts | **none** | **10**, unknown-safe | selects; off-switch works |
| 1 | Campaigns on the same six | **4 of 5** | **5 of 5** | resolved from his config |
| 2a | The profile purchase | before the judge | **unchanged — blocked** | 4 lines would be lost |
| 2c | The number that actually cuts | — | **90**, per model | 80 governs nothing |

---

# 3. WHAT WAS MEASURED

## 3.1 THE BOOKING RAN BEFORE THE SEND — at three sites, not one

`_book_paid_call()` executed, and only *then* `txt = _ask(...)`. If the request failed, nothing
reversed it. The brief named `free_judge.py:1503`; **the identical five lines appear three
times**, at 1503, 1855 and 2025. Fixing only the named one would have left two-thirds live —
this project has a key-mismatch that was fixed three times for the same reason.

The fix is one chokepoint, `_ask_billed`, which owns the send *and* the booking so the sites
cannot diverge again. Whether a failure cost money is now a stated property:

```
failure mode                                 books   why
the request SUCCEEDS                           1     a delivered generation
connection refused (no socket opened)          0     THE DEFECT -- this used to bill
DNS failure                                    0     never left this machine
HTTP 401 (no key) / HTTP 402 (no credit)       0     the vendor REFUSED before generating
HTTP 500                                       1     may have generated, failed to deliver
read timeout                                   1     sent; may have completed server-side
torn JSON from a RECEIVED response             1     the bytes arrived, so it generated
```

**8 of 8 correct**, driven through the shipped function against a real ledger writer. It errs
toward **billing** where it cannot tell, because under-counting is the dangerous direction: the
ledger feeds the caps, so a low ledger authorises *more* spend.

> ### ⚠️ AND THERE IS A BETTER PROOF THAN MY SYNTHETIC MATRIX, BECAUSE IT WAS AN ACCIDENT
>
> A concurrent round ran two probes today that sealed the network completely — `socket.socket`,
> `create_connection`, `getaddrinfo`, `socketpair` and `ssl.wrap_socket` all replaced with
> raisers **before any project import**, the API key stubbed, and sockets asserted still blocked
> at exit. **Not one packet left the machine.** What neither probe patched was
> `_book_paid_call`. The ledger recorded **eight bookings** — 8 × $0.000089 = **$0.000712** —
> at 16:22:47–16:23:15 and 18:02:56–18:03:24, all `FREE_JUDGE` / `free_judge_paid_fallback`.
> The second batch is **four rows, one per brain**: exactly the four rubric captures that agent
> was making.
>
> **An agent that had sealed every socket and stubbed the key still booked one row per brain —
> because the booking happened before the send, and did not care whether a send was even
> possible.** That is the defect stated as cleanly as it can be: the ledger was recording
> *intentions*, not calls.
>
> It is independent of my instrument, it was produced by someone not trying to demonstrate it,
> and it is still on disk — which is the main reason I left those rows in place (§6) rather
> than tidying away the only unforced evidence of the bug this round exists to fix.
>
> *(Provenance note: that round first attributed the second batch to a different script of its
> own and then corrected itself by reading the imports rather than trusting which script
> happened to be running. The corrected mechanism is the one above, and it is sharper than the
> first telling.)*

**Category: GENERAL** — one chokepoint, and a property test rather than a name test.

## 3.2 INSTAGRAM WAS PRICED AT THE OTHER PLATFORM'S RATE

`ig_cost = ig_calls * cost_per_call`, and `cost_per_call` is LamaTok's — it even **defaults to
`0.0006`** on both aux writers. HikerAPI bills `$0.00069064`, and `ig_client.py` already declares
that as "the one place it is written down".

**Re-derived from his live ledger** by recovering the price from each row — the two rates are
incommensurate, so the divisor that yields a whole number of calls identifies which was used
(control: synthesised rows at each price classify correctly at n = 1, 7, 25, 100, 1626, 5000):

```
rows with ig_usd > 0      7,688      total booked $45.5028
  booked CHEAP            6,642      $31.9878     86.4% of rows
  booked CORRECTLY        1,023      $12.8259
  ambiguous / neither        23      $ 0.6891
calls at the wrong price 53,313
should have been         $36.8201     NEVER RECORDED $4.8323   (13.12% short)
the Instagram ledger is  9.60% low
```

That is independent agreement with the brief's $4.80 / 9.56% from a different method.

Fixed at all three arithmetic sites — `record_spend`, `_record_aux_spend_locked`,
`preflight_check` — through one owner, `ig_client.HIKERAPI_USD_PER_CALL`, with an explicit
`ig_cost_per_call` override for a config that carries its own.

**THE CONTROL THAT MATTERS: TikTok did not move.** LamaTok genuinely bills $0.000600, and a
"fix" that re-priced both vendors would look identical on the Instagram arm while inflating
TikTok by 15.1%. Driven at n = 1, 25 and 1626: TikTok unchanged, Instagram correct, a mixed
three-vendor row correct on each column.

⚠️ **This was never only a reporting error.** `meme_finder` computes `max_calls = int(cap / cost)`.
Driven through the real `preflight_check`: **5,000 Instagram calls now project $3.4532 where they
projected $3.0000.** A $3.00 cap was authorising $3.45 of spend. The cap was not a cap.

**Category: GENERAL** — a single owner plus a safer default at the chokepoint.

## 3.3 THE JUDGE'S DOLLARS NEVER REACHED THE RUN THAT SPENT THEM

`run.py:_spend_now` filtered `campaign == <the run's campaign>`; `free_judge` books under the
hard-coded `"FREE_JUDGE"`, which is not in `run.py`'s CAMPAIGNS table. So every judge dollar was
invisible to the run record that caused it. **`tools/status_board.py` has been printing a warning
about this for several rounds and nothing acted on it.**

Driven on a synthetic run — its own rows, judge rows inside its window, a judge row from *before*
it started, and a concurrent funnel:

```
the run's own rows              $0.160000
the judge's rows in-window      $0.013900
_spend_now now reports          $0.173900   (it reported $0.160000)
the run record was understating itself by 7.99%
```

which independently reproduces the brief's 7.94%. Lifetime: **17,124 rows, $1.5240, 2.48% of the
ledger.**

**Two controls, both required.** A different funnel is **still excluded** — a fix that merely
stopped filtering would have credited every run with every other run's spend, the exact
misattribution the filter exists to prevent. And with **no time window** no shared-service rows
are added at all, so one run can never be charged the judge's entire lifetime.

⚠️ **The known limit, stated rather than papered over:** two runs judging simultaneously will each
count the shared rows in their window, so the figure **over**-attributes under concurrency. That
is the safe direction for a cap, and it cannot be fixed here — the ledger has no `run_id` column
(status_board reports that too: not one of 25,460 rows carries one).

**Category: GENERAL** — a declared set with a documented rule, not a special case.

## 3.4 A MODEL THAT BILLS WAS COUNTED AS FREE

"Paid" was `model == PAID_FALLBACK`. But `z-ai/glm-5.3-flash` is in `SCORED_PAID`, is asked, holds
**reject authority at 90**, and the module's own comment says *"IT IS NOT FREE. prompt
$0.000000075/token … 3x nex-n2-mini's rate."* Being a different string, it was:

* counted as a **free** send against a 1,000/day free-tier ceiling it is not subject to, and
* **never booked to the ledger at all**.

Now `PAID_MODELS` is a membership test over a price table, at all six decision points across the
three send loops (checked by **AST**, not substring — see §5.4). Driven:

```
nex-n2-mini    books 1   $0.0000890   estimated=False   MEASURED from observed usage
glm-5.3-flash  books 1   $0.0002670   estimated=True    DERIVED = 3x nex's prompt rate
minimax:free   books 0        --          --            genuinely free, still free
free-tier ceiling: only the free model counts against it
```

⚠️ **One price is measured and one is derived, and the ledger now says which.** glm has never been
metered here, so its figure comes from this file's own statement about its rate and is written
with `estimated=True`. **It should be replaced by a measured number, and it is probably LOW** —
glm runs at full reasoning (9–15 s, no `effort: low` gate), so its completion side is likely
larger than a prompt-rate multiple implies.

**Category: GENERAL** — a rule about the property ("does this id bill?") replaces a rule about
one name, which is the same lesson this file already records about a model-name substring.

**⚠️ THE CONTROL FOR ALL OF PART 0, AND I DID NOT RUN IT.** 151 lines changed in `free_judge.py`
— the module that builds every judging prompt — so the thing to prove is that **no brief moved**.
A concurrent round re-hashed all four rubrics against my committed change, with the network
blocked and the booker neutered, and reports them unchanged:

```
tiktok/memes     28c05f855e13      instagram/memes  46a1a4d89cbc
tiktok/edits     d43802ad3f9a      instagram/edits  ff1ff0b70cb0
negative control: the bare RUBRIC   f81c4b39bd4f    -- correctly differs from all four
```

Those are the four values my brief pins. **Zero bookings on that run**, which is also the first
independent confirmation that the §3.1 fix holds outside my own harness. An independent check by
someone with no stake in my result is worth more than a control I wrote myself, and it is the
reason this section can claim "no verdict moved" at all.

## 3.5 HIS SIX THRESHOLDS — two were already right, and the brief's "current" column is stale

Resolved the way the shipped code resolves them, from his real config, per campaign:

| filter | brief says current | **actually was** | his value | verdict |
|---|---|---|---|---|
| IG min avg views | 500 | **1,000** | 1,000 | **already his value** |
| IG min posts | 13 | 13 | 10 | changed — a loosening |
| IG recency | 152 | **152 on ONE campaign, 180 on four** | 180 | changed — a loosening |
| TT min avg views | 3,000 | 3,000 | 1,000 | changed — a loosening |
| TT min posts | none | none | 10 | **created — the only one that can kill** |
| TT recency | 180 | 180 | 180 | **already live, confirmed** |

⚠️ **The Instagram views floor was never 500.** It is `meme_finder.MIN_AVG_VIEWS = 1000`, and four
of five campaigns set `ig_min_avg_views: 1000` explicitly. Nothing to change.

⚠️ **And ANIME15K was quietly on a different rule.** It is the only campaign that sets *nothing*,
so it alone ran on the 152-day code default while the other four set `ig_max_age_days: 180`. All
five now resolve to the identical six values.

## 3.6 WHAT THE NEW THRESHOLDS COST — and the one I could not measure

**Three of the four changes are LOOSENINGS and cannot kill a page.** That is arithmetic, not a
measurement, and saying so is more honest than presenting a measured zero as a retired risk:

* IG min posts 13 → 10 admits a superset. It also settles a case the code already flagged: 13
  *"rejects his twelve-post page by exactly one post"*. At 10 that page is kept.
* IG recency 152 → 180 admits a superset.
* TT min avg views 3,000 → 1,000 rejects a strict subset. (It was also measured at 0 of 101
  killed at 3,000 — but a measured zero on 101 observations cannot rule out 1-in-27, so the
  arithmetic is the stronger argument.)

**Driven, and each proved to SELECT with a control that changes the outcome:**

```
avg views    at 1000    at 3000 (old)
   999        reject       reject
  1000        KEEP         reject     <- newly kept
  2999        KEEP         reject     <- newly kept
  3000        KEEP         KEEP
```

> ### ⚠️ THE ONE THAT CAN KILL, AND I COULD NOT PRICE IT
>
> **TikTok min posts = 10 did not exist before**, so every page below it is newly rejected. Its
> kill rate on his own marks is **UNMEASURED**, and here is exactly why: `media_count` is empty
> on **72,757 of 72,956** lead-store rows (99.7%), it is empty on **all 163** of his wanted
> TikTok pages that join the store, and **no corpus on disk carries a per-handle video count for
> them**. A sweep would have returned "0 of 0 killed = 0.0%", which is a false zero, so it is not
> reported as a result.
>
> **Two things bound the risk, both driven:**
> 1. **A MISSING COUNT IS KEPT, NEVER REJECTED.** `None`, `''` and `'n/a'` all return
>    `is_target=True`. A failure to look is not a verdict — and the count is missing far more
>    often than it is low, so treating absent as zero would have rejected almost everything.
> 2. **It reads the FREE count.** `author_video_count` rides on the discovery payload, not the
>    paid profile's `videos_total` — verified by AST over the function body. A floor built on the
>    paid field would have re-created the purchase §3.7 is trying to avoid.
>
> **To turn it off: `"tt_min_posts": null`.** Driven — a 9-post page is kept with the floor off.

**A guard made me do more than change a number.** `tests/test_bl1282_thresholds.py` went red on
`MIN_TOTAL_POSTS: docs say 13, meme_finder.py says 10`, with the message *"A moved threshold
needs its classification re-read, not just its number changed."* It is right. `docs/THRESHOLDS.md`
justified 13 as **FITTED-ONLY** on *"33 accounts behind his 37 example reels — positives only, no
rejects"*. **10 is not fitted at all — he dictated it**, which is a different kind of number and
now says so, at the same standing the doc already gives his other dictated values. The new TikTok
floor was added to the doc's *"What has no provenance at all"* section, because that is exactly
what it is until someone can measure it.

## 3.7 ⚠️ THE PROFILE PURCHASE MUST NOT MOVE YET

The brief asks to move the paid TikTok profile call to *after* the picture judge — but only after
measuring what it supplies, *"if any field the judge or a rule reads comes from that call, moving
it changes behaviour, not just cost."*

**It does.** Driven through `free_judge.facts_block`, the thing that actually renders facts into
the prompt, with the profile present and with `_pf = {}` exactly as on a page that never bought
one:

```
LINES THE JUDGE LOSES:
   - display name: <name>
   - followers: 48,200
   - verified: yes
   - 217 posts read          (falls back to the free count, 214 -- a different number)

prompt bytes 266 -> 202     sha256 85d0d3497f6c -> 9cebfddebc77
```

The bio **survives** (free on 93.8% of authors). But display name, followers and verified do not
— and those are exactly the lines a judge uses to tell a creator page from an edits page, the
class causing 71% of his TikTok rejections.

**So the move was NOT made.** Measuring the bytes was the precondition; the bytes changed; the
precondition fails. It needs its own A/B on his marks. ⚠️ Note also that the code says `_pf` is
already empty on *"most pages since BL-1358"* — so the saving may be much smaller than 1,185
pages implies, and that is worth establishing before spending a round on it.

## 3.8 WHICH REJECT NUMBER ACTUALLY CUTS

Three numbers exist and they disagree. The answer, from the code:

| number | what it is | does it cut? |
|---|---|---|
| **`REJECT_AT = 80`** | the gate's **floor** — no model may hold authority below it | **NO. It governs nothing.** Every live bar is 90, so 80 is beneath all of them |
| **`MAY_REJECT` = 90** | the per-model bar | **YES — this is the cut.** Both live models sit at 90 |
| **`KEEP_AT = 95`** | labels a *confident keep* band | no — a label, not a cut |

**Nothing stale is still printed.** A previous round already replaced the operator line: it now
names the cutters with their own bars (`glm-5.3-flash@90, nex-n2-mini@90`) and calls 80 a
"Floor". A repo-wide check found `REJECT_AT` in no other operator-facing string. **This item was
already fixed before this round; reporting it as newly fixed would be taking credit for someone
else's work.**

---

# 4. WHAT WAS REFUSED OR NOT DONE

- **The profile purchase was not moved** (§3.7). The brief's own precondition blocks it.
- **The slow model was not removed or time-boxed (Part 2b).** It holds reject authority and said
  REJECT on 7 of its 9 pages, so removing it **will** change verdicts — the brief requires that
  scored on his marks with Wilson bounds first, and that needs a model run per arm which this
  round's $1.00 cap and remaining time do not cover. What this round *did* establish is the
  constraint the scoring must respect: the paid model is tried **first, deliberately**, and
  `glm-5.3-flash` is the one that bills per token, holds authority at 90, and until today booked
  nothing — so any timing figure quoted for it before this fix was measured against a $0.00 line.
- **⚠️ NO LIVE BEFORE/AFTER PER BRAIN (Part 3).** This is the largest omission and I am not going
  to disguise it. A 50–100 page live sample per brain across four brains is hours of wall clock
  and real vendor spend; I had $1.00 and had already spent the round on Parts 0 and 1. **I will
  not compose a price out of a carry rate** — the brief names that as exactly how $137.31 and
  $78.53 were manufactured — and a per-1,000-delivered figure measured any other way would be
  fiction. The baselines stand unchallenged: TikTok memes **$19.52 / 8.21 h**, Instagram edits
  **$131.21 / 175.22 h**, Instagram memes **$176.76 / 265.69 h**, TikTok edits **delivered ZERO —
  undefined, not free**, against targets of **$2.00 and 2 hours**.
- **No judging rule was added or loosened** beyond the four threshold values he specified.
- **No seen-store row was written, rewritten or deleted.**
- **His sheet server was left running** throughout.
- **BL-1497's phantom ledger rows were left in place** — see §6.

---

# 5. WHAT I GOT WRONG

1. **⚠️ I WROTE FIVE REAL ROWS INTO HIS LEDGER.** My first booking probe set
   `CLIPPERSHQ_SPEND_FILE` and assumed that redirected the write. **It does not:**
   `_book_paid_call` passes an *explicit* path to `record_aux_spend`, and an explicit argument
   beats the environment. So the probe wrote **5 × $0.000089 = $0.000445** into `spend.json`
   while reading an empty scratch file — which means it also reported **"0 bookings" on every
   arm**, a false zero, at the same moment it was polluting the thing it was measuring. Both
   halves wrong from one assumption. I removed exactly those five rows after proving the delta
   was exactly mine and nothing foreign had landed, restored `total_spent_usd` and
   `vision_spent_usd`, and the ledger is byte-equivalent to my pre-probe backup apart from its
   write timestamp. Every probe since forces the path at `_book_paid_call` itself and re-checks
   `spend.json`'s sha256 **after every arm**, so a repeat stops on the first row rather than the
   fifth.
2. **⚠️ I NEARLY PUBLISHED A FALSE FINDING IN A REPORT ABOUT LEDGER ACCURACY.** I compared the
   per-row `dollars` column against `total_spent_usd`, saw a $0.0012 gap, and concluded the
   ledger "no longer reconciles" and was being written mid-flight. A peer session challenged it;
   I checked, and it is **one row from 2026-08-04** — a deliberate `dollars`-only correction
   booking money the ledger had not known about. `total_spent_usd` equals the five category
   scalars **to the digit**. Two different quantities, compared as if they were one. That is the
   exact class of error this round exists to remove, and it was mine.
3. **My verification could not see what it was verifying.** I checked "the ledger is
   byte-equivalent to my backup" — but four phantom rows from another round predate that backup
   and sit *inside* my baseline, so that check would report success whether or not they were
   there. A baseline taken after the contamination cannot detect the contamination.
4. **A comment-vs-code check went red three separate times in one round.** My "no equality tests
   remain" counter matched the phrase inside a *comment*; my "reads the free count" check matched
   `videos_total` inside its own *docstring*, which mentions it only to explain why it is not
   used. Both rewritten as AST over the function body. I have a standing note that byte-window
   guards trip on comments and I still wrote two more.
5. **A shell heredoc ate my escapes and corrupted a patch script**, and a patch written with bare
   `\n` against a CRLF file inserted **four LF-terminated lines** into `meme_finder.py`. Caught by
   counting bare LF before and after; normalised; the diff is 5 insertions, 1 deletion, with no
   mass terminator rewrite. My own notes say to write patch scripts as files. I did that *after*
   the heredoc failed, not before.
6. **My first threshold driver built a synthetic author with the wrong field** (`play_count`
   instead of `views`) and the judge raised rather than answering — which is the right behaviour
   from the judge and a wasted cycle from me.
7. **I asked a session whether it was a round number.** Sessions do not carry round numbers;
   `.claims/*.json` is the mapping, and I had already read the file that answered it.

---

# 6. MONEY AND SAFETY

**This round: $0.00, 0 vendor calls**, counted by the run's own counter, not a ledger delta —
every driver stubs the socket and no API key was ever used. The only ledger movement I caused was
the accidental $0.000445 in §5.1, which I removed.

**Backups: 9 of 9 verified by sha256 against the source**, with a control proving a corrupted copy
is detected as a mismatch.

**Seen stores at publication, compared as ROW key sets** (not top-level keys — that mistake made a
2,446-row store read as 3 last round): TikTok **2,446** · meme **6,125** · clip **2,193** · repost
**1,715** · Spotify **1,898**. **No row was written, rewritten or deleted by this round.**

**The ledger at publication:** 25,460 rows; `total_spent_usd` **$61.385350**, equal to the sum of
its five category scalars to the digit.

⚠️ **EIGHT ROWS DATED TODAY ARE NOT MINE AND I LEFT THEM.** They are `FREE_JUDGE`
`free_judge_paid_fallback` rows, 8 × $0.000089 = **$0.000712**, written by a concurrent round
whose probe hit the same trap I did. **I did not remove them**, for three reasons: they are not
mine, and this project has already lost a round to someone deleting 56 rows another had paid for;
they are 0.0012% of the ledger and change no figure here; and they are the *before-picture* of the
defect §3.1 fixes — four rows billed with no socket ever opened. If he wants them gone, the
reconciliation is `vision_spent_usd` and `total_spent_usd` each **−$0.000712**, or the ledger
stops reconciling.

**Ports:** re-checked immediately before **every** write under `clippershq/` — six times, never
once at the start. His sheet server was up throughout and was not touched. No `taskkill` was run.

**Concurrency.** Another live round holds `clippershq/main.py` for a different purpose. I messaged
it with the exact four functions I touched, agreed to land first, and passed on the
`_book_paid_call` trap so it would not repeat my §5.1 mistake.

---

# 7. WHAT HE SHOULD DO NEXT — RANKED

1. **The Instagram ledger is $4.83 light and 9.60% low on everything before today.** New spend is
   now priced correctly, but historical Instagram figures — and any per-address cost derived from
   them — are 13.1% understated. Nothing needs restating unless a decision rests on one.
2. **Decide about the TikTok posts floor** (§3.6). It is live at his 10 and cannot reject a page
   whose count we never learned, but its true cost is unmeasured. To measure it, a run has to
   record `author_video_count` per page — it is free and already on the discovery payload; it
   simply is not being written to the lead store, where `media_count` is empty on 99.7% of rows.
   **`"tt_min_posts": null` turns it off** in the meantime.
3. **The profile-move saving needs its own round** (§3.7), and should start by establishing how
   many pages still buy a profile at all — the code says most no longer do.
4. **Give `glm-5.3-flash` a measured price** (§3.4). It is booked at a derived $0.267/1,000 flagged
   `estimated`, and that figure is probably low.
5. **The judge still has no `run_id`.** Its dollars now reach the run record by time window, which
   over-attributes when two runs judge at once. A `run_id` column on the ledger would end that
   whole class of question.
6. **⚠️ `dashboard/.running.json` claims a server that has been dead since 30 August.** It names a
   pid; that process does not exist and nothing has listened on the dashboard port for five days.
   Nothing cleans the marker up. It bears directly on this round: a pid in a file is a *claim*,
   and the only *observation* is the listening-port table — which is why every one of my six
   pre-write checks used the port table and not that file. Two sessions cited the marker to me as
   evidence of a live server tonight and both were wrong. Anything that reads it to decide whether
   a run is alive is reading a five-day-old assertion.
6. **Part 3 remains open**: nobody has a current $ per 1,000 delivered or hours per 1,000 for any
   of the four brains, and TikTok edits has still delivered zero, which is undefined rather than
   free.

---

# 8. FULL PATHS

Relative to the repository root; no absolute paths are published.

**Changed:** `clippershq/free_judge.py` *(the booking chokepoint, the paid-model table)* ·
`clippershq/main.py` *(the Instagram price at three writers)* · `clippershq/run.py` *(shared-service
campaigns)* · `clippershq/meme_finder.py` *(two Instagram thresholds)* ·
`clippershq/tiktok_finder.py` *(the views floor and the new posts floor)*

**Instruments, all re-runnable:** `scratch/bl1496_drive_booking.py` ·
`scratch/bl1496_ig_price_audit.py` · `scratch/bl1496_drive_ig_price.py` ·
`scratch/bl1496_drive_runrecord.py` · `scratch/bl1496_drive_paidmodels.py` ·
`scratch/bl1496_effective_thresholds.py` · `scratch/bl1496_sweep_thresholds.py` ·
`scratch/bl1496_drive_thresholds.py` · `scratch/bl1496_drive_profile_move.py` ·
`scratch/bl1496_backup.py` · `scratch/bl1496_unbook.py` · and the three patch scripts.

**Read but never modified:** `spend.json` (apart from §5.1, reversed) · `master_leads.csv` ·
all five seen stores · `config.json`.

**Backups:** `backups/bl1496_<timestamp>/`.

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/BL-1496-the-ruler-was-wrong-four-ways.md
