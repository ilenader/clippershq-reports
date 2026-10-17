# BL-1666 -- Instagram public phone saved from the profile call we already pay for; TikTok has no hidden contact field

Order: office 1_LEADS 2026-10-17_1428 (ALFRED for Dusan, HELM chat 14:28): on every Instagram profile we pay for, also
save public_phone_number + its country code (same call, no extra cost), show it next to the email, keep public_email
as the top contact; check whether TikTok has an email/contact field we miss. **Spent: $0** (code + 8 free page reads).

## What changed
- `clippershq/ig_discovery.py`: the profile parser reads `public_phone_number` / `contact_phone_number` (top level or
  under `user`) next to the country code it already read, and returns `phone` = "+<code> <number>" (number alone
  without a code, "" when none). Same response, no new request.
- `clippershq/main.py`: where the IG profile's link is merged into the lead, `phone` is copied too (only if empty).
  The email logic is untouched; public_email stays first.
- `clippershq/writer.py`: `phone` appended LAST to FULL_COLUMNS (old masters migrate by name, no column moves); in the
  review sheet it sits right after `email`. Only a value shaped like a phone skips the formula-injection apostrophe;
  anything else from that public field is still sanitized.
- `tools/deliver_workbook.py`: his workbook's Emails sheet gets a "Phone" header at the END (never inserted beside
  Email, which would shift his columns), created only when a new row has a phone; only phone-shaped values are written.
- Tests: `tests/test_ig_phone.py` (11, new) + `tests/test_bl1592_buttons_and_rank.py` (rank_score keeps its index,
  phone is now last): 22/22 OK; `writer.py --selftest` ALL PASS. Full suite not run (shared runner).

Today no Instagram profile calls run (all lead runs are TikTok), so the first phones arrive with the next IG run.

## TikTok: is there a contact field we miss?
- Hashtag-feed author objects (what the paid walk buys) carry only the bio (`signature`) -- no link, no email field.
- The logged-out web profile (`webapp.user-detail`, 8 business pages read free) has only `bioLink` and
  `commerceUserInfo` (a business flag) -- **no email or phone field**; the business "Email" button is not exposed.
- App-API user objects (search results) also carry the linked Instagram id (`ins_id`) and YouTube channel -- a
  pointer to the IG business email, which is the IG route above, not a TikTok email.
