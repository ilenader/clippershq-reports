# BL-1503 — Two brains, and his own pages wired into them

**Round:** BL-1503 · **Date:** 2026-09-05 · **Spend this round:** see §2, counted by the run's
own call counter (never a ledger delta — `spend.json` is shared with every live round, so a
before/after difference cannot be attributed to one).

---

## 0. His decision, and the thing that was already true

He said:

> "We should just create two brains — meme and edit page — because when I really think about
> it, TikTok and Instagram are basically the same. Obviously similar, not exactly exactly the
> same, but like 90% of it is literally the same."

**The two-brain structure already existed, and that is a measurement, not a reading.** Every
one of the four briefs is an exact concatenation — `built == live`, byte for byte, on all four:

```
memes brief  =  RUBRIC  +  <platform addendum>
edits brief  =  RUBRIC  +  <platform addendum>  +  EDITS_ADDENDUM
```

So `RUBRIC` (2126 chars) *is* the meme body, `EDITS_ADDENDUM` (6624 chars, 6628
UTF-8 bytes) *is* the edit body,
and the two platform addenda are exactly the "small named platform section" he asked for.
There were never four independent brains to collapse — there were two bodies and two platform
blocks, assembled four ways.

He chose **shared body + a named platform block**, and **only the page's own block is sent**.
That choice has a consequence worth stating plainly, because it is what makes this round safe:
a change confined to the edit body **cannot reach a meme brief at all**. The two meme hashes
below are therefore not merely unchanged — they were structurally incapable of changing, and
if one ever moves alongside an edit hash, the concatenation property has broken and the brains
are no longer separable. That would be a much larger finding than a stale hash.

### The two platform blocks, verbatim

He asked to see both. These are spliced into this report directly from the shipped constants,
so this is a copy, not a description. **Every platform-specific line is kept**; none was
dropped, merged or reworded this round.

<details><summary><b>TikTok block</b> — 2792 bytes, sha256[:16] <code>a907b37ab108389b</code></summary>

```text


THIS PAGE IS ON TIKTOK. The rules below OVERRIDE nothing above; they say what he rejects here.

He grades every page 1 to 10 and almost everything he rejects is a 1. These are his own words.

REJECT, AND HE SAYS SO EVERY TIME:

1. AI-GENERATED VIDEO OF ANY KIND. This is the single most common thing he throws away. AI cats,
   AI hippos, AI pigeons, AI horses, AI people, AI celebrity mashups, "brainrot AI", any clip
   whose subject was generated rather than filmed. On TikTok there is no exception and no
   attractive-looking carve-out: if a cover looks even remotely AI-made, reject.

2. REAL ANIMALS AS THE SUBJECT. Cats and dogs above all. This is about SHARE, not a keyword: if
   most of the covers are real animals being animals, reject. A couple of animal clips on an
   otherwise good page is fine -- he kept a page with two of nine and scored it 8. CARTOON OR
   FICTIONAL ANIMALS ARE NOT THIS RULE and are welcome.

3. BABIES AND SMALL CHILDREN as the subject.

4. A PERSONAL PAGE -- the same unknown person appearing across the covers as the subject rather
   than as found footage. Who pointed the camera is the test, not whether a face appears.

5. GREEN SCREEN. A person keyed over other footage, especially the same stranger every time.

6. A PAGE POSTING ITS OWN ANIMATION or its own drawings. A page REPOSTING cartoon clips is
   wanted; an animator publishing their own work is not.

7. LYRICS PAGES -- song words on a background, post after post.

8. MOTIVATIONAL QUOTE CARDS -- "no risk no story" on a wall. A motivational line inside a real
   meme is fine; a page that is nothing but quote cards is not.

9. TALKING HEADS AND PODCASTS. Someone speaking to camera, clipped podcast segments, anyone
   explaining something. If the video is mostly a person talking, reject.

10. SNAPCHAT-STYLE MEMES -- a screenshotted chat or story post as the whole video.

11. PORN or sexual content.

12. INCOHERENT PAGES -- random unrelated posts with no recognisable subject holding them
    together.

13. BURNED-IN TEXT THAT IS NOT ENGLISH, judged across the covers rather than from one.

WANTED -- these are the shapes he scores 8, 9 and 10:

  * BORROWED REAL FOOTAGE WITH A LINE OF TEXT OVER IT. Streamers reacting, celebrities, film and
    TV, sport, gaming. He scored a streamer-reaction page 10.
  * REPOSTED CARTOONS AND GAMES -- SpongeBob, Mario, Godzilla. He scored these 9.
  * EDIT PAGES -- cuts of films, players, characters, set to music. He scored these 8 and 9.
  * SCENERY OR A LANDSCAPE WITH A LINE OF TEXT -- nature, a city, a room, and one relatable or
    sad sentence burned in. He scored this 9 and asked for more of it.

The common shape is footage he did not film, a relatable or funny or sad line burned into the
frame, and NOBODY TALKING TO CAMERA.
```
</details>

