# BL-909 — Whole machine disk audit

Machine: KINGSTON SNV2S1000G, single internal SSD, 931.5 GB. `D:` is a 29.3 GB removable USB stick
(UBUNTU 26_0), not part of this audit. Date 2026-09-19. No admin rights in this session.

## THE ARITHMETIC, FIRST, BECAUSE IT DECIDES EVERYTHING

**Roughly 500 GB free is NOT reachable by deleting junk on this machine, and it never was.**
The disk is 931.5 GB in total. 500 GB free means everything on it must fit in 430 GB. A single
folder, `OneDrive\Desktop\editing content`, is **383.96 GB** on its own, and the whole Desktop is
**498.14 GB**. Deleting every cache, log and temporary file on the machine is worth roughly
36 GB in practice, which this round has now taken. The honest answer is that the footage has to
move to another drive, or be turned into cloud only files, and nothing else gets there.

| | GB |
|---|---|
| Free at session start | 59.90 |
| Free immediately before the first deletion | 58.06 |
| **Free now, after this round** | **94.39** |
| Reclaimed by this round, measured as free space delta | **36.33** |
| Needed on top of that to reach 500 GB | **405.61** |
| `editing content` alone, verified NOT NTFS compressed | 383.96 |
| `editing content` + `twitch-clipper\library` | 408.09 |

Moving those two to an external drive lands at **502.5 GB free**. That is the plan that works.
See PART 5 for the two ways to do it.

---

## PART 0 — WHAT WAS OFF LIMITS, FIXED BEFORE ANYTHING WAS SCANNED

Nothing in this list was deleted, moved or modified.

• **The Desktop in full**, `C:\Users\Game Centar\OneDrive\Desktop`, 498.14 GB, 609,909 files. Every
  subfolder of it, including the project folders, was treated as untouchable.
• **All content and editing work**: `editing content` (Football, Combat Sports, Basketball, Tennis,
  Other Sports, B-Roll, Cars, Motorsport, Gym, American Sports), `C:\ClippersHQ_renders`,
  `AppData\Local\twitch-clipper\library`, and the footage in `Downloads`.
• **CapCut in its entirety**, 47.41 GB. It is his video editor, so Part 0 covers it.
• **Adobe Creative Cloud**, OBS Studio, HandBrake, Avidemux, FFmpeg, Tesseract.
• Windows itself, drivers, everything under Program Files and ProgramData belonging to an
  installed application, his Documents and Pictures, every repository, every browser profile.
• Anything a running process held open. Chrome (26 processes), Claude (18), Discord (6),
  Edge (8), OneDrive.Sync.Service, node and Docker were all live throughout.

### How an editor cache that a project depends on was told apart from a regenerable one

The test used was **what the file extension proves about the writer, not what the folder is named**.
Two folders on this machine are both called `ListSync` and only one is a log:

• `...\Microsoft\OneDrive\logs\ListSync` held 65,947 files with the `.odl` extension, which is
  OneDrive's diagnostic log format. A log file is written once and never read back by the product.
  **Deleted.**
• `...\Microsoft\OneDrive\ListSync\Common` holds 12 files, and they are
  `Microsoft.ListSync.Thumbnails.db` (6.54 GB), `Microsoft.LocalContent.db`,
  `Microsoft.CommonMediaCache.db` and their `-wal` and `-shm` companions. Those are live SQLite
  databases with open write ahead logs, held by a running service. That is sync state, not a log.
  **Left alone**, and it is in the DECIDE list instead.

That one letter of difference between the two paths is the whole audit in miniature, and it is why
nothing was deleted by pattern. Where the test could not be applied, the folder was left and named:
`.cache\codex-runtimes` (3.07 GB) contains what look like two runtime installs, one with a random
suffix that suggests an abandoned install, but nothing in it proves the codex CLI would still start
without them, so it was **not touched** and appears in DECIDE.

CapCut's `User Data\Cache` (2.32 GB) is genuinely a regenerable media cache and would normally
qualify for Part 3. It was still left alone, because Part 0 put content editing off limits without
an exception and 2.32 GB is not worth reading that instruction loosely.

---

## PART 1 — THE TRUE SIZE MAP

Measured with a reparse point aware walker so nothing is double counted through a junction. The
first pass missed 477 GB because `C:\Users\Game Centar\OneDrive` is itself a reparse point and was
being skipped; that is corrected here. Sizes are logical file length unless marked.

### Every directory over 1 GB, largest first

