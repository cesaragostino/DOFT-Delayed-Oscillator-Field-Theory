from __future__ import annotations

import json
from pathlib import Path

from scripts.doft_cluster_simulator.data import LossWeights, MaterialConfig, ParameterBounds, SubnetParameters, SubnetTarget, TargetDataset
from scripts.doft_cluster_simulator.engine import SimulationEngine
from scripts.doft_cluster_simulator.loss import compute_subnet_loss
from scripts.doft_cluster_simulator.model import SimulationResult


def test_target_dataset_handles_missing_values(tmp_path: Path) -> None:
    targets = {
        "MgB2_sigma": {"e_exp": [1.0, 0.0, 0.0, 0.0], "q_exp": None, "residual_exp": -0.01},
        "MgB2_pi": {"e_exp": [1.2, 0.7, 0.2, 0.4], "q_exp": 6.0, "residual_exp": -0.02},
        "MgB2_sigma_vs_pi": {"C_AB_exp": 1.5},
    }
    path = tmp_path / "targets.json"
    path.write_text(json.dumps(targets))

    dataset = TargetDataset.from_file(path)
    assert dataset.subnets["MgB2_sigma"].q_exp is None
    assert dataset.subnets["MgB2_sigma"].use_q is False
    assert dataset.contrasts[0].subnet_b == "MgB2_pi"


def test_loss_gates_missing_terms() -> None:
    params = SubnetParameters(L=2, f0=1.5, ratios={"r2": 1.0, "r3": 0.5, "r5": 0.2, "r7": 0.1}, delta={"d2": 0.0, "d3": 0.0, "d5": 0.0, "d7": 0.0}, layer_assignment=[1, 1, 2, 2])
    simulation = SimulationResult(e_sim=[1.0, 0.8, 0.2, 0.4], q_sim=None, residual_sim=-0.015, layer_factors=[1.0, 1.0, 1.18, 1.18])
    target = SubnetTarget(e_exp=[1.0, 0.7, None, None], q_exp=None, residual_exp=None, use_q=False)
    weights = LossWeights(w_e=1.0, w_q=2.0, w_r=3.0, lambda_reg=0.0005)

    breakdown = compute_subnet_loss(
        target,
        params,
        simulation,
        weights,
        anchor_value=None,
        subnet_name="MgB2_sigma",
        huber_delta=0.02,
        lambda_reg=weights.lambda_reg,
        active_ratio_keys=["r2", "r3"],
        active_delta_keys=["d2", "d3"],
    )
    assert breakdown.q_loss == 0.0
    assert breakdown.residual_loss == 0.0
    assert breakdown.e_loss > 0.0
    assert breakdown.regularization_loss > 0.0


def test_engine_runs_end_to_end(tmp_path: Path) -> None:
    config_data = {
        "material": "MgB2",
        "subnetworks": ["sigma", "pi"],
        "anchors": {"sigma": {"f0": 1.5}, "pi": {"f0": 1.6}},
        "primes": [2, 3],
        "constraints": {"ratios_bounds": [-0.2, 0.2], "deltas_bounds": [-0.3, 0.3], "f0_bounds": [1.0, 2.0]},
        "freeze_primes": [],
        "layers": {"sigma": 1, "pi": 1},
        "contrasts": [{"type": "sigma-vs-pi", "A": "sigma", "B": "pi", "C_AB_exp": 1.5}],
    }
    targets = {
        "MgB2_sigma": {"e_exp": [1.0, 0.0, 0.0, 0.0], "q_exp": None, "residual_exp": -0.01},
        "MgB2_pi": {"e_exp": [1.2, 0.7, 0.2, 0.4], "q_exp": 6.0, "residual_exp": -0.02},
        "MgB2_sigma_vs_pi": {"C_AB_exp": 1.5},
    }

    config_path = tmp_path / "config.json"
    targets_path = tmp_path / "targets.json"
    config_path.write_text(json.dumps(config_data))
    targets_path.write_text(json.dumps(targets))

    config = MaterialConfig.from_file(config_path)
    dataset = TargetDataset.from_file(targets_path)
    weights = LossWeights()

    engine = SimulationEngine(
        config=config,
        dataset=dataset,
        weights=weights,
        max_evals=5,
        seed=123,
        seed_sweep=1,
        huber_delta=0.02,
        bounds_override={
            "ratios_bounds": (-0.2, 0.2),
            "deltas_bounds": (-0.3, 0.3),
            "f0_bounds": (1.0, 2.0),
        },
    )
    bundle = engine.run()
    out_dir = tmp_path / "out"
    bundle.write(out_dir, config_path, targets_path, max_evals=5, seed=123)

    assert (out_dir / "best_params.json").exists()
    assert (out_dir / "simulation_results.csv").exists()
    assert (out_dir / "report.md").exists()
    assert (out_dir / "manifest.json").exists()
    assert bundle.runs[0].contrasts, "Se esperaba al menos un contraste reportado"


def test_material_config_parses_extended_structure(tmp_path: Path) -> None:
    config = {
        "material": "MgB2",
        "sub_networks": {
            "sigma": {
                "enabled": True,
                "L_candidates": [1, 2],
                "f0_anchor": 20.8,
                "f0_range": [19.5, 21.0],
                "init": {"L": 1, "ratios": {"2": 0.01, "7": 0.02}},
                "bounds": {"ratio_abs_max": 0.15},
            },
            "pi": {
                "enabled": True,
                "L_candidates": [2],
                "f0_anchor": 19.2,
            },
        },
        "primes": [2, 3, 5, 7],
        "freeze_primes": [7],
        "constraints": {"ratios_bounds": [-0.3, 0.3], "deltas_bounds": [-0.4, 0.4], "f0_bounds": [19.0, 22.0]},
        "layers": {"sigma": 2, "pi": 1},
        "contrasts": {
            "sigma_vs_pi": {"enabled": True, "target": 1.58974, "type": "gap_ratio"}
        },
    }
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config))

    parsed = MaterialConfig.from_file(path)
    assert parsed.subnets == ["sigma", "pi"]
    assert parsed.anchors["sigma"]["f0"] == 20.8
    assert parsed.subnet_configs["sigma"].layer == 2
    assert parsed.subnet_configs["sigma"].f0_range == (19.5, 21.0)
    assert parsed.subnet_configs["sigma"].init_ratios["r2"] == 0.01
    assert parsed.subnet_configs["sigma"].ratio_abs_max == 0.15
    assert parsed.freeze_primes == (7,)
    assert parsed.primes == (2, 3, 5, 7)
    assert parsed.layers["sigma"] == 2
    assert parsed.contrasts[0].subnet_a == "MgB2_sigma"
    assert parsed.contrasts[0].label == "gap_ratio"
    assert parsed.contrasts[0].value == 1.58974
