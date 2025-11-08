"""Data structures and parsers for the DOFT cluster simulator."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
import json
import math


PRIMES: Tuple[int, int, int, int] = (2, 3, 5, 7)
PRIME_KEYS: Tuple[str, str, str, str] = ("r2", "r3", "r5", "r7")
DELTA_KEYS: Tuple[str, str, str, str] = ("d2", "d3", "d5", "d7")


@dataclass
class LossWeights:
    """Collection of weights for each component of the loss function."""

    w_e: float = 1.0
    w_q: float = 0.5
    w_r: float = 0.25
    w_c: float = 0.3
    w_anchor: float = 0.05

    @classmethod
    def from_json(cls, data: Dict[str, float]) -> "LossWeights":
        kwargs = {k: float(v) for k, v in data.items() if hasattr(cls, k)}
        return cls(**kwargs)


@dataclass
class SubnetConfig:
    """Configuration hints and bounds for a subnet."""

    name: str
    enabled: bool = True
    l_candidates: List[int] = field(default_factory=lambda: [1, 2, 3])
    f0_anchor: Optional[float] = None
    f0_range: Optional[Tuple[float, float]] = None
    init_L: Optional[int] = None
    init_ratios: Dict[str, float] = field(default_factory=dict)
    ratio_abs_max: Optional[float] = None


@dataclass
class OptimizationSettings:
    """Optional optimization hints sourced from the config file."""

    n_random_starts: Optional[int] = None
    seed: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, object]]) -> "OptimizationSettings":
        if not isinstance(data, dict):
            return cls()
        n_random = data.get("n_random_starts")
        seed = data.get("seed")
        return cls(
            n_random_starts=int(n_random) if isinstance(n_random, (int, float)) else None,
            seed=int(seed) if isinstance(seed, (int, float)) else None,
        )


@dataclass
class SubnetTarget:
    """Target observables for a single subnet."""

    e_exp: Optional[List[Optional[float]]] = None
    q_exp: Optional[float] = None
    residual_exp: Optional[float] = None
    input_exponents: Optional[List[int]] = None
    use_q: bool = True

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "SubnetTarget":
        def _clean_e(values: Optional[Iterable[Optional[float]]]) -> Optional[List[Optional[float]]]:
            if values is None:
                return None
            cleaned: List[Optional[float]] = []
            for value in values:
                if value is None:
                    cleaned.append(None)
                    continue
                if isinstance(value, (int, float)) and math.isnan(value):
                    cleaned.append(None)
                else:
                    cleaned.append(float(value))
            return cleaned

        q_value = data.get("q_exp")
        if isinstance(q_value, (int, float)) and math.isnan(q_value):
            q_value = None

        residual_value = data.get("residual_exp")
        if isinstance(residual_value, (int, float)) and math.isnan(residual_value):
            residual_value = None

        input_exponents = data.get("input_exponents")
        if input_exponents is not None:
            input_exponents = [int(v) for v in input_exponents]

        q_clean = None if q_value is None else float(q_value)
        return cls(
            e_exp=_clean_e(data.get("e_exp")),
            q_exp=q_clean,
            residual_exp=None if residual_value is None else float(residual_value),
            input_exponents=input_exponents,
            use_q=q_clean is not None,
        )


@dataclass
class ContrastTarget:
    """Target contrast between two subnets."""

    subnet_a: str
    subnet_b: str
    value: Optional[float]
    label: Optional[str] = None


@dataclass
class SubnetParameters:
    """Simulation parameters for a subnet."""

    L: int
    f0: float
    ratios: Dict[str, float] = field(default_factory=dict)
    delta: Dict[str, float] = field(default_factory=dict)
    layer_assignment: List[int] = field(default_factory=list)

    def copy(self) -> "SubnetParameters":
        return SubnetParameters(
            L=self.L,
            f0=self.f0,
            ratios=dict(self.ratios),
            delta=dict(self.delta),
            layer_assignment=list(self.layer_assignment),
        )


def _normalize_subnet_name(name: str, material: str) -> str:
    prefix = f"{material}_"
    if name.startswith(prefix):
        return name[len(prefix) :]
    return name


def _normalize_ratio_key(key: str) -> Optional[str]:
    cleaned = str(key).strip().lower()
    if cleaned.startswith("r") and cleaned[1:].isdigit():
        cleaned = cleaned[1:]
    if cleaned in {"2", "3", "5", "7"}:
        return f"r{cleaned}"
    if cleaned in {"r2", "r3", "r5", "r7"}:
        return cleaned
    return None


def _normalize_ratio_mapping(values: Optional[Dict[str, object]]) -> Dict[str, float]:
    if not isinstance(values, dict):
        return {}
    normalized: Dict[str, float] = {}
    for key, value in values.items():
        prime_key = _normalize_ratio_key(str(key))
        if prime_key is None:
            continue
        normalized[prime_key] = float(value)
    return normalized


def _parse_subnet_configs(material: str, data: Dict[str, object]) -> Tuple[Dict[str, SubnetConfig], List[str]]:
    subnet_configs: Dict[str, SubnetConfig] = {}
    enabled_order: List[str] = []

    raw_networks = data.get("sub_networks")
    if isinstance(raw_networks, dict):
        items = raw_networks.items()
    elif isinstance(raw_networks, list):
        items = []
        for entry in raw_networks:
            if isinstance(entry, dict):
                name = entry.get("name")
                spec = entry
            else:
                name = entry
                spec = {}
            items.append((name, spec))
    else:
        items = []

    for raw_name, spec in items:
        if raw_name is None:
            continue
        name = _normalize_subnet_name(str(raw_name), material)
        subnet_configs[name] = _build_subnet_config(name, spec)
        if subnet_configs[name].enabled:
            enabled_order.append(name)

    raw_subnets = data.get("subnets", [])
    if isinstance(raw_subnets, list):
        for entry in raw_subnets:
            name = _normalize_subnet_name(str(entry), material)
            if name not in subnet_configs:
                subnet_configs[name] = SubnetConfig(name=name)
            if subnet_configs[name].enabled and name not in enabled_order:
                enabled_order.append(name)

    if not subnet_configs and enabled_order:
        subnet_configs = {name: SubnetConfig(name=name) for name in enabled_order}

    return subnet_configs, enabled_order


def _build_subnet_config(name: str, spec: object) -> SubnetConfig:
    if not isinstance(spec, dict):
        spec = {}
    enabled = bool(spec.get("enabled", True))

    raw_l = spec.get("L_candidates") or spec.get("l_candidates") or spec.get("L_options")
    l_candidates = _clean_l_candidates(raw_l)
    if not l_candidates:
        l_candidates = [1, 2, 3]

    f0_anchor = spec.get("f0_anchor", spec.get("X_anchor"))
    f0_anchor = float(f0_anchor) if isinstance(f0_anchor, (int, float)) else None

    f0_range = None
    raw_range = spec.get("f0_range") or spec.get("f0_bounds")
    if isinstance(raw_range, (list, tuple)) and len(raw_range) == 2:
        lo = float(raw_range[0])
        hi = float(raw_range[1])
        if hi < lo:
            lo, hi = hi, lo
        if lo != hi:
            f0_range = (lo, hi)

    init_spec = spec.get("init")
    if not isinstance(init_spec, dict):
        init_spec = None
    init_L = None
    init_ratios: Dict[str, float] = {}
    if isinstance(init_spec, dict):
        init_L_value = init_spec.get("L") or init_spec.get("l")
        if isinstance(init_L_value, (int, float)):
            init_L = max(1, int(init_L_value))
        init_ratios = _normalize_ratio_mapping(init_spec.get("ratios"))

    bounds = spec.get("bounds") if isinstance(spec.get("bounds"), dict) else None
    ratio_abs_max = None
    if bounds and "ratio_abs_max" in bounds:
        raw_ratio_max = bounds["ratio_abs_max"]
        if isinstance(raw_ratio_max, (int, float)) and raw_ratio_max > 0:
            ratio_abs_max = float(raw_ratio_max)

    return SubnetConfig(
        name=name,
        enabled=enabled,
        l_candidates=l_candidates,
        f0_anchor=f0_anchor,
        f0_range=f0_range,
        init_L=init_L,
        init_ratios=init_ratios,
        ratio_abs_max=ratio_abs_max,
    )


def _clean_l_candidates(values: object) -> List[int]:
    if not isinstance(values, (list, tuple)):
        return []
    cleaned = []
    for value in values:
        if isinstance(value, (int, float)):
            cleaned.append(max(1, min(3, int(value))))
    deduped = sorted(set(cleaned))
    return deduped


def _parse_contrasts(material: str, subnets: List[str], raw_contrasts: object) -> List[ContrastTarget]:
    if raw_contrasts is None:
        return []
    results: List[ContrastTarget] = []
    subnet_set = set(subnets)

    def _append_contrast(a_name: str, b_name: str, value: Optional[object], label: Optional[str]) -> None:
        if value is None:
            return
        if a_name not in subnet_set or b_name not in subnet_set:
            raise ValueError(f"Contraste inválido: {a_name} o {b_name} no definidos en subnets")
        value_float = float(value)
        results.append(
            ContrastTarget(
                subnet_a=f"{material}_{a_name}",
                subnet_b=f"{material}_{b_name}",
                value=value_float,
                label=label,
            )
        )

    if isinstance(raw_contrasts, dict):
        for key, entry in raw_contrasts.items():
            if isinstance(entry, dict) and entry.get("enabled", True) is False:
                continue
            label = entry.get("type") if isinstance(entry, dict) else None
            value = None
            a_raw = None
            b_raw = None
            if isinstance(entry, dict):
                value = entry.get("target", entry.get("C_AB_exp"))
                a_raw = entry.get("A") or entry.get("a")
                b_raw = entry.get("B") or entry.get("b")
            if (a_raw is None or b_raw is None) and isinstance(key, str) and "_vs_" in key:
                parts = key.split("_vs_", 1)
                a_raw = parts[0]
                b_raw = parts[1]
            if a_raw is None or b_raw is None:
                raise ValueError("Cada contraste debe definir los campos 'A' y 'B' o usar una clave *_vs_*")
            a_name = _normalize_subnet_name(str(a_raw), material)
            b_name = _normalize_subnet_name(str(b_raw), material)
            label_value = str(label) if label else (key if isinstance(key, str) else None)
            _append_contrast(a_name, b_name, value, label_value)
        return results

    if isinstance(raw_contrasts, list):
        for entry in raw_contrasts:
            if not isinstance(entry, dict):
                continue
            if entry.get("enabled", True) is False:
                continue
            value = entry.get("C_AB_exp") or entry.get("target")
            a_raw = entry.get("A") or entry.get("a")
            b_raw = entry.get("B") or entry.get("b")
            if a_raw is None or b_raw is None:
                raise ValueError("Cada contraste debe definir los campos 'A' y 'B'")
            a_name = _normalize_subnet_name(str(a_raw), material)
            b_name = _normalize_subnet_name(str(b_raw), material)
            label = entry.get("type")
            _append_contrast(a_name, b_name, value, str(label) if label else None)
        return results

    return results


@dataclass
class MaterialConfig:
    """Description of the material, subnets, anchors, and optional contrasts."""

    material: str
    subnets: List[str]
    anchors: Dict[str, Dict[str, float]]
    contrasts: List[ContrastTarget] = field(default_factory=list)
    subnet_configs: Dict[str, SubnetConfig] = field(default_factory=dict)
    optimization: OptimizationSettings = field(default_factory=OptimizationSettings)

    @classmethod
    def from_file(cls, path: Path) -> "MaterialConfig":
        data = json.loads(Path(path).read_text())
        material = str(data["material"])
        subnet_configs, subnet_order = _parse_subnet_configs(material, data)
        if not subnet_order:
            raise ValueError("material_config.json debe incluir al menos una subred habilitada")

        anchors: Dict[str, Dict[str, float]] = {}
        raw_anchors = data.get("anchors")
        if isinstance(raw_anchors, dict):
            for subnet, anchor_data in raw_anchors.items():
                normalized = _normalize_subnet_name(str(subnet), material)
                anchors[normalized] = {key: float(value) for key, value in anchor_data.items()}
        for name, subnet_cfg in subnet_configs.items():
            if subnet_cfg.f0_anchor is not None:
                anchors.setdefault(name, {"X": float(subnet_cfg.f0_anchor)})

        contrasts = _parse_contrasts(material, subnet_order, data.get("contrasts"))
        optimization = OptimizationSettings.from_dict(data.get("optimization"))

        return cls(
            material=material,
            subnets=subnet_order,
            anchors=anchors,
            contrasts=contrasts,
            subnet_configs=subnet_configs,
            optimization=optimization,
        )


@dataclass
class TargetDataset:
    """Collection of subnet targets and optional contrast entries."""

    subnets: Dict[str, SubnetTarget]
    contrasts: List[ContrastTarget]

    @classmethod
    def from_file(cls, path: Path) -> "TargetDataset":
        raw = json.loads(Path(path).read_text())
        subnets: Dict[str, SubnetTarget] = {}
        contrasts: List[ContrastTarget] = []
        for key, value in raw.items():
            if "_vs_" in key:
                parts = key.split("_vs_")
                if len(parts) != 2:
                    raise ValueError(f"Invalid contrast key: {key}")
                base = parts[0]
                other = parts[1]
                prefix = base.split("_")[0]
                if "_" not in other:
                    other = f"{prefix}_{other}"
                contrast_value = float(value["C_AB_exp"]) if isinstance(value, dict) else float(value)
                contrasts.append(ContrastTarget(subnet_a=base, subnet_b=other, value=contrast_value))
            else:
                if not isinstance(value, dict):
                    raise TypeError(f"Expected object for subnet target '{key}'")
                subnets[key] = SubnetTarget.from_dict(value)
        return cls(subnets=subnets, contrasts=contrasts)


def load_loss_weights(path: Optional[Path]) -> LossWeights:
    """Load loss weights from JSON or return defaults when ``path`` is ``None``."""

    if path is None:
        return LossWeights()
    data = json.loads(Path(path).read_text())
    if not isinstance(data, dict):
        raise TypeError("Loss weight file must contain a JSON object")
    return LossWeights.from_json(data)  # type: ignore[arg-type]
