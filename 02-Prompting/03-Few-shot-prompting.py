from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url= 'https://generativelanguage.googleapis.com/v1beta/openai/'
)

# Few shot prompting: Model given few examples before asking to generate response
SYSTEM_PROMPT = '''
You are an AI expert in coding. You know python and nothing else.
You help users in solving their python doubts and nothing else.
If user ask about anything other than python doubts , you roast them.

Example : 
User : Explain how to make tea?
Assistant : Oh my love! Leave those things to ladies. Men focus on python.

Examples: 
User : How to write a function in python?
Assistant : def fn_name(x:int)-> int:
              pass

'''

response = client.chat.completions.create(
    model='gemini-1.5-flash-8b',
    messages=[
        {'role' : 'system', 'content' : SYSTEM_PROMPT},
        {'role' : 'user', 'content' : 'Hey, There'},
        {'role' : 'assistant', 'content' : 'Hey, How can I help you.'},
        {'role' : 'user', 'content' : 'How can I get admission in colleges?'},
    ]
)

print(response.choices[0].message.content)