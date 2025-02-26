#!/bin/bash

# Colors
CYAN='\033[1;36m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
GREEN='\033[1;32m'
RESET='\033[0m'

# Clear the screen for a dramatic start
clear

# Cyberpunk ASCII Banner
echo -e "${CYAN}"
cat << "EOF"
  █████╗ ██████╗ ██╗  ██╗███╗   ██╗██╗███████╗██████╗ 
 ██╔══██╗██╔══██╗██║  ██║████╗  ██║██║██╔════╝██╔══██╗
 ███████║██████╔╝███████║██╔██╗ ██║██║███████╗██████╔╝
 ██╔══██║██╔═══╝ ██╔══██║██║╚██╗██║██║╚════██║██╔═══╝ 
 ██║  ██║██║     ██║  ██║██║ ╚████║██║███████║██║     
 ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝╚═╝     
EOF
echo -e "${YELLOW}            [ APKnife Auto-Installer ] ${RESET}"
echo -e "${GREEN}           Script by: Mr_Nightmare 🔥 ${RESET}"
echo ""

sleep 2

# Root Check
if [[ $EUID -ne 0 ]]; then
    echo -e "${RED}[⚠️] Please run this script as root!${RESET}"
    exit 1
fi

# Detect Operating System
OS=""
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    OS=$ID
elif [[ $(uname) == "Darwin" ]]; then
    OS="macos"
elif [[ $(uname) == "Linux" ]]; then
    OS="linux"
elif [[ $(uname) == "Android" ]]; then
    OS="termux"
else
    echo -e "${RED}[❌] Unsupported Operating System!${RESET}"
    exit 1
fi

echo -e "${CYAN}[💻] Detected OS: $OS ${RESET}"
sleep 1

# Function to Install Dependencies
install_dependencies() {
    echo -e "${YELLOW}[📦] Installing dependencies...${RESET}"
    sleep 1

    case "$OS" in
        ubuntu|debian)
            apt update && apt install -y python3 python3-pip unzip openjdk-17-jdk
            ;;
        arch|manjaro)
            pacman -Syu --noconfirm python python-pip unzip jdk-openjdk
            ;;
        termux)
            pkg update && pkg install -y python python-pip unzip openjdk-17
            ;;
        macos)
            brew install python unzip openjdk
            ;;
        *)
            echo -e "${RED}[❌] Unsupported OS! Exiting...${RESET}"
            exit 1
            ;;
    esac
}

install_dependencies

# Ensure pip is installed and updated
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}[⚠️] pip3 not found! Installing...${RESET}"
    python3 -m ensurepip
fi
pip3 install --upgrade pip

# Create and Activate Virtual Environment (Optional but Recommended)
if [[ ! -d "env" ]]; then
    echo -e "${CYAN}[🐍] Creating Python Virtual Environment...${RESET}"
    python3 -m venv env
fi
source env/bin/activate

# Install Python Libraries
echo -e "${YELLOW}[🚀] Installing Required Python Libraries...${RESET}"
pip3 install androguard requests lxml

# Setting Up APK Signer (For Linux)
if [[ "$OS" != "macos" ]]; then
    echo -e "${CYAN}[🔏] Setting up APK Signer...${RESET}"
    if ! command -v apksigner &> /dev/null; then
        echo -e "${RED}[⚠️] apksigner not found! Downloading...${RESET}"
        mkdir -p ~/Android/Sdk/cmdline-tools
        cd ~/Android/Sdk/cmdline-tools || exit
        wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O sdk-tools.zip
        unzip sdk-tools.zip && rm sdk-tools.zip
        export PATH=$PATH:~/Android/Sdk/cmdline-tools/bin
        echo 'export PATH=$PATH:~/Android/Sdk/cmdline-tools/bin' >> ~/.bashrc
        source ~/.bashrc
    fi
fi

# Make APKnife Executable
chmod +x APKnife/apknife.py

# Final Message
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${YELLOW} ✅ APKnife Installation Complete! 🔥 ${RESET}"
echo -e "${CYAN} ➡️  Run: python3 APKnife/apknife.py --help ${RESET}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${RED} [🔰] Created by: Mr_Nightmare ${RESET}"
echo ""
