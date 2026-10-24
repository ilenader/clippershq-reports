# BL-1699 -- the last three unguarded os.replace/os.remove in clippershq

edits_clean.py:126 (replace), edits_gdrive.py:241 and farm_sheets.py:211 (remove) now use atomic_io (Windows sharing-violation retry), same drop-in call.
Proof: tests/test_atomic_io.py (script) lists no unguarded site after BL-1698 + this.
