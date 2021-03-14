
# PACKAGE := {{cookiecutter.package_name}}
PACKAGE := src/app
TEST_PACKAGE := tests
MODULES := $(wildcard $(PACKAGE)/*.py)

.DEFAULT_GOAL := help

#################################################
### Virtual Environment for Local Development
#################################################

# flag to skip use of venv and install from requirments.txt
SKIP_VENV ?= 0

# directory of the venv to create
VIRTUAL_ENV ?= .venv

ifeq ($(SKIP_VENV),0)
# pre-command to activate venv when venv is used
PY3_VENV=. $(VIRTUAL_ENV)/bin/activate;
endif

# enable skip rerun of this step if no change to depenencies
$(VIRTUAL_ENV)/touchfile: requirements.txt requirements-dev.txt
ifeq ($(SKIP_VENV),0)
	test -d $(VIRTUAL_ENV) || python3 -m venv $(VIRTUAL_ENV)
	. $(VIRTUAL_ENV)/bin/activate; pip install -Ur requirements.txt
	. $(VIRTUAL_ENV)/bin/activate; pip install -Ur requirements-dev.txt
endif
	touch $(VIRTUAL_ENV)/touchfile

.PHONY: install
install: $(VIRTUAL_ENV)/touchfile ## Create virtual env if needed, and install dependencies

.PHONY: install-hooks
install-hooks: install ## Install any pre-commit git hooks
	$(PY3_VENV) pre-commit install
	$(PY3_VENV) pre-commit run --all-files

#################################################
### Main Tasks
#################################################

.PHONY: all
all: install

.PHONY: ci
ci: check test ## Run all tasks that determine CI status

.PHONY: watch
watch: install ## Continuously run all CI tasks when files chanage
  # TODO: add implementation

#################################################
### Code Style and Static Code Analysis
#################################################

format: install ## Format python codes
	@ echo "+ $@"
	$(PY3_VENV) isort $(PACKAGE) $(TEST_PACKAGE)
	$(PY3_VENV) black $(PACKAGE) $(TEST_PACKAGE)
	@ echo

lint: install ## Check code style with flake8
	@echo "+ $@"
	-$(PY3_VENV) flake8 $(PACKAGE) $(TEST_PACKAGE)

check: install format lint ## Run formaters, linters, and static analysis
	@echo "+ $@"
	-$(PY3_VENV) mypy $(PACKAGE) $(TEST_PACKAGE)

#################################################
### Tests
#################################################

test: install ## Run unit tests locally
	@echo "+ $@"
	$(PY3_VENV) PYTHONPATH=./src pytest

test-container: ## Run unit tests in container
	# build arg (NOCACHE) is always set to a random value to
	# invalidate docker cache to ensure test are rerun
	docker-compose -f docker-compose.test.yaml build --build-arg NOCACHE=$$(/bin/bash -c 'echo $$RANDOM')

#################################################
### Build and OCI Container
#################################################

build: ## Build into a OCI container image
	docker-compose build

run: ## Run the app as a container locally using docker-compose
	docker-compose up -d

#################################################
### Clean up
#################################################

clean-local: ## Clean up local dev environment and virtual env
	rm -rf $(VIRTUAL_ENV)
	find -iname "*.pyc" -delete

clean-container: ## Clean up and remove any existing app containers
	docker-compose down

#################################################
### Dependencies Update
#################################################

update: install ## Update requirements.txt based on imports in src directory
	@echo "+ $@ requirements.txt"
	$(PY3_VENV) pipreqs --force --savepath requirements.txt src/app

#################################################
### Build and OCI Container
#################################################

# HELP ######################################################################

.PHONY: help
# Leverge on comment prefix with '##' next to make command as their help text
help: ## Help command
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
