from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_documents(documents):
  """Split documents into smaller chunks for vector storage."""
  splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
  return splitter.split_documents(documents)