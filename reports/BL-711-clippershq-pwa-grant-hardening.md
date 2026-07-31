# BL-711 (ClippersHQ) — the PWA flag grant, hardened forward

## The server cannot observe a browser's standalone display mode, and no verification pretending otherwise was invented. What changed is that the grant no longer rests on a header any page script can send: `Sec-Fetch-Site` and `Origin` are forbidden header names the browser stamps, so the browser-console forge is closed and only non-browser tooling still works. Every grant from now on records when it happened and whether the account ever came back, which is exactly the gap that made BL-710's cleanup impossible. Not one of the 323 existing flags was touched and not one cent moved.

**Shipped** `checkpoint/BL-711` `c590b836`, merged to `main` **`8b5aaf57`**, origin==local verified. Base `501032b2`. Tags `pre-BL-711` / `post-BL-711` / `pre-merge-BL-711` / `post-merge-BL-711`, all pushed. Worktree `C:/b711`, short path, `node_modules` never junctioned. Every timestamp is `::text` against DB `now()`, which read **2026-07-31 19:06 to 19:14 UTC**. Handles and emails are never selected.

**Rollback:** `git revert -m 1 8b5aaf57`, or `reset --hard pre-merge-BL-711`. The three new columns are additive and nullable, so reverting the code leaves them harmlessly unread and nothing needs dropping.

---

## PART 0 — what can genuinely be verified server-side, and what cannot

**Stated first, because the honest answer shapes everything else: a browser's standalone display mode is a CLIENT fact and this server cannot observe it.** There is no request property that proves an installed app. Nothing below claims to prove the claim. What follows is defence in depth and provenance, which is what BL-710 recommended and what is actually achievable.

**1. `lastPWAOpenAt`, traced rather than assumed.** It is written by a **different path** from the grant: the hourly sync at `app-layout.tsx:150-161`, which fires only when `useIsPWA()` is true, and that hook reads the real `matchMedia("(display-mode: standalone)")` and `navigator.standalone`. **Is it equally forgeable? Per request, yes** — it lands on the same endpoint and the same header. **Over time, no.** A forged one-off request sets it once and it then goes stale, because the forger has to keep coming back on a schedule to keep it fresh. That asymmetry is real and it is the only genuine corroboration available.

**2. Request characteristics that differ, and how reliable each is.**

| signal | reliable or suggestive |
|---|---|
| `Sec-Fetch-Site`, `Origin` | **Reliable against browser-based forgery.** Both are FORBIDDEN HEADER NAMES: page JavaScript cannot set or override them, the browser stamps them. A fetch typed into the console on our own origin cannot lie about them. **Merely suggestive against non-browser tooling**, which can set anything |
| `User-Agent` | suggestive at best; trivially spoofed and does not reliably differ for an installed PWA |
| the `X-PWA-Mode` header itself | **not a signal at all.** It is a constant our own client always sends, which is the defect BL-708 identified |

**3. Can the grant be made conditional on a later corroborating signal? Yes, and it now RECORDS one.** It deliberately does **not gate the bonus** on it. Gating would mean an existing flag could stop applying the bonus, which this round is explicitly forbidden from doing, and BL-710 proved a legitimate installer who stopped clipping is indistinguishable from a forger. So the corroboration is captured as evidence for a future round rather than used as a weapon today.

## PART 1 — the hardening, and what a forger must now do

Three changes, all in `src/app/api/user/pwa-status/route.ts`. **No client file changed**, so a genuine installer's browser does exactly what it did yesterday: no extra friction, no delay, no second step.

**(a) Reject a request whose browser-set characteristics contradict the claim.** `Sec-Fetch-Site` present and `cross-site` or `none` refuses. A parsed `Origin` whose host differs from the serving host refuses.

> **FAIL OPEN ON ABSENCE, FAIL CLOSED ON CONTRADICTION**, which is the same shape as the posting-window rule and for the same reason. Older Safari sends no `Sec-Fetch-Site` at all, and refusing on absence would strip a genuine iOS installer of a bonus because of their browser's age. An unparseable `Origin` is treated as noise, not as a contradiction.

**(b) A dedicated limiter on the transition only**, 5 per hour per account, on the `false` to `true` edge. A genuine installer crosses that edge once in their life; the hourly refresh never reaches it, so nobody real can feel it.

**(c) Provenance recorded on every grant**, described in PART 2.

**What a forger must now do that they did not have to before:**

