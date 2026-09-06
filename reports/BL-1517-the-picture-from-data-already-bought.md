# BL-1517 — Can the picture be built from data already bought?

**Round:** BL-1517 · **Filed:** 2026-09-06 · **Cap:** $2.00 · **Spent: $0.00**

---

## The one paragraph

**Yes — the data is there, and the two facts that were supposed to decide it both came back
favourable.** One paid Instagram posts call returns a **median of 12 post thumbnails** (up to 24
on one endpoint, and a median of 30 on sectioned hashtag payloads), and those thumbnails are
**640×1136 portrait stills**, not small crops — with a genuine separate `first_frame` cover
available on **883 of 883** media that carry an image block. That is the same 9–12 tiles a
screenshot delivers, at a usable size. And the signed URLs do **not** expire immediately: the
declared window is a **median of 34.8 hours** from the moment the payload is written, p05 13.2 h,
max 108 h. **"Fetch them now or not at all" is wrong — a run-time fetch sits comfortably inside
the window; only a RETAINED url is dead.** So the ingredients for a browser-free sheet exist.

**But this round did not finish, and I will not tell you it did.** All five sub-agents were
killed by a session rate limit part-way through their work. **The picture was not built, not
scored on his marks, and nothing about the browser has changed.** What shipped is Part 5 — the
free account id, persisted and protected — which halves the buy-outright price from **$19.73 to
$9.88 per 1,000** with no new capability. **On the proxy question: do not cancel that purchase
on the strength of this report.** The evidence points that way, but the measurement that would
justify it — a paired score with delivered counts — was not made.

---

## 1. What one paid call actually returns

Measured by walking every saved Instagram payload on disk, per endpoint, counting medias
**including carousel children** and never trusting a "biggest list" heuristic.

| endpoint | files | top-level medias, median | max |
|---|---:|---:|---:|
| `/v2/hashtag/medias/*` (sectioned) | 74 | **30** | 33 |
| `/gql/user/clips` | 3 | **24** | 24 |
| `/v2/user/medias` | 23 | **12** | 22 |
| `/v2/user/clips` | 78 | **12** | 13 |
| `/gql/user/medias` (flat) | 2 | **12** (23 incl. carousel children) | 12 |
| `/v2/search/reels` | 9 | **12** | 12 |
| **`/v2/user/by/username` (the PROFILE call)** | 65 | **0** | 0 |
| `/v1/media/comments` | 20 | 0 | 0 |
| `www.instagram.com/<h>/embed` (free) | 2 | 0 | 0 |

**The profile call carries no post thumbnails at all — the picture must come from a POSTS call.**

⚠️ **That zero was checked for the field-name error before being believed**, because three
one-word mismatches have cost this project months each (`bio` vs `biography`, `media_count` vs
`posts`, and a follower field whose producer and renderer used different spellings). Across 65
profile payloads and **376 distinct key paths**, every key whose name could possibly mean media
was enumerated, and every field holding an HTTP url was counted: the profile call's urls are
`hd_profile_pic_versions[].url` (130), `bio_links[].url` (83), `profile_pic_url` (65) — **profile
pictures and link-in-bio, no post covers.** The zero is real.

### The pixel size, and a cover frame nobody reads

Across **883 media carrying `image_versions2`**:

| primary still size | count |
|---|---:|
| **640×1136** | **427** |
| 720×1280 | 174 |
| 750×1333 | 83 |
| 640×1138 | 40 |
| 750×1334 | 37 |
| 540×960 | 29 |

**These are full portrait stills, not thumbnails in the small sense.** And every one of the 883
also carries `first_frame` and `igtv_first_frame` candidates — **DIFFERENT FILES from the
primary on 883 of 883** — so a genuine video cover frame is available separately from whatever
the primary happens to be.

### The expiry window — the brief's framing is wrong

Measured offline from the `oe` (expiry) parameter on **53,180 URLs** with a decodable expiry
(35,676 more carried none), against each file's own mtime:

| | hours |
|---|---:|
| p05 | 13.19 |
| p25 | 32.24 |
| **median** | **34.76** |
| p75 | 105.41 |
| p95 | 107.47 |
| max | 108.00 |

