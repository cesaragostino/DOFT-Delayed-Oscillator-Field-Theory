"""DOFT Cluster Simulator package."""

<<<<<<< ours
from __future__ import annotations

from typing import Iterable, Optional

__all__ = ["run_from_args"]


def run_from_args(argv: Optional[Iterable[str]] = None) -> None:
    """Entry point wrapper that defers importing the CLI module.

    Delaying the import avoids confusing runpy when executing
    ``python -m scripts.doft_cluster_simulator.cli``.
    """

    from .cli import run_from_args as _run_from_args

    _run_from_args(list(argv) if argv is not None else None)
=======
from .cli import run_from_args

__all__ = ["run_from_args"]
>>>>>>> theirs
