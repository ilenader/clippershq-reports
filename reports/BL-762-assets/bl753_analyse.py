"""scratch/bl753_analyse.py — where should the view floor N sit? $0, offline.

Reads scratch/bl753_viewfloor.json (200 channels, 4 niches) and reports the viewCount
distribution among channels that FAIL the 50,000-subscriber floor — the population the
proposed `subs >= 50k OR views >= N` clause would rescue.

The question N has to answer is not "which channels are big" but "which sub-50k channels are
ALIVE". So the distribution is reported against three free signals that separate those:
views, views-per-subscriber, and views-per-year-of-channel-age.
"""
import json
import os
import statistics
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = json.load(open(os.path.join(ROOT, "scratch", "bl753_viewfloor.json"), encoding="utf-8"))
FLOOR = 50_000
NOW = datetime(2026, 7, 31, tzinfo=timezone.utc)


def age_years(iso):
    try:
        d = datetime.fromisoformat((iso or "").replace("Z", "+00:00"))
        return max(0.25, (NOW - d).days / 365.25)
    except Exception:
        return None


for r in rows:
    r["age_y"] = age_years(r.get("published_at"))
    r["vps"] = (r["views"] / r["subs"]) if (r.get("views") and r.get("subs")) else None
    r["vpy"] = (r["views"] / r["age_y"]) if (r.get("views") and r.get("age_y")) else None
    r["vpv"] = (r["views"] / r["videos"]) if (r.get("views") and r.get("videos")) else None

print("=" * 100)
print("POPULATION")
print("=" * 100)
print(f"  channels: {len(rows)}  across {len(set(r['niche'] for r in rows))} niches")
hidden = [r for r in rows if r.get("hidden_subs")]
print(f"  hiddenSubscriberCount = true: {len(hidden)}  "
      f"({100*len(hidden)/len(rows):.1f}%)   <- must NOT be cut on subs")
nosubs = [r for r in rows if r.get("subs") is None]
print(f"  subscriberCount absent      : {len(nosubs)}")
print(f"  viewCount present           : {sum(1 for r in rows if r.get('views') is not None)}/{len(rows)}")
print(f"  customUrl present           : {sum(1 for r in rows if r.get('custom_url'))}/{len(rows)}")
print(f"  publishedAt present         : {sum(1 for r in rows if r.get('published_at'))}/{len(rows)}")

print("\n" + "=" * 100)
print("PASS / FAIL AGAINST THE CURRENT 50k SUBSCRIBER FLOOR, BY NICHE")
print("=" * 100)
print(f"  {'niche':11s} {'n':>4s} {'pass 50k':>9s} {'fail':>6s} {'hidden':>7s}")
for n in sorted(set(r["niche"] for r in rows)):
    sub = [r for r in rows if r["niche"] == n]
    p = sum(1 for r in sub if (r.get("subs") or 0) >= FLOOR)
    h = sum(1 for r in sub if r.get("hidden_subs"))
    print(f"  {n:11s} {len(sub):4d} {p:9d} {len(sub)-p:6d} {h:7d}")

fail = [r for r in rows if not r.get("hidden_subs")
        and r.get("subs") is not None and r["subs"] < FLOOR and r.get("views") is not None]
print(f"\n  FAIL-the-floor population with a usable viewCount: n={len(fail)}")

print("\n" + "=" * 100)
print("VIEWCOUNT DISTRIBUTION AMONG CHANNELS THAT FAIL THE 50k FLOOR")
print("=" * 100)
v = sorted(r["views"] for r in fail)


def pct(p):
    if not v:
        return 0
    return v[min(len(v) - 1, int(len(v) * p / 100))]


for p in (10, 25, 50, 75, 90, 95, 99):
    print(f"    p{p:<3d} {pct(p):>14,}")
print(f"    max  {v[-1]:>14,}      min {v[0]:>12,}")

