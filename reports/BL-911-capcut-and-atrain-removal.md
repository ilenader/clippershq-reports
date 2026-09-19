# BL-911 — CapCut old versions and aTrain removed. Two items, nothing else.

Follows BL-909, which audited the whole disk, reclaimed 36.33 GB across 12 cache classes and left a
DECIDE list untouched. The owner was asked and named exactly two items from it. Exactly two were
removed.

**Result: 93.222 GB free before, 136.858 GB free after, a real delta of 43.636 GB.** CapCut's 23
superseded program versions returned 34.675 GB and aTrain returned 8.961 GB. Nothing was refused,
nothing else was touched, and CapCut's current version is byte for byte intact.

---

## MODEL SPLIT

Every decision and every deletion in this round ran on the strongest model, reading raw tool output
directly. **No subagent was used at all.** BL-909 delegated its installed application inventory to a
Haiku subagent because that work fed a report rather than a delete, and it then had to discard part
of that subagent's "last used" table as an artifact. In this round every single measurement fed
straight into a decision about removing something, so none of it qualified for a cheaper model and
none of it was delegated. The version identification, the dependency checks, the removal scripts and
the verification were all read first hand.

That paid for itself twice here, in PART 0 and in PART 3, both noted below.

---

## PART 0 — WHICH CAPCUT VERSION IS ACTUALLY CURRENT, AND IS CAPCUT RUNNING

### CapCut was not running, so the round could proceed

Checked three ways before anything was touched: no process whose name matches CapCut, lveditor,
VideoEditor or Bytedance; no process anywhere on the machine whose executable path lies under the
CapCut tree; and the removal script re-checks the same condition and aborts if it finds one. It did
not find one. **CapCut was closed for the entire round.**

### The current version was read from CapCut's own files, not assumed from the highest number

BL-909 named 9.5.0.4050 but measured it on 19 September, and CapCut updates roughly fortnightly, so
that number was treated as unverified. The launcher chain is what settles it:

• The Start Menu shortcut does **not** point at a version folder. It points at
  `AppData\Local\CapCut\Apps\CapCut.exe`, a 4.74 MB **stub launcher** sitting above all of them.
• Beside that stub are `ProductInfo.xml` and `Configure.ini`. Searching the stub's own bytes finds
  **one** occurrence of the string `ProductInfo` and **zero** occurrences of `9.5.0.4050`, so the
  stub resolves the version at run time by reading that file rather than having one compiled in.
• `ProductInfo.xml`, written 2026-09-16 11:41, declares `full_appver value="9.5.0.4050"` and
  `appver value="9.5.0"`.
• The registry entry at `HKCU\...\Uninstall\CapCut` independently reports
  `DisplayVersion = 9.5.0.4050`.

**Current version = 9.5.0.4050**, confirmed by two independent sources that agree. It does happen to
be the highest number present, but that is a result here, not the method.

### One more thing the config gave up, which mattered

`Configure.ini` is 28 bytes and contains exactly this:

```
[capcut]
last_version=
```

`last_version` is CapCut's own rollback pointer and **it is empty**. Nothing on this machine was
pinned to an older build. Had it named a version, that version would have been kept.

### Every version folder before removal. The count was 24, not 25.

**BL-909 stated 25 version folders and that was wrong. There were 24.** Its own measurement table
listed 24 distinct version directories, so the 25 was a counting error in the prose, not a folder
that has since vanished. The figure it derived from it, about 34.8 GB freed by keeping only the
current version, was still very close: the true answer measured 34.741 GB before removal and
34.675 GB was actually returned.

