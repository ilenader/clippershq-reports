# MEMEBOT-056: the publish gate is satisfiable again — the length heuristic is replaced, not narrowed a seventh time, and this report was published by the script itself

**Date:** 2026-08-01 · **Type:** Fix + replacement · **Spend:** **$0.00 · 0 paid calls**
Claim filed via `tools/claim.py`, **6 paths registered individually** with repeated `--write`. Registry checked with `tools/claims_read.py` **and** `git status --porcelain` on every target: all four **FREE and clean**. `git -C` throughout, no `reset --hard`, no bypass flag added. Committed at `176fb9b`.

Acts on [MEMEBOT-051](MEMEBOT-051.md).

---

## 1. The gate could not be satisfied. It can now.

`tools/publish_report.py` gates on the secret scanner's exit code, and the scanner's
`>=32`-char opaque-literal rule fired on the **raw URL last line that every report is required
to carry**. Every round therefore had to hand-roll the check or bypass it — the exact outcome
BL-906 built the script to prevent.

**Before, on reports nobody had touched:**

```
  MEMEBOT-048  FAIL      MEMEBOT-046  FAIL      BL-885  FAIL
```

**After, the same three files scanned unmodified — plus two more:**

```
  MEMEBOT-048  PASS   MEMEBOT-046  PASS   BL-885  PASS   MEMEBOT-051  PASS   MEMEBOT-045  PASS
```

**And this report was published by `tools/publish_report.py` itself.** If it had refused, you
would be reading that instead.

Why the `http` allowlist never fired: the candidate regex `[A-Za-z0-9+/=_\-]{32,}` excludes
`:` and `.`, so the URL is chopped and the match *starts* at `com/ilenader/...`. The allowlist
tested `startswith("http")` on a string that could never begin with it.

---

## 2. Replaced, not narrowed. The discriminator is structure.

BL-829 said the **fourth** narrowing should replace the heuristic. It reached **six**: a
filename, a config-value path, a film-genre phrase, long test names, `====` banner rules, and
the mandatory URL. Each exemption was locally correct and the rule got worse anyway, because a
length test on a codebase full of long identifiers generates false positives faster than
exemptions can be written.

**Measured, not asserted** — this table is in the code:

| case | len | entropy | longest run | classes |
|---|---:|---:|---:|---:|
| REAL key, hex 64 | 64 | 3.98 | **64** | 2 |
| REAL key, mixed 40 | 40 | 5.12 | **40** | 3 |
| REAL key, base64 44 | 44 | 4.50 | **43** | 3 |
| the mandatory report URL | 56 | 4.40 | 10 | 3 |
| `====` banner rule | 39 | 0.00 | 0 | 0 |
| hyphenated prose | 52 | 3.77 | 8 | 1 |
| long test name | 50 | 4.08 | 10 | 1 |
| repo path | 33 | 3.84 | 8 | 1 |
| one long lowercase word | 38 | 4.00 | 38 | 1 |
| config film phrase | 42 | 4.03 | 14 | 1 |

**A credential is one unbroken run.** Everything that false-positived is separator-structured,
single-case, or repetitive. The replacement requires all three of, on the longest run:

```
  run >= RUN_MIN (24)   a path/URL/identifier breaks into short segments; a key does not
  letter AND digit      rejects words and CamelCase names, which no key resembles
  entropy >= 3.0        rejects padding and repetition
```

**The `http`/`reports/` prefix allowlist and the `_is_repo_path` call are gone from this rule.**
It is a replacement, not a seventh exemption.

### Two things the proof harness caught that reading would not have

**A 31-character key was invisible to both halves of the rule.** The candidate regex said
`{32,}` and `_looks_like_credential` said `>= 24`, so keys of 24–31 characters were never even
considered. **Two thresholds for one decision is a blind spot neither half reveals.** There is
now one `RUN_MIN`, used by both, and a test asserts `{32,}` no longer appears in the file.

**"At least 2 of {lower, upper, digit}" flagged `BedLevelIsMeasuredOverTheWindow`** — a
CamelCase test-class name, 31 unbroken characters. I measured case-transition rate as a
possible discriminator and it **does not separate**: CamelCase 0.38–0.45, real keys 0.30–0.41,
fully overlapping. Digit presence separates cleanly — **5 of 5 keys carry digits, 0 of 3
CamelCase names do** — so the rule requires a letter *and* a digit.

### The honest limit, written into the docstring rather than discovered later

**A credential of 24+ characters made of letters only would pass this rule.** That is the
price of letting a CamelCase class name through. It is still caught by both rules above it —
the secret-block rule (any length ≥8, no exemptions of any kind) and the credential-named-field
rule. **This is the third of three checks, not the only one.**

---

