from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import User


def get_or_create_user(db: Session, telegram_user_id: str) -> User:
    user = db.execute(select(User).where(User.telegram_user_id == telegram_user_id)).scalars().first()
    if user:
        return user
    user = User(telegram_user_id=telegram_user_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