| Version | GB | Files | Created | Last modified | CapCut.exe |
|---|---|---|---|---|---|
| 7.3.0.2974 | 1.650 | 3552 | 2025-10-31 16:22 | 2025-11-19 15:55 | yes |
| 7.5.0.3053 | 1.458 | 3550 | 2025-11-19 15:56 | 2025-12-04 23:21 | yes |
| 7.6.0.3123 | 1.462 | 3552 | 2025-12-04 23:22 | 2025-12-11 19:59 | yes |
| 7.7.0.3143 | 1.464 | 3552 | 2025-12-11 19:59 | 2026-01-11 22:55 | yes |
| 7.9.0.3294 | 1.479 | 3714 | 2026-01-11 22:55 | 2026-02-02 15:55 | yes |
| 8.0.1.3366 | 1.490 | 3715 | 2026-02-02 15:55 | 2026-02-18 02:40 | yes |
| 8.1.1.3417 | 1.492 | 3739 | 2026-02-18 02:41 | 2026-03-12 11:40 | yes |
| 8.2.0.3462 | 1.492 | 3735 | 2026-03-12 11:40 | 2026-03-22 19:19 | yes |
| 8.3.0.3497 | 1.492 | 3737 | 2026-03-22 19:20 | 2026-04-22 18:03 | yes |
| 8.5.0.3590 | 1.503 | 3752 | 2026-04-22 18:03 | 2026-05-20 17:05 | yes |
| 8.6.0.3667 | 1.462 | 3744 | 2026-05-20 17:05 | 2026-06-04 21:08 | yes |
| 8.7.0.3685 | 1.472 | 3934 | 2026-06-04 21:09 | 2026-06-21 13:36 | yes |
| 8.8.0.3774 | 1.481 | 3990 | 2026-06-21 13:37 | 2026-06-25 14:20 | yes |
| 8.9.0.3794 | 1.490 | 3983 | 2026-06-25 14:21 | 2026-06-26 14:05 | yes |
| 8.9.1.3802 | 1.490 | 3992 | 2026-06-26 14:06 | 2026-07-18 21:46 | yes |
| 9.0.0.3858 | 1.500 | 4039 | 2026-07-18 21:47 | 2026-07-22 21:20 | yes |
| 9.1.0.3879 | 1.501 | 4039 | 2026-07-22 21:20 | 2026-07-28 15:38 | yes |
| 9.2.0.3914 | 1.557 | 4052 | 2026-07-28 15:38 | 2026-08-04 21:51 | yes |
| 9.2.0.3925 | 1.557 | 4050 | 2026-08-04 21:52 | 2026-08-06 12:28 | yes |
| 9.2.0.3930 | 1.557 | 4050 | 2026-08-06 12:28 | 2026-08-09 15:21 | yes |
| 9.2.0.3931 | 1.557 | 4041 | 2026-08-09 15:22 | 2026-09-01 13:33 | yes |
| 9.3.0.3970 | 1.565 | 4050 | 2026-09-01 13:34 | 2026-09-06 15:15 | yes |
| 9.4.0.4015 | 1.570 | 4094 | 2026-09-06 15:16 | 2026-09-16 11:41 | yes |
| **9.5.0.4050 (KEPT)** | **1.573** | **4081** | **2026-09-16 11:41** | **2026-09-16 11:41** | **yes** |

**24 folders, 36.314 GB in total. The 23 to remove came to 34.741 GB.**

### Nothing still pointed at an old version

Checked before removing anything, because a folder vanishing under an application that tracks its
own installs is exactly how this goes wrong:

• `Configure.ini` `last_version` is empty, as above.
• A regular expression search for any old version string across `User Data\Config`, `MMKV`,
  `Migration`, `SettingsSDK`, `ComponentStore` and `Presets` returned **0 matching files**.
• A search of `User Data\Projects` for any path containing `AppData\Local\CapCut\Apps` returned
  **0 matching files**. No saved project pins a build.

---

## PART 1 — CAPCUT OFFERS NO WAY TO DO THIS, SO IT WAS DONE BY HAND

BL-909 said to do this from CapCut or the Store rather than by hand. That instruction was right to
give and it turns out not to be available here, so this section states plainly why, and what was
done instead.

### There is no Store path, because this is not the Store build

`Get-AppxPackage` returns **no package matching CapCut, Bytedance or lveditor**. This CapCut is a
per user desktop installer build: it lives under `AppData\Local`, registers under
`HKEY_CURRENT_USER\...\Uninstall\CapCut`, and ships its own `uninst.exe`. The Microsoft Store has no
entry to click for it and Settings, Apps, Installed apps will only offer the vendor uninstaller.

### There is no per version mechanism inside CapCut either

The only vendor removal tool present is `Apps\uninst.exe`, 3.93 MB, and its registry
`UninstallString` confirms it is the whole product uninstaller. It removes CapCut, not old copies of
it. Each version folder also contains `uninstshell.exe`, but that is the helper `uninst.exe` drives,
it is undocumented, and invoking it per version could plausibly deregister the product. It was not
used.

**What could not be checked, stated rather than implied:** CapCut's in application settings screens
were **not** inspected, because doing so means launching his video editor, and this round was run on
the explicit basis that nothing would happen under a live editor. So the honest position is that no
per version removal mechanism exists in the files CapCut ships, and whether a menu exists inside the
running application was not determined either way.

### What was done instead

