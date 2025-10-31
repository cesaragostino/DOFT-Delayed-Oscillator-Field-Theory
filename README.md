# README — DOFT

*(Delayed Oscillator Field Theory Repository Overview)*

---

## 1. Repository Index Diagram

```
          ┌────────────────────────────┐
          │        Manifesto           │
          │  (Conceptual Foundation)   │
          └─────────────┬──────────────┘
                        │
                        ▼
          ┌────────────────────────────┐
          │          Studies           │
          │  (Scientific Validation)   │
          │  e.g., Study_01, Study_02  │
          └─────────────┬──────────────┘
                        │
                        ▼
          ┌────────────────────────────┐
          │      Implementation        │
          │ (Simulation & Software)    │
          └─────────────┬──────────────┘
                        │
                        ▼
          ┌────────────────────────────┐
          │          Results           │
          │  (Data, Plots, Validation) │
          └────────────────────────────┘
```

This structure reflects the logical flow of the project:

* **Manifesto** (v1.8 internally) — conceptual foundation of DOFT.
* **Studies** — formal derivations and empirical tests.
* **Implementation** — simulation and programming layer.
* **Results** — visualizations and experimental comparisons.

---

## 2. What is DOFT?

The **Delayed Oscillator Field Theory (DOFT)** describes reality as a field of **coupled oscillators with memory and delay**.

In this framework, every layer of the universe — from quantum fields to macroscopic matter — is part of a nested hierarchy of resonant systems.  Coherence, memory, and resonance replace the static notions of particles and forces.

> **Matter is a standing wave of memory.  Temperature is the rate of forgetting.**

DOFT provides a unified language to connect **energy, memory, and structure**, where physical laws emerge from the way oscillators synchronize across scales.

---

## 3. Repository Structure

| Path                                                                                                         | Description                                                                               |
| :----------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------- |
| [`Manifesto`](./MANIFESTO_v1.8.md)                                                                           | Conceptual and theoretical foundation. Introduces DOFT, memory, resonance, and coherence. |
| [`STUDY_01_MotherFrequency_and_ThermalMemoryShift.md`](./STUDY_01_MotherFrequency_and_ThermalMemoryShift.md) | Full scientific derivation of the Mother Frequency and the thermal–memory correction law. |
| *Future Studies*                                                                                             | Each Study focuses on one phenomenon: gauge emergence, field coherence, etc.              |
| [`README-DOFT.md`](./README-DOFT_v1.8.md)                                                                    | This document — global overview, roadmap, and conceptual index.                           |

The **Manifesto** tells the story; the **Studies** make it testable; the **Implementation** (coming next) will make it executable.

---

## 4. Core Principles (Summary)

| Concept            | Definition                                                   | Physical Meaning                        |
| :----------------- | :----------------------------------------------------------- | :-------------------------------------- |
| **Memory**         | The persistence of past states through delayed interactions. | Encoded by kernel (K_{\ell m}(\tau)).   |
| **Resonance**      | Stable frequency ratios between layers.                      | Expressed by prime-locking ({2,3,5,7}). |
| **Temperature**    | Rate of phase decoherence.                                   | Derived from FDT: (T_{\mathrm{eff}}).   |
| **Entropy**        | Loss of coherent phase volume.                               | Spread of correlated oscillation.       |
| **Energy**         | Amplitude of oscillation.                                    | (E = \hbar \omega).                     |
| **Gauge symmetry** | Stable degeneracy between coupled oscillators.               | 3–2–1 pattern → SU(3)×SU(2)×U(1).       |

---

## 5. The Hierarchy of Resonance

A simplified view of the DOFT frequency cascade:

```
    Mother Frequency (ω*)  ~ 10^25 Hz  | 200–260 GeV
    ├── Electroweak Field (SU(2)×U(1))
    │   ↓
    ├── QCD Resonance       ~ 10^22 Hz  | 220 MeV
    │   ↓
    ├── Nuclear Binding     ~ 10^21 Hz  | 28 MeV
    │   ↓
    ├── Electronic Shells   ~ 10^15 Hz  | eV scale
    │   ↓
    └── Rotonic / Thermal   ~ 10^10–10^11 Hz  | K scale
```

Each level transmits coherence through a **memory kernel** and loses a fraction of phase alignment (interpreted as temperature).  The same mathematical structure appears from condensed matter to field theory.

---

## 6. Key Equations (Informal Overview)

