# Study 01 — Research Log

## Extraction scope

This log records how Study 01 was incorporated into the central DOFT
repository. The operation is an evidence extraction, not a repository import:
no source code, Git history, raw dataset, generated figure, or nested
repository has been copied here.

## Sources reviewed

| Source | Role | Status |
| --- | --- | --- |
| [GitHub source repository](https://github.com/cesaragostino/doft-study01-superconductors) | Development history, pipeline, paper source, and post-release changes | Reviewed through `fa71d6641429d2d4f45ae3d607fa0a784f306a71` |
| [Zenodo record 17620713](https://doi.org/10.5281/zenodo.17620713) | Canonical published v1.0 artifact | Reviewed |
| Zenodo archive `doft-study01-superconductors-zenodo-v1.zip` | Dataset, pipeline snapshot, paper, figures, and summary CSV files | Reviewed and cross-checked |
| Zenodo `main.pdf` | Published manuscript | Reviewed alongside its source and summaries |
| Local ignored post-publication outputs | Exploratory Rydberg/low-`X` follow-up | Logged separately; not treated as published evidence |

The six Zenodo summary tables match their corresponding source-repository
files byte for byte. The main pipeline modules in the archive also match the
reviewed source versions. This confirms that the uploaded directory is a
complete extraction of the published bundle.

An exact comparison against the public Zenodo download produced the following
integrity checks:

- the downloaded ZIP matches Zenodo's published MD5 checksum
  `39bb7fcfbee7efb8745ef8170fa51a49`;
- after excluding macOS metadata and Python bytecode caches, both the public
  ZIP and the uploaded directory contain 28 substantive files;
- all 28 relative file names and SHA-256 content hashes match exactly.

The published bundle is a curated snapshot, not a complete processed-results
dump. It includes the input dataset, pipeline, paper, figures, and six
aggregate CSV summaries. It does not include the generated row-level
calibration, cluster, and full-factorization CSV files described in its
README. Those outputs can in principle be regenerated, but their omission
limits direct row-level verification without rerunning the pipeline.

The package README also refers to `notebooks/` and a root `environment.yml`;
the actual paths are `notebook/` and `notebook/environment.yml`.

## Verification run

A canonical robustness run was executed in a temporary directory using the
published input and pipeline:

- winsorization cap: 800;
- prime cutoff: 7,919;
- sensitivity grid: disabled;
- interpreter used for this check: Python 3.13.9.

The run completed successfully and regenerated the calibration, 175-row
cluster outputs, 796-row fingerprint outputs, digest tables, baseline, and
figures. The integer-fingerprint, rational-denominator, and baseline summaries
match their published CSV files byte for byte.

The calibration and κ summaries do not match numerically. The pipeline uses
unseeded bootstrap resampling and sets the operational `Γ` and `η` to the
bootstrap means, so each execution can change the coefficients and downstream
continuous corrections. In this run, cap-800 `η` was
`1.8340 × 10⁻⁵`, compared with `1.8773 × 10⁻⁵` in the published digest and
`1.8413 × 10⁻⁵` in the packaged configuration. The κ result retained the same
structure—6 nonzero rows, all MgB₂—but its delta range changed from
approximately `[-0.00936, 0.00971]` to `[-0.00984, 0.01020]`.

All verification outputs were kept outside the central and source
repositories. The package configuration modified as a side effect of the run
was restored and checked against the public artifact hash.

## Study timeline

| Date | Event |
| --- | --- |
| 2025-11-15 | The v6 material dataset appears in source history. |
| 2025-11-15 | v6 processed results and digest tables are added. |
| 2025-11-15 | Large generated `data/processed/run2` results are removed from tracked Git history while paper work continues. |
| 2025-11-16 | The paper reaches its final preprint revision. |
| 2025-11-16 | Zenodo v1.0 is published with the curated dataset, pipeline, figures, paper, and summaries. |
| 2025-11-16 to 2025-11-17 | The repository is reorganized and cleaned up after publication. |
| 2026-06-14 | A low-`X` Rydberg/leave-one-material-out analysis script is added to the source repository. |
| 2026-07-24 | Study 01 is extracted into the DOFT central index. |

## Extraction decisions

1. **Zenodo v1.0 is the canonical published evidence.** Later source changes
   are not silently folded into the published result.
2. **The source repository remains the computational home.** This central
   repository stores summaries, findings, provenance, and links only.
3. **Descriptive output is separated from physical interpretation.** A pattern
   produced by a constrained grammar is not described as independent proof of
   that grammar.
4. **Design-imposed properties are explicit.** The denominator limit and
   category-level lock-family assignments are recorded alongside the results.
5. **Known inconsistencies remain visible.** The `η` configuration mismatch,
   unseeded bootstrap, logarithm mismatch, baseline implementation, and missing
   statistical output are not normalized away.
6. **Post-publication ignored outputs are leads, not release evidence.** They
   are logged because they materially change the interpretation of coefficient
   stability.
7. **The earlier central Study 01 report is historical.** It is preserved in
   the document archive, not used as the current findings summary.

## Reproducibility map

| Claim area | Material in the published package | Central assessment |
| --- | --- | --- |
| Dataset composition | Input CSV | Directly verifiable |
| Integer fingerprints | Pipeline and aggregate summary; row-level output omitted | Aggregate result is inspectable; row-level result requires rerunning |
| Rational denominator distribution | Pipeline and aggregate summary; row-level output omitted | Aggregate result is inspectable, with imposed `q ≤ 8` |
| Calibration coefficients | Pipeline and aggregate summary; row-level output omitted | Regenerates in the same regime, but not exactly because the operational coefficient is an unseeded bootstrap mean |
| κ localization | Pipeline and 175-row κ summary | Directly verifiable from the summary |
| Residual group summaries | Pipeline and prose/figure summary; row-level output omitted | Requires regeneration after resolving the intended log base |
| DOFT versus power-law baseline | Partially | Script and output exist, but comparison design needs correction |
| Mann–Whitney significance/effect size | No complete output found | Not independently verified from the release |
| Low-`X` Rydberg/LOMO result | Local ignored output only | Not part of Zenodo v1.0 |

## Open questions for a future Study 01 revision

1. Can every input value be mapped to a row-level source and tagged as
   measured, inferred, predicted, or proxy?
2. What happens when lock family and denominator range are selected without
   using the material category?
3. Does a material-level or hierarchical bootstrap preserve a positive,
   stable `η`?
4. Can a fixed seed and a separately reported deterministic point estimate
   distinguish sampling uncertainty from run-to-run drift?
5. Can clipping and subset rules be fixed before calibration and evaluated on
   a held-out material set?
6. Does the prime grammar outperform matched alternatives with comparable
   search freedom and parameter accounting?
7. Which logarithm is intended for residual reporting, and do all tables and
   figures use it consistently?
8. Can the statistical comparison be regenerated with effect size, confidence
   interval, exact sample definition, and correction for dependent rows?
9. Does κ remain localized to MgB₂ in a prospectively curated dataset?
