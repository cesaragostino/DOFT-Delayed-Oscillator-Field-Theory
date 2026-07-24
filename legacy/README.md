# Legacy

This area contains historical DOFT implementations that have been removed from
active development.

| Snapshot | Status | Description |
| --- | --- | --- |
| [`simulation-v0.1/`](./simulation-v0.1/) | Deprecated | Python simulator, scripts, and tests from the previous development cycle |

The content is preserved for traceability. It does not represent the current
implementation of the theory and should not be used as the basis for new
development without an explicit review.

## Boundary and provenance

`simulation-v0.1/` contains the complete code, scripts, dependency metadata,
and tests that were present in the active root immediately before the 2026
central-repository reorganization. Generated results and missing configuration
files are not reconstructed.

An older Cluster Simulator, its configurations, generated report, and mixed-
language development notes had already been removed in commit `7df7c24` before
this reorganization began. They remain recoverable from its parent commit
`384d76c` through Git history, but they are not silently restored as part of
this later snapshot.

## Policy

- Nothing under `legacy/` is an active dependency of the central repository or
  future website.
- No compatibility, correctness, or security support is provided.
- Historical material should not be moved back into active areas without a
  documented review.
- The repository's MIT License applies unless a file states otherwise.