Histogram: **29,392 at ~1 day, 22,080 at ~4 days.** And **174 URLs were already expired when
they were written to disk.**

**0 of 53,180 are still inside their declared window today** — which is exactly why every
retained URL fails, and why the earlier "39 of 39 expired / 9 of 9 fresh returned 200" result
looked like instant death. **It is not instant. It is one to four days.** A sheet built during
the run that bought the payload is far inside the window; a sheet built from anything on disk is
far outside it. That distinction is the whole design constraint and it was previously stated
backwards.

*(MEASURED for the declared window; the window is what the CDN promises, and I did NOT
separately confirm by fetching at the boundary — that arm died with its agent.)*

---

## 2. The free route, and its ceiling

The `/embed/` route returns **6 covers per response** — not 12. Probed to **301 requests**,
paced:

| | |
|---|---|
| responses returning posts | **205 / 301 (68.1%)** |
| covers per successful response | median **6**, max 6 |
| elapsed | median **0.92 s**, p90 1.33 s, max 3.03 s |
| last successful request | seq **298** |
| shell responses (page served, no grid) | 13 |

⚠️ **95 of those 301 responses were HTTP 200 WITH NO POSTS.** That is the trap the brief names
in its own words — *validate on list length, never on status* — arriving live: a third of the
route's replies look like successes and carry nothing. **Anything built on this route must count
the list, not the status code.**

The probe stopped itself at seq 300 when its own control returned HTTP 500 with zero bytes.
**So the free route sustains roughly 300 paced requests before refusing** — which is a real
ceiling, and it delivers half the tiles of the paid route.

---

## 3. What shipped: the free account id, persisted and protected

**Fix category: GENERAL** — the protection sits at the two chokepoints every store write passes
through, not at a caller.

