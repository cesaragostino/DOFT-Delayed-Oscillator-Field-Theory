# Test Plan – DOFT Cluster Simulator (v0.2)

## 0) Convenciones

**Material de referencia:** MgB2 con subredes sigma y pi.

**Archivos:**

```
--config configs/material_config_MgB2.json
--targets configs/ground_truth_targets_MgB2.json
--weights configs/loss_weights_default.json
```

**Salida base:** `--outdir runs/<nombre_test>`

**Umbrales tentativos (ajustables):**

| Métrica | Umbral |
|----------|---------|
| \|C_AB_sim − 1.5897\| | ≤ 0.05 |
| mean(\|e_sim − e_exp\|) | ≤ 0.08 por subred |
| Si hay q_exp | \|q_sim − q_exp\| ≤ 0.4; si no hay, debe quedar “NA” sin NaNs |
| \|f0 − f0_anchor\| | ≤ 1.0 salvo tests que lo deshabilitan |
| Outputs | Sin NaNs/inf; exit code 0 |

---

## 1) Sanity / Smoke

**Objetivo:** el pipeline corre “end-to-end” sin NaNs y genera outputs.

**Cmd:**

```bash
python cli.py --config configs/material_config_MgB2.json \
  --targets configs/ground_truth_targets_MgB2.json \
  --weights configs/loss_weights_default.json \
  --outdir runs/01_smoke --max-evals 300 --seed 123
```

**Checks:**

- Archivos generados: `best_params.json`, `simulation_results.csv`, `report.md`, `manifest.json`
- Sin NaNs/inf en métricas
- Criterios base de umbrales se cumplen

---

## 2) Manejo de q_exp = null (mask por subred)

**Objetivo:** si q_exp falta en sigma, el término w_q se enmascara (no da NaN ni penaliza).

**Cmd:**

```bash
python cli.py --config configs/material_config_MgB2.json \
  --targets configs/ground_truth_targets_MgB2.json \
  --weights configs/loss_weights_default.json \
  --outdir runs/02_mask_q --max-evals 300 --seed 123
```

**Checks:**

- En el reporte, `q_error_sigma` debe figurar como “NA” o “0.0 (masked)”
- No hay NaNs en la pérdida total
- Métricas de pi con q_exp sí se calculan

---

## 3) Bounds + Clipping + Huber

**Objetivo:** validar robustez numérica y respeto de límites.

**Cmd:**

```bash
python cli.py --config configs/material_config_MgB2.json \
  --targets configs/ground_truth_targets_MgB2.json \
  --weights configs/loss_weights_default.json \
  --bounds ratios=-0.25,0.25 deltas=-0.35,0.35 f0=15,30 \
  --huber-delta 0.02 \
  --outdir runs/03_bounds_huber --max-evals 500 --seed 42
```

**Checks:**

- Ningún parámetro sale de los bounds (`best_params.json`)
- Sin explosiones numéricas; pérdida desciende estable
- Sin NaNs

---

## 4) Anclas f0 (regularización)

**Objetivo:** verificar que un w_anchor bajo estabiliza sin “forzar”.

**Cmd (ancla baja):**

```bash
python cli.py ... --anchor-weight 0.02 \
  --outdir runs/04_anchor_low --max-evals 500 --seed 7
```

**Cmd (ancla más fuerte):**

```bash
python cli.py ... --anchor-weight 0.08 \
  --outdir runs/04_anchor_high --max-evals 500 --seed 7
```

**Checks:**

- \|f0 − f0_anchor\| más chico con 0.08 que con 0.02
- No se degrada significativamente C_AB ni e_error (∆ ≤ 10% respecto a 0.02)

---

## 5) Freeze de primos (ablación estructural controlada)

**Objetivo:** medir contribución de cada primo.

**Cmd (congelar 7):**

```bash
python cli.py ... --freeze-primes 7 \
  --outdir runs/05_freeze7 --max-evals 400 --seed 21
```

**Cmd (congelar 5 y 7):**

```bash
python cli.py ... --freeze-primes 5 7 \
  --outdir runs/05_freeze57 --max-evals 400 --seed 21
```

**Checks:**

- C_AB se mantiene cercano a 1.5897 (≤ 0.05) aun sin 7
- Con menos primos, la pérdida total sube levemente pero sin colapso
- Reporte compara vs baseline (test 1)

---

## 6) Ablation matrix {2,3,5} vs {2,3,5,7} (flag --ablation)

**Objetivo:** cuantificar efecto global del 7.

**Cmd:**

```bash
python cli.py ... --ablation 2,3,5|2,3,5,7 \
  --outdir runs/06_ablation --max-evals 400 --seed 99
```

**Checks:**

