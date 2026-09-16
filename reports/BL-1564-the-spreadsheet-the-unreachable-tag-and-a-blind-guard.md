# BL-1564 — the spreadsheet he reads, a tag nobody could reach, and a guard that could not see his own list

**Round:** BL-1564 · **Endpoint:** LamaTok v2 hashtag · **Unit:** `api.cost_per_call_usd`
= $0.00060000, read by named key (never `ig_api`'s $0.00069064, which is 15.1% higher)

## The paragraph

**The spreadsheet now holds 2982 rows on its Emails sheet, up from 2237** — the file is
`Random/clipper_emails_ALL.xlsx` on his Desktop, in a *subfolder*, found by searching rather
than by a hard-coded path. **745 rows were added**: 657 from BL-1563's backlog (the rest of
that batch was already there) and 88 from this round's walk. **479 fresh tags are queued**
(129 with a recorded yield and an unwalked v2 surface, 2 re-opened, 346 with no record at
all). **And the next 1,000 will cost far more than the $7.13 this round was planned against:
measured here it is $13.92 per 1,000** at a net-new rate of **0.71% [0.49-0.93]** — against 2.11% last round
and the 3.08% before that. **The rate has roughly halved for the third round running.** That
is the finding; the addresses are the by-product.

## 1. What this project is, for a reader with no context

It finds video editors on TikTok and Instagram who put an email address in their bio, so
they can be contacted about clipping work. A paid vendor API returns hashtag pages; each page
carries up to 30 posts and, on TikTok, **the author's bio rides along for free**. Addresses
are extracted from those bios. A dedup guard refuses accounts and addresses already held. The
durable store is `master_leads.csv`; the operator actually reads an Excel workbook.

Standing fact, restated because every price here is a proxy for it: **13,007 addresses have
been collected and not one has ever been contacted.** All outreach columns are empty on all
rows. `outcomes.py` is 847 lines with production callers and 63 passing tests and has never
written a real outcome. **This project does not send.**

## 2. Safety, money, and the cap

Ten stores were backed up sha256-verified with bodies found **by shape** — `spend.json` under
`runs`, `clip_seen.json` a bare list of 2,193, `tiktok_pages_seen.json` under `pages` with
3,270 where a dict-only reader reports 3. `master_leads.csv` anchored at **74,074 rows × 72
columns**.

**All six corruption controls fired**, each on damage planted on purpose. The backup module's
own docstring says "THE FIVE"; there are six. They were **counted in the source** — and
counted by matching the *numbered* control lines, because `controls()` also prints a warning
and a summary line, so a naive count of print-sites answers 8 and would pass a threshold of 6
even with two real controls deleted.

**The cap was driven before the first call**, with `Budget` lifted out of `harvest_run.py` by
AST so it cannot drift from the class the walk uses: a funded budget allows and the meter
advances; a $0.00 budget raises on the first reserve; **the meter does not advance on a
refusal**; a budget funded for exactly 3 calls allows 3 and refuses the 4th; and the proof
**wrote nowhere** — all ten stores' sha256 unchanged. Result: **THE CAP BINDS**.

## 3. Part 1 — the 911 into the spreadsheet, and what that exposed

The workbook was **found by searching**, not by a path: it sits in a *subfolder* of a Desktop
this machine redirects into OneDrive, and a hard-coded path once reported "workbook not
found", which reads exactly like *deleted* and was nothing of the kind.

Counted with a parser, never by counting lines — bios contain newlines. BL-1563's batch:
**908 records, 908 distinct account ids, 911 distinct addresses.**

|  |  |
|---|---|
| records parsed | 908 |
| distinct account ids | 908 |
| distinct addresses | 911 |
| skipped — account already in the workbook | 246 |
| skipped — every address already present | 5 |
| **appended** | **657** |
| distinct addresses on the sheet | 2172 → 2831 (+659) |
| rows marked `Platform` + `Tag` + `Round=BL-1563` | 657 |
| C0 control bytes asserted before writing | 0 |

Three columns as before — profile **link** (not the handle), Instagram, Email — plus
**Platform and Tag on every new row** so this batch is visible as a batch. **The Instagram
column was left blank**: zero of 1,104 bios once carried an instagram.com URL, BL-1563 did not
even keep the bio for these accounts, and a handle written in text is not proof of an account.
A wrong link is worse than a blank one.

Read back per sheet after writing: Emails 2237 → 2894, **No email and Unjudged leads
unchanged**. A workbook once silently lost 66 addresses and nobody noticed for a round.

### 3a. THE FINDING: the guard reads master, he reads the workbook, and they are not the same store

|  |  |
|---|---|
| master (BL-1563 round start) | 73144 TikTok handles, 12886 addresses |
| workbook Emails | 1889 TikTok handles, 2172 addresses |
| workbook handles **not** in master | 1775 |
| workbook addresses **not** in master | 1941 |
| master addresses **not** in the workbook | 12655 |

**27.1% of BL-1563's "net-new" batch was already in his spreadsheet** — 246 accounts — and
**none of them were in master**, so the guard could not have known. `DedupGuard.build()` reads
`master_leads.csv` only. The two stores have drifted until they are nearly disjoint: **1775
of the workbook's 1889 TikTok handles (94.0%) are absent from master**, while 12655 of master's
addresses are absent from the workbook.

The fix costs $0.00: `build()` already takes `extra_accounts` and `extra_addresses`. This
round's walk feeds both, and the guard loaded **1,529 accounts master does not have**.

