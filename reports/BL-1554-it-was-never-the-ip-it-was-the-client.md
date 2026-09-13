# BL-1554 — it was never (only) the IP, it was the CLIENT — and the free email is already being thrown away

**Can he get the Instagram bio for free without buying anything, how fast, and what is the
honest fallback price?** **Yes.** The logged-out profile page still serves the real biography,
and it serves it to **small** accounts — this round pulled the exact, paid-verified bio of an
account with **15 followers**, and recovered the page 14 times out of 15 on accounts whose
median size is **251 followers**. The reason this machine could not see it is not the reason I
published last round. **A browser engine on this same machine, same network, same URL, gets
the real page where Python's `urllib` gets a content-free shell — 10/10 against 0/10, Fisher
p = 1.08e-5.** `urllib` with a perfect Chrome User-Agent fails; with full Chrome header order
and `Sec-Fetch-*` it fails; over HTTP/2 it fails. What Chromium supplies that no Python HTTP
client can is the **TLS handshake fingerprint**, and that is the one dimension this project
had never varied. **So the free route is: drive a real browser engine, which is already
installed here.** Inside its allowance it runs at **0.137 s per page** — his 2,000 usernames
is **4.6 minutes** of *fetching*, but see the next sentence, because fetching is not the
binding constraint. The catch is a **silent per-IP quota at roughly 445 hydrated
renders** (HTTP 200 throughout, no error, no CAPTCHA), keyed to the IP and **not** reset by
cookies, a fresh process or a different engine — so 2,000 pages needs about **4.5 quota
windows** — and **the quota did not recover at all in 72.6 minutes of monitoring (0 of 50,
Wilson [0.00% – 7.14%])**, so those windows are not cheap. **For "1,000–2,000 usernames,
really fast and reliably" the honest answer is therefore the paid call, not the free
route.** He does not need to buy those either: **PrivadoVPN,
Windscribe and Proton are all already installed on this machine and all three have free
tiers.** And the honest fallback he should hear before spending a day on any of this: at
$0.00069064 a call, **2,000 usernames costs $1.38**, and every bio-less Instagram row he owns
costs **$11.26**. Finally, two corrections that matter more than the route: **his objection to
the verified filter is right and I was wrong** — verified accounts are gated as likely editors
at **16.25% [11.34–22.75]** against unverified **28.81% [26.58–31.14]**, non-overlapping and
the *wrong way round*, and the filter can only ever reach **17.4%** of the editor supply. And
**the free email is already being extracted in production and discarded**: `page_capture.py`
runs an address regex over the free bio into `out.emails`, and the only consumer of that
payload never reads the key. Spend this round: **$0.0504** of a $0.25 cap.

---

## 1. What this project is, for a reader with no context

This system finds video editors and meme-page operators on TikTok and Instagram and collects
the email address many of them publish in their profile bio. A "bio" is the short free-text
blurb on a profile. On TikTok it arrives free with search results. On Instagram it has to be
bought one profile at a time from a reseller API at **$0.00069064 per call** — unless the
public, logged-out profile page can be read, which is what this round is about.

## 2. Safety and the cap

* **Nine stores backed up**, sha256-verified, **bodies found by shape** — `spend.json`'s
  payload is the list at `runs` (36,482 rows), `clip_seen.json` is a **bare list** (2,193),
  `tiktok_pages_seen.json` is a **dict at `pages`** (3,270), where a dict-only reader reports
  **3**.
* **All six corruption controls FIRED**, including the position-qualified one: delete one row
  of a duplicated pair and the natural-key set is **provably identical** while only the
  indexed digest moves.
* **The cap was proved to bind before the first call** by lifting `Budget` from
  `harvest_run.py` **by AST**: it advances by the **Instagram** unit ($0.00069064) and not
  TikTok's ($0.00060000), 15.1% apart; `$0.00` **raises**; the meter does not move on a
  refusal; under **8 threads** the locked counter stops at exactly 50 of 50; **the proof wrote
  nowhere**.
* `IgClient` constructed **`metered_by_caller=True`** throughout.
* **`docs/FACTS.md` at lag +0** against a live 36,482 rows (limit +2000). No re-stamp needed.
* `clippershq/` **read-only all round. Not one production file was modified.**
* **No proxy was bought and no VPN was connected.** He said no proxies; and connecting a VPN
  re-routes the whole machine, which is his call, not this round's.

## 3. Part 2 — the question that decided the round: does a clean exit serve SMALL accounts?

Every previous remote success was a space agency, a magazine or a global brand. If Instagram
serves those logged-out and walls everyone else, every free-exit plan is worthless.

