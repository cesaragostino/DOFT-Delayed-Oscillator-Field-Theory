# DOFT — MANIFESTO v1.4.1

> **Status**: Research Alpha  
> **Version**: 1.4.1  
> **License**: MIT

Extends v1.4 by making explicit:  
- **LPC(t)** (Layers-Per-Cycle) as the DOFT notion of propagation “speed”: **very high** at the beginning (no structure), then **decreasing** as structure/“skin” forms, and finally **converging** to a stable value with **slow residual drift**.  
- **Pulsed propagation** via a **breathing skin** (short transmission windows, local rebounds, inhomogeneous advance).

The rest of the v1.4 framework remains: **RE/RCB/IC**, **cavity+skin**, breakpoint **\(R_\*\)** (clean→dirty), and **\(P_\mathrm{DOFT}\)** as operational power (decoherence flux).

---

## 0) Scope

This document states **what we test** and **how we try to break it**. It is compatible with the repo’s current pipeline: `configs/`, `scripts/`, `tests/`.

---

## 1) DOFT Premises (v1.4.1, updated)

1. **Oscillators + Elementary Delay (RE).** Each coupling imposes a minimal delay in cycles.  
2. **Loop-Closure Rule (RCB).** Cohesion (resonance) holds if the total loop phase misfit stays within a **tolerance** that **tightens** as “energy” decreases.  
3. **Composite Interference (IC).** Interference does **not** create new RE; it **modulates** the **effective** delay needed for a net effect.  
4. **Layers.** “Space” is relational and emerges from delays; **time** is cycle counting.  
5. **Abrupt shock; no instantaneity.** The onset of change is abrupt but **everything** still propagates layer-by-layer.  
6. **Cavity + Skin.** A coherent interior (cavity) bounded by a **nearly static skin** most of each cycle.  
7. **Skin filter.** The skin **reflects** low frequencies, **transmits** high frequencies, and **emits in pulses** when it grazes the tolerance limit.  
8. **Two regimes + \(R_\*\).** **Clean** (few active channels) → loss scales like “channel”; **Dirty** (many skin modes) → loss scales like “surface”. \(R_\*\) is the breakpoint.  
9. **LPC(t) as propagation.**  
   - **Early** (no structure): **LPC high** (IC ≈ 0, skin effectively open).  
   - **Structure forming** (grains + skin): **LPC decreases** and **converges** to a stable value with **slow residual drift**.  
   *Note:* Phenomenologically aligns with “early extremely fast effective propagation” scenarios; our implementation is strictly in DOFT terms (layers/cycles), not field-theory dogma.  
10. **Breathing / Pulsed propagation.** The skin **opens/closes** in **windows** (small duty \(d\) in clean regime), driving **pulse trains**, **local rebounds** (multiple local round-trip times), and **inhomogeneous** advance.  
11. **End of cycle.** Destruction is abrupt (not instantaneous). Residuals remain and define a **floor**: **A** (asymptotic decay) and **B** (structural).

---

## 2) Minimal construction (operational formulas)

### 2.1 Effective delay and LPC

\[
\tau_\mathrm{eff}(t) \;=\; \tau_\mathrm{RE}\,\bigl[1+\sigma_\mathrm{IC}(t)\bigr]\;\frac{1}{d_\mathrm{skin}(t)} ,
\qquad
\mathrm{LPC}(t) \;=\; \frac{1}{\tau_\mathrm{eff}(t)} .
\]

- \(\tau_\mathrm{RE}\): elementary per-link delay (in cycles).  
- \(\sigma_\mathrm{IC}(t)\): aggregate **complexity** of parallel routes/misfits (IC).  
- \(d_\mathrm{skin}(t)\in(0,1]\): **skin duty** (fraction of a cycle the skin is effectively at rest/transmissive).

**Early:** \(\sigma_\mathrm{IC}\!\approx\!0\), \(d\!\approx\!1\) ⇒ **LPC high** (very large but finite).  
**Later:** \(\sigma_\mathrm{IC}\!\uparrow\), \(d\!\downarrow\) ⇒ **LPC decreases** and **converges** (slow drift persists).

### 2.2 Pulsed propagator (breathing skin)