## 4. Part 2 — the tag nobody could reach, and the class of bug behind it

`nightwingedit` was cut at **page 42** by a $0.05 smoke-test cap after yielding 14 addresses
off 334 accounts — **4.19%, one of the best rates on record** — and every resume since has
skipped it. The ledger recorded it identically to a tag that had been walked to exhaustion.

**The shape, not the instance.** `TagLedger.record()` is called at the end of `walk_tag`
*unconditionally*, including when the walk was cut by the cap or halted by the stop event,
and `TagLedger.walked()` then returned True **because the key existed**. Nothing anywhere
asked *why* the walk stopped.

Auditing the whole ledger found **seven** such tags, not one:

| tag | cut at page | authors | addr | rate |
|---|---|---|---|---|
| `nightwingedit` | 42 | 334 | 14 | 4.19% |
| `clarkkentedit` | 94 | 551 | 21 | 3.81% |
| `bellinghamedit` | 104 | 581 | 16 | 2.75% |
| `moneyheistedit` | 143 | 391 | 7 | 1.79% |

And three that correctly **stay** closed:

| ledger key | why it STAYS closed |
|---|---|
| `darriusedit` | v1 key: never walked on v2 at all, so its v2 key is free already. Not retired -- just unwa |
| `garlandedit` | v1 key: never walked on v2 at all, so its v2 key is free already. Not retired -- just unwa |
| `miketysonedit@v2` | REAL-FIGHTER tag: 1.21%% [0.68-2.15] measured three times, non-overlapping with film's 3.4 |

### 4a. Counting the sites, with both instruments

**AST** resolved **8** sites that decide "already walked", every one in
`clippershq/email_harvester.py`: the `walked()` gate, the unconditional `record()`, and six
reads of `done_tags`. **grep** returned 63 text lines over the same names.

**Which answered: the AST.** `TagLedger.walked()` is a real attribute call and resolves
cleanly; grep's extra lines are comments and docstrings about the same three names. Neither
is trusted alone — the AST cannot see a call built inside a string literal, and a bare-word
grep once over-counted a module **440x**.

**The fix is general, and both halves were needed.** The ledger now records a `stop_reason`
on every write and `walked()` returns True only for a **finished** state. The same bug lived
in the checkpoint: `done_tags.add(tag)` was also unconditional, so fixing only the ledger
would have left a resume against the run's own checkpoint still skipping a cut tag. Of seven
past fixes tested by driving them, **only 1 of 7 was general and 3 of the 6 local ones were
still failing** — so both halves were driven, not read.

**Driven, with negative controls:** every stop state classifies correctly; `walked()` retires
the finished and re-opens the cut; it reads the **historical** ledger, where **0 of 647
entries had a `stop_reason` field**, with no migration pass; and a genuinely drained tag and a
wall-stopped tag both **stay retired** — a test that only proves things re-open would pass on
code that had simply disabled the ledger.

Re-opened on the live ledger: **10** entries (the seven above plus three v1 entries with no
recorded reason at all, which **fail open** — failing open costs one re-walk, failing closed
costs the tag forever).

**`guard.report()` is now dumped after every tag**, which splits the refusal count BL-1563
could only report merged.

## 5. Part 3 — the depth wall, recorded as a wall and not as exhaustion

BL-1563 measured it: **33 of 75 tags stopped between page 168 and 171 and not one went
beyond**, none near the walker's own 200-page ceiling. They carried **822 of that round's 911
addresses**. The feed simply stops serving at ~2,000–2,800 items with the tag's supply
untouched — and it reports that **the same way it reports a drained tag: an empty list**.
Only page depth separates them.

`DEPTH_WALL_LO = 165` is now a named constant in the shipped module, and every ledger entry
carries its classification:

| stop_reason | tags |
|---|---|
| saturated | 485 |
| drained | 103 |
| depth_wall | 49 |
| cut_by_stop | 5 |
| unknown | 3 |
| cut_by_cap | 2 |

**49 tags across all rounds are now recorded as `depth_wall`, not `drained`.** The distinction
decides whether anyone ever re-walks them if the endpoint's ceiling moves. Nothing deeper is
reachable at any price today.

⚠️ **And the body-hash saturation detector fired 0 times in 75 tags.** It carries no weight
and has never been shown to work on this endpoint, so saturation is being decided by "empty
list" alone — the exact string the depth wall also returns. It is not trusted here.

### 5a. The v2 uplift is not uniform

Pooled, v2 returns **7.12x** the accounts of the plain endpoint (704.4 vs 98.9 per tag, median
6.83x). But **49 tags grew 9.9x and delivered 884 net-new, while 23 tags SHRANK on v2 and
produced 2 net-new between them.** A third of the supply was worth *less* on the richer
endpoint. Report growth per tag; do not assume v2 always wins.

## 6. Part 4 — the fresh tags, published in full

**543 candidates** generated in the `<name>edit` form from named people, films, shows,
characters, clubs and drivers — every name hand-checked as a real thing, because 35 of 35
invented "fresh" tags once returned server errors and then looked fresh in the ledger forever
precisely because nobody could ever walk them.

⚠️ **Shape generates; recorded yield orders.** Tag shape is **refuted** as a predictor —
SPECIFIC 3.01% [2.86–3.17] against GENERIC 3.03% [2.14–4.27], and with the tag as the unit of
randomisation the difference is **+0.02 points [−1.25, +1.13]**. It is used only to build
candidates, never to rank them.

