from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from config import Config
config = Config.load()


def get_prompt(word):
    class State(TypedDict):
        graph_state: str

    def node_1(state):
        return {"graph_state": state['graph_state'] + f"Покажи {config.synonims.num} синонимов и {config.antomyms.num} антонимов "}

    def node_2(state, word=word):
        return {"graph_state": state['graph_state'] + f'к слову {word}'}

    builder = StateGraph(State)
    builder.add_node("node_1", node_1)
    builder.add_node("node_2", node_2)

    builder.add_edge(START, 'node_1')
    builder.add_edge('node_1', "node_2")
    builder.add_edge("node_2", END)

    graph = builder.compile()

    prompt = graph.invoke({"graph_state": ""})

    return prompt["graph_state"]


if __name__ == "__main__":
    print(get_prompt(word='добро'))
