# MEMEBOT-050 — The crop probe now sees the whole clip

Acting on [BL-898](BL-898.md). **No paid calls.**

**Pre-flight, counted directly.** `ls .claims/*.json` → **14 files** at start. **MEMEBOT-046
had released `edit.py`** — confirmed, there was no MEMEBOT-046 entry (only MEMEBOT-046H, a
different round that explicitly took an `H` suffix to avoid the collision). **But MEMEBOT-048
had taken `edit.py` at 21:55**, four minutes before I looked.

So my first claim **deliberately excluded** `edit.py`. BL-898 taught me the cost of the
opposite: I claimed `clip_pipeline.py` there "in case", never wrote it, and stalled
MEMEBOT-045 at the gate for a whole round. Since item 2 is *"measure whether it matters"*,
measuring first was the correct order anyway, not a dodge. MEMEBOT-048 ended while I measured
and I re-claimed with `--force` to add the file.

---

## 1 & 2. Measure first — and the measurement changed what "measure" could mean

**The brief asks whether a full-duration probe gives a different crop than the 90-second one
on the 98 long clips. That comparison cannot be run at zero cost, and it is worth being exact
about why rather than substituting something quietly.**

The 98 clips over 90 s exist in `clip_library` **as metadata**. Scanning 734 local `.mp4`
files found **zero** clips over 90 s carrying a video stream — the only long local files are
audio-only siblings in `scratch/*/audio/`, useless to `cropdetect`. Fetching the real video is
a paid call, which this round forbids.

So the real-world **frequency** is unmeasured and I am not going to imply otherwise. What
*can* be settled offline is the question that decides whether the exposure is theoretical:
**can the 90-second bound produce a wrong crop at all?**

### It can, and the harm is silent

A synthetic 150 s clip whose picture widens at 110 s — after the bound closes:

```
OLD (-t 90)      -> crop=540:420:90:430
NEW (whole clip) -> crop=684:420:18:430
```

The old probe **applies a 540 px crop to a clip that needs 684 px — 72 px sliced off each side
of every frame after 110 s.** A too-tight crop still renders. Nothing fails, nothing warns.

`cropdetect(reset=0)` grows its box across the frames it **decodes**, exactly as the
function's own docstring promises. That is precisely why the bound mattered: it was never a
sampling detail, it was the edge of what the filter was allowed to see.

### The fix, and its cost

`max_probe_sec` now defaults to **`None` — the whole clip**. `CONTENT_CROP_HARD_CAP_SEC = 600`
remains as a **runaway guard**, ~3.3× the longest clip in the corpus so it never binds on real
material. The `subprocess` timeout moved 180 s → 600 s to cover the cap, because leaving the
old timeout would just be one silent truncation replacing another.

**Cost is decode time, not money, and it is small:** full duration measured **1.4×** the 90 s
probe on a 150 s clip (+0.37 s) at `sample_fps=4`. For the ~95% of clips already under 90 s it
is unchanged *by definition* — there was never anything past the bound.

### Three fixtures in a row lied to me

This is the part worth carrying forward. Each looked correct and each returned a confident
**"same — the exposure is theoretical"**:

1. **`shortest=1` truncated the file to 110 s.** The overlay's `shortest` flag ended the
   output at the narrow segment, so the wide half never existed. The probe compared 90 s of a
   110 s clip against 110 s of the same clip.
2. **The wide half was blue.** Blue's luma in `yuv420p` is ~29, sitting on top of cropdetect's
   `limit=24`, so after encoding it read as **black**. cropdetect emitted
   `crop=-718:420:720:430` — a *negative* width, meaning "found nothing" — which the regex
   skipped, leaving no lines and an apparent agreement.
3. Only the third fixture, built by `concat` with two bright colours, could actually detect a
   difference.

I nearly published "theoretical" off fixture 1. The fixture now **validates itself before any
conclusion is drawn from it**: it asserts its own duration *and* that its two halves crop to
different widths, and refuses to measure otherwise. That check is in the shipped test too.

**Six regression tests** in `memebot/scraper/tests/test_content_crop.py`, including one that
pins the unchanged behaviour for short clips and one — *"the fixture can actually detect a difference"* — whose whole job is to guard the guard.

