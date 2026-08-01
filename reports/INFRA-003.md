# INFRA-003 — SPEC: the local dashboard. Six panels, one visible at a time, reading the state files the menus already read. **Smallest honest build: 11–14 hours, zero funnel changes.** The mockup is at `scratch/infra003_mockup.html`

**Date:** 2026-08-01 · **Type:** Spec + static mockup, READ-ONLY · **Spend:** **$0.0000 · 0 API calls**
Nothing implemented. Claim filed as `.claims/INFRA-003.json`. Open the mockup in any browser — real layout, fake data.

---

## The one finding that changes a requirement

**`run_id` is on 0 of 128 ledger rows.** The brief expected history to be "thin looking back"; it is currently **empty** looking back. The dollars are real and total correctly — they simply cannot be tied to a run.

So History does not show 128 rows with gaps. It shows the runs that carry an id, and says why the rest are absent. **A dashboard that inferred which run spent what would be inventing the answer**, and this ledger has already been overstated once by a double-count.

---

## The aesthetic, as a rule rather than a mood

Every panel obeys four constraints. They are testable, which is the point.

1. **One thing per screen.** Six tabs, exactly one visible.
2. **Nothing on screen unless asked for.** Everything secondary sits in a `<details>`. The Now view shows two running funnels and collapses the four idle ones behind a single line.
3. **A number and a word, never a sentence.** `412 / leads`, not "leads found so far". The only prose is where prose is the safety feature — the send-file warning and the settings consequences.
4. **If a panel needs a paragraph, it is wrong.** The two paragraphs that survive both exist to stop a mistake, not to explain a feature.

Type is the system font stack, so it looks native and costs nothing to load. No icon font, no images, no external request — the CSP-safe, offline-by-construction option.

---

## The six panels

### 1. Now
A card per running funnel: name, a 4px progress bar, and four numbers — progress, leads, spend, elapsed. Idle funnels collapse into one row. `Details` opens the status file's own fields.

**Reads:** `scratch/<funnel>.status.json` — the marker shape INFRA-002 already writes:

```json
{"round":"repost_finder","status":"completed","ts":"2026-08-01 13:27:09",
 "epoch":1785583629.28,"pid":14540,"pages":116,"calls":242,
 "appended_incrementally":116,"halted":"","out_path":"./output/repost_20260801.xlsx"}
```

**Five funnels already emit this.** The dashboard adds no field and asks for none. It does need two conventions that shape already supports:
- `status` ∈ `running | completed | failed` — and **an absent marker means *unknown*, never *failed***. That distinction is load-bearing; conflating them once made a completed run get reported as killed.
- progress is `pages / target`, both already present.

### 2. Start
Funnel, target, cap, one button. Shows the estimate and confirms once — the same Proceed gate the menus use, not a new one. **The button calls the headless entry point INFRA-002 builds; if that is not ready, this panel ships disabled rather than shelling out to the interactive menu.**

### 3. History
Date, funnel, leads, cost, duration; a row click opens that run's xlsx. Scoped to runs with a `run_id`, with the honest note above.

### 4. Spend
Three numbers — lifetime, metered, estimated — then everything collapsed. Estimated and correction rows are **visually distinct**, because the ledger carries both:

| kind | example | shown as |
|---|---|---|
| metered | `spotify_finder` $0.1452 | plain |
| estimated | `ig_xlink_interrupted_upperbound_est` $0.1500 | amber `estimated` tag |
| correction | `CORRECTION_bl842_double_count` **−$0.1452** | red `correction` tag, negative preserved |

**Corrections are negative and must stay negative.** A UI that clamps at zero keeps the overstatement — the exact failure that hid a double-count worth up to 100%. Reuses `spend_ledger.reconcile()`, which already separates the two and whose matcher is deliberately narrow.

### 5. Settings
Only the knobs, each with its current value and **one line on what happens if you move it** — "0 turns the follower gate off entirely", "1 keeps the library spread across many pages instead of draining a few".

**Credentials: the page never sees them.** It does not read `config.json`. It reuses `control.py`'s allowlist — 16 editable specs — behind `secrets_guard.SECRET_BLOCKS`, which is enforced at import and refuses to start if a spec names a credential block. The server exposes an endpoint that returns *only* allowlisted keys; there is no path from the browser to the file.

### 6. Files
`ALL_BOT_READY.csv` gets its own bordered card and the only strong sentence on the page: **"Send from this one. It contains every other send file — using a second one mails the same people twice."** The six decoys collapse behind one line, each labelled with what it actually is — `LATEST_BOT_READY.csv` reads *"a single past run, not the list"*.

### 7. Videos
Present, empty, honest: *"Nothing yet — memebot is not wired."* When it lands: finished video, source clip, chosen song, download-all.

---

## Accessibility, since this is the first user-facing surface here

Not a later pass. Built into the mockup: semantic landmarks and a real tablist; **arrow-key roving focus** across tabs so a keyboard user is not tabbed through every panel; visible `:focus-visible` rings on every control; `<details>`/`<summary>` for disclosure so it works with JS off; every input has a real `<label>`; status conveyed by text and shape, never colour alone — the estimated/correction tags carry words, not just amber and red. Light and dark both defined, with a `data-theme` override.

---

## 8. The smallest honest build

**FastAPI + one HTML file. No funnel changes. Nothing new written to disk.**

| piece | hours |
|---|---:|
| server skeleton, static file, localhost bind | 1 |
| `/api/now` — read + parse the 5 status files | 1 |
| `/api/history` + `/api/spend` — reuse `spend_ledger.reconcile()` | 2 |
| `/api/settings` GET/PUT behind the `control.py` allowlist | 2–3 |
| `/api/files` — list, label, stream downloads | 1.5 |
| `/api/start` — call the INFRA-002 headless entry | 1.5–2 |
| wire the mockup to live data, polish, dark mode | 2 |
| **total** | **11–14 h** |

**What keeps it small:** it reads the same files the menus read, so there is no new source of truth and nothing to keep in sync. **What is not in that estimate:** `run_id` backfill (impossible — the data was never written), auth (localhost-only, single user), and anything memebot.

**Two dependencies, stated plainly.** Start is blocked on INFRA-002's headless entry point. History is thin until runs start carrying `run_id`. Everything else — Now, Spend, Files, Settings — can be built today against files that already exist.

---

## Limits

- **Mockup only. Fake data throughout.** No endpoint exists; no funnel was touched; nothing was measured beyond reading state files.
- **The status shape is read from five live files**, not from an INFRA-002 spec I have seen. If that round changes the shape, `/api/now` follows it — the dashboard must not become a second definition of what a run is.
- **Progress as `pages / target` assumes a target is knowable.** For the clip walk it is; for a hashtag crawl that stops on a dollar cap it is not, and those funnels should show elapsed and spend with no bar rather than a fabricated percentage.
- **No auth by design.** Localhost, one user. If it is ever bound to anything other than `127.0.0.1`, that assumption fails and settings become writable by anything on the network.
- **I did not build or run a server**, so the hour estimate is a considered one, not a measured one.
