import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.rag_pipeline import setup_rag_pipeline

if __name__ == "__main__":
    print("Rebuilding FAISS index...")
    setup_rag_pipeline(data_path="data", index_path="faiss_index")
    print("FAISS index rebuilt successfully at faiss_index.")