⚠️ **No real-fighter tags.** Boxing and MMA measure **1.21% [0.68–2.15]** across three
independent measurements, non-overlapping with film's 3.43%; Canelo, Khabib and Makhachev
returned zero. `miketysonedit` is in the re-opened set and was **still refused**. Fight-adjacent
*films* — Rocky, Creed, Raging Bull, Warrior, Southpaw, Bloodsport — are a different and good
bucket and are included. `#caredit` is left alone as instructed. The refusal list was proven on
planted controls: **4 of 4 forbidden names refused, 0 allowed names wrongly refused** — a
filter that never fires is indistinguishable from one that does not work.

⚠️ **Expect a third to be duds.** 25 of 75 tags (33.3%) returned zero last round, and dead tags
are **not predictable**: a cross-validated classifier scores 19.6% [15.4–24.5] against a 15.29%
base rate. Budget for it rather than trying to dodge it.

### 6a. Queue 1 — a recorded yield and an unwalked v2 surface (129 tags, ranked)

The ledger keys on **tag *and* endpoint**, so a tag walked on the plain endpoint is *not*
walked on v2 — and v2 goes ~7x deeper. These have a known yield and an untouched surface.

| # | tag | bucket | authors | addr | recorded yield |
|---|---|---|---|---|---|
| 1 | `makimaedit` | anime | 87 | 3 | 3.45% |
| 2 | `realmadridedit` | football | 87 | 3 | 3.45% |
| 3 | `itachiedit` | anime | 88 | 3 | 3.41% |
| 4 | `spartacusedit` | tv | 61 | 2 | 3.28% |
| 5 | `aliensedit` | film | 92 | 3 | 3.26% |
| 6 | `tenetedit` | film | 93 | 3 | 3.23% |
| 7 | `sanjiedit` | anime | 94 | 3 | 3.19% |
| 8 | `sakaedit` | football | 96 | 3 | 3.12% |
| 9 | `gohanedit` | anime | 97 | 3 | 3.09% |
| 10 | `osimhenedit` | football | 97 | 3 | 3.09% |
| 11 | `verstappenedit` | f1 | 136 | 4 | 2.94% |
| 12 | `goodfellasedit` | film | 103 | 3 | 2.91% |
| 13 | `henryedit` | football | 104 | 3 | 2.88% |
| 14 | `theflashedit` | film | 140 | 4 | 2.86% |
| 15 | `bourneedit` | film | 105 | 3 | 2.86% |
| 16 | `southpawedit` | film | 71 | 2 | 2.82% |
| 17 | `grimmjowedit` | anime | 71 | 2 | 2.82% |
| 18 | `nobaraedit` | anime | 108 | 3 | 2.78% |
| 19 | `shinobuedit` | anime | 72 | 2 | 2.78% |
| 20 | `griffithedit` | anime | 36 | 1 | 2.78% |
| 21 | `thorfinnedit` | anime | 109 | 3 | 2.75% |
| 22 | `prisonersedit` | film | 74 | 2 | 2.70% |
| 23 | `ipmanedit` | film | 75 | 2 | 2.67% |
| 24 | `lukadoncicedit` | nba | 75 | 2 | 2.67% |
| 25 | `beerusedit` | anime | 113 | 3 | 2.65% |
| 26 | `moonknightedit` | tv | 152 | 4 | 2.63% |
| 27 | `salahedit` | football | 76 | 2 | 2.63% |
| 28 | `liverpooledit` | football | 115 | 3 | 2.61% |
| 29 | `johnramboedit` | film | 40 | 1 | 2.50% |
| 30 | `madaraedit` | anime | 81 | 2 | 2.47% |
| 31 | `mancityedit` | football | 81 | 2 | 2.47% |
| 32 | `bladerunneredit` | film | 125 | 3 | 2.40% |
| 33 | `mikasaedit` | anime | 127 | 3 | 2.36% |
| 34 | `sashaedit` | anime | 127 | 3 | 2.36% |
| 35 | `robocopedit` | film | 86 | 2 | 2.33% |
| 36 | `gerrardedit` | football | 87 | 2 | 2.30% |
| 37 | `zidaneedit` | football | 134 | 3 | 2.24% |
| 38 | `lampardedit` | football | 136 | 3 | 2.21% |
| 39 | `kakashiedit` | anime | 93 | 2 | 2.15% |
| 40 | `kenpachiedit` | anime | 93 | 2 | 2.15% |
| 41 | `megumiedit` | anime | 93 | 2 | 2.15% |
| 42 | `russelledit` | f1 | 93 | 2 | 2.15% |
| 43 | `scarfaceedit` | film | 96 | 2 | 2.08% |
| 44 | `daredeviledit` | tv | 96 | 2 | 2.08% |
| 45 | `tottenhamedit` | football | 96 | 2 | 2.08% |
| 46 | `blackpantheredit` | film | 97 | 2 | 2.06% |
| 47 | `kickboxeredit` | film | 98 | 2 | 2.04% |
| 48 | `vegetaedit` | anime | 98 | 2 | 2.04% |
| 49 | `americanpsychoedit` | film | 99 | 2 | 2.02% |
| 50 | `shutterislandedit` | film | 99 | 2 | 2.02% |
| 51 | `messiedit` | football | 102 | 2 | 1.96% |
| 52 | `sicarioedit` | film | 103 | 2 | 1.94% |
| 53 | `kaneedit` | football | 103 | 2 | 1.94% |
| 54 | `ronaldoedit` | football | 107 | 2 | 1.87% |
| 55 | `doctorstrangeedit` | film | 109 | 2 | 1.83% |
| 56 | `jaysontatumedit` | nba | 55 | 1 | 1.82% |
| 57 | `historiaedit` | anime | 168 | 3 | 1.79% |
| 58 | `yujiedit` | anime | 56 | 1 | 1.79% |
| 59 | `odegaardedit` | football | 60 | 1 | 1.67% |
| 60 | `missionimpossibleedit` | film | 121 | 2 | 1.65% |
| 61 | `thewireedit` | tv | 68 | 1 | 1.47% |
| 62 | `hellboyedit` | film | 70 | 1 | 1.43% |
| 63 | `sanemiedit` | anime | 71 | 1 | 1.41% |
| 64 | `lokiedit` | tv | 145 | 2 | 1.38% |
| 65 | `bayernedit` | football | 145 | 2 | 1.38% |
| 66 | `zoroedit` | anime | 150 | 2 | 1.33% |
| 67 | `dortmundedit` | football | 77 | 1 | 1.30% |
| 68 | `lawedit` | anime | 78 | 1 | 1.28% |
| 69 | `breakingbadedit` | tv | 78 | 1 | 1.28% |
| 70 | `debruyneedit` | football | 78 | 1 | 1.28% |
| 71 | `lewandowskiedit` | football | 78 | 1 | 1.28% |
| 72 | `shaqedit` | nba | 84 | 1 | 1.19% |
| 73 | `wonderwomanedit` | film | 85 | 1 | 1.18% |
| 74 | `jimmybutleredit` | nba | 85 | 1 | 1.18% |
| 75 | `sopranosedit` | tv | 89 | 1 | 1.12% |
| 76 | `narcosedit` | tv | 89 | 1 | 1.12% |
| 77 | `kokushiboedit` | anime | 90 | 1 | 1.11% |
| 78 | `eternalsedit` | film | 91 | 1 | 1.10% |
| 79 | `neymaredit` | football | 92 | 1 | 1.09% |
| 80 | `aquamanedit` | film | 94 | 1 | 1.06% |
| 81 | `terminatoredit` | film | 94 | 1 | 1.06% |
| 82 | `arminedit` | anime | 94 | 1 | 1.06% |
| 83 | `braveheartedit` | film | 95 | 1 | 1.05% |
| 84 | `shikamaruedit` | anime | 95 | 1 | 1.05% |
| 85 | `aizenedit` | anime | 97 | 1 | 1.03% |
| 86 | `jiraiyaedit` | anime | 98 | 1 | 1.02% |
| 87 | `drogbaedit` | football | 98 | 1 | 1.02% |
| 88 | `kawhiedit` | nba | 100 | 1 | 1.00% |
| 89 | `modricedit` | football | 100 | 1 | 1.00% |
| 90 | `garouedit` | anime | 102 | 1 | 0.98% |
| 91 | `nezukoedit` | anime | 105 | 1 | 0.95% |
| 92 | `sasukeedit` | anime | 112 | 1 | 0.89% |
| 93 | `walterwhiteedit` | tv | 115 | 1 | 0.87% |
| 94 | `shanksedit` | anime | 121 | 1 | 0.83% |
| 95 | `rengokuedit` | anime | 124 | 1 | 0.81% |
| 96 | `obanaiedit` | anime | 129 | 1 | 0.78% |
| 97 | `neueredit` | football | 135 | 1 | 0.74% |
| 98 | `constantineedit` | film | 132 | 0 | 0.00% |
| 99 | `friezaedit` | anime | 130 | 0 | 0.00% |
| 100 | `nanamiedit` | anime | 116 | 0 | 0.00% |
| 101 | `underworldedit` | film | 110 | 0 | 0.00% |
| 102 | `katakuriedit` | anime | 108 | 0 | 0.00% |
| 103 | `obitoedit` | anime | 107 | 0 | 0.00% |
| 104 | `gaaraedit` | anime | 106 | 0 | 0.00% |
| 105 | `mbappeedit` | football | 106 | 0 | 0.00% |
| 106 | `fodenedit` | football | 105 | 0 | 0.00% |
| 107 | `gaviedit` | football | 103 | 0 | 0.00% |
| 108 | `minatoedit` | anime | 98 | 0 | 0.00% |
| 109 | `askeladdedit` | anime | 97 | 0 | 0.00% |
| 110 | `reineredit` | anime | 96 | 0 | 0.00% |
| 111 | `juventusedit` | football | 96 | 0 | 0.00% |
| 112 | `acmilanedit` | football | 95 | 0 | 0.00% |
| 113 | `mahitoedit` | anime | 94 | 0 | 0.00% |
| 114 | `denjiedit` | anime | 93 | 0 | 0.00% |
| 115 | `schumacheredit` | f1 | 92 | 0 | 0.00% |
| 116 | `brolyedit` | anime | 88 | 0 | 0.00% |
| 117 | `oldboyedit` | film | 86 | 0 | 0.00% |
| 118 | `ulquiorraedit` | anime | 86 | 0 | 0.00% |
| 119 | `pedriedit` | football | 83 | 0 | 0.00% |
| 120 | `predatoredit` | film | 82 | 0 | 0.00% |
| 121 | `rockleeedit` | anime | 81 | 0 | 0.00% |
| 122 | `ongbakedit` | film | 78 | 0 | 0.00% |
| 123 | `bloodsportedit` | film | 78 | 0 | 0.00% |
| 124 | `ronaldinhoedit` | football | 74 | 0 | 0.00% |
| 125 | `doflamingoedit` | anime | 73 | 0 | 0.00% |
| 126 | `hangeedit` | anime | 71 | 0 | 0.00% |
| 127 | `loganedit` | film | 67 | 0 | 0.00% |
| 128 | `musialaedit` | football | 60 | 0 | 0.00% |
| 129 | `tojiedit` | anime | 58 | 0 | 0.00% |

