#!/bin/bash

# Check if a version argument is provided
if [ -z "$1" ]; then
    echo "Usage: ./update_pypi.sh <new_version>"
    exit 1
fi

NEW_VERSION="$1"

# Project settings
PROJECT_NAME="your_project"  # Replace with your actual project name on PyPI
VERSION_FILE_SETUP="setup.py"
VERSION_FILE_TOML="pyproject.toml"
DIST_DIR="dist"

echo "[✔] Updating version to: $NEW_VERSION"

# Update `setup.py`
sed -i "s/version=\"[^\"]*\"/version=\"$NEW_VERSION\"/" "$VERSION_FILE_SETUP"

# Update `pyproject.toml` if it exists
if [ -f "$VERSION_FILE_TOML" ]; then
    sed -i "s/version = \"[^\"]*\"/version = \"$NEW_VERSION\"/" "$VERSION_FILE_TOML"
fi

# Clean previous builds
rm -rf "$DIST_DIR"

# Build the package
echo "[✔] Building package..."
python3 -m pip install --upgrade build twine
python3 -m build

# Upload the package to PyPI
echo "[✔] Uploading package to PyPI..."
python3 -m twine upload dist/*

# Verify the new version on PyPI
echo "[✔] Verifying the updated version on PyPI..."
pip install --upgrade "$PROJECT_NAME"

echo "[✔] Update successful! New version: $NEW_VERSION"
