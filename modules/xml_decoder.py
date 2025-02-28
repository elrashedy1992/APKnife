import os


def decode_xml(apk_dir, output_file="decoded_manifest.xml"):
    manifest_path = os.path.join(apk_dir, "AndroidManifest.xml")
    if not os.path.exists(manifest_path):
        print("❌ AndroidManifest.xml not found!")
        return

    os.system(f"androguard axml -i {manifest_path} -o {output_file}")
    print(f"✅ AndroidManifest.xml decoded successfully and saved to {output_file}!")
