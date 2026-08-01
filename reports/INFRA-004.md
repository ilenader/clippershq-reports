# INFRA-004 — The dashboard backend. Every endpoint on live data, zero credential strings in any response, and a "what's running" panel that would have lied on 3 of 4 rows

**Date:** 2026-08-01 · **Type:** Feature + live proof · **Spend:** **$0.0000** — no paid call
Claimed as INFRA-004 · `dashboard/` only, no `clippershq` module edited
Suite **61/61, 2,591 checks** (+24) · campaigns SHA `8e02f8d6f6307ae8` · config 162 keys

Built to the [INFRA-003](INFRA-003.md) contract. The frontend is being written against these
shapes in a parallel round, so **nothing was redesigned** — every field name is as specified.

---

## What shipped

`dashboard/server.py` — FastAPI, loopback-only, ~450 lines. `tests/test_dashboard.py` — 24
tests. Nothing in `clippershq/` was touched, and the server adds **no state of its own**: it
reads the same files the menus read.

| endpoint | live result |
|---|---|
| `GET /api/now` | 5 markers read · **0 running, 5 idle** after staleness detection |
| `GET /api/spend` | lifetime **$4.4950**, metered $4.3048, estimated $0.1902, **2 corrections totalling −$0.1452** |
| `GET /api/history` | **0 runs of 133 ledger rows**, with the note explaining why |
| `GET /api/files` | primary `ALL_BOT_READY.csv` + **40 labelled decoys** |
| `GET /api/settings` | **44 allowlisted knobs**, each with its consequence string |
| `PUT /api/settings` | allowlist-checked, atomic write |
| `POST /api/start` | **real pid 15296**, alive 3 s later |
| `GET /download/{name}` | allowlisted by directory listing |
| `GET /api/videos` | the memebot stub |

All verified over **real HTTP against a real uvicorn process**, not a test client.

---

## The finding: `/api/now` would have lied on 3 of 4 rows

The five funnels already emit `write_marker` status files, and the contract says to read them
and add no field. Read literally, the endpoint reported **4 funnels running**. Measured
against the OS:

```
spotify_finder   status=running   pid=32152  alive=False
twitch_finder    status=running   pid=32152  alive=False
youtube_finder   status=running   pid=32152  alive=False
clip_library     status=running   pid=22604  alive=False
```

**A killed run cannot rewrite its own marker** — that is the entire reason the completion
marker exists (BL-830). So `status: running` means "was running when last written", and a
panel that trusts it shows work that finished hours ago as in-flight.

The fix is a **derived** liveness check at read time: `status` is passed through verbatim so
the contract holds, and a new `stale` boolean says whether the pid is still alive. **No field
is added to the marker format on disk** — the constraint is respected; the derivation happens
in the reader, which is the only place it can happen. After it: **running 0, idle 5**, four
flagged stale with a note naming the dead pid.

Incidentally, those three `running` markers all carried pid 32152 — **the test-suite process**.
Importing `control` writes a RUNNING marker as a side effect, so running the suite leaves three
funnels looking live. That is worth knowing independently of this dashboard.

## The credential boundary

Enforced **at import**, not per request:

```python
secrets_guard.assert_specs_clean(SETTING_SPECS)     # raises -> server never starts
```

A per-request filter has to be right every time; a startup assertion has to be right once. On
top of it, `PUT` refuses any key that is a secret block, a secret leaf, or a secret field —
before `config.json` is opened.

**Proved, not asserted.** The test pulls every credential string out of the live `config.json`
via `secrets_guard.secret_values()` and greps **every endpoint response** for each one:

```
0 credential strings across /api/health /now /spend /history /files /settings /videos
```

The test also fails if no secrets are found, so it can never pass vacuously.

`GET /api/settings` returns only allowlisted knobs — `config.json` is never returned wholesale,
and none of the seven `SECRET_BLOCKS` appears in the response.

**Binding is part of the boundary.** `serve()` refuses any non-loopback host unless explicitly
forced, because `PUT /api/settings` has no auth by design: the tool is single-user and
localhost-only, and binding elsewhere silently turns it into a remote config write.

## Corrections stay negative

```
CORRECTION_bl842_double_count_242_calls_reversed   -0.1452   tag=correction
corrections total: -$0.1452 across 2 rows
```

