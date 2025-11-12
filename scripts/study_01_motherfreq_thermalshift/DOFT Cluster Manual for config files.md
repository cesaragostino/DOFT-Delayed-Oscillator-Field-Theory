# DOFT Cluster Simulator — Manual para preparar `material_config.json`, `ground_truth_targets.json` y `loss_weights*.json` (desde tu dataset previo)

**Objetivo:** que cualquier persona (o script) pueda construir correctamente los **3 JSON de entrada** del simulador a partir de los artefactos que ya generaste con el pipeline anterior (CSV/PNG/MD), **sin ambigüedades de nombres** y con **validaciones mínimas** para evitar errores del tipo “Missing target for subnet”.

---

## 0) Qué necesito tener a mano (del pipeline previo)

De tus corridas anteriores (v4/v5) vas a usar:

### Base de materiales crudos
**`materials_clusters_real_v5.csv`**  
Campos típicos por fila: `name, sub_network, category, Tc_K, Gap_meV, ThetaD_K, EF_eV, lock_family, notes`

### Resultados factorados (por material/subred/salto)
**`results_*_full_factorized.csv`**  
Columnas: `material, sub_network, jump_desc, prime_value, fingerprint_str, (q opcional)`

- Sirve para reconstruir exponentes enteros `e_exp = [e2,e3,e5,e7]` (desde `fingerprint_str`).
- Sirve para **q** cuando está por fila/salto o para validar que existe.

### Resumen de fingerprints por familia/subred (bootstrap)
**`fingerprint_*_bootstrap_CIs.csv`**

- Sirve para **q_avg** por `category` o `category+sub_network` cuando no hay *q* por material.
- También podés usar los intervalos como **prior suave**.

### Residuales logarítmicos
**`fingerprint_*_log_residual.csv`** o reporte con tabla *“Reporte de Fingerprint Residual (log(R_corr_eta) − log(prime_value))”* por `category, sub_network`.

- Sirve para **`residual_exp`** (si no hay por material, usar el **mean** de su `category+sub_network`).

### Contraste intra-material (clusters)
`results_cluster_*` o el diagnóstico de cluster donde aparece **C_AB** (p. ej. “MgB2 (sigma vs pi) → C_AB=1.5897”).

- Sirve para claves **`_vs_`** del `ground_truth_targets.json`.

### Parámetros globales (calibración)
`results_*_calib.csv` o tu `doft_config.json` (si lo tenés)

- Sirve para fijar **η (Eta)** global del simulador (si querés mantener la coherencia).  
  En tus corridas, η típicamente **~ 3.9e-05 – 4.0e-05**.

> **Disciplina de nombres:** mantené el string **exacto** de `name` y `sub_network` como aparece en `materials_clusters_real_v5.csv` y/o en los resultados factorados. Ese es el mayor motivo de errores.

---

## 1) Archivo `material_config.json`

### 1.1. Estructura mínima
```json
{
  "material": {
    "name": "Hg",                     
    "category": "SC_TypeI",           
    "eta": 3.98e-05,                  
    "primes": {
      "2": { "enabled": true },
      "3": { "enabled": true },
      "5": { "enabled": true },
      "7": { "enabled": true }
    },
    "subnets": [
      {
        "name": "single",            
        "enabled": true,               
        "thermal": {
          "ThetaD_K": 96.0,
          "EF_eV": 5.5
        },
        "prime_layers": {             
          "2": 1,
          "3": 1,
          "5": 1,
          "7": 1
        },
        "anchors": [
          
          
        ],
        "f0_init_range": [15.0, 30.0]
      }
    ]
  }
}
```

### 1.2. Cómo llenar cada campo
- **`name`**: igual al `name` de tu CSV base para ese material.
- **`category`**: familia (`SC_TypeI`, `SC_TypeII`, etc.). Ayuda en reportes.
- **`eta`**: copiá el η de tu última calibración (para coherencia con DOFT previo). Si no lo sabés, omitilo (default interno), pero es recomendable fijarlo.
- **`primes.enabled`**: dejá `true` los primos que querés usar (por ahora 2,3,5,7).
- **`subnets[].name`**: debe coincidir **exactamente** con las subredes de tu dataset:
  - Monorred: `"single"`.
  - Multired: `"sigma"`, `"pi"` (el contraste `_vs_` va en *targets*, no aquí).
- **`thermal.ThetaD_K / EF_eV`**: desde `materials_clusters_real_v5.csv` (por subred).
- **`prime_layers`**: asignación fija por primo. Si no sabés, empezá con todos `1`. Para estudios con capas podés fijar p.ej. `{ "2":1, "3":2, "5":2, "7":1 }`.
- **`anchors` (opcional):**
  - `{ "type": "f0", "value": X, "weight": w }` → ancla de frecuencia base.
  - `{ "type": "X",  "value": X_clean, "weight": w }` → ancla térmica (si la usás).
