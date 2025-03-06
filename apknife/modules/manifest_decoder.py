import logging
from xml.dom import minidom
from lxml import etree
from androguard.core.apk import APK

# ANSI color codes for terminal output styling
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def decode_manifest(apk_path, output_path=None):
    try:
        # Load the APK file
        apk = APK(apk_path)
        
        # Get the AndroidManifest.xml content as an lxml.etree._Element object
        manifest = apk.get_android_manifest_xml()
        
        # Convert the lxml.etree._Element object to a string
        manifest_str = etree.tostring(manifest, encoding="utf-8", pretty_print=True).decode("utf-8")
        
        # Use minidom to further prettify the XML
        parsed_xml = minidom.parseString(manifest_str)
        pretty_xml = parsed_xml.toprettyxml(indent="  ")
        
        # Save the decoded manifest to a file if output path is provided
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(pretty_xml)
            logging.info(f"{GREEN}[*] Decoded AndroidManifest.xml saved to: {output_path}{RESET}")
        else:
            logging.info(f"{GREEN}[*] Decoded AndroidManifest.xml:{RESET}")
            print(pretty_xml)
        
        return pretty_xml
    
    except Exception as e:
        logging.error(f"{RED}[!] Error decoding AndroidManifest.xml: {e}{RESET}")
        return None
