from openai import OpenAI
from dotenv import load_dotenv
import os 
from datetime import datetime
import json
import requests
import subprocess

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
) 


def get_weather(city : str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    
    return "Something went wrong"

# def run_command(cmd : str):
#     return os.system(f"powershell -command '{cmd}'")


def run_command(cmd: str):
    result = os.system(cmd)
    return result


available_tools = {
    "get_weather" : get_weather,
    "run_command" : run_command
}


# Automated
SYSTEM_PROMPT = '''
You are helpful AI assitant who is specialized in resolving user query.
You work on start, plan, action, observe mode.
For the given user query and available tools , plan the step by step execution, based on planning, select the relevant tool from the available tool and based on the tool selection you perform an action to call the tool.
Wait for the observation and based on observation from the tool call , resolve the query.

Rules:
-Follow strict output JSON format.
-Always perform one step  at a time and wait for next input.
-Carefully analyse the user query.
-Do not include markdown code blocks, explanations, or text outside of JSON.
-Every reply must be a single JSON object with this schema:
    {
    "step": "plan" | "action" | "observe" | "output",
    "function": string (only if step == "action"),
    "input": any (only if step == "action"),
    "content": string (for plan/output steps)
    }

Output JSON format:
{{
    "step" : "string",
    "content" : "string",
    "function" : "the name of the function  only and only if step is action",
    "input" : "the input parameter of the function only and only if step is action"
}}
Available tools:
-"get_weather" : takes a city name as an input and retuns the current weather of the city.
-"run_command": takes a shell command as a string, executes it, and returns the result.
    - You can use it for creating files, writing multi-line HTML, CSS, JS code,
      making directories, or opening files. Example:
        * mkdir todo
        * echo "<!DOCTYPE html>..." > todo/index.html
        * echo "body { background: #eee; }" > todo/style.css
        * echo "console.log('todo');" > todo/script.js
Example:
User query: what is the weather of new york?
User Query: What is the weather of new york?
Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}
Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
Output: {{ "step": "observe", "output": "12 Degree Cel" }}
Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}
'''


messages = [
    {'role' : 'system', 'content' : SYSTEM_PROMPT}
]


while True:
    query = input("-> ")
    messages.append({'role' : 'user', 'content' : query})

    while True:
        response = client.chat.completions.create(
            model='gemini-2.5-flash',
            response_format={'type' : 'json_object'},
            messages=messages
        )

        messages.append({'role' : 'assistant', 'content' : response.choices[0].message.content})
        parsed_reponse = json.loads(response.choices[0].message.content)
        
        if (parsed_reponse.get('step') == 'plan'):
            print(f"🧠 : {parsed_reponse.get('content')}")
            continue
        
        if(parsed_reponse.get('step') == 'action'):
            function_name = parsed_reponse.get("function")
            function_input = parsed_reponse.get("input")
            
            print(f"⚒️ : Calling tool {function_name}  with input {function_input}")
            
            if available_tools.get(function_name) != False:
                output = available_tools[function_name](function_input)
                messages.append({'role' : 'user', 'content' : json.dumps({'step' : 'observe', 'output' : output})})
                continue
            
        if  parsed_reponse.get("step") == "output":
                print(f"🤖: {parsed_reponse.get('content')}")
                break
