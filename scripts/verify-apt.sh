#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../html/apt" && pwd)"
scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
for distro in debian ubuntu mint; do
    archive="$root/$distro"
    gpgv --keyring "$root/admins-net-archive-keyring.gpg" "$archive/dists/stable/InRelease"
    gpgv --keyring "$root/admins-net-archive-keyring.gpg" "$archive/dists/stable/Release.gpg" "$archive/dists/stable/Release"
    state="$scratch/$distro"
    mkdir -p "$state/lists/partial" "$state/cache/archives/partial" "$state/empty"
    echo "deb [arch=amd64 signed-by=$root/admins-net-archive-keyring.gpg] file:$archive stable main" > "$state/sources.list"
    options=(-o "Dir::Etc::sourcelist=$state/sources.list"
        -o "Dir::Etc::sourceparts=$state/empty" -o "Dir::State::lists=$state/lists"
        -o "Dir::Cache=$state/cache" -o APT::Sandbox::User=root
        -o APT::Get::List-Cleanup=0 -o APT::Update::Error-Mode=any)
    apt-get "${options[@]}" update
    (cd "$state" && apt-get "${options[@]}" download admins-net)
    package=("$state"/*.deb)
    dpkg-deb --extract "${package[0]}" "$state/extracted"
    "$state/extracted/usr/bin/admins.net" --help
    "$state/extracted/usr/bin/admins-net" --daemon=once
    apt-get "${options[@]}" --simulate --no-install-recommends install admins-net
    # Only enable inside a disposable container, never on the workstation.
    if [[ "${ADMINS_NET_TEST_INSTALL:-0}" == 1 ]]; then
        test -f /.dockerenv
        apt-get "${options[@]}" -y --no-install-recommends install admins-net
        admins.net --help
        dpkg --purge admins-net
        test ! -e /usr/bin/admins.net
    fi
    echo "PASS: signed $distro archive, download, binary and dependency resolution"
    cp -a "$archive" "$state/tampered"
    sed -i 's/Origin: Admins.net/Origin: Tampered/' "$state/tampered/dists/stable/InRelease"
    echo "deb [arch=amd64 signed-by=$root/admins-net-archive-keyring.gpg] file:$state/tampered stable main" > "$state/sources.list"
    if apt-get "${options[@]}" update > "$state/tampered.log" 2>&1; then
        echo 'FAIL: APT accepted tampered metadata' >&2
        exit 1
    fi
    grep -Eq 'BADSIG|invalid signature' "$state/tampered.log"
    echo "PASS: $distro tampered metadata rejected by APT"
done
