# Security Policy

## Scope

The central repository contains documentation, references, a future website
workspace, and deprecated historical software. It does not currently provide a
supported runtime or public service.

Security reports may nevertheless concern:

- credentials or private data committed to the repository;
- malicious or unsafe website content;
- dependency or execution risks in material presented as active;
- vulnerabilities in repository automation;
- unsafe instructions in archived software that could affect readers.

Deprecated code under `legacy/` receives no compatibility or security support.
Its presence is for historical traceability and does not imply that it is safe
to run.

## Reporting

Use GitHub private vulnerability reporting from the repository's **Security**
tab when available.

If private reporting is unavailable, contact the repository owner through the
options on the [maintainer's GitHub profile](https://github.com/cesaragostino)
or open a minimal issue requesting a private contact channel. Do not publish
exploit details, secrets, or sensitive data in a public issue.

Include:

- the affected file, revision, or URL;
- the potential impact;
- reproduction information that is safe to share privately;
- any suggested mitigation.

## Response

The maintainer will acknowledge a valid private report, assess its scope, and
coordinate a correction or disclosure appropriate to the risk. No fixed
service-level guarantee is currently offered.
