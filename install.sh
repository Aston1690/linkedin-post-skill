#!/bin/bash
# Claude Code Skill Installer — LinkedIn Post Builder
# Paste this in your terminal:
#   bash <(curl -sL https://raw.githubusercontent.com/Aston1690/linkedin-post-skill/main/install.sh)

SKILL_NAME="linkedin-post"
SKILL_DIR="$HOME/.claude/skills/$SKILL_NAME"
REPO_URL="https://github.com/Aston1690/linkedin-post-skill.git"
TEMP_DIR=$(mktemp -d)

echo ""
echo "Installing Claude Code skill: /$SKILL_NAME"
echo "────────────────────────────────────────────"

# Check for Python 3
if ! command -v python3 &>/dev/null; then
  echo "WARNING: Python 3 not found. Install Python 3 before using this skill."
  echo "  https://www.python.org/downloads/"
fi

# Check for required Python packages
python3 -c "import requests" 2>/dev/null || echo "WARNING: 'requests' package not found. Install with: pip3 install requests"
python3 -c "from PIL import Image" 2>/dev/null || echo "WARNING: 'Pillow' package not found. Install with: pip3 install Pillow"

install_skill() {
  echo "Installing to $SKILL_DIR..."
  mkdir -p "$SKILL_DIR/scripts" "$SKILL_DIR/references"

  cd "$TEMP_DIR" && git clone "$REPO_URL" repo 2>/dev/null

  if [ -f "repo/skills/linkedin-post/SKILL.md" ]; then
    # Copy core skill file
    cp repo/skills/linkedin-post/SKILL.md "$SKILL_DIR/SKILL.md"

    # Copy Python scripts
    cp repo/skills/linkedin-post/scripts/*.py "$SKILL_DIR/scripts/" 2>/dev/null

    # Copy reference directories (structure + any images)
    cp -r repo/skills/linkedin-post/references/* "$SKILL_DIR/references/" 2>/dev/null
  fi
}

if [ -d "$SKILL_DIR" ]; then
  echo "Updating existing installation..."
  rm -rf "$SKILL_DIR"
fi

install_skill

rm -rf "$TEMP_DIR"

if [ -f "$SKILL_DIR/SKILL.md" ]; then
  echo ""
  echo "Installed! Restart Claude Code and type /linkedin-post to use it."
  echo ""
  echo "Required API keys (set as environment variables):"
  echo "  SEADREAM_API_KEY  — OpenRouter API key (for Nano Banana 2 + Seedream 4.5)"
  echo "  FLUX_API_KEY      — BFL or OpenRouter key (for Flux 2 Pro, optional)"
  echo ""
  echo "Required Python packages:"
  echo "  pip3 install requests Pillow"
  echo ""
else
  echo ""
  echo "ERROR: Installation failed. Try manually:"
  echo "  git clone $REPO_URL /tmp/linkedin-post-skill"
  echo "  mkdir -p $SKILL_DIR/{scripts,references}"
  echo "  cp -r /tmp/linkedin-post-skill/skills/linkedin-post/* $SKILL_DIR/"
  echo ""
  exit 1
fi