- **`f0_init_range`**: rango de búsqueda de `f0` (usaste `[15,30]` o bandas 20.5–21.2).

> **Validación rápida:** al menos **una** subred con `"enabled": true`; si no → error: *“material_config.json debe incluir al menos una subred habilitada”*.

---

## 2) Archivo `ground_truth_targets.json`

Contiene objetivos empíricos para comparar la simulación: `e_exp`, `q_exp`, `residual_exp` por subred y, si aplica, **contrastes** `_vs_`.

### 2.1. Estructura
```json
{
  "material": "Hg",
  "targets": {
    "single": {
      "e_exp": [0.80, 0.66, 0.52, 0.31],
      "q_exp": 6.50,
      "residual_exp": -0.0184,
      "input_exponents": [1,0,0,0]
    }
    
    
  }
}
```

Para materiales multired, agregá `"sigma"`, `"pi"`, etc., y contrastes:
```json
{
  "material": "MgB2",
  "targets": {
    "sigma": { "e_exp": [1,0,0,0], "q_exp": null, "residual_exp": -0.008642 },
    "pi":    { "e_exp": [1.228,0.7565,0.2525,0.489], "q_exp": 6.022, "residual_exp": -0.006469 },
    "sigma_vs_pi": { "C_AB_exp": 1.5897 }
  }
}
```

### 2.2. De dónde sacar cada cosa
- **`e_exp = [e2,e3,e5,e7]`**
  - **A (mejor):** por material/subred desde *factorized CSV*. Usá `fingerprint_str` o columnas `exp_a_2…exp_d_7`.
  - **Proxy:** promedios por `category` (dejá constancia).
- **`q_exp`**
  - **A (ideal):** por material/subred en `results_*_full_factorized.csv` (`q`) o en `bootstrap_CIs` por `category+sub_network` (`q_avg`).
  - **B (no hay q):** poné `null` u omití; la pérdida aplicará **gating** (`w_q=0`) hasta tener un valor confiable.
- **`residual_exp`**
  - Fórmula pipeline: `residual = log_R - eta*X - log(prime_value)` (con `ε=1e-12`).
  - Usá **mean** por `category+sub_network` si no hay por material. En casos dudosos, `0.0` como proxy (declarálo).
- **Contrastes `_vs_`**
  - Para multired (p.ej. MgB2): `"sigma_vs_pi": { "C_AB_exp": <valor> }` del reporte de clusters.  
  - Para presión: `"0-bar_vs_10-bar": { "C_AB_exp": ... }`.

> **Claves exactas:** subredes en *targets* deben coincidir con `material_config.json`. Para contrastes: **`<subA>_vs_<subB>`** en minúsculas y con guión bajo.

---

## 3) Archivo `loss_weights*.json`

Podés usar un *default* y variantes.

### 3.1. Default suave
```json
{
  "w_e": 1.0,
  "w_q": 0.5,
  "w_r": 0.25,
  "w_c": 0.30,
  "w_anchor": 0.05,
  "lambda_reg": 0.0,
  "q_gate": {
    "sigma": 0,
    "single": 1,
    "pi": 1
  }
}
```

### 3.2. Ancla fuerte (para estabilizar `f0`)
```json
{
  "w_e": 1.0,
  "w_q": 0.5,
  "w_r": 0.25,
  "w_c": 0.30,
  "w_anchor": 0.25,
  "lambda_reg": 0.0,
  "q_gate": { "sigma": 0, "single": 1, "pi": 1 }
}
```

---

## 4) Procedimiento paso a paso (receta)

1. **Elegí el material** (empezá por simples: Al, Sn, In, Pb de *Type I*).
2. **Abrí `materials_clusters_real_v5.csv`** y recuperá `ThetaD_K` y `EF_eV` para la subred `single` (o `sigma/pi`). Confirmá `category`.
3. **Abrí `results_*_full_factorized.csv`** → filtrá `material` y `sub_network` → extraé `fingerprint_str` o columnas de exponentes → construí `e_exp`. Si hay `q` por subred, extraelo; si no, `null`.
4. **Abrí `fingerprint_*_bootstrap_CIs.csv`** → si falta `q` por material/subred, tomá `q_avg` por `category` o `category+sub_network` y usalo como `q_exp`.
5. **Residuales**: si tenés `fingerprint_*_log_residual.csv` por `category+sub_network`, tomá el `mean` y ponelo como `residual_exp`; si no, `0.0` o bajá `w_r` temporalmente.
6. **Contrastes**: si hay pares (`sigma` vs `pi`, `0-bar` vs `10-bar`, etc.), buscá su `C_AB` y agregá la clave `<subA>_vs_<subB>` en *targets*.
7. **Armá `material_config.json`**: `name, category, eta (opcional), subnets` con `thermal`, `prime_layers`, `anchors (opcional)`, `f0_init_range`.
8. **Armá `ground_truth_targets.json`** con las reglas del punto 2.
9. **Armá `loss_weights*.json`** (default o ancla fuerte).
10. **Smoke test**:
    ```bash
    --bounds ratios=-0.25,0.25 deltas=-0.35,0.35 f0=15,30 \
    --seed-sweep 10 --max-evals 300 --huber-delta 0.02
    ```
