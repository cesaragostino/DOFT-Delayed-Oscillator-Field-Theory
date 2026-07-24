#!/usr/bin/env python3
"""Render the website's Study 06 figures from the versioned draft data.

Source artifact:
  doft-study06-fundamental-lock-dynamics/artifact_estado_programa.html
  commit 5e2889b9842e251d8e31a2c3580ebfd0d1d40966

The values below are a direct transcription of that artifact's seven inline
charts. The website selects five and renders them in English without adding
new fits or smoothing.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "public" / "figures"

PAPER = "#fbf8f2"
INK = "#1c1b19"
MUTED = "#68645e"
LINE = "#cdc3b6"
ORANGE = "#b95738"
ORANGE_DARK = "#843c28"
TEAL = "#2f6f68"
TEAL_LIGHT = "#6f9f98"
GREY_LIGHT = "#a79c8f"


def configure() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": PAPER,
            "axes.facecolor": PAPER,
            "savefig.facecolor": PAPER,
            "font.family": "DejaVu Serif",
            "font.size": 11,
            "axes.labelcolor": MUTED,
            "axes.edgecolor": LINE,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "text.color": INK,
            "grid.color": LINE,
            "grid.alpha": 0.5,
            "grid.linewidth": 0.7,
        }
    )


def finish(fig: plt.Figure, name: str) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        OUTPUT / name,
        dpi=180,
        bbox_inches="tight",
        pad_inches=0.16,
    )
    plt.close(fig)


def setup_axes(
    xlabel: str,
    ylabel: str,
    *,
    figsize: tuple[float, float] = (7.6, 4.5),
) -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=figsize)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(LINE)
    ax.spines["bottom"].set_color(LINE)
    ax.grid(axis="y")
    ax.set_xlabel(xlabel, labelpad=10)
    ax.set_ylabel(ylabel, labelpad=10)
    return fig, ax


def hold_vs_energy() -> None:
    pair_a = np.array(
        [[0.2, 17.4], [1.0, 16.03], [5.1, 10.56], [20.7, 5.89], [57.9, 3.12]]
    )
    pair_b = np.array(
        [[0.11, 24.4], [0.95, 15.42], [5.0, 8.22], [11.0, 5.6], [20.1, 4.19]]
    )
    fig, ax = setup_axes(
        "weaker-node energy at connection (log scale)",
        "antisymmetric-lock hold (model time)",
    )
    ax.set_xscale("log")
    ax.plot(
        pair_a[:, 0],
        pair_a[:, 1],
        color=ORANGE,
        marker="o",
        linewidth=2,
        markersize=6,
        label="pair A · seed 42",
    )
    ax.plot(
        pair_b[:, 0],
        pair_b[:, 1],
        color=TEAL,
        marker="o",
        linewidth=2,
        markersize=6,
        label="pair B · seed 57",
    )
    ax.set_xlim(0.08, 75)
    ax.set_ylim(0, 27)
    ax.set_xticks([0.1, 1, 10, 60], ["0.1", "1", "10", "60"])
    ax.legend(frameon=False, loc="upper right")
    ax.text(
        0.02,
        0.04,
        "two histories · same monotone staircase",
        transform=ax.transAxes,
        color=MUTED,
        fontsize=9,
    )
    finish(fig, "hold-vs-energy.png")


def escape_law() -> None:
    points = np.array([[0.2, 12.64], [0.1, 14.16], [0.0632, 15.28], [0.02, 19.60]])
    x = -np.log(points[:, 0])
    fit_x = np.linspace(-np.log(0.22), -np.log(0.018), 100)
    fit_y = 7.33 + 3.06 * fit_x

    fig, ax = setup_axes(
        r"perturbation amplitude  $\delta$  (shown as $-\ln \delta$)",
        r"escape time  $t_{\mathrm{esc}}$  (model time)",
    )
    ax.plot(fit_x, fit_y, color=GREY_LIGHT, linewidth=1.6, label="effective log fit")
    ax.scatter(x, points[:, 1], s=58, color=ORANGE, edgecolor=PAPER, linewidth=1.2, zorder=3)
    for xi, yi, delta in zip(x, points[:, 1], points[:, 0], strict=True):
        ax.annotate(
            f"δ={delta:g}",
            (xi, yi),
            xytext=(0, 9),
            textcoords="offset points",
            ha="center",
            color=MUTED,
            fontsize=8,
        )
    ax.set_ylim(11, 21)
    ax.text(
        0.03,
        0.9,
        r"$t_{\mathrm{esc}} \approx 7.33 + 3.06\,\ln(1/\delta)$",
        transform=ax.transAxes,
        color=INK,
        fontsize=11,
    )
    ax.text(
        0.03,
        0.82,
        "R²=0.98 · n=4 · effective description",
        transform=ax.transAxes,
        color=ORANGE_DARK,
        fontsize=9,
    )
    finish(fig, "escape-law.png")


def instability_pulse() -> None:
    series = {
        "t_c = 70 · rising": [
            [1, 0.1019],
            [2, 0.1325],
            [3, 0.1254],
            [4, 0.114],
            [5, 0.0996],
            [6, 0.0816],
            [7, 0.0579],
            [8, 0.0229],
            [9, -0.0031],
            [10, -0.0361],
            [11, -0.0475],
            [12, 0.0201],
            [13, 0.2154],
            [14, 0.3776],
            [15, 0.4075],
            [16, 0.3729],
            [17, 0.328],
            [18, 0.2849],
            [19, 0.244],
            [20, 0.204],
        ],
        "t_c = 75 · rising": [
            [1, 0.0613],
            [2, 0.0778],
            [3, 0.0692],
            [4, 0.0532],
            [5, 0.0206],
            [6, -0.0059],
            [7, -0.0383],
            [8, -0.1099],
            [9, -0.174],
            [10, -0.1131],
            [11, 0.1777],
            [12, 0.4813],
            [13, 0.4739],
            [14, 0.4014],
            [15, 0.3372],
            [16, 0.2854],
            [17, 0.2391],
            [18, 0.2025],
            [19, 0.162],
            [20, 0.1255],
        ],
        "t_c = 80 · rising": [
            [1, 0.0365],
            [2, 0.0334],
            [3, 0.0288],
            [4, 0.0064],
            [5, -0.0238],
            [6, -0.0634],
            [7, -0.1287],
            [8, -0.222],
            [9, -0.263],
            [10, 0.005],
            [11, 0.4454],
            [12, 0.522],
            [13, 0.4204],
            [14, 0.3393],
            [15, 0.2818],
            [16, 0.2354],
            [17, 0.1977],
            [18, 0.1566],
            [19, 0.1274],
            [20, 0.0916],
        ],
        "t_c = 90 · peak": [
            [1, 0.0008],
            [2, 0.0057],
            [3, 0.0058],
            [4, 0.0212],
            [5, 0.0277],
            [6, 0.0145],
            [7, 0.009],
            [8, 0.0084],
            [9, -0.0346],
            [10, -0.0286],
            [11, 0.0304],
            [12, 0.0277],
            [13, -0.0039],
            [14, -0.0102],
            [15, -0.0054],
        ],
        "t_c = 104 · falling": [
            [1, -0.0241],
            [2, -0.0228],
            [3, -0.0343],
            [4, -0.0174],
            [5, 0.0055],
            [6, 0.0272],
            [7, 0.0311],
            [8, 0.0414],
            [9, 0.0304],
            [10, 0.0387],
            [11, 0.0328],
        ],
    }
    colors = [TEAL_LIGHT, ORANGE, ORANGE_DARK, MUTED, TEAL]
    fig, ax = setup_axes(
        r"time since connection  $t - t_c$  (model time)",
        r"local antisymmetric growth rate  $\lambda_-$",
        figsize=(8.8, 4.8),
    )
    ax.axhline(0, color=LINE, linestyle="--", linewidth=1)
    for (label, values), color in zip(series.items(), colors, strict=True):
        values_array = np.array(values)
        ax.plot(
            values_array[:, 0],
            values_array[:, 1],
            color=color,
            linewidth=2.1 if "rising" in label else 2.5,
            label=label,
        )
    ax.set_xlim(1, 20)
    ax.set_ylim(-0.32, 0.58)
    ax.legend(frameon=False, ncol=2, loc="upper left", fontsize=9)
    ax.text(
        0.98,
        0.08,
        "same scalar energy,\ndifferent dynamical epoch",
        transform=ax.transAxes,
        color=ORANGE_DARK,
        fontsize=10,
        ha="right",
        va="bottom",
    )
    finish(fig, "instability-pulse.png")


def spectroscopic_age() -> None:
    measured = np.array([[0.05, 48.6], [3.82, 56.2], [39.6, 105.3]])
    age = np.linspace(0, 43, 200)
    predicted = 47.77 * np.sqrt(1 + 0.1 * age)

    fig, ax = setup_axes(
        "accumulated S2-sector age  b",
        r"odd-sector frequency  $|\omega|$  (rad / model time)",
    )
    ax.plot(age, predicted, color=GREY_LIGHT, linewidth=1.8, label="motor prediction")
    ax.scatter(
        measured[:, 0],
        measured[:, 1],
        s=68,
        color=ORANGE,
        edgecolor=PAPER,
        linewidth=1.4,
        zorder=3,
        label="signed measurements",
    )
    for x, y, label in zip(
        measured[:, 0],
        measured[:, 1],
        ["cold", "hold", "post-release"],
        strict=True,
    ):
        ax.annotate(
            label,
            (x, y),
            xytext=(8, 6),
            textcoords="offset points",
            color=MUTED,
            fontsize=8,
        )
    ax.set_xlim(0, 44)
    ax.set_ylim(40, 115)
    ax.legend(frameon=False, loc="upper left")
    ax.text(
        0.52,
        0.34,
        r"$\omega_{\mathrm{eff}} = \omega_0 \sqrt{1 + 0.1b}$"
        "\n"
        r"$\omega_0 = 47.77$",
        transform=ax.transAxes,
        color=INK,
        fontsize=10,
    )
    finish(fig, "spectroscopic-age.png")


def causal_splitting() -> None:
    labels = ["draw 1\ns42", "draw 2\ns57", "draw 3\ns71", "draw 4\ns73"]
    values = np.array([0.117, 0.1037, 0.0972, 0.1185])
    causal = np.array([False, False, True, True])
    x = np.arange(len(labels))

    fig, ax = setup_axes(
        "",
        r"cold differential-clock shift  $\Delta\omega$  (rad / model time)",
        figsize=(7.6, 4.2),
    )
    ax.axhline(
        0.028,
        color=GREY_LIGHT,
        linestyle="--",
        linewidth=1.2,
        label="pre-registered replication floor",
    )
    for xi, value, is_causal in zip(x, values, causal, strict=True):
        color = ORANGE if is_causal else MUTED
        ax.vlines(xi, 0, value, color=color, linewidth=3)
        ax.scatter(
            xi,
            value,
            s=76,
            color=color,
            edgecolor=PAPER,
            linewidth=1.3,
            zorder=3,
        )
        ax.text(
            xi,
            value + 0.007,
            f"{value:.3f}",
            ha="center",
            color=INK,
            fontsize=9,
        )
        if is_causal:
            ax.text(
                xi,
                0.009,
                "paired causal",
                ha="center",
                color=ORANGE_DARK,
                fontsize=8,
            )
    ax.set_xticks(x, labels)
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(0, 0.14)
    ax.legend(frameon=False, loc="upper center", fontsize=9)
    finish(fig, "causal-splitting.png")


def main() -> None:
    configure()
    hold_vs_energy()
    escape_law()
    instability_pulse()
    spectroscopic_age()
    causal_splitting()


if __name__ == "__main__":
    main()
