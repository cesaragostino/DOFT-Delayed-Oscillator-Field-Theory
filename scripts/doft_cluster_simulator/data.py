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


@dataclass
class MaterialConfig:
    """Description of the material, subnets, anchors, and optional contrasts."""

    material: str
    subnets: List[str]
    anchors: Dict[str, Dict[str, float]]
    contrasts: List[ContrastTarget] = field(default_factory=list)

    @classmethod
    def from_file(cls, path: Path) -> "MaterialConfig":
        data = json.loads(Path(path).read_text())
        material = str(data["material"])

        raw_subnets: Optional[List[str]] = data.get("subnets")
        if raw_subnets is None:
            raw_subnets = [str(entry["name"]) for entry in data.get("sub_networks", [])]
        if not raw_subnets:
            raise ValueError("material_config.json debe incluir al menos una subred")
        subnets = [_normalize_subnet_name(str(name), material) for name in raw_subnets]

        anchors: Dict[str, Dict[str, float]] = {}
        raw_anchors = data.get("anchors")
        if isinstance(raw_anchors, dict):
            for subnet, anchor_data in raw_anchors.items():
                normalized = _normalize_subnet_name(str(subnet), material)
                if normalized not in subnets:
                    continue
                anchors[normalized] = {key: float(value) for key, value in anchor_data.items()}
        elif data.get("sub_networks"):
            for entry in data["sub_networks"]:
                name = _normalize_subnet_name(str(entry.get("name")), material)
                if name not in subnets or "X_anchor" not in entry:
                    continue
                anchors[name] = {"X": float(entry["X_anchor"]) }

        contrasts: List[ContrastTarget] = []
        for entry in data.get("contrasts", []):
            a_raw = entry.get("A") or entry.get("a")
            b_raw = entry.get("B") or entry.get("b")
            if a_raw is None or b_raw is None:
                raise ValueError("Cada contraste debe definir los campos 'A' y 'B'")
            a_name = _normalize_subnet_name(str(a_raw), material)
            b_name = _normalize_subnet_name(str(b_raw), material)
            if a_name not in subnets or b_name not in subnets:
                raise ValueError(f"Contraste inválido: {a_name} o {b_name} no definidos en subnets")
            value = entry.get("C_AB_exp")
            label = entry.get("type")
            contrasts.append(
                ContrastTarget(
                    subnet_a=f"{material}_{a_name}",
                    subnet_b=f"{material}_{b_name}",
                    value=float(value) if value is not None else None,
                    label=str(label) if label else None,
                )
            )

        return cls(material=material, subnets=subnets, anchors=anchors, contrasts=contrasts)


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
