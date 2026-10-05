# BL-1604: downloads are paused, your scope is five niches, and 7,453 out-of-scope accounts are set aside (nothing deleted)

## CARD

1. **Downloads paused: YES.** That is the default now. Tomorrow's 07:00 run downloads 0 files and moves nothing into Drive (proved through the same code path the task runs).
2. **Your swipe feed now:** football 3,584 · superhero (Marvel + DC) 3,103 · UFC 1,272 · basketball 1,008 · tennis 588. **9,555 in total.**
3. **Out of scope: 7,453 accounts.** Golf 3,822 · anime 1,309 · music 1,005 · other movies/shows 712 · gaming 313 · other sports 292. Also 8,434 good edits.
4. **Moved in Drive:** 3,256 files / 13.69 GB into `ClippersHQ Edits\_out_of_scope\`, each re-hashed equal (0 mismatches). **0 deleted.**
5. **Your swipes and video votes: untouched.** 1 swipe decision and 0 video votes. The digest was identical before and after.
6. **The paused daily still spends about $2.65/day** on feed calls (harvest $2.12, top-up $0.50, snowball $0.03), capped at $3/run. **Not stopped; your call.**
7. **Drive free space keeps falling, and it is not us.** Free space fell from 69.99 to 60.79 GB in about 3 hours. Our folder has been unchanged since 06:11, and this PC backs up 0 folders. 62 GB of your quota is outside My Drive.
8. **$ spent: $0.00.**

**Round:** BL-1604 · LamaTok $0 · counts only (classes, never an account) · nothing on the Desktop · master, MARK, your workbook, the clipper label store, config.json and dashboard/ never written · leak scan on both corpora (section 6).

## YOUR STEPS

1. **Downloads:** nothing to do; they stay paused. When you want them, run `.venv\Scripts\python.exe tools\edits.py downloads on` (and `downloads off` to pause again). The swipe page shows a red **DOWNLOADS PAUSED** until then.
2. **Decide on the daily spend.** While paused, the 07:00 run still buys about $2.65/day of feed calls. That judges new edits, but every link it keeps expires within a day. Tell me "pause the daily" or "keep it".
3. **Bring a niche back:** `.venv\Scripts\python.exe tools\edits.py scope restore golf`. Any class works: anime, music, other_movies_shows, other_sports, gaming. Its accounts, edits and terms come back as they were.
4. **See what is eating Drive:** open one.google.com/storage. It shows whether Photos, Gmail or Drive trash is growing.
5. **The set-aside clips** are in Drive > ClippersHQ Edits > `_out_of_scope` > one folder per class, with an `index.csv`.

## 1. What it was asked to do

- **Part 1 (first, before 07:00):** pause all downloads by default, with an on/off command and a red flag on the page. Prove a paused run downloads 0. Report what the paused daily still spends.
- **Part 2:** make the scope configuration (football, basketball, UFC, tennis, superhero), not code. Every mode and both swipe queues use it. Out-of-scope terms are retired with a reason, and out-of-scope mined terms are dropped.
- **Part 3:** reclassify every account and good edit for free. Dry run first, then apply. OUT_OF_SCOPE is never NO and never blocklisted; your own decisions are never changed. One-command restore.
- **Part 4:** move (never delete) downloaded out-of-scope edits within Drive. Find out what is eating Drive's free space.

## 2. What shipped, and how each was proved

Tests first, each seen failing: Part 1 had **11 checks, all red** before the code; Part 2-4 had **27 checks, all red**. **46 named suites are green (479 checks):** every edit-harvester suite from BL-1599 to BL-1604 plus the repo guards (`atomic_io`, `config_contract`, `tools_tracked`, `guard_resolution`, `operator_home`, `facts_guard`, `secrets_guard`, `backup`). The full suite was not run.

| Part | Shipped | Proof |
|---|---|---|
| 1 | `downloads_enabled` setting, **default off**. `edits.py downloads on/off/status` writes only your override file. | **Paused harvest:** 0 videos and 0 thumbnails fetched, and the good edit stays QUALIFIED with its link. **Control:** the same harvest with downloads on downloads 1. **Paused deferred fetch:** 0 vendor calls. **Drive while paused:** sync moves 0 and no index.csv is written; the control (on) moves 1. **config.json:** byte-identical. **`run_paid("daily")`:** the path the 07:00 task runs downloads 0 and records it. |
| 1 | Live check of the switch and the 07:00 path | The switch reads PAUSED (no override file). The task runs `cmd /c edits_daily_task.bat`, which runs `tools\edits.py daily`, this code. |
| 1 | The swipe page: a red **DOWNLOADS PAUSED** in the status bar, a first banner saying how to turn downloads on, and a health row | The accessibility review came before the edit. It led to the red span plus the banner placed first, and to announcing only on a change. The breaker now says "stopped", and the storage text says "would be X GB when downloads are on". **Driven in Chromium on your live page, read-only: 14 of 14** at 1280 and 320 px. |
| 2 | `allowed_niches` setting plus `clippershq/edits_scope.py` (`canonical`, `in_scope`, `niche_sql`). "marvel" is an alias of superhero. | **Discovery:** refuses golf with 0 calls. **Harvest:** an in-scope YES is fed (positive control), while a golf auto-YES and your own golf YES are not. **Parked pass:** feeds football, not golf. **Auto-approve:** of two proven accounts, only the in-scope one is approved. **Both swipe queues:** in scope only. **Mining:** a golf name is dropped, and mined when golf is allowed (control). **Config:** changing `allowed_niches` changes all of it. |
| 2 | DC added: 36 people, 9 teams/films and 7 generic tags in `edits_terms`, and a DC names pack | `superhero_names()` contains Batman, Superman, Joker, Wonder Woman, Spider-Man and Iron Man. 149 new superhero terms were seeded. |
| 3 | Free classifier, plus `scope plan` (dry run), `scope apply` and `scope restore <niche>` | **Labels:** football, basketball, UFC and tennis pages; a Marvel page and a DC page filed under marvel come out as superhero; anime, another TV show and golf come out as out-of-scope; no evidence falls back to the term that found the page, and nothing at all is "unclassifiable". **Mixed page:** stays in scope unless its posts' out-of-scope evidence is 2× or more. **Dry run:** writes nothing. **Apply:** sets OUT_OF_SCOPE, never NO, never a blocklist entry. **Your work:** your swipes and votes are untouched. **Auto-approvals:** withdrawn as a recorded decision. **Terms:** retired with the reason `out_of_scope:<class>`. **Out-of-scope accounts:** never fed and never shown, even if their niche is later allowed. **Idempotent and reversible:** applying twice changes nothing more, and a restore of golf brings back its accounts, auto-approvals and terms. |
| 4 | `scope move [--dry-run]`: a rename inside Drive into `_out_of_scope\<class>\`, with size and sha256 checked before and after | **Files:** each moved file re-hashes equal at its new path. **Changed on disk:** a file whose hash no longer matches is left where it is. **Dry run:** moves nothing. **Nothing deleted:** proved by walking the code's calls (AST), with no remove, unlink, rmtree or trash call anywhere. **Index:** `_out_of_scope\index.csv` is written. |

## 3. What was measured

**The live dry run, then the apply (your 39,014 accounts):**

| | Accounts | Good edits | Downloaded files in Drive |
|---|---:|---:|---:|
| football | 9,852 | 8,779 | stays |
| superhero (Marvel + DC) | 9,726 | 6,964 | stays |
| tennis | 4,147 | 1,068 | stays |
| basketball | 3,908 | 1,938 | stays |
| ufc | 3,687 | 3,070 | stays |
| OUT: golf | 4,023 (3,822 changed) | 725 | 155 · 0.80 GB |
| OUT: anime | 1,320 (1,309) | 2,055 | 766 · 3.32 GB |
| OUT: music | 1,016 (1,005) | 2,290 | 937 · 4.35 GB |
| OUT: other movies/shows | 716 (712) | 1,917 | 862 · 3.03 GB |
| OUT: gaming | 316 (313) | 642 | 301 · 0.94 GB |
| OUT: other sports | 303 (292) | 805 | 235 · 1.24 GB |

- **The old "marvel" niche was mixed, as you thought.** 9,278 of its accounts are refiled as superhero, 267 as football, and the rest are out of scope.
- **Other refiles:** 10,987 accounts moved to a better-fitting in-scope niche. For example, 259 tennis accounts became football, and 183 golf accounts became football.
- **The rule was tuned before applying.** The first dry run would have filed about 950 mixed pages out of scope. Their posts carried real in-scope evidence, often a football edit with a generic #song or #music tag.
  - So an account now goes out only when its posts' out-of-scope evidence is at least 2× their in-scope evidence.
  - The search term that found a page, or its old niche, cannot keep a page whose posts show nothing of your scope.
  - Those pages' off-topic edits still go out one by one.
- **What carried each class** (counted against my own keyword list):
  - golf: "golf"
  - anime: anime, jjk, bleach, gojo, blue lock, naruto
  - music: kpop, song, music
  - other movies/shows: kdrama, transformers, game of thrones, the boys
  - gaming: roblox
  - other sports: nfl, hockey, wwe, formula1
- **Terms:** 378 retired (golf 354, anime 10, other movies/shows 10, gaming 3, music 1), 945 refiled (941 marvel became superhero), 149 DC terms added.
- **What the paused 07:00 run still spends:** about $2.65/day, capped at $3/run, $5/day and $60/month.
  - Harvest: 3,527 in-scope YES accounts at one feed call each, $2.12.
  - Snowball: up to 20 seeds, about $0.03.
  - Discovery top-up: $0.50.
  - Before the scope change, the 10-05 run spent $2.994. Out-of-scope YES accounts are no longer fed.
- **The Drive drain is not ours:**
  - **Free space:** 69.99 GB at the start (just after 17:37), 65.25 at 19:47, **60.79 at 20:42**. About 9.2 GB went in 3 hours, while downloads were paused and nothing of ours wrote.
  - **Our folder:** 14,682 files, 68.75 GB. Today's only writes were the 11.91 GB from the BL-1601 chain, before 06:11.
  - **Everything else visible in My Drive:** 23 GB in 10 other items. Today it changed only 1,194 small files, under 0.01 GB.
  - **This PC:** Drive for desktop backs up **0** folders from it, and its cache stayed at 10.2 GB.
  - **Your quota:** 153.96 GB is used, but only 91.92 GB is visible on G:. **62 GB is used somewhere G: cannot show** (Drive trash, Gmail, Google Photos, or a backup from another device), and that is where it is growing.

## 4. What was refused or not done, and why

- **The daily spend was not stopped.** You asked me to report it and ask.
- **Nothing deleted.** Files were only moved within Drive.
- **Your own decisions were not changed,** including any of your accounts that are now out of scope (there are none today).
- **The Start Menu "Find new accounts" menu still lists Golf** (it now answers "REFUSED: outside his scope", spending $0), **and lists Marvel**, which now means superhero (Marvel + DC). The shortcut file belongs to another script; say if you want the menu redrawn.
- **The Drive drain could not be traced further** without signing in to your Google account.
- **Not done:** no vendor call, no config.json write, and the full suite was not run.

## 5. What I got wrong

1. **A heredoc-like slip (stray command):** an empty `python -` call with no input; no file was written. I also created one backup script with `sed` and a shell redirect instead of the file tool. That is a file written outside the editor, and I am noting it.
2. **My first test file had four mistakes,** caught before any code:
   - a placeholder assertion that could never pass;
   - a video id computed wrongly twice;
   - a "never deletes" check by text (rewritten to walk the code through its AST, as the repo's guards require);
   - an auto-approve test whose fixture was not actually proven.
3. **My first dry run's rule was too eager:** it would have filed about 950 mixed in-scope pages as out of scope. Measured before applying, and the margin rule fixed it (section 3).
4. **The pause made one earlier fixture wrong in a useful way.** BL-1599's creator-rule test discovered in "golf", which is now refused. I switched it to football; the niche was incidental.
5. **I first wrote "music" without a margin.** Generic tags like #song and #music sit on many football edits. The 2× rule plus video-level filing is my correction, and it is still a heuristic. Spot-check `_out_of_scope\music` in Drive.

## 6. Money, stores, disk

| | |
|---|---|
| LamaTok | **$0.00**, 0 calls |
| edits.db | Backed up first (446 MB, integrity ok, row counts equal) in `edits\backups\`. Apply changed account status for 7,453, account niche for 10,987, video niche for 17,314 good edits and 1,472 term rows. Every change is in `scope_log`, so it can be restored per class. |
| Your work | 1 swipe decision, 0 video votes, 3 blocklist keys: **digest identical before and after** |
| Drive | **3,256 files / 13.69 GB renamed into `_out_of_scope`** (a detached job, 20:42-21:47). Each was sha256-verified before and after: 0 mismatches, 0 failed, 0 missing. 0 deleted. Free space: 60.79 GB of 214.75 GB. |
| Checked independently | 3,256 mp4 files sit under `_out_of_scope`, and 3,256 rows point there. 14,658 of 14,661 downloaded edits are consistent. **The 3 that are not are IN-scope edits whose Drive file is missing:** the move never touched in-scope rows, so this predates the round. Not explained further. |
| Never written | master_leads.csv, MARK, your workbook, the clipper label store, config.json, dashboard/ |
| Processes | Only my own swipe server was restarted (by its PID, through the shortcut path). The move ran as a detached job. |
| Leak scan | 22 files: this report, the code, tests, scripts and claims. **Shape layer:** 0 hits, with its 4 planted controls caught. **Edit corpus:** 14 hits. **Lead corpus:** 93 hits. All were adjudicated **by value** without printing one: 798 equal a word of the public name packs and keyword lists or a frequent report word; 15 are ordinary words or famous names, read off masked lines (a status word, an edit-tag word, two common words, a test-fixture word, and actors in the name packs). **0 leaks.** The report's one hit is a Marvel character's name. |

## 7. Ranked next steps

1. **You: decide the daily spend** while downloads are paused (step 2).
2. **You: look at one.google.com/storage.** Something outside My Drive is taking 3-5 GB an hour.
3. **Spot-check `_out_of_scope`** in Drive. If a class should come back, use `scope restore <class>`.
4. **When you want files again:** `downloads on`. The day limit follows Drive's free space (and goes to 25 GB/day once the 2 TB plan shows).

## 8. Paths

- **New:** `clippershq/edits_scope.py`
- **Changed:**
  - `clippershq/edits_db.py` (downloads switch, scope setting, OUT_OF_SCOPE, scope_log)
  - `clippershq/edits_engine.py` (pause gates, scope filters)
  - `clippershq/edits_auto.py`, `edits_votes.py`, `edits_mine.py`, `edits_terms.py` (DC), `edits_names.py` (DC)
  - `edits_swipe_server.py`, `edits_swipe.html` (the paused flag)
  - `tools/edits.py` (`downloads`, `scope`)
- **Tests:** `tests/test_bl1604_downloads_paused.py`, `tests/test_bl1604_scope.py`. Fixture-only changes in `tests/test_bl1599_edits_engine.py`.
- **Round files:** `scratch/bl1604/`
- **Claims:** `docs/claims/BL-1604.claims`

Say DELETE OUT OF SCOPE and these 3,256 files / 13.69 GB go to Drive's trash (recoverable 30 days).
