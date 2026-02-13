.PHONY: help install test lint run clean docker-build

help:
	@echo "CSE Stock Analyzer Makefile"
	@echo "---------------------------"
	@echo "make install      Install dependencies"
	@echo "make test         Run tests with coverage"
	@echo "make lint         Run linting checks"
	@echo "make run          Run CLI application"
	@echo "make run-gui      Run GUI application"
	@echo "make clean        Clean up build artifacts"
	@echo "make docker-build Build Docker image"

install:
	pip install -e .[dev]

test:
	pytest

lint:
	flake8 src tests
	black --check src tests
	isort --check-only src tests
	mypy src

run:
	python main.py

run-gui:
	python main_gui.py

clean:
	rm -rf __pycache__ .pytest_cache .coverage htmlcov dist build *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +

docker-build:
	docker build -t cse-stock-analyzer .
