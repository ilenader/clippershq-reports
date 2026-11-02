# BL-1737 -- self-editing edit finder UI (first build)

Spec was not given; built reading (a): a queue page where one click per candidate is stored and the queue re-ranks itself from all clicks.

- `clippershq/edit_finder.py`: logic (candidates file in, append-only verdicts out, word weights re-derived from verdicts, e-mails and @mentions masked, one row per id, decided ids never return).
- `dashboard/editfinder_routes.py` + one word added to the mount list in `dashboard/server.py`: `/api/editfinder/queue|learned|verdict`.
- `dashboard/static/editfinder.html`: one card, three buttons (Editor / Not an editor / Skip), "what it has learned" box.
- `tests/test_edit_finder.py`: 4 tests, pass (no-dupes, masking, learning, skip, bad input, missing files). FastAPI is not installed on the 3090, so the routes were only compile-checked; run the dashboard once at HQ.

Data it needs at HQ: `ground_truth/edit_finder_candidates.jsonl`, lines `{"id": "<opaque>", "text": "<bio>"}` (e.g. exported from the gate output). Verdicts go to `ground_truth/edit_finder_verdicts.jsonl`.
Not done: filling the candidates file (needs HQ data), Dusan's choice if he wanted another reading.
