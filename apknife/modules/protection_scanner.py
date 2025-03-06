import os
import subprocess
from androguard.core.apk import APK

class ProtectionScanner:
    def __init__(self, apk_path):
        self.apk_path = apk_path
        self.apk = APK(apk_path)

    def check_proguard(self):
        """
        Check if ProGuard is used for code obfuscation.
        """
        for file in self.apk.get_files():
            if "proguard" in file.lower() or "mapping" in file.lower():
                return True
        return False

    def check_firewall(self):
        """
        Check if the app uses a firewall.
        """
        manifest = self.apk.get_android_manifest_xml()
        if "NetworkSecurityConfig" in manifest:
            return True
        return False

    def check_anti_tampering(self):
        """
        Check if the app has anti-tampering mechanisms.
        """
        for file in self.apk.get_files():
            if "tamper" in file.lower() or "integrity" in file.lower():
                return True
        return False

    def check_ssl_pinning(self):
        """
        Check if the app uses SSL pinning.
        """
        for file in self.apk.get_files():
            if "ssl" in file.lower() and "pinning" in file.lower():
                return True
        return False

    def check_root_detection(self):
        """
        Check if the app has root detection mechanisms.
        """
        for file in self.apk.get_files():
            if "root" in file.lower() and "detection" in file.lower():
                return True
        return False

    def check_data_encryption(self):
        """
        Check if the app uses data encryption.
        """
        for file in self.apk.get_files():
            if "encrypt" in file.lower() or "crypto" in file.lower():
                return True
        return False

    def check_runtime_protection(self):
        """
        Check if the app has runtime protection mechanisms.
        """
        for file in self.apk.get_files():
            if "runtime" in file.lower() and "protection" in file.lower():
                return True
        return False

    def scan_protections(self):
        """
        Scan the app for various protection mechanisms.
        """
        protections = {
            "ProGuard": self.check_proguard(),
            "Firewall": self.check_firewall(),
            "Anti-Tampering": self.check_anti_tampering(),
            "SSL Pinning": self.check_ssl_pinning(),
            "Root Detection": self.check_root_detection(),
            "Data Encryption": self.check_data_encryption(),
            "Runtime Protection": self.check_runtime_protection(),
        }
        return protections

    def get_protection_guidance(self, protection, status):
        """
        Provide guidance on the risks, exploitation, and mitigation for each protection.
        """
        guidance = {
            "ProGuard": {
                "risk": "Without ProGuard, the app's code is easily reverse-engineered, exposing sensitive logic and data.",
                "exploitation": "Attackers can decompile the app to understand its logic, find vulnerabilities, or extract sensitive information.",
                "mitigation": "Enable ProGuard or R8 in your build.gradle file to obfuscate the code.",
                "testing": "Use tools like JADX or APKTool to decompile the app and verify obfuscation.",
            },
            "Firewall": {
                "risk": "Without a firewall, the app is vulnerable to network-based attacks like MITM (Man-in-the-Middle).",
                "exploitation": "Attackers can intercept and manipulate network traffic to steal data or inject malicious content.",
                "mitigation": "Implement Network Security Config and use HTTPS with strong ciphers.",
                "testing": "Use tools like Burp Suite or Frida to test network security.",
            },
            "Anti-Tampering": {
                "risk": "Without anti-tampering, the app can be modified or repackaged with malicious code.",
                "exploitation": "Attackers can modify the APK to bypass security checks or inject malware.",
                "mitigation": "Implement integrity checks using checksums or digital signatures.",
                "testing": "Use tools like Apktool to repackage the app and test integrity checks.",
            },
            "SSL Pinning": {
                "risk": "Without SSL pinning, the app is vulnerable to MITM attacks even with HTTPS.",
                "exploitation": "Attackers can use self-signed certificates to intercept HTTPS traffic.",
                "mitigation": "Implement SSL pinning using libraries like OkHttp or TrustKit.",
                "testing": "Use tools like Frida or Objection to bypass SSL pinning and test its effectiveness.",
            },
            "Root Detection": {
                "risk": "Without root detection, the app is vulnerable to attacks from rooted devices.",
                "exploitation": "Attackers can use rooted devices to bypass security mechanisms or access sensitive data.",
                "mitigation": "Implement root detection using libraries like SafetyNet or RootBeer.",
                "testing": "Use rooted devices or emulators to test root detection mechanisms.",
            },
            "Data Encryption": {
                "risk": "Without data encryption, sensitive data stored on the device is easily accessible.",
                "exploitation": "Attackers can extract sensitive data from the app's storage or databases.",
                "mitigation": "Use strong encryption algorithms like AES for sensitive data storage.",
                "testing": "Use tools like SQLite Browser or Frida to inspect stored data.",
            },
            "Runtime Protection": {
                "risk": "Without runtime protection, the app is vulnerable to dynamic analysis and tampering.",
                "exploitation": "Attackers can use tools like Frida to manipulate the app's behavior at runtime.",
                "mitigation": "Implement runtime integrity checks and anti-debugging mechanisms.",
                "testing": "Use tools like Frida or Xposed to test runtime protections.",
            },
        }
        return guidance.get(protection, {})

