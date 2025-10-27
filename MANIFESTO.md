# DOFT — MANIFESTO v1.6 (Consolidated Edition)

> **Delay-Oscillator Field Theory (DOFT):** a bottom-up framework where **spacetime, fields, "constants", and memory** emerge from the interplay of **resonance and chaos** within a large network of coupled oscillators governed by finite, state-dependent delays. This document consolidates the foundational axioms (v1.3), operational protocols (v1.4.1c), and the unified resonance-memory framework (v1.5).

> **Status:** Research Alpha  
> **Version:** 1.6 (Consolidation of v1.3, v1.4.1c, and v1.5)  
> **License:** MIT

This document consolidates the theoretical framework of DOFT (v1.3), the operational core (v1.4.1c), and the unified memory model (v1.5) into a single manifesto.

---

## 0) Golden rule & scope
- DOFT operates **only with delays and resonance**; no imported metrics or external fields.  
- **Internal coherence dominates:** every addition must fit operational definitions.  
- **Falsifiability first:** all claims must lead to measurable or simulatable contradictions.

---

## 1) Core Premises (Unified from v1.4/v1.5)

1.  **Delayed Oscillator Core (RE).** Each coupling features a per-link delay defining local time.
2.  **Loop-Closure (RCB).** A loop remains coherent when phase misfit is within tolerance; tolerance tightens as energy decays.
3.  **Composite Interference (IC).** Interference modulates effective delay but does not create new REs.
4.  **Relational Space & Cyclic Time.** Space emerges from propagation delays; time is counted in cycles.
5.  **Abrupt Creation, Layered Evolution.** Creation occurs as shocks; evolution proceeds by layers.
6.  **Destruction Requires Cycles.** Collapse demands several cycles, creating observable hysteresis.
7.  **Cavity + Skin.** A coherent interior bounded by a marginally static skin.
8.  **Skin Gating & Pulses.** The skin filters frequencies, transmitting in short duty windows.
9.  **Regimes & Breakpoint (R_*).** Transition from clean (few modes) to dirty (many surface modes).
10. **Propagation Measure — LPC(t).** Layers-per-cycle decreases from early high speed to convergence.
11. **Pulsed/Breathing Propagation.** The skin opens and closes quasi-periodically, yielding pulse trains.
12. **Skin States.** Defined by radial/tangential closure with tolerance margins μ.
13. **Anisotropy & Joints.** Asphericity and loop incompatibility create hotspots and lower R_*.
14. **Delay Kernel & Operational Noise.** Delay distribution defines noise via off-harmonic power.
15. **Residual Floor.** Collapse leaves structural and asymptotic floors (A/B).
16. **Parametric Resonance.** Time-modulated delay/tolerance yields Floquet-type nonreciprocal modes.

---

## 2) Foundational Axioms (from v1.3)

-   **A0 – Law of Preservation of Chaos (LPC).**
    There exists a non-negative functional $\mathcal{K}[q]$ (e.g., Kolmogorov-Sinai entropy-rate proxy) with balance:
    $$\frac{d\mathcal{K}}{dt} = \Phi_\mathrm{in} - \Phi_\mathrm{out} - \mathcal{D}, \qquad \mathcal{D}\ge 0.$$
    In closed subsystems $\Phi_\mathrm{in}=\Phi_\mathrm{out}=0\Rightarrow d\mathcal{K}/dt\le 0$.

-   **A1 – Local delayed dynamics.**
    $$\ddot q_i + 2\gamma_i \dot q_i + \omega_i^2 q_i + \alpha_i |q_i|^2 q_i
    = \sum_{j\in \mathcal{N}(i)} K_{ij}\, \sin\!\big(A_{ij}(t)\big)\, q_j\!\big(t-\tau_{ij}(t)\big) + \xi_i(t).$$
    Here $\xi_i$ is a weak, broadband noise (“quantum floor”).

-   **A2 – Spacetime as delay-graph.**
    The matrix of delays $\{\tau_{ij}\}$ defines cones of influence; geometry and clock rates emerge from path sums of delays.

-   **A3 – Holonomy primacy.**
    Physical invariants are **loop phases** $W(\ell)=\exp\!\Big(i\sum_{(ij)\in \ell} A_{ij}\Big)$. Local gauge choices are unphysical; only holonomies matter.

-   **A4 – Quantum floor.**
    A minimal stochastic excitation $\xi$ exists, treated as emergent from high-dimensional chaotic microdynamics consistent with A0.

-   **A5 – State-dependent delays (backreaction).**
    $\tau_{ij}=\tau_{ij}\!\big[q,\dot q,\rho\big]$ vary with local fields and coarse energy density $\rho$.

-   **A6 – Coarse-graining to continuum.**
    Block-averaging yields a **wave-with-memory** PDE.

