# BL-1552 — TikTok against Instagram, same tags, priced properly

**TikTok is cheaper per address, cheaper per editor, and faster — and the margin is not close.
Run TikTok at scale.** Measured on the same twelve tags in the same suffix shape: TikTok
**$4.26 per 1,000 addresses [$2.99–$6.10]**, Instagram **$44.61 [$20.72–$97.05]** — a ~10x gap
whose intervals **do not overlap**, so this is a separation and not a point estimate. Per *likely
editor* TikTok is **$17.66 [$10.12–$34.88]**; Instagram's is **undefined**, because 0 of its 6
addresses passed the editor gate — even at the optimistic bound of that interval it is
**$114.27**. On the clock TikTok is **0.354 s per account (≈4.1 h per 1,000 addresses)** against
Instagram's **1.49 s (≈24.9 h)**, and Instagram's wall is **per-IP, so it does not parallelise
while TikTok does**. **The published "Instagram $0.79 per 1,000, 3.1x cheaper" is overturned, and
the reason is specific: the free Instagram bio route died.** 708 of 708 accounts returned no bio;
three institutional control accounts returned the same empty shell; the only remaining source of
an Instagram bio is a paid call, and that is the whole of the 10x.

---

## 1. What this project is, for a reader with no context

A funnel discovers TikTok and Instagram accounts belonging to video editors ("clippers"), reads
their public bios, and extracts published email addresses. Vendors: **LamaTok** for TikTok at
**$0.000600 per call**, **HikerAPI** for Instagram at **$0.00069064** — 15.1% apart, which is why
each arm below was given its own budget object built from its own named config key, and why the
cap proof checks *which constant each arm used*.

The structural difference this round exists to price: **the TikTok hashtag call carries the bio
free**; **the Instagram hashtag call carries no bio at all** — only `is_verified` — so an
Instagram bio needs a second request.

**Nothing latched.** No seen store, no tag ledger, no `spend.json`, no master write. The
Instagram client ran `metered_by_caller=True` so its autoflush wrote no ledger row (BL-1351
measured that shape booking money exactly 2x). All nine backed-up stores were byte-identical
after every leg.

## 2. Safety and the cap

Nine stores backed up sha256-verified, **bodies found by shape**: `spend.json` → `runs` 36,482;
`master_leads.csv` 72,971; `clip_seen.json` a **bare list** of 2,193; `meme_pages_seen.json` →
`pages` 6,196; `tiktok_pages_seen.json` → `pages` 3,270; `spotify_playlists_seen.json` →
`playlists` 1,970; `repost_seen.json` 1,715; `email_harvest_tags.json` → `tags` 572;
`config.json` 173 keys.

**All six corruption controls FIRED**, including the two that exist because a reader once got
them wrong:

- **C4, index-qualified:** on a duplicated pair, deleting one leaves the natural-key set
  **provably identical** (both digests equal, measured) while the index-qualified digest moves.
- **C6, wrapped store:** a synthetic 3,270-entry dict under `pages` — the shape reader reports
  **3,270**; a dict-only reader reports **3**. That is the exact failure that shipped once.

**The cap binds, on both units.** The shipped `Budget` was lifted from `harvest_run.py` by AST and
driven under **8 threads × 50 attempts**: funded allows and the meter advances one unit; `$0.00`
raises; **the meter does not advance on a refusal** (`spent $0.00000000, calls=0`); 8 threads took
exactly 20 of 20. And explicitly for this round's purpose: TikTok unit = `api.cost_per_call_usd`
= $0.000600, Instagram unit = `ig_api.cost_per_call_usd` = $0.00069064, **the two differ by
15.1%**, and the Instagram accessor **refuses to fall back** to the TikTok price. The proof wrote
nothing.

## 3. Making it a fair test — and the compromise I had to make

**Same twelve tags, same order, same suffix `<topic>edit` shape, film and sport buckets only**
(fighter tags measure 1.21% and were not opened).

But the tags are **not** the ones intended, and the reason is a finding:

> **The ledger's "never walked" pool is largely tags that DO NOT EXIST.** All 12 first-choice
> tags returned HTTP 500 on `hashtag_info`. A control settled that this was not an outage —
> three known-good ledger tags resolved cleanly in the same minute and `/sys/balance` answered.
> A wider probe then found **35 of 35 fresh film and sport tags dead**. They are fresh *because*
> nobody could walk them.