<details><summary><b>Instagram block</b> — 3623 bytes, sha256[:16] <code>25abfaf89e663f23</code></summary>

```text


THIS PAGE IS ON INSTAGRAM. The rules below say what he rejects HERE. Instagram is not TikTok
and one rule is exactly inverted -- read rule B before rejecting anything for having no text.

A. A TEXTLESS FIRST FRAME IS NOT A REJECTION HERE, AND THIS IS THE MOST IMPORTANT LINE.
   A clean banner still -- a footballer, a cinematic frame, something aesthetic or apparently
   random -- IS WANTED when the caption fits his pattern: a long caption, often not in English,
   carrying no hashtags. Do not require text on the image. He confirmed this twice while
   grading: "it was the exact same picture across multiple videos and you kept it -- that was
   good." IF THE ONLY THING WRONG WITH A PAGE IS THAT ITS FRAMES CARRY NO WORDS, DO NOT REJECT
   IT. Answer WANT, or REJECT with a confidence below 50 so it gets looked at properly.

B. BUT A PAGE WITH NO BURNED-IN TEXT AND NO BANNER PATTERN IS A REJECT. He scored a football
   page 1 for exactly this: "it's not meme style, I want to avoid this." The difference from
   rule A is REPETITION AND INTENT -- a banner page repeats one deliberate still; a no-text
   page is just clips with nothing written on them.

REJECT:

1. AI SLOP. Anything generated rather than filmed. He scored an AI panda 1 -- "what the fuck
   even is this".
   ITS COMMONEST FORM IS AN AI-GENERATED ANIMAL COUPLE, AND IT IS THE SINGLE MOST COMMON THING
   HE THROWS AWAY: TEN OF FIFTY PAGES ON ONE SHEET, EVERY ONE SCORED 1. Guinea pigs, penguin
   couples, lemon couples, cat couples. His own description was "a man and a woman but they are
   animals" -- a couple acting out a domestic routine, rendered smooth and plasticky in 3D, the
   same two characters in every frame.
   THIS OVERRIDES THE CARTOON CARVE-OUT IN RULE 5. "Cartoon animals are always fine" means
   HAND-DRAWN OR STUDIO animation the page did not make -- Tom and Jerry, Spongebob, a clip from
   a film. AN AI-GENERATED ANIMAL IS NOT A CARTOON. It is rule 1 and it is a REJECT.

2. PAGES SERVING AN INDIAN OR PAKISTANI AUDIENCE. He scored three of these 1: "our target
   audience isn't that". THIS IS ABOUT THE AUDIENCE THE PAGE SERVES, not the script a caption
   happens to be written in -- read the handle, the display name, the people and places in the
   frames, and the language of the burned-in text.

3. CREATOR PAGES -- the same unknown person across every video, filming themselves. The test is
   WHO POINTED THE CAMERA. Borrowed faces are fine; a person vlogging their own life is not.

4. SHIT PAGES -- random incoherent posting with no format holding it together.

5. REAL ANIMALS OR REAL BABIES AS THE SUBJECT, BUT ONLY ABOVE ABOUT 30% OF THE FRAMES. HE SET
   THIS THRESHOLD HIMSELF: he scored a page 8 that had one dog and one baby among nine, because
   the majority was cartoon and celebrity. CARTOON ANIMALS ARE ALWAYS FINE and are not this
   rule. Do not reject a page for one animal.
   AI-GENERATED ANIMALS ARE NOT THIS RULE AND ARE NOT THE CARVE-OUT -- they are rule 1, a reject.

6. BURNED-IN TEXT THAT IS NOT ENGLISH. English only ON THE IMAGE. CAPTIONS ARE A DIFFERENT
   THING and Japanese or Chinese captions are FINE -- see rule A, his best banner pages are
   Japanese-captioned. Spanish and Indic burned-in text are rejects.

HE WANTS -- and RECOGNISABLE MAINSTREAM SUBJECTS ARE A POSITIVE SIGNAL, NOT A NEUTRAL ONE:
Spiderman, the Avengers, Ryan Gosling, Sydney Sweeney, cartoons, famous footballers, well-known
films and games. He scored an obscure horror page only 5 and said why: "I want more RELATABLE
and KNOWN." If you recognise the subject instantly, that is evidence FOR the page.
```
</details>

