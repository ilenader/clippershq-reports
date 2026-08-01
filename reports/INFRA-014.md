# INFRA-014 — The Now tab stops fabricating, and the numbers you actually track are on it

**Date:** 2026-08-01 · **Type:** Fix + feature · **Spend:** **$0.00** — no paid call
Claimed as INFRA-014, six paths registered individually and verified · `dashboard/` + its own
test file · suite **84 of 86** (both reds are other rounds', below) · campaigns SHA
`8e02f8d6f6307ae8` **MATCH** · config 162 keys

![Now tab](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/infra014/now.png)

---

## 1. `unknown` is not `$0.000`

`Number(null)` is `0`, and `0` is finite, so `money(null)` formatted a spend the backend never
sent. `/api/now` returns `"spend": null` for a marker that carries no spend field; the page
turned that into a claim that a live run had cost nothing while the ledger had it at `$0.015`.

The sharpest part is that `undefined` already did the right thing — `Number(undefined)` is
`NaN`, so it returned `null` and rendered a dash. **`null` and `undefined` took opposite paths
through one function** that has no reason to distinguish them.

`progressOf()`, ten lines below, already carries the rule: *"A null target must yield no bar,
never a fabricated percentage."* And the file header has said *"never a fabricated zero… on a
spend panel that is the difference between unknown and free"* since it was written. The
discipline was there; it had never been applied to this hole.

**Both directions are now proven, because collapsing them either way is the same bug:**

| run | backend | page |
|---|---|---|
| `repost_finder` (marker, no spend field) | `spend: null` | **unknown** |
| `repost` (run status, genuinely metered) | `spend_usd: 0.0` | **$0.000** |

The word is styled to not read as a measured figure — smaller, dimmed, non-tabular — and
carries no hidden alternative text, so the visible token and the announced one are the same.

## 2. The liveness check now covers both sources

`_pid_alive` ran over markers only. A per-run status file cannot correct itself for exactly the
reason a marker cannot: **the process that would rewrite it is the process that died.** That
asymmetry was never a decision — the run-status source arrived after the check was written.

Measured on the running dashboard: pid 15296, a `repost` run stamped 15:21, still reading
`running` at 18:09 with `elapsed 0.2s` frozen. It now reads *ended*, with its reason.

## 3. Reconciled by pid — not by name

**The obvious rule is wrong.** "Same funnel, therefore one card" would collapse two genuinely
concurrent repost runs into one, hiding a live run rather than a duplicate. Two records for one
pid are one run seen twice; two records with different pids are two runs, however alike their
names. Merging keeps the richer side — the run status has `run_id`, `target`, `cap_usd`; the
marker has `calls` and `pages` — and a value the primary already holds is never overwritten,
including an explicit null.

**A correction to my own INFRA-013.** I reported the duplicate card as "one funnel appearing
twice". It was not: the second card was the **dead** headless run. Fixing liveness removed it
on its own. Pid reconciliation is still right, and now proven by test, but it was not what
produced the screenshot I published.

Dead markers group by pid for the same reason — one process wrote the spotify, twitch and
youtube markers and then died, so that is **one** event and the page now says so rather than
printing it three times.

## 4. `idleLine()` is called

It existed, was never called, and the inlined version that beat it read `['summary','last']` —
two keys `/api/now` does not send — so every entry fell through to the literal word **"idle"**.
Four runs killed mid-flight said the same thing as a funnel that was never started.

Killed runs no longer sit behind a disclosure at all. They render above the fold with the
sentence the backend has been writing all along:

> **spotify_finder, twitch_finder, youtube_finder — ended**
> marker says running but pid 36740 has exited — a killed run cannot update its own marker.
> Treat as ended, not failed. All 3 were written by the same process, so this is one run that
> ended, not 3.

A stale row's own `status` still reads `running`, so the line says **ended** rather than
repeating the string the note exists to correct.

## 5. The standing numbers

New `/api/library`. The headline is pulled out of the list and written as a sentence, so it
differs from the other three by position, by being prose, by its prefix word and by a rule down
the left — four channels, none of them colour or size.

> **Needs attention:** 1,796 of 2,003 clips — 89.7% — match no mood, so no song can be chosen
> for them. The song store (4 songs) is the bottleneck, not the clip supply.

| | |
|---|---|
| clips in library | **2,003** |
| accounts | **172** |
| top-2 concentration | **10.3%** |
| vision-labelled | **74.8%** |

**These moved while I built it, and that is the story.** Vision labelling is running right now:
36.5% at INFRA-013, 53.4%, 64.4%, 66.3%, 74.8% across my own test runs this evening — and the
no-mood share fell with it, 94.4% → 92.5% → 90.7% → **89.7%**. The bottleneck is real but it is
being eaten into as we speak, which is precisely the thing a standing number tells you and a
report cannot.

**~1.9s to compute** (0.64 stats + 0.64 read + 0.60 matching 2,003 clips across 52 shards)
against ~0.01s for every other endpoint, on a 5s poll. It is cached on an mtime signature with a
60s floor, polled on its own 60s cadence, and says how old it is when it is over 90s.

**Which denominator (item 7), stated on the page:** *"Shares are of every clip in the standing
library, not one walk's contribution. Top: loste1980 6.1%, movies.avengers 4.2%."* I have not
chased the 10.3%-versus-1.8% discrepancy; the page now says what it is measuring so the two
numbers can be compared rather than confused.

**Videos:** `/api/videos` counted **55 files, 35 distinct** (`_v01`/`_v02` are variants of one
clip), broken down by directory, replacing the constant string *"Nothing yet — memebot is not
wired."* Nothing in the tree declares a video finished, so the definition is stated in the
response: a video file in an `out/` or `final/` directory.

## 6. The two figures that were computed and discarded

![Spend tab](https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/infra014/spend.png)

**estimated share 3.95%** — with the reason it decays, on the page:

> Share of lifetime spend that is reconstructed rather than metered. It falls as total spend
> grows even though nothing has become more measured — the estimated dollars are frozen.

It read 4.55%, then 4.00% when I measured it for INFRA-013, and **3.95%** by the time I finished
this round. Not one cent of it became better known.

**corrections −$0.1452** — routed through `moneyCell()`, not `money()`. `money()` emits a bare
U+2212, which is suppressed at default screen-reader punctuation levels, so a negative total
would have been announced as *"$0.1452"* — identical to a positive figure, opposite meaning.
This is the first negative value ever to reach that strip, so the hazard shipped live with this
change or not at all. Verified: the screen-reader text reads **"minus $0.1452"**.

---

## Three bugs caught in review, before they shipped

I had the planned markup reviewed before writing it, and three of the findings were correctness
bugs that would have produced **confidently wrong numbers rather than visible failures**:

1. **The strip could not go inside `#now-live`.** `renderNow()` updates cards *by position* —
   `box.children[i]`. A strip prepended there becomes `children[0]`, so the first funnel's
   progress and spend would have been written into the standing figures, successfully and
   silently, and the last funnel would have fallen off the end. It sits in a sibling container,
   the same precedent as the save bar living outside `#set-groups`.
2. **`statsOf()` returns a variable-length array aligned to fixed cells by position.** Progress
   only appears when a target is knowable; leads only when the field exists. The alignment was
   correct by luck — and my own change, making spend *always* render, was exactly the kind of
   edit that shifts it. Cells are now matched **by label**, rebuilt when the set changes, and
   the `querySelector('b')` deref is guarded (unguarded, one missing node throws inside the
   `forEach` and every later card silently freezes at a stale value).
3. **`nowKey` omitted `status`.** A run going stale could leave the key unchanged, take the
   in-place branch, and go on saying "running" — the exact bug this round exists to remove.
   Both lists are now keyed by a signature including status and staleness.

## Verification

| check | result |
|---|---|
| null spend renders | **unknown** (and a real metered 0.0 still renders `$0.000`) |
| dead headless pid | moved out of `running`, reads **ended**, note shown |
| one card per process | 2 cards, **0 duplicate names**, no two share a pid |
| four standing numbers | live on the page, headline as a sentence |
| videos count | **55** (35 distinct), by directory |
| estimated_pct / corrections_total | both rendered; negative survives a screen reader |
| strip is outside `#now-live` | yes · not a live region: yes |
| page errors | **0** |
| dashboard tests | **72** (13 new) |
| full suite | 84 of 86 |
| campaigns SHA | `8e02f8d6f6307ae8` **MATCH** · config 162 keys · live config untouched |

## Honest limits and corrections

- **A test caught me shipping the same bug this round is about.** `clip_library.stats()` answers
  `0 clips` quite happily for a path that does not exist, so `/api/library` reported **`clips: 0`**
  for a missing library — a confident "the library is empty" where the truth was "I could not
  find it". A missing directory now returns nulls with a reason; a genuinely empty library
  returns `0` with every *share* still null, because there is no population to be a share of.
- **I nearly reported a false campaigns-SHA mismatch.** My first check hashed with compact JSON
  separators and produced `7a029ee5447cddd8`. The repo's own method uses default separators;
  with it the hash is `8e02f8d6f6307ae8`, MATCH. The config never moved — my checker did.
- **Two suites are red and neither is mine.** `test_claims_manifest` fails on MEMEBOT-028's
  `scratch/memebot028_*.py`, which are claimed but not committed at HEAD. `test_filelock` passes
  standalone **twice** and flakes only under full-suite load (27 python processes were running);
  it is the same load flake INFRA-002 and INFRA-012 recorded. Neither suite exercises dashboard
  code, and `git status` shows I touched neither file.
- **The standing numbers are a moving target.** Every figure above changed during the round
  because labelling is in flight. They are correct as measured, not as constants.
- **`no_mood` depends on a rule that is being edited right now.** MEMEBOT-022 is changing the
  mood map and title matcher this hour. `match()` returns `(mood, tier, matched_on)` and never
  returns `None`, so what is counted is a null **mood** — not a null return, which is what an
  earlier reading of mine got wrong.
- **`_reconcile` merges the marker as primary.** When a marker and a run status describe one pid,
  the marker's funnel name wins the card title, so a card can be labelled `repost_finder` while
  carrying a `run_id` from a run that called itself `repost`.
- **I did not fix the raw-key setting labels or the empty History tab** — both named in
  INFRA-013, neither in this round's scope.
- **One accessibility item is deferred:** a failed poll still leaves standing figures looking
  current. For a progress bar that self-corrects in 5s; for a figure quoted in a decision it
  could sit stale longer. Nothing announces the staleness yet.
