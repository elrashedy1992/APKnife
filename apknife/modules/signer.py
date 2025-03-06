import subprocess


def sign_apk(apk_path):
    try:
        subprocess.run(["apksigner", "sign", "--ks", "my-release-key.jks", apk_path])
        print(f"✅ Signed APK: {apk_path}")
    except Exception as e:
        print(f"❌ Error signing APK: {e}")
