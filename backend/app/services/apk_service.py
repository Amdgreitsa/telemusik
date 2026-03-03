from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import ApkRelease


def get_latest_release(db: Session) -> ApkRelease | None:
    return db.execute(select(ApkRelease).order_by(ApkRelease.created_at.desc())).scalars().first()


def get_changelog(db: Session) -> list[ApkRelease]:
    return list(db.execute(select(ApkRelease).order_by(ApkRelease.created_at.desc())).scalars().all())
