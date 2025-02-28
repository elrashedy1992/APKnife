# 📌 APKnife - Advanced APK Analysis & Modification Tool

<p align="center">
  <img src="assets/cover.png" alt="APKnife Cover" width="100%">
</p>

🔹 **Version:** 2.0  
🔹 **Author:** Mr_Nightmare  
🔹 **Description:** A powerful tool for APK analysis, modification, and security scanning

---

## 🚀 Features


✅ Extract APK Files – Extracts APK contents for modification


✅ Modify AndroidManifest.xml – Edit package name and permissions


✅ Analyze APK – Retrieves package details and permissions


✅ Decode XML Files – Decrypts AndroidManifest.xml


✅ Find OnCreate Methods – Scans Smali code for onCreate()


✅ Find API Calls – Detects sensitive API calls


✅ Sign APK – Signs modified APKs for installation

✅ Vulnerability Scanner – Detects security flaws AndroidManifest.xml

✅ Scan Permissions – Lists all permissions used by the APK and identifies risky ones


✅ Catch RAT – Detects potential Remote Access Trojans (RATs) by analyzing APK network activity

---

## 📥 Installation

### 🔹 On Linux / Termux
```sh
git clone https://github.com/elrashedy1992/APKnife.git
cd APKnife
chmod +x apknife.py
chmod +x setup.sh
sudo bash setup.sh
pip install -r requirements.txt
python3 apknife.py
```
🔹 Dependencies

Ensure you have the following installed:
```
pip install androguard
```
kalilinux/parrot
```
sudo apt install androguard
sudo apt install install zip apksigner
```


---

🛠 Usage

Basic Command Structure

python3 apknife.py -i <input.apk> -o

🎯 Examples

🔹 Extract APK
```
python3 apknife.py extract -i app.apk -o extracted_app
````
🔹 Modify Manifest
```
python3 apknife.py edit-manifest -i extracted_app
```
🔹 Analyze APK
```
python3 apknife.py analyze -i payload_test.apk

   ___      _  __      _
  / _ \__ _(_)/ _| ___| |_ _ __
 | | | / _` | | |_ / _ \ __| '__|
 | |_| | (_| | |  _|  __/ |_| |
  \___/ \__,_|_|_|  \___|\__|_|  v2.0
-------------------------------------
 APK modification tool 
 Created by mr_nightmare

Starting analysis on AndroidManifest.xml
APK file was successfully validated!
📊 APK Package: com.metasploit.stage
📜 Permissions: android.permission.READ_CONTACTS, android.permission.READ_SMS, android.permission.SEND_SMS, android.permission.CALL_PHONE, android.permission.WRITE_CALL_LOG, android.permission.ACCESS_WIFI_STATE, android.permission.WRITE_CONTACTS, android.permission.ACCESS_NETWORK_STATE, android.permission.ACCESS_FINE_LOCATION, android.permission.WAKE_LOCK, android.permission.SET_WALLPAPER, android.permission.RECEIVE_SMS, android.permission.READ_CALL_LOG, android.permission.WRITE_SETTINGS, android.permission.RECORD_AUDIO, android.permission.RECEIVE_BOOT_COMPLETED, android.permission.ACCESS_COARSE_LOCATION, android.permission.WRITE_EXTERNAL_STORAGE, android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, android.permission.READ_PHONE_STATE, android.permission.CHANGE_WIFI_STATE, android.permission.CAMERA, android.permission.INTERNET
[+] Execution time for analyze_apk: 0.0506 seconds
```
🔹 Sign APK
```
python3 apknife.py sign -i modified.apk
```

