"""Reporting utilities for the DOFT cluster simulator."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple
import csv
import json
from datetime import datetime
import math

from .data import LossWeights, MaterialConfig, SubnetTarget, TargetDataset
from .loss import LossBreakdown
from .results import SimulationRun, SubnetSimulation


@dataclass
class SubnetReport:
    name: str
    parameters: SubnetSimulation
    loss: LossBreakdown
    e_sim: List[float]
    q_sim: Optional[float]
    residual_sim: float
    e_abs_errors: List[Optional[float]]
    e_abs_mean: Optional[float]
    q_error: Optional[float]
    residual_error: Optional[float]
    f0_anchor_error: Optional[float]

    def to_dict(self) -> Dict[str, object]:
        return {
            "L": self.parameters.parameters.L,
            "f0": self.parameters.parameters.f0,
            "ratios": self.parameters.parameters.ratios,
            "delta": self.parameters.parameters.delta,
            "layer_assignment": self.parameters.parameters.layer_assignment,
            "loss": self.loss.as_dict(),
            "e_sim": self.e_sim,
            "q_sim": self.q_sim,
            "residual_sim": self.residual_sim,
            "e_abs_errors": self.e_abs_errors,
            "e_abs_mean": self.e_abs_mean,
            "q_error": self.q_error,
            "residual_error": self.residual_error,
            "f0_anchor_error": self.f0_anchor_error,
        }


@dataclass
class ContrastReport:
    pair: str
    target: float
    simulated: float
    loss: float

    @property
    def error(self) -> float:
        return abs(self.simulated - self.target)


@dataclass
class RunReport:
    label: str
    seed: int
    primes: Tuple[int, ...]
    freeze_primes: Tuple[int, ...]
    subnets: Dict[str, SubnetReport]
    contrasts: List[ContrastReport]
    total_loss: float


@dataclass
class AggregateStats:
    f0: Dict[str, Tuple[float, float]]
    e_mean: Dict[str, Tuple[float, float]]
    q: Dict[str, Tuple[float, float]]
    residual: Dict[str, Tuple[float, float]]
    contrast: Dict[str, Tuple[float, float]]


@dataclass
class AblationStats:
    prime_signature: str
    mean_total_loss: float
    mean_contrast_error: float


@dataclass
class ReportBundle:
    material: str
    weights: LossWeights
    runs: List[RunReport]
    aggregates: AggregateStats
    ablations: List[AblationStats]
    best_run_label: str
    timestamp: str

    def write(
        self,
        out_dir: Path,
        config_path: Optional[Path],
        targets_path: Optional[Path],
        max_evals: int,
        seed: int,
    ) -> None:
        out_dir.mkdir(parents=True, exist_ok=True)
        best_run = self._find_best_run()
        self._write_best_params(out_dir, best_run)
        self._write_csv(out_dir)
        self._write_report_md(out_dir, best_run)
        self._write_manifest(out_dir, config_path, targets_path, max_evals, seed)

    def _find_best_run(self) -> RunReport:
        return min(self.runs, key=lambda run: run.total_loss)

    def _write_best_params(self, out_dir: Path, run: RunReport) -> None:
        best_params = {
            "material": self.material,
            "run_label": run.label,
            "params": {
                subnet: report.to_dict()
                for subnet, report in run.subnets.items()
            },
        }
        (out_dir / "best_params.json").write_text(json.dumps(best_params, indent=2))

    def _write_csv(self, out_dir: Path) -> None:
        csv_path = out_dir / "simulation_results.csv"
        fieldnames = [
            "run_label",
            "seed",
            "primes",
            "freeze_primes",
            "subnet",
            "L",
            "f0",
            "e2",
            "e3",
            "e5",
            "e7",
            "e_mean_abs_error",
            "q_sim",
            "q_error",
            "residual_sim",
            "residual_error",
            "f0_anchor_error",
            "loss_total",
            "loss_e",
            "loss_q",
            "loss_residual",
            "loss_anchor",
            "loss_regularization",
        ]
        with csv_path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for run in self.runs:
                for subnet, report in run.subnets.items():
                    row = {
                        "run_label": run.label,
                        "seed": run.seed,
                        "primes": ",".join(str(p) for p in run.primes),
                        "freeze_primes": ",".join(str(p) for p in run.freeze_primes),
                        "subnet": subnet,
                        "L": report.parameters.parameters.L,
                        "f0": report.parameters.parameters.f0,
                        "e2": report.e_sim[0],
                        "e3": report.e_sim[1],
                        "e5": report.e_sim[2],
                        "e7": report.e_sim[3],
                        "e_mean_abs_error": report.e_abs_mean,
                        "q_sim": report.q_sim,
                        "q_error": report.q_error,
                        "residual_sim": report.residual_sim,
                        "residual_error": report.residual_error,
                        "f0_anchor_error": report.f0_anchor_error,
                        "loss_total": report.loss.total,
                        "loss_e": report.loss.e_loss,
                        "loss_q": report.loss.q_loss,
                        "loss_residual": report.loss.residual_loss,
                        "loss_anchor": report.loss.anchor_loss,
                        "loss_regularization": report.loss.regularization_loss,
                    }
                    writer.writerow(row)

    def _write_report_md(self, out_dir: Path, best_run: RunReport) -> None:
        lines: List[str] = []
        lines.append(f"# DOFT Cluster Simulator Results — {self.material}")
        lines.append("")
        lines.append(f"Fecha de ejecución: {self.timestamp}")
        lines.append("")
        lines.append(f"**Mejor corrida:** `{best_run.label}` con pérdida total {best_run.total_loss:.6f}")
        lines.append("")
        lines.append("## Runs")
        lines.append("")
        lines.append("| Run | Seed | Primes | Freeze | Total Loss |")
        lines.append("| --- | --- | --- | --- | --- |")
        for run in self.runs:
            lines.append(
                f"| `{run.label}` | {run.seed} | {','.join(str(p) for p in run.primes)} | "
                f"{','.join(str(p) for p in run.freeze_primes) or '—'} | {run.total_loss:.6f} |"
            )
        lines.append("")

        lines.append("## Métricas agregadas (media ± desviación)")
        lines.append("")
        lines.append("| Subred | f0 | |e| | q | residual |")
        lines.append("| --- | --- | --- | --- | --- |")
        for subnet in sorted(self.aggregates.f0.keys()):
            f0_mean, f0_std = self.aggregates.f0[subnet]
            e_mean, e_std = self.aggregates.e_mean.get(subnet, (0.0, 0.0))
            q_mean, q_std = self.aggregates.q.get(subnet, (0.0, 0.0))
            r_mean, r_std = self.aggregates.residual.get(subnet, (0.0, 0.0))
            lines.append(
                f"| {subnet} | {f0_mean:.4f} ± {f0_std:.4f} | {e_mean:.4f} ± {e_std:.4f} | "
                f"{q_mean:.4f} ± {q_std:.4f} | {r_mean:.5f} ± {r_std:.5f} |"
            )
        lines.append("")

        lines.append("## Contrastes")
        lines.append("")
        lines.append("| Par | error medio ± std |")
        lines.append("| --- | --- |")
        for pair, (mean_val, std_val) in self.aggregates.contrast.items():
            lines.append(f"| {pair} | {mean_val:.5f} ± {std_val:.5f} |")
        lines.append("")

        if self.ablations:
            lines.append("## Ablaciones por primos")
            lines.append("")
            lines.append("| Primos | pérdida media | error contraste medio |")
            lines.append("| --- | --- | --- |")
            for entry in self.ablations:
                lines.append(
                    f"| {entry.prime_signature} | {entry.mean_total_loss:.6f} | {entry.mean_contrast_error:.5f} |"
                )
            lines.append("")

        (out_dir / "report.md").write_text("\n".join(lines))

    def _write_manifest(
        self,
        out_dir: Path,
        config_path: Optional[Path],
        targets_path: Optional[Path],
        max_evals: int,
        seed: int,
    ) -> None:
        manifest = {
            "version": "0.2",
            "generated_at": self.timestamp,
            "material": self.material,
            "config_path": str(config_path) if config_path else None,
            "targets_path": str(targets_path) if targets_path else None,
            "max_evals": max_evals,
            "seed": seed,
            "run_count": len(self.runs),
            "best_run": self.best_run_label,
            "weights": {
                "w_e": self.weights.w_e,
                "w_q": self.weights.w_q,
                "w_r": self.weights.w_r,
                "w_c": self.weights.w_c,
                "w_anchor": self.weights.w_anchor,
                "lambda_reg": self.weights.lambda_reg,
            },
        }
        (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))


def create_report_bundle(
    config: MaterialConfig,
    weights: LossWeights,
    runs: List[SimulationRun],
    contrast_targets: List[ContrastTarget],
    dataset: TargetDataset,
) -> ReportBundle:
    run_reports: List[RunReport] = []
    contrast_map = {(c.subnet_a, c.subnet_b): c for c in contrast_targets}

    for run in runs:
        sub_reports: Dict[str, SubnetReport] = {}
        for subnet, result in run.subnet_results.items():
            target_key = f"{config.material}_{subnet}"
            target = dataset.subnets.get(target_key)
            anchor_value = None
            anchor_info = config.anchors.get(subnet)
            if anchor_info is not None:
                anchor_value = anchor_info.get("f0") or anchor_info.get("X")
            sub_reports[subnet] = _build_subnet_report(subnet, result, target, anchor_value)

        contrasts: List[ContrastReport] = []
        total_loss = run.base_loss
        for contrast in contrast_targets:
            report_a = sub_reports.get(_strip_material_prefix(contrast.subnet_a, config.material))
            report_b = sub_reports.get(_strip_material_prefix(contrast.subnet_b, config.material))
            if report_a is None or report_b is None or contrast.value is None:
                continue
            simulated = compute_contrast_value(report_a, report_b)
            loss = weights.w_c * (simulated - contrast.value) ** 2
            contrasts.append(
                ContrastReport(
                    pair=contrast.label or f"{report_a.name}_vs_{report_b.name}",
                    target=contrast.value,
                    simulated=simulated,
                    loss=loss,
                )
            )
            total_loss += loss

        run_reports.append(
            RunReport(
                label=run.label,
                seed=run.seed,
                primes=run.primes,
                freeze_primes=run.freeze_primes,
                subnets=sub_reports,
                contrasts=contrasts,
                total_loss=total_loss,
            )
        )

    aggregates = _compute_aggregate_stats(run_reports)
    ablations = _compute_ablation_stats(run_reports)
    best_run_label = min(run_reports, key=lambda r: r.total_loss).label
    timestamp = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    return ReportBundle(
        material=config.material,
        weights=weights,
        runs=run_reports,
        aggregates=aggregates,
        ablations=ablations,
        best_run_label=best_run_label,
        timestamp=timestamp,
    )


# ---------------------------------------------------------------------------
# Helpers


def _build_subnet_report(
    name: str,
    simulation: SubnetSimulation,
    target: Optional[SubnetTarget],
    anchor_value: Optional[float],
) -> SubnetReport:
    e_abs_errors: List[Optional[float]] = []
    e_abs_mean: Optional[float] = None
    q_error: Optional[float] = None
    residual_error: Optional[float] = None
    f0_anchor_error: Optional[float] = None

    if target and target.e_exp is not None:
        diffs: List[float] = []
        for idx, exp_value in enumerate(target.e_exp):
            if exp_value is None:
                e_abs_errors.append(None)
                continue
            diff = abs(simulation.simulation_result.e_sim[idx] - exp_value)
            e_abs_errors.append(diff)
            diffs.append(diff)
        if diffs:
            e_abs_mean = sum(diffs) / len(diffs)
    else:
        e_abs_errors = [None, None, None, None]

    if target and target.q_exp is not None and simulation.simulation_result.q_sim is not None:
        q_error = abs(simulation.simulation_result.q_sim - target.q_exp)

    if target and target.residual_exp is not None:
        residual_error = abs(simulation.simulation_result.residual_sim - target.residual_exp)

    if anchor_value is not None:
        f0_anchor_error = abs(simulation.parameters.f0 - anchor_value)

    return SubnetReport(
        name=name,
        parameters=simulation,
        loss=simulation.loss,
        e_sim=simulation.simulation_result.e_sim,
        q_sim=simulation.simulation_result.q_sim,
        residual_sim=simulation.simulation_result.residual_sim,
        e_abs_errors=e_abs_errors,
        e_abs_mean=e_abs_mean,
        q_error=q_error,
        residual_error=residual_error,
        f0_anchor_error=f0_anchor_error,
    )


def compute_contrast_value(a: SubnetReport, b: SubnetReport) -> float:
    scale_a = a.parameters.parameters.f0 + sum(a.e_sim) / max(len(a.e_sim), 1)
    scale_b = b.parameters.parameters.f0 + sum(b.e_sim) / max(len(b.e_sim), 1)
    return scale_a / max(scale_b, 1e-6)


def _strip_material_prefix(name: str, material: str) -> str:
    prefix = f"{material}_"
    return name[len(prefix) :] if name.startswith(prefix) else name


def _compute_aggregate_stats(runs: List[RunReport]) -> AggregateStats:
    f0: Dict[str, List[float]] = {}
    e_mean: Dict[str, List[float]] = {}
    q_errors: Dict[str, List[float]] = {}
    residual_errors: Dict[str, List[float]] = {}
    contrast_errors: Dict[str, List[float]] = {}

    for run in runs:
        for subnet, report in run.subnets.items():
            f0.setdefault(subnet, []).append(report.parameters.parameters.f0)
            if report.e_abs_mean is not None:
                e_mean.setdefault(subnet, []).append(report.e_abs_mean)
            if report.q_error is not None:
                q_errors.setdefault(subnet, []).append(report.q_error)
            if report.residual_error is not None:
                residual_errors.setdefault(subnet, []).append(report.residual_error)
        for contrast in run.contrasts:
            contrast_errors.setdefault(contrast.pair, []).append(contrast.error)

    return AggregateStats(
        f0={key: _mean_std(values) for key, values in f0.items()},
        e_mean={key: _mean_std(values) for key, values in e_mean.items()},
        q={key: _mean_std(values) for key, values in q_errors.items()},
        residual={key: _mean_std(values) for key, values in residual_errors.items()},
        contrast={key: _mean_std(values) for key, values in contrast_errors.items()},
    )


def _compute_ablation_stats(runs: List[RunReport]) -> List[AblationStats]:
    groups: Dict[Tuple[int, ...], List[RunReport]] = {}
    for run in runs:
        groups.setdefault(run.primes, []).append(run)
    stats: List[AblationStats] = []
    for primes, entries in groups.items():
        mean_loss = sum(run.total_loss for run in entries) / len(entries)
        contrast_values: List[float] = []
        for run in entries:
            contrast_values.extend(contrast.error for contrast in run.contrasts)
        mean_contrast = sum(contrast_values) / len(contrast_values) if contrast_values else 0.0
        stats.append(
            AblationStats(
                prime_signature=",".join(str(p) for p in primes),
                mean_total_loss=mean_loss,
                mean_contrast_error=mean_contrast,
            )
        )
    return stats


def _mean_std(values: Iterable[float]) -> Tuple[float, float]:
    data = list(values)
    if not data:
        return (0.0, 0.0)
    mean = sum(data) / len(data)
    if len(data) == 1:
        return (mean, 0.0)
    variance = sum((value - mean) ** 2 for value in data) / (len(data) - 1)
    return (mean, math.sqrt(max(variance, 0.0)))
