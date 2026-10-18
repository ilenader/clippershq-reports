# BL-1672 -- a cheaper route to strict-faceless editor emails: re-walk the tags that already gave faceless editors

Order: office 1_LEADS 2026-10-18_1332 (ALFRED for Dusan, HELM 13:32): no to $106 per 1,000; find a way to >= 1,000
strict-faceless editor emails for <= $30 ($0.03 each), honest counts, free routes first, prove the price on the smallest
sample, then ONE money question. **Spent: $0.2052** (LamaTok counter 138,162 -> 137,820; money_guard booked $0.30 on
"Finder leads 18 Oct" first). Counts only -- no handle, name or email here.

## Result in one line
**Update 20:00 (A7 step A1, 100 tags, $0.83): 14 faceless = $59 per 1,000 -- the probe price did not hold; stop rule tripped, see section 5.**

One route reached the price on a small sample: re-walking 30 tags that gave >= 2 faceless editors 3+ days earlier found
**7 new strict-faceless editors (Opus F) for $0.205 = $29 per 1,000** (7 is a small count: plausible range ~$14-73 per 1,000).
But its pool is small: ~330 such tags -> ~70-80 faceless per round. **1,000 for $30 in one go is not available**; 1,000
needs about 6-8 weekly re-walk rounds of this pool plus the one-hit tags, at an estimated $30-50 per 1,000 overall.

## 1. What the old runs say ($0)
- Old lists after the strict check: 2,295 faceless of 3,680 pages the old eyes called EDITOR (walks ~$55).
- By tag type: bare named tags 3.0 % of email pages are faceless, edit-word tags 11.5 % -- but edit tags carry an email
  on few pages, so both come out at ~$40 per 1,000. Today's fresh named tags: $106 per 1,000 (BL-1670).
- v1 tag feeds end after ~6 pages (~160 videos, "has_more false"): depth cannot be bought on v1; v2 goes deeper but
  repeats authors. Vendor price ($0.0006/call, ~28 videos) is already the lowest found (BL-1665 web research).
- Hindsight price per tag ("1,201 tags under $15") is selection on the outcome, not a forecast -- not used.

## 2. Free routes ($0) -- closed
- **Re-check old pages the first look called CREATOR / UNSURE** (53,464 + 969 pages, already paid, with emails):
  Opus strict look on 56 random sheets (448 pages): every F fell on pages already called EDITOR (already listed);
  **0 F on ~400 old CREATOR/UNSURE pages**. Dead. (Sonnet first look also under-calls F: Opus found 8 where Sonnet had 3.)
- **Urlebird** (free TikTok mirror, no wall for bios): a tag page lists ~12 authors behind a signed "load more"; every bio
  is one more page (~2 s). At edit-tag email rates 1,000 faceless = hundreds of hours. Too slow; also his call (third-party site).
- **Business-email field**: the vendor's TikTok feeds carry no contact email field (has_email / bind_phone always empty);
  LamaTok's spec has no email field on any of its 29 paths.
- Collab partners of faceless editors: 2,950 distinct, most already read (BL-1669/1670: 368 new emails from 9,905 reads,
  still waiting for a face check). One-off pool, cannot reach 1,000.

## 3. The probe ($0.2052)
- 30 tags drawn AT RANDOM (seed 72) from the 203 tags that gave >= 2 strict-faceless editors and were last walked <= 15 Oct.
- Walk: raw_emails.py walk with its **own tag ledger** (bl1672_work\ledger72.json -- the global ledger marks every tag
  "walked once, never again", so the first try walked 0 tags and spent $0). 37 tag walks (30 v1 + 7 v2 follow-ups),
  249 pages, **115 new addresses** (not in master, his workbook, any operator file or the edit app).
- Processing (process70: filter, feeds, covers, sheets): 91 email pages on 12 sheets.
- Eyes: Sonnet first look 3 F / 8 U; Opus strict look on all 12 sheets: **7 F**, 73 C, 3 B, 3 X, 5 U.
  All 7 Opus F were on sheets Sonnet had marked F or U -> the ROUTER pipeline (Sonnet, then Opus on F/U sheets) loses none here.
- 7 F came from 6 of the 30 tags. Price **$0.0068 per tag re-walk; 0.23 faceless per tag; $29 per 1,000**.
- Delivered: operator\rewalk_EDITORS_20261018_p2.xlsx (+ first-world split), same close-out as BL-1670 (opus70 + fin70).

## 4. What 1,000 would take (estimate, not measured)
| step | tags | cost | expected faceless |
|---|---|---|---|
| A: other tags with >= 2 faceless (walked <= 16 Oct) | ~300 | ~$2.10 | ~70 (30-140) |
| B: tags with 1 faceless (only if A holds <= $30/1k) | ~920 | ~$6.30 | unknown, likely fewer per tag |
| weekly repeat of A+B (new videos: ~1/3 of a feed is < 7 days old) | ~1,220 | ~$8.40 / round | ~100-170 / round (guess) |
Stop rule per step: after the first 100 tags, stop when the price passes $45 per 1,000.

## 5. A7 step A1, measured (Dusan's yes 19:24; $0.8304)
- 100 best of the 302 tags with >= 2 faceless (bl1672_work\a72_1.tsv), own ledger, chain72.py; money_guard booked $0.85
  on "Finder leads 18 Oct". LamaTok counter 137,811 -> 136,427: walk 999 pages $0.5994 + 385 feeds $0.231 = **$0.8304**.
- 509 new addresses -> 385 email pages kept by the filter -> 49 sheets. Sonnet first look on all 49; Opus strict look on
  the 26 sheets where Sonnet left an F or U: **14 F** (13 first world), 0 F outside them by construction.
- **$59 per 1,000 faceless** (first world $64). The probe's $29 did not hold on the bigger set: 0.14 faceless per tag
  (probe 0.23), 3.6 % of email pages faceless (probe 7.7 %). The probe was 30 tags; 7 F was the small-count luck its
  range ($14-73) allowed.
- Stop rule (> $45 per 1,000 after the first 100 tags) tripped -> A2 (202 tags) and B (919 one-hit tags) NOT walked.
  A7 total: probe + A1 = 21 faceless for $1.04 ($50 per 1,000). $7.36 of the $8.40 A7 cap unspent.
- Delivered: operator\rewalk_EDITORS_20261018_a1.xlsx (14) + editors_rewalk_20261018_firstworld_a1.xlsx (13).
- **Answer to "1,000 for $30":** not reachable with strict-faceless on any route measured ($29 on 30 tags -> $59 on 100,
  BL-1670 $106, BL-1630 $62). At $59 per 1,000, $30 buys ~500; 1,000 would cost ~$60 and needs more pool than
  A2 + B hold (~1,100 tags x 0.1 = ~110 more). Even with feeds free the walk alone is $43 per 1,000.

## Files
scratch/bl1672/: chain72.py (A7 chunk runner, own ledger), hist72.py (price per old run), tags72.py (per-tag faceless density), partners72.py, samplec72.py /
sampleu72.py (blind re-look samples), pool72.py (old-page pool + Opus join). Work data: %LOCALAPPDATA%\ClippersHQ\bl1672_work
(probe72_tags.tsv, ledger72.json, run_p2.sh, money72.txt, opus/sonnet answers), raw_emails\b72_p2.
