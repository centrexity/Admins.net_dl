# ExecOS downloads

ExecOS Ghost x64 is published at `/execos/ghost/x64/latest/ExecOS-x64.iso`.
The homepage selects x64 generic by default and enables its download button.
Other Ghost hardware selections, Titan and Core remain unlinked; their entries
are not claims of validated releases. Existing desktop, OpenWRT, and APT URLs
remain unchanged.

Large images are stored outside the Git-deployed website at
`/var/www/dl.admins.net/execos`. Apache serves that persistent directory with an
Alias from the existing download virtual host, through the Cloudflare Tunnel.
The former Cloudflare Pages file limit does not apply to this origin storage.
The S3 poller force-refreshes only its remote-tracking main ref during its shallow
fetch; otherwise ordinary new commits can be rejected as non-fast-forward at the
shallow boundary. The installed deployer remains root-owned and is not replaced
by website commits.

Website deployments must preserve this directory and the installed Apache
fragment `/config/dl.admins.net/execos.conf`.

Each desktop release contains its bootable ISO, `release.txt`, `release.sig`,
`public.pem`, `SHA256SUMS`, and `README.txt` with installation/recovery notes.
Version directories are immutable. An atomic `latest` symlink selects the
published version. The release publisher in the ExecOS workspace verifies build
checksums, signed policy, and update payload before upload; the host checks
transferred file checksums before switching the channel. Private keys are never
uploaded. Do not treat a downloaded public key as automatic trust enrollment.

Installed immutable Ghost/Titan desktops check signed metadata after startup
and every six hours. Newer matching releases download and stage automatically,
then wait for the user to restart. A current release only fetches small metadata.
A custom administrator-supplied ISO URL remains a manual update source. Existing
systems that predate automatic checking need one manual update to this release
(or the documented trusted bootstrap if they lack the current update key).

The published x64 release was tested in QEMU with BIOS and UEFI boot. Physical
hardware has not been certified by these VM tests. Installation erases the
selected destination drive. Ghost has one system copy and no automatic previous
system recovery; keep installation media and personal-file backups available.

`html/assets/downloads.css` retains the existing visual design.
`html/assets/execos-downloads.js` maps only the available Ghost x64 selection to
the real ISO and disables unlinked selections. A direct x64 download is included
for browsers without JavaScript. Core, Raspberry Pi and Chromebook update
formats require their own publication contract and are not enabled here.

## Edition names and use terms

The editions are ExecOS Titan (formerly Full), ExecOS Ghost, and ExecOS Core. All three are completely free to use, provided without warranty to the extent permitted by applicable law, and carry no guarantee of security. Describe security as an effort to follow best practices and use appropriate protective measures. Renaming/rebranding of ExecOS and its Admins.net branding is not permitted; third-party component licenses retain their own rights. The public terms are at `https://admins.net/terms#execos`. This wording does not establish a complete distribution license for future images.