def scan_apk_protections(apk_path):
    """
    Scan an APK for protection mechanisms and provide guidance.
    """
    try:
        scanner = ProtectionScanner(apk_path)
        protections = scanner.scan_protections()
        for protection, status in protections.items():
            print(f"{protection}: {'✅' if status else '❌'}")
            if not status:
                guidance = scanner.get_protection_guidance(protection, status)
                print(f"  Risk: {guidance['risk']}")
                print(f"  Exploitation: {guidance['exploitation']}")
                print(f"  Mitigation: {guidance['mitigation']}")
                print(f"  Testing: {guidance['testing']}")
                print()
    except Exception as e:
        print(f"[!] Error scanning APK: {e}")

def execute_shell_command(command):
    """
    Execute a shell command and return the output.
    """
    try:
        # Handle 'cd' command separately
        if command.startswith("cd "):
            new_dir = command.split(" ", 1)[1].strip()
            try:
                os.chdir(new_dir)
                return f"[+] Changed directory to: {os.getcwd()}"
            except FileNotFoundError:
                return f"[!] Directory not found: {new_dir}"
            except Exception as e:
                return f"[!] Error changing directory: {e}"

        # Execute other shell commands
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"[!] Error: {e.stderr}"

def interactive_shell():
    """
    Start an interactive shell for APKnife.
    """
    from prompt_toolkit import PromptSession
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.history import FileHistory

    # Define available commands
    commands = {
        "scan": "Scan an APK for protection mechanisms.",
        "exit": "Exit the interactive shell.",
        "help": "Show this help message.",
    }

    # Create a completer for command suggestions
    completer = WordCompleter(list(commands.keys()), ignore_case=True)

    # Create a prompt session
    session = PromptSession(
        history=FileHistory(".apknife_history"),
        auto_suggest=AutoSuggestFromHistory(),
        completer=completer,
    )

    print("APKnife Interactive Shell. Type 'help' for a list of commands.")

    while True:
        try:
            # Read user input
            user_input = session.prompt("APKnife> ").strip()

            if not user_input:
                continue

            # Split input into command and arguments
            parts = user_input.split()
            command = parts[0]
            args = parts[1:]

            # Handle commands
            if command == "exit":
                print("Exiting APKnife. Goodbye!")
                break
            elif command == "help":
                print("\nAvailable Commands:")
                for cmd, desc in commands.items():
                    print(f"  {cmd.ljust(10)} - {desc}")
                print()
            elif command == "scan":
                if not args:
                    print("[!] Please provide the path to the APK file.")
                    continue
                apk_path = args[0]
                if not os.path.exists(apk_path):
                    print(f"[!] APK file not found: {apk_path}")
                    continue
                scan_apk_protections(apk_path)
            else:
                # Execute as a shell command
                output = execute_shell_command(user_input)
                print(output)

        except KeyboardInterrupt:
            print("\nType 'exit' to quit.")
        except Exception as e:
            print(f"[!] Error: {e}")

if __name__ == "__main__":
    interactive_shell()
