# BL-1683 -- strict re-check of the 112, the Spanish rule, and a $0 lab plan

Orders (Dusan's HELM chat 20 Oct 19:47 and 19:56, relayed by ALFRED): reject Spanish pages and add the no-business /
no-creator / no-streamer rules to every check; take the 4 bad accounts he found off the 112 sheet and re-check all 112
for the same kinds; go back to the lab and bring one short plan with the cost per good editor, testing only with $0.
**Money: $0.1992** (plan A, section 9); everything else $0.

| | Result |
|---|---|
| **1. The 112, re-checked strictly** | **46 kept, 66 moved** to the sheet's Removed tab with a reason (nothing deleted): 21 not an edit page (fan archive, news, memes, trivia, reposts), 13 creator / streamer / YouTuber, 12 business / shop, 8 Spanish, 12 too little on the page to confirm. All 4 accounts Dusan named were caught by both readers. |
| **2. How** | Two blind Opus readers judged every page picture (bio + up to 12 covers) with one strict rubric (`scratch/bl1683/STRICT83.md`), the second in a shuffled order with new ids. They agreed keep/remove on **97 of 110** pages; I looked at the 13 splits myself and overrode 2 agreed rejects whose only reason was "DM for promo" (faceless edit pages that sell promo slots are editors, not businesses). |
| **3. Live sheets** | 112 sheet read back: Editors 46, Removed 66, 0 rejects left in Editors, anyone-link opens (`chk112.py`). The same 66 moved out of "New emails - never sent" too (push: 0 added, 66 moved, 1,180 rows left). |
| **4. Spanish rule** | LESSONS 70/71; code L in RUBRIC77 / face RUBRIC / eyes70 / eyes77 / chk77 / celeb77 / merge77; captions by `spanish83.py` ($0, stored captions). On the 112 the caption check and the eyes agreed on all 11 Spanish pages. |
| **5. True price of the $10 tests** | **46 good for $5.21 = $113 per 1,000** (was $46.5 under the older check). T5 Instagram e-mail of known editors 13/13 = **$48/1k**; T3 re-walk of fresh tags 22/39 = **$65/1k**; T1 6/36 = $284/1k; T4 refill 2/17 = $418/1k; T2 1/5. |
| **6. $0 lab findings** | Strict-good editors come **1-2 per hashtag at most**, from every page depth: tag picking or shallower walks cannot cut the price. Movie tags cost ~3x football. TikTok profiles carry no hidden business e-mail (BL-1268). 34% of the Instagram accounts named in our editors' bios use **exactly** the TikTok handle (+9% near-same), so the T5 route can be extended by guessing. The 368 free partner e-mails (BL-1670) include 96 verified stars / clubs and have no stored picture, so they cannot be judged at $0. |
| **7. Plan sent to Dusan** | A: $0.20 pictures of the 272 non-verified partner accounts -> strict check, expect ~$5-15/1k, one-off pool. B: $0.35 probe then up to $3.40, Instagram same-handle lookup for the 4,870 no-email editors whose videos he approved, expect ~$50/1k, stop above $60/1k. C: no more TikTok hashtag walks ($65-140/1k under the strict rules). Nothing runs until his yes. |

## Why the old check passed them

The 112 had passed a Sonnet first look and an Opus look with RUBRIC77 (K = sports / movie / TV edit page). The four pages
Dusan named are obvious on the picture (a face-cam on every cover; "Check out my items in the TikTok Shop"; a crowd-filmed
concert archive), so the miss was the rubric's bar, not the picture: "mostly K expected" invited K. The strict rubric says
the opposite ("an earlier check passed everything and Dusan found that was wrong; when in doubt it is NOT K") and names
the reject kinds with examples. It also over-reads "DM for promo" as a business, which is why a third look is part of it.

## 8. The never-sent sheet, re-checked the same way ($0, 22:02)

The other rows of "New emails - never sent" had passed the same softer check. 1,056 of its 1,180 rows have a stored page
picture (BL-1670 pics); each was read by an Opus reader and a Sonnet reader (STRICT83, now with a "NOT reasons to reject"
block: promo lines, non-Spanish languages, TV dramas). They agreed on 875 pages (83%); the 181 splits went to a third Opus
look. **Kept 614, moved 442** to the sheet's Removed tab: 128 not an edit page, 106 business / shop, 99 Spanish, 26 creator /
streamer, 83 too little to confirm. Push read back: Editors 738 rows (614 + the 46 + 78 rows with no stored picture, still
unchecked), Removed 791. Calibration first: Sonnet alone on the settled 110 caught 63 of 66 rejects but wrongly rejected 11
of 44 keepers (Portuguese read as Spanish, "DM for promo" read as business), which is why it never decides alone.

## 9. Plan A run (Dusan HELM 20 Oct 22:10 "yes", hard cap $0.20)

**34 good editors, 46 new e-mails for $0.1992 = $5.90 per 1,000 good editors** (LamaTok counter 129,140 -> 128,808 =
332 calls). Input: the 271 still-new, public, non-verified accounts that proven editors tag (BL-1669/1670 free read).
Each needs 2 calls (user_by_username for the secUid + one `/v2/user/medias/by/secUid` page), so the cap bought 166
(edit-word accounts first, then most-tagged); my plan had priced 1 call. Covers from the CDN ($0), 165 page pictures,
STRICT83 Opus + Sonnet blind (159 agree), 6 splits by my own look. Codes: K 34, C 78 (mostly the stars being edited), F 30,
B 13, U 9, L 1. 28 of the 34 sat in the first 56 (edit words); after those only 6 of 109 -- the 105 not bought would run
~5% good. Delivered: `operator/editors_partners83_20261020.xlsx` -> "New emails - never sent" (+46, 784 rows).
The route is cheap but small; it grows only by reading the tagged accounts of new good editors (free, slow; a farm-PC job).

## Next

The 78 never-sent rows without a stored picture need covers (1 paid call each, ~$0.05) before they can be checked.

## Files

- `scratch/bl1683/STRICT83.md` rubric; `merge83.py` (two readers + caption check + third look -> `remove112.json`);
  `rm112.py` (live sheet -> Removed tab, read back); `mergens83.py` (never-sent sheet: Opus + Sonnet + tie-break -> new_emails_removed.json; NS83=pa for plan A); `partpages83.py` (plan A paid pages, cap guard); `deliver83.py` (plan A K -> lead file); `spanish83.py` (captions); `lab83.py` (strict good per niche / tag / page).
- Work data (private, not in git): `%LOCALAPPDATA%\ClippersHQ\bl1683_work\` (strict answers, review, final.json).
