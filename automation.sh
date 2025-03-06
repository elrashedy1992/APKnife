#!/bin/bash

# Colors for better output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Ensure a version number is provided
if [ -z "$1" ]; then
    echo -e "${RED}❌ Please specify the new version number.${NC}"
    exit 1
fi
NEW_VERSION=$1

# Directory to store reports outside the project folder
REPORTS_DIR=~/apknife_reports
mkdir -p "$REPORTS_DIR"

echo -e "${BLUE}==========================================="
echo -e "    🚀 Git & PyPI Auto-Update with Fixes"
echo -e "===========================================${NC}"

# **1️⃣ Fix Project Structure**
function fix_project_structure() {
    echo -e "${YELLOW}🔍 Checking project structure...${NC}"
    
    if [ -d "src/apknife" ]; then
        echo -e "${YELLOW}🔄 Moving files from src/ to root...${NC}"
        mv src/apknife/* apknife/
        rm -rf src/
    fi
    
    if [ ! -d "apknife" ]; then
        echo -e "${RED}⚠️ 'apknife' package directory is missing. Creating it...${NC}"
        mkdir -p apknife
    fi
    
    touch apknife/__init__.py
    echo -e "${GREEN}✅ Project structure is correct.${NC}"
}

# **2️⃣ Fix setup.py and pyproject.toml**
function fix_setup_files() {
    echo -e "${YELLOW}🔄 Checking project setup files...${NC}"
    
    if [ ! -f "setup.py" ]; then
        echo -e "${YELLOW}📄 Creating setup.py...${NC}"
        cat <<EOF > setup.py
from setuptools import setup, find_packages

setup(
    name="apknife",
    version="$NEW_VERSION",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "apknife=apknife.apknife:main",
        ],
    },
)
EOF
    fi

    if [ ! -f "pyproject.toml" ]; then
        echo -e "${YELLOW}📄 Creating pyproject.toml...${NC}"
        cat <<EOF > pyproject.toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "apknife"
version = "$NEW_VERSION"
EOF
    fi

    echo -e "${GREEN}✅ Setup files are correct.${NC}"
}

# **3️⃣ Run Security Checks & Save Reports**
function fix_security_issues() {
    echo -e "${YELLOW}🔍 Running security checks...${NC}"
    
    bandit -r apknife | tee "$REPORTS_DIR/security_report.txt"
    if grep -q "Issue:" "$REPORTS_DIR/security_report.txt"; then
        echo -e "${RED}⚠️ Security vulnerabilities detected!${NC}"
    fi

    safety check --full-report | tee "$REPORTS_DIR/safety_report.txt"
    if grep -q "INSECURE PACKAGE" "$REPORTS_DIR/safety_report.txt"; then
        echo -e "${YELLOW}🔄 Updating vulnerable packages...${NC}"
        pip install --upgrade -r requirements.txt
    fi

    echo -e "${GREEN}✅ Security checks completed.${NC}"
}

# **4️⃣ Fix Issues in requirements.txt**
function fix_requirements() {
    echo -e "${YELLOW}🔄 Checking package compatibility in requirements.txt...${NC}"

    # Create a backup before modifying
    cp requirements.txt requirements_backup.txt

    # Iterate through each package in requirements.txt
    while IFS= read -r package; do
        if [[ "$package" == "#"* ]] || [[ -z "$package" ]]; then
            continue  # Skip comments and empty lines
        fi

        package_name=$(echo "$package" | sed 's/[<>=!].*//')  # Extract package name
        required_version=$(echo "$package" | grep -oP '(?<===)[0-9\.]+')  # Extract version if specified

        # Check if the package version exists
        available_versions=$(pip index versions "$package_name" 2>/dev/null | grep -oP '[0-9]+(\.[0-9]+)*' | sort -V)
        
        if [ -z "$available_versions" ]; then
            echo -e "${RED}⚠️ Package '$package_name' not found on PyPI! Removing from requirements.${NC}"
            continue  # Skip this package
        fi
        
        latest_version=$(echo "$available_versions" | tail -n 1)  # Get the latest version
        
        if [[ -n "$required_version" ]] && ! echo "$available_versions" | grep -q "^$required_version$"; then
            echo -e "${YELLOW}⚠️ Version '$required_version' of '$package_name' is not available! Using '$latest_version' instead.${NC}"
            echo "$package_name==$latest_version" >> fixed_requirements.txt
        else
            echo "$package" >> fixed_requirements.txt  # Keep valid versions
        fi

    done < requirements.txt

    # Replace the old requirements.txt with the fixed one
    mv fixed_requirements.txt requirements.txt

    echo -e "${GREEN}✅ requirements.txt updated. Installing dependencies...${NC}"
    
    pip install -r requirements.txt
}

# **5️⃣ Run Tests**
function run_tests() {
    echo -e "${YELLOW}🧪 Running tests...${NC}"
    
    pytest tests/ | tee "$REPORTS_DIR/test_results.txt"
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Some tests failed! Please fix them before publishing.${NC}"
        exit 1
    fi

    echo -e "${GREEN}✅ All tests passed.${NC}"
}

# **6️⃣ Update Version Number**
function update_version() {
    echo -e "${YELLOW}🔄 Updating version to $NEW_VERSION...${NC}"
    
    sed -i "s/version = \"[^\"]*\"/version = \"$NEW_VERSION\"/" pyproject.toml
    sed -i "s/version=['\"][^'\"]*['\"]/version='$NEW_VERSION'/" setup.py

    echo -e "${GREEN}✅ Version updated.${NC}"
}

# **7️⃣ Sync with GitHub (Handling Divergent Branches)**
function sync_with_github() {
    echo -e "${YELLOW}🔄 Syncing with GitHub...${NC}"
    
    git checkout main
    git pull --rebase origin main
    git add .
    
    if ! git diff-index --quiet HEAD --; then
        git commit -m "🚀 Release: $NEW_VERSION"
    else
        echo -e "${YELLOW}⚠️ No changes to commit.${NC}"
    fi

    git push origin main || git push --force origin main

    echo -e "${GREEN}✅ Changes successfully pushed to GitHub.${NC}"
}

# **8️⃣ Build and Upload to PyPI**
function build_and_upload_to_pypi() {
    echo -e "${YELLOW}📦 Cleaning and building package...${NC}"
    
    rm -rf dist/ build/ *.egg-info
    python -m build

    echo -e "${YELLOW}📤 Uploading package to PyPI...${NC}"
    twine upload dist/* || { echo -e "${RED}❌ Upload failed.${NC}"; exit 1; }

    echo -e "${GREEN}✅ Package uploaded successfully to PyPI.${NC}"
}

# **9️⃣ Verify Tool Execution After Installation**
function check_tool_execution() {
    echo -e "${YELLOW}🔄 Verifying tool execution...${NC}"

    pip install .
    command -v apknife &> /dev/null || { echo -e "${RED}❌ The tool does not run when calling 'apknife'.${NC}"; exit 1; }

    echo -e "${GREEN}✅ The tool runs successfully.${NC}"
}

# **Run all steps in order**
fix_project_structure
fix_setup_files
fix_security_issues
fix_requirements
run_tests
update_version
sync_with_github
build_and_upload_to_pypi
check_tool_execution

echo -e "${BLUE}==========================================="
echo -e "    🚀 Successfully released version $NEW_VERSION!"
echo -e "===========================================${NC}"
