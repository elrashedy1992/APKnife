import os
import shutil
import subprocess
import logging
import tempfile
from typing import List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_apk(apk_path: str, output_dir: str) -> List[str]:
    """Extract APK contents using apktool and return a list of extracted file paths."""
    if not os.path.isfile(apk_path):
        logging.error("APK file does not exist.")
        return []

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            command = f"apktool d -f {apk_path} -o {temp_dir}"
            subprocess.run(command, shell=True, check=True)

            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
            shutil.move(temp_dir, output_dir)

            extracted_files = []
            for root, _, files in os.walk(output_dir):
                for file in files:
                    extracted_files.append(os.path.join(root, file))

            logging.info(f"✅ APK extracted to {output_dir}")
            return extracted_files

    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Error using apktool to extract APK: {e}")
    except Exception as e:
        logging.error(f"❌ General error extracting APK: {e}")

    return []

# Example usage:
# extracted_files = extract_apk("path/to/apkfile.apk", "path/to/output_dir")
