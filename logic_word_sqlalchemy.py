from sqlalchemy import create_engine, ForeignKey, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker
import datetime
from sqlalchemy.orm import relationship
from logic_prompt_sqlalchemy import Prompt
# строка подключения
SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://easysolutions:password@localhost:5432/postgres'

# создаем движок SqlAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
# создаем базовый класс для моделей


class Base(DeclarativeBase):
    pass

# создаем модель, объекты которой будут храниться в бд


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String)
    last_datetime = Column(
        TIMESTAMP, default=datetime.datetime.now(datetime.UTC))
    first_datetime = Column(
        TIMESTAMP, default=datetime.datetime.now(datetime.UTC))
    synonims = relationship("Synonim", back_populates="word")
    antonyms = relationship("Antonym", back_populates="word")


class Synonim(Base):
    __tablename__ = "synonims"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, primary_key=True, index=True)
    synonim = Column(String)
    word = relationship("Word", back_populates="synonims")
    word_id = Column(Integer, ForeignKey("words.id"))


class Antonym(Base):
    __tablename__ = "antonyms"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, primary_key=True, index=True)
    antonym = Column(String)
    last_datetime = Column(
        TIMESTAMP, default=datetime.datetime.now(datetime.UTC))
    word = relationship("Word", back_populates="antonyms")
    word_id = Column(Integer, ForeignKey("words.id"))


def get_db():
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autoflush=False, bind=engine)
    db = SessionLocal()
    return db

def get_synonims_antonyms(word):
    word = word.lower()
    db = get_db()
    word_db = Word(word=word)
    res = db.query(Word).filter(Word.word == word).first()
    if res:
        db.query(Word).filter(Word.word == word).first().update({Word.last_datetime:datetime.datetime.now()})
        answer = 'синонимы: '
        lst = []
        for synonim in res.synonims:
            lst.append(synonim.synonim)
        answer += ' '.join(lst)
        answer += ' aнnонимы: '
        lst = []
        for antonim in res.antonyms:
            lst.append(antonim.antonim)
        answer += ' '.join(lst)
        return answer
    else:
        prompt = db.query(Prompt).order_by(Prompt.id.desc()).first()
        res = get_answer(prompt)
        for synonim in mes.synonyms:
            synonim_db = Synonim(synonim=synonim)
            word_db.synonims.extend([synonim_db])
        for antonim in mes.antonym:
            antonym_db = Antonym(antonim=antonim)
            word_db.antonyms.extend([antonym_db])
        db.add(word_db)
        db.commit()
    return res


if __name__ == "__main__":
    from logic_langgraph import get_prompt
    from logic_langchain import get_answer
    word = 'Добро'
    word = word.lower()
    db = get_db()
    word_db = Word(word=word)
    # b.add(word_db)
    # db.commit()
    res = db.query(Word).filter(Word.word == word).one()
    if res:
        print(res.synonims)
        print(res.synonims[0].synonim)
        answer = 'синонимы'
        lst = []
        for synonim in res.synonims:
            lst.append(synonim.synonim)
        print(lst)
    else:
        prompt = get_prompt(word='Добро')
        mes = get_answer(prompt)
        for synonim in mes.synonyms:
            synonim_db = Synonim(synonim=synonim)
            word_db.synonims.extend([synonim_db])
        for antonim in mes.antonym:
            antonym_db = Antonym(antonim=antonim)
            word_db.antonyms.extend([antonym_db])
        db.add(word_db)
        db.commit()
