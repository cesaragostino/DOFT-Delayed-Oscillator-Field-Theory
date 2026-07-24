# Study 05 — Hierarchical Oscillator Networks

## Status

**Published computational study; extracted into the DOFT central index. Its
principal physical conclusions are not retained as validated findings.**

This page is the central, website-ready overview of Study 05. It does not copy
the source repository, code, datasets, generated outputs, or Git history.
Detailed evidence and provenance are maintained in:

- [`findings.md`](./findings.md)
- [`research-log.md`](./research-log.md)

## Source record

| Item | Record |
| --- | --- |
| Source repository | [`cesaragostino/doft-study05-internal-string-layers-below-quark`](https://github.com/cesaragostino/doft-study05-internal-string-layers-below-quark) |
| Repository snapshot reviewed | `554100c88b38d7f67b1fd3a65fa23769db3e7234` |
| Published package commit | `36ff63cdd81e39efe343bbd6d94335898116949b` |
| Published artifact | [Zenodo v1.0](https://doi.org/10.5281/zenodo.18200973) |
| Publication date | 2026-01-09 |
| Central extraction date | 2026-07-24 |

Zenodo v1.0 is the canonical publication. The repository has one later commit
that adds a memory-weighted disorder proxy and revised paper material; that
post-publication extension is recorded separately and is not treated as part
of v1.0.

## Scope boundary

The source repository name proposes internal string layers below the quark
scale. The published result does not test that proposal. Its final paper
studies synthetic hierarchical oscillator networks with 2–12 nodes and offers
a phenomenological analogy to vortex matter.

The package includes particle-matching infrastructure and a Standard Model
reference universe, but the final Ola1 selection has `require_match: false`.
No subquark observation, string-scale dataset, particle-spectrum fit, or
superconducting measurement is used to validate the reported network results.

The central title therefore describes what the released experiment actually
contains. The source-repository title remains preserved in the source record.

## Research question

How do global phase order, memory participation, topology, and promotion rates
change as recursively constructed oscillator networks grow from 2 to 12
nodes?

## Website synopsis

Study 05 built a substantial recursive search, simulation, classification, and
publication pipeline. Its released aggregate contains 4,323 entities, of which
1,187 were evaluated by the differential sweep and 448 were promoted.

The raw mean global order parameter decreases smoothly with node count, and
the published per-size values reproduce an effective fit
`R ≈ 0.81 × N^-0.322`. That curve is a valid description of the archived
numbers, but it is not evidence for a coordination cost in coupled networks.
The released sweep passes the parameter `kappa_global`, while its differential
integrator reads only `K_global`; the effective inter-node coupling is
therefore zero under the published configuration.

Two additional analysis defects change the meaning of the principal figures.
The topology heatmap uses the operational explorer score `L` while labelling
it global coherence `R`, and the main memory-residual figure makes the same
substitution. No swept entity has the global `R ≥ 0.85` required by the
published topology caption.

Study 05 is therefore retained as a useful record of model and pipeline
development, a reproducible aggregate dataset, and a source of diagnostic
lessons. Its claimed topology ceiling, memory-enabling mechanism, coupled-
network scaling law, vortex correspondence, and below-quark interpretation
are not established by the released experiment.

## Dataset and pipeline

- 4,323 aggregate entity rows across Ola2–Ola4.
- 1,187 entities with finite differential-sweep results.
- 448 promoted entities: 323 in Ola2, 118 in Ola3, and 7 in Ola4.
- Network sizes from `N=2` through `N=12`.
- Ring, complete, ladder, and bipartite templates.
- Four deterministic sweep seeds per selected entity.
- An Ola1 library of 298 canonical oscillator blocks.
- A published package with code, configuration, paper sources, figures,
  aggregate metrics, and genome-layer summaries.
- No archived raw attempts, seed-level evaluations, or time series.

## Main findings

| Finding | Audited result | Central interpretation |
| --- | --- | --- |
| Raw coherence trend | Per-`N` means reproduce `α=0.3216` with log-fit `R²=0.9869` | Descriptive aggregate pattern only; the released differential network has zero inter-node coupling. |
| Scaling form | The paper's own comparison prefers an exponential with offset over the power law by AIC and BIC | `α≈0.32` is an effective summary over `N=2–12`, not a unique or asymptotic law. |
| Topology | Published heatmap uses `L≥0.85`, not global `R≥0.85`; actual global `R` ranges from 0.311 to 0.753 | The claimed ring collapse and bipartite survival are not established. |
| Memory | Global `R` and `L` are nearly uncorrelated; the main residual plot uses `L` while calling it `R` | A weak change in within-`N` correlation is visible, but memory as an enabling mechanism is unsupported. |
| Phase dispersion | Phase-variance IQR rises sharply between small and larger networks | A reproducible generated-data pattern, not evidence of a topological transition under an uncoupled sweep. |
| Promotion funnel | Retention falls from 323 to 118 to 7, but stages use different thresholds and output policies | The percentages are not comparable estimates of a physical survival probability. |
| Below-quark layers | No final validation uses subquark or particle data | No below-quark conclusion is retained. |

## Central assessment

The most durable Study 05 result is methodological: it demonstrates the need
to verify parameter wiring, metric identity, null scaling, stage denominators,
and publication-to-code correspondence before interpreting a generated
pattern physically.

The aggregate files and per-size curve remain useful for diagnosing the
released pipeline. A scientific rerun would need a corrected and tested
coupling interface, a model specification that matches the implementation,
raw seed-level outputs, preregistered stage rules, explicit uncoupled and
random-phase controls, and figures that bind each label to the intended
metric. Only then could topology, memory, or physical analogies be reassessed.
