# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import settings
from sqlmodel import create_engine,Session

print(f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}")

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = Session(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()