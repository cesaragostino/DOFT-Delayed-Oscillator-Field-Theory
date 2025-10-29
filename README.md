# DOFT — Delayed Oscillator Field Theory

_A research program on emergent spacetime, gravity, and quantum signatures from networks of delayed oscillators_

**Status:** Research Alpha | Open Methodology | Cross-Lab Collaboration

> “Order is memory made visible. Chaos is the fuel that keeps memory from fading.” — DOFT Axiom A0 (Law of Chaos Preservation)

---

## 1. Overview

This repository hosts the reference implementation, experiments, and analysis pipeline for DOFT—a bottom-up, network-dynamics framework where the building blocks are identical oscillators coupled through retarded links. In DOFT, **space, time, fields, and gravitation are not fundamental objects**; they emerge from the causal pattern of delays and phases on a large graph.

The project's goals are:
- **Theory-to-data:** Derive falsifiable predictions (scalings, collapse laws, stability bounds) from DOFT’s axioms.
- **Data-to-theory:** Test those predictions with numerics and public datasets, and report success/failure with code-audited, reproducible runs.

[This is the DOFT Manifesto](./MANIFESTO.md)  
*(This repository should use the `DOFT_MANIFESTO_v1.6-Consolidated.md` content for this file)*

[This is the DOFT Manifesto uses plain language and analogies](./MANIFESTO_EXPLAINED.md)  
*. This text uses plain language and analogies to make DOFT accessible to non-specialists. It does not replace the technical formulation or aim to provoke; any simplification is intentional to aid understanding.*

[This is the DOFT Manifesto en lenguaje coloquial y analogías](./MANIFESTO_EXPLICADO.md)  
*. Este texto usa lenguaje coloquial y analogías para acercar DOFT a lectores no especialistas. No sustituye la formulación técnica ni busca polemizar; cualquier simplificación es intencional para facilitar la comprensión.*

---

## Table of Contents

