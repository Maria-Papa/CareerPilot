.PHONY: install install-dev test test-unit test-integration lint

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test: test-unit test-integration

test-unit:
	PYTHONPATH=. pytest -m "not integration" tests -q --disable-warnings

test-integration:
	PYTHONPATH=. pytest -m integration tests -q --disable-warnings --tb=short

lint:
	black --check .
	flake8 .
