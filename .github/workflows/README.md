# GitHub Actions Workflows

This directory contains the GitHub Actions workflows for the dify-api-client project.

## Workflows

### CI (`ci.yml`)
**Triggers:** Push to `main`/`develop` branches, Pull Requests

**Jobs:**
- **Lint**: Runs Ruff linter and formatter checks
- **Test**: Runs pytest on Python 3.10, 3.11, and 3.12

### Publish (`publish.yml`)
**Triggers:** When a release is published on GitHub

**Jobs:**
- Verifies tag version matches package version
- Builds the package using Hatch
- Publishes to PyPI using `PYPI_API_TOKEN` secret

## Setup Required

### For Publishing to PyPI

Add your PyPI API token as a GitHub secret:
1. Generate a token at https://pypi.org/manage/account/token/
2. Go to repository Settings → Secrets and variables → Actions
3. Add secret named `PYPI_API_TOKEN` with your token

### For CI/CD

No additional setup required. The CI workflow runs automatically on pushes and pull requests.

