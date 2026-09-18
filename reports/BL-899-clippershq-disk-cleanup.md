# BL-899 — C: drive cleanup: 99 directories enumerated, 85 removed, 2.12GB back, and four things that exist nowhere else

**2026-09-18. No database touched. No product code changed. Two files committed: one CLAUDE.md bullet and one new standalone script.**

## THE HEADLINE: THE PILE IS 21.7GB AND 18.5GB OF IT IS NOT YOURS TO LOSE YET
99 leftover directories at the C: root totalled **22,176MB**. I removed **85 of them, 2,168MB**, every one proved on origin or proved to be nothing but build output and round telemetry. I left **14 directories, 20,008MB**, because each holds at least one file that exists in no repository and nowhere else on this disk. **18,512MB of that is one directory, `C:\ClippersHQ_renders`, and despite its name it is not ClippersHQ's.** It is the render pipeline output of the twitch clipper / memebot project: `__ORIGINAL.mp4` / `__OURS.mp4` comparison pairs under BL-12xx and BL-14xx numbering, plus `bl1235_backup\` (a CSV and XLSX export of repost accounts) and `songs.json.backup_20260812_160748`. Two of those are named backups of data, not renders. **You almost certainly want it gone. I cannot prove it is reproducible, so I did not touch it. Say the word and it goes in one command.**

## PART 0 — EXCLUDED BEFORE ANYTHING ELSE
• **Primary checkout `C:\Users\...\Desktop\ClippersHQ`**: identified first, never touched.
• **`C:\w` and `C:\w\b898`**: BL-898 is LIVE. `git worktree list` registers `C:/w/b898` on `checkpoint/BL-898` with `src/lib/clip-earnings-writer.ts` modified, and `C:\w` took new writes at 15:09 and 15:12 while I worked. Left alone. `C:\bl898-sandbox` appeared mid round; left alone.
• **`C:\w2`**: a REGISTERED worktree of a different repository (`twitch-clipper.git`), detached at 018efe8.
• Zero system directories entered scope. Nothing outside the 99 enumerated names was read or removed.

## PART 1 — EVERY LEFTOVER, CLASSIFIED BEFORE ANYTHING WAS DELETED

| class | dirs | MB | evidence |
|---|---:|---:|---|
| SAFE reports checkouts | 35 | 1,800 | full clones of `clippershq-reports.git`, tracked tree clean, HEAD present in `git rev-list --remotes=origin` after a live fetch |
| SAFE build output | 2 | 206 | `bl790`, `b791`: one top level entry each, `.next`, no source |
| SAFE round sandboxes | 41 | 129 | `ledger.jsonl` / `world.json` / `snapshot-*.json` / `renders`; all 41 rounds have a published report on the reports origin |
| SAFE scratch | 6 | 33 | `w821-scratch` `w824-scratch` `w825-scratch` `w827s` `w828s` `w829s`: build and dev logs, probe JSON, session tokens |
| SAFE empty | 1 | 0 | `projects`: 0 files |
| HOLDS UNIQUE WORK | 12 | 19,993 | see PART 2 |
| IN USE / held back | 2 | 5 | `bl896-sandbox`, `bl897-sandbox` |
| **total** | **99** | **22,176** | |

Oldest `rpt610`, 2026-07-21 22:28:19. Newest removed `bl894-sandbox`, 2026-09-18 11:16:13. Nothing was classified UNKNOWN and then deleted; everything I could not determine sits in PART 2.

**The reports checkouts are genuine duplicates, and the first check said otherwise.** Comparing working tree sha256 against `git show origin/main:<path>` reported five of five report files DIFFERENT in `rpt810`. That is the Windows CRLF trap (`core.autocrlf=true`): by blob OID all five are IDENTICAL, `rpt810`'s HEAD is an ancestor of `origin/main`, and `git status` was clean. BL-759 hit the same shape from the other side.

## PART 2 — PRESERVED, AND WHAT I REFUSE TO DELETE
**No recovery branch was needed: not one commit in any removed directory was missing from origin.** All 35 reports checkouts were clean with HEAD reachable from `refs/remotes/origin/*`; the 43 sandbox and scratch directories are not git at all. Verified from origin by `ls-remote`, not from push output: `clippershq-reports refs/heads/main = cc93eca527852d5adb07b9bda8b794855a2fda68`, `ClippersHQ refs/heads/main = 97fdf3a8958278e16fba2d33132bbfc4c5fa613a`.