The paid grid costs **one** billed call when the numeric id is known and **two** when it is not:
**$9.88 against $19.73 per 1,000 delivered.** The id is free on the discovery record (61 of 61
pages that bought a profile carried it; the page's own embedded JSON corroborates on 56 of 61),
but only the seen store keeps it after the run that learned it.

**What would destroy it is not a delete — it is an ordinary write carrying `user_id: ""`.**
`dict.update` takes the blank without a word and the next run pays again. The merge is now
monotonic: a stored numeric id may be **replaced by another valid id, never blanked**, and every
other field keeps `update` semantics exactly as before.

⚠️ **The helper existed with ZERO CALL SITES and I nearly shipped it that way.** `PageSeen._merged`
was written, correct and documented, while **both** writers still used `dict.update`. An AST
sweep for its call sites returned **zero** — against a control that found **7** `update()` calls
with the same sweep, so the finder worked. **A helper is not a protection until something calls
it.** Both `record()` and `record_many()` now call it; the batch path matters most, because a
500-page walk takes it.

**Mutation-proved in both directions**, by monkeypatching the merge in memory so no production
file is ever left half-reverted:

| arm | `record()` | `record_many()` |
|---|---|---|
| as shipped | protects ✓ | protects ✓ |
| **mutated to plain `update`** | **fails ✗** | **fails ✗** |
| restored | protects ✓ | — |

⚠️ **And the harness failed its own restore first.** Reading `PageSeen._merged` in Python 3
yields a plain function, so assigning it straight back makes it an instance method that receives
`self`. **Both red arms passed and the restore raised `TypeError`** — the one direction that
would otherwise have gone unnoticed.

`tests/test_bl1517_user_id_is_never_blanked.py` is **committed**, 8 methods with a declared
census so a class appended after the main guard cannot go unrun, and it carries the control that
makes the rest mean anything: **an ordinary field must still be overwritable, including to a
blank** — otherwise a merge that refused everything would pass every other assertion.

---

## 4. What the capture path actually costs today

From **3,653 capture records**:

| state | count |
|---|---:|
| grid ok | 2,694 |
| **private** | **392** |
| **login wall** | **310** |
| unknown | 175 |
| key absent | 82 |
| **zero tiles (any cause)** | **626** |

And of 427 pages where the free-facts extractor ran successfully, **111 yielded a bio and only
9 yielded an email.** That is the number to hold against the claim that removing the browser
costs a free address source: on this corpus the free bio-email path produced **9 addresses out
of 427 reads (2.1%)**. *(MEASURED on the stored corpus; the paired comparison against the paid
contact button was not completed — see §6.)*

---

## 5. Two things found on the way that were not on the brief

**The reports clone was broken, and it looked fine.** `../clippershq-reports/.git/objects` had
been **deleted** while `HEAD`, `config`, `refs/heads/main` and `packed-refs` all remained. So
`[ -d .git ]` returned TRUE and every git command returned *"fatal: not a repository"*. Repaired
by cloning fresh — and **before moving anything**, both working trees were compared by sha256:
**1,190 files against 1,213, with ZERO files existing only in the broken copy**, so nothing was
lost. The broken clone is preserved untouched at
`clippershq-reports.BROKEN-objects-deleted-20260906`. The deletion falls in a **1h48m window**
(last successful git op 13:42, `.git` mtime 15:30). **I do not know the cause and am not going
to guess one.**

**The mark-reader resolution fix is live**, confirmed by driving rather than reading, because the
brief requires it before anything is scored: a split key adopts to one, last keystroke wins
(the later mark survives), and a handle naming two platforms is **refused rather than merged**.
⚠️ **My first probe fed dicts where `resolve()` expects `Mark` objects — and its own control
(two different handles must give two keys) returned 0 and refused to certify anything, printing
DO NOT SCORE.** The refusal was correct and it was about my instrument.

---

## 6. What this round did NOT do

**All five sub-agents were terminated part-way through by a session rate limit (HTTP 429), not
by their work.** What follows is missing, and none of it is being reported as a zero:

* **The sheet was not built and not delivered to a judge.** A peer round created
  `clippershq/payload_sheet.py` this round — it reuses the existing compositors
  (`paid_grid.build_sheet` with `trim=False`, `pad_pair_share` on raw tiles) on the free
  6-cover embed route. **It is untracked, it is not mine, and I did not measure it.**
* **No paired score on his marks.** No catches, no kills, no Wilson bounds, no delivered counts.
  **This is the measurement that would justify changing anything, and it does not exist.**
* **No pixel measurement at the network boundary** — the base64-decoded request body was never
  opened, so how a built sheet differs from a screenshot in *delivered* pixels is unknown.
* **The address trade was not completed.** §4 gives one side only.
* **No seconds-per-delivered-page comparison**, built versus screenshotted.
* **The reserved question was not answered.** Its volume probe survived (§2); its verdict did not.

**Nothing about the browser has changed. The IP wall is exactly where it was.**

---

## 7. What I got wrong

* **I ran five agents in parallel against a session limit I had not checked**, and lost all five
  mid-flight. The measurements that survived did so because each agent snapshotted to disk —
  which is the only reason this report has numbers at all.
* **I nearly shipped a correct helper with no call site** (§3). Caught by an AST sweep with a
  working control, not by reading the diff.
* **My mutation harness failed its own restore** and would have reported a clean pass on the two
  arms that mattered (§3).
* **My mark-reader probe was wrong before it was right**, and its control caught it (§5).

---

## 8. Safety and spending

**Spend: $0.00.** No vendor call was made by me or by any surviving agent artefact; every figure
above comes from payloads already on disk or from the free embed route. Nothing to book.

**The cap was proven to bind before any page**, by driving `harvest_run.Budget.reserve`: a $0.00
cap **refuses the first call**, a negative cap refuses, the refusal is a raised `BudgetExceeded`
rather than a return value, and **the meter does not advance on a refusal**.

**Backups** taken at round start, sha256-verified with a corruption control that fired both ways,
under a path built from a single round constant. **No seen-store row was removed or altered** —
verified by row key sets with the body found by shape, against a control proving the comparison
can detect a removal: 2,193 / 6,196 / 2,518 / 1,923 / 4,146 rows, **0 added, 0 removed**.
