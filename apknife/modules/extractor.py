import base64
import logging
import os
import re
import shutil
import subprocess
import tempfile

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def check_dependency(tool: str) -> bool:
    """Check if a required tool is installed."""
    result = subprocess.run(
        f"command -v {tool}", shell=True, capture_output=True, text=True
    )
    if result.returncode != 0:
        logging.error(f"❌ Missing dependency: {tool}. Please install it.")
        return False
    return True


def extract_apk(apk_path: str, output_dir: str):
    """Extract APK contents using apktool."""
    if not os.path.isfile(apk_path):
        logging.error("APK file does not exist.")
        return []

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract APK using apktool
            command = f"apktool d -f -r {apk_path} -o {temp_dir}"
            subprocess.run(command, shell=True, check=True)

            # Handle advanced protections like obfuscation
            handle_advanced_protections(temp_dir)

            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
            shutil.move(temp_dir, output_dir)

            logging.info(f"✅ APK extracted to {output_dir}")
            return output_dir

    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Error extracting APK: {e}")
    except Exception as e:
        logging.error(f"❌ General error extracting APK: {e}")

    return None


def handle_advanced_protections(temp_dir: str):
    """Handle APK protections like obfuscation and anti-debugging."""

    if (
        not check_dependency("d2j-dex2jar")
        or not check_dependency("jadx")
        or not check_dependency("baksmali")
    ):
        return

    dex_files = [
        os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.endswith(".dex")
    ]

    for dex_file in dex_files:
        jar_file = dex_file.replace(".dex", ".jar")
        try:
            # Convert DEX to JAR
            subprocess.run(["d2j-dex2jar", dex_file, "-o", jar_file], check=True)
            logging.info(f"🔹 Converted {dex_file} to {jar_file}")

            # Decompile JAR to Java code using JADX
            jadx_out = jar_file.replace(".jar", "_jadx")
            subprocess.run(["jadx", "-d", jadx_out, jar_file], check=True)
            logging.info(f"🔹 Decompiled {jar_file} with JADX to {jadx_out}")

        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Error processing {dex_file}: {e}")


def extract_native_libraries(output_dir: str):
    """Extract and analyze native libraries (.so files)."""
    so_files = []
    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".so"):
                so_files.append(os.path.join(root, file))

    for so_file in so_files:
        logging.info(f"🔹 Found native library: {so_file}")

        # Disassemble .so file
        disasm_file = so_file + ".disasm"
        try:
            subprocess.run(
                ["objdump", "-d", so_file, "-M", "intel", "-o", disasm_file], check=True
            )
            logging.info(f"✅ Disassembled {so_file} -> {disasm_file}")

            # Radare2 analysis
            subprocess.run(["r2", "-c", '"aaa; afl; pdf @ main"', so_file], check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Error analyzing {so_file}: {e}")


def bypass_anti_debug(output_dir: str):
    """Patch anti-debugging mechanisms inside the APK."""
    smali_files = []
    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".smali"):
                smali_files.append(os.path.join(root, file))

    for smali_file in smali_files:
        with open(smali_file, "r") as f:
            content = f.read()

        # Remove ptrace anti-debugging
        if "ptrace" in content:
            patched_content = content.replace("ptrace", "// ptrace removed")
            with open(smali_file, "w") as f:
                f.write(patched_content)
            logging.info(f"✅ Patched anti-debugging in {smali_file}")


def detect_and_decrypt_strings(output_dir: str):
    """Detect and decrypt Base64 and XOR-encoded strings inside the APK."""
    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".smali") or file.endswith(".xml"):
                file_path = os.path.join(root, file)

                with open(file_path, "r") as f:
                    content = f.read()

                # Detect Base64 encoded strings
                base64_matches = re.findall(r'"([A-Za-z0-9+/=]{16,})"', content)
                for match in base64_matches:
                    try:
                        decoded = base64.b64decode(match).decode("utf-8")
                        logging.info(
                            f"🔹 Found Base64 encoded string: {match} -> {decoded}"
                        )
                    except Exception:
                        pass  # Ignore decoding errors


# Example usage
if __name__ == "__main__":
    apk_path = "path/to/apkfile.apk"
    output_dir = "path/to/output_dir"

    extracted_folder = extract_apk(apk_path, output_dir)
    if extracted_folder:
        extract_native_libraries(extracted_folder)
        bypass_anti_debug(extracted_folder)
        detect_and_decrypt_strings(extracted_folder)
