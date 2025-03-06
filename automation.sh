#!/bin/bash

# Colors for better output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to display a header
function display_header() {
    echo -e "${BLUE}"
    echo "==========================================="
    echo "      Git & PyPI Auto-Update Script        "
    echo "==========================================="
    echo -e "${NC}"
}

# Get the current Git branch
function get_current_branch() {
    git rev-parse --abbrev-ref HEAD
}

# Sync with GitHub
function sync_with_github() {
    BRANCH=$(get_current_branch)
    echo -e "${YELLOW}🔄 Syncing with GitHub (Branch: $BRANCH)...${NC}"
    git pull origin "$BRANCH"
}

# Update version in pyproject.toml or setup.py
function update_version() {
    local NEW_VERSION=$1
    FILES=("pyproject.toml" "setup.py")

    for FILE in "${FILES[@]}"; do
        if [ -f "$FILE" ]; then
            if [[ "$FILE" == "pyproject.toml" ]]; then
                sed -i "s/version = \".*\"/version = \"$NEW_VERSION\"/" "$FILE"
            elif [[ "$FILE" == "setup.py" ]]; then
                sed -i "s/version=['\"].*['\"];/version='$NEW_VERSION'/" "$FILE"
            fi
            echo -e "${GREEN}✅ Updated $FILE to version $NEW_VERSION.${NC}"
        fi
    done
}

# Commit and push changes
function commit_and_push_changes() {
    local NEW_VERSION=$1
    BRANCH=$(get_current_branch)

    git add .
    git commit -m "Release version $NEW_VERSION"
    git push origin "$BRANCH"

    echo -e "${GREEN}✅ Changes pushed to GitHub.${NC}"
}

# Build and upload package to PyPI
function build_and_upload_to_pypi() {
    echo -e "${YELLOW}📦 Cleaning up previous builds...${NC}"
    rm -rf dist/ build/ *.egg-info

    echo -e "${BLUE}🚀 Building package...${NC}"
    python -m build

    echo -e "${YELLOW}📤 Uploading package to PyPI...${NC}"
    twine upload dist/*

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Successfully uploaded to PyPI!${NC}"
    else
        echo -e "${RED}❌ Upload failed. Please check your credentials and try again.${NC}"
        exit 1
    fi
}

# Main function
function automate_update() {
    display_header

    # Check if version argument is provided
    if [ -z "$1" ]; then
        echo -e "${RED}❌ Error: Please provide the new version as an argument.${NC}"
        echo "Usage: ./script.sh <new_version>"
        exit 1
    fi

    NEW_VERSION=$1

    sync_with_github
    update_version "$NEW_VERSION"
    commit_and_push_changes "$NEW_VERSION"
    build_and_upload_to_pypi
}

# Run the script with the provided version number
automate_update "$1"

echo -e "${BLUE}==========================================="
echo -e "        Script Execution Complete          "
echo -e "===========================================${NC}"
