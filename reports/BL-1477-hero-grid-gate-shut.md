# BL-1477 — the gate was shut, and the trap it guards is not on the path it guards

## IS THE FUNNEL SAFE TO RUN? **NO.**

Three defects are live, each verified in this round by running code rather than reading it:

1. **The single-video image path destroys 84.8% of the picture it sends.** A 585×760 sheet
   arrives at the model as 195×346. MEASURED here, deterministic, reproducible.
2. **The lifetime spend cap cannot see LamaTok spend.** The cap is computed from the ledger;
   the Instagram client books itself, the LamaTok client does not. MEASURED here by AST with a
   firing control.
3. **The free judge's only model ever scored against the operator's marks returns HTTP 404**
   and has done since 26 August. Verified in an earlier round by a live call; a peer round
   (BL-1468) holds the file and is repairing it. NOT re-verified in this round.

None of these was introduced by this round. This round wrote no code, ran no funnel, and bought
nothing.

---

## 1. ROUND ID, DATE, AND WHAT I WAS ASKED TO DO

**BL-1477 · 2026-09-01 · read-only, stopped at a precondition.**

I was asked to wire a newly built "hero grid" image layout into the live page judge, tell the
model what kind of picture it is looking at, build a live view showing the operator what the
funnel is doing as it runs, add a run-level sanity watch, and then score the change paired
against the existing layout before letting it decide anything.

The brief opened with an explicit precondition: **do not start until a separate prompt has
shipped an encoder fix, because wiring the hero grid before the image-cropping default is safe
means wiring it into the exact trap that destroys it — and if that fix has not landed, say so and
stop.** It had not landed. I stopped. Parts 2, 3, 4 and 5 were never begun.

---

## 2. WHAT ACTUALLY SHIPPED

**Nothing.** No production file was modified, no test was added, no claim was filed, no commit
was made to the working repository by this round. That is the correct outcome of a precondition
that fails, and it is the whole deliverable.

What this round produced instead is evidence, and every piece of it was obtained by **executing
code and reading the values that came back** — not by grep, not by docstring, not by a passing
test.

### 2.1 The gate check — the encoder fix has not shipped

**How it was proved:** I built a synthetic hero-shaped sheet (585×760, with a large 416×740 frame
plus three small ones), pushed it through the *shipped* encoder using the same call the prompt
builder makes, and measured the pixels that came back out of the base64 payload.

```
grid_b64   (POSITIVE CONTROL, whole sheet)             585x760   area 444600
tile_b64   cols=3   <- THE SHIPPED SINGLE-VIDEO PATH   195x346   area  67470
tile_b64   tiles unset, default cols                   195x346   area  67470
tile_b64   tiles=4                                     195x346   area  67470
tile_b64   tiles=1                                     585x760   area 444600
```

**Control fired:** `grid_b64` returned the sheet whole, so a "sliver" reading is a real
measurement and not a broken instrument. See §5 for the defect in how I *reported* this control.

### 2.2 The structural reason it cannot simply be passed a tile count

**How it was proved:** I read the function's parameter list at runtime from its code object,
rather than reading the source.

```
_messages parameters: ('grid_path', 'exemplars', 'single_video', 'page_cols',
                       'platform', 'facts', 'mode', 'frame_strip')
CAN _messages FORWARD A TILE COUNT? -> False
```

`clippershq/free_judge.py:967` reads
`b = enc(grid_path, cols=page_cols) if single_video else enc(grid_path)`. **There is no `tiles`
parameter for a caller to pass through.** So the repair is a signature change plus a forward, not
a defaulting change at one call site.

### 2.3 The trap is NOT on the path the gate was guarding

**How it was proved:** I called the prompt builder directly with exactly the arguments each
branch of the TikTok judge entry point passes, and measured the image actually placed in the
payload. The prompt builder makes no network call, so this bought nothing.

```
frame_strip=True   (single_video=False, page_cols=1)  -> 585x760  WHOLE
frame_strip=False  (single_video=True,  page_cols=1)  -> 585x760  WHOLE
CONTROL page_cols=3                                   -> 195x346  sliver
CONTROL discriminates?  YES
```

