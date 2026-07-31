"""scratch/bl753_viewfloor_probe.py — measure the viewCount distribution BEFORE setting N.

The size gate is `subs >= 50_000`. BL-748 found it drops a 26.9k-sub podcast carrying 16.8M
views (626 views/sub) while a 218k-sub channel with 1.72M views passes. The proposed fix is
`subs >= 50k OR views >= N` — and N is the gate's entire behaviour, so it is measured here
rather than guessed. BL-750 explicitly says to pick N from a multi-niche sample, not the
single 50-channel one.

WHAT IT MEASURES, per niche: for every channel that FAILS the 50k subscriber floor, its
viewCount, videoCount, views-per-sub, views-per-video, channel age and country. That is the
population the OR-clause would rescue, so it is the population N has to separate.

Cost: 4 queries x (100 search + ~1 channels) = ~404 of the 10,000/day free quota. $0 cash.
Read-only on the repo: writes ONLY scratch/bl753_viewfloor.json. The API key is read into a
local and is never printed, logged or written to the output.
"""
import json
import os
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "clippershq"))

CFG = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))
YA = CFG.get("youtube_api") or {}
_KEY = (YA.get("key") or "").strip()
if not _KEY:
    sys.exit("youtube_api.key missing")
BASE = YA.get("base_url") or "https://www.googleapis.com/youtube/v3"
TIMEOUT = int(YA.get("timeout_seconds", 15))

# One query per niche, deliberately spread: the two BL-748 measured as best (gaming 82%,
# fitness 68% in-band), the current default it wants demoted, and one money-adjacent control.
NICHES = [
    ("fitness", "fitness coach online"),
    ("gaming", "gaming lets play channel"),
    ("podcaster", "business podcast"),
    ("business", "entrepreneur business"),
]
PER_QUERY = 50


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "bl753_probe/1.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.load(r)


def search(q, n=PER_QUERY):
    p = {"part": "snippet", "type": "channel", "q": q, "maxResults": min(n, 50), "key": _KEY}
    d = _get(BASE + "/search?" + urllib.parse.urlencode(p))
    return [it["id"]["channelId"] for it in d.get("items", [])
            if (it.get("id") or {}).get("channelId")]


def details(ids):
    """Everything the SAME channels.list call already returns — including the five fields the
    funnel currently discards. Same 1 unit / 50 ids either way."""
    out = {}
    for j in range(0, len(ids), 50):
        p = {"part": "snippet,statistics", "id": ",".join(ids[j:j + 50]), "key": _KEY}
        d = _get(BASE + "/channels?" + urllib.parse.urlencode(p))
        for it in d.get("items", []):
            st = it.get("statistics") or {}
            sn = it.get("snippet") or {}

            def _i(v):
                try:
                    return int(v)
                except (TypeError, ValueError):
                    return None
            out[it.get("id")] = {
                "subs": _i(st.get("subscriberCount")),
                "hidden_subs": bool(st.get("hiddenSubscriberCount")),
                "views": _i(st.get("viewCount")),
                "videos": _i(st.get("videoCount")),
                "country": str(sn.get("country") or "").strip().upper(),
                "custom_url": sn.get("customUrl") or "",
                "published_at": sn.get("publishedAt") or "",
                "title": sn.get("title") or "",
                "description": sn.get("description") or "",
            }
    return out


rows = []
for niche, q in NICHES:
    try:
        ids = search(q)
        det = details(ids)
    except Exception as exc:
        print("  %-10s QUERY FAILED %s" % (niche, type(exc).__name__))
        continue
    for cid, d in det.items():
        rows.append({"niche": niche, "query": q, "channel_id": cid, **d})
    print("  %-10s %-28s -> %3d channels" % (niche, q, len(det)))

json.dump(rows, open(os.path.join(ROOT, "scratch", "bl753_viewfloor.json"), "w",
                     encoding="utf-8"), indent=1, ensure_ascii=False)
print("\ntotal channels: %d  (quota ~%d units)" % (len(rows), len(NICHES) * 101))
print("-> scratch/bl753_viewfloor.json")