### 6b. Queue 3 — no record anywhere (346 tags, DELIBERATELY UNRANKED)

Any ordering here would be decoration pretending to be information, so they are seed-shuffled
rather than sorted — alphabetical order would correlate with nothing but would *look* like a
ranking.

**anime** (68)

`aceedit`, `akiedit`, `alphonseedit`, `astaedit`, `bakiedit`, `banedit`, `borosedit`, `buuedit`, `byakuyaedit`, `canuteedit`, `cascaedit`, `ccedit`, `celledit`, `chromeedit`, `doumaedit`, `edwardelricedit`, `erenedit`, `escanoredit`, `estarossaedit`, `flochedit`, `genosedit`, `gojoedit`, `gokuedit`, `gutsedit`, `hanmaedit`, `hashiramaedit`, `hieiedit`, `ippoedit`, `jeanedit`, `kallenedit`, `kenshinedit`, `kingbradleyedit`, `kobeniedit`, `kuramaedit`, `lawlietedit`, `lelouchedit`, `leviedit`, `lightedit`, `meliodasedit`, `melloedit`, `miyataedit`, `nachtedit`, `nearedit`, `noelleedit`, `painedit`, `pickleedit`, `porcoedit`, `poweredit`, `rezeedit`, `roymustangedit`, `saitoedit`, `sanosukeedit`, `sendoedit`, `senkuedit`, `shishioedit`, `suzakuedit`, `takamuraedit`, `tatsumakiedit`, `thorsedit`, `toguroedit`, `tsukasaedit`, `yamiedit`, `yujiroedit`, `yunoedit`, `yusukeedit`, `zekeedit`, `zeldrisedit`, `zoddedit`

