# Study 05 — Research Log

## Extraction scope

This log records how Study 05 was incorporated into the central DOFT
repository. It is an evidence extraction, not a repository import: no source
code, Git history, dataset, generated output, figure, or nested repository has
been copied here.

Study 06 was not inspected or modified. Studies 03 and 04 are recorded in the
central index as having no valid conclusions retained, following the author's
direction.

## Sources reviewed

| Source | Role | Status |
| --- | --- | --- |
| [GitHub source repository](https://github.com/cesaragostino/doft-study05-internal-string-layers-below-quark) | History, source, configurations, generated data, paper revisions, and packaged releases | Reviewed through `554100c88b38d7f67b1fd3a65fa23769db3e7234` |
| [Zenodo record 18200973](https://doi.org/10.5281/zenodo.18200973) | Canonical published v1.0 preprint | Reviewed |
| Official Zenodo `zenodo.zip` | Published code, configurations, aggregates, figures, and paper source | Downloaded and verified |
| Official Zenodo `main.pdf` | Canonical claims and presentation | Downloaded, text-extracted, rendered, and visually checked |
| Source history | Evolution of the research question and pipeline | Reviewed across 219 commits |

The local source worktree already contained an untracked `migrate/` directory.
It was not read as canonical evidence, modified, staged, or removed. All
verification work used tracked snapshots or temporary copies outside both
repositories.

## Canonical-version decision

Zenodo v1.0 corresponds to source commit
`36ff63cdd81e39efe343bbd6d94335898116949b`, dated 2026-01-09. The current
source `main` is one commit later. That 2026-01-11 commit revises the paper and
adds a memory-weighted disorder proxy.

The official Zenodo ZIP is byte-identical to the source repository's tracked
`zenodo_v1.zip`. The repository's newer `zenodo.zip` and current
`paper/main.pdf` differ from the public release. This extraction therefore
uses:

1. Zenodo v1.0 for canonical published claims;
2. the later commit only for a clearly labelled post-publication note.

## Archive integrity

- Official ZIP size: 6,511,803 bytes.
- Official ZIP MD5: `53ff8cb006c7ec38a93b2184dbeebd0a`.
- Official PDF size: 2,720,487 bytes.
- Official PDF MD5: `bb324db7cd0a0e97c83cc68f8b09fa18`.
- The PDF renders as a readable 9-page paper.
- The ZIP contains 49 macOS metadata entries plus Python bytecode caches.
- Excluding `.DS_Store`, `__MACOSX`, and bytecode caches, the bundle has 136
  substantive files.
- All 75 Python source/script files pass static syntax parsing.
- All 38 inspected JSON files parse successfully.

The package contains aggregate data rather than the full numerical record.
Raw attempts, candidate JSONL, per-seed evaluations, and time series are
absent. A complete bottom-up reproduction requires rerunning the simulation
pipeline; the package README estimates about 14 hours for Ola2–Ola4 and more
than three days including Ola1.

## Verification work

### Aggregate reconstruction

The consolidated CSV was checked for row counts, unique entity IDs, stage
labels, candidate flags, sweep coverage, grades, and promotion flags.

- 4,323 unique entities are present.
- 1,187 are marked as candidates and swept.
- All 1,187 swept rows have finite primary metrics.
- 448 are promoted.
- The README and summary metadata use incorrect population labels, so counts
  were reconstructed from row-level flags.

### Scaling reproduction

Per-`N` means of `R_network_S1_mean` were recomputed from swept rows. A
log-linear regression gives:

- amplitude `0.81336`;
- exponent `0.321646`;
- `R²=0.98690`;
- regression standard error for the exponent `0.01235`.

The paper's 2,000-sample, seed-42 bootstrap was also reproduced, yielding an
exponent interval approximately `[0.276, 0.348]`.

The source paper's AIC/BIC comparison was inspected rather than silently
accepting the power-law presentation. Its exponential-with-offset model is
preferred over the power law on both criteria.

### Coupling-interface audit

The full parameter path was traced from JSON configurations through bin
resolution, sweep construction, and the differential integrator.

- Configurations and the resolver use `kappa_global`.
- `DifferentialNetwork` reads `K_global`, defaulting to zero.
- No adapter maps one name to the other.
- The inter-node force is therefore zero under the released configuration.

A dynamic test used the published integrator, three canonical blocks, the same
seed, and two graphs. With `kappa_global`, resolved coupling was zero and all
scalar outputs were exactly equal. With `K_global`, coupling resolved to 0.3
and the topology outputs diverged.

This was a temporary diagnostic only; no source file was edited.

### Metric-identity audit

The paper and aggregate distinguish global differential-sweep coherence `R`
from explorer lock score `L`. Their measured correlation is essentially zero.

Figure-generation paths were traced individually:

- the scaling figure correctly uses global `R`;
- the topology heatmap calls a selector that prefers `L`, then labels it `R`;
- the main binned memory-residual figure also uses `L` while labelling the
  residual `R`;
- the published Appendix C Spearman-by-`N` figure explicitly selects global
  `R` and is not affected by that substitution.

This distinction matters: no swept row reaches global `R=0.85`, while many
rows reach the explorer `L` threshold used by the topology heatmap.

### Memory and topology reanalysis

The three genome-layer CSVs were merged one-to-one with the aggregate using
entity ID, and S2 share was reconstructed as:

`pS2_mean / (pS1_mean + pS2_mean)`

Within-`N` Spearman values, promoted/non-promoted S2 means, residual slopes,
and per-topology global-`R` means were recomputed. This confirmed:

- a negative-to-near-zero correlation pattern at several sizes;
- no consistent elevation of S2 among high-`N` survivors;
- a small negative global-`R` residual association;
- no entity satisfying the heatmap's stated global-`R` threshold;
- only small within-size differences in global-`R` means among topology
  labels.

### Finite-size null

An illustrative fixed-seed simulation of independent uniform phases was run
for `N=2–12`. Its expected phasor magnitude also decays with `N`, with an
effective exponent near 0.51 over this short range.

This is not proposed as a complete null for the hierarchical oscillator
library. It establishes that raw phasor magnitude requires a finite-size
baseline before its decay can be attributed to a coordination mechanism.

### Stage-denominator audit

Explorer configurations were compared across stages. Ola2 omits rejected
attempts, while Ola3 and Ola4 retain them, and their acceptance thresholds
tighten. Published promotion percentages therefore do not share a common
denominator or gate.

### Model-to-code audit

The paper's Appendix A equations were compared with the released physics and
differential-engine modules. The paper describes first-order phase dynamics
and delayed coupling on `Q`; the code implements second-order multi-mode
dynamics and intends inter-node coupling on `S1`.

The publication package has no automated test suite capable of detecting this
specification mismatch or the coupling-key defect.

## Study timeline

| Date | Event |
| --- | --- |
| 2025-12-05 | Repository and early layered-model iterations begin. |
| 2025-12-08 | Ola1 is marked complete and the engine refactor begins. |
| 2025-12-15 to 2025-12-18 | Several mass, energy, and Standard Model proxy attempts are developed; some internal reports explicitly reject intermediate hypotheses. |
| 2025-12-18 to 2025-12-23 | Explorer, spin, DNA, species, and particle-matching paths evolve. |
| 2025-12-23 | The pipeline is redirected toward DNA-style structure without requiring Standard Model matching. |
| 2025-12-26 | Taxonomy and promotion logic are consolidated. |
| 2025-12-28 to 2026-01-01 | Recursive Ola pipeline and larger-network stages are completed. |
| 2026-01-02 to 2026-01-07 | The hierarchical-network paper and final figures are developed. |
| 2026-01-05 | Ola1 empty-run bugs are fixed during paper preparation. |
| 2026-01-09 | Zenodo v1.0 package is committed and published. |
| 2026-01-11 | A post-publication paper revision adds a memory-weighted disorder proxy. |
| 2026-07-24 | Study 05 is extracted into the DOFT central index. |

## Method-evolution note

The repository explores many candidate interpretations—particle matching,
mass and energy proxies, species classification, recursive blocks, coherence
scaling, topology, and condensed-matter analogies—before settling on the
published question. This is normal exploratory activity, but it creates
substantial researcher degrees of freedom.

Future confirmation should freeze the model equations, parameter names,
metrics, thresholds, stage populations, topology comparisons, and physical
mapping before producing new results.

## Extraction decisions

1. **Zenodo v1.0 is the canonical publication.** Later source material is
   labelled post-publication.
2. **The central title follows the performed experiment.** The source name is
   preserved, but no below-quark result is implied.
3. **A reproducible aggregate pattern is not automatically a physical
   finding.** The `R(N)` curve is retained descriptively.
4. **The coupling defect is outcome-determining.** Claims requiring interacting
   graph nodes are marked invalidated.
5. **Metrics remain distinct.** Explorer lock score `L` is not relabelled as
   differential-sweep global coherence `R`.
6. **Stage counts use reconstructed populations.** “Attempted,” “candidate,”
   “swept,” and “promoted” are not treated as synonyms.
7. **Archive integrity and archive completeness are separate.** Checksums are
   verified, while missing raw evidence is recorded.
8. **Software checks do not validate scientific claims.** Static parsing and
   deterministic diagnostics establish code behavior only.
9. **The source repository remains the computational home.** The central
   repository contains summaries, provenance, assessments, and links.

## Reproducibility map

| Claim area | Published material | Central assessment |
| --- | --- | --- |
| Package identity | Official ZIP/PDF, repository release ZIP, commit history | Canonical v1.0 identified and checksum-verified |
| Aggregate population | Consolidated CSV and summary JSON | Reconstructed; documentation labels are inaccurate |
| Coherence curve | Per-entity aggregate and figure script | Numerically reproducible; descriptive only |
| Inter-node coupling | Configs, resolver, sweep, integrator | Released parameter path resolves coupling to zero |
| Topology ceiling | Aggregate and heatmap script | Uses `L` as `R`; impossible stated threshold; invalidated |
| Memory correlation | Genome summaries, aggregate, scripts | Some correlation shift is reproducible; enabling inference unsupported |
| Promotion collapse | Flags and explorer configurations | Counts are real; denominators and gates are incomparable |
| Critical heterogeneity | Aggregate phase variance and scripts | Reproducible output pattern; causal transition unsupported |
| Model equations | Paper Appendix A and released source | Material mismatch between specification and implementation |
| Complete reproduction | Code/config/aggregate package | Raw attempts, evaluations, and time series absent |
| Vortex analogy | Paper discussion and references | Phenomenological suggestion, not validated by the released experiment |
| Below-quark interpretation | Source name and legacy matching infrastructure | No final evidentiary test |

## Requirements for a valid rerun

1. Choose one canonical mathematical model and make the paper equations match
   the implementation.
2. Replace ambiguous coupling names with a typed, validated configuration
   interface and fail on unknown parameters.
3. Add unit tests proving that changing coupling strength and graph edges
   changes the intended dynamics.
4. Preserve raw attempts, candidate decisions, seed-level evaluations, time
   series, code hashes, and environment metadata.
5. Use the same emission policy, gates, and denominators across stages, or
   report stage-specific estimands explicitly.
6. Bind every figure to named columns and assert metric ranges before
   rendering.
7. Include zero-coupling, random-phase, node-composition, and topology-shuffled
   controls.
8. Compare scaling forms prospectively over a wider size range and account for
   finite-size order-parameter bias.
9. Test memory through controlled ablation rather than survivor correlation.
10. Keep condensed-matter and subquark analogies outside the findings until
    they receive independent empirical tests.
