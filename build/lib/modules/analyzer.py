from androguard.core.apk import APK


def analyze_apk(apk_path):

    try:
        apk = APK(apk_path)
        print(f"📊 APK Package: {apk.get_package()}")
        print(f"📜 Permissions: {', '.join(apk.get_permissions())}")
    except Exception as e:
        print(f"❌ Error analyzing APK: {e}")
