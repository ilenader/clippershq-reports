# BL-1705 -- a paid STEP runs only inside a named wallet line

Before: money_guard_ok() ran <repo>/tools/money_guard.py check (no such file; MILOJE/tools/money_guard.py is the real one) with no line and no amount, so every paid STEP was refused.
Now a paid step is written
    STEP: tag3090 b89_q7 1.90 r4_q6.tsv --line "Finder daily" --yes 2026-10-24_1800_<order>.md
and the relay, in this order, refuses on the first failure and runs NOTHING when it refuses:
1. the sub-command (first positional) is allowed and every arg matches the arg regex (no `..`, no shell characters; shlex, never a shell);
2. the amount is the positional at the step's `usd_arg` index, 0 < usd <= $50 per step; the wallet line matches [A-Za-z0-9 _.-]{3,40};
3. MILOJE money_guard `check "<line>" <usd>` (path: CLIPPERSHQ_MONEY_GUARD or <Desktop>\MILOJE\tools\money_guard.py) must exit 0 -- exactly those two arguments; a missing guard refuses;
4. Dusan's yes made checkable: `--yes <order file name>` must be a real file in office\<role>\ or read\, at most 36 h old, naming Dusan and a standalone "yes". The relay cannot judge the words beyond that; it does stop a paid STEP that quotes no order, a stale one, or a path trick (name regex, no `..`).
Then the script runs with `--line "<line>"` passed on (it books the wallet and obeys pause89 itself); `--yes` is not passed on. Output is text, addresses/@handles scrubbed, and any 24+ char token (a key) is replaced by <removed>, in refusals too.
Entries in STEPS for paid scripts need "paid": True and "usd_arg": <index>. A paid entry without usd_arg is always refused (no amount).
Proof: tests/test_remote_fixer.py 25 passed (19 + 6 new in PaidStepTest, fake guard with $2.00 left on 'Finder daily', fake script that prints a key): inside the line passes and the line reaches the script; refused with no line / no amount / bad amount / over the remainder / wrong line / over the ceiling / missing guard, each with the script NOT run; yes missing, stale, without Dusan, or path trick refused; the key never comes back; --line on a free step refused. No vendor call, $0.

## Landed at HQ by 1 LEADS (24 Oct 18:45) -- with one change
3 FIXER sent this as BL-1704; HQ had already used BL-1704 (2 APP's steps), so the claim was refused and 1 LEADS landed it
as BL-1705. **Changed:** MILOJE money_guard `check` calls spend(), i.e. it BOOKS the amount, and tag3090/fol3090 book their
own cap again before their first call -- every chunk would have been booked twice (the wallet inflation BL-1697 found:
$45.35 booked against $28.57 spent). The relay now only READS the line through money_guard's own summary(): the line must
exist, be active and have at least the step's amount left; the runner books it once. New test: the relay check books
nothing, and an expired line refuses (test_remote_fixer 27/27).
Paid entries: `tag3090` and `fol3090` (usd_arg 1); they take `--line` (fol3090 LINE, read by tag3090 too) and tag3090 finds a
tag list by bare file name in bl1689_work. feeds89 / part3090 are not on the list yet.
$0 proof at HQ against the real wallet ("Finder daily", $5.00 left): `tag3090 b89_q4 0.01 r4_q6.tsv --line "Finder daily"
--yes 2026-10-24_1634_...` passed the relay and stopped at tag3090's own run-name guard before any booking or call; $9.00 ->
refused (over the line); no --yes -> refused. wallet.json byte-identical before and after.
