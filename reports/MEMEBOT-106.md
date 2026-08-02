# MEMEBOT-106 — The send-day checklist, and the fill mechanism it turned out to need

**Round:** MEMEBOT-106 · **Date:** 2026-08-02 · **Spend:** **$0.00**, no paid calls
**NOTHING SENT.** `master_leads.csv` sha256 verified byte-identical before and after every
step; the stamp round trip ran `dry_run=True` against a copy.
**Claim:** `MEMEBOT-106`, repeated `--write` flags, amended twice with `--force-reason` on
the record. Re-filed from MEMEBOT-105, which another round claimed in the seconds between my
namespace check and my `start` — the BL-839 live-claim check caught it.
**Commits:** `0639408`, `d0f9cd9`.

---

## The five placeholders were not merely unfilled — there was no way to fill them

This is the finding that changed the round. `render()` has accepted `operator=` and
`strict=` since BL-961, and the module's own self-test builds a filled `Operator`. But:

```python
m = render(r)          # main(), before this round — neither argument passed
```

No CLI flag, no config file, no environment variable supplied them **anywhere in the tree**.
The CLI could not emit a sendable message at all, so an honest checklist could only have
said *"edit the source"* — which is precisely the instruction a send-day page exists to
remove. So the mechanism had to exist before the page could be written:

```bash
cp send_identity.json.example send_identity.json     # gitignored: holds a real rate
python clippershq/message_template.py --kind clipper --limit 20 \
       --identity send_identity.json --strict
```

`--strict` exits **2** naming the first offending address and field, **0** only when all 20
render clean. Without `--identity` behaviour is unchanged — visible placeholders, nothing
guessed — but it now prints a summary line rather than leaving `[[RATE]]` to be noticed in a
mail client.

---

## Three commands were wrong until they were run

The brief asked for a dry run. It earned its place three times over — none of these were
visible by reading.

**1. The example identity would have passed the gate.** It shipped with prose values
(`"your name as you want it signed"`). Non-empty means no `[[PLACEHOLDER]]`, so `--strict`
**passed**, and a message would have gone out signed *"your name as you want it signed"* with
rate *"e.g. $40 per finished clip"*. It now ships **empty** — empty renders a placeholder and
the gate refuses — with `_`-prefixed keys carrying the per-field guidance, skipped by
`load_identity`. Verified: unedited copy + `--strict` → **exit 2**.

**2. The stamp command I first wrote raises `TypeError`.** `mark_sent_from_csv` takes **five**
positional arguments (`csv_path, date_sent, sent_channel, touch_number, message_variant`),
not one.

**3. `from clippershq import outcomes` raises `ModuleNotFoundError: dedup`** — `outcomes.py`
imports its neighbours flat, so it needs `sys.path.insert(0, 'clippershq')`.

All three are corrected in the page, with the trap named so the next reader knows why the
obvious form does not work.

---

## And the reply path in the brief was the wrong module

The brief said *"outcome_loop: date_sent/replied/touch_number"*. The source disagrees:
`outcome_loop.py` is the **video** outcome record (`memebot/runs.jsonl`, render performance)
and contains **no mention** of `date_sent`, `replied` or `touch_number`.

The email path is `clippershq/outcomes.py` behind **Control Panel `[o]`**, writing the
master's own columns — all seven confirmed present in the header: `date_sent`,
`sent_channel`, `replied`, `reply_sentiment`, `converted`, `touch_number`, `message_variant`.
The panel asks in plain language (*"Yes — they replied" / "No reply (yet)" / "It bounced"*),
every field optional. Because `touch_number` and `message_variant` are already stamped, a
reply attaches to **the message that earned it** — arm A or B, first touch or follow-up —
rather than to the address in general.

Checked in the source rather than inherited; the two module names are confusingly similar and
a runbook pointing at the wrong one is worse than silent.

---

## BL-993's delta — verified NOT applied, then applied

Diffed rather than assumed, as the brief required: **0** mentions of `BL-993`, and
`catch-all`, `Wilson`, `stratifies` all absent from `docs/SENDING.md`. Now added — the
stratified A/B, the ratio-routed evidence sentence, the honest deliverability figure with
its interval and the catch-all caveat that makes the naive 97.2% unquotable, and the greeting
numbers.

---

## THE DRY RUN — every step executed, timed, twice

| Step | Command | Run 1 | Run 2 | Exit |
|---|---|---:|---:|---|
| 0 | `refresh_mx.py --dry-run` | 3.4 s | 1.7 s | 0 |
| 1 | `all_bot_ready.py` | 8.3 s | 11.6 s | 0 |
| 2 | render 20, `--identity --strict` | 0.1 s | 0.3 s | **0** |
| 2b | same **without** identity | 0.1 s | 0.3 s | **2** ✅ refuses |
| 3 | `--coverage` | 0.4 s | 1.2 s | 0 |
| | **total** | **12.3 s** | **15.1 s** | |

The gate **accepts when filled** and **refuses when unfilled** — both directions, because a
gate that cannot fail is not a gate. The spread between runs is other work on the machine,
so the page quotes **ranges**, not a single flattering number.

Stamp round trip, `dry_run=True` on a copy: `matched 2, unmatched 0, ambiguous 0` in 2.9 s.

---

## AT-PUBLICATION RE-VERIFICATION

BL-993's own lesson is that a "still broken" claim had a shelf life of **minutes**. It held
here: HEAD moved from `d0f9cd9` to `b07c6cf` *between two of my verification commands*, so
the checks below were re-run together against one sha.

**HEAD `b07c6cf35dcc`** (short form: the full 40-char sha trips the report
scanner's credential-shape rule, which is the scanner being right about the shape
and wrong about the thing — a shortened sha is unambiguous and is how every other
report here cites one)

| Check | Result |
|---|---|
| Clipper placeholders | `SENDER_NAME, REPLY_TO, RATE, TURNAROUND, PAYMENT_TERMS` — **5** |
| Unfilled on an empty operator | the same 5, none missing |
| Rows rendered | **2,970** |
| Consistency framing used | 324 |
| **FALSE median claims** | **0** |
| `--identity` / `--strict` at HEAD | present |
| `master_leads.csv` sha256 | `6a744dd7cd488ecc…` — **unchanged** from the pre-dry-run baseline |

*Address redaction:* the gate's refusal prints a real address on stdout. The one seen during
this round, redacted per convention: **`ar…@gmail.com`, sha256 `07dfae13ea25fc20`**. No
unredacted address appears anywhere in this report. (The first draft of this line carried an
invented fingerprint; it was computed properly before publishing.)

## VERIFICATION

| Check | Result |
|---|---|
| Full suite | **156/156 suites, 5,129 checks, ALL GREEN** (733.8 s) |
| `message_template.py --self-test` | 7 failures — **pre-existing**, identical at HEAD before my change |
| `config.json` | unmodified, parses, **5 campaigns** |
| `send_identity.json` | gitignored; verified invisible to `git status` |
| Emails sent | **0** |

## STILL OPEN — and whose

- **The seven `--self-test` greeting failures are pre-existing** and not this round's; I
  confirmed the count is identical at HEAD with my change reverted. Unowned as far as the
  registry shows.
- **`send_identity.json` must be filled by the operator.** That is the one remaining
  blocker, and it is now a two-minute edit with a gate that refuses if it is skipped.