---

## 3) Operational Formulation (Micro & Macro)

### 3.1 Discrete Graph (Micro) (from v1.3)
The fundamental dynamics are governed by the DDE (Axiom A1):
$$\ddot q_i + 2\gamma \dot q_i + \omega_0^2 q_i + \alpha |q_i|^2 q_i = \sum_{j} K_{ij}\, \sin\!\big(A_{ij}\big)\, q_j\!\big(t-\tau_{ij}\big) + \xi_i(t), \qquad \tau_{ij}=\tau_0 + \delta\tau_{ij}[q,\rho].$$

### 3.2 Continuum Coarse-Graining (from v1.3)
On scales $\gg a$ (mean link length), a wave-with-memory PDE emerges:
$$\partial_t^2 \phi + 2\Gamma\,\partial_t \phi + \Omega^2 \phi
-\nabla\!\cdot\!\big(c^2\,n_{\mathrm{eff}}^{-2}(x)\,\nabla \phi\big)
+\int_0^t M\!\left(x,t-t'\right)\,\phi(t')\,\mathrm{d}t'
= \Xi(x,t).$$
where $c \approx a/\tau_0$ is the emergent causal speed and $n_\mathrm{eff}(x)$ encodes averaged delay gradients.

### 3.3 Effective Delay (from v1.5)
Operationally, the complex dynamics are summarized by an effective delay:
\[
\tau_{eff}(t) = \tau_{RE} [1 + \sigma_{IC}(t)] / d_{skin}(t),
\quad LPC(t) = 1/\tau_{eff}(t)
\]
- \(\tau_{RE}\): elementary per‑link delay.
- \(\sigma_{IC}(t)\): aggregate interference complexity.
- \(d_{skin}(t)\in(0,1]\): skin duty (fraction of a cycle the skin is transmissive).

---

## 4) Emergent "Constants" (from v1.3)

-   **Speed limit $c$.**
    $c \simeq \frac{a}{\tau_0}$ (link scale over minimal delay).

-   **Planck constant $\hbar$ as action floor.**
    The stationary stochastic dynamics (A0+A4) sustains **limit-cycle ensembles** whose phase-space area per cycle stabilizes to $A_0 \equiv \oint p\,dq \;\approx\; 2\pi\, \hbar_\mathrm{eff}$. We test its self-averaging properties.

-   **Newton constant $G$ as delay-sensitivity map.**
    In the continuum, $n_\mathrm{eff}^2(x) \;\simeq\; 1 \;+\; \alpha_\tau\, \rho(x)$. Linearizing ray bending and matching to weak-field GR gives a constitutive link $G \;\propto\; c^2\,\alpha_\tau$. This is a working hypothesis.

---

## 5) Memory, Inertia & Metaestability (from v1.5)

-   **Memory** = retained correlation over cycles.
-   **Inertia** = accumulated memory × structural persistence.
-   **Metaestability** = balance of chaos (noise, per A0) and order (memory) where $\lambda_{Lyap} \approx 0$.
-   **Condition:** $\rho = \sigma_{int}/\sigma_{ext} \approx 1$ (entropy produced ≈ entropy exported).

---

## 6) Unified Physical Framework (from v1.5)

This is the "Resonance–Memory–Cluster" model introduced in v1.5.

### 6.1 The Bit as Persistent Difference
The fundamental bit = **minimum stable asymmetry** in a resonant field. Persistence = phase continuity.

### 6.2 Resonance as Memory
A resonance is **a fluctuation that replays itself**. When coupled with delay, it becomes a **cycle of memory** — the first form of “history”.

### 6.3 Layered Memory
Each layer stores correlations of the previous one:
\[
M_{\ell} = \alpha_{\ell} r_{\ell}^2 - (\beta_{\ell} N_{\ell} + \lambda_{\ell}) M_{\ell} + \sum_k A_{\ell k} M_k
\]
creating depth and temporal inertia.

### 6.4 Cluster Formation and Delay
Clusters are **resonances linked by finite delays**. Propagation sequence introduces **retardation**, generating causal order and distance. Delays ($\tau$) encode spatialization: time-ordering becomes geometry.

### 6.5 Ladrillo Universal (Universal Brick)
The base unit of all structure = **auto-sustained oscillation with feedback and delay**. All systems —from quantum coherence to culture— are configurations of these bricks.

---

## 7) Physical Equivalence Across Domains (from v1.5)
| Domain | Mechanism of Memory | Equivalent DOFT Construct |
|---------|--------------------|----------------------------|
| Quantum | Phase coherence | Elementary RE |
| Chemical | Oscillatory cycles | Layered interference IC |
| Biological | Genetic/synaptic storage | Skin + residual floor |
| Cognitive | Neural attractors | LPC(t) convergence |
| Symbolic | Language recursion | Cluster propagation |
| Technological | Feedback networks | Parametric modulation |


