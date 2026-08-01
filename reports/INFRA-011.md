# INFRA-011 — The settings page saves. And the reason it looked broken was mine: /api/now was blocking the entire dashboard behind a liveness check

**Date:** 2026-08-01 · **Type:** Feature + fix · **Spend:** **$0.00** — no paid call
Claimed as INFRA-011 · `dashboard/` + its tests · Suite **64/64, 2,811 checks**
Campaigns SHA `8e02f8d6f6307ae8` **unchanged** · config 162 keys

---

## The bug that hid the feature

Wiring the save, the settings panel rendered **nothing** — an empty placeholder, no inputs,
no console error, `/api/settings` returning 200 with all 66 knobs. Calling `renderSettings`
by hand worked instantly. Recording every response at load found the answer:

```
responses at load:  /  app.css  app.js  spend  history  settings  files
                                                  ^ `now` never arrives
```

`refresh()` uses `Promise.all` over all five endpoints, so **the whole page waits on the
slowest**. Timed:

| endpoint | before |
|---|---|
| `/api/now` | **2.77 s** |
| `/api/settings` | 0.01 s |
| `/api/spend` | 0.01 s |

**The cause was mine, from INFRA-004.** The stale-marker liveness check ran
`tasklist /FI "PID eq N"` **once per running marker** — a process spawn each. The settings
panel was never broken; it was **queued behind a liveness check**.

My first fix made it worse: one full `tasklist /FO CSV` snapshot took **40.2 s** on this
loaded box. The right answer was to stop spawning processes at all and ask the kernel:

```python
h = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
GetExitCodeProcess(h, &code);  alive = (code == STILL_ACTIVE)
```

No fork, no parsing, and `STILL_ACTIVE` checked because on Windows a handle outlives the
process — without it a zombie reads as alive and a finished run keeps claiming the panel.

**2.77 s → 0.026 s cold, 0.006 s warm.** Verified: `_pid_alive(self)` True,
`_pid_alive(999999)` False.

---

## 1. The save

A save bar lives **outside `#set-groups`**, because that div is re-rendered and a result you
are still reading must not be wiped by a redraw.

- **Qualified ids** go back verbatim from `data-key` — `spotify_finder.run_target`.
- **Dirty tracking compares against the API payload, not the DOM**, so a knob that is unset
  server-side compares as *unset* rather than as the empty string the box happens to show.
- The button ships disabled and names what will change: *"1 change to save:
  twitch_finder.min_viewers"*.

## 2. Unset is not zero

A cleared number field sends `null`, and the server **deletes the key** so the code's default
wins again. Writing `0` where the operator meant "revert to default" is the same class of
error as a fabricated zero in the outcome ledger: a confident value nobody chose, and it
changes behaviour silently — a `0` view floor keeps everything, an absent one keeps 20,000.

A checkbox always sends a real boolean, because it has no unset state to express.

```
clear the field  ->  config now: ABSENT   (never 0)
summary          ->  "twitch_finder.min_viewers: 37 -> not set (using the default)"
```

Empty strings and whitespace are treated the same way.

## 3. The credential boundary, on the write path

`assert_specs_clean()` at import means a bad spec stops the server from starting. That covers
the read path. For the write path, every spelling a browser could try is refused **before
config.json is opened**:

| attempted | result |
|---|---|
| `{"ig_api": {"key": "PWNED"}}` — whole block | 400/403 |
| `{"ig_api.key": "PWNED"}` — qualified, as curated ids are | 400/403 |
| `{"key": …}`, `{"api_key": …}`, `{"token": …}` — bare leaves | 400/403 |

…across all seven `SECRET_BLOCKS`, with **`config.json` asserted byte-unchanged afterwards**,
and no credential value appearing in any refusal response.

**It cannot pass vacuously.** One test asserts `SECRET_BLOCKS` is non-empty *and* that at
least one of those blocks is actually present in the live config — otherwise the loop above
would be asserting nothing.

## 4. Validate, back up, then write

In order, and the order is the point:

1. **Serialise and re-parse in memory.** If the result would not round-trip, nothing on disk
   has been touched — a half-applied write to the file every funnel reads is worse than a
   refused one.
2. **Timestamped backup** via `control._make_backup()` — control's own helper, not a second
   implementation, so the menus and the dashboard leave the same trail.
3. **Atomic** temp → `fsync` → `os.replace`.
4. **Re-read**, and restore the backup if the result is unreadable.

Measured: every save left a backup (`config_20260801_170045.json`), config stayed parseable,
and **campaigns SHA `8e02f8d6f6307ae8` was identical before and after**.

A bad type (`"not-a-number"`) is refused 400 with config unchanged.

## 5. It says what moved

The response reports what **actually landed**, re-read from disk, key by key — not what was
intended:

> **Saved.** 1 key(s) changed. Backup: config_20260801_170045.json
> • twitch_finder.min_viewers: 37 → not set (using the default)

Also announced through the existing live region, so it is not a visual-only confirmation.
Silent success on the file every funnel reads is how a wrong knob survives a week.

## 6. The three measured knobs confirm first

The dialog **quotes the number** rather than asking "are you sure":

```
spotify_finder.run_target -> 888

Above ~777 the run exhausts its seeds and forces expansion, measured at a
17-POINT drop in handle rate. Raise the seed list instead of this number.
```

Only those three confirm. A confirm on all 23 would be clicked through blind, which is how a
gate stops being a gate.

Proven end to end: dialog shown, quotes `17-POINT`, and **dismissing it left config at 700**.

---

## Verification

| check | result |
|---|---|
| save button disabled with nothing to save | **yes** |
| ordinary knob saves without a confirm | 20 → 37 on disk |
| backup taken per save | `config_20260801_170045.json` |
| clearing a field | **ABSENT, never 0** |
| danger knob confirms | shown, quotes 17-POINT |
| declining the confirm | config unchanged at 700 |
| PUT reaching a credential | **refused, every spelling**, config byte-unchanged |
| non-vacuous secret test | asserts a block is present |
| campaigns SHA | `8e02f8d6f6307ae8` **identical before and after** |
| `/api/now` | **2.77 s → 0.026 s** |
| page errors | **0** |
| suite | **64/64, 2,811 checks** |

## Honest limits

- **My own test corrupted a real setting and I only caught it by accident.** An early run
  accepted the danger confirm and genuinely saved `spotify_finder.run_target = 900`. The next
  run then typed 900 into a field already showing 900, which correctly read as *not dirty* and
  looked like a broken dirty-check. Restored to 700, and the test now picks a value that
  differs from whatever is on screen. A test that writes to the live config is a hazard even
  when the feature works.
- **Saves go to the live `config.json`.** There is no dry-run and no diff-preview before the
  write — the confirm is the only gate, and only on three knobs.
- **No optimistic-concurrency check.** Two people (or a menu and the dashboard) editing at
  once will have the last writer win; the backup is the only recovery.
- **The advanced 43 are editable too** and carry no danger lines, because none of them has a
  measured consequence to quote. That is an absence of evidence, not evidence of safety.
- **`/api/now` is fast on Windows only via `OpenProcess`.** The POSIX branch uses
  `os.kill(pid, 0)`, which is correct but untested here.
- **`_pid_alive` returns `None` when it cannot tell**, and callers treat that as "not stale" —
  deliberately, since declaring a live run dead is the worse error.
