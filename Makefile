.PHONY: lint
lint:
    flake8
    isort -qc .
