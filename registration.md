# Pre-registration — Bad Bunny's all-Spanish Super Bowl Halftime Performance: Partisan Meaning Making around a High-salience Sport Event

Deposited on Zenodo as a dated, versioned record with a DOI before any caption text was retrieved (A32; the approved plan named the Open Science Framework, and the authors chose Zenodo instead, deviation X1 in `plan/deviations.json`; the registration's content is unchanged). Plan revision 1, approved 2026-10-17 by Mohammad Yousuf.

## Research questions
- **RQ1.** How did the share of belonging frames, relative to generic partisan conflict frames, differ across Fox News, CNN, and MSNBC?
- **RQ2.** How did the frame distance between the networks change from the announcement phase to the performance phase?
- **RQ3.** Was the change in distance between the networks carried by belonging frames or by generic partisan conflict frames?
- **RQ4.** How did the networks differ in evaluating the Spanish language, as a claim to belonging or as a breach of it?

## Data
Closed captions of Fox News, CNN and MSNBC programs whose captions match the keyword filter (A6), with network, program and airing date. Source: Internet Archive TV News Archive (https://archive.org/details/tv); licensed transcripts of the same programs as a recall and coverage check (A2). Period: September 28, 2025, to February 28, 2026; phases announcement (Sep 28–Oct 25, 2025), build-up (Oct 26, 2025–Feb 7, 2026), performance with aftermath (Feb 8–28, 2026) (A5).

**Frame.** All airings of Fox News, CNN and MSNBC (under either name, A9) held by the TV News Archive in the period, daytime and prime time. Unit of analysis: network × phase; unit of observation: caption segment: the text 30 s either side of a keyword hit, overlapping windows merged, at most 3 minutes (A7). Procedure: census of keyword matches.
Inclusion: captions contain "Bad Bunny" OR "Benito" OR "halftime show" OR "half-time show" OR "halftime performance" OR "All-American Halftime" (A6); aired in the period on Fox News, CNN or MSNBC/MS NOW. Exclusion: advertising segments (A8); reruns: a program repeating an earlier airing on the same network within 48 hours at ≥ .90 similarity is counted once (A8); other outlets, Spanish-language outlets, web and social media (brief scope).

## Variables, procedures, decision rules
Variables V0–V8, procedures P0–P5 with their decision rules, tables and figures: `plan/analysis_plan.json` (verbatim, as approved). Codebook: `plan/codebook.json`. Model prompts: `plan/prompts/relevance_prompt.md`, `plan/prompts/coder_prompt.md`, `plan/prompts/coder_prompt_reworded.md`.

**Reliability.** Krippendorff's alpha, floor 0.8. Sample: all segments (stability); a random sample of 180 segments, 20 per network × phase (human spot check, A35). If below: If stability or model–checker alpha for a variable is below .80, its codebook entry is revised once and the variable recoded under the same protocol (and the spot-check sample re-compared); if it is still below, the variable is reported as unreliable, the procedures that use it are reported as descriptive only, and the change is logged in deviations.json before any analysis that uses it (A17).

**Multiple comparisons.** Decisions rest on intervals for contrasts fixed a priori, not on significance tests; no correction for multiple tests is applied.  **Missing data.** Airings without captions are counted by network and phase and left out; no imputation. Segments not relevant (V0 = no) are counted and dropped before P1–P5; segments with no frame stay in every denominator and in V8.

## Pre-registration counts and interval-width simulation (A34)
Before registration, the authors retrieved only counts of airings whose captions match the keyword filter (no caption text), by network and phase, from the TV News Archive's public search on October 17, 2026 (`code/a34_hit_counts.py`, `data/a34_hit_counts.csv`). The Archive's index reported 555 matching airings; 507 were retrievable through its public search.

Matching airings by network and phase (the broadcast window, February 8–10, 2026, lies inside the performance phase):

| Network | announcement | build-up | performance with aftermath | broadcast window |
|---|---|---|---|---|
| CNN | 62 | 120 | 86 | 43 |
| Fox News | 18 | 50 | 40 | 25 |
| MSNBC | 39 | 49 | 41 | 18 |

Simulated 95% interval half-widths for the change in corrected mean pairwise divergence from the announcement phase (P2/P3), 500 bootstrap draws over airings, seed 20261017 (`code/a34_width_sim.py`, `data/a34_width_sim.json`; settings A38):

| Scenario | segments/airing | relevant | differences | Δ build-up | Δ performance with aftermath | Δ broadcast window |
|---|---|---|---|---|---|---|
| S1 | 1.5 | 0.6 | none | ±0.122 | ±0.126 | ±0.171 |
| S2 | 3.0 | 0.7 | none | ±0.062 | ±0.065 | ±0.083 |
| S3 | 3.0 | 0.7 | moderate | ±0.069 | ±0.065 | ±0.094 |
| S4 | 6.0 | 0.8 | moderate | ±0.053 | ±0.057 | ±0.059 |

**Statement required by the plan (A34).** In every simulated scenario and every phase, the interval half-width for the change from the announcement phase exceeds the ±.05 band (A14). Under these counts, a change can meet the decision rules only if it is larger than roughly .05–.17 in divergence units, depending on segments per airing; a smaller change is classed "none" under the decision rules, as the plan already specifies. The sensitivity bands (±.025, ±.10) are kept as planned.

## Ethics
No human subjects. TV News Archive terms (A1 open); licensed-transcript terms (A2 open); aired names kept as aired, never joined or re-identified; the release holds identifiers and codes, never caption text (A4 open). Personal data: pseudonymised public text.

## Deviations
X1 (registry: Zenodo instead of OSF), decided by the authors before any caption text was retrieved. Any further departure from this plan is logged in `deviations.json` before the affected run and reported in the Method and Limitations.
