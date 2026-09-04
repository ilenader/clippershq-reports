# BL-1497 — He did send them. All four sets are on disk.

**2026-09-04.** Vendor spend **$0.00** — no request left the machine. Cap was $1.50.

---

## HEADLINE: THE PREMISE I WAS GIVEN IS WRONG, IN HIS FAVOUR

I was told the record showed **130 edit pages and no meme set at all**, and asked to find out
whether two sets never arrived or arrived and were never saved.

**Neither. All four arrived and all four are saved.** A presence sweep over **18,610 files**
found **161 of 161 supplied handles still on disk — zero lost.**

| set | count | where | when |
|---|---|---|---|
| TikTok edits | **66** | a scratch handle table | 2026-08-30 |
| Instagram edits | **64** | same file | 2026-08-30 |
| **TikTok memes** | **31** | a scratch URL list | **2026-08-08** |
| **Instagram memes** | **15 + 1 reel** | a prose table in a scratch study | **2026-08-13** |

**Why the record read "130 edits and no meme set" is an asymmetry in what happened after
they arrived**, not a loss:

| set | files holding the WHOLE set |
|---|---|
| TikTok edits | **12** |
| Instagram edits | **11** |
| TikTok memes | **3** |
| Instagram memes | **1** |

The edit sets were re-derived into a dozen downstream instruments each. The meme sets never
left the round that received them, were captured under unrelated round ids in two
incompatible formats — mobile share URLs and prose — and only the edits set was ever given a
name the project reuses.

**He is right that he sent them and right to be annoyed. He is wrong that they are missing.
They are 31 and 16, not 50–100, so if he wants 50–100 per brain that is a real resend — but
not because anything was dropped.**

---

## 1. WHAT I WAS ASKED TO DO

Find his four supplied example sets; build reference material for four brains with both a
want and a reject side; propose four platform- and mode-correct exemplar packs that he
approves before anything ships; verify his edits definition in the brief; and measure whether
it helps.

**Live at filing:** two python processes (one serving a sheet since 2026-09-03) — **neither
touched**; the dashboard port free; two other rounds in flight. **Backups: 8 of 8 sha256-
verified against source**, with seen-store row counts recorded for a publication-time delta.

---

## 2. WHAT SHIPPED

| # | thing | fix category |
|---|---|---|
| 1 | The Part 0 answer: all four sets located, counted, with the propagation asymmetry | — |
| 2 | **26 pages of new reference material**, 245 videos, frame-stripped, both sides | LOCAL (data) |
| 3 | **The approval screen** — he approves every entry; the funnel may propose, never promote | **GENERAL** |
| 4 | A proposal file with **every picture opened and measured per tile** | **GENERAL** (detector) |
| 5 | Two real bugs in my own screen, found only by launching it as he will | — |
| 6 | The comment block that tells the next reader to disbelieve a true finding | LOCAL |

**Nothing under `clippershq/`, `dashboard/`, `config.json`, the ledger, the lead store or any
seen store was modified.** A 640-file fingerprint at start and end confirms it.

---

## 3. WHAT WAS MEASURED

### 3a. The new reference material   [MEASURED]

| | |
|---|---|
| pages built | **26 of 26 ok** |
| videos | **245**, median **10** per page (min 7, max 10) |
| pinned posts excluded | **11** — but see the caveat below |
| bytes downloaded | **341.6 MB** |
| **bytes verified freed** | **341.6 MB — exact match** |
| pages with an undeleted video | **0** |
| work-directory leftovers, found by **listing** the directory | **0** |
| sheet size | 1284×3040 |
| **size as the model would receive it** | **428×760** |

Every video was deleted as soon as its frames were cut and **the delete was verified after**,
per video, not claimed. An independent directory listing of all 26 working folders found **0
non-frame files and 0 bytes**. Free space was re-read before every page (never near the 3 GB
floor). 244 of 244 downloads answered on the third host; **244 of 244 typed `isobmff` by magic
bytes**, never by extension. The no-watermark route was used throughout — the watermarked form
carries a logo parameter and would have burned the handle onto every frame.

