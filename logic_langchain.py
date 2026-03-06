from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import List

with open('api_key.txt') as f:
    api_key = f.read().strip()

class Answer(BaseModel):
    word: str
    synonyms: List[str]
    antonyms: List[str]


def get_answer(prompt):
    model = ChatOpenAI(model="gpt-4o-mini-2024-07-18",
                       api_key=api_key,
                       base_url='https://openrouter.ai/api/v1')

    model_with_tools = model.bind_tools([Answer])

    messages = [
        SystemMessage("You should only give answers in Russian."),
        HumanMessage(
            prompt),
    ]

    ai_msg = model_with_tools.invoke(messages)

    return ai_msg.tool_calls[0]['args']


if __name__ == "__main__":
    word = 'добро'
    from logic_langgraph import get_prompt
    prompt = get_prompt(word=word)
    mes = get_answer(prompt)
    print('mes:', mes)
