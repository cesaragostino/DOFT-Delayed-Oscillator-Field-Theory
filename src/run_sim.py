# src/run_sim.py
# -*- coding: utf-8 -*-
"""
Main entry point for running DOFT Phase 1 simulations.
- Correctly generates the full parameter sweep.
- Ensures all LPC metrics are logged according to the data contract.
- Added robust handling of NaN/inf values during results aggregation.
"""

import os
import json
import csv
import pathlib
import argparse
import uuid
import itertools
import pandas as pd
from joblib import Parallel, delayed
from tqdm import tqdm
from .model import DOFTModel

def run_one_simulation(cfg, out_dir):
    run_id = f"run_{uuid.uuid4().hex[:8]}"
    model = DOFTModel(cfg)
    experiment_type = cfg.get("experiment_type", "chaos")

    run_result, blocks_data = {}, []
    if experiment_type == "pulse":
        run_result, blocks_data = model.run_pulse_experiment(xi_amp=float(cfg.get("xi_amp", 1e-4)))
    else:
        run_result, blocks_data = model.run_chaos_experiment(xi_amp=float(cfg.get("xi_amp", 1e-4)))

    run_row = {
        "run_id": run_id,
        "seed": cfg["seed"],
        "a_mean": cfg["a"]["mean"],
        "tau_mean": cfg["tau0"]["mean"],
        "gamma": cfg["gamma"],
        "ceff_pulse": run_result.get("ceff_pulse", None),
        "ceff_pulse_ic95": None,
        "anisotropy_max_pct": run_result.get("anisotropy_max_pct", None),
        "lpc_deltaK_neg_frac": run_result.get("lpc_deltaK_neg_frac", None),
        "lpc_vcount": run_result.get("lpc_vcount", None)
    }

    for block in blocks_data:
        block["run_id"] = run_id

    meta_info = {"run_id": run_id, "config": cfg}
    with open(out_dir / f"{run_id}_meta.json", "w") as f:
        json.dump(meta_info, f, indent=2, default=lambda o: '<not serializable>')

    return run_row, blocks_data

def main():
    parser = argparse.ArgumentParser(description="DOFT Phase 1 Simulation Runner")
    parser.add_argument("--config", required=True, help="Path to JSON experiment config.")
    parser.add_argument("--out", required=True, help="Output directory for results.")
    parser.add_argument("--n-jobs", type=int, default=1, help="Number of parallel jobs.")
    args = parser.parse_args()

    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(args.config, "r") as f:
        config = json.load(f)

    tasks = []
    for experiment in config["experiments"]:
        exp_base_cfg = {k: v for k, v in config.items() if k != "experiments"}
        exp_base_cfg.update({k: v for k, v in experiment.items() if not isinstance(v, list)})

        if experiment['experiment_type'] == 'pulse':
            param_combinations = list(itertools.product(
                experiment['a'],
                experiment['tau0'],
                experiment['seeds']
            ))
            for a_param, tau0_param, seed in param_combinations:
                run_cfg = exp_base_cfg.copy()
                run_cfg['a'] = a_param
                run_cfg['tau0'] = tau0_param
                run_cfg['seed'] = seed
                tasks.append(run_cfg)
        else: # Handle chaos experiment
            for seed in experiment.get('seeds', [0]):
                run_cfg = exp_base_cfg.copy()
                run_cfg['a'] = experiment['a'][0]
                run_cfg['tau0'] = experiment['tau0'][0]
                run_cfg['seed'] = seed
                tasks.append(run_cfg)

    print(f"# Starting {len(tasks)} simulation runs with {args.n_jobs} parallel jobs...")

    results = Parallel(n_jobs=args.n_jobs)(
        delayed(run_one_simulation)(task_cfg, out_dir) for task_cfg in tqdm(tasks)
    )

    # --- Aggregate and save results robustly using pandas ---
    all_runs = [r[0] for r in results if r is not None and r[0] is not None]
    all_blocks = [b for r in results if r is not None for b in r[1]]

    if all_runs:
        df_runs = pd.DataFrame(all_runs)
        # Coerce numeric columns to handle potential errors like NaN/inf
        for col in df_runs.columns:
            if df_runs[col].dtype == 'object':
                 df_runs[col] = pd.to_numeric(df_runs[col], errors='ignore')
        df_runs.to_csv(out_dir / "runs.csv", index=False, na_rep='NA')
        print(f"# Saved {len(df_runs)} entries to runs.csv")

    if all_blocks:
        df_blocks = pd.DataFrame(all_blocks)
        for col in df_blocks.columns:
            if df_blocks[col].dtype == 'object':
                 df_blocks[col] = pd.to_numeric(df_blocks[col], errors='ignore')
        df_blocks.to_csv(out_dir / "blocks.csv", index=False, na_rep='NA')
        print(f"# Saved {len(df_blocks)} entries to blocks.csv")

if __name__ == "__main__":
    main()
