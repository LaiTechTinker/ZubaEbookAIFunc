#this section of my code will handle both uploaded request file processing and also uploading the embedding to vector store
import os
from datetime import datetime
import uuid
from dotenv import load_dotenv
from Mainfold.utils import Embedd,UploadEMbedding,SplitDocument,exception
from flask import jsonify,request
import tempfile
from Mainfold.utils.Mongo_connect import MongoDBOp
from Mainfold.utils.SplitDocument import serialize,deserialize
from Mainfold.utils.UploadEMbedding import upload_embedding
DB_NAME=os.getenv("DATABASE_NAME")
MONGO_URL=os.getenv("MONGO_URL")
COLLECTION_NAME=os.getenv("COLLECTION_NAME")

Mongo_class=MongoDBOp(MONGO_URL=MONGO_URL,DB_NAME=DB_NAME)

def process_upload(file,user_id,book_id,book_title):
    text_content=[]
    try:
        # file=request.files.get(file)
        if not file:
            return jsonify({"status":"error","message":"No file provided"}),400
        filename=file.filename
        ext=os.path.splitext(filename)[1].lower()
        if ext not in [".pdf",".docx"]:
            return jsonify({"status":"error","message":"Unsupported file type"}),400
        if ext==".pdf":
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
                file.save(temp_pdf.name)
                temp_path = temp_pdf.name
            text_content=SplitDocument.split_pdf(temp_path,user_id,book_id,book_title)
            # text_content=SplitDocument.split_pdf(file,user_id,book_id,book_title)
        elif ext==".docx":
            with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temp_docx:
              file.save(temp_docx.name)
              temp_path = temp_docx.name
            text_content=SplitDocument.split_docx(temp_path,user_id,book_id,book_title)
        split_id=str(uuid.uuid4())
        #this serialize the text_content
        serilize_docs=serialize(text_content)
        #let's define obj to push to mongodb
        obj={
            "split_id":split_id,
            "user_id":user_id,
            "book_id":book_id,
            "book_title":book_title,
            "chunk":serilize_docs,
            "status":"pending",
            "created_At":datetime.utcnow()
        }
        #let push to mongo_db
        Mongo_class.insertOne(COLLECTION_NAME=COLLECTION_NAME,obj=obj)
            # text_content=SplitDocument.split_docx(file,user_id,book_id,book_title)
        return jsonify({"status":"success","message":"File processed successfully",
                        "split_id":split_id}),200
        
    except Exception as e:
       return jsonify({"status":"error","message":str(e)}),500
def upload_to_pine(data):
    try:
        data=data
        split_id=data.get("split_id")
        record=Mongo_class.findOne(COLLECTION_NAME=COLLECTION_NAME,id={"split_id":split_id})
        if not record:
            return jsonify({"status":"error","message":"split not found"}),404
        #this get's our deserialize document
        docs=deserialize(record["chunk"])
        #this upload our document
        upload_embedding(docs)
        #after uploading i want to delete the record to free up space in my database
        Mongo_class.deleteOne(COLLECTION_NAME=COLLECTION_NAME,id={"split_id":split_id})

        return jsonify({
            "status":"success","message":"File uploaded to pine successfully",
        }),200

    except Exception as e:
        return jsonify({"status":"error","message":str(e)}),500