**1. Fundamental dynamics:**
[
\ddot{\phi}*\ell + 2\zeta*\ell\omega_\ell\dot{\phi}*\ell + \omega*\ell^2\phi_\ell + \alpha_\ell\phi_\ell^3 = \sum_m \int_0^t K_{\ell m}(\tau),\phi_m(t-\tau),d\tau + \xi_\ell(t).
]

**2. Effective temperature from FDT:**
[
\langle \xi_\ell(t)\xi_m(t')\rangle = 2k_B T_{\mathrm{eff}},\zeta_\ell,\delta_{\ell m},\delta(t-t').
]

**3. Correction law for frequency shift:**
[
\frac{\Delta \omega}{\omega} = -\beta X - \Gamma X^2 - \Eta d X, \quad X = \Theta_D / T_c.
]

Each parameter (β, Γ, Η) corresponds to a measurable aspect of how **thermal noise and memory loss distort resonance**.

---

## 7. Validation and Studies

| Study        | Focus                                   | Current Status                                                 |
| :----------- | :-------------------------------------- | :------------------------------------------------------------- |
| **Study 01** | Mother Frequency & Thermal–Memory Shift | Complete — formal derivation, validated with Al, Pb, Nb, He-4. |
| **Study 02** | Gauge Emergence & Mode Degeneracy       | In progress — SU(3)×SU(2)×U(1) as resonance symmetry.          |
| **Study 03** | Field Coherence & Memory Propagation    | Planned — computational test of memory kernels.                |

The studies serve as **scientific modules** — each one a bridge between theory and measurable physics.

---

## 8. Simulation Roadmap

DOFT can be simulated numerically using ordinary differential equations with delay and noise.  A minimal prototype involves 4–6 coupled oscillators.

**Canonical model:**
[
\ddot{\phi}*\ell + 2\zeta*\ell\omega_\ell\dot{\phi}*\ell + \omega*\ell^2\phi_\ell + \alpha_\ell\phi_\ell^3 = \kappa(\phi_{\ell-1}-2\phi_\ell+\phi_{\ell+1}) + \xi_\ell(t).
]

**Memory kernel:**  (K_{\ell m}(\tau) = \mu_{\ell m} e^{-\tau/\tau_m}).

**Noise:**  (\langle \xi(t)\xi(t')\rangle = 2k_BT_{\mathrm{eff}}\zeta\delta(t-t')).

### Steps:

1. Initialize frequencies using prime ratios relative to ω*.
2. Integrate in time (Runge–Kutta or symplectic).
3. Compute FFT spectra and measure frequency ratios.
4. Vary noise level (X = Θ_D/T_c) and fit β, Γ, Η.
5. Verify stabilization of the prime-locking pattern.

---

## 9. Why DOFT Matters

DOFT aims to bridge domains that physics currently treats as separate:

* **Quantum field theory:** resonance and gauge symmetries.
* **Condensed matter:** coherence, temperature, and phonon structure.
* **Cosmology:** hierarchy of fields and large-scale oscillations.

By grounding all these in a single principle — *delayed resonance with memory* — DOFT provides a way to interpret constants, symmetries, and energy scales as manifestations of one coherent grammar.

> **Energy is the amplitude of existence; memory is its shape.**

---

## 10. Contributing and Testing

Researchers and developers can contribute by:

* Running simulations based on Study 01 equations.
* Extending the correction law to new materials.
* Searching for prime-locking ratios in experimental data (phonons, plasma, etc.).
* Developing visualization tools for phase coherence and drift.

Future versions of the repository will include:

* Example code (Python / C++).
* Data sets and fitting notebooks.
* A visualization package for resonance hierarchies.

---

## 11. Learn More

* 📄 [**Manifesto**](./MANIFESTO_v1.8.md) — philosophical and conceptual foundation.
* 🧠 [**Study 01**](./STUDY_01_MotherFrequency_and_ThermalMemoryShift.md) — first scientific implementation.
* 🧩 *Upcoming Studies* — deeper layers of coherence, gauge, and field structure.

---

## 12. Final Note

This repository is a bridge between intuition and measurement — a place where ideas about coherence and memory can be made testable.  DOFT is not finished; it is evolving, and its goal is to *connect what physics already knows with what it has not yet remembered.*

> **Reality is a delayed oscillator.  Everything else is resonance.**

---

*End of README — DOFT*
