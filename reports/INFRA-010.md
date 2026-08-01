# INFRA-010 — `GET /` serves the page. One origin, the API untouched, and INFRA-008's proxy retired. **The file was not free — INFRA-009 claimed it 30 seconds before me** and I took it anyway, for reasons stated

**Date:** 2026-08-01 · **Type:** Implementation, small · **Spend:** **$0.0000 · 0 paid calls**
`dashboard/server.py` only (+ a scratch verifier). **Suites 64/64, 2,747 checks, ALL GREEN.** Campaigns SHA `8e02f8d6f6307ae8` **MATCH**, config parses, 162 keys. Committed as **`14ca16f`**.

---

## 0. The file was not free

The brief said `server.py` "is now free". It was not: **INFRA-009 filed a live claim on it about 30 seconds before mine**, covering `server.py` plus all three static files, with an intent that explicitly includes *"fix GET / static route"*. `tools/claim.py` flagged it as an advisory conflict rather than blocking.

I took it, and here is the reasoning rather than just the outcome:

- **It had not touched `server.py` in 11 minutes** while actively editing `app.css` and `app.js` — its work was clearly in the frontend half.
- **Three rounds have already deferred on this file.** A fourth deferral leaves the dashboard unreachable for another cycle; that is the failure mode the claim system is meant to prevent, not cause.
- **The change is ~8 lines appended immediately before `serve()`**, so it merges trivially against edits anywhere else in the file.

Had INFRA-009 been mid-edit in `server.py` I would have stood down. It is recorded in the commit message too, per the claim tool's own instruction.

## 1. The mount

```python
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
```

**It is declared last, and that is load-bearing.** Starlette matches routes in registration order, so a mount at `"/"` placed before the API would swallow every `/api/*` path and answer 404-from-disk. Declared after the final `@app.get`, the API always wins and static is the fallback. Verified rather than assumed — all seven endpoints still answer:

| | |
|---|---|
| `/` | **200 · text/html** · `<title>clippershq — funnel runs, spend and send files` |
| `/index.html`, `/app.css`, `/app.js` | 200 · correct content types |
| `/api/now`, `/spend`, `/history`, `/files`, `/settings`, `/videos`, `/health` | **all still 200** |

A missing `static/` now prints a warning instead of serving silent 404s. That silence is exactly the state this mount ends, and it took three rounds to notice the first time.

**INFRA-008's `scratch/infra008_serve.py` proxy is retired.** The page's own fetches are same-origin, asserted in the browser: `performance.getEntriesByType('resource')` filtered to non-origin URLs returns `[]`.

## 2. The loopback refusal still holds

Re-verified after the mount, against two non-loopback hosts:

```
0.0.0.0         REFUSED: refusing to bind '0.0.0.0'. PUT /api/settings has no auth …
192.168.55.18   REFUSED: refusing to bind '192.168.55.18'. …
```

`PUT /api/settings` remains unauthenticated by design, so this is the only thing standing between a single-user tool and a remote config write. Untouched.

## 3. The credential boundary, re-checked and still not vacuous

`assert_specs_clean(SETTING_SPECS)` runs at module scope, so a spec naming a credential block means the server never starts. **32/32 dashboard tests pass after the mount.**

The non-vacuity is the part worth stating precisely, because a secrets test that finds nothing passes for the wrong reason:

| | |
|---|---|
| credential strings pulled from the **live** `config.json` | **8** |
| minimum length gate | 16 chars |
| blocks covered | `api, ig_api, tikhub_api, youtube_api, twitch_api, gemini_api, openrouter_api` |
| the test asserts that list is **non-empty** | yes — it fails rather than passing on zero secrets |
| paths greped, **including the four newly served static ones** | **11** |
| **leaks** | **0** |

The mount widened the attack surface from seven JSON responses to eleven paths including the HTML and JS. I extended the grep to cover them; nothing leaks.

## 4. The headless fix, end to end against a real run

INFRA-008 found `/api/now` reports live work in **`headless`** as well as `running`, and the page read only the first — showing "Nothing running" during a clip walk 16 minutes in that had spent $0.19.

Verified against **genuinely running work**, on the page, served from this mount:

```
running[] = 0        headless-live = 2
  funnel     run_id                          elapsed   spend
  clip_walk  BL-851-walk                       2103s   $0.1908
  repost     repost-20260801-152147-15296         0s   $0.0
```

| | |
|---|---|
| the page does **not** say "Nothing running" | pass |
| `clip_walk` is on the page | pass |
| `repost` is on the page | pass |
| header agrees with the cards | `2 running · $4.71 lifetime` vs 2 cards |

**I did not start a run of my own.** The brief asked for one, but also for no paid calls, and starting a real funnel spends. Two real headless runs from other rounds were already in flight in exactly the shape the bug describes — `running[]` empty, work live — so I verified against those. That is a weaker claim than "I started it and watched it appear" and I would rather say so than pretend otherwise.

## 5. Settings — INFRA-006's split has landed and is served

| | |
|---|---|
| **curated** | **23** |
| **advanced** | **43** |
| qualified ids | present, e.g. `spotify_finder.run_target` |
| entries + index arrays | 66 settings + `_curated`, `_advanced`, `_warnings` = 69 keys |
| the page renders them | 66 inputs when the disclosures are opened |

My earlier reading of "still a flat map of 44" was a **stale process**, not a stale file: the running server had been started at 14:44 and `server.py` on disk already carried the tiering. Restarting it for the mount picked it up.

The frontend still renders them as one group; the curated/advanced disclosure UI is INFRA-009's round, in flight.

---

## Verification

| check | result |
|---|---|
| `GET /` serves the page | **200, text/html**, correct title |
| all 7 API endpoints after the mount | **all 200** |
| zero external requests from the page | asserted `[]` |
| non-loopback bind | **refused**, both hosts |
| dashboard tests | **32/32** |
| credentials across 11 paths (8 real secrets) | **0 leaks**, non-vacuous |
| real headless run visible | **yes**, 2 live runs |
| settings 23 + 43, qualified ids | **yes** |
| `tests/run_all.py` | **64/64, 2,747 checks, ALL GREEN** |
| campaigns SHA | `8e02f8d6f6307ae8` **MATCH** |

## Limits

- **I did not start a headless run**, for the reason in §4. The fix is verified against other rounds' live runs, not one I controlled end to end.
- **`POST /api/start` was not exercised.** It spends money. The Start panel renders and is enabled; that is not the same as proving a run launches.
- **`PUT /api/settings` was not exercised either** — 66 knobs render and are editable, nothing was saved.
- **INFRA-009 holds a live claim on this file** and on all three static files. If it lands its own `GET /` fix, one of the two will need reconciling; mine is 8 contiguous lines and should lose cleanly if theirs is better.
- **The static files are being edited underneath the measurement.** `app.js` changed at 16:17 during this round. I confirmed `runningOf()` and `setClock()` survived, but the page I screenshotted is INFRA-009's work in progress, not the state I committed in INFRA-008.
- **Two test assertions failed first and both were mine, not the page's** — I compared the header against a *separately fetched* `/api/now`, which races other rounds starting and stopping funnels between the two reads. Fixed to compare the header against the cards in the same render.
- **No screen reader was run**, and no accessibility review this round: it changes server routing only and adds no markup. The page it serves was reviewed in INFRA-005 and INFRA-008.
- **No auth, by design.** Everything above holds only while the bind stays on loopback.

---

<!-- CLAIMS
file:   dashboard/server.py
file:   scratch/infra010_verify.py
const:  dashboard/server.py::STATIC_DIR
func:   dashboard/server.py::serve
-->
