# Lead-gen report index (clipper-finder Python CLI)

Generated index for the **lead-gen** subset of `clippershq-reports`. The other 165 reports in this directory describe the **ClippersHQ payments app** and are a different codebase — see `MANIFEST.tsv` for the full classification.

**Nothing here has been renamed or moved.** Every existing link still resolves.


## Read these first — the current answers

| question | answer | report |
|---|---|---|
| ready-to-send total | **1,600 deliverable** (1,620 exported − 20 no-MX). Supersedes 4,217 / 3,659 / 1,576. | [BL-764](reports/BL-764.md) |
| Spotify seed pool | **~777** (95% CI 659–857) at full playlist depth, not ~452. | [BL-769](reports/BL-769.md) |
| the live send file | `LATEST_BOT_READY.csv` holds **2 rows** and is stale. Do not treat it as the send list. | [BL-765](reports/BL-765.md) |

## Superseded — do not quote these numbers

| report | superseded by | why |
|---|---|---|
| [BL-743](reports/BL-743.md) | **[BL-764](reports/BL-764.md)** | 3,659 is a quality view of the data, not the send path. BL-764 reproduces it at 3,660 (±1) and supersedes the framing. |
| [BL-751](reports/BL-751.md) | **[BL-764](reports/BL-764.md)** | 1,576 was measured before BL-760/BL-761 appended rows; BL-764 recomputes the same predicate at 1,620, then 1,600 deliverable. |
| [BL-757](reports/BL-757.md) | **[BL-764](reports/BL-764.md)** | 4,217 counts addresses that EXIST, not addresses you can send to; 62% never reaches the send file. BL-764: "the number to stop quoting". |
| [BL-766](reports/BL-766.md) | **[BL-769](reports/BL-769.md)** | seed pool ~452 was measured at the wrong depth — get_playlist max_tracks defaults to 100. BL-769: full playlists give ~777. |
| [BL-774](reports/BL-774.md) | **[BL-764](reports/BL-764.md)** | quotes the stale 1,576 as the ready-to-send total. The segmentation and offer findings stand; the NUMBER does not. |

> **[BL-765](reports/BL-765.md)** — Establishes that output/LATEST_BOT_READY.csv holds 2 rows and is STALE. Any report or automation treating it as the live send list is wrong — this is the correction, not the error.


## All lead-gen reports, newest first

