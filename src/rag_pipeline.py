import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, JSONLoader
from langchain_core.runnables import RunnableLambda
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

def setup_rag_pipeline(data_path: str = None, index_path: str = None):
    """
    Set up the RAG pipeline by creating or loading a vector store with data from specific files.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = data_path or os.path.join(project_root, "data")
    index_path = index_path or os.path.join(project_root, "src", "faiss_index")
    os.makedirs(index_path, exist_ok=True)
    
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    
    index_file = os.path.join(index_path, "index.faiss")
    if not os.path.exists(index_file):
        logger.info(f"FAISS index not found at {index_file}. Creating new index.")
        brochure_path = os.path.join(data_path, "Productimate Brochure.pdf")
        json_path = os.path.join(data_path, "social_media_links.json")  # Updated to match structure
    
        all_documents = []
        if os.path.exists(brochure_path):
            loader = PyPDFLoader(brochure_path)
            documents = loader.load()
            all_documents.extend(documents)
        else:
            raise ValueError(f"Company brochure not found at {brochure_path}")
        
        if os.path.exists(json_path):
            loader = JSONLoader(file_path=json_path, jq_schema=".[]")
            documents = loader.load()
            all_documents.extend(documents)
        
        # Attempt to load company website content
        company_url = os.getenv("COMPANY_URL", "https://productimate.io/")
        try:
            from src.loaders.web_loader import load_website_content
            web_docs = load_website_content(company_url)
            all_documents.extend(web_docs)
        except Exception as e:
            logger.warning(f"Failed to fetch website content from {company_url}: {e}")

        if not all_documents:
            raise ValueError("No documents loaded from data folder or website")
        
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = splitter.split_documents(all_documents)
        db = FAISS.from_documents(docs, embeddings)
        db.save_local(index_path)
        logger.info(f"FAISS index created and saved at {index_file}")
    
    vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    logger.info(f"FAISS index loaded from {index_file}")
    return vector_store

def get_rag_chain(index_path: str = None, use_case: str = "content", platform: str = "linkedin", **kwargs):
    """
    Create an async-compatible RAG chain tailored to the use case and platform with dynamic input variables.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_path = index_path or os.path.join(project_root, "src", "faiss_index")
    
    vector_store = setup_rag_pipeline(index_path=index_path)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(temperature=0.3, model="gpt-4o-mini", openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    # Define platform-specific prompts with feedback_context
    if platform == "linkedin":
        prompt = PromptTemplate(
            template="""Use the following context to generate a LinkedIn post. The response should be engaging, professional, and optimized for SEO and conversions.
            
            Context: {context}
            Content Topic: {content_topic}
            Tone: {tone}
            Professional Insight: {professional_insight}
Length: {length}
            High-performing examples: {feedback_context}
            
            Generate a LinkedIn post based on the above details. IMPORTANT: Include the exact word 'SEO' (uppercase) at least once to ensure SEO keyword presence.""",
            input_variables=["context", "content_topic", "tone", "professional_insight", "length", "feedback_context"]
        )
    elif platform == "instagram":
        prompt = PromptTemplate(
            template="""Use the following context to generate an Instagram caption. The response should be engaging, trendy, and optimized for SEO and conversions.
            
            Context: {context}
            Content Topic: {content_topic}
            Tone: {tone}
            Persona: {persona}
Length: {length}
            High-performing examples: {feedback_context}
            
            Generate an Instagram caption based on the above details. IMPORTANT: Include the exact word 'SEO' (uppercase) at least once to ensure SEO keyword presence.""",
            input_variables=["context", "content_topic", "tone", "persona", "length", "feedback_context"]
        )
    elif platform == "facebook":
        prompt = PromptTemplate(
            template="""Use the following context to generate a Facebook post. The response should be engaging, friendly, and optimized for SEO and conversions.
            
            Context: {context}
            Content Topic: {content_topic}
            Tone: {tone}
            Audience: {audience}
Length: {length}
            High-performing examples: {feedback_context}
            
            Generate a Facebook post based on the above details. IMPORTANT: Include the exact word 'SEO' (uppercase) at least once to ensure SEO keyword presence.""",
            input_variables=["context", "content_topic", "tone", "audience", "length", "feedback_context"]
        )
    elif platform == "all" and use_case == "strategy":
        prompt = PromptTemplate(
            template="""Develop a comprehensive **content marketing strategy** for the next 3 months targeting the following platforms: {platforms}.

                Format your answer in **Markdown** using the sections below. Use bullet lists or tables where appropriate.

                1. **Objectives** – what we aim to achieve (aligned with {content_goals})
                2. **Target Audience** – key personas & pain-points
                3. **Key Messages & Content Pillars** – 3-5 pillars with examples
                4. **Channel-Specific Approach** – for each platform outline best formats, tone, CTAs
                5. **Posting Cadence & Formats** – weekly frequency, content types
                6. **SEO & Conversion Tactics** – keyword strategy, internal linking, CTAs
                7. **Measurement & KPIs** – how success will be tracked
                8. **Timeline / Next Steps** – high-level roadmap

                Leverage the following information when crafting the strategy:
                High-performing examples: {feedback_context}
                Context: {context}
                """,
            input_variables=["platforms", "content_goals", "context", "feedback_context"]
        )
    elif platform == "all" and use_case == "calendar":
        prompt = PromptTemplate(
            template="""Based on the brand_summary and topics below, create a 7-day content plan focusing on SEO, conversions, and our SEO-friendly website product.
            Return: Day | Platform | Content Type | Topic | Caption Summary | CTA
            Use these high-performing examples for inspiration: {feedback_context}
            Brand Summary: {brand_summary}
            Topics: {topic_list}
            Context: {context}
            """,
            input_variables=["brand_summary", "topic_list", "context", "feedback_context"]
        )
    else:
        raise ValueError(f"Unsupported platform or use case: {platform}, {use_case}")
    
    rag_chain = LLMChain(llm=llm, prompt=prompt)
    
    async def preprocess_input(input_dict):
        query = ""
        if platform == "linkedin":
            query = f"Provide context for a {use_case} post about {input_dict.get('content_topic', 'general topic')} with a {input_dict.get('tone', 'neutral')} tone with insight: {input_dict.get('professional_insight', '')} for LinkedIn audience."
        elif platform == "instagram":
            query = f"Provide context for a {use_case} post about {input_dict.get('content_topic', 'general topic')} with a {input_dict.get('tone', 'neutral')} tone for {input_dict.get('persona', 'general persona')} on Instagram."
        elif platform == "facebook":
            query = f"Provide context for a {use_case} post about {input_dict.get('content_topic', 'general topic')} with a {input_dict.get('tone', 'neutral')} tone for {input_dict.get('audience', 'general audience')} on Facebook."
        elif platform == "all" and use_case in ["strategy", "calendar"]:
            query = f"Provide context for a {use_case} about {input_dict.get('content_goals', input_dict.get('brand_summary', 'general topic'))}."
        
        docs = await retriever.ainvoke(query)
        return {
            "context": "\n".join(doc.page_content for doc in docs),
            "content_topic": input_dict.get("content_topic", ""),
            "tone": input_dict.get("tone", "neutral"),
            "professional_insight": input_dict.get("professional_insight", ""),
            "persona": input_dict.get("persona", ""),
            "audience": input_dict.get("audience", ""),
            "content_goals": input_dict.get("content_goals", ""),
            "brand_summary": input_dict.get("brand_summary", ""),
            "topic_list": input_dict.get("topic_list", ""),
            "length": input_dict.get("length", "medium"),
            "feedback_context": input_dict.get("feedback_context", ""),
            "query": query
        }
    
    class _RAGChainWrapper:
        """Thin proxy that preprocesses input before delegating to the underlying chain."""
        def __init__(self, chain, preprocess):
            self._chain = chain
            self._preprocess = preprocess
        async def ainvoke(self, input_dict):
            processed = await self._preprocess(input_dict)
            res = await self._chain.ainvoke(processed)
            if isinstance(res, dict):
                if "result" in res:
                    return res
                # LangChain LLMChain returns {'text': '...'}
                if "text" in res:
                    return {"result": res["text"]}
                # Fallback: wrap entire dict as string
                return {"result": str(res)}
            return {"result": res}
        def __getattr__(self, name):
            # Delegate everything else to the wrapped chain
            return getattr(self._chain, name)
    
    return _RAGChainWrapper(rag_chain, preprocess_input)

def initialize_chains():
    """
    Initialize chain instances with RAG integration for different platforms.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_path = os.path.join(project_root, "src", "faiss_index")
    
    setup_rag_pipeline(index_path=index_path)
    
    chains = {}
    for platform in ["linkedin", "instagram", "facebook"]:
        chains[platform] = get_rag_chain(index_path=index_path, use_case="content", platform=platform)
    chains["all"] = get_rag_chain(index_path=index_path, use_case="strategy", platform="all")
    return chains