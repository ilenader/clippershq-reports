# BL-707 (ClippersHQ) — the form can no longer write auto_reject, and the 9 it already wrote are now rank

## The form never had an enforcement control. It derived the CONSEQUENCE from the rule TYPE the owner picked, so choosing what to CHECK was choosing to auto-refuse. That one function can now return `auto_reject` for no type at all, which closes both the form and the quieter omission route in six changed code lines. All 9 live rules across 7 campaigns are now `rank`, applied as a scoped data operation with the rollback captured first, and the clipper-facing text is byte-identical on every one of the 7 so no clipper sees anything.

**Shipped** `checkpoint/BL-707` `d5d6f90e`, merged to `main` **`4b1d86aa`**, origin==local verified. Base `0112361e`. Tags `pre-BL-707` / `post-BL-707` / `pre-merge-BL-707` / `post-merge-BL-707`, all pushed. Worktree `C:/b707`, short path, `node_modules` never junctioned. Every timestamp below is `::text` against DB `now()`, which read **2026-07-31 17:38 to 17:47 UTC**.

**Rollback:** `BL-707-ROLLBACK.sql` (committed) restores each campaign's exact prior `rulesJson`; then `git revert -m 1 4b1d86aa`, or `reset --hard pre-merge-BL-707`, for the code.

---

## PART 0 — the truth, established before anything changed

### The mechanism, with file:line

`src/app/(app)/admin/campaigns/page.tsx:329` serialises

```
enforcement: defaultEnforcementForType(r.type),
```

**The form has no enforcement control anywhere.** The owner picks a rule TYPE from a dropdown (`page.tsx:1276-1278`) whose options are labelled by what the rule **CHECKS**: "Required caption text", "Required sound", "Video length". `campaign-rules.ts:58-70` then silently derived the **CONSEQUENCE** from that type and returned `auto_reject` for exactly those three. So it is **neither a hidden control nor a server-side default**. It is a hardcoded type-to-consequence mapping applied without ever asking.

There was a second, quieter route to the same value: `parseCampaignRules` (`campaign-rules.ts:99`) falls back to the same function whenever a stored rule's `enforcement` key is missing or holds an invalid value. **Enforcement could therefore be set by pure omission**, not only by the form.

### All 9, confirmed as 9 across 7 campaigns

Every one is `REQUIRED_CAPTION_TOKENS`. Timestamps are the campaign's `updatedAt`, the last time its `rulesJson` was written.

| campaign | status | rule | what it checks (tokens) | written (::text) |
|---|---|---|---|---|
| BAD BITCH ANTHEM (0.50 CPM) | **ACTIVE** | r5 | `@gratefulxo1` | 2026-07-28 20:11:10.264 |
| BAD BITCH ANTHEM (0.50 CPM) | **ACTIVE** | r6 | `#BadBitchAnthem`, `#grateful` | 2026-07-28 20:11:10.264 |
| BAD BITCH ANTHEM (2.50 CPM) | **ACTIVE** | r6 | `@gratefulxo1` | 2026-07-20 11:28:37.735 |
| BAD BITCH ANTHEM (2.50 CPM) | **ACTIVE** | r7 | `#BadBitchAnthem`, `#grateful` | 2026-07-20 11:28:37.735 |
| CROCS | PAUSED | r2 | `@crocsshop_us`, `@wisdm8` | 2026-07-20 11:28:37.646 |
| Deja Shoe | PAUSED | r1 | `@crocsshop_us` | 2026-07-20 11:28:37.691 |
| GainzAlgo (REPOST CAMPAIGN) | PAST | r5 | `#gainzalgo` | 2026-07-26 15:23:06.095 |
| SomeSome | **ACTIVE** | r8 | `#SomeSomeApp` | **2026-07-31 10:06:49.515** |
| STRAENGE | PAST | r5 | `#STRAENGE` | 2026-07-28 11:12:06.576 |

The SomeSome rule was written **the same morning as this round**, which is the clearest possible evidence the mechanism was still live and still producing new auto_reject rules.

### If auto-rejection were switched on tomorrow

