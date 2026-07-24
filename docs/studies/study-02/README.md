# Study 02 — Structural Noise and Cluster Oscillator Model

## Status

**Published exploratory study; extracted into the DOFT central index.**

This page is the central, website-ready overview of Study 02. It does not copy
the source repository, code, datasets, or generated outputs. Detailed results,
qualifications, and provenance are maintained in:

- [`findings.md`](./findings.md)
- [`research-log.md`](./research-log.md)

## Source record

| Item | Record |
| --- | --- |
| Source repository | [`cesaragostino/doft-study02-structural-oscillator`](https://github.com/cesaragostino/doft-study02-structural-oscillator) |
| Repository snapshot reviewed | `b5deb6296d7127c4e992321fb5a628029ded445e` |
| Published package commit | `cf0b0da0cd1053a580955e4cda653524090ac034` |
| Published artifact | [Zenodo v1.0](https://doi.org/10.5281/zenodo.17784477) |
| Publication date | 2025-12-01 |
| Central extraction date | 2026-07-24 |

The Zenodo record is the canonical published artifact. The listed package
commit contains that release; the current repository adds preliminary Study 04
material but does not change the published Study 02 package.

## Scope boundary

The source repository contains two research layers:

1. **Study 02 core:** structural-noise construction, per-material cluster
   configuration, algebraic simulator, sensitivity summaries, and validation.
2. **Study 03 crossover:** integer participation, null comparisons, and
   coherence-length analysis.

The Zenodo paper combines both layers under the title *Integer participation
and structural noise in superconducting clusters*. This extraction evaluates
the full published artifact but does not silently reclassify the participation
analysis as a Study 02 result. It remains here only because it is inseparable
from the Study 02 publication archive. No standalone Study 03 conclusions are
retained, following the author's direction.

## Research question

Can differences between the prime-lock fingerprints of material subnetworks be
represented as a structural-noise field, and can a layered cluster model use
that field to recover family-specific thermal, spatial, and pressure patterns?

## Website synopsis

Study 02 produced a complete, executable pipeline that turns between-subnetwork
prime-lock mismatches into a structural-noise variable and fits a layered
cluster representation across 138 materials. Its strongest result is an
inspectable computational framework and a set of model-derived hypotheses.
The current outputs do not independently establish the claimed binary
surface-dissipation or iron-based core-coupling mechanisms: those topologies
are partly encoded in the configuration rules, and the reported correlations
are weak or mixed.

The accompanying integer-participation analysis is best treated as a Study 03
crossover record, not a retained conclusion. Its published null test does not
recalibrate family frequencies for each null sample as the manuscript
describes. When that recalibration is performed, the global deviation from
integer participation is not conventionally significant.

## Dataset and pipeline

- 268 rows representing 234 named materials in 9 categories.
- Full Study 01 v7 inputs and processed outputs are included in the published
  package.
- Structural noise is defined for 20 multi-subnetwork materials and propagates
  to 45 dataset rows.
- The simulator generates 690 result rows: 138 materials × 5 seeds.
- Each per-material fit tunes 21 continuous parameters against a compact target
  representation.
- The published package contains 3,548 substantive files after excluding
  macOS metadata and Python bytecode caches.
- The implementation test suite passes all 8 tests.

## Main findings

| Finding | Result | Interpretation |
| --- | --- | --- |
| Structural-noise coverage | 20 unique multi-subnetwork materials; 45 affected dataset rows | The proposed noise field is a small, non-random subset of the full dataset. |
| Noise correction | For affected rows, `Tc_ideal / Tc` has median 1.639 and maximum 2.415 | This is a model-defined transformation, not an independently measured correction. |
| Family topology | Binary and iron-based correlation summaries are weak or mixed | Current output does not support the paper's strong skin/core mechanism claims. |
| Pressure pattern | Optimized high-pressure terms change sign between lower and higher prime layers | A descriptive model pattern worth testing; not yet an empirical pressure law. |
| LOO validation | Mean absolute error is reported for 18 binary or iron-based cases | The test predicts held-out configurations from family means; it does not refit and predict held-out physical observations. |
| Model selection | One 21-parameter model is assigned AIC/BIC values | With no comparator and no likelihood calculation, this does not validate model complexity. |
| Integer participation | Published empirical null count is zero of 1,000; recalibrated-null audit gives `p=0.059` or `p=0.14` | The strong locking claim depends on an asymmetric null comparison. |
| Coherence length | `N ∝ ξ₀^0.434`, `R²=0.455`, `n=10`, `p=0.032` | An interesting small-sample association with unstable leave-one-out behavior. |

## Central assessment

Study 02 is strongest as research infrastructure: the archive is complete, the
code executes, outputs are extensive, and the pipeline makes its assumptions
inspectable. It generates concrete hypotheses about subnetwork mismatch,
layer-specific effects, and pressure response.

The scientific claims require a more prospective test. Family profiles,
geometry weights, and the iron-based inversion are partly hard-coded; the
structural-noise target is derived from the same ratios used to construct its
predictor; the per-material model is highly flexible; and the packaged
validation does not test prediction of independent observations. The current
evidence therefore supports an exploratory model, not a validated physical
mechanism.
