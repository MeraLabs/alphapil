# Contributing to AlphaPIL

Thank you for your interest in contributing to **AlphaPIL**! We welcome contributions of all kinds – bug fixes, new features, documentation improvements, and more. This guide will help you get started quickly.

---

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Reporting Issues](#reporting-issues)
4. [Pull Request Process](#pull-request-process)
5. [Development Workflow](#development-workflow)
6. [Running Tests](#running-tests)
7. [Documentation](#documentation)
8. [Versioning & Releases](#versioning--releases)
9. [License](#license)
10. [Contact & Support](#contact--support)

---

## Code of Conduct
We follow the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/0/code_of_conduct/). By participating, you are expected to uphold this behavior. Please read it before interacting with the community.

---

## Getting Started
1. **Fork the repository** on GitHub.
2. **Clone your fork**:
   ```bash
   git clone https://github.com/<your‑username>/AlphaPIL.git
   cd AlphaPIL
   ```
3. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install --upgrade build twine
   ```
4. **Install development dependencies** (if any are added later, list them here). For now, the core dependencies are managed via `pyproject.toml` and can be installed with:
   ```bash
   pip install -e .
   ```
5. **Run the test suite** (see the section below) to ensure everything works.

---

## Reporting Issues
- **Search first** – check existing issues to avoid duplicates.
- **Open a new issue** with the following template:
  ```markdown
  ### Description
  A clear and concise description of the problem.

  ### Steps to Reproduce
  1. …
  2. …

  ### Expected Behavior
  What you expected to happen.

  ### Environment
  - OS: Ubuntu 22.04 (or your OS)
  - Python: 3.12
  - AlphaPIL version: 0.1.0
  ```
- Attach logs or screenshots when relevant.

---

## Pull Request Process
1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feat/your-feature-name
   ```
2. **Make your changes** and ensure they adhere to the project’s coding style (black, isort, etc.).
3. **Run tests** – see the testing section.
4. **Commit locally** with a clear message:
   ```bash
   git add .
   git commit -m "feat: brief description of your change"
   ```
5. **Push to your fork**:
   ```bash
   git push origin feat/your-feature-name
   ```
6. **Open a Pull Request** on GitHub targeting `MeraLabs/AlphaPIL:main`.
7. **Fill the PR template** (GitHub will provide it automatically).
8. **Address review feedback** – make additional commits to the same branch as needed.

---

## Development Workflow
- **Formatting** – we use `black` and `isort`. Run:
  ```bash
  black .
  isort .
  ```
- **Linting** – use `flake8` (install via `pip install flake8` if required).
- **Pre‑commit hooks** – optionally set up the repository’s [pre‑commit] configuration:
  ```bash
  pip install pre-commit
  pre-commit install
  ```

---

## Running Tests
We use `pytest` for the test suite.
```bash
pip install pytest pytest-asyncio
pytest
```
All tests should pass before you submit a PR.

---

## Documentation
- The main README covers installation and usage.
- Additional docs live in the `docs/` folder.
- When adding new features, update the relevant sections of the document.

---

## Versioning & Releases
We follow **Semantic Versioning (SemVer)**. When you contribute a change that will be part of a release, bump the version in:
- `pyproject.toml` (`version = "0.x.y"`)
- `src/alphapil/__init__.py` (`__version__ = "0.x.y"`)
Create a Git tag after merging to `main`:
```bash
git tag -a v0.x.y -m "Release v0.x.y"
 git push origin v0.x.y
```
The CI pipeline (if set up) will publish the package to PyPI.

---

## License
By contributing, you agree that your contributions will be released under the same license as the project – **MIT License**.

---

## Contact & Support
- **Maintainer**: MeraLabs (meralabs.official@gmail.com)
- **Discord/Slack**: Join the community channel (link in the README) for live help.
- **Issues**: Use the GitHub issue tracker for bugs and feature requests.

---

Thank you for helping make AlphaPIL better! 🎨🚀
