from openai import OpenAI
from dotenv import load_dotenv
import os 
from datetime import datetime
import json

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

#NNow suppose we want llm to get current weather of a particular city. One option is to give in system prompt.
'''SYSTEM_PROMPT = f"""
YOu are a helpful AI assistaant.
Todays date and time is {datetime.now()}
Current weather of Delhi is 27 degrees celcius.
"""
'''
# but this is not dynamic , need to input every city 
#Second option is to enable to call a fucntion which reurns weather of city 

def get_weather(city : str):
    #api call to get weather 
    return "32 degrees celcius"

#MANUAL WAY 
SYSTEM_PROMPT = '''
You are helpful AI assitant who is specialized in resolving user query.
You work on start, plan, action, observe mode.
For the given user query and available tools , plan the step by step execution, based on planning, select the relevant tool from the available tool and based on the tool selection you perform an action to call the tool.
Wait for the observation and based on observation from the tool call , resolve the query.

Rules:
-Follow strict output JSON format.
-Always perform one step  at a time and wait for next input.
-Carefully analyse the user query.

Output JSON format:
{{
    "step" : "string",
    "content" : "string",
    "function" : "the name of the function  only and only if step is action",
    "input" : "the input parameter of the function only and only if step is action"
}}
Available tools:
-"get_weather" : takes a city name as an input and retuns the current weather of the city.

Example:
User query: what is the weather of new york?
User Query: What is the weather of new york?
Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}
Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
Output: {{ "step": "observe", "output": "12 Degree Cel" }}
Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}
'''

response = client.chat.completions.create(
    model='gemini-1.5-flash-8b',
    response_format={'type' : 'json_object'},
    messages=[
        {'role' : 'system', 'content' : SYSTEM_PROMPT},
        {'role' : 'user', 'content' : 'what is the current weather of delhi?'},
        {'role': 'assistant', 'content' : json.dumps({"step": "plan", "content": "The user is interested in the current weather of Delhi."})},
        {'role': 'assistant', 'content' : json.dumps({"step": "plan", "content": "From the available tools, I should call get_weather."})},
        {'role': 'assistant', 'content' : json.dumps({"step": "action", "function": "get_weather", "input": "Delhi"})},
        {'role': 'user', 'content' : json.dumps({ "step": "observe", "output": "-12 Degree Cel" })},
        
        
    ]
)

print(response.choices[0].message.content)
