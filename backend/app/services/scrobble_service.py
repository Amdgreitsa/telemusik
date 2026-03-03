import hashlib
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.models import ScrobbleQueueItem, User
from app.services import lastfm_service


def _fingerprint(user_id: int, artist: str, track: str, played_at: int, now_playing: bool) -> str:
    payload = f'{user_id}:{artist.strip().lower()}:{track.strip().lower()}:{played_at}:{int(now_playing)}'
    return hashlib.sha256(payload.encode()).hexdigest()


def _enqueue(
    db: Session,
    user: User,
    artist: str,
    track: str,
    duration: int,
    played_at: int,
    now_playing: bool,
) -> ScrobbleQueueItem:
    normalized_artist = artist.strip()
    normalized_track = track.strip()
    fp = _fingerprint(user.id, normalized_artist, normalized_track, played_at, now_playing)

    item = ScrobbleQueueItem(
        user_id=user.id,
        artist=normalized_artist,
        track=normalized_track,
        duration=max(duration, 0),
        now_playing=now_playing,
        played_at=played_at,
        fingerprint=fp,
    )
    db.add(item)
    try:
        db.commit()
        db.refresh(item)
        return item
    except IntegrityError:
        db.rollback()
        existing = db.execute(
            select(ScrobbleQueueItem).where(
                ScrobbleQueueItem.user_id == user.id,
                ScrobbleQueueItem.fingerprint == fp,
            )
        ).scalars().first()
        if existing:
            return existing
        raise


def enqueue_now_playing(db: Session, user: User, artist: str, track: str, duration: int) -> ScrobbleQueueItem:
    return _enqueue(db, user, artist, track, duration, played_at=0, now_playing=True)


def enqueue_scrobble(db: Session, user: User, artist: str, track: str, duration: int, played_at: int) -> ScrobbleQueueItem:
    return _enqueue(db, user, artist, track, duration, played_at=played_at, now_playing=False)


async def process_queue(db: Session, session_key: str, limit: int = 100) -> tuple[int, int]:
    items = db.execute(
        select(ScrobbleQueueItem)
        .where(ScrobbleQueueItem.processed.is_(False), ScrobbleQueueItem.retries < 5)
        .order_by(ScrobbleQueueItem.created_at.asc())
        .limit(limit)
    ).scalars().all()
    processed, failed = 0, 0
    for item in items:
        try:
            if item.now_playing:
                await lastfm_service.now_playing(session_key, item.artist, item.track, item.duration)
            else:
                await lastfm_service.scrobble(session_key, item.artist, item.track, item.played_at)
            item.processed = True
            item.error = ''
            processed += 1
        except Exception as exc:  # noqa: BLE001
            item.retries += 1
            item.error = str(exc)[:255]
            failed += 1
    db.commit()
    return processed, failed
