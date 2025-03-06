<p align="center">
  <img src="apknife/assets/cover.png" alt="APKnife Cover" width="100%">
</p>
---

APKnife – The Double-Edged Blade of APK Analysis 🔪

Fear the Blade, Trust the Power!

APKnife is an advanced tool for APK analysis, modification, and security auditing. Whether you're a security researcher, penetration tester, or Android developer, APKnife provides powerful features for reverse engineering, decompiling, modifying, and analyzing APK files.


---

🚀 Features & Capabilities

✅ Extract & decompile APKs into readable formats
✅ Modify & repackage APKs effortlessly
✅ Analyze APKs for security vulnerabilities
✅ Edit AndroidManifest.xml & Smali code
✅ Extract Java source code from an APK
✅ Detect Remote Access Trojans (RATs) & malware
✅ Decode binary XML files & scan for API calls
✅ Change APK metadata (icon, name, package name)
✅ Identify security risks like excessive permissions
✅ Sign APKs for smooth installation


---

🔧 Installation

📌 Prerequisites

Ensure you have the following installed on your system:

Python 3.12

Java (JDK 8 or later)

apktool

zipalign

keytool


🛠 Setting Up a Python Virtual Environment

Before installing apknife, it's recommended to set up a Python virtual environment to avoid package conflicts.

1️⃣ Create a Python Virtual Environment:

python3 -m venv venv
source venv/bin/activate  # On Linux/macOS

venv\Scripts\activate  # On Windows

2️⃣ Install Required Packages

Once the virtual environment is activated, install APKnife:

pip install apknife


---

📥 Installing Rust (Required for APKnife)

apknife requires Rust for building. Follow the installation steps based on your OS:

🐧 On Linux:
```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```
Then follow the on-screen instructions.

🍏 On macOS (Using Homebrew):

brew install rust

🖥️ On Windows:

1. Visit rustup.rs and install Rust.


2. Verify installation:


```
rustc --version
```

---

⚠️ Troubleshooting Common Issues

❌ Issue Installing Rust on Termux

Ensure Termux is up to date:

pkg update && pkg upgrade

Install required build tools:

pkg install clang make python rust

❌ Issues Installing APKnife

Rust not installed properly? Ensure it's correctly installed via rustup or your package manager.

Python conflicts? If there are issues with virtual environments, reset it:

```
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```
✅ Verifying Installed Versions

python --version
rustc --version


---

🌍 Setting Up Rust Environment Variables

🐧 On Linux/macOS
```
nano ~/.bashrc # For bash
```
```
nano ~/.zshrc   # For zsh
```
Add this line at the end:

```
export PATH="$HOME/.cargo/bin:$PATH"
```
Apply changes:
```
source ~/.bashrc  # For bash
```
```
source ~/.zshrc   # For zsh
```
🖥️ On Windows

1. Open "Environment Variables" from the Start menu.


2. Edit Path under System Variables and add:


```
C:\Users\<YourUsername>\.cargo\bin
```
3. Click OK and restart your terminal.



Verify the setup:
```
cargo --version
```
```
rustc --version
```


---

📥 Installing APKnife
```
pip install apknife
```


---

📜 Usage

🖥️ Interactive Mode
---
To enter interactive mode, run:
```
python3 apknife.py interactive
```
This will launch a command-line interface for executing APKnife commands.


---

🛠️ Available Commands

🟢 Extract APK Contents
```
python3 apknife.py extract -i target.apk -o extracted/
```
🟢 Modify & Rebuild APK
```
python3 apknife.py build -i
extracted/ -o modified.apk
```
🟢 Sign APK
```
apknife sign -i modified.apk
```
🟢 Analyze APK for Vulnerabilities
```
apknife scan_vulnerabilities -i target.apk
```
🟢 Detect Remote Access Trojans (RATs)
```
apknife catch_rat -i malicious.apk
```
🟢 Extract Java Source Code
```
apknife extract-java -i target.apk -o src_folder
```
🟢 Change APK Name
```
apknife modify-apk --name -i app.apk
```
🟢 Change APK Icon
```
apknife modify-apk --icon new_icon.png -i app.apk
```
🟢 Modify Package Name
```
apknife modify-apk --package com.example.example -i app.apk
```

```
apknife modify-apk --name new_name --package new.package.name --icon anysize.any -o modified_apk.apk
```
🟢 Scan APK Permissions
```
apknife scan_permissions -i target.apk
```
👇help menu👇

---
apknife -h
usage: apknife.py [-h] [-i INPUT] [-o OUTPUT] [-c] [--name NAME] [--icon ICON]
                  [--package PACKAGE]
                  {extract,build,sign,analyze,edit-manifest,smali,decode-xml,find-oncreate,find-api,scan-vulnerabilities,scan-permissions,catch_rat,extract-java,interactive,extract-sensitive,modify-apk}

APKnife: Advanced APK analysis & modification tool

positional arguments:
  {extract,build,sign,analyze,edit-manifest,smali,decode-xml,find-oncreate,find-api,scan-vulnerabilities,scan-permissions,catch_rat,extract-java,interactive,extract-sensitive,modify-apk}
                        Command to execute

options:
  -h, --help            show this help message and exit
  -i, --input INPUT     Input APK file
  -o, --output OUTPUT   Output file/directory
  -c, --compress        Compress extracted Java files into a ZIP archive
  --name NAME           New app name
  --icon ICON           New app icon (resized automatically)
  --package PACKAGE     New package name


⚠️ Legal Disclaimer

This tool is designed for educational and security research purposes only. Unauthorized use of APKnife on third-party applications without permission is illegal. The developers are not responsible for any misuse.


---

📜 License

APKnife is released under the MIT License – You are free to modify and distribute it for legal use.


---

💡 Contributions & Support

🚀 Contributions are welcome! Fork the repo, submit pull requests, and report issues. Let's make APKnife even better!