print("\n  how many sub-50k channels would each candidate N rescue:")
print(f"    {'N':>12s} {'rescued':>8s} {'% of fail':>10s}   {'median subs':>12s} {'median v/sub':>13s} {'median v/yr':>12s}")
for N in (500_000, 1_000_000, 2_000_000, 3_000_000, 5_000_000, 10_000_000):
    sel = [r for r in fail if r["views"] >= N]
    if sel:
        ms = statistics.median([r["subs"] for r in sel])
        mv = statistics.median([r["vps"] for r in sel if r["vps"]])
        my = statistics.median([r["vpy"] for r in sel if r["vpy"]])
        print(f"    {N:>12,} {len(sel):8d} {100*len(sel)/len(fail):9.1f}%   "
              f"{ms:>12,.0f} {mv:>13.1f} {my:>12,.0f}")
    else:
        print(f"    {N:>12,} {0:8d} {0.0:9.1f}%")

print("\n" + "=" * 100)
print("WHO IS IN THERE? every sub-50k channel with >= 1M views, sorted by views")
print("=" * 100)
big = sorted([r for r in fail if r["views"] >= 1_000_000], key=lambda r: -r["views"])
print(f"  {'niche':10s} {'subs':>8s} {'views':>13s} {'v/sub':>7s} {'age_y':>6s} {'v/yr':>12s} {'vids':>6s} cc  title")
for r in big:
    print(f"  {r['niche']:10s} {r['subs']:>8,} {r['views']:>13,} {r['vps']:>7.0f} "
          f"{(r['age_y'] or 0):>6.1f} {(r['vpy'] or 0):>12,.0f} {(r['videos'] or 0):>6,} "
          f"{r['country'] or '--':2s}  {r['title'][:38]}")

print("\n" + "=" * 100)
print("THE CONTROL: sub-50k channels BELOW 1M views (the ones the floor is right to drop)")
print("=" * 100)
small = [r for r in fail if r["views"] < 1_000_000]
if small:
    print(f"  n={len(small)}   median views {statistics.median([r['views'] for r in small]):,.0f}"
          f"   median subs {statistics.median([r['subs'] for r in small]):,.0f}")
    vps = [r["vps"] for r in small if r["vps"]]
    vpy = [r["vpy"] for r in small if r["vpy"]]
    if vps:
        print(f"  median views/sub {statistics.median(vps):.1f}   "
              f"median views/yr {statistics.median(vpy):,.0f}")

print("\n" + "=" * 100)
print("SEPARATION CHECK — is viewCount actually discriminating, or just a size proxy?")
print("=" * 100)
passers = [r for r in rows if (r.get("subs") or 0) >= FLOOR and r.get("views")]
if passers:
    pv = sorted(r["views"] for r in passers)
    print(f"  channels that PASS the 50k floor (n={len(passers)}): "
          f"median views {pv[len(pv)//2]:,}   p10 {pv[int(len(pv)*.1)]:,}")
    lowpass = [r for r in passers if r["views"] < 2_000_000]
    print(f"  ...of which BELOW 2M views: {len(lowpass)} "
          f"({100*len(lowpass)/len(passers):.1f}%)  <- pass on subs but are quieter than "
          f"the channels an N=2M clause would rescue")

json.dump({"n": len(rows), "fail_floor": len(fail),
           "views_percentiles": {f"p{p}": pct(p) for p in (10, 25, 50, 75, 90, 95, 99)},
           "rescue_counts": {str(N): len([r for r in fail if r["views"] >= N])
                             for N in (500_000, 1_000_000, 2_000_000, 3_000_000, 5_000_000,
                                       10_000_000)},
           "hidden_subs": len(hidden)},
          open(os.path.join(ROOT, "scratch", "bl753_viewfloor_analysis.json"), "w",
               encoding="utf-8"), indent=1)
print("\nwrote scratch/bl753_viewfloor_analysis.json")