A shipped guard, `test_neither_platforms_rules_reach_the_other`, asserts that nothing past the
shared preamble in one platform's brief mentions the other platform. **It caught my own first
attempt this round** — see §7.

⚠️ **A NOTE ON HOW THAT GUARD HAD TO BE BUILT, because two other rounds independently tried the
obvious version and it cannot work.** A control on the bare words "TikTok" and "Instagram"
**cannot fire**: each word appears in all four briefs, and so does "CONTACT SHEET". The check
has to be built on whole LINES. Measured on the live briefs, under the rule *"present in both
of that platform's briefs and neither of the other's"*: **36 TikTok-only lines and 43
Instagram-only**, and **0 cross-platform lines in any of the four** — which is the invariant
that matters. A peer measured 35/41 with a >25-character filter, and I quoted 34/41 from an
older round without re-measuring; all three are the same guard under different rules, which is
exactly why the rule belongs beside the number. Their filter also turned out to be masking a
false positive of their own: a substring test matched the 9-character fragment `together.`
inside Instagram prose, and the length filter had been silently suppressing it.

⚠️ **AND A TRAP LEFT IN PLACE DELIBERATELY, recorded here because the fix belongs to whoever is
next in that file.** In `meme_finder`, `_cols = min(_tiles, 3) if _single else 3` computes a
value that, on the composed-sheet path, **nothing reads**: `_cols` is passed as `page_cols`, and
`free_judge._messages` consumes it only when `single_video` is true, which requires
`1 <= _tiles <= 2`. Two separate rounds read that assignment and concluded the funnel was
cropping composed sheets. It is not: measured over every `capture_manifest.json` on disk,
**3,292 Instagram capture records — 96.5% take the whole sheet, 3.5% take the crop**, and that
3.5% genuinely is one or two covers. A computed value nothing uses will keep producing that
inference until it carries a comment saying so. I have not added one, because another round is
mid-edit in that file and a comment is not worth a merge conflict for them.

---

## 1. The four briefs, and what moved

| brain | before | after | |
|---|---|---|---|
| tiktok / memes | `28c05f855e13c9c2` | `28c05f855e13c9c2` | **control — must not move** |
| instagram / memes | `46a1a4d89cbc6fa3` | `46a1a4d89cbc6fa3` | **control — must not move** |
| tiktok / edits | `d43802ad3f9a1ee2` | `cf4f13aa6e5023ee` | moved, deliberately |
| instagram / edits | `ff1ff0b70cb0c873` | `dcdeabb170e73783` | moved, deliberately |

Measured at the payload, not at the constant: the hash is taken from the text `_messages`
actually places in the request body.

**The pin guard was mutation-proved, both ways.** Mutating the edit body turns exactly the two
edit brains red and leaves both meme brains green; mutating the shared body turns all four red;
mutating the Instagram platform block turns only the two Instagram brains red. A guard that
cannot go red is not a guard, and this project has a recorded case of a whole rubric being
replaced while four assertions held.

**Only `EDITS_ADDENDUM` changed** — 5161 → 6624 characters (+1,463), or 5,161 →
6628 UTF-8 bytes (+1,467). ⚠️ **The two figures differ and the difference is not a defect:**
the new text contains two non-ASCII characters (a warning sign and its variation selector) at
three bytes each. A peer round and I read 6,624 and 6,628 off the same clean file and spent a
round-trip on it before noticing we were quoting different units — so this report states which.
`RUBRIC`,
`TIKTOK_ADDENDUM` and `INSTAGRAM_ADDENDUM` are byte-identical to the committed versions, which
is the two-brain claim proven rather than asserted.

### The paired score

**n = 100 of his own graded pages, 240 calls, $0.0214** — same pages, same order, same
exemplar pack, same model chain, same threshold. The only difference between the arms is
`EDITS_ADDENDUM`, and each arm's briefs were hash-checked at run time against the pins above,
so the "old" arm really is the old brief. **0 pages went unjudged in either arm** (a model
error is an abstention here, never a rejection).

