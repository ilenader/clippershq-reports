"""quietwatch.py — is this repo actually idle? Read-only; touches nothing.

The brief's precondition is "no funnel process AND zero repo writes for 10 continuous
minutes". Both halves have to hold at the same time, so this samples both together and
RESETS the clock on any activity rather than reporting an average.

Watched files are the ones this task must back up and edit — a write to any of them by
another agent is the specific hazard (a concurrent writer means my edit either clobbers
theirs or is clobbered).
"""
import os
import subprocess
import sys
import time

REPO = r"C:\Users\Game Centar\OneDrive\Desktop\clipper finder"
WATCH = ["config.json", "spend.json", "master_leads.csv", "resolve_cache.json",
         "clippershq/youtube_finder.py", "clippershq/main.py"]
NEED_QUIET_S = 600
SAMPLE_S = 20


def snap():
    out = {}
    for rel in WATCH:
        p = os.path.join(REPO, rel)
        try:
            out[rel] = os.path.getmtime(p)
        except OSError:
            out[rel] = None
    return out


def repo_procs():
    """python processes whose command line points INTO this repo (tests, funnels, scripts).
    Excludes the unrelated http.server and this watcher itself."""
    try:
        ps = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-CimInstance Win32_Process -Filter \"Name like '%python%'\" | "
             "Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"],
            capture_output=True, text=True, timeout=60).stdout
    except Exception:
        return []
    import json
    try:
        d = json.loads(ps or "[]")
    except Exception:
        return []
    if isinstance(d, dict):
        d = [d]
    hits = []
    for r in d:
        cl = (r.get("CommandLine") or "")
        low = cl.lower()
        if "quietwatch" in low or "http.server" in low:
            continue
        if "clipper finder" in low or "clippershq" in low or "tests\\" in low or "tests/" in low:
            hits.append((r.get("ProcessId"), cl[:110]))
    return hits


base = snap()
quiet_since = time.time()
t0 = time.time()
print("watching: %s" % ", ".join(WATCH))
print("need %ds continuous quiet\n" % NEED_QUIET_S)
while True:
    time.sleep(SAMPLE_S)
    now = snap()
    changed = [k for k in WATCH if now[k] != base[k]]
    procs = repo_procs()
    if changed or procs:
        quiet_since = time.time()
        why = []
        if changed:
            why.append("WROTE: " + ",".join(changed))
        if procs:
            why.append("PROC: " + "; ".join("pid%s %s" % p for p in procs[:3]))
        print("[%4ds] RESET -- %s" % (time.time() - t0, " | ".join(why)))
        base = now
    else:
        q = time.time() - quiet_since
        print("[%4ds] quiet %ds/%ds" % (time.time() - t0, q, NEED_QUIET_S))
        if q >= NEED_QUIET_S:
            print("\nQUIET WINDOW ACHIEVED")
            sys.exit(0)
    if time.time() - t0 > 2400:
        print("\nGAVE UP after 40 min -- repo never went quiet")
        sys.exit(2)
