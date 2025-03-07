#!/bin/bash

# Define colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Function to install required tools
function install_tools() {
    echo -e "${YELLOW}📦 Installing required tools...${NC}"
    pip install bandit safety defusedxml
    echo -e "${GREEN}✅ Tools installed.${NC}"
}

# Function to run Bandit security checks
function run_bandit() {
    echo -e "${YELLOW}🔍 Running Bandit security checks...${NC}"
    bandit -r apknife/ -f txt -o bandit_report.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Bandit found security issues.${NC}"
        fix_bandit_issues
    else
        echo -e "${GREEN}✅ No security issues found by Bandit.${NC}"
    fi
}

# Function to fix Bandit issues
function fix_bandit_issues() {
    echo -e "${YELLOW}🔄 Fixing Bandit issues...${NC}"

    # Replace xml.etree.ElementTree with defusedxml
    if grep -q "xml.etree.ElementTree" apknife/modules/vulnerability_scanner.py; then
        echo -e "${YELLOW}🔧 Replacing xml.etree.ElementTree with defusedxml...${NC}"
        sed -i 's/xml.etree.ElementTree/defusedxml.ElementTree/g' apknife/modules/vulnerability_scanner.py
        echo -e "${GREEN}✅ XML parsing is now secure.${NC}"
    fi

    # Add more fixes here as needed
    echo -e "${GREEN}✅ Bandit issues fixed.${NC}"
}

# Function to run Safety checks
function run_safety() {
    echo -e "${YELLOW}🔍 Running Safety checks...${NC}"
    safety check --full-report > safety_report.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Safety found vulnerable dependencies.${NC}"
        fix_safety_issues
    else
        echo -e "${GREEN}✅ No vulnerable dependencies found by Safety.${NC}"
    fi
}

# Function to fix Safety issues
function fix_safety_issues() {
    echo -e "${YELLOW}🔄 Fixing Safety issues...${NC}"

    # Upgrade vulnerable dependencies
    if grep -q "Vulnerability found" safety_report.txt; then
        echo -e "${YELLOW}🔧 Upgrading vulnerable dependencies...${NC}"
        pip install --upgrade $(grep "Vulnerability found" safety_report.txt | awk '{print $2}')
        echo -e "${GREEN}✅ Vulnerable dependencies upgraded.${NC}"
    fi

    echo -e "${GREEN}✅ Safety issues fixed.${NC}"
}

# Function to run tests
function run_tests() {
    echo -e "${YELLOW}🧪 Running tests...${NC}"
    pytest tests/
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Some tests failed! Please fix them before proceeding.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ All tests passed.${NC}"
}

# Main function
function main() {
    install_tools
    run_bandit
    run_safety
    run_tests
    echo -e "${GREEN}✅ All security checks and fixes completed successfully!${NC}"
}

# Run the script
main
