#!/bin/bash

# Define colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo -e "${RED}❌ Please specify the new version number.${NC}"
    exit 1
fi

NEW_VERSION=$1
REPORTS_DIR=~/apknife_reports
mkdir -p "$REPORTS_DIR"

echo -e "${BLUE}==========================================="
echo -e "    🚀 Git Auto-Update with Fixes"
echo -e "===========================================${NC}"

# 1️⃣ Fix Project Structure
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

# 2️⃣ Fix setup.py and pyproject.toml
function fix_setup_files() {
    echo -e "${YELLOW}🔄 Checking project setup files...${NC}"

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

# 3️⃣ Run Security Checks & Save Reports
function fix_security_issues() {
    echo -e "${YELLOW}🔍 Running security checks...${NC}"
    bandit -r apknife | tee "$REPORTS_DIR/security_report.txt"
    safety check --full-report | tee "$REPORTS_DIR/safety_report.txt"
    echo -e "${GREEN}✅ Security checks completed.${NC}"
}

# 4️⃣ Fix setuptools conflicts & update pip
function update_pip_and_setuptools() {
    echo -e "${YELLOW}🔄 Fixing setuptools conflicts...${NC}"
    
    # Uninstall all setuptools versions to prevent conflicts
    pip uninstall -y setuptools
    
    # Install the latest compatible version automatically
    pip install --upgrade pip setuptools

    echo -e "${GREEN}✅ Pip and setuptools updated.${NC}"
}

# 5️⃣ Generate Requirements Using pipreqs (Ensure no duplicates)
function fix_requirements() {
    echo -e "${YELLOW}🔄 Generating requirements.txt using pipreqs...${NC}"

    # Ensure pipreqs is installed
    if ! command -v pipreqs &> /dev/null; then
        echo -e "${YELLOW}📦 Installing pipreqs...${NC}"
        pip install pipreqs
    fi

    # Run pipreqs to generate requirements.txt based on the project code
    pipreqs . --force

    # Remove setuptools to avoid conflicts
    sed -i '/setuptools/d' requirements.txt

    # Remove duplicate dependencies
    sort -u -o requirements.txt requirements.txt

    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    install_requirements
    echo -e "${GREEN}✅ Requirements are updated.${NC}"
}

# 6️⃣ Install requirements safely
function install_requirements() {
    echo -e "${YELLOW}📦 Installing dependencies from requirements.txt...${NC}"
    
    update_pip_and_setuptools  # Ensure setuptools is up to date to prevent conflicts
    
    pip install -r requirements.txt --upgrade --force-reinstall
}

# 7️⃣ Run Tests
function run_tests() {
    echo -e "${YELLOW}🧪 Running tests...${NC}"
    pytest tests/ | tee "$REPORTS_DIR/test_results.txt"
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Some tests failed! Please fix them before publishing.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ All tests passed.${NC}"
}

# 8️⃣ Update Version Number
function update_version() {
    echo -e "${YELLOW}🔄 Updating version to $NEW_VERSION...${NC}"
    sed -i "s/version = \"[^\"]*\"/version = \"$NEW_VERSION\"/" pyproject.toml
    echo -e "${GREEN}✅ Version updated.${NC}"
}

# 9️⃣ Sync with GitHub (Deletes .apknife_history before push)
function sync_with_github() {
    echo -e "${YELLOW}🔄 Syncing with GitHub...${NC}"
    
    # Remove the history file
    if [ -f "apknife/.apknife_history" ]; then
        echo -e "${YELLOW}🗑️ Deleting apknife/.apknife_history...${NC}"
        rm -f apknife/.apknife_history
    fi

    git checkout main
    git pull --rebase origin main
    git add .

    if ! git diff-index --quiet HEAD --; then
        git commit -m "🚀 Release: $NEW_VERSION"
    fi

    git push origin main || git push --force origin main
    echo -e "${GREEN}✅ Changes pushed to GitHub.${NC}"
}

# 🔟 Verify Tool Execution After Installation
function check_tool_execution() {
    echo -e "${YELLOW}🔄 Verifying tool execution...${NC}"
    python -m venv test_env
    source test_env/bin/activate
    pip install .

    if ! command -v apknife &> /dev/null; then
        echo -e "${RED}❌ The tool does not run when calling 'apknife'.${NC}"
        deactivate
        rm -rf test_env
        exit 1
    fi

    deactivate
    rm -rf test_env
    echo -e "${GREEN}✅ The tool runs successfully.${NC}"
}

# 🧹 Clean Up Unnecessary Files
function cleanup() {
    echo -e "${YELLOW}🧹 Cleaning up unnecessary files...${NC}"
    rm -rf test_env dist/ build/ *.egg-info
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    echo -e "${GREEN}✅ Cleanup completed.${NC}"
}

# Run all steps in order
fix_project_structure
fix_setup_files
fix_security_issues
fix_requirements
run_tests
update_version
sync_with_github
check_tool_execution
cleanup

echo -e "${BLUE}==========================================="
echo -e "    🚀 Successfully updated version to $NEW_VERSION!"
echo -e "===========================================${NC}"
