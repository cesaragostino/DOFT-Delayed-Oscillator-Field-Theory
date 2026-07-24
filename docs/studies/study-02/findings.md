# Study 02 — Extracted Findings

This document separates direct artifact evidence from model-dependent
interpretation, post-extraction reanalysis, and unresolved claims.

## Evidence labels

- **Direct artifact:** directly reported in a dataset, configuration, code
  path, or reproducible output.
- **Model-dependent:** follows from the selected profiles, transformations,
  fitted parameters, or category scheme.
- **Reanalysis:** independently recomputed during this central extraction.
- **Unresolved:** claimed or implied, but not adequately demonstrated by the
  reviewed package.

## 1. Scope of the published artifact

The source README explicitly labels the structural-noise and simulator
pipeline as the **Study 02 core** and integer participation as a **Study 03
add-on**. The Zenodo package and paper combine both under one publication.

This document preserves that boundary:

- Sections 2–7 evaluate Study 02.
- Sections 8–9 record the published Study 03 crossover analysis because it is
  inseparable from the archive.
- No standalone Study 03 conclusions are retained, following the author's
  direction. The crossover is preserved only as an audited part of the Study
  02 publication record.

## 2. Dataset

The v7 material table contains 268 rows, 234 unique names, and 9 categories.
Twenty-eight names occur more than once, accounting for 62 rows.

| Category | Rows | Unique names |
| --- | ---: | ---: |
| Binary | 77 | 67 |
| Heavy fermion | 12 | 12 |
| High pressure | 82 | 80 |
| Iron based | 36 | 20 |
| Molecular | 10 | 10 |
| Oxide | 18 | 15 |
| Type I | 11 | 10 |
| Type II | 18 | 18 |
| Superfluid | 4 | 2 |

**Assessment — Direct artifact.** The main physical fields are populated, and
the package includes the complete upstream Study 01 v7 input and processed
results used by the Study 02 pipeline. It does not provide row-level
bibliographic provenance: source information is primarily carried in free-text
notes, and some values cannot be traced to a specific reference from the
dataset alone.

## 3. Structural-noise construction

For each eligible subnetwork, the code constructs three scale ratios, maps
them to the nearest exponent vectors over `{2, 3, 5, 7}`, and measures
between-subnetwork exponent mismatch. A log-ratio measure, `M_struct`, is then
related to the mean mismatch through a fitted coefficient `ζ`:

`predicted_noise = ζ × mismatch_mean`

The fit is an ordinary least-squares regression through the origin. With
category-specific fitting enabled, categories represented by one material can
reproduce that material's target directly.

Only 20 unique multi-subnetwork materials receive structural-noise values:

| Category | Materials |
| --- | ---: |
| Binary | 10 |
| Iron based | 8 |
| High pressure | 1 |
| Type I | 1 |

After merging by material name, 45 of the 268 dataset rows receive a noise
value. The remaining 223 rows use no structural-noise correction.

Among affected rows, predicted noise ranges from 0 to approximately 1.415,
with a median of 0.639. Because the code defines
`Tc_ideal = Tc × (1 + predicted_noise)`, the corresponding median correction
factor is 1.639 and the maximum is 2.415.

**Assessment — Model-dependent.** This is a reproducible transformation of
the source ratios. It is not an independent prediction of measured structural
noise: both mismatch and `M_struct` are constructed from the same input
fingerprints, and `Tc_ideal` is defined from the fitted transformation rather
than observed independently.

## 4. Encoded family structure

Configuration generation uses hard-coded family profiles, a default
skin-weighted geometry, category-dependent scales and caps, and an explicit
inward inversion for iron-based materials. Pressure terms are initialized as
a deterministic positive decay from the input pressure before optimization.

**Assessment — Direct artifact for implementation; unresolved for physical
interpretation.** The pipeline can test the behavior of the proposed
topologies, but it does not independently discover them. Family-specific
results must therefore be interpreted conditional on these encoded profiles.

## 5. Cluster simulator

Despite oscillator terminology in the surrounding methodology, the released
model is algebraic. It applies layer factors and offsets to a base frequency,
then computes exponent-like outputs, rational terms, and residuals. It does
not integrate coupled oscillators through time and does not implement an
explicit delay differential equation or stochastic dynamical process.

The optimizer produces 690 rows for 138 materials and 5 seeds. Per material,
it tunes 21 continuous values—four each for ratios, base offsets, thermal
terms, spatial terms, and pressure terms, plus `f0`—with discrete structural
choices also present in configuration generation. The typical run allows up
to 1,200 evaluations.

