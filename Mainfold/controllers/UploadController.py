#this section of my code will handle both uploaded request file processing and also uploading the embedding to vector store
import os
from Mainfold.utils import Embedd,UploadEMbedding,SplitDocument,exception
from flask import jsonify,request
import tempfile

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
            # text_content=SplitDocument.split_docx(file,user_id,book_id,book_title)
        return jsonify({"status":"success","message":"File processed successfully",
                             "test_content": text_content[0].page_content,
                              "metadata": text_content[0].metadata
                            }),200
        
    except Exception as e:
       return jsonify({"status":"error","message":str(e)}),500