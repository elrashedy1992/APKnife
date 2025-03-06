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

# Display script header
echo -e "${BLUE}==========================================="
echo -e "    Git & PyPI Auto-Update with Security Checks"
echo -e "===========================================${NC}"

# Check and fix project structure
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

# Check if the tool runs after installation
function check_tool_execution() {
    echo -e "${YELLOW}🔄 Checking tool execution after installation...${NC}"

    pip install .
    if ! command -v apknife &> /dev/null; then
        echo -e "${RED}❌ The tool does not run when calling 'apknife'.${NC}"
        exit 1
    fi

    echo -e "${GREEN}✅ The tool runs successfully.${NC}"
}

# Security checks without stopping execution
function security_check() {
    echo -e "${YELLOW}🔍 Running security checks...${NC}"
    
    local security_issues=0

    # Static security analysis with bandit
    echo -e "${BLUE}🔹 Running Bandit...${NC}"
    bandit -r apknife | tee bandit_report.txt
    if grep -q "Issue" bandit_report.txt; then
        echo -e "${RED}⚠️ Security vulnerabilities detected by Bandit! Please review:${NC}"
        cat bandit_report.txt | grep "Issue"
        security_issues=1
    fi

    # Check for vulnerabilities in dependencies
    echo -e "${BLUE}🔹 Running Safety...${NC}"
    safety check | tee safety_report.txt
    if grep -q "vulnerabilities" safety_report.txt; then
        echo -e "${RED}⚠️ Security issues found in dependencies!${NC}"
        cat safety_report.txt
        security_issues=1
    fi

    if [ $security_issues -eq 1 ]; then
        echo -e "${YELLOW}⚠️ Security issues were found, but continuing with the release.${NC}"
    else
        echo -e "${GREEN}✅ No critical security issues detected.${NC}"
    fi
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

# Update version in setup.py & pyproject.toml
function update_version() {
    echo -e "${YELLOW}🔄 Updating version to $NEW_VERSION...${NC}"
    
    sed -i "s/version = \"[^\"]*\"/version = \"$NEW_VERSION\"/" pyproject.toml
    sed -i "s/version=['\"][^'\"]*['\"]/version='$NEW_VERSION'/" setup.py

    echo -e "${GREEN}✅ Version updated.${NC}"
}

# Sync updates with GitHub
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
security_check  # لا يوقف التنفيذ عند وجود ثغرات
run_tests
update_version
sync_with_github
build_and_upload_to_pypi

echo -e "${BLUE}==========================================="
echo -e "    🚀 Successfully released version $NEW_VERSION!"
echo -e "===========================================${NC}"
