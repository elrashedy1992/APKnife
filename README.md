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


## Setting Up a Python Virtual Environment Before Installing `apknife`

Before installing the `apknife` library or any library that depends on Rust, it is recommended to set up a Python virtual environment to avoid package conflicts. You can follow these steps to set up and configure the virtual environment:

### 1. Create a Python Virtual Environment:
```
python3 -m venv venv
source venv/bin/activate
```

# On Linux/macOS
```
venv\Scripts\activate
```
# On Windows

2. Install the Required Packages:

Once the virtual environment is activated, you can install apknife 

Installing Rust

apknife requires Rust for building, so make sure Rust is installed on your system. Below are the installation steps for Rust on different operating systems:

1. On Linux:

To install Rust on Linux, you can use the following command to download and install Rust via rustup:
```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```
After this, follow the on-screen instructions to complete the installation.

2. On macOS:

If you are using macOS, you can install Rust using Homebrew:
```
brew install rust
```
3. On Windows:

For Windows, you can install Rust via rustup:

1. Visit https://rustup.rs and follow the instructions to install rustup, which is the official tool for managing Rust installations.


2. Once installed, you can verify that Rust is installed correctly by running:
```
rustc --version
```


Troubleshooting Common Issues

1. Issue Installing rust on Termux:

Sometimes, users may encounter issues installing rust on Termux due to system environment restrictions. Possible solutions include:

Make sure Termux is up to date:

pkg update && pkg upgrade

Install necessary build tools: Make sure you have installed essential build tools like clang and make:
```
pkg install clang make python
```

2. Issues While Installing apknife:

If you face issues during the installation of apknife or any library that depends on Rust, check the following:

Rust Installation Issues: Ensure you’ve correctly installed rust via rustup or your system’s package manager.

Virtual Environment Conflicts: If there are conflicts between Python environments, delete the old virtual environment and recreate a new one:
```
rm -rf venv
python3 -m venv venv
```
source venv/bin/activate  
```


3. Verifying Installed Versions:

To make sure everything is installed correctly:

Check the Python version:
```
python --version
```
Check the Rust version:
```
rustc --version
```

Additional Notes:

Ensure that all the necessary build tools are installed correctly. If you run into additional issues, refer to the documentation for each library or build tool.

If the problems persist, you can search developer communities or support forums for customized solutions.



Setting the Environment Variable for Rust

After installing Rust using rustup, you need to add the cargo (Rust's package manager) path to the PATH environment variable. You can do this using the following steps:

On Linux/macOS:

1. Open your .bashrc, .zshrc, or the appropriate shell configuration file for your user:

If you use bash:
```
nano ~/.bashrc
```
If you use zsh:
```
nano ~/.zshrc
```


2. Add the following line at the end of the file:
```
export PATH="$HOME/.cargo/bin:$PATH"
```

3. Save the file and exit the editor.


4. Reload the session to apply changes:

For bash:
```
source ~/.bashrc
```
For zsh:
```
source ~/.zshrc
```



On Windows:

1. Open the Environment Variables window by searching for Environment Variables in the Start menu.


2. In the Environment Variables window, select Path under System Variables and click on Edit.


3. Add the following path to the list of paths:
```
C:\Users\<YourUsername>\.cargo\bin
```

4. Click OK to save the changes.



Verify the Installation:

After setting up the environment variable, you can check if cargo and rustc are working correctly by running the following commands:
```
cargo --version
rustc --version
```

you are ready now to use APKnife


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

📌 some of Available Commands & Usage


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