| campaign | status | PENDING clips it could reject now | already-APPROVED clips it would have been applied to |
|---|---|---|---|
| BAD BITCH ANTHEM (0.50 CPM) | ACTIVE | 0 | 57 |
| BAD BITCH ANTHEM (2.50 CPM) | ACTIVE | **4** | 32 |
| CROCS | PAUSED | 0 | 6 |
| Deja Shoe | PAUSED | **1** | 12 |
| GainzAlgo (REPOST CAMPAIGN) | PAST | 0 | **934** |
| SomeSome | ACTIVE | 0 | 12 |
| STRAENGE | PAST | 0 | 156 |
| **total** | | **5** | **1,209** |

**The exact false-rejection count is NOT computable from stored data, and I am not going to guess it.** Three reasons, each measured: `clips` has **no caption column at all**; `rule_shadow_decisions` only began **2026-07-24** and only the single-submit route writes to it; and of its **340** rows only **98** carry a caption. In the sample that *is* measurable, **10 captioned clips across 3 of the 7 campaigns**, the count of clips that would have been rejected is **0**, and the entire shadow table records **zero** `wouldReject` rows. That is a sample of ten. It is not an answer.

The honest headline is worse than a missing number: **the platform cannot yet measure its own rate at all.** Across the shadow table, **26 of 2,638 rule evaluations produced a verdict and 2,612 failed open, so 99.0% of evaluations decided nothing.**

**The estimate, clearly labelled as an estimate.** Applying R-2's measured machine caption-gate rate of **11.05%** to the 1,209 already-approved clips gives about **134 honest clippers wrongly refused**. Applying BL-664's measured human reviewer overturn rate of **0.77%** to the same population gives about **9**. That is the whole argument, and it holds without needing our own number.

**One rule is the argument in a single line.** A campaign named **"Deja Shoe"** carries an auto_reject rule demanding the token **`@crocsshop_us`**. Whether that is a copy-paste from the CROCS campaign or deliberate, an auto-rejecting machine would have refused clips over it with no human ever looking. **Its content was NOT changed by this round.** It needs an owner decision, not a silent fix.

## PART 1 — the fix, and which option was chosen

**Chosen: auto_reject is not selectable at all, and cannot be reached by default or by omission.** `defaultEnforcementForType` can now return `auto_reject` for **no type whatsoever**, and the `RULE_TYPES` metadata was aligned so table and function cannot drift apart.

**Why not the selectable-with-a-warning option.** A warning has to quote a number. BL-659 estimated **2 to 3 months** of shadow data before a false-rejection rate is calculable; the shadow table is **7 days old** and 99.0% fail-open. The only measured numbers available are the ones arguing against auto-rejection: 0.77% human, 11.05% machine. There is no honest warning to write yet, so the control does not exist yet.

**What this deliberately does NOT do, and why it matters.** The parser still reads an **explicitly stored** `auto_reject` back verbatim. `evaluateRulesShadow` sets `wouldReject` only for rules whose enforcement **is** `auto_reject`, so downgrading on read would have destroyed the shadow layer's ability to measure what auto-rejection would have done, which is exactly the evidence auto-rejection has to produce before it can ever be earned. **The gate belongs on the write side, and that is where it now sits.**

### The full diff of the protected file, printed and justified loudly

`src/lib/campaign-rules.ts` is on the byte-identical list. It changed, from `fc91216fdf1b248cdeb6fd2d0b863763e6fedc85` to `006c4d1a37c69bc7f54c27f2af695c400a586df0`, and it **had to**: it is the single place the default lives, so there is nowhere else the fix could be made. **Six changed code lines**, three in the table and three in the switch, plus comment:

```
-  { value: "REQUIRED_CAPTION_TOKENS", label: "Required caption text",  enforcement: "auto_reject" },
-  { value: "REQUIRED_SOUND",         label: "Required sound",         enforcement: "auto_reject" },
+  { value: "REQUIRED_CAPTION_TOKENS", label: "Required caption text",  enforcement: "rank" },
+  { value: "REQUIRED_SOUND",         label: "Required sound",         enforcement: "rank" },
   { value: "LOGO_PRESENT_THROUGHOUT", label: "Logo present (rank)",   enforcement: "rank" },
   { value: "POSTING_WINDOW",         label: "Posting window",         enforcement: "rank" },
-  { value: "VIDEO_LENGTH",           label: "Video length",           enforcement: "auto_reject" },
+  { value: "VIDEO_LENGTH",           label: "Video length",           enforcement: "rank" },

 export function defaultEnforcementForType(type: RuleType): RuleEnforcement {
   switch (type) {
     case "REQUIRED_SOUND":
     case "REQUIRED_CAPTION_TOKENS":
     case "VIDEO_LENGTH":
-      return "auto_reject";
     case "LOGO_PRESENT_THROUGHOUT":
     case "POSTING_WINDOW":
       return "rank";
     default:
       return "human_only";
   }
 }
```

The option **labels** were deliberately left untouched, because they are the strings actually rendered in the dropdown and changing them would change what the owner sees.

## PART 2 — the cleanup, as a data operation

**The rollback was captured BEFORE any write.** `scripts/bl707-snapshot.js` (read only, one SELECT) recorded every affected campaign's exact `rulesJson` and emitted **`BL-707-ROLLBACK.sql`**, seven statements each keyed to one campaign id, committed to the repo so it outlives this worktree. Snapshot taken at DB now() **2026-07-31 17:42:23.767164+00**, with per-campaign `rulesJson` md5 `ba73b47e`, `0431eb6c`, `725eae36`, `371323d3`, `1b8c0276`, `85d27d63`, `dbf0d55a`.

**The dry run compared every key of every rule.** `scripts/bl707-dryrun.js` (read only) ran the identical transform in the database as a SELECT and diffed before against after, key by key:

```
rule keys compared and IDENTICAL: 363
rule keys that DIFFER: 9  (every one must be an enforcement flip on a listed rule)
enforcement flips auto_reject -> rank: 9  (expected 9)
```

Zero illegal differences. Full before and after JSON per campaign was written for the owner to eyeball.

**The apply.** `scripts/migrations/BL-707-AUTOREJECT-TO-RANK.sql` through `run-mutation-once.js`: **7 statements, `rowCount=1` each.** Every statement is keyed to **ONE campaign id** and its `CASE` requires **both** a listed rule id **and** a current value of `auto_reject`, so it is idempotent and structurally cannot reach anything else. Order is preserved with `WITH ORDINALITY` plus `ORDER BY ord`, and only the `enforcement` key is set via `jsonb_set`, so `type`, `text`, `platforms` and `params` ride through untouched. The `requirements` column is never named in the file at all. **The admin form was not used.**

## PART 3 — every writer of `rulesJson`, and why none can reintroduce it

| # | writer | verdict |
|---|---|---|
| 1 | admin form, `admin/campaigns/page.tsx:331` | builds via `defaultEnforcementForType`, **fixed at the source** |
| 2 | `api/campaigns/route.ts:383` and `:450` | contain **0** references to `enforcement` (`grep -c`); they pass the client value straight through, so they cannot **invent** it, only persist what an owner-gated caller sent |
| 3 | `scripts/bl602-backfill-rulesjson.ts:51` | calls the same `defaultEnforcementForType`, so it **inherited the fix for free** |
| 4 | `api/clips/route.ts:822` | builds an in-memory object for evaluation, **writes nothing** |
| 5 | `scripts/bl668-live-proof.ts:172`, `scripts/test-bl-666-reviewer-note.ts:27-28` | hardcode `auto_reject` in **test fixtures**; `grep -c` for `campaign.update`/`campaign.create` returns **0** in both, so neither writes to the database |
| 6 | the database itself | `prisma/schema.prisma:611` declares `rulesJson Json?` with **no default** |

**No server-side default existed to fix.** The only default was the client-side one in `campaign-rules.ts`, and it is now closed on both its routes: the form path and the parse-time omission path.

## PART 4 — the evidence

**The form cannot produce auto_reject, proved on the SAVED OUTPUT.** `scripts/bl707-form-output-proof.ts` reproduces `page.tsx:320-330` verbatim using the **real imported helpers**, not a copy:

