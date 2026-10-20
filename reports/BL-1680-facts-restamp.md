# BL-1680: FACTS.md lifetime spend re-stamped before the commit guard refused anything -- drift $6.79 (91.8% of $7.40) -> 0.0% ($0)

3 FIXER, 20 Oct 05:30. Seen in BL-1679's commit: `facts_guard` printed lifetime drift **$6.79, 91.8% of the $7.40 limit**.
One more paid run would have made the pre-commit guard refuse commits in every window.

| # | Item | Result |
|---|---|---|
| 1 | **Re-stamp** | `scratch/bl1634/restamp_facts.py --round BL-1680`: one live read of spend.json (`updated 2026-10-18 19:42:47`, **47,718** rows), recomputed from the rows. Table + machine block + a BL-1680 note in docs/FACTS.md. Lifetime **$245.209595** (TikTok 171.602224, Instagram 55.304186, Vision 17.007985, TikHub 1.294000). |
| 2 | **Guard after** | `.venv` facts_guard: **OK, 35 facts**, drift **0.0%** on every column, row lag +0. (The system Python cannot import `main`, so it reports 5 facts UNCHECKED -- run the guard with `.venv`.) |
| 3 | **Nothing paid running** | 1 LEADS NOW_PLAIN: "nothing paid running" at 05:18, so the read is not mid-run. |

Next re-stamp: when a commit's facts_guard line shows drift above ~80% of $7.40.
