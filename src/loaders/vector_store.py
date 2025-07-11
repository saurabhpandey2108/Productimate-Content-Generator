from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

def create_vector_store(documents, index_path="faiss_index"):
  """Create and save a FAISS vector store from documents."""
  embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
  db = FAISS.from_documents(documents, embeddings)
  db.save_local(index_path)
  return db