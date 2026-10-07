#!/usr/bin/env python3
"""Build an amd64 package and signed, independent APT archive roots."""
import argparse
import gzip
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def run(*args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', required=True, type=Path)
    parser.add_argument('--version', required=True)
    parser.add_argument('--signing-key', required=True, help='Full signing fingerprint')
    args = parser.parse_args()
    if not re.fullmatch(r'[0-9][A-Za-z0-9.+:~\-]*', args.version):
        parser.error('Invalid Debian package version')
    if not re.fullmatch(r'[A-Fa-f0-9]{40}', args.signing_key):
        parser.error('Use the full signing fingerprint')
    binary = args.binary.resolve()
    os.environ.setdefault('SOURCE_DATE_EPOCH', str(int(binary.stat().st_mtime)))
    if not os.environ.get('GNUPGHOME'):
        parser.error('Set GNUPGHOME to the private signing key directory outside this repository')
    if ROOT in Path(os.environ['GNUPGHOME']).resolve().parents:
        parser.error('Signing keys must be outside this repository')
    info = run('file', str(binary), capture_output=True, text=True).stdout
    if 'ELF 64-bit' not in info or 'x86-64' not in info:
        parser.error('Expected an x86-64 Linux ELF executable')
    filename = f'admins-net_{args.version}_amd64.deb'
    with tempfile.TemporaryDirectory(prefix='admins-net-package-') as scratch:
        stage = Path(scratch) / 'package'
        (stage / 'DEBIAN').mkdir(parents=True)
        (stage / 'usr/bin').mkdir(parents=True)
        installed = stage / 'usr/bin/admins.net'
        shutil.copyfile(binary, installed)
        installed.chmod(0o755)
        (stage / 'usr/bin/admins-net').symlink_to('admins.net')
        doc = stage / 'usr/share/doc/admins-net'
        doc.mkdir(parents=True)
        (doc / 'README').write_text('Admins.net preview build. Run admins.net --help.\n'
            'Services and remote access are opt-in; installation starts no processes.\n'
            'Desktop features require a supported display and optional graphics libraries.\n')
        (stage / 'DEBIAN/control').write_text(f'''Package: admins-net
Version: {args.version}
Architecture: amd64
Maintainer: Admins.net <packages@admins.net>
Section: admin
Priority: optional
Depends: libc6 (>= 2.34)
Recommends: libx11-6, libxtst6, libgl1, libglx0, libvulkan1, libwayland-client0, libglib2.0-0, libpangocairo-1.0-0, zlib1g
Homepage: https://admins.net/
Installed-Size: {(binary.stat().st_size + 1023) // 1024 + 4}
Description: Admins.net desktop and system management preview
 Command-line application with opt-in daemon, desktop session listener,
 overlay, and HTTP/WebSocket system management tools.
''')
        package = Path(scratch) / filename
        run('dpkg-deb', '--root-owner-group', '--build', str(stage), str(package))
        for distro in ('debian', 'ubuntu', 'mint'):
            archive = ROOT / 'html/apt' / distro
            pool = archive / 'pool/main/a/admins-net'
            pool.mkdir(parents=True, exist_ok=True)
            target = pool / filename
            if target.exists() and target.read_bytes() != package.read_bytes():
                raise SystemExit(f'Refusing to replace immutable package {target}; bump version')
            shutil.copyfile(package, target)
            indexes = archive / 'dists/stable/main/binary-amd64'
            indexes.mkdir(parents=True, exist_ok=True)
            packages = run('apt-ftparchive', 'packages', 'pool/main', cwd=archive,
                           capture_output=True).stdout
            (indexes / 'Packages').write_bytes(packages)
            (indexes / 'Packages.gz').write_bytes(gzip.compress(packages, mtime=0))
            # Keep previous indexes by hash so clients can finish an in-flight update.
            hashes = indexes / 'by-hash/SHA256'
            hashes.mkdir(parents=True, exist_ok=True)
            for name in ('Packages', 'Packages.gz'):
                data = (indexes / name).read_bytes()
                (hashes / hashlib.sha256(data).hexdigest()).write_bytes(data)
            release_dir = archive / 'dists/stable'
            (release_dir / 'InRelease').unlink(missing_ok=True)
            (release_dir / 'Release.gpg').unlink(missing_ok=True)
            (release_dir / 'Release').unlink(missing_ok=True)
            release = run('apt-ftparchive',
                '-o', 'APT::FTPArchive::Release::Origin=Admins.net',
                '-o', f'APT::FTPArchive::Release::Label=Admins.net {distro}',
                '-o', 'APT::FTPArchive::Release::Suite=stable',
                '-o', 'APT::FTPArchive::Release::Codename=stable',
                '-o', 'APT::FTPArchive::Release::Architectures=amd64',
                '-o', 'APT::FTPArchive::Release::Components=main',
                '-o', 'APT::FTPArchive::Release::Acquire-By-Hash=yes',
                'release', 'dists/stable', cwd=archive, capture_output=True).stdout
            (release_dir / 'Release').write_bytes(release)
            for mode, output in (('--clearsign', 'InRelease'), ('--detach-sign', 'Release.gpg')):
                run('gpg', '--batch', '--yes', '--local-user', args.signing_key,
                    '--digest-algo', 'SHA256', '--armor', '--output',
                    str(release_dir / output), mode, str(release_dir / 'Release'))
        public = run('gpg', '--batch', '--export', args.signing_key, capture_output=True).stdout
        (ROOT / 'html/apt/admins-net-archive-keyring.gpg').write_bytes(public)
        (ROOT / 'html/apt/signing-key-fingerprint.txt').write_text(args.signing_key.upper() + '\n')
        print(f'Published {filename} to Debian, Ubuntu and Mint archives')

if __name__ == '__main__':
    main()
