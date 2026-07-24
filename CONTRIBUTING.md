# Contributing

Thank you for helping improve the central DOFT research record.

## Before contributing

This repository is a research index, not the active codebase for a current
study. Contributions should normally improve:

- evidence-reviewed study summaries;
- theory-document organization and status;
- references and repository links;
- reproducibility or provenance records;
- governance, citation, and public website material.

Study-specific code, raw data, and generated outputs should remain in their
source repository or published archive. Deprecated central code belongs only
under `legacy/`.

## Language

Repository-maintained prose is written in English. The explicitly identified
Spanish manifesto edition is the sole standing translation exception.
Historical material may preserve its original language only when it is clearly
archived and necessary for provenance.

## Evidence requirements

Scientific changes should identify their evidence level:

- **Direct artifact:** present in a source dataset, code path, configuration,
  paper, or archive.
- **Reanalysis:** independently recomputed from identified source material.
- **Interpretation:** a reasoned inference from the evidence.
- **Unresolved or invalidated:** not demonstrated, contradicted, or prevented
  by a material implementation or analysis defect.

Do not rewrite a historical claim as if it had never existed. Preserve its
source and explain why the active assessment changed.

## Study extraction structure

A completed extraction normally contains:

```text
docs/studies/study-XX/
├── README.md
├── findings.md
└── research-log.md
```

- `README.md` is a concise, website-ready overview.
- `findings.md` contains the detailed evidence assessment.
- `research-log.md` records provenance, archive integrity, verification work,
  decisions, and open questions.

Repository links belong in `references/repositories.md`; citation guidance
belongs in `references/citation.md`.

## Pull requests

Keep changes focused and explain:

1. what changed;
2. why it changed;
3. the source records or evidence used;
4. whether a scientific conclusion or status changed;
5. the checks performed;
6. any material AI assistance and its human review.

Do not commit secrets, credentials, private data, dependency directories,
temporary outputs, or large generated artifacts.

## Validation

Use checks appropriate to the change. At minimum:

- verify relative Markdown links;
- validate `CITATION.cff` after citation changes;
- check that repository-maintained prose is English;
- run `git diff --check`;
- confirm no active code was added outside `legacy/`;
- review the complete staged diff before committing.

The maintainer makes the final decision under
[`GOVERNANCE.md`](./GOVERNANCE.md).