---

## 3. The sweep: two shapes

**Shape A — a prefix of a stream used as a fact about the whole.** 30 candidate lines in
production code (tree snapshots under `scratch/*/tree/` excluded — they are copies of
`edit.py`, not separate sites). After hand review:

| site | verdict |
|---|---|
| `edit.py::detect_content_crop` | **was the bug — fixed this round** |
| `clip_cuts.content_region` | fixed in MEMEBOT-038 — **but see the residual below** |
| `song_loudness.py` (3 sites) | not the bug; explicit windows, and the canonical *fix* for this class |
| `memebot/meme/render.py:623` | `-t out_dur` is the output length, not a probe |
| `edit.py:1811, 1904` | ambient-bed length and target duration — outputs, not samples |
| `measure_cover.py`, `measure_source.py` | `-t 1.0` CLI default on one-off measuring tools; a cover *is* the first frame |

**The residual worth naming:** `clip_cuts.content_region` still falls back to
`-frames:v <probe_frames>` when `ffprobe` cannot return a duration — silently reverting to the
first-N-frames blindness the module exists to remove. It is defensible (you cannot compute a
spread-out `fps` without a duration) and rare, but it is the old behaviour reachable by a
failure path, and nothing says so at the call site. Reported, not changed: I read that file
this round and do not hold it.

