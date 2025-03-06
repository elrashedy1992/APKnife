import os
import logging
import traceback
from androguard.core.apk import APK

# Configure logging for clear debugging messages
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def extract_dex(apk_path, output_dir=None):
    """
    Extract DEX files from an APK without fully decompiling it.
    
    :param apk_path: Path to the APK file.
    :param output_dir: Directory to save the extracted DEX files (default: "extracted_dex").
    :return: List of paths to the extracted DEX files.
    """
    try:
        if not os.path.isfile(apk_path):
            logging.error(f"File '{apk_path}' does not exist!")
            return []

        # Set output directory
        if not output_dir:
            output_dir = os.path.join(os.getcwd(), "extracted_dex")
        os.makedirs(output_dir, exist_ok=True)

        logging.info(f"Loading APK: {apk_path}")
        apk = APK(apk_path)

        # Validate APK
        if not apk.is_valid_APK():
            logging.error(f"Invalid APK file: {apk_path}")
            return []

        # Attempt to extract all DEX files
        dex_files = apk.get_all_dex()
        if not dex_files:
            logging.warning("No DEX files found using 'get_all_dex()'! Trying 'get_dex()' instead...")
            dex_data = apk.get_dex()
            if dex_data:
                dex_files = [dex_data]  # Convert single DEX data to a list
            else:
                logging.error("Failed to extract DEX files! The APK may be encrypted or protected.")
                return []

        # Save extracted DEX files
        extracted_files = []
        for i, dex in enumerate(dex_files):
            dex_filename = f"classes{'' if i == 0 else i + 1}.dex"
            dex_path = os.path.join(output_dir, dex_filename)
            with open(dex_path, "wb") as f:
                f.write(dex)
            extracted_files.append(dex_path)
            logging.info(f"Extracted {dex_filename} to {dex_path}")

        return extracted_files

    except Exception as e:
        logging.error(f"Error while extracting DEX files: {e}")
        traceback.print_exc()
        return []
