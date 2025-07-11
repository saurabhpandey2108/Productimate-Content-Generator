from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def create_vector_index(file_path: str, index_path: str, overwrite: bool = False):
    """
    Create a FAISS vector index from the given file.
    """
    embeddings = OpenAIEmbeddings()
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        documents = loader.load()
    elif file_path.endswith(".json"):
        loader = JSONLoader(file_path, jq_schema=".[]")
        documents = loader.load()
    else:
        raise ValueError(f"Unsupported file format: {file_path}")
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)
    db = FAISS.from_documents(docs, embeddings)
    
    # Check if index_path directory exists and handle the file
    index_dir = os.path.dirname(index_path) or "."
    if not os.path.exists(index_dir):
        os.makedirs(index_dir, exist_ok=True)
    if os.path.exists(index_path) and not overwrite:
        raise FileExistsError(f"Index file {index_path} already exists. Use overwrite=True to replace it.")
    db.save_local(index_path)

def load_index(index_path: str):
    """
    Load a FAISS vector index from the given path.
    """
    embeddings = OpenAIEmbeddings()
    # Allow deserialization only if the index is trusted (e.g., locally generated)
    return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)