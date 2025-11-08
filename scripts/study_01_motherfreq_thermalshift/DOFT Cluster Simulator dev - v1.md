# Cambios recientes en la especificación del DOFT Cluster Simulator

## Qué cambió (en una frase)

Pasamos de un esquema mínimo a uno donde:

- `ground_truth_targets.json` puede tener `q_exp=null` (se apaga ese término en la pérdida por subred),
- `material_config.json` separa subredes y anclas por nombre,
- se agregan contrastes explícitos `_vs_`,
- los pesos de la pérdida pueden venir en un JSON aparte.

---

## Especificación efectiva (lo que el código debe aceptar hoy)

### 1) `material_config.json`

**Campos obligatorios:**

- `material`: string (p.ej., "MgB2").
- `subnets`: array de subredes por nombre (p.ej., `["sigma", "pi"]`).

**Campos opcionales:**

- `anchors`: objeto `{ <subnet>: { "X": number } }` con el X de cada subred (regularización/guía).
- `contrasts`: lista de pares para evaluar `C_AB` (si existen).

**Ejemplo (vigente):** contiene material, subnets, anchors y un contraste sigma-vs-pi con `C_AB_exp=1.58974`.

**Acciones para dev:**

- Parser: leer `material`, `subnets`, `anchors` y (si está) `contrasts[*].{type,A,B,C_AB_exp}`.
- Validar que todas las subnets nombradas en contrasts existan en subnets.
- Guardar `anchors[s].X` como regularizador suave (peso chico).

---

### 2) `ground_truth_targets.json`

**Claves por subred con el patrón `<Material>_<subnet>` y por contraste con `<Material>_<A>_vs_<B>`.**

**Para subred:**

- `e_exp`: `[e2,e3,e5,e7]` (floats permitidos).
- `q_exp`: number | null (si null/NaN → no penalizar q en esa subred).
- `residual_exp`: número (log-residual objetivo).
- `input_exponents`: vector entero de entrada (documental/chequeo).

**Para contraste:**

- `C_AB_exp`: número (ej. 1.58974 para σ vs π).

**Ejemplo:** `MgB2_sigma` tiene `e_exp=[1,0,0,0]`, `q_exp=null`, `residual_exp≈-0.008642`; `MgB2_pi` tiene `q_exp≈6.022`; y `MgB2_sigma_vs_pi` fija `C_AB_exp≈1.58974`. El término de `q` para σ debe quedar *gateado* (off).

**Acciones para dev:**

- Parser: si `q_exp` es null/NaN, marcar `use_q=false` en esa subred.
- En la pérdida, multiplicar el término de q por 1 o 0 según `use_q`.
- Aceptar floats en `e_exp` (no redondear previo a la pérdida; el forward ya hace soft-rounding).

---

### 3) `loss_weights_default.json`

**Estructura simple con pesos:**

```json
{"w_e":1.0, "w_q":0.5, "w_r":0.25, "w_c":0.3, "w_anchor":0.05}
```

(puede faltar `w_anchor`; poner default 0.0)

**Acciones para dev:**

- Cargar si se provee; si no, usar defaults embebidos.

**Pérdida total:**

```
L = Σ_s w_e * L_e + Σ_s gate(q)*w_q * L_q + Σ_s w_r * L_r + Σ_pairs w_c * L_c + w_anchor * Ω_anchor
```

---

## Cambios de código mínimos (diff conceptual)

### Capa de datos

**Antes:** esquema rígido sin contrasts/gating de q.  
**Ahora:**

**Targets:**

- `targets[subnet].e_exp`: float[4]  
- `targets[subnet].q_exp`: Optional[float]  
- `targets[subnet].residual_exp`: float  
- `targets["<A>_vs_<B>"].C_AB_exp`: float (opcional)  
- `targets[subnet].use_q = (q_exp is not None and not NaN)`

**Config:**

- `config.material`: str  
- `config.subnets`: List[str]  
- `config.anchors`: Dict[str, {"X": float}] (opcional)  
- `config.contrasts`: List[{type,A,B,C_AB_exp}] (opcional)

---

### Forward

Igual que en la spec: calcula `e_sim`, `q_sim` (si aplica), `residual_sim`, y `C_AB_sim` para pares `{(A,B)}` definidos.  
(Ver “Modelo de simulación (forward)” y “Contraste” en el doc principal.)

---

### Pérdida

- `L_e`: L1 entre vectores `e_sim` y `e_exp`.
- `L_q`: |q_sim − q_exp| solo si `use_q=true`.
- `L_r`: |residual_sim − residual_exp|.
- `L_c`: |C_AB_sim − C_AB_exp| por cada par.
- `Ω_anchor`: penaliza desviarse de `X` (si anchors existe) con un término suave (ej., L2 sobre escala simulada vs X).

**Pesos desde `loss_weights_default.json`.**

---

### NaN / faltantes

- `q_exp=null/NaN` → `use_q=false` (no tocar el resto de la pérdida).  
- Si no hay contrasts, `L_c=0`.  
- Si falta anchors, `w_anchor` se ignora.

---

## Ejemplos concretos (del repo actual)

- **Config MgB2:** subredes y anclas (`σ: 20.82`, `π: 19.23`) y contraste σ–π (`C_AB=1.58974`). Esto ya está representado en `material_config_MgB2.json`.
- **Targets MgB2:** σ sin `q_exp` (se apaga el término) y π con `q_exp≈6.022`. Incluye `residual_exp` e `input_exponents`. Esto ya está en `ground_truth_targets_MgB2.json`.

**Especificación de simulador** con modelo, pérdidas y CLI (lo que debe implementar el runner). Úsese como contrato para la implementación.

---

## Checklist para el programador (implementar sin ambigüedad)

- [ ] Actualizar modelos de datos (**Targets**, **Config**, **LossWeights**) según lo de arriba.  
- [ ] Gating de q por subred (`use_q=false` si `q_exp==null/NaN`).  
- [ ] Soportar contrasts (pares {A,B}) y calcular `C_AB_sim`.  
- [ ] Leer anchors y aplicar `w_anchor` si está definido.  
- [ ] Mantener tolerancias y cotas del optimizador (`f0>0`, `L∈{1..3}`, ratios en rango).  
- [ ] Exportar `best_params.json`, `results.csv`, y un reporte `.md` exp vs sim.  
- [ ] Semillas reproducibles (`rng_seed`).  
- [ ] Tests: (i) gating de q, (ii) ausencia/presencia de contrasts, (iii) anchors opcional.

