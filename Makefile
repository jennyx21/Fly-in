VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

MAIN = src/main.py


install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt


run:
	$(PYTHON) $(MAIN)


debug:
	$(PYTHON) -m pdb $(MAIN)


clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf .mypy_cache
	rm -rf src/.mypy_cache


lint:
	flake8 . --exclude .venv
	mypy . --exclude $(VENV)\
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs


lint-strict:
	flake8 . --exclude .venv
	mypy . --strict