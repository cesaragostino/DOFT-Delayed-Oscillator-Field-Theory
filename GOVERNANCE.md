# Governance

This document describes how the central DOFT repository is maintained and how
its research record is changed.

Repository:
<https://github.com/cesaragostino/DOFT-Delayed-Oscillator-Field-Theory>

## Repository role

This repository is the central index for DOFT theory, evidence-reviewed study
summaries, references, and the future public website. It is not the active
computational repository for any current study. Deprecated software is
preserved under `legacy/`.

Study-specific source code, datasets, and generated artifacts remain in their
source repositories and published archives. The central repository records
their provenance, findings, limitations, and relationships.

## Maintainer

The repository owner and current maintainer is
[Cesar Agostino](https://github.com/cesaragostino).

The maintainer has final responsibility for:

- the scope and direction of DOFT;
- the status assigned to each study;
- acceptance of changes to theory and research synthesis;
- releases, licensing, and repository transfer;
- security and conduct decisions.

Additional maintainers may be appointed through a public governance change.

## Decision-making

Routine corrections, link updates, and evidence-preserving reorganizations may
be accepted by the maintainer directly.

Changes that materially alter theory, scientific conclusions, study status,
licensing, or repository ownership require explicit maintainer approval and a
written rationale in the commit, pull request, or accompanying research log.

When evidence conflicts with an existing claim, the repository should preserve
the provenance of the claim while clearly recording the conflict. Historical
documents are archived rather than silently rewritten as current evidence.

## Content policy

- Repository-maintained content is written in English.
- An explicitly identified Spanish manifesto edition may be maintained as a
  translation.
- Study summaries distinguish direct artifact evidence, independent
  reanalysis, interpretation, and unresolved claims.
- A published artifact is not silently replaced by a later source revision.
- Source repositories are linked, not nested or copied into this repository.
- Active code does not belong at the repository root. Historical code belongs
  under `legacy/` and must be marked deprecated.
- Large generated artifacts should remain in their source archive unless they
  are essential to the central record.

## Branches and review

`main` is the public repository state. Topic branches are recommended for
substantial work. The maintainer may also make direct, reviewed commits for
repository administration or focused corrections.

Pull requests should be narrow enough to review and should describe:

- what changed and why;
- which evidence or source record supports the change;
- whether scientific interpretation changed;
- what validation was performed;
- any use of automated or AI-assisted generation that materially affected the
  result.

The contribution process is described in
[`CONTRIBUTING.md`](./CONTRIBUTING.md).

## Releases and citation

Repository releases are created when a stable central snapshot is ready to be
cited or archived. A release should:

1. identify the exact Git commit;
2. summarize incorporated studies and status changes;
3. update citation metadata;
4. create a GitHub release and, when appropriate, a Zenodo version;
5. distinguish the version DOI from the concept DOI.

The human-readable citation policy is maintained in
[`references/citation.md`](./references/citation.md).

## AI-assisted work

AI tools may assist with research review, code inspection, editing, or
analysis. The maintainer remains accountable for every merged result.

Material AI assistance should be disclosed in a commit or pull-request note
when it affects scientific reasoning, nontrivial analysis, or substantial
generated text. The disclosure should identify the task performed and the
human validation applied; it need not preserve private prompts or expose
sensitive information.

Secrets, private data, unpublished third-party material, and restricted data
must not be submitted to external tools without authorization.

## Security and conduct

Security reporting is described in [`SECURITY.md`](./SECURITY.md). Community
expectations are described in [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md).

## Amendments

Governance changes are proposed through a commit or pull request that explains
their effect. Material changes require explicit approval by the repository
owner.

Last updated: 2026-07-24.
