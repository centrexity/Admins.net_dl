# Admins.net APT preview

amd64 only. Verified with Debian 12, Ubuntu 24.04, and Linux Mint 22.3.
The package requires glibc 2.34 or newer. This is a preview of the current
Hindsight port; desktop and remote-control features are still in development.
The archive suite is `stable`, independent of your OS codename.

Choose `debian`, `ubuntu`, or `mint` below for your distribution.
These commands require curl and GnuPG (`sudo apt install curl gnupg`).

```sh
repo=mint
test "$(dpkg --print-architecture)" = amd64 || { echo 'amd64 required'; exit 1; }
key_file=$(mktemp)
curl -fsSL https://dl.admins.net/apt/admins-net-archive-keyring.gpg -o "$key_file"
fingerprint=$(gpg --batch --show-keys --with-colons "$key_file" | awk -F: '$1 == "fpr" {print $10; exit}')
test "$fingerprint" = 24F98D0A6DCC21D4CE504C11DF26CB725FB409CF || { rm -f "$key_file"; echo 'Unexpected signing key'; exit 1; }
sudo install -d -m 0755 /etc/apt/keyrings
sudo install -m 0644 "$key_file" /etc/apt/keyrings/admins-net-archive-keyring.gpg
rm -f "$key_file"
printf 'deb [arch=amd64 signed-by=/etc/apt/keyrings/admins-net-archive-keyring.gpg] https://dl.admins.net/apt/%s stable main\n' "$repo" | sudo tee /etc/apt/sources.list.d/admins-net.list
sudo apt update
sudo apt install admins-net
admins.net --help
```

The package installs `admins.net` and an `admins-net` alias. It starts no services
and opens no ports during installation. Review `--help` before enabling daemon,
desktop-session, or web-server functionality.

To update: `sudo apt update && sudo apt upgrade admins-net`.
To remove the package: `sudo apt remove admins-net`.
To stop receiving repository updates, remove
`/etc/apt/sources.list.d/admins-net.list` and
`/etc/apt/keyrings/admins-net-archive-keyring.gpg`.
Any user services or state you explicitly created must be removed separately.

Direct package downloads:

- [Debian](debian/pool/main/a/admins-net/admins-net_0.1.8~preview.20261006.1_amd64.deb)
- [Ubuntu](ubuntu/pool/main/a/admins-net/admins-net_0.1.8~preview.20261006.1_amd64.deb)
- [Linux Mint](mint/pool/main/a/admins-net/admins-net_0.1.8~preview.20261006.1_amd64.deb)

APT verifies archive signatures and package hashes. Direct downloads require
separate checksum verification; using the signed APT repository is preferred.