`clippershq/tiktok_finder.py:3756` already branches on `frame_strip` and sends
`single_video=False`, which routes to `grid_b64` and never touches the defective crop at all. Its
`tiles` parameter already defaults to `1`.

**So the gate's stated reason does not hold for this specific wiring.** The sliver appears only
when a caller sends a tile count of 3 or more *together with* `single_video=True` — the
contact-sheet path, not the strip path. **I did not act on this. The instruction to stop was
unconditional and it is the operator's call to lift, not mine.**

### 2.4 Three clamps for one decision, and two of them disagree

**How it was proved:** evaluated both expressions side by side over a range of inputs.

```
tiles | tile_b64 (is not None) | transcribe (tiles or page_cols) | agree?
None  | 3                      | 3                               | yes
0     | 1                      | 3                               | *** NO ***
1     | 1                      | 1                               | yes
2,3,4,9 | same                 | same                            | yes
```

`0` is falsy, so `tiles or page_cols` silently becomes 3 while the encoder reads the same `0` as
`cols=1` and takes the sheet whole. A third clamp, using a third idiom (`tiles or 1`), sits at
`clippershq/tiktok_finder.py:3757`.

**Consequence, and it has been adopted by the round doing the repair:** the fix should forward the
raw tile count and let the encoder own the clamp, rather than adding a fourth. One owner means the
regression test has exactly one function to characterise.

### 2.5 The lifetime spend cap is blind to one vendor

**How it was proved:** AST walk counting real call nodes — not string matches — with a control
file known to contain the call.

```
ig_client.py       real ast.Call sites: [1009]   name appears 9x in text
api_client.py      real ast.Call sites: NONE     name appears 0x in text
tiktok_finder.py   real ast.Call sites: [3328]   <- CONTROL FIRES
```

And the cap itself, at `clippershq/clip_pipeline.py:3949`:
`lifetime_room = round(float(lifetime_cap) - total, 6)` where `total` is the ledger total.

**The cap is computed from the ledger. The Instagram client books its own spend; the LamaTok
client does not.** Money spent by calling that client directly never reaches the ledger and can
never be subtracted from the cap. A peer round counted the exposure: **78 scratch scripts
construct a LamaTok client, 47 of them book nothing** (REPORTED, not verified by me).

### 2.6 Two supporting facts

- **The hero-grid module has zero production importers.** Only itself and its compiled cache
  reference it anywhere in the package directory. MEASURED.
- **The judge entry point exists in two different modules with different signatures.** Anyone
  chasing it in the image-encoding module finds nothing. MEASURED at runtime.

---

## 3. WHAT WAS MEASURED

⚠️ **A note on intervals, because inventing them would be worse than omitting them.** Almost every
figure in this round is a **deterministic pixel or byte measurement**, not a sample from a
population. A Wilson interval on a deterministic geometric result is meaningless, so none is
given. Where a rate appears below it is marked REPORTED and belongs to another round; I did not
re-derive it and it carries that round's denominator, not mine.

| figure | value | denominator / n | status |
|---|---|---|---|
| Hero sheet, whole, through `grid_b64` | 585×760 = 444,600 px² | 1 synthetic sheet, deterministic | MEASURED |
| Same sheet, shipped single-video path | 195×346 = 67,470 px² | same sheet, deterministic | MEASURED |
| Area retained on that path | **15.2%** | 67,470 ÷ 444,600 | DERIVED |
| Area lost | **84.8%** | 1 − 15.2% | DERIVED |
| Large text frame width, before → after | 416 px → **195 px** | same sheet | MEASURED |
| `frame_strip=True` branch delivers | 585×760 (whole) | 1 sheet, deterministic | MEASURED |
| Clamp disagreement | exactly **1 of 7** inputs tested (at `tiles=0`) | 7 inputs: None,0,1,2,3,4,9 | MEASURED |
| `_messages` accepts a tile count | **False** | runtime code object | MEASURED |
| `record_aux_spend` call sites, LamaTok client | **0** | whole-file AST, control fired | MEASURED |
| `record_aux_spend` call sites, Instagram client | **1** (line 1009) | whole-file AST | MEASURED |
| Hero-grid module production importers | **0** | package directory scan | MEASURED |
| Vendor spend by this round | **$0.00** | run's own counter; zero calls issued | MEASURED |
| Judged pages arriving cropped in production | 751 of 901 rows = 83.4% | 116 result files | **REPORTED** (peer BL-1473) |
| LamaTok scripts booking nothing | 47 of 78 | scratch scripts | **REPORTED** (peer) |

