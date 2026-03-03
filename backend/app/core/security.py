from datetime import UTC, datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.models import User

ALGORITHM = 'HS256'
TOKEN_TTL_HOURS = 24 * 30
bearer = HTTPBearer(auto_error=True)


def create_token(user_id: int) -> str:
    payload = {
        'sub': str(user_id),
        'exp': datetime.now(UTC) + timedelta(hours=TOKEN_TTL_HOURS),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(credentials.credentials, settings.jwt_secret, algorithms=[ALGORITHM])
        user_id = int(payload['sub'])
    except (JWTError, KeyError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token') from exc

    user = db.execute(select(User).where(User.id == user_id)).scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user