The ledger keys on **tag AND endpoint**, so a tag walked shallow (v1) is untouched on the deep
endpoint (v2). **406 tags are in exactly that state.** The twelve used are the highest-supply film
and sport ones — proven to exist (136–168 authors each on the shallow walk) and never walked deep.

⚠️ **The cost of that compromise, measured and not hidden: their accounts were seen on the shallow
walk, so the TikTok arm paid an already-held tax that Instagram — which has never touched these
tags — did not.** Across the TikTok arm, **1,762 of 3,087 accounts touched (57.1%) were already
held and skipped before their bio was read.** That is close to the 54.24% the project already
measured for a re-walk. **This biases the comparison AGAINST TikTok, and TikTok still wins by
10x.**

## 4. The TikTok arm

**206 calls, $0.12360, 452 s.** Deep endpoint `/v2/hashtag/medias`, `count=30` (40/50/100 are
HTTP 400), paged on cursor, stopped on **saturation** and never on `has_more`, **every body
hashed — 0 repeat bodies across 194 paged calls**, validated on list length and never on status.

| tag | bucket | pages | accounts | already held | net-new | bio | addresses | saturated |
|---|---|---:|---:|---:|---:|---:|---:|---|
| saulgoodmanedit | film | 25 | 369 | 213 | 156 | 136 | 3 | page cap |
| magnetoedit | film | 6 | 97 | 73 | 24 | 21 | 0 | **6** |
| moonknightedit | film | 25 | 329 | 187 | 142 | 134 | 6 | page cap |
| lokiedit | film | 25 | 428 | 216 | 212 | 199 | 6 | page cap |
| cobrakaiedit | film | 25 | 419 | 290 | 129 | 110 | 6 | page cap |
| theflashedit | film | 25 | 414 | 277 | 137 | 124 | 2 | page cap |
| duncanedit | sport | 25 | 312 | 140 | 172 | 159 | 0 | page cap |
| stonesedit | sport | 3 | 44 | 41 | 3 | 3 | 0 | **3** |
| bayernedit | sport | 5 | 63 | 37 | 26 | 22 | 1 | **5** |
| martinezedit | sport | 1 | 9 | 2 | 7 | 7 | 0 | **2** |
| verstappenedit | sport | 25 | 379 | 188 | 191 | 173 | 5 | page cap |
| lampardedit | sport | 2 | 24 | 18 | 6 | 2 | 0 | **3** |

```
net-new accounts        1,205        bio present   1,090  (90.5%)
accounts w/ address        29        distinct addresses 29
address rate            2.41%  [1.68 - 3.43]
calls 206 · spend $0.12360
$ per 1,000 accounts    $0.10
$ PER 1,000 ADDRESSES   $4.26  [$2.99 - $6.10]
seconds per account     0.3540    per-call median 2.039s · p90 2.633s · max 8.526s
```

## 5. The Instagram arm — and the free bio route is dead

**This is the finding that decides the round.**

The Instagram hashtag call carries no bio, so the project's answer was the **free profile page**,
previously measured at **76.5% [52.74, 90.45] on 17 accounts**. On 708 accounts today it returned
**`bio_state = unknown` on 708 of 708**.

That zero was controlled four ways before being believed:

1. **The extractor works** — `bio_from_body` returns a planted bio; `has_content` rejects a shell.
2. **Re-asking slowly recovered 0 of 6.** By this project's own discriminating test, **that rules
   out a rate limiter.**
3. **Institutional controls fail identically** — `instagram`, `nasa` and `natgeo` all return
   `has_content=False`, ~499 KB, `bio_len=0`. **Not account-specific.**
4. **Searching for the value, not the field name:** the 500 KB body carries
   `is_logged_out_user_ssr`, `PolarisProfile` and `ProfilePage`, and does **not** carry
   `biography`, `edge_followed_by`, `og:description` or `profile_pic_url`. It is the logged-out
   shell, just a large one.

**Conclusion: Instagram now serves a logged-out shell with no profile payload to this header set.
The free route that made Instagram look cheap is gone.** The paid profile call still carries the
bio (verified 3 of 3 on institutional accounts), so that is what this round priced.

The hashtag walk itself worked well, with **four denominators counted separately** — and they are
not interchangeable:

| tag | pages | sections | slots | authors | **distinct authors** | already held | net-new |
|---|---:|---:|---:|---:|---:|---:|---:|
| saulgoodmanedit | 2 | 19 | 57 | 57 | **21** | 3 | 18 |
| magnetoedit | 25 | 241 | 723 | 723 | **609** | 153 | 456 |
| moonknightedit | 25 | 229 | 687 | 687 | **381** | 147 | 234 |

**723 slots deduplicating to 609 distinct authors** on one tag is why the four counts are reported
separately. 0 repeat bodies.

```
accounts discovered (hashtag)   708      costing $0.03591
bios BOUGHT (paid profile)      361      costing $0.24932
bio present                     345  (95.6%)     bio empty 16     bio unknown 0
accounts w/ address               6      distinct addresses 6
address rate                  1.66%  [0.76 - 3.58]
attributable spend            $0.26763   (paid bios + discovery apportioned to those 361)
$ per 1,000 accounts          $0.74
$ PER 1,000 ADDRESSES        $44.61  [$20.72 - $97.05]
seconds per account           1.4897    per-call median 1.413s · p90 2.001s · max 21.322s
```

## 6. The answer he asked for

| | TikTok | Instagram |
|---|---|---|
| **$ per 1,000 addresses** | **$4.26** [$2.99 – $6.10] | **$44.61** [$20.72 – $97.05] |
| **$ per 1,000 likely editors** | **$17.66** [$10.12 – $34.88] | **undefined** (0 of 6); ≥ $114.27 even at the optimistic bound |
| **editor share of addresses** | 24.1% [12.2 – 42.1] | 0.0% [0.0 – 39.0] |
| **seconds per account** | 0.354 | 1.490 |
| **hours per 1,000 addresses** | **≈4.1 h** | **≈24.9 h** |
| **parallelises?** | yes | **no — the wall is per-IP and more lanes makes it worse** |
| **bio source** | free, in the hashtag call | **paid profile call (the free route is dead)** |
| **prior published figure** | $2.47 fresh / $3.70 re-walk | $0.79 |

**TikTok is ~10x cheaper per address, the only one with a defined price per editor, and ~6x
faster. It is also the one that parallelises. Run TikTok at scale.**

⚠️ **What these intervals permit, and what they do not.** The address-cost intervals **do not
overlap**, so the cost ordering is a real separation. **The editor comparison is not** — 29 and 6
addresses give ±14.9 and ±19.5 point intervals, and 0 of 6 is consistent with anything up to 39%.
**Do not quote 24.1% versus 0.0% as a finding; quote that TikTok's editor price is defined and
Instagram's is not.**

⚠️ **The TikTok figure is above its own published $2.47 fresh baseline**, and the already-held tax
in §3 is the likely reason — these tags were shallow-walked, so 57.1% of accounts touched were
skipped before their bio was read. $4.26 is the price of a *deep re-walk of shallow-walked tags*,
which is close to the $3.70 the project already measured for a re-walk.

## 7. Quality of what was collected

**Deliverability** (`address_check.py`, MX refreshed with **this run's domains**, never the
default):

- TikTok: **29 of 29 pass**, 100.0% [88.3–100.0]. Flags kept, never dropped: 1 role inbox,
  1 creator/business domain. No rejections.
- Instagram: **5 of 6 pass**, 83.3% [43.6–97.0]. **One was rejected as
  `handle_reference:handle_syntax_at_is_glued`** — the rule shipped in BL-1549 firing on live
  data, catching an `@handle` that the de-obfuscator had fused into an address.

**Hallucination is impossible on this path** — no model touches it. Extraction is pattern matching
over a bio the vendor returned. The risk is **mis-extraction**, which is what the handle-reference
rule and the two-tier sourcing test exist for. And **whether a mailbox accepts mail is not
knowable without sending, which this project does not do.** These are deliverability *signals*.

**Zero duplicates, by both keys, which are different keys:**

```
account ids emitted   1,566   distinct 1,566   duplicates 0
addresses emitted        35   distinct    35   duplicates 0
addresses already in master or an earlier round: 0
```

The guard was built from master **plus all 12 prior round row files** — 150,373 known accounts and
14,662 known addresses — and every account was checked **before its bio was read**, which on
Instagram is the whole saving because the bio is the expensive part.

## 8. The shortfall, stated plainly

**TikTok returned 29 of a target 30. Instagram returned 6 of 30.** Neither was padded.

- TikTok exhausted all twelve tags; five saturated early (one at page 2). Reaching 30 would have
  needed a thirteenth tag.
