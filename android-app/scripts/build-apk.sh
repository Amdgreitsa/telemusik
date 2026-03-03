#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -x ./gradlew ]]; then
  echo "gradlew not found or not executable. Generate wrapper first: gradle wrapper --gradle-version 8.7"
  exit 1
fi

BUILD_TYPE="${1:-release}"
if [[ "$BUILD_TYPE" != "debug" && "$BUILD_TYPE" != "release" ]]; then
  echo "Usage: $0 [debug|release]"
  exit 1
fi

if [[ "$BUILD_TYPE" == "release" ]]; then
  if [[ ! -f keystore.properties ]]; then
    echo "keystore.properties not found. Create it for signed release build (see README)."
    exit 1
  fi
  ./gradlew :app:assembleRelease
  echo "APK: app/build/outputs/apk/release/app-release.apk"
else
  ./gradlew :app:assembleDebug
  echo "APK: app/build/outputs/apk/debug/app-debug.apk"
fi
