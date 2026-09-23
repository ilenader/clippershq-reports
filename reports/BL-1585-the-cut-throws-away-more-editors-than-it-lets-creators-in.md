# BL-1585: the craft cut hides about 8 editors for every creator it lets through, its real editor loss is 21%, not 14.8%, and nothing improves until he grades a cut stratum

**Round:** BL-1585 · **read-only audit, $0.00, no vendor call** · every store byte-identical at close
(44 files: master, `spend.json`, config, the tag ledger, the workbook, all of `ground_truth/`, all
five review pages and their four manifests) · paths redacted (`<Desktop>` is the OneDrive Desktop) ·
hashtags are named, accounts never are, and no bio is quoted.

**Whose judgement.** Every rate below carries one of three tags, and they are never pooled:
- **[HIS]** his 100 operator grades. They were drawn only from craft-cut survivors, so they measure
  creators let through and **cannot see an editor the cut removed**.
- **[247]** the 247 masked labels, written by an earlier agent from masked TikTok bios. They are a
  model's judgement, not his, and the only labelled sample that contains cut rows.
- **[CUT]** the craft cut's own opinion (`editor_gate.bio_rule`).

## The paragraph

**The pipeline is not yet fit for "faceless editors only", and the error costing him more is the
one nobody can see.**

On TikTok, what survives is mostly right: he rejected 4 of 50 survivors, 8.0% [3.2–18.8] [HIS].
But the cut removes **23 of 109 independently labelled editors, 21.1% [14.5–29.7] [247]**. The
14.8% this project has been quoting is 23/155, and that denominator includes his 46 TikTok
survivors, which by construction could never have been cut. In accounts, about **616 [420–883]
editors sit unseen in master's 4,284 TikTok CUT rows**, against about **80 [32–188] creators among
the 999 TikTok KEEP rows**, roughly eight lost editors for every leaked creator. His 5% line is on
the loss, and the loss is four times that.

On Instagram the cut keeps 75 of 9,739 addressed rows. He rejected 13 of the 50 survivors he graded
(26.0% [15.9–39.6]), and **nobody has measured how many editors are in the other 9,096**: the 247
contain no Instagram rows.

**The single highest-value change is not code. He has to grade the cut cards already on his
Desktop.** 110 of them (60 Instagram, 50 TikTok) sit in four ungraded pages, and they are the only
way anyone will ever learn what the cut throws away. Three rounds have reported that he hasn't
graded; this one puts it as the recommendation. **Nothing about the cut can responsibly change until
he grades a page.**

The "dm for" rule, measured properly, **recovers none of the lost editors (0 of 23 [247])**. It is
worth something only as a ranking inside what he already gets: 21 of 21 survivors carrying it were
editors [HIS].

## 1. What this is, for a reader with no context

ClippersHQ walks TikTok and Instagram, keeps accounts whose bio shows they edit video for other
people, and delivers their addresses to one operator. His goal: **faceless editor channels only; no
creators, no businesses.** His standing rule outranks it: **never wrongly cut a real editor; unknown
is a hold, never a cut.** The "craft cut" is a bio keyword rule that decides what he is shown. Every
KEEP rate this project has quoted, including BL-1584's 45.5% for `#aftereffects`, is that rule
grading its own output. This round asks what the rule gets wrong in his terms, using only what is
already on disk.

## 2. The 17 he rejected, characterised by hand, not fitted

He marked 17 of 100 survivors NOT, with no reason on any of them: 4 TikTok, 13 Instagram. All 17
were read by hand, with addresses reduced to a domain class on first read. No rule was learned from
them. BL-1579 already showed that seven candidate rules fitted to these rows each cost 6–35% of his
editors.

