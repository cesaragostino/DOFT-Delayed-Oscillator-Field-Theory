# Study 01 — Superconductors and Superfluid Helium

## Status

**Published exploratory study; extracted into the DOFT central index.**

This page is the central, website-ready overview of Study 01. It does not copy
the source repository or its datasets. Detailed results, qualifications, and
provenance are maintained in:

- [`findings.md`](./findings.md)
- [`research-log.md`](./research-log.md)

## Source record

| Item | Record |
| --- | --- |
| Source repository | [`cesaragostino/doft-study01-superconductors`](https://github.com/cesaragostino/doft-study01-superconductors) |
| Repository snapshot reviewed | `fa71d6641429d2d4f45ae3d607fa0a784f306a71` |
| Published artifact | [Zenodo v1.0](https://doi.org/10.5281/zenodo.17620713) |
| Publication date | 2025-11-16 |
| Central extraction date | 2026-07-24 |

For the published study, the Zenodo v1.0 package is the canonical snapshot.
The source repository contains later work that was not part of that release.

## Research question

Can a fixed, constrained prime-space locking grammar compress a curated set of
superconducting and superfluid energy-scale ratios without fitting separate
parameters to every material?

The study compares observed scale ratios with nearby products of the primes
`{2, 3, 5, 7}`. It also tests a constrained thermal–memory correction
calibrated on Type I and Type II superconductors, then reused across material
families.

## Website synopsis

Study 01 found reproducible descriptive patterns within its imposed locking
grammar: the prime `2` dominates integer fingerprints, rational-denominator
distributions vary across material categories, the fitted curvature term is
effectively zero, and the additional κ correction changes only the MgB₂
subnetwork. These are exploratory regularities in a curated dataset and a
constrained algorithm; they are not evidence by themselves that DOFT is a
fundamental physical theory.

## Dataset and pipeline

- 252 material or subnetwork rows representing 221 named materials.
- 9 material categories, including 4 superfluid rows.
- Three within-row transitions: thermal at `Tc → gap`, `gap → Debye`, and
  `Debye → EF`, plus selected inter-band or subnetwork contrasts.
- Integer locks are products of `{2, 3, 5, 7}`.
- Rational locks use `p/q` with `q` restricted to `1..8`.
- The correction parameters satisfy `Γ ≥ 0` and `η ≥ 0`.
- Calibration uses Type I and Type II superconductors, 500 bootstrap
  resamples, and winsorization caps of 400, 600, and 800.

The published material reports 621 calibration jumps, 175 cluster jumps, and
796 factorized rows: 327 complete integer locks and 469 rational locks. The
archive contains the input, pipeline, figures, and aggregate summaries, but
not the generated row-level result CSV files.

## Main findings

| Finding | Result | Interpretation |
| --- | --- | --- |
| Integer fingerprint | Mean exponents `(2, 3, 5, 7) ≈ (1.50, 0.65, 0.45, 0.26)` across 327 rows | Prime `2` is the dominant basis factor in this constructed representation. |
| Rational locks | Mean `q` ranges from 2.06 for superfluids to 5.89 for high-pressure superconductors | Category-level structure is descriptive, but `q ≤ 8` and lock-family assignments are imposed by design. |
| Global correction | `Γ` is effectively zero; `η` changes with the winsorization cap and an unseeded bootstrap | The release does not establish a unique or exactly reproducible universal correction coefficient. |
| κ refinement | Only 6 of 175 cluster rows change, all from MgB₂; none of the 796 lock assignments change | κ behaves as a local MgB₂ refinement, not a dataset-wide mechanism. |
| Residual structure | Several category/subnetwork groups cluster near zero; others remain displaced | The grammar compresses some groups better than others and leaves structured exceptions. |

## Central assessment

Study 01 is strongest as a reproducible exploratory compression pipeline. It
provides concrete fingerprints, a frozen-calibration workflow, and inspectable
summary outputs.

Its evidence for a universal thermal–memory correction is limited by
preassigned lock families, constrained denominator range, sensitivity to the
winsorization cap, unseeded calibration, dependent jumps within each material,
and unresolved analysis inconsistencies. The study does not validate the
broader historical claims about a Mother Frequency or electroweak-scale
universality.

## Historical note

An earlier central-repository report made broader claims under the title
“Mother Frequency and Thermal–Memory Shift.” It predates this evidence review
and is now preserved only as a
[historical precursor](../../archive/study-01-early-theory/STUDY_01_MotherFrequency_and_ThermalMemoryShift.md).
