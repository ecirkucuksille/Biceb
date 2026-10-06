#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VERSION="$(python3 -c 'import tomllib, pathlib, sys; print(tomllib.loads(pathlib.Path(sys.argv[1]).read_text())["project"]["version"])' "$ROOT/pyproject.toml")"
ARCH="$(uname -m)"
APP="$ROOT/dist/BICEB.app"
OUTPUT="$ROOT/dist/installers/BICEB-$VERSION-macos-$ARCH.dmg"

if [[ ! -d "$APP" ]]; then
  echo "Missing $APP; run the macOS PyInstaller build first" >&2
  exit 1
fi

STAGING="$(mktemp -d)"
trap 'rm -rf "$STAGING"' EXIT
mkdir -p "$ROOT/dist/installers"
ditto "$APP" "$STAGING/BICEB.app"
ln -s /Applications "$STAGING/Applications"
hdiutil create -volname "BİÇEB $VERSION" -srcfolder "$STAGING" -ov -format UDZO "$OUTPUT"
echo "$OUTPUT"
