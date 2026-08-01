# INFRA-009 — Qualified settings ids, 23 curated with 43 folded away, danger lines that read differently. And the static mount was silently disabling the Start panel

**Date:** 2026-08-01 · **Type:** Frontend · **Spend:** **$0.00** — no paid call
Claimed as INFRA-009 · `dashboard/` only · campaigns SHA `8e02f8d6f6307ae8` · config 162 keys
Verified in a real browser against the live server, not a fixture.

---

## What it looks like now

The Settings tab, served from `GET /`, nothing opened by hand:

- the **MusicBrainz run-level warning** at the top, in its own card
- **THE 23 WORTH CHANGING**, every id qualified — `spotify_finder.run_target` (700),
  `twitch_finder.run_target` (500), `youtube_finder.run_target` (50),
  `repost_finder.run_target` (50), all four distinct and all four correct
- three **Careful:** blocks, set off by a left rule, under the knobs they belong to
- **Advanced — the other 43 (rarely touched)**, closed
- one visible panel of six

Screenshot: `scratch/infra009_settings.png` (committed).

## 1. Qualified ids

`data-key` now carries the qualified id the API uses. Measured in the browser: **11 of 66
settings carry a dotted id**, and the four `run_target`s resolve to four distinct entries.
Under the old bare-name scheme they collapsed into one showing repost's 50 — and Spotify's
danger note went with it, which is the single line on the page you most need to see.

## 2. 23 curated, 43 behind a disclosure

| | |
|---|---|
| curated rows rendered on arrival | **23** |
| advanced rows | **43** |
| advanced rows **open** at rest | **0** |

Tier membership is read from `_curated` / `_advanced`. A config key never begins with an
underscore, so stripping the meta keys cannot drop a real setting, and the flat contract is
untouched — the page still reads `{id: {value, consequence, …}}` exactly as before.

There is a deliberate fallback: if the server ever stops sending tiers, the page renders one
flat list rather than 66 knobs in a card claiming to be "the ones worth changing".

## 3. The danger line reads differently — by three signals, never colour

`consequence` says *this changes X*. `danger` says *this costs you 17 points*. They must not
scan as the same sentence, so the danger line is its own element with its own class, and
differs by **a left rule, a heavier weight, and a literal `Careful:` prefix**.

Three signals, and the prefix is real text — so it survives a monochrome display,
`forced-colors: active` (where the rule is pinned to `CanvasText`), and a screen reader
equally. Nothing here depends on colour.

Both lines join the **same `aria-describedby`**, so the warning is part of the control's
*description* and never its accessible *name* — otherwise it would be re-read on every focus
and could not be silenced.

Rendered: **4 danger elements** — the three knobs plus the run-level warning.

- `spotify_finder.run_target` — above ~777 forces expansion at a **measured 17-point
  handle-rate penalty**
- `clip_max_pages_per_account` — at the old default, **95.5% of the library from two accounts**
- `clip_round_robin` — off reaches **17 of 41 pages**
- run-level: two concurrent Spotify runs breach MusicBrainz's 1 req/sec, **because the limiter
  is process-local**

The run-level warning is deliberately **not** a disclosure. It is the one thing on this panel
you cannot afford to have folded away.

Two smaller corrections fell out of rendering the real list: booleans (`clip_round_robin`,
the four `*_enabled`) were being drawn as **number inputs** and are now checkboxes; and an
unset knob now says **"(not set — using the default)"** instead of showing an empty box,
because unset is not the same as off.

## 4. `GET /` — already fixed, and it was hiding a second bug

A concurrent round had already mounted `dashboard/static` at `/` with the same
mounted-last reasoning. I removed my duplicate rather than leave two, and committed their
change, which was sitting uncommitted in a file I had to touch. `GET /` returns **200**,
`app.js` and `app.css` serve, and `/api/health` still wins over the mount.

**But the mount was silently disabling the Start panel.** `StaticFiles` at `/` answers *any*
unmatched GET, so `GET /api/start` — a POST-only route — returned **404 from disk** instead of
the 405 the capability probe expected. The probe concluded the endpoint was missing and Start
shipped **disabled against a live backend**, which is precisely the failure the probe was
written to prevent, reintroduced by the fix for a different bug.

A POST probe fixed the logic but left a **400 in the console on every load** — asking a
question you expect to be refused is still a failed request in the network log. So the page
now infers the capability from `funnels`, which `/api/now` already returns: **no extra
request, no console noise**, and one less thing to keep in step.

```
before: Start disabled, 1 console error (404)
after : Start enabled  (0 of 4 controls disabled), 0 console errors
```

## 5. Everything frozen stayed frozen

Measured in Chromium against the live server, after visiting all six tabs:

| | |
|---|---|
| tabs / tabpanels / visible | **6 / 6 / 1** |
| `<details>` in the DOM | 6 |
| `<details>` open at rest | **0** |
| live regions | 2, **both outside every tabpanel** |
| elements loading http(s) | **0** |
| off-origin requests | **0** |
| `:focus-visible` rule present | **yes** |
| advanced disclosure across a poll | open **1 → 1** |

That last row is the in-place poll doing its job: the refresh rewrites the panel without
slamming shut a section you opened.

---

## Verification

| check | result |
|---|---|
| qualified ids resolving | 11 dotted, **4 distinct `run_target`s** |
| curated / advanced | **23 / 43**, 0 advanced open at rest |
| danger lines distinct | 4 rendered; rule + weight + `Careful:` prefix, no colour dependency |
| Spotify 777 warning visible without opening anything | **yes** |
| run-level MusicBrainz warning | present, above all knobs |
| `GET /` | **200**, assets serve, API still wins |
| Start panel | **enabled**, 0 console errors |
| frozen structure | 6/6/1, 0 open, live regions outside panels, 0 external requests |
| screenshot | `scratch/infra009_settings.png` |
| campaigns SHA | `8e02f8d6f6307ae8` **MATCH** · config 162 keys |

## Honest limits

- **Nothing saves.** The page renders `data-key` and `data-type` on every input, but there is
  no handler that PUTs them — `/api/settings` accepts writes and the UI never sends one. That
  predates this round and was not in scope, but a settings page you cannot save from is worth
  naming plainly.
- **The suite ended 1 red, and it is not mine.** `test_clip_pipeline.py` — an untracked suite
  from a round in flight — fails on its own AST guard tripping over the word `speech_frac`
  inside a docstring. I touched only `dashboard/`.
- **I committed another round's uncommitted static mount.** It was in `server.py`, which I had
  to edit to remove my duplicate, and leaving it unstaged risked it being lost.
- **The 23/43 split is INFRA-006's judgement, not re-litigated here.** If a knob you reach for
  is in the advanced fold, that is a curation call to revisit on the backend, not a rendering
  bug.
- **`consequence` text is not wrapped or truncated by the page.** Two of the curated lines run
  to two visual lines at 1180px. They are still one sentence, which is the rule that mattered.
- **Screenshot is one viewport width (1180px) in light mode.** Dark mode and narrow widths are
  covered by existing CSS but were not re-shot this round.