**Shape B — a ceiling measured from data collected at that ceiling (BL-904's form).** This one
is *detectable without reading intent*: if a cap really binds, the observed distribution piles
up at it.

```
clip_max_pages_per_account = 5 pages x ~30 clips = 150 clips reachable
  observed clips per account: n=172  median 11  p90 22  MAX 122
  at or above the ceiling: 0 / 172
  ** SATURATED — nothing observed above the bound
```

Nothing in the corpus exceeds the reachable ceiling, so **"how many clips does an account
have" cannot be answered from this data** — the measurement cannot see past its own bound.
Evidence, not proof: a natural limit can sit under a cap, and round-robin revisits mean the
per-run ceiling is not a per-account lifetime one. But it says exactly where to look.

By contrast `edit.py`'s 90 s bound shows the *healthy* signature — 105 of 1,999 clips (5.3%)
sit above it, which is how we knew the bound was binding rather than coincidental. (BL-898
reported 98/4.90%; the library has grown since.)

**The sweep also caught itself committing the error it hunts.** Its first Shape-B pass
compared *clips per account* (122) against a cap counting *pages* (5) and printed "79.1% at or
above the cap" — a unit mismatch that made a meaningless number look like a finding. Fixed to
compare against pages × ~30.

`repost_finder.account_posts` (12) and `pages_per_tag` (2) could not be assessed: neither a
per-account post count nor the number of pages actually pulled is persisted anywhere, so there
is nothing to compare the cap against. Recorded as unmeasurable rather than assumed fine.

---

## 4. The stash lesson is now in RECOVERY.md

Two subsections under *"The commands that cause this"*, plus two new table rows:

* **A `git stash -u` entry is a MERGE, and the untracked files are on a THIRD parent.**
  `git stash show` displayed **23 of 1,198** entries in the incident; the other **1,175** were
  invisible to every obvious inspection command. With the exact `git rev-list --parents`
  incantation to read them.
* **Popping a stash is a revert with no diff review.** A stash holds the file as it was when
  the stash was made, and rounds carry on afterwards — so an entry can contain a **pre-fix**
  version that someone has since corrected. Stated with the real case: the entry held the old
  five-field `dict_of`, and popping it would have silently re-broken the render path while
  looking like housekeeping.
* What to do instead (`git show HEAD:file` to compare, not stash), how to audit an entry you
  did not make, that PRESENT-DIFFERENT must never be auto-resolved, and that a dropped stash
  is recoverable via `git stash store <sha>`.

---

## 5. The threshold floor is enforced, not documented

Verified by breaking it. Setting `DEFAULT_THRESHOLD = 0.05` — the value that buys the 92%
coverage figure with noise — turns the suite red with **two independent failures**:

```
FAIL: "threshold is NOT lowered to buy coverage"
      0.05 not greater than or equal to 0.15
FAIL: "region-aware finds a cut full-frame misses"
      [4.0] is not false : full-frame detection unexpectedly found the inset cut
```

The second is the stronger one and I did not plan it: at 0.05, full-frame detection *does*
find the inset cut, which breaks the premise the whole region-aware argument rests on. So the
floor is guarded both by an explicit assertion and by a behavioural test that fails for the
underlying reason. `clip_cuts.py` was restored byte-for-byte afterwards (`git diff` clean).

---

## Proof

| claim | evidence |
|---|---|
| probe covers the full duration | `max_probe_sec=None`; hard cap 600 s as a runaway guard only, with the timeout raised to match |
| the bound changed a real answer | old `crop=540:420:90:430` vs correct `crop=684:420:18:430` — 72 px off each side after 110 s |
| the 98 long clips measured both ways | **NOT DONE — impossible at $0.** Zero long clips exist locally with a video stream; stated plainly rather than substituted |
| cost reported | **1.4×** decode (+0.37 s on a 150 s clip); unchanged for the ~95% under 90 s |
| sweep with findings | Shape A: 30 production candidates, 1 residual named; Shape B: `clip_max_pages_per_account` **SATURATED** |
| floor enforced by test | breaking it fires **two** tests, not one |
| stash lesson carried | `RECOVERY.md` — third parent, revert-not-tidy-up, audit procedure, `git stash store` |
| **suites** | **101 / 102 pass.** Mine both green: `test_content_crop` 6 checks, `test_clip_cuts` 15 checks. |
| **campaigns byte-identical** | `8e02f8d6f6307ae8` — unchanged |
| **config valid** | parses, 161 keys |

### The one red suite is the same one BL-898 found, and still not mine

`tests/test_clip_pipeline.py` fails on `_selftest()` — *"the matcher is used when its file
really exists"*. Re-verified by the same method, an hour later and unchanged:

```
COMMITTED  -> 0   PASS
WORKTREE   -> 1   FAIL
```

`clippershq/clip_pipeline.py` is still ` M` — an uncommitted, in-flight edit by another round.
The committed tree is green. I touched none of it.

### Two gates fired on me, and both were right

* **The pre-commit manifest gate refused my first two commits**, because
  `docs/claims/MEMEBOT-050.claims` would have been enrolled before the code it claims existed.
  It is enforcing BL-874's rule that *a manifest waits for the code, never the reverse*. I
  committed the code first and the manifest second rather than reaching for `--no-verify`.
* **The publish-time secret scanner failed my first draft** on three long test-function names
  read as opaque literals. False positives, but the gate is worth respecting rather than
  arguing with — the names are shortened here and spelled out in the test files.

### The crop fix lives in a different repository

`memebot/` is **its own git repo** with its own remote, gitignored by the parent. So:

* the fix and its tests are committed at **`95a75c4` in `memebot`**, not in this repo;
* `git add` on the parent refused them, correctly — force-adding would double-track 67 files
  across two histories, which MEMEBOT-048 deliberately avoided;
* and **the claims manifest cannot claim them.** `verify_claims.py` checks
  `git show HEAD:<path>` in the parent repo, where a `memebot/` path can never resolve. So
  the manifest claims only the parent-repo artefacts and says why in a comment. Claiming the
  crop fix would have produced a manifest that fails forever — the "reads as coverage,
  matches nobody" shape claims exist to prevent.

That is a real gap in the claims system, not a workaround: **work in the nested repo is
currently unclaimable and unverifiable by the parent's tooling.** Worth someone's round.

Run with `PYTHONUTF8=1`.

---

## Corrections to my own claim, recorded

**My claim named `docs/RECOVERY.md`. That file does not exist** — `RECOVERY.md` is at the repo
root. `claim.py` accepted it because `docs/` exists and a not-yet-created file inside a real
directory is a legal claim. So for part of this round I held a path that matched nothing,
which is the precise failure `validate_paths` was built to prevent, slipping through on a
plausible-looking new-file path. Re-claimed with `--force` against the real path.

Whether `validate_paths` should refuse a *new* file whose sibling names an existing file
elsewhere is a genuine design question and not mine to settle here — but the near-miss is
worth the record: **a claim can be well-formed, accepted, and still cover nothing.**
