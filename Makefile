PYTHON = python3
SCRIPT = a_maze_ing.py
CONFIG = config.txt
PIP = pip
PACKAGE_MANAGER = pip


## install: Install activity dependencies
## run: Run the maze generator and save output to maze.txt
run:
	$(PYTHON) $(SCRIPT) $(CONFIG)

install:
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

## lint: Run linting with mandatory flags and strict checking
lint:
	@echo "Running linter..."
	flake8
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8
	mypy . --strict --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
## clean: Remove temporary files and build artifacts
clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache amazeing/__pycache__

debug:
	$(PYTHON) -m pdb $(SCRIPT) $(CONFIG)


.PHONY: install lint clean help