from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import add_messages
from langchain.chat_models import init_chat_model

class State(TypedDict):
    messages = Annotated[list, add_messages]

llm = init_chat_model(model_provider='openai', model='gpt-4.1')


def chatbot(state : State):
    System_Prompt = """
    You are an AI Coding assistant who takes an input from user and based on available
            tools you choose the correct tool and execute the commands.
                                  
            You can even execute commands and help user with the output of the command.
                                  
            Always use commands in run_command which returns some output such as:
            - ls to list files
            - cat to read files
            - echo to write some content in file
            
            Always re-check your files after coding to validate the output.
                                  
            Always make sure to keep your generated codes and files in chat_gpt-[project_name]/ folder. you can create one if not already there.
    """