```
  r1  type=HUMAN_ONLY               enforcement=human_only
  r2  type=REQUIRED_CAPTION_TOKENS  enforcement=rank
  r3  type=REQUIRED_SOUND           enforcement=rank
  r4  type=LOGO_PRESENT_THROUGHOUT  enforcement=rank
  r5  type=POSTING_WINDOW           enforcement=rank
  r6  type=VIDEO_LENGTH             enforcement=rank
  r7  type=EDIT_QUALITY             enforcement=human_only
PASS  NO saved rule carries enforcement auto_reject  (7 rules produced)
PASS  defaultEnforcementForType returns auto_reject for NO type
PASS  the RULE_TYPES table itself contains no auto_reject
PASS  table value and function agree for every type (no drift)
PASS  a rule stored WITHOUT an enforcement key parses to something other than auto_reject
PASS  an INVALID stored enforcement value also cannot fall back to auto_reject
PASS  an EXPLICITLY stored auto_reject is still read back verbatim, so the shadow layer can still measure it
7 passed, 0 failed
```

**All 9 read `rank` from the database, with byte-identical params:**

| campaign | status | rule | enforcement | params |
|---|---|---|---|---|
| BAD BITCH ANTHEM (0.50 CPM) | ACTIVE | r5 | **rank** | `{"tokens":["@gratefulxo1"]}` |
| BAD BITCH ANTHEM (0.50 CPM) | ACTIVE | r6 | **rank** | `{"tokens":["#BadBitchAnthem","#grateful"]}` |
| BAD BITCH ANTHEM (2.50 CPM) | ACTIVE | r6 | **rank** | `{"tokens":["@gratefulxo1"]}` |
| BAD BITCH ANTHEM (2.50 CPM) | ACTIVE | r7 | **rank** | `{"tokens":["#BadBitchAnthem","#grateful"]}` |
| CROCS | PAUSED | r2 | **rank** | `{"tokens":["@crocsshop_us","@wisdm8"]}` |
| Deja Shoe | PAUSED | r1 | **rank** | `{"tokens":["@crocsshop_us"]}` |
| GainzAlgo (REPOST CAMPAIGN) | PAST | r5 | **rank** | `{"tokens":["#gainzalgo"]}` |
| SomeSome | ACTIVE | r8 | **rank** | `{"tokens":["#SomeSomeApp"]}` |
| STRAENGE | PAST | r5 | **rank** | `{"tokens":["#STRAENGE"]}` |

**`auto_reject` rules remaining platform-wide: 0.**

**The clipper-facing text is byte-identical on all 7.** `requirements` md5 and length, before against after:

| campaign | requirements md5 | length | rule count |
|---|---|---|---|
| BAD BITCH ANTHEM (0.50 CPM) | `1d94a8454cd4be9d6804cf7e404b1e0a` | 530 | 12 |
| BAD BITCH ANTHEM (2.50 CPM) | `b53e47a4ac44652cdbab9c6ded402c86` | 696 | 13 |
| CROCS | `3f364a4b2e6fe4feadf5ed635e5a3b3f` | 391 | 6 |
| Deja Shoe | `c75a205bd4bee77ac7d2f72418b1a59d` | 392 | 5 |
| GainzAlgo (REPOST CAMPAIGN) | `51eb1ede0346ac9be5a4991204287355` | 421 | 8 |
| SomeSome | `97500d13cc17700517b9792bd5ae2661` | 893 | 10 |
| STRAENGE | `b52412b401805bef4319531808ae28e3` | 471 | 8 |

Identical in both readings, every one. **No rule's checked content changed** (the dry run's 363 identical keys prove it key by key). **No other campaign was touched**: of the 9 other rules-carrying campaigns, **0** have an `updatedAt` inside the write window.

**`RULES_AUTO_REJECT_LIVE` is still off and gates nothing.** `grep -c` returns **0** in both `.env` and `.env.local`, so `isAutoRejectLive()` (`src/lib/auto-reject-flag.ts:20`, `process.env.RULES_AUTO_REJECT_LIVE === "true"`) evaluates false. That file is byte-identical.

