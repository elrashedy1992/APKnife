import os
import re

API_LIST = [
    "getDeviceId",
    "getSubscriberId",
    "getSimSerialNumber",
    "getNetworkOperator",
    "getInstalledPackages",
]


def find_api_calls(smali_dir):
    print("🔍 Searching for API calls...")
    for root, _, files in os.walk(smali_dir):
        for file in files:
            if file.endswith(".smali"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read()
                    for api in API_LIST:
                        if api in content:
                            print(f"⚠️ Found {api} in {file}")
