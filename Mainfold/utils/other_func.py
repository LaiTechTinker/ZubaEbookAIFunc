#this part of the file initiate other fuctions of our app
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_pinecone import PineconeVectorStore

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
PINE_API_KEY=os.getenv("PINECONE_API_KEY")
INDEX_NAME=os.getenv("INDEX_NAME")

def initiate_LLM():
 return init_chat_model(
        "google_genai:gemini-2.5-flash-lite",
        google_api_key=GEMINI_API_KEY,
        
    )
def stream_LLM(handler):
    return init_chat_model(
        "google_genai:gemini-2.5-flash-lite",
        google_api_key=GEMINI_API_KEY,
        temperature=0,
        streaming=True,
        callbacks=[handler]
        
    )
def retrieval(model,user_id,book_id):
 vector_store= PineconeVectorStore.from_existing_index(
        index_name=INDEX_NAME,
        embedding=model
    )
 return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3,
                       "filter":{
                "user_id":user_id,
                "book_id":book_id
            }},
        
    )
