# Study 02 — Research Log

## Extraction scope

This log records how Study 02 was incorporated into the central DOFT
repository. It is an evidence extraction, not a repository import: no source
code, Git history, dataset, generated output, figure, or nested repository has
been copied here.

The source repository also contains integer-participation work explicitly
described there as a Study 03 add-on and preliminary Study 04 documents. The
published package combines Study 02 and the Study 03 crossover; both were
reviewed, but their ownership remains explicit. Study 04 material was outside
this extraction.

## Sources reviewed

| Source | Role | Status |
| --- | --- | --- |
| [GitHub source repository](https://github.com/cesaragostino/doft-study02-structural-oscillator) | History, active source, tests, specifications, and packaged release | Reviewed through `b5deb6296d7127c4e992321fb5a628029ded445e` |
| [Zenodo record 17784477](https://doi.org/10.5281/zenodo.17784477) | Canonical published v1.0 artifact | Reviewed |
| Zenodo archive `doft-study02-superconductors-zenodo-v1.zip` | Code, data, processed outputs, figures, and paper | Downloaded, verified, and cross-checked |
| Zenodo `main.pdf` and LaTeX source | Published claims, methods, tables, figures, and bibliography | Reviewed |
| Source history before the final package | Method evolution and boundary between studies | Reviewed |

The current source `main` differs from the package commit only by a preliminary
Study 04 addendum. Review of tracked source content used the exact Git snapshot
and did not depend on the state of the local working copy.

## Archive integrity

The uploaded Zenodo directory was checked against the official public
download:

- the downloaded ZIP matches Zenodo's MD5 checksum
  `6a3fba15b3ea5d4f06756c5546cb3b41`;
- the packaged `main.pdf` matches Zenodo's separately published PDF checksum
  `8c82aee1d436b405f679dc39ca04d094`;
- after excluding `.DS_Store` and Python bytecode caches, both the official ZIP
  and local uploaded directory contain 3,548 substantive files;
- relative file names and file contents match across all 3,548 files;
- the package contains 3,509 data files, 20 notebook/code files, 16 paper
  files, and the root README, citation file, and requirements file.

Unlike the Study 01 release, this package includes the full upstream input and
processed-results tree required by the new pipeline. The Zenodo directory is
therefore complete relative to the public archive.

## Verification work

### Implementation tests

The source test suite was run with bytecode and pytest cache creation disabled.
All 8 tests passed. One Python deprecation warning was emitted for
`datetime.utcnow`.

### Participation reproduction

The integer-participation script was rerun in a temporary directory with the
published input, seed 123, 1,000 permutations, bounds `[0.5, 5.0]`, and penalty
`0.001`.

- `participation_summary.csv` matched the published file byte for byte.
- The manifest differed only in absolute versus relative input paths.

This establishes deterministic reproduction of that output under the released
implementation. It does not validate the statistical design of its null test.

### Independent null audit

The manuscript states that the base frequency is recalibrated within every
null sample. The released implementation does not do this, so an independent
audit repeated 1,000 seeded null samples with equal calibration freedom:

- global `ThetaD` shuffle plus per-family recalibration: `p=0.059`;
- within-family `ThetaD` shuffle plus per-family recalibration: `p=0.140`.

The audit outputs were kept outside both the source and central repositories.

### Coherence and plotting checks

The published coherence table was recomputed and gives
`α=0.434 ± 0.168`, `R²=0.455`, `p=0.0324`, and `n=10`. Leave-one-out
regressions were also checked and show substantial sensitivity to individual
materials.

The very small plotted KS and Mann–Whitney p-values were reproduced from the
released plotting procedure. That procedure uses one representative null
without recalibration and performs a many-to-many name merge that expands the
analysis table. Reproduction therefore confirms the code path, not the
inferential claim.

All temporary verification work was kept outside the central repository. The
source repository was not modified.

## Study timeline

| Date | Event |
| --- | --- |
| 2025-11-17 | Initial structural oscillator implementation appears in source history. |
| 2025-11-18 | Structural-noise code is added. |
| 2025-11-19 | Family topology and interpretation documents develop around the new model. |
| 2025-11-21 | First global-frequency integer-participation analysis is added; its initial null result shows no near-integer excess. |
| 2025-11-28 | Participation is redesigned with bounded family-specific bases and identified as a Study 02/03 bridge. |
| 2025-11-29 to 2025-11-30 | Participation, coherence validation, figures, and paper are integrated. |
| 2025-12-01 | The paper is finalized and Zenodo v1.0 is published. |
| 2025-12-02 | The full Zenodo package is committed at `cf0b0da`. |
| 2025-12-03 | Preliminary Study 04 documentation is added without changing the package. |
| 2026-07-24 | Study 02 is extracted into the DOFT central index. |

## Method-evolution note

The first participation report used a global fitted base near 2,950 and found
no excess of real near-integer values over the null. The later formulation
constrained bases to `[0.5, 5.0]`, fitted separate family bases, and compared
`Fm` with `Fm/2`. The final publication reports the later, stronger-looking
result.

This evolution is legitimate exploratory work, but it adds researcher degrees
of freedom. Future confirmation should freeze the hypothesis, bounds,
family definitions, eligibility rules, and null calibration before evaluating
new data.

## Extraction decisions

1. **Zenodo v1.0 is the canonical publication.** The archive is complete and
   is not replaced by later preliminary Study 04 content.
2. **Study ownership remains explicit.** Structural noise and the cluster
   simulator are Study 02; participation and coherence are logged as a Study
   03 crossover.
3. **The source repository remains the computational home.** This central
   repository contains summaries, evidence qualifications, provenance, and
   links only.
4. **A generated field is not called a measurement.** Structural noise and
   `Tc_ideal` are recorded as model-defined transformations.
5. **Encoded topology is distinguished from discovered topology.** Hard-coded
   profiles and the iron-based inversion are part of the result's conditions.
6. **Implementation verification is not scientific validation.** Passing
   tests and deterministic reruns establish software behavior.
7. **Null models receive equal fitting freedom in the central assessment.**
   The recalibrated audit is recorded alongside, not substituted into, the
   published artifact.
8. **Duplicate material names are treated as dependent records.** Statistical
   conclusions cannot assume that many-to-many expanded rows are independent.

## Reproducibility map

| Claim area | Material in the published package | Central assessment |
| --- | --- | --- |
| Dataset and upstream Study 01 results | Complete input and processed trees | Directly inspectable; row-level bibliography remains incomplete |
| Structural-noise construction | Code, values, summaries, and configurations | Reproducible model transformation; not an independent measurement |
| Per-material simulator | Code, 138 configurations, 690 run summaries | Reproducible fitting system with high per-material flexibility |
| Family correlations | Summary table and generated configurations | Directly inspectable; does not support the strongest topology claims |
| Pressure profile | Configurations and digest | Descriptive optimized pattern; requires independent testing |
| LOO | Code and 18-row output | Reproduces configuration similarity, not physical prediction |
| AIC/BIC | Code and one-row summary | Not a valid comparative likelihood analysis |
| Integer participation | Code, manifest, 268-row output, and figures | Exactly reproducible under the released asymmetric null |
| Recalibrated-null claim | Described in paper, absent from code | Independent implementation gives nonconclusive p-values |
| Noise–participation relation | Code, summary columns, and figures | Small effective sample and interval crossing zero |
| Coherence relation | Code, 11-source table, 10 matched outputs, and figure | Reproducible but small, source-incomplete, and LOO-sensitive |

## Open questions for a future Study 02 revision

1. Can structural noise be defined from observables independent of the
   prime-lock ratios used as its predictor?
2. Can family profiles and geometry weights be learned on training data and
   evaluated unchanged on held-out materials?
3. What is the minimal parameterized model that retains the same explanatory
   performance?
4. Can the oscillator language be implemented as an actual time-domain model
   with explicit coupling, delay, stability, and falsifiable dynamics?
5. Does the layer-specific pressure sign pattern predict new measurements
   under prospectively chosen pressures?
6. Can LOO validation predict physical targets rather than generated
   configurations?
7. Can model comparison use explicit likelihoods, correct parameter counts,
   and meaningful simpler alternatives?
8. Can every dataset value and coherence-length measurement be mapped to a
   specific source with uncertainty and measurement conditions?

## Questions left by the Study 03 crossover

No standalone Study 03 conclusions are retained, following the author's
direction. If this line of inquiry is ever restarted, it should be treated as
a new, prospectively specified study addressing:

1. Does integer proximity survive preregistered bounds and family definitions
   on a new dataset?
2. Do null models recalibrated with exactly the same fitting freedom retain a
   significant effect?
3. What is the correct unit of independence when materials have multiple rows
   or subnetworks?
4. Does the noise relation survive a unique-name or hierarchical analysis?
5. Can the coherence exponent be predicted on held-out materials with
   uncertainty propagation and a fully documented experimental table?
