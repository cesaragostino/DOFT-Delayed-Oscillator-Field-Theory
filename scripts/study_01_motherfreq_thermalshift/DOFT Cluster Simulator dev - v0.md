# DOFT Cluster Simulator — Functional Specification

**Version:** 0.9 (draft)  
**Audience:** developers (Codex-assisted) & researchers  
**Scope:** simulador que reproduce/ajusta los “fingerprints” DOFT observados para materiales/subredes (σ/π) y generaliza para predecir patrones en nuevos materiales.

---

## 1) Purpose & Goals

**Goal.** Dado un set de ground-truth y anclas, sintetizar un modelo mínimo de **cluster de osciladores** (1–3 capas) que reproduzca:

- **Fingerprint entero** `e_exp = [exp_a_2, exp_b_3, exp_c_5, exp_d_7]`.
- **Fingerprint racional** `q_exp` (promedio de primas), si existe para la subred.
- **Residuo logarítmico** `residual_exp = log(R_corr_eta) - log(prime_value)`.
- **Contraste inter-canal** `C_AB` (p.ej., σ vs π).

**Non-goals.**

- No explica microfísica de primer principio; captura patrones DOFT efectivos.  
- No usa redes neuronales; emplea optimización de bajo/medio costo (random+local / CMA-ES).

---

## 2) Conceptos (resumen operativo)

- **Capas (L = 1..3):** osciladores acoplados por ratios discretos (primas) + correcciones suaves.  
- **Mother frequency** `f0`: frecuencia base interna.  
- **Locks enteros:** potencias sobre 2,3,5,7 → vector `e = [e2, e3, e5, e7]`.  
- **Lock racional q:** media de saltos racionales observados (cuando aplica).  
- **Residuo:** desviación en log-escala entre `R_corr_eta` y `prime_value`.  
- **Contraste C_AB:** relación de escalas entre subredes/condiciones (σ/π, 0–10 bar).

---

## 3) Entradas

### 3.1 Ground truth targets (por material/subred)

**JSON (ejemplo MgB2)**

```json
{
  "MgB2_sigma": {
    "e_exp": [1.0, 0.0, 0.0, 0.0],
    "q_exp": null,
    "residual_exp": -0.008642,
    "input_exponents": [1, 0, 0, 0]
  },
  "MgB2_pi": {
    "e_exp": [1.228, 0.7565, 0.2525, 0.489],
    "q_exp": 6.022,
    "residual_exp": -0.006469,
    "input_exponents": [3, 1, 0, 0]
  },
  "MgB2_sigma_vs_pi": { "C_AB_exp": 1.58974 }
}
```

Nota: `q_exp = null` (o `NaN`) es válido → el término de pérdida de **q** se desactiva.

### 3.2 Archivos del pipeline (opcional)

- `results_*_full_factorized.csv`: por material/subred/salto (prime_value, q, etc.).  
- `fingerprint_*_bootstrap_CIs.csv`: CIs por familia/subred (validación externa).  
- `*_log_residual.csv`: residuales pre-computados (si se prefiere).

### 3.3 Config de material

```json
{
  "material": "MgB2",
  "subnets": ["sigma", "pi"],
  "anchors": {
    "sigma": { "X": 20.82 },
    "pi":    { "X": 19.23 }
  }
}
```

`X` = parámetro-escala del ancla del pipeline (ayuda como regularizador).

---

## 4) Salidas

- **Best-fit parameters** por subred (JSON): `f0`, ratios `{r2,r3,r5,r7}`, correcciones `{delta...}`, y asignación **capa→lock**.  
- **Fingerprint simulado:** `e_sim`, `q_sim` (si aplica), `residual_sim`, `C_AB_sim`.  
- **Métricas de ajuste:** pérdida total y por término.  
- **Reportes (Markdown/CSV):** tablas exp vs sim con errores.  
- **Manifiesto:** versión, configuración y `rng_seed` para reproducibilidad.

---

## 5) Modelo de simulación (forward)

### 5.1 Parámetros por subred `s`

- Nº de capas `L ∈ {1,2,3}`  
- `f0_s > 0` (mother frequency)  
- Ratios base `r = (r2, r3, r5, r7)` (primas 2,3,5,7)  
- Correcciones suaves `δ` (pequeñas, continuas)  
- **Asignación capa→lock** (qué capa contribuye a cada exponente/salto)

### 5.2 Síntesis del fingerprint