| GB | Last modified | What it is | Category |
|---|---|---|---|
| 498.14 | 2026-09-18 23:43 | `OneDrive\Desktop` (whole) | content |
| 383.96 | 2026-09-19 10:47 | `Desktop\editing content` | content |
| 114.39 | 2026-09-19 10:16 | `editing content\Football` | content |
| 93.55 | 2026-09-18 23:39 | `editing content\Combat Sports` | content |
| 74.94 | 2026-09-19 04:45 | `Desktop\clipper finder` | content/project |
| 57.91 | 2026-09-18 23:04 | `editing content\Basketball` | content |
| 47.41 | 2025-10-31 16:22 | `AppData\Local\CapCut` | content (editor) |
| 45.96 | 2026-09-18 23:41 | `editing content\Tennis` | content |
| 36.32 | 2026-09-17 16:31 | `CapCut\Apps` (25 versions) | content (editor) |
| 36.48 | 2026-09-19 04:45 | `clipper finder\output` | content/project |
| 36.19 | 2026-09-17 23:56 | `C:\Windows` | system |
| 28.00 | 2026-09-18 19:39 | `C:\pagefile.sys` | system |
| 27.67 | 2026-09-19 10:20 | `AppData\Local\Google\Chrome\User Data` (36 profiles) | cache/profile |
| 27.04 | 2026-09-18 22:16 | `editing content\Other Sports` | content |
| 24.13 | 2026-08-17 13:14 | `AppData\Local\twitch-clipper\library` (7,664 mp4) | content |
| 22.50 | 2026-09-18 21:24 | `Downloads` | downloads |
| 18.52 | 2026-09-19 04:45 | `clipper finder\quarantine` | content/project |
| 18.38 | 2026-09-17 23:52 | `Windows\WinSxS` | system |
| 16.60 | 2026-09-17 23:12 | `editing content\ChatExport_2026-09-17` | content |
| 13.22 | 2026-08-16 19:05 | `Desktop\twitch clipper` | content/project |
| 13.21 | 2026-09-19 10:49 | `Desktop\neuraltrack` | content/project |
| 11.08 | 2026-09-18 19:01 | `C:\Program Files (x86)` | applications |
| 10.31 | 2026-09-19 10:22 | `AppData\Roaming\Claude` | applications |
| 10.13 | 2026-09-18 23:39 | `editing content\B-Roll` | content |
| 9.98 | 2026-09-12 12:43 | `AppData\Local\Programs` | applications |
| 9.56 | 2026-09-16 15:27 | `C:\hiberfil.sys` | system |
| 9.14 | 2026-09-18 10:01 | `C:\Program Files` | applications |
| 9.12 | 2026-09-19 10:48 | `Roaming\Claude\vm_bundles` (9 files) | applications |
| 9.09 | 2026-09-18 13:58 | `Windows\System32` | system |
| 8.94 | 2026-02-03 07:46 | `WindowsApps\...aTrain` | applications |
| 8.74 | 2026-09-18 16:56 | `C:\ClippersHQ_renders` | content |
| 8.66 | 2026-09-18 23:39 | `editing content\Cars` | content |
| 7.42 | 2026-09-19 10:48 | `OneDrive\ListSync\Common` (sync dbs) | cache (live) |
| 7.14 | 2026-09-18 17:44 | `neuraltrack\scratch` | content/project |
| 6.32 | 2026-09-17 17:06 | `CapCut\User Data` | content (editor) |
| 6.12 | 2026-09-19 04:45 | `clipper finder\scratch` | content/project |
| 6.10 | 2026-09-18 19:34 | `AppData\Local\AMD` (shader caches) | cache |
| 5.90 | 2026-09-19 04:45 | `clipper finder\backups` | content/project |
| 5.58 | 2026-09-19 10:00 | `editing content\Motorsport` | content |
| 5.52 | 2026-08-31 19:40 | `AppData\Local\npm-cache` | cache |
| 4.77 | 2025-12-03 00:53 | `CapCut\Videos` (9 files) | content (editor) |
| 4.71 | 2026-08-06 20:42 | `Program Files (x86)\Microsoft` | applications |
| 4.65 | 2026-09-17 14:48 | `.cache\huggingface` (ML models) | cache |
| 4.42 | 2026-09-17 14:29 | `AppData\Local\Programs\Python` | applications |
| 4.41 | 2026-08-11 12:16 | `AppData\Local\ClippersHQ` | applications |
| 4.40 | 2026-09-19 10:22 | `C:\Users\Game Centar\.claude` | applications |
| 4.08 | 2026-08-25 11:57 | `Program Files\Docker` | applications |
| 3.86 | 2026-09-05 17:32 | `AppData\Local\wsl` (Linux disk image) | applications |
| 3.81 | 2026-09-17 14:04 | `Desktop\S8+ G955U 20251126OK root` | content |
| 3.81 | 2026-09-19 09:53 | `Desktop\Random` | content |
| 3.74 | 2026-01-03 00:20 | `AppData\Local\uv` | cache |
| 3.54 | 2026-09-18 10:01 | `C:\ProgramData` | applications |
| 3.43 | 2026-09-17 14:40 | `.claude\projects` | applications |
| 3.33 | 2026-08-24 15:04 | `.vscode\extensions` | applications |
| 3.11 | 2025-09-04 18:14 | `AppData\Local\pip` | cache |
| 3.11 | 2026-09-19 10:25 | `AppData\Local\Temp` | temp |
| 3.07 | 2026-08-30 21:33 | `.cache\codex-runtimes` | unknown |
| 2.99 | 2026-08-30 16:10 | `Program Files (x86)\Microsoft Visual Studio` | applications |
| 2.96 | 2026-09-16 16:23 | `AppData\Local\ms-playwright` | cache |
| 2.94 | 2026-09-16 15:25 | `AppData\Local\Packages` | applications |
| 2.82 | 2026-09-18 23:39 | `editing content\American Sports` | content |
| 2.74 | 2026-08-31 20:45 | `AppData\Local\Programs\Ollama` | applications |
| 2.24 | 2026-09-18 23:16 | `AppData\Local\Spotify` | applications |
| 2.07 | 2026-08-31 18:43 | `Desktop\ceo-dashboard` | content/project |
| 1.95 | 2026-09-18 23:32 | `Desktop\ClippersHQ` | content/project |
| 1.93 | 2026-09-12 16:33 | `neuraltrack\.venv` | content/project |
| 1.79 | 2026-08-28 22:32 | `Roaming\.minecraft` | applications |
| 1.74 | 2026-08-30 16:09 | `Windows\assembly` | system |
| 1.70 | 2026-09-19 09:58 | `ProgramData\Microsoft` | applications |
| 1.61 | 2026-09-19 10:00 | `Roaming\Telegram Desktop` | applications |
| 1.59 | 2026-09-15 21:17 | `neuraltrack\media` | content/project |
| 1.49 | 2025-08-09 16:01 | `Program Files (x86)\Windows Kits` | applications |
| 1.39 | 2026-09-19 10:07 | `Roaming\npm` | applications |
| 1.32 | 2026-07-16 16:24 | `Windows\SystemApps` | system |
| 1.31 | 2026-09-18 10:19 | `Windows\SysWOW64` | system |
| 1.29 | 2026-09-19 09:43 | `Local\Microsoft\Edge\User Data` | cache/profile |
| 1.18 | 2026-09-19 10:01 | `editing content\Gym` | content |
| 1.17 | 2026-09-17 23:19 | `Local\Microsoft\WinGet\Packages` | applications |
| 1.14 | 2025-08-08 00:37 | `AppData\LocalLow` | applications |
| 1.05 | 2026-09-18 18:55 | `Roaming\Code` | applications |