```
python3 apknife.py -h

   ___      _  __      _
  / _ \__ _(_)/ _| ___| |_ _ __
 | | | / _` | | |_ / _ \ __| '__|
 | |_| | (_| | |  _|  __/ |_| |
  \___/ \__,_|_|_|  \___|\__|_|  v2.0
-------------------------------------
 APK modification tool 
 Created by mr_nightmare

usage: apknife.py [-h] -i INPUT [-o OUTPUT]
                  {extract,build,sign,analyze,edit-manifest,smali,decode-xml,find-oncreate,find-api,scan-vulnerabilities,scan-permissions,catch_rat}

APKnife: Advanced APK analysis & modification tool

positional arguments:
  {extract,build,sign,analyze,edit-manifest,smali,decode-xml,find-oncreate,find-api,scan-vulnerabilities,scan-permissions,catch_rat}
                        Command to execute

options:
  -h, --help            show this help message and exit
  -i, --input INPUT     Input APK file
  -o, --output OUTPUT   Output file/directory

```

The catch_rat😈 module in APKnife scans APK files for hardcoded IP addresses🧟, helping detect potential RATs🐭 and malicious connections🦇.

```

kaboos@localhost:~/apk_tool/newapknif/APKnife$ python3 apknife.py catch_rat -i payload_test.apk           
   ___      _  __      _
  / _ \__ _(_)/ _| ___| |_ _ __
 | | | / _` | | |_ / _ \ __| '__|
 | |_| | (_| | |  _|  __/ |_| |
  \___/ \__,_|_|_|  \___|\__|_|  v2.0
-------------------------------------
 APK modification tool 
 Created by mr_nightmare

✅ APK extracted to temp_extracted_apk

🔎 Found Suspicious IPs:
  - 192.168.1.199

📡 IP: 192.168.1.199 Information:
{
    "ip": "192.168.1.199",
    "bogon": true
}

🔍 WHOIS Information for 192.168.1.199:

#
# ARIN WHOIS data and services are subject to the Terms of Use
# available at: https://www.arin.net/resources/registry/whois/tou/
#
# If you see inaccuracies in the results, please report at
# https://www.arin.net/resources/registry/whois/inaccuracy_reporting/
#
# Copyright 1997-2025, American Registry for Internet Numbers, Ltd.
#


NetRange:       192.168.0.0 - 192.168.255.255
CIDR:           192.168.0.0/16
NetName:        PRIVATE-ADDRESS-CBLK-RFC1918-IANA-RESERVED
NetHandle:      NET-192-168-0-0-1
Parent:         NET192 (NET-192-0-0-0-0)
NetType:        IANA Special Use
OriginAS:
Organization:   Internet Assigned Numbers Authority (IANA)
RegDate:        1994-03-15
Updated:        2024-05-24
Comment:        These addresses are in use by many millions of independently operated networks, which might be as small as a single computer connected to a home gateway, and are automatically configured in hundreds of millions of devices.  They are only intended for use within a private context  and traffic that needs to cross the Internet will need to use a different, unique address.
Comment:
Comment:        These addresses can be used by anyone without any need to coordinate with IANA or an Internet registry.  The traffic from these addresses does not come from ICANN or IANA.  We are not the source of activity you may see on logs or in e-mail records.  Please refer to http://www.iana.org/abuse/answers
Comment:
Comment:        These addresses were assigned by the IETF, the organization that develops Internet protocols, in the Best Current Practice document, RFC 1918 which can be found at:
Comment:        http://datatracker.ietf.org/doc/rfc1918
Ref:            https://rdap.arin.net/registry/ip/192.168.0.0



OrgName:        Internet Assigned Numbers Authority
OrgId:          IANA
Address:        12025 Waterfront Drive
Address:        Suite 300
City:           Los Angeles
StateProv:      CA
PostalCode:     90292
Country:        US
RegDate:
Updated:        2024-05-24
Ref:            https://rdap.arin.net/registry/entity/IANA


OrgAbuseHandle: IANA-IP-ARIN
OrgAbuseName:   ICANN
OrgAbusePhone:  +1-310-301-5820
OrgAbuseEmail:  abuse@iana.org
OrgAbuseRef:    https://rdap.arin.net/registry/entity/IANA-IP-ARIN

OrgTechHandle: IANA-IP-ARIN
OrgTechName:   ICANN
OrgTechPhone:  +1-310-301-5820
OrgTechEmail:  abuse@iana.org
OrgTechRef:    https://rdap.arin.net/registry/entity/IANA-IP-ARIN


#
# ARIN WHOIS data and services are subject to the Terms of Use
# available at: https://www.arin.net/resources/registry/whois/tou/
#
# If you see inaccuracies in the results, please report at
# https://www.arin.net/resources/registry/whois/inaccuracy_reporting/
#
# Copyright 1997-2025, American Registry for Internet Numbers, Ltd.
#


kaboos@localhost:~/apk_tool/newapknif/APKnife$
```
🔍 permissions_scanner: Analyzes APK permissions to detect potential security risks and privacy violations. 🛡️📱
```
kaboos@localhost:~/apk_tool/newapknif/APKnife$ python3 apknife.py scan-permissions -i payload_test.apk

   ___      _  __      _
  / _ \__ _(_)/ _| ___| |_ _ __
 | | | / _` | | |_ / _ \ __| '__|
 | |_| | (_| | |  _|  __/ |_| |
  \___/ \__,_|_|_|  \___|\__|_|  v2.0
-------------------------------------
 APK modification tool (without apktool)
 Created by mr_nightmare


🔍 Scanning permissions in: payload_test.apk

✅ **Permissions Found:**

🔵 **Normal Permissions:**
  - android.permission.ACCESS_NETWORK_STATE: Allows applications to access networks.
  - android.permission.CHANGE_WIFI_STATE: Allows changing Wi-Fi state.
  - android.permission.ACCESS_WIFI_STATE: Allows applications to access Wi-Fi networks.
  - android.permission.SET_WALLPAPER: Allows setting the wallpaper.

🟠 **Dangerous Permissions:**
  - android.permission.CALL_PHONE: Initiate a phone call without user interaction.
  - android.permission.WRITE_CONTACTS: Write user contacts data.
  - android.permission.ACCESS_FINE_LOCATION: Precise location access using GPS.
  - android.permission.READ_CALL_LOG: Read the user's call log.
  - android.permission.WRITE_CALL_LOG: Modify the user's call log.
  - android.permission.CAMERA: Access the camera for photos and videos.
  - android.permission.READ_CONTACTS: Read user contacts data.
  - android.permission.RECORD_AUDIO: Record audio using the microphone.
  - android.permission.READ_SMS: Read SMS messages.
  - android.permission.SEND_SMS: Send SMS messages.
  - android.permission.ACCESS_COARSE_LOCATION: Approximate location access using network sources.
  - android.permission.READ_PHONE_STATE: Read phone state information.
  - android.permission.RECEIVE_SMS: Receive SMS messages.

🔴 **Critical Permissions:**
  - android.permission.WRITE_SETTINGS: Modify system settings, which can be dangerous.
  - android.permission.RECEIVE_BOOT_COMPLETED: Start after boot, potentially for persistent background execution.
  - android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS: Ignore battery optimizations, potentially draining battery.
  - android.permission.WRITE_EXTERNAL_STORAGE: Write to external storage, potentially exposing user data.
  - android.permission.INTERNET: Access the internet, often used for external communication.

⚠️ **Unknown Permissions:** (Might need further analysis)
  - android.permission.WAKE_LOCK: Unknown permission - may require further analysis.
kaboos@localhost:~/apk_tool/newapknif/APKnife$
```

```
python3 apknife.py interactive

      || ________________
O|===|* >________________>
      ||
     APKnife – The Double-Edged Blade of APK Analysis 🔪🧸
     Fear the Blade, Trust the Power! 🎨
     Where Hacking Meets Art! 🖌️

⚙️  Loading the blade...
🔪  Sharpening edges...
🟢  Ready to cut!

APKnife Interactive Mode (Type 'help' for commands, 'exit' to quit)
APKnife> help

APKnife - The Double-Edged Blade of APK Analysis 🔪
Available Commands:

  extract -i <apk_file> -o <output_dir>      Extracts the contents of an APK file.
  build -i <input_dir> -o <output_apk>      Rebuilds an APK from extracted files.
  sign -i <apk_file>                       Signs an APK file to make it installable.
  analyze -i <apk_file>                    Provides detailed analysis of an APK file.
  edit-manifest -i <apk_file>              Modifies the AndroidManifest.xml file.
  smali -i <apk_file> -o <output_dir>      Decompiles an APK into Smali code.
  decode-xml -i <apk_file>                 Decodes XML files inside an APK.
  find-oncreate -i <apk_file>              Searches for the onCreate method.
  find-api -i <apk_file>                   Detects API calls inside an APK.
  scan-vulnerabilities -i <apk_file>       Scans the APK for known vulnerabilities.
  scan-permissions -i <apk_file>           Lists all permissions requested by the APK.
  catch_rat -i <apk_file>                  Detects RAT (Remote Access Trojan) indicators.
  extract-java -i <apk_file> -o <output_dir> -c Extracts Java source code from an APK.
  extract-sensitive -i <apk_file> [-o report.json] Extracts sensitive data from an APK.

  General Commands:
  help  - Shows this help menu.
  exit  - Exits the interactive mode.

APKnife>
```
---

🛡 Security Scanner

🔍 Scans APKs for:
✔️ android:debuggable="true"
✔️ android:allowBackup="true"

python3 apknife.py scan-vulnerabilities -i extracted_app


---

📜 License

MIT License – Free to use and modify with credit to Mr_Nightmare.

