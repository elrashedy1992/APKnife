import json
import argparse
import logging
import os
import subprocess
import sys
import time
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from apknife.modules import (
    analyzer, api_finder, builder, catch_rat, extract_sensitive, extractor,
    java_extractor, manifest_editor, permission_scanner, signer, smali_tools,
    vulnerability_scanner, dex_extractor, manifest_decoder
)
from apknife.modules.interactive_mode import interactive_shell
from apknife.modules.apk_modifier import APKModifier

# ANSI color codes for terminal output styling
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(message)s")

# Banner ASCII Art
BANNER = f"""{RED}
APKnife: The Cyber Blade of APK Domination
@@@@@@   @@@@@@@   @@@  @@@  @@@  @@@  @@@  @@@@@@@@  @@@@@@@@
@@@@@@@@  @@@@@@@@  @@@  @@@  @@@@ @@@  @@@  @@@@@@@@  @@@@@@@@
@@!  @@@  @@!  @@@  @@!  !@@  @@!@!@@@  @@!  @@!       @@!
!@!  @!@  !@!  @!@  !@!  @!!  !@!!@!@!  !@!  !@!       !@!
@!@!@!@!  @!@@!@!   @!@@!@!   @!@ !!@!  !!@  @!!!:!    @!!!:!
!!!@!!!!  !!@!!!    !!@!!!    !@!  !!!  !!!  !!!!!:    !!!!!:
!!:  !!!  !!:       !!: :!!   !!:  !!!  !!:  !!:       !!:
:!:  !:!  :!:       :!:  !:!  :!:  !:!  :!:  :!:       :!:
::   :::   ::        ::  :::   ::   ::   ::   ::        :: ::::
:   : :   :         :   :::  ::    :   :     :        : :: :::

{RESET}{CYAN}     APKnife – The Double-Edged Blade of APK Analysis 🔪🧸
{YELLOW}     Fear the Blade, Trust the Power! 🎨
{WHITE}     Where Hacking Meets Art! 🖌️
"""

# Animated loading effect
def loading_effect(text, delay=0.1):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Display the banner
def display_banner():
    print(BANNER)
    loading_effect(f"{PURPLE}⚙️  Loading the blade...", 0.05)
    loading_effect(f"{BLUE}🔪  Sharpening edges...", 0.07)
    loading_effect(f"{GREEN}🟢  Ready to cut!", 0.1)
    print(RESET)

# Load commands from external file
def load_commands():
    if not os.path.exists("commands.json"):
        logging.warning(f"{YELLOW}[!] commands.json not found. Creating a default one...{RESET}")
        default_commands = {
            "help": "Displays this help menu",
            "exit": "Exits the interactive mode",
            "update-commands": "Reloads the commands from the external file",
            "list-commands": "Displays the current list of available commands",
            "extract-dex": "Extract DEX files from an APK without fully decompiling it",
            "decode_manifest": "Decode AndroidManifest.xml without fully decompiling the APK",
            "waf": "Scan the app for protection mechanisms (e.g., Firewall, ProGuard, etc.)"  # Added the new command
        }
        with open("commands.json", "w") as file:
            json.dump(default_commands, file, indent=4)
        return default_commands

    try:
        with open("commands.json", "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        logging.error(f"{RED}[!] Invalid JSON format in commands file!{RESET}")
        return {}

def main():
    parser = argparse.ArgumentParser(
        description="APKnife: Advanced APK analysis & modification tool"
    )

    parser.add_argument(
        "command",
        choices=[
            "extract", "build", "sign", "analyze", "edit-manifest", "smali",
            "decode_manifest", "find-oncreate", "find-api", "scan-vulnerabilities",
            "scan-permissions", "catch_rat", "extract-java", "interactive",
            "extract-sensitive", "modify-apk", "extract-dex", "waf"  # Added the new command
        ],
        help="Command to execute",
    )

    parser.add_argument("-i", "--input", help="Input APK file")
    parser.add_argument("-o", "--output", help="Output file/directory")
    parser.add_argument(
        "-c", "--compress", action="store_true",
        help="Compress extracted Java files into a ZIP archive",
    )

    # Additional arguments for APK modification
    parser.add_argument("--name", help="New app name")
    parser.add_argument("--icon", help="New app icon (resized automatically)")
    parser.add_argument("--package", help="New package name")

    args = parser.parse_args()

    # Ensure input file is provided for required commands
    if args.command != "interactive" and not args.input:
        logging.error(f"{RED}[!] You must specify an input file using `-i`{RESET}")
        sys.exit(1)

    # Execute the selected command
    try:
        if args.command == "interactive":
            display_banner()
            COMMANDS = load_commands()
            interactive_shell(COMMANDS)  # Pass COMMANDS to interactive_shell
        elif args.command == "extract":
            extractor.extract_apk(args.input, args.output)
        elif args.command == "build":
            builder.build_apk(args.input, args.output)
        elif args.command == "sign":
            signer.sign_apk(args.input)
        elif args.command == "analyze":
            analyzer.analyze_apk(args.input)
        elif args.command == "edit-manifest":
            manifest_editor.edit_manifest(args.input)
        elif args.command == "smali":
            smali_tools.decompile_apk(args.input, args.output)
        elif args.command == "decode_manifest":
            manifest_decoder.decode_manifest(args.input, args.output)
        elif args.command == "find-oncreate":
            smali_tools.find_oncreate(args.input)
        elif args.command == "find-api":
            api_finder.find_api_calls(args.input)
        elif args.command == "scan-vulnerabilities":
            vulnerability_scanner.scan_apk(args.input)
        elif args.command == "scan-permissions":
            permission_scanner.scan_permissions(args.input)
        elif args.command == "catch_rat":
            catch_rat.analyze_apk_ips(args.input)
        elif args.command == "extract-java":
            java_extractor.extract_java(args.input, args.output, args.compress)
        elif args.command == "extract-sensitive":
            if not args.output:
                args.output = "sensitive_report.json"
            extract_sensitive.extract_sensitive_data(args.input, args.output)
        elif args.command == "modify-apk":
            logging.info(f"{GREEN}[*] Modifying APK: {args.input}{RESET}")
            modifier = APKModifier(args.input, args.name, args.icon, args.package)
            modifier.run()
        elif args.command == "extract-dex":
            logging.info(f"{GREEN}[*] Extracting DEX files from: {args.input}{RESET}")
            dex_files = dex_extractor.extract_dex(args.input, args.output)
            if dex_files:
                logging.info(f"{GREEN}[*] DEX files extracted successfully: {dex_files}{RESET}")
            else:
                logging.error(f"{RED}[!] Failed to extract DEX files{RESET}")
        elif args.command == "waf":
            from apknife.modules.protection_scanner import scan_apk_protections
            protections = scan_apk_protections(args.input)
            for protection, status in protections.items():
                print(f"{protection}: {'✅' if status else '❌'}")
        else:
            logging.error(f"{RED}[!] Unknown command!{RESET}")

    except Exception as e:
        logging.error(f"{RED}[!] Error executing `{args.command}`: {e}{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
