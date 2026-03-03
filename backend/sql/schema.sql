CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    telegram_user_id VARCHAR(64) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS listening_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    track_id VARCHAR(128) NOT NULL,
    listened_seconds INTEGER NOT NULL,
    listened_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS recommendations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    track_id VARCHAR(128) NOT NULL,
    score DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS apk_releases (
    id SERIAL PRIMARY KEY,
    version_name VARCHAR(32) UNIQUE NOT NULL,
    file_name VARCHAR(256) NOT NULL,
    changelog TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS scrobble_queue (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    artist VARCHAR(128) NOT NULL,
    track VARCHAR(128) NOT NULL,
    duration INTEGER NOT NULL DEFAULT 0,
    played_at INTEGER NOT NULL DEFAULT 0,
    now_playing BOOLEAN NOT NULL DEFAULT FALSE,
    fingerprint VARCHAR(64) NOT NULL,
    retries INTEGER NOT NULL DEFAULT 0,
    processed BOOLEAN NOT NULL DEFAULT FALSE,
    error VARCHAR(255) NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_scrobble_user_fingerprint UNIQUE (user_id, fingerprint)
);

CREATE INDEX IF NOT EXISTS idx_scrobble_queue_unprocessed ON scrobble_queue (processed, retries, created_at);
