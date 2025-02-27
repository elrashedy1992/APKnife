import argparse
import os
import logging
import time
import sys
from modules import extractor, builder, signer, analyzer, manifest_editor, smali_tools, xml_decoder, api_finder, vulnerability_scanner, permission_scanner, catch_rat

# ANSI color codes for styling
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"

logging.basicConfig(level=logging.INFO, format="%(message)s")

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

def benchmark(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        logging.info(f"[+] Execution time for {func.__name__}: {elapsed_time:.4f} seconds")

        with open("benchmark.log", "a") as log_file:
            log_file.write(f"{func.__name__}: {elapsed_time:.4f} seconds\n")

        return result
    return wrapper

def main():
    parser = argparse.ArgumentParser(description="APKnife: Advanced APK analysis & modification tool")

    parser.add_argument("command", choices=["extract", "build", "sign", "analyze", "edit-manifest", "smali", "decode-xml", "find-oncreate", "find-api", "scan-vulnerabilities", "scan-permissions", "catch_rat"], help="Command to execute")
    parser.add_argument("-i", "--input", help="Input APK file", required=True)
    parser.add_argument("-o", "--output", help="Output file/directory")

    args = parser.parse_args()

    try:
        if args.command == "extract":
            benchmark(extractor.extract_apk)(args.input, args.output)
        elif args.command == "build":
            benchmark(builder.build_apk)(args.input, args.output)
        elif args.command == "sign":
            benchmark(signer.sign_apk)(args.input)
        elif args.command == "analyze":
            benchmark(analyzer.analyze_apk)(args.input)
        elif args.command == "edit-manifest":
            benchmark(manifest_editor.edit_manifest)(args.input)
        elif args.command == "smali":
            benchmark(smali_tools.decompile_apk)(args.input, args.output)
        elif args.command == "decode-xml":
            benchmark(xml_decoder.decode_xml)(args.input)
        elif args.command == "find-oncreate":
            benchmark(smali_tools.find_oncreate)(args.input)
        elif args.command == "find-api":
            benchmark(api_finder.find_api_calls)(args.input)
        elif args.command == "scan-vulnerabilities":
            benchmark(vulnerability_scanner.scan_apk)(args.input)
        elif args.command == "scan-permissions":
            permission_scanner.scan_permissions(args.input)
        elif args.command == "catch_rat":
            catch_rat.analyze_apk_ips(args.input)
    except Exception as e:
        logging.error(f"[!] Error: {e}")

if __name__ == "__main__":
    main()
