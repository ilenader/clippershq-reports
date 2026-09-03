# BL-1492 — his approvals were never read, and the reject side of the pack is pages he wants

> **Reading this cold?** This project runs an automated funnel that finds social-media pages
> worth contacting. A vision model — the "judge" — is shown a screenshot of a page and decides
> whether the operator would want it. The judge is given **worked examples**: real pages the
> operator graded himself, some he loved and some he hated. That set is the **exemplar pack**.
> There are four judges — Instagram and TikTok, each in "memes" and "edits" mode.
>
> Creator handles are redacted throughout. Paths are relative to the repository or use
> `%USERPROFILE%`. No port numbers appear.

---

## HIS FILE EXISTS AND IT IS NOT EMPTY. He reviewed **16 pictures** on 2026-09-03 at 13:45 — 8 APPROVE, 8 REJECT, evenly split across both platforms. Four earlier reports still say *"approvals.jsonl does not exist — he has clicked nothing."* They are wrong.

## AND NOTHING READ IT. Measured across **622 `.py` files**: the only occurrences of `approvals.jsonl` in the shipped tree are the writer, a comment, a receipt string and a test's failure message. `clippershq/` had **zero**. Four positive controls fired on the same instrument. **His clicks changed nothing.** They do now.

## ⚠️ FOUR OF THE EIGHT "REJECT" EXAMPLES ON DISK ARE PAGES HE SCORED 8, 8, 8 AND 6. The hand-built edits pack teaches the judge to reject pages he marked WANT — relabelled by the car rule he has since had reversed. Not a wording problem; the reject side is inverted.

## ⚠️ AND FIVE OF THE EIGHT PICTURES TEACHING INSTAGRAM TODAY ARE MOSTLY BLANK. Measured per tile, at both sizes: **7 of 9 cells flat**, in the capture as stored *and* in what the judge receives. **The shrink is not the cause** — the pages really are that empty. The proposed replacement is **0 of 8**.

## ⚠️ THE REVIEW CANNOT SAY WHAT HE MEANT, AND THAT IS MEASURED. Two readings fit his sixteen presses perfectly, and there are **ZERO rows that could tell them apart**. So nothing was promoted. §3.2 has the one question that settles it.

**Money: $0.00. 0 vendor calls**, counted by this round's own counter rather than by the ledger, because one cutting model bills per token and never books a row.

---

# 1. ROUND ID, DATE, AND WHAT I WAS ASKED TO DO

**BL-1492**, 2026-09-03. Asked to read his approvals and make them actually select; to build four
exemplar packs from the pages **he supplied himself**; to measure what each exemplar shows; and
to run his own pages through the current filter.

**Checked before touching anything:** two live Python processes were his review viewer — left
alone, not killed. No dashboard or sheet-server listener, re-checked immediately before every
write under `clippershq/`. One stale claim in the registry, no collision. Backups of the config,
the ledger, the lead store, all five seen stores **and his approvals file**, each verified by
sha256 against its source: **9 of 9**.

**Research first, and it changed the plan.** A round that finished hours earlier had already
shipped an allow-list refusal for this exact defect. I verified it **by driving it** rather than
by reading it — and found it cannot fire (§3.3).

---

# 2. THE TABLE

| # | The thing | Before | After | Proof |
|---|---|---|---|---|
| 1 | His approvals are read by shipped code | **never** | yes | 622-file census, 4 controls |
| 1 | The refusal can fire on a production run | **no** | yes | driven both ways |
| 1 | The mode reaches the pack function | **no** | yes | AST of the shipped file |
| 2 | His supplied pages located and counted | "unused" | **66 + 64 = 130** | re-derived independently |
| 2 | Reject exemplars available, tiktok/edits | unknown | **0** — short by 4 | 4-cell supply table |
| 2 | His marks answering in a second field | **uncounted** | **56 rows / 48 pages** | field census |
| 3 | Reject examples on disk that are his WANTS | unknown | **4 of 8** | joined to his own scores |
| 3 | Shipped IG pictures that are mostly blank | unknown | **5 of 8** | per-tile, both sizes |
| 3 | Anything promoted | — | **nothing** | driven, `usable=False` |
| 4 | His hand-picked pages the filter would reject | unknown | **20 of 66 TikTok** | real filter driven |
| 4 | The subject list | closed, "these three" | examples + recognisability | 4 briefs hashed |
| — | Verdicts moved | — | **none** | control that can see a change |

