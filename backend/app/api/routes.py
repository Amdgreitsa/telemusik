from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.schemas import ApkInfo, ChangelogItem, ScrobbleNowPlaying, ScrobbleSubmit
from app.services import apk_service, recommendation_service

router = APIRouter()


@router.get('/health')
def health():
    return {'status': 'ok'}


@router.get('/app/latest', response_model=ApkInfo)
def app_latest(db: Session = Depends(get_db)):
    release = apk_service.get_latest_release(db)
    if not release:
        raise HTTPException(status_code=404, detail='No APK release configured')
    return ApkInfo(version=release.version_name, download_url=f'/releases/{release.file_name}')


@router.get('/app/changelog', response_model=list[ChangelogItem])
def app_changelog(db: Session = Depends(get_db)):
    return [ChangelogItem(version=r.version_name, changelog=r.changelog) for r in apk_service.get_changelog(db)]


@router.get('/recommendations/{user_id}')
def recommendations(user_id: int, db: Session = Depends(get_db)):
    return {'items': recommendation_service.get_user_recommendations(db, user_id)}


@router.post('/scrobble/now-playing')
async def scrobble_now_playing(payload: ScrobbleNowPlaying):
    # session keys are intentionally not persisted in this example; fetch from secure store in production
    return {'queued': True, 'payload': payload.model_dump()}


@router.post('/scrobble/submit')
async def scrobble_submit(payload: ScrobbleSubmit):
    return {'queued': True, 'payload': payload.model_dump()}