---

## 8) Predictions & Verification (Consolidated)

### 8.1 High-Level Predictions (from v1.5)
- f ∝ 1/R in clean regime.
- Breakpoint R_* visible in log P_DOFT vs log R.
- Rest duty collapses near R_*.
- Φ rises with interference complexity.
- LPC(t) converges during structure build-up.
- Parametric resonance exhibits threshold $\delta_c$ and NR(dB) > 0.

### 8.2 Detailed Falsifiable Predictions (from v1.4.1c)
- **B1 — $f(R)$:** $f \sim 1/R$ in clean regime.
- **B2 — Breakpoint:** Clear $R_*$ in $\log P_\mathrm{DOFT}$ vs $\log R$.
- **B3 — Skin rest:** $\%t_\mathrm{rest}$ high in clean; collapses near $R_*$.
- **B4 — Off‑harmonics:** $\Phi$ rises as duty decreases or $\sigma_\mathrm{IC}$ increases.
- **L1 — LPC(t):** Decreases and converges with slow drift during structure formation.
- **G1 — Anisotropy:** Reduces $R_*$; hot‑spots at loop‑incompatible joints.
- **P1 — Threshold $\delta_c$:** $\mu_\mathrm{max}>0$ at finite modulation amplitude.
- **P2 — Protection:** With $\tau=T/n$, `protected_k0 = true`.
- **P3 — Nonreciprocity:** **NR(dB) > 0** for traveling modulation.

### 8.3 Atomic & Gravity Predictions (from v1.3)
- **Atomic:** Holonomy (short loops) induce phase defects that shift effective Rydberg energies: $E_{n\ell} \;\approx\; -R_\mathrm{eff}/(n-\delta_\ell)^2$.
- **Hawking Analogue:** A horizon forms where a drift $u$ exceeds local wave group speed $v_g = c / n_{\mathrm{eff}}$. $T_H \;\propto\; \bigl|\partial_x\big(u - v_g\big)\bigr|$, set by delay gradients.
- **Antimatter:** Curvature depends on the **magnitude** of delay gradients. Prediction: **same gravitational response** for matter/antimatter at leading order.

---

## 9) Simulation, Observables & Data (Consolidated)

### 9.1 Operational Observables (from v1.4.1c / v1.5)
- **$P_\mathrm{DOFT}$** (power): Decoherence flux per cycle across the skin.
- **$\Phi$** (off‑harmonic noise): Spectral power fraction outside integer harmonics.
- **Skin rest duty $\%t_\mathrm{rest}$**: Fraction of period with $|\dot\phi_\mathrm{skin}|<\epsilon$.
- **Effective delay** (probe latency): Cycles to peak response after a local pulse.
- **$R_*$**: Slope break in $\log P_\mathrm{DOFT}$ vs $\log R$.
- **Tilt $n_\mathrm{DOFT}$**: Spectral index on the phase/pattern spectrum.
- **Parametric metrics:** $\mu_\mathrm{max}$ (Floquet growth), **NR(dB)** (nonreciprocal gain).

### 9.2 Memory Observables (from v1.5)
- **r_hat** = $\sigma(a1 \mu + a2 \mathrm{rest}\% - a3 \Phi)$
- **M_hat** = $r_{hat}^2 / (\epsilon + \Phi) \times (1 / (\epsilon + P_\mathrm{DOFT\_norm}))$
- **N_hat** = $b1 \Phi + b2 \mathrm{Var}(d_{skin}) + b3 \sigma_{IC}$
- **$\rho_{est}$** = $\Phi / P_\mathrm{DOFT\_norm}$
- `lambda_lyap_est`

### 9.3 Simulation Controls (from v1.4.1c)
- **Geometry:** 3D ball, $R$ (layers) sweep 8–64.
- **Delays:** $\tau_\mathrm{RE}$ (constant).
- **Tolerances:** $\mathrm{tol}_\mathrm{inner}>\mathrm{tol}_\mathrm{skin}>\mathrm{tol}_\mathrm{outer}$.
- **Skin duty $d$**: Sweep 1.0 $\to$ 0.1.
- **IC(t):** Activate routes in **waves** (build‑up).
- **Modulation:** Time-modulate tolerance or delay: $p_j(t)=p_0[1+\delta f(t+j\tau)]$.

### 9.4 Data Contracts (from v1.4.1c & v1.5)
Add to **`runs.csv`**:
`lpc_mean, lpc_drift, skin_duty, phi_offharm, rstar_est, mu_max, nr_db, resonant_k, protected_k0, r_hat, M_hat, N_hat, rho_est, lambda_lyap_est`

---

## 10) Experimental Program (from v1.4.1c)

