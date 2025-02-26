import xml.etree.ElementTree as ET, os
def edit_manifest(apk_extracted_dir):
    manifest_path = os.path.join(apk_extracted_dir, "AndroidManifest.xml")
    try:
        tree = ET.parse(manifest_path)
        root = tree.getroot()
        root.attrib["package"] = "com.example.modified"
        tree.write(manifest_path)
        print("✅ AndroidManifest.xml modified successfully!")
    except Exception as e:
        print(f"❌ Error modifying manifest: {e}")
