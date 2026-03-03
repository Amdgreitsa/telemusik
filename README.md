# TeleMusik Monorepo

Production-oriented platform for a Telegram-powered music streaming Android client with backend services and APK distribution website.

## Components

- `android-app/` — Android app (Kotlin, Material 3, ExoPlayer, TDLib, Room, WorkManager)
- `backend/` — FastAPI backend (Ubuntu 24.04 target, PostgreSQL, Redis, recommendations + Last.fm scrobbling queue)
- `website/` — Next.js 14 + Tailwind marketing/download website
- `deploy/` — Nginx, Docker Compose, operational configs

## Quick start (local)

### 1) Backend

```bash
cd backend
cp .env.example .env
docker compose up -d --build
```

Backend endpoints:
- `GET /health`
- `GET /app/latest`
- `GET /app/changelog`
- `POST /scrobble/now-playing`
- `POST /scrobble/submit`
- `POST /scrobble/process?session_key=...`
- `GET /recommendations` (JWT required)
- `POST /auth/telegram`

### 2) Website

```bash
cd website
cp .env.example .env.local
npm ci
npm run dev
```

### 3) Android app

Open `android-app/` in Android Studio (Panda or newer) and run on Android 8.0+.

Set `local.properties`:

```properties
telegram.apiId=YOUR_TD_API_ID
telegram.apiHash=YOUR_TD_API_HASH
backend.baseUrl=https://api.example.com
lastfm.apiKey=YOUR_LASTFM_API_KEY
lastfm.apiSecret=YOUR_LASTFM_API_SECRET
```

## VPS deployment (Ubuntu 24.04)

1. Install Docker + Compose plugin.
2. Copy repository to `/opt/telemusik`.
3. Put release APK in `/var/www/app/releases/telemusik-vX.Y.Z.apk`.
4. Configure `.env` in `backend/` and `website/.env.local`.
5. Run:

```bash
cd /opt/telemusik/deploy
docker compose up -d --build
```

Nginx handles HTTPS, redirect HTTP→HTTPS, gzip and cache headers.

## Data policy

Server does **not** store Telegram audio files.
Server stores only:
- user identifiers
- listening stats / history
- recommendation artifacts
- APK metadata/changelog

## Security highlights

- Android encrypted offline files + checksum validation
- Last.fm session key stored encrypted (Android Keystore / backend secret management)
- JWT for backend client APIs
- Rate limiting and structured audit logging in backend

## CI

GitHub Actions workflow runs backend tests and frontend lint/build checks.

## Implemented hardening (v2)

- JWT auth for user-scoped API operations (`/auth/telegram`, protected recommendations/scrobble endpoints).
- Persistent scrobble queue table with retry counters and manual processing endpoint.
- Android Room DAOs and bottom-navigation shell to replace plain single-screen placeholder.
- Website technical auth page for API token bootstrap/testing.


## Production readiness upgrades

- API hardening: JWT issuer/audience validation, admin-protected scrobble queue processing, request-id middleware and structured request logging.
- Data consistency: scrobble queue idempotency via fingerprint unique constraint to prevent duplicate submits.
- Resilience: Last.fm client includes retry with exponential backoff for transient failures.
- Android media service: upgraded from plain `Service` to `MediaSessionService` with ExoPlayer lifecycle management and launcher activity manifest wiring.
- Website observability: landing page now shows backend health status from API.
- Android TDLib client now tracks auth states (`phone/code/password/ready`) and maps channel audio history to structured track metadata.
- Offline repository now includes checksum verification and cache limit enforcement with oldest-first eviction.
- Android UI baseline completed for Channels/Player/Profile/Settings with interactive controls and in-app navigation wiring.
- Recommendations service now falls back to listening-history aggregation when explicit model rows are absent.


## Android Studio/Gradle JVM note (Windows)

If Android Studio shows: *"It is not possible to use the currently selected Gradle JVM..."*

1. Open **Settings → Build, Execution, Deployment → Build Tools → Gradle**.
2. Set **Gradle JDK = Embedded JDK 17** (or another valid local JDK 17 installation).
3. Run wrapper commands from `android-app/`:

```bash
./gradlew --version
./gradlew tasks
```

This repository includes Gradle Wrapper scripts/config (`gradlew`, `gradlew.bat`, `gradle/wrapper/gradle-wrapper.properties`) pinned to Gradle 8.7 for AGP 8.5.x compatibility. In binary-restricted PR systems, regenerate `gradle-wrapper.jar` locally with `gradle wrapper --gradle-version 8.7`.


## Local TDLib module compatibility (Android Studio)

If you include a local `:tdlib` module and get errors:
- `Incorrect package=... in AndroidManifest.xml`
- `package android.support.annotation does not exist`

Apply these fixes inside `android-app/tdlib`:

