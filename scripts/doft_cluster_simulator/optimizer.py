"""Random + local search optimizer for DOFT cluster simulation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple
import random

from .data import DELTA_KEYS, PRIME_KEYS, LossWeights, SubnetConfig, SubnetParameters, SubnetTarget
from .loss import LossBreakdown, compute_subnet_loss
from .model import ClusterSimulator


@dataclass
class OptimizationResult:
    """Optimization outcome for a subnet."""

    params: SubnetParameters
    simulation_loss: LossBreakdown
    simulation_result: "SimulationResult"


class SubnetOptimizer:
    """Search for parameters that minimise the loss for a subnet."""

    def __init__(
        self,
        simulator: ClusterSimulator,
        weights: LossWeights,
        max_evals: int,
        rng: random.Random,
        anchor: Optional[float],
        subnet_config: Optional[SubnetConfig],
        random_starts: Optional[int] = None,
    ) -> None:
        self.simulator = simulator
        self.weights = weights
        self.max_evals = max_evals
        self.rng = rng
        self.anchor = anchor
        self.subnet_config = subnet_config
        self.random_starts = random_starts
        self.allowed_L = self._derive_allowed_layers()

    def optimise(self, target: SubnetTarget) -> OptimizationResult:
        best_params: Optional[SubnetParameters] = None
        best_loss: Optional[LossBreakdown] = None
        best_result = None

        evaluations = 0

        for candidate in self._initial_candidates():
            loss, simulation_result = self._evaluate(target, candidate)
            evaluations += 1
            if best_loss is None or loss.total < best_loss.total:
                best_params = candidate
                best_loss = loss
                best_result = simulation_result
            if evaluations >= self.max_evals:
                break

        random_budget = self.random_starts if self.random_starts is not None else self.max_evals
        random_budget = max(0, min(self.max_evals - evaluations, random_budget))
        for _ in range(random_budget):
            candidate = self._sample_parameters()
            loss, simulation_result = self._evaluate(target, candidate)
            evaluations += 1
            if best_loss is None or loss.total < best_loss.total:
                best_params = candidate
                best_loss = loss
                best_result = simulation_result

        if best_params is None or best_loss is None or best_result is None:
            raise RuntimeError("No candidate evaluated during optimisation")

        local_budget = min(64, max(0, self.max_evals - evaluations))
        for _ in range(local_budget):
            candidate = self._perturb(best_params)
            loss, simulation_result = self._evaluate(target, candidate)
            if loss.total < best_loss.total:
                best_params = candidate
                best_loss = loss
                best_result = simulation_result

        return OptimizationResult(params=best_params, simulation_loss=best_loss, simulation_result=best_result)

    def _evaluate(self, target: SubnetTarget, params: SubnetParameters) -> Tuple[LossBreakdown, "SimulationResult"]:
        simulation_result = self.simulator.simulate(params)
        loss = compute_subnet_loss(target, params, simulation_result, self.weights, self.anchor)
        return loss, simulation_result

    def _initial_candidates(self) -> List[SubnetParameters]:
        hints: List[SubnetParameters] = []
        if self.subnet_config is None:
            return hints
        ratios = {key: 0.0 for key in PRIME_KEYS}
        ratios.update(self.subnet_config.init_ratios)
        L = self._clamp_L(self.subnet_config.init_L or self.allowed_L[0])
        f0 = self.subnet_config.f0_anchor or self.anchor or 1.5
        f0 = self._clamp_f0(f0)
        delta = {key: 0.0 for key in DELTA_KEYS}
        layer_assignment = [1 for _ in PRIME_KEYS]
        hints.append(SubnetParameters(L=L, f0=f0, ratios=ratios, delta=delta, layer_assignment=layer_assignment))
        return hints

    def _sample_parameters(self) -> SubnetParameters:
        L = self._sample_L()
        f0 = self._sample_f0()
        ratios = {key: self._sample_ratio() for key in PRIME_KEYS}
        delta = {key: self.rng.uniform(-0.2, 0.2) for key in DELTA_KEYS}
        layer_assignment = [self.rng.randint(1, L) for _ in PRIME_KEYS]
        return SubnetParameters(L=L, f0=f0, ratios=ratios, delta=delta, layer_assignment=layer_assignment)

    def _perturb(self, params: SubnetParameters) -> SubnetParameters:
        candidate = params.copy()
        candidate.L = self._perturb_L(candidate.L)
        candidate.f0 = self._clamp_f0(candidate.f0 + self.rng.gauss(0.0, 0.05))
        for key in PRIME_KEYS:
            candidate.ratios[key] = self._clamp_ratio(candidate.ratios[key] + self.rng.gauss(0.0, 0.02))
        for key in DELTA_KEYS:
            candidate.delta[key] = candidate.delta[key] + self.rng.gauss(0.0, 0.02)
        candidate.layer_assignment = [
            max(1, min(candidate.L, layer + self.rng.choice([-1, 0, 1]))) for layer in candidate.layer_assignment
        ]
        return candidate

    def _derive_allowed_layers(self) -> List[int]:
        if self.subnet_config and self.subnet_config.l_candidates:
            allowed = sorted({max(1, min(3, int(value))) for value in self.subnet_config.l_candidates})
            return allowed or [1, 2, 3]
        return [1, 2, 3]

    def _clamp_L(self, value: int) -> int:
        if value in self.allowed_L:
            return value
        return self.allowed_L[0]

    def _sample_L(self) -> int:
        return self.rng.choice(self.allowed_L)

    def _perturb_L(self, current: int) -> int:
        if current not in self.allowed_L:
            return self.allowed_L[0]
        idx = self.allowed_L.index(current)
        if len(self.allowed_L) == 1:
            return current
        shift = self.rng.choice([-1, 0, 1])
        new_idx = max(0, min(len(self.allowed_L) - 1, idx + shift))
        return self.allowed_L[new_idx]

    def _sample_f0(self) -> float:
        if self.subnet_config and self.subnet_config.f0_range is not None:
            lo, hi = self.subnet_config.f0_range
            return self.rng.uniform(lo, hi)
        anchor = self.subnet_config.f0_anchor if self.subnet_config and self.subnet_config.f0_anchor is not None else self.anchor
        base = anchor if anchor is not None else 1.5
        return self._clamp_f0(max(0.25, self.rng.gauss(base, 0.4)))

    def _clamp_f0(self, value: float) -> float:
        if self.subnet_config and self.subnet_config.f0_range is not None:
            lo, hi = self.subnet_config.f0_range
            return min(max(value, lo), hi)
        return max(0.25, value)

    def _sample_ratio(self) -> float:
        limit = self.subnet_config.ratio_abs_max if self.subnet_config else None
        if limit is not None:
            return self.rng.uniform(-limit, limit)
        return max(0.0, self.rng.uniform(0.0, 1.5))

    def _clamp_ratio(self, value: float) -> float:
        limit = self.subnet_config.ratio_abs_max if self.subnet_config else None
        if limit is not None:
            return max(-limit, min(limit, value))
        return max(0.0, value)