**Mutation-proved 6 of 6**, with `__pycache__` purged between runs — one mutant was
length-preserving, so the purge was load-bearing rather than ceremony.

---

# 3. WHAT WAS MEASURED

## 3.1 HIS APPROVALS, BY CLASS

```
rows 16   unparseable 0   file sha256 unchanged by every read in this round

               APPROVE   REJECT
   instagram         4        4
   tiktok            4        4

   klass WANTED   : APPROVE 8, REJECT 0     his score on these: min 9, median 10, max 10
   klass REJECTED : APPROVE 0, REJECT 8     his score on these: min 1, median 1, max 1

   pack 'current'         8 rows, ALL TikTok      <- the Instagram pack that was 8-of-8 TikTok
   pack 'proposal_bl1486' 8 rows, ALL Instagram
   one session, 13:45:10 -> 13:45:45.  Notes left: none.
```

He reviewed both the **current** Instagram pack — which is eight TikTok pages, the defect
itself — and a **proposed** Instagram replacement, and pressed the same pattern on both.

## 3.2 ⚠️ THE ONE QUESTION HE STILL HAS TO ANSWER

The viewer's heading reads *"approve or reject each picture"*, and each card announces the role
the picture would teach: *"taught as a page you WANT"* / *"taught as a page you DO NOT want"*.
That admits two readings of the same sixteen presses:

| reading | what APPROVE means | result |
|---|---|---|
| **(a) the picture** | "use this picture in the role its card announced" | **4 wants, 0 rejects** — no pack |
| **(b) the page** | "this page is good / bad" | **4 wants, 4 rejects** — a complete pack |

**The file cannot separate them.** A row that would separate them is a REJECT-slot picture of a
page he **liked**, or a WANT-slot picture of a page he **disliked**. There are **zero** such
rows in the sixteen: every WANTED card carried a page he scored 9–10 and every REJECTED card a
page he scored 1. The instrument had no discriminating case, **by construction of what it showed
him**. (Proved with a control: planting a single discriminating row flips the detector to
`separable=True`, so the `False` is a measurement and not a broken check.)

So the funnel takes reading **(a)**, the conservative one, under which his approvals do not yet
yield a usable pack — and **nothing was promoted**. Promoting an exemplar he did not knowingly
approve is the single thing this whole review exists to prevent.

> ### ⚠️ WHAT HE NEEDS TO DO — ONE QUESTION, ABOUT 30 SECONDS
>
> **For the four pictures shown as "taught as a page you DO NOT want": did pressing REJECT mean
> *"this page is bad — correct, teach the model to reject pages like it"*, or *"don't use this
> picture as an example at all"*?**
>
> If the first, the Instagram pack is complete today and one constant flips.
> If the second, four replacement reject examples are needed and §3.6 says where they are.

## 3.3 THE WIRING — and why the previous refusal could never fire

**Nothing read the file.** Denominator: 622 `.py` files under `clippershq/`, `tools/`,
`dashboard/`, `tests/`. Hits on `approvals.jsonl`: the **writer** (the generated review server),
a comment, a receipt string, and a test's failure message. `clippershq/`: **0**. Positive
controls on the same instrument: `marks.jsonl` 49 hits, `config.json` 327, `spend.json` 195,
`APPROVED_IG_EXEMPLARS` 42 — all non-zero, so the zero stands.

**⚠️ AND THE EXISTING REFUSAL WAS UNREACHABLE.** A `ValueError` was placed inside the pack
function under a comment reading *"a refusal must sit where the untrusted value ENTERS, not one
layer below the code that has already swallowed it"* — and the sole production caller passes
`cross_platform_fallback=True`, which takes the branch that skips it. Driven:

```
_exemplar_pack(platform="instagram")                          -> RAISES
_exemplar_pack(platform="instagram", cross_platform_fallback=True)   <- the shipped line
                                                              -> RETURNS 8, all TikTok
```

Its entire delivered effect on the Instagram path was **one log line**. The check now happens at
the call site, where the run mode is already in scope, and the fallback is taken only when his
approvals are genuinely unusable — a stated condition rather than a constant argument.

**Four brains, two packs.** The pack function took **no mode**, so instagram/memes and
instagram/edits received byte-identical packs, as did the two TikTok brains. It takes one now,
and a per-mode pack is looked up before the platform-level one — so declaring a name is all it
takes to give one brain its own examples. Until such a name exists the result is unchanged,
which is why this moves no verdict.

