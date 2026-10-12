# BL-1618: no transfer -- this PC stays the main PC, and the friend reviews through a private Tailscale link

**Written after the fact by BL-1634 (3 FIXER housekeeping, 2026-10-12).** BL-1618 committed its work on 2026-10-09 but
never wrote a report. Everything below comes from what is on disk: commit `c383622e` (the code), commit `046f541d`
(its claims manifest `docs/claims/BL-1618.claims`, which re-verifies at HEAD today as **ALL CLAIMS VERIFIED**), and its
scratch scripts in `scratch/bl1618/`. Nothing was re-measured. The live link that came after it is in BL-1620's report.
$0 vendor spend.

## Card

| | |
|---|---|
| **Decision** | **No move to a new PC.** His PC stays the main PC. The friend uses the app over a private Tailscale link instead. |
| **How the friend gets in** | `tailscale serve` (tailnet only, **never Funnel**) points to `127.0.0.1:8794`, the share listener only. The friend is identified by the Tailscale login header that Serve adds. A listed login gets the **friend** role, never owner. An unknown login, a Funnel request, or access switched off gets **403** on everything. |
| **Two kinds of friend** | A **final** friend's YES and NO count like the owner's. An opinion-only friend's NO deletes nothing: it is logged as `FRIEND_NO`, and the video leaves only that friend's own queue. |
| **Server stays up** | The server no longer idles out while friend access is on. |
| **Auto-start** | One HKCU Run value, which starts the server only (`tools/edits_autostart.py`). |
| **CLI** | `tools/edits.py share friend ...` and `share tailscale ...`. Neither prints a login. |
| **Texts** | The Approve videos texts are worded for each kind of reviewer. Accessibility was reviewed before and after. |
| **Tests** | `tests/test_bl1618_friend_tailscale.py`: **27 new checks** (commit message). |
| **Disk** | Every file of the old portable folder was found in Drive or the live app. Before that, the **66 old files** not found elsewhere were backed up to Drive. Agents are blocked from deleting `D:\ClippersHQ_portable`, so he deletes it himself. `review_floor_gb` 25 → 10. 2 real downloads OK. |
| **Left open at the time** | Tailscale on this PC was stuck in NoState (never signed in), so serve and the real-tailnet test had to wait for him. **Closed later by BL-1620:** the link went live and the real-Tailscale test passed as the friend. |

## Sources on disk

- `git show c383622e`: 13 files. `clippershq/edits_share.py`, `edits_review.py`, `edits_swipe_server.py`, `edits_app.js`, `edits_i18n.json`, `tools/edits.py`, `tools/edits_autostart.py`, the test file, and 5 scratch scripts (`backup_leftovers.py`, `friend_browser_test.py`, `portable_cover.py`, `space_audit.py`, `ts_check.py`).
- `docs/claims/BL-1618.claims`: verified at HEAD on 2026-10-12 by `tools/verify_claims.py`.
- The BL-1620 commit message: "BL-1618 claim released (its work was committed)".
