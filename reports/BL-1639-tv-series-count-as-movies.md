# BL-1639: TV-series edits count as "movies" -- the send gate now agrees with the AI reviewer ($0)

2 APP order `2026-10-14_1056_ANSWER-tv-series-count` (P2). His answer (10:55): **YES, TV-series edits count as
"movies"**. Money: **$0** (no model call).

| # | Item | Result |
|---|---|---|
| 1 | **AI reviewer (BL-1637)** | Already counted films **and** series (`film_tv`) as the movies / superheroes niche. Only the spec text changed. **No score changes**: ground truth, the fresh-set grades and audit #1 (240 / 240, a159 / a066 counted right) all stand. |
| 2 | **Send gate (BL-1636)** | The niche check said **NO** to a film / series edit in a superhero send, and relabelled it `out_of_scope:film_tv`. Now `niche_of()` maps `film_tv` -> `superhero` for both the verdict and the relabel. Cached answers are re-judged from their stored subject, so no new calls are needed. |
| 3 | **Re-scored what changed** | The library had **1** row the gate had filed as `out_of_scope:film_tv` (BL-1636's basketball check). It is back in **superhero**: file moved to the Superhero folder, logged in `scope_log`, undoable. |
| 4 | **Not changed (flag)** | **869** library rows are filed `out_of_scope:other_movies_shows` by the older account-scope rule (BL-1604: superhero = Marvel + DC). Under his answer, many may belong to the movies niche. Moving them is a scope decision (discovery scope words too), so it is left for him / the prompter. |
| 5 | **Tests** | `tests/test_bl1639_film_is_superhero.py` (2): the gate says YES in a superhero send and NO in a basketball send; the relabel goes to superhero; the AI reviewer files a film / series YES as superhero. `run_all -k test_bl1631*,test_bl1636*,test_bl1637*,test_bl1639*`: **4/4 green, 38 checks.** Live app restarted through `restart_app` (the friend was idle 2.5 h). |

- 11:25 FINDER BL-1639 TV series = movies: send gate + reviewer agree, 1 library row back to superhero, $0 (DONE)
