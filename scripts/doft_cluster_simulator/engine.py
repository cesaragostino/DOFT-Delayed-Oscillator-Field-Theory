"""High level orchestration for the DOFT cluster simulator."""

from __future__ import annotations

from typing import Dict, List, Optional
import random

from .data import ContrastTarget, LossWeights, MaterialConfig, TargetDataset
from .model import ClusterSimulator
from .optimizer import SubnetOptimizer
from .reporting import ReportBundle, create_report_bundle
from .results import SubnetSimulation


class SimulationEngine:
    """Orchestrate optimisation across subnets and produce reports."""

    def __init__(
        self,
        config: MaterialConfig,
        dataset: TargetDataset,
        weights: LossWeights,
        max_evals: int = 250,
        seed: int = 42,
    ) -> None:
        self.config = config
        self.dataset = dataset
        self.weights = weights
        self.max_evals = max_evals
        self.rng = random.Random(seed)
        self.simulator = ClusterSimulator()

    def run(self) -> ReportBundle:
        subnet_results: Dict[str, SubnetSimulation] = {}
        for subnet_name in self.config.subnets:
            subnet_cfg = self.config.subnet_configs.get(subnet_name)
            if subnet_cfg is not None and not subnet_cfg.enabled:
                continue
            target = self.dataset.subnets.get(f"{self.config.material}_{subnet_name}")
            if target is None:
                raise KeyError(f"Missing target for subnet '{subnet_name}'")
            anchor = self._lookup_anchor(subnet_name)
            optimizer = SubnetOptimizer(
                simulator=self.simulator,
                weights=self.weights,
                max_evals=self.max_evals,
                rng=self.rng,
                anchor=anchor,
                subnet_config=subnet_cfg,
                random_starts=self.config.optimization.n_random_starts,
            )
            result = optimizer.optimise(target)
            subnet_results[subnet_name] = SubnetSimulation(
                parameters=result.params,
                loss=result.simulation_loss,
                simulation_result=result.simulation_result,
            )

        bundle = create_report_bundle(
            config=self.config,
            weights=self.weights,
            subnet_results=subnet_results,
            contrast_targets=self._collect_contrasts(),
        )
        return bundle

    def _lookup_anchor(self, subnet_name: str) -> Optional[float]:
        subnet_cfg = self.config.subnet_configs.get(subnet_name)
        if subnet_cfg and subnet_cfg.f0_anchor is not None:
            return subnet_cfg.f0_anchor
        anchor_data = self.config.anchors.get(subnet_name)
        if anchor_data is None:
            return None
        return anchor_data.get("X")

    def _collect_contrasts(self) -> List[ContrastTarget]:
        merged: Dict[tuple[str, str], ContrastTarget] = {}
        for contrast in self.config.contrasts:
            merged[(contrast.subnet_a, contrast.subnet_b)] = contrast
        for contrast in self.dataset.contrasts:
            key = (contrast.subnet_a, contrast.subnet_b)
            if contrast.label is None and key in merged and merged[key].label is not None:
                contrast.label = merged[key].label
            merged[key] = contrast
        return list(merged.values())
