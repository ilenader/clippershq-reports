# BL-1712 -- the new judge (frames + speech-to-text) and the main route, measured on 300 hand-checked accounts

Orders: Dusan 10:17 (1022, the main route: one search page, no paid second profile visit, judge free on the 3090) and
Dusan 10:55 (1055, urgent: the judge passed narrators as editors; build a new judge, test it on 300, no paid e-mail
until it scores 99.5%). Money this round: $0.0224 (the three search pages at 10:41). Everything after that was $0.

## 1. The answer in one paragraph
The new judge is right on **285 of 300 = 95.0%**. That is below Dusan's 99.5%, so the paid e-mail step **stays
paused**. It rejects all 3 of Dusan's bad examples. Of last night's 82 "editors" only **2 are real edit pages**: the
other 80 are journalists and commentators (41), narrated recap / lore / reality-TV pages and media outlets (39).
The 95% is not mostly judge mistakes on clear pages: my blind hand labels and a careful Opus label agree on only
95.3% of the same 300, and the splits are the same formats the judge trips on. Nobody can measure 99.5% until
Dusan rules on six formats (section 5).

## 2. What the new judge sees (one sheet per account, built free on the 3090)
Profile picture, name, handle, followers, likes, bio; this post's views, length, sound, caption, hashtags; the 12
newest covers; one frame every 2 s (under 30 s) or 3 s (to 90 s), at most 40; the speech-to-text of the post's audio
(whisper on the 3090, any language). Sonnet judges every sheet (rubric `scratch/bl1712/RUBRIC12b.md`); Opus takes a
second look at the ones Sonnet calls unsure. Tool: `scratch/bl1712/route12.py sheets2`, `scratch/bl1712/sheet2_remote.py`.
Built: 565 sheets (82-list 82, Dusan's 3, hashtag 211, keyword 185, sound 84); video found for 562, speech in 441.

## 3. The test set and how the truth was made
- 300 sheets: the 82-list, Dusan's 3, hashtag pages 1-80, keyword pages 1-70, sound pages 1-65. Dusan's 3 are also
  inside the 82-list, so it is **297 different accounts**.
- Truth: every sheet looked at **blind** (frames, speech, covers, bio) by this window, split over 8 parallel copies of
  itself that never saw a judge answer. Then I looked again myself at every sheet where the judge and that label
  disagreed, and every sheet where the label and a careful Opus label disagreed (18 sheets). Dusan's 3 = his own words.
- Score: `scratch/bl1712/compare12.py score ... --look-at-k`; result file `%LOCALAPPDATA%\ClippersHQ\bl1712_work\test300_score.json`.

## 4. The score
| | count |
|---|---|
| right (of all 300; an unsure answer counts as wrong) | **285 (95.0%)** |
| judged editor | 143 |
| real editors in the set | 147 |
| **false editors** (judged editor, not one) | **5** -> 96.5% of its "editor" answers are right |
| **missed editors** | **9** (6 of them left unsure even after Opus) |
| still unsure after Opus | 7 |
| right on the 293 it decided | 97.3% |
| my labels vs a careful Opus label, same 300 | 95.3% agree |

Per source: 82-list 81/82 (1 false editor: a TV-scene compilation with ranking covers), Dusan's 3 3/3, hashtag 74/80,
keyword 62/70, sound 65/65.

The 15 errors, by kind:
- edit pages whose post carries speech (a fighter's interview words, pundit clips) -> judge says unsure or person: 5
- pages that mix memes and edits, or a tiny page with one edit: 4
- highlight compilations (broadcast footage, with or without a song): 3
- free raw-clip packs for other editors: 1; TV-scene compilation with ranking covers: 1; AI-made skit left unsure: 1

## 5. What is needed to reach 99.5%: six rulings from Dusan
I had to decide these myself to score at all; the labels split on exactly these:
1. NBA / football highlight compilations cut to a song under the page's own watermark, no effects -- editor? (I said yes)
2. An edit page whose post uses an athlete's interview words or pundit clips over the footage -- editor? (yes)
3. An edit page whose post is one continuous voice explaining the play -- reject? (yes, reject: narrator rule)
4. A page with "editor" in the bio where about half the covers are memes -- editor? (yes)
5. A page posting free raw clip packs for other editors -- editor? (no)
6. Broadcast compilations with the original TV commentary and no song -- editor? (no)
With his answers in the rubric, the same 300 run again for $0 on the 3090, then a fresh held-out 300 to prove it.

## 6. Hashtag vs keyword search vs sound pages (order 1022), on the new judge
One page per query, 8 queries each, the three paid at 10:41 for $0.0224 together.
| source | paid | authors | real editors | with e-mail in bio | NEW e-mail | only this source finds |
|---|---|---|---|---|---|---|
| hashtag pages | $0.0096 | 211 | 154 | 9 | 0 | 137 |
| keyword search | $0.0048 | 185 | 149 | 16 | 1 | 131 |
| sound pages | $0.0080 | 84 | 27 | 1 | 0 | 25 |
- Finding real editors is cheap: 311 different real editors for $0.0224 (about $0.07 per 1,000), and the three
  sources barely overlap. Keyword search is cheapest per editor; sound pages bring mostly creators and shops.
- **The e-mail is the bottleneck, not the search or the judge.** Only 26 of the real editors show an e-mail in the
  bio, and 25 of those are already in our stores. A second paid profile call returns the same bio (lesson 95), so it
  cannot add e-mails. New real editors with an e-mail per dollar: 1 for $0.0224 -- too few to price; a bigger test on
  fresh queries is needed before any money.
- The bio now comes FREE from the embed page, so even keyword search needs no paid profile call.

## 7. Last night's 82-list, rechecked
Cleaned file: `Desktop\Tools\Editors_82_rechecked_25_Oct.xlsx` (copy in the operator home): sheet "Real edit pages"
= 2, sheet "Rejected (80)" with the reason per row. The night price ($0.40 for 82 = $4.9 per 1,000) was really
**$200 per 1,000 real edit pages**: the old picture-only judge passed commentators and narrators.

## 8. Also done
- 3 FIXER order 1147: 40 clips (20 film-dialogue edits, 20 narrators, named by hash) through
  `tools/clip_voice_kind.py`: speech fraction < 0.82 kept all 20 wanted clips and caught 18 of 20 narrators, in-sample
  only (bl1712_work\clips40). Tool `scratch/bl1712/clips12.py`.
- Head-to-head tool `scratch/bl1712/h2h12.py`.

## 9. Lesson
A judge cannot be measured past the agreement of its own labels. Two careful labellers split on 4.7% of these pages,
always on the same formats; the fix is the owner's ruling on those formats, written into the rubric, not a bigger model.

## 10. Fresh test, 358 never-seen accounts (order 1401, Dusan's yes 14:01)
- Pages: 12 new keyword searches (Suits, Dexter, Matrix, John Wick, Batman, Game of Thrones, Mbappe, Neymar, Haaland,
  LeBron, F1, boxing) + 6 new hashtags, $0.0108. Every account that was on any earlier sheet was left out: 358 fresh.
- Rubric `scratch/bl1712/RUBRIC12c.md` = the 10:55 rubric + 8 interim format rulings (mine, until Dusan rules):
  highlight compilations cut to a song = editor; edit pages using interview/pundit clips = editor; one explaining voice =
  reject; "editor" bio with at least half edit covers = editor; free clip packs, TV-commentary compilations, brand-new
  pages with no edits = reject; movie scenes cut to a song = editor.
- Truth: every sheet hand-checked blind; my own look at all 16 judge-vs-label splits (the label stood on 13).
- **Result: 345 of 358 right = 96.4%.** False editors 4 (98.6% of the judge's 282 "editor" answers are right), missed
  editors 9. Still below 99.5%, so the paid e-mail step stays paused.
- What it still gets wrong: it judges the ONE post instead of the PAGE. An edit page whose post happens to be animated,
  game footage or creator clips is called a reject (7 of the 9 misses); a meme-caption page or a page reposting another
  team's edits is called an editor (3 of the 4 false editors).
- Two things broke on the way, both fixed: the 3090's cached speech-to-text model ("small") disappeared at ~14:18, so 101
  sheets had no transcript (now falls back to the cached large-v3-turbo model; those pages were rebuilt and re-checked);
  the farm dispatcher started none of our jobs from 14:30 (log: "dispatch held -- a lane bug", reported to 3 FIXER), so
  the same Sonnet + Opus judge ran as agents of this window with the same rubric.
- E-mails on the fresh pages: 282 real editors, 24 with an e-mail in the bio, 1 new. Over both tests: 593 real editors,
  50 with a bio e-mail, 2 new. The search is not the problem; real editors who show a NEW e-mail are about 1 in 300.
- Old 300 re-judged with the new rubric (partial, the farm stalled): on the 82-list and Dusan's 3 it now gives
  0 false editors (it sends the one TV-scene page to a second look instead of passing it).
- Files: `bl1712_work\fresh358_score.json`, `bl1712_work\<run>\hand_*.json / handr_*.json / adj.json`.
