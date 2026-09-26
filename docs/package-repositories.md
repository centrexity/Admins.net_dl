# Package repository layout

These are starter directories only. No package manager repository is ready for clients yet. Do not publish an installation command until the packages, indexes, signatures, and client verification steps exist and have been tested.

## APT: Ubuntu, Linux Mint, and Debian

Each distribution has an independent archive root:

| Distribution | URL root | On-disk root |
| --- | --- | --- |
| Ubuntu | `https://dl.admins.net/apt/ubuntu/` | `html/apt/ubuntu/` |
| Linux Mint | `https://dl.admins.net/apt/mint/` | `html/apt/mint/` |
| Debian | `https://dl.admins.net/apt/debian/` | `html/apt/debian/` |

Each root has `dists/` for release-specific indexes and `pool/main/` for `.deb` files. When a release is supported, create `dists/<codename>/main/binary-<architecture>/Packages` and its compressed version, plus a signed `InRelease` (or signed `Release` and `Release.gpg`) with hashes of the indexes. Generate these from the real `.deb` files; do not hand-write or copy an index between releases.

Mint's main editions use an Ubuntu base, while LMDE uses a Debian base. Keep separate roots until each package is tested against the actual release. A package may be shared later if its compatibility is verified. Add only the codenames and architectures that are built and tested.

## RPM-based Linux

`html/rpm/Packages/` will hold RPMs and `html/rpm/repodata/` will hold generated DNF/YUM metadata. This is a single repository root for now. If packages differ by distribution, release, or architecture, create separate roots beneath `rpm/` before publishing client configuration. Generate `repodata/` with `createrepo_c` from the real package set and decide how RPM and repository metadata signatures will be published.

The reader-facing name includes Fedora, RHEL-compatible distributions, and other Linux distributions that use RPM packages. The short `/rpm/` URL is a package-format path, not a claim that one build works on every RPM-based system.

## FreeBSD pkg

`html/freebsd/All/` is the starter package directory. Generate the repository catalogue with `pkg repo` after adding real `.pkg` files and signing the repository. If packages are built for different FreeBSD ABIs, give each ABI its own repository root before publishing client configuration.

## Static hosting checks

Cloudflare Pages serves `html/`. The top-level `404.html` makes missing package indexes return a real 404 rather than the homepage. Before enabling a client, confirm that its exact metadata and package URLs return the expected files and that the signatures verify. Keep signing keys outside this repository; only public verification keys may be published here.
