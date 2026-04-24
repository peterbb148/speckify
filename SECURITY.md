# Security Policy

## Supported Versions

Speckify is currently maintained from the `main` branch. Security fixes are applied there
first.

## Reporting A Vulnerability

Please do not open a public GitHub issue for a suspected security vulnerability.

Instead, report it privately to the maintainer before public disclosure so the issue can
be reviewed and fixed responsibly. Include:

- a clear description of the issue
- affected files, commands, or workflows
- reproduction steps if available
- expected impact

If you are unsure whether something is a security issue, report it anyway.

## Scope Notes

Speckify is a local, model-driven downstream specification toolkit. Security-relevant
concerns may include:

- unsafe command execution or shell handling
- unsafe file overwrite or path handling
- malformed bundle or export parsing behavior
- workflow or automation behavior that could trigger unintended side effects
- documentation or examples that could mislead users into insecure operation

Third-party platform configuration outside this repository is not covered by code fixes
here, but documentation gaps should still be reported.
