#simple grapgh illustration
#grapgh:
#start -> [chatbot]-> end

from langgraph.graph import START, END, StateGraph
from typing_extensions import TypedDict
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

class State(TypedDict):
    query : str
    llm_result : str | None


#node 
def chatbot(state : State):
    user_query = state['query']
    # llm call with query
    client = OpenAI(
        api_key= GEMINI_API_KEY,
        base_url= 'https://generativelanguage.googleapis.com/v1beta/openai/'
    )
    result = client.chat.completions.create(
        model="gemini-2.0-flash-lite",
        messages=[
            {'role':'user', 'content' : user_query}
        ]
    )
    state['llm_result'] = result.choices[0].message.content

    return state

#build graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()


def main():
    query = input("-> ")

    #invoke the graph 
    _state = {
        "query" : query,
        "llm_result" : None
    }

    graph_result = graph.invoke(_state)
    print(graph_result)


main()
