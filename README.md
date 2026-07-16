# clippershq-reports

Build reports from the automated agents that work on ClippersHQ, published here so they can be read directly by URL. Each round of work (a ticket like BL-546) produces one report describing what was investigated or changed, what evidence was gathered, and what was deliberately left alone. Reports live at `reports/<TICKET>.md` and are readable raw at `https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/<TICKET>.md`. This repository is public by design, because the tools that need to read these reports cannot fetch from private hosts or from GitHub gists. It contains reports only: no source code, no configuration, and no credentials of any kind. Every report is scanned for secrets before it is published, and anything sensitive is removed at that point rather than committed and rotated later.

## Reading a report

| Ticket | Report |
|---|---|
| BL-546 | [reports/BL-546.md](reports/BL-546.md) |

## Pattern

* Path: `reports/<TICKET>.md`
* Raw URL: `https://raw.githubusercontent.com/ilenader/clippershq-reports/main/reports/<TICKET>.md`
