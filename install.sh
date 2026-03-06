#!/usr/bin/env bash
#
# Install Agno Claude Code Skills
#
# Preferred method (Claude Code plugin marketplace):
#   /plugin marketplace add ajshedivy/agno-cookbook
#   /plugin install agno-framework@agno-skills
#   /plugin install agno-agentos-api@agno-skills
#
# Manual fallback (this script):
#   ./install.sh            # Install to project-local .claude/skills/
#   ./install.sh --global   # Install to global ~/.claude/skills/
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Determine target directory
if [[ "${1:-}" == "--global" ]]; then
    TARGET_DIR="$HOME/.claude/skills"
    echo "Installing skills globally to $TARGET_DIR"
else
    TARGET_DIR=".claude/skills"
    echo "Installing skills locally to $TARGET_DIR"
fi

mkdir -p "$TARGET_DIR"

TOTAL=0

# Install framework skills
FRAMEWORK_SRC="$SCRIPT_DIR/plugins/agno-framework/skills"
if [[ -d "$FRAMEWORK_SRC" ]]; then
    for skill_dir in "$FRAMEWORK_SRC"/*/; do
        skill=$(basename "$skill_dir")
        echo "  Installing $skill..."
        rm -rf "$TARGET_DIR/$skill"
        cp -r "$skill_dir" "$TARGET_DIR/$skill"
        TOTAL=$((TOTAL + 1))
    done
fi

# Install API skills
API_SRC="$SCRIPT_DIR/plugins/agno-agentos-api/skills"
if [[ -d "$API_SRC" ]]; then
    for skill_dir in "$API_SRC"/*/; do
        skill=$(basename "$skill_dir")
        echo "  Installing $skill..."
        rm -rf "$TARGET_DIR/$skill"
        cp -r "$skill_dir" "$TARGET_DIR/$skill"
        TOTAL=$((TOTAL + 1))
    done
fi

echo ""
echo "Installed $TOTAL skills."
echo ""
echo "Tip: For automatic updates, use the plugin marketplace instead:"
echo "  /plugin marketplace add ajshedivy/agno-cookbook"
echo "  /plugin install agno-framework@agno-skills"
echo "  /plugin install agno-agentos-api@agno-skills"
