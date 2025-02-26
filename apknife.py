import argparse
import os
import logging
from modules import extractor, builder, signer, analyzer, manifest_editor, smali_tools, xml_decoder, api_finder, vulnerability_scanner

logging.basicConfig(level=logging.INFO, format="%(message)s")
BANNER = r"""
   ___      _  __      _
  / _ \__ _(_)/ _| ___| |_ _ __
 | | | / _` | | |_ / _ \ __| '__|
 | |_| | (_| | |  _|  __/ |_| |
  \___/ \__,_|_|_|  \___|\__|_|  v2.0
-------------------------------------
 APK modification tool (without apktool)
 Created by mr_nightmare
"""

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="APKnife: Advanced APK analysis & modification tool")

    parser.add_argument("command", choices=["extract", "build", "sign", "analyze", "edit-manifest", "smali", "decode-xml", "find-oncreate", "find-api", "scan-vulnerabilities"], help="Command to execute")
    parser.add_argument("-i", "--input", help="Input APK file")
    parser.add_argument("-o", "--output", help="Output file/directory")

    args = parser.parse_args()

    if args.command == "extract":
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
        vulnerability_scanner.scan_apk(args.input)

if __name__ == "__main__":
    main()
