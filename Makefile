.PHONY: dependencies install-env requirements quality format lint security typecheck data train test coverage clean

#####################################################
# 1. Dependencies Installation
#####################################################

# Main target for installing dependencies
dependencies: install-env requirements
	@echo "✅ All dependencies installed successfully!"

# Create a virtual environment
install-env:
	@echo "🔄 Creating virtual environment..."
	python3 -m venv venv || { echo "❌ Failed to create virtual environment"; exit 1; }
	@echo "✅ Virtual environment created successfully."

# Install dependencies from requirements.txt using the venv pip
requirements:
	@echo "🔄 Installing dependencies from requirements.txt..."
	./venv/bin/pip install -r requirements.txt || { echo "❌ Dependency installation failed"; exit 1; }
	@echo "✅ Dependencies installed successfully."

#####################################################
# 2. Code Quality Checks
#####################################################

# Main quality target that runs all checks
quality: format lint security typecheck
	@echo "✅ All code quality checks passed!"

# Code formatting using black
format:
	@echo "🔄 Running black for code formatting..."
	./venv/bin/black . || { echo "❌ Black formatting failed"; exit 1; }
	@echo "✅ Black formatting completed successfully."

# PEP8 compliance using flake8 and code quality analysis with pylint
lint:
	@echo "🔄 Running flake8 for PEP8 compliance..."
	./venv/bin/flake8 . || { echo "❌ Flake8 found issues"; exit 1; }
	@echo "✅ Flake8 passed successfully."
	@echo "🔄 Running pylint for code quality analysis..."
	./venv/bin/pylint *.py || { echo "❌ Pylint found issues"; exit 1; }
	@echo "✅ Pylint passed successfully."

# Security vulnerability checks using bandit
security:
	@echo "🔄 Running bandit for security vulnerability checks..."
	./venv/bin/bandit -r . || { echo "❌ Bandit found vulnerabilities"; exit 1; }
	@echo "✅ Bandit passed successfully."

# Type checking using mypy
typecheck:
	@echo "🔄 Running mypy for type checking..."
	./venv/bin/mypy . || { echo "❌ Mypy type checking failed"; exit 1; }
	@echo "✅ Mypy type checking passed successfully."

#####################################################
# 3. Data Preparation
#####################################################

data:
	@echo "🔄 Executing data preparation..."
	python3 main.py --prepare || { echo "❌ Data preparation failed"; exit 1; }
	@echo "✅ Data preparation completed successfully."

#####################################################
# 4. Model Training
#####################################################

train:
	@echo "🔄 Executing model training..."
	python3 main.py --train || { echo "❌ Model training failed"; exit 1; }
	@echo "✅ Model training completed successfully."

#####################################################
# 5. Testing Suite
#####################################################

test:
	@echo "🔄 Running unit tests..."
	./venv/bin/pytest tests/unit || { echo "❌ Unit tests failed"; exit 1; }
	@echo "✅ Unit tests passed successfully."
	@echo "🔄 Running integration tests..."
	./venv/bin/pytest tests/integration || { echo "❌ Integration tests failed"; exit 1; }
	@echo "✅ Integration tests passed successfully."
	@echo "🔄 Running model validation tests..."
	./venv/bin/pytest tests/model_validation || { echo "❌ Model validation tests failed"; exit 1; }
	@echo "✅ Model validation tests passed successfully."

coverage:
	@echo "🔄 Generating test coverage reports..."
	./venv/bin/pytest --maxfail=1 --disable-warnings -q || { echo "❌ Test coverage generation failed"; exit 1; }
	@echo "✅ Test coverage generated successfully."

#####################################################
# Clean Up
#####################################################

clean:
	@echo "🔄 Cleaning up generated artifacts and temporary files..."
	rm -rf venv __pycache__ *.pyc *.joblib confusion_matrix.png roc_curve.png || { echo "❌ Clean up failed"; exit 1; }
	@echo "✅ Clean up completed successfully."
