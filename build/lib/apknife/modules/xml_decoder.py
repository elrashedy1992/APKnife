import os
import zipfile
import xml.etree.ElementTree as ET
import subprocess
import sys

def check_and_install_androguard():
    """Check if Androguard is installed, and install it if necessary."""
    try:
        subprocess.run(['androguard', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("❌ Androguard is not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "androguard"])

def extract_manifest_from_apk(apk_file, extract_dir):
    """Extract AndroidManifest.xml from the APK file."""
    with zipfile.ZipFile(apk_file, 'r') as apk_zip:
        if 'AndroidManifest.xml' not in apk_zip.namelist():
            raise FileNotFoundError("❌ AndroidManifest.xml not found inside the APK!")
        apk_zip.extract('AndroidManifest.xml', extract_dir)

def decode_xml(apk_dir, output_file="decoded_manifest.xml"):
    """Decode AndroidManifest.xml and fix its formatting."""
    # Check and install Androguard if necessary
    check_and_install_androguard()

    manifest_path = os.path.join(apk_dir, "AndroidManifest.xml")

    # Check if the file exists in the APK directory
    if not os.path.exists(manifest_path):
        print("❌ AndroidManifest.xml not found!")
        return

    # Extract AndroidManifest.xml if it's not already present in the directory
    try:
        extract_manifest_from_apk(apk_dir, apk_dir)
    except FileNotFoundError as e:
        print(e)
        return
    except Exception as e:
        print(f"❌ Error extracting AndroidManifest.xml: {e}")
        return

    # Decode using Androguard
    try:
        subprocess.run(['androguard', 'axml', '-i', manifest_path, '-o', output_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error decoding the manifest: {e}")
        return

    # Verify the XML format after decoding
    try:
        tree = ET.parse(output_file)
        root = tree.getroot()
        print("✅ AndroidManifest.xml decoded successfully!")
    except ET.ParseError:
        print("❌ Error parsing the decoded AndroidManifest.xml")
        return

    print(f"✅ AndroidManifest.xml decoded and saved to {output_file}")

    # Fix XML formatting after decoding (if needed)
    try:
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        print("✅ Manifest XML formatting fixed successfully!")
    except Exception as e:
        print(f"❌ Error fixing XML formatting: {e}")
        return

# If you want to decode AndroidManifest.xml from multiple APK files in a directory
def decode_all_manifests_in_directory(directory):
    """Decode AndroidManifest.xml from all APK files in the directory."""
    for file in os.listdir(directory):
        if file.endswith(".apk"):
            print(f"\nDecoding AndroidManifest.xml from {file}...")
            decode_xml(os.path.join(directory, file))

if __name__ == "__main__":
    # This code will run only when the script is executed directly
    # Example to decode a single APK
    decode_xml('path_to_apk_directory')

    # Example to decode all APK files in a folder
    # decode_all_manifests_in_directory('path_to_apk_folder')
