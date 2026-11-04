# ExecOS release slots

The homepage's `#execos` section lists Titan and Ghost. Both remain in development without downloadable images. Ghost's first hardware target is Acer Chromebook CB5-571, not yet validated for release.

Reserved artifact directories:

- `html/execos/titan/`
- `html/execos/ghost/acer-cb5-571/`

When a build exists, publish versioned artifacts with checksums, verification guidance, requirements, tested hardware, and installation/recovery instructions; then add a real download link to the edition card. Do not link empty directories or invent versions. Never replace another project's binaries with an ExecOS image.

Cloudflare Pages enforces an individual-file size limit; verify the current deployment limit before publishing OS images. An image that exceeds that limit needs a separately agreed hosting approach. These placeholders add no hosting service or expense.

`html/assets/downloads.css` styles the landing page. Bump its query version when changing it. Existing Windows, Linux, OpenWRT, and APT links remain in place. `/releases` and `/betas` redirects remain unchanged.

Public edition copy uses product-focused language without development badges. Keep download availability factual: the current cards say “Installer not currently listed” and must only gain download links when artifacts exist.

## Edition names and use terms

The editions are ExecOS Titan (formerly Full) and ExecOS Ghost. Both are completely free to use, provided without warranty to the extent permitted by applicable law, and carry no guarantee of security. Describe security as an effort to follow best practices and use appropriate protective measures. Renaming/rebranding of ExecOS and its Admins.net branding is not permitted; third-party component licenses retain their own rights. The public terms are at `https://admins.net/terms#execos`. This wording does not establish a complete distribution license for future images.
