#!/bin/bash

############################################################################
# Agno Cookbook Setup
# Usage: ./scripts/setup.sh
############################################################################

CURR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "${CURR_DIR}")"
source "${CURR_DIR}/_utils.sh"

print_heading "Agno Cookbook Setup"

print_heading "Installing dependencies with uv"
uv sync --extra quickstart

# Copy .env.example if .env doesn't exist
if [ ! -f "${REPO_ROOT}/.env" ]; then
  print_heading "Creating .env from .env.example"
  cp "${REPO_ROOT}/.env.example" "${REPO_ROOT}/.env"
  print_info "Edit .env to configure your model and API keys"
else
  print_info ".env already exists — skipping"
fi

print_heading "Setup complete!"
print_info "1. Edit .env with your API keys and preferred model"
print_info "2. Install your provider SDK: uv sync --extra anthropic"
print_info "3. Run: uv run python cookbook/00_quickstart/agent_with_tools.py"
