from langchain_community.document_loaders import WebBaseLoader


def load_website_content(url: str):
    """Fetch a single web page and return LangChain `Document` objects.

    We use `WebBaseLoader`, which grabs the HTML, strips boilerplate, and
    returns one or more `Document`s.  If you need multi-page crawling, extend
    this function with an external crawler later.
    """
    loader = WebBaseLoader(url)
    documents = loader.load()
    for doc in documents:
        doc.metadata["source"] = url
    return documents