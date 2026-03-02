# ============================================================================
# SNOBOL4python — top-level Makefile
# ============================================================================
# Targets:
#   all            build the C extension in-place (default for dev)
#   build-ext      compile sno4py .so in-place
#   build          build sdist + wheel via python -m build
#   sdist          source distribution only
#   wheel          platform wheel only
#   install        editable install: pip install -e .[test]
#   install-dist   install from latest dist/*.whl
#   test           full test suite (both backends, pytest)
#   test-pure      tests with pure-Python backend only
#   test-c         tests with C backend only
#   test-sno4py    low-level sno4py C extension tests
#   lint           ruff linter
#   typecheck      mypy
#   clean          remove build artefacts, .so, caches
#   distclean      clean + remove dist/
#   docs           build MkDocs documentation
#   docs-serve     live-preview docs at localhost:8000
#   upload-test    upload to TestPyPI
#   upload         upload to PyPI
#   version        print current package version
#   help           print this message
# ============================================================================

PYTHON     := python3
PIP        := $(PYTHON) -m pip
BUILD      := $(PYTHON) -m build
PYTEST     := $(PYTHON) -m pytest
TWINE      := $(PYTHON) -m twine
RUFF       := $(PYTHON) -m ruff
MYPY       := $(PYTHON) -m mypy
MKDOCS     := $(PYTHON) -m mkdocs

SRC_DIR    := src/SNOBOL4python
EXT_SRC    := src/sno4py/src
TEST_DIR   := tests
SNO4PY_DIR := src/sno4py

VERSION    := $(shell $(PYTHON) -c \
    "import tomllib,pathlib; \
     d=tomllib.loads(pathlib.Path('pyproject.toml').read_text()); \
     print(d['project']['version'])")

.PHONY: all build-ext build sdist wheel \
        install install-dist \
        test test-pure test-c test-sno4py \
        lint typecheck \
        clean clean-dist distclean \
        docs docs-serve \
        upload-test upload \
        version help

# ── default ──────────────────────────────────────────────────────────────────
all: build-ext

# ── build C extension in-place (for editable / dev use) ──────────────────────
build-ext:
	@echo "==> Building sno4py C extension in-place"
	$(PYTHON) setup.py build_ext --inplace
	@echo "==> C extension ready"

# ── distribution builds ──────────────────────────────────────────────────────
build: clean-dist
	@echo "==> Building sdist + wheel  (version $(VERSION))"
	$(BUILD)
	@echo "==> Artefacts:"
	@ls -lh dist/

sdist: clean-dist
	$(BUILD) --sdist

wheel: clean-dist
	$(BUILD) --wheel

# ── install targets ──────────────────────────────────────────────────────────
install:
	@echo "==> Editable install (includes test extras)"
	$(PIP) install --break-system-packages -e ".[test]"

install-dist: wheel
	$(eval LATEST_WHL := $(shell ls -t dist/*.whl | head -n 1))
	@echo "==> Installing $(LATEST_WHL)"
	$(PIP) install --break-system-packages "$(LATEST_WHL)"

# ── test targets ─────────────────────────────────────────────────────────────
test: build-ext
	@echo "==> Full test suite (both backends)"
	$(PYTEST) $(TEST_DIR) $(SNO4PY_DIR)/tests -v

test-pure:
	@echo "==> Tests — pure-Python backend only"
	SNOBOL4_BACKEND=pure $(PYTEST) $(TEST_DIR) -v

test-c: build-ext
	@echo "==> Tests — C backend only"
	SNOBOL4_BACKEND=c $(PYTEST) $(TEST_DIR) -v

test-sno4py:
	@echo "==> sno4py low-level C tests"
	$(MAKE) -C $(SNO4PY_DIR) test

# ── code quality ─────────────────────────────────────────────────────────────
lint:
	$(RUFF) check $(SRC_DIR) $(TEST_DIR)

typecheck:
	$(MYPY) $(SRC_DIR) --ignore-missing-imports

# ── docs ─────────────────────────────────────────────────────────────────────
docs:
	$(MKDOCS) build

docs-serve:
	$(MKDOCS) serve

# ── PyPI upload ──────────────────────────────────────────────────────────────
upload-test: build
	@echo "==> Uploading $(VERSION) to TestPyPI"
	$(TWINE) upload --repository testpypi dist/*

upload: build
	@echo "==> Uploading $(VERSION) to PyPI"
	$(TWINE) upload dist/*

# ── clean ────────────────────────────────────────────────────────────────────
clean-dist:
	rm -rf dist/

clean:
	@echo "==> Cleaning build artefacts"
	rm -rf build/ *.egg-info src/*.egg-info src/SNOBOL4python.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.so" -delete
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	$(MAKE) -C $(SNO4PY_DIR) clean

distclean: clean clean-dist
	@echo "==> Full distclean done"

# ── helpers ──────────────────────────────────────────────────────────────────
version:
	@echo "SNOBOL4python $(VERSION)"

help:
	@echo ""
	@echo "SNOBOL4python $(VERSION) — make targets"
	@echo ""
	@echo "  Build"
	@echo "    all            build C extension in-place (default)"
	@echo "    build-ext      compile sno4py .so for dev use"
	@echo "    build          sdist + platform wheel"
	@echo "    sdist          source distribution only"
	@echo "    wheel          platform wheel only"
	@echo ""
	@echo "  Install"
	@echo "    install        pip install -e .[test]  (editable)"
	@echo "    install-dist   install from latest dist/*.whl"
	@echo ""
	@echo "  Test"
	@echo "    test           full suite (both backends)"
	@echo "    test-pure      pure-Python backend only"
	@echo "    test-c         C backend only"
	@echo "    test-sno4py    low-level C extension tests"
	@echo ""
	@echo "  Quality"
	@echo "    lint           ruff"
	@echo "    typecheck      mypy"
	@echo ""
	@echo "  Docs"
	@echo "    docs           build MkDocs site into site/"
	@echo "    docs-serve     live-preview at localhost:8000"
	@echo ""
	@echo "  Publish"
	@echo "    upload-test    push to TestPyPI"
	@echo "    upload         push to PyPI"
	@echo ""
	@echo "  Clean"
	@echo "    clean          build artefacts + .so + caches"
	@echo "    distclean      clean + dist/"
	@echo ""
