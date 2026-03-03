from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.models import ListeningHistory, Recommendation


def get_user_recommendations(db: Session, user_id: int) -> list[dict]:
    explicit_rows = db.execute(
        select(Recommendation.track_id, Recommendation.score)
        .where(Recommendation.user_id == user_id)
        .order_by(Recommendation.score.desc())
        .limit(50)
    ).all()

    explicit_map: dict[str, float] = {track_id: float(score) for track_id, score in explicit_rows}

    history_rows = db.execute(
        select(ListeningHistory.track_id, func.sum(ListeningHistory.listened_seconds).label('listened'))
        .where(ListeningHistory.user_id == user_id)
        .group_by(ListeningHistory.track_id)
        .order_by(func.sum(ListeningHistory.listened_seconds).desc())
        .limit(100)
    ).all()

    if history_rows:
        max_listened = max(float(row.listened or 0) for row in history_rows) or 1.0
        for row in history_rows:
            normalized = (float(row.listened or 0) / max_listened) * 0.5
            explicit_map[row.track_id] = explicit_map.get(row.track_id, 0.0) + normalized

    ranked = sorted(explicit_map.items(), key=lambda item: item[1], reverse=True)
    return [{"track_id": track_id, "score": round(score, 4)} for track_id, score in ranked[:50]]