**f1** (21)

`albonedit`, `alonsoedit`, `astonmartinf1edit`, `ferrarif1edit`, `gaslyedit`, `hamiltonedit`, `leclercedit`, `mclarenedit`, `mercedesamgf1edit`, `norrisedit`, `oconedit`, `perezedit`, `piastriedit`, `prostedit`, `raikkonenedit`, `redbullracingedit`, `rosbergedit`, `sainzedit`, `sennaedit`, `tsunodaedit`, `vetteledit`

**film** (47)

`antmanedit`, `arrivaledit`, `babydriveredit`, `batmanbeginsedit`, `bladeiiedit`, `casinoedit`, `crouchingtigeredit`, `departededit`, `driveedit`, `dunkirkedit`, `fearlessedit`, `furyroadedit`, `gameofdeathedit`, `guardiansofthegalaxyedit`, `heatedit`, `heroedit`, `infernalaffairsedit`, `interstellaredit`, `isawthedeviledit`, `jackreacheredit`, `johnwickedit`, `kungfuhustleedit`, `lalalandedit`, `madmaxedit`, `manofsteeledit`, `margincalledit`, `matrixedit`, `maverickedit`, `mementoedit`, `nightcrawlermovieedit`, `notimetodieedit`, `oppenheimeredit`, `parasiteedit`, `prestigeedit`, `ragingbulledit`, `snowpierceredit`, `spectreedit`, `taxidriveredit`, `thebigshortedit`, `theraidedit`, `thoredit`, `trainingdayedit`, `traintobusanedit`, `warriormovieedit`, `wayofthedragonedit`, `whiplashedit`, `zodiacedit`

**football** (28)

`atleticoedit`, `bergkampedit`, `buffonedit`, `cannavaroedit`, `casillasedit`, `delpieroedit`, `griezmannedit`, `ibrahimovicedit`, `iniestaedit`, `interedit`, `kakaedit`, `lamineyamaledit`, `maldiniedit`, `martinelliedit`, `napoliedit`, `nestaedit`, `pirloedit`, `psgedit`, `puyoledit`, `rodriedit`, `romaedit`, `ronaldonazarioedit`, `samueletooedit`, `sonheungminedit`, `tottiedit`, `vlahovicedit`, `wirtzedit`, `xaviedit`

**music_streamers** (31)

`21savageedit`, `adinrossedit`, `arianagrandeedit`, `badbunnyedit`, `biggieedit`, `billieeilishedit`, `brunomarsedit`, `drakeedit`, `dukedennisedit`, `eminemedit`, `ishowspeededit`, `juicewrldedit`, `kaicenatedit`, `kanyeedit`, `kendricklamaredit`, `ksiedit`, `lildurkedit`, `loganpauledit`, `metroboominedit`, `mrbeastedit`, `nipseyhussleedit`, `playboicartiedit`, `pokimaneedit`, `postmaloneedit`, `sidemenedit`, `taylorswiftedit`, `theweekndedit`, `travisscottedit`, `tupacedit`, `xqcedit`, `xxxtentacionedit`

**nba** (31)

`alleniversonedit`, `anthonydavisedit`, `anthonyedwardsedit`, `bucksedit`, `bullsedit`, `chrispauledit`, `damianlillardedit`, `devinbookeredit`, `dirknowitzkiedit`, `dwyanewadeedit`, `hakeemolajuwonedit`, `heatnbaedit`, `jameshardenedit`, `jamorantedit`, `jaylenbrownedit`, `kevingarnettedit`, `kyrieirvingedit`, `nuggetsedit`, `pennyhardawayedit`, `russellwestbrookedit`, `scottiepippenedit`, `sixersedit`, `stevenashedit`, `sunsedit`, `thunderedit`, `timduncanedit`, `tracymcgradyedit`, `traeyoungedit`, `vincecarteredit`, `warriorsedit`, `zionwilliamsonedit`

