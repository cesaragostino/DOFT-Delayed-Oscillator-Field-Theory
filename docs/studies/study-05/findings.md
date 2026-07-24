# Study 05 — Extracted Findings

This document separates direct artifact evidence, central reanalysis, and
unsupported interpretation for Study 05.

## Evidence labels

- **Direct artifact:** directly present in the published code, configuration,
  aggregate data, paper, or archive metadata.
- **Reanalysis:** independently recomputed during this central extraction.
- **Descriptive only:** a real pattern in the generated output whose physical
  cause is not identified.
- **Invalidated:** the released implementation or analysis does not perform
  the experiment represented by the claim.
- **Unresolved:** not testable from the archived material.

## 1. Published scope and actual scope

The Zenodo paper is titled *Coherence Scaling in Hierarchical Oscillator
Networks: Power-Law Decay, Memory Overhead, and Topological Constraints with
Parallels to Disordered Condensed Matter*. It presents a generic simulated
network and explicitly calls the vortex-matter mapping phenomenological.

The source repository also contains a Standard Model universe and
particle-matching machinery. Those components do not validate the final
results:

- final Ola1 selection sets `require_match` to false;
- the 298 canonical input blocks carry oscillator parameters, grades, and
  provenance hashes, but no required particle identity;
- the reported Ola2–Ola4 metrics do not compare against particle,
  superconducting, or subquark observations.

**Assessment — Direct artifact.** The published study concerns a synthetic
network pipeline. It provides no evidence for internal strings below quarks.

## 2. Aggregate dataset

The consolidated CSV has 4,323 unique entity IDs and 36 columns.

| Stage | Aggregate rows | Actual candidates | Swept | Promoted | Retained grades |
| --- | ---: | ---: | ---: | ---: | --- |
| Ola2 | 323 | 323 | 323 | 323 | A: 183; B: 140 |
| Ola3 | 3,000 | 402 | 402 | 118 | B: 118; C: 210; F: 74; U: 2,598 |
| Ola4 | 1,000 | 462 | 462 | 7 | B: 7; C: 129; F: 326; U: 538 |
| **Total** | **4,323** | **1,187** | **1,187** | **448** | |

The package README calls `paper_metrics_all.csv` a table of all 1,187 promoted
entities. Both parts are incorrect: it contains 4,323 entities, 1,187 swept
entities, and 448 promoted entities. The summary JSON similarly names 4,323 as
`candidates_total`, although the candidate flag is true for 1,187 rows.

**Assessment — Direct artifact.** The aggregate is internally usable once its
row populations are reconstructed. Published descriptions of those
populations should not be used as denominators without correction.

## 3. Decisive coupling defect

The published sweep configuration defines and varies `kappa_global`. The
parameter resolver preserves that name and passes the resulting dictionary
directly into `DifferentialNetwork`.

The differential integrator reads:

`engine_params.get("K_global", 0.0)`

It never reads `kappa_global`, and no translation between the two names exists
on the released sweep path. Consequently, `self.k_global` resolves to zero and
the delayed inter-node force is multiplied by zero.

An independent dynamic check instantiated the published integrator with three
identical input blocks, one seed, and two different graphs:

| Parameter dictionary | Resolved coupling | Ring/path result |
| --- | ---: | --- |
| Published key, `kappa_global: 0.30` | `0.0` | All scalar metrics exactly identical |
| Solver key, `K_global: 0.30` | `0.3` | Coherence metrics differ by topology |

For example, with the published key both graphs returned
`R_network_S1_mean_lastW=0.5637601403`. With the solver key, the two values
were approximately `0.6319720` and `0.6423570`.

The archived aggregate does not include raw evaluation records or time series,
so it cannot independently prove which executable produced every published
row. Under the released code and configuration, however, the claimed
nonzero-coupling experiment cannot be reproduced. If a different executable
was used, that executable and its seed-level evidence are absent from the
publication package.

**Assessment — Invalidated.** The published results cannot establish a
coordination cost, delayed network interaction, or topology-dependent
differential dynamics in coupled networks.

## 4. Raw global-coherence curve

The 1,187 swept rows contain finite global coherence values for `N=2–12`.
Their per-size means are:

| `N` | Swept entities | Mean global `R` |
| ---: | ---: | ---: |
| 2 | 180 | 0.66976 |
| 3 | 59 | 0.57151 |
| 4 | 75 | 0.51037 |
| 5 | 9 | 0.48882 |
| 6 | 245 | 0.44671 |
| 7 | 39 | 0.42312 |
| 8 | 66 | 0.40838 |
| 9 | 114 | 0.39776 |
| 10 | 210 | 0.39254 |
| 11 | 35 | 0.38423 |
| 12 | 155 | 0.37626 |