| id | date | status | title |
|---|---|---|---|
| [BL-778](reports/BL-778.md) | 2026-07-31 | current | The dead-knob population at source — 83 invisible knobs, 11 unread keys (one BL-775 missed), 32 orphan functions, and a  |
| [BL-777](reports/BL-777.md) | 2026-07-31 | current | YouTube has NEVER been run. Not once. It works when you run it — 12% pass, all six fixes firing — and then **every lead  |
| [BL-776](reports/BL-776.md) | 2026-07-31 | current | Baselines captured for all four unbaselined funnels. And the optional-field hazard turns out not to exist outside the ra |
| [BL-775](reports/BL-775.md) | 2026-07-31 | current | What this project knows about itself: none of the four "contradictions" is one, evidence survives at 100%, and the real  |
| [BL-774](reports/BL-774.md) | 2026-07-31 | **SUPERSEDED by BL-764** | The list you can actually send to is one segment, not three — 1,568 fandom video editors, and it is a RECRUITING list, n |
| [BL-773](reports/BL-773.md) | 2026-07-31 | current | The $3.53 is real and irrelevant: time costs 100× the cash. Total addressable pool is ~2,000 fresh email leads, and the  |
| [BL-772](reports/BL-772.md) | 2026-07-31 | current | Platform-change exposure: the loud-zero guard exists in exactly one funnel, five funnels have no saved baseline at all,  |
| [BL-771](reports/BL-771.md) | 2026-07-31 | current | Duplicate humans: master is clean (5, all Google Play). But the send path **would double-send 1,395 people** — because d |
| [BL-770](reports/BL-770.md) | 2026-07-31 | current | Junk sweep: 1 live junk address, not a guard failure. letsencrypt is in a 14-day-stale FILE that today's code already re |
| [BL-769](reports/BL-769.md) | 2026-07-31 | current | Seeds re-measured: six of seven unchanged, the trial playlist is now the best of the set AND the largest contributor. Bu |
| [BL-768](reports/BL-768.md) | 2026-07-31 | current | Spec: suppression + bulk outcome marker. The briefed marker plan is O(n) per key and costs 73s; an index costs 0.04s. Bo |
| [BL-767](reports/BL-767.md) | 2026-07-31 | current | SPEC: the two gates protect nothing on client funnels, there is a third gate nobody has counted, and the fix is one decl |
| [BL-766](reports/BL-766.md) | 2026-07-31 | **SUPERSEDED by BL-769** | Cause found: the run asked for 1,000 leads from a seed pool that holds ~452. The overflow came from related-artist expan |
| [BL-765](reports/BL-765.md) | 2026-07-31 | correction | Send-path audit: **NO, not safe to send from today.** The file n8n watches holds 2 rows, nothing is suppressed, and 2,50 |
| [BL-764](reports/BL-764.md) | 2026-07-31 | current | The number is 1,600 — and 1,592 of them come from one source. Six of your eight funnels export nothing because of a sing |
| [BL-763](reports/BL-763.md) | 2026-07-31 | current | Audio genre labelling: CLOSE IT. Non-reproducibility is upstream of accuracy, and no threshold or vote is worth buying. |
| [BL-762](reports/BL-762.md) | 2026-07-31 | current | The YouTube size gate now measures reach, not just followers: N = 2,000,000 views, measured on 200 channels across 4 nic |
| [BL-761](reports/BL-761.md) | 2026-07-31 | current | The 52% discard is closed, the counters are honest, and 'personal' now means it. The X-scraper idea is dead — measured 0 |
| [BL-760](reports/BL-760.md) | 2026-07-31 | current | Engagement fields LANDED. And the caveat was right: save_count is 0% on four new accounts — it is account-specific, not  |
| [BL-759](reports/BL-759.md) | 2026-07-31 | current | A fresh clone imports cleanly but fails 6 of 48 suites — and there is exactly one copy of everything that matters, on on |
| [BL-758](reports/BL-758.md) | 2026-07-31 | current | Build HELD: every module sections 3/4/6 must edit is mid-edit by another agent. The regression is NOT depth — it is free |
| [BL-757](reports/BL-757.md) | 2026-07-31 | **SUPERSEDED by BL-764** | Send order — your sendable pool is 4,217 addresses, not 57,000, and 7.6% of it is structural bounce risk |
| [BL-756](reports/BL-756.md) | 2026-07-31 | current | Capture NOT applied: 108 files written in 3 minutes by ~4 concurrent rounds. But the six fields are re-measured on 3× th |
| [BL-755](reports/BL-755.md) | 2026-07-31 | current | View floor N measured at n=200 across 4 niches; the description fill drops 12.5% → 7.1% once the country gate is honoure |
| [BL-754](reports/BL-754.md) | 2026-07-31 | current | Spec: a self-audit that prints after every run. Building it surfaced two unflagged regressions and one dead recommendati |
| [BL-753](reports/BL-753.md) | 2026-07-31 | current | Clipper-side audit — the persona hunch is wrong (0.2–0.3%, not "the bulk"), the email-drop bug is absent, and the IG cra |
| [BL-752](reports/BL-752.md) | 2026-07-31 | current | The audio benchmark completed: the model is not reproducible at temperature 0, and the requested headline number does no |
| [BL-751](reports/BL-751.md) | 2026-07-31 | **SUPERSEDED by BL-764** | 1,576 leads are ready to send — and 100% of them come from two funnels. The other six export literally nothing, for one  |
| [BL-750](reports/BL-750.md) | 2026-07-31 | current | Fix NOT applied: three agents are writing every ~30s and one took a `pre_bl749` backup of config.json. Item 1's fill rat |
| [BL-749](reports/BL-749.md) | 2026-07-31 | current | Cross-funnel unread-field sweep: the clip walk gets a full engagement panel free and reads none of it |
| [BL-748](reports/BL-748.md) | 2026-07-31 | current | YouTube funnel audit: the stack is the CORRECT (Spotify) shape, but three fields arriving free at 100% are discarded, an |
| [BL-747](reports/BL-747.md) | 2026-07-31 | current | The Spotify no-contact pool is 18.9% and genuinely dead. The real leak is next door: 52% of delivered leads never reach  |
| [BL-746](reports/BL-746.md) | 2026-07-31 | current | The counter isn't broken — it's counting a different population. The leads are real and genuinely new; the run's problem |
| [BL-745](reports/BL-745.md) | 2026-07-31 | current | Spec: what a downstream editing bot needs to recreate a clip. 29 of 39 fields already ship; the one that matters most is |
| [BL-744](reports/BL-744.md) | 2026-07-31 | current | Spotify funnel audit: the filter order is already correct, the seeds have drifted, and 41.5% of delivered leads have no  |
| [BL-743](reports/BL-743.md) | 2026-07-31 | **SUPERSEDED by BL-764** | READY TO SEND TODAY: 3,659. Cross-funnel lead-quality audit of 57,386 rows. |
| [BL-742](reports/BL-742.md) | 2026-07-30 | current | FALSE-NEGATIVE RATE 63.3%. The music detector discards 31 of 49 music clips. Do not ship this gate. |
| [BL-741](reports/BL-741.md) | 2026-07-30 | current | Fetch-chain fix APPLIED. Both chain_proof verdicts BOUNDED against the real module, 50/50 suites green. Paid re-measurem |
| [BL-740](reports/BL-740.md) | 2026-07-30 | current | Fix written and VERIFIED against both adversarial servers, but not applied: the funnel process from BL-738 is now 180 mi |
| [BL-739](reports/BL-739.md) | 2026-07-30 | current | Run not started: the funnel process from BL-738 is still alive at 164 minutes. Items 2 and 5 answered read-only; item 2' |
| [BL-738](reports/BL-738.md) | 2026-07-30 | current | Not fixed, and not fixable this round: a funnel process has been livelocked at 99.5% of a core for 85 minutes with ZERO  |
| [BL-737](reports/BL-737.md) | 2026-07-30 | current | Item 4 was not produced: OpenRouter blocks every audio request below a flat $0.50 balance and the account holds $0. The  |
| [BL-736](reports/BL-736.md) | 2026-07-30 | current | The downscale fix works exactly as measured — and changes nothing this module actually outputs |
| [BL-735](reports/BL-735.md) | 2026-07-30 | current | The benchmark did not run: there is no `openrouter_api` block in config.json. The guard for it is now in place, so the k |
| [BL-734](reports/BL-734.md) | 2026-07-30 | current | You don't need to replace Gemini — you need a different payer. OpenRouter routes the same model for half the price, with |
| [BL-733](reports/BL-733.md) | 2026-07-30 | current | OCR transcription accuracy, measured for the first time: production is throwing away half its accuracy on a `max_side=51 |
| [BL-732](reports/BL-732.md) | 2026-07-30 | current | schema fix shipped, pilot measured — the bank supports ~200 pages, but the cost is 3.7 hours, not dollars |
| [BL-731](reports/BL-731.md) | 2026-07-30 | current | Source-footage ID from a frame: the model never declines, is wrong 20% of the time, and the free route is licence-blocke |
| [BL-730](reports/BL-730.md) | 2026-07-30 | current | No live run (gate failed), but the timeout spike is explained from BL-728's own saved data: fetches run to 218s despite  |
| [BL-729](reports/BL-729.md) | 2026-07-30 | current | Comments are a noise pit for song ID (5%) and a duplicate for source ID (20%) — close the channel, but keep three free f |
| [BL-728](reports/BL-728.md) | 2026-07-30 | current | Retaining the dropped rows found the filter was wrong: `nsfw` produced 4 false positives out of 6 keyword drops, all of  |
| [BL-727](reports/BL-727.md) | 2026-07-30 | current | The clip library is wired and ran live: 20 real clips off the wire for $0.0048, the view floor stopped 3 of 4 accounts,  |
| [BL-726](reports/BL-726.md) | 2026-07-29 | current | Twitch on Helix: discovery is free and instant, the free website scrape is 82% of the clock, and the in-band pool is 260 |
| [BL-725](reports/BL-725.md) | 2026-07-29 | current | Gemini audio benchmark — blocked at 18 of 60 calls by a 20/day free-tier cap, but the one stratum that completed is not  |
| [BL-724](reports/BL-724.md) | 2026-07-29 | current | Measured per-field error on 60 hand-labelled clips: tag-derived franchise is wrong 28.6% of the time. There is no purity |
| [BL-723](reports/BL-723.md) | 2026-07-29 | current | SECRET_BLOCKS now redacts credentials out of every log record and refuses to start if a menu names one. Plus 3 more decl |
| [BL-722](reports/BL-722.md) | 2026-07-29 | current | STOPPED: tree is not quiet. No process is running, but another agent is writing control.py and main.py right now. |
| [BL-721](reports/BL-721.md) | 2026-07-29 | current | the pilot is now answerable — 73 targets, and the window question resolves in the pilot's favour |
| [BL-720](reports/BL-720.md) | 2026-07-29 | current | One of the two small audio models is viable: LFM2-Audio-1.5B GGUF runs here, guard-clean, at ~1.5 GB. Mellow is licence- |
| [BL-719](reports/BL-719.md) | 2026-07-29 | current | Caption-text labelling does not save the high-usage band — 14.8% → 14.8%. The popular sounds are not franchise content a |
| [BL-718](reports/BL-718.md) | 2026-07-29 | current | the fingerprinting pilot is underpowered before it starts — the target slice is 8.7%, not 24% |
| [BL-717](reports/BL-717.md) | 2026-07-29 | current | NOT BENCHMARKED: this CPU cannot run a 7B audio-LM (measured), and there is no Gemini key. Two blockers, both structural |
| [BL-716](reports/BL-716.md) | 2026-07-29 | current | what a sound is FOR, inferred from what it's used on: the idea works, the labeller is the ceiling |
| [BL-715](reports/BL-715.md) | 2026-07-29 | current | Both Spotify serial bottlenecks fixed: 24% of all HTTP requests deleted, the MusicBrainz lookup can no longer outlive it |
| [BL-714](reports/BL-714.md) | 2026-07-29 | current | the block-terminator fix — cluster-A caption coverage 5.2% → 66.5%, and BL-694's baseline did not move |
| [BL-713](reports/BL-713.md) | 2026-07-29 | current | 483 paid-for Spotify handles salvaged from run.log and merged — all genuinely new, and the artist-ID hint is provably wr |
| [BL-712](reports/BL-712.md) | 2026-07-29 | current | STOPPED: tree is not quiet, another agent is editing enrich_links.py. Fix #3 measured read-only: 71.8% of scraper fetche |
| [BL-711](reports/BL-711.md) | 2026-07-29 | current | song identification: line CLOSED by owner decision, with the decisive question still unmeasured |
| [BL-710](reports/BL-710.md) | 2026-07-29 | current | Clip library and catalogue walk: the storage and filtering halves, built and proven offline |
| [BL-709](reports/BL-709.md) | 2026-07-29 | current | Discogs genre is CC0 after all (BL-704 was wrong), Wikipedia infobox buys nothing, and the free comma-split is worth 3×  |
| [BL-708](reports/BL-708.md) | 2026-07-29 | current | What sounds go on each franchise: the curated map fails, and the 51% concentration that motivated it was an artifact |
| [BL-707](reports/BL-707.md) | 2026-07-29 | current | Medium and genre split into two axes: 4 false conflicts → 0, coverage unchanged at 91.5% |
| [BL-706](reports/BL-706.md) | 2026-07-29 | current | The curated head-artist genre map — 49% from three credits an encyclopaedia will never carry, 61.2% with the recurring t |
| [BL-705](reports/BL-705.md) | 2026-07-29 | current | Format is a property of the CLIP, not of the ACCOUNT. One post does not label a page. |
| [BL-704](reports/BL-704.md) | 2026-07-29 | current | Genre from title+artist — the provably-clean source covers 30% of licensed clips, the source that covers 90% isn't prova |
| [BL-703](reports/BL-703.md) | 2026-07-29 | current | Content genre from the discovery hashtag: 91.5% coverage, free, on 351 real reels |
| [BL-702](reports/BL-702.md) | 2026-07-29 | current | Music presence is a PAGE-FORMAT property: 68% / 67% / 30% / 11%. Song ID is reopened. |
| [BL-701](reports/BL-701.md) | 2026-07-29 | current | The Spotify funnel's stalls are NOT O(n²). 67% of a real run is spent blocked on one global MusicBrainz lock, and the 30 |
| [BL-700](reports/BL-700.md) | 2026-07-29 | current | Only 8.5% of clips are music-dominant. Fingerprinting has no target here. Do not build it. |
| [BL-699](reports/BL-699.md) | 2026-07-29 | current | Can we identify WHICH SONG is in a reel? Yes, for about 7× what finding the lead costs — and the one free option cannot  |
| [BL-698](reports/BL-698.md) | 2026-07-29 | current | Identifying the film or show from a clip: two of the three routes are structurally dead, the third is unmeasured, and th |
| [BL-697](reports/BL-697.md) | 2026-07-29 | current | every caller of the /v2/user/clips envelope, and the two breakages waiting on the NEXT migration |
| [BL-695](reports/BL-695.md) | 2026-07-29 | current | the caption parser is wired into the repost finder: mood, genre, title and a farm detector on every discovered account,  |
| [BL-694](reports/BL-694.md) | 2026-07-29 | current | the caption parser: built, measured on 42 hand-labelled captions, three fields with provenance |
| [BL-693](reports/BL-693.md) | 2026-07-29 | current | The numpy 2.0 ABI break is now a machine check, not a memo |
| [BL-692](reports/BL-692.md) | 2026-07-29 | current | How common is caption templating? 37.5% of confirmed repost pages, ~14% of the raw discovery pool — and a parser built f |
| [BL-691](reports/BL-691.md) | 2026-07-29 | current | the Spotify bridge is paid, the router mix is unstable, and the track-id routing is now a chokepoint |
| [BL-690](reports/BL-690.md) | 2026-07-29 | current | Energy-step detector on REAL audio: fabrication went 0% → 100% |
| [BL-689](reports/BL-689.md) | 2026-07-29 | current | CLAP for the coarse 4-way mood split: the model is cleared, the labels are the blocker |
| [BL-688](reports/BL-688.md) | 2026-07-29 | cross-project | the report-ID race: three reports were destroyed, not one, and only one was noticed |
| [BL-686](reports/BL-686.md) | 2026-07-29 | current | Instagram reels move to /v2/user/clips, and a test that was set to fail on a date nobody chose |
| [BL-683](reports/BL-683.md) | 2026-07-17 | current | `energy_step_ts`: built, measured, and honest about which number it is |
| [BL-682](reports/BL-682.md) | 2026-07-29 | current | Mood from text, not audio: the owner is right, and the reason is stronger than the premise |
| [BL-678](reports/BL-678.md) | 2026-07-29 | current | `/v2/track/by/id` — the count passes through intact, but `best_audio_cluster_id` is the wrong key for licensed music |
| [BL-676](reports/BL-676.md) | 2026-07-29 | current | the view-count decoy: which field actually carries reach, per platform |

---

_94 lead-gen + 1 cross-project reports indexed; 165 payments and 1 ambiguous excluded. Regenerate with the script in the publishing report._