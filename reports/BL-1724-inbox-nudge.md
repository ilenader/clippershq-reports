# BL-1724 -- inbox read between chunks

Changes (in the patch):
- tools/office/stop_guard.py: ALLOW_STOP is ignored when older than 2 h (mtime), so it is no longer a permanent bypass.
- tools/office/inbox_nudge.py (new): with CLIPPERSHQ_OFFICE_ROLE set, prints `NEW ORDER <name>: read it at the next chunk
  boundary and reply` for each order in the role folder not nudged in the last 5 min (state `.inbox_nudge.json`).
  PostToolUse gets it as JSON additionalContext (plain stdout does not reach the model there); UserPromptSubmit as plain text.
- tools/office/test_inbox_nudge.py (new): 6 tests, all pass (no order -> empty; order -> one nudge naming it; second call
  -> empty; again after 5 min; PostToolUse JSON; no role env -> empty; 3 h-old ALLOW_STOP no longer bypasses stop_guard).

NOT in the patch (.claude/settings.json is not in the code-only copy): HQ must add under "hooks", next to Stop:

    "UserPromptSubmit": [{"hooks": [{"type": "command", "command": "python tools/office/inbox_nudge.py"}]}],
    "PostToolUse": [{"hooks": [{"type": "command", "command": "python tools/office/inbox_nudge.py"}]}]

(use the same python invocation style as the existing Stop entry). LESSONS.md line to add (not in the repo copy):
`Long jobs check the inbox between chunks (27 Oct: 40 min unread).`

Tests: tools/office/test_inbox_nudge.py 6/6 OK on Linux. tests/test_office_tools.py -k stop: 10 passed; 1 failed
(test_the_project_settings_register_the_stop_hook) only because .claude/settings.json is absent in this copy.
