# BL-1733 -- JARVIS try-out: what ran, what did not (29 Oct, 3090)
Idea 2 (link-in-bio reading), code only: enrich_links.extract_from_html read mailto and __NEXT_DATA__ / mail_to JSON but NOT Cloudflare data-cfemail.
Fixed: _decode_cfemail (XOR) + append to the page before every email pass; bad token -> no address. tests/test_enrich_cfemail.py 3/3; module selftest run.
NOT run: any measurement. The bio links of judged-good editors, the pool/sent lists, new_rows.jsonl and test_plan.md are not on the 3090.
Paid tests (ideas 1 and 3): not run -- no wallet, no money_guard, no vendor keys or counter here; money stays at 0.
