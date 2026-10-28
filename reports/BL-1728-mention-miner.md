# BL-1728 -- free @mention miner (code half)
tools/mention_miner.py: mine (extract @handles from stored bio/caption rows, drop known, count) -> fetch (public profile GET, resumable,
errors recorded per handle, no login) -> batch (handles with an e-mail not yet handed over). Counts only on stdout, never a handle.
Tests: tests/test_mention_miner.py 5/5 (synthetic text). NOT run live: fetch_bio (TikTok page parse) is untested against the real site;
no stored data on the 3090 (116,199 bios live at HQ). Several tabs/throwaway profiles are not needed for the plain-GET path; a headless
browser path is a follow-up only if plain GET is blocked.
