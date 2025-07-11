from langchain.tools import tool
from src.langchain_utils import save_output
from src.rag_pipeline import get_rag_chain
from src.langchain_utils import validate_content

@tool
def generate_calendar(brand_summary: str, topic_list: str, context: str = "") -> str:
    """Generate a 7-day content calendar based on brand summary and topics with RAG context."""
    rag_chain = get_rag_chain(use_case="calendar")
    if not context:
        context = rag_chain.run({"context": f"SEO calendar for {brand_summary}", "topics": topic_list})
    calendar = f"Calendar for {brand_summary}: Day 1-7 covering {topic_list} with SEO focus. {context}"
    if not validate_content(calendar, "calendar"):
        raise ValueError("Generated calendar does not meet SEO criteria")
    save_output(calendar, "calendars", f"calendar_{brand_summary}_{timestamp()}")
    return calendar