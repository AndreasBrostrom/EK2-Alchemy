#!/bin/bash

PROJECT_NAME="Elder Kings 2 - Alchemy"
CK3_MOD_PATH="$HOME/.local/share/Paradox Interactive/Crusader Kings III/mod"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MOD_PATH="$(dirname "$SCRIPT_DIR")"
MOD_NAME="$(basename "$MOD_PATH")"

SRC="$MOD_PATH/descriptor.mod"

# Extract fields from source descriptor
VERSION=$(grep '^version=' "$SRC" | head -1)
TAGS=$(awk '/^tags=\{/,/^\}/' "$SRC")
SUPPORTED=$(grep '^supported_version=' "$SRC" | head -1)

# Dev build
ln -sfn "$MOD_PATH" "$CK3_MOD_PATH/${MOD_NAME}_DevBuild"
{
  echo "name=\"$PROJECT_NAME DevBuild\""
  echo "$VERSION"
  echo "$TAGS"
  echo "$SUPPORTED"
  echo "path=\"mod/${MOD_NAME}_DevBuild\""
} > "$CK3_MOD_PATH/${MOD_NAME}_DevBuild.mod"

# Manual release
RELEASE_LOCAL="$MOD_PATH/release/local/$PROJECT_NAME"
mkdir -p "$RELEASE_LOCAL"
ln -sfn "$RELEASE_LOCAL" "$CK3_MOD_PATH/${MOD_NAME}_ManualRelease"
{
  echo "name=\"$PROJECT_NAME (Manual Release)\""
  echo "$VERSION"
  echo "$TAGS"
  echo "$SUPPORTED"
  echo "path=\"mod/${MOD_NAME}_ManualRelease\""
} > "$CK3_MOD_PATH/${MOD_NAME}_ManualRelease.mod"

# Steam release
RELEASE_STEAM="$MOD_PATH/release/steam/$PROJECT_NAME"
mkdir -p "$RELEASE_STEAM"
ln -sfn "$RELEASE_STEAM" "$CK3_MOD_PATH/${MOD_NAME}_SteamRelease"
{
  echo "name=\"$PROJECT_NAME (Steam Release)\""
  echo "$VERSION"
  echo "$TAGS"
  echo "$SUPPORTED"
  echo "path=\"mod/${MOD_NAME}_SteamRelease\""
} > "$CK3_MOD_PATH/${MOD_NAME}_SteamRelease.mod"
