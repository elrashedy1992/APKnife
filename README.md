<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APKnife - Advanced APK Analysis & Modification Tool</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            padding: 20px;
            background-color: #f4f4f4;
        }
        h1, h2, h3 {
            color: #333;
        }
        a {
            color: #007bff;
            text-decoration: none;
        }
        .container {
            max-width: 800px;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .menu {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }
        .menu a {
            padding: 10px;
            background: #007bff;
            color: white;
            border-radius: 5px;
        }
        .cover {
            text-align: center;
        }
        .cover img {
            max-width: 100%;
            border-radius: 5px;
        }
        .features {
            background: #e9ecef;
            padding: 10px;
            border-radius: 5px;
        }
        .code {
            background: #272822;
            color: #f8f8f2;
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            overflow-x: auto;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>📌 APKnife - Advanced APK Analysis & Modification Tool</h1>
    <p><strong>🔹 Version:</strong> 2.0 | <strong>🔹 Author:</strong> Mr_Nightmare</p>
    <p><strong>🔹 Description:</strong> A powerful tool for APK analysis, modification, and security scanning without using apktool.</p>

    <div class="cover">
        <img src="assets/cover.png" alt="APKnife Cover">
    </div>

    <h2>🚀 Features</h2>
    <ul class="features">
        <li>✅ Extract APK Files – Extracts APK contents for modification</li>
        <li>✅ Modify AndroidManifest.xml – Edit package name and permissions</li>
        <li>✅ Analyze APK – Retrieves package details and permissions</li>
        <li>✅ Decode XML Files – Decrypts AndroidManifest.xml</li>
        <li>✅ Find OnCreate Methods – Scans Smali code for onCreate()</li>
        <li>✅ Find API Calls – Detects sensitive API calls</li>
        <li>✅ Sign APK – Signs modified APKs for installation</li>
        <li>✅ Vulnerability Scanner – Detects security flaws in AndroidManifest.xml</li>
    </ul>

    <h2>📥 Installation</h2>
    <h3>🔹 On Linux / Termux</h3>
    <pre class="code">git clone https://github.com/elrashedy1992/APKnife.git
cd APKnife
chmod +x apknife.py
chmod +x install.sh
sudo bash install.sh
python3 apknife.py</pre>

    <h3>🔹 Dependencies</h3>
    <p>Ensure you have the following installed:</p>
    <pre class="code">pip install androguard
pkg install zip apksigner</pre>

    <h2>🛠 Usage</h2>
    <p>Basic Command Structure:</p>
    <pre class="code">python3 apknife.py -i &lt;input.apk&gt; -o</pre>

    <h3>🎯 Examples</h3>
    <pre class="code">python3 apknife.py extract -i app.apk -o extracted_app
python3 apknife.py edit-manifest -i extracted_app
python3 apknife.py analyze -i facebook.apk
python3 apknife.py sign -i modified.apk</pre>

    <h2>🛡 Security Scanner</h2>
    <p>🔍 Scans APKs for:</p>
    <ul>
        <li>✔️ android:debuggable="true"</li>
        <li>✔️ android:allowBackup="true"</li>
    </ul>
    <pre class="code">python3 apknife.py scan-vulnerabilities -i extracted_app</pre>

    <h2>📜 License</h2>
    <p>MIT License – Free to use and modify with credit to Mr_Nightmare.</p>

    <h2>🔗 Repository Navigation</h2>
    <div class="menu">
        <a href="https://github.com/elrashedy1992/APKnife">Code</a>
        <a href="https://github.com/elrashedy1992/APKnife/issues">Issues</a>
        <a href="https://github.com/elrashedy1992/APKnife/pulls">Pull Requests</a>
        <a href="https://github.com/elrashedy1992/APKnife/stargazers">⭐ Stars (0)</a>
        <a href="https://github.com/elrashedy1992/APKnife/forks">🍴 Forks (0)</a>
        <a href="https://github.com/elrashedy1992/APKnife/watchers">👀 Watching (1)</a>
    </div>

    <div class="footer">
        <p>🎭 Enjoy Hacking & Stay Ethical! 🛡</p>
    </div>
</div>

</body>
</html>
