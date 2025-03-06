import logging
import os
import shutil
import subprocess
import zipfile

# Configure logging to save errors and outputs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="log.txt",
    filemode="a",
)


def is_jadx_installed():
    """Check if JADX is installed on the system."""
    return shutil.which("jadx") is not None


def extract_java(apk_path, output_dir="extracted_java", compress=False):
    """Extract Java files from an APK using JADX."""

    if not os.path.exists(apk_path):
        logging.error(f"[!] APK file not found: {apk_path}")
        return

    if not is_jadx_installed():
        logging.error(
            "[!] JADX is not installed! Please install it using: sudo apt install jadx or download it from https://github.com/skylot/jadx"
        )
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    logging.info(f"[+] Extracting Java files from {apk_path} to {output_dir}")

    # Unzip APK to extract DEX files
    with zipfile.ZipFile(apk_path, "r") as zip_ref:
        zip_ref.extractall(output_dir)

    dex_files = [f for f in os.listdir(output_dir) if f.endswith(".dex")]
    if not dex_files:
        logging.warning("[!] No DEX files found in the APK!")
        return

    # Create an output directory for Java sources
    jadx_output = os.path.join(output_dir, "java_sources")
    os.makedirs(jadx_output, exist_ok=True)

    # Run JADX to process all DEX files at once
    dex_paths = [os.path.join(output_dir, dex) for dex in dex_files]
    logging.info(f"[+] Converting all DEX files to Java at once...")

    try:
        subprocess.run(["jadx", "-d", jadx_output] + dex_paths, check=True)
        logging.info("[✔] Java files extracted successfully!")
    except subprocess.CalledProcessError as e:
        logging.error(f"[!] JADX execution failed: {e}")

    # Compress output if requested
    if compress:
        compress_output(jadx_output)


def compress_output(output_dir):
    """Compress extracted Java files into a ZIP archive."""
    zip_file = os.path.join(output_dir, "java_sources.zip")
    logging.info(f"[+] Compressing files into {zip_file}")

    with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, output_dir))

    logging.info(f"[✔] Compressed files saved in {zip_file}")
