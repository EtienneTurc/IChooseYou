default:

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -path '*/__pycache__/*' -delete
	find . -type d -empty -delete
	find . -type f -name '*.html' -delete
	find . -type f -name '*.c' -delete
	rm -rf build
	rm -rf htmlcov
	rm *.so

install:
	${PYTHON_ALIAS} -m pip install -e ".[options]" && rm -r i_choose_you.egg-info

install-dev:
	${PYTHON_ALIAS} -m pip install -e ".[dev]"

BUILD_CYTHON=${PYTHON_ALIAS} cython_build.py build_ext --inplace --force
build:
	$(BUILD_CYTHON)

run:
	${PYTHON_ALIAS} -m flask run --host=0.0.0.0

run-debug:
	FLASK_DEBUG=1 ${PYTHON_ALIAS} -m flask run --host=0.0.0.0

.PHONY: default clean install install-dev build run

test:
	${PYTHON_ALIAS} -m pytest

test-cov:
	${PYTHON_ALIAS} -m pytest --cov=server/ --cov-report term-missing --cov-report html

test-quality: flake8 isort

test-all: test-quality build test

build-dev:
	BUILD_HTML_FILE=True $(BUILD_CYTHON)

.PHONY: test test-cov test-quality test-all build-dev

flake8:
	${PYTHON_ALIAS} -m flake8 .

isort:
	${PYTHON_ALIAS} -m isort --check --diff .

isort-fix:
	${PYTHON_ALIAS} -m isort .

.PHONY: flake8 isort isort-fix
