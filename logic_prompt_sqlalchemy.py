from sqlalchemy import TIMESTAMP
from sqlalchemy import Column, String, Integer
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from config import Config


class Base(DeclarativeBase):
    pass


config = Config.load()

# строка подключения
SQLALCHEMY_DATABASE_URL = config.db.SQLALCHEMY_DATABASE_URL

# создаем движок SqlAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)


def get_db():
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autoflush=False, bind=engine)
    db = SessionLocal()
    return db


class Base(DeclarativeBase):
    pass

# создаем модель, объекты которой будут храниться в бд


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String)
    version = Column(Integer)
    adding_datetime = Column(
        TIMESTAMP, default=datetime.datetime.now(datetime.UTC))


if __name__ == "__main__":
    db = get_db()
    prompt = Prompt(prompt='покажи десять антонимов и синонимов слов к слову ',
                    version=1)
    db.add(prompt)
    db.commit()