11. **Verificá**: sin `KeyError: Missing target for subnet '<objeto>'`; pérdida y métricas en escala esperada; `C_AB_sim` razonable; `e_abs_mean` y `|Δq|` contenidos. Si el optimizador viola anclas, subí `w_anchor` o cerrá `f0_init_range`.

---

## 5) Convenciones de nombres (evitan el 90% de errores)

- **Material `name` exacto:** `"Sn"`, `"Al"`, `"In"`, `"Pb"`, `"Hg"`, `"MgB2"`, etc. Evitá sufijos/prefijos no usados en tus CSV.
- **Subred `name` exacto:** `"single"`, `"sigma"`, `"pi"`, `"0-bar"`, `"10-bar"`, etc.
- **Contrastes en targets:** `"<subA>_vs_<subB>"`. *Nunca* en `material_config.json`.

---

## 6) Ejemplos “simples” (Type I) — plantillas
> **ATENCIÓN:** Los números son orientativos. Reemplazalos con tus valores reales.

### 6.1. Estaño (Sn) — monorred
**`configs/study01/material_config_Sn.json`**
```json
{
  "material": {
    "name": "Sn",
    "category": "SC_TypeI",
    "eta": 3.98e-05,
    "primes": { "2": {"enabled": true}, "3": {"enabled": true}, "5": {"enabled": true}, "7": {"enabled": true} },
    "subnets": [
      {
        "name": "single",
        "enabled": true,
        "thermal": { "ThetaD_K": 195.0, "EF_eV": 10.2 },
        "prime_layers": { "2": 1, "3": 1, "5": 1, "7": 1 },
        "anchors": [],
        "f0_init_range": [15.0, 30.0]
      }
    ]
  }
}
```

**`configs/study01/ground_truth_targets_Sn.json`**
```json
{
  "material": "Sn",
  "targets": {
    "single": {
      "e_exp": [1.56, 0.82, 0.52, 0.41],
      "q_exp": 6.18,
      "residual_exp": -0.042,
      "input_exponents": [1,0,0,0]
    }
  }
}
```

**`configs/study01/loss_weights_default_Sn.json`**
```json
{
  "w_e": 1.0, "w_q": 0.5, "w_r": 0.25, "w_c": 0.0, "w_anchor": 0.05, "lambda_reg": 0.0,
  "q_gate": { "single": 1 }
}
```

### 6.2. Aluminio (Al)
```json
{
  "material": {
    "name": "Al",
    "category": "SC_TypeI",
    "eta": 3.98e-05,
    "primes": { "2": {"enabled": true}, "3": {"enabled": true}, "5": {"enabled": true}, "7": {"enabled": true} },
    "subnets": [
      {
        "name": "single",
        "enabled": true,
        "thermal": { "ThetaD_K": 428.0, "EF_eV": 11.7 },
        "prime_layers": { "2": 1, "3": 1, "5": 1, "7": 1 },
        "anchors": [],
        "f0_init_range": [15.0, 30.0]
      }
    ]
  }
}
```
```json
{
  "material": "Al",
  "targets": {
    "single": {
      "e_exp": [1.40, 0.80, 0.52, 0.40],
      "q_exp": 6.18,
      "residual_exp": -0.042,
      "input_exponents": [1,0,0,0]
    }
  }
}
```

### 6.3. Indio (In)
```json
{
  "material": {
    "name": "In",
    "category": "SC_TypeI",
    "eta": 3.98e-05,
    "primes": { "2": {"enabled": true}, "3": {"enabled": true}, "5": {"enabled": true}, "7": {"enabled": true} },
    "subnets": [
      {
        "name": "single",
        "enabled": true,
        "thermal": { "ThetaD_K": 108.0, "EF_eV": 10.7 },
        "prime_layers": { "2": 1, "3": 1, "5": 1, "7": 1 },
        "anchors": [],
        "f0_init_range": [15.0, 30.0]
      }
    ]
  }
}
```
```json
{
  "material": "In",
  "targets": {
    "single": {
      "e_exp": [1.56, 0.82, 0.52, 0.41],
      "q_exp": 6.18,
      "residual_exp": -0.042,
      "input_exponents": [1,0,0,0]
    }
  }
}
```

