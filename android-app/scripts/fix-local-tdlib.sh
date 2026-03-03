#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TDLIB_DIR="$ROOT_DIR/tdlib"

if [[ ! -d "$TDLIB_DIR" ]]; then
  echo "Local tdlib module not found at: $TDLIB_DIR"
  exit 1
fi

MANIFEST="$TDLIB_DIR/src/main/AndroidManifest.xml"
if [[ -f "$MANIFEST" ]]; then
  python3 - <<PY
from pathlib import Path
p=Path(r"$MANIFEST")
text=p.read_text(encoding='utf-8')
text=text.replace('package="org.drinkless.td.libcore"','')
text=text.replace('  >','>')
text=text.replace('<manifest  ','<manifest ')
p.write_text(text,encoding='utf-8')
print('Patched manifest:',p)
PY
else
  echo "Warning: AndroidManifest.xml not found in tdlib module"
fi

TDAPI_FILES=$(find "$TDLIB_DIR/src/main/java" -type f -name "TdApi.java" 2>/dev/null || true)
if [[ -z "$TDAPI_FILES" ]]; then
  echo "Warning: TdApi.java not found under tdlib/src/main/java"
else
  while IFS= read -r file; do
    sed -i 's/import android.support.annotation.Nullable;/import androidx.annotation.Nullable;/g' "$file"
    sed -i 's/import android.support.annotation.IntDef;/import androidx.annotation.IntDef;/g' "$file"
    echo "Patched annotations imports: $file"
  done <<< "$TDAPI_FILES"
fi

BUILD_FILE="$TDLIB_DIR/build.gradle.kts"
if [[ -f "$BUILD_FILE" ]]; then
  python3 - <<PY
from pathlib import Path
p=Path(r"$BUILD_FILE")
text=p.read_text(encoding='utf-8')
if 'namespace =' not in text:
    text=text.replace('android {','android {\n    namespace = "org.drinkless.td.libcore"\n',1)
if 'compileSdk' not in text:
    text=text.replace('android {','android {\n    compileSdk = 34\n',1)
if 'defaultConfig {' not in text:
    text=text.replace('android {','android {\n    defaultConfig { minSdk = 26 }\n',1)
if 'sourceCompatibility = JavaVersion.VERSION_17' not in text:
    insert='\n    compileOptions {\n        sourceCompatibility = JavaVersion.VERSION_17\n        targetCompatibility = JavaVersion.VERSION_17\n    }\n'
    text=text.replace('android {','android {'+insert,1)
if 'implementation("androidx.annotation:annotation:1.8.2")' not in text:
    if 'dependencies {' in text:
        text=text.replace('dependencies {','dependencies {\n    implementation("androidx.annotation:annotation:1.8.2")\n',1)
    else:
        text += '\n\ndependencies {\n    implementation("androidx.annotation:annotation:1.8.2")\n}\n'
p.write_text(text,encoding='utf-8')
print('Patched build script:',p)
PY
else
  cat > "$BUILD_FILE" <<'GRADLE'
plugins {
    id("com.android.library")
}

android {
    namespace = "org.drinkless.td.libcore"
    compileSdk = 34

    defaultConfig {
        minSdk = 26
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

dependencies {
    implementation("androidx.annotation:annotation:1.8.2")
}
GRADLE
  echo "Created tdlib build.gradle.kts with AndroidX annotation dependency"
fi

echo "Done. Next steps:"
echo "1) cd android-app"
echo "2) ./gradlew :app:assembleDebug"
