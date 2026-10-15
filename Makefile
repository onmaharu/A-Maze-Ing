NAME_VENV = venv_test
PYTHON_VENV = $(NAME_VENV)/bin/python3
PIP_VENV = $(NAME_VENV)/bin/pip
MYPY_VENV = $(NAME_VENV)/bin/mypy
MYPY_VENV_STRICT = $(NAME_VENV)/bin/mypy --strict
FLAKE8_VENV = $(NAME_VENV)/bin/flake8
VERIFY = $(NAME_VENV)/.verify

all: run

$(VERIFY):
	python3 -m venv $(NAME_VENV)
	$(PIP_VENV) install --upgrade pip
	$(PIP_VENV) install flake8 mypy
	$(PIP_VENV) install pyfiglet
	$(PIP_VENV) install poetry
	touch $(VERIFY)

install: $(VERIFY)

run: $(VERIFY)
	$(PYTHON_VENV) a_maze_ing.py config.txt

debug: $(VERIFY)
	$(PYTHON_VENV) -m pdb a_maze_ing.py config.txt

clean:
		find . -type d -name "__pycache__" -exec rm -rf {} +
		rm -rf .mypy_cache
		rm -rf $(NAME_VENV)


lint: $(VERIFY)
	$(FLAKE8_VENV) .
	$(MYPY_VENV) . --warn-return-any \
			--warn-unused-ignores \
			--ignore-missing-imports \
			--disallow-untyped-defs \
			--check-untyped-defs

lint-strict: $(VERIFY)
	$(FLAKE8_VENV) .
	$(MYPY_VENV_STRICT) .

re: clean install run

.PHONY:
	all clean install run debug re lint lint-strict
