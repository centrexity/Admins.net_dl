# Package repository layout

The APT archives are signed and contain an amd64 preview package. RPM and FreeBSD remain placeholders.

## APT: Debian, Ubuntu, and Linux Mint

| Distribution | URL root | Verified environment |
| --- | --- | --- |
| Debian | `https://dl.admins.net/apt/debian/` | Debian 12 container: update, download, install, run, purge |
| Ubuntu | `https://dl.admins.net/apt/ubuntu/` | Ubuntu 24.04 container: update, download, install, run, purge |
| Linux Mint | `https://dl.admins.net/apt/mint/` | Mint 22.3 host: update, download, extracted binary smoke checks, simulated install |

All three independent roots use the `stable` archive suite and `main` component. This suite is independent of the operating system codename; the current application package is explicitly a **preview**, version `0.1.8~preview.20261006.1`. The package installs `/usr/bin/admins.net` and the `admins-net` command alias. It does not start services, change desktop startup, or expose ports. Service and desktop features are opt-in. Only amd64 is published. The executable requires `libc6 >= 2.34`; older systems and other architectures are not supported by this build. Optional runtime graphics libraries are recommendations rather than prerequisites for headless commands. Full desktop and remote-control functionality was not tested in these package checks. LMDE has not been tested separately.

Each root contains real `.deb` files under `pool/main/a/admins-net/`, generated `Packages` and `Packages.gz`, SHA-256 by-hash indexes, and signed `InRelease`, `Release`, and `Release.gpg`. The shared public key is `html/apt/admins-net-archive-keyring.gpg`. Fingerprint:

```text
24F98D0A6DCC21D4CE504C11DF26CB725FB409CF
```

Client instructions are published at [APT installation instructions](../html/apt/INSTALL.md) and [the APT page](../html/apt/index.html). They use a repository-specific `Signed-By` key, following [Debian's APT authentication model](https://manpages.debian.org/bookworm/apt/apt-secure.8.en.html).

### Build and update

Install `python3`, `file`, `dpkg-dev`, `apt-utils`, and `gnupg` on the packaging host. Supply a built x86-64 Linux ELF binary and an explicit Debian package version. The initial package uses the current Hindsight port's `Admins.net/Build/lin_x64_c/admins_net`; it is newer than the legacy standalone download at `html/Linux/x64/Admins.net`.

```sh
export GNUPGHOME=/path/outside/the/repository/to/private-signing-directory
python3 scripts/build-apt.py \
  --binary ../Admins.net/Build/lin_x64_c/admins_net \
  --version '0.1.8~preview.20261006.1' \
  --signing-key 24F98D0A6DCC21D4CE504C11DF26CB725FB409CF
scripts/verify-apt.sh
```

The private archive key is kept in the workspace's `.admins-net-apt-signing/` directory, outside this project's Git repository and public root, with directory permissions `0700`. Back up that directory securely before moving or cleaning this workspace; losing the key prevents future updates from being signed with the same identity. Only the public key and fingerprint may be committed. The local key is protected by filesystem permissions and has no passphrase for automated signing.

Use a new package version whenever its contents change. The builder refuses to overwrite different bytes under an existing package filename, retains prior versions, and sets `SOURCE_DATE_EPOCH` from the input executable's modification time unless supplied explicitly. Indexes are generated independently for every root. Retained by-hash indexes allow APT clients to finish an update across metadata deployments. Publish all roots, public key, and instructions in one commit; short metadata caching is configured in `_headers`.

The verification script isolates APT source lists, caches, and downloaded packages in a temporary directory without installing on the host. To verify installation and removal, run it inside disposable containers with `ADMINS_NET_TEST_INSTALL=1`:

```sh
docker run --rm -v "$PWD:/repo:ro" -e ADMINS_NET_TEST_INSTALL=1 debian:bookworm-slim bash /repo/scripts/verify-apt.sh
docker run --rm -v "$PWD:/repo:ro" -e ADMINS_NET_TEST_INSTALL=1 ubuntu:24.04 bash /repo/scripts/verify-apt.sh
```

Release metadata currently has no `Valid-Until`: this static archive does not require periodic re-signing when unchanged. Signatures authenticate content but do not limit replay age. Refresh and re-sign indexes with each release.

## RPM-based Linux

`html/rpm/Packages/` will hold RPMs and `html/rpm/repodata/` will hold generated DNF/YUM metadata. This is a single repository root for now. If packages differ by distribution, release, or architecture, create separate roots beneath `rpm/` before publishing client configuration. Generate `repodata/` with `createrepo_c` from the real package set and decide how RPM and repository metadata signatures will be published.

The reader-facing name includes Fedora, RHEL-compatible distributions, and other Linux distributions that use RPM packages. The short `/rpm/` URL is a package-format path, not a claim that one build works on every RPM-based system.

## FreeBSD pkg

`html/freebsd/All/` is the starter package directory. Generate the repository catalogue with `pkg repo` after adding real `.pkg` files and signing the repository. If packages are built for different FreeBSD ABIs, give each ABI its own repository root before publishing client configuration.

## Static hosting checks

Cloudflare Pages serves `html/`. The top-level `404.html` makes missing package indexes return a real 404 rather than the homepage. Before enabling a client, confirm that its exact metadata and package URLs return the expected files and that the signatures verify. Keep signing keys outside this repository; only public verification keys may be published here.