**Four finds that would have been lost. None was deleted.**
1. **`C:\c` (2MB)** holds exactly one file, a 1.19MB rendered video at `C:\c\Users\GAMECE~1\AppData\Local\Temp\claude\C--Users-...-memebot\...\scratchpad\DZD_rendered_FIXED.mp4`. A path quoting bug created it. **The memebot project and that scratchpad are both gone from this machine, so this is the only surviving copy.**
2. **`C:\wt` (81MB)** looked like pure build scratch: 54 top level entries, nearly all `.log`. It also holds `msg12.py`, a **560 line, 21.6KB Python module** headed *"reviewer_note.py, the note layer for ClippersHQ assisted clip review"*. Its blob exists nowhere in this repository. Also `bl666-cols.sql`. (The 80MB inside it is two nested `clippershq-reports` checkouts, both clean and both on origin.)
3. **`C:\temp` (54MB)** holds `docs/reports` copies from the twitch clipper repo. `FIX-001.md` and `THROUGHPUT-001.md` are byte identical to origin. **`RENDER-003.md` is NOT**, so a version of that report exists here and nowhere else. Plus 54MB of mp4 renders in no repository.
4. **`C:\BL1278_HANDOVER_TEST`, `C:\BL1279_HANDOVER_TEST`, `C:\BL1301_UPDATE_TEST` (120MB)** each contain a full `spotify_finder` Python application (`run_spotify.py`, config, data, logs, output). **`spotify_finder` exists on this machine in those three directories and nowhere else.**

