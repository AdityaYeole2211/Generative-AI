from openai import OpenAI
from dotenv import load_dotenv
import os 
from datetime import datetime

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)
'''
SYSTEM_PROMPT = """
You are a hepful AI assistant.
"""
response = client.chat.completions.create(
    model='gemini-1.5-flash-8b',
    messages=[
        {'role' : 'system', 'content' : SYSTEM_PROMPT},
        {'role' : 'user', 'content' : 'what is current date and time '}
    ]
)

print(response.choices[0].message.content)
## CURRENTLY NO INFO ABOUT RECENT EVENTS OR NO CONTEXT.
'''


#below has context hence able to answer current date and time.
SYSTEM_PROMPT = f"""
YOu are a helpful AI assistaant.
Todays date and time is {datetime.now()}
"""

response = client.chat.completions.create(
    model='gemini-1.5-flash-8b',
    messages=[
        {'role' : 'system', 'content' : SYSTEM_PROMPT},
        {'role' : 'user', 'content' : 'what is current date and time '}
    ]
)

print(response.choices[0].message.content)
