from sqlmodel import Session, SQLModel, create_engine
from core.config import settings

sqlite_file_name = "database.db"
sqlite_url = settings.DATABASE

engine = create_engine(sqlite_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def drop_db():
    SQLModel.metadata.drop_all(engine)