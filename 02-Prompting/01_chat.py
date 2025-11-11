from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url= 'https://generativelanguage.googleapis.com/v1beta/openai/'
)

response = client.chat.completions.create(
    model= 'gemini-1.5-flash-8b',
    messages= [
        {'role' : 'user', 'content' : 'Hey there'}
    ]
)

print(response.choices[0].message.content)


## NOTES 
'''
1. The requests by default are stateless. no context of previous message history.
2. To give context , everytime , we have to send entire messages again . This does not mean that everytime 
we have to process all the tokens again and again . It caches the input tokens for some time. 
3. Some optmization can be keeping recent 100 (or any no.) of messages context. and then summarizing the previous all messages into one message 
'''