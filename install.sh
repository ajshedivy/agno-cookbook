#!/usr/bin/env bash
#
# Install Agno Claude Code Skills
#
# Usage:
#   ./install.sh            # Install to project-local .claude/skills/
#   ./install.sh --global   # Install to global ~/.claude/skills/
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$SCRIPT_DIR/config/skills"

# Determine target directory
if [[ "${1:-}" == "--global" ]]; then
    TARGET_DIR="$HOME/.claude/skills"
    echo "Installing skills globally to $TARGET_DIR"
else
    TARGET_DIR=".claude/skills"
    echo "Installing skills locally to $TARGET_DIR"
fi

# Check source exists
if [[ ! -d "$SKILLS_SRC" ]]; then
    echo "Error: Skills source directory not found at $SKILLS_SRC"
    exit 1
fi

# Create target directory
mkdir -p "$TARGET_DIR"

# Copy each skill
SKILLS=(agno-agent agno-team agno-workflow agno-tools agno-agentos agno-test)
for skill in "${SKILLS[@]}"; do
    if [[ -d "$SKILLS_SRC/$skill" ]]; then
        echo "  Installing $skill..."
        rm -rf "$TARGET_DIR/$skill"
        cp -r "$SKILLS_SRC/$skill" "$TARGET_DIR/$skill"
    fi
done

echo ""
echo "Installed ${#SKILLS[@]} skills:"
for skill in "${SKILLS[@]}"; do
    echo "  - $skill"
done
echo ""
echo "Done! Skills are ready to use."