The 23 superseded folders were removed **by explicit literal path, one at a time**. The script
contains all 23 paths written out in full and contains no wildcard of any kind. Before doing
anything it refuses to run if the keep version has no `CapCut.exe`, if any CapCut process is live,
or if the keep path appears anywhere in the target list. Free space was sampled before and after
each individual folder.

| Removed | GB freed | Removed | GB freed |
|---|---|---|---|
| 7.3.0.2974 | 1.656 | 8.9.1.3802 | 1.278 |
| 7.5.0.3053 | 1.463 | 9.0.0.3858 | 1.507 |
| 7.6.0.3123 | 1.467 | 9.1.0.3879 | 1.505 |
| 7.7.0.3143 | 1.474 | 9.2.0.3914 | 1.569 |
| 7.9.0.3294 | 1.486 | 9.2.0.3925 | 1.564 |
| 8.0.1.3366 | 1.496 | 9.2.0.3930 | 1.564 |
| 8.1.1.3417 | 1.495 | 9.2.0.3931 | 1.563 |
| 8.2.0.3462 | 1.498 | 9.3.0.3970 | 1.568 |
| 8.3.0.3497 | 1.499 | 9.4.0.4015 | 1.577 |
| 8.5.0.3590 | 1.509 | | |
| 8.6.0.3667 | 1.468 | | |
| 8.7.0.3685 | 1.486 | | |
| 8.8.0.3774 | 1.488 | | |
| 8.9.0.3794 | 1.494 | | |

**23 of 23 removed. 0 refused. 34.675 GB returned.**

### Verification that CapCut still works

What was checked, all after the removal:

• `Apps\9.5.0.4050` holds **4,081 files and 1.573 GB, identical to before**, to three decimals.
• All seven key executables present with non zero sizes: `CapCut.exe` 90,536 bytes,
  `VEHelper.exe` 3,524,520, `ffmpeg.exe` 473,512, `VECrashHandler.exe` 2,100,136,
  `uninstshell.exe` 665,512, `CapCut-DiffUpgrade.exe` 304,040, `hpatchz.exe` 449,448.
• The launcher chain resolves end to end: the Start Menu shortcut targets
  `Apps\CapCut.exe`, that stub is present, `ProductInfo.xml` is present and still reads
  `9.5.0.4050`, `Configure.ini` is present, `uninst.exe` is present.
• `Apps` now contains exactly **1** version folder plus those four files, and nothing else.
• The registry entry is still valid and still points at a file that exists.
• His data is untouched: `User Data\Projects` 2.693 GB in 5,502 files, `Videos` 4.766 GB in 9 files,
  `User Data\Config` 0.002 GB in 95 files, all unchanged.
• Updates still work. Each version ships `CapCut-DiffUpgrade.exe` and `hpatchz.exe`, which patch
  forward from the **currently installed** build. That build is the one that was kept, so the next
  differential update has its source.

**What was NOT verified, said plainly: CapCut was not launched, so this report does not claim it
starts.** Every file the launcher needs is present and correct, which is as far as a check can go
without opening his editor. If he wants certainty, opening CapCut once takes a few seconds.

### What he loses

**The ability to roll back to an older CapCut.** That is the entire cost and there is nothing hidden
behind it. If build 9.5.0.4050 turns out to have a bug that an earlier build did not, the earlier
build is no longer sitting on the disk to fall back to and he would have to download it. His
projects, presets, exports and settings are all in `User Data` and `Videos`, none of which was
touched.

---

## PART 2 — aTRAIN, REMOVED THROUGH THE PROPER STORE PATH

### What it was

`26987BusinessAnalyticsand.aTrain`, version 1.4.1.0, publisher CN=B4781B91-0034-4936-9923-AE1D76660B41,
installed from the Microsoft Store on 2026-02-03 and unchanged since. It transcribes audio to text
offline. BL-909 measured its payload at 8.94 GB and flagged it as the largest application he might
not recognise.

### Nothing depended on it. Checked, not assumed.

BL-909 named a whole class of things whose removal breaks other programs, Edge WebView2, the Windows
10 SDK, the Build Tools, the .NET Desktop Runtime and FFmpeg among them, so this was verified before
removal rather than reasoned about:

• `IsFramework = False`. It is an application package, not a runtime, so nothing can bind to it the
  way apps bind to WebView2.
• Every installed package's dependency list was enumerated and searched. **No installed package
  lists aTrain as a dependency.** Zero.
