# BL-1735 -- face29 sheet DRAW step on the 3090 (30 Oct)
tools/sheet_draw_bench.py: same layout as face29.sheets() (4x2 tiles of 450x750, header box, number badge), SYNTHETIC name/bio (real bios not copied), DejaVu font on Linux.
Input: /srv/finder_gate/face29b/tiles_sample (200 tiles -> 25 sheets). Result: 25 sheets in 2.0 s on 1 worker (~44,800 sheets/h), 0.61 s on 4 workers (~148,600/h), 0.40 s on 8 (~227,800/h); jpg ~589 KB.
One sheet viewed: layout correct. Differences to check on the real run: (1) real bios/names (emoji and non-Latin glyphs need a font like Noto, DejaVu has gaps); (2) the original font was Arial/Segoe, so line wraps will differ slightly.
Not tested: face29.py itself (it needs LOCALAPPDATA + meta.jsonl with bios, not copied). Drawing is ~100x faster than the stated 150-300 sheets/h, so drawing is not the bottleneck; fetch/judge are.
Tests: tests/test_sheet_draw_bench.py 2/2.
