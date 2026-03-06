from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface import ChatHuggingFace
from pydantic import BaseModel
from typing import List
import json

with open('token.txt') as f:
    token = f.read().strip()


class Answer(BaseModel):
    word: str
    synonyms: List[str]
    antonyms: List[str]


def get_answer(prompt):
    model_repo_id = "meta-llama/Meta-Llama-3-8B-Instruct"

    llm = HuggingFaceEndpoint(
        repo_id=model_repo_id,
        temperature=0.8,
        task="text-generation",
        max_new_tokens=1000,
        do_sample=False,
        huggingfacehub_api_token=token
    )

    model = ChatHuggingFace(llm=llm)

    end_prompt = f"""Ты должен вернуть данные в точном JSON формате.
        Пример корректного ответа:
        {json.dumps(Answer.model_json_schema(), ensure_ascii=False)}

        Схема:
        - word: строка
        - synonyms: список из синонимов
        - antonyms: список из антонимов
        """
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         f"You should only give answers in Russian."),
        ("user", prompt + end_prompt)
    ], template_format="jinja2")

    chain = prompt | model
    answer = chain.invoke({}).content
    return answer
    try:
        out = Answer(**json.loads(answer))
    except Exception:
        out = 'ответ не прошёл валидацию'
    return out


if __name__ == "__main__":
    word = 'добро'
    from logic_langgraph import get_prompt
    prompt = get_prompt(word=word)
    mes = get_answer(prompt)
    print('mes:', mes)