• aTrain's own dependency list is empty, so removing it strands no shared framework.
• No running process, no service, no scheduled task references it.
• `NonRemovable = False`, `SignatureKind = Store`, `Status = Ok`.

### The removal, and the rights question

**This session has no administrator rights** (`IsAdmin = False`), exactly as BL-909 recorded. That
did not block this, because aTrain was installed **for the current user**, and removing a per user
Store package does not require elevation. It is the same operation Settings, Apps, Installed apps
performs when you click Uninstall.

Command used, the supported Store uninstall path:

```
Remove-AppxPackage -Package 26987BusinessAnalyticsand.aTrain_1.4.1.0_x64__j0q0f918hn8dc
```

It returned without error. **Its WindowsApps folder was never deleted by hand**, which is what
leaves a broken registration behind.

### Verified clean afterwards

• `Get-AppxPackage` matching aTrain or BusinessAnalytics returns **0 packages**.
• `C:\Program Files\WindowsApps\26987BusinessAnalyticsand.aTrain_1.4.1.0_x64__j0q0f918hn8dc` is gone.
• `C:\Program Files\WindowsApps\Deleted` does not exist, so nothing is staged for later cleanup.
• `AppData\Local\Packages\26987BusinessAnalyticsand.aTrain_j0q0f918hn8dc` is gone.
• `ProgramData\Microsoft\Windows\AppRepository\Packages\...aTrain...` is gone.
• 0 leftover Start Menu shortcuts.

No click by hand was needed, so there is no "where to click" instruction to give. For reference, had
elevation been required, the path is Settings, Apps, Installed apps, search **aTrain**, the three
dot menu, Uninstall, and afterwards it should disappear from that list and from the Start menu.

---

## PART 3 — WHAT EACH ITEM ACTUALLY FREED

Measured as a real C: free space delta, never as a sum of file lengths, for the reason BL-909
documented: its OneDrive logs measured 64.36 GB by length and returned 16.51 GB because NTFS had
them compressed about 4 to 1, and its uv cache returned 3.12 of 3.74 GB because the remainder was
hardlinked into live virtualenvs.

| | GB |
|---|---|
| Free at the start of this round | 93.222 |
| Free after the CapCut removal | 127.850 |
| Free immediately after the aTrain command | 129.858 |
| **Free settled, two identical consecutive readings** | **136.858** |
| **Total returned by this round** | **43.636** |

| Item | BL-909 predicted | Actually returned | Verdict |
|---|---|---|---|
| CapCut, 23 superseded version folders | ~34.8 GB | **34.675 GB** | matched |
| aTrain | 8.94 GB | **8.961 GB** | matched |

Neither fell short. Nothing was refused. **0 failures across 23 folder removals and 1 package
uninstall.**

### One measurement that was nearly reported wrong, and the correction

The reading taken three seconds after `Remove-AppxPackage` returned showed only **1.999 GB**
recovered against a predicted 8.94, and the obvious explanation to reach for was compression, since
that is precisely what caught BL-909 out on the OneDrive logs. **That explanation would have been
wrong.** Later readings kept climbing, from 129.858 to 136.858, and settled there across two
identical consecutive samples. **The Store reclaims a package's disk space asynchronously after the
uninstall command returns.** The 3 second sample was simply taken too early. A compression probe of
a remaining WindowsApps package also came back at a ratio of 1.0 to 1, which rules compression out
directly rather than by inference.

Taking the settled figure, aTrain returned 8.961 GB against 8.94 predicted, an almost exact match.

### Nothing refused, and one false alarm in the verification

Every removal succeeded. The only line in this round that looked like a failure was in the PART 4
verification sweep, where `C:\hiberfil.sys` printed as ABSENT. **It is not absent.** `Test-Path`
cannot read it without administrator rights. Listing the volume root directly shows
`hiberfil.sys` still present at **9.56 GB**, last written 2026-09-16 15:27, and `powercfg /a`
confirms hibernate is still enabled. `pagefile.sys` is likewise still present at 28 GB. Neither was
touched, and neither was ever in scope.

---

## PART 4 — NOTHING ELSE MOVED