|                | new KEEP | new CUT |
|----------------|---------:|--------:|
| **old KEEP**   | 44 | 11 |
| **old CUT**    | 9 | 36 |

**20 of 100 verdicts moved** (95% Wilson [13.3%, 28.9%]). **McNemar exact, two-sided:
b = 9, c = 11, p = 0.824 — no detectable direction.** So his definitions are *not* a no-op:
they change the answer on one page in five. What they do not do is push systematically toward
keeping or toward cutting.

**The kill test — pages HE scored 9 or 10 that the brief throws away.** This is the metric that
matters, and it needs no mode assignment: a page he scored 9 or 10 is a page he wants, full stop.

| | n | old cuts | new cuts |
|---|---:|---|---|
| pages he WANTS (score ≥ 9) | 50 | 13 &nbsp;[16%, 40%] | **13** &nbsp;[16%, 40%] |
| pages he does NOT want (≤ 2) | 50 | 32 &nbsp;[50%, 76%] | **34** &nbsp;[54%, 79%] |

**Newly killed: 4. Newly saved: 4.** Exactly balanced, and the total on his wanted pages is
unchanged at 13. The new-kill rate is 4/50 with a 95% upper bound of **18.8%** — which is the
honest limit of what 100 pages can tell you, and I am not going to dress it up as a clean bill
of health. With 20 discordant pairs this is underpowered against a small directional shift;
what it does rule out is a large one.

**Read plainly:** adding his own words moves a fifth of the verdicts, in no particular
direction, and costs nothing measurable on the pages he wants. That is the account of the
movement the round was asked to produce — not a claim that the new brief is better, which this
sample cannot support either way.

⚠️ **Confound, named on every accuracy figure this round produces, and not re-tuned here.**
`REJECT_AT = 80` was calibrated while the delivered picture was 155×275. BL-1499
changed the delivered picture to 356×760 — 6.3× more of the page. Every threshold in the gate
was therefore set on a *different picture* from the one now being judged. Re-tuning it belongs
to its own round; this one must neither move it nor pretend it is not there.

---

## 2. His examples, wired — and the trap found on the way

### What is now wired

Four packs, one per brain, built from **the ~200 accounts he sent by hand** — one list labelled
MEME, one labelled EDIT. In his words: *"I chose every one of them myself, I looked at them
myself, and they are approved by the fact that I sent them."*

| brain | full sheets available | picked |
|---|---|---|
| tiktok / memes | 20 | 4 |
| instagram / memes | 12 | 4 |
| tiktok / edits | 45 | 4 |
| instagram / edits | 55 | 4 |

Selection rule, so it can be re-derived rather than trusted: of his sheets for that
(platform, list), the ones whose grid came back **full** (`cells_used == cells`), sorted by
shipped name, first four. Recorded in `scratch/bl1503_pack_selection.json`.

**Every brain gets its own platform's pages.** All 156 of his sheets read their own platform
correctly off their own path — 156 agree, 0 disagree, 0 unreadable — so the BL-1471 defect
("the Instagram pack is 8/8 TikTok") cannot recur here, and the existing platform guard did not
have to be weakened to make room for his material.

**The pack is keyed by sheet stem, not by handle, and that was load-bearing.** `_grid_index`
keys on a PNG's basename stem; his sheets are named `<list>_<platform>_<digest>.png` so no real
creator handle is committed to a public repository. Measured: of his 156 sheets, **5 resolve by
handle and 156 resolve by stem**. A handle-keyed pack would have loaded 3.2% of itself and
looked perfectly wired.

### ⚠️ The documented extension point was a trap

BL-1492 added a per-mode pack lookup and wrote the instructions for using it: *"declaring
`APPROVED_IG_EDITS_EXEMPLARS` is all it takes to give one brain its own worked examples."*

**Follow those instructions and you get an empty pack.** A pack declared `"instagram/edits"` is
compared against a caller asking for `"instagram"`, so `declared != want` was true for every
entry and the enforcement loop refused the whole thing. Driven, not read — four of his own
TikTok edit sheets, declared exactly as instructed:

```
RESULT: pack returned 0 of 4 entries
   REFUSED edit_tiktok_37840cf0fe -- APPROVED_TT_EDITS_EXEMPLARS declares platform
                                     'tiktok/edits', caller asked for 'tiktok'
   ... x4
```