**tv** (101)

`aemondedit`, `alfiesolomonsedit`, `arcaneedit`, `arthurshelbyedit`, `aryastarkedit`, `avonbarksdaleedit`, `batiatusedit`, `berlinedit`, `bettercallsauledit`, `billionsedit`, `billybutcheredit`, `bjornedit`, `bobbyaxelrodedit`, `caitlynedit`, `cerseiedit`, `christophermoltisantiedit`, `ciriedit`, `crixusedit`, `cyberpunkedgerunnersedit`, `daemonedit`, `daenerysedit`, `danielsanedit`, `davidmartinezedit`, `dexteredit`, `dextermorganedit`, `eddiemunsonedit`, `elevenedit`, `ellieedit`, `elliotaldersonedit`, `flokiedit`, `frankunderwoodedit`, `gameofthronesedit`, `gannicusedit`, `geraltedit`, `gusfringedit`, `harveyspecteredit`, `homelanderedit`, `housedragonedit`, `houseofcardsedit`, `invincibleedit`, `ivaredit`, `jaimeedit`, `jessepinkmanedit`, `jinxedit`, `joelmilleredit`, `johnnylawrenceedit`, `jonsnowedit`, `kendallroyedit`, `kimwexleredit`, `kingpinedit`, `lagerthaedit`, `lalosalamancaedit`, `lincolnburrowsedit`, `littlefingeredit`, `loganroyedit`, `louislittedit`, `lucyedit`, `markgraysonedit`, `michaelscofieldedit`, `mikeehrmantrautedit`, `mikerossedit`, `mrrobotedit`, `nachovargaedit`, `nairobiedit`, `omarlittleedit`, `omnimanedit`, `ottoedit`, `pabloescobaredit`, `paulieedit`, `peakyblindersedit`, `prisonbreakedit`, `professoredit`, `ragnarlothbrokedit`, `ramsayedit`, `rhaenyraedit`, `romanroyedit`, `sansastarkedit`, `silcoedit`, `soldierboyedit`, `steveharringtonedit`, `stevemurphyedit`, `strangerthingsedit`, `stringerbelledit`, `successionhboedit`, `suitsedit`, `tbagedit`, `terrysilveredit`, `theboysedit`, `thelastofusedit`, `theonedit`, `thewitcheredit`, `tokyoedit`, `tommyshelbyedit`, `tonysopranoedit`, `trinitykilleredit`, `tyrionedit`, `varysedit`, `vecnaedit`, `viedit`, `vikingsedit`, `yenneferedit`

**wrestling** (19)

`beckylynchedit`, `brethartedit`, `cmpunkedit`, `codyrhodesedit`, `eddieguerreroedit`, `edgewweedit`, `johncenaedit`, `jonmoxleyedit`, `kennyomegaedit`, `kurtangleedit`, `randyortonedit`, `reymysterioedit`, `romanreignsedit`, `sethrollinsedit`, `shawnmichaelsedit`, `stonecoldedit`, `theundertakeredit`, `triplehedit`, `willospreayedit`

### 6c. Instagram — the list is useful, the walk is not this round's job

The same names work as Instagram tags and he asked for both. But the economics are honestly
different: **Instagram needs ~26x more calls per account**, because the bio does *not* ride
along with the hashtag page — one call returns ~28 accounts with no bios, then one call each.
TikTok returns ~25 accounts *and* their bios in a single call. The cheap Instagram figures on
record came from **one exceptional tag** at a 30.9% address rate on 91 rows and must not be
used as a baseline.

## 7. Part 5 — the walk

**88 net-new addresses** across 88 distinct accounts for **$1.22460**

⚠️ **THE CAP DID NOT BIND, AND I AM NOT GOING TO DRESS THIS UP AS IF IT DID.** The walk used
**24.5% of the $5.00**. It stopped because **I stopped it**: at ~6 minutes a tag, spending
the remaining **$3.78** needed roughly **3.7 more hours**, which is not a thing I could hold
a session open for. So this is not "what $5.00 buys" — it is what **$1.22** bought, and the
rate is reported so the rest can be priced honestly.

**At the measured rate the unspent $3.78 would buy roughly 271 more addresses**, for about
**359** in total — against the ~700–1,000 the brief projected off last round's numbers. The
gap is the rate collapse, not the budget.

|  |  |
|---|---|
| unit (`api.cost_per_call_usd`, by named key) | $0.00060000 |
| calls | **2041** |
| spend | **$1.22460** of a $5.00 cap |
| booked (checkpoint `calls_booked`) | 2041 |
| ledger rows `run_id=bl1564` | 2041 calls / $1.22460 |
| **three-way control** | **counter == checkpoint == ledger** |
| accounts kept | 12326 |
| kept accounts per call | 6.039 |
| net-new addresses | **88** |
| $ per 1,000 net-new | **$13.92** |
| interrupted processes | 1 |
| unbooked in-flight (bounded, NOT booked) | $0 – $0.1200 |
| worst-case true spend | $1.34460 |

| stop reason | tags |
|---|---|
| depth_wall | 9 |
| drained | 8 |

### 7a. Yield per tag, and how each one stopped