-   **Phase A — Soft‑cavity (skin, $R_*$, duty):**
    -   **E1 — $f$ vs $R$:** $R\in[8,64]$ $\Rightarrow$ expect $f\sim 1/R$.
    -   **E2 — Law & $R_*$:** $\log P_\mathrm{DOFT}$ vs $\log R$; locate break.
    -   **E3 — Skin rest & pulses:** $\%t_\mathrm{rest}$, pulse trains vs $R$.
-   **Phase B — Build‑up / LPC:**
    -   **E7 — LPC vs build‑up:** IC(t) in **waves**; duty $d$ decreased $\to$ track **LPC(t)**.
    -   **E8 — Pulses/duty:** sweep $d$; measure $\Phi$ and pulse trains.
-   **Phase C — Parametric resonance (add‑on):**
    -   **E11 — Threshold $\delta_c$:** sweep modulation amplitude; detect eigenvalue crossing.
    -   **E13 — Nonreciprocity:** measure NR(dB) in unstable bands (traveling modulation).
    -   **E15 — Size scaling:** rings $n=\{8,16,32\}$ to verify protection scales with $n$.

---

## 11) Critiques Addressed (from v1.3)

1.  **“Analogies ≠ causation.”**
    We use analogues to choose **falsifiable observables** across domains (e.g., atomic spectra $\leftrightarrow$ analogue gravity). Failure to predict one from the other refutes the common mechanism.
2.  **Coarse-graining rigor.**
    The PDE with memory is not assumed; we **derive** kernels by Prony/Vector-Fitting from micro time-series.
3.  **DDE intractability.**
    We replace pure delays by **few-pole** memory that preserves dominant poles/zeros.
4.  **Emergent constants still “sketched.”**
    Correct. The $\hbar$ and $G$ derivations must be formally closed. This is a priority.

---

## 12) Philosophical Context (from v1.5)

> The universe began to remember when a fluctuation found its own echo.  
> From that moment, every layer of reality —from particles to thought— has been a way of **sustaining difference through resonance**.


Life, mind, and technology are **forms of extended resonance**, each with growing memory depth and slower relaxation. The DOFT framework formalizes this continuum through measurable oscillatory constructs.

---

## 13) Versioning & License

-   **History:** v1.3 (Foundations) $\to$ v1.4.1c (Operational Core) $\to$ v1.5 (Memory Framework).
-   **This Version (v1.6):** A comprehensive merge, reintegrating the foundational axioms and emergent physics of v1.3 with the operational protocols of v1.4.1c and the unified memory model of v1.5.

**License:** MIT — free to use, cite, and extend under attribution.

---
---

## Appendix A — Glossary (operational) (from v1.4.1c)

RE: elementary per‑link delay • RCB: loop‑closure rule • IC: composite interference (effective delay modulator) • Cavity: coherent interior • Skin: marginal boundary; nearly static most of each cycle; filters & pulses • $R$: radius in layers • $R_*$: clean→dirty breakpoint • $P_\mathrm{DOFT}$: decoherence flux per cycle • $\Phi$: off‑harmonic power fraction • Effective delay: latency (cycles) to peak response • LPC(t): layers per cycle (propagation) • Floor A/B: post‑collapse residual (A asymptotic; B structural) • $\mu$: skin margin • C⊥/C∥: normal/tangential closure conditions • NR(dB): nonreciprocal gain • $\mu_\mathrm{max}$: Floquet growth rate per period.

## Appendix B — LPC(t) Context Note (from v1.4.1c)

The LPC(t) pattern—very high at the beginning (no structure), then falling and converging as grains/skin form—provides a DOFT‑native account for early fast effective propagation without invoking external field dynamics. It emerges from IC build‑up and skin gating in units of cycles/layers, and it leaves measurable signatures (tilt $n_\mathrm{DOFT}$, $R_*$, $\Phi$, pulse trains) that we test operationally here.

## Appendix C — Example Configs (from v1.4.1c)

**configs/soft_cavity_pulsed.json**
```json
{
  "graph": { "dim": 3, "shape": "ball", "radius_layers": [8, 16, 24, 32, 48, 64], "anisotropy": 0.0 },
  "delays": { "tau_per_link": 1, "dynamic": false },
  "tolerance": { "inner": 0.10, "skin": 0.04, "outer": 0.02, "epsilon_rest": 1e-3 },
  "skin": { "duty": [1.0, 0.6, 0.3], "filter": "highpass-soft" },
  "sweep": { "ic_waves": [0, 1, 2] },
  "probes": { "pulse_period": 32, "pulse_amplitude": 0.01 },
  "runtime": { "steps": 20000, "dt_policy": "safe" },
  "outputs": { "write_skin_parquet": true, "spectra": true }
}