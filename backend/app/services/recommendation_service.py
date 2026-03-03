from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Recommendation


def get_user_recommendations(db: Session, user_id: int) -> list[dict]:
    rows = db.execute(
        select(Recommendation).where(Recommendation.user_id == user_id).order_by(Recommendation.score.desc()).limit(50)
    ).scalars().all()
    return [{"track_id": r.track_id, "score": r.score} for r in rows]