**The accounts had to be found without ever sending a lead handle to a third party.** So the
pool was built from **off-domain** public searches — ceramics, bookbinding, model railways,
birdwatching, letterpress, amateur astronomy; nobody's clipper lead — and every candidate was
passed through a corpus gate holding **126,342 lead handles and 30,904 walked handles**, whose
reverse control was proved first (a real lead handle and a real walked handle must both be
refused, a fabricated one admitted). **172 candidates, 0 already in either corpus.**

60 of them were then bought as ground truth. **This is a genuinely small population:**

    follower distribution   min=0   p25=62   MEDIAN=251   p75=976   p90=7,735   max=103,423
    size bands              under 1k: 46     1k-10k: 9    10k-100k: 4    100k-1M: 1

Scored **by value** against the paid bio text, from a clean exit:

| band | followers | served |
|---|---|---|
| under 1k | 15 – 937 | **7 / 10** |
| 1k – 10k | 1,815 – 3,715 | 2 / 2 |
| 10k – 100k | 21,094 – 44,805 | 2 / 2 |
| over 100k | 103,423 | 1 / 1 |

* **bio recovered and value-matched: 12/15 = 80.0% [54.8% – 93.0%]**
* **the page itself was served 14/15 = 93.3% [70.2% – 98.8%]** — measured independently by the
  follower count, which matched the paid API **exactly on 11** and was **rounding-consistent
  on 3** ("21K", "44.8K", "103K"), with **0 inconsistent**. A page returning the correct live
  follower count is not a cached shell.
* **The smallest served account had 15 followers.**
* **Control:** a fabricated handle returned no bio, no follower count and no display name.

Two of the three "failures" under 1k returned the **correct exact follower count**, so the
page was served and only the bio text was not surfaced — the instrument is a summariser, and
every such case was scored **against** the route. **80% is a floor, not an estimate.**

**Answer: yes. Account size is not the gate.**

## 4. The correction: BL-1553 said "it is the IP". That was half wrong, and I published it.

**BL-1553's comparison moved two variables at once** — the exit IP *and* the HTTP client — and
attributed the whole difference to the IP. Holding the exit **fixed** and varying only the
client is the test that had never been run:

| client, same machine, same exit, same URLs | real handles returning `biography` |
|---|---|
| `urllib` + Chrome User-Agent, HTTP/1.1 *(BL-1553's arm)* | **0 / 10** |
| `httpx`, full Chrome header order + `Sec-Fetch-*`, HTTP/1.1 | **0 / 10** |
| `httpx`, same headers, **HTTP/2** | **0 / 10** |
| **Chromium browser engine, logged out, no cookies** | **10 / 10** |

Fisher exact **p = 1.08e-5**, and the browser ran **last**, from the most quota-consumed
position. **HTTP/2 alone does not help. Header order alone does not help.** The bio is in
server-rendered HTML, so this is not JavaScript — the remaining variable a Python client
cannot change and Chromium supplies for free is the **TLS handshake fingerprint**.

I verified the client split myself in a third way. From this machine, right now:

    python urllib     -> HTTP 200, 626,047 bytes, 0 `biography` keys, no display name
    curl.exe (Schannel) -> HTTP 302 -> /accounts/login/
    PowerShell (.NET)   -> HTTP 302 -> /accounts/login/

**Three clients, one machine, one exit, three different answers.** `urllib` is the only one
that returns a **200 that looks like success and contains nothing** — which is exactly how it
was mistaken for an IP ban.

## 5. The catch: a silent per-IP quota, and this round spent it

    976 sustained requests, concurrency 6, logged out, public brand handles:
      pass  1-6   bio 60/60 each   (360/360, Wilson [98.94 - 100])
      pass  7     bio 12/60        <- the wall arrives mid-pass
      pass  8-16  bio  0/60 each   (0/540,  Wilson [0 - 0.71])

The quota broke at roughly **445 successful hydrated renders**. It is **silent**: HTTP 200
throughout, **0 errors in 976 requests**, no challenge, no rate-limit string — and latency
*fell*, because a shell is cheaper to serve. **That is precisely the symptom BL-1553 diagnosed
as a permanent IP block.**

What it is keyed to, **tested rather than assumed**: same context again **0/5**; fresh context
and fresh cookie jar **0/5**; fresh browser process **0/5**; a different engine entirely
**0/5**. **Keyed to the IP.** Which also means clearing cookies is not a route — so the one
gray-area move that might have needed a policy decision is simply unavailable.

**This round then spent that quota on itself.** My own browser run, executed afterwards, got
**0 of 12** — every one a login wall — and the native TLS clients went to 302 as well. A
pacing probe on `urllib` ran to completion — **21 probes, 14 of them on real
institutional accounts, gaps widening to 15 minutes, 0 ever served [0.00% – 21.53%]** — but
that probe was measuring `urllib`, which fails for a reason pacing cannot fix, so **it does
not answer the recovery question.**

**The recovery question now HAS an answer, and it is the one that decides the route.** A
browser-engine monitor ran to completion: **25 probes over 72.6 minutes**, recovering **0 of
50 [0.00% – 7.14%]**. The quota did not lift at all in an hour and a quarter.

⚠️ **ONE CONFOUND, STATED RATHER THAN BURIED:** probing every 3 minutes is not a clean idle
test. If the limiter is a *sliding* window, the monitor's own probes may have been holding it
shut. A correct measurement needs a single probe after one long, fully idle gap, and this
round did not run one. So the honest claim is **"no recovery observed in 72.6 minutes of
3-minute polling"**, not "the window exceeds 75 minutes" and not "the quota never
recovers".

## 6. Part 3 — free exits, and he already owns three

| route | result |
|---|---|
| **VPN clients already installed** | **PrivadoVPN, Windscribe, Proton** — all three have free tiers; the `ovpn-dco` driver is **already running**; a WireGuard driver is present |
| native OS TLS clients (`curl.exe`, PowerShell) | **not shelled** — served real content until the anonymous allowance tripped, then honest 302s |
| Tor | **not installed**, no daemon on the usual local SOCKS ports. Not installed by this round; flagged for him to decide |
| a popular reader/extraction service | dead — bot challenge |
| a CORS-anywhere-style relay | dead — service outage |
| a formerly-free CORS proxy | dead — now paywalled, API key required |
| public proxy lists | **not retested.** Already refuted: 2.89% usable, **91 of 91 forged certificates** |

The three relay services also share a structural defect worth recording: **you cannot verify
Instagram's own certificate through them** — you see the relay's TLS session, not Instagram's.

**Nothing was connected and nothing was installed.** A VPN on Windows re-routes the entire
machine, and the certificate chain of any candidate exit must be pinned against the genuine
fingerprint before anything else is measured.

## 7. Part 4 — his objection to the verified filter, settled. He is right; I was wrong.

BL-1553 (mine) recommended a `verified`-only filter on a 3.2x cut in cost per **address**. He
replied: *"99.9% of editors are not verified."*

| | k / n | rate | Wilson 95% |
|---|---|---|---|
| VERIFIED gated as a likely editor | 26 / 160 | **16.25%** | [11.34% – 22.75%] |
| UNVERIFIED gated as a likely editor | 437 / 1,517 | **28.81%** | [26.58% – 31.14%] |

**Non-overlapping, and the wrong way round.** Of every account the gate calls a likely editor,
**437 of 463 — 94.4% — are unverified.** He said 99.9%; the measured figure is 94.4%. Same
direction, same conclusion.

Repriced on the unit the business actually buys:

| | accounts bought | editor-addresses | **$ per 1,000 EDITOR-addresses** |
|---|---:|---:|---:|
| buy everything | 1,677 | 23 | **$50.36** |
| buy ONLY verified | 160 | 4 | **$27.63** |

A nominal 1.8x — but the underlying yields are **9.30% [3.68–21.60]** and **19.59%
[12.91–28.58]**, which **overlap almost entirely**. The advantage is not established; it rests
on **4** successes. **And the disqualifier is supply:** of the 23 editor-addresses in the whole
corpus the filter can ever reach **4 (17.4%)** and **permanently discards 19 (82.6%)**.

**Do not ship it.** BL-1553 priced the wrong unit: cost per address fell because the
denominator fell, and the numerator fell further.

⚠️ **The size confound remains UNMEASURED** — 0 of 1,677 rows carry a follower count, because
the free surface has none. **ABSENT, never "no confound".**

## 8. The finding that outranks every route above

**The free Instagram email is already being extracted in production, and nothing reads it.**

`clippershq/page_capture.py` defines `FREE_FACTS_JS`, evaluated live inside `capture_one`,
which the real camera loop calls. It runs an address regex over the free bio:

    out.emails = Array.from(new Set(em.map(x => x.toLowerCase())));

Scoped to the payload at `cap["free_facts"]`, here is every key its only consumer reads:

    biography  captions  follower_count  full_name  posts  user_pk  video_posts

    produced by the JS blob : biography, emails, follower_count, posts, source, user_pk, video_posts
    PRODUCED BUT NEVER READ : emails, source

**Positive control:** `biography` is known to be read off this payload, and the scoped detector
finds it at two sites — so its zero for `emails` means something. `source` is the three-state
wall detector, also unread, which is why the funnel still cannot tell "no bio" from "never
read this page".

## 9. WHAT I GOT WRONG

**1. I published "the wall is the IP, not the platform" from a two-variable comparison.** It
was the headline of BL-1554's predecessor. Local fetches used `urllib`; remote fetches used a
different fetcher entirely; the whole difference went to the IP. The client was doing most of
the work, and a silent per-IP quota that had *already been spent* supplied the rest. Both
halves were invisible because `urllib` returns **HTTP 200 with 626 KB of nothing** — a failure
shaped exactly like a success.

**2. I recommended a filter that would have discarded 82.6% of the editor supply**, because I
priced per address when the business buys editors. He caught it; the data backs him.

**3. My first re-derivation of his objection called the gate wrong.** The signature is
`gate(handle, nick=None, bio=None)` — three arguments. I called `gate(bio)`, which passes the
bio text as the **handle** and leaves `bio=None`, so it ran the name rule over bio prose and
never ran the bio rule at all. It produced a clean, separated, non-overlapping result pointing
the same way (13.12% vs 21.89%) — **which is what made it dangerous.** Wrong positional
arguments are the same failure class as a wrong field name: the call succeeds and the answer
is about something else.

**4. I contaminated my own Part 2 measurement.** For the three accounts whose page displays a
**rounded** follower count ("21K", "44.8K", "103K") I recorded the **paid integer** in the
"what the remote exit returned" table, so the comparison was `21094 == 21094` — ground truth
checked against itself. Three of fifteen "exact" matches were manufactured that way. Fixed:
the remote record now holds only what the page displayed, and a rounded string is tested for
**consistency**, which is a weaker and honest claim.

**5. My first check of the free-email claim answered a different question and "refuted" a true
finding.** I asked whether anything in `clippershq/` reads the key `emails`, got **98** AST
reads, and wrote NOT CONFIRMED. But `emails` is a common key name package-wide and almost none
of those reads are on this payload. A detector that answers a different question will refute a
true claim as confidently as it confirms a false one. Re-scoped to the payload, the answer is
the opposite.

**6. I nearly attributed this round's spend with a ledger delta — the exact thing the rules
forbid — and then demonstrated why on myself.** The vendor-side balance moved **138 requests**
while my own counter said **73**. `spend.json` was **unchanged** (36,482 rows, last written the
previous day), so no concurrent funnel explains it: the window simply **spans two rounds**,
because its start was a reading taken while the previous round was still spending. I also
checked the receipts themselves with a controlled before/after on two endpoint types — both
**AGREE exactly** — so the receipt-sum is sound and the delta is the broken instrument.

## 10. What the round cost

| | |
|---|---|
| **my own counter at the wrapper** (sum of `x-hiker-info` receipts) | **73 billable requests · $0.050417** |
| — 10 off-domain searches to build a non-lead pool | $0.006906 |
| — 60 paid profiles as ground truth (bio + real follower count) | $0.041438 |
| — 3 measurement controls | $0.002072 |
| vendor balance delta over the window | 138 requests — **spans two rounds, not attributable** |
| everything in sections 4, 5, 6, 7 and 8 | **$0.00** |
| cap | $0.25 — **finished at 20.2% of it** |
| proxies bought | **none** |

## 11. What to do next, in order

1. **Read the `emails` key you already produce.** The free address is being extracted and
   dropped at the point of use. This is a local change in one consumer, costs nothing, and
   needs no network route at all.
2. **Stop using `urllib` for the page. It can never work** — it is not the IP, it is the TLS
   fingerprint. Drive Chromium, which is already installed.
3. **Treat the free browser route as a background trickle, not a bulk route — this is a
   change from what this report first recommended.** At ~445 renders per window and **no
   recovery observed in 72.6 minutes**, 2,000 usernames is roughly 4.5 windows of unknown and
   apparently long duration — most of a day at best. Rotating exits (PrivadoVPN, Windscribe, Proton — installed and
   free) buys one window each, which is worth having against the **16,306-row backlog** over
   weeks. It is **not** the way to get this week's 2,000.
4. **Do not ship the verified filter.** It discards 82.6% of the editor supply.
5. **And know the fallback price before spending a day on any of it: 2,000 usernames is
   $1.38.** Every bio-less Instagram row you own is $11.26. The free route is worth building
   for the *next* 100,000, not for this week's 2,000.

## 12. What did not run, reported as ABSENT

* **Whether the free VPN exits are served by Instagram.** Commercial VPN ranges are widely
  abused and are often blocked *harder* than a home IP. **Unmeasured — a real risk, not an
  assumption.** The harness is built and validated against the blocked exit (it correctly
  reports a clean zero with its controls intact) and needs one command once a VPN is up.
* **Quota recovery time under a CLEAN idle gap.** Measured under 3-minute polling: **0 of
  50 over 72.6 minutes [0.00% – 7.14%]**. A single probe after one long untouched gap was
  **not** run, so a sliding-window limiter held open by the monitor's own traffic is not
  excluded, and the window's true length is therefore still unknown.
* **The mobile-hotspot exit**, which is a residential mobile address and usually the least
  blocked kind. Not tested.
* **Tor.** Not installed; nothing was installed to find out.
* **The size confound on the verified filter.** Structurally unmeasurable on the free surface.