**Driven, eleven arms, all green** — his approvals read and reported; nothing promoted; every arm
resolving to the identical pack; the refusal reachable; **a control proving the instrument can
see a pack change**; his file untouched; the shipped call site reading approvals by AST; the mode
reaching the pack function; a missing file raising rather than reading as "he approved nothing";
a readable-but-empty file returning a real answer; and the separability claim with its own
control.

**Mutation-proved 6 of 6.** Two survived the first pass and both were real gaps in my own test:
nothing exercised the **missing-file** path, and nothing asserted the **separability** claim the
entire conclusion rests on. Both are arms now — collapsing "I could not look" into "he approved
nothing" would silently empty a pack, and an empty pack measured **12 points below** the
constant-answer baseline.

## 3.4 HIS 130 SUPPLIED PAGES — found, and counted

They are on disk, verbatim, and the count is **exactly what he said**:

```
TikTok    66   distinct 66   duplicates 0      (he says 66)
Instagram 64   distinct 64   duplicates 0      (he says 64)
TOTAL    130                 cross-platform overlap 0
all ten of the seed handles quoted in the brief are present
```

**The parsing traps are real and were avoided:** 32 of the 130 carry a **dot**, 25 an
**underscore**, 4 a **leading digit**. A word boundary is the wrong test because it treats `.`
and `_` as boundaries; the correct rule is that neither neighbour is `[A-Za-z0-9._]` or `@`. None
currently begins with a dot — checked rather than assumed, because a leading-dot handle writes a
hidden file invisible to every glob.

**⚠️ HE HAS NEVER SCORED A SINGLE PAGE HE SUPPLIED.** Against the **448 handle-bearing rows** of
his own graded workbook — 181 Instagram, 267 TikTok, including 141 nines and tens — the overlap
with his 130 is **zero** by exact match, platform-blind match, punctuation-and-case-insensitive
fuzzy match, and a regex over the entire link column. **Not one of those 141 top scores is a page
he supplied.**

That zero is real rather than broken, and the reason is in the workbook's own first line: *"Every
**meme** page YOU personally graded 6 or above."* The 130 are **edit** pages. Two disjoint
populations. The same lookup, same code path, finds **276 of the 448** graded pages in the meme
corpus — so the instrument can find pages when they are there.

**And 129 of the 130 already have pictures on disk** — cover, strip and source video — under
`output/bl1436_tt`, `output/bl1436_ig` and `output/bl1440_strips`. Only one Instagram page has
none, because it has since gone private. **Building the WANT side of both edits packs therefore
costs no capture and no vendor call.** The material was invisible to earlier rounds only because
BL-1436 de-identified the filenames deliberately; the handle-to-file mapping lives in two
answer-key files in `scratch/`.

⚠️ **And none of his 130 has ever been put in front of him in a sheet.** The three edits sheets
he was given were built from funnel discoveries, not from his list. So the pages he supplied have
never been graded *because he was never shown them* — not because he declined to.

**They are positive by construction** — he supplied them as pages he likes. They can fill a WANT
slot and can never fill a REJECT slot. That is the whole reason the shortage in §3.6 exists.

## 3.5 ⚠️ 56 MARKS THAT ANSWER IN A DIFFERENT FIELD

Inside the same sheet files, delivered rows answer in `score` (1–10) and **funnel-rejected rows
answer in `call`** (GOOD/BAD, meaning *"was the rejection right?"*):

| file | `score` rows | **`call` rows** |
|---|---:|---:|
| `output/bl1397_instagram_sheet/marks.jsonl` | 49 | **5** |
| `output/bl1397_tiktok_sheet/marks.jsonl` | 100 | **9** |
| `output/bl1404_tiktok_sheet/marks.jsonl` | 33 | **42** |

**56 raw rows → 48 distinct pages → 47 `GOOD` / 1 `BAD`.** A `GOOD` on a rejected page is him
saying *"yes, drop it"* — a reject exemplar backed by his own opinion. **46 are pack-eligible.**
Every prior inventory keyed on `score` and scored these as `None`, which is why the rejected side
has been reported as "0 of 56 scored ≤2": the score was never the field. It does **not** rescue
the edits cells — all 48 are memes-mode.

⚠️ **And `mark` means two different things across the corpus.** `GOOD`/`BAD` means *"the filter
was right"*, so his want/not-want is `GOOD XNOR judge_verdict`; `WANT`/`REJECT` is a page
verdict. Reading GOOD as "he wants it" inverts every row where the funnel said REJECT.

⚠️ **Mode is written into zero of 1,074 rows.** Only two directory names say `edits`.
"TikTok/edits" is a **directory claim, not a mode he set** — which is why the edits cells are so
thin.

