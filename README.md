# DOFT — Delayed Oscillator Field Theory

This repository is the central index for DOFT. It brings together the theory,
studies, references, and the project's public website.

Research currently continues outside this repository and has reached
**Study 06**. The local content does not yet fully reflect that stage. This
reorganization first preserves the existing material and prepares a place to
consolidate findings from every study.

## Repository status

- The former Python simulator has been removed from the active area and
  preserved in [`legacy/simulation-v0.1/`](./legacy/simulation-v0.1/).
- Existing documents have been preserved without rewriting their content.
- Protocols tied to the former simulator have been archived so they are not
  presented as current methodology.
- The first local website version is implemented in [`website/`](./website/).
  Its GitHub Pages workflow is ready; it has not yet been deployed.
- Study-specific source code and data remain in their own repositories and
  published archives; they are linked rather than copied here.

## Index

| Area | Contents |
| --- | --- |
| [`docs/`](./docs/) | Theory, studies, and the document archive |
| [`references/`](./references/) | Bibliography and related-repository map |
| [`website/`](./website/) | Public-facing DOFT overview and website source |
| [`legacy/`](./legacy/) | Unmaintained code and technical material |

## Available material

- [DOFT website source](./website/)
- [Study 06 dynamics page source](./website/app/dynamics/)
- [DOFT Manifesto v1.8](./docs/theory/MANIFESTO_v1.8.md)
- [Manifesto explained](./docs/theory/MANIFESTO_EXPLAINED.md)
- [Manifesto explained in Spanish](./docs/theory/MANIFESTO_EXPLICADO.md)
- [Study 01 — extracted overview and findings](./docs/studies/study-01/)
- [Study 02 — extracted overview and findings](./docs/studies/study-02/)
- [Study 05 — extracted overview and findings](./docs/studies/study-05/)
- [Study 06 — active source repository](https://github.com/cesaragostino/doft-study06-fundamental-lock-dynamics)
- [Study 01–06 index](./docs/studies/)
- [Bibliographic references](./references/)
- [DOFT repository map](./references/repositories.md)
- [Citation guide](./references/citation.md)

## Next stage

Study 01, Study 02, and Study 05 have been extracted from their source
repositories and published archives. No valid conclusions are retained from
Study 03 or Study 04, following the author's direction. The first website
version now combines those audited records with a dated synthesis of the
active Study 06 evidence. A full Study 06 central extraction remains pending.

The website is prepared for deployment through GitHub Actions at:

<https://doft.space/>

The workflow builds the website as a static export and publishes it from the
root of the custom domain.

## License and citation

The repository is distributed under the [MIT License](./LICENSE) unless an
individual file states otherwise. Deprecated code is provided without
maintenance or security support.

For repository and study-specific citation guidance, see:

- [`references/citation.md`](./references/citation.md)
- [`CITATION.cff`](./CITATION.cff)

## Contributing and governance

- [Contributing guide](./CONTRIBUTING.md)
- [Governance](./GOVERNANCE.md)
- [Code of Conduct](./CODE_OF_CONDUCT.md)
- [Security policy](./SECURITY.md)
