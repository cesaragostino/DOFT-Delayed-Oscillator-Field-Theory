# Study 01 — Extracted Findings

This document separates direct artifact evidence from model-dependent
interpretation and unresolved claims.

## Evidence labels

- **Direct artifact:** directly reported in a published table, dataset, or
  reproducible output.
- **Model-dependent:** follows from the chosen locking grammar, correction
  model, or category scheme.
- **Unresolved:** claimed or implied, but not adequately demonstrated by the
  reviewed package.

## 1. Published dataset

The Zenodo v1.0 dataset contains 252 material or subnetwork rows and 221 unique
material names. All rows contain `Tc`, Debye temperature, Fermi energy, and gap
fields.

| Category | Rows |
| --- | ---: |
| High-pressure superconductor | 83 |
| Binary superconductor | 72 |
| Iron-based superconductor | 34 |
| Type II superconductor | 18 |
| Oxide superconductor | 14 |
| Type I superconductor | 11 |
| Molecular superconductor | 10 |
| Heavy-fermion superconductor | 6 |
| Superfluid | 4 |

**Assessment — Direct artifact.** The package provides a substantial curated
input table and reproducible summary files. Row-level source provenance still
needs an audit: the `REFERENCE` field points to a broad bibliography, and some
records are marked as predicted values, proxies, or BCS-derived proxies.

## 2. Prime-space fingerprints

The factorized output contains 796 rows. Of these, 327 have complete integer
fingerprints and 469 use rational locks.

### Integer locks

| Population | Mean exponent of 2 | Mean exponent of 3 | Mean exponent of 5 | Mean exponent of 7 |
| --- | ---: | ---: | ---: | ---: |
| All complete integer rows (`N=327`) | 1.50 | 0.65 | 0.45 | 0.26 |
| Type I, single (`N=27`) | 1.556 | 0.815 | 0.519 | 0.407 |
| Type II, single (`N=46`) | 2.043 | 0.870 | 0.543 | 0.348 |
| High pressure, single (`N=104`) | 1.038 | 0.548 | 0.346 | 0.087 |

The overall median exponent vector is `(1, 0, 0, 0)`.

**Assessment — Model-dependent.** Prime `2` dominates the selected
representation. This is a valid description of the factorized output, not yet
an independent physical result: the basis primes and nearest-lock procedure
are fixed in advance.

### Rational locks

| Category | Defined `q` rows | Mean `q` | Median `q` |
| --- | ---: | ---: | ---: |
| Superfluid | 16 | 2.063 | 1 |
| Iron based | 109 | 4.119 | 3 |
| Type II | 8 | 4.875 | 5 |
| Binary | 100 | 5.180 | 5 |
| Heavy fermion | 18 | 5.389 | 5 |
| Molecular | 30 | 5.533 | 5 |
| Oxide | 40 | 5.075 | 5 |
| Type I | 7 | 5.429 | 5 |
| High pressure | 141 | 5.887 | 7 |

Across the published output, `q` has mean 5.06 and median 5. The distribution
is: `q=1: 40`, `q=2: 30`, `q=3: 67`, `q=4: 42`, `q=5: 110`, `q=6: 6`,
`q=7: 74`, and `q=8: 100`.

**Assessment — Model-dependent.** Category distributions differ, especially
between superfluids and high-pressure superconductors. However, denominators
are constrained to `1..8`, so the statement that denominators are “small” is
true by construction. Lock families are also preassigned by material
category, which means the apparent family separation is not an independent
classification result.

## 3. Thermal–memory correction

The published calibration constrains both coefficients to be nonnegative.
`Γ` remains effectively at the zero boundary in every reported configuration.
The fitted `η` changes systematically with the winsorization cap:

| Winsor cap | Prime cutoff | `η` | Bootstrap 95% interval |
| --- | ---: | ---: | ---: |
| 400 | 7,919 | `4.217 × 10⁻⁵` | `[1.361 × 10⁻⁵, 6.934 × 10⁻⁵]` |
| 600 | 7,919 | `2.710 × 10⁻⁵` | `[5.992 × 10⁻⁶, 4.546 × 10⁻⁵]` |
| 800 | 7,919 | `1.877 × 10⁻⁵` | `[2.973 × 10⁻⁶, 3.242 × 10⁻⁵]` |

Changing the prime cutoff from 7,919 to 10,000 has little effect compared with
changing the winsorization cap.

**Assessment — Direct artifact for the fit; unresolved for universality.**
The data support `Γ ≈ 0` under this fit. They do not establish a unique,
cap-independent value of `η`. The bootstrap resamples individual jumps even
though three jumps usually come from the same material, so the reported
intervals do not account for within-material dependence. The nonnegative
constraint can also bias a weak coefficient away from negative values.

The calibration has no fixed random seed and defines the applied coefficients
as the means of 500 bootstrap fits. Consequently, the fitted coefficient and
downstream corrected ratios change between executions. The published
cap-800 digest reports `η = 1.8773 × 10⁻⁵`, the packaged configuration contains
`η = 1.8413 × 10⁻⁵`, and a clean verification run produced
`η = 1.8340 × 10⁻⁵`. All fall in the same reported interval, but the pipeline
does not exactly reproduce its continuous outputs.

## 4. κ refinement

Of 175 cluster rows, only 6 receive a nonzero κ adjustment. All six belong to
the MgB₂ sigma/pi subnetwork. The adjustment ranges from approximately
`−0.00936` to `+0.00971`. It changes none of the integer exponents or rational
denominators in the 796-row factorized output.