| | before | now |
|---|---|---|
| needed | an authenticated session, plus one `fetch` carrying `X-PWA-Mode: standalone` | the same, **plus** request characteristics a browser stamps and page JavaScript **cannot** override |
| a browser console on our own origin | **sufficient** | **refused** |
| non-browser tooling | worked | still works, but must replicate the stamped headers by hand, must not exceed 5 grant attempts an hour, and **will be recorded as an uncorroborated grant** |

**Said plainly: this does not make forgery impossible.** It removes the cheapest route and makes the remaining route leave a record. That is the honest ceiling given the server cannot observe display mode.

## PART 2 — provenance

Three **additive, nullable** columns on `users`, closing the exact gap BL-710 named:

| column | what it records |
|---|---|
| `pwaGrantedAt` | when **this** grant crossed false to true. Stored separately from `lastPWAOpenAt` **precisely because** `lastPWAOpenAt` is overwritten on every refresh and destroys the grant instant, which is why BL-710 could not do this retrospectively |
| `pwaGrantSource` | a coarse label for how the grant arrived, currently `client-standalone-claim` |
| `pwaGrantCorroboratedAt` | the first standalone refresh arriving at least **10 minutes** after the grant. Ten minutes is deliberately shorter than the hourly sync, so a genuine installer is corroborated on their first sync while a forged one-off request never returns and is never corroborated |

A fresh grant resets `pwaGrantCorroboratedAt` to null on purpose, so a re-install after an uninstall does not inherit the previous grant's corroboration.

**Applied with `ALTER TABLE users ADD COLUMN IF NOT EXISTS` on all three**, through `scripts/run-schema-sql.js`, which refuses DROP, TRUNCATE, DELETE, UPDATE, INSERT, ALTER COLUMN and RENAME. **`npx prisma generate` only. `prisma migrate` was NEVER run.** Verified in `information_schema` after applying:

```
| column_name            | data_type                   | is_nullable | column_default |
| pwaGrantCorroboratedAt | timestamp without time zone | YES         | null           |
| pwaGrantSource         | text                        | YES         | null           |
| pwaGrantedAt           | timestamp without time zone | YES         | null           |
```

Nullable, no default, no backfill. Every existing row keeps its current meaning exactly.

## PART 3 — the past is untouched, proved on live data

| measure | before (19:06:49) | after (19:14:20) | verdict |
|---|---|---|---|
| accounts with `isPWAUser` | **323** | **323** | identical |
| accounts with `pwaGrantedAt` not null | 0 | **0** | **nothing backfilled, nothing re-evaluated** |
| accounts with `pwaGrantCorroboratedAt` not null | 0 | 0 | forward only |
| approved earnings | **$10,336.36** | **$10,336.36** | identical to the cent |
| approved bonus total | **$470.29** | **$470.29** | identical to the cent |
| earnings-invariant violations | 0 | **0** | holds |
| approved clips | 3,686 | 3,691 | **+5 from ordinary platform activity in the eight minutes between readings, not from this round.** The money totals did not move |

**BL-708's figure of 319 has grown to 323**, which is four genuine installs since that audit and is worth knowing on its own: real people are still installing the app.

**No existing flag would lose its bonus.** The bonus is applied purely from `isPWAUser` inside `earnings-calc.ts`, which this round neither reads differently nor touches. Nothing in the change re-evaluates, downgrades or clears a flag; the only write to `isPWAUser` on the grant path is the same `false` to `true` transition as before, now accompanied by provenance. **BL-538's never-decrease guard is untouched and was never approached.**

## PART 4 — the bonus itself is unchanged

**`src/lib/earnings-calc.ts` is BYTE-IDENTICAL**, blob `797e20985ad57475ef321afcf3cb1ea7b0d6ab84` on both refs. `PWA_BONUS_PERCENT = 2` still sits at `:61` and is still applied exactly as it was. **`src/lib/gamification.ts` is byte-identical too**, blob `abbec6a0`, so the recalculation path the endpoint calls is unchanged. **This round changed only HOW the flag is granted, never how it is applied.**

## PART 5 — the evidence

`scripts/test-bl-711-pwa-grant-hardening.ts`, **9 passed, 0 failed**. It grants nothing, clears nothing, writes nothing and calls no provider; its only database access is a read-only SELECT.

**A genuine installer is not refused, so there is no added friction:**