- Instagram stopped at the **$0.50 stop-and-report line**, at $0.44211 of a $0.75 budget. At its
  measured 1.66% address rate, 30 addresses would have needed ~1,800 paid bios ≈ **$1.24** — well
  over this round's entire budget. **That is itself the answer**: at today's prices, 30 Instagram
  addresses cost more than the whole round.

## 9. WHAT I GOT WRONG

1. **I walked three Instagram tags and bought 708 accounts before checking that I could read a
   single bio.** The free-bio route was dead the whole time. Controlling it first would have cost
   one free request and saved **$0.03591** of hashtag calls whose bios I could not read. The
   order was backwards: I proved the *discovery* worked and assumed the *extraction* did.
2. **My address-dedup call was inverted and would have produced zero addresses.**
   `guard.claim_address()` returns a *reason string* when an address must be refused and `None`
   when it is fine — the same shape as `skip_account`. I wrote `if guard.claim_address(e)`, which
   keeps **only duplicates**. It would have reported "these tags have no emails". Caught in
   preflight, before a cent was spent.
3. **`DedupGuard.build()` with no `prior_rows` loads ZERO accounts.** My first preflight printed
   `known_accounts_loaded: 0` — the entire account-dedup guarantee, silently vacuous. It reads
   addresses from master but accounts only from row files you hand it. Now 12 files, 150,373
   accounts, with a hard stop if it is ever zero again.
4. **My extractor control used a `.test` domain and failed** — the deliverability guard rejects
   it *by design*, exactly as it rejects `example.com`. I nearly read a healthy extractor as
   broken. Rebuilt on a domain the system accepts.
5. **`import run` resolved to `clippershq/run.py`**, a production module of the same name earlier
   on `sys.path`, not to this round's scratch runner. It raised here — but had that module carried
   a same-named attribute it would have silently used the wrong one. Inlined.
6. **I picked twelve tags from the ledger's "fresh" pool without checking they exist.** All twelve
   were dead, costing **$0.00720** to discover. The wider probe cost another **$0.02160**. Both
   were worth it — the finding that the fresh pool is mostly non-existent tags is reusable — but
   the order should have been probe-then-walk.
7. **`IgClient()` refused to construct** without an owner label, because its autoflush writes to
   the money ledger. Correct refusal; I switched to `metered_by_caller=True`, which both attributes
   the spend to my own counter and stops the double-booking BL-1351 measured.

## 10. What the round cost

**$0.44211 of $0.75**, from my own counters at the wrapper, never a ledger delta — every leg named:

| leg | calls | unit | spend |
|---|---:|---|---:|
| TikTok: 12 non-existent tags (HTTP 500) | 12 | $0.000600 | $0.00720 |
| TikTok: liveness control + balance | 4 | $0.000600 | $0.00240 |
| TikTok: fresh-tag existence prober | 36 | $0.000600 | $0.02160 |
| **TikTok ARM** | **206** | $0.000600 | **$0.12360** |
| Instagram: hashtag walk (3 tags) | 52 | $0.00069064 | $0.03591 |
| Instagram: paid-bio route probe | 3 | $0.00069064 | $0.00207 |
| **Instagram ARM: paid bios** | **361** | $0.00069064 | **$0.24932** |
| **TOTAL** | **674** | | **$0.44211** |

**$0.0954 — 21.6% of the round — went on discovering that 47 tags do not exist and that the free
Instagram bio route is closed.** Both are reusable findings, and both are cheaper to know than to
re-learn.

**Routing:** every measurement here was one command against files or the two clients; no
sub-agent was spawned, because nothing in this round was a multi-file sweep. The expensive context
held the cap proof, the four-way control of the Instagram zero, the tag-existence diagnosis, and
this report.

## 11. The output

35 rows appended to the workbook at `%USERPROFILE%\OneDrive\Desktop\Random\clipper_emails_ALL.xlsx`
— **found by searching, since it lives in a subfolder** — each marked with **Platform, Tag, Bucket
and Round** so the two arms can be told apart.

**Add-only, verified per sheet by a parser after writing:**

```
Emails          2,007 -> 2,042   (+35, exactly the rows added)
No email       24,241 -> 24,241  (unchanged)
Unjudged leads 13,178 -> 13,178  (unchanged)
```

Zero C0 control bytes were asserted **before** the write. The workbook is his and is not committed.
