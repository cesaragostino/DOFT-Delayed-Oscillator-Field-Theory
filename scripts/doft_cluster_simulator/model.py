"""Simulation primitives for the DOFT cluster simulator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence
import math

from .data import DELTA_KEYS, PRIMES, PRIME_KEYS, SubnetParameters


@dataclass
class SimulationResult:
    """Container for a simulated fingerprint."""

    e_sim: List[float]
    q_sim: float | None
    residual_sim: float
    layer_factors: List[float]
    log_r: float


def soft_round(value: float, softness: float = 0.35) -> float:
    """Return a smooth approximation of the nearest integer."""

    nearest = round(value)
    diff = value - nearest
    return nearest + diff * math.tanh(abs(diff) / max(softness, 1e-6))


def _layer_factor(layer_index: int) -> float:
    """Compute a deterministic factor for the given layer index."""

    return 1.0 + 0.18 * (layer_index - 1)


class ClusterSimulator:
    """Compute fingerprints for a set of simulation parameters."""

    def __init__(self, softness: float = 0.35) -> None:
        self.softness = softness

    def simulate(self, params: SubnetParameters) -> SimulationResult:
        e_sim: List[float] = []
        layer_factors: List[float] = []
        raw_levels: List[float] = []
        for idx, prime in enumerate(PRIMES):
            key = PRIME_KEYS[idx]
            delta_key = DELTA_KEYS[idx]
            ratio = params.ratios.get(key, 0.0)
            delta = params.delta.get(delta_key, 0.0)
            layer_index = params.layer_assignment[idx] if idx < len(params.layer_assignment) else 1
            layer_index = max(1, min(params.L, layer_index))
            layer_factor = _layer_factor(layer_index)
            base_value = params.f0 * (1.0 + ratio) * layer_factor + delta
            raw_levels.append(base_value)
            e_value = soft_round(base_value, self.softness)
            e_sim.append(e_value)
            layer_factors.append(layer_factor)

        q_sim = self._compute_q(e_sim)
        log_r = self._compute_log_r(raw_levels, params.f0)
        return SimulationResult(
            e_sim=e_sim,
            q_sim=q_sim,
            residual_sim=0.0,
            layer_factors=layer_factors,
            log_r=log_r,
        )

    def _compute_q(self, e_sim: Sequence[float]) -> float | None:
        weights = [max(e, 0.0) for e in e_sim]
        total = sum(weights)
        if total <= 0:
            return None
        numerator = sum(weight * prime for weight, prime in zip(weights, PRIMES))
        return numerator / total

    def _compute_log_r(self, raw_levels: Iterable[float], f0: float) -> float:
        values = [value for value in raw_levels if math.isfinite(value)]
        if not values:
            values = [f0]
        avg_value = sum(values) / len(values)
        return math.log(max(avg_value, 1e-12))
