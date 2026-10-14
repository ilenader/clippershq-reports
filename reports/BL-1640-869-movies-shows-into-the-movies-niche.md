# BL-1640: the 869 "other movies / shows" library rows are now in the movies (superhero) niche ($0)

2 APP order `2026-10-14_1135_MOVE-869-movies-shows` (P2). The owner said TV series and movies count (BL-1639).
Money: **$0** (no model call).

| # | Item | Result |
|---|---|---|
| 1 | **Moved** | **869 / 869** library rows `out_of_scope:other_movies_shows` -> `superhero` (the movies / superheroes niche). 0 left; superhero rows 3,976 -> 4,845. |
| 2 | **What they are** | All 869 are **old-Drive inventory** (`source = old_drive`, approved "pre-review", **no local file**: path empty, the file sits in his Drive folder). So nothing moved on disk; only the library's niche changed. None was ever sent. |
| 3 | **Undo** | One transaction; one `scope_log` row each (kind `library`, cls `owner_movies_count`, prior niche kept), so every row can be put back. Script: `scratch/bl1640/move_movies_shows.py` (refuses to run if any row has a local file). |
| 4 | **Safety** | Before any Send, the BL-1636 gate checks each video's picture again. Since BL-1639 a film / series edit passes as superhero, and anything that is really another niche is gated and relabelled. |

- 11:50 FINDER BL-1640 869 movies/shows rows -> superhero niche, logged + undoable, $0 (DONE)