Carried through untouched and tagged so the frontend can render them distinctly. A UI that
clamps at zero silently preserves an overstatement — which is exactly how a 100% double-count
hid in this ledger until it was found by hand. The sign **is** the signal.

`estimated` rows are separated by `spend_ledger`'s own flag rather than re-derived here, and
tagged `estimated`.

## History is thin, and says so

**0 of 133 ledger rows carry a `run_id`**, so the endpoint returns an empty list plus:

> *Shows only runs that carry a run_id. 133 of 133 ledger rows have none, so they cannot be
> attributed to a run and are omitted rather than guessed. run_id is stamped forward-only:
> rows written before it shipped can never be attributed, and master must be migrated before
> new rows carry it.*

No inference. BL-834 measured that attribution from timestamps is impossible (92.1% of rows
predate the ledger; 3.8% fall inside exactly one run's window), and a guessed attribution is
worse than an honest gap because nobody can tell it was guessed.

## Files: one to send from, 40 labelled decoys

`ALL_BOT_READY.csv` is flagged as primary with the warning that it *contains* the others, so
sending from a second file mails the same people twice. Every decoy carries what it actually
is — `LATEST_DM_LIST.csv` is "handles to DM, not emails"; the `*_SEND.csv` exports "predate the
current suppression rules". The danger this panel removes is not a missing file but a
**plausible** one: BL-787 measured 262 dead-MX addresses across 17 older exports.

`/download` allowlists by directory listing, not path arithmetic; traversal attempts and
`config.json` are refused (403).

## POST /api/start

Reuses INFRA-002's headless entry — no reimplementation. The cap check is duplicated only so
the browser gets a clean 400 instead of a subprocess exiting 2 with nothing to show.

```
POST {"funnel":"repost","target":2}              -> 400  "cap is required…"
POST {"funnel":"repost","target":1,"cap":0.01}   -> 200  queued, pid=15296, alive 3s later
```

The process was **terminated immediately**: the claim under test is that the endpoint launches
a genuine headless run, not that a funnel completes. **Spend before $4.4950 → after $4.4950,
delta $0.0000.**

---

## Verification

| check | result |
|---|---|
| every endpoint on live data | **7/7 over real HTTP** |
| credential strings in any response | **0** (test fails if no secrets exist to check) |
| secret blocks settable | refused (400/403) for all 7 |
| corrections negative + tagged | **−$0.1452**, preserved |
| history without run_id | 0 runs, note states why |
| absent marker | `unknown`, never `failed` |
| stale running marker | detected, 4 flagged, `running` 4 → 0 |
| POST without cap | **400** |
| POST with cap | **200, real pid**, spend delta **$0.0000** |
| non-loopback bind | refused |
| suite | **61/61, 2,591 checks** |
| campaigns SHA | `8e02f8d6f6307ae8` **MATCH** · config 162 keys |

## Honest limits

- **44 settings are exposed, not the 16 INFRA-003 describes.** I used control's own global
  spec lists — `_GLOBAL_TOGGLES` (30) + `_ADVANCED` (14) — because those are the outer
  allowlist the menus already trust. `_FUNNEL_FILTERS` (33 more) is deliberately excluded as
  per-run context rather than global settings. If 16 was a specific curated subset, it is not
  identifiable in `control.py` today and the frontend should expect 44.
- **`/api/now` reports headless runs from a second source.** INFRA-002's per-run status files
  are richer than the markers and are returned under a `headless` key. The frontend may ignore
  it; it is additive.
- **`progress` is only computable for funnels that write `pages` and `target`.** For the rest
  it is `None` rather than a fabricated fraction.
- **Staleness is checked by pid liveness, which can be wrong.** A recycled pid reads as alive,
  and on a busy box `tasklist` costs ~50 ms per running marker. It is the best signal
  available without changing the marker format.
- **No frontend, and no auth.** Both are by design for this round. The security model is
  entirely "loopback only, single user" — if that assumption ever changes, `PUT /api/settings`
  and `POST /api/start` become remote code and config execution.
- **`POST /api/start` returns as soon as the process spawns.** It does not wait for the
  funnel's own estimate or confirm gate — the cap replaces that gate, exactly as in INFRA-002.
- **One suite ran red once** (`test_spotify_serial_fix`, a MusicBrainz network timeout) and
  passed 22/22 standalone and on re-run. Reporting the red I saw, not only the green I ended
  on; the suite took 303 s that pass versus ~105 s normally, with other agents active.
