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
  repository snapshot.
- `scripts/README_RUN_P1.md` refers to earlier paths.
- Compatibility with current environments and dependencies is not guaranteed.
- Tests were neither run nor repaired during deprecation.

The move preserves Git history; it does not imply that the simulator was
validated.
