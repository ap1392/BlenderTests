#!/bin/sh
# Project-local launcher; no shell profile changes required.
set -eu
BLENDER_APP="${BLENDER_APP:-/Applications/Blender.app/Contents/MacOS/Blender}"
if [ ! -x "$BLENDER_APP" ]; then
  echo "Blender not found at $BLENDER_APP. Set BLENDER_APP to its executable path." >&2
  exit 1
fi
exec "$BLENDER_APP" "$@"
