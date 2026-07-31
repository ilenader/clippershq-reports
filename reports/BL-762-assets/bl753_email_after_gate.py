"""scratch/bl753_email_after_gate.py — description-email yield, measured AFTER the gates. $0.

BL-750's point: parsing before the country gate reports a fill rate against a population that
never converts (its example is a country=BD channel whose address is perfectly parseable and
then dropped anyway). So this measures the yield at the position the code now parses at —
after the size, country and language gates — and reports the before/after gap that motivated
the ordering.

Offline: reads the 200 channels already fetched by bl753_viewfloor_probe.py. No new API call.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "clippershq"))
import youtube_finder as yf                                    # noqa: E402
import google_play_finder as gp                                # noqa: E402

rows = json.load(open(os.path.join(ROOT, "scratch", "bl753_viewfloor.json"), encoding="utf-8"))
CFG = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))
ALLOWED_CC = CFG.get("youtube_allowed_countries", ["US", "GB", "CA", "AU", "IE", "NZ"])
MIN_SUBS = int(CFG["youtube_finder"]["min_subscribers"])
MIN_VIEWS = int(CFG["youtube_finder"]["min_views"])
EMAIL_RE = yf._EMAIL_RE


def about(_cid):
    return {"status": 200, "html": "<html></html>"}


raw_hits = 0
for r in rows:
    if EMAIL_RE.findall(r.get("description") or ""):
        raw_hits += 1

passed, with_email, personal, role = [], [], 0, 0
examples = []
for r in rows:
    ch = {"id": r["channel_id"], "title": r["title"], "subscribers": r["subs"],
          "views": r["views"], "hidden_subs": r["hidden_subs"], "country": r["country"],
          "custom_url": r["custom_url"], "published_at": r["published_at"],
          "description": r["description"], "videos": r["videos"], "niche": r["niche"]}
    res = yf.find_contact(ch, about, min_subscribers=MIN_SUBS, min_views=MIN_VIEWS,
                          allowed_countries=ALLOWED_CC, allowed_languages=[])
    if not res["passed_filter"]:
        continue
    passed.append(res)
    if res["email"] and res["email_source"] == "description":
        with_email.append(res)
        k = gp.classify_email_quality(res["email"])
        if k == "personal":
            personal += 1
        else:
            role += 1
        if len(examples) < 8:
            dom = res["email"].rpartition("@")[2]
            examples.append((r["niche"], r["subs"], r["country"], k, dom, r["title"][:32]))

print("=" * 96)
print("DESCRIPTION-EMAIL YIELD — before vs after the gates (n=%d channels)" % len(rows))
print("=" * 96)
print(f"  raw regex hit anywhere in the 200 descriptions : {raw_hits:3d}"
      f"  ({100*raw_hits/len(rows):.1f}% of all channels)")
print(f"  channels SURVIVING size+country gates          : {len(passed):3d}")
print(f"  ...of those, a usable address from description : {len(with_email):3d}"
      f"  ({100*len(with_email)/max(1,len(passed)):.1f}% of survivors)")
print(f"       personal : {personal}   role : {role}")
print()
gap = raw_hits - len(with_email)
print(f"  THE ORDERING GAP: {gap} channels carry a parseable address but never reach the parse,")
print("  because the size or country gate drops them first. Parsing before the gate would have")
print("  reported those as fill and none of them can be contacted.")

# what actually removed them
dropped_with_addr = []
for r in rows:
    if not EMAIL_RE.findall(r.get("description") or ""):
        continue
    ch = {"id": r["channel_id"], "title": r["title"], "subscribers": r["subs"],
          "views": r["views"], "hidden_subs": r["hidden_subs"], "country": r["country"],
          "description": r["description"], "niche": r["niche"]}
    res = yf.find_contact(ch, about, min_subscribers=MIN_SUBS, min_views=MIN_VIEWS,
                          allowed_countries=ALLOWED_CC, allowed_languages=[])
    if not res["passed_filter"]:
        dropped_with_addr.append((res["filter_reason"], r["country"], r["title"][:30]))
import collections
print("\n  why the %d were dropped:" % len(dropped_with_addr))
for k, v in collections.Counter(x[0] for x in dropped_with_addr).most_common():
    print(f"    {k:26s} {v}")
cc = collections.Counter(x[1] or "--" for x in dropped_with_addr if x[0] == "non_target_country")
if cc:
    print("    non-target countries seen:", dict(cc))

print("\n  REAL EXAMPLES that survived and yielded an address:")
print(f"    {'niche':10s} {'subs':>8s} cc  {'kind':9s} {'domain':24s} channel")
for n, s_, c, k, dom, t in examples:
    print(f"    {n:10s} {s_:>8,} {c or '--':2s}  {k:9s} {dom:24s} {t}")

json.dump({"n": len(rows), "raw_hits": raw_hits, "passed_gates": len(passed),
           "with_description_email": len(with_email), "personal": personal, "role": role,
           "ordering_gap": gap},
          open(os.path.join(ROOT, "scratch", "bl753_email_yield.json"), "w",
               encoding="utf-8"), indent=1)
print("\nwrote scratch/bl753_email_yield.json")
