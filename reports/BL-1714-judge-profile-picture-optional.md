# BL-1714 -- the AI judge can now be given the profile picture (OFF until HQ opts in)

Order: Dusan 25 Oct 10:17 -- give the judge the profile picture, several post pictures, name and caption.
Already sent before this change: name, caption (up to 12 verbatim), bio, followers (facts_block) and the contact sheet of many covers. Only the profile picture was missing.

Change (clippershq/free_judge.py, _messages): if `facts["profile_pic"]` is a readable image file, the prompt gets one small image (240 px) labelled "the page's PROFILE PICTURE" just before the contact sheet. No key in `facts` or an unreadable file = the prompt is byte-identical to before (tested), so nothing changes until a caller opts in.
Test: tests/test_bl1714_profile_pic.py (3 tests, pass). Free-judge tests that run without data: 14 + more pass, 2 skipped.
NOT done / needs HQ: (1) the funnel must save the profile picture and put its path in `facts`; (2) the free_judge file records that prompt changes killed wanted pages before, so run the labelled set with and without the picture and ship it on only if wanted-killed does not rise.