Before this round, `OneDrive\logs\ListSync` sat at 64.36 GB logical and would have been line three
of that table. It is gone, so it is listed in PART 3 instead.

### Total per category

| Category | GB | Note |
|---|---|---|
| **Content and editing work (HIS, UNTOUCHABLE)** | **578.42** | Desktop 498.14 + CapCut 47.41 + twitch-clipper library 24.13 + ClippersHQ_renders 8.74 |
| Installed applications | 76.80 | includes an estimate for WindowsApps, which is only partly readable without admin |
| Caches and temporary files | 84.28 | on disk, not logical (see the compression note below) |
| Downloads and installers | 22.50 | mostly footage, see PART 4 |
| System and Windows | 73.77 | Windows 36.19 + pagefile 28.00 + hiberfil 9.56 + swapfile 0.02 |
| Project leftovers from prior rounds | 1.34 | `C:\mbwt` 0.75, `projects1` 0.34, `w` 0.09, `wt` 0.08, `w2` 0.01, six empty `bl9xx-sandbox` dirs, `tmp`, `temp` |
| Unknown or unreadable without admin | 34.93 | `System Volume Information`, the rest of `WindowsApps`, `$Recycle.Bin` 0.69, assorted denied directories |
| **Total, against 872.04 GB measured used at session start** | **872.04** | |

**Why logical sizes overstate, and it is worth knowing.** The OneDrive `.odl` logs measured
64.36 GB by file length, but deleting 65,974 of them returned only **16.51 GB** of free space,
because NTFS had them compressed at about 4 to 1. The same effect applies to hardlinks: the `uv`
cache measured 3.74 GB but freed 3.12 GB, the rest being hardlinked into live virtualenvs. The
caches row above therefore uses on disk figures. The footage does not have this problem: a sample
of `editing content\Football` shows plain `Archive` attributes with no compression flag, so
**383.96 GB there is 383.96 GB of real disk**, and moving it frees all of it.

