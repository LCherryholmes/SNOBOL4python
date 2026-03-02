# Contributing to SNOBOL4python

## Development setup

```bash
git clone https://github.com/LCherryholmes/SNOBOL4python
cd SNOBOL4python
make install          # editable install + test deps
make all              # build C extension in-place
make test             # run full test suite
```

## Running tests

```bash
make test             # both backends
make test-pure        # pure-Python only (no C compiler needed)
make test-c           # C backend only
```

## Code style

```bash
make lint             # ruff
make typecheck        # mypy
```

## Releasing a new version

1. Update `version` in `pyproject.toml` **and** `setup.py` and `src/SNOBOL4python/__init__.py`
2. Add a section to `CHANGELOG.md`
3. Commit: `git commit -am "Release v0.X.Y"`
4. Tag:    `git tag v0.X.Y && git push --tags`

The `wheels.yml` GitHub Action fires automatically on the tag push,
builds wheels for Linux / macOS / Windows across Python 3.10–3.12,
and publishes everything to PyPI via OIDC Trusted Publisher.

## Project layout

```
src/
  SNOBOL4python/     Python package (patterns, backend selector, functions)
  sno4py/
    src/             C sources (spipat.c, sno4py.c, …)
    tests/           Low-level C extension tests
tests/               Python-level test suite
.github/workflows/
  ci.yml             Test matrix on every push/PR
  wheels.yml         Build + publish on version tag
  docs.yml           Deploy MkDocs to GitHub Pages
```
