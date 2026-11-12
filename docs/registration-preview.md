# Registration preview — November 12, 2026

Published Linux x64 and Windows x64 desktop builds plus the Kotlin Android MDM version-3 debug APK from the verified registration artifacts. Versioned download URLs and SHA-256 values are listed in `html/Android/mdm/registration-preview.json`. Existing Linux/x64/Admins.net and Windows/x64/Admins.net.exe URLs also contain the new binaries. ARM64, x86 and APT builds are unchanged.

The library and app Devices page link directly to these previews. Android installation notes clearly identify the debug signer and upgrade restriction. No production `latest.json` feed is created; signing continuity with the legacy production keystore remains unresolved. See the client verification report at `../../Admins.net/REGISTRATION_VERIFIED.md` and public installation notes at `../html/Android/mdm/INSTALL.md`.

Publish with the existing Git main deployment. Verify public bytes against registration-preview.json and check the deployed app links after both repositories update.
