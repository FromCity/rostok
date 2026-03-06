from logic_db import get_db
from fastapi import FastAPI
from logic_prompt_sqlalchemy import Prompt
from logic_word_sqlalchemy import get_synonims_antonyms

app = FastAPI()


@app.post("/")
def synonyms(word):
    res = get_synonims_antonyms(word)
    return res


@app.get('/prompts')
def prompt():
    db = get_db()
    prompts = db.query(Prompt).all()
    return prompts

@app.get('/prompt')
def prompt():
    db = get_db()
    prompt = db.query(Prompt).order_by(Prompt.id.desc()).first()
    return prompt

@app.post('/prompt')
def prompt_insert(prompt_in, version):
    db = get_db()
    prompt = Prompt(prompt=prompt_in,
                    version=version)
    db.add(prompt)
    db.commit()
    ans = prompt = db.query(Prompt).order_by(Prompt.id.desc()).first()
    return ans

@app.put('/prompt')
def prompt_update(prompt_in, id):
    db = get_db()
    db.query(Prompt).filter_by(id=id).update({Prompt.prompt:prompt_in})
    db.commit()
    ans = db.query(Prompt).filter_by(id=id).one()
    return ans

@app.delete('/prompt')
def prompt_delete(id):
    db = get_db()
    db.query(Prompt).filter_by(id=id).delete()
    db.commit()
    return id