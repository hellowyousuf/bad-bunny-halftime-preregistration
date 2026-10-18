#!/usr/bin/env python3
"""A34 · pre-registration keyword-hit COUNTS (no caption text), TV News Archive.

Queries the Internet Archive TV News search (service_backend=tvs, public, guest) with the
A6 keyword filter, per channel identifier, over the A5 period (padded one day each side),
and keeps ONLY the item identifier (channel_YYYYMMDD_HHMMSS_program, UTC) and the query.
No caption text, description or snippet is written. Phase is assigned from the airing
start converted to America/New_York (A37) against the A5 boundaries.

Usage: python3 data/analysis/a34_hit_counts.py <project_dir>
Writes data/raw/a34_hit_identifiers.csv, data/raw/a34_hit_counts.csv, writes data/search_log.csv (one row per query × weekly window, index total and retrieved).
"""
import csv, json, sys, time, urllib.parse, urllib.request, datetime as dt
from zoneinfo import ZoneInfo
from pathlib import Path

ENDPOINT = "https://archive.org/services/search/beta/page_production/"
TERMS = ['"Bad Bunny"', '"Benito"', '"halftime show"', '"half-time show"',
         '"halftime performance"', '"All-American Halftime"']          # A6, verbatim
CHANNELS = {"CNN": ["CNNW"], "Fox News": ["FOXNEWSW"], "MSNBC": ["MSNBCW", "MSNOW"]}   # A9: MS NOW = MSNBC
EMPTY_FEEDS = ["CNN", "FOXNEWS", "MSNBC"]   # east-coast ids: checked once over the whole range (0 hits on 2026-10-17)
PHASES = [("announcement", dt.date(2025, 9, 28), dt.date(2025, 10, 25)),
          ("build-up", dt.date(2025, 10, 26), dt.date(2026, 2, 7)),
          ("performance with aftermath", dt.date(2026, 2, 8), dt.date(2026, 2, 28))]  # A5
QUERY_START, QUERY_END = dt.date(2025, 9, 27), dt.date(2026, 3, 1)
WINDOW_DAYS = 7   # weekly windows: one page each, stable paging (a 100-per-page walk lost items)
ET = ZoneInfo("America/New_York")
PER_PAGE = 250

def fetch(q, page):
    url = ENDPOINT + "?" + urllib.parse.urlencode({"user_query": q, "service_backend": "tvs",
        "hits_per_page": PER_PAGE, "page": page})
    req = urllib.request.Request(url, headers={"User-Agent": "rihlah-research/1.0 (research; counts only)"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)["response"]["body"]["hits"]
        except Exception as e:
            time.sleep(5 * (attempt + 1)); err = e
    raise RuntimeError(f"query failed: {q} p{page}: {err}")

def phase_of(ident):
    parts = ident.split("_")
    t = dt.datetime.strptime(parts[1] + parts[2], "%Y%m%d%H%M%S").replace(tzinfo=dt.timezone.utc)
    d = t.astimezone(ET).date()
    for name, a, b in PHASES:
        if a <= d <= b: return name, d.isoformat()
    return None, d.isoformat()

def main(proj):
    proj = Path(proj); raw = proj / "data/raw"; raw.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    rows, log = {}, []
    queries = [("ALL", "(" + " OR ".join(TERMS) + ")")]
    for cid in EMPTY_FEEDS:
        q = f"{queries[0][1]} AND creator:{cid.lower()} AND date:[{QUERY_START} TO {QUERY_END}]"
        h = fetch(q, 1)
        log.append({"ts": now, "network": "check", "channel_id": cid, "term": "ALL", "window": f"{QUERY_START}..{QUERY_END}",
                    "query": q, "endpoint": ENDPOINT, "index_total": h.get("total", 0), "retrieved": len(h.get("hits", []))})
    wins, a = [], QUERY_START
    while a <= QUERY_END:
        b = min(a + dt.timedelta(days=WINDOW_DAYS - 1), QUERY_END); wins.append((a, b)); a = b + dt.timedelta(days=1)
    for net, idents in CHANNELS.items():
        for cid in idents:
            for label, kq in queries:
                for a, b in wins:
                    q = f"{kq} AND creator:{cid.lower()} AND date:[{a} TO {b}]"
                    page, got, total = 1, 0, None
                    while True:
                        h = fetch(q, page); total = h.get("total", 0)
                        hits = h.get("hits", [])
                        for x in hits:   # identifier only; cc_excerpt and all text fields are discarded
                            i = x["fields"]["identifier"]
                            r = rows.setdefault(i, {"identifier": i, "network": net, "channel_id": cid, "terms": set()})
                            r["terms"].add(label)
                        got += len(hits)
                        if not hits or got >= total or len(hits) < PER_PAGE: break
                        page += 1; time.sleep(1)
                    log.append({"ts": now, "network": net, "channel_id": cid, "term": label, "window": f"{a}..{b}",
                                "query": q, "endpoint": ENDPOINT, "index_total": total, "retrieved": got})
                    time.sleep(0.5)
    out = []
    for r in rows.values():
        ph, d = phase_of(r["identifier"])
        out.append({"identifier": r["identifier"], "network": r["network"], "channel_id": r["channel_id"],
                    "air_date_et": d, "phase": ph or "outside", "all_filter": True})
    out.sort(key=lambda r: r["identifier"])
    with open(raw / "a34_hit_identifiers.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
    counts = {}
    for r in out:
        if r["phase"] == "outside": continue
        k = (r["network"], r["phase"]); counts[k] = counts.get(k, 0) + 1
    with open(raw / "a34_hit_counts.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["network", "phase", "matching_airings_retrieved"])
        for net in CHANNELS:
            for ph, _, _ in PHASES: w.writerow([net, ph, counts.get((net, ph), 0)])
    lp = proj / "data/search_log.csv"
    with open(lp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(log[0].keys())); w.writeheader(); w.writerows(log)
    print(json.dumps({"airings": len(out), "counts": {f"{a}|{b}": c for (a, b), c in counts.items()},
                      "queries": len(log)}, indent=1))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
