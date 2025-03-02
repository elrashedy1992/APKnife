import logging
import sys
import time

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style

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

# Define a style for the prompt
style = Style.from_dict(
    {
        "prompt": "fg:ansicyan",
        "input": "fg:ansigreen",
    }
)

# Banner ASCII Art
BANNER = f"""{RED}
      || ________________
O|===|* >________________>
      ||
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
print(BANNER)
loading_effect(f"{PURPLE}⚙️  Loading the blade...", 0.05)
loading_effect(f"{BLUE}🔪  Sharpening edges...", 0.07)
loading_effect(f"{GREEN}🟢  Ready to cut!", 0.1)
print(RESET)

# Available commands and their descriptions
COMMANDS = {
    "extract": "Extracts an APK file (-i input.apk -o output_folder)",
    "build": "Builds an APK from a modified directory (-i folder -o output.apk)",
    "sign": "Signs an APK file (-i input.apk)",
    "analyze": "Analyzes an APK for vulnerabilities (-i input.apk)",
    "edit-manifest": "Modifies the AndroidManifest.xml of an APK (-i input.apk)",
    "smali": "Decompiles APK into smali code (-i input.apk -o output_folder)",
    "decode-xml": "Decodes binary XML files in an APK (-i input.apk)",
    "find-oncreate": "Finds the onCreate methods inside smali code (-i input.apk)",
    "find-api": "Finds API calls used in an APK (-i input.apk or -i smali_file(recommended))",
    "scan-vulnerabilities": "Scans APK for security vulnerabilities (-i input.apk)",
    "scan-permissions": "Lists all permissions requested by an APK (-i input.apk)",
    "catch_rat": "Detects potential RAT (Remote Access Trojan) in APK (-i input.apk)",
    "extract-java": "Extracts Java source code from an APK (-i input.apk -o output_folder -c [optional])",
    "extract-sensitive": "Extracts sensitive information from APK (-i input.apk -o output.json)",
    "modify-apk --icon": "Modifies the APK icon (-i input.apk )",
    "modify-apk --name ": "Changes the application name (-i input.apk )",
    "modify-apk --package": "Modifies the package name (-i input.apk -o new_package_name)",
    "help": "Displays this help menu",
    "exit": "Exits the interactive mode",
}


def interactive_shell():
    completer = WordCompleter(COMMANDS.keys(), ignore_case=True)
    session = PromptSession(
        history=FileHistory(".apknife_history"),
        auto_suggest=AutoSuggestFromHistory(),
        completer=completer,
        style=style,
    )

    while True:
        try:
            text = session.prompt("APKnife> ")
            if text.strip() == "exit":
                break

            args = text.split()
            if not args:
                continue

            command = args[0]

            if command == "help":
                print(f"\n{YELLOW}Available Commands:{RESET}")
                for cmd, desc in COMMANDS.items():
                    print(f"  {GREEN}{cmd.ljust(20)}{RESET} - {WHITE}{desc}{RESET}")
                print()
                continue

            if command not in COMMANDS:
                logging.error(f"{RED}[!] Unknown command: {command}{RESET}")
                continue

            # Simulate argparse behavior
            input_file = None
            output_file = None
            compress = False

            for i, arg in enumerate(args):
                if arg == "-i" and i + 1 < len(args):
                    input_file = args[i + 1]
                elif arg == "-o" and i + 1 < len(args):
                    output_file = args[i + 1]
                elif arg == "-c":
                    compress = True

            if (
                command != "interactive"
                and not input_file
                and command not in ["help", "exit"]
            ):
                logging.error(
                    f"{RED}[!] You must specify an input file using `-i`{RESET}"
                )
                continue

            try:
                if command == "extract":
                    from modules.extractor import extract_apk

                    extract_apk(input_file, output_file)
                elif command == "build":
                    from modules.builder import build_apk

                    build_apk(input_file, output_file)
                elif command == "sign":
                    from modules.signer import sign_apk

                    sign_apk(input_file)
                elif command == "analyze":
                    from modules.analyzer import analyze_apk

                    analyze_apk(input_file)
                elif command == "edit-manifest":
                    from modules.manifest_editor import edit_manifest

                    edit_manifest(input_file)
                elif command == "smali":
                    from modules.smali_tools import decompile_apk

                    decompile_apk(input_file, output_file)
                elif command == "decode-xml":
                    from modules.xml_decoder import decode_xml

                    decode_xml(input_file)
                elif command == "find-oncreate":
                    from modules.smali_tools import find_oncreate

                    find_oncreate(input_file)
                elif command == "find-api":
                    from modules.api_finder import find_api_calls

                    find_api_calls(input_file)
                elif command == "scan-vulnerabilities":
                    from modules.vulnerability_scanner import scan_apk

                    scan_apk(input_file)
                elif command == "scan-permissions":
                    from modules.permission_scanner import scan_permissions

                    scan_permissions(input_file)
                elif command == "catch_rat":
                    from modules.catch_rat import analyze_apk_ips

                    analyze_apk_ips(input_file)
                elif command == "extract-java":
                    from modules.java_extractor import extract_java

                    extract_java(input_file, output_file, compress)
                elif command == "extract-sensitive":
                    from modules.extract_sensitive import extract_sensitive_data

                    if not output_file:
                        output_file = "sensitive_report.json"
                    extract_sensitive_data(input_file, output_file)
                elif command == "change-icon":
                    from modules.icon_editor import change_icon

                    change_icon(input_file, output_file)
                elif command == "change-name":
                    from modules.name_editor import change_app_name

                    change_app_name(input_file, output_file)
                elif command == "change-package":
                    from modules.package_editor import change_package_name

                    change_package_name(input_file, output_file)
                else:
                    logging.error(f"{RED}[!] Unknown command!{RESET}")
            except Exception as e:
                logging.error(f"{RED}[!] Error executing `{command}`: {e}{RESET}")

        except KeyboardInterrupt:
            continue
        except EOFError:
            break
