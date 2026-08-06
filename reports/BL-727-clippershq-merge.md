# BL-727 — Both branches landed, in the order that mattered

**BL-724 merged FIRST (`771a3654`), BL-725 SECOND (`fe8e29cd`).** The policy was corrected before
anything started pointing at it, so at no commit on `main` does a public footer link a TikTok reviewer to
a document naming Apify and Vercel.

**2026-08-06 · Merge only, no source authored this round.**
`main`: `de0169bd` → **`fe8e29cd`** · **BL-723 deliberately NOT merged.**

---

# STEP 0 — TRUTH PER BRANCH

| Branch | SHA on origin | Ancestor of `main` before this round? | Diff vs `main` |
|---|---|---|---|
| `checkpoint/BL-724` | `cfbebfde2413181e95872ceeb22f0ed894f8f6d3` | **NOT_MERGED** | 4 files, 701 insertions, 15 deletions |
| `checkpoint/BL-725` | `33609c4176e063bd675f76114b04babc2ae04c53` | **NOT_MERGED** | 3 files, 458 insertions |
| `checkpoint/BL-723` | `22039307eb3dda87f4b302569807cc1146ea916d` | not merged, **and deliberately left that way** | not merged |

Both were genuinely on origin, genuinely unmerged, and genuinely non-empty. `git merge-base --is-ancestor`
returned NOT_MERGED for each against `origin/main` at `de0169bd`.

**BL-723 was not merged, and that is checked rather than assumed.** After both merges,
`git merge-base --is-ancestor origin/checkpoint/BL-723 HEAD` returns **NOT_MERGED**. It targets
`business-api.tiktok.com` and is not usable under the Login Kit app being submitted, so merging it would
have shipped a dead code path.

## The dirty worktree, and what was done about it

`C:/b575` is the repo's own `main` worktree and it was **both stale and dirty**: `HEAD` at `91b84410`
(BL-648, far behind `de0169bd`) with **77** modified or staged-deleted paths, including staged deletions
of `docs/` files and `public/splash/*.png` and modifications to `BACKLOG.md` and `prisma/schema.prisma`.

Nothing in it was touched. The merge was performed in a **separate clean worktree** created at the short
path `C:/m727`, detached at `origin/main`, verified clean (`git status --porcelain` = 0 lines) before the
first merge. `node_modules` was installed there with `npm ci`, never junctioned.

**`C:/b575` was left exactly as found**, verified after the push: still on `main`, still at `91b84410`,
still **77** dirty lines. None of its uncommitted work was swept into either merge.

---

# THE MERGES

## 1. BL-724 first

`git merge --no-ff origin/checkpoint/BL-724` → **`771a3654`**, clean, **0 conflicts**.

Verified on the merged tree before going any further:

| Check on `public/privacy.html` | Count |
|---|---|
| **Apify** | **0** |
| **Vercel** | **0** |
| Railway | 1 |
| Supabase | 1 |
| Resend | 1 |
| Sentry | 1 |
| Ably | 1 |
| HikerAPI | 1 |
| LamaTok | 1 |
| YouTube Data API | 1 |
| ScrapeBadger | 1 |
| TikHub | 1 |
| **"Connecting Your TikTok Account"** | **1** |

`Last updated: August 2026`. `TOS_VERSION = "v2"` in `src/lib/legal-version.ts`.

Both false statements are gone and every provider now named is one the platform actually uses, each
verified in BL-724 from `apify_usage_entries`, `creator_scans` and the live response headers rather than
assumed. The TikTok disclosure section is present.

## 2. BL-725 second

`git merge --no-ff origin/checkpoint/BL-725` → **`fe8e29cd`**, with **one** conflict, in `BACKLOG.md`
only, exactly as expected: both branches appended a new entry at the tail of the same file.

### The conflict was resolved as a UNION, both sides, losing nothing

Three markers at lines 20127 (`<<<<<<< HEAD`), 20206 (`=======`) and 20285 (`>>>>>>>`). The HEAD side
carried the **78-line** BL-724 entry, the incoming side the **78-line** BL-725 entry. Resolution kept
**both**, in that order, and restored the `---` section break between them (the break above the conflict
had been consumed by the BL-724 side). Nothing from either side was dropped, reordered or rewritten.

Counted with `grep -c`, never piped to `head`:

| Ref | `^## BL-` entries |
|---|---|
| `origin/main` before the round | **121** |
| after merging BL-724 | **122** |
| after the BL-725 union | **123** |

`121 + 1 + 1 = 123`. Exactly one occurrence each of `^## BL-724` and `^## BL-725`.

### Conflict markers

`grep -c '^<<<<<<<\|^=======$\|^>>>>>>>'` on `BACKLOG.md` after resolution: **0**.
Repository-wide scan excluding `node_modules` for `^<<<<<<< ` and `^>>>>>>> `: **0**.

### Verified on the merged tree

Against a real production build served from the merged tree at `http://localhost:3727`:

