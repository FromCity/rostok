
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


config = Config.load()

print(f"{config.db.SQLALCHEMY_DATABASE_URL=}")
print(f"{config.antomyms.num=}")
print(f"{config.synonims.num=}")
