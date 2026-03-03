from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings

_engine_kwargs = {'pool_pre_ping': True}
if settings.database_url.startswith('sqlite+pysqlite:///:memory:'):
    _engine_kwargs['connect_args'] = {'check_same_thread': False}
    _engine_kwargs['poolclass'] = StaticPool

engine = create_engine(settings.database_url, **_engine_kwargs)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
