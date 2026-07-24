# DOFT — MANIFESTO v1.4.1c (Consolidated)

> **Status**: Research Alpha  
> **Version**: 1.4.1c (consolidated from v1.3 → v1.4.1 + parametric‑resonance add‑on)  
> **License**: MIT

This manifesto states **what we test** and **how we try to break it**. It consolidates all prior pieces:
- v1.3 core (delayed oscillators, resonance by loop‑closure, layered propagation, abrupt shock, destruction needs cycles, residual floor).
- v1.4 additions (cavity+skin, breakpoint \(R_*\), operational power as **decoherence flux** \(P_\mathrm{DOFT}\)).
- v1.4.1 additions (**LPC(t)** as propagation measure; **breathing/pulsed skin**; local rebounds; inhomogeneous advance).
- Add‑on: **parametric resonance & space–time symmetry** (nonreciprocity; symmetry‑protected modes; Floquet maps).

We keep a strict **parsimony** rule: no external dogmas; only operational constructs compatible with DOFT.

---

## 0) Golden rule & scope
- **DOFT works with delays and resonance only.** No imported fields/metrics beyond what is *defined here*.  
- **Internal coherence > everything.** Every new element must fit the definitions below.  
- **Falsifiability first.** Every claim must point to an experiment/simulation that can contradict it.

---

## 1) Core premises (unified)

1. **Oscillators + Elementary Delay (RE).** Each coupling has a minimal per‑link delay (in cycles).

2. **Loop‑Closure Rule (RCB).** A loop is coherent if its total phase misfit is within a **tolerance** that **tightens** as “energy” decreases.

3. **Composite Interference (IC).** Interference does **not** create new RE; it **modulates** the **effective** delay required for a net effect.

4. **Layers & time.** “Space” is relational and emerges from delays (layer‑by‑layer propagation). **Time** is cycle counting. No global instantaneity.

5. **Abrupt shock; layered change.** Creation is **locally abrupt**; evolution still proceeds by layers (delays).

6. **Destruction needs inertia.** Destruction requires cycles (delays) to occur; hence the possibility of abrupt end‑of‑cycle collapses.

7. **Cavity + Skin.** A coherent **cavity** bounded by a **skin** that is nearly static most of each cycle (border of tolerance).

8. **Skin filter & pulses.** The skin **reflects** low frequencies, **transmits** higher ones; when it grazes tolerance it **emits in pulses** (short transmission windows).

9. **Two regimes & breakpoint \(R_*\).**  
   - **Clean:** few active channels; loss scales like a *channel*.  
   - **Dirty:** many skin modes; loss scales like *surface*.  
   \(R_*\) is the scaling break (clean→dirty).

10. **Propagation measure — LPC(t).** \(\mathrm{LPC}(t)\) (Layers‑Per‑Cycle) is the DOFT “speed”.  
    - **Early:** no structure (IC≈0; skin effectively open) → **LPC high** (very large but finite).  
    - **Build‑up:** grains + skin appear (IC↑; duty ↓) → **LPC decreases** and **converges** to a stable value with **slow residual drift**.

11. **Breathing/pulsed propagation.** The skin opens/closes in windows (duty \(d\ll 1\) in clean regime), leading to **pulse trains**, **local rebounds** (multiple round‑trip times), and **inhomogeneous** advance.

12. **Skin states (levels vs bands).**  
    - **Radial closure C⊥:** \(\Delta_\perp=|\Omega\,T_\perp-2\pi q|\le\varepsilon\).  
    - **Tangential closure C∥:** \(\Delta_\parallel=\min_m|\Omega\,\rho_\parallel L_g-2\pi m|\le\varepsilon\).  
    - **Margin:** \(\mu=\varepsilon-\max(\Delta_\perp,\Delta_\parallel)\).  
      \(\mu>0\) clean; \(\mu\to 0^+\) threshold \(R_*\); \(\mu<0\) dirty.  
      Commensurability (radial/tangential) yields **discrete‑like levels**; otherwise **bands** (windows of stability).

