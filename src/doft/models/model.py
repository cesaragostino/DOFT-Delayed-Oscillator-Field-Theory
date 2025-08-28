# src/doft/models/model.py
import numpy as np
import pandas as pd
from scipy.stats import theilslopes
import math
import warnings

from doft.utils.utils import spectral_entropy


def compute_energy(Q: np.ndarray, P: np.ndarray) -> float:
    """Return total nondimensional energy of the lattice.

    Parameters
    ----------
    Q, P:
        Field displacement and momentum arrays.

    Notes
    -----
    Uses a simple quadratic energy: kinetic (``P``) plus potential (``Q``).
    Coupling terms are omitted; this monitor is intended only to check that
    the semi-implicit scheme with damping does not spuriously increase the
    basic oscillator energy.
    """

    kinetic = 0.5 * np.sum(P ** 2)
    potential = 0.5 * np.sum(Q ** 2)
    return float(kinetic + potential)


class DOFTModel:
    def __init__(
        self,
        grid_size,
        a,
        tau,
        a_ref,
        tau_ref,
        gamma,
        seed,
        dt_nondim: float | None = None,
    ):
        self.grid_size = grid_size
        self.seed = seed
        self.rng = np.random.default_rng(self.seed)

        # STABILITY FIX #1: NONDIMENSIONALIZATION
        # Use reference scales to make all simulation variables of order ~1.
        self.tau_ref = tau_ref  # Reference time scale (e.g., 1.0)
        self.a_ref = a_ref      # Reference coupling scale (e.g., 1.0)

        # Nondimensionalize the parameters for this specific run
        self.a_nondim = a / self.a_ref
        self.tau_nondim = tau / self.tau_ref
        self.gamma_nondim = gamma * self.tau_ref

        # STABILITY FIX #2: SAFE TIME STEP
        # Determine a stable dimensionless time step based on current parameters.
        denom = self.gamma_nondim + abs(self.a_nondim) + 1.0
        if denom > 0:
            gamma_bound = 0.1 / denom
        else:
            gamma_bound = float("inf")
        safe_dt = min(0.02, 0.1, self.tau_nondim / 50.0, gamma_bound)
        if dt_nondim is not None and not math.isclose(dt_nondim, safe_dt, rel_tol=0, abs_tol=1e-12):
            warnings.warn(
                f"Requested dt_nondim={dt_nondim} replaced by stable dt_nondim={safe_dt}",
                RuntimeWarning,
            )
        self.dt_nondim = safe_dt
        self.min_dt_nondim = 1e-6  # Lower bound to prevent infinite halving loops
        self.dt = self.dt_nondim * self.tau_ref  # Actual dt in "physical" units

        # The physical tau is still needed for delay calculation
        self.tau = tau

        # Precompute delay in time steps to avoid repeated calculation
        self.delay_in_steps = self.tau / self.dt

        # Correctly size the history buffer with the new, smaller dt
        self.history_steps = int(math.ceil(self.tau / self.dt)) + 5  # Added safe margin

        self.Q = np.zeros((grid_size, grid_size), dtype=np.float64)
        self.P = np.zeros((grid_size, grid_size), dtype=np.float64)
        self.Q_history = np.zeros((self.history_steps, grid_size, grid_size), dtype=np.float64)

        # Energy monitoring for source-free simulations
        self.energy_log: list[float] = []
        self.last_energy = compute_energy(self.Q, self.P)

        # Track scaling applied to the fields to avoid overflow
        self.scale_threshold = 1e6
        self.scale_accum = 1.0
        self.scale_log: list[float] = []

    def _get_delayed_q_interpolated(self, t_idx):
        """
        STABILITY FIX #3: LINEAR INTERPOLATION FOR DELAYS
        Improves accuracy and stability by interpolating between two past time steps
        instead of taking the nearest neighbor.
        """
        delay_in_steps = self.delay_in_steps

        idx_floor = int(math.floor(delay_in_steps))
        idx_ceil = int(math.ceil(delay_in_steps))

        if idx_floor == idx_ceil:
            # The delay is an exact multiple of dt
            history_idx = (t_idx - idx_floor) % self.history_steps
            return self.Q_history[history_idx]

        # Get the two bracketing time steps from history
        hist_idx1 = (t_idx - idx_floor) % self.history_steps
        hist_idx2 = (t_idx - idx_ceil) % self.history_steps
        Q1 = self.Q_history[hist_idx1]
        Q2 = self.Q_history[hist_idx2]

        # Interpolation factor (fractional part)
        frac = delay_in_steps - idx_floor

        # Linearly interpolate between the two states
        return Q2 * frac + Q1 * (1.0 - frac)

    def _step_euler(self, t_idx):
        Q_prev = self.Q.copy()
        P_prev = self.P.copy()
        energy_prev = self.last_energy

        while True:
            Q_delayed = self._get_delayed_q_interpolated(t_idx)

            # The equations of motion now use dimensionless parameters
            K_term = self.a_nondim * (
                np.roll(Q_delayed, 1, axis=0) + np.roll(Q_delayed, -1, axis=0) +
                np.roll(Q_delayed, 1, axis=1) + np.roll(Q_delayed, -1, axis=1) - 4 * Q_delayed
            )
            # Semi-implicit update for P with gamma term treated implicitly
            # P_new = (P - dt_nondim * Q + dt_nondim * K_term) / (1 + dt_nondim * gamma_nondim)
            P_new = (
                self.P - self.dt_nondim * self.Q + self.dt_nondim * K_term
            ) / (1.0 + self.dt_nondim * self.gamma_nondim)
            # Leapfrog-style update for Q using the newly updated momentum
            Q_new = self.Q + self.dt_nondim * P_new

            # Compute norms and rescale if necessary to avoid overflow
            norm_Q = np.linalg.norm(Q_new)
            norm_P = np.linalg.norm(P_new)
            scale = max(norm_Q, norm_P)
            if scale > self.scale_threshold:
                Q_new /= scale
                P_new /= scale
                self.Q_history /= scale
                self.scale_accum *= scale
                self.last_energy /= scale ** 2
                energy_prev = self.last_energy

            energy_new = compute_energy(Q_new, P_new)
            energy_prev_phys = energy_prev * self.scale_accum ** 2
            energy_new_phys = energy_new * self.scale_accum ** 2

            if (
                np.isfinite(P_new).all()
                and np.isfinite(Q_new).all()
                and energy_new_phys <= energy_prev_phys + 1e-12
            ):
                self.P, self.Q = P_new, Q_new
                self.Q_history[t_idx % self.history_steps] = self.Q
                self.last_energy = energy_new
                self.energy_log.append(energy_new_phys)
                self.scale_log.append(self.scale_accum)
                break

            if not (np.isfinite(P_new).all() and np.isfinite(Q_new).all()):
                print(
                    f"WARNING: Non-finite values encountered at step {t_idx}. "
                    f"Reducing dt_nondim from {self.dt_nondim}"
                )
            else:
                print(
                    f"WARNING: Energy increased from {energy_prev} to {energy_new} at step {t_idx}. "
                    f"Reducing dt_nondim from {self.dt_nondim}"
                )

            self.P = P_prev.copy()
            self.Q = Q_prev.copy()
            self.last_energy = energy_prev
            new_dt = self.dt_nondim * 0.5
            if new_dt < self.min_dt_nondim:
                print(
                    f"ERROR: Minimum dt_nondim {self.min_dt_nondim} reached. "
                    "Aborting step."
                )
                self.dt_nondim = self.min_dt_nondim
                self.dt = self.dt_nondim * self.tau_ref
                self.delay_in_steps = self.tau / self.dt
                required_history = int(math.ceil(self.tau / self.dt))
                if self.history_steps < required_history:
                    new_history_steps = required_history + 5
                    new_Q_history = np.zeros(
                        (new_history_steps, self.grid_size, self.grid_size),
                        dtype=self.Q_history.dtype,
                    )
                    for i in range(self.history_steps):
                        new_Q_history[(t_idx - i) % new_history_steps] = self.Q_history[
                            (t_idx - i) % self.history_steps
                        ]
                    self.Q_history = new_Q_history
                    self.history_steps = new_history_steps
                break

            self.dt_nondim = new_dt
            self.dt = self.dt_nondim * self.tau_ref
            self.delay_in_steps = self.tau / self.dt

            required_history = int(math.ceil(self.tau / self.dt))
            if self.history_steps < required_history:
                new_history_steps = required_history + 5
                new_Q_history = np.zeros(
                    (new_history_steps, self.grid_size, self.grid_size),
                    dtype=self.Q_history.dtype,
                )
                for i in range(self.history_steps):
                    new_Q_history[(t_idx - i) % new_history_steps] = self.Q_history[
                        (t_idx - i) % self.history_steps
                    ]
                self.Q_history = new_Q_history
                self.history_steps = new_history_steps

    
    def _calculate_pulse_metrics(self, n_steps, noise_std: float = 0.0):
        r"""Estimate wave-front speed using multiple noise-relative thresholds.

        Parameters
        ----------
        n_steps:
            Number of integration steps.
        noise_std:
            Standard deviation of the synthetic noise added before injecting the
            pulse. The resulting floor :math:`\xi` sets the detection thresholds
            ``{1σ, 3σ, 5σ}``.
        """

        # Reset fields and optional pre-pulse noise
        self.Q.fill(0.0)
        self.P.fill(0.0)
        self.Q_history.fill(0.0)
        if noise_std > 0.0:
            self.Q += self.rng.normal(0.0, noise_std, size=self.Q.shape)

        # Noise floor and thresholds relative to it
        xi_floor = float(np.std(self.Q))
        xi_floor = max(xi_floor, 1e-12)
        thresholds = xi_floor * np.array([1.0, 3.0, 5.0])

        center = self.grid_size // 2

        # Inject Gaussian pulse
        x, y = np.meshgrid(np.arange(self.grid_size), np.arange(self.grid_size))
        self.Q += 0.1 * np.exp(-((x - center) ** 2 + (y - center) ** 2) / 10.0)

        num_angles = 16
        thetas = np.linspace(0, 2 * np.pi, num_angles, endpoint=False)

        front_detections = {
            (theta, thr_idx): []
            for theta in thetas
            for thr_idx in range(len(thresholds))
        }
        max_r_so_far = {
            (theta, thr_idx): 0
            for theta in thetas
            for thr_idx in range(len(thresholds))
        }

        for t_idx in range(n_steps):
            self._step_euler(t_idx)
            t_now = t_idx * self.dt
            for theta in thetas:
                cos_t, sin_t = np.cos(theta), np.sin(theta)
                for thr_idx, thr in enumerate(thresholds):
                    r_start = max_r_so_far[(theta, thr_idx)]
                    for r in range(r_start, center):
                        px = int(center + r * cos_t)
                        py = int(center + r * sin_t)
                        if self.Q[py, px] > thr:
                            max_r_so_far[(theta, thr_idx)] = r
                    rmax = max_r_so_far[(theta, thr_idx)]
                    if rmax > 0:
                        front_detections[(theta, thr_idx)].append((t_now, rmax))

        c_thetas = []
        c_thetas_ci_low = []
        c_thetas_ci_high = []
        for idx, theta in enumerate(thetas):
            detections = np.array(
                list(dict.fromkeys(front_detections[(theta, 1)]))
            )
            if len(detections) < 10:
                continue
            times, dists = detections[:, 0], detections[:, 1]
            res = theilslopes(dists, times, 0.95)
            c_thetas.append(res[0])
            c_thetas_ci_low.append(res[2])
            c_thetas_ci_high.append(res[3])

        if not c_thetas:
            return {
                'xi_floor': xi_floor,
                'ceff_pulse': 0.0,
                'ceff_pulse_ic95_lo': 0.0,
                'ceff_pulse_ic95_hi': 0.0,
                'anisotropy_max_pct': 100.0,
                'var_c_over_c2': 1.0,
                'ceff_iso_x': 0.0,
                'ceff_iso_y': 0.0,
                'ceff_iso_z': 0.0,
                'ceff_iso_diag': 0.0,
            }

        c_thetas = np.array(c_thetas)
        mean_c = float(np.mean(c_thetas))
        var_c_over_c2 = np.var(c_thetas) / (mean_c ** 2) if mean_c > 0 else 1.0
        anisotropy_max_pct = (
            np.max(np.abs(c_thetas - mean_c)) / mean_c * 100 if mean_c > 0 else 100.0
        )
        ci_low = float(np.mean(c_thetas_ci_low))
        ci_high = float(np.mean(c_thetas_ci_high))

        c_x = c_thetas[0] if len(c_thetas) > 0 else 0.0
        c_y = c_thetas[num_angles // 4] if len(c_thetas) > num_angles // 4 else 0.0
        c_z = c_thetas[num_angles // 8] if len(c_thetas) > num_angles // 8 else 0.0
        c_diag = (
            c_thetas[3 * num_angles // 8]
            if len(c_thetas) > 3 * num_angles // 8
            else 0.0
        )

        return {
            'xi_floor': xi_floor,
            'ceff_pulse': mean_c,
            'ceff_pulse_ic95_lo': ci_low,
            'ceff_pulse_ic95_hi': ci_high,
            'anisotropy_max_pct': anisotropy_max_pct,
            'var_c_over_c2': var_c_over_c2,
            'ceff_iso_x': c_x,
            'ceff_iso_y': c_y,
            'ceff_iso_z': c_z,
            'ceff_iso_diag': c_diag,
        }

    def _calculate_lpc_metrics(self, n_steps):
        self.Q = self.rng.normal(0, 0.1, self.Q.shape); self.P.fill(0.0); self.Q_history.fill(0.0)
        center = self.grid_size // 2
        time_series = np.zeros(n_steps)
        for t_idx in range(n_steps):
            self._step_euler(t_idx)
            time_series[t_idx] = self.Q[center, center]

        # STABILITY FIX #4: NUMERICAL GUARD
        # Check for non-finite values before spectral calculations.
        # We no longer abort the entire metric calculation if non-finite
        # values appear; instead, individual windows will be skipped.
        if not np.all(np.isfinite(time_series)):
            print("  WARNING: Non-finite values detected in time series.")

        win_size, overlap = 4096, 2048 # Larger window for finer frequency resolution with small dt
        step = win_size - overlap
        if len(time_series) < win_size:
            return {'block_skipped': 0}, pd.DataFrame()
        block_data, last_K = [], None
        block_skipped = 0
        num_windows = (len(time_series) - win_size) // step + 1
        for i in range(num_windows):
            window_data = time_series[i*step : i*step + win_size]
            if not np.isfinite(window_data).all():
                block_skipped += 1
                block_data.append({'window_id': i,
                                    'K_metric': np.nan,
                                    'deltaK': np.nan,
                                    'block_skipped': 1})
                continue
            K_metric = spectral_entropy(window_data)
            deltaK = K_metric - last_K if last_K is not None else 0.0
            block_data.append({'window_id': i,
                                'K_metric': K_metric,
                                'deltaK': deltaK,
                                'block_skipped': 0})
            last_K = K_metric

        blocks_df = pd.DataFrame(block_data)

        valid_blocks = blocks_df[blocks_df['block_skipped'] == 0]
        windows_analyzed = len(valid_blocks)
        if windows_analyzed > 1:
            deltaK_neg_count = (valid_blocks['deltaK'][1:] <= 0).sum()
            lpc_ok_frac = deltaK_neg_count / (windows_analyzed - 1)
        else:
            lpc_ok_frac = 0.0

        return {
            'lpc_ok_frac': lpc_ok_frac,
            'lpc_vcount': 0,
            'lpc_windows_analyzed': windows_analyzed,
            'block_skipped': block_skipped,
        }, blocks_df

    def run(self):
        # Adjust n_steps to account for the much smaller dt, simulating a similar physical duration.
        # old_dt=0.1, new_dt=0.005*tau_ref. Ratio is ~20.
        pulse_steps = int(3000 * (0.1 / self.dt))
        lpc_steps = int(30000 * (0.1 / self.dt))

        pulse_metrics = self._calculate_pulse_metrics(n_steps=pulse_steps)
        lpc_metrics, blocks_df = self._calculate_lpc_metrics(n_steps=lpc_steps)
        final_run_metrics = {**pulse_metrics, **lpc_metrics}
        return final_run_metrics, blocks_df
    