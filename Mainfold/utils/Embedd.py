#this code block creates embeddings for the splitted documents
from langchain_community.embeddings import HuggingFaceEmbeddings

def creating_model(model_name="sentence-transformers/all-MiniLM-L6-v2"):
    model=HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs={"device": "cpu"},      # or "cuda" if GPU available
    encode_kwargs={"normalize_embeddings": True}
)
    return model
def create_embeddings(documents):
    model=creating_model()
    embeddings = model.embed_documents(documents)
    return embeddings