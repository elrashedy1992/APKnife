import os
import readline
import logging
import sys
import time
from modules import (
    extractor, builder, signer, analyzer, manifest_editor, smali_tools,
    xml_decoder, api_finder, vulnerability_scanner, permission_scanner,
    catch_rat, java_extractor, extract_sensitive
)

# ANSI color codes for styling
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"

# Animated loading effect
def loading_effect(text, delay=0.1):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Banner ASCII Art
BANNER = f"""{RED}
      || ________________
O|===|* >________________>
      ||
{RESET}{CYAN}     APKnife – The Double-Edged Blade of APK Analysis 🔪🧸
{YELLOW}     Fear the Blade, Trust the Power! 🎨
{WHITE}     Where Hacking Meets Art! 🖌️
"""

# Display the banner
print(BANNER)

# Simulate a loading effect
loading_effect(f"{PURPLE}⚙️  Loading the blade...", 0.05)
loading_effect(f"{BLUE}🔪  Sharpening edges...", 0.07)
loading_effect(f"{GREEN}🟢  Ready to cut!", 0.1)
print(RESET)

HISTORY_FILE = os.path.expanduser("~/.apknife_history")

COMMANDS = [
    "extract", "build", "sign", "analyze", "edit-manifest", "smali",
    "decode-xml", "find-oncreate", "find-api", "scan-vulnerabilities",
    "scan-permissions", "catch_rat", "extract-java", "extract-sensitive",
    "help", "exit"
]

def completer(text, state):
    """Autocomplete function for readline"""
    options = [cmd for cmd in COMMANDS if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    return None

# Enable readline features
readline.set_completer(completer)
readline.parse_and_bind("tab: complete")
readline.parse_and_bind("set editing-mode vi")  # Enables arrow key navigation

# Load command history if available
if os.path.exists(HISTORY_FILE):
    readline.read_history_file(HISTORY_FILE)

def save_history():
    """Save command history to file"""
    readline.write_history_file(HISTORY_FILE)

def show_help():
    help_text = f"""
{CYAN}APKnife - The Double-Edged Blade of APK Analysis 🔪{RESET}
{GREEN}Available Commands:{RESET}

  {YELLOW}extract -i <apk_file> -o <output_dir>{RESET}      Extracts the contents of an APK file.
  {YELLOW}build -i <input_dir> -o <output_apk>{RESET}      Rebuilds an APK from extracted files.
  {YELLOW}sign -i <apk_file>{RESET}                       Signs an APK file to make it installable.
  {YELLOW}analyze -i <apk_file>{RESET}                    Provides detailed analysis of an APK file.
  {YELLOW}edit-manifest -i <apk_file>{RESET}              Modifies the AndroidManifest.xml file.
  {YELLOW}smali -i <apk_file> -o <output_dir>{RESET}      Decompiles an APK into Smali code.
  {YELLOW}decode-xml -i <apk_file>{RESET}                 Decodes XML files inside an APK.
  {YELLOW}find-oncreate -i <apk_file>{RESET}              Searches for the onCreate method.
  {YELLOW}find-api -i <apk_file>{RESET}                   Detects API calls inside an APK.
  {YELLOW}scan-vulnerabilities -i <apk_file>{RESET}       Scans the APK for known vulnerabilities.
  {YELLOW}scan-permissions -i <apk_file>{RESET}           Lists all permissions requested by the APK.
  {YELLOW}catch_rat -i <apk_file>{RESET}                  Detects RAT (Remote Access Trojan) indicators.
  {YELLOW}extract-java -i <apk_file> -o <output_dir> -c{RESET} Extracts Java source code from an APK.
  {YELLOW}extract-sensitive -i <apk_file> [-o report.json]{RESET} Extracts sensitive data from an APK.

  {CYAN}General Commands:{RESET}
  {YELLOW}help{RESET}  - Shows this help menu.
  {YELLOW}exit{RESET}  - Exits the interactive mode.
"""
    print(help_text)

def handle_command(command):
    args = command.split()

    if args[0] == "help":
        show_help()

    elif args[0] == "extract-sensitive":
        if len(args) < 2:
            print(f"{RED}[!] Usage: extract-sensitive -i <apk_file> [-o report.json]{RESET}")
        else:
            apk_path = args[1]
            output_file = args[2] if len(args) > 2 else None
            try:
                extract_sensitive.extract_data(apk_path, output_file)
                print(f"{GREEN}[*] Sensitive data extraction completed successfully.{RESET}")
            except Exception as e:
                print(f"{RED}[!] Error extracting sensitive data: {e}{RESET}")

    elif args[0] == "exit":
        print(f"{GREEN}[*] Saving command history and exiting...{RESET}")
        save_history()
        sys.exit(0)

    else:
        print(f"{RED}[!] Unknown command: {command}{RESET}")

def interactive_shell():
    print(f"{CYAN}APKnife Interactive Mode (Type 'help' for commands, 'exit' to quit){RESET}")

    while True:
        try:
            command = input(f"{YELLOW}APKnife> {RESET}").strip()
            if command:
                handle_command(command)
        except KeyboardInterrupt:
            print(f"\n{GREEN}[*] Saving command history and exiting...{RESET}")
            save_history()
            sys.exit(0)

if __name__ == "__main__":
    interactive_shell()
