from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
import requests

load_dotenv()

@tool()
def get_weather(city : str):
    """This function/tool takes a city name as an input and returns the current weather of the city."""
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    
    return "Something went wrong"

tools = [get_weather]
class State(TypedDict):
    messages : Annotated[list, add_messages]

llm = init_chat_model(model_provider="google_genai", model="gemini-2.0-flash-lite")
llm_with_tools = llm.bind_tools(tools)

def chat_node(state:State):
    message = llm_with_tools.invoke(state['messages'])
    return {"messages" : [message]}

tool_node = ToolNode(tools=[get_weather])


graph_builder = StateGraph(State)
graph_builder.add_node("chat_node", chat_node)
graph_builder.add_node("tools", tool_node)
graph_builder.add_edge(START, "chat_node")

graph_builder.add_conditional_edges("chat_node", tools_condition)
graph_builder.add_edge("tools", "chat_node")


graph = graph_builder.compile()


def main():
    query = input("-> ")
    
    _state = State(
        messages = [{"role" : "user", "content" : query}]
    )
    
    for event in graph.stream(_state, stream_mode="values"):
        if "messages" in event:
            event["messages"][-1].pretty_print()


main()






'''
Raw output for tool call : 
Tool Calls:
  get_weather (35c9b4ed-2447-4454-acf9-64aad9f190c0)
 Call ID: 35c9b4ed-2447-4454-acf9-64aad9f190c0
  Args:
    city: Delhi

returns a tool call id -> uses tool call id to differentiate between consecutive tool  calls


TOOL_CALL OUTPUT: 
 python tool_call.py
-> what is weather of nagpur
================================ Human Message =================================

what is weather of nagpur
================================== Ai Message ==================================
Tool Calls:
  get_weather (12b68ba7-6786-4e33-8fbe-d8523db223b3)
 Call ID: 12b68ba7-6786-4e33-8fbe-d8523db223b3
  Args:
    city: nagpur
================================= Tool Message =================================
Name: get_weather

The weather in nagpur is Haze +28°C.
================================== Ai Message ==================================

The weather in nagpur is Haze +28°C.
'''