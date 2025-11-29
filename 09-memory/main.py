from mem0 import Memory
from openai import OpenAI
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import os
import json

load_dotenv()
# mem0_api_key = os.getenv("MEM0_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI()
#oepnai compatible endpoint  not  supported in embedding and llm in mem0 -> langhcain 
config = {
    "version" : "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "text-embedding-3-small"
        }
    },
   "llm": {"provider": "openai", "config": {"api_key": OPENAI_API_KEY, "model": "gpt-4.1"}},
    
    "vector_store"  : {
        "provider" : "qdrant",
        "config" : {
            "host" : "vector-db",
            "port" : "6333"
        }
    },
    "graph_store" : {
        "provider" : "neo4j",
        "config" : {
            "url" : "bolt://neo4j:7687",
            "username" : "neo4j",
            "password" : "reform-william-center-vibrate-press-5829" 
        }
        
    }
}

mem_client = Memory.from_config(config)


def chat():
    while True:
        user_query = input("> ")
        relevant_memories = mem_client.search(
            query=user_query, user_id="aditya")

        memories = [
            f"ID: {mem.get("id")} Memory: {mem.get("memory")}" for mem in relevant_memories.get("results")]

        SYSTEM_PROMPT = f"""
            You are an memeory aware assistant which responds to user with context.
            You are given with past memories and facts about the user.
            
            Memory of the user:
            {json.dumps(memories)}
        """
        result = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_query}
            ]
        )

        print(f"🤖: {result.choices[0].message.content}")

        mem_client.add([
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": result.choices[0].message.content}
        ], user_id="aditya")

        

chat()