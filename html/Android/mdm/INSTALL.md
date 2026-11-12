# Device registration preview — November 12, 2026

Download Linux x64 or Windows x64 from the download library, or Android MDM version 3 / 1.2-registration from this directory. The desktop binary supports GUI and CLI registration.

In app.admins.net select your company, open Devices and create a Desktop or Android MDM enrollment code. In the client choose Register with company. On desktop you can instead run `./Admins.net --register` (Windows: `Admins.net.exe --register`). Enter the code at the prompt; do not put it in command arguments. Codes expire after ten minutes. The app inventory shows registration and connection status and allows access revocation.

Linux requires the existing OpenSSL runtime provider; its dialog requires GTK 3. Make the downloaded Linux file executable before running it (`chmod +x Admins.net-2026.11.12`). Startup is per operating-system user; configure the desktop listener/daemon startup for reboot persistence.

Android requires Android 9 or newer. This is a debug-signed preview, not a production-signed release. Upgrade only an installation with the same signer. Do not uninstall a managed device-owner app to bypass a signing mismatch. The production automatic-update feed is unchanged. Installing the APK alone does not provision Android device-owner management.

Linux public enrollment and Android emulator restart/upgrade recovery were verified. Windows cryptography/storage passed under Wine; real Windows GUI and physical managed Android qualification remain pending. These builds provide identity and presence; new remote-management commands are not included.

SHA-256 checksums and file sizes: registration-preview.json. Earlier ARM64/x86 desktop downloads and APT packages do not include this registration update.
