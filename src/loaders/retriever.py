from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

class FeedbackRetriever:
    def __init__(self, index_path: str = None):
        
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Resolve index path robustly
        if index_path:
            self.index_path = index_path
        else:
            # Check common locations
            candidate1 = os.path.join(self.project_root, "faiss_index")
            candidate2 = os.path.join(self.project_root, "src", "faiss_index")
            if os.path.exists(os.path.join(candidate1, "index.faiss")):
                self.index_path = candidate1
            else:
                self.index_path = candidate2
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        
        # Check if index exists, create if it doesn't (optional fallback)
        index_file = os.path.join(self.index_path, "index.faiss")
        if not os.path.exists(index_file):
            print(f"Warning: FAISS index not found at {index_file}. Please initialize it using setup_rag_pipeline.")
        
        self.vector_store = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)
        self.output_store = {}  # In-memory store; replace with database for production

    def store_output(self, content: str, metadata: dict):
        self.vector_store.add_texts([content], metadatas=[metadata], ids=[metadata["output_id"]])
        self.output_store[metadata["output_id"]] = {"content": content, "metadata": metadata}
        self.vector_store.save_local(self.index_path)

    def get_output(self, output_id: str) -> dict:
        return self.output_store.get(output_id)

    def update_output(self, output_id: str, updated_data: dict):
        self.output_store[output_id] = updated_data
        self.vector_store.delete([output_id])
        self.vector_store.add_texts(
            [updated_data["content"]],
            metadatas=[updated_data["metadata"]],
            ids=[output_id]
        )
        self.vector_store.save_local(self.index_path)

    def retrieve_relevant_outputs(self, query: str, platform: str, k: int = 3):
        results = self.vector_store.similarity_search(
            query,
            k=k,
            filter=lambda x: x.get("platform") == platform and x.get("feedback", {}).get("label") == "high_engagement"
        )
        return [doc.metadata for doc in results]

    def as_retriever(self, **kwargs):
        return self.vector_store.as_retriever(**kwargs)