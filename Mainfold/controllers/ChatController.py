#this the part where we initialize the chat controller section
import os
from dotenv import load_dotenv
from flask import jsonify
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from Mainfold.utils.PromptTemp import system_prompt
from Mainfold.utils.Embedd import creating_model
from Mainfold.utils.other_func import *

model=creating_model()
LLM=initiate_LLM()
retrieval=retrieval(model=model)
prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{user_input}")
    ])
 # Build RAG chain
rag_chain = (
        {
            "context": retrieval | (lambda docs: "\n\n".join(d.page_content for d in docs)),
            "user_input": RunnablePassthrough(),
        }
        | prompt
        | LLM
    )
def intiate_chat(data):
 user_msg = data.get("message")
 if not user_msg:
        return jsonify({"reply": "No message received!"})

    # Invoke RAG chain
 response = rag_chain.invoke(user_msg)
 return jsonify({"reply": response.content})
 