### 6.4. Plomo (Pb)
```json
{
  "material": {
    "name": "Pb",
    "category": "SC_TypeI",
    "eta": 3.98e-05,
    "primes": { "2": {"enabled": true}, "3": {"enabled": true}, "5": {"enabled": true}, "7": {"enabled": true} },
    "subnets": [
      {
        "name": "single",
        "enabled": true,
        "thermal": { "ThetaD_K": 96.0, "EF_eV": 9.5 },
        "prime_layers": { "2": 1, "3": 1, "5": 1, "7": 1 },
        "anchors": [],
        "f0_init_range": [15.0, 30.0]
      }
    ]
  }
}
```
```json
{
  "material": "Pb",
  "targets": {
    "single": {
      "e_exp": [1.94, 0.58, 0.52, 0.41],
      "q_exp": 6.18,
      "residual_exp": -0.074,
      "input_exponents": [2,0,0,0]
    }
  }
}
```

> **Reemplazá** los números por los tuyos:
> - `ThetaD_K` y `EF_eV` del CSV.  
> - `e_exp` del *factorized* por material (o promedios de categoría).  
> - `q_exp` desde *bootstrap_CIs* por categoria/subred o *full_factorized* si existe por material.  
> - `residual_exp` desde tu tabla de residuales (mean para `SC_TypeI/single` si no tenés por material).

---

## 7) Checklist y errores típicos

- **Missing target for subnet '{...}'** → La clave en `targets` debe ser un **string** exacto (`"single"`, `"sigma"`, `"pi"`). Estructura correcta: `"targets": { "single": { ... } }`.
- **Debe incluir al menos una subred habilitada** → En `material_config.json` asegurate de `"enabled": true` en al menos una subred.
- **No aparece q para una subred (NaN/None)** → Dejá `q_exp` como `null` u omitilo y activá `q_gate=0` para esa subred en los `loss_weights`.
- **Conflicto de ancla `f0`** → Subí `w_anchor` o acotá `f0_init_range`. Si la solución exige `ratios/deltas` extremos: (a) bajá el ancla, (b) revisá `prime_layers`, (c) subí `w_c` si hay contraste confiable.
- **`C_AB_sim` se desvía mucho** → Subí `w_c` (0.5–0.8) y verificá *targets* de ambas subredes (`e/q/residual`). Revisá `prime_layers` y coherencia térmica (`ThetaD_K`, `EF_eV`).

---

## 8) Comandos de smoke/referencia

```bash
# Smoke simple
python3 -m scripts.doft_cluster_simulator.cli \
  --config configs/study01/material_config_Sn.json \
  --targets configs/study01/ground_truth_targets_Sn.json \
  --weights configs/study01/loss_weights_default_Sn.json \
  --bounds ratios=-0.25,0.25 deltas=-0.35,0.35 f0=15,30 \
  --huber-delta 0.02 \
  --outdir runs/sn_smoke --max-evals 400 --seed-sweep 10

# Con ancla fuerte de f0
python3 -m scripts.doft_cluster_simulator.cli \
  --config configs/study01/material_config_Sn.json \
  --targets configs/study01/ground_truth_targets_Sn.json \
  --weights configs/study01/loss_weights_anchor_strong.json \
  --bounds ratios=-0.25,0.25 deltas=-0.35,0.35 f0=20.5,21.2 \
  --huber-delta 0.02 \
  --outdir runs/sn_anchor --max-evals 800 --seed-sweep 10
```

---

## 9) Recomendación de flujo para construir en lote (muchos materiales)

Hacé un **script generador** que:

1. Lee `materials_clusters_real_v5.csv`.
2. Filtra `category in ["SC_TypeI"]` y materiales elegidos.
3. Rellena `ThetaD_K`, `EF_eV`, `prime_layers = {2:1,3:1,5:1,7:1}`, `f0_init_range`.
4. Busca en *factorized/bootstraps/residuales* los `e_exp`, `q_exp (o null)`, `residual_exp`.
5. Si encuentra **C_AB** (para multired) agrega `_vs_`.
6. Emite tres archivos por material en `configs/study01/`:
   - `material_config_<NAME>.json`
   - `ground_truth_targets_<NAME>.json`
   - `loss_weights_default_<NAME>.json`
7. Corre el **smoke** y, si todo ok, arma una **seed-sweep**.

