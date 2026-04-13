.PHONY: help install_django18 test test_with_coverage build_with_django_18 build_with_django_111

# Default target
help:
	@echo "Available commands:"
	@echo "  make install_django18   - Install Test dependencies for django 1.8"
	@echo "  make test      - Run all test cases"
	@echo "  make test_with_coverage - Run tests with coverage report"
	@echo "  make build_with_django_18 - Build and run docker image with django 1.8"
	@echo "  make build_with_django_111 - Build and run docker image with django 1.11"

# Install dependencies
install_django18:
	@echo "Installing test dependencies for django 1.8 ..."
	pip install -r requirements/django18/test.txt

# Run tests
test:
	@echo "Running tests..."
	python -m pytest -vv

# Run tests with coverage
test_with_coverage:
	@echo "Running tests with coverage..."
	python -m pytest --cov=cropimg --cov-report=term-missing

# Start build with django version 1.8 and start container
build_with_django_18:
	@echo "Starting Docker build..."
	docker build -t cropimg-django18 --build-arg REQUIREMENTS_FILE=requirements/django18/test.txt .
	docker run -it --rm cropimg-django18

# Start build with django version 1.11 and start container
build_with_django_111:
	@echo "Starting Docker build..."
	docker build -t cropimg-django111 --build-arg REQUIREMENTS_FILE=requirements/django111/test.txt .
	docker run -it --rm cropimg-django111