Pre-skin signal: \(y=(K*s)\) with **delay kernel**
\[
K(\tau)=\sum_{p}w_p\,\delta(\tau-T_p),
\quad
T_p=\sum_{e\in p}\tau_e .
\]
Skin acts as **temporal gating** \(g(t;d)\) and **frequency filter** \(T(\omega)\):
\[
Y_\mathrm{ext}(\omega)=\bigl[\mathcal{F}\{g(t;d)\}\!*\,T(\omega)\bigr]\;\hat K(\omega)\,S(\omega) .
\]
**Pulses** (small duty) broaden spectra and coordinate **wavefront bursts** with **local rebounds**.

---

## 3) Deductions

1. **\(f\)–\(R\) in clean regime.** Round-trip time \(\propto R\) ⇒ base frequency **\(f\propto 1/R\)**.  
2. **Pre-critical behavior.** When the skin margin shrinks: \(d\downarrow\), \(\sigma_\mathrm{IC}\uparrow\) ⇒ **effective delay rises**, **LPC falls**, **off-harmonic power** increases.  
3. **Breakpoint \(R_\*\).** Once many skin modes light up, operational power \(P_\mathrm{DOFT}\) changes scaling law (channel→surface).  
4. **Breathing observable.** Duty \(d\) imprints side lobes in spectra and **pulse trains** in time series.  
5. **Convergence + slow drift.** After the “basic architecture” stabilizes, LPC flattens with slow residual drift (floor A/B; slow re-harmonizations).

---

## 4) Operational definitions

- **\(R\)**: radius in **layers** (cycles) from the core to the skin.  
- **\(P_\mathrm{DOFT}\)**: **decoherence flux per cycle** across the skin  
  (e.g., count of nodes leaving RCB per cycle normalized by skin area/perimeter, or drop per cycle of an exterior coherence index).  
- **Skin rest duty \(\%t_\mathrm{rest}\)**: fraction of a period with \(|\dot\phi_\mathrm{skin}|<\epsilon\).  
- **\(\Phi\)**: fraction of spectral power **off the harmonics** of the base \(\Omega\).  
- **Effective delay**: cycles to reach the peak response at a probe after a local pulse.  
- **\(R_\*\)**: slope break in \(\log P_\mathrm{DOFT}\) vs \(\log R\) (two-segment regression; low→high slope).  
- **\(\mathrm{LPC}(t)\)**: layers traversed per cycle (windowed average).

---

## 5) Falsifiable predictions (v1.4.1 adds LPC/pulses)

- **P-LPC.** With increasing IC and decreasing duty \(d\), **LPC(t)** **decreases** and then **converges** (slow drift).  
  *Falsified if:* LPC stays flat.  
- **P-Duty.** Lowering \(d\) **broadens** the exterior spectrum and **increases** pulse rate.  
  *Falsified if:* spectrum remains unchanged.  
- **P-Rebounds.** Multiple local **round-trip times** (peaks in effective delay across regions) appear before synchronization.  
  *Falsified if:* a single global delay dominates throughout.  
- **P-Breakpoint.** A clear **\(R_\*\)** with a slope change in \(\log P_\mathrm{DOFT}\)–\(\log R\).  
  *Falsified if:* no break.  
- **P-\(f(R)\).** **\(f\sim 1/R\)** in clean regime.  
  *Falsified if:* \(f\) remains ≈ constant.

---

## 6) Experiments (Phase “soft-cavity”, extended)

- **E1 — \(f\) vs \(R\).** Sweep \(R\in[8,64]\); expect \(1/R\).  
- **E2 — Law & \(R_\*\).** Plot \(\log P_\mathrm{DOFT}\) vs \(\log R\); segmented slope fit.  
- **E3 — Skin rest & pulses.** \(\%t_\mathrm{rest}\), pulse trains, duty vs \(R\).  
- **E4 — Pre-critical.** Effective delay and \(\Phi\) vs skin margin.  
- **E5 — Anisotropy.** Tangential deformations reduce \(R_\*\).  
- **E7 — LPC vs build-up.** IC(t) added in **waves**; duty \(d\) decreased → track **LPC(t)**.  
- **E8 — Pulses/duty.** Sweep duty \(d\); measure \(\Phi\) and pulse trains.  
- **E9 — Local rebounds.** Regions with different \(R\) → distribution of effective delays.  
- **E10 — \(f\)–\(R\) (redundant for robustness).** Confirm \(f\sim 1/R\) in clean regime.

---

## 7) Data contracts (minimal outputs)

Append to `runs.csv` (besides existing fields):

