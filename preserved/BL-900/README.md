# preserved/BL-900 — the few megabytes that were holding 19 GB hostage

`BL-900-unique-files.tar.gz` holds every file BL-900 found in the 13 leftover directories at the
C: root that exists in **no git repository on this machine**, checked by blob OID against eight
object stores: ClippersHQ, twitch clipper, ClippersHQ-Deck-2026, ceo-dashboard, clipper finder,
insta outreach, neuraltrack and clippershq-reports itself.

**3,106 files, 23.04 MB compressed, 62.54 MB raw.** Paths are preserved, so any file can be put
back exactly where it came from: an entry `C/mbwt/clipnet/x.py` was `C:\mbwt\clipnet\x.py`, and an
entry under `zip-contents/` was inside the zip archive its path names.

`BL-900-unique-files.manifest.tsv` lists every entry with its original path, byte size and
LF blob OID, so a later round can re-verify without unpacking.

## What is NOT in here, and where it is instead

**30 files were excluded by the secret and personal data scan** and were never pushed anywhere.
They remain exactly where they were on disk, untouched and undeleted:

| what | where it stays |
|---|---|
| 4 copies of `master_leads.csv` carrying 9,784 to 10,136 email addresses each, plus api key, Resend key and wallet address pattern matches | `C:\BL1279_HANDOVER_TEST\`, `C:\BL1301_UPDATE_TEST\` |
| `master_leads_delta.csv`, 352 email addresses | `C:\BL1301_UPDATE_TEST\LEADS_UPDATE_2026-08-15\data\` |
| 18 `spotify_finder` source files carrying 7 to 76 email addresses each in fixtures and policy lists | the three `*_HANDOVER_TEST` directories |
| `bl882-prompt.txt`, which contains an Auth.js session token | `C:\tmp\` |
| 6 files matching the wallet address pattern, all of which look like false positives on base58 style hashes (`package-lock.json` integrity strings, OCR report tokens) | `C:\mbwt\`, `C:\projects1\` |

**The two data backups the owner asked to keep are not in here either.** They were never at risk:
`bl1235_backup\` and `songs.json.backup_20260812_160748` sit where they always have inside
`C:\ClippersHQ_renders\`, they are tracked in the **clipper finder** repository already, and
BL-900 additionally placed a sha256 verified copy at `Desktop\BL900-preserved-backups\`. They are
kept out of this archive because `output_ALL_BOT_READY.csv` carries 3,972 email addresses.

## Is a reports repository the right home for this

**No, and it is worth saying so plainly.** Most of what is in this archive belongs to other
projects: `spotify_finder` is outreach tooling, `mbwt` is the meme render OCR evidence, `wt` and
`temp` are twitch clipper scratch. A report log is not their home, and every round that clones
this repository now pays 23 MB for them.

It is here because the alternatives were worse. Creating a new repository is an outward facing
action nobody authorised, and pushing another project's source into that project's own repository
changes it without being asked. One compressed file under `preserved/` keeps the tree clean and
is removed with a single `git rm`.

**The recommendation:** move this into a dedicated `clippershq-attic` repository, or split it back
to `clipper finder` and `twitch clipper`, and delete it from here once that is done.
