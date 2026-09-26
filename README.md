# Admins.net downloads

Static downloads for `dl.admins.net`. The public root is `html/`.

For Cloudflare Pages, connect `centrexity/Admins.net_dl` on the `main` branch, leave the build command empty, and set the output directory to `html`. Attach `dl.admins.net` as a custom domain in Pages.

The landing page lists the binaries currently present in `html/`. OpenWRT package files and installation notes are in `html/OpenWRT/`. This repository is a download site, not a Git server.

Cloudflare Pages redirects both `/releases` and `/releases/` to the download homepage using `html/_redirects`.