| Check | Result |
|---|---|
| `/preview` | **HTTP 200**, 181,010 bytes |
| `<footer` on the signed-out landing | **1** |
| "Terms of Service" / "Privacy Policy" / "Cookie Policy" | 1 / 1 / 1 |
| `/terms.html` / `/privacy.html` / `/cookies.html` hrefs present | 1 / 1 / 1 |
| **`/terms.html` loads** | **HTTP 200** |
| **`/privacy.html` loads** | **HTTP 200** |
| **`/cookies.html` loads** | **HTTP 200** |
| The served `/privacy.html` is the CORRECTED one | Apify **0**, Vercel **0**, Railway **1**, TikTok section **1** |

So on the merged result the footer renders **and** the policy it points at is the corrected document. That
is the whole point of the ordering, confirmed end to end rather than inferred from the merge order.

### Signed-in surfaces and the CTAs

Verified in the rendered output of the merged build:

| Thing | Count | Status |
|---|---|---|
| `Brands: book a call` | 1 | unchanged |
| `Get started` | 1 | unchanged |
| `https://calendly.com/clipershq/30min` | 1 | **byte-identical** |

The footer is inside `{!isLoggedIn && …}`, so a signed-in user renders the identical tree as before. No
source was authored this round, so nothing could have drifted: both merges applied their branches verbatim
and the only hand edit anywhere was the `BACKLOG.md` union.

---

# BUILD

Run in `C:/m727` on the fully merged tree, in this order.

* `npm ci` → exit **0** (run FIRST, before anything else).
* `npx prisma generate` → exit **0**, run explicitly **after** `npm ci` and **before** `tsc`, because `npm ci` wipes the generated client.
* `eslint` genuinely present: `npx eslint --version` → **v9.39.4**. The hooks gate is not silently no-opping.
* `npx tsc --noEmit` → exit **0**. `grep -c "error TS"` on the log = **0**.
* `npm run build` → **BUILD_EXIT=0**, read from `$?` and echoed directly, never piped through `tail`. One `Compiled successfully`; `grep -cE 'error TS|Failed to compile'` = **0**.
* **BL-348 hooks gate: `11 problems (0 errors, 11 warnings)`** against `eslint --config eslint.hooks.mjs --max-warnings 11`. It **passes**, and it passes **exactly at the limit**. All 11 are pre-existing `react-hooks/exhaustive-deps` warnings in files neither branch touched, but stated plainly because one new warning from any future round breaks the gate.

`tsc` and `next build` were both actually run. Neither was inferred from the other.

---

# MONEY SAFETY

Blob OID on `origin/main` (`de0169bd`) compared against merged `HEAD` (`fe8e29cd`). All seven identical:

| File | Blob OID on both refs |
|---|---|
| `src/lib/clip-earnings-writer.ts` | `ac5be7deb061768fec800aa89aae512a56a9e065` |
| `src/lib/earnings-calc.ts` | `797e20985ad57475ef321afcf3cb1ea7b0d6ab84` |
| `src/lib/balance.ts` | `e887f80acfc70fee438e719a32a60025eda22749` |
| `src/lib/tracking.ts` | `83ce4babfd39a6261114465639f2eac4e23bfceb` |
| `src/lib/clip-earnings-invariant-middleware.ts` | `61cef39395363c31f0c902dd4c64e8c06b3e6449` |
| `src/lib/money-decimal.ts` | `ef5cdae757b9ad3c23380ee8b63e279f98d0b6ac` |
| `src/lib/campaign-era.ts` | `106e16ad75125c3b10b6949a2981d33614c69ab9` |

No schema change, no `prisma migrate`, no DB write, no DB query of any kind. No clip's earnings, status or
payout was read or written. Neither merged branch contains a migration.

---

# THE PUSH, AND A FALSE FAILURE WORTH KNOWING ABOUT

`main` is pushed. **`origin/main` == local `HEAD` == `fe8e29cdcdf6ec63fc0d1832ce3eb18d62e95302`**,
confirmed with `git ls-remote origin refs/heads/main`. Both tags are on origin:
`pre-merge-BL-727` → `de0169bd`, `post-merge-BL-727` → `fe8e29cd`.

**`scripts/safe-push.mjs` printed a FAILURE that was wrong, and it must not be trusted in this form.** It
reported:

```
[safe-push] branch HEAD:main: push attempt 1/3 OK
[safe-push] ✗ PUSH FAILED — origin/HEAD:main (none) is NOT up to date with local HEAD (fe8e29c).
```

The push itself succeeded; the **verifier** failed. Given the refspec `HEAD:main` it looked for a local
tracking ref literally named `origin/HEAD:main`, found none, and read that absence as "not pushed". The
independent `git ls-remote` check above is what actually settles it, and it says the commit landed.

## And the opposite trap, hit on the very next push

Taking the obvious lesson from the above and calling `safe-push.mjs main` instead produced a **real**
failure, and a dangerous one:

```
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
[safe-push] ✗ PUSH FAILED — origin/main (fe8e29c) is NOT up to date with local HEAD (9ea5339).
```

