# BL-1578 — No results file exists yet: the grades are in his browser, not on disk

**Round:** BL-1578 · **Read-only.** · **Spent: $0.00** — `spend.json` sha256 `4edc0802cd…` /
16,043,805 bytes at start and at close, byte-identical; no vendor call; no store written; no
suite run. · Paths redacted: `<PROFILE>` is the user folder.

## The paragraph

**There is no results file, so there is nothing to analyse, and this round stops there.** The
review page is on the Desktop the shell names (the OneDrive one), 36,734 bytes, written
2026-09-18, with 100 cards (50 TikTok, 50 Instagram). Its grading buttons are **two — EDITOR and
NOT AN EDITOR** — plus "Download results" and "← back"; every press is saved to `localStorage`
under one key (`load()`/`save()` at lines 67–69 of the page), which lives in his browser
profile, not on disk. The file "Download results" would write, `bl1572_review_results.csv`, exists
**nowhere**: not on the OneDrive Desktop, not on the plain profile Desktop (the two places files
have gone unseen before), not in Downloads, Documents or the `Random/` folder. So what he graded,
how clean the survivors are, and whether Instagram is dead or just different **cannot be said
today** — he has to press "Download results" first. Nothing was reconstructed, nothing was graded
here, and nothing was read from browser storage.

## 1. What this project is, for a reader with no context

ClippersHQ finds video editors on TikTok and Instagram and delivers their addresses to one
operator. BL-1572 built a review page of 100 accounts that survived the craft cut — 50 per
platform — for him to grade by hand. Those grades would be the first real evidence of the cut's
false-pass rate and the first Instagram evidence of any kind (the cut's 247 labels contain zero
Instagram rows). This round was to read them.

## 2. Inventory of the Desktop (project-relevant files only)

| file | bytes | mtime | what |
|---|---|---|---|
| `clipper_review_100.html` | 36,734 | 2026-09-18 | the review page: 100 cards, two grade buttons, saves to `localStorage`, downloads `bl1572_review_results.csv` |
| `BL-1576_never_delivered_581.xlsx` | 68,236 | 2026-09-20 | the 581 never-delivered addresses (BL-1576); not a grading output |
| `BL-1563_TikTok_emails_good_only.xlsx` | 10,469 | 2026-09-20 | an earlier delivery sheet; not a grading output |
| `bl1572_review_results.csv` | — | — | **does not exist** (OneDrive Desktop, profile Desktop, Downloads, Documents, `Random/` all searched) |

Older `review_marks*.jsonl` files sit in Downloads from August (BL-1196 / BL-1207 packs); they
predate this page and are not its output.

## 3. Why the page's own storage was not read

`localStorage` is per browser profile and per origin; reading it means opening his browser
profile, which this project's rules forbid (never drive the real profile). The brief is explicit
and right: a measured refusal beats a reconstruction. The zero here is **untestable from disk**,
not false — the file simply has not been produced.

## 4. What the grades will settle when they exist

With 50 per platform: a false-pass rate per platform with a Wilson interval about ±12–14 points
wide at the extremes and wider in the middle; whether the two platforms' intervals overlap; and
the grouped "why" text — but **not recall**: the sample is drawn from what survived the cut, so
it cannot say how many real editors the cut removed.

## 5. Assertions at close

```
master_leads.csv 74,218 x 75 · workbook Emails 3,028 rows, MARK non-empty 0 · spend.json 4edc0802cd… / 16,043,805 bytes == start
```

## 6. What BL-1579 should do

Wait for `bl1572_review_results.csv` on the Desktop, then run the analysis this round was
written for; if the file is still absent, ask him to press "Download results" and stop again.

## 7. Scope check

Nothing built, nothing graded, nothing reconstructed, nothing written.

## 8. What I got wrong

- While reading the page's source for its grade vocabulary, one grep printed a card's data
  field — an address — into this session's tool output. It went nowhere else (not to a file,
  not to this report, not to the commit), and the later greps masked addresses; the lesson is
  that the page's data block must be read with the mask on from the first command.
- **Leak scan of this report:** both corpora, detectors proven on planted `.invalid` controls;
  0 leaks, 0 C0 bytes, asserted before writing.