- Tabla con ambos escenarios: pérdida total, C_AB_error, e_error_mean
- Esperable: {2,3,5,7} mejora levemente e_error sin romper C_AB

---

## 7) Seed sweep / estabilidad

**Objetivo:** dispersión de resultados y reproducibilidad.

**Cmd:**

```bash
python cli.py ... --seed-sweep 7 \
  --outdir runs/07_seed_sweep --max-evals 300
```

**Checks:**

- `report.md` incluye mean±std para C_AB, e_error, f0
- Std moderado: std(C_AB) ≤ 0.02, std(e_error) ≤ 0.02
- Top-1 (mejor seed) cumple los umbrales base

---

## 8) Contraste C_AB (σ vs π)

**Objetivo:** clavar el contraste ancla.

**Cmd:**

```bash
python cli.py ... --outdir runs/08_contrast --max-evals 500 --seed 5
```

**Checks:**

- \|C_AB_sim − 1.5897\| ≤ 0.03
- No empeora e_error (>15% vs test 1)

---

## 9) Residuos (consistencia log residual)

**Objetivo:** reproducir residual_exp por subred dentro de tolerancia.

**Cmd:**

```bash
python cli.py ... --outdir runs/09_residuals --max-evals 500 --seed 11
```

**Checks:**

- \|r_sim − r_exp\| ≤ 0.02 en sigma y pi (si hay r_exp)
- Si no hay r_exp en alguna subred → campo “NA” sin NaNs

---

## 10) Sensibilidad a huber-delta

**Objetivo:** robustez frente a outliers en e/q/r.

**Cmd (delta bajo):**

```bash
python cli.py ... --huber-delta 0.01 \
  --outdir runs/10_huber_low --max-evals 400 --seed 3
```

**Cmd (delta alto):**

```bash
python cli.py ... --huber-delta 0.05 \
  --outdir runs/10_huber_high --max-evals 400 --seed 3
```

**Checks:**

- Con 0.01, mayor robustez a outliers pero convergencia similar
- Con 0.05, puede bajar pérdida más rápido pero ser menos robusto
- En ambos casos, sin NaNs y C_AB dentro de ±0.05

---

## 11) Stress test (max-evals alto)

**Objetivo:** estabilidad a corridas prolongadas.

**Cmd:**

```bash
python cli.py ... --outdir runs/11_stress --max-evals 3000 --seed 1
```

**Checks:**

- No memory leak; pérdida no oscila caóticamente
- No NaNs; parámetros dentro de bounds
- Métricas finales igual o mejores que test 1

---

## 12) I/O y validación de archivos

**Objetivo:** robustez de lectura/escritura.

**Procedimiento:**

- Alterar un JSON (p. ej., quitar una clave de anchors.sigma.f0)
- Re-correr

**Expectativa:**

- Error claro y legible (mensaje con ruta y clave faltante)
- Exit code ≠ 0
- Sin archivos “a medias” (o marcados como fallidos en manifest.json)

---

## 13) Determinismo con --seed

**Objetivo:** misma salida con misma semilla.

**Cmd:**

```bash
python cli.py ... --outdir runs/13_seed_a --max-evals 400 --seed 777
python cli.py ... --outdir runs/13_seed_b --max-evals 400 --seed 777
```

**Checks:**

- `best_params.json` numéricamente idéntico (o diferencias < 1e-6)
- Métricas idénticas

---

## 14) Reportes y manifiesto

**Objetivo:** completitud y trazabilidad.

**Checks en report.md:**

- Breakdown de loss por término: e/q/r/anchor/contrast/reg
- Tablas por subred + contraste
- Seed sweep y/o ablation si se usaron flags
- Versión, fecha, flags, paths en manifest.json

---

## 15) (Opcional) Material de control: 2H-NbSe₂

**Objetivo:** validar otro binario con C_AB ≈ 0.

**Cmd:**

```bash
python cli.py --config configs/material_config_NbSe2.json \
  --targets configs/ground_truth_targets_NbSe2.json \
  --weights configs/loss_weights_default.json \
  --outdir runs/15_nbse2 --max-evals 400 --seed 13
```

**Checks:**

- \|C_AB_sim\| ≤ 0.02
- e_error_mean en σ/π similar a MgB2 (misma escala)

---

## Resumen de aceptación mínima (para marcar “verde” en CI)

Tests 1–4, 5 (freeze 7), 6 (ablation), 7 (seed-sweep), 8 (C_AB), 9 (residuales), 10 (huber-delta), 11 (stress), 12 (I/O), 13 (seed) pasan con los umbrales detallados.

**Condiciones finales:**

- No hay NaNs/inf
- Parámetros respetan bounds
- Reportes completos

