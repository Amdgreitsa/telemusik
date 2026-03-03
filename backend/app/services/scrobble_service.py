from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import ScrobbleQueueItem, User
from app.services import lastfm_service


def enqueue_now_playing(db: Session, user: User, artist: str, track: str, duration: int) -> ScrobbleQueueItem:
    item = ScrobbleQueueItem(
        user_id=user.id,
        artist=artist,
        track=track,
        duration=duration,
        now_playing=True,
        played_at=0,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def enqueue_scrobble(db: Session, user: User, artist: str, track: str, duration: int, played_at: int) -> ScrobbleQueueItem:
    item = ScrobbleQueueItem(
        user_id=user.id,
        artist=artist,
        track=track,
        duration=duration,
        now_playing=False,
        played_at=played_at,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


async def process_queue(db: Session, session_key: str, limit: int = 50) -> tuple[int, int]:
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