**Entero (`e_sim`)** (potencias efectivas con *soft rounding*):
$$
 e_{k,\mathrm{sim}}=\mathrm{RoundOrSoft}\bigl(\,\phi_k(f_0,\mathbf r,\delta,L)\,\bigr),\quad k\in\{2,3,5,7\}.
$$

**Racional (`q_sim`)** (si aplica): media de primes inducidas por la ruta térmica/energética simulada.

**Residuo (`residual_sim`)**: mapear escala simulada a `\log(R_\mathrm{corr\_eta})` y comparar con `\log(\mathrm{prime\_value})`.

**Contraste (`C_AB_sim`)**: relación de escalas entre subredes/condiciones (σ/π u otras).

`φ_k(·)` puede ser mínima (productos/ratios discretos) o extendida con acoples entre capas (`alpha_12`, `alpha_23`).

---

## 6) Función de pérdida

Con subredes `S` (ej. `{sigma, pi}`) y pares `P` (ej. `{(sigma,pi)}`):

$$
\begin{aligned}
L =\;& \sum_{s\in S} w_e \,\lVert e_{\mathrm{sim}}(s)-e_{\mathrm{exp}}(s)\rVert_1 \\
&+ \sum_{s\in S} \mathbf{1}_{q_{\exp}(s)\,\mathrm{válido}}\; w_q \, \bigl|q_{\mathrm{sim}}(s)-q_{\exp}(s)\bigr| \\
&+ \sum_{s\in S} w_r \, \bigl|\mathrm{res}_{\mathrm{sim}}(s)-\mathrm{res}_{\exp}(s)\bigr| \\
&+ \sum_{(a,b)\in P} w_c \, \bigl|C_{\mathrm{sim}}(a,b)-C_{\exp}(a,b)\bigr| \\
&+ \lambda\,\Omega(\theta).
\end{aligned}
$$

- **Gate en q:** si `q_exp` es `null/NaN` → ese término **no se penaliza**.  
- **Prior suave** (opcional) en `q` si se quiere tirar a un rango plausible.  
- **Normas:** L1 por robustez; L2 opcional.  
- **Pesos base:** `w_e=1.0`, `w_q=0.5`, `w_r=0.25`, `w_c=0.3` (tuneable por material).

---

## 7) Optimización

- **Híbrido:** random/grid amplio → élites → refinamiento local (Nelder-Mead / Powell).  
- **Alternativa:** CMA-ES (cuando se habilite).  
- **Restricciones:** `f0>0`, `L ∈ {1,2,3}`, `r_k∈[0,4]` aprox., `|δ|≤0.25`.  
- **Semillas reproducibles:** `rng_seed` global y por subred.  
- **Parada:** límite de evaluaciones, mejora mínima, tolerancias.

---

## 8) CLI & API

**CLI**

```bash
# Fit por material
doft-sim fit \
  --material "MgB2" \
  --targets path/to/ground_truth_targets.json \
  --config  path/to/material_config.json \
  --outdir  runs/mgb2_sigma_pi \
  --rng-seed 42 \
  --max-evals 10000 \
  --weights '{"w_e":1.0,"w_q":0.5,"w_r":0.25,"w_c":0.3}' \
  --use-q-prior false

# Sólo forward con parámetros ya ajustados
doft-sim forward \
  --params runs/mgb2_sigma_pi/best_params.json \
  --out path/to/forward_result.json
```

**Python (esqueleto)**

```python
from doftsim import Simulator, FitConfig, Targets

targets = Targets.from_json("ground_truth_targets.json")
cfg = FitConfig.from_json("material_config.json")
sim = Simulator(cfg, targets, weights={"w_e":1.0,"w_q":0.5,"w_r":0.25,"w_c":0.3})

best = sim.fit(max_evals=10000, rng_seed=42)
sim.save(best, "runs/mgb2_sigma_pi")

fwd = sim.forward(best)
print(fwd["MgB2_sigma"]["e_sim"], fwd["MgB2_pi"]["q_sim"])
```

---

## 9) Esquemas (JSON Schema informal)

**`ground_truth_targets.json`**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "patternProperties": {
    "^[A-Za-z0-9_\\-]+$": {
      "type": "object",
      "properties": {
        "e_exp": { "type": "array", "items": { "type": "number" }, "minItems": 4, "maxItems": 4 },
        "q_exp": { "type": ["number","null"] },
        "residual_exp": { "type": "number" },
        "input_exponents": { "type": "array", "items": { "type": "number" }, "minItems": 4, "maxItems": 4 }
      },
      "required": ["e_exp", "residual_exp", "input_exponents"]
    }
  }
}
```

**`material_config.json`**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "material": { "type": "string" },
    "subnets": { "type": "array", "items": { "type": "string" } },
    "anchors": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": { "X": { "type": "number" } },
        "required": ["X"]
      }
    }
  },
  "required": ["material", "subnets"]
}
```

