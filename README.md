<p align="center">
  <img src="assets/cover.png" alt="APKnife Cover" width="100%">
</p>

APKnife – The Double-Edged Blade of APK Analysis 🔪

Fear the Blade, Trust the Power! 🎨

APKnife is an advanced tool for APK analysis, modification, and security auditing. Whether you're a security researcher, penetration tester, or Android developer, APKnife provides powerful features for reverse engineering, decompiling, modifying, and analyzing APK files.


---

🚀 Features & Capabilities

✅ Extract & Decompile APKs into readable formats
✅ Modify & Repackage APKs effortlessly
✅ Analyze APKs for security vulnerabilities
✅ Edit AndroidManifest.xml & smali code
✅ Extract Java source code from an APK
✅ Detect Remote Access Trojans (RATs) & malware
✅ Decode binary XML files & scan for API calls
✅ Change APK metadata (icon, name, package name)
✅ Identify security risks like excessive permissions
✅ Sign APKs for smooth installation


---

🔧 Installation

📌 Prerequisites:

Ensure you have the following installed on your system:

Python 3.12

Java (JDK 8 or later)

apktool

zipalign

keytool


📥 Clone the Repository & Install Dependencies:
```
git clone https://github.com/elrashedy1992/APKnife.git
cd APKnife
pip install -r requirements.txt
```

---

📜 Usage

1️⃣ Interactive Mode

To enter interactive mode, run:
```
python3 apknife.py interactive
```
This will display a command-line interface where you can execute APKnife commands directly.


---

📌 Available Commands & Usage


---

🛠️ Command Demonstrations

🟢 Extract APK Contents

Extracts an APK into a specified folder for modification.
```
python3 apknife.py extract -i target.apk -o extracted/
```
🟢 Modify and Rebuild APK

After making changes inside the extracted folder, rebuild the APK:
```
python3 apknife.py build -i extracted/ -o modified.apk
```
🟢 Sign an APK

To sign the modified APK before installing it on a device:
```
python3 apknife.py sign -i modified.apk
```
🟢 Analyze APK for Vulnerabilities

Scan an APK for security issues:
```
python3 apknife.py analyze -i target.apk
```
🟢 Detect Remote Access Trojans (RATs)

Identify potential malware and backdoors:
```
python3 apknife.py catch_rat -i malicious.apk
```
🟢 Extract Java Source Code

Decompile and retrieve Java code from an APK:
```
python3 apknife.py extract-java -i target.apk -o src_folder
```
🟢 Change APK Name

Modify the displayed app name inside the APK:
```
python3 apknife.py modify-apk --name -i app.apk
```
🟢 Change APK Icon

Replace the default app icon with a new one:
```
python3 apknife.py modify-apk --icon new_icon.png -i app.apk
```
🟢 Modify Package Name

Change the package name of an APK for customization:
```
python3 apknife.py modify-apk --package com.example.example -i app.apk
```

🟢 scan permissions
```
python3 apknife.py scan_permissions -i target.apk
```

---

⚠️ Legal Disclaimer

This tool is designed for educational and security research purposes only. Unauthorized use of APKnife on third-party applications without permission is illegal. The developers are not responsible for any misuse.


---

📜 License

APKnife is released under the MIT License – You are free to modify and distribute it for legal use.


---

💡 Contributions & Support

Feel free to contribute! Fork the repo, create pull requests, and report issues. 🚀

