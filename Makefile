PYTHON = python3
PIP = $(PYTHON) -m pip
BUILD = $(PYTHON) -m build

.PHONY: all build test install install_dist clean

all: build

build:
	$(BUILD)

test:
	$(PYTHON) -m pytest tests/

install:
	$(PIP) install -e .

install_dist: build
	$(eval LATEST_WHL := $(shell ls -t dist/*.whl | head -n 1))
	$(PIP) install $(LATEST_WHL)

clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.so" -delete