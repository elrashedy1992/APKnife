import os
import zipfile


def build_apk(input_dir, output_apk):

    with zipfile.ZipFile(output_apk, "w", zipfile.ZIP_DEFLATED) as apk:
        for root, _, files in os.walk(input_dir):
            for file in files:
                file_path = os.path.join(root, file)
                apk.write(file_path, os.path.relpath(file_path, input_dir))
    print(f"✅ APK built: {output_apk}")