13. **Anisotropy & joints.** Strong asphericity lowers \(R_*\). Joints between skins must satisfy loop‑sum compatibility; otherwise **hot‑spots** (dirty).

14. **Delay kernel & operational noise.** A network of routes with delays \(T_p\) defines

    \[
      K(\tau)=\sum_p w_p\,\delta(\tau-T_p),\quad \hat K(\omega)=\sum_p w_p e^{-i\omega T_p}.
    \]

    “Noise” is **off‑harmonic power** produced by \(\hat K\) (delay dispersion) and skin gating/filtering.

15. **Floor after collapse.** Residuals define a **floor**: **A** (asymptotic decay) and **B** (structural/frustration).

16. **Parametric resonance & space–time symmetry (add‑on).**  
    Time‑modulated tolerance or delay with a **traveling phase** \(f(t+j\tau)\); analyze with **per‑period map** \(M_T\) and **space–time Floquet** \(F_\mathrm{ST}=S^{-1}M_\tau\).  
    - **Resonance:** eigenvalue of \(M_T\) crosses unit circle.  
    - **Symmetry‑protected ground mode:** with \(\tau=T/n\), the uniform mode needs \(T=n\pi/\omega_0\) to resonate.  
    - **Nonreciprocity:** traveling modulation yields one‑way gain (different growth for ±k).

---

## 2) Minimal operational construction

### 2.1 Effective delay & LPC

\[
  \tau_\mathrm{eff}(t)=\tau_\mathrm{RE}\,\bigl[1+\sigma_\mathrm{IC}(t)\bigr]\;\frac{1}{d_\mathrm{skin}(t)},
  \qquad
  \mathrm{LPC}(t)=\frac{1}{\tau_\mathrm{eff}(t)}.
\]

- \(\tau_\mathrm{RE}\): elementary per‑link delay.  
- \(\sigma_\mathrm{IC}(t)\): aggregate interference complexity.  
- \(d_\mathrm{skin}(t)\in(0,1]\): skin duty (fraction of a cycle the skin is effectively transmissive/static).

### 2.2 Pulsed propagator (breathing skin)
- Pre‑skin signal \(y=(K*s)\).  
- Skin gating & filtering:

\[
  Y_\mathrm{ext}(\omega)=\bigl[\mathcal{F}\{g(t;d)\}\!*\,T(\omega)\bigr]\,\hat K(\omega)\,S(\omega).
\]

Small duty \(d\) broadens spectra and yields **pulse trains** with **local rebounds**.

### 2.3 Skin closures & margin
- **C⊥:** \(\Delta_\perp=|\Omega T_\perp-2\pi q|\le \varepsilon\).  
- **C∥:** \(\Delta_\parallel=\min_m|\Omega \rho_\parallel L_g-2\pi m|\le \varepsilon\).  
- **Margin:** \(\mu=\varepsilon-\max(\Delta_\perp,\Delta_\parallel)\).

### 2.4 Operational observables
- **\(P_\mathrm{DOFT}\)** (power): **decoherence flux per cycle** across the skin (count exits from RCB per cycle normalized by skin area/perimeter, or drop per cycle of an exterior coherence index).
- **\(\Phi\)** (off‑harmonic noise): spectral power fraction outside integer harmonics of base \(\Omega\).
- **Skin rest duty** \(\%t_\mathrm{rest}\): fraction of period with \(|\dot\phi_\mathrm{skin}|<\epsilon\).
- **Effective delay** (probe latency): cycles to peak response after a local pulse.
- **\(R_*\)**: slope break in \(\log P_\mathrm{DOFT}\) vs \(\log R\) (two‑segment regression).
- **Tilt \(n_\mathrm{DOFT}\)**: spectral index on the phase/pattern spectrum generated during build‑up.
- **Parametric metrics:** \(\mu_\mathrm{max}=(1/T)\log\max_i|\lambda_i(M_T)|\), **NR(dB)** \(=10\log_{10}(G_+/G_-)\), `resonant_k`, `protected_k0` (bool), `st_bloch_phase`.

---

## 3) Deductions