| # | tag | pages | kept | addr | NET-NEW | stopped |
|---|---|---|---|---|---|---|
| 1 | `nightwingedit` | 170 | 1080 | 10 | **9** | depth_wall |
| 2 | `clarkkentedit` | 171 | 908 | 6 | **2** | depth_wall |
| 3 | `bellinghamedit` | 171 | 845 | 9 | **8** | depth_wall |
| 4 | `moneyheistedit` | 169 | 477 | 0 | **0** | depth_wall |
| 5 | `makimaedit` | 169 | 1427 | 21 | **21** | depth_wall |
| 6 | `realmadridedit` | 169 | 952 | 10 | **9** | depth_wall |
| 7 | `itachiedit` | 169 | 1317 | 12 | **12** | depth_wall |
| 8 | `spartacusedit` | 12 | 47 | 1 | **1** | drained |
| 9 | `aliensedit` | 11 | 86 | 0 | **0** | drained |
| 10 | `tenetedit` | 76 | 581 | 2 | **1** | drained |
| 11 | `sanjiedit` | 171 | 954 | 6 | **5** | depth_wall |
| 12 | `sakaedit` | 88 | 572 | 2 | **2** | drained |
| 13 | `gohanedit` | 169 | 1148 | 6 | **6** | depth_wall |
| 14 | `osimhenedit` | 34 | 253 | 1 | **1** | drained |
| 15 | `verstappenedit` | 77 | 473 | 3 | **3** | drained |
| 16 | `goodfellasedit` | 94 | 615 | 6 | **5** | drained |
| 17 | `henryedit` | 104 | 591 | 3 | **3** | drained |

### 7b. Yield by tier — the ordering hypothesis, tested

| tier | tags | kept | NET-NEW | net-new rate | mean recorded | $/1k net-new |
|---|---|---|---|---|---|---|
| A — re-opened (cut short, partial record) | 4 | 3310 | **19** | 0.57% | 3.13% | $21.51 |
| B — recorded yield, **never walked on v2** | 13 | 9016 | **69** | 0.77% | 3.18% | $11.68 |

**The ordering was wrong, and it was mine.** Tier A went first *because* of its recorded rates; it delivered **0.57%** against a mean recorded **3.13%**. Tier B — a recorded yield on a surface that has **never been walked** — delivered **0.77%** at **$11.68 per 1,000** against Tier A's **$21.51**, a **1.8x** difference in price for the same money.

Both tiers came in *below* their recorded rates, which is the coin-flip effect on top of a store that keeps growing. But the ranking conclusion is unambiguous: **a tag with an untouched v2 surface is worth far more than a tag whose best pages were already taken.**

### 7c. Can the ledger predict a tag's v2 supply? No — and that turns out to be survivable

Ordering by recorded yield only helps if the record carries information. Tier B's records sit
in a **very** narrow band. Their outcomes do not.

| quantity (tier B, n=13) | range | spread |
|---|---|---|
| v1 recorded **authors** | 61 – 136 | **2.23x** |
| v1 recorded **yield** | 2.88% – 3.45% | **1.20x** |
| v2 accounts **kept** (the outcome) | 47 – 1427 | **30.36x** |

**A 2.23x spread in the input beside a 30.36x spread in the outcome means the record is not carrying the information the ordering assumes.** Within tier B the recorded rates span barely anything and the per-tag results run from 0 to 21 net-new. **You cannot rank these tags with what is on disk** — which also means the refuted tag-shape predictor was not hiding a better one.

**But the losers cost less, and that is why this is survivable:**

| | tags | cost | $/tag | net-new |
|---|---|---|---|---|
| reached the depth wall | 5 | $0.5112 | $0.1022 | **53** |
| drained early | 8 | $0.3024 | $0.0378 | 16 |

A tag that drains early costs **$0.0378** on average against **$0.1022** for one that runs to the wall — **2.7x cheaper**. The losers you cannot pick are the cheap ones, so the price of being unable to rank is small. **The lever is not ordering — it is that a dud stops itself.**

### 7d. The refusals, split — the number BL-1563 could only report merged

`guard.report()` is dumped after every tag now, so the refusal count decomposes:

|  |  |
|---|---|
| account sightings seen | 26850 |
| accounts **kept** | 12326 |
| refused — re-sighting **within this run** (page overlap) | 11570 (80%) |
| refused — **already held** (master + workbook) | 2954 (20%) |
| addresses seen / kept | 100 / 89 |
| addresses already held | 11 |

**Most of what the guard refuses is the feed re-serving the same accounts across its own
pages**, not duplicates against the store. Those are different problems with different fixes,
and one number hid both. (`addresses_kept` runs one ahead of net-new: the extra is the
**startup polarity probe**, which the guard correctly accepted and counted. Noted so it is
not mistaken later for an off-by-one.)

### 7e. A re-opened tag does NOT recover its recorded rate — and I ranked on the assumption it would

| tag | recorded rate (on its cut-short walk) | rate on the re-walk |
|---|---|---|
| `nightwingedit` | 4.19% (14 addr / 334 accounts) | **0.83%** (9 net-new / 1080 kept) |
| `clarkkentedit` | 3.81% (21 addr / 551 accounts) | **0.22%** (2 net-new / 908 kept) |
| `bellinghamedit` | 2.75% (16 addr / 581 accounts) | **0.95%** (8 net-new / 845 kept) |
| `moneyheistedit` | 1.79% (7 addr / 391 accounts) | **0.00%** (0 net-new / 477 kept) |

