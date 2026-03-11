#!/bin/bash
# Claude Code Skill Installer — LinkedIn Post Builder
# Paste this in your terminal or Claude Code:
#   bash <(curl -sL https://raw.githubusercontent.com/Aston1690/linkedin-post-skill/main/install.sh)

SKILL_NAME="linkedin-post"
SKILL_DIR="$HOME/.claude/skills/$SKILL_NAME"
REPO_URL="https://github.com/Aston1690/linkedin-post-skill.git"
TEMP_DIR=$(mktemp -d)

echo ""
echo "Installing Claude Code skill: /$SKILL_NAME"
echo "────────────────────────────────────────────"

if [ -d "$SKILL_DIR" ]; then
  echo "Updating existing installation..."
  cd "$TEMP_DIR" && git clone "$REPO_URL" repo 2>/dev/null
  if [ -f "repo/skills/linkedin-post/SKILL.md" ]; then
    rm -rf "$SKILL_DIR"
    mkdir -p "$SKILL_DIR/scripts"
    cp repo/skills/linkedin-post/SKILL.md "$SKILL_DIR/SKILL.md"
    cp repo/skills/linkedin-post/scripts/flux_image.py "$SKILL_DIR/scripts/flux_image.py" 2>/dev/null
  fi
else
  echo "Installing to $SKILL_DIR..."
  mkdir -p "$SKILL_DIR/scripts"
  cd "$TEMP_DIR" && git clone "$REPO_URL" repo 2>/dev/null
  if [ -f "repo/skills/linkedin-post/SKILL.md" ]; then
    cp repo/skills/linkedin-post/SKILL.md "$SKILL_DIR/SKILL.md"
    cp repo/skills/linkedin-post/scripts/flux_image.py "$SKILL_DIR/scripts/flux_image.py" 2>/dev/null
  fi
fi

rm -rf "$TEMP_DIR"

if [ -f "$SKILL_DIR/SKILL.md" ]; then
  echo ""
  echo "Installed! Restart Claude Code and type /linkedin-post to use it."
  echo ""
else
  echo ""
  echo "ERROR: Installation failed. Try manually:"
  echo "  git clone $REPO_URL /tmp/linkedin-post-skill"
  echo "  mkdir -p $SKILL_DIR/scripts"
  echo "  cp /tmp/linkedin-post-skill/skills/linkedin-post/SKILL.md $SKILL_DIR/SKILL.md"
  echo "  cp /tmp/linkedin-post-skill/skills/linkedin-post/scripts/flux_image.py $SKILL_DIR/scripts/"
  echo ""
  exit 1
fi
