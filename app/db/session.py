from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.utils.config import get_settings

DATABASE_URL_SYNC = get_settings().database_url_sync

sync_engine = create_engine(DATABASE_URL_SYNC)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