`C:/m727` is a **detached** worktree, so the bare name `main` does not mean "what I have checked out". It
resolves to the local branch ref `main`, which is held by `C:/b575` and still sits at the stale
`91b84410`. The push tried to send that stale commit and the remote correctly rejected it as a
non-fast-forward. Nothing was lost, but a push that "succeeded" here would have **rewound `main` by
dozens of commits**.

**So both forms fail from a detached worktree, in opposite directions:**

| Form | Push | Verifier | Danger |
|---|---|---|---|
| `safe-push.mjs main` | pushes the **wrong** (stale branch) commit | correctly fails | would rewind `main` if it ever succeeded |
| `safe-push.mjs HEAD:main` | pushes the **right** commit, succeeds | falsely reports failure | none, but the alarm is untrustworthy |

**Practical rule for future rounds: from a detached merge worktree, use `HEAD:main` and confirm the result
with `git ls-remote origin refs/heads/main` rather than believing the script either way.** That is what
was done here, twice. Reported, not fixed, since this round is merge-only.

---

# WHAT A REVIEWER WOULD SEE, ON THE LIVE SITE

The live URLs to check are:

* Public landing (the page a TikTok reviewer opens): **https://clipershq.com/** — which redirects to **https://clipershq.com/preview**
* **https://clipershq.com/privacy.html**
* **https://clipershq.com/terms.html**

## Immediately after the push, the deploy had NOT completed

Recorded rather than skipped, because it is the state anyone checking too early would have seen:

| Live check, minutes after the push | Result |
|---|---|
| `https://clipershq.com/privacy.html` size | 3,737 bytes — the **old** document |
| "Apify" on the live policy | **1** (still present) |
| "Vercel" on the live policy | **1** (still present) |
| "Connecting Your TikTok Account" | 0 |
| `<footer` on `https://clipershq.com/preview` | **0** |

Railway builds on push to `main`. The live site was polled every 25 seconds; the changeover landed on the
**7th** poll, roughly **3 minutes** after the push.

## DEPLOY CONFIRMED — this is what a reviewer sees right now

Fetched fresh from the live site with `Cache-Control: no-cache`, after the changeover:

### https://clipershq.com/ — HTTP 200

Follows its redirect to `/preview` and serves 181,010 bytes containing:

| Check | Count |
|---|---|
| `<footer` | **1** |
| "Terms of Service" | 1 |
| "Privacy Policy" | 1 |
| "Cookie Policy" | 1 |
| `/terms.html` href | 1 |
| `/privacy.html` href | 1 |
| `/cookies.html` href | 1 |

The footer is live on the page a TikTok reviewer opens.

**And the hero survived the deploy unchanged**, verified on the live HTML rather than only on the merged
tree: `Brands: book a call` **1**, `Get started` **1**, `calendly.com/clipershq/30min` **1**.

### https://clipershq.com/privacy.html — HTTP 200, and it is the CORRECTED document, not a cached old one

**8,582 bytes**, up from the 3,737 of the old version, which is itself proof the cache turned over:

| Check on the live policy | Count |
|---|---|
| **Apify** | **0** |
| **Vercel** | **0** |
| Railway | 1 |
| Sentry | 1 |
| Ably | 1 |
| HikerAPI | 1 |
| LamaTok | 1 |
| ScrapeBadger | 1 |
| TikHub | 1 |
| **"Connecting Your TikTok Account"** | **1** |

`Last updated: August 2026`.

**Both false statements are gone from the live, publicly served, legally-operative document.** Every
provider it now names is one the platform actually uses.

### https://clipershq.com/terms.html — HTTP 200

Serves `<h1>Terms of Service</h1>`. Unchanged by this round, as intended: BL-724 confirmed it needed no
edit.

### https://clipershq.com/cookies.html — HTTP 200

The third footer link also resolves.

**All three footer links resolve to live pages that load, and the Privacy Policy link now lands on the
corrected policy.** This round is reviewer-ready.

---

# NEXT

1. **[YOU]** Once the deploy lands, open `https://clipershq.com/` signed out and confirm the footer, then click Privacy Policy and check it says "Last updated: August 2026" and names Railway rather than Apify or Vercel. A hard refresh clears any cached copy.
2. **[YOU]** Register the TikTok Website URL as `https://clipershq.com`, per BL-724 §2.7 option A, now available.
3. **[YOU]** Verify the domain and register the Terms of Service and Privacy Policy URLs, per BL-724 §2.5.
4. **[BUILD]** Port BL-723 to Login Kit before any demo video can be filmed, per BL-724 §2.4 and PART 3.

**Rollback:** `git revert -m 1 fe8e29cd` removes the footer; `git revert -m 1 771a3654` restores the old
policy and `TOS_VERSION` `v1`. Revert them in that order, or `git reset --hard pre-merge-BL-727` to undo
both at once. Reverting only `771a3654` would leave the footer pointing at the uncorrected policy, which
is the exact state this round exists to prevent.