All 4 fell by a large multiple, and not by luck. **The recorded rate was measured on the pages
that WERE walked; the re-walk gets the rest.** `nightwingedit` was cut at page 42 — those
accounts were harvested then and are in master now, so the guard refuses them and the
surviving addresses come only from pages 43–170, the part of the feed nobody had seen and
about which the first pass's rate says nothing.

So the recorded yield of a cut tag is **the rate of the part you already own**, and using it
to rank the part you do not own is a category error. It is mine: I put the re-opened tier
first *because* of those rates.

**This does not make re-opening wrong.** Those tags returned addresses that were unreachable
before the fix — `nightwingedit` had been skipped by every resume since it was cut. What was
wrong was the expected rate, not the decision to walk. **The correction:** rank a re-opened
tag by the supply it still *owes* — pages remaining against the ~170-page wall, and accounts
not yet held — never by the rate of the fraction already taken. A tag cut at page 42 owes
~128 pages; one cut at page 143 owes ~27. The recorded rate does not distinguish them.

### 7f. The editor rate, with the bio kept

| gate | k/n | rate |
|---|---|---|
| **FULL gate** (`name_rule` OR `bio_rule`) | 11/88 | **12.50% [7.13–21.01]** |
| `name_rule` alone | 4/88 | 4.55% |
| `bio_rule` alone | 11/88 | 12.50% |

BL-1563 reported **8.26% [6.64–10.23]** — `name_rule` **alone**, because it stored `bio_len` and threw the bio away. The gap between the first two rows *is* that instrument fault, measured.

⚠️ **The four priors remain unreconciled** — 6.59% [3.06–13.65] n=91, 13.33% [5.31–29.68] n=30, 22.54% [14.37–33.52] n=71, 29.37% [27.57–31.23] n=2387. With the bio kept this is the first honest large sample, and it is **reported, not claimed as a settlement**: nobody has shown those four populations are the same question. The gate's own accuracy is precision 87.65% [78.74–93.15], recall 94.67% [87.07–97.91] on n=240 — not 97.56%, which was one sample of 120 while a disjoint 120 of the same gate scored 79.41%. It is **not** validated against `lead_kind` or `verdict`: `writer.py` returns CLIPPER for any `tt:`/`ig:` source regardless of the bio and says so in its own docstring.

### 7g. Deliverability

| verdict | addresses |
|---|---|
| pass | 86 |
| reject | 2 |

Role inboxes and short local parts are **flagged and kept**, not dropped. MX was resolved
against **this run's domains**, never the default table. And an `@handle` in a bio is not an
email: the de-obfuscator fuses a lead-in word onto a handle, 66 of 1,870 addresses were once
removed for exactly that, and a first-draft rule caught 20 rows of which **11 were genuine
Gmail addresses**.

## 8. The output

* **The workbook**: `Random/clipper_emails_ALL.xlsx` on his Desktop — Emails 2237 → 2894
  rows, 659 addresses added, other sheets unchanged, read back and counted per sheet.
  **Not committed.**
* **10 tags un-retired**, including `nightwingedit`, and the class fixed in both the ledger and
  the checkpoint.
* **49 tags recorded as `depth_wall`** rather than drained.
* **543 fresh tag candidates**, existence-checked, published in full above.
* The row file carrying real addresses is **gitignored and stays so**.

## 9. WHAT I GOT WRONG

**I nearly published a cross-platform dedup bug.** My first workbook merge keyed accounts on
the bare handle extracted from the profile link — which put TikTok and Instagram handles in
*one namespace*. The workbook holds 287 Instagram handles and 12 names that exist on **both**
platforms, so a TikTok account could have been silently dropped because an unrelated Instagram
account shared its name. I caught it only because 246 skips looked too high to believe, and
measured it: **0 of the 246 were cross-platform collisions**, so the merge was correct by luck
of the data, not by design. The key should be (platform, handle) and this round's number
happens not to depend on it.

**My first leak scan reported 0 refusals from the forbidden-tag list and I almost shipped
that.** Zero refusals is exactly the shape of a broken filter. Adding a positive control took
four lines and turned "0 refusals" from an unverified claim into a measured one.

**I used `git grep` through a subprocess without an encoding and it raised
`UnicodeDecodeError` mid-audit** — which, had I caught the exception instead of crashing,
would have read as *no matches*: a false zero in the exact instrument I was using to count
fix sites.

**And a process query matched the wrong process.** Looking for the walker by command line
returned the launcher stub, whose CPU sits flat at 0.0156s forever — which reads exactly like
a hung worker. The authoritative PID is the one in the walker's own lock file; the same class
of mistake (`kill -0` in Git Bash reporting a *running* native Windows process as EXITED)
cost the previous round two walkers on one budget for ~50 minutes.

## 10. What did not run, reported as ABSENT

* **The Instagram walk did not run** and was never planned to. The tag list is delivered; the walk is a different round's money.
* **No outreach was sent.** This project does not send.
* **The paid profile route stayed off** — 52 paid profile calls once returned zero addresses.


**BL-1562's claim is stale-OPEN** with its report already published to this repo and no
`docs/claims/BL-1562.claims` manifest. It is another round's claim: **noted, not touched.**

**Duplicate count 1 was conflated in BL-1563** and is split here only from the point
`guard.report()` began writing — the counters live in the process and every earlier round's
died with it.

**The unbookable money is bounded, not booked.** A tag in flight when a process dies is paid
for and invisible: checkpoint and ledger both write *after* a tag completes. It is reported as
a range; an estimate must never sit in the money ledger beside counted calls.