**No clip status, earnings or payout changed, and nothing became clipper-visible.** 3686 APPROVED clips at **$10,271.99**, **0** earnings-invariant violations, **11** in-flight payout requests totalling **$423.15** in `finalAmount`. Nothing renders machine suspicion to any clipper: the only surface `enforcement` reaches is the **admin** reviewer note, never a clipper page.

> **What the owner would now have to do, deliberately, to enable auto-rejection at all: two separate acts, neither of which any UI performs.** First, write `"enforcement":"auto_reject"` into a campaign's `rulesJson` by hand, outside the form, because no dropdown, default or omission can produce it any more. Second, set `RULES_AUTO_REJECT_LIVE=true`, which is absent from every env file today. Neither happens by accident and neither happens by clicking.

## Accessibility review

**GO-WITH-NOTES, and it corrected one of my premises.** My claim of "no rendered change" **holds for the form**: the dropdown at `page.tsx:1276-1278` renders `rt.label` only and never `rt.enforcement`, and the edit path maps stored rules to `type` only. But `enforcement` **does** reach a rendered surface, through `reviewer-note.ts:182-193` into `ReviewerNoteCard.tsx:103-165`, which is the **admin clip reviewer** and never clipper-facing.

**Existing rules are unaffected**, and the lead asked for one cheap pre-merge check to prove it, which I ran: across **all 100 rule elements on 12 campaigns, 0 are missing the `enforcement` key and 0 carry an invalid value**, so the parse-time fallback is never consulted for any existing rule and no reviewer note changes today. Rules created **after** this merge will produce a different reviewer note, with no "would reject" headline. That is the intended effect, and it is stated rather than glossed.

**Follow-ups it raised, none merge-blocking, none actioned here.** (a) The rule-type picker never shows the consequence at all, which it rates **SC 3.3.2 and SC 1.3.1, Level A**, and which becomes **blocking on any round that flips shadow evaluation to live**; the cheapest fix is to put the consequence into the option label itself rather than add a described-by hint. It was explicit that blocking this round on a labelling fix would leave auto-reject armed for longer and would be worse on every axis. (b) `removeRequirement` focuses `req-remove-${idx-1}`, which does not exist once the list drops to one row (`page.tsx:883-892` against the render guard at `:1280`), so focus falls to `<body>`. (c) `src/components/ui/modal.tsx` has no focus trap, no `role="dialog"`, no `aria-modal` and no focus restore. (d) The hint at `page.tsx:1259` calling the type "used only for automated pre checks (shadow only for now)" becomes misleading the moment shadow flips live.

## Gates, honestly

`npm ci` **exit 0**, then `npx prisma generate` **exit 0** before any typecheck, because `npm ci` wipes the generated client. `npx tsc --noEmit` **TSC_EXIT=0 with 0 output lines**. `npm run build` **BUILD_EXIT=0** on the branch and **again on the merged tree**, each read from a log with the exit code echoed directly, never through a pipe. Prebuild: BYPASS detector **0 violations**, removed-fields **OK**, **hooks gate 0 errors / 11 warnings** (limit 11) with eslint **v9.39.4** confirmed present so the gate ran rather than silently no-opping. 61/61 static pages. The real diff was confirmed non-empty before any claim: 44 insertions and 5 deletions in `campaign-rules.ts`.

## Safety

6 money files plus `tracking.ts`, `campaign-era.ts` and `apify.ts` **byte-identical by blob OID** on both refs: `clip-earnings-writer.ts` 7aa6be48, `earnings-calc.ts` 797e2098, `balance.ts` e887f80a, `tracking.ts` 847dcf70, `clip-earnings-invariant-middleware.ts` 61cef393, `money-decimal.ts` ef5cdae7, `campaign-era.ts` 106e16ad, `apify.ts` **656bf4c0** so the BL-678 guards are intact and no Apify actor was run. **`campaign-rules.ts` is the one loudly justified exception**, diffed in full above. No rule added, removed or reordered; no rule's checked content changed; no other campaign touched; no clipper-facing text touched; no clip rejected, flagged or status-changed; no env flag flipped; no `prisma migrate`. No heredocs; one shell at a time. NO dashes.
