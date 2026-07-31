# BL-697 — merge round, BL-694 onto main

## THE BOOKING LINK IS BYTE-IDENTICAL TO THE ONE THE CLIENTS PAGE ALREADY USES, checked three ways on the merged tree and once more inside the compiled bundle: `https://calendly.com/clipershq/30min`, the same sha256 as `public/brands.html:354`, and the ONLY distinct Calendly URL the whole build emits. `origin/main` moved `46115e32` → `f7a1a344`, verified origin==local. Two files changed in total, one of them BACKLOG. "Get started" keeps `/login` and its client-side navigation exactly; the signed-in hero is byte-identical to before; the new button opens in a new tab with `rel="noopener noreferrer"`. The 6 money files, `tracking.ts`, `campaign-era.ts`, the payouts route, `globals.css` and `brands.html` are all byte-identical by blob OID.

**2026-07-31 · MERGE ONLY. No source file was written or edited by this round.**
**Base** `46115e32` (`post-merge-BL-693`) · **Result** `f7a1a344` · **Tags** `pre-merge-BL-697` (46115e32) → `post-merge-BL-697` (f7a1a344), both pushed.

---

## STEP 0 — truth, with the SHA

| branch | SHA | ancestor of main before this round? | code diff |
| --- | --- | --- | --- |
| `origin/checkpoint/BL-694` | **`7f917997e7a99bed4b11f54d5f1c46d8e06115ea`** | **NO, genuinely unmerged** (`git merge-base --is-ancestor` returned false) | **NON-EMPTY `.tsx`**: `src/app/preview/preview-landing.tsx`, **80 insertions, 11 deletions** |

Measured before any merge, so the claim is not made from the merge result. The branch touches exactly two files, `BACKLOG.md` and `src/app/preview/preview-landing.tsx`, confirming the "one source file changed" claim.

**Nothing a live round holds was merged.** Exactly one branch was merged and nothing else was touched. BL-695 exists as an audit branch only and was deliberately left alone.

### The dirty main worktree, and what I did about it

**`C:/b575` holds the `main` branch and is both STALE and DIRTY:** HEAD at `91b844105a232225211835fa7da7aaf0414004ae`, far behind `46115e32`, with **77 uncommitted files**. I did not touch it, did not stash it, and did not check out `main` anywhere.

I created a **separate clean worktree at the short path `C:/m697`, detached at `origin/main`**, merged there, and pushed `HEAD:main`. `node_modules` was installed in place by `npm ci` and **never junctioned**. Re-checked after the push: `C:/b575` is still on `main` at `91b84410` with the same **77** dirty files, exactly as found.

**The standing consequence, unchanged from BL-685 and BL-687:** because the push went `HEAD:main` from a detached worktree, the shared repo's LOCAL `main` ref still points at `91b84410` inside `C:/b575`. **`origin/main` is correct at `f7a1a344`**; whoever owns that worktree needs to commit or clear its 77 files and pull.

---

## The merge

`git merge --no-ff origin/checkpoint/BL-694`. **Clean, no conflicts.**

```
 BACKLOG.md                          | 11 +++++
 src/app/preview/preview-landing.tsx | 91 ++++++++++++++++++++++++++++++++-----
 2 files changed, 91 insertions(+), 11 deletions(-)
```

**Exactly one production file changed.** Nothing else in the repository is in the diff.

### BACKLOG, unioned and counted with `grep -c`, never piped through `head`

| ref | `^## BL-` entries |
| --- | --- |
| `origin/main` before the round | **107** |
| `checkpoint/BL-694` | 108 |
| **merged result** | **108** |

**107 + 1 = 108. The union is exact and nothing was lost.** BACKLOG auto-merged with no conflict, and `grep -c '^## BL-694'` returns 1, so the new entry survived.

### Conflict markers

Repo-wide across `BACKLOG.md`, `src/`, `scripts/`, `public/` and `prisma/`: **0 conflict markers**.

---

## CONFIRMED ON THE MERGED RESULT

### The Calendly URL, printed from both sources and compared

This is the check that matters most, because a wrong booking link silently loses real clients. Both strings printed from the merged tree:

```
=== SOURCE OF TRUTH: public/brands.html:354 ===
      <a href="https://calendly.com/clipershq/30min" target="_blank" class="btn-primary btn-large reveal" id="ctaBtn"><span class="btn-label">Book a Strategy Call &rarr;</span></a>

brands.html:354 -> [https://calendly.com/clipershq/30min]
landing page    -> [https://calendly.com/clipershq/30min]
RESULT: BYTE-IDENTICAL
sha256 brands:  dddbbec91fbececf880331cd55453d95
sha256 landing: dddbbec91fbececf880331cd55453d95
```

**Identical strings, identical sha256.** The shipped landing page carries exactly one Calendly occurrence, at `src/app/preview/preview-landing.tsx:215`.

**Verified a second time, and more strongly, inside the compiled output.** After `npm run build`, every Calendly URL the build emits:

```
      3 https://calendly.com/clipershq/30min
```

**One distinct URL, three occurrences (server chunk, client chunk, prerendered HTML). No variant, no typo, no stray query string reached the bundle.**

For completeness, `public/brands.html` contains three Calendly references: line 354 and line 469 are this same bare URL, and line 356 is the same URL with embed styling parameters. **The bare form was the correct one to copy for a link, and it is what shipped.** `public/brands.html` itself is byte-identical (`4b61ecce`) and was not edited.

### "Get started" keeps its destination and behaviour

| | before | after |
| --- | --- | --- |
| component | `<Link>` (Next.js client-side nav) | `<Link>` (unchanged) |
| destination | `/login` | **`/login`, unchanged** |
| target | same tab | **same tab, unchanged** |
| label when signed out | `Get started` | **`Get started`, unchanged** |
| appearance | accent pill with arrow chip | quieter bordered button, no chip |

