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

# Check for Node.js
if ! command -v node &>/dev/null; then
  echo "WARNING: Node.js not found. Install Node.js v18+ before using this skill."
  echo "  https://nodejs.org"
fi

install_skill() {
  echo "Installing to $SKILL_DIR..."
  mkdir -p "$SKILL_DIR/scripts" "$SKILL_DIR/templates" "$SKILL_DIR/references"

  cd "$TEMP_DIR" && git clone "$REPO_URL" repo 2>/dev/null

  if [ -f "repo/skills/linkedin-post/SKILL.md" ]; then
    # Copy core files
    cp repo/skills/linkedin-post/SKILL.md "$SKILL_DIR/SKILL.md"

    # Copy scripts
    cp repo/skills/linkedin-post/scripts/generate_image.js "$SKILL_DIR/scripts/" 2>/dev/null
    cp repo/skills/linkedin-post/scripts/fetch_image.js "$SKILL_DIR/scripts/" 2>/dev/null
    cp repo/skills/linkedin-post/scripts/package.json "$SKILL_DIR/scripts/" 2>/dev/null

    # Copy templates
    cp repo/skills/linkedin-post/templates/*.html "$SKILL_DIR/templates/" 2>/dev/null
    cp repo/skills/linkedin-post/templates/*.css "$SKILL_DIR/templates/" 2>/dev/null

    # Copy reference directories (structure + any images)
    cp -r repo/skills/linkedin-post/references/* "$SKILL_DIR/references/" 2>/dev/null

    # Install npm dependencies (Puppeteer)
    echo "Installing Puppeteer..."
    cd "$SKILL_DIR/scripts" && npm install 2>/dev/null
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
  echo "Required API keys (set at least one for stock photos):"
  echo "  UNSPLASH_ACCESS_KEY — https://unsplash.com/developers"
  echo "  PEXELS_API_KEY      — https://www.pexels.com/api/"
  echo "  PIXABAY_API_KEY     — https://pixabay.com/api/docs/"
  echo ""
else
  echo ""
  echo "ERROR: Installation failed. Try manually:"
  echo "  git clone $REPO_URL /tmp/linkedin-post-skill"
  echo "  mkdir -p $SKILL_DIR/{scripts,templates,references}"
  echo "  cp -r /tmp/linkedin-post-skill/skills/linkedin-post/* $SKILL_DIR/"
  echo "  cd $SKILL_DIR/scripts && npm install"
  echo ""
  exit 1
fi
