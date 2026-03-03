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
- `GET /recommendations/{user_id}`

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
