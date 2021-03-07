default:

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -path '*/__pycache__/*' -delete
	find . -type d -empty -delete

install:
	${PYTHON_ALIAS} -m pip install -e ".[options]" && rm -r i_choose_you.egg-info

install-dev:
	${PYTHON_ALIAS} -m pip install -e ".[dev]"


.PHONY: default clean install install-dev

test:
	${PYTHON_ALIAS} -m pytest

test-quality: flake8 isort

test-all: test-quality test

.PHONY: test test-quality test-all

flake8:
	${PYTHON_ALIAS} -m flake8 .

isort:
	${PYTHON_ALIAS} -m isort --check --diff .

isort-fix:
	${PYTHON_ALIAS} -m isort .

.PHONY: flake8 isort isort-fix
