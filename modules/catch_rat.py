import os
import re
import requests
import subprocess
import json
from modules.extractor import extract_apk

def extract_ips_from_apk(apk_path):
    """Extract all suspicious IPs from the APK files."""
    output_dir = "temp_extracted_apk"
    extracted_files = extract_apk(apk_path, output_dir)

    if not extracted_files:
        print("❌ Extraction failed or no files found.")
        return []

    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    found_ips = set()

    for file_path in extracted_files:
        if not os.path.isfile(file_path):
            continue  # تخطي المجلدات

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                matches = ip_pattern.findall(content)
                found_ips.update(matches)
        except Exception as e:
            print(f"❌ Failed to read {file_path}: {e}")

    return list(found_ips)

def get_ip_info(ip):
    """Fetch IP information using ipinfo.io."""
    url = f"https://ipinfo.io/{ip}/json"
    try:
        response = requests.get(url)
        data = response.json()
        print(f"\n📡 IP: {ip} Information:")
        print(json.dumps(data, indent=4))
        return data
    except requests.RequestException as e:
        print(f"❌ Failed to fetch IP info: {e}")
        return None

def run_whois(ip):
    """Run WHOIS lookup for the given IP address."""
    try:
        result = subprocess.run(["whois", ip], capture_output=True, text=True)
        print(f"\n🔍 WHOIS Information for {ip}:")
        print(result.stdout)
    except FileNotFoundError:
        print("❌ WHOIS command not found. Please install it first.")
    except Exception as e:
        print(f"❌ Failed to run WHOIS: {e}")

def analyze_apk_ips(apk_path):
    """Extract and analyze suspicious IPs from APK."""
    ips = extract_ips_from_apk(apk_path)
    if not ips:
        print("✅ No suspicious IPs found in APK.")
        return

    print("\n🔎 Found Suspicious IPs:")
    for ip in ips:
        print(f"  - {ip}")
        get_ip_info(ip)
        run_whois(ip)