⚠️ **THE PINNED EXCLUSION IS ONLY VERIFIED ON 8 OF 26 PAGES.** The pinned flag is present in
the payload on 8 pages; on the other 18 the payload carries no such field at all, so exclusion
there is **NOT VERIFIED rather than done**. Reject-side pages were deliberately drawn from
payloads that do carry it.

⚠️ **THE BUILD IS TIKTOK-ONLY: 20 want, 6 reject, 0 Instagram — and the reason is measured,
not assumed.**

**Instagram is dead on disk.** Every retained Instagram URL returns HTTP 403 `URL signature
expired`. Controlled: **6 freshest posts × 5 header variants = 39/39 403**, while the
identical request shape returns 206 on TikTok. The expiry parameter decodes to **2026-09-02**;
today is 2026-09-04. Instagram serves **one host per post**, so there is no fallback. The two
Instagram brains are **skipped-unavailable, not skipped for convenience.**

⚠️ **AND HIS FOUR SUPPLIED SETS COULD NOT BE BUILT AT ALL.** The retained files hold *derived*
metadata for them — descriptions, one id, attempt records — but **no post payload with a
video URL was ever kept**: TikTok edits **0 of 66**, TikTok memes **0 of 31**, Instagram edits
**1 of 64**, Instagram memes **6 of 15** (and those 7 are dead Instagram URLs). **So the 26
pages built come from his MARKS, not from the pages he supplied.** Building his supplied sets
needs either one paid call per page or the free routes already on record — neither of which
this round's "find them, do not fetch them" rule permitted.

⚠️ **THE REJECT SIDE IS 6 PAGES, NOT 20, AND 6 IS THE CEILING.** Of 478 reject-side TikTok
pages in his marks, **exactly 6 have any URL on disk.**

### 3b. Every proposed picture, opened and measured   [MEASURED, three controls fired]

Calibrated to the builder's real canvas `RGB(24,24,27)`, measured **per tile**:

**32 items across four brains: 16 platform-wrong for their brain, 20 at ≥75% blank canvas,
8 where one cover is repeated inside the grid.**

Blank tiles per 12-tile grid: **10, 0, 10, 10, 0, 11, 0, 9.**

Controls, all planted and all fired: a synthetic 11-blank-tile sheet read 11; a 12×-repeated
cover read 1 distinct tile; a 12-distinct-cover sheet read 12 and not-repeated.

⚠️ **PRIOR ART, CITED NOT CLAIMED: BL-1489 already found this to the decimal.** This round
re-derived it independently. Stating that as corroboration rather than discovery.

### 3b-ii. Two findings that change how his marks should be read   [MEASURED]

**The prior corpus is want-only, confirmed exactly.** 276 pages / 2,303 strips, score bands
**≥9: 131 · 4–8: 145 · ≤3: ZERO**, and mode is `None` on all 276.

⚠️ **AND THE MARK RESOLVER DESTROYS THE BRAIN LABEL.** 2,323 raw mark rows carry
`mode='memes'` across 247 TikTok handles — but after last-keystroke-wins resolution **zero**
pages resolve with a mode, because a later mode-less row erases the provenance.
**Last-keystroke-wins is right for an OPINION and wrong for WHICH SHEET A PAGE CAME FROM.**
Reading mode from the raw rows instead recovers **379 labelled pages**, of which **108 carry
both modes and were dropped rather than guessed**; all 271 unambiguous ones are `memes`, so
the two edits brains have **no cleanly labelled marks at all**. I used that resolver for my
own selection, so this limits my own numbers too.

### 3b-iii. A single-threshold padding test is blind to a third of this corpus   [MEASURED]

