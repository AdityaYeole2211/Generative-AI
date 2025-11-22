from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.types import interrupt, Command
import json

load_dotenv()

@tool
def human_assitance(query : str)-> str:
    """ Request assitance from a human """
    human_response = interrupt({"query" : query}) #this saves the state in db and kills the graph
    return human_response

tools = [human_assitance]
class State(TypedDict):
    messages : Annotated[list,add_messages]

llm = init_chat_model(model_provider="google_genai", model="gemini-2.0-flash-lite")
llm_with_tools = llm.bind_tools(tools)

def chatbot(state):
    messages = llm_with_tools.invoke(state['messages'])
    return {"messages" : [messages]}

tool_node = ToolNode(tools=tools)

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("chatbot", END)

def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)

def user_call():
    DB_URI = "mongodb://admin:admin@mongo-db:27017"
    config = {"configurable" : {"thread_id" : "13"}}
    
    with MongoDBSaver.from_conn_string(DB_URI) as mongo_checkpointer:
        graph_with_cp = create_chat_graph(mongo_checkpointer)
        
        while True:
            user_query = input("-> ")
            state = State(
                messages = [{'role' : 'user', 'content' : user_query}]
            )
            
            for event in graph_with_cp.stream(state, config, stream_mode="values"):
                if "messages" in event:
                    event["messages"][-1].pretty_print()

def admin_call():
    DB_URI = "mongodb://admin:admin@mongo-db:27017"
    config  = {"configurable" : {"thread_id" : "13"}}
    
    with MongoDBSaver.from_conn_string(DB_URI) as mongo_checkpointer:
        graph_with_cp = create_chat_graph(mongo_checkpointer)
        
        state = graph_with_cp.get_state(config=config)
        # print("STATE : \n\n", state, "\n\n")

        # ✅ interrupt payload already contains the user query
        if not state.interrupts:
            print("No pending human assistance interrupt.")
            return
        
        last_interrupt = state.interrupts[-1]
        interrupt_payload = last_interrupt.value   # {'query': 'i want to know about coupons in genai course'}
        user_query = interrupt_payload.get("query")

        print("User has a query:", user_query)

        solution = input("-> ")

        # You pass solution back to the graph as the tool return value
        resume_command = Command(resume={"data": solution})

        for event in graph_with_cp.stream(resume_command, config, stream_mode="values"):
            if "messages" in event:
                event["messages"][-1].pretty_print()
                
                
# admin_call()
user_call()











'''
INTERRUPT WITH HUMAN ASSISTANCE TOOL CALL:

================================ Human Message =================================

i am having a payment issue . can you please connect me to someone 
================================== Ai Message ==================================
Tool Calls:
  human_assitance (e09fa54c-feee-4231-a32d-90ddcd88116d)
 Call ID: e09fa54c-feee-4231-a32d-90ddcd88116d
  Args:
    query: I am having a payment issue. Please connect me to a human for assistance.
    
'''