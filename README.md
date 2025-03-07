```
# APKnife: The Cyber Blade of APK Domination 🔪🧸

<p align="center">
  <img src="apknife/assets/cover.png" alt="APKnife Cover" width="100%">
</p>

APKnife – The Double-Edged Blade of APK Analysis 🔪

Fear the Blade, Trust the Power!

APKnife is an advanced tool for APK analysis, modification, and security auditing. Whether you're a security researcher, penetration tester, or Android developer, APKnife provides powerful features for reverse engineering, decompiling, modifying, and analyzing APK files.

---

## 🚀 Features & Capabilities

- ✅ Extract & decompile APKs into readable formats
- ✅ Modify & repackage APKs effortlessly
- ✅ Analyze APKs for security vulnerabilities
- ✅ Edit AndroidManifest.xml & Smali code
- ✅ Extract Java source code from an APK
- ✅ Detect Remote Access Trojans (RATs) & malware
- ✅ Decode binary XML files & scan for API calls
- ✅ Change APK metadata (icon, name, package name)
- ✅ Identify security risks like excessive permissions
- ✅ Sign APKs for smooth installation

---

## 🔧 Installation

### 📌 Prerequisites

Ensure you have the following installed on your system:

- **Python 3.12**
- **Java (JDK 8 or later)**
- **apktool**
- **zipalign**
- **keytool**

### 🛠 Setting Up a Python Virtual Environment

Before installing APKnife, it's recommended to set up a Python virtual environment to avoid package conflicts.

1️⃣ **Create a Python Virtual Environment:**

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate  # On Windows
```

2️⃣ **Install Required Packages**

Once the virtual environment is activated, install APKnife:

```bash
pip install apknife
```

---

## 📥 Installing Rust (Required for APKnife)

APKnife requires Rust for building. Follow the installation steps based on your OS:

### 🐧 On Linux:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Then follow the on-screen instructions.

### 🍏 On macOS (Using Homebrew):

```bash
brew install rust
```

### 🖥️ On Windows:

1. Visit [rustup.rs](https://rustup.rs/) and install Rust.
2. Verify installation:

```bash
rustc --version
```

---

## ⚠️ Troubleshooting Common Issues

### ❌ Issue Installing Rust on Termux

Ensure Termux is up to date:

```bash
pkg update && pkg upgrade
```

Install required build tools:

```bash
pkg install clang make python rust
```

### ❌ Issues Installing APKnife

- **Rust not installed properly?** Ensure it's correctly installed via rustup or your package manager.
- **Python conflicts?** If there are issues with virtual environments, reset it:

```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

### ✅ Verifying Installed Versions

```bash
python --version
rustc --version
```

---

## 🌍 Setting Up Rust Environment Variables

### 🐧 On Linux/macOS

```bash
nano ~/.bashrc # For bash
nano ~/.zshrc   # For zsh
```

Add this line at the end:

```bash
export PATH="$HOME/.cargo/bin:$PATH"
```

Apply changes:

```bash
source ~/.bashrc  # For bash
source ~/.zshrc   # For zsh
```

### 🖥️ On Windows

1. Open "Environment Variables" from the Start menu.
2. Edit Path under System Variables and add:

```
C:\Users\<YourUsername>\.cargo\bin
```

3. Click OK and restart your terminal.

Verify the setup:

```bash
cargo --version
rustc --version
```

---

## 📥 Installing APKnife

```bash
pip install apknife
```

---

## 📜 Usage

### 🖥️ Interactive Mode

To enter interactive mode, run:

```bash
python3 apknife.py interactive
```

This will launch a command-line interface for executing APKnife commands.

---

## 🛠️ Available Commands

### 🟢 Extract APK Contents

```bash
python3 apknife.py extract -i target.apk -o extracted/
```

### 🟢 Modify & Rebuild APK

```bash
python3 apknife.py build -i extracted/ -o modified.apk
```

### 🟢 Sign APK

```bash
apknife sign -i modified.apk
```

### 🟢 Analyze APK for Vulnerabilities

```bash
apknife scan_vulnerabilities -i target.apk
```

### 🟢 Detect Remote Access Trojans (RATs)

```bash
apknife catch_rat -i malicious.apk
```

### 🟢 Extract Java Source Code

```bash
apknife extract-java -i target.apk -o src_folder
```

### 🟢 Change APK Name

```bash
apknife modify-apk --name -i app.apk
```

### 🟢 Change APK Icon

```bash
apknife modify-apk --icon new_icon.png -i app.apk
```

### 🟢 Modify Package Name

```bash
apknife modify-apk --package com.example.example -i app.apk
```

### 🟢 Modify Multiple APK Attributes

```bash
apknife modify-apk --name new_name --package new.package.name --icon anysize.any -o modified_apk.apk
```

### 🟢 Scan APK Permissions

```bash
apknife scan_permissions -i target.apk
```

---

## 👇 Help Menu



### 🟢 **Extract APK Contents**
Extract the contents of an APK file.

```bash
python3 apknife.py extract -i target.apk -o extracted/
```

- **`-i`**: Path to the input APK file.
- **`-o`**: Directory to save the extracted files.

---

### 🟢 **Build APK**
Rebuild an APK from extracted files.

```bash
python3 apknife.py build -i extracted/ -o modified.apk
```

- **`-i`**: Directory containing the extracted files.
- **`-o`**: Path to save the rebuilt APK.

---

### 🟢 **Sign APK**
Sign an APK file.

```bash
apknife sign -i modified.apk
```

- **`-i`**: Path to the APK file to sign.

---

### 🟢 **Analyze APK**
Analyze an APK for security vulnerabilities.

```bash
apknife analyze -i target.apk
```

- **`-i`**: Path to the APK file to analyze.

---

### 🟢 **Edit Manifest**
Edit the `AndroidManifest.xml` of an APK.

```bash
apknife edit-manifest -i target.apk
```

- **`-i`**: Path to the APK file.

---

### 🟢 **Decompile to Smali**
Decompile an APK to Smali code.

```bash
apknife smali -i target.apk -o smali_output/
```

- **`-i`**: Path to the APK file.
- **`-o`**: Directory to save the decompiled Smali code.

---

### 🟢 **Decode Manifest**
Decode the `AndroidManifest.xml` of an APK.

```bash
apknife decode_manifest -i target.apk -o output_dir/
```

- **`-i`**: Path to the APK file.
- **`-o`**: Directory to save the decoded manifest.

---

### 🟢 **Find onCreate Methods**
Find `onCreate` methods in an APK.

```bash
apknife find-oncreate -i target.apk
```

- **`-i`**: Path to the APK file.

---

### 🟢 **Find API Calls**
Find API calls in an APK.

```bash
apknife find-api -i target.apk
```

- **`-i`**: Path to the APK file.

---

### 🟢 **Scan for Vulnerabilities**
Scan an APK for vulnerabilities.

```bash
apknife scan-vulnerabilities -i target.apk
```

- **`-i`**: Path to the APK file.

---

### 🟢 **Scan Permissions**
Scan and list permissions used by an APK.

```bash
apknife scan-permissions -i target.apk
```

- **`-i`**: Path to the APK file.

---

### 🟢 **Catch RAT**
Analyze an APK for Remote Access Trojan (RAT) indicators.

```bash
apknife catch_rat -i malicious.apk
```

- **`-i`**: Path to the APK file.

---

### 🟢 **Extract Java Source Code**
Extract Java source code from an APK.

```bash
apknife extract-java -i target.apk -o src_folder/
```

- **`-i`**: Path to the APK file.
- **`-o`**: Directory to save the extracted Java source code.

---

### 🟢 **Extract Sensitive Data**
Extract sensitive data from an APK.

```bash
apknife extract-sensitive -i target.apk -o sensitive_data.json
```

- **`-i`**: Path to the APK file.
- **`-o`**: Path to save the extracted sensitive data (JSON format).

---

### 🟢 **Modify APK Metadata**
Modify an APK's metadata (name, icon, package name).

```bash
apknife modify-apk -i target.apk --name "New App Name" --icon new_icon.png --package com.new.package
```

- **`-i`**: Path to the APK file.
- **`--name`**: New app name.
- **`--icon`**: Path to the new icon (any size/format).
- **`--package`**: New package name.

---

### 🟢 **Extract DEX Files**
Extract DEX files from an APK.

```bash
apknife extract-dex -i target.apk -o dex_output/
```

- **`-i`**: Path to the APK file.
- **`-o`**: Directory to save the extracted DEX files.

---

### 🟢 **Scan for Protection Mechanisms**
Scan an APK for protection mechanisms (e.g., Firewall, ProGuard).

```bash
apknife waf -i target.apk
```

- **`-i`**: Path to the APK file.

---

### 🟢 **Interactive Mode**
Launch APKnife in interactive mode.

```bash
python3 apknife.py interactive
```

---

### 🟢 **Help Menu**
Display the help menu with all available commands.

```
apknife -h
```

---

### 🟢 **Update Commands**
Reload the commands from the external file.

```
apknife update-commands
```

---

### 🟢 **List Commands**
Display the current list of available commands.

```
apknife list-commands
```

---

### 🟢 **Exit Interactive Mode**
Exit the interactive shell.

```
exit
```

---

## ⚠️ Legal Disclaimer

This tool is designed for educational and security research purposes only. Unauthorized use of APKnife on third-party applications without permission is illegal. The developers are not responsible for any misuse.

---

## 📜 License

APKnife is released under the MIT License – You are free to modify and distribute it for legal use.

---

## 💡 Contributions & Support

🚀 Contributions are welcome! Fork the repo, submit pull requests, and report issues. Let's make APKnife even better!

---

**APKnife – The Double-Edged Blade of APK Analysis 🔪🧸**

All rights reserved to **MR_nightmare**.
``` 
