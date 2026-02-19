#!/bin/bash

############################################################################
# Validate the cookbook using ruff
# Usage: ./scripts/validate.sh
############################################################################

CURR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "${CURR_DIR}")"
COOKBOOK_DIR="${REPO_ROOT}/cookbook"
source "${CURR_DIR}/_utils.sh"

print_heading "Validating cookbook"

print_heading "Running: ruff check ${COOKBOOK_DIR}"
ruff check "${COOKBOOK_DIR}"
