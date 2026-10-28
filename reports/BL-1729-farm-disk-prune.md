# BL-1729 -- farm_disk_prune.py
Safe 3090 disk prune (dry run default). gzips old transcripts in place; removes own /tmp scratch folders (_to_delete*, _td_*, td_*, qa_art*, qa_copy*, qa_junk*, junk*)
only when nothing in them changed for --age-min AND no process has cwd/open file there. Tests: tests/test_farm_disk_prune.py 3/3.
Finding: /tmp refills with ~300 MB QA copies (several per hour) from another team's QA runs; that, not the farm, is what pulls the 3090 below 8 GB.
Not done: running it on a schedule (needs a cron/loop owner) -- until then it is a manual `python tools/farm_disk_prune.py --apply`.
