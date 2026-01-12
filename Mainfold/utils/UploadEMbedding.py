#this func will upload embedding to vector database
import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from Mainfold.utils.Embedd import creating_model
load_dotenv()
index_name=os.getenv("INDEX_NAME")

def upload_embedding(splitted_doc):
    model=creating_model()
    vectorstore = PineconeVectorStore.from_documents(
        documents=splitted_doc,
        embedding=model,
        index_name=index_name
    )
    return None
def retrieval_func(user_id,book_id):
    model=creating_model()
    vectorstore = PineconeVectorStore(
        embedding=model,
        index_name=index_name
    )
    return vectorstore.as_retriever(search_type="similarity", search_kwargs={
            "k":3,
            "filter":{
                "user_id":user_id,
                "book_id":book_id
            }
        })