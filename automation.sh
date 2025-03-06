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
    
    if pip install -r requirements.txt 2>&1 | grep -q "No matching distribution found"; then
        echo -e "${RED}⚠️ Incompatible packages found! Updating requirements...${NC}"
        pip freeze > new_requirements.txt
        mv new_requirements.txt requirements.txt
    fi

    echo -e "${GREEN}✅ requirements.txt is updated.${NC}"
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

# **7️⃣ Sync with GitHub**
function sync_with_github() {
    echo -e "${YELLOW}🔄 Syncing with GitHub...${NC}"
    
    git pull origin main
    git add .
    git commit -m "🚀 Release: $NEW_VERSION"
    git push origin main

    echo -e "${GREEN}✅ Changes pushed to GitHub.${NC}"
}

# **8️⃣ Build and Upload to PyPI**
function build_and_upload_to_pypi() {
    echo -e "${YELLOW}📦 Cleaning and building package...${NC}"
    
    rm -rf dist/ build/ *.egg-info
    python -m build

    echo -e "${YELLOW}📤 Uploading package to PyPI...${NC}"
    twine upload dist/*

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Package uploaded successfully to PyPI.${NC}"
    else
        echo -e "${RED}❌ Upload failed. Please check for errors.${NC}"
        exit 1
    fi
}

# **9️⃣ Verify Tool Execution After Installation**
function check_tool_execution() {
    echo -e "${YELLOW}🔄 Verifying tool execution...${NC}"

    pip install .
    if ! command -v apknife &> /dev/null; then
        echo -e "${RED}❌ The tool does not run when calling 'apknife'.${NC}"
        exit 1
    fi

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
