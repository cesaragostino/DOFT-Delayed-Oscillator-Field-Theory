# tests/test_model_run.py
"""Basic tests for the high-level ``DOFTModel.run`` interface."""

import sys
from pathlib import Path

import numpy as np

# Ensure the package import works when repository root is the current directory
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from doft.models.model import DOFTModel


def create_model(seed=0, dt_nondim=0.1):
    return DOFTModel(
        grid_size=4,
        a=1.0,
        tau=1.0,
        a_ref=1.0,
        tau_ref=1.0,
        gamma=0.1,
        seed=seed,
        dt_nondim=dt_nondim,
    )


def test_pulse_metrics_numeric():
    model = create_model(seed=0)
    metrics = model._calculate_pulse_metrics(n_steps=50, noise_std=0.0)

    assert "ceff_pulse" in metrics
    assert "ceff_pulse_ic95_lo" in metrics
    assert "ceff_pulse_ic95_hi" in metrics
    assert "ceff_iso_diag" in metrics
    assert np.isfinite(metrics["ceff_pulse"])


def test_seed_reproducibility_lpc_metrics():
    m1 = create_model(seed=123)
    m2 = create_model(seed=123)
    r1, _ = m1._calculate_lpc_metrics(n_steps=50)
    r2, _ = m2._calculate_lpc_metrics(n_steps=50)
    assert r1 == r2


def test_blocks_df_contains_block_skipped():
    model = create_model(seed=0)
    metrics, blocks_df = model._calculate_lpc_metrics(n_steps=7000)
    assert 'lpc_ok_frac' in metrics
    assert 'block_skipped' in blocks_df.columns
    # block_skipped metric should match the count of skipped windows
    assert metrics['block_skipped'] == int((blocks_df['block_skipped'] == 1).sum())
    # All entries should be either 0 or 1
    assert set(blocks_df['block_skipped'].unique()).issubset({0, 1})
    

def test_noise_floor_effect():
    m_low = create_model(seed=0)
    m_high = create_model(seed=0)
    metrics_low = m_low._calculate_pulse_metrics(n_steps=50, noise_std=0.01)
    metrics_high = m_high._calculate_pulse_metrics(n_steps=50, noise_std=0.03)
    assert metrics_high['xi_floor'] > metrics_low['xi_floor']
    # Effective speed should remain finite under varying noise floors
    assert np.isfinite(metrics_low['ceff_pulse'])
    assert np.isfinite(metrics_high['ceff_pulse'])


def test_run_returns_required_fields():
    model = create_model(seed=0)
    metrics, _ = model.run()
    required = {
        'ceff_pulse_ic95_lo',
        'ceff_pulse_ic95_hi',
        'ceff_iso_diag',
        'lpc_ok_frac',
    }
    assert required.issubset(metrics.keys())
