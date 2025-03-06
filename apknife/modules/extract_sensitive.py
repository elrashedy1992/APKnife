import csv
import json
import os
import re
import subprocess
import zipfile
from concurrent.futures import ThreadPoolExecutor

from androguard.misc import AnalyzeAPK
from tqdm import tqdm

# أنماط البحث عن البيانات الحساسة
PATTERNS = {
    "API Keys": r"(?i)(google_api_key|aws_secret_access_key|firebase_api_key|auth_key)=[\"']?([A-Za-z0-9_\-]+)[\"']?",
    "Passwords": r"(?i)(password|pass|pwd|secret)=[\"']?([A-Za-z0-9@#$%^&+=]{6,})[\"']?",
    "JWT Tokens": r"eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.?[a-zA-Z0-9_-]*",
    "IP Addresses": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "URLs": r"https?://[^\s]+",
    "RSA Keys": r"-----BEGIN RSA PRIVATE KEY-----[\s\S]+?-----END RSA PRIVATE KEY-----",
}


def analyze_dex_files(apk_file):
    """تحليل ملفات DEX داخل APK"""
    print("[+] Analyzing DEX files for potential vulnerabilities...")
    a, d, dx = AnalyzeAPK(apk_file)

    for cls in dx.get_classes():
        print(f" - {cls}")


def scan_shared_preferences(apk_path):

    with zipfile.ZipFile(apk_path, "r") as apk:
        for file in apk.namelist():
            if "shared_prefs" in file and file.endswith(".xml"):
                with apk.open(file) as f:
                    content = f.read().decode(errors="ignore")
                    if "password" in content or "api_key" in content:
                        print(f"[!] Sensitive data found in: {file}")


def process_file(file, apk, extracted_data):

    try:
        with apk.open(file) as f:
            content = f.read().decode(errors="ignore")

            for category, pattern in PATTERNS.items():
                matches = re.findall(pattern, content)
                if matches:
                    extracted_data.setdefault(category, []).extend(matches)
    except Exception:
        pass


def save_report_json(extracted_data, output_file):

    with open(output_file, "w", encoding="utf-8") as report:
        json.dump(extracted_data, report, indent=4, ensure_ascii=False)
    print(f"[✔] Report saved in: {output_file}")


def extract_sensitive_data(apk_file, output_file="sensitive_report.json"):

    if not os.path.exists(apk_file):
        print("[!] File not found:", apk_file)
        return

    print("[*] Extracting sensitive data from:", apk_file)
    extracted_data = {}

    with zipfile.ZipFile(apk_file, "r") as apk:
        file_list = apk.namelist()

        with ThreadPoolExecutor() as executor:
            for file in tqdm(file_list, desc="🔎 Scanning files", unit="file"):
                executor.submit(process_file, file, apk, extracted_data)

    analyze_dex_files(apk_file)

    scan_shared_preferences(apk_file)

    if not extracted_data:
        print("[✓] No sensitive data found in the application.")
        return

    print("\n[+] Sensitive data found!")
    save_report_json(extracted_data, output_file)