## 3.6 THE FOUR PACKS — and the shortage is not where it was expected

Cuts, declared: **WANT = his score ≥ 6** (his own sheet is "6 or above"), **REJECT = score ≤ 2**.
His 1–10 scores reproduce only 18.5% of the time, so the cut is on want/not-want and is stated
rather than implied. Corpus: 16 mark files, 1,074 raw rows, **793 resolved pages**.

| cell | scored | chrome excl. | reversed-subj excl. | usable | **WANT avail.** | **REJECT ≤2** | **short by** |
|---|---:|---:|---:|---:|---:|---:|---|
| tiktok / memes | 522 | 0 | 2 | 520 | **191** | **235** (+45 from `call`) | — |
| **tiktok / edits** | 30 | 0 | **11** | **19** | **16** | **0** | **4 REJECTS** |
| instagram / memes | 220 | **4** | 4 | 212 | **78** | **113** (+1) | — |
| instagram / edits | 21 | 0 | 2 | 19 | **7** | **10** | — |

**⚠️ This corrects two earlier rounds.** The shortage was expected at instagram/edits ("one
reject short", from a count of 11 images declared in a *leak-declaration* file rather than a mark
corpus). Measured against the actual mark file — 45 rows, 21 pages — instagram/edits has **11
pages he scored 1, each with his own written reason**, and **10** survive every filter. A
separate round had excluded that whole file as a "car/gym/motivation sitting"; page by page it is
anime, news, quotes and creator pages, and only 2 of 21 touch a reversed subject at all.

**It is `tiktok/edits` that has the hole**, and the zero has a passing positive control: the
identical query returns 235 for tiktok/memes and 10 for instagram/edits from the same code path,
and that sheet's own histogram shows the lowest score he gave was **5** — `{5:1, 6:2, 7:4, 8:3,
9:15, 10:5}`. He rejected nothing on that sitting. Its usable denominator also collapses from 30
to 19 because **11 of its 30 pages are car/gym/motivation scored 6–9** — marks the reversal
invalidates.

**The reversed-subject matcher, naive versus boundary-safe**, on 793 pages:

```
naive substring          80 pages
word-boundary regex      20 pages   <- still wrong: a dot reads as a boundary, so it fires
                                       INSIDE handles of the form <car><dot><word>