Measured per tile on the 244 new tiles, calibrated to canvas grey rather than a `< grey 16`
threshold: **76 of 244 tiles (31.1%) carry more than 5% canvas padding that a `< grey 16` test
reads as ~0** (their padding median 0.4368, max 0.6842), and 5 of 26 sheets would be
under-read wholesale. 131 tiles show the inverse. **The two signals are near-complementary, so
any single-threshold padding detector is structurally blind to about a third of this
material** — independently reproducing the same artefact on pages the earlier measurement
never touched.

### 3c. The comment block — the finding that IS new   [MEASURED]

A shipped source comment tells the next reader that two claims **"MUST NOT BE REPEATED"**.
Both of its instruments were pointed at the wrong object:

| quantity | value | which claim it answers |
|---|---|---|
| distinct grid **files** | **8 of 8** | the comment's — true |
| grids whose content tiles are **all identical** | **2 of 8** | the one it "refutes" — also true |

**Both are true simultaneously.** "8 distinct sha256" hashes the eight *files*; "the same
cover pasted twice" is about repetition *inside* one file. The refutation **could not have
detected the claim however true it was.** Its companion claim, "worst is 16%", came from a
detector counting blank below grey 16 while the builder paints at **grey 24** — and its
all-white control validated a branch the real data never reaches.

The same block also states the pack function "takes neither platform nor mode". **It takes
both**, and both production call sites pass them.

**Three false assertions in one comment, all still shipped, all load-bearing for whoever
reads that file next.**

### 3d. The four briefs, re-verified after the file moved   [MEASURED]

A concurrent round changed that file by 151 lines mid-round. I re-derived all four:

| brain | hash | |
|---|---|---|
| tiktok/memes | `28c05f855e13` | MATCH |
| tiktok/edits | `d43802ad3f9a` | MATCH |
| instagram/memes | `46a1a4d89cbc` | MATCH |
| instagram/edits | `ff1ff0b70cb0` | MATCH |

Negative control: the bare rubric constant hashes `f81c4b39bd4f` and correctly differs from
all four. Sockets blocked at `connect`, **zero bookings**, asserted still blocked at exit.

**The edits brief does read the three named subjects as EXAMPLES, not as the whole list** —
verbatim, *"he named these three as EXAMPLES, not as the whole list"*, followed by *"a subject
outside the three above is NOT a reason to reject."* The list is open.

### 3e. The packs today, driven per brain   [MEASURED]

| brain | exemplars | platform |
|---|---|---|
| tiktok/memes | 8 | 8 TikTok |
| tiktok/edits | 8 | same 8 |
| instagram/memes | 8 | **8 TikTok, 0 Instagram** |
| instagram/edits | 8 | **8 TikTok, 0 Instagram** |

**Four brains, two packs** — the Instagram pair is byte-identical. The wiring to fix this
already shipped in earlier rounds; what is missing is **data**, and the data may not ship
until he approves it.

⚠️ The platform refusal is **real but unreachable in production**: the shipped Instagram call
site never omits the cross-platform fallback flag. **Reporting that fall-through as closed
would be wrong.**

---

## 4. WHAT WAS REFUSED OR NOT DONE

- **The two Instagram brains got no new material.** Retained payloads carried no usable video
  URLs and buying them was not permitted. The largest remaining gap.
- **No exemplar constant was populated.** The screen proposes; **he promotes.** Shipping an
  unapproved pack would be exactly the failure this round exists to prevent.
- **I did not make the empty allow-list refuse.** A peer supplied the measurement behind that
  fall-through — 0 exemplars scored 53.0% against a 65.0% constant-answer baseline — and
  making it raise would take the funnel down. **A settled, tested decision is not mine to
  reverse**, and I have made that mistake twice in recent rounds.
- **No judging rule was added or loosened.** This round changes examples, not rules.
- **Part 4 paired scoring: NOT DONE.** It needs paid calls and the material is TikTok-only.
  Doing it on one platform would produce a number that reads as general.
- **No file held by another round was touched** — not the finder modules, not the config.

---

## 5. WHAT I GOT WRONG

**Two attributions, both wrong in the same direction: I inferred cause from proximity.**

