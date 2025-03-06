import os
import subprocess


def decompile_apk(apk_dir, output_dir):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cmd = f"java -jar tools/baksmali.jar d {apk_dir} -o {output_dir}"
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ Smali code extracted to {output_dir}")
    except subprocess.CalledProcessError:
        print("❌ Error during Smali decompilation")


def find_oncreate(smali_dir):
    for root, _, files in os.walk(smali_dir):
        for file in files:
            if file.endswith(".smali"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read()
                    if "onCreate" in content:
                        print(f"✅ Found onCreate in {file}")
