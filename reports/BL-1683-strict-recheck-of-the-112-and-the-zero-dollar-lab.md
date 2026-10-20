# BL-1683 -- strict re-check of the 112, the Spanish rule, and a $0 lab plan

Orders (Dusan's HELM chat 20 Oct 19:47 and 19:56, relayed by ALFRED): reject Spanish pages and add the no-business /
no-creator / no-streamer rules to every check; take the 4 bad accounts he found off the 112 sheet and re-check all 112
for the same kinds; go back to the lab and bring one short plan with the cost per good editor, testing only with $0.
**Money: $0.** No vendor call was made.

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

## Next ($0, Claude only)

The other 1,180 rows of "New emails - never sent" passed the same softer check, so expect a similar share of bad pages.
Re-check them with STRICT83 (Opus; a Sonnet K is not trusted, BL-1677) and move rejects to its Removed tab.

## Files

- `scratch/bl1683/STRICT83.md` rubric; `merge83.py` (two readers + caption check + third look -> `remove112.json`);
  `rm112.py` (live sheet -> Removed tab, read back); `spanish83.py` (captions); `lab83.py` (strict good per niche / tag / page).
- Work data (private, not in git): `%LOCALAPPDATA%\ClippersHQ\bl1683_work\` (strict answers, review, final.json).