**Only three of those seven categories are even candidates for deletion** (caches 84.28, downloads
22.50, leftovers 1.34, so roughly 108 GB gross), and most of that 108 is either locked by a running
process, or is his. That is the whole reason 500 GB is out of reach without moving content.

---

## PART 2 — INSTALLED APPLICATIONS OVER 1 GB. NOTHING WAS UNINSTALLED.

### First, an honest warning about "last used" on this machine

**This machine cannot tell you reliably when most applications were last opened, and I am not going
to invent it.**

• `C:\Windows\Prefetch` is **empty**, zero `.pf` files, so there is no run history to read.
• Last access timestamps are enabled, but nearly every executable on the disk reports a last access
  of 2026-09-18 or 2026-09-19, including ones that are obviously not in daily use. Something swept
  the whole disk on those two days, most likely a Defender scan or the search indexer, and it reset
  them all. The Start Menu shortcuts show the same tell: 60 of them share the timestamp
  2026-09-18 12:33 to the minute.

So the "last used" column below is marked `no evidence` wherever the evidence is that artifact
rather than a real launch. **Rank by size and install date, and by whether you recognise the name.**

### Every installed application over 1 GB

| GB | Installed | Last used | What it is, plainly |
|---|---|---|---|
| 36.32 | ongoing | in use | **CapCut**, his video editor. 25 separate program versions kept side by side, 7.3.0 through 9.5.0. Only the newest is needed. |
| 8.94 | 2026-02-03 | no evidence | **aTrain**, a Microsoft Store app that transcribes audio to text offline. Installed once in February and the files have not changed since. The largest app you may not recognise. |
| 4.42 | 2026-08-05 | in use | **Python** 3.11 and 3.13, two full installs. Used by the projects. |
| 4.08 | 2026-08-25 | service running | **Docker Desktop**, runs Linux containers. Heavy, and only useful if you are running containers. |
| 3.86 | 2026-09-05 | no evidence | **WSL disk image**, the virtual hard disk holding a Linux install inside Windows. Two files. |
| 3.33 | 2026-08-24 | in use | **VS Code extensions**, 18,484 files. |
| 2.99 | 2026-08-30 | no evidence | **Visual Studio Build Tools 2019**. FLAG: a compiler toolchain. Some Python and Node packages need it to build. |
| 2.74 | 2026-08-31 | no evidence | **Ollama**, runs AI language models on your own machine. The model store `.ollama` is empty, so it is installed with nothing loaded. |
| 2.24 | 2026-09-14 | 2026-09-18 | **Spotify**. |
| 2.23 | 2026-09-15 | in use | **Microsoft Edge WebView2 Runtime**. FLAG: NOT a browser. Many desktop apps render their windows with it. Removing it breaks them. |
| 2.11 | 2026-09-18 | in use | **Microsoft Edge**. |
| 2.07 | ongoing | in use | **Claude** desktop app, of which 9.12 GB is `vm_bundles`, its sandbox virtual machine images. |
| 1.94 | 2026-09-15 | no evidence | **OpenAI Codex**, a coding assistant. |
| 1.79 | 2026-08-28 | 2026-08-28 | **Minecraft**, plus **Lunar Client** at 0.38 GB, a Minecraft launcher. |
| 1.61 | 2026-09-17 | 2026-09-19 | **Telegram Desktop**, size is almost entirely downloaded photos and videos. |
| 1.49 | 2025-08-09 | no evidence | **Windows 10 SDK**. FLAG: a dependency of the Build Tools above. |
| 1.39 | ongoing | in use | **npm global packages**. |
| 1.33 | 2026-09-18 | in use | **Visual Studio Code**. |
| 1.17 | 2026-09-17 | no evidence | **FFmpeg** via WinGet, two copies (Gyan build 0.63 GB, yt-dlp build 0.43 GB). Video conversion engine. FLAG: other tools call it. |
| 1.05 | 2026-09-18 | in use | **VS Code user data**. |
| 1.01 | 2026-09-01 | no evidence | **LobeHub**, a Chrome installed web app. |
| 1.01 | 2026-09-16 | no evidence | **Chrome Remote Desktop**. |
| 0.98 | 2024-04-24 | in use | **Google Chrome** program files. The 27.67 GB of profiles is separate. |
| 0.82 | ongoing | no evidence | **Adobe Creative Cloud**. Content editing, off limits. |

### Runtimes, redistributables and dependencies. Do not remove these to save space.

Every one of these is something another program needs, and removing it is how an app you do want
stops working:

