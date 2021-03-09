#!make
# Makefile for lazy people
SHELL      := /bin/bash
CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

ENV = $(VIRTUAL_ENV)
version = 3

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

# virtualenv executables
PYTHON := python3
PIP := pip
FLAKE8 := flake8
PYTEST := py.test
PYLINT := pylint

# Remove if you don't want pip to cache downloads
PIP_CACHE_DIR := .cache
PIP_CACHE := --download-cache $(PIP_CACHE_DIR)

all: .installed.cfg

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: clean
clean: ## Cleanning
	@find . \( -type f -a -name '*.pyc' -o -name '*.pyo' -o -name '*~' -o -type d -a -iname '__pycache__' -o -type d -a -iname 'amcham.restapi.egg-info' -o -type d -a -iname 'htmlcov' \) -exec rm -rf '{}' +

.PHONY: Build Docs
docs:  ## Build Docs
	bin/sphinxbuilder
