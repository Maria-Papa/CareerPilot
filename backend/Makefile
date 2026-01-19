.PHONY: install install-dev test test-unit test-integration lint format typecheck security coverage coverage-html clean pre-commit pre-commit-install check-all

# -------------------------
# Installation
# -------------------------

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# -------------------------
# Testing
# -------------------------

test: test-unit test-integration

test-unit:
	PYTHONPATH=. pytest -m "not integration" tests -q --disable-warnings

test-integration:
	PYTHONPATH=. pytest -m integration tests -q --disable-warnings --tb=short

coverage:
	PYTHONPATH=. pytest --cov=app --cov-report=term-missing --disable-warnings --cov-fail-under=90

coverage-html:
	PYTHONPATH=. pytest --cov=app --cov-report=html --disable-warnings --cov-fail-under=90

# -------------------------
# Code Quality
# -------------------------

lint:
	black --check .
	ruff check .

format:
	black .
	ruff check --select I --fix .

typecheck:
	mypy app

security:
	bandit -r app
	pip-audit

# -------------------------
# Pre-commit
# -------------------------

pre-commit-install:
	pre-commit install

pre-commit:
	pre-commit run --all-files

# -------------------------
# Utility
# -------------------------

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf htmlcov .coverage

# -------------------------
# Meta target
# -------------------------

check-all: lint typecheck security test pre-commit
