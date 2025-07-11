from langchain.tools import tool
from src.langchain_utils import save_output
from src.rag_pipeline import get_rag_chain
from src.langchain_utils import validate_content

@tool
def content_strategy(platforms: str, content_goals: str, context: str = "") -> str:
    """Generate a content strategy for specified platforms and goals with RAG context."""
    rag_chain = get_rag_chain(use_case="strategy")
    if not context:
        context = rag_chain.run({"context": f"SEO strategy for {platforms}", "platforms": platforms})
    strategy = f"Strategy for {platforms}: Weekly plan to achieve {content_goals} with SEO focus. {context}"
    if not validate_content(strategy, "strategy"):
        raise ValueError("Generated strategy does not meet SEO criteria")
    save_output(strategy, "strategies", f"strategy_{content_goals}_{timestamp()}")
    return strategy