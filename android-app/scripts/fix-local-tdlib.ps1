$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$Tdlib = Join-Path $Root 'tdlib'

if (-not (Test-Path $Tdlib)) {
  throw "Local tdlib module not found at: $Tdlib"
}

$Manifest = Join-Path $Tdlib 'src/main/AndroidManifest.xml'
if (Test-Path $Manifest) {
  (Get-Content $Manifest -Raw).Replace('package="org.drinkless.td.libcore"','') | Set-Content $Manifest
  Write-Host "Patched manifest: $Manifest"
}

$TdApiFiles = Get-ChildItem -Path (Join-Path $Tdlib 'src/main/java') -Recurse -Filter 'TdApi.java' -ErrorAction SilentlyContinue
foreach ($f in $TdApiFiles) {
  $c = Get-Content $f.FullName -Raw
  $c = $c.Replace('import android.support.annotation.Nullable;','import androidx.annotation.Nullable;')
  $c = $c.Replace('import android.support.annotation.IntDef;','import androidx.annotation.IntDef;')
  Set-Content $f.FullName $c
  Write-Host "Patched annotations imports: $($f.FullName)"
}

$BuildFile = Join-Path $Tdlib 'build.gradle.kts'
if (Test-Path $BuildFile) {
  $c = Get-Content $BuildFile -Raw
  if ($c -notmatch 'namespace\s*=') { $c = $c -replace 'android\s*\{', "android {`n    namespace = \"org.drinkless.td.libcore\"" }
  if ($c -notmatch 'androidx.annotation:annotation:1.8.2') {
    if ($c -match 'dependencies\s*\{') {
      $c = $c -replace 'dependencies\s*\{', "dependencies {`n    implementation(\"androidx.annotation:annotation:1.8.2\")"
    } else {
      $c += "`n`ndependencies {`n    implementation(\"androidx.annotation:annotation:1.8.2\")`n}`n"
    }
  }
  Set-Content $BuildFile $c
  Write-Host "Patched build script: $BuildFile"
}

Write-Host "Done. Next steps:"
Write-Host "1) cd android-app"
Write-Host "2) .\gradlew.bat :app:assembleDebug"
