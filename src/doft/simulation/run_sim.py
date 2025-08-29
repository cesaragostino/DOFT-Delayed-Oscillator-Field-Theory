# src/doft/simulation/run_sim.py
import argparse
import logging
import pandas as pd
import numpy as np
import time
import json
import os
from pathlib import Path
import subprocess

from doft.models.model import DOFTModel

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def main():
    """
    Main orchestrator for the DOFT Phase 1 counter-trial.
    This version incorporates numerical stability fixes based on audit feedback.
    """
    parser = argparse.ArgumentParser(description="Run DOFT Phase-1 Simulation Sweep.")
    parser.add_argument(
        "--boundary",
        choices=["periodic", "reflective", "absorbing"],
        default="periodic",
        help="Boundary condition for lattice interactions",
    )
    args = parser.parse_args()

    # --- Sweep Configuration ---
    group1 = [(1.0, 1.0), (1.2, 1.2), (1.5, 1.5)]
    group2 = [(1.0, 1.0), (1.2, 1.0), (1.5, 1.0)]
    group3 = [(1.0, 1.0), (1.0, 0.8), (1.0, 0.67)]
    simulation_points = group1 + group2 + group3

    point_to_group = {}
    for pt in group1: point_to_group[pt] = 'g1'
    for pt in group2: point_to_group[pt] = 'g2'
    for pt in group3: point_to_group[pt] = 'g3'

    seeds = [42, 123, 456, 789, 1011]
    gamma = 0.05
    grid_size = 100

    # STABILITY FIX: Define reference parameters for nondimensionalization.
    # We use the central point of the sweep as the reference scale.
    a_ref = 1.0
    tau_ref = 1.0

    # --- Create Unique Output Directory ---
    base_run_dir = 'runs'
    os.makedirs(base_run_dir, exist_ok=True)

    timestamp = time.strftime('%Y%m%d_%H%M%S')
    output_dir = os.path.join(base_run_dir, f'phase1_run_{timestamp}')
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Saving results to: {output_dir}")

    # --- Simulation Execution ---
    all_runs_data = []
    all_blocks_data = []

    print(f"🚀 Starting DOFT Phase-1 Simulation Sweep across {len(simulation_points)} points...")

    run_counter = 0
    total_sims = len(simulation_points) * len(seeds)

    for (a_val, tau_val) in simulation_points:
        for seed in seeds:
            run_counter += 1
            run_id = f"run_{int(time.time())}_{run_counter}"
            print(f"[{run_counter}/{total_sims}] Running sim: a={a_val}, τ={tau_val}, seed={seed}")

            # STABILITY FIX: Pass reference scales to the model for stabilization.
            model = DOFTModel(
                grid_size=grid_size,
                a=a_val,
                tau=tau_val,
                a_ref=a_ref,
                tau_ref=tau_ref,
                gamma=gamma,
                seed=seed,
                boundary_mode=args.boundary,
            )

            run_metrics, blocks_df = model.run()
            logger.info(
                "run_id=%s C-1: ceff_pulse=%s ceff_pulse_ic95_lo=%s ceff_pulse_ic95_hi=%s "
                "C-2: var_c_over_c2=%s anisotropy_max_pct=%s "
                "C-3: lpc_ok_frac=%s lpc_vcount=%s",
                run_id,
                run_metrics.get('ceff_pulse'),
                run_metrics.get('ceff_pulse_ic95_lo'),
                run_metrics.get('ceff_pulse_ic95_hi'),
                run_metrics.get('var_c_over_c2'),
                run_metrics.get('anisotropy_max_pct'),
                run_metrics.get('lpc_ok_frac'),
                run_metrics.get('lpc_vcount'),
            )

            run_metrics['run_id'] = run_id
            run_metrics['seed'] = seed
            run_metrics['a_mean'] = a_val
            run_metrics['tau_mean'] = tau_val
            run_metrics['gamma'] = gamma
            run_metrics['param_group'] = point_to_group.get((a_val, tau_val), 'unknown')
            run_metrics['lorentz_window'] = 'NA'
            all_runs_data.append(run_metrics)

            if blocks_df is not None and not blocks_df.empty:
                blocks_df['run_id'] = run_id
                if 'block_skipped' in blocks_df.columns:
                    blocks_df['block_skipped'] = blocks_df['block_skipped'].astype(int)
                all_blocks_data.append(blocks_df)

    print(f"\n✅ Simulation sweep finished. Consolidating and writing results to {output_dir}...")

    runs_df = pd.DataFrame(all_runs_data)
    runs_output_path = os.path.join(output_dir, 'runs.csv')
    runs_df.to_csv(runs_output_path, index=False)
    print(f"--> Wrote {len(runs_df)} rows to {runs_output_path}")

    if all_blocks_data:
        blocks_df_final = pd.concat(all_blocks_data, ignore_index=True)
        blocks_output_path = os.path.join(output_dir, 'blocks.csv')
        blocks_df_final.to_csv(blocks_output_path, index=False)
        print(f"--> Wrote {len(blocks_df_final)} rows to {blocks_output_path}")
    else:
        print("--> No block data generated for blocks.csv.")

    meta_data = {
        'run_directory': f'phase1_run_{timestamp}',
        'timestamp_utc': time.asctime(time.gmtime()),
        'total_runs_in_sweep': run_counter,
        'simulation_points': simulation_points,
        'seeds_used': seeds,
        'fixed_params': {'gamma': gamma, 'grid_size': grid_size},
        'stability_params': {
            'dt_logic': 'min(0.02, 0.1, tau_nondim/50, 0.1/(gamma_nondim + |a_nondim| + 1))',
            'a_ref': a_ref,
            'tau_ref': tau_ref,
            'delay_interpolation': True,
        },
    }

    repo_root = Path(__file__).resolve().parents[2]
    try:
        code_version = subprocess.check_output([
            'git', 'rev-parse', 'HEAD'
        ], cwd=repo_root).decode().strip()
    except Exception:
        code_version = 'unknown'

    meta_data.update({
        'manifest': 'MANIFESTO.md',
        'code_version': code_version,
        'seeds_detailed': [{'seed': s} for s in seeds],
        'front_thresholds': [1.0, 3.0, 5.0],
    })
    meta_output_path = os.path.join(output_dir, 'run_meta.json')
    with open(meta_output_path, 'w') as f:
        json.dump(meta_data, f, indent=4)
    print(f"--> Wrote metadata to {meta_output_path}")

if __name__ == "__main__":
    main()