It had never fired because **no key in the table contained a `/`**, so the branch was
unreachable. The first person to follow the documentation would have got zero exemplars — and
zero exemplars at the live call site is the arm measured at **53.0% against a 65.0%
constant-answer baseline**, delivered as one log line. Fixed by `_declared_platform`, which
reads the platform half of a declaration; regression-tested and mutation-proved.

### ⚠️ The landmine, defused

The live call site chose between two `_exemplar_pack` calls on
`_approvals_state("instagram")["usable"]`. **The `True` branch — the one that fires the day he
approves a pack — omitted `cross_platform_fallback`**, which makes that call raise; the raise
was caught by the enclosing `except Exception` and turned into `_fj_pack = []`. So *the success
path was the failure path*: the day his approval finally landed, the pack would have silently
emptied into the 53% arm. It could not be noticed because `usable` was `False` on every run
ever made. There is one call now, and no branch nobody has driven.

Separately, that `except` handler now **turns the free judge off** for the run instead of
carrying on with no worked examples. Describing the worse condition in a log line for three
rounds is not the same as declining to enter it. A judge that cannot be given its examples does
not judge — nothing is rejected on that run, which is the direction that cannot cost a wanted
page.

### The 16-card approvals file is superseded

He ruled it out: *"Those 16 cards came from my marks, picked by an earlier round. Forget them
… The old 16-card approval file is dead. Do not read it, do not act on it."*

**Nothing in the shipped tree reads it any more.** `_approvals_state` is gone, replaced by
`_pack_state`, which reports the state of *his own lists*. `clippershq/approvals.py` is left on
disk — it is what `tools/exemplar_review.py` is built on — but it is now orphaned, and a test
asserts both that it is the only remaining reader **and** that nothing imports it, with a
positive control proving the detector can actually see a read. `APPROVED_IG_EXEMPLARS`, the
pack an earlier round built *out of his marks*, stays permanently empty for the same reason.

### The TikTok side could not tell its two brains apart at all

`tt_exemplar_pack()` took **no arguments** — its signature was literally `()`. The TikTok meme
brain and the TikTok edit brain could not be handed different examples even in principle, not
because a pack was missing but because there was no argument through which one could ever be
selected. It now takes `mode`, the live call site passes it, and both the acceptance and the
divergence are mutation-proved.

---

## 3. His definitions, in the edit body

Six things he said about an edit page were in **no brief**. All six are now in
`EDITS_ADDENDUM`, and therefore in both edit brains and neither meme brain:

1. **Fast-paced, lots happening at once, cuts on the beat.**
2. **Text is small and inside the video**, over the footage — not a bar across the top.
3. **Sometimes dialogue between two people with their words on screen** — the words belong to
   the people in the footage, not to a meme caption.
4. **Sometimes no text at all.**
5. **Sometimes motion graphics.**
6. **The photo-carousel carve-out, kept narrow:** a slideshow of stills swiped one after
   another is a **reject**; photos that *move* inside a video are fine. A still that is panned,
   zoomed, cut to the beat or composited into an edit is edited footage, not a slideshow.

Plus his wider subject examples — basketball and sport generally, money, religious, country,
history, streamers, reality shows, named people — stated explicitly as **more examples and
still not a closed set**, because over half of the pages he scored 9 or 10 have a subject
outside the three the brief used to name.

**Cars are a query rule, not a page rule**, and no car rejection was added to the judge. No
threshold was moved and no judging rule was added or loosened beyond the text he specified.

---

## 4. The facts each brain receives

Verified on **rendered bytes**, by driving `facts_block` one field at a time — not by reading
the packer, because a key the source mentions may still render nothing.

The follower fix is real and behaves correctly at the edges: `12345` and `"12345"` both render
`followers: 12,345`; **`0` renders** (a real observation); absent and `None` are **omitted**,
because "nobody looked" must not read as "they have none".

`verified` renders `yes` / `no` only when it is an actual observation, and is omitted when
`None`. **Instagram deliberately does not pack it, and that was left alone.**

What the renderer can show, against what Instagram actually packs:

| field | renders? | packed on Instagram? |
|---|---|---|
| `handle` | yes | **yes** |
| `full_name` | yes | **yes** |
| `biography` | yes | **yes** |
| `captions` | yes | **yes** |
| `found_via` | yes | **yes** |
| `followers` | yes | **no** |
| `verified` | yes | **no — deliberate, not a defect** |
| `posts` | yes | **no** |
| `video_posts` | yes, alongside `posts` | **no** |

