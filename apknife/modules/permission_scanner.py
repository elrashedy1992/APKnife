import logging
import xml.etree.ElementTree as ET
import zipfile

from androguard.core.axml import AXMLPrinter

logging.basicConfig(level=logging.INFO, format="%(message)s")

PERMISSION_CATEGORIES = {
    "normal": {
        "android.permission.ACCESS_WIFI_STATE": "Allows applications to access Wi-Fi networks.",
        "android.permission.ACCESS_NETWORK_STATE": "Allows applications to access networks.",
        "android.permission.SET_WALLPAPER": "Allows setting the wallpaper.",
        "android.permission.CHANGE_WIFI_STATE": "Allows changing Wi-Fi state.",
    },
    "dangerous": {
        "android.permission.ACCESS_FINE_LOCATION": "Precise location access using GPS.",
        "android.permission.ACCESS_COARSE_LOCATION": "Approximate location access using network sources.",
        "android.permission.CALL_PHONE": "Initiate a phone call without user interaction.",
        "android.permission.READ_CONTACTS": "Read user contacts data.",
        "android.permission.WRITE_CONTACTS": "Write user contacts data.",
        "android.permission.RECORD_AUDIO": "Record audio using the microphone.",
        "android.permission.CAMERA": "Access the camera for photos and videos.",
        "android.permission.READ_SMS": "Read SMS messages.",
        "android.permission.SEND_SMS": "Send SMS messages.",
        "android.permission.RECEIVE_SMS": "Receive SMS messages.",
        "android.permission.READ_CALL_LOG": "Read the user's call log.",
        "android.permission.WRITE_CALL_LOG": "Modify the user's call log.",
        "android.permission.READ_PHONE_STATE": "Read phone state information.",
    },
    "critical": {
        "android.permission.WRITE_SETTINGS": "Modify system settings, which can be dangerous.",
        "android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS": "Ignore battery optimizations, potentially draining battery.",
        "android.permission.RECEIVE_BOOT_COMPLETED": "Start after boot, potentially for persistent background execution.",
        "android.permission.INTERNET": "Access the internet, often used for external communication.",
        "android.permission.WRITE_EXTERNAL_STORAGE": "Write to external storage, potentially exposing user data.",
    },
}


def extract_manifest(apk_path):
    """Extracts and decodes AndroidManifest.xml from the APK file."""
    try:
        with zipfile.ZipFile(apk_path, "r") as apk:
            manifest_data = apk.read("AndroidManifest.xml")
            decoded_manifest = AXMLPrinter(manifest_data).get_xml()
            return decoded_manifest
    except Exception as e:
        logging.error(f"❌ Failed to extract AndroidManifest.xml: {e}")
        return None


def parse_permissions(manifest_data):
    """Parses permissions from decoded AndroidManifest.xml."""
    try:
        root = ET.fromstring(manifest_data)
        permissions = {
            elem.attrib["{http://schemas.android.com/apk/res/android}name"]
            for elem in root.findall(".//uses-permission")
        }
        return list(permissions)
    except Exception as e:
        logging.error(f"❌ Failed to parse permissions: {e}")
        return []


def classify_permissions(permissions):
    """Classifies permissions into normal, dangerous, critical, and unknown."""
    categorized = {"normal": [], "dangerous": [], "critical": [], "unknown": []}

    for perm in permissions:
        found = False
        for category, perms in PERMISSION_CATEGORIES.items():
            if perm in perms:
                categorized[category].append(
                    (perm, perms[perm])
                )  # Store with description
                found = True
                break
        if not found:
            categorized["unknown"].append(
                (perm, "Unknown permission - may require further analysis.")
            )

    return categorized


def display_permissions(permissions):
    """Displays classified permissions with descriptions."""
    categorized = classify_permissions(permissions)

    print("\n✅ **Permissions Found:**\n")

    if categorized["normal"]:
        print("🔵 **Normal Permissions:**")
        for perm, desc in categorized["normal"]:
            print(f"  - {perm}: {desc}")

    if categorized["dangerous"]:
        print("\n🟠 **Dangerous Permissions:**")
        for perm, desc in categorized["dangerous"]:
            print(f"  - {perm}: {desc}")

    if categorized["critical"]:
        print("\n🔴 **Critical Permissions:**")
        for perm, desc in categorized["critical"]:
            print(f"  - {perm}: {desc}")

    if categorized["unknown"]:
        print("\n⚠️ **Unknown Permissions:** (Might need further analysis)")
        for perm, desc in categorized["unknown"]:
            print(f"  - {perm}: {desc}")


def scan_permissions(apk_path):
    """Scans APK for permissions and analyzes their risks."""
    print(f"\n🔍 Scanning permissions in: {apk_path}")

    manifest_data = extract_manifest(apk_path)
    if not manifest_data:
        return

    permissions = parse_permissions(manifest_data)
    if not permissions:
        logging.warning("⚠️ No permissions found in AndroidManifest.xml.")
        return

    display_permissions(permissions)
