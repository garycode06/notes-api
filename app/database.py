from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine
from app.core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=True,
    autoflush=True,
    bind=engine
)

class Base(DeclarativeBase):
    pass