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

## 11. "Judge the page, not the post" (order 1618) and a second fresh test, 345 never-seen accounts
- Fix: `scratch/bl1712/RUBRIC12d.md` = 12c + "look at the 12 covers first: at least half real-footage edits = editor even
  when this post is animated / game / creator clips; mostly memes, anime, news, other pages' watermarks = reject even
  when this post is a good edit; the post decides only when covers are missing, or to catch one narrating voice".
- New pages: 12 new keywords (The Boys, Interstellar, Oppenheimer, Gladiator, Spider-Man, Iron Man, Stranger Things,
  Vinicius, Yamal, Kobe, Curry, McGregor) + 6 new hashtags, $0.0108; 345 accounts never on any earlier sheet.
- **Result on the new 345: 334 right = 96.8%** (5 false editors -> 98.2% of its 279 "editor" answers right; 6 missed).
  The 358 set before was 96.4% with the old rubric: the fix moved it within noise, not to 99.5%.
- Same fix on the earlier 358 set (313 pages that were actually seen, see below): 94.3% with the fix vs 95.9% without.
  The page-first rule rescues some edit pages but now rejects some real ones (pages with half meme covers).
- Conclusion: on fresh pages the judge sits at 96-97%, with about 2% false editors. My own blind labels and a careful
  Opus label agree about 95% on the same kind of pages, so the remaining errors are mostly "what counts as an edit
  page" -- Dusan's rulings, not a bigger model, decide them.
- E-mails on the new pages: 279 real editors, 25 with a bio e-mail, 0 new. Over all three fresh tests: ~870 real
  editors, ~75 with a bio e-mail, 2 new. The bottleneck stays the e-mail.
- Process notes: the farm could not take the work (bogdan paused/offline, the 3090 slow), so the same Sonnet + Opus
  judge ran as agents of this window. Under that load the image reads hit a "request limit" twice: two judge agents
  coded 45 + 19 sheets without seeing them; they said so, those pages were re-run or left out of the score.
- Files: `bl1712_work\fresh345_score.json`, `bl1712_work\fresh358_12d_seen313.txt`.
- Update 19:30: the 45 sheets an agent had not seen were judged on the 3090 farm (Dusan's load order: 3090 first, then
  bogdan, his PC only when both are full). Full 358 set: page-first rubric 338/358 = 94.4% (6 false / 14 missed) vs the
  previous rubric 345/358 = 96.4%. The page-first rule is not better; keep RUBRIC12c until Dusan rules on the formats.

## 12. Night 25-26 Oct: 1,369 good TikTok editor e-mails (orders 2012, 2356, 0935)
- Result: **1,369 good TikTok editor e-mails**, one row per address, every account judged with frames + speech-to-text
  (Sonnet, Opus on the unsure); 446 still unsure are not in the list. Files: Desktop\Tools\Good_TikTok_editor_emails_26_Oct.xlsx,
  Desktop\!CLIPPER LEADS 26 Oct.xlsx, Desktop\Tools\Good_editing_pages_with_emails_26_Oct.xlsx. Dusan asked for 2,000.
- Sources ($0): the 7,092 e-mail "editors" already in his operator lists (judged by the old picture-only judge) -> only
  ~19% are real edit pages; 500 edit-app editors whose e-mail was never delivered; 113 from two paid hashtag tests.
- Paid test (A1/A2, $0.503 on "Finder daily" before the supervisor ruled only the named $20 line may be used): 113 new
  addresses at $4.3-4.6 per 1,000 raw, but A1 had only 5 real editors in 44 (26 creators) -> ~4 cents per good e-mail,
  above Dusan's 1-cent stop line. The $20 line never reached the wallet, so nothing was bought after 01:19.
- What went wrong, in order: (1) the 3090's shared whisper cache lost large-v3-turbo too (~21:50) -> ~4,000 sheets with
  no transcript; fixed with our own model copy (/home/farm/b12_models) and by rebuilding only the editor/unsure pages and
  judging them again; (2) a 3090 line cut short crashed a chunk build (now skipped); (3) parallel image-reading agents hit
  a request limit and coded sheets they had not seen (they removed those; the sheets went back to the farm); (4) the farm
  lost the jobs of 6 chunks (resubmitted); (5) a hidden Windows line end in a shell list made the repair loop idle for two
  hours. Lessons in LESSONS/COUNCIL.
- Tools: scratch/bl1712/pool12.py (main | op2 | fixspeech <run> | deliver), route12.py sheets2 --redo <pages>, paid chain
  bl1712_work\paid\run_a.sh.