- [What this repository is](#what-this-repository-is)
- [Theory snapshot (v1.6 Consolidated)](#theory-snapshot-v16-consolidated)
- [Repository layout](#repository-layout)
- [Quick start](#quick-start)
  - [Environment](#environment)
  - [Time step selection](#time-step-selection)
  - [Development Guidelines](#development-guidelines)
  - [Run experiments from configs](#run-experiments-from-configs)
  - [Self-averaging report](#self-averaging-report)
  - [Dynamic delay parameters](#dynamic-delay-parameters)
- [Data contracts](#data-contracts)
- [Validation suite](#validation-suite)
- [Falsifiable predictions](#falsifiable-predictions)
- [Core concepts](#core-concepts)
- [Experiments: Phase A, B, C](#experiments-phase-a-b-c)
- [Open questions](#open-questions)
- [Workflow & Governance](#workflow--governance)
- [A final note](#a-final-note)

---

## What this repository is

This repo contains:
- A **CPU-only** reference simulator for networks of **delayed oscillators** with finite-memory kernels.
- Optional **dynamic-delay mode** using per-node ring buffers and fractional interpolation.
- A **validation harness** focused on **falsification-first** checks (self-averaging, LPC in closed systems, etc.).
- A **reporting pipeline** that emits CSV/Parquet plus plots for independent auditing.

All historic patch bundles and hotfixes have been **consolidated** into this repository. The current code represents the latest state; no external patch application is required.

The goal is not to “prove” DOFT, but to **break it quickly** under clean tests. What survives earns attention.

---

## Theory snapshot (v1.6 Consolidated)

DOFT’s working hypothesis is built on these consolidated pillars:

1. **Substrate:** The world is a graph of **oscillators** coupled with **propagation delays** ($\tau_{ij}$).
2. **Dynamics:** Coherence is governed by a **Loop-Closure Rule (RCB)**, where loops remain coherent if phase misfit is within a tightening tolerance.
3. **Structure:** Coherent systems form a **Cavity + Skin**. The skin filters frequencies and transmits in pulses. The transition from a clean (few modes) to a dirty (many modes) state is marked by a **Breakpoint ($R_*$)**.
4. **Propagation:** "Space" emerges from delays. The effective propagation speed **LPC(t)** (Layers-per-cycle) decreases from a high initial value and converges as structure forms.
5. **Memory:** Resonance is memory. The framework is a **Resonance–Memory–Cluster Model**, where clusters of resonances are linked by delays, storing correlations in layers.
6. **Axioms:** The **Law of Chaos Preservation (LPC/A0)** states that chaos is a conserved "fuel" that redistributes. Emergent "constants" ($c$, $\hbar$, $G$) are hypotheses derived from network statistics and delay sensitivities.

These are **claims under test**, not final truths.

---

## Repository layout

```
DOFT/
├── README.md               # quick guide and project goals
├── LICENSE
├── pyproject.toml
├── requirements.txt        # Python dependencies
├── src/
│   └── doft/               # Python package
│       ├── __init__.py
│       ├── models/
│       ├── simulation/
│       ├── analysis/
│       └── utils/
├── scripts/                # CLI or maintenance scripts
├── configs/                # JSON/YAML configuration files
├── docs/                   # documentation, guides, papers
└── .gitignore
```

---

## Quick start

### Environment

- Python 3.11 or 3.12
- NumPy, SciPy, pandas, pyyaml, matplotlib
- No GPU code; **CPU-only** by design
- Install dependencies from the root `requirements.txt`

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Time step selection

The simulator chooses a safe dimensionless time step automatically to
avoid runaway integrations. For each run the step is clamped via

```text
dt_nondim = min(0.02, 0.1, tau_nondim/50, 0.1/(gamma_nondim + |a_nondim| + 1))
```

Any configuration requesting a larger step triggers a warning and the
value above is used instead.

### Development Guidelines

See: `docs/protocols/iteration1_phase1.md` for guidelines to participate in this project.

```bash
export PYTHONPATH="$PWD/src"   # or pip install -e .
```

### Run experiments from configs

The helper scripts read parameters from JSON files under `configs/`.

- **Soft-cavity (Phase A) & Parametric (Phase C) sweeps**

  ```bash
  # Uses configs/soft_cavity_pulsed.json
  DOFT_CONFIG=configs/soft_cavity_pulsed.json bash scripts/run_quick.sh

  # Uses configs/parametric_st.json
  DOFT_CONFIG=configs/parametric_st.json bash scripts/run_quick.sh
  ```

- **Smoke test**

  ```bash
  DOFT_CONFIG=configs/smoke_test.json bash scripts/run_quick.sh
  ```

  Runs a tiny 16×16 grid for a handful of steps to verify the pipeline.

Each run writes results to a timestamped directory.

### Self-averaging report

```bash
python -m reports.self_avg --in out/sanity --out out/sanity/report
```

Emits summary CSV/PNG with estimated $\bar c$ and anisotropy $\Delta c / c$.

### Dynamic delay parameters

The simulator can evolve link delays during a run when `tau_dynamic_on` is enabled. Related settings:

- `tau_dynamic_on`: toggle dynamic delay updates.
- `alpha_delay`: scales how strongly the local field `G` modulates the delay.
- `lambda_z`: relaxation rate for an auxiliary `z` state that smooths `G` before applying `alpha_delay`.
- `epsilon_tau`: fractional slack for the delay ring buffer (0.05–0.2) to accommodate changing $\tau$.
- `eta`: maximum allowed normalized change of $\tau$ per step (slew bound).

-----

## Data contracts

Contracts are strict; CI checks schema on PR.

**runs.csv** (one row per run, consolidated from v1.4.1c & v1.5)

- `run_id, seed, n_nodes, ... (standard params)`
- `lpc_mean, lpc_drift`
- `skin_duty, phi_offharm, rstar_est`
- `mu_max, nr_db, resonant_k, protected_k0`
- `r_hat, M_hat, N_hat, rho_est, lambda_lyap_est`
- `... (and other metrics from v1.3 runs)`

**edges.parquet** (graph snapshot)

- `i, j, tau_ij, K_type, K_params, weight`

-----

## Validation suite

We include tests that must pass before trusting any “result”:

1. **Determinism (seeded):** repeated runs with same seed produce same statistics within tolerance.
2. **Finite outputs:** `_step_imex` on CPU produces finite positions/momenta (no NaNs/Infs).
3. **Self-averaging:** estimate $\bar c$ across blocks $(d=2,4,8,16)$; require slopes consistent with $\beta \approx 1$.
4. **Anisotropy metric:** unique definition $\Delta c / c$ with CI reported.
5. **Closed vs open LPC:** closed systems keep chaos functional $\mathcal{K}$ stationary (within numeric tolerance); open systems balance flux.

-----

## Falsifiable predictions

This simulation suite is designed to test these consolidated predictions:

### P1 — Basic & Skin Predictions

- **$f(R)$:** $f \sim 1/R$ in the clean regime.
- **Breakpoint:** A clear scaling break (Breakpoint $R_*$) is visible in $\log P_\mathrm{DOFT}$ vs $\log R$.
- **Skin rest:** $\%t_\mathrm{rest}$ (skin rest duty) is high in the clean regime and collapses near $R_*`.

### P2 — Build-up & Propagation

- **LPC(t):** The propagation measure LPC(t) (Layers-per-cycle) **decreases** from a high initial value and **converges** with a slow drift as structure forms.
- **Off-harmonics:** $\Phi$ (off-harmonic noise) rises as skin duty $d$ decreases or interference $\sigma_\mathrm{IC}$ increases.

### P3 — Parametric Resonance

- **Threshold $\delta_c$:** A finite modulation amplitude $\delta$ is required to achieve positive growth ($\mu_\mathrm{max}>0$).
- **Nonreciprocity:** A traveling-wave modulation yields nonreciprocal gain (**NR(dB) > 0**) in unstable bands.
- **Protection:** The ground mode is symmetry-protected (`protected_k0 = true`) for specific spatial modulation periods ($\tau=T/n$).

### P4 — Emergent Physics

- **Atomic Analogue:** Short-loop holonomies (Axiom A3) induce phase defects that shift effective Rydberg energies: $E_{n\ell} \;\approx\; -R_\mathrm{eff}/(n-\delta_\ell)^2$.
- **Gravity Analogue:** An analogue Hawking temperature $T_H$ scales with the gradient of the effective refractive index ($n_\mathrm{eff}$) at the horizon.
- **Antimatter Gravity:** Matter and antimatter exhibit the **same gravitational response** at leading order.

-----

## Core concepts

### How to Read DOFT as a Shortcut

DOFT can be seen as an emergent framework where the known fields and forces are effective layers of a deeper multi-resonant substrate.  
Bricks (mode + kernel) replace point particles; Memory (order parameters, gaps, topology) replaces static constants.  
Each layer iterates with memory, reproducing the known gauge structures as stable resonant envelopes.  
[Read “Emergence from Resonance” →](./EMERGENCE_FROM_RESONANCE.md)

### Oscillators with Delays (RE) & Loop Closure (RCB)

The substrate is a graph of oscillators (Axiom A1). The fundamental interaction is the **Loop-Closure Rule (RCB)**: a loop is coherent if its phase misfit is within tolerance. This is the basis of resonance.

### Cavity, Skin & Breakpoint (R_\*)

Coherent systems self-organize into a tolerant **Cavity** (interior) and a marginal **Skin** (boundary). The skin acts as a filter, gating signals in pulses. The **Breakpoint (R_\*)** marks the phase transition from a "clean" (channel-loss) to a "dirty" (surface-loss) regime.

### Propagation (LPC(t)) & Pulsed Gating

Space emerges from delays (Axiom A2). The effective propagation speed, **LPC(t)** (Layers-per-cycle), is a key observable. It is modulated by interference ($\sigma_{IC}$) and skin duty cycle ($d_{skin}$).

### Resonance-as-Memory & Clusters

Introduced in v1.5, this framework defines **memory** as retained correlation over cycles. A resonance is a "fluctuation that replays itself". Structures are **Clusters** of these resonances linked by finite delays, creating layered memory and causal order.

### Parametric Resonance

Time-modulation of system parameters (like delay or tolerance) can create nonreciprocal modes (one-way gain) and Floquet-type instabilities.

### Law of Chaos Preservation (LPC / Axiom A0)

In closed systems, the chaos functional $\mathcal{K}$ is conserved. Order emerges as a dissipative organization of this chaos budget. This is the foundational axiom (A0) from v1.3.

-----

## Experiments: Phase A, B, C

The repository tests are structured around the experimental phases defined in v1.4.1c:

### Phase A — Soft-cavity (skin, $R_*$, duty)

- **E1 — $f$ vs $R$:** Test $f \sim 1/R$ scaling.
- **E2 — Law & $R_*$:** Find the breakpoint $R_*$ in $\log P_\mathrm{DOFT}$ vs $\log R$.
- **E3 — Skin rest & pulses:** Measure $\%t_\mathrm{rest}$ and pulse trains vs $R$.

### Phase B — Build-up / LPC

- **E7 — LPC vs build-up:** Track **LPC(t)** as interference (IC) is activated in waves.
- **E8 — Pulses/duty:** Sweep skin duty $d$ and measure $\Phi$ (off-harmonics).

### Phase C — Parametric resonance

- **E11 — Threshold $\delta_c$:** Sweep modulation amplitude to find the instability threshold.
- **E13 — Nonreciprocity:** Measure **NR(dB)** under traveling-wave modulation.
- **E15 — Size scaling:** Verify ground-mode protection scales with ring size $n$.

-----

## Open questions

1. **Emergent constants:** Under what regimes do $c$ and $\hbar_\mathrm{eff}$ self-average ($\beta \to 1$)? When does this fail (critical clustering)?
2. **Memory Model:** How does the layered memory model (v1.5) map to observable metrics? Can we measure `M_hat` reliably?
3. **Breakpoint Physics:** What universality class does the $R_*$ breakpoint belong to?
4. **Antimatter gravity parity:** Can any parity-breaking term in $\tau[q]$ generate measurable deviations from matter-antimatter gravitational equivalence?
5. **Lorentz emergence:** Quantify Lorentz-violation terms in the coarse-grained PDE and their suppression with scale.

-----

## Workflow & Governance

This project follows a strict, multi-party workflow to ensure correctness and reproducibility.

- **Evaluators (OpenAI/Google):** Propose experiments and acceptance criteria via Pull Requests to the `/configs/` directory.
- **Developer (Google Track):** Implements features and solvers, including unit tests and performance notes.
- **Code Auditor (OpenAI Track):** Reviews numerical stability, determinism, and metric integrity. Has the authority to block merges that fail audit.
- **Runner:** Executes merged experiments and publishes signed artifacts to a results store.

## A final note

This repository aims to **earn** credibility by making failure modes obvious, documented, and repeatable. If a prediction breaks under a better test, that’s progress.

Happy falsifying.

