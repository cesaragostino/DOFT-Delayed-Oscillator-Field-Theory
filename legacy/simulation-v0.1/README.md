# DOFT simulation v0.1 — DEPRECATED

> **Status:** dead code, unmaintained, and excluded from the project's active
> architecture.

This snapshot preserves the Python package, its tests, execution scripts, and
environment files as a single unit. It was moved to `legacy/` during the
reorganization of the central repository.

## Preserved contents

- `src/` — Python implementation.
- `tests/` — historical test suite.
- `scripts/` — execution, installation, and analysis tools.
- `pyproject.toml`, `requirements.txt` — snapshot metadata and dependencies.

## Known limitations at the time of archival

- The scripts expect `configs/*.json` files that are absent from the current
  repository snapshot. Those files had been removed before this snapshot was
  archived; some remain recoverable from earlier Git history.
- The orphaned `test_doft_cluster_simulator.py` file was excluded from this
  snapshot. It targeted the previously removed Cluster Simulator, depended on
  missing modules, and contained unresolved merge markers. Its original state
  remains recoverable from commit `7df7c24`.
- `scripts/README_RUN_P1.md` refers to earlier paths.
- Compatibility with current environments and dependencies is not guaranteed.
- Tests were neither run nor repaired during deprecation.

The move preserves Git history; it does not imply that the simulator was
validated.

## Use warning

This directory receives no maintenance, dependency updates, or security
patches. Do not treat its commands as current project instructions. If it must
be examined, use an isolated environment and pin dependencies explicitly.