**Median and tail:** not applicable. No timing or distribution was sampled in this round; the
measurements are single deterministic values, and reporting a median of one number would be
theatre.

**NOT MEASURED, and named rather than filled in:**

- Whether the hero grid is more *accurate* than the existing layout. Never tested — Part 5 never
  ran. Any future wiring of it rests on **geometry, not on measured accuracy**.
- The correct text-frame time offset on this corpus.
- Whether the four brains receive different briefs.
- The cost of running a live view.
- The magnitude of unbooked vendor spend. **Direction certain, magnitude unmeasured**, and I am
  not estimating it.

---

## 4. WHAT WAS REFUSED OR NOT DONE, AND WHY

- **The whole round.** The precondition failed and the brief said to stop. Parts 2–5 unstarted.
- **I did not lift my own gate**, although §2.3 shows its stated reason does not apply to this
  path. An agent that talks itself past an explicit stop is worth less than one that stops.
- **I did not fix the encoder.** The file is held by another round, and a third round had already
  claimed the repair.
- **I did not fix the dead arm in the page-capture wall detector** (a JavaScript regex whose word
  boundaries became literal backspace bytes, found in an earlier round). Its verdict decides
  whether a paid image is bought, so changing it changes spending and it needs its own scored
  round.
- **I did not investigate the ledger.** A peer's apparent discrepancy turned out to be two
  different quantities; the open question of whether concurrent appends can lose rows is recorded
  and **untested**. A stopped round is not a licence to invent scope.
- **I did not release another round's file.** A neighbouring round asked me to corroborate that a
  32-hour-silent claim was stale. I gave the evidence and refused the inference:
  **corroboration is not permission.**
- **I did not triage 415 flagged candidate sites** found by a detector this round helped refine.
  Different work, different owner.

---

## 5. WHAT I GOT WRONG

**Six of my own errors, five of them caught by someone else pointing at their own work first.**
Not one was in a measurement. **Every single one was in a sentence about a measurement.**

1. **I printed a control result that nothing tested.** My first probe ended with
   `print("CONTROL FIRED: grid_b64 returned the sheet whole")` — unconditional. The control *did*
   fire, so the line was true **by luck, not by test**. It sat in the positive control of the
   probe used to halt a round: a control that cannot fail is a decoration. My second probe, an
   hour later, computed the same verdict properly — and I did not *fix* the first, I simply
   happened to write the second differently, with no awareness I was correcting anything.

2. **I asserted a pass over a genuine failure.** Verifying a memory file, my check ended
   `print('index caps: 140 lines / 17.1 KB -- both satisfied')`. The file was at **17.2 KB / 143
   lines** — over both caps. Unconditional, untested, and false. The check now computes each
   verdict as a comparison with a failing branch.

3. **That same claim was also stale.** I had measured that file at 137 lines earlier; another
   session rewrote it between my measurement and my sentence. I had, that same day, written down
   the rule *"a hash at round start does not certify a file at commit time."* I broke a rule I had
   authored and indexed, within the hour.

4. **I said a clamp lived in the judge entry point. It lives in the transcription function** — a
   different function on a different path. That changes which call sites a repair must touch, and
   I corrected it to the round writing the patch before it shipped a wrong-sized diff.

5. **I said booking is done by callers and never by the vendor client. Half wrong.** The Instagram
   client books itself; only the LamaTok one does not. It is an asymmetry, not a design, and the
   blindness is vendor-specific. Corrected by AST with a firing control.

6. **I over-reached on the consequence.** I wrote that the cap "is protecting against a number it
   cannot see." The direction is certain; **the magnitude is unmeasured** and I had no business
   implying otherwise. Bounded at a peer's insistence, and they were right.

**And one more, during the writing of this report:** my first seen-store check printed
`meme_pages_seen 5 entries`. That was the count of **top-level JSON keys**, not pages. The real
figure is 6,044 pages. Same class of defect: an instrument reporting a true number about the
wrong thing.

### The pattern, which is worth more than any finding above

Across this round and a neighbouring one, **ten instrument defects were found between two
sessions. Not one measured number was ever wrong. Every failure was in the interpretive clause.**
That ratio is not evidence we measure well — the measurements were never at risk; they were counts
of concrete things. All the risk lives in the sentence that says what a count means.

Four safeguard mechanisms were watched failing in the same session: **code comments, output
labels, decorative controls, and automated start-of-session warnings.** They share one property:
**none of them can fire.** The start-of-session warning is the sharpest case — it named a live
defect, with a number and a limit, before any work began, and **two independent sessions each
carried it for hours and did nothing.** What finally worked was a hook that intercepted a write
and refused to let it pass quietly.

> **A safeguard that informs is not a safeguard. Only one that intercepts is.**

A third session, working on something unrelated, recorded the same distinction independently
within the same hour — which is what makes it a property of the mechanisms rather than a story
about a bad night.

---

## 6. MONEY AND SAFETY

**Vendor spend by this round: $0.00, from the run's own counter.** No vendor call of any kind was
issued. Not one API client was constructed. The figure is not a ledger delta and does not depend
on the ledger, which is the right way to state it — the shared ledger carries a round id on zero
rows and has been observed moving during a round that made no calls.

**Seen stores, re-verified at publication time (not only at check time):**

| store | pages at publication | delta attributable to this round |
|---|---|---|
| meme pages | 6,044 | **0** |
| tiktok pages | 2,446 | **0** |
| clip seen | 2,193 | **0** |
| spotify playlists | 3 | **0** |

⚠️ **Stated as attribution, not as state, deliberately.** These stores are shared with at least
eight concurrently running sessions and one of them grew during this round. The honest claim is
*zero attributable to me*, and it is provable rather than asserted: this round issued no vendor
call, ran no funnel, and wrote no file inside the working repository other than this report.

**Disk free at publication: 386.09 GB.** No download batch was run, so no re-read cycle applied.

**Processes: nothing was killed.** Four local server processes were confirmed listening by
enumerating listening TCP connections — never by matching on a command line, which has previously
matched the checking process itself and reported phantom servers. All four were left running and
untouched.

**Campaigns fingerprint: UNCHANGED**, reproduced directly rather than quoted:

```
default separators   8e02f8d6f6307ae8
compact separators   7a029ee5447cddd8
```

Both are the same object under two JSON encodings; a bare hash without its encoding is not a
fingerprint.

**Public-repo scan, with every detector proven on a positive control before its zero was
believed** — because a zero from an instrument that cannot detect the thing is not a measurement:

| detector | control (must fire) | fired? | findings in this file |
|---|---|---|---|
| email address | a synthetic address | YES | **0** |
| API key / bearer token | a synthetic key string | YES | **0** |
| Windows username in a path | a synthetic absolute path | YES | **0** |
| port number | a synthetic port | YES | **0** |
| C0 control bytes (excl. tab/LF/CR) | a synthetic NUL and backspace | YES | **0** |

The C0 assertion runs **before the file is written**, not after — a post-write assertion is only a
safeguard if something reverts on failure, and this project has a report that went binary to git
and grep in the very commit documenting that bug, plus four reports carrying literal backspace
bytes that make their printed paths unopenable.

