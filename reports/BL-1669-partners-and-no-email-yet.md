# BL-1669 -- "No email yet" editors list (10,099) + the overnight free read of 9,905 collab partners

Orders: office 1_LEADS 2026-10-17_2021 (Dusan yes: read the never-scanned collab partners tonight, no spending) and
2021 (keep EVERY editor found, also without an email, in a separate "no email yet" list; never used or contacted).
**Spent: $0.** Counts only -- no handle, name or email here.

## The "no email yet" list
- New module `clippershq/no_email_yet.py`: one store (`%LOCALAPPDATA%\ClippersHQ\no_email_yet\editors.json`, keyed
  platform + handle) and his sheet `operator\no_email_yet\Editors_no_email_yet.xlsx`.
- Columns: platform, handle, profile link, niche, **basis** (how we know it is an editor), source, followers,
  nickname, bio, bio link, region, status, approved videos, first seen. Blank = not seen, never a guess.
- A row whose bio shows an email is refused (that editor belongs in the lead files). The same account seen again
  merges: later values only fill blanks; basis and source keep every distinct value.
- **Seeded now: 10,099** -- 4,870 proven editors (an approved video in his library) + 5,229 the AI judged as real
  edits, all with no email in the bio; 670 refused because they do show one; accounts he marked NO and official club
  accounts left out. Biggest niches: superhero 2,864, football 2,811, tennis 1,601, ufc 985, marvel 755,
  basketball 672, golf 372.
- **Why a subfolder:** `raw_emails.known_from_xlsx` reads every top-level sheet in `operator\` and treats each
  TikTok link in it as a known account, so the walk skips it. In the top folder this list would block these editors
  forever -- even on the day they add an email. `operator_files()` does not recurse; a test pins that.
- Tests: `tests/test_no_email_yet.py` 6/6 (refusal, merge, platform scope, edit-app seed incl. the live unix-time
  first_seen shape, reader rows, sheet outside the duplicate check).

## The overnight collab-partner read
- `scratch/bl1669/partners69.py`: the BL-1667 partner pool (accounts proven editors @tag in captions with no stored
  bio, 9,905), 2 detached lanes, each its own headless Chrome with a throwaway profile, closed by its own handle.
- Resumable (every account appended at once; a restart skips what is done), STOP file, CAPTCHA x3 -> 15 min pause,
  3 pauses in a row end the lane.
- Pace: ~7-9 s per account per lane while the PC was busy (4.6 s on a quiet PC) -> ~6.5-11 h for all.
- Every edit-like page it reads with no email goes into the list (`no_email_yet.py add-jsonl`).
- BL-1667 measured on 133 of them: 3 new emails, 22 edit-like pages. Results of the full read follow in the reply.

## Tests
- `tests/test_no_email_yet.py` 6/6 OK.
- Full suite (`tests/run_all.py`, run during the overnight read, PC loaded): 2 reds in the first 85 suites, neither
  from this round -- `test_atomic_io` (unguarded os.replace/os.remove in edits_clean.py, edits_gdrive.py,
  farm_sheets.py, raw_pages.py, tools/office/launcher.py; this round adds none and touches none of them) and
  `test_bl1300_judge_first` (judge_page order in main.py, changed by another round at 15:24). Left to their owners.
