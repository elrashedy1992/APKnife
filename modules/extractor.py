import os
import shutil
import zipfile

def extract_apk(apk_path, output_dir):
    """Extract APK contents and return a list of extracted file paths."""
    try:
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)

        with zipfile.ZipFile(apk_path, 'r') as apk:
            apk.extractall(output_dir)

        extracted_files = []
        for root, _, files in os.walk(output_dir):
            for file in files:
                extracted_files.append(os.path.join(root, file))

        print(f"✅ APK extracted to {output_dir}")
        return extracted_files

    except Exception as e:
        print(f"❌ Error extracting APK: {e}")
        return []

