# BL-1598: 1,000 new Spotify client emails for $1.25 in 4.6 hours, and where they are

| new emails | $ spent | hours | $ per 1,000 | hours per 1,000 |
|---:|---:|---:|---:|---:|
| **1,000** | **$1.2515** | **4.56** | **$1.25** | **4.56** |

- **The spend:** $1.250768 for the run (1,811 Instagram lookups) plus $0.000691 for the vendor check. The hard cap was $2.00 and expectation about $1.16.
- **The hours:** launch 19:53:49 to exit 00:27:37. That includes 33 minutes of discovery; artist processing took 4.0 h.

**Emails by source:**
- Instagram: **967**
- link-in-bio: **33**
- website: **0**

**Was the speed fix used? YES.** It is commit `58f809b5`, written test-first and finished in about 35 minutes.
- It skipped **685 of 3,101** country lookups (22.1%).
- Country lookups taking more than 5 s fell to **2** in the whole run, against **9,698** in the last run.

**Errors:** 0 Instagram server errors, 1 per-artist timeout, 3 record errors.

**Did any cap fire?** Yes: the **1,000-new-email stop**. The run's own end marker reads `stop_reason = email_target`, and it is not a halt. The $2.00 cap, the 6-hour limit and the outage stop never fired.

**The delivered files:**
- `<PROFILE>\AppData\Local\ClippersHQ\operator\spotify_clients_20261002.xlsx`
- a `.csv` beside it with the same 1,000 rows
- Start Menu: **ClippersHQ > Spotify clients** opens the newest one.

**Close-out:**
- **Master** grew by **exactly this run's 1,777 rows**: 75,540 to 77,317, every row tagged `run_id = bl1598`. All were appended through the locked path (`crossdedup.append_leads`, 34 merged into people already held).
  - Distinct emails in master went from 15,260 to 16,260: **+1,000, the delivered count.**
- **spend.json:** my rows are exactly **$1.251459** (`SPOTIFY_FINDER` $1.250768 + `BL-1598_VENDOR_CHECK` $0.000691). Other rounds booked $4.2444 in the same window (BL-1599 $2.9934, BL-1600 $1.2336, EDITS $0.0174), and those are not mine. The total ledger movement, $5.495859, is the sum of the two.
- **MARK** (96 files) and **his clipper workbook: byte-identical** start to end. Nothing on the Desktop.
- **config.json:** backed up, changed for the run only, then restored byte-for-byte. The changes are listed below.

## The one thing to act on

**Rotate the LamaTok API key.** While checking `config.json`'s format, I printed its first 120 bytes. My mask failed because the cut fell inside the key's value, so 25 characters of that value reached my terminal and this session's transcript. It is in no file.

## Config changes (all restored after the run)

Backup: `config.backups\config.json.20261002_195305.bl1598_pre_run.bak`. The restore was refused-if-changed and matched the backup's hash.

| key | before | for the run |
|---|---|---|
| `spotify_finder.seeds` | 24 | 15 (the 9 measured-dead seeds off) |
| `spotify_skip_ids_file` | absent | 52,376 artist ids already looked at |
| `spotify_harvest_query_list` | absent | 102 never-used queries: size 26, genre 3, region 62, decade 11 |
| `spotify_contact_before_country` | absent | true |
| `spotify_stop_after_new_emails` | absent | 1000 |
| `spotify_max_run_minutes` | absent | 320 |
| `spotify_stop_file` | absent | `scratch\bl1598\STOP` (the watcher's clean stop) |

- **Run cap:** `--cap 1.73`, given on the command line, so it was never written to config. The run's cap check counts lookups at $0.0006 while the ledger now books $0.00069064, so $1.73 there means $1.99 real.
- **Unchanged:** the country filter, the 100k–5.1M listener bounds and related-artist hops.

## What happened

1. **Preflight:**
   - No other Spotify or walker process was running, and C: had 201 GB free.
   - **Vendor check:** 1 paid lookup on a public brand account returned a full profile in 1.6 s ($0.00069). I stopped there; the brief allowed 3.
2. **Speed fix:** 12 tests written first (11 failed, then 12 passed). The 8 related Spotify suites and the contract and wiring suites are green.
   - `test_silent_zero_shape` is red at the same 7 sites BL-1596 recorded, none of them in these files.
   - **A no-link artist still "passes",** so related-artist hops fire as before. An artist with a new link takes exactly the old path.
   - **The commit also adds a clean stop hook and an ordered query list, all default OFF.** Your stop rules needed them: the run's own target counts DM-only leads, and before this a run had no time limit and no clean manual stop.
3. **Run:**
   - Discovery took 33 min: 1,796 artists from the seeds, 18,738 from 400 playlists (28 size-first queries), and 418 from ListenBrainz.
   - It then processed 14,964 artists, with 17,510 more skipped free by the skip list.
   - Status every 15 minutes is in `scratch\bl1598\watch.log`.

## What was wrong or worse than planned

- **BL-1597's speed forecast was too optimistic: it said 2.1 h per 1,000, and this run took 4.56.**
  - The fix skipped 22% of country lookups, not 57%. The skip list had already removed most already-held artists before they were read.
  - The time then moved to Spotify reads, and fresh artists yielded less: 6.7% emails per artist read, against 9.2% last run.
- **BL-1597's dollar figures were about 15% low.** August's ledger rows booked Instagram lookups at $0.0006, and the measured price is $0.00069064; today's rows book the right price. Its "$1.16 per 1,000" is about $1.34 at the real price. This run's $1.25 is at the real price.
- **The run's summary line "Cost $5.495" is wrong for this run.** It differences the whole ledger, which other rounds were writing at the same time. Use the campaign rows above.
- **The second vault root is missing.** `D:\clippershq_vault_bl1574` doesn't exist: D: is now an internal 894 GB disk, not the USB stick. Both files are vaulted, and re-hashed, in the local root only. **Your call:** plug the stick back in, or name a new second root.
- **My own mistakes:**
  - **The watcher's launch failed on the space in the folder name.** The run was unguarded for its first 31 minutes, all of them in discovery with $0 spent.
  - **Its outage counter expected timestamps, and headless warnings have none.** Both were fixed before the first paid lookup.
  - **`run_all.py --help` started the full suite.** I stopped it after one suite; it runs sandboxed, and nothing moved.
  - **One stderr read printed an artist's website domain.** It is in no file.

## Proposals (none applied)

1. **Keep `spotify_contact_before_country` and the skip list ON for future runs.** Neither lost an email: the skip list costs about 1.9%, and contact-first is lossless.
2. **Fix the cap check's price.** Passing `ig_api.cost_per_call_usd` into the funnel's cap would make "$X" mean $X. It is a spend-gate change, so it is your call.
3. **Next 1,000:** 74 of the 102 queued queries are still unused (region and decade), plus the playlists that were found but not walked.

## Paths

- Code: `clippershq/spotify_finder.py`, `clippershq/control.py`
- Test: `tests/test_bl1598_spotify_contact_first.py` (commit `58f809b5`)
- Proof files: `scratch/bl1598/` (`snap_*.json`, `state_*.json`, `vendor_check.json`, `watch.log`, `deliver.json`, `suites.out`)
- Checkpoint: `scratch/resume/spotify.bl1598.jsonl.20261003-002625.done`
