param(
  [ValidateSet("debug", "release")]
  [string]$BuildType = "release"
)

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if (-Not (Test-Path "./gradlew.bat")) {
  Write-Error "gradlew.bat not found. Generate wrapper first: gradle wrapper --gradle-version 8.7"
  exit 1
}

if ($BuildType -eq "release") {
  if (-Not (Test-Path "./keystore.properties")) {
    Write-Error "keystore.properties not found. Create it for signed release build (see README)."
    exit 1
  }
  .\gradlew.bat :app:assembleRelease
  Write-Host "APK: app/build/outputs/apk/release/app-release.apk"
} else {
  .\gradlew.bat :app:assembleDebug
  Write-Host "APK: app/build/outputs/apk/debug/app-debug.apk"
}
