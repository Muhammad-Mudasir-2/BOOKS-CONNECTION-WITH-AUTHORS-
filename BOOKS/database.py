from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# To recreate the table (only do this if you're okay with losing existing data)


# SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://user_3:123@localhost:5433/bs_system'
SQLALCHEMY_DATABASE_URL = 'sqlite:///./books_crud.db'


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
