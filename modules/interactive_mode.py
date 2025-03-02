import json
import logging
import os
import subprocess
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
            "list-commands": "Displays the current list of available commands"
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
import os

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

                # Handle other APKnife commands here...
                # (Keep the existing command execution logic)

            # Handle shell commands
            else:
                output = execute_shell_command(text)
                print(output)

        except KeyboardInterrupt:
            continue
        except EOFError:
            break