## 3. The three checks that have never false-positived still fire

```
  credential-named field   -> FIRES
  email address            -> FIRES
  secret-block value       -> FIRES
```

**And a real value from every secret block, planted into a report, is still caught:**

```
  api  CAUGHT    ig_api  CAUGHT    tikhub_api  CAUGHT    youtube_api  CAUGHT
  twitch_api  CAUGHT    gemini_api  CAUGHT    openrouter_api  CAUGHT
```

Seven of seven. The values are read from `config.json`, written to a temp file and **never
printed** — the scanner's own "verdicts only" rule applies to its test harness too.

**Six credential shapes that are NOT in config are also caught** — hex 64, mixed 40, base64 44,
mixed 31, mixed 24 (at the floor), bearer-style 49. That matters: if only the planted-config
test passed, the new rule would be dead weight riding on the secret-block rule.

---

## 4. `guard_amend` can now say yes to prose — verified, not asserted

MEMEBOT-051 left a permanently mangled commit message (backticks inside a double-quoted shell
string were executed) because the guard refused the repair. The guard was right on the evidence
it had, and **the hazard it was protecting against could not occur.**

A message-only amend is now allowed when **three independent facts all hold, each checked**:

1. **`git write-tree` == `HEAD^{tree}`** — the same object id, so no file can change and
   nothing can be absorbed. This is the BL-820 hazard, and identical trees make it impossible.
2. **HEAD is on no remote** (`git branch -r --contains HEAD`) — no published history is
   rewritten.
3. **HEAD's own message names the round** — authorship said by the commit, not inferred from
   the `will_write` proxy that misfired on MEMEBOT-051's own commit.

**Drop any one and it still refuses.** Tests pin all three: amending another round's commit is
refused (message does not name the round), amending a *published* commit is refused, and a
staged extra file is refused even when the message names the round — the index check is
independent and message-only never suppresses it.

**18 checks in `tests/test_guard_amend.py`, 22 in `tests/test_secrets_guard.py`, all green.**

---

## 5. The backups decision stands

Recorded as still correct and unchanged: **`backups/` is a same-session undo, not disaster
recovery**, because those copies die in the same event as their subjects. It is carried by the
copy script as history. Nothing in this round touched it.

---

## Proof

| claim | evidence |
|---|---|
| gate satisfiable | three published reports **PASS unmodified**; this report published **by the script** |
| heuristic replaced | `http`/`reports/` allowlist and `_is_repo_path` removed from the rule; `{32,}` gone |
| planted credential caught | **7 of 7 secret blocks**; 6 of 6 shapes not in config |
| three real checks | credential-named, email, secret-block — all FIRE |
| message-only amend | tree-oid equality + unpublished + HEAD names the round; each independently required |
| suites | **105 of 107 green.** Reds are `test_config_contract.py` (`youtube_finder_max_run_usd`, a cap round's key) and `test_tools_tracked.py` (`tools/gen_manifest.py`, **MEMEBOT-055**, created at 23:04 during my run). I touched no config key and no tool of theirs |
| campaigns SHA | **8e02f8d6f6307ae8 — MATCH** |
| config | valid JSON, 161 keys |
| claim hygiene | `claims_read.py` **and** `git status --porcelain` on all four targets before claiming |

---

## Honest limits

- **A letters-only credential of 24+ characters passes the new rule.** Stated in the docstring and repeated here because it is the real cost of the change. Two other rules still cover it; nothing covers it if it is *also* absent from config *and* appears with no name beside it.
- **`RUN_MIN = 24` and `ENTROPY_MIN = 3.0` are calibrated on ten examples**, five of them keys I constructed. They separate cleanly on that set. A key shorter than 24 unbroken characters, or one deliberately shaped to look like a path, is not covered by this rule.
- **I did not touch `tools/publish_report.py`.** The brief said fix the scanner, not the gate, and no bypass flag was added. The script is unchanged and now works because its dependency does.
- **The message-only amend relies on rounds naming themselves in commit subjects.** Every round here does, and the tests assume it. A round that commits without its id in the message gets the old refusal — correctly, but it will look arbitrary to whoever hits it.
- **`git write-tree` writes an unreferenced tree object** on every guard invocation. Harmless and gc-collected, but the guard is no longer strictly read-only, which it was before.
- **`_is_repo_path` and `_is_plain_word` are still used by rule 1** (config-value matching) and are untouched. Only the opaque-literal rule was replaced, so rule 1 keeps whatever false-positive surface it had.
- **Two suites are red and neither is mine**, but I only diagnosed them far enough to establish that. `youtube_finder_max_run_usd` being undocumented may be a real gap in someone's cap work rather than noise.

---

https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/MEMEBOT-056.md