handle-aware boundary    19 pages   <- the correct test
naive minus correct      61 pages WRONG
pages with NO subject text at all      50   <- the answer is UNKNOWN, not NO
```

Controls fired on 13 strings: `search:car edits` and `motivation quotes` hit; `cartoon network`,
`gymnastics`, `oscar`, `carousel`, `hashtag:cartoonmemes`, and handles that merely *contain* the
letters — a dotted `car.<word>` form, a doubled `carr<word>` form — correctly do not. All 19 real
hits come from `found_via` search strings, not from bios.

⚠️ **The exclusion has a direction.** The reversal invalidates his **high** marks on those
subjects, not his low ones — 12 of the 19 he scored 6–10, 3 he scored 1–5. Dropping the low ones
discards reject exemplars the new rule *agrees with*. The blanket rule is quoted above as
primary; the directional read is carried in the raw data.

**EVERY SLOT'S SOURCE.** Four wants and four rejects per brain. Nothing is promoted (§3.2), so
this is what each pack *would* be built from, named by origin rather than by handle:

| brain | the 4 WANT slots come from | the 4 REJECT slots come from |
|---|---|---|
| tiktok / memes | his marks at **≥6** across `bl1397_tiktok_sheet`, `bl1402/bl1404_tiktok_sheet` — **191** eligible, and his 66 supplied TikTok pages are additionally available | his marks at **≤2** — **235** eligible, plus **45** more where he answered `call=GOOD` on a page the funnel had already dropped |
| **tiktok / edits** | his marks at **≥6** in `bl1427_edits_tiktok` — **16** eligible after removing the 11 reversed-subject pages | ⚠️ **NOTHING. 0 eligible.** His lowest score on that sheet is 5. **This is the hole.** |
| instagram / memes | his marks at **≥6** across `bl1363_sheet_instagram`, `bl1397_instagram_sheet`, `bl1423`–`bl1425` — **78** eligible, and his 64 supplied IG pages are additionally available | his marks at **≤2** — **113** eligible, after removing the 4 wall/age-gate pictures |
| instagram / edits | his marks at **≥6** in `bl1427_edits_instagram` — **7** eligible | his **11 pages scored 1 with his own written reasons**, of which **10** survive every filter |

⚠️ **A caveat carried on the instagram/edits rejects:** their grids sit under unlabelled
directories, so the platform guard returns `None` — which the shipped loader treats as *missing
evidence, not a mismatch*, so they pass. The guard **accepts them but cannot confirm them**.

**Held out, and not drawn from:** `output/bl1380_run/sheet/marks.jsonl` (100 pages, 74 wanted —
this is the "74" behind the published wanted-kill rates) and
`ground_truth/score_marks_tiktok.jsonl` (311 pages — **all 8 shipped pinned exemplars come from
here**, and the "0 of 34 wanted killed" safety claim was measured on it). Holding both out cuts
tiktok/memes reject supply **235 → 63**; Instagram is barely touched (2 of 113). Also excluded:
nine backup files that reproduce their sources byte-for-byte, and four model logs carrying
`agent`/`model_why` fields — one of which scores **100% agreement on 100 rows** purely because
its verdict is `WANT` on every row.

## 3.7 ⚠️ THE PICTURES THEMSELVES — 38 opened and measured

Every detector was first asserted against a synthesised picture whose answer is known — a white
canvas (must read 9 dead cells), nine copies of one tile (must read 8 repeats), nine distinct
tiles (must read 0 and 0). **All controls passed**, so the readings below are measurements rather
than a silent failure to open the files. Blank share is measured **per tile against each cell's
own modal colour**, not against white — a dark-mode grid's empty cell is black. Bytes are
measured through the **shipped encoder at the shipped cap**, `tile_b64(path, 760)`.

**Result A — five of the eight pictures teaching Instagram today are mostly empty.**

```
                                model size   dead   on-disk size  dead
   current_00  WANTED  score 10   215x460      7      465x992       7    the page really is empty
   current_02  WANTED  score 10   215x460      7      465x992       7    the page really is empty
   current_03  WANTED  score 10   215x460      7      465x992       7    the page really is empty
   current_05  REJECTED score 1   215x460      7      465x992       8    the page really is empty
   current_07  REJECTED score 1   215x460      6      465x992       6    the page really is empty
   the other three  current_*                             0    ok
   all eight proposal pictures                            0    ok

   dead at model size but full on disk : 0    <- so the shrink is NOT the cause
   dead in BOTH sizes                  : 5    <- the pages really are that empty
