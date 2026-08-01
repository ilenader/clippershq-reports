# INFRA-012 — A save that refuses to clobber, a diff you see before it lands, and tests that finally stop writing the live config

**Date:** 2026-08-01 · **Type:** Feature + fix · **Spend:** **$0.00** — no paid call
Claimed as INFRA-012 · `dashboard/` + its tests · Suite **64/65** (the red is a known flake,
below) · campaigns SHA `8e02f8d6f6307ae8` · config 162 keys

---

## 1. The concurrency check

`GET /api/settings` now publishes `_version` — the **sha256 of config.json's bytes**. A save
sends it back. If the file has moved, the write is **refused with 409** and the response says
exactly what moved:

```
THE PAGE LOADS          version 685cb979fa9e   min_viewers=20  spotify.run_target=700
SOMEONE ELSE EDITS      twitch.max_viewers=1234, spotify.run_target=555
THE STALE SAVE          HTTP 409 — config.json changed since this page loaded
                          spotify_finder.run_target   you loaded 700   now on disk 555
                          twitch_finder.max_viewers   you loaded 1000  now on disk 1234
                        my edit was NOT written: min_viewers still 20
RELOAD, RE-APPLY        HTTP 200 — and the other writer's changes SURVIVE
```

A hash proves the file moved; only the old values can say **what** moved, and the page is
already holding them, so it sends `_known` alongside. The 409 body carries a per-key
`you_loaded` / `now_on_disk` list and the page renders it with a **Reload settings** button.

### Why a version check and not a lock

A lock here would have to be held across a human deciding. And the last time locking went
wrong in this repo it went wrong **quietly**: `file_lock()` takes the DATA path and appends
`.lock` itself, so a caller that passed `lock_path_for(...)` locked
`master_leads.csv.lock.lock` — a path nothing else contends for — and rewrote **58,000 rows
completely unprotected** while looking correct.

Compare-and-refuse has no such failure mode. If the token does not match, nothing is written.
The hash is over **bytes, not the parsed dict**, deliberately: a formatting-only rewrite by
the menus is still someone else having written the file.

**Backwards compatible** — a save with no `_version` still works, so an older page is not
broken by this. `_version`, `_known` and `_dry_run` are `_`-prefixed control fields, pulled
out before the allowlist check, and a config key never starts with an underscore.

## 2. The diff preview

`PUT` with `_dry_run: true` returns the from/to per key and **touches nothing**. The page runs
it first, renders the diff, then asks once:

```
About to change 1 setting(s). Nothing is written yet.
  • twitch_finder.min_viewers: 20 → 51
```

Cancelling leaves *"Cancelled — nothing was written."* and the file at 20. Accepting writes and
reports what landed, with the backup name.

**This is a preview, not a second confirm.** The three measured knobs keep their own confirm
quoting the number, because their cost is known; everything else now gets *seen* rather than
interrogated. A confirm on all 23 gets clicked through blind, which is why only three have one.

The preview also catches invalid values (`"nope"` for an int) before any write, and marks a
cleared field as `unset` rather than `0`.

## 3. No test writes the live config — third time for this class

`config_path()` reads `CLIPPERSHQ_DASH_CONFIG`, **resolved per call** so a test can point it
elsewhere without re-importing. The suite copies the real config to a temp file and points
there — a **copy**, not a fixture, so tests keep asserting against the real shape.

A guard test asserts the server under test is *not* pointed at the live file, and that the live
bytes are unchanged. **Verified: `config.json` is byte-identical after a full suite run**, with
`twitch.min_viewers = 20` and `spotify.run_target = 700` intact.

This is the third instance of the same class — status markers written into the real `scratch/`,
155 phantom rows into the money ledger, and INFRA-011's test saving `run_target = 900` for real
(which then cost several rounds, because the next run typed 900 into a field already showing
900 and it read as a broken dirty-check). The fix has been one line every time: make the path
redirectable, then redirect it.

## 4. Liveness — untouched

`OpenProcess` + `GetExitCodeProcess` with `STILL_ACTIVE`, as built. No subprocess reintroduced.

## 5. Panels render independently

`refresh()` was `Promise.all`, so the page waited on its slowest endpoint and one slow call
blanked everything with no error anywhere. Each panel now paints as its own data arrives; the
returned promise still settles when all are done, so the capability probe and the tests keep
working, and a failing endpoint cannot stop the others.

Measured through a proxy that stalls `/api/now` by 4 seconds:

| panel | painted at |
|---|---|
| spend | **0.26 s** |
| files | **0.40 s** |
| settings | **0.46 s** |
| now | 4.26 s (the stalled one) |

Three of four painted before the slow endpoint returned. This is exactly the failure that hid
the settings panel in INFRA-011 — 2.77 s on `/api/now` while settings sat 0.01 s away showing
an empty placeholder.

> **My first measurement of this was wrong and said "False".** The proxy was a single-threaded
> `HTTPServer`, so the 4-second sleep serialised every other request behind it — the harness
> was doing the blocking, not the app. Threaded proxy, and the real behaviour showed.

---

## Verification

| check | result |
|---|---|
| stale save refused | **409**, nothing written |
| refusal names what moved | per-key `you_loaded` / `now_on_disk` |
| other writer's change survives a re-apply | **yes** |
| save with no version | still 200 (older client unbroken) |
| dry run writes nothing | file byte-identical |
| preview reports from/to per key | yes, incl. `unset` and `invalid` |
| cancel at the preview | *"Cancelled — nothing was written."* |
| live config after a FULL suite run | **byte-identical** |
| guard test | asserts the server is not on the live file |
| panels independent | spend 0.26 s / files 0.40 s / settings 0.46 s vs a 4 s stall |
| liveness check | unchanged |
| page errors | **0** |
| dashboard tests | **56** |
| campaigns SHA | `8e02f8d6f6307ae8` **MATCH** · config 162 keys |

## Honest limits

- **One suite ran red: `test_filelock`.** It failed once and passed once on code I never
  touched (`git status` clean for both `filelock.py` and its test), and it is the same
  torn-row concurrency test that flaked in INFRA-002 under load — nine other rounds were
  running. Reporting the red I saw, not only the green.
- **The window between preview and write is small but not zero.** The file can move in
  between, so 409 is handled on *both* requests — but the preview you approved could in
  principle describe a state one write old.
- **`_known` is sent on every save**, which is all 66 values. Cheap on loopback, wasteful
  anywhere else, and it is the price of being able to say *what* changed rather than only
  *that* something did.
- **The 409 diff only covers settable keys.** A change elsewhere in `config.json` still blocks
  the save — the hash covers the whole file — but this panel cannot describe it, and says so
  only implicitly by listing nothing.
- **`history` was not measurable in the independence test**: it renders an empty table (no
  ledger row carries a `run_id`), which is under the size threshold I used. Three of four is
  the honest figure.
- **No merge.** A conflict is refused and you re-apply by hand; nothing attempts a three-way
  merge of two people's settings, and I would not want it to.
