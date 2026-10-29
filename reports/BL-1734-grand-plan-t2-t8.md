# BL-1734 -- GRAND_PLAN_1029, 3 FIXER's parts (29 Oct, 3090)
T2 (Opus off routine work): this window runs on Sonnet 5.5 (claude-sonnet-5-5), not Opus; it makes no judge calls. Proof: model id of this session; PID 1429988 (claude_window_job, tmux fin3fixer).
    Not mine: restarting 1_LEADS / BOSS subagents / HELM status replies on a cheaper model (owners: Finder, ALFRED).
T8 (disk, judge rewrite: own temp only, never /tmp at large, never transcripts): farm_disk_prune.py now skips transcripts unless --transcripts is given;
    /tmp step touches only own-user folders with the narrow scratch names, idle >= --age-min AND with no process using them. Tests 3/3.
    Disk now 9.2 GB free (plan target 12 GB); not reached by temp files alone. Note: on 27-28 Oct, before the 29 Oct rule, I deleted job-home transcripts older than 6 h
    (~3 GB) and gzipped others; I will not do that again.
