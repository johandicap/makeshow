#####################
# Makeshow Makefile #
#####################

# Define Python files and folders to analyze
PYTHON_FILES_AND_FOLDERS = \
	makeshow.py \
	utils \
	test

# Set Makefile shell to bash in order to print colored headers
SHELL := /bin/bash

# Function to print a colored header
COL=\033[1;35m
NC=\033[0m
define header
    @echo -e "${COL}$1${NC}"
endef

isort_check:
	$(call header,"[make isort_check]")
	@isort --settings-path ./pyproject.toml --diff --color --check-only $(PYTHON_FILES_AND_FOLDERS)

isort_fix:
	$(call header,"[make isort_fix]")
	@isort --settings-path ./pyproject.toml $(PYTHON_FILES_AND_FOLDERS)

black_check:
	$(call header,"[make black_check]")
	@black --config ./pyproject.toml --diff --color $(PYTHON_FILES_AND_FOLDERS)

black_fix:
	$(call header,"[make black_fix]")
	@black --config ./pyproject.toml $(PYTHON_FILES_AND_FOLDERS)

ruff_check:
	$(call header,"[make ruff_check]")
	@ruff check --config ./pyproject.toml --show-source $(PYTHON_FILES_AND_FOLDERS)

ruff_fix:
	$(call header,"[make ruff_fix]")
	@ruff check --config ./pyproject.toml --fix $(PYTHON_FILES_AND_FOLDERS)

mypy:
	$(call header,"[make mypy]")
	@python3 -m mypy --config-file ./mypy.ini $(PYTHON_FILES_AND_FOLDERS)

test:
	$(call header,"[make test]")
	@python3 -m pytest --verbose --color=auto .

fix: isort_fix black_fix ruff_fix

ci_no_test: isort_check black_check ruff_check mypy

ci: ci_no_test test

# List phony targets, i.e. targets that are not the name of a file
# See https://www.gnu.org/software/make/manual/html_node/Phony-Targets.html
.PHONY: isort_check isort_fix black_check black_fix ruff_check ruff_fix mypy test fix ci_no_test ci
