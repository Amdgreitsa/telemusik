from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_user_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ListeningHistory(Base):
    __tablename__ = 'listening_history'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    track_id: Mapped[str] = mapped_column(String(128), index=True)
    listened_seconds: Mapped[int] = mapped_column(Integer)
    listened_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Recommendation(Base):
    __tablename__ = 'recommendations'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    track_id: Mapped[str] = mapped_column(String(128), index=True)
    score: Mapped[float] = mapped_column(Float)


class ApkRelease(Base):
    __tablename__ = 'apk_releases'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    version_name: Mapped[str] = mapped_column(String(32), unique=True)
    file_name: Mapped[str] = mapped_column(String(256))
    changelog: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ScrobbleQueueItem(Base):
    __tablename__ = 'scrobble_queue'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    artist: Mapped[str] = mapped_column(String(128))
    track: Mapped[str] = mapped_column(String(128))
    duration: Mapped[int] = mapped_column(Integer, default=0)
    played_at: Mapped[int] = mapped_column(Integer, default=0)
    now_playing: Mapped[bool] = mapped_column(Boolean, default=False)
    retries: Mapped[int] = mapped_column(Integer, default=0)
    processed: Mapped[bool] = mapped_column(Boolean, default=False)
    error: Mapped[str] = mapped_column(String(255), default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