So the Instagram brain receives 5 of the 8 fields its own renderer can show. `followers`,
`posts` and `video_posts` are **candidates, not fixes** — the instruction is to measure a
field's effect before adding it, and this round measured none of them. They are named here so
the next round has a list rather than a hunch.

*(Two entries in my first pass — `handle` and `video_posts` "render nothing" — were artefacts
of my own probe baseline, not findings. Corrected above.)*

---

## 5. What is still missing, and exactly how short

**The reject side of all four packs.** A worked-example pack teaches by *contrast* — four pages
he wants and four he does not. He supplied the want side. The reject side has to come from
pages he scored low, and it has not been supplied.

So **all four packs are held back**, and the funnel serves exactly what it served yesterday.
That is stated in the run log every time, not swallowed:

```
HIS pack HIS_TIKTOK_EDIT_PAGES HELD BACK: 4 want, 0 reject -- a pack teaches by contrast
and the reject side is short by 4. Serving the existing pack unchanged rather than making
an unmeasured swap.
```

The day a reject side lands, all four promote themselves. That path is **not dead code**: a
positive control completes one pack synthetically and asserts it promotes, and the mutant that
jams the gate shut is caught.

### Could I build the reject side from his existing marks? Not honestly.

A census of his grading (**12 mark files, 683 rows, 537 distinct pages after last-keystroke-
wins** — reproduced independently twice, by me and by a sub-agent, with identical row and page
counts) says the count is *nominally* there:

| threshold | MEME rejects | EDIT rejects |
|---|---|---|
| score ≤ 2 | 8 | 10 |
| score ≤ 3 | 8 | 11 |
| score ≤ 5 | 9 | 13 |

**But every one of them fails a provenance test, and I am not shipping them.**

1. **The picture is not the page he graded.** `_grid_index` is newest-wins across all of
   `output/`. For **18 of 18** mode-assignable low-scored pages it hands back a photograph
   taken by a *different round* — `bl1350_grids` (9), `bl1415_grids` (8), `bl1428_grids` (1) —
   never the sheet he actually marked. An exemplar built from these shows the model a picture
   he never graded, wearing his grade.
2. **"MEME" and "EDIT" here mean the run's mode, not the page's content.** No page was assigned
   a brain by looking at it. A page rejected during a meme run is not thereby a meme page.
3. **Only 8.5% of his low-scored pages can be assigned a brain at all** — 18 of 211 at ≤2.
   The other 193 live on sheets that record no mode anywhere.
4. **Provenance warnings travel with the source.** All the EDIT candidates come from
   `bl1427_edits_*`, which the mark reader itself flags as superseded; all the MEME candidates
   come from one sheet carrying a `DO_NOT_USE_THIS_SHEET.txt`.

He said: *"if you cannot build it, say how short you are rather than filling it with something
else."* **I am short 4 reject examples on each of the four brains — 16 in total** — and the
material on hand cannot fill them without putting a mislabelled picture in front of the model.

⚠️ **AND POINT 1 MAY STOP BEING TRUE, WHICH WOULD CHANGE THIS ANSWER.** A concurrent round
(BL-1505) is replacing `_grid_index`'s selection rule for an independent reason — three of his
10-scored pages resolve to thin 27–119 KB captures while full 12-tile sheets of the same
handles sit on disk at 308–489 KB. It is the same defect measured from the other end, and my
18-of-18 is the stronger statement of its scale: **3,030 of 11,157 stems under `output/` have
more than one PNG**, worst case 156 copies of one stem, so the tie-break is live across a
quarter of the index rather than at three files. I have handed that function over to them and
confirmed first that **0 of my 16 pack entries are ambiguous**, so no tie-break rule can move
them. **If their rule lands, the reject side may become buildable and this shortfall should be
re-measured rather than re-quoted.**

One constraint I passed to them and record here because it is easy to undo by accident:
BL-1419 changed this rule *from* "largest file wins" *to* "newest wins" deliberately, because a
bigger PNG is usually a photograph of the account when it was at its busiest — often years
stale — so size-preferring reached back through history and defeated the point of running the
camera immediately before the walk. "Richer sheet" is close enough to "larger file" that a
naive implementation reintroduces exactly that.

### A smaller thing I refused to invent

`free_judge` renders an exemplar's score straight into the prompt as *"he scored this X of 10"*.
He never scored the pages on his own lists — he **sent** them. Writing a number there would put
a grade in his mouth that he never gave and quote it to the model as his word. Unscored
exemplars now carry `score = None` and render *"he picked this page out himself as one he
WANTS."* instead.

