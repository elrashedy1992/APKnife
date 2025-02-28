import argparse
import logging
import sys
from modules.interactive_mode import interactive_shell
from modules import (
    extractor, builder, signer, analyzer, manifest_editor, smali_tools,
    xml_decoder, api_finder, vulnerability_scanner, permission_scanner,
    catch_rat, java_extractor, extract_sensitive
)

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

def main():
    parser = argparse.ArgumentParser(description="APKnife: Advanced APK analysis & modification tool")

    parser.add_argument("command", choices=[
        "extract", "build", "sign", "analyze", "edit-manifest", "smali",
        "decode-xml", "find-oncreate", "find-api", "scan-vulnerabilities",
        "scan-permissions", "catch_rat", "extract-java", "interactive",
        "extract-sensitive"
    ], help="Command to execute")

    parser.add_argument("-i", "--input", help="Input APK file")
    parser.add_argument("-o", "--output", help="Output file/directory")
    parser.add_argument("-c", "--compress", action="store_true", help="Compress extracted Java files into a ZIP archive")

    args = parser.parse_args()

    # Ensure input file is provided for required commands
    if args.command != "interactive" and not args.input:
        logging.error(f"{RED}[!] You must specify an input file using `-i`{RESET}")
        sys.exit(1)

    # Execute the selected command
    try:
        if args.command == "interactive":
            interactive_shell()
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
        elif args.command == "decode-xml":
            xml_decoder.decode_xml(args.input)
        elif args.command == "find-oncreate":
            smali_tools.find_oncreate(args.input)
        elif args.command == "find-api":
            api_finder.find_api_calls(args.input)
        elif args.command == "scan-vulnerabilities":
            vulnerability_scanner.scan_apk(args.input)  # ✅ استدعاء موديول الفحص
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
        else:
            logging.error(f"{RED}[!] Unknown command!{RESET}")
    except Exception as e:
        logging.error(f"{RED}[!] Error executing `{args.command}`: {e}{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
