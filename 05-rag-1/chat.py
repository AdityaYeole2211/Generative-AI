from dotenv import load_dotenv
from openai import OpenAI
import os
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

embedding_model = GoogleGenerativeAIEmbeddings(
    model='gemini-embedding-001'
)
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url='http://localhost:6333',
    collection_name='learning_vectors',
    embedding=embedding_model
)

#take user qeury
query = input("->")

search_results = vector_db.similarity_search(
    query=query
)

# print("search results : ", search_results)

context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

SYSTEM_PROMPT = f'''
You are a helpful AI assistant who answers user query based on given context retrived from a PDF file along with page_contents and page_number.
You should only answer based on following context and navigate user to appropriate page number for further information.

Context :
{context}
'''

chat_completion = client.chat.completions.create(
    model = 'gemini-2.5-flash',
    messages = [
        {'role' : 'system', 'content' : SYSTEM_PROMPT},
        {'role' : 'user', 'content' : query}
    ]
)

print(chat_completion.choices[0].message.content)