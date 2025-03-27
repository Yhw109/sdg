from typing import Annotated
from sqlmodel import Session, create_engine, SQLModel
from .config import settings
from fastapi import Depends

engine = create_engine(str(settings.DATABASE_URI))

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
