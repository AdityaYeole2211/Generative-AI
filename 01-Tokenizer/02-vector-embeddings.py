from openai import OpenAI
from dotenv import load_dotenv
import os 


load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')



client = OpenAI(
    api_key= GEMINI_API_KEY ,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


text = "dog chases cat"

response = client.embeddings.create(
    model='gemini-embedding-001',
    input=text
)

# print("Vector Embeddings :  \n", response)

print("Len: ", len(response.data[0].embedding)) #3072 -> address in 3027 dimension is output of vector embedding 