• **Microsoft Edge WebView2 Runtime** (2.23 GB) — desktop apps draw their windows with it.
• **Windows 10 SDK** 10.0.19041 (1.49 GB) and its four sibling components (Universal CRT Headers
  0.28, Store Apps Headers 0.22, Store Apps Libs 0.18, Store Apps Tools 0.14).
• **Visual Studio Build Tools 2019** (2.99 GB) — needed to compile native Node and Python modules.
• **Microsoft Windows Desktop Runtime 8.0.22** (0.22 GB) — needed by .NET applications.
• **FFmpeg**, both copies — yt-dlp and other tools shell out to it.
• **AMD Install Manager** and the AMD driver tree — graphics.
• **Microsoft GameInput**, **GamingServices**, **EasyAntiCheat** — game support.

### One thing worth looking at for a different reason

**Outbyte PC Repair** (0.10 GB, installed 2026-07-31, `C:\Program Files (x86)\Outbyte`, plus
0.29 GB in ProgramData) is a "PC cleaner" of the kind usually installed by accident alongside
something else. It is small so it is not a disk question, but it runs on this machine and you may
not have chosen it. Your call, and it is in DECIDE.

---

## PART 3 — WHAT WAS DELETED. EXPLICIT PATHS ONLY, ONE FILE AT A TIME, NEVER A WILDCARD.

Method, the same discipline BL-899 and BL-900 used: every file in a class was enumerated into a
written list on disk first, then each was deleted by its own literal path in a loop, then the
emptied subdirectories were removed deepest first. No wildcard was ever passed to a delete. Every
refusal was recorded with its reason and none was forced. **248,785 files deleted, 243 refused.**

Reclaim is measured as the **C: free space delta**, not as the sum of file lengths, because
compression and hardlinks make those two different numbers and the free space one is the true one.

| # | Path | Files gone | Refused | GB freed | Running total free |
|---|---|---|---|---|---|
| 1 | `...\AppData\Local\Microsoft\OneDrive\logs\ListSync` | 65,974 | 13 | **16.507** | 74.57 |
| 2 | `...\AppData\Local\AMD\DxCache` | 993 | 104 | 3.859 | 78.43 |
| 3 | `...\AppData\Local\AMD\DxcCache` | 505 | 57 | 1.382 | 79.81 |
| 4 | `...\AppData\Local\CrashDumps` | 10 | 0 | 0.288 | 80.10 |
| 5 | `C:\Windows\SoftwareDistribution\Download` | 0 | 38 | 0.000 | 80.10 |
| 6 | `...\AppData\Local\npm-cache\_cacache` | 5,029 | 0 | 4.098 | 84.20 |
| 7 | `...\AppData\Local\npm-cache\_logs` | 11 | 0 | 0.000 | 84.20 |
| 8 | `...\AppData\Local\npm-cache\_npx` | 95,934 | 0 | 1.048 | 84.36 |
| 9 | `...\AppData\Local\npm-cache\_prebuilds` | 3 | 0 | 0.016 | 84.37 |
| 10 | `...\AppData\Local\pip\cache` | 3,988 | 0 | 3.114 | 87.31 |
| 11 | `...\AppData\Local\uv\cache` | 42,155 | 0 | 3.120 | 91.49 |
| 12 | `...\AppData\Local\Temp` | 34,183 | 31 | 2.924 | 94.41 |
| | **TOTAL** | **248,785** | **243** | **36.33** | **94.39** |

### What regenerates each one, and what deleting it costs

| Class | What rebuilds it | Cost to him |
|---|---|---|
| **OneDrive `.odl` diagnostic logs**, 16.51 GB | OneDrive writes new ones continuously; it had already written fresh ones before this sentence was typed | **Free.** These are write only telemetry. The only loss is diagnostic history if Microsoft support ever asked for it. Nothing reads them back. |
| **AMD `DxCache` and `DxcCache`**, 5.24 GB | The graphics driver recompiles a shader the first time each app or game needs it | **Near free.** One brief extra pause the first time a given game or GPU accelerated app runs, then it is back to normal. |
| **Crash dumps**, 0.29 GB | Written only when something crashes | **Free.** They were records of past crashes, 10 files. |
| **npm `_cacache`, `_npx`, `_prebuilds`, `_logs`**, 5.16 GB | `npm install` and `npx` re download and refill it | **Costs bandwidth.** The next install in each project downloads packages instead of reading them locally. Slower once per project, no functional change. |
| **pip cache**, 3.11 GB | `pip install` re downloads wheels | **Costs bandwidth.** Same shape as npm. |
| **uv cache**, 3.12 GB | `uv` re downloads and re links | **Costs bandwidth.** Note only 3.12 of 3.74 GB came back, because the remainder is hardlinked into live virtualenvs such as `neuraltrack\.venv`, which are untouched and still work. |
| **User `Temp`**, 2.92 GB | Applications write there constantly | **Free.** 31 files in current use were refused and left. |