1. **\(f\)–\(R\) (clean):** round‑trip time \(\propto R\) ⇒ **\(f\propto 1/R\)**.  
2. **Pre‑critical:** skin margin ↓ ⇒ duty ↓ and \(\sigma_\mathrm{IC}\) ↑ ⇒ **effective delay ↑**, **LPC ↓**, **off‑harmonics ↑**.  
3. **Breakpoint \(R_*\):** loss scaling changes (channel→surface); spectra dirty; memory rises.  
4. **Breathing signature:** duty \(d\) imprints spectral side‑lobes and pulse trains.  
5. **Levels vs bands:** strong commensurability ⇒ near‑discrete skin states; otherwise bands (windows).  
6. **Anisotropy:** lowers \(R_*\) and narrows stable bands; joints that fail loop sums generate hot‑spots.  
7. **Parametric resonance:** per‑period map eigenvalue crosses unit circle; traveling modulation yields **nonreciprocal** gain; uniform mode protected for \(\tau=T/n\).

---

## 4) Falsifiable predictions

**Basic / skin**
- **B1 — \(f(R)\):** \(f\sim 1/R\) in clean regime.  
- **B2 — Breakpoint:** clear \(R_*\) in \(\log P_\mathrm{DOFT}\) vs \(\log R\) (slope low→high).  
- **B3 — Skin rest:** \(\%t_\mathrm{rest}\) high in clean; collapses near \(R_*\).  
- **B4 — Off‑harmonics:** \(\Phi\) rises as duty decreases or \(\sigma_\mathrm{IC}\) increases.

**Build‑up / LPC**
- **L1 — LPC(t):** increases early (very high but finite), then **decreases** and **converges** with slow drift during structure formation.  
- **L2 — Tilt:** \(n_\mathrm{DOFT}<1\) stabilizes after skin formation.

**Geometry / joints**
- **G1 — Anisotropy:** reduces \(R_*\); hot‑spots at loop‑incompatible joints.  
- **G2 — Bands:** stable windows in \(R\) vs delay‑ratio maps; band width decreases with asphericity.

**Parametric resonance (add‑on)**
- **P1 — Threshold \(\delta_c\):** \(\mu_\mathrm{max}>0\) at finite modulation amplitude.  
- **P2 — Protection:** with \(\tau=T/n\), `protected_k0 = true` until \(T=n\pi/\omega_0\).  
- **P3 — Nonreciprocity:** **NR(dB) > 0** for traveling modulation in unstable bands.  
- **P4 — Static predictor:** unmodulated spectrum + symmetry predicts which modes will resonate.

Each prediction is **falsified** by the negation (no scaling, no break, no NR, etc.).

---

## 5) Experiments

### Phase A — Soft‑cavity (skin, \(R_*\), duty)
- **E1 — \(f\) vs \(R\):** \(R\in[8,64]\) ⇒ expect \(f\sim 1/R\).  
- **E2 — Law & \(R_*\):** \(\log P_\mathrm{DOFT}\) vs \(\log R\); segmented fit; locate break.  
- **E3 — Skin rest & pulses:** \(\%t_\mathrm{rest}\), pulse trains, duty vs \(R\).  
- **E4 — Pre‑critical:** effective delay and \(\Phi\) vs margin.

### Phase B — Build‑up / LPC
- **E7 — LPC vs build‑up:** IC(t) in **waves**; duty \(d\) decreased → track **LPC(t)**.  
- **E8 — Pulses/duty:** sweep \(d\); measure \(\Phi\) and pulse trains.  
- **E9 — Local rebounds:** regions with different \(R\) → distribution of effective delays.  
- **E10 — \(f\)–\(R\)** (redundant for robustness): confirm \(1/R\).

### Phase C — Parametric resonance (add‑on)
- **E11 — Threshold \(\delta_c\):** sweep modulation amplitude; detect eigenvalue crossing.  
- **E12 — Space–time symmetry:** set \(\tau=T/n\); check ground‑mode protection.  
- **E13 — Nonreciprocity:** measure NR(dB) in unstable bands (traveling modulation).  
- **E14 — Static predictor:** compare predicted resonant modes with measured.  
- **E15 — Size scaling:** rings \(n=\{8,16,32\}\) to verify protection scales with \(n\).

