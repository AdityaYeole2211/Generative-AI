from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url= 'https://generativelanguage.googleapis.com/v1beta/openai/'
)

#zero shot prompting 

SYSTEM_PROMPT = """
You are an AI expert in coding. You know python and nothing else.
You help users in solving their python doubts and nothing else.
If user ask about anything other than python doubts , you roast them.
"""
response = client.chat.completions.create(
    model= 'gemini-1.5-flash-8b',
    messages= [
        {'role' : 'system', 'content' : SYSTEM_PROMPT},
        {'role' : 'user', 'content' : 'Tell me about 70 percent attendance in colleges '}
        
    ]
)

print(response.choices[0].message.content)
