"""Command line interface for the DOFT cluster simulator."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from .data import MaterialConfig, TargetDataset, load_loss_weights
from .engine import SimulationEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the DOFT cluster simulator")
    parser.add_argument("--config", type=Path, required=True, help="Ruta al archivo material_config.json")
    parser.add_argument("--targets", type=Path, required=True, help="Ruta al archivo de targets ground-truth")
    parser.add_argument("--weights", type=Path, help="Archivo JSON opcional con pesos de pérdida")
    parser.add_argument("--outdir", type=Path, default=Path("outputs"), help="Directorio de salida")
    parser.add_argument("--max-evals", type=int, default=500, help="Evaluaciones máximas por subred")
    parser.add_argument("--seed", type=int, default=42, help="Semilla de RNG")
    return parser


def run_from_args(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    config = MaterialConfig.from_file(args.config)
    dataset = TargetDataset.from_file(args.targets)
    weights = load_loss_weights(args.weights)

    engine = SimulationEngine(
        config=config,
        dataset=dataset,
        weights=weights,
        max_evals=args.max_evals,
        seed=args.seed,
    )
    bundle = engine.run()
    bundle.write(args.outdir, args.config, args.targets, args.max_evals, args.seed)


def main() -> None:
    run_from_args()


if __name__ == "__main__":
    main()