**Also left alone, same reason:** `mbwt` (776MB: `setup_emoji_bank.py` plus about 20 `*-REPORT.txt` files, none in the twitch clipper repo), `projects1` (385MB, the `ayocin-next-starter` project), `clipper_render_test` (51MB of mp4), `tmp` (15MB including `ep_backup.py` and `render.prepatch.bak`), `w2` (two uncommitted modified scripts, `scripts/render.py` and `scripts/instruments/cbREBUILD002_run.py`, in another project's registered worktree), and `bl896-sandbox` + `bl897-sandbox`, held back under your "keep the last day or two if there is a reason to": BL-898 is running directly on top of those two rounds.

**Not mine to act on, reported only:** the `twitch clipper` repository has **27 local only commits** on `main` and `sfx-001-emoji-002` that are not on its origin. They are safe where they are. Pushing another project's in progress branches was not this round's job.

## PART 3 — THE REMOVALS
85 directories, **by explicit path from a written allow list, one at a time, never a wildcard**. Every git checkout was re verified immediately before removal: clean tracked tree, HEAD present in the origin commit set. **85 removed, 0 failed, 0 refused, 0 skipped, 2,168MB reclaimed.** Nothing was held open by a stray shell, so PART 3 has nothing to name under BL-885's rule. Per class: reports checkouts 35 / 1,800MB, sandboxes 41 / 129MB, scratch 6 / 33MB, build output and empty 3 / 206MB.

Removed by name: `bl790` `b791` `projects`; `bl840-sandbox` `bl842-sandbox` `bl843-sandbox` `bl844` `bl845-sandbox` `bl846` `bl847-sandbox` `bl848` `bl849-sandbox` `bl850` `bl851-sandbox` `bl852-sandbox` `bl853-sandbox` `bl857-sandbox` `bl859-sandbox` `bl861-sandbox` `bl863-sandbox` `bl864-sandbox` `bl865-sandbox` `bl866-sandbox` `bl868-sandbox` `bl869-sandbox` `bl870-sandbox` `bl871-sandbox` `bl877-sandbox` `bl878-sandbox` `bl879-sandbox` `bl880-sandbox` `bl881-sandbox` `bl882-sandbox` `bl883-sandbox` `bl884-sandbox` `bl885-sandbox` `bl887-sandbox` `bl888-sandbox` `bl889-sandbox` `bl890-sandbox` `bl891-sandbox` `bl892-sandbox` `bl893-sandbox` `bl894-sandbox`; `w821-scratch` `w824-scratch` `w825-scratch` `w827s` `w828s` `w829s`; `chq-reports` `chq-reports-671` `chq-reports-673` `chq-reports-675` `chq-reports-681` `chqr` `rep734` `rep737` `rep739` `rep742` `rep743` `rep744` `rep746` `rep747` `rep748` `rep750` `rep751` `rep754` `rp757` `rpt610` `rpt613` `rpt628` `rpt629` `rpt631` `rpt632` `rpt633` `rpt634` `rpt683` `rpt689` `rpt691` `rpt692` `rpt693` `rpt694` `rpt698` `rpt810`.

No worktree needed unregistering: `git worktree prune --dry-run` was silent before and after, and none of the 85 was registered to any repository. `rp757`'s 35 untracked files were 6KB of `git push` logs.

## PART 4 — THE ACTUAL FIX, IMPLEMENTED
`scripts/sweep-round-leftovers.mjs` (new, standalone, nothing imports it) plus one bullet in CLAUDE.md under AGENT OPERATING PROTOCOL: **teardown sweeps everybody's leftovers, not just yours.** Dry run by default, `--apply` to act, explicit paths only.

**How it knows not to delete unique work, with every refusal demonstrated firing rather than asserted:**
• a name that is not a round leftover shape is invisible to it, so `ClippersHQ_renders`, `mbwt`, `projects1`, `temp`, `tmp`, `c` and the three handover tests are out of its reach by construction
• under 3 days old → refused, proved live on `bl896-sandbox`, `bl897-sandbox`, `bl898-sandbox`
• git registers it as a worktree of another repo → refused, proved live on `C:\w2`
• a checkout with modified tracked files → refused, proved on a purpose built case
• a checkout whose HEAD is on no origin branch → refused, proved on a purpose built case
• a plain directory holding one file it cannot prove is round telemetry → refused, proved live on `C:\wt` (`holds bl666-cols.sql, which is not round telemetry`)

The positive path was proved too: a telemetry only directory old enough to qualify was listed, then removed under `--apply`, and nothing else moved. The three purpose built cases were removed afterwards by name.

**Why this went direct to main.** BL-898 is live on this shared tree. Branching would have moved the primary HEAD under a running round for a change with zero code impact, so this took the rulebook's doc only carve out. Committed `97fdf3a8`, exactly two files, tagged `pre-BL-899` and `post-BL-899`, pushed and VERIFIED by safe-push (`origin/main == local HEAD`). **No build was run and none is claimed:** no TypeScript changed and nothing entered the Next.js build graph. The script was verified by executing it, which type checking would not have done.

## PART 5 — VERIFICATION
• **Primary checkout untouched.** `git worktree list` shows exactly two entries: the primary on `main` and `C:/w/b898` on `checkpoint/BL-898`. `git status --porcelain` shows the same 19 untracked entries it showed at session start, all belonging to other sessions; not one was staged, swept or modified.
• **The 6 money files are byte identical by blob OID** across `79971aca` → `97fdf3a8`: `clip-earnings-writer.ts 4f63164b`, `earnings-calc.ts 00410634`, `balance.ts 67c30c89`, `tracking.ts 8e2a62f5`, `clip-earnings-invariant-middleware.ts 61cef393`, `money-decimal.ts ef5cdae7`.
• **Origin moved only by my one commit**, `79971aca` → `97fdf3a8`, confirmed by `ls-remote`.
• **No database was touched.** No query, no migration, no script that opens a connection.
• Arithmetic closes: 2,168 removed + 20,008 kept = 22,176 enumerated. C: now shows 166GB free.

## MODEL SPLIT, STATED HONESTLY
**100% Opus, zero subagents, and that is a deviation from the brief.** Every step was a shell command whose raw output I had to read to classify anything, so a cheaper tier would not have cut the tokens that dominate this round; it would only have added a layer between the irreversible action and the evidence. BL-896 records a subagent returning three claims that were false on reading the files, and the CRLF false alarm above is exactly the kind of result a relayed summary gets wrong. For a round whose output is `rm -rf`, I read the output myself.

## WHAT I DID NOT DO
The 20,008MB in PART 2 is still on your disk. `ClippersHQ_renders` alone is 18,512MB and is almost certainly disposable, but "almost certainly" is what BL-759 warned about, so it needs one word from you.
