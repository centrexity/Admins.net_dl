# Admins.net downloads

Static downloads for `dl.admins.net`. The public root is `html/`.

For Cloudflare Pages, connect `centrexity/Admins.net_dl` on the `main` branch, leave the build command empty, and set the output directory to `html`. Attach `dl.admins.net` as a custom domain in Pages.

The landing page lists the binaries currently present in `html/`. OpenWRT package files and installation notes are in `html/OpenWRT/`. This repository is a download site, not a Git server.

The homepage uses the transparent Admins.net favicon assets copied from `Admins.net_site/htdocs/`. They are browser icons and are not listed as downloads.

Cloudflare Pages redirects `/releases` and `/betas` (with or without a trailing slash) to the download homepage using `html/_redirects`.

The `html/apt/`, `html/rpm/`, and `html/freebsd/` trees are placeholders for future package repositories. The RPM section is called "RPM-based Linux" in user-facing text while its URL stays `/rpm/`. These trees do not contain packages or valid repository metadata yet. See [package repository notes](docs/package-repositories.md) before publishing packages or install instructions.