**Assessment — Direct artifact.** The simulator is a substantial parameter
fitting system, but “oscillator” should be read as a structural analogy in
this version. The high number of per-material degrees of freedom limits the
meaning of in-sample fit quality.

## 6. Family-specific results

The packaged family-correlation summary contains 10 binary and 8 iron-based
materials, plus one high-pressure and one Type I case.

| Family | Quantity | Prime layer 2 | Prime layer 7 |
| --- | --- | ---: | ---: |
| Binary | Correlation of noise with thermal term | 0.285 | 0.401 |
| Binary | Correlation of noise with spatial term | 0.181 | 0.530 |
| Iron based | Correlation of noise with thermal term | 0.071 | 0.408 |
| Iron based | Correlation of noise with spatial term | 0.329 | −0.014 |

These values do not demonstrate a binary surface-dissipation / stable-core
pattern or a strong iron-based core-coupling relation. The reported
high-pressure averages do show a sign change in optimized pressure terms:
approximately `+0.0059` and `+0.0121` for the prime-2 and prime-3 layers, then
`−0.0078` and `−0.0161` for prime 5 and prime 7.

**Assessment — Model-dependent.** The pressure sign pattern is a useful
hypothesis for future testing. It is an optimized internal parameter pattern,
not a direct measurement. The stronger family-mechanism claims in the paper
are not supported by the packaged correlation table.

## 7. Validation and model selection

### Leave-one-out analysis

The LOO table contains 18 cases: 10 binary and 8 iron-based materials. Mean
absolute errors are approximately:

| Target group | Mean absolute error |
| --- | ---: |
| Exponent vector (`ξ`) | 0.3916 |
| Thermal terms | 0.0071 |
| Spatial terms | 0.0070 |
| Pressure terms | 0.0000 |
| All flattened configuration terms | 0.0345 |

The implementation does not refit the simulator and predict held-out physical
observations. It predicts the held-out material's flattened configuration from
the mean configuration of the other members of its family. The small thermal
and spatial errors mostly measure similarity among rule-generated
initializations. Pressure error is trivially zero because the evaluated
families have zero input pressure; the single high-pressure structural-noise
case is not eligible for family LOO.

**Assessment — Unresolved as predictive validation.** The output is a
configuration-consistency diagnostic, not an out-of-sample test of the
physical model.

### AIC and BIC

The model-selection table contains one row, named `vector_pressure`, with
`k=21`, `n=690`, total loss about 8,549.4, AIC about 8,591.4, and BIC about
8,686.7.

The code substitutes the optimizer's arbitrary total loss for
`−2 log-likelihood`, counts 21 parameters once even though they are optimized
per material, and provides no competing model.

**Assessment — Unresolved.** These AIC/BIC numbers cannot select a model or
justify its complexity in their current form.

### Implementation tests

The repository test suite completes with 8 passing tests. These cover
implementation behavior and pipeline components; they are not scientific
validation of the model.

## 8. Integer participation — Study 03 crossover

The participation table contains 268 rows representing 234 unique names. It
defines:

- `Fm_raw = ThetaD / Tc`;
- `Tc_ideal = Tc × (1 + predicted_noise)`;
- `Fm_corr = ThetaD / Tc_ideal`;
- a family-specific `f_base` selected within `[0.5, 5.0]`;
- `N = Fm_corr / f_base`, with deviation from the nearest integer.

Calibration uses the same data later assessed for integer proximity. The
winning `Fm` hypothesis gives a global median absolute integer deviation of
approximately 0.155. Family-specific bases and deviations are:

| Family | Fitted `f_base` | Median absolute deviation |
| --- | ---: | ---: |
| Binary | 4.1569 | 0.1750 |
| Heavy fermion | 2.3074 | 0.0711 |
| High pressure | 4.2786 | 0.1800 |
| Iron based | 1.0897 | 0.0678 |
| Molecular | 4.6655 | 0.0903 |
| Oxide | 2.3342 | 0.0693 |
| Type I | 4.8298 | 0.1535 |
| Type II | 2.4872 | 0.1565 |
| Superfluid | 3.9953 | 0.1430 |

The released code compares these real-data-optimized bases with shuffled and
parametric null samples **without recalibrating the bases for each null**. The
manuscript says the null models are recalibrated and that smooth distributions
are fitted within each family; the implementation keeps the real bases and
fits the parametric null globally.

The paper's very small KS and Mann–Whitney p-values can be reproduced from a
single plotted null realization. The plotting merge expands 268 source rows
to 332 rows because duplicate material names create a many-to-many join. This
pseudo-replication and the asymmetric optimization make those p-values
unsuitable as evidence of strong integer locking.

