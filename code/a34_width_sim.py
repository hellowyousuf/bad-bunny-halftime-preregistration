#!/usr/bin/env python3
"""A34 · interval-width simulation from keyword-hit counts (no text).

Input: data/raw/a34_hit_identifiers.csv (airings by network × phase, from a34_hit_counts.py).
For each scenario, synthetic segments are drawn per airing and coded into the eight V8
categories; the P1 belonging share, the P2 corrected mean pairwise Jensen–Shannon divergence
(base 2) per phase and the change from the announcement phase are bootstrapped over airings
as the plan specifies. Reported: 95% interval half-widths, compared with the ±.05 band (A14).

Simplifications (A38): B = 500 bootstrap draws (plan: 2,000) and the permutation baseline
estimated once per synthetic data set from 100 shuffles and subtracted as a constant.
Seed fixed. Usage: python3 data/analysis/a34_width_sim.py <project_dir>
Writes data/analysis/a34_width_sim.json.
"""
import csv, json, sys, datetime as dt
import numpy as np
from pathlib import Path

SEED = 20261017
NETS = ["CNN", "Fox News", "MSNBC"]
PHASES = ["announcement", "build-up", "performance with aftermath", "broadcast window"]
WINDOW = (dt.date(2026, 2, 8), dt.date(2026, 2, 10))   # A29
CATS = 8   # belonging-include, belonging-exclude, national identity, immigration, cultural representation,
           # political controversy, generic partisan conflict, no frame
BASE = np.array([.12, .10, .08, .08, .14, .16, .14, .18])
SHIFT = {"CNN": np.array([.04, -.03, 0, 0, .02, -.01, -.01, -.01]),
         "Fox News": np.array([-.05, .07, .01, .03, -.04, .01, -.01, -.02]),
         "MSNBC": np.array([.05, -.04, 0, -.01, .02, -.01, 0, -.01])}
SCENARIOS = [  # segments per airing (Poisson mean, min 1), relevance share, network differences
    {"id": "S1", "seg_per_airing": 1.5, "relevant": 0.6, "differences": "none"},
    {"id": "S2", "seg_per_airing": 3.0, "relevant": 0.7, "differences": "none"},
    {"id": "S3", "seg_per_airing": 3.0, "relevant": 0.7, "differences": "moderate"},
    {"id": "S4", "seg_per_airing": 6.0, "relevant": 0.8, "differences": "moderate"},
]
B, SHUF = 500, 100

def jsd(p, q):
    m = (p + q) / 2
    def kl(a, b):
        mask = a > 0
        return np.sum(a[mask] * np.log2(a[mask] / b[mask]))
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)

def mean_pair_jsd(counts):  # counts: nets × CATS
    P = [c / c.sum() if c.sum() else np.full(CATS, 1 / CATS) for c in counts]
    return np.mean([jsd(P[0], P[1]), jsd(P[0], P[2]), jsd(P[1], P[2])])

def main(proj):
    proj = Path(proj); rng = np.random.default_rng(SEED)
    air = {(n, p): 0 for n in NETS for p in PHASES}
    for r in csv.DictReader(open(proj / "data/raw/a34_hit_identifiers.csv")):
        if r["phase"] == "outside": continue
        air[(r["network"], r["phase"])] += 1
        d = dt.date.fromisoformat(r["air_date_et"])
        if WINDOW[0] <= d <= WINDOW[1]: air[(r["network"], "broadcast window")] += 1
    out = {"seed": SEED, "B": B, "shuffles": SHUF, "airings": {f"{n}|{p}": v for (n, p), v in air.items()}, "scenarios": []}
    for sc in SCENARIOS:
        data = {}   # (net, phase) -> list of per-airing category count vectors (relevant segments only)
        for (n, p), k in air.items():
            probs = BASE + (SHIFT[n] if sc["differences"] == "moderate" else 0)
            probs = np.clip(probs, 0.001, None); probs /= probs.sum()
            rows = []
            for _ in range(k):
                s = max(1, rng.poisson(sc["seg_per_airing"]))
                rel = rng.binomial(s, sc["relevant"])
                rows.append(rng.multinomial(rel, probs))
            data[(n, p)] = np.array(rows) if rows else np.zeros((0, CATS), int)
        res = {"id": sc["id"], **{k: v for k, v in sc.items() if k != "id"}, "phases": {}}
        # permutation baseline per phase (constant)
        base = {}
        for p in PHASES:
            allrows = np.vstack([data[(n, p)] for n in NETS]); sizes = [len(data[(n, p)]) for n in NETS]
            vals = []
            for _ in range(SHUF):
                idx = rng.permutation(len(allrows)); o = 0; cs = []
                for s in sizes: cs.append(allrows[idx[o:o + s]].sum(0)); o += s
                vals.append(mean_pair_jsd(cs))
            base[p] = float(np.mean(vals))
        boots = {p: [] for p in PHASES}; share = {(n, p): [] for n in NETS for p in PHASES}
        for _ in range(B):
            for p in PHASES:
                cs = []
                for n in NETS:
                    m = data[(n, p)]
                    bs = m[rng.integers(0, len(m), len(m))].sum(0) if len(m) else np.zeros(CATS)
                    cs.append(bs); tot = bs.sum()
                    share[(n, p)].append((bs[0] + bs[1]) / tot if tot else np.nan)
                boots[p].append(mean_pair_jsd(cs) - base[p])
        hw = lambda x: float((np.nanpercentile(x, 97.5) - np.nanpercentile(x, 2.5)) / 2)
        a = np.array(boots["announcement"])
        for p in PHASES:
            x = np.array(boots[p])
            res["phases"][p] = {
                "relevant_segments_expected": int(sum(data[(n, p)].sum() for n in NETS)),
                "corrected_jsd_halfwidth": round(hw(x), 4),
                "change_from_announcement_halfwidth": None if p == "announcement" else round(hw(x - a), 4),
                "change_wider_than_band_.05": None if p == "announcement" else hw(x - a) > 0.05,
                "belonging_share_halfwidth": {n: round(hw(np.array(share[(n, p)])), 3) for n in NETS}}
        out["scenarios"].append(res)
    json.dump(out, open(proj / "data/analysis/a34_width_sim.json", "w"), indent=1)
    for s in out["scenarios"]:
        print(s["id"], s["seg_per_airing"], s["relevant"], s["differences"])
        for p, v in s["phases"].items():
            print("   ", p.ljust(28), v["relevant_segments_expected"], v["corrected_jsd_halfwidth"],
                  v["change_from_announcement_halfwidth"], v["belonging_share_halfwidth"])

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
