# BL-1715 -- free audio features for "movie dialogue vs AI voice / random talker"

Order: Dusan 25 Oct 10:54. The edit judges only see frames, so this is a separate, free, local measurement.
tools/clip_voice_kind.py (new, called by nothing): decode with ffmpeg (clip_speech.decode_pcm), Silero VAD spans (clip_speech.speech_spans), then per clip: speech share, span count, longest and median span, median gap, bed-under-voice gap in dB, pitch spread in semitones (autocorrelation F0 on voiced frames), loudness spread. With `--labels name,label(keep|reject)` it prints, per feature, the best single-threshold accuracy on the labelled clips (0.5 = chance).
Tests: tests/test_bl1715_voice_kind.py (4, synthetic audio: flat vs varying pitch, silence, threshold search); end-to-end smoke on a generated tone through the CLI.
NOT claimed: no real clips here, so nothing is known yet about whether any feature separates movie dialogue from TTS or a talker. Ship rule: a feature goes in only as a FLAG, only if it splits >= 90% on labelled clips with 0 wanted rejected (clip_speech.py warns against audio gates).
Needs from HQ: 40 clips with sound (20 keep, 20 reject, names = hashes) and a labels.csv, then `python tools/clip_voice_kind.py --dir <clips> --labels labels.csv`.
