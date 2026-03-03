from sqlalchemy import text
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_token, get_current_user, require_admin_key
from app.db.session import get_db
from app.models.models import User
from app.schemas.schemas import (
    ApkInfo,
    AuthRequest,
    AuthResponse,
    ChangelogItem,
    QueueProcessResponse,
    ScrobbleNowPlaying,
    ScrobbleSubmit,
)
from app.services import apk_service, recommendation_service, scrobble_service, user_service

router = APIRouter()


@router.get('/health')
def health(db: Session = Depends(get_db)):
    db.execute(text('SELECT 1'))
    return {'status': 'ok'}


@router.post('/auth/telegram', response_model=AuthResponse)
def auth_telegram(payload: AuthRequest, db: Session = Depends(get_db)):
    user = user_service.get_or_create_user(db, payload.telegram_user_id)
    return AuthResponse(access_token=create_token(user.id))


@router.get('/app/latest', response_model=ApkInfo)
def app_latest(db: Session = Depends(get_db)):
    release = apk_service.get_latest_release(db)
    if not release:
        raise HTTPException(status_code=404, detail='No APK release configured')
    return ApkInfo(version=release.version_name, download_url=f'/releases/{release.file_name}')


@router.get('/app/changelog', response_model=list[ChangelogItem])
def app_changelog(db: Session = Depends(get_db)):
    return [ChangelogItem(version=r.version_name, changelog=r.changelog) for r in apk_service.get_changelog(db)]


@router.get('/recommendations')
def recommendations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {'items': recommendation_service.get_user_recommendations(db, current_user.id)}


@router.post('/scrobble/now-playing')
async def scrobble_now_playing(
    payload: ScrobbleNowPlaying,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = scrobble_service.enqueue_now_playing(db, current_user, payload.artist, payload.track, payload.duration)
    return {'queued': True, 'queue_id': item.id}


@router.post('/scrobble/submit')
async def scrobble_submit(
    payload: ScrobbleSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = scrobble_service.enqueue_scrobble(
        db,
        current_user,
        payload.artist,
        payload.track,
        payload.duration,
        payload.played_at,
    )
    return {'queued': True, 'queue_id': item.id}


@router.post('/scrobble/process', response_model=QueueProcessResponse, dependencies=[Depends(require_admin_key)])
async def scrobble_process(session_key: str, db: Session = Depends(get_db)):
    processed, failed = await scrobble_service.process_queue(db, session_key)
    return QueueProcessResponse(processed=processed, failed=failed)