The same change fixes a caveat that was about to become a lie: the edits brief tells the model
*"these were graded while he was looking for MEME pages … do not trust the scores."* True of the
old pinned pack. **False, and harmful, about the edit pages he chose by hand** — it would
instruct the model to distrust the very examples he picked for this mode. The caveat now follows
the *pack* (is anything in it actually scored?) rather than the mode, so it cannot be attached
to his own material.

---

## 6. His three questions, answered

**Are there two brains now?** Yes — and there already were, structurally. There is one meme
body and one edit body, plus a named platform block, exactly as he chose. What changed is that
the edit body now contains his own description of an edit page, and that only the page's own
platform block is sent.

**Does each brain have its own examples?** The wiring exists and is proven for all four; the
material is **half there**. Each brain has its own four *want* examples, drawn from his own
lists and from its own platform. None has a *reject* side, so none is switched on yet.

**What does he still need to approve — how many, where, how long?** Nothing to *approve*: he
has already said the lists are approved by his having sent them, and this round does not ask
him to re-review anything. What is needed is **material, not permission**: **16 pages he does
not want — 4 for each of the four brains** — ideally sent the same way he sent the others, as
plain lists labelled by mode. That is the single thing standing between the packs and going
live. If he would rather they come out of his existing low scores, that is a decision he can
make, but it should be made knowing points 1–4 in §5 — and knowing that point 1 is actively
being worked on by another round.

⚠️ **One thing he may be expecting that has not arrived**, flagged because it bears on what he
sends next: BL-1505 reports that a resent MEME list — one plain labelled list, expected around
108 accounts — is not on this machine, established by searching for the specific handles rather
than for anything list-shaped, with the needles proving the instrument. **That is their finding
and their report, not a measurement of mine.** What I verified is only that it changes nothing
here: nothing in this round is sized against 108. The packs take four per brain from whatever
full sheets exist, and the meme material on disk is 25 TikTok and 12 Instagram sheets from his
original 46.

---

## 7. Corrections, and what I got wrong

- **The cross-platform guard caught my own change.** My first attempt justified the wider
  subject list with *"52.6% of his Instagram 9s and 10s and 52.7% of his TikTok ones …"* — a
  sentence naming both platforms inside a body that ships to both, so the Instagram brief was
  leaking TikTok wording. The fix was not to widen the guard. It was to stop citing our own
  measurements in a brief at all: **a brief instructs the model; the evidence for it belongs in
  this report.** The hashes moved a second time as a result, and both pinned tests were
  re-pinned deliberately.
- **My first mutation proof fired on zero brains.** I mutated `free_judge.RUBRIC`, but
  `rubric_for` delegates to `edits_rubric`, so the re-exported name is never read. A mutation
  run that catches nothing is indistinguishable from a guard that works; corrected by mutating
  the module that is actually read.
- **My first pass at his marks used the wrong corpus.** `mark_reader.discover()` sniffs the
  whole repo and returned **5,919 files / 193,705 rows / 20,515 pages** — seen stores, rejection
  stores and config backups, i.e. the funnel's own memory, which last-write-wins then lays on
  top of his actual grading. Restricted to the `marks.jsonl` files inside delivered sheet
  directories it returns **12 / 683 / 537**, matching the independent census exactly. The
  pooled corpus has produced a wrong answer in this project before; it nearly did again here.
- **Two probe results in §4 were artefacts of my own baseline**, not findings, and are corrected
  in place rather than left standing.
- ⚠️ **My own attribution harness deleted this round's work from the working tree.** It held
  the six original files in process memory and restored them in a `finally`; a two-minute
  default timeout killed the process first, and all six were left reverted to `HEAD`. Recovered
  in full and proved byte-exact by hash, not by eye — `EDITS_ADDENDUM` back to 6,624 B and all
  four brief hashes matching. **What made recovery possible was that most of the changes were
  scripted patch files that replay onto HEAD; what nearly lost it was that his six definitions
  had been edited by hand and existed in exactly one place.** They are scripted now, as is the
  re-pinning. The rerun snapshots to disk *before* touching anything.
- ⚠️ **And that same window nearly put a false claim in this report.** This report is generated
  from the live modules on purpose, so the platform blocks are a copy rather than a description
  — which means it will faithfully describe whatever is on disk. Run while the files were
  reverted, it produced a version stating `EDITS_ADDENDUM` was 5,161 B with the **old** hashes
  in the "after" column: a published claim that nothing moved. It was caught by reading the
  output, which is not a control, so the generator now **refuses to write** unless all four
  briefs hash to this round's values. Note that file size did not discriminate — both versions
  are 28,316 bytes, because the differing numbers happen to be the same width.
