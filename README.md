# Admins.net downloads

Static downloads for `dl.admins.net`. The public root is `html/`.

For Cloudflare Pages, connect `centrexity/Admins.net_dl` on the `main` branch, leave the build command empty, and set the output directory to `html`. Attach `dl.admins.net` as a custom domain in Pages.

The landing page lists the binaries currently present in `html/`. OpenWRT package files and installation notes are in `html/OpenWRT/`. This repository is a download site, not a Git server.

The homepage uses the transparent Admins.net favicon assets copied from `Admins.net_site/htdocs/`. They are browser icons and are not listed as downloads.

Cloudflare Pages redirects `/releases` and `/betas` (with or without a trailing slash) to the download homepage using `html/_redirects`.

The `html/apt/` tree contains signed amd64 preview packages for Debian, Ubuntu, and Linux Mint. See [installation instructions](html/apt/INSTALL.md) and [package repository notes](docs/package-repositories.md) for verified platforms and release tooling. `html/rpm/` and `html/freebsd/` remain placeholders without packages or valid metadata. The RPM section is called "RPM-based Linux" while its URL stays `/rpm/`.

## Download library and ExecOS

The redesigned landing page uses `html/assets/downloads.css` and groups existing downloads by platform, package repository, and ExecOS edition. Existing artifact URLs are unchanged. RPM and FreeBSD are clearly marked planned rather than linked as usable repositories.

ExecOS Ghost x64 has a bootable ISO with signed automatic updates at `/execos/ghost/x64/latest/ExecOS-x64.iso`. Large release files are served from persistent S3 storage outside the Git deployment tree. Titan, Core, and other Ghost hardware entries remain unlinked. See [release and hosting notes](docs/execos.md) for installation, recovery, verification, tested platforms, and update behavior.

ExecOS Titan and Ghost are desktop editions; ExecOS Core is the minimal command-line edition. Core has a reserved download slot at `html/execos/core/` in the downloads repository, with no published image.