A log-linear fit to these 11 means reproduces
`R ≈ 0.8134 × N^-0.32165`, with `R²=0.98690`. The paper's seeded bootstrap is
also reproducible, with a mean exponent near `0.318` and a 95% interval of
approximately `[0.276, 0.348]`.

This fit has four important limits:

1. Inter-node coupling is zero in the released differential sweep.
2. Global phasor magnitude has a positive finite-size baseline even for
   independent random phases. An illustrative uniform-phase Monte Carlo gives
   an effective exponent near `0.51` over the same sizes.
3. Network size is strongly confounded with pipeline stage, recursively
   selected input blocks, templates, and explorer thresholds.
4. The paper's own model comparison prefers an exponential with offset
   (`AIC=-107.8`, `BIC=-106.6`) to the power law (`AIC=-99.2`,
   `BIC=-98.4`).

The one shared size, `N=9`, is similar between Ola3 and Ola4
(`0.3953` versus `0.3998`; `p≈0.266`), but one overlap cannot remove the
remaining stage confounding.

**Assessment — Descriptive only.** The archived `R(N)` curve is reproducible.
Its interpretation as a universal coordination-cost exponent is invalidated
by the coupling defect and is not uniquely supported as a power law.

## 5. Topology claim and metric substitution

The paper defines:

- global coherence `R` as the late-time phasor magnitude from the
  differential sweep;
- lock score `L` as `R_mean_lastW` from the explorer, operationally distinct
  from `R`.

The aggregate confirms that distinction: for the 1,187 swept entities,
Pearson `r(R,L)=0.00386` with `p=0.894`.

The topology-heatmap script calls a selector that prefers
`R_mean_lastW_mean`—that is, `L`—before `R_network_S1_mean`. It then applies a
threshold of `0.85` and labels the result “Coherence rate (`R ≥ 0.85`).”

Actual global `R` spans approximately `0.3115–0.7526`; zero of 1,187 swept
entities has `R≥0.85`. The nonzero published heatmap is therefore a heatmap of
`L≥0.85`, not the stated global-coherence event.

Even without that substitution, released differential outputs cannot test
edge topology because their inter-node coupling is zero. Within a fixed `N`,
mean global-`R` spreads across named templates range from zero to about 0.013;
those differences can arise from recursively selected node composition and
sampling, not edge interaction.

**Assessment — Invalidated.** The published ring-collapse and
bipartite-survival result is not a test of the claimed `R` threshold and is not
a topology effect in the released differential model.

## 6. Memory-layer interpretation

The published memory discussion contains two different analyses.

### Within-size correlation

When the intended global `R` is used, Spearman correlation between S2 share and
`R` is negative at some small sizes and near zero at most large sizes:

| `N` | `ρ(S2,R)` | `p` |
| ---: | ---: | ---: |
| 2 | −0.224 | 0.0025 |
| 4 | −0.520 | <0.00001 |
| 6 | −0.011 | 0.858 |
| 7 | −0.326 | 0.043 |
| 8 | +0.061 | 0.624 |
| 9 | +0.094 | 0.319 |
| 10 | +0.034 | 0.628 |
| 11 | +0.096 | 0.585 |
| 12 | +0.023 | 0.772 |

This is a real aggregate pattern, although the low-size sequence is not
monotonic and most individual correlations are not significant.

### Main mechanism figure

The published mechanism-residual figure again uses the selector that prefers
`L`, then labels its residual as global coherence `R`. Its reported near-zero
slope is approximately `−0.00327` with `p≈0.407`.

Using global `R` instead gives a small negative residual slope of approximately
`−0.00727`, Pearson `r≈−0.072`, and `p≈0.0129`. This small association does
not establish causation, but it shows that the published “zero direct effect”
result is metric-dependent.

Promoted high-`N` entities also do not consistently have greater S2 share.
At `N=7`, `8`, `10`, and `12`, the promoted mean is lower than the
non-promoted mean; at `N=9` it is higher, but only one entity is promoted.
The survivor counts above `N=6` are too small and inconsistent to support an
enabling mechanism.

**Assessment — Descriptive correlation only.** A change from negative to
near-zero correlation may be recorded as a generated-data observation.
Memory as stabilization overhead or an enabling condition is not established.

## 7. Phase dispersion

The phase-variance interquartile range grows from approximately
`6.6×10^-9` at `N=2` to `1.14×10^-3` at `N=6`,
`2.20×10^-3` at `N=7`, and `2.44×10^-3` at `N=9`. Larger networks therefore
show much greater dispersion in the archived metric.