**`best_params.json` (salida; por subred)**

```json
{
  "material": "MgB2",
  "params": {
    "sigma": {
      "L": 2,
      "f0": 1.73,
      "ratios": { "r2": 1.0, "r3": 0.1, "r5": 0.0, "r7": 0.0 },
      "delta":  { "d2": 0.05, "d3": 0.02, "d5": 0.0, "d7": 0.0 }
    },
    "pi": {
      "L": 3,
      "f0": 1.61,
      "ratios": { "r2": 1.2, "r3": 0.7, "r5": 0.25, "r7": 0.45 },
      "delta":  { "d2": 0.03, "d3": 0.01, "d5": 0.01, "d7": 0.02 }
    }
  }
}
```

---

## 10) Políticas de NaN / faltantes

- `q_exp` faltante: **gate** local → no penalizar q (equivalente a `w_q=0` sólo en esa subred).  
- `C_AB_exp` faltante: si el par no existe, omitir término.  
- `e_exp` parcial: permitir `null` por componente y penalizar sólo donde hay dato.  
- Valores no físicos: proyección suave al dominio (*clipping*) y reintento.

---

## 11) Validación & Reportes

- Comparativas por subred: exp vs sim en `e`, `q`, `residual`, `C_AB`.  
- Resumen global de pérdidas.  
- Chequeo contra IC95 bootstrap (si hay): *flag* si sim está fuera del rango.  
- Plots opcionales: barras de `e`, distros de `q`, residuales.

---

## 12) Ejemplo mínimo — MgB₂ (σ/π)

**Targets (resumen)**  
- `sigma`: `e=[1,0,0,0]`, `q_exp=None`, `residual=-0.008642`  
- `pi`: `e≈[1.228,0.7565,0.2525,0.489]`, `q≈6.022`, `residual≈-0.006469`  
- `C_AB(σ,π)=1.58974`

**Pesos sugeridos**

```json
{"w_e":1.0, "w_q":0.5, "w_r":0.25, "w_c":0.3}
```

Nota: en **sigma**, el término `q` se apaga automáticamente.  
Búsqueda: `max_evals=10000`, `rng_seed=42`, `L ∈ {1,2,3}`.

---

## 13) Extensiones

- **kappa (cluster coefficient):** agregar término de pérdida y *forward* (si se usa).  
- **Modo multi-material:** ajuste conjunto con priors compartidos.  
- **Superfluidos:** subredes por presión (0/1/10 bar) y contrastes.  
- **Exploración bayesiana:** prior jerárquico por familia (σ/π) para `q` faltante.

---

## 14) Glosario

- `e_exp`: potencias sobre 2,3,5,7.  
- `q_exp`: promedio de primas (si aplica).  
- `residual_exp`: `log(R_corr_eta) - log(prime_value)`.  
- `C_AB`: contraste entre subredes/canales.  
- `f0`: *mother frequency* (capa interna).  
- `r_k`: contribuciones ligadas a `{2,3,5,7}`.  
- `δ`: correcciones suaves.

---

## 15) Checklist de implementación (Codex)

- [ ] Parser JSON de **targets** y **config**.  
- [ ] Generador de parámetros iniciales con semillas.  
- [ ] **Forward** (capas, ratios, síntesis de `e`, `q`, `residual`, `C_AB`).  
- [ ] Pérdida con *gates* por NaN y pesos configurables.  
- [ ] Optimizador (random+local; **CMA-ES** opcional).  
- [ ] Export de `best_params.json`, `results.csv`, `manifest.json`.  
- [ ] Reportes **.md** con tablas exp vs sim.  
- [ ] Tests mínimos (gates, dominio, reproducibilidad).

---

### Nota sobre tu caso (q de σ en MgB₂)

Está bien dejar `q_exp` como `null/NaN` y **apagar ese término** en `sigma`.  
Si más adelante aparece evidencia para `q` en `σ`, se habilita el término sin tocar el resto del diseño.  
Si necesitás suavizar el ajuste, podés activar un **prior leve** sobre `q_sim` (no obligatorio).

