from openai import OpenAI
from pydantic import BaseModel
from langgraph.graph import START, END, StateGraph
from typing_extensions import TypedDict
from typing import Literal
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

class State(TypedDict):
    user_query : str
    llm_result : str | None
    is_coding_question : str| None
    accuracy_percentage : str | None

class classifyMessageResponse(BaseModel):
    is_coding_question : bool

class accuracyResponse(BaseModel):
    accuracy_percentage : str


#node -> classify query
def classify_query(state: State):
    print("🧠 Classifying Query..... \n")
    query = state['user_query']
    SYSTEM_PROMPT = '''
    You are a helpful AI assitant capable of classifying query type. Your  job is to understand user query properly and classify whether query is related to coding question or not.
    You are expected  to return response strictly in valid JSON object.
    '''
    response = client.beta.chat.completions.parse(
        model="gemini-2.0-flash-lite", #less capable model
        messages=[
            {'role' : 'system' , 'content' : SYSTEM_PROMPT},
            {'role' : 'user', 'content' : query}
        ],
        response_format=classifyMessageResponse
    )

    is_coding_ques = response.choices[0].message.parsed.is_coding_question
    state['is_coding_question'] = is_coding_ques
    return state

def route_query(state : State) -> Literal['general_query_resolver', 'coding_query_resolver']:
    print("🧠 Routing Query..... \n")
    #literal -> routing fn need to know firsthand , where all the routing can happen
    if state['is_coding_question']:
        print("⚠️ Coding related ->  coding_query_resolver ✅\n")
        return "coding_query_resolver"
    
    print("⚠️ General query ->  general_query_resolver ✅\n")
    return "general_query_resolver"
    
def general_query_resolver(state:State):
    #general wury -> less capable model 
    print("⚠️ General query ->  resolving....\n")
    response = client.chat.completions.create(
        model='gemini-2.5-flash-lite',
        messages=[
            {'role' : 'user', 'content' : state['user_query']}
        ]
    )

    state['llm_result'] = response.choices[0].message.content
    return state



def coding_query_resolver(state : State):
    print("⚠️ Coding query ->  resolving....\n")
    query = state['user_query']
    SYSTEM_PROMPT = '''
    You are a helpful AI  Coding agent. You understand the given coding related user query and answer appropriately.
    '''
    response = client.chat.completions.create(
        model = 'gemini-3-pro-preview',
        messages=[
            {'role' : 'system', 'content':SYSTEM_PROMPT},
            {'role' : 'user', 'content' : query}
        ]
    )

    state['llm_result'] = response.choices[0].message.content
    return state


def coding_evaluation(state : State):
    print("🧠 Evaluating Accuracy..... \n")
    query = state['user_query']
    code = state['llm_result']
    SYSTEM_PROMPT = f'''
    You are a helpful AI assistant who specialize in calculating an accuracy percentage of a code according to question. You will recieve a user query and a code response. Your task is to return the accuracy percentage of the code according to user query.

    User query : 
    {query}
    Code : 
    {code}
    '''
    response = client.beta.chat.completions.parse(
        model="gemini-2.5-pro", 
        messages=[
            {'role' : 'system' , 'content' : SYSTEM_PROMPT},
            {'role' : 'user', 'content' : query}
        ],
        response_format=accuracyResponse
    )

    accuracy = response.choices[0].message.parsed.accuracy_percentage
    state['accuracy_percentage'] = accuracy
    return state
    

graph_builder = StateGraph(State)
graph_builder.add_node("classify_query", classify_query)
graph_builder.add_node("route_query", route_query)
graph_builder.add_node("general_query_resolver", general_query_resolver)
graph_builder.add_node("coding_query_resolver", coding_query_resolver)
graph_builder.add_node("coding_evaluation", coding_evaluation)

graph_builder.add_edge(START, "classify_query")
graph_builder.add_conditional_edges("classify_query", route_query)
graph_builder.add_edge("general_query_resolver", END)
graph_builder.add_edge("coding_query_resolver", "coding_evaluation")
graph_builder.add_edge("coding_evaluation", END)


graph = graph_builder.compile()

def main():
    query = input("-> ")

    _state = State(
        user_query=query,
        llm_result=None,
        accuracy_percentage=None,
        is_coding_question=False
    )

    response = graph.invoke(_state)
    print("\n\n", response)

main()
    