| box | TikTok | Instagram | what they look like |
|---|---:|---:|---|
| **creators** | 2 | 3 | a face-on commentary channel whose owner calls himself a video editor; a teenager's personal fan account; a food creator who was once a magazine "food editor"; an amateur athlete who lists "editing" among hobbies; a photographer selling a colour grade |
| **edit accounts that are not editors for hire** (unnamed until now) | 2 | 2 | large fan-edit accounts that sell *promotion slots* or run an edit community (349k–706k followers); hobby fan-editors offering "credit me" reposts and "collabs" |
| **musicians** (unnamed until now) | 0 | 3 | a DJ "making music for edits", a band announcing a "video premiere", an artist with a "new edit" of a song |
| **fan / meme / news pages** | 0 | 3 | a K-pop fan page, a regional TV troll page, a film-review and news page |
| **businesses** | 0 | 2 | an electronic-music promotion community and a music-news outlet, both "premieres" |

What reading them shows, without turning it into a rule:
- **Most rejects contain real editing words used in another sense.** "Premiere" means a music
  premiere in 3 of the 13 Instagram rejects, and bare "premiere" (not "premiere pro") appears in
  **0 of his 83 editors [HIS]**. "Editor" means a food editor; "edit" means a song edit. Bare
  "premiere" is the only craft term keeping just **6 master KEEP rows** (3 TikTok, 3 Instagram), so
  fixing it is worth 6 rows. It appears in none of the 247 (the regex's positive control passes), so
  that zero is untestable there.
- **Four of the 17 do edit video.** They edit for themselves or sell advertising, not editing. His
  "editor" seems to mean *editor for hire*. The new three-button page (EDITOR / CREATOR / BUSINESS)
  would force these four into CREATOR. That is a limit of the page, not of the grades.
- **The TikTok rejects are big accounts:** median 197,100 followers against 5,030 for his 46 TikTok
  editors [HIS]. Characterisation only: a follower floor is refuted (≥100k fires on 13 of his 83
  editors).
- **The source funnel is not the explanation.** 9 of 13 Instagram rejects came from non-hashtag
  funnels (meme-page finder, Spotify finder, suggested crawl), but so did 30 of 37 of his Instagram
  editors. False-pass rate: hashtag walk 4/11 = 36.4% [15.2–64.6] vs other funnels
  9/39 = 23.1% [12.6–38.3] [HIS]. The intervals overlap.
- **"Faceless" is on no label.** No grade says whether a face is shown, so no rate in
  this project measures "faceless". At least one reject (the commentary channel) is plainly
  face-on.

## 3. The two errors, side by side, in accounts

Master as it stands (TikTok addressed is **5,480**, not the brief's 4,158: BL-1583 and BL-1584
appended 514 + 808):

| platform | addressed | KEEP | CUT | HOLD (no bio) | review_hold set |
|---|---:|---:|---:|---:|---:|
| TikTok | 5,480 | 999 | 4,284 | 197 | 796 (677 of them already CUT) |
| Instagram | 9,739 | 75 | 9,096 | 568 | 4,673 (4,429 of them already CUT) |

| error | rate | whose | in accounts |
|---|---|---|---|
| **creator let through, TikTok** | 4/50 = 8.0% [3.2–18.8] | [HIS] | ~**80** [32–188] of 999 KEEP |
| **creator let through, Instagram** | 13/50 = 26.0% [15.9–39.6] | [HIS] | ~**20** [12–30] of 75 KEEP |
| **editor thrown away, TikTok** | 23/109 = **21.1% [14.5–29.7]**; P(editor given CUT) 23/160 = 14.4% [9.8–20.6] | [247] | ~**616** [420–883] in 4,284 CUT |
| **editor thrown away, Instagram** | **unmeasured**: 0 Instagram rows in the 247 | none | unknown; each 1 point of P(editor given CUT) is ~91 accounts in 9,096 |

How the key numbers were checked:
- **The 21.1%.** Recomputed from the stored `bio_hit` key, it is 24/109 = 22.0% [15.3–30.7]. The
  quoted 14.8% is the same 23 lost editors over 155, with his 46 survivors added, which cannot be
  lost.
- **The 616.** 4,284 × 23/160 = 615.8. The 247 are a random draw from master's TikTok bios, but only
  14 of them carry an address, so applying their rate to addressed rows is an assumption, stated
  here rather than hidden.
- **The two judges disagree about what is kept.** The 247 say KEEP holds 1 non-editor in 87
  (1.1% [0.2–6.2]); he says 4 in 50. Different judge, different population. His number is the one
  that counts.

**The asymmetry he has stated.** A creator let through costs him one email. An editor who is cut
never appears in front of him, so he never learns it existed. One correction to "gone forever":
**master never deletes a CUT row.** It keeps `craft_cut=CUT` and never ships it, so every lost
editor is recoverable by a re-read. It is invisible to him, not destroyed.

**Is the craft cut worth its loss rate?** Per 1,000 TikTok addressed rows, on the 247's class mix
[247, a model's judgement]:

| policy | shipped to him | non-editors in it | editors he never sees |
|---|---:|---:|---:|
| **do nothing**: ship every addressed row | 1,000 | 559 (55.9%) | 0 |
| **craft cut as today** | 352 | 4 (1.1%) [247], ~28 at his 8.0% [HIS] | **93** |
| **HOLD-only**: ship KEEP, park CUT, delete nothing | 352 | same | 93, **all parked and recoverable** |
| **tighter cut**: named tool/term only | fewer | 0/138 kept [247] | editor loss **48.6% [39.4–57.9]** [247]; would remove 44 of his 83 editors [HIS] |

The honest reading of this table:
- **"Craft cut as today" already is HOLD-only in data terms**, because nothing is deleted. What is
  missing is any route by which a CUT row is ever looked at. The cut stratum on the review pages is
  that route, and none of it has been graded.
- **A tighter cut moves away from his line, not toward it.**
- Ship-everything is 56% junk. The cut removes 137 of 138 non-editors [247] at the price of one
  editor in five.

## 4. Every gate on the path, and what each actually removes

| gate | where | what it removes today | measured by |
|---|---|---|---|
| **the tag** | the walk's tag list | title-only tags keep 3.4%, "edit" tags 28.8%, `#aftereffects` 45.5% | [CUT] only: these are the craft cut's opinion of its own supply |
| **the craft cut** | stamped only by scratch delivery scripts; **no production module computes `craft_cut`** (AST: string reads at `writer.py:237`, `main.py:1163`, `review_loop.py:138`; 0 calls) | TikTok 4,284 of 5,480 addressed; Instagram 9,096 of 9,739 | [247]: 137/138 non-editors caught, 23/109 editors lost |
| **review_hold** | same: a column set by scratch delivery (AST: 0 production writers) | nothing; it parks. Of 4,673 held Instagram rows, **4,429 are already CUT and only 24 are KEEP** | resolving the "48% of Instagram" would change his deliverable by at most **24 Instagram + 80 TikTok rows** |
| **the creator gate** (`quality_gate.garbage_cut_reason`) | called once, `main.py:3484`, inside `main.py`'s own run loop; **the hashtag harvest path never reaches it**. `email_harvester.py` imports `main` only to book spend (`:249`). Grep and AST agree. | nothing. `cut_garbage_enabled` is False on ZHUS, PANICBABY, STRAENGE and DAYLIGHT, unset on ANIME15K and top level | **Untestable offline, not "safe".** Positive control cuts and negative control keeps, but master stores none of the fields that can trigger it alone (`niche_flag`, `clip_verdict`, `deep_latest_ts`, `_editor_pct`), and only 15 of his 100 rows carry a `quality_score`. **Nobody can say whether turning it on would help, and turning it on would not touch the rows he receives.** |
| **`looks_agency`** | **not wired on the harvest path.** AST: 3 calling modules (`free_contact.py:189`, `outcomes.py:136`, `send_suppress.py:389`, where it only flags). Grep: 7 files, because 4 mention it in comments or define it (`meme_finder.py:8489`, `tiktok_finder.py:4593`, `writer.py:1455`, `role_policy.py:180`). **AST answered; grep over-counted.** | nothing on his path | measured on his 100 anyway [HIS]: **fires on 0 of 17 rejects and 0 of 83 editors** (positive control on a `.invalid` agency address fires). **Wiring it would catch none of the creators he rejected.** |

The path from hashtag to him: `email_harvester` classifies each row into `editor_class` (name rule
OR bio rule) but removes nothing. `crossdedup.append_leads` writes master and removes nothing. A
scratch delivery script stamps `craft_cut` and `review_hold`, and a Desktop sheet carries KEEP. **The
only gate that removes anything from his view is a script under `scratch/`**, not a production
module. That matters: the rule protecting his inbox has no test in `tests/` and no single owner.

## 5. What would move the needle, ranked by what the data already says

Refuted ideas are not re-proposed here (`<title>edit` tags, consumer-tool tags, business words as a
cut, `is_verified`, follower floors, caps/digit/URL ratios, the self-description rule, the
personal-name rule).

1. **He grades the cut cards already on his Desktop.** Why: every loss number in this report
   rests on a model's 247 labels, and Instagram loss has no number at all. 110 cut cards are drawn
   and waiting: 60 Instagram (the 50-card cut-only page plus 10 on the mixed page) and 50 TikTok.
   **This is the only item on the list nobody else can do, and it outranks everything below.**
2. **Add `name_rule` as a HOLD, not a KEEP.** It is already computed in production as part of
   `editor_class`, so it costs $0. On the 247 it recovers **7 of the 23 lost editors**, taking loss
   from 21.1% to **16/109 = 14.7% [9.2–22.5]**. It also admits 6 non-editors, so false keeps go from
   1 to **7/138 = 5.1% [2.5–10.1]** [247]. As a HOLD, those 6 are parked for review and never shipped
   to him, so it cannot add a creator to his inbox. It would move **156 TikTok + 26 Instagram** CUT
   rows to HOLD. It still leaves loss above his 5% line.
3. **"dm for" as a priority rank inside survivors, and nothing else.** Measured three ways:
   - **[HIS]:** fires on **0 of 17 rejects and 21 of 83 editors**. Precision where it fires:
     21/21 = 100% [84.5–100]. Survivors *without* it are 17/79 = 21.5% [13.9–31.8] rejects.
   - **[247]:** precision 7/11 = 63.6% [35.4–84.8]. **Added to the cut it recovers 0 of the 23 lost
     editors** and admits 4 non-editors. As a cut it would lose 25.3% [17.2–35.6] of his editors.
   - **Verdict:** ship dm-for rows first, or treat them as already reviewed. It is not a KEEP rescue
     and not a cut. The broader availability set is similar: it recovers 2 of 23, loss 19.3%
     [13.0–27.7].
4. **Hold bare "premiere".** 3/17 rejects vs 0/83 editors [HIS], but it keeps only 6 master rows.
   Correct but tiny, and learned from 17 rows, so HOLD at most.
5. **The orphan bios cannot test a rule.** They are 65,972 bios with no labels. They price a rule's
   **reach** (bio_rule fires on 31.3% [30.9–31.6], dm-for on 5.2% [5.0–5.3], dm-for without bio_rule
   on 1,884), never its precision or recall. They become a test corpus only when someone grades a
   sample, which is item 1 again.
6. **Wiring `looks_agency`, or turning on the creator gate: no value measured.** The first catches
   0 of his 17; the second is untestable and not on his path.

## 6. The loose ends BL-1584 left

| loose end | file:line | does it matter | what it would take |
|---|---|---|---|
| tag ledger uncommitted | `email_harvest_tags.json`: tracked, modified, 669 keys at HEAD vs 720 on disk (51 differ, 26 from BL-1583 and 25 from BL-1584); last committed at `d3fc1e88` (BL-1566) | **yes**: it is what stops tags being re-walked and re-paid. Correction to the premise: it is *tracked*, so `git clean` cannot remove it; `checkout --`, `reset --hard` or `stash` would silently revert 51 tags | one pathspec commit spanning two rounds, which only the operator or a claim-holding round should decide |
| false "ledger disagrees" after any kill | `scratch/bl1584/walk.py:223` (`tot_calls = sum(sessions)`), printed at `:231–232`, alarm at `:234–235`; the booking itself uses the fixed `max(...)` at `:162` | **yes**: a known-false alarm trains people to ignore the real one | apply the `:162` expression at `:223`, a one-line change in a scratch walker (not fixed: read-only round) |
| `test_funnel.py` "fails at HEAD" | **the premise is stale.** `ig_budget_declared` is a parameter of `preflight_check` (`clippershq/main.py:1212`, read at `:1230`, `:1264`), and the working tree matches HEAD | the real finding is smaller: the suite **passes in the tree (815 checks, ALL GREEN)** and **fails under `run_all --head` at check 548** because `tests/test_funnel.py:4581` reads `./master_leads.csv`, which is untracked and absent from a `git archive` extract | give the test a fixture header; until then `--head` cannot vouch for this suite |
| review pages ungraded | `<Desktop>`: `…152635` 87 cards (37 Instagram, 50 TikTok, 20 of them cut); `…202836` **50 Instagram cut** cards; `…192431` 86 TikTok (20 cut); `…095856` 100 TikTok (20 cut). Correction to the premise: 87 / 50 / 86 / 100 | **the whole audit rests on this** | him, and nobody else |

Both suite runs named the suite exactly (`run_all.py -k test_funnel`, exact-or-glob since BL-1580),
and store snapshots were taken around each: 0 of 44 store files and 0 of 1,274 snapshot files moved.

## 7. What I got wrong

1. **My first creator-gate positive control was not a positive control.** It used a stale date the
   gate never reads, so it did not cut, and a zero on his 100 would have read as "measured". I
   rebuilt it on a field the gate does read. Then my verdict line keyed on the wrong field
   (`deep_posts_checked`, which is stored but cannot fire alone) and printed "a measured zero". It
   now keys on the four fields that can fire alone, and says **untestable**.
2. **In BL-1584 I quoted the 14.8% loss rate without checking its denominator.** It was diluted by
   46 survivors that cannot be lost; the independent figure is 21.1%. My own previous report carried
   the wrong yardstick.
3. **The orphan pass crashed twice on file shapes**: one checkpoint file changed shape since the
   census, and 5 JSONL lines are malformed. The final n is 65,972 against the census's 66,147. The
   shortfall is 175 bios, counted and printed rather than hidden.
4. **A snapshot helper wrote into a closed round's directory.** `scratch/bl1584/snap.py` put its
   files in `scratch/bl1584/`. I moved them to `scratch/bl1585/`; no store and no tracked file was
   touched.
5. **Had I stopped at the first suite result I would have confirmed a false premise.** `--head`
   said FAIL; only the in-tree run showed the red is the test reading an untracked file, not the
   `NameError` the brief described.
6. **My first draft of this report had two leak-scan hits:** two ordinary words that one account
   each also uses as a handle, used as words in only 6 and 58 master bios. That is below the
   100-bio bar at which a token counts as vocabulary. Both were rephrased, not argued away, and the
   re-scan is 0 hits.

## 8. Assertions at close, and the recommendation

```
diff start -> end: 44 vs 44 files, 0 moved     (master, spend.json, config.json, email_harvest_tags.json,
                                                workbook, bl1572 results, every ground_truth/ file incl. the
                                                label store and all mark files, 5 review pages + 4 manifests)
suite run 1 (--head, -k test_funnel): 0 of 44 + 0 of 1,274 moved
suite run 2 (in-tree, -k test_funnel): ALL GREEN -- 1/1 suites passed, 815 checks; 0 of 44 + 0 of 1,274 moved
vendor calls: 0     spend.json: byte-identical     MARK: not opened
```

**Recommendation.** Grade the cut cards first: the 50-card Instagram cut page (`…202836`), then the
20 cut cards on each TikTok page. Until those grades exist, no change to the cut can be justified in
his terms, and this report recommends none. When the grades arrive, measure the `name_rule`-as-HOLD
change against them before shipping it.
