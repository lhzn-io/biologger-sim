# Contributing to Biologger Sim

Thank you for your interest in contributing to the Biologger Sim project! This document outlines the standards and workflows for contributing code to this repository.

## Development Environment

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd biologger-sim
   ```

2. **Set up the Micromamba environment**:

   ```bash
   micromamba env create -f environment.yml
   micromamba activate biologger-sim
   ```

3. **Install the package in editable mode**:

   ```bash
   pip install -e .
   ```

4. **Install Pre-commit Hooks**:

   We use `pre-commit` to enforce code quality standards automatically:

   ```bash
   pre-commit install
   ```

   This runs code quality checks (linting, formatting, type checking, secrets) before each commit (~5-10 seconds).

## Code Quality Standards

We use a strict set of tools to maintain code quality. These are run automatically via pre-commit hooks, but you can also run them manually.

### Linting & Formatting (Ruff)

We use [Ruff](https://docs.astral.sh/ruff/) for both linting and formatting.

- **Linting**: Checks for bugs, style issues, and best practices.
- **Formatting**: Enforces a consistent code style (similar to Black).

To run manually:

```bash
ruff check .
ruff format .
```

### Type Checking (Mypy)

We use [Mypy](https://mypy-lang.org/) for static type checking.

- Currently configured with `ignore_errors = true` to allow for gradual adoption, but new code should strive to be type-safe.

To run manually:

```bash
mypy .
```

### Secret Scanning (Detect-secrets)

We use `detect-secrets` to prevent accidental commit of credentials.

- If you encounter a false positive, you can update the baseline:

  ```bash
  detect-secrets scan > .secrets.baseline
  ```

## Testing

We use `pytest` for testing. Tests run automatically in CI, but run them locally before pushing:

### Automatic Testing (CI)

- **GitHub Actions**: Runs on all PRs and pushes
  - Unit tests on PRs: `pytest -m "not slow and not integration"`
  - All tests except integration on main: `pytest -m "not integration"`
  - Integration tests excluded (require large uncommitted CSV files)

### Manual Testing

```bash
# Fast unit tests (recommended for local development)
make test-fast
pytest tests/ -v -m "not slow and not integration"

# All tests including slow ones (but not integration)
pytest tests/ -v -m "not integration"

# Full suite including integration tests (requires data files)
make test
pytest tests/ -v
```

### Test Markers

Our test suite uses pytest markers for organization:

- `@pytest.mark.unit` - Fast unit tests (always run)
- `@pytest.mark.slow` - Slow tests (excluded from pre-push, run in CI)
- `@pytest.mark.integration` - Integration tests requiring large data files (excluded from CI)
- `@pytest.mark.streaming` - Streaming component tests
- `@pytest.mark.regression` - Regression tests for critical bug fixes

### Integration Tests

Integration tests require large CSV files not committed to the repository. To run them locally:

1. Ensure you have the full dataset files in `data/test/`
2. Run: `pytest tests/integration/ -v`

These tests validate against R outputs and test full pipeline workflows.

## Pull Request Workflow

1. Create a new branch for your feature or fix.
2. Make your changes.
3. Run tests locally: `make test-fast` (recommended before pushing).
4. Commit your changes. Pre-commit hooks will run automatically (linting, formatting, type checking).
   - If hooks fail or make changes, they will modify the files. Stage the changes (`git add .`) and commit again.
   - To bypass hooks (not recommended): `git commit --no-verify`
5. Push your branch and open a Pull Request on GitHub.
6. CI will automatically run all checks (pre-commit hooks + tests).
7. Address any CI failures before requesting review.

## Continuous Integration

All pull requests and pushes to main trigger automated CI checks via GitHub Actions ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)):

**On all PRs and pushes:**

- Pre-commit checks (ruff, mypy, detect-secrets)
- Unit tests: `pytest -m "not slow and not integration"`

**On pushes to main branch:**

- All tests except integration: `pytest -m "not integration"`

**Note:** Integration tests are excluded from CI because they require large CSV files not committed to the repository. Run them locally if you modify integration test code.

## Release Process

See [RELEASE_GUIDELINES.md](RELEASE_GUIDELINES.md) for details on the versioning and release process.
