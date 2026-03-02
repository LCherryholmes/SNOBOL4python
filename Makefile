.PHONY: all clean build install test publish

all: clean build install test

clean:
	rm -rf dist/ build/ *.egg-info src/*.egg-info

build:
	python3 -m pip install --upgrade pip build pytest twine
	python3 -m build

install:
	python3 -m pip install dist/*.whl --force-reinstall

test:
	python3 -m pytest tests/

publish: clean build test
	python3 -m twine upload dist/*