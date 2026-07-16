# clippershq-reports

Build reports from the automated agents that work on ClippersHQ, published here so they can be read directly by URL. Each round of work (a ticket like BL-546) produces one report describing what was investigated or changed, what evidence was gathered, and what was deliberately left alone. Reports live at `reports/<TICKET>.md` and are readable raw at `https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/<TICKET>.md`. This repository is public by design, because the tools that need to read these reports cannot fetch from private hosts or from GitHub gists. It contains reports only: no source code, no configuration, and no credentials of any kind. Every report is scanned for secrets before it is published, and anything sensitive is removed at that point rather than committed and rotated later.

## The convention (default for every future round)

**Every agent report is published to `reports/<TICKET>.md` on `main` in this repository. Gists are not used.** A secret gist is readable by a human with the link but returns nothing useful to an automated reader, so a report parked in a gist is effectively unreadable by the assistants that most need it, and the work it describes gets re-derived from scratch by the next round. Publishing here fixes that: a raw URL fetches anonymously, with no authentication, and returns the report text. So the final step of a round is to write the report to `reports/<TICKET>.md`, commit it to `main`, and print the raw URL. The trade for that readability is that this repository is world-readable and GitHub indexes it, which is an accepted decision by the owner: money figures, campaign names, and clipper usernames may appear in these reports and are deliberately not stripped. **Credentials are the one hard line.** No API key, token, password, or connection string may ever be committed here. Any secret found in a draft report is removed before publishing AND reported to the owner as compromised and needing rotation, because a key that reached a report has already been handled carelessly enough to assume it leaked.

## Reading a report

| Ticket | Subject | Report |
|---|---|---|
| BL-549 | Deploy truth: LamaTok is not dark, the ledger mislabels it | [reports/BL-549.md](reports/BL-549.md) |
| BL-547 | Scraper ledger truth: BL-543 merged locally but never pushed | [reports/BL-547.md](reports/BL-547.md) |
| BL-546 | Merge BL-543 (the ~$45/month saving) plus four audit docs | [reports/BL-546.md](reports/BL-546.md) |
| BL-545 | HikerAPI failure audit: 83% of failures are correct refusals | [reports/BL-545.md](reports/BL-545.md) |
| BL-544 | Scraper migration plan: HikerAPI is already primary for IG | [reports/BL-544.md](reports/BL-544.md) |
| BL-541 | isOwnerOverride root-cause fix (money deliberately not written) | [reports/BL-541.md](reports/BL-541.md) |
| BL-540 | Apify cost audit and TikHub migration design | [reports/BL-540.md](reports/BL-540.md) |
| BL-539 | Owner override share audit: isOwnerOverride cost $332.76 | [reports/BL-539.md](reports/BL-539.md) |
| BL-538 | The Pause and Freeze undo | [reports/BL-538.md](reports/BL-538.md) |

## Pattern

* Path: `reports/<TICKET>.md`
* Raw URL: `https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/<TICKET>.md`