---

## 6) Simulation protocols (what to control & record)

**Initial state (common):** no structure → **shock** → cavity + skin appear.

**Controls**
- Geometry: 3D ball (clean vs surface scaling visible).  
- **R** (layers): sweep 8–64.  
- Delays: per‑link \(\tau_\mathrm{RE}\) (constant to isolate effects).  
- Tolerances: \(\mathrm{tol}_\mathrm{inner}>\mathrm{tol}_\mathrm{skin}>\mathrm{tol}_\mathrm{outer}\).  
- Skin duty \(d\): 1.0 → 0.1.  
- IC(t): activate routes in **waves** (build‑up).  
- Anisotropy: low‑order tangential deformation; joints (Y/T).

**Parametric add‑on controls**
- Modulation: tolerance **or** delay (choose one)  
  \(p_j(t)=p_0[1+\delta f(t+j\tau)]\), with period \(T\), amplitude \(\delta\), spatial offset \(\tau\); include \(\tau=T/n\).

**Metrics**
- \(f(R)\), \(P_\mathrm{DOFT}\), \(\%t_\mathrm{rest}\), \(\Phi\), effective delay, \(R_*\).  
- **LPC(t)** (windowed), **tilt** \(n_\mathrm{DOFT}\).  
- Parametric: \(\mu_\mathrm{max}\), NR(dB), `resonant_k`, `protected_k0`, `st_bloch_phase`.

**End‑of‑cycle criteria**  
- Breakpoint \(R_*\) present; \(\%t_\mathrm{rest}\) collapses; LPC(t) converges; (parametric) \(\mu_\mathrm{max}>0\) & NR>0 where expected.

---

## 7) Laboratory analogs (generic)

- **System:** 3D network with fixed per‑link delay; interior tolerant, **skin** marginal, exterior strict.  
- **Protocol:** grow \(R\); sweep duty \(d\); activate routes in waves; add small anisotropy; (parametric) time‑modulate tolerance or delay with traveling phase.  
- **Observe:** \(f\sim 1/R\), \(R_*\) in scaling, \(\%t_\mathrm{rest}\) drop, \(\Phi\) growth (pre‑critical), LPC convergence; (parametric) threshold \(\delta_c\), NR(dB), protected ground mode.

---

## 8) Data contracts (minimal outputs)

Append to **`runs.csv`** (besides your current fields):  
`lpc_mean, lpc_drift, skin_duty, phi_offharm, ret_eff_peak, rstar_est, pulses_per_period, mu_max, nr_db, resonant_k, protected_k0, st_bloch_phase`

Optional per‑run **`skin.parquet`**:  
`ring_id, layer, rest_duty, exits_per_cycle, local_anisotropy`

---

## 9) Validation & CI

- Determinism (seeded); finite outputs; self‑averaging (as in prior versions).  
- **Breakpoint \(R_*\)**: two‑segment regression with low→high slope prior; report CI.  
- **Surrogate control:** force \(d\to 1\) (no gating) ⇒ \(\Phi\) must **decrease**, \(R_*\) must **vanish**.  
- **Parametric:** detect \(\delta_c\) ( \(\mu_\mathrm{max}>0\) ), **NR>0** under traveling modulation; ground‑mode protection with \(\tau=T/n\).

---

## 10) How to run (quick)

**Soft‑cavity smoke:**
```bash
DOFT_CONFIG=configs/soft_cavity_pulsed.json bash scripts/run_quick.sh
```

**Parametric (space–time) smoke:**
```bash
DOFT_CONFIG=configs/parametric_st.json bash scripts/run_quick.sh
```

**Report (if present):**
```bash
python -m reports.soft_cavity --in out/soft --out out/soft/report
```

---