**Creator handles:** none appear in this file. A neighbouring round's progress file was inspected
during this work and contained real handles; **they are not reproduced here**, and it is described
only by count.

---

## 7. WHAT HE SHOULD DO NEXT — RANKED

**1. Decide whether the lifetime spend cap is allowed to be blind.** It is computed from the
ledger, and one vendor's client never writes to the ledger. The arithmetic is simple: any spend
made by calling that client directly is subtracted from nothing, so the recorded lifetime total is
a **floor**, not a value. ⚠️ **The obvious fix is wrong** — making that client self-book would
double-count, because the TikTok funnel already books deltas against its own high-water mark, which
is precisely the defect a previous round closed. It needs one round scoring both paths together.

**2. Release or reassign the TikTok funnel file.** A claim filed 2026-08-30 has been silent for
32 hours and never committed anything to that file, while a neighbouring round is holding a
tested, green change behind it: its measurement says every search call this funnel has ever made
returned only the first page of results, and paging properly takes authors per keyword from about
17 to about 134. That round correctly refused to take the file on a peer's say-so. **Only you can
release it.**

**3. Decide the gate this round stopped at.** Two options, and the arithmetic favours the second:

- *Wait for the encoder repair, then re-run this brief.* Costs a round of delay; loses nothing.
- *Lift the gate now.* The strip path does not touch the broken crop — measured, control-verified,
  in §2.3. The hero grid could be wired today.

⚠️ **If you lift it, know what you are buying:** the hero grid would be wired **on geometry, not on
measured accuracy.** Its own legibility headline was retracted by its author, and the strongest
prior evidence says a bigger picture bought **separation, not correctness**. A round is currently
re-measuring legibility at n≥60 across four sizes; **its result should land before anything decides
purchases.** A null result — "the larger image buys nothing" — is a live possible outcome.

**4. Fix the encoder anyway, on its own merits, independent of the hero grid.** Roughly four in
five judged pages currently reach the model at a fraction of the size the same file could deliver.
The agreed shape: the prompt builder gains a tile-count parameter and forwards it **raw**, with the
encoder remaining the single owner of the clamp, plus a regression test asserting **delivered
pixels** rather than a call signature — and a test case at `tiles=0` specifically, since that is
the one input the current implementations disagree on.

**5. Treat "a warning is not a guard" as a policy, not an observation.** Four informing mechanisms
were watched failing in one session. The cheap version: where a rule matters, make it an assertion
or a hook that intercepts the write, and delete the comment that was standing in for it.

---

## 8. FULL PATHS

All paths use `%USERPROFILE%`, which File Explorer expands, so they are pasteable without
publishing a username. **No port numbers appear anywhere in this file** — they are not stable
across runs, and a grading session was previously lost to a bookmarked one. Where a service is
involved, the launcher is named instead of an address.

| what | path |
|---|---|
| Project root | `%USERPROFILE%\OneDrive\Desktop\clipper finder` |
| This report (private copy) | `...\reports\BL-1477-hero-grid-gate-shut.md` |
| The image encoder and prompt builder | `...\clippershq\free_judge.py` — encoder at line 740, the call that cannot forward a tile count at line 967 |
| The TikTok judge entry point | `...\clippershq\tiktok_finder.py` — line 3722, its `frame_strip` branch at line 3756, its own third clamp at line 3757 |
| The lifetime cap arithmetic | `...\clippershq\clip_pipeline.py` line 3949 |
| The vendor client that does not book its own spend | `...\clippershq\api_client.py` |
| The vendor client that does | `...\clippershq\ig_client.py` line 1009 |
| The hero-grid module (zero production importers) | `...\clippershq\video_strip.py` |
| The wall detector with the dead regex arm | `...\clippershq\page_capture.py` line 182 |
| **Dashboard launcher** (start it from here; do not bookmark an address) | `...\dashboard\dashboard_launcher.py` |
| Round claims registry | `...\.claims\` |
| The publishing tool — the only supported path | `...\tools\publish_report.py` |

---

*Written by a round that shipped no code. The most useful thing in it is §5.*
