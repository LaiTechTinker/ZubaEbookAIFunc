#this code block below will split pdf file
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
#this handles text splitting generally
def text_splitter():
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
        
    )
    return text_splitter
def split_pdf(pdf_file_path,user_id,book_id,book_title):
    loader = PyPDFLoader(pdf_file_path)
    pdf_data = loader.load()
    pdf_split=text_splitter().split_documents(pdf_data)
    for doc in pdf_split:
     doc.metadata.update({
        "user_id": user_id,
        "book_id": book_id,
        "book_title": book_title,
        "source": "pdf"
     })
    return pdf_split
def split_docx(docx_file_path,user_id,book_id,book_title):
    loader = Docx2txtLoader(docx_file_path)
    docx_data = loader.load()
    docx_split=text_splitter().split_documents(docx_data)
    for doc in docx_split:
     doc.metadata.update({
        "user_id": user_id,
        "book_id": book_id,
        "book_title": book_title,
        "source": "docx"
     })
    return docx_split