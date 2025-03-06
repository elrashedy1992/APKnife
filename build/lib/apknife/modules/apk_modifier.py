import os
import shutil
import subprocess
import sys
import re
from PIL import Image

class APKModifier:
    def __init__(self, apk_path=None, new_name=None, icon_path=None, new_package=None):
        self.apk_path = apk_path
        self.new_name = new_name
        self.icon_path = icon_path
        self.new_package = new_package
        self.decompiled_dir = "decompiled_apk"
        self.output_apk = "modified.apk"
        self.icon_sizes = {
            "mipmap-mdpi": (48, 48),
            "mipmap-hdpi": (72, 72),
            "mipmap-xhdpi": (96, 96),
            "mipmap-xxhdpi": (144, 144),
            "mipmap-xxxhdpi": (192, 192),
        }

    def decompile_if_needed(self):
        """Decompile the APK if it's not already decompiled."""
        if not os.path.isdir(self.apk_path):
            print("[*] APK detected, decompiling...")
            if os.path.exists(self.decompiled_dir):
                shutil.rmtree(self.decompiled_dir)
            subprocess.run(["apktool", "d", self.apk_path, "-o", self.decompiled_dir], check=True)
            self.apk_path = self.decompiled_dir
        else:
            print("[*] Using existing decompiled directory.")

    def modify_app_name(self):
        """Modify the app name inside AndroidManifest.xml"""
        if not self.new_name:
            return

        print(f"[*] Changing app name to: {self.new_name}")
        manifest_path = os.path.join(self.apk_path, "AndroidManifest.xml")

        with open(manifest_path, "r", encoding="utf-8") as file:
            content = file.read()

        content = re.sub(r'android:label="([^"]+)"', f'android:label="{self.new_name}"', content)

        with open(manifest_path, "w", encoding="utf-8") as file:
            file.write(content)

    def modify_icon(self):
        """Replace the app icon with automatic resizing and format conversion."""
        if not self.icon_path:
            return
        
        print(f"[*] Changing app icon using: {self.icon_path}")
        try:
            icon = Image.open(self.icon_path).convert("RGBA")  # Ensuring transparency support
        except Exception as e:
            print(f"[!] Error loading icon: {e}")
            return

        # Convert to PNG if necessary
        if not self.icon_path.lower().endswith(".png"):
            self.icon_path = self.icon_path.rsplit(".", 1)[0] + ".png"
            icon.save(self.icon_path, "PNG")
            print(f"[*] Converted icon to PNG: {self.icon_path}")

        for res_dir, size in self.icon_sizes.items():
            icon_resized = icon.resize(size, Image.ANTIALIAS)
            icon_path = os.path.join(self.apk_path, "res", res_dir, "ic_launcher.png")
            if os.path.exists(icon_path):
                icon_resized.save(icon_path, "PNG")
                print(f"[*] Icon resized and saved to: {icon_path}")

    def modify_package_name(self):
        """Modify Package Name in AndroidManifest.xml and smali files."""
        if not self.new_package:
            return
        
        print(f"[*] Changing package name to: {self.new_package}")
        manifest_path = os.path.join(self.apk_path, "AndroidManifest.xml")

        with open(manifest_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Extract the current package name
        old_package_match = re.search(r'package="([^"]+)"', content)
        if not old_package_match:
            print("[!] Package name not found!")
            return

        old_package = old_package_match.group(1)
        content = content.replace(old_package, self.new_package)

        with open(manifest_path, "w", encoding="utf-8") as file:
            file.write(content)

        # Update package name in smali files
        smali_dir = os.path.join(self.apk_path, "smali")
        if os.path.exists(smali_dir):
            old_package_path = old_package.replace(".", "/")
            new_package_path = self.new_package.replace(".", "/")
            for root, dirs, files in os.walk(smali_dir):
                for file in files:
                    if file.endswith(".smali"):
                        smali_file = os.path.join(root, file)
                        with open(smali_file, "r", encoding="utf-8") as f:
                            smali_content = f.read()
                        smali_content = smali_content.replace(old_package_path, new_package_path)
                        with open(smali_file, "w", encoding="utf-8") as f:
                            f.write(smali_content)

            # Rename package directories in smali
            old_package_dir = os.path.join(smali_dir, *old_package.split("."))
            new_package_dir = os.path.join(smali_dir, *self.new_package.split("."))
            if os.path.exists(old_package_dir):
                shutil.move(old_package_dir, new_package_dir)

    def recompile_if_needed(self):
        """Recompile the APK if it was decompiled."""
        if os.path.isdir(self.apk_path):
            print("[*] Recompiling modified APK...")
            subprocess.run(["apktool", "b", self.apk_path, "-o", self.output_apk], check=True)
            print(f"[✔] Modified APK saved as: {self.output_apk}")

    def run(self):
        self.decompile_if_needed()
        self.modify_app_name()
        self.modify_icon()
        self.modify_package_name()
        self.recompile_if_needed()
        print("[✔] Process completed!")

# Run from command line
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python modifier.py <apk_path_or_decompiled_dir> [--name <new_name>] [--icon <icon_path>] [--package <new_package_name>]")
        sys.exit(1)

    apk_path = sys.argv[1]
    new_name = None
    icon_path = None
    new_package = None

    if "--name" in sys.argv:
        new_name = sys.argv[sys.argv.index("--name") + 1]

    if "--icon" in sys.argv:
        icon_path = sys.argv[sys.argv.index("--icon") + 1]

    if "--package" in sys.argv:
        new_package = sys.argv[sys.argv.index("--package") + 1]

    modifier = APKModifier(apk_path, new_name, icon_path, new_package)
    modifier.run()
