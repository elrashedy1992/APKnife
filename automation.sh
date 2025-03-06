#!/bin/bash

# Colors for better output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Ensure a new version number is provided
if [ -z "$1" ]; then
    echo -e "${RED}❌ Please specify the new version number.${NC}"
    exit 1
fi
NEW_VERSION=$1

echo -e "${BLUE}==========================================="
echo -e "    Git & PyPI Auto-Update with Security Fixes"
echo -e "===========================================${NC}"

# Fix project structure if needed
function check_and_fix_project_structure() {
    echo -e "${YELLOW}🔍 Checking project structure...${NC}"

    if [ ! -f "setup.py" ] && [ ! -f "pyproject.toml" ]; then
        echo -e "${RED}❌ setup.py or pyproject.toml not found. This is not a valid Python project.${NC}"
        exit 1
    fi

    if [ ! -d "apknife" ]; then
        echo -e "${RED}⚠️ The main package directory 'apknife' is missing. Fixing...${NC}"
        mkdir -p apknife
        mv {__init__.py,apknife.py,assets,modules,commands.json,tools} apknife/ 2>/dev/null
    fi

    echo -e "${GREEN}✅ Project structure is correct.${NC}"
}

# Check tool execution
function check_tool_execution() {
    echo -e "${YELLOW}🔄 Checking tool execution after installation...${NC}"

    pip install . >/dev/null
    if ! command -v apknife &> /dev/null; then
        echo -e "${RED}❌ The tool does not run when calling 'apknife'.${NC}"
        exit 1
    fi

    echo -e "${GREEN}✅ The tool runs successfully.${NC}"
}

# Fix security issues
function security_check_and_fix() {
    echo -e "${YELLOW}🔍 Running security checks and applying fixes...${NC}"

    bandit -r apknife | tee security_report.txt
    if grep -q "Issue:" security_report.txt; then
        echo -e "${RED}⚠️ Security vulnerabilities detected!${NC}"
        cat security_report.txt
    fi

    echo -e "${YELLOW}🔄 Checking dependencies for security vulnerabilities...${NC}"
    safety check --full-report | tee safety_report.txt
    if grep -q "INSECURE PACKAGE" safety_report.txt; then
        echo -e "${RED}⚠️ Vulnerable dependencies detected! Updating packages...${NC}"
        pip install --upgrade -r requirements.txt
    fi

    echo -e "${GREEN}✅ Security checks completed.${NC}"
}

# Fix issues in requirements.txt
function fix_requirements() {
    echo -e "${YELLOW}🔄 Checking for package compatibility issues...${NC}"

    if pip install -r requirements.txt 2>&1 | grep -q "No matching distribution found"; then
        echo -e "${RED}⚠️ Incompatible packages found. Updating requirements...${NC}"
        pip freeze > new_requirements.txt
        mv new_requirements.txt requirements.txt
    fi

    echo -e "${GREEN}✅ Requirements file is up-to-date.${NC}"
}

# Run tests
function run_tests() {
    echo -e "${YELLOW}🧪 Running tests...${NC}"
    
    pytest tests/
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Some tests failed! Please fix them before publishing.${NC}"
        exit 1
    fi

    echo -e "${GREEN}✅ All tests passed successfully.${NC}"
}

# Update version
function update_version() {
    echo -e "${YELLOW}🔄 Updating version to $NEW_VERSION...${NC}"
    
    sed -i "s/version = \"[^\"]*\"/version = \"$NEW_VERSION\"/" pyproject.toml
    sed -i "s/version=['\"][^'\"]*['\"]/version='$NEW_VERSION'/" setup.py

    echo -e "${GREEN}✅ Version updated.${NC}"
}

# Sync with GitHub
function sync_with_github() {
    echo -e "${YELLOW}🔄 Syncing with GitHub...${NC}"
    
    git pull origin main
    git add .
    git commit -m "🚀 Release: $NEW_VERSION"
    git push origin main

    echo -e "${GREEN}✅ Changes pushed to GitHub.${NC}"
}

# Build and upload package to PyPI
function build_and_upload_to_pypi() {
    echo -e "${YELLOW}📦 Cleaning up and building package...${NC}"
    
    rm -rf dist/ build/ *.egg-info
    python -m build

    echo -e "${YELLOW}📤 Uploading package to PyPI...${NC}"
    twine upload dist/*

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Package successfully uploaded to PyPI.${NC}"
    else
        echo -e "${RED}❌ Upload failed. Please check for errors.${NC}"
        exit 1
    fi
}

# ** Run all steps in order **
check_and_fix_project_structure
check_tool_execution
security_check_and_fix
fix_requirements
run_tests
update_version
sync_with_github
build_and_upload_to_pypi

echo -e "${BLUE}==========================================="
echo -e "    🚀 Successfully released version $NEW_VERSION!"
echo -e "===========================================${NC}"