```
  modern Chrome, installed app               contradiction=none
  same-site subdomain                        contradiction=none
  older Safari, NO sec-fetch-site at all     contradiction=none
  no Origin header (fail open on absence)    contradiction=none
  neither header present                     contradiction=none
  unparseable Origin is noise, not contradiction contradiction=none
PASS  every genuine-installer shape passes the new gate  (fail OPEN on absence, so an older browser is never penalised)
```

**A forged or cross-origin claim is refused:**

```
  cross-site fetch from another site         contradiction=sec-fetch-site=cross-site
  direct navigation / no browsing context    contradiction=sec-fetch-site=none
  Origin points at an attacker host          contradiction=origin-host-mismatch
  cross-site AND mismatched Origin           contradiction=sec-fetch-site=cross-site
PASS  every contradicting request context is refused
```

**Actual endpoint behaviour over real HTTP**, against a running server:

```
  unauthenticated POST with a perfect header set -> HTTP 401
PASS  an unauthenticated caller is refused before any database work
```

> **Overclaiming avoided, deliberately.** The **authenticated** forged-versus-genuine distinction could not be exercised over the wire without creating a session and mutating a real user's flag, which this round forbids. It is therefore proven against the **real exported gate** driven with **real `Request` objects** — the same function the handler calls, not a copy of it. That is stated rather than dressed up as an end-to-end test it is not.

**Provenance is recorded and readable:** the three columns exist, are nullable, and read 0 populated rows today, which is the correct forward-only state. The first genuine install after this deploy will populate `pwaGrantedAt` and `pwaGrantSource`, and its first standalone refresh an hour later will populate `pwaGrantCorroboratedAt`. The grant also emits `[PWA-GRANT] granted userId=... source=client-standalone-claim grantedAt=... corroborated=false`, and the corroboration emits `[PWA-GRANT] corroborated userId=... grantedAt=... corroboratedAt=...`, so both are visible in the log as well as the database.

### What a future round can now measure that BL-710 could not

BL-710 could positively confirm 168 of 319 flags and had to write "**NO for the other 151, and I will not estimate**", because nothing recorded how or when a flag was obtained and `lastPWAOpenAt` had already been overwritten. From this deploy onward, for every new grant, a future round can answer three questions directly: **when it was granted, by which path, and whether that account ever came back in a standalone context.** That turns "indistinguishable" into a query. It does nothing for the 323 already in place, and that is honest: their grant instants are genuinely unrecoverable.

## One pre-existing risk surfaced but deliberately NOT changed

`installed: false` in the request body still **clears** `isPWAUser` (the third branch of the POST handler). That is the legitimate uninstall path, but it is driven by a **client-controlled body field** with no corroboration, and it **removes** a flag rather than granting one, which is the more damaging direction. It now sits behind the same browser-context gate, so it is strictly harder to drive than before, but changing its behaviour would alter a legitimate flow and belongs in its own round. Recorded here rather than quietly fixed.

## Gates, honestly

`npm ci` **exit 0**, then `npx prisma generate` **exit 0** before any typecheck, and again after the schema edit. `npx tsc --noEmit` **TSC_EXIT=0 with 0 output lines**. `npm run build` **BUILD_EXIT=0** on the branch and **again on the merged tree**, each read from a log with the exit code echoed directly, never through a pipe. Prebuild: BYPASS detector **0 violations**, removed-fields **OK**, **hooks gate 0 errors / 11 warnings** (limit 11) with eslint **v9.39.4** confirmed present so the gate ran rather than silently no-opping. 61/61 static pages. The real `.ts` diff was confirmed non-empty before any claim: 105 changed lines in the route plus 9 in the schema. **No UI code was written, so no accessibility review was applicable.**

## Safety

6 money files plus `tracking.ts` and `campaign-era.ts` **byte-identical by blob OID** on both refs: `clip-earnings-writer.ts` 7aa6be48, `earnings-calc.ts` **797e2098**, `balance.ts` e887f80a, `tracking.ts` 847dcf70, `clip-earnings-invariant-middleware.ts` 61cef393, `money-decimal.ts` ef5cdae7, `campaign-era.ts` 106e16ad. Also unchanged: `apify.ts` **656bf4c0**, so the BL-678 guards are intact and no Apify actor was run, and `gamification.ts` `abbec6a0`. **Forward only:** no existing flag cleared, downgraded or re-evaluated; no clip's status, earnings or payout changed; no payout created, modified, approved or cancelled. Schema additive and nullable, applied via generate not migrate. No heredocs; one shell at a time. NO dashes.
