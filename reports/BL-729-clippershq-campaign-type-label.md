# BL-729 — the owner sets what a campaign IS, in the top left of the clipper card
**Merged to main** `2ceb2eef` · **Branch** `checkpoint/BL-729` @ `d6295b37` · **Base** `6688bad0` · 2026-08-07 · **Display only**
## 0. Recovery: what survived, what this session added
A prior session on this ticket died mid-build. Nothing restarted, nothing discarded. Branch `checkpoint/BL-729` existed **locally at `6688bad0` — which IS `origin/main`, so it carried ZERO commits**, and **not on origin** (`git ls-remote origin "*BL-729*"` → empty). The work survived **uncommitted** in worktree `C:/b729`: 5 modified + 3 untracked, backed up to a patch before anything was touched. **No** docs or report file for BL-729 existed. `C:/b575` left **exactly as found** — stale at `91b84410`, not used, not cleaned.
**Prior session completed:** the column (schema + SQL + already applied to prod + `prisma generate` already run),
`src/lib/campaign-type-label.ts` whole, both API write paths, the clipper card, the radio-group control, a 78-check
offline harness. **Its ruling — a RADIO GROUP, not a select, not free text — is preserved.**
**This session added:** two more a11y passes — one finding **7 real defects** in that work, one verifying the fixes
and **rejecting one of mine** (§6); a ninth defect found here that neither review could see; a real Chromium
measurement (the prior harness proved arithmetic only); 26 regression guards; BACKLOG; commits, tags, verified push,
merge, this report. Harness grew 78 → **104 checks**.
## 1. What the top left showed before
`CampaignsRedesign.tsx:31-35` lowercased `campaign.description` and substring-matched `"app"`, then `"song"`.
**The owner had no control over it** — no field in the admin form writes `description`. The rule is also loose enough
to be wrong: of 14 live campaigns it buckets 8 song / 3 app, and `"happy apparel drop"` reads **App** ("apparel").
## 2. The column — confirmed, not re-applied
`campaigns.typeLabel VARCHAR(24) NULL`, additive, no default, no backfill. Applied with `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` via `run-schema-sql.js`, **never `prisma migrate`**; `npx prisma generate` only. The prior session had **already applied it**, so this round **confirmed** it against `information_schema` rather than re-running it:
```
| typeLabel | character varying | 24 | is_nullable=YES | column_default=null |
| total 33  | set_count 0 | null_count 33 |    <-- 33 campaigns, 0 labelled
```
## 3. NULL renders exactly as today — measured, not asserted
NULL is not a special case bolted on; it **is** the pre-BL-729 path. `resolveCampaignTypeLabel` falls through to the old derivation kept verbatim, `app` before `song`. The harness runs the **new resolver over every real campaign** against the old rule copied verbatim from `origin/main`, and the browser harness confirms it visually (**`a NULL label renders NO pill`** at all five widths):
```
14 live campaigns, 0 with an owner label · buckets: song=8 app=3 other=3
PASS  LIVE: no campaign without a label changed badge or filter bucket
PASS  LIVE: the typeLabel column exists and reads
```
## 4. The control: a radio group, and why
The chip-button rows used elsewhere give one tab stop **per chip**, no arrow keys, and convey selection **by colour alone**. A native `fieldset` + `legend` + `sr-only` real radios inside styled labels gives one tab stop, arrow keys and `aria-checked` for free. Nine presets + **Automatic** + **Custom**; Automatic is first and default, because that is what every existing campaign already is. On **creation AND editing**, with the effect stated in the form — owner: *"Any change shows to clippers right away."* / admin: *"Your change goes to the owner for review before clippers see it."* `Home`/`End` deliberately **not** claimed: Chromium does not implement them for radio groups.
## 5. Validation is server-side; the form is only a convenience
`sanitizeCampaignTypeLabel` strips zero-width and bidi controls, folds every C0/C1 control to a space (the newline that would make the pill two lines tall), collapses whitespace, drops angle brackets, caps at 24, returns NULL for anything empty so **"no label" has one representation**. Both write paths call it: `POST` create and `PATCH` — the latter covering OWNER direct-save and the ADMIN `pendingEdit` diff alike. Nothing from the client is trusted.
```
PASS 200 chars capped at 24  PASS script tag leaves no angle brackets  PASS bidi override removed
PASS newline cannot make the pill two lines  PASS zero width space removed  PASS invisible-only -> NULL
```
## 6. THREE a11y passes — and the third rejected one of my own fixes
Review 1 (the prior session's ruling) chose the radio group. Review 2 found **7 defects in the delivered work**.
Review 3 verified those fixes and **rejected one**, correctly. Final: all fixed or reverted, all pinned by guards.
**D1 (BLOCKING)** `typeLabelError` was never reset on close, so a field holding **valid** text re-opened announced
**invalid** (3.3.1) → reset in `openCreate`, `openEdit`, `onClose`. **D2** focus moved before React committed
`aria-invalid` and the error paragraph, so the field was announced **valid** → `flushSync` commits first, toast last.
**D4** the counter was announced before the error → error leads. **D5** the group's hints were unassociated, so a
forms-mode admin never heard "goes to the owner for review" → `aria-describedby` on the fieldset. **D6** the hint
said the field appears "below this group" when it appears inside → corrected and conditional.
**D7 — REVERTED, not defended.** My fix removed `maxLength` and re-keyed the live region on a truncation counter.
Review 3: *"the only fix where the remedy is riskier than the defect it replaced."* Remounting a region whose text
is already present is the classic silent-live-region failure; the message was derived from **length** not from a
truncation event, so paste→backspace→type announced "limit reached" when nothing was truncated (**4.1.3, a false
status message**); and with `maxLength` gone every keystroke at the cap announced. `maxLength` restored, counter
deleted, single permanently-mounted region. **Disclosed residual:** a paste into an already-full field fires no
change and is not announced; the counter still reads 24 of 24 and the first paste that *reaches* the cap does.
**D3 — fixed at the real site.** My first fix was **unreachable dead code**: the strip pattern needs whitespace
before the word and the sanitizer trims, so it could never consume a whole label. The actual defect was one level
up, where the call site appended `" campaign"` to whatever came back — so `"Campaign"` was announced **"Campaign
campaign"**. The phrase is now composed in **one** place, making doubling structurally impossible.
**D8 — found here, by neither review, because neither could see localStorage.** `openCreate` passed `loadDraft()`'s
raw JSON straight to `setForm`. A draft saved before this round has no `typeLabelChoice` → **no radio checked** → an
unchecked radio group makes **every** radio a tab stop, destroying the exact property the group was chosen for.
Draft now spread over `defaultForm` and the choice narrowed to one the picker offers. **3.3.2:** the custom field had
`aria-required` but no visible indicator; it now carries the same asterisk as its siblings.
Passing throughout and unchanged: fieldset/legend grouping; sr-only radios genuinely focusable and arrow-operable;
focus ring **5.42:1**; selection icon **+** text never colour alone; target 44px vs AA's 24px; pill word **5.74:1**
worst case; icon tints 3.48:1 / 3.44:1 vs 3:1; 2.5.3 label-in-name holds; no duplicate announcement.
## 7. The clipper view — real browser, five widths
Chromium via Playwright against **the app's own compiled Tailwind** and the real card markup, not arithmetic.
**120 assertions, 0 failures**, at **320 / 375 / 414 / 1280 / 1440px**.
```
=== truncation actually observed ===
  320px: widew truncated (232->208), widem truncated (222->208), cjk truncated (240->208)
  375 / 414 / 1280 / 1440px: no case needed truncation (every 24-char label fit)
PASS 320: page does not scroll horizontally    PASS 320: a NULL label renders NO pill (card 288px)
PASS 320: "widew" clears the star (gutter 6px) PASS 320: "widew" stays ONE line (h 19px)
PASS 320: "cjk" clears the star (gutter 6px)   PASS 320: "cjk" card does not overflow its box
```
Worst cases are the widest 24 chars storable: 24 × `W`/`M`/full-width CJK. **Honest:** at 375px+ a 24-char label fits, so the cap is the primary defence and `truncate` the backstop engaging at 320.
## 8. Nothing else moved — proven by diff, not assertion
Of the **34 lines** in the card file mentioning `effectiveSpent`, `pct`, `isPast`, `dragScroll`, `Chevron`, `Completed` or `budget`, **exactly two differ** across the refs — and both **are** the type badge (its render line and the icon import). **BL-641**'s somesome (PAST, budget 9750, 383 approved clips → $9,750.00 of $9,750.00 at 100%), **BL-535**'s fully-spent rule and **BL-651**'s Completed row scrolling with arrows and edge fades are untouched. A past card never shows a type pill — it keeps its Completed pill, unchanged.
**Byte-identical by blob OID on BOTH refs** (not a working-tree sha256, which CRLF fakes):
```
ac5be7de clip-earnings-writer  797e2098 earnings-calc  e887f80a balance  83ce4bab tracking
61cef393 clip-earnings-invariant-middleware  ef5cdae7 money-decimal  106e16ad campaign-era
```
No clip's earnings or status changed, no payout touched; the only DB write was the `ALTER` already run. After:
**3,364 approved clips, $7,878.98, invariant 0 violations.**
## 9. Gates, stated honestly
`eslint v9.39.4` **confirmed present**, so the hooks gate is not silently a no-op. `tsc --noEmit` → **0 errors, exit
0**. `npm run build` → **exit 0**, "Compiled successfully", run on every code change, last exit 0. BL-348 hooks gate →
**0 errors, 11 warnings — at the limit of 11**, all pre-existing `exhaustive-deps` elsewhere. Offline **104/104**, browser **120/120**. Exit codes echoed directly, never piped through `tail`.
## 10. Reported, not fixed
The merge tree OID equals the branch tree OID (main had not advanced), so the build verified on the branch IS the
build of the merge. The shared `Modal` has no `role="dialog"`, no `aria-modal`, no focus trap, no focus return and an unlabelled close
button — **pre-existing**, affects every modal, wants its own round; not weighed in this verdict. An unselected
chip's border is 1.17:1, the page-wide pattern already used by Platforms and Pricing Model; the checked chip passes
at 4.83:1. **One honest change on the NULL path:** the link's accessible name now says "*, Song campaign*" not
"*, song campaign*" — capitalisation only (so `NBA` is not spoken "nuh-buh"), 2.5.3 matching is case-insensitive,
and the visible pill is byte-identical.
**Rollback:** `git revert -m 1 <merge>`. The column can stay — nullable, unread by the reverted code, every row NULL.