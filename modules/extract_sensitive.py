import os
import json
import re
import zipfile
import time
from tqdm import tqdm  # شريط تحميل لتحسين تجربة المستخدم

# قائمة الأنماط للبحث عن البيانات الحساسة
PATTERNS = {
    "API Keys": r"(?i)(google_api_key|aws_secret_access_key|firebase_api_key|auth_key)=[\"']?([A-Za-z0-9_\-]+)[\"']?",
    "Passwords": r"(?i)(password|pass|pwd|secret)=[\"']?([A-Za-z0-9@#$%^&+=]{6,})[\"']?",
    "JWT Tokens": r"eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.?[a-zA-Z0-9_-]*",
    "IP Addresses": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "URLs": r"https?://[^\s]+",
    "RSA Keys": r"-----BEGIN RSA PRIVATE KEY-----[\s\S]+?-----END RSA PRIVATE KEY-----",
}

def extract_sensitive_data(apk_file, output_file="report.json", output_format="json"):
    """ استخراج البيانات الحساسة من ملف APK وتحليلها """
    if not os.path.exists(apk_file):
        print("[!] الملف غير موجود: ", apk_file)
        return

    print("[*] جاري استخراج البيانات الحساسة من:", apk_file)

    extracted_data = {}

    # فك ضغط ملف الـ APK
    with zipfile.ZipFile(apk_file, 'r') as apk:
        file_list = apk.namelist()

        for file in tqdm(file_list, desc="🔎 فحص الملفات", unit="ملف"):
            try:
                with apk.open(file) as f:
                    content = f.read().decode(errors="ignore")  # قراءة الملف بتجاهل الأخطاء

                    for category, pattern in PATTERNS.items():
                        matches = re.findall(pattern, content)
                        if matches:
                            extracted_data.setdefault(category, []).extend(matches)
            except Exception as e:
                pass  # تجاهل الأخطاء التي قد تحدث أثناء قراءة الملفات

    if not extracted_data:
        print("[✓] لم يتم العثور على بيانات حساسة في التطبيق.")
        return

    print("\n[+] تم العثور على بيانات حساسة!")

    # حفظ التقرير بتنسيق JSON أو TXT
    if output_format.lower() == "json":
        with open(output_file, "w", encoding="utf-8") as report:
            json.dump(extracted_data, report, indent=4, ensure_ascii=False)
        print(f"[✔] تم حفظ التقرير في: {output_file}")

    elif output_format.lower() == "txt":
        with open(output_file, "w", encoding="utf-8") as report:
            for category, values in extracted_data.items():
                report.write(f"== {category} ==\n")
                for value in values:
                    report.write(f"- {value}\n")
                report.write("\n")
        print(f"[✔] تم حفظ التقرير في: {output_file}")

    else:
        print("[!] تنسيق غير مدعوم! استخدم JSON أو TXT.")

# اختبار الأداة بشكل مباشر
if __name__ == "__main__":
    apk_path = "hello.apk"
    extract_sensitive_data(apk_path, "sensitive_data_report.json", "json")
