# BL-1509 — The free filter: what the funnel can decide without spending a cent

**Round:** BL-1509 · **Date:** 2026-09-06 · **Spend:** $0.00 in new vendor calls. Every figure
below comes from payloads already on disk, from driving shipped code with the network poisoned,
or from runs other rounds paid for. The cap was proved to bind before anything started.

---

## What share can be decided free, what that costs, and what stands between him and $1

**Instagram already decides 61.6% of pages for free — 68.0% in memes mode, and 88.3% on the
cleanest recent sample. TikTok decides 24.3%, and its free picture judge buys nothing at all
because it runs *after* the first paid call.** At Instagram's current rate a delivered page
costs about $3.40 per 1,000 on TikTok and the free filter is doing most of the work it can do
with the inputs it has. **The next largest thing standing between him and $1 is not a better
filter — it is that three of the four biggest levers are already built and switched off.** The
free picture judge is configured to ask a *paid* model first; nine free rules are provably dead;
and TikTok's rule engine runs twenty lines after the purchase it could have prevented. None of
these needs new capability. All three need a measurement this round could not finish, and I am
not going to ship a judging change I have not scored on his marks.

---

## 1. What the free filter decides today

Measured on the funnel's own journal — 51,266 rows, 84 runs — with two independent derivations
(reason prose, and presence of fields only a purchased payload can fill) agreeing to **0.00–0.28
points** on every usable cohort.