```

Five of these also repeat cells — up to **6 of 9 identical**. So the eight pictures currently
teaching both Instagram brains are not merely the wrong platform: **five are near-blank canvases,
and the emptiness survives at full capture resolution.** The proposed replacement is clean on
every measure, which is a point in its favour independent of §3.2.

**Result B — the hand-built edits pack's reject side is inverted.** `output/bl1429_exemplars/`
holds 22 pictures. Joining them to his own scores:

| picture | his score |
|---|---:|
| `tt_edits_reject_01_car_subject_supercar_showroom` | **8** |
| `tt_edits_reject_02_car_subject_tuned_street_cars` | **8** |
| `tt_edits_reject_03_car_subject_thin_page` | **6** |
| `ig_edits_reject_01_car_subject_single_vehicle` | **8** |

**Four of the eight reject examples are pages he marked WANT**, relabelled REJECT by the car
rule. The other four IG rejects *are* his own 1s. Separately, four of the six `ig_edits_want_*`
pictures come from a **memes** sheet, so the "IG edits" pack is part memes-mode marks. And
`tt_edits_reject_03_car_subject_thin_page` measures **6 dead cells and 5 repeats of 9** — a thin
page taught as a reject for the wrong reason.

**Result C — walls and chrome.** Four Instagram pages in the mark corpus are not pages at all:
one **login screen he scored 10**, and three age gates he scored 10, 9 and 5. He was grading the
page he remembered, not the picture in front of him. Removing them reproduces a prior round's
140→136 exactly, to the row. TikTok has no equivalent: **0 walls in 220 sampled** from 2,883
grids, with a fired positive control (a synthesised login wall).

**Result D — bytes as sent.** Across all 38: **min 1.4 KiB, median 7.8 KiB, max 66.3 KiB**. The
current pack's pictures are the smallest in the corpus (1.4–3.0 KiB) — consistent with being
mostly flat colour, and a second signature of the same defect.

## 3.8 HIS OWN PAGES THROUGH THE CURRENT FILTER

Every rejection is a rule disagreeing with a page **he chose himself**.

| platform | supplied | evaluable | REJECT | rule |
|---|---:|---:|---:|---|
| tiktok | 66 | 66 | **20** | `stale` — all twenty |
| instagram | 64 | 62 | 0 terminal | 15 rule-level disagreements, below |

**20 of 66 — nearly a third of the TikTok pages he hand-picked — would be thrown away for being
old**, on the shipped 152-day cut. The curve on his own choices:

```
62 days  -> 33 rejected      152 days (shipped) -> 20      180 -> 19      365 -> 4      1095 -> 1
```

Re-derived a second way without the judge, from the post dates alone: **20 of 66**, identical.

**Instagram cannot reach a verdict at all.** All 62 evaluable pages return UNJUDGED — 47 of them
purely because the Instagram leg **kept no captions**. Underneath that, 15 rules fired on his own
pages: `photo_heavy` 11 of 63 and `too_few_posts` 4 of 63. Those are named disagreements that
would become rejections the moment captions exist. `photo_heavy` is an **upper bound**: the media
count includes carousel sub-items, so photos are over-counted.

## 3.9 THE SUBJECT RULE — fixed, and scored with a control

The edits rubric named subjects as a **closed list**: *"THE SUBJECTS HE WANTS — he named these
three himself"*, followed by three bullets. A hedge search over all 23,820 bytes — *such as, for
example, e.g., not limited, among others, and more, including but, etc* — returned **0 hits**,
with controls firing.

Its **sister file two files away already phrased it correctly**: *"RECOGNISABLE MAINSTREAM
SUBJECTS ARE A POSITIVE SIGNAL… If you recognise the subject instantly, that is evidence FOR the
page."* That names a **property**; the edits list enumerated the **extension** and closed it with
a count. The fix mirrors the sister rather than inventing new wording.

**What the closed list costs, on his own top pages:** **52.6%** (Instagram, 20 of 38) and
**52.7%** (TikTok, 49 of 93) of his 9s and 10s show a subject outside the three — reproduced two
ways, including against an independent score source with **0 disagreements** across 276 pages.

⚠️ **The number is aggregation-dependent.** Pooling every description of a page into one label
answers a different question — *"does this page show none of the three anywhere?"* — and gives
**10.5% / 11.8%**. Quote 52.6/52.7 as a **tile-level** claim. **Do not say "half his top pages
never touch the three."**

`tennis` appears in **0 of 8,571** handles (6,125 Instagram + 2,446 TikTok), exactly as he
predicted — with `meme` 72, `memes` 125, `anime` 28, `football` 18, `movie` 18 firing as controls
on the same instrument. Also zero: cricket, darts, snooker, rowing, surfing, skateboarding,
fishing, boxing, chess.

**CAR, GYM and MOTIVATION were not loosened.** That is taste, not over-fitting.

**THE CONTROL, at the network boundary — the request body, not a helper's return value:**

```
tiktok/memes      28c05f855e13 -> 28c05f855e13   UNCHANGED   <- the control
instagram/memes   46a1a4d89cbc -> 46a1a4d89cbc   UNCHANGED   <- the control
tiktok/edits      258d5590748b -> d43802ad3f9a   moved, as intended
instagram/edits   eb5bcc28a170 -> ff1ff0b70cb0   moved, as intended
```

All four originals reproduced before the change, with a negative control (two briefs that differ
must differ; the same brief twice must match) — both legs passed. **The edits change did not leak
into either memes brain.**

⚠️ **These four hashes are ALSO pinned in a test, and I did not update it.** `tests/
test_bl1440_frame_strip.py` holds all four as expected values, under a docstring reading *"If a
round edits RUBRIC or an addendum, these move and the round has to say so out loud."* The guard
did exactly its job and went red; I had measured the movement and published it without updating
the pin. The two **edits** pins are now updated with the previous values recorded beside them,
and the two **memes** pins are untouched — they are the control, and a change that moved them
would mean the edit leaked. Because updating a guard's expected value is the easiest way to turn
a real check into a rubber stamp, the update carries its own proof: mutating the edits addendum
by one character makes it red, mutating the memes rubric makes it red, and restoring makes it
green (`scratch/bl1492_pin_still_binds.py`). **The guard still binds in both directions.**

⚠️ **What was NOT done, stated plainly: a paid A/B of judge accuracy under the two phrasings.**
That needs a model run per arm; this round's cap is $1.00, and the last such comparison here was
n=100 unpaired on a since-dead model — the kind of number that then gets quoted for months. The
byte-level control and the offline count above are what this round can honestly claim.

---

# 4. WHAT WAS REFUSED OR NOT DONE

- **Nothing was promoted.** His approvals are read, and under the conservative reading they do
  not yet yield a usable pack. The funnel may propose; it may never promote.
- **No pack was padded to hide the tiktok/edits hole**, and the three reject pictures on disk for
  that cell were **not** reused — they are pages he scored 8, 8 and 6.
- **No judging rule was added or loosened** beyond the subject phrasing, which the brief
  permitted and which is scored above with an unchanged-memes control.
- **No paid A/B** — see §3.9.
- **No seen-store row was written, rewritten or deleted.**
- **His review viewer was left running.** Two live Python processes were his own tool; killing
  them was never considered.
- **The ~806 stale wall pictures were not swept** — named here, not touched.
- **Four sheets whose funnel column is a constant** are kept but flagged: a constant cannot agree
  or disagree, so their independence is **unproven, not proven**. They supply 41 of the
  instagram/memes rejects.

---

# 5. WHAT I GOT WRONG

1. **My handle parser found nothing and I nearly reported an empty list.** I walked the file's
   AST looking for list literals; the handles are stored in triple-quoted **strings**. The zero
   was my instrument, caught because a file whose docstring discusses 130 handles cannot contain
   none. Re-parsed properly: 66 + 64.
2. **A mutant survived because my driver tested the helper, not the shipped call site.**
   Disabling the approvals read *at the call site* changed nothing any arm could see — the exact
   shape of a test that proves the thing it calls rather than the thing that ships. Now read by
   AST.
3. **Two more mutants survived** because nothing exercised the missing-file path or asserted the
   separability claim — the fact the entire "nothing promoted" conclusion rests on.
4. **My mutation harness hard-coded one line ending** and reported "SKIPPED (instrument fault)"
   on two anchors against a CRLF file. It said *skipped*, not *caught* — that distinction is the
   only reason the harness did not silently claim a clean sweep.
5. **My harness then aborted on its own correct mutant**, because it demanded the original text
   be *gone* while one mutant deliberately keeps it behind `if False:`.
6. **I nearly published "5 of 8 pictures are blank" without asking what caused it.** A picture
   dead only at model size is a shrink bug; dead at both is a selection bug. They need different
   fixes, and only the on-disk twin separates them.
7. **⚠️ My own safety check was fail-open, and I published a wrong number from it.** The
   seen-store verifier compared each file's **top-level** keys, so `tiktok_pages_seen.json` read
   as **3** (`pages`, `version`, `updated`) instead of 2,446 — and comparing those three *names*
   would have reported UNCHANGED after every row inside `pages` was deleted. That is the exact
   defect class this round exists to close, in the instrument asserting that no data was lost. I
   had also carried its reading of the Spotify store — **"3"** — into a draft of §6; the real
   count is **1,896**. Fixed by naming each store's row container explicitly rather than
   guessing, and by adding two controls: a deletion must be visible, and the descent must find
   more than a handful of rows. The other four counts were right, and all five stores are
   genuinely unchanged.
8. **⚠️ I REPORTED A SUITE RESULT I HAD NOT EARNED.** I read a partial log — 32 suites of 439 —
   and wrote *"32 of 32 green so far."* The finished run was **15 red of 439**. A prefix of an
   alphabetical run is not a sample of it, and "so far" does not make a premature number safe:
   it gets quoted without the qualifier. The rule is to report the verdict line or nothing.
9. **⚠️ And one of those reds was mine.** The four brief hashes are pinned in
   `tests/test_bl1440_frame_strip.py`, whose docstring says a round that moves them *"has to say
   so out loud."* I measured the movement, published it, and never updated the pin. Fixed, with
   the previous values recorded and a mutation proof that the guard still binds (§3.9).
   **14 of the 15 reds are pre-existing**, established by reverting *only my three files* to the
   commit before this round and re-running all fifteen — 14 fail identically without my change,
   and `test_bl1440_frame_strip` is the single one that flips. I used the working tree rather
   than a clean worktree on purpose: the data files are gitignored, so a worktree without them
   answers a different question.
10. **Three shell heredocs ate backslashes**, twice writing literal newlines into Python string
    escapes. Each was caught by a parse check before the write. Patches are written as files.

---

# 6. MONEY AND SAFETY

**This round: $0.00, 0 vendor calls**, counted by the run's own counter. Every stub **returns** a
well-formed answer rather than raising — a raising stub latches the free gate off after 12
consecutive failures and manufactures false zeros.

**Backups, each verified by comparing sha256 against the source: 9 of 9**, including his
`approvals.jsonl` and a pre-edit copy of the funnel file.

**Seen stores at publication, compared as ROW key sets rather than bytes:** all five unchanged —
TikTok **2,446** · meme **6,125** · clip **2,193** · repost **1,715** · Spotify **1,896**. **No
row was written, rewritten or deleted by this round.** The comparison carries its own control:
removing one row from an in-memory copy must be seen, and the descent must find real rows rather
than wrapper keys. Both fired (§5.7).

**His approvals file:** sha256 identical before and after every read in this round.

**Campaigns SHA, re-verified at publication, both forms:** short `8e02f8d6f6307ae8` **MATCHES**;
compact `7a029ee5447cddd8` **MATCHES**.

**Ports:** re-checked immediately before every write under `clippershq/` — never once at the
start. His review viewer was running throughout on its own port and was not touched.

**THE TEST SUITE, stated in full rather than as a headline.** `tests/run_all.py`, the whole
thing: **439 suites, 10,045 checks, 2,542s — 424 green, 15 red, 19 skipped.** A skip is not a
pass. **Fourteen of the fifteen reds are pre-existing** and are named in the log; I established
that by reverting *only my three files* to the commit before this round and re-running all
fifteen, where fourteen fail identically. The fifteenth, `test_bl1440_frame_strip`, was **mine**
and is fixed (§3.9, §5.9). The suites closest to this round's change are green:
pack/exemplar **3/3**, claims **4/4**, and the drift and preflight contracts **2/2**.

---

# 7. WHAT HE SHOULD DO NEXT — RANKED

1. **Answer the one question in §3.2** — about 30 seconds. It decides whether the Instagram pack
   is complete today or four examples short, and it is the only thing blocking his sixteen
   clicks from taking effect.

2. **Grade `output/bl1442_sheet_tt_edits` — 36 rows, already built, never opened.**
   His measured pace across six graded sheets is a **median 2–6 seconds per mark**, so
   **36 rows is about 2–4 minutes.** Four reject examples are needed.
   ⚠️ **Honestly: it may return zero.** On the only edits sitting he has done he scored **0 of 30
   at ≤2** (Wilson 95% upper bound 11.4%). The **3 funnel-rejected rows** in that sheet are the
   likeliest source — and note those ask for `call` (GOOD/BAD), not a 1–10 score. If it does
   return zero, the honest answer is that tiktok/edits has no reject side and should not ship a
   pack at all rather than ship pages he wants.

3. **The four reject pictures on disk should not be used** (§3.7 Result B). Three are pages he
   scored 8, 8 and 6. Whatever replaces them must come from step 2.

4. **Look at the 152-day staleness cut** (§3.8). It would reject 20 of the 66 TikTok pages he
   chose himself. At 365 days it rejects 4.

5. **Instagram keeps no captions**, so 47 of his 62 evaluable Instagram pages cannot be judged at
   all. Until that changes, the Instagram edits brain has almost nothing to read.

6. **Re-run the review with the wording fixed** so the next set of clicks is unambiguous — the
   card should ask about the picture's *role*, and should include at least one case where the
   page's quality and the slot disagree, so the answer is separable.

**Twelve built-but-never-graded sheets are on disk, 1,322 rows total** — including one of 50 rows
built entirely from the funnel's rejects, which is the only sheet in the project aimed squarely
at the reject side.

---

# 8. FULL PATHS

Relative to the repository root; no absolute paths are published.

**Changed:** `clippershq/approvals.py` *(new — the reader)* · `clippershq/meme_finder.py` ·
`clippershq/edits_rubric.py`

**Instruments, all re-runnable:** `scratch/bl1492_read_approvals.py` ·
`scratch/bl1492_drive_wiring.py` · `scratch/bl1492_mutants_wiring.py` ·
`scratch/bl1492_score_subject.py` · `scratch/bl1492_measure_exemplars.py` ·
`scratch/bl1492_shrink_control.py` · `scratch/bl1492_apply_wiring.py` · and the four sub-agents'
findings under `scratch/bl1492_agent{A,B,C,D}_*`.

**His material, read but never modified:** `output/bl1486_pack_review/approvals.jsonl` ·
`output/bl1426_graded_pages/` · `scratch/bl1436_handles.py` (his 130 supplied pages, verbatim) ·
the 16 mark files listed in `scratch/bl1492_agentC_findings.json`.

**Backups:** `backups/bl1492_<timestamp>/`.