### What would not delete, named rather than forced

• **38 files in `C:\Windows\SoftwareDistribution\Download`** (0.23 GB), all `Access to the path is
  denied`. This session has no administrator rights. These are finished Windows Update payloads and
  Windows clears them itself in time; Disk Cleanup as administrator would take them now.
• **13 files under `OneDrive\logs\ListSync`**: `microsoftNucleusTelemetryCache.otc` and its `-shm`
  and `-wal` companions in four subfolders, plus three `.aodl` files currently being appended to.
  Held open by `OneDrive.Sync.Service` (PID 37952), which is running.
• **161 shader files under the two AMD cache folders**, split between `being used by another
  process` and `Access to the path is denied`. Live GPU state.
• **31 `.tmp` files in `AppData\Local\Temp`**, held open by running Claude, node and Chrome
  processes.

### What qualified as a cache and was deliberately NOT deleted

• **Chrome**, 27.67 GB across 36 profiles. Chrome was running with 26 processes throughout. Part 0
  put both browser profiles and anything a running process holds out of scope, and deleting cache
  folders under a live Chrome risks corrupting a profile for a few GB. Left entirely.
• **Edge**, 1.29 GB. Same reason, 8 processes running.
• **CapCut `User Data\Cache`**, 2.32 GB. Genuinely regenerable, but CapCut is his editor and Part 0
  admitted no exception.
• **`.cache\codex-runtimes`**, 3.07 GB. Could not be proven regenerable. Left and named.
• **`OneDrive\ListSync\Common`**, 7.42 GB of live SQLite sync databases. Not a log.
• **`$Recycle.Bin`**, 0.69 GB. That is his own deleted files and emptying it would remove his
  ability to restore them. His call, not mine.

---

## PART 4 — FOR HIM TO DECIDE. NOTHING HERE WAS TOUCHED.

Ranked by size. Everything on the Desktop is listed for information only, because Part 0 put the
Desktop off limits, but he can move or delete any of it himself.

