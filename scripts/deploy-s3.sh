#!/bin/sh
# Run as dl-deploy; install root-owned at /config/dl.admins.net/deploy.sh.
set -eu
umask 022
export GIT_TERMINAL_PROMPT=0
base=/var/www/dl.admins.net
exec 9>"$base/deploy.lock"
flock -n 9 || exit 0
if [ ! -d "$base/repository.git" ]; then
    git init --bare "$base/repository.git"
    git --git-dir="$base/repository.git" remote add origin https://github.com/centrexity/Admins.net_dl.git
fi
git --git-dir="$base/repository.git" -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=60 fetch --depth=1 origin +refs/heads/main:refs/remotes/origin/main
sha=$(git --git-dir="$base/repository.git" rev-parse refs/remotes/origin/main)
release="$base/releases/$sha"
[ "$(readlink "$base/current" 2>/dev/null || true)" != "releases/$sha" ] || exit 0
if [ ! -d "$release" ]; then
    stage=$(mktemp -d "$base/releases/.stage.XXXXXX")
    trap 'rm -rf "$stage"' EXIT HUP INT TERM
    git --git-dir="$base/repository.git" archive --format=tar --output="$stage/source.tar" "$sha" html
    tar -xf "$stage/source.tar" -C "$stage"
    rm "$stage/source.tar"
    test -s "$stage/html/index.html"
    # Static downloads never execute scripts or follow repository symlinks.
    if find "$stage/html" -type l | grep -q .; then echo 'Refusing symlinks in public files' >&2; exit 1; fi
    chmod 755 "$stage"
    mv "$stage" "$release"
    trap - EXIT HUP INT TERM
fi
ln -s "releases/$sha" "$base/current.next"
mv -Tf "$base/current.next" "$base/current"
echo "Deployed $sha at $(date -u +%FT%TZ)"