| brain | n | free rules | free judge | **free total** | needs paid | unjudged pre-pay |
|---|---:|---:|---:|---:|---:|---:|
| instagram (today's funnel) | 3,295 | 31.0% | 30.5% | **61.6%** | 18.7% | 19.7% |
| instagram / memes | 2,588 | 36.4% | 31.5% | **68.0%** | 16.0% | 16.0% |
| instagram / edits | 707 | 11.2% | 26.9% | **38.0%** | 28.7% | 33.2% |
| cleanest IG sample | 231 | 32.9% | 55.4% | **88.3%** | 7.8% | 3.9% |
| tiktok / memes | 218 | 24.3% | 7.8% | **32.1%** | 75.7% | — |
| tiktok / edits | 129 | 10.1% | 3.1% | **13.2%** | 89.9% | — |

**The biggest free rejector on Instagram is a near-tie:** the free vision judge at 30.5% and the
letterbox-bars cover rule at 29.5%, one point apart. Contributing almost nothing: the drawn-cover
gate 1.5%, private-at-discovery 0.8%, and **judge-first at 0.00%** in the modern cohort — 38 hits
in 51k rows lifetime.

⚠️ **On TikTok the free judge is not free, and not because of pricing.** The picture judge runs
at `tiktok_finder.py:3031`; the first paid call is at `:2535`, in the same function. **Verified
by AST, not by report.** So TikTok's 7.8% of free-judge rejections avoid **zero** first calls.
Instagram's 30.5% genuinely does avoid them, because there the judge precedes the purchase.

⚠️ **And the raw corpus will lie to you.** 71.1% of all 51,266 journal rows are "no cover image
was captured" UNJUDGED, and ~3,000 are artefacts of earlier sealed probe rounds. Read straight
off it you get free-rules 5.9% / free-judge 9.0% — a manufactured number. 31 of 84 runs excluded.
`bars_pair_share` is absent from every Instagram journal written before 2026-08-28, so a 0.00%
there is the gate not existing yet, not the gate not firing (control: the same classifier reports
32.9–49.5% on 08-28 runs).

---

## 2. Every free field the vendors already hand over

**409 saved vendor payloads, 19 types, 3 vendors**, found by `os.walk` over 6,405 files and
classified by structural markers rather than filename. The whole tree walked, every dict and every
list element, indices normalised — **no "biggest list" heuristic anywhere.**

- **18,356 type-qualified key paths**, 2,976 distinct leaf names.
- **13,279 unread** by shipped `clippershq/` code.
- 4,486 of those at ≥90% fill — ⚠️ **but only 1,441 actually VARY.**

**That gap is the most important line in this section.** A "100% fill" count treats `0`, `"0"`
and `False` as filled, so roughly two thirds of the high-coverage unread fields are constants that
cannot decide anything. Restricted to fields that are unread, high-fill, **and genuinely varying,
on endpoints the funnel already pays for: 901.**

**Read-by-code was proved by AST, never by grep**: a Subscript with a constant string slice in Load
context, the first constant string argument of `.get/.pop/.setdefault/getattr`, or a constant
string operand of a comparison. A bare string constant is recorded separately as the
grep-equivalent baseline and never counts as a read. **14 of 14 positive controls came back READ**;
3 of 3 negative controls came back UNREAD; and the brief's own control passes — `grep -c "tiles="`
returns 0 while the detector finds it as `_g.get("tiles")`.

### The candidates that could actually decide something

| field | endpoint | fill | why it could decide |
|---|---|---|---|
| `cta_rendering_config.primary_cta_type` | IG hashtag medias | 100% of 1,609 | **`MADE_WITH_EDITS` on 201 (12.5%)** — Instagram itself declaring the reel was cut in Meta's Edits app |
| `original_width` / `original_height` | IG hashtag medias | 100% of 1,923 | free aspect ratio on every post; BL-1500 established aspect discriminates |
| `gen_ai_detection_method` | IG hashtag medias | 100% | the platform's own AI flag — 58 SELF_DISCLOSURE, 2 C2PA |
| `shoot_tab_name` | TT `/v2/search` | 81.2% | photo 564 / video_15 487 / video_600 354 — a free photo-heavy detector |
| `author.ins_id` | TT `/v2/search` | 23.8% | the creator's own Instagram handle — a free cross-platform join key |

### Four "known wins" checked, and three do not survive

- **The TikTok `signature` bio — REFUTED, and it hides a new absence.** It is already read. And
  **LamaTok `/v2/search` has no `signature` field at all** — all 202 leaf names under the search
  author object enumerated across 2,020 authors. The only bio-shaped field is `search_user_desc`,
  median 11 characters. **The bio win does not apply to the search call the funnel leans on
  hardest.**
- **`taken_at` + `play_count` — half confirmed.** Fill is real (`taken_at` 100%, `play_count`
  **97.8%, not 100%**) but "unread" is refuted: both are read. Branch trap worth knowing —
  `items[].taken_at` is 38.3% while `items[].media.taken_at` is 100% on the same payloads.
- **The Instagram embedded JSON — partly refuted.** 90 of 400 records really did extract fields;
  310 claimed `source: "embedded_json"` while extracting nothing (a label bug already fixed).
  **No raw embed HTML is written to disk**, so there is no unparsed blob to mine.
- **The 105-frame filmstrip — FULLY CONFIRMED.** 97.6% of 1,923 medias and 100% of 383, one URL
  per media, 105 tiles on a single sheet. **Zero shipped readers.** Meanwhile `video_strip.py` and
  `frame_pipeline.py` both ffmpeg-*decode* to build the same thing, and both are unwired.

### And a structural finding that explains a lot

**The only free no-model reject rule is `free_judge.his_rules_say(facts)`. It reads exactly three
fields. It is reached only through `classify()`. And `meme_finder.py:7018` calls `should_reject`
directly, never crossing `classify` — so his hand rules have never fired on Instagram at all.**

---

## 3. The nine dead rules — all nine confirmed, each with a control

| # | rule | why it is dead | what reviving buys | kills of his 8–10s |
|---|---|---|---|---|
| 1 | his hand rules (TikTok) | the `_facts` dict carries 8 keys, **none of the 3** it reads | 11 of 112, all from the video-count limb | 1 of 60 (Wilson upper **8.9%**) |
| 2 | talking-head | `speech_fracs = None` literal | unmeasurable — no TikTok speech value exists | — |
| 3 | template-overlay | **same literal**; the OCR guard reads the same variable | 1 of 93 on the only OCR'd corpus | 0 of 9 |
| 4 | share-per-play | sentinel `−1.0`; a ratio of 0.0 never trips it | not scoreable (ratio present on 1 of 876) | **deliberately dead** — it killed 11 pages he scored ≥6, one a 10/10 |
| 5 | short-caption floor | `MIN_CAPTION_CHARS = 0`; a mean is never < 0 | 21 newly rejected of 475 at a 40-char floor | 0 of 6 |
| 6 | IG language gate | key absent from the block **and** all 173 top-level keys | 4 of 475; real value ~8,754 model calls | — |
| 7 | film/TV | computed, never added to the list | **0 of 475** — worthless to revive | — |
| 8 | account recency | `gates["recency"] = True` written literally | **0 of 984** as configured | — |
| 9 | `page_rules.py` | 3 imports repo-wide: 1 test, 2 scratch, **0 shipped** | **150–180 of 475** — the biggest saving | **2 of 6** — and the biggest risk |

**Rules 2 and 3 are one fault.** A single literal at `tiktok_finder.py:2849` kills the
talking-head gate directly and the template-overlay rule indirectly. One assignment revives both.
Rule 2 is dead **on TikTok only** — the Instagram equivalent is wired and measured.

⚠️ **The kill denominators are uneven and must not be quoted flat.** 60 and 87 of his 8–10 pages
join the TikTok corpora; only **6** join the Instagram post-list corpus. Every Instagram bound is
therefore wide — Wilson upper 39–70% on counts of 0–2.

### And his config does not select edits mode

**Both funnels resolve to `memes`, from the config.** Driven through `run_mode.resolve()` with
`env={}` and `argv=[]`; positive control — `CLIPPERSHQ_MODE=edits` and `--mode=edits` both return
`edits`, so the instrument can see a change. **Consequence: every edits-mode rule suspension is
not in force**, and `format_share`, `letterbox_bars` and `no_text_on_cover` all run in their meme
form. The hashtag claim is confirmed (an edits run walks 0 of 9 TikTok and 0 of 11 Instagram
hashtags) but **"zero supply" is refuted** — search survives, so an edits run would be
search-only, not empty.

---

## 4. The facts each brain receives

Verified **on rendered bytes**, which is the distinction the two earlier one-word mismatches
turned on.

**The TikTok brain receives six lines**: handle, display name, followers, biography, post count.
`captions`, `found_via` and `video_posts` **all render when packed** — so their absence is the
packer, not the renderer. Instagram packs captions; TikTok does not.

**TikTok captions are free and already extracted.** `tiktok_finder._video_of` lifts `desc` from
the discovery call the funnel already makes, at **92.3% fill (120 of 130 video dicts, median 87
characters, p90 213)**. It is read by two free rules and never forwarded to the judge. Control:
handle / author_name / sec_uid at 100% on the same 130 objects.

⚠️ **I am not shipping it, and the reason is the round's own rule.** When TikTok facts were last
forwarded and measured, *not one field earned its tokens and the bio was slightly worse.* The
effect must be scored on his marks first — **and it cannot be, from disk.** Captions are extracted,
used transiently, and **never persisted**: of 459 marked-and-scored pages with a grid, captions
exist for **1 (0.2%)**, and the seen store has no caption field at all. Scoring it needs a fresh
fetch, which is a measurement, not a change.

**The `verified` flag is deliberately not packed on Instagram, and that is correct.** The free
extractor does not produce it, and the facts block states what it is given **as fact** — so
packing `False` would report an unchecked page as NOT VERIFIED. **Absent and false are different,
and only one of them is a fact.** This is a finding, not a caveat.

**The Instagram follower spelling-drop is fixed, and the proof cited for it does not exist.** The
producer spells `follower_count`, the renderer spells `followers`, and the bridge now exists at
`meme_finder.py:5321-5323`. Driven end to end: 41,234 renders as `followers: 41,234`, absence
renders nothing. ⚠️ But the fix's own comment cites `scratch/bl1499_facts_render.py` as its
evidence, **and that file does not exist** — this round's drive is the first artefact that
verifies it.

---

## 5. The address-rate lever, priced — and I would not ship it

Carry rate rises monotonically with page size. Second derivation without bands: Spearman
**rho = +0.2969, n=56,919**, against a 200-shuffle permutation null whose maximum |rho| is 0.0114.
**The relationship is real.**

| band | TikTok carry | Instagram carry |
|---|---|---|
| 1–999 | 0.82% (n=11,942) | 23.38% (n=154) |
| 1k–9.9k | 2.30% (n=26,341) | 35.19% (n=233) |
| 10k–99.9k | 8.86% (n=13,389) | 77.85% (n=474) |
| 100k–999.9k | 25.35% (n=3,270) | 92.58% (n=445) |
| 1M+ | 51.51% (n=398) | 97.34% (n=263) |

⚠️ **The five briefed levels (12.5 / 28.9 / 46.5 / 49.0 / 58.1) match neither platform** — TikTok
is 15x lower in the smallest band, Instagram roughly 2x higher in the largest. They came from a
different store with a different denominator.

**Scored on his marks, a follower floor is a bad trade:**

| floor | kills his 8–10s | rate | **Wilson 95% upper** | removes his 1–5s |
|---:|---:|---:|---:|---:|
| 0 | 0 / 126 | 0% | 2.96% | 0 / 52 |
| **500** | **11** | 8.7% | **14.96%** | 3 |
| **1,000** | **20** | 15.9% | **23.25%** | 4 |
| 10,000 | 63 | 50.0% | 58.60% | 16 |

**Median followers: his 8–10s = 9,053; his 1–5s = 18,408. The pages he rejects are BIGGER.** The
highest floor killing zero wanted pages is **3 followers** pooled, **269** on TikTok — both *below*
the floors already in `config.json`. **Four of the pages a 500-floor kills are pages he scored 10.**

**Two reasons not to ship it, either of which is sufficient:**

1. **It is priced against the wrong target.** Follower count predicts whether an *address gets
   published*, not whether *he wants the page*. On TikTok the trade is pure loss — floors up to
   10,000 remove **zero** of his low-scored pages while killing up to 39 of his 8–10s.
2. **On Instagram, where the carry rate would justify it, the free follower value is gone.**
   Pre-wall it was 97.9% available free; **post-wall it is 0 of 310**, with 310/310 login-walled.
   The floor would have to run on the paid call it exists to avoid — **$0.00 saved.**

**What is supportable instead:** use page size as a **ranking key on the paid queue** rather than a
cut. Same ordering benefit, zero pages lost.

⚠️ **And the contact call cannot be dropped, only deferred.** About 51% of Instagram addresses come
from the paid contact button and are provably absent from the bio; that call carries 86% of every
address the funnel has produced.

---

## 6. Before and after — and there is no after, deliberately

**I shipped no judging change, and that is the finding rather than a shortfall.** Every candidate
this round surfaced is in one of three states:

- **Unmeasurable retrospectively.** TikTok captions: 92.3% free fill, never persisted, present for
  1 of 459 marked pages. Scoring needs a fresh fetch.
- **Measured and refused.** The follower floor: real relationship, wrong target, and free only on
  the platform where it does not pay.
- **Blocked on a measurement I could not finish.** `PAID_FIRST` — see below.

The brief says *do not iterate toward a target; if a number cannot be reached, say so with the
arithmetic and name the blocker.* These are the blockers.

### The largest unpulled lever, and why it is not a one-line change

**`free_judge.PAID_FIRST = True`.** Driven on the shipped config, the models actually asked are
`nex-n2-mini` ×2, then `glm-5.3-flash` ×2, then the free chain — **the paid model is asked first
and answers, so the free chain is never reached.** A peer round measured 89 of 89 live calls going
to the paid model.

⚠️ **My correction to that peer's reading:** the free models are not *absent* from the order, they
are asked **last**. Positive control — with `PAID_FIRST=False` the free chain leads.

**The flag was set for a measured reason, and that measurement is now stale.** BL-1418 recorded:
*192 free calls × 3.33 s = 640 s, the entire wall clock of the stage, to reach a paid model
running at 235 calls/min; ox-alpha answered 0 of 96.* **But ox-alpha is dead and gone from the
chain.** The current free models — `minimax-m3`, `dots-3-note-preview`, `nemotron` — have never
been measured in that position. **The decision that makes the free judge paid rests on a chain
that no longer exists.**

The stake: the vision judge is **13% of run spend and 79% of stage work**, already parallelised
4.5x. Flipping the flag trades money for clock, and the clock cost was once the entire stage. That
is a real experiment, not a config edit, and it is the first thing the next round should run.

---

## 7. Corrections — three to my own work, all caught before publication

- ⚠️ **I corrected a published BL-1508 claim.** My cost baseline said the funnel *"buys discovery
  for roughly 1,700 accounts for every one it judges"*. **The ratio is right; the verb is wrong.**
  Those accounts are read **free** from a 15,971-handle seed file. The run made 36 discovery calls;
  at 22–27 accounts each that is at most **972**, so 15,915 is **16.4x more than any paid call
  could produce**. Discovery cost **$0.0249**, not the $10.99 the wrong reading implies. **The
  supply glut is real; the spend glut on discovery is not** — which moves the target downstream,
  onto exactly this round's brief. Found by a peer; arithmetic re-derived here two ways. The
  published report is corrected.
- ⚠️ **My emit-site census was answering a question nobody asked.** I published "159 of 1,699 sites
  (9.4%) raise `UnicodeEncodeError`". **154 of those 159 are the em-dash.** The real answer is that
  **there is no single answer** — it depends entirely on the launch context:

  | codepage | sites that raise | of 1,699 |
  |---|---:|---:|
  | cp1252 (my run's `sys.stdout.encoding`) | **6** | 0.4% |
  | cp437 (a peer's console) | **158** | 9.3% |
  | cp850 | 158 | 9.3% |
  | utf-8 | **0** | 0% |

  Three sessions produced four numbers and every one was correct under its own unstated premise.
  **A codec *name* is family-level and cannot identify a codepage; the module path in the traceback
  is codepage-level and can.** `PYTHONUTF8=1` takes the whole class to zero.

  ⚠️ **And the two codepages are not nested, so "which is worse" has no general answer.** At the
  character level: `U+2500` (box-drawing) is **cp1252-fatal and cp437-safe**; `U+2014` (em-dash) is
  the exact reverse. On *my* site set the non-nesting happens not to bite — 0 sites are
  cp1252-fatal-and-cp437-safe, so there cp437 is a strict superset — but a peer measured 3 such
  sites on a larger set, and the principle holds regardless of which set you look at.

  ⚠️ **And every literal census we ran — my 1,699, a peer's 2,180, a third's 1,261 — is blind to
  the class that actually kills the error reporter.** The failure fires on the **interpolated
  exception message**, not on the format string. I sized the visible part independently: **33 of
  351 `raise` sites carry a cp437-fatal literal** (a peer got the same numerator, 33, against a
  denominator of 323), and the leaders are in the money path. But that still undercounts, because
  the message usually interpolates a runtime value. **The population is not a property of the
  source at all** — no static census can bound it.
- **The pattern, which matters more than either number:** twice in two rounds I took a stated
  figure's *units* on trust — first comparing a decode+OCR constant against a decode-only
  measurement, then inheriting the brief's claim that the em-dash is an offender. Both times the
  arithmetic was fine and the premise was not.
- **My first caption probe returned 0% and I discarded it**, because its control returned 0% too:
  I was walking `run.json` findings summaries that contain no raw video fields at all. A probe that
  cannot see the field returns the same zero as an absence.

### And a coordination failure worth recording

Another session began work under **this round's id** two minutes before I filed a claim.
`claim.py` correctly reported "no path conflicts" — **because they had never filed.** A claim
addresses *files, not sessions*, so an id being worked without a claim is invisible to the only
instrument that could report it. It was caught by three sessions comparing notes, not by any tool.
Their stated cause is the sharpest example of the class: they checked `docs/claims/` — 127
**published** manifests — concluded the id was free, and filed nothing. **An archive answered a
question about the present and did not say it was an archive.** I verified my own files by content
and mtime rather than presence; nothing of mine was overwritten.

---

## 8. Test state, controls, and one repository-wide unblock

**This round shipped no change to any judging rule, threshold, or prompt**, which is the strongest
available statement about verdict movement. The four brief hashes are unmoved from BL-1503's pins.

**Controls run:** the cap was proved to bind **before the first page** (explicit zero, absent key,
declared lifetime ceiling of zero and malformed input all refuse; positive control returns 2.0).
Backups sha256-verified with a corruption control that fires on a single flipped bit. Seen stores
verified by **row key sets with the body found BY SHAPE** — the spotify store reads 1,902 rows, the
value a name-based helper once reported as 3. Every zero in this report carries a positive control
on the same code path, and the two zeros whose controls failed were discarded and are named above.

⚠️ **`docs/FACTS.md` was refusing every commit in the repository**, for all six rounds in flight —
its ledger stamp said `n=25,143` against a live 27,674, a lag of +2,531 past its +2,000 limit. I
re-stamped it from a **single read** of `spend.json` (both the prose table and the machine block,
because stamping them from two reads never converges while peers are billing): total
61.357137 → **62.618426**, typed sum equal to header, **delta 0.000000**. `facts_guard: OK — 35
facts checked.` It will go stale again; with six concurrent rounds the +2,000 limit is about an
hour.

**I did not run the full suite** — five peer rounds were writing to the tree throughout, and a
suite run against a tree six sessions are editing measures nothing attributable. The families my
files touch are unchanged because **I made no production edit**.

---

*Every number here can be re-run from `scratch/bl1509_*`: the field inventory, the dead-rule
census, the free-decision measurement, the follower-floor scoring, and the leak scanner with its
positive and negative controls.*