**Destination and behaviour are exactly unchanged. Its appearance did change**, which is inherent to placing two buttons side by side, and is stated here plainly rather than glossed: the accent fill moved to the new client CTA and "Get started" became the secondary treatment, losing its arrow chip.

### The signed-in hero is byte-identical to before

The branch splits the hero on `isLoggedIn`. The signed-in arm renders a single `<Link href="/login">Go to dashboard</Link>` **with the original class string character for character**, including the arrow chip. **A logged-in user sees exactly what they saw before this merge**, and no off-site booking link is rendered to them at all.

### The new button opens in a new tab with correct rel attributes

```
target="_blank"
rel="noopener noreferrer"
```

Both present. It also carries an `sr-only` span reading " (opens in a new tab)" after the visible label, so the visible text still leads the accessible name.

### Nothing outside the hero button row changed

The entire diff is confined to the button container inside `function Hero`. The heading, subheading, background, section wrapper and every other component in the file are untouched. **`src/app/globals.css` is byte-identical (`e8b55860`)**, so the "globals.css untouched" claim holds on the merged tree.

**No logged-in surface, navigation, API, auth or data path was touched.** The only production file in the diff is the signed-out preview landing page.

### Byte-identity by blob OID, `git rev-parse` on BOTH refs

| file | blob OID | verdict |
| --- | --- | --- |
| `src/lib/clip-earnings-writer.ts` | `7aa6be48` | IDENTICAL |
| `src/lib/earnings-calc.ts` | `797e2098` | IDENTICAL |
| `src/lib/balance.ts` | `e887f80a` | IDENTICAL |
| `src/lib/tracking.ts` | `847dcf70` | IDENTICAL |
| `src/lib/clip-earnings-invariant-middleware.ts` | `61cef393` | IDENTICAL |
| `src/lib/money-decimal.ts` | `ef5cdae7` | IDENTICAL |
| `src/lib/campaign-era.ts` | `106e16ad` | IDENTICAL |
| `src/app/api/payouts/route.ts` | `a9c7164e` | IDENTICAL |
| `src/app/globals.css` | `e8b55860` | IDENTICAL |
| `public/brands.html` | `4b61ecce` | IDENTICAL |

`tracking.ts` is not in the diff.

### No money moved

Read-only check against DB `now()` = **2026-07-31 10:25:53.076672+00**, timestamps cast to `::text`:

| measure | value |
| --- | --- |
| clips | 4478 |
| **earnings invariant violations** | **0** |
| total earnings | $10,322.43 |
| payout rows | 146 |
| newest payout created | 2026-07-31 10:18:22.921 |

**No clip's earnings or status was changed by this round and no payout was created, modified, approved or cancelled by it.** This merge cannot touch any of them: the only production file it changes is a signed-out marketing page with no data path. `GLOBAL_PAYOUT_CLAMP_ENABLED` was not flipped. No `prisma migrate` was run.

---

## Build gates, stated honestly

Run in order, one shell at a time, each exit code echoed by me rather than inferred, and **never piped through `tail`**:

| step | result |
| --- | --- |
| `npm ci` | **exit 0** (this wipes the generated Prisma client) |
| `npx prisma generate` | **exit 0**, "Generated Prisma Client (7.8.0)", run **before** tsc |
| `npx tsc --noEmit` | **exit 0**, **0 output lines** |
| `npx eslint --version` | **v9.39.4 present**, exit 0, so the hooks gate is real and not a silent no-op |
| `npm run build` | **BUILD_EXIT=0**, echoed from a captured log |
| `check:prisma-bypass` | **0 violations** across `src/` + `scripts/` |
| `check:removed-fields` | **OK**, no residual reads |
| `lint:hooks` | **11 problems (0 errors, 11 warnings)**, at the ≤11 cap, no new warning added |
| static pages | **61/61** |

`next build` was actually run and its output was inspected for the Calendly URL; tsc alone was not trusted. **No heredoc was used anywhere in this round** and shells were run strictly one at a time.

---

## Push, verified per BL-288

```
git push origin HEAD:main     46115e32..f7a1a344  HEAD -> main
local:  f7a1a344ed3b615b9a125d62d1fd85a4441521fb
origin: f7a1a344ed3b615b9a125d62d1fd85a4441521fb
VERIFIED: origin/main == local HEAD
```

Tags `pre-merge-BL-697` and `post-merge-BL-697` both pushed.

**Rollback:** `git revert -m 1 f7a1a344`, or `git reset --hard pre-merge-BL-697`. Reverting restores the single-button hero and changes nothing else; no data or money state is involved either way.

---

## Safety summary

Merge only; no source file was authored or edited by this round. The shipped Calendly URL is byte-identical to `public/brands.html:354` by string comparison, by sha256 and by inspection of the compiled bundle, which emits exactly one distinct Calendly URL. "Get started" keeps `/login` and its client-side navigation; only its appearance changed, which is stated rather than glossed. The signed-in hero is byte-identical to before. The new button carries `target="_blank"` and `rel="noopener noreferrer"`. Nothing outside the hero button row changed, and no logged-in surface, navigation, API, auth or data path was touched. The 6 money files plus `tracking.ts`, `campaign-era.ts`, the payouts route, `globals.css` and `brands.html` are byte-identical by blob OID on both refs. The earnings invariant is 0 violations, no clip earnings or status changed, and no payout was created, modified, approved or cancelled. `GLOBAL_PAYOUT_CLAMP_ENABLED` was not flipped. No `prisma migrate`. The dirty `C:/b575` worktree was left exactly as found. Every count comes from `grep -c`, never a pipe into `head`. No heredocs were used and shells ran one at a time. NO dashes used as bullets.
