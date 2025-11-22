from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()



class State(TypedDict):
    messages : Annotated[list,add_messages]

llm = init_chat_model(model_provider="google_genai", model='gemini-2.5-flash-lite')

def chat_node(state:State):
    
    response = llm.invoke(state['messages'])
    return {'messages' : [response]} #anotated automatically adds in existing messages, appends not rewritee

graph_builder = StateGraph(State)
graph_builder.add_node("chat_node", chat_node)
graph_builder.add_edge(START, "chat_node")
graph_builder.add_edge("chat_node", END)
# graph = graph_builder.compile()

def compile_with_checkpointer(checkpointer):
    graph_with_checkpointer = graph_builder.compile(checkpointer=checkpointer)
    return graph_with_checkpointer

def main():
    DB_URI = "mongodb://admin:admin@mongo-db:27017"  #mongodb://<username>:<pass>@<host>:<port>
    config = {"configurable" : {"thread_id" : "2"}} #thread_id needed ,,can be username ,id etc
    
    with MongoDBSaver.from_conn_string(DB_URI) as mongo_checkpointer:
        
        graph_with_mongo = compile_with_checkpointer(mongo_checkpointer)
        query = input("-> ") 
        result = graph_with_mongo.invoke({"messages" : [{"role" : "user", "content" :query}]}, config=config)
        print(result)
    
main()







'''
NORMAL -> STATE RESETS AFTER START->Chat_node->END
def chat_node(state:State):
    
    response = llm.invoke(state['messages'])
    return {'messages' : [response]} #anotated automatically adds in existing messages, appends not rewritee

graph_builder = StateGraph(State)
graph_builder.add_node("chat_node", chat_node)
graph_builder.add_edge(START, "chat_node")
graph_builder.add_edge("chat_node", END)
graph = graph_builder.compile()


def main():
    query = input("-> ")
    FRESH NEW STATE CREATED
    result = graph.invoke({"messages" : [{"role" : "user", "content" :query}]})
    STATE TERMINATED
    print(result)
    
main()
'''