1. **I told two peer sessions that my search agent wrote four phantom rows to his live
   ledger.** It cannot — **no** script in that agent imports any booking path. The real writer
   was a *different* agent's rubric capture, nine seconds after its file was written, four
   rows for four brains. I accepted a peer's process-table inference instead of reading the
   imports I had on disk. Corrected to both.
2. **I treated "no ledger row carries my round id" as an alibi in the previous round** —
   when **no row carries any id**.

**The corrected version is better evidence than the mistake:** that agent had blocked
`socket.socket`, `create_connection`, `getaddrinfo`, `socketpair` and `ssl.wrap_socket` before
any import and asserted them still blocked at exit — **and still booked one row per brain**,
because booking precedes sending and never checks whether sending is possible. Eight bookings
today, **zero packets**, **$0.000712** of fiction. I did not hand-edit them; a concurrent
round is using them as the unforced before-picture of that bug.

**And my own syntax check lied to me once.** A shell pipeline printed "PASS" without the
checker running. I re-ran it with the exit code read and a planted broken file to prove the
checker rejects bad input. **A no-op wearing a fix's name is caught only by a control.**

---

## 6. MONEY AND SAFETY

- **Vendor calls by this round: 0. Spend $0.00.** The video URLs came from payloads already
  bought. Counted by the run's own driver, never from a ledger delta — that ledger is shared
  and three other rounds were writing it.
- **8 ledger rows exist today totalling $0.000712**, all booking-before-send artefacts, four
  from this round's boundary probe. Disclosed, not deleted.
- **Backups 8/8 sha256-verified**, seen-store rows recorded: 2193 / 6125 / 2446 / 3 / 1715.
  **No seen-store row was read, written or deleted by this round.**
- **Disk:** free space re-read before every page; 341.6 MB transited and **341.6 MB verified
  freed**; zero videos remain.
- **No process was killed except my own**, each verified by parentage first. His sheet server
  was untouched throughout.
- **No handle, address or key printed, logged or committed.** Handles live only in local
  scratch files and on his own screen, where he needs them to recognise his pages.

---

## 7. WHAT HE SHOULD DO NEXT

1. **Open the approval screen and grade the 32 proposals.** At his measured pace this is a few
   minutes. Nothing changes until he does — that is the design, not a delay.
2. **Resend the meme sets if he wants 50–100 per brain.** 31 and 16 is what arrived. Sending
   them as a plain list under one name would stop this recurring.
3. **Decide the Instagram material question.** The two Instagram brains cannot be given
   platform-correct examples from retained data. That needs either a small paid fetch or his
   supplied Instagram pages walked once.
4. **The three false sentences in that comment block should go**, before a fourth round
   re-derives the same measurement.

---

## 8. PATHS

```
tools/bl1497_review.py            the approval screen (threaded server, keyboard, refusals)
OPEN_EXEMPLAR_REVIEW.bat          the door -- double-click; no port is ever shown
scratch/bl1497_proposal.py        builds the proposal; three detectors proved first
scratch/bl1497_selection.py       both sides, resolved through the mark reader
scratch/bl1497_sha_object.py      files-vs-tiles: why the refutation could not see the claim
scratch/bl1497_rehash.py          the four briefs re-derived after the file moved
scratch/bl1497_backup.py          the 8/8 verified backup
output/bl1497_agentC_corpus/      26 pages, 245 videos' frames, zero videos left
```

Reproduce:
```
python scratch/bl1497_rehash.py         four hashes + a negative control
python scratch/bl1497_sha_object.py     both controls fire
python scratch/bl1497_proposal.py       32 items measured per tile
```

---

## 9. THE HONEST SUMMARY

He asked a fair question — *"how does he not see it?"* — and the answer is that the system
did see it, saved it, and then never used it. Two of his four sets have been sitting in a
scratch file and a markdown table since early August, one of them as prose.

The material now exists for one platform. The screen that lets him approve it exists and
works. **The two Instagram brains are still empty, and no pack ships until he says so.**
