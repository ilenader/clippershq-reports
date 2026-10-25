# BL-1717 -- flag-only "long continuous narration" rule, swept on the whisper transcripts

Order (1 LEADS 17:41 for Dusan): resume the 11:00 clip-keep order on wanted120 and clips40; flag-only; wanted-killed must be 0; report narrators caught.
Built: tools/narration_flag.py. A clip is FLAGGED when speech share >= F AND words >= W AND words per speech second is in [1.2, 4.5] (a steady narrator; sparse movie lines and fast chatter are not). No model, no money, no drop: the sweep prints, for F in 0.5..0.9 and W in 15..90, wanted-killed on wanted120, narrators caught and keeps killed on clips40, and the best setting with wanted-killed 0 and keeps-killed 0 (or "stays off").
Tests: tests/test_bl1717_narration_flag.py (2, synthetic transcripts).
NOT measured: the two tx.json files and labels live on HQ (bl1712_work/wanted120, clips40), not in my code-only copy, so the numbers are not in this report. Run on HQ:
  python tools/narration_flag.py --wanted <wanted120>/tx.json --mixed <clips40>/tx.json --mixed-labels <clips40>/labels.csv
Combine with frames later (frames + transcript) only if this flag alone leaves narrators uncaught.