| GB | Last touched | What it is and what he loses |
|---|---|---|
| 383.96 | 2026-09-19 10:47 | `Desktop\editing content`. His footage library, 12,266 files across 11 sports folders. **Losing it is unthinkable; moving it is the entire answer to his question.** See PART 5. |
| 74.94 | 2026-09-19 04:45 | `Desktop\clipper finder`. Of which `output` 36.48, `quarantine` 18.52, `scratch` 6.12, `backups` 5.90. Generated output, not source. Likely the largest genuinely reclaimable item after the footage, if the outputs have been used. |
| 36.32 | 2026-09-17 16:31 | `CapCut\Apps`, 25 program versions. Keeping only 9.5.0.4050, the current one, frees about **34.8 GB**. He loses the ability to roll back to an older CapCut. Do it from CapCut or the Store, not by hand. |
| 24.13 | 2026-08-17 13:14 | `AppData\Local\twitch-clipper\library`, 7,664 mp4 files downloaded by the twitch clipper tool. Not touched in a month. He loses the local copies; they can be re downloaded. |
| 22.50 | 2026-09-18 21:24 | `Downloads`. Top items are footage: Conor McGregor 3.85, Neymar 2.33, Ronaldo 0.72, plus tennis highlights. Also about 0.6 GB of old installers (Discord, VS Code, ProtonVPN, DroidCam, Shift). He loses whatever he has not already filed into `editing content`. |
| 13.22 | 2026-08-16 19:05 | `Desktop\twitch clipper`. Project folder. |
| 13.21 | 2026-09-19 10:49 | `Desktop\neuraltrack`. Project folder, in use today. |
| 9.12 | 2026-09-19 10:48 | `Roaming\Claude\vm_bundles`, 9 sandbox VM images. Regenerable by re download, but it is a large download and the app is running. |
| 8.94 | 2026-02-03 07:46 | **aTrain** transcription app. Untouched since February. If he does not transcribe audio, this is 8.94 GB for nothing. Uninstall from the Store. |
| 8.74 | 2026-08-28 23:17 | `C:\ClippersHQ_renders`, 14,181 png and 1,872 mp4 of project render output. He loses render history from August. |
| 7.42 | 2026-09-19 10:48 | `OneDrive\ListSync\Common`, of which `Microsoft.ListSync.Thumbnails.db` is 6.54 GB. A thumbnail database that grew unchecked. Only safe to clear by resetting OneDrive, which re syncs. |
| 6.32 | 2026-09-17 17:06 | `CapCut\User Data`. Contains `Projects` 2.69 GB, which is real project data, and `Cache` 2.32 GB, which is not. Clear the cache from inside CapCut. |
| 4.77 | 2025-12-03 00:53 | `CapCut\Videos`, 9 exported videos from last December. If those are already uploaded, this is free. |
| 4.65 | 2026-09-17 14:48 | `.cache\huggingface`, 67 downloaded AI model files. Re downloadable, but it is several GB over the network. |
| 4.42 | 2026-09-17 14:29 | Two full Python installs, 3.11 and 3.13. Removing one frees roughly 2 GB, but check nothing points at it first. |
| 4.41 | 2026-08-11 12:16 | `AppData\Local\ClippersHQ`. App data, untouched since August. |
| 4.08 | 2026-08-25 11:57 | **Docker Desktop**. If he is not running containers, this is the single biggest app he could drop. |
| 3.86 | 2026-09-05 17:32 | `AppData\Local\wsl`, the Linux virtual disk. Deleting it destroys whatever is inside that Linux install. |
| 3.33 | 2026-08-24 15:04 | VS Code extensions. Pruning unused ones might free 1 to 2 GB. |
| 3.07 | 2026-08-30 21:22 | `.cache\codex-runtimes`. **Could not classify.** One of the two looks like an abandoned install with a random suffix, but that was not provable, so it stays. |
| 2.99 | 2026-08-30 16:10 | Visual Studio Build Tools 2019. Only if nothing needs to compile native modules. |
| 2.96 | 2026-09-16 16:23 | `ms-playwright` browser binaries. Regenerable with `npx playwright install`, costs a download. |
| 2.74 | 2026-08-31 20:45 | **Ollama** with no models loaded. Installed and apparently unused. |
| 1.94 | 2026-09-15 | **OpenAI Codex** Store app. |
| 1.79 | 2026-08-28 22:32 | Minecraft, plus Lunar Client 0.38. Last played 2026-08-28. |
| 1.61 | 2026-09-19 10:00 | Telegram media cache. Clearable from inside Telegram; he loses locally cached photos and videos. |
| 1.49 | 2025-08-09 16:01 | Windows 10 SDK. **FLAG: the Build Tools need it.** Remove both or neither. |
| 1.47 | 2026-09-18 21:00 | Spotify offline audio. Clearing it removes downloaded playlists. |
| 0.75 | 2026-07-28 20:48 | `C:\mbwt`, a root folder from a prior round. 2,318 files, not touched since July. |
| 0.72 | 2026-07-30 13:06 | `.EasyOCR`, 7 downloaded OCR model files. |
| 0.69 | 2026-08-31 18:46 | `$Recycle.Bin`. Emptying it is instant and gives up the ability to restore. |
| 0.39 | 2026-07-31 | **Outbyte PC Repair**, program plus ProgramData. Probably not installed on purpose. |
| 0.34 | 2025-09-15 03:12 | `C:\projects1`, 18,236 files, untouched for a year. |
| 0.18 | mixed | Six empty `C:\bl89x/bl90x-sandbox` directories, `C:\w`, `C:\wt`, `C:\w2`, `C:\tmp`, `C:\temp`, `C:\c`, `C:\.ADSPOWER_GLOBAL`. Round leftovers. |

**Total this DECIDE group would free if every line went: about 660 GB**, but 384 of that is the
footage he must keep somewhere, and 111 more is Desktop project folders. **Excluding the footage
and the Desktop entirely, the DECIDE list is worth roughly 105 GB.**

---

## PART 5 — THE HONEST RECOMMENDATION

**No. He cannot reach roughly 500 GB free by deleting, because his footage alone is 383.96 GB on a
931.5 GB disk; the only things that get him there are moving `editing content` to an external drive
or turning it into OneDrive cloud only files, and either one does it on its own.**

### The numbers

| | GB |
|---|---|
| Free before this round | 58.06 |
| **Free after this round** | **94.39** |
| Reclaimed by this round | 36.33 |
| Still to find to reach 500 | 405.61 |
| Everything left in DECIDE excluding footage and Desktop | ~105 |
| Best case by deleting only, keeping the footage | **~199** |
| `editing content` moved off, verified uncompressed | +383.96 → **478.35** |
| plus `twitch-clipper\library` | +24.13 → **502.48** |

Deleting alone tops out near **199 GB free** and that already assumes he gives up Docker, Ollama,
aTrain, Minecraft, the WSL image, the huggingface models and his Downloads folder. It is 300 GB
short.

### Option A, an external drive. The straightforward answer.

