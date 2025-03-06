import json
import logging
import os
import subprocess
import argparse
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

# Load commands from external file
def load_commands():
    if not os.path.exists("commands.json"):
        logging.warning(f"{YELLOW}[!] commands.json not found. Creating a default one...{RESET}")
        default_commands = {
            "help": "Displays this help menu",
            "exit": "Exits the interactive mode",
            "update-commands": "Reloads the commands from the external file",
            "list-commands": "Displays the current list of available commands",
            "extract-dex": "Extract DEX files from an APK",
            "decode_manifest": "Decode AndroidManifest.xml",
            "waf": "Scan the app for protection mechanisms",
            "analyze": "Analyze the APK",
            "build": "Build the APK",
            "sign": "Sign the APK",
            "edit-manifest": "Edit the AndroidManifest.xml",
            "smali": "Decompile the APK to Smali",
            "find-oncreate": "Find onCreate methods in the APK",
            "find-api": "Find API calls in the APK",
            "scan-vulnerabilities": "Scan the APK for vulnerabilities",
            "scan-permissions": "Scan the APK for permissions",
            "catch_rat": "Analyze the APK for RATs",
            "extract-java": "Extract Java code from the APK",
            "extract-sensitive": "Extract sensitive data from the APK",
            "modify-apk": "Modify the APK",
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

# Execute shell commands
def execute_shell_command(command):
    try:
        # Handle 'cd' command separately
        if command.startswith("cd "):
            new_dir = command.split(" ", 1)[1].strip()
            try:
                os.chdir(new_dir)
                return f"{GREEN}[+] Changed directory to: {os.getcwd()}{RESET}"
            except FileNotFoundError:
                return f"{RED}[!] Directory not found: {new_dir}{RESET}"
            except Exception as e:
                return f"{RED}[!] Error changing directory: {e}{RESET}"

        # Execute other shell commands
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"{RED}[!] Error: {e.stderr}{RESET}"

# Get common shell commands
def get_shell_commands():
    return ["ls", "cd", "mkdir", "rm", "cp", "mv", "pwd", "cat", "echo", "grep", "find", "chmod", "ps", "kill"]

# Parse arguments for APKnife commands
def parse_arguments(command, args):
    parser = argparse.ArgumentParser(description=f"APKnife {command} command")
    parser.add_argument("-i", "--input", help="Input APK file", required=True)
    parser.add_argument("-o", "--output", help="Output file/directory")
    parser.add_argument("-c", "--compress", action="store_true", help="Compress output")
    parser.add_argument("--name", help="New app name")
    parser.add_argument("--icon", help="New app icon")
    parser.add_argument("--package", help="New package name")
    try:
        return parser.parse_args(args)
    except SystemExit:
        return None

# Execute APKnife commands
def execute_command(command, args):
    try:
        parsed_args = parse_arguments(command, args)
        if not parsed_args:
            return f"{RED}[!] Invalid arguments for command: {command}{RESET}"

        if command == "extract-dex":
            from apknife.modules.dex_extractor import extract_dex
            dex_files = extract_dex(parsed_args.input, parsed_args.output)
            if dex_files:
                return f"{GREEN}[*] DEX files extracted successfully: {dex_files}{RESET}"
            else:
                return f"{RED}[!] Failed to extract DEX files{RESET}"
        elif command == "decode_manifest":
            from apknife.modules.manifest_decoder import decode_manifest
            decode_manifest(parsed_args.input, parsed_args.output)
            return f"{GREEN}[*] Manifest decoded successfully{RESET}"
        elif command == "waf":
            from apknife.modules.protection_scanner import scan_apk_protections
            protections = scan_apk_protections(parsed_args.input)
            output = ""
            for protection, status in protections.items():
                output += f"{protection}: {'✅' if status else '❌'}\n"
            return output
        elif command == "analyze":
            from apknife.modules.analyzer import analyze_apk
            analyze_apk(parsed_args.input)
            return f"{GREEN}[*] APK analyzed successfully{RESET}"
        elif command == "build":
            from apknife.modules.builder import build_apk
            build_apk(parsed_args.input, parsed_args.output)
            return f"{GREEN}[*] APK built successfully{RESET}"
        elif command == "sign":
            from apknife.modules.signer import sign_apk
            sign_apk(parsed_args.input)
            return f"{GREEN}[*] APK signed successfully{RESET}"
        elif command == "edit-manifest":
            from apknife.modules.manifest_editor import edit_manifest
            edit_manifest(parsed_args.input)
            return f"{GREEN}[*] Manifest edited successfully{RESET}"
        elif command == "smali":
            from apknife.modules.smali_tools import decompile_apk
            decompile_apk(parsed_args.input, parsed_args.output)
            return f"{GREEN}[*] APK decompiled to Smali successfully{RESET}"
        elif command == "find-oncreate":
            from apknife.modules.smali_tools import find_oncreate
            find_oncreate(parsed_args.input)
            return f"{GREEN}[*] onCreate methods found{RESET}"
        elif command == "find-api":
            from apknife.modules.api_finder import find_api_calls
            find_api_calls(parsed_args.input)
            return f"{GREEN}[*] API calls found{RESET}"
        elif command == "scan-vulnerabilities":
            from apknife.modules.vulnerability_scanner import scan_apk
            scan_apk(parsed_args.input)
            return f"{GREEN}[*] Vulnerabilities scanned{RESET}"
        elif command == "scan-permissions":
            from apknife.modules.permission_scanner import scan_permissions
            scan_permissions(parsed_args.input)
            return f"{GREEN}[*] Permissions scanned{RESET}"
        elif command == "catch_rat":
            from apknife.modules.catch_rat import analyze_apk_ips
            analyze_apk_ips(parsed_args.input)
            return f"{GREEN}[*] RAT analysis completed{RESET}"
        elif command == "extract-java":
            from apknife.modules.java_extractor import extract_java
            extract_java(parsed_args.input, parsed_args.output, parsed_args.compress)
            return f"{GREEN}[*] Java code extracted{RESET}"
        elif command == "extract-sensitive":
            from apknife.modules.extract_sensitive import extract_sensitive_data
            extract_sensitive_data(parsed_args.input, parsed_args.output or "sensitive_report.json")
            return f"{GREEN}[*] Sensitive data extracted{RESET}"
        elif command == "modify-apk":
            from apknife.modules.apk_modifier import APKModifier
            modifier = APKModifier(parsed_args.input, parsed_args.name, parsed_args.icon, parsed_args.package)
            modifier.run()
            return f"{GREEN}[*] APK modified successfully{RESET}"
        else:
            return f"{RED}[!] Unknown command: {command}{RESET}"
    except Exception as e:
        return f"{RED}[!] Error executing command: {e}{RESET}"

# Interactive shell
def interactive_shell(COMMANDS):
    shell_commands = get_shell_commands()
    completer = WordCompleter(list(COMMANDS.keys()) + shell_commands, ignore_case=True)
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

            # Handle APKnife commands
            if command in COMMANDS:
                if command == "help":
                    print(f"\n{YELLOW}Available Commands:{RESET}")
                    for cmd, desc in COMMANDS.items():
                        print(f"  {GREEN}{cmd.ljust(20)}{RESET} - {WHITE}{desc}{RESET}")
                    print()
                    continue

                if command == "update-commands":
                    COMMANDS = load_commands()
                    completer = WordCompleter(COMMANDS.keys(), ignore_case=True)
                    logging.info(f"{GREEN}[+] Commands updated successfully!{RESET}")
                    continue

                if command == "list-commands":
                    print(f"\n{YELLOW}Current Commands:{RESET}")
                    for cmd, desc in COMMANDS.items():
                        print(f"  {GREEN}{cmd.ljust(20)}{RESET} - {WHITE}{desc}{RESET}")
                    print()
                    continue

                # Execute APKnife commands
                output = execute_command(command, args[1:])
                print(output)

            # Handle shell commands
            else:
                output = execute_shell_command(text)
                print(output)

        except KeyboardInterrupt:
            continue
        except EOFError:
            break

# Main function
def main():
    COMMANDS = load_commands()
    interactive_shell(COMMANDS)

if __name__ == "__main__":
    main()
