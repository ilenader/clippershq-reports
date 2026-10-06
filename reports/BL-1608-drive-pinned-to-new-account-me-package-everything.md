# BL-1608 (finishes BL-1607): your new Google Drive account is pinned, and the "me" package carries everything

## CARD

1. **Drive account pinned: YES.** ClippersHQ now uses only your new account's Google Drive. It recognises the account by a marker file inside that account's own Drive, not by drive letter. With any other account signed in, it saves nothing there, shows a red warning, and your YES videos wait in review.
2. **Test write OK:** writing, reading back and deleting a file in `My Drive\ClippersHQ Edits` all worked (54.6 GB free).
3. **Package: `D:\ClippersHQ_portable\me`, 12.0 GB**, in 84,565 files.
   - Inside: your key, every setting, your 42,376 accounts and history, your friends' links, the 2,007 waiting videos, `brain\`, and a bundled Python.
4. **New-PC test passed: 31 of 31.**
   - No Python on PATH, and zero questions with the same Drive account signed in.
   - With another account signed in, it asks one question.
   - Your own setup was unchanged afterwards.
5. **Still not inside:**
   - the 14,661 videos you approved earlier, which live in the OLD account's Drive;
   - the development repository (tests and build tools), which stays on this PC.

## Steps (srpski)
1. Na STAROM računaru, pre prelaska: Podešavanja > Moj paket > **Napravi ponovo moj paket** (oko 15 minuta).
2. Kopiraj `D:\ClippersHQ_portable\me` na USB. **Folder sadrži tvoj ključ: nikad ga ne otpremaj i ne deli.**
3. Na drugom računaru: prijavi Google Drive for desktop **novim nalogom**, kopiraj folder (ne na Radnu površinu, ne u OneDrive) i dva puta klikni **START.bat**. Ništa se ne instalira.
4. Ako hoćeš da proveriš kopiju, dva puta klikni **VERIFY.bat**.
5. Stari DA videi su u Drive-u starog naloga. Ako ih želiš u novom, podeli ili premesti tu fasciklu na drive.google.com.

## Steps (English)
1. On the OLD PC, before moving: Settings > My package > **Rebuild my package** (about 15 minutes).
2. Copy `D:\ClippersHQ_portable\me` to a USB stick. **The folder contains your key: never upload or share it.**
3. On the other PC: sign in to Google Drive for desktop with the **new account**, copy the folder (not onto the Desktop, not into OneDrive) and double-click **START.bat**. Nothing to install.
4. To check the copy, double-click **VERIFY.bat**.
5. The videos you approved before are in the old account's Drive. If you want them in the new one, share or move that folder on drive.google.com.

## What was done

**The Drive pin.**
- A marker file `My Drive\ClippersHQ Edits\.clippershq_account` holds a hash of the Google Drive account id, and the setting `drive_account` holds the same hash. The raw id is never stored or printed.
- The app accepts only a My Drive that carries this marker. The YES button, the daily run, sync and the package all use that same check.
- Before pinning, I confirmed that the signed-in account is the new one, by a yes/no check that its account data names it. Only one Drive account is signed in on this PC.
- The 14,661 earlier Drive paths point at the old account's files; none of those files is in the new Drive.

**The "me" package.**
- **Keys and links:**
  - The app and its runs use exactly one vendor key, LamaTok. It is in `data\secrets` in the app's own format; `config.json` is never copied.
  - Your friends' share tokens are in `data\share`.
- **Settings:** all 23 of your settings come along, including the Drive pin.
- **Data:**
  - the database copy (integrity OK);
  - the waiting videos and their pictures (11.27 GB);
  - `brain\`: 8 reports, 8 claim files, the FACTS sections on prices and spend, 29 memory notes, and `BRAIN.md` in Serbian and English.
- **Python:** python.org's embeddable 3.11.9 with the 10 pinned packages pre-installed. Its download is verified two ways:
  - python.org's signature on the zip checks out against Steve Dower's Windows release key (fingerprint `7ED10B65…FC624643487034E5`; not the 3.11 release manager's key);
  - `python.exe`, `pythonw.exe` and `python311.dll` all carry a valid Authenticode signature from the Python Software Foundation.
- **Files you click:** `START.bat` (on the first start it moves the paths, adds the Start Menu shortcut and sets up the daily run), `VERIFY.bat`, and READMEs in Serbian and English.
- **First start, with the same account signed in:** zero questions. If something is missing, the wizard asks only that: the key, or where YES videos go.
- **Settings > My package > "Rebuild my package"** builds the package in the background. This package was built by that button's route.
- **Accessibility:** reviewed before and after the interface changes. No blocking defects; the 4 minor findings are fixed.

**New-PC test (31 of 31)** used a temp folder with a space in its path, on D:, with its own ports and a fake "new" Google Drive carrying the same account's marker. In it:
- the server ran on the bundled Python, with no Python on PATH;
- 106,239 stored paths moved to the copy and to the new Drive;
- no wizard appeared, and your niches and settings were there;
- the key showed as set and never appeared on the page; Test key was blocked by test mode;
- a waiting video played;
- `VERIFY.bat` reported 0 failures;
- with another account's Drive signed in, the wizard asked only where YES videos go, and nothing was written to that Drive.
- Afterwards, the test task and the folder were removed, and your Start Menu, tasks, settings, key, share files, database and server were byte-identical.

## What I got wrong
1. **My first new-PC run left its test task in your Task Scheduler.** `schtasks` writes names with a leading `\`, so my check never recognised the task and the cleanup skipped it. I deleted the task by its exact name, fixed the test, and the rerun removes it.
2. **My first `python.org` signature check failed twice:**
   - I assumed the 3.11 release manager signs the Windows files; in fact the Windows release manager does.
   - keys.openpgp.org serves that key without its user ID, which GPG refuses.
   - Both are fixed in `scratch/bl1607/get_python.py`. Nothing was pinned before every check passed.
3. **BL-1607's claim was released with `--force`.** Its own work was all committed. The remaining edits were BL-1608's, and the commit hook will not mix two live rounds.
4. **One test (`test_bl1602_drive_guard`) read your real settings.** It now uses a temp folder.
5. **My Drive-pin script had your new account's name written in it** (part of an email address), in a local commit. The script now takes it as an argument and no file carries it, but that local commit still contains it. The repository is not pushed anywhere, and older local commits already contained the same word.

## Money
$0. Nothing was written to master, MARK, your workbook, the clipper label store, `config.json` or `dashboard/`.

## Leak scan
Scanned 50 files: the round's code, tests, scripts, claims and this report. The package itself is never committed or published.
- **Shape layer:** controls caught.
  - 2 hits, both the example link "tiktok.com/@name" (Serbian: "@ime") in the Accounts hint. These are the words "name" and "ime", not accounts.
- **Edit and lead corpus, by value:**
  - 400 hits are explained by the public vocabulary or by how often they appear in earlier reports;
  - 5 more were read with the value masked, and all are ordinary words or code tokens, the same ones as in BL-1606: the JS option name "notation", the start of the Serbian word for "moved" (×2), the edit word "velocity", and a test-fixture key.
- **0 leaks in what is published.**
- **One slip in a local file (#5 below):** the scratch script had your new account's name in it. It now takes the name as an argument, and no file carries it.