Buy a **1 TB external SSD**. 512 GB is the arithmetic minimum for `editing content` today at
383.96 GB, but that folder was written to at 10:47 this morning and is still growing, so 512 GB
leaves no headroom and 1 TB is the sensible buy. Move `editing content` and, if he wants margin,
`twitch-clipper\library` as well. That is 502 GB free and the work stays entirely intact.

One thing to know before moving it: `editing content` currently lives inside
`OneDrive\Desktop`, so it is being synced to OneDrive. Moving it to an external drive takes it out
of sync, which means **the cloud copy stops being a backup**. If OneDrive is his only backup of
that footage today, he needs a backup plan for the external drive before he moves anything.

### Option B, no hardware at all, if his OneDrive plan has room

Because that folder is already in OneDrive, he can right click it and choose **Free up space**.
OneDrive keeps the files in the cloud and leaves local placeholders that take almost no disk. That
would free the same 383.96 GB with nothing to buy. The catch is real: every clip has to download
again the moment he opens it in an editor, which is painful when scrubbing large `.mov` files, and
his OneDrive quota has to actually hold 384 GB. **Check the quota first.** Best used on the sports
folders he is not currently cutting, for example Tennis, Motorsport and American Sports, keeping
Football and Combat Sports local.

### Recommended: do both, partially.

Free up space on the archive sports folders, and keep whatever he is actively cutting on the local
disk. He gets most of the 384 GB without waiting on a delivery, and buys the drive for the folders
he touches every day.

### What stops it filling up again

Ranked by how fast each one actually regrew, measured from the oldest surviving file:

1. **OneDrive `.odl` logs, by a distance.** The oldest was dated 2026-01-17 and they reached
   64 GB logical by 2026-09-19. That is about **8 GB of logical log per month**, roughly 2 GB of
   real disk, and it will do it again. This is a known OneDrive defect, not something he did.
   **Check `%LOCALAPPDATA%\Microsoft\OneDrive\logs\ListSync` every few months** and clear it. It
   cannot be capped from the OneDrive settings UI.
2. **CapCut keeps every version it ever installs.** 25 of them, about 1.45 GB each, one new one
   roughly every two weeks. That is **3 GB a month, forever**. Prune `CapCut\Apps` back to the
   current version whenever it is updated.
3. **The `ListSync` thumbnail database**, 6.54 GB and growing with the size of the synced library.
   It will grow further as `editing content` grows.
4. **AMD shader caches**, 6.1 GB. These regrow with normal use and are harmless. Leave them unless
   space is tight.
5. **npm, pip and uv caches**, 12.4 GB combined. `npm cache clean --force`, `pip cache purge` and
   `uv cache clean` are the supported commands. Once or twice a year is plenty.
6. **Chrome**, 27.67 GB across **36 profiles**. That profile count is the thing worth looking at.
   Each one carries its own cache and history. If some of those profiles are dead, removing them
   from `chrome://settings` is worth several GB and is safer than touching the folders.

The one thing that can be scheduled: turn on **Storage Sense** in Settings, System, Storage. It
clears temporary files and the Recycle Bin on a schedule by itself. It will not touch the OneDrive
logs, which is why item 1 stays manual.

Two further items that need administrator rights and were therefore out of reach here:
`powercfg /h off` removes **`hiberfil.sys`, 9.56 GB**, at the cost of losing hibernate, and Disk
Cleanup run as administrator would take the 38 Windows Update files that were refused.

---

## METHOD AND MODEL SPLIT

**Cheap model, measurement only:** one Haiku subagent produced the installed application inventory,
the registry uninstall entries, the Store package sizes and the last access evidence. It was given
explicit instructions to print raw tables and to interpret nothing, and it was told not to delete,
uninstall or modify anything.

**Strongest model, everything that decides an outcome:** all directory walking that fed a deletion,
every classification, every path on the delete list and every deletion itself. Per BL-899, the raw
output of every measurement that led to a delete was read directly rather than through a relayed
summary. That mattered twice in this round:

1. The first whole disk walk reported 395 GB against 872 GB used. Accepting a summary would have
   meant reporting a 477 GB hole. Reading the reparse point inventory directly showed that
   `OneDrive` is itself a reparse point and the walker was skipping the entire Desktop.
2. The subagent's "last used" table looked authoritative and was mostly an artifact of a disk wide
   scan on 2026-09-18. Reading it against the empty Prefetch folder and the 60 Start Menu shortcuts
   sharing one timestamp is what turned it from an answer into a caveat.

No build was run and none is claimed; this was a disk round. No database, no repository and no
project code was touched. The accessibility agents were not invoked because this round wrote no
user facing code of any kind, no component, template or stylesheet.