### Recalibrated-null audit

The participation output was reproduced with the published seed and inputs;
`participation_summary.csv` matched byte for byte. An independent audit then
recalibrated every family base for every null sample, as described in the
manuscript.

| Null construction | Empirical `p` | Null median deviation |
| --- | ---: | ---: |
| Global shuffle of `ThetaD`, with family recalibration | 0.059 | 0.1711 |
| Within-family shuffle of `ThetaD`, with family recalibration | 0.140 | 0.1652 |

The corresponding 95% null ranges are approximately `[0.1515, 0.1911]` and
`[0.1457, 0.1835]`.

**Assessment — Reanalysis.** The strong integer-locking claim is not robust
to giving the null model the same calibration freedom as the observed data.
The published zero exceedances out of 1,000 permutations provide resolution
no finer than roughly `1/1000`; they do not establish a p-value on the order
of `10⁻¹³`.

## 9. Noise relation and coherence-length crossover

### Participation versus structural noise

Only 42 rows have both finite structural noise and valid integer participation.
The packaged association is Spearman `ρ≈0.303`, `p≈0.0508`, with a bootstrap
interval of approximately `[−0.033, 0.602]`. The interval crosses zero.

The reported near-integer versus remaining-group effect changes materially
with sample construction: the direct participation output gives Cliff's
delta about `−0.348`, while the duplicate-expanding plotting merge gives about
`−0.471`. Neither reproduces the paper's stated value near `−0.58`.

**Assessment — Direct artifact.** The current data suggest a possible
relationship but do not establish it.

### Coherence length

The experimental input contains 11 records, of which 10 match the
participation table. The reproduced log-log regression is:

- exponent `α = 0.434`;
- standard error `0.168`;
- `R² = 0.455`;
- `p = 0.0324`;
- `n = 10`.

The manuscript reports approximately `0.43 ± 0.05`; the `±0.05` value is not
produced by the released analysis and is inconsistent with the regression
standard error. Leave-one-out fits are unstable: `α` ranges from about 0.294
to 0.550 and `R²` from 0.179 to 0.769; removing Al raises the p-value to about
0.257.

The source table's short reference labels are not completely mapped to the
paper bibliography, and no measurement uncertainties are supplied.

**Assessment — Direct artifact plus reanalysis.** This is an interesting
small-sample association, not yet a stable validation. It should be repeated
with prospectively selected materials, explicit sources, uncertainty
propagation, and a held-out prediction.

## 10. Internal inconsistencies to resolve

| Issue | Manuscript or documentation | Reviewed evidence |
| --- | --- | --- |
| Study ownership | One paper combines structural noise and participation | Source README identifies participation as a Study 03 add-on |
| Simulator type | Described in oscillator/delay language | Released model is algebraic and has no time integration or delay dynamics |
| Family topology | Strong skin/core mechanisms are described | Profiles are partly encoded; current correlations are weak or mixed |
| Structural-noise validation | Presented as a predicted physical field | Predictor and target are transformations of the same source ratios |
| LOO | Presented as model validation | Predicts held-out generated configurations from a family mean |
| Model selection | AIC/BIC values are reported | One model, no likelihood, and incorrect parameter accounting |
| Null calibration | Manuscript says each null is recalibrated | Released code retains bases optimized on the real data |
| Null distribution | Manuscript says family-specific smooth fits | Released parametric fit is global |
| Significance | KS/Mann–Whitney `p≤10⁻¹³` | One plotted null, unfair calibration, and duplicate-expanding merge |
| Noise effect | Cliff's delta near `−0.58` | Packaged constructions give approximately `−0.35` or `−0.47` |
| Coherence exponent | Approximately `0.43 ± 0.05` | Reproduced standard error is approximately `0.168` |
| Citation type | Repository citation identifies software | Zenodo classifies the release as a preprint |

## 11. Overall conclusion

- **Supported:** a complete, executable research package; deterministic
  participation output with the fixed seed; a broad generated configuration
  and simulator corpus; and explicit model hypotheses.
- **Provisionally useful:** the structural mismatch variable, layer-specific
  pressure pattern, and small-sample coherence association as leads for
  prospective testing.
- **Not established:** independent discovery of family topology, predictive
  validity of the 21-parameter simulator, justified model complexity, strong
  integer locking, or a universal participation–coherence relation.
- **Needed next:** prospectively fixed profiles, row-level source provenance,
  matched-null calibration, independent
  validation targets, and uncertainty-aware held-out tests.