- **I mislabelled a red as mine and am correcting it here.** The one-shot A/B above reported
  `test_song_examples` GREEN on HEAD and therefore "MINE". It is green **with** my changes too
  — 4 runs, including through the runner, 48 checks. Its full-run red took 12.1 s against a
  normal 19–28 s, i.e. it was cut short. **A single-run A/B cannot attribute a non-deterministic
  test**, and I should have re-run it before assigning blame.
- **Earlier this round I passed two wrong claims to peers and have withdrawn both:** that
  `if want == "instagram" and APPROVED_IG_EXEMPLARS:` was live code (it survives only inside a
  comment quoting history; BL-1489 replaced it), and that his meme-side media no longer existed
  (true of retained payloads only — a fresh fetch returned 9/9 HTTP 200).

## 8. Test state

`tests/test_bl1503_his_own_packs.py` — **20 checks, green.** Every guard in it was
mutation-proved: eight mutants across `meme_finder`, `free_judge` and `tiktok_finder` were all
caught, and a control mutation that changes only a comment correctly stays green. All files
were restored byte-for-byte afterwards, verified by sha256.

⚠️ **I DO NOT HAVE A COMPLETE FULL-RUN VERDICT LINE, AND I AM NOT GOING TO IMPLY ONE.** Three
attempts to run the whole tree were cut short — the first by my own 3,000-second timeout, the
next two killed. The furthest reached 249 suites of the tree before stopping. A partial run is
not a result, and this project has published a wrong number from a tidy partial before.

What I have instead is per-suite evidence, which for attribution is stronger than one line:

**Every suite touching the files this round changed is green** — `bl1503` (20 checks), `bl1440`
(13), `bl1499` (7), `bl1447` (13), `bl1486` (12), `bl1471` (6), and the TikTok group 7/7 (187).

**Every red observed across the partial runs has been attributed by driving, not assumed.** All
six files this round touches were reverted to the committed `HEAD` and each red re-run:

- **14 were already red without my changes** — `bl1307_veto_refused`, `bl1308_refuted_brief`,
  `bl1350_gates`, `bl1359_ig_cost_fixes`, `bl1389_no_caller`, `bl1400_ordering_and_third_state`,
  `bl1444_board_and_sheets`, `dashboard`, `dashboard_redesign`, `doc_citations`,
  `estimated_flag`, `meme_finder`, `send_list_rebuild`, `silent_zero_shape`. Two of them fail on
  `scratch/bl1441_ast_sink_tests.json`, an untracked artefact dated 2026-08-30 belonging to
  BL-1441. Reported, not fixed: other rounds' territory.
- **1 was a flake I briefly mislabelled as mine** — `test_song_examples`; see §7.
- **1 is another round's work in flight** — `bl1419_defects_and_bands`, whose
  `TheGridIndexPicksTheNewest` pins the exact rule BL-1505 is replacing in `_grid_index`. I
  confirmed it from their diff rather than swapping their file out mid-edit.
- **1 was genuinely mine, and is fixed.** `test_claims_manifest` went red because
  `docs/claims/BL-1492.claims` declares `func clippershq/meme_finder.py::_approvals_state` and
  this round deleted that function. The wrong repair is to drop the line, which erases a finding
  that was correct. The right one is `superseded:`, a kind that exists for this and asserts
  **absence** — so the claim passes while the function is gone and **fails if it is ever
  re-added**, which is the point, because re-adding it would re-wire the dead 16-card review
  into the funnel. BL-1492 now verifies 17/17 and this round files its own manifest at 20/20.
  Both were committed *after* the code and instruments, because a manifest checks at HEAD: it
  waits for the code, never the reverse. Filing it first produced 6 failures that said nothing
  about the work. `tools/commit.py` also refused to bundle BL-1492's file with mine — correctly,
  since that would put a departed round's work under my name — so they are two commits, the
  foreign one filed under BL-1492's own id.

`tests/test_bl1503_his_own_packs.py` is **20 checks, green**, and every guard in it was
mutation-proved: eight mutants across `meme_finder`, `free_judge` and `tiktok_finder` all
caught, a control mutation touching only a comment correctly staying green, and every file
restored byte-for-byte afterwards, verified by sha256.
