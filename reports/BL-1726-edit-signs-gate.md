# BL-1726 -- edit-signs text gate (half of the e-mail-first gate)
tools/edit_signs_gate.py: free, no network. score(name, bio, captions) -> score/hits/edit (threshold 3). `measure` CLI prints
speed (ms/account) and precision/recall/accuracy on a labelled CSV/JSONL (id,name,bio,captions,label). Weights are a first guess on
synthetic text: NOT yet measured on the 300 known accounts (sample not received). Not covered: the TikTok bio re-read (needs live fetch).
Tests: tests/test_edit_signs_gate.py 5/5.