The paper interprets the rise around `N=6–7` as coexistence near a topological
transition. The metric is reproducible, but the causal interpretation is not:
the differential graphs are uncoupled, and size changes together with stage,
node library, and sampling policy.

**Assessment — Descriptive only.** The heterogeneity increase is retained as
an output property, not as evidence of a critical or topological transition.

## 8. Promotion funnel and incomparable denominators

Ola2 sets `emit_non_candidates: false`; Ola3 and Ola4 set it to true.
Therefore:

- the 323 Ola2 rows are selected candidates retained from a budget of 5,000
  attempts;
- the 3,000 Ola3 rows and 1,000 Ola4 rows include both candidates and
  non-candidates.

The published 100%, 3.9%, and 0.7% promotion rates divide by these different
row populations. Among actual candidates, the retained rates are:

- Ola2: 323/323, while 4,677 rejected attempts are absent;
- Ola3: 118/402, or approximately 29.4%;
- Ola4: 7/462, or approximately 1.52%.

Explorer gates also tighten across stages:

| Stage | Minimum `L` | Maximum phase variance | Minimum quality |
| --- | ---: | ---: | ---: |
| Ola2 | 0.75 | 0.05 | 0.70 |
| Ola3 | 0.88 | 0.03 | 0.85 |
| Ola4 | 0.89 | 0.02 | 0.89 |

**Assessment — Invalid as a common survival curve.** The declining counts are
real, but they combine growing networks, recursive selection, different
thresholds, and different output policies.

## 9. Model-description mismatch

The paper describes first-order three-layer phase equations, places
inter-node delayed coupling on the `Q` layer, and says global phase is
extracted from `Q`.

The released differential sweep implements multi-mode, second-order damped
oscillators with position, velocity, auxiliary memory, and structural state.
Its intended inter-node force is computed from `S1` phases, not `Q`. Several
declared sweep parameters are not consumed by this differential-network
constructor, and the coupling parameter it does consume is misnamed upstream.

**Assessment — Invalidated as documented reproducibility.** The mathematical
model in the publication is not the model represented by the released
integrator.

## 10. Archive and reproducibility

The official Zenodo ZIP is byte-identical to the repository's
`zenodo_v1.zip`. It contains:

- the 9-page paper and figures;
- 75 Python files across `src/` and `scripts/`;
- 35 JSON configuration files;
- four aggregate or genome CSV files;
- Ola1 canonical blocks and DNA catalogs.

All 75 Python files parse, and all 38 substantive JSON files inspected are
valid JSON. There is no automated test suite. The declared requirements list
only NumPy and Matplotlib, while figure generation also imports pandas,
SciPy, and seaborn, and other source paths use additional undeclared
dependencies.

The archive omits raw explorer attempts, candidate JSONL files, seed-level
sweep evaluations, and time series. Its “complete numerical dataset” wording
therefore overstates what can be independently audited without rerunning the
multi-day pipeline.

**Assessment — Direct artifact.** Archive integrity is verified, but the
publication is an aggregate-results package rather than a complete
reproduction record.

## 11. Post-publication extension

The current repository has one commit after the v1.0 package. It adds a
constructed proxy:

`E_disorder = (1 - R) × H_part`

and fits that quantity against `ln N`, reporting a strong relation and a
Bragg-glass analogy. This proxy contains `R` by definition, while `R` already
changes with `N`; it is fitted to 11 per-size means and has no independent
validation. The extension does not fix the coupling key or topology heatmap.

**Assessment — Unresolved, post-publication lead.** It is not part of Zenodo
v1.0 and is not retained as a finding.

## 12. Overall conclusion

- **Supported:** a large recursive pipeline; a verified publication snapshot;
  a 4,323-row aggregate; exact descriptive counts; the raw `R(N)` curve; and a
  strong rise in generated phase dispersion.
- **Useful as diagnostics:** stage-dependent promotion counts, within-size
  S2 correlations, and the post-publication proxy as prompts for redesigned
  experiments.
- **Invalidated by the released implementation or analysis:** nonzero delayed
  network coupling, topology-dependent survival, the `R≥0.85` heatmap, and
  the main memory-residual inference.
- **Not established:** a universal scaling law, a memory-enabling mechanism,
  a vortex-matter correspondence, a critical topology ceiling, or internal
  strings below quarks.
- **Needed next:** correct and test the coupling interface; align paper and
  implementation; retain raw seed-level evidence; define comparable stage
  populations; add uncoupled and random-phase controls; preregister metrics
  and thresholds; and rerun before drawing physical conclusions.
