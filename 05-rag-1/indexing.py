#steps : upload a pdf, chunkit, create embeddings, upload them to qdrant db

from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
# from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

#load the file 
file_path = Path(__file__).parent / "nodejs.pdf"

loader = PyPDFLoader(file_path=file_path)
docs = loader.load()

# print(docs[5])

# chunking 
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000 , #1000 chars per chunk
    chunk_overlap = 400 # for added conttext
)

split_docs = text_splitter.split_documents(documents=docs)

# vector embeddings

embedding_model = GoogleGenerativeAIEmbeddings(
    model='gemini-embedding-001'
)

#using [embedding model] convert [split docs ]to embeddings and store in db
vector_store = QdrantVectorStore.from_documents(
    documents = split_docs,
    embedding=embedding_model,
    url = 'http://localhost:6333',
    collection_name="learning_vectors"
)

print("Idexing of documents done")










##-----------------OUTPUT-------------------###################
# print(docs[5])
'''
page_content='Version 1.0 6 
Lesson 7: Serving up Files .............................................................................................................. 94 
Lesson 8: Auto-Cropping and Image Formatting ..................................................................... 95 
Section 15: Sending Emails ................................................................................................... 96
Lesson 1: Section Intro ..................................................................................................................... 96
Lesson 2: Exploring SendGrid ....................................................................................................... 96
Lesson 3: Sending Welcome and Cancelation Emails ............................................................ 97
Lesson 4: Environment Variables ................................................................................................. 97
Lesson 5: Creating a Production MongoDB Database ........................................................... 98
Lesson 6: Heroku Deployment ..................................................................................................... 98
Section 16: Testing Node.js ................................................................................................... 99
Lesson 1: Section Intro ..................................................................................................................... 99
Lesson 2: Jest Testing Framework .............................................................................................. 99
Lesson 3: Writing Tests and Assertions .................................................................................... 100
Lesson 4: Writing Your Own Tests .............................................................................................. 101
Lesson 5: Testing Asynchronous Code ..................................................................................... 101
Lesson 6: Testing an Express Application: Part I ................................................................... 102   
Lesson 7: Testing an Express Application: Part II ................................................................... 103  
Lesson 8: Jest Setup and Teardown ......................................................................................... 104
Lesson 9: Testing with Authentication ...................................................................................... 105
Lesson 10: Advanced Assertions ................................................................................................ 106
Lesson 11: Mocking Libraries ........................................................................................................ 106
Lesson 12: Wrapping up User Tests ........................................................................................... 107
Lesson 13: Setup Task Test Suite ................................................................................................ 107
Lesson 14: Testing with Task Data .............................................................................................. 107
Lesson 15: Bonus: Extra Test Ideas ............................................................................................ 108
Section 17: Real-Time Web Applications with Socket.io ................................................. 108
Lesson 1: Section Intro ................................................................................................................... 108
Lesson 2: Creating the Chat App Project ................................................................................. 108
Lesson 3: WebSockets .................................................................................................................. 108
Lesson 4: Getting Started with Socket.io ................................................................................. 109
Lesson 5: Socket.io Events ............................................................................................................. 111
Lesson 6: Socket.io Events Challenge ....................................................................................... 112
Lesson 7: Broadcasting Events .................................................................................................... 112
Lesson 8: Sharing Your Location .................................................................................................. 113
Lesson 9: Event Acknowledgements .......................................................................................... 114' 
metadata={'producer': 'macOS Version 10.14.1 (Build 18B75) Quartz PDFContext', 'creator': 'Acrobat PDFMaker 17 for Word', 'creationdate': "D:20190227140340Z00'00'", 'author': 'Andrew Mead', 'moddate': "D:20190227140340Z00'00'", 'source': 'c:\\Users\\adity\\Desktop\\GenAI-Cohort\\05-rag-1\\nodejs.pdf', 'total_pages': 125, 'page': 5, 'page_label': '6'}
'''