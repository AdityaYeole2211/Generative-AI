from fastapi import FastAPI, Query
from .queue.connection import queue
from .queue.worker import process_query
from dotenv import load_dotenv

load_dotenv()


# make an app
app = FastAPI()

# default get
@app.get('/')
def chat():
    return {"status" : "Server is up and running"}

@app.post('/chat')
def chat(
    query : str = Query(..., description="Chat message")
):
    #query ko queue mein dal do 
    job = queue.enqueue(process_query, query)  # internally calling process_query(query) and returnnig a job object
    #user ko inform karo ki job recieved
    return {"status" : "queued", "job_id" : job.id}
