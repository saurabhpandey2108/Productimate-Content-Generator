import logging
from langchain_core.tools import StructuredTool
from src.loaders.retriever import FeedbackRetriever
from src.langchain_utils import validate_content
from src.rag_pipeline import initialize_chains  

logger = logging.getLogger(__name__)

class SocialMediaAgent:
    def __init__(self, platform: str):
        self.platform = platform
        self.chains = initialize_chains()
        self.retriever = FeedbackRetriever()

    async def generate(self, use_case: str, **kwargs):
        platform = kwargs.pop("platform", self.platform)
        logger.debug(f"Entering generate: platform={platform}, use_case={use_case}, kwargs={kwargs}")
        rag_chain = self.chains.get(platform)
        if not rag_chain:
            raise ValueError(f"No chain found for platform: {platform}")
        
        # Retrieve high-performing outputs
        query = kwargs.get("content_topic", kwargs.get("content_goals", kwargs.get("brand_summary", "")))
        feedback_context = self.retriever.retrieve_relevant_outputs(query, platform)
        feedback_text = "\n".join([f"Example: {doc['content']}" for doc in feedback_context])
        
        input_data = {
            "content_topic": kwargs.get("content_topic", ""),
            "tone": kwargs.get("tone", "neutral"),
            "professional_insight": kwargs.get("professional_insight", ""),
            "persona": kwargs.get("persona", ""),
            "audience": kwargs.get("audience", ""),
            "content_goals": kwargs.get("content_goals", ""),
            "brand_summary": kwargs.get("brand_summary", ""),
            "topic_list": kwargs.get("topic_list", ""),
            "context": kwargs.get("context", ""),
            "feedback_context": feedback_text
        }
        
        try:
            response = await rag_chain.ainvoke(input_data)
            return response["result"]
        except Exception as e:
            logger.error(f"Error in RAG chain invocation: {str(e)}")
            raise

    def validate_output(self, output: str, use_case: str, platform: str) -> tuple[bool, str]:
        is_valid, message = validate_content(output, use_case)
        return is_valid, message

def initialize_agent():
    from src.rag_pipeline import initialize_chains
    chains = initialize_chains()
    return SocialMediaAgent("all")