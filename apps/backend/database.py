from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .settings import settings

# SQLAlchemy engine
# If using SQLite, keep check_same_thread=False
connect_args = {"check_same_thread": False} if settings.DB_URL.startswith("sqlite") else {}
engine = create_engine(settings.DB_URL, connect_args=connect_args)

# Session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Declarative base (THIS is the Base you were missing)
Base = declarative_base()

# Dependency for FastAPI routes
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