| Path | Before (BL-909) | After (now) | Verdict |
|---|---|---|---|
| `Desktop\clipper finder` | 74.94 GB, 152,897 files | 74.94 GB, 152,897 files | identical |
| `Desktop\twitch clipper` | 13.22 GB, 118,816 files | 13.22 GB, 118,816 files | identical |
| `Desktop\ceo-dashboard` | 2.07 GB, 45,596 files | 2.07 GB, 45,596 files | identical |
| `Desktop\ClippersHQ` | 1.95 GB, 77,039 files | 1.95 GB, 77,039 files | identical |
| `Desktop\Random` | 3.81 GB, 40,936 files | 3.81 GB, 40,936 files | identical |
| `twitch-clipper\library` | 24.13 GB, 7,673 files | 24.13 GB, 7,673 files | identical |
| `C:\ClippersHQ_renders` | 8.74 GB, 17,646 files | 8.74 GB, 17,646 files | identical |
| `Downloads` | 22.50 GB, 3,898 files | 22.50 GB, 3,898 files | identical |
| `AppData\Local\wsl` | 3.86 GB, 2 files | 3.86 GB, 2 files | identical |
| `Program Files\Docker` | 4.08 GB, 204 files | 4.08 GB, 204 files | identical |
| `Programs\Ollama` | 2.74 GB, 980 files | 2.74 GB, 980 files | identical |
| `Roaming\.minecraft` | 1.79 GB, 10,597 files | 1.79 GB, 10,597 files | identical |
| `.cache\huggingface` | 4.65 GB, 67 files | 4.65 GB, 67 files | identical |
| `$Recycle.Bin` | 0.69 GB, 176 files | 0.69 GB, 176 files | identical |
| `hiberfil.sys` | 9.56 GB | 9.56 GB | identical |
| `pagefile.sys` | 28.00 GB | 28.00 GB | identical |

### Two rows that changed, and neither was this round

Reported rather than glossed over, because a verification that only reports matches is not a
verification:

• **`Desktop` as a whole: 498.14 GB / 609,909 files, now 499.01 GB / 610,335 files.** Up 0.87 GB and
  426 files. Inside it, `editing content` went from 383.96 GB / 12,266 files to 383.97 GB / 12,364
  files, and `neuraltrack` from 13.21 GB / 143,164 files to 13.92 GB / 143,324 files. That is the
  owner adding footage and an active project writing files in the day between the two rounds. The
  Desktop **grew**; nothing on it was removed, and nothing on it was opened by this round.
• **Chrome `User Data`: 27.67 GB / 213,044 files, now 27.65 GB / 212,531 files.** Chrome's own cache
  eviction while it runs. No Chrome profile was touched.

No repository, no database and no project code was touched. **No build was run and none is claimed**;
this is a disk round.

### Where the disk stands now

| | GB |
|---|---|
| Free now | **136.86** |
| Used | 793.63 |
| Disk total | 931.5 |

### What the DECIDE list is still worth

Recomputed fresh rather than carried over, since BL-911 has now taken two items out of it. Excluding
the footage and everything on the Desktop, which remain off limits, the remaining DECIDE items total
about **127 GB**, the largest being the twitch clipper library 24.13, Downloads 22.50, Claude
`vm_bundles` 9.12, `ClippersHQ_renders` 8.74, the OneDrive `ListSync` thumbnail database 7.42,
CapCut `User Data` 6.32 of which 2.32 is clearable cache, CapCut `Videos` 4.77, huggingface 4.65,
`AppData\Local\ClippersHQ` 4.41, Docker 4.08 and the WSL image 3.86. A further 9.56 GB sits in
`hiberfil.sys`, which needs administrator rights and costs him hibernate.

For the record, BL-909 put that same figure at about 105 GB. Recomputing it line by line gives 127.
BL-909 undercounted it, in the same way it miscounted the CapCut folders as 25.

---

## THE ONE THING THAT ACTUALLY SOLVES HIS PROBLEM

Said once, plainly, and **not acted on**.

These two items were worth 43.6 GB against the roughly 405 GB he was short. Even taking every
remaining item on the DECIDE list would add only about 127 GB more and would cost him Docker, the
WSL image, his Downloads and the twitch clipper library.

**His `editing content` folder is already inside OneDrive. Right clicking it and choosing Free up
space returns 383.96 GB with no hardware to buy.** The cost is real and he should weigh it: every
clip re-downloads the moment he opens it in an editor, which is painful when scrubbing large `.mov`
files, and his OneDrive quota has to actually hold 384 GB, so he should check that first. BL-909's
recommendation stands, and it is the sensible shape: do it for the sports folders he is not
currently cutting, such as Tennis, Motorsport and American Sports, and keep Football and Combat
Sports local. The alternative that avoids the re-download entirely is a 1 TB external SSD.

Nothing in this round acted on that, and nothing should until he decides.