1. In `src/main/AndroidManifest.xml`, remove `package="..."` attribute from `<manifest>`.
2. In `src/main/java/.../TdApi.java`, replace:
   - `android.support.annotation.Nullable` -> `androidx.annotation.Nullable`
   - `android.support.annotation.IntDef` -> `androidx.annotation.IntDef`
3. In `tdlib/build.gradle.kts`, ensure:

```kotlin
plugins { id("com.android.library") }

android {
    namespace = "org.drinkless.td.libcore"
    compileSdk = 34
    defaultConfig { minSdk = 26 }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

dependencies {
    implementation("androidx.annotation:annotation:1.8.2")
}
```

The app build is configured to automatically use local `:tdlib` when the module exists, otherwise it falls back to Maven dependency `org.drinkless.tdlib:tdlib`.


## APK build guide (max detailed)

### Prerequisites (Windows + Android Studio Panda)

1. Install **Android Studio Panda**.
2. Install SDK components:
   - Android SDK Platform 34
   - Android SDK Build-Tools (latest for API 34)
   - NDK and CMake (if your local TDLib module compiles native libs)
3. Set Gradle JDK to **JDK 17**:
   - `Settings -> Build, Execution, Deployment -> Build Tools -> Gradle -> Gradle JDK`
4. Open project root: `android-app/`.

### TDLib mode selection

The app supports two modes automatically:

- **Remote Maven TDLib**: default fallback `org.drinkless.tdlib:tdlib:1.8.40`
- **Local module TDLib**: if `android-app/tdlib` exists, Gradle uses `project(":tdlib")`

### If you use local `:tdlib` and get compile errors

Apply these mandatory fixes inside local module:

1. `tdlib/src/main/AndroidManifest.xml`:
   - remove `package="..."` from `<manifest>` root
2. In generated/legacy `TdApi.java`:
   - `android.support.annotation.Nullable` -> `androidx.annotation.Nullable`
   - `android.support.annotation.IntDef` -> `androidx.annotation.IntDef`
3. `tdlib/build.gradle.kts` must contain:
   - `plugins { id("com.android.library") }`
   - `android { namespace = "org.drinkless.td.libcore"; compileSdk = 34; defaultConfig { minSdk = 26 } }`
   - Java 17 compile options
   - dependency `implementation("androidx.annotation:annotation:1.8.2")`

### Debug APK build

From terminal:

```bash
cd android-app
./scripts/build-apk.sh debug
```

Output:
- `android-app/app/build/outputs/apk/debug/app-debug.apk`

Windows PowerShell:

```powershell
cd android-app
./scripts/build-apk.ps1 -BuildType debug
```

### Release APK build (signed)

1. Create keystore (one-time):

```bash
keytool -genkeypair -v -keystore telemusik-release.jks -alias telemusik -keyalg RSA -keysize 2048 -validity 10000
```

2. Create `android-app/keystore.properties`:

```properties
storeFile=telemusik-release.jks
storePassword=YOUR_STORE_PASSWORD
keyAlias=telemusik
keyPassword=YOUR_KEY_PASSWORD
```

3. Build signed release APK:

```bash
cd android-app
./scripts/build-apk.sh release
```

Windows PowerShell:

```powershell
cd android-app
./scripts/build-apk.ps1 -BuildType release
```

Output:
- `android-app/app/build/outputs/apk/release/app-release.apk`

### Verify APK signature

```bash
apksigner verify --verbose android-app/app/build/outputs/apk/release/app-release.apk
```


### One-command auto-fix for local TDLib module

If your local `:tdlib` module throws exactly the errors you pasted (`Incorrect package=...` and `android.support.annotation...`), run:

```bash
cd android-app
./scripts/fix-local-tdlib.sh
./gradlew :app:assembleDebug
```

Windows PowerShell:

```powershell
cd android-app
./scripts/fix-local-tdlib.ps1
./gradlew.bat :app:assembleDebug
```

The fixer script:
- removes deprecated `package="..."` from `tdlib/src/main/AndroidManifest.xml`
- migrates `android.support.annotation.{Nullable,IntDef}` to `androidx.annotation.*` in `TdApi.java`
- ensures `tdlib/build.gradle.kts` contains namespace and `androidx.annotation` dependency

### Common failures and fixes

- **"currently selected Gradle JVM"**:
  - switch Gradle JDK to embedded/local JDK 17 in Android Studio.
- **`Incorrect package="..." in tdlib manifest`**:
  - remove `package` attribute from local tdlib manifest.
- **`android.support.annotation` not found**:
  - migrate imports to `androidx.annotation` and add `androidx.annotation` dependency in tdlib module.
- **`next: not found` or Python module missing in local checks**:
  - run `npm ci` in `website/` and `pip install -r backend/requirements.txt` in backend environment.