**Assessment — Direct artifact.** κ is localized to MgB₂ in this release and
does not alter the reported locking grammar. Describing it as a global
correction would exceed the evidence.

## 5. Residual structure

Several groups have residual means close to zero:

| Category / subnetwork | Mean residual | Standard deviation | `N` |
| --- | ---: | ---: | ---: |
| Binary / pi | −0.0024 | 0.0099 | 9 |
| Molecular / single | −0.0030 | 0.0118 | 30 |
| Iron based / single | −0.0023 | 0.0205 | 36 |
| Oxide / single | −0.0051 | 0.0152 | 42 |
| High pressure / single | −0.0031 | 0.0382 | 240 |

Other groups remain displaced or broad, including high-pressure La-acoustic
sigma, Type II single rows, binary gap2 rows, high-pressure H1 optic rows, and
the two superfluid pressure groups.

**Assessment — Direct artifact with a calculation caveat.** The code computes
the residual with the natural logarithm, while the manuscript defines and
labels it as `log10`. The qualitative ordering may survive a constant scale
change, but numerical claims must use one definition consistently.

## 6. Baseline comparison

The published summary reports much lower mean absolute relative error for the
DOFT nearest-lock representation than for a two-parameter power-law baseline
in every category.

**Assessment — Unresolved as a model comparison.** The comparison script
detects an `err_after_kappa` column but recomputes the DOFT error directly from
the nearest prime value and observed ratio. It also records zero DOFT
parameters, omitting global calibration parameters, the discrete grammar, and
nearest-lock selection. The power law is therefore a weak comparator and the
reported parameter-count comparison is not like-for-like.

The manuscript mentions a Mann–Whitney significance test and a moderate
effect, but the reviewed release does not include the corresponding U
statistic, p-value, effect-size table, or a reproducible test output.

## 7. Post-publication local analysis

The reviewed source working copy contains ignored outputs generated after the
Zenodo release. They are useful leads but are neither in Zenodo v1.0 nor
tracked at the reviewed Git revision.

- With the published-style caps, `η` decreases from approximately
  `4.38 × 10⁻⁵` at cap 400 to `1.90 × 10⁻⁵` at cap 800.
- Without the cutoff and winsorization regime, the point estimate drops to
  approximately `6.22 × 10⁻⁹` with `R² ≈ 0.006`.
- Restricting the calibration to `X < 100` gives
  `η ≈ 5.50 × 10⁻⁴` with `R² ≈ 0.306`.
- Leave-one-material-out values in the `X < 100` subset retain
  `R² ≈ 0.277..0.360`, but the coefficient is roughly 30 times the cap-800
  estimate.

**Assessment — Unversioned lead.** The subset stability is interesting, but
the large cross-regime variation argues against treating `η` as universal
until the selection and clipping rules are fixed prospectively and validated
on held-out materials.

## 8. Internal inconsistencies to resolve

| Issue | Published or source statement | Reviewed evidence |
| --- | --- | --- |
| Baseline `η` | Manuscript associates `w=800`, cutoff 7,919 with approximately `4 × 10⁻⁵` | Digest reports `1.877 × 10⁻⁵`; approximately `4.2 × 10⁻⁵` belongs to `w=400` |
| Residual logarithm | Manuscript and figures label `log10` residuals | Pipeline uses the natural logarithm |
| Dataset expansion | Manuscript describes approximately 50 additions | v5 to v6 changes from 140 to 252 rows and 132 to 221 unique material names |
| Baseline error | Output names a post-κ error field | Script recomputes error without using that field |
| Statistical separation | Significance and effect size are described | Supporting test output is absent from the published package |
| Reproduction paths | README names `notebooks/` and a root `environment.yml` | The archive contains `notebook/` and `notebook/environment.yml` |
| Generated outputs | README describes the 621-, 175-, and 796-row CSV files | The archive includes aggregate summaries but omits those row-level result files |
| Randomness | README presents the run as reproducible | Bootstrap resampling is unseeded, and its mean becomes the applied `Γ` and `η` |

## 9. Verification run

A clean canonical run was executed from the published package with `w=800`,
prime cutoff 7,919, and the sensitivity grid disabled. The run completed and
regenerated the omitted row-level outputs.

| Output | Comparison with the published summary |
| --- | --- |
| Integer fingerprint summary | Exact byte-for-byte match |
| Rational denominator summary | Exact byte-for-byte match |
| Power-law baseline summary | Exact byte-for-byte match |
| Calibration summary | Same qualitative regime, different unseeded bootstrap values |
| κ summary | Same 175 rows and same 6 nonzero MgB₂ cases; numerical deltas differ |

The verification supports the discrete descriptive findings and κ
localization. It also confirms that the continuous correction values are not
deterministically reproducible with the released implementation.

## 10. Overall conclusion

- **Supported:** a reproducible, inspectable descriptive compression of the
  curated v6 dataset under a fixed prime-space grammar.
- **Provisionally supported:** category-specific fingerprint and residual
  patterns worth testing on prospectively curated or held-out data.
- **Not established:** a universal correction coefficient, independent
  discovery of material families, or a fundamental physical basis for the
  prime grammar.
- **Outside the evidence of this study:** the historical Mother Frequency,
  QCD-to-electroweak alignment, and broad cross-scale universality claims.
