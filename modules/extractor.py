import zipfile, os
def extract_apk(apk_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    with zipfile.ZipFile(apk_path,'r') as apk:
        apk.extractall(output_dir)
    print(f"✅ APK extracted to {output_dir}")
