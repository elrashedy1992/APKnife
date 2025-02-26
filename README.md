# 📌 APKnife - Advanced APK Analysis & Modification Tool

<p align="center">
  <img src="assets/cover.png" alt="APKnife Cover" width="100%">
</p>

🔹 **Version:** 2.0  
🔹 **Author:** Mr_Nightmare  
🔹 **Description:** A powerful tool for APK analysis, modification, and security scanning without using apktool.

---

## 🚀 Features

✅ **Extract APK Files** – Extracts APK contents for modification  
✅ **Modify AndroidManifest.xml** – Edit package name and permissions  
✅ **Analyze APK** – Retrieves package details and permissions  
✅ **Decode XML Files** – Decrypts AndroidManifest.xml  
✅ **Find OnCreate Methods** – Scans Smali code for `onCreate()`  
✅ **Find API Calls** – Detects sensitive API calls  
✅ **Sign APK** – Signs modified APKs for installation  
✅ **Vulnerability Scanner** – Detects security flaws in `AndroidManifest.xml`

---

## 📥 Installation

### 🔹 On Linux / Termux
```sh
git clone https://github.com/elrashedy1992/APKnife.git
cd APKnife
chmod +x apknife.py
chmod +x install.sh
sudo bash install.sh
python3 apknife.py
```
🔹 Dependencies

Ensure you have the following installed:

pip install androguard
kalilinux/parrot
sudo apt install androguard
pkg install zip apksigner



---

🛠 Usage

Basic Command Structure

python3 apknife.py -i <input.apk> -o

🎯 Examples

🔹 Extract APK

python3 apknife.py extract -i app.apk -o extracted_app

🔹 Modify Manifest

python3 apknife.py edit-manifest -i extracted_app

🔹 Analyze APK

python3 apknife.py analyze -i facebook.apk

🔹 Sign APK

python3 apknife.py sign -i modified.apk


---

🛡 Security Scanner

🔍 Scans APKs for:
✔️ android:debuggable="true"
✔️ android:allowBackup="true"

python3 apknife.py scan-vulnerabilities -i extracted_app


---

📜 License

MIT License – Free to use and modify with credit to Mr_Nightmare.

