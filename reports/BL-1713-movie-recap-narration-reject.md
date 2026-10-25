# BL-1713 -- reject movie/TV recap videos (a narrator retells a film over its footage)

Dusan, 25 Oct 10:54 (via ALFRED): reject videos where a content creator narrates or recaps a movie instead of showing movie footage.

What was there: both edit-judge prompts (edits_claude_lane.py, edits_ai_review.py) already put "voice-over storytelling, explainers, word-by-word-subtitle videos" under NOT an edit / kind `creator`. A recap is the hard case: the clips ARE real movie footage, so a model can still call it an edit.
What I changed: one added sentence in each of those two creator definitions: a MOVIE / TV RECAP (voice or subtitles retelling the plot over film footage, scenes in story order, no music-synced cutting) is creator, NOT an edit, even though the footage is real.
Not changed: free_judge.py (the page/cover judge) and edit_checker.py. The page judge sees covers, not the audio or the cut rhythm; its own file records that rewording its prompt killed wanted pages, so I did not touch it without a labelled measurement.
Risk: wording only, additive; a recap-like but music-cut fan edit of a film should still be an EDIT because the sentence requires the narration AND story order AND no music-synced cutting. Not measured (no labelled clips here). HQ should run the labelled recap/edit clips through the claude lane before and after; ship-bar: no wanted edit newly rejected.
Tests: see the reply (data-free tests only).
