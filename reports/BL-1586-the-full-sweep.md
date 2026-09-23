# BL-1586 (INTERIM, 4 of 8 territories returned): the grading loop has worked once, its pages are now deleted, and "never contacted" was never measured

**Round:** BL-1586 · **read-only sweep, $0.00, no vendor call** · INTERIM checkpoint published at the
halfway mark; the final version replaces this file at the same path. · Paths redacted (`<Desktop>` is the
OneDrive Desktop). · Accounts are never named.

**Status of the eight territory agents at this checkpoint:**
- **Returned:** T1b (dead code), T2 (gate wiring), T4 (client side), T7 (reserved dissent).
- **Still running, reported here as ABSENT, not zero:** T1a (dead fields), T3 (clipper path and money),
  T5 (money and safety guards), T6 (deletion).

## The paragraph (interim)

The system's biggest hole is not in its code. **The loop that carries his judgement back has worked
exactly once**, and this round found the four pages waiting on him deleted from the Desktop:
- 5 review pages (423 cards) have been put in front of him since BL-1572, and 1 page (100 cards)
  came back, with a reason on 0 of them [T7_01].
- The MARK column of his workbook is filled on 0 of 3,028 rows [T7_01].
- The four ungraded pages and their manifests are gone, and so is BL-1584's KEEP sheet [F00]. Only the
  one page that was already graded had been vaulted.

**The fact every round has leaned on, "not one address ever contacted", is a label, not a
measurement.** This repo's own `docs/NO_SEND.md:13` says he runs *"a separate tool that sends leads
daily and closes clients"* outside this repo. The nine outcome columns are empty because nothing ever
fed his tool's log back, not because nobody was contacted [T7_02]. The cheapest high-value action in
the project costs $0: ask him whether his tool has mailed addresses from these sheets, and whether it
can export who replied.

## 1. What this system is, for a reader with no context

ClippersHQ walks TikTok and Instagram hashtags, reads bios, keeps addresses, and delivers them to one
operator who wants **faceless editor channels only, no creators, no businesses**, and never wants a
real editor wrongly cut. A second "client" half finds people who might pay for editing (musicians,
streamers, meme pages). He asked for *"a really big investigation of the whole system -- find holes,
things not working but pretending to work, things we don't need -- focus most on clippers, and
clients too."*

## 2. Things that pretend to work (so far)

| # | finding | bucket | measured by | cost to him |
|---|---|---|---|---|
| F00 | the 4 ungraded review pages + 4 manifests and BL-1584's KEEP sheet are gone from disk; the Recycle Bin is empty; only the already-graded page was vaulted | DANGEROUS | 35 of 44 store files present at round start vs BL-1585 close; name search to depth 9 | the only route to measuring editor loss (110 cut cards) is gone; a new page must be drawn |
| M01 | **his entire clipper path is round-numbered scratch code.** Walker, dedup-guard wiring, craft cut, delivery, sheet: `scratch/bl1584/walk.py:113,144,195` wires the guard; no production launcher reaches `email_harvester` | DANGEROUS | AST reachability (T1b) + grep + reading the walker | each round copies and edits the last round's walker, with no test on the composition; this is how craft_cut, looks_agency and the creator gate hid |
| T2_02 | `page_rules` (his own quoted "50-60% of videos must be the kind we want / last post two years ago is dead" rule) has **0 production callers** | VALUABLE | AST and grep both true zero | the share-of-videos half of his rule runs nowhere |
| T2_01 | `main.py`'s whole niche/quality/vision stack is confined to a run path his recent walks never touch; `niche_fraction` and `vision_verdict` have 0 callers even there | harmless today | AST call graph | none now; it misleads anyone reading `main.py` |
| T4_02 | `meme_finder.py:8913` hardcodes `"lead_kind": "clipper"` on meme pages. Diagnosed by BL-1445 and BL-1432, never fixed; 8 rows since 08-31 mislabelled | VALUABLE (one line) | read at `:8913`, orchestrator-verified | every census by `lead_kind` misclassifies them, growing each run |
| T1b_03 | the client-intake / delivery / assignment / brief modules have 0 production callers; their validators run only in `tests/` | DANGEROUS if the client half is ever used | AST BFS + grep + `tools/no_caller_sweep.py:379` | 15,173 client rows have no tracked validation path |
| T1b_06 | `triage.py` (the token guard for the judge) is wired into nothing, by its own docstring | VALUABLE | AST + `judge_batches.py:14` | judge-token spend (priced by T3, still running) |
| T2_04 | nothing has written his workbook since BL-1579 (file mtime 2026-09-21 15:11); every later round delivered a one-off Desktop sheet | DANGEROUS | workbook properties + grep of every scratch round | 1,322 delivered rows (514 + 808) never reached his working sheet; BL-1584's is now deleted |

**Re-measured and downgraded:** T2_03 said the weak production address normaliser lets duplicates
through. On master's 15,583 real address tokens it misses **0** duplicates that the stronger guard
would catch (the control fires) [M02]. That is harmless today.

## 3. The client side (T4), first audit in twenty rounds

- `lead_kind=client` is a real, explicitly stamped label: 15,173 rows, 8,719 addressed, 57.46%
  [56.68–58.25]. `docs/FACTS.md`'s split reproduces exactly; the brief's "10,164" does not reproduce
  under any definition tried.
- **All five client funnels are wired and all have been silent 24–54+ days.** The last client master
  row is dated 2026-08-30.
- **No grade of any client row exists anywhere in `ground_truth/`.** "Is this client worth pitching?"
  is UNTESTABLE, not untested.
- The `writer.py:363-367` citation repeated for weeks is stale; the source catch-all is now at
  `writer.py:443-446`.

## 4. The reserved agent (T7): three findings that disagree with the brief

1. **The grading loop's throughput is one page.** Three open decisions are now bound to files that no
   longer exist: the Instagram pause (its pre-registered rule names the deleted 50-card page), BL-1585's
   recommendation, and "dm for" ranking. DANGEROUS.
2. **"Never contacted" was never measured.** BL-1559 said it could not prove it. 10 later reports state
   it as fact, and 0 of 26 carry the caveat. The intake to record real outcomes already exists and has
   never been fed (`outcomes.mark_sent_from_csv`, `outcomes.py:345`). DANGEROUS.
3. **His "EDITOR" grade does not mean "for hire".** Only 32 of the 82 accounts he graded EDITOR,
   39.0% [29.2–49.8] [HIS], show any for-hire wording in their bio (broad pattern). Every KEEP rate
   measures "edits video", not "will take paid work from him". VALUABLE, and **not a cut**: cutting on
   it would remove 61% of his editors.

## 5–8. (final report)

The ranked list, what can be deleted, the money and guard audit, and WHAT I GOT WRONG land in the
final version of this file.
