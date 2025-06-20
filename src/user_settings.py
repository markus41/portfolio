from __future__ import annotations

"""Simple per-user configuration storage using SQLite."""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional

try:  # pragma: no cover - optional dependency
    from sqlalchemy import JSON, Column, DateTime, Integer, String, create_engine
    from sqlalchemy.orm import declarative_base, sessionmaker
except Exception:  # pragma: no cover - graceful fallback
    class _Dummy:
        def __init__(self, *_, **__):
            pass

    JSON = Column = DateTime = Integer = String = _Dummy  # type: ignore

    def declarative_base():  # type: ignore
        class Base:
            pass

        return Base

    def sessionmaker(**_):  # type: ignore
        return None

    create_engine = None

Base = declarative_base()
SessionLocal = sessionmaker() if callable(sessionmaker) else None


@dataclass
class UserSettingsData:
    """Typed representation of settings returned by :func:`get_settings`."""

    api_key: str
    organization: Optional[str] = None
    openai_api_key: Optional[str] = None
    crm_api_url: Optional[str] = None
    crm_api_key: Optional[str] = None
    email_service_api_key: Optional[str] = None
    disabled_teams: Optional[List[str]] = None

    def dict(self) -> dict:
        return asdict(self)


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True)
    api_key = Column(String, unique=True, index=True, nullable=False)
    organization = Column(String)
    openai_api_key = Column(String)
    crm_api_url = Column(String)
    crm_api_key = Column(String)
    email_service_api_key = Column(String)
    disabled_teams = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def init_db(url: str) -> None:
    """Initialise the SQLite database configured at ``url``."""

    if not create_engine or not callable(SessionLocal):
        return
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    SessionLocal.configure(bind=engine)


def get_settings(api_key: str) -> Optional[UserSettingsData]:
    """Return settings for ``api_key`` if present."""

    if not callable(SessionLocal):
        return None
    session = SessionLocal()
    try:
        rec: UserSettings | None = (
            session.query(UserSettings).filter_by(api_key=api_key).first()
        )
        if not rec:
            return None
        return UserSettingsData(
            api_key=rec.api_key,
            organization=rec.organization,
            openai_api_key=rec.openai_api_key,
            crm_api_url=rec.crm_api_url,
            crm_api_key=rec.crm_api_key,
            email_service_api_key=rec.email_service_api_key,
            disabled_teams=rec.disabled_teams or [],
        )
    finally:
        session.close()


def upsert_settings(api_key: str, data: UserSettingsData) -> UserSettingsData:
    """Create or update settings for ``api_key`` with ``data``."""

    if not callable(SessionLocal):
        return data
    session = SessionLocal()
    try:
        rec: UserSettings | None = (
            session.query(UserSettings).filter_by(api_key=api_key).first()
        )
        if rec is None:
            rec = UserSettings(api_key=api_key)
            session.add(rec)
        rec.organization = data.organization
        rec.openai_api_key = data.openai_api_key
        rec.crm_api_url = data.crm_api_url
        rec.crm_api_key = data.crm_api_key
        rec.email_service_api_key = data.email_service_api_key
        rec.disabled_teams = data.disabled_teams
        session.commit()
        session.refresh(rec)
        return get_settings(api_key)
    finally:
        session.close()
