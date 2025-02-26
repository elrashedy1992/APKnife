📌 APKnife - Advanced APK Analysis & Modification Tool

🔹 Version: 2.0
🔹 Author: Mr_Nightmare
🔹 Description: A powerful tool for APK analysis, modification, and security scanning without using apktool.


---

🚀 Features

✅ Extract APK Files – Extracts APK contents for modification
✅ Modify AndroidManifest.xml – Edit package name and permissions
✅ Analyze APK – Retrieves package details and permissions
✅ Decode XML Files – Decrypts AndroidManifest.xml
✅ Find OnCreate Methods – Scans Smali code for onCreate()
✅ Find API Calls – Detects sensitive API calls
✅ Sign APK – Signs modified APKs for installation
✅ Vulnerability Scanner – Detects security flaws in AndroidManifest.xml


---

📥 Installation

🔹 On Linux / Termux

git clone https://github.com/mrnightmare/APKnife.git
cd APKnife
chmod +x apknife.py
chmod +x install.sh
sudo bash install.sh
python3 apknife.py

🔹 Dependencies

Ensure you have the following installed:

Python 3

zip

apksigner

androguard


Install them using:

pip install androguard
pkg install zip apksigner


---

🛠 Usage

Basic Command Structure

python3 apknife.py <command> -i <input.apk> -o <output>


---

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

Run:

python3 apknife.py scan-vulnerabilities -i extracted_app


--
📜 License

MIT License – Free to use and modify with credit to Mr_Nightmare.

🔗 GitHub Repository: APKnife


---

🎭 Enjoy Hacking & Stay Ethical! 🛡


# APKnife