## 11) Example configs

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
```

**configs/parametric_st.json**
```json
{
  "graph": { "dim": 1, "shape": "ring", "sites": 32 },
  "delays": { "tau_per_link": 1 },
  "tolerance": { "inner": 0.08, "skin": 0.05, "outer": 0.03, "epsilon_rest": 1e-3 },
  "modulation": {
    "parameter": "tolerance",          
    "delta": [0.00, 0.02, 0.05, 0.10],
    "period_T": [32, 40, 48, 64],
    "spatial_tau": ["0", "T/8", "T/16"],   
    "waveform": "cos"                  
  },
  "skin": { "duty": 1.0 },             
  "runtime": { "steps": 40000 },
  "outputs": { "spectra": true }
}
```

---

## 12) Change log (v1.3 → v1.4.1c)

- **v1.3:** delayed oscillators; RCB; interference as delay modulator; layers; abrupt shock; destruction needs cycles; residual floor.
- **v1.4:** cavity+skin; clean vs dirty scaling; breakpoint \(R_*\); operational power \(P_\mathrm{DOFT}\) as decoherence flux.
- **v1.4.1:** LPC(t) (early fast → convergent); breathing/pulsed skin; local rebounds; inhomogeneous advance; extended metrics & experiments.
- **add‑on:** parametric resonance & space–time symmetry (threshold, symmetry‑protected ground mode, nonreciprocity; Floquet maps).

---

## 13) Methodological principles

- **Zero preconceptions.** Only what is defined here.
- **Parsimony.** Minimal new assumptions.
- **Explicit vs implicit.** Mark assumptions; prefer operational definitions.
- **Falsifiability.** Each claim must map to a measurable test (sim or analog).
- **Local abruptness, not global instantaneous.** Respect delays.
- **Metrics, not metaphors.** Always reduce to measurable quantities in DOFT units (cycles/layers).

---

## 14) Templates (copy–paste ready)

### 14.1 Hypothesis/prediction
```
H# (statement): …
Key variables: …
What to observe: …
Validation criterion: …
What would falsify it: …
```

### 14.2 Simulation (delays & layers)
```
Initial state: ordered oscillators; apply abrupt shock; cavity emerges with skin.
Controls: shock intensity, coupling map, delay distribution, skin duty d, anisotropy, modulation (if any).
Metrics: coherence/RCB, layer-by-layer propagation, post-collapse residuals, P_DOFT, Φ, LPC, R*, pulse stats.
End-of-cycle: resonance loss threshold + sudden collapse, or scaling break (clean→dirty).
Logging: time series, spectra, pulse events, layer maps vs time.
```

### 14.3 Lab analogue (order blackout / pulsed skin)
```
System: coupled oscillators with controllable delays; interior tolerant; skin marginal; exterior strict.
Protocol: create resonant state → sweep energy/tolerance downward or add modulation → detect abrupt collapse → measure residuals.
Observables: fall of order, near-silence windows, residual modes, hysteresis; scaling change (channel→surface).
Notes: “T→0” here = extreme reduction of operational tolerance; verify if total blackout occurs or residual floor remains.
```

---

## Appendix A — Glossary (operational)

RE: elementary per‑link delay • RCB: loop‑closure rule • IC: composite interference (effective delay modulator) • Cavity: coherent interior • Skin: marginal boundary; nearly static most of each cycle; filters & pulses • \(R\): radius in layers • \(R_*\): clean→dirty breakpoint • \(P_\mathrm{DOFT}\): decoherence flux per cycle • \(\Phi\): off‑harmonic power fraction • Effective delay: latency (cycles) to peak response • LPC(t): layers per cycle (propagation) • Floor A/B: post‑collapse residual (A asymptotic; B structural) • \(\mu\): skin margin • C⊥/C∥: normal/tangential closure conditions • NR(dB): nonreciprocal gain • \(\mu_\mathrm{max}\): Floquet growth rate per period.

---

## Appendix B — Early‑fast → convergent propagation (context note)

The LPC(t) pattern—very high at the beginning (no structure), then falling and converging as grains/skin form—provides a DOFT‑native account for early fast effective propagation without invoking external field dynamics. It emerges from IC build‑up and skin gating in units of cycles/layers, and it leaves measurable signatures (tilt \(n_\mathrm{DOFT}\), \(R_*\), \(\Phi\), pulse trains) that we test operationally here.

