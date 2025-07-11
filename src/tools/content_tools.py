from langchain.tools import tool
from src.langchain_utils import save_output
from src.rag_pipeline import get_rag_chain
from src.langchain_utils import validate_content

@tool
async def instagram_content(content_topic: str, tone: str, persona: str, context: str = "") -> str:
    """Generate Instagram content (caption) based on topic, tone, persona, and RAG context, focusing on SEO and product."""
    rag_chain = await get_rag_chain(use_case="content", platform="instagram")
    if not context:
        response = await rag_chain.ainvoke({"query": f"SEO and website builder for {persona}", "platform": "instagram"})
        context = response.get("result", "")
    caption = f"🌟 {content_topic} in a {tone} tone for {persona}! {context} SEO boosts conversions—build with our SEO-friendly site! 💡 DM us! #SEO #Conversions #WebsiteBuilder"
    if not validate_content(caption, "content"):
        raise ValueError("Generated caption does not meet SEO criteria")
    save_output(caption, "instagram_contents", f"instagram_content_{content_topic}_{timestamp()}")
    return caption

@tool
async def facebook_content(content_topic: str, tone: str, audience: str, context: str = "") -> str:
    """Generate Facebook content (post) based on topic, tone, audience, and RAG context, focusing on SEO and product."""
    rag_chain = await get_rag_chain(use_case="content", platform="facebook")
    if not context:
        response = await rag_chain.ainvoke({"query": f"SEO and website builder for {audience}", "platform": "facebook"})
        context = response.get("result", "")
    post = f"🎉 {content_topic} update with a {tone} tone for {audience}! {context} SEO drives conversions—try our SEO-friendly website tool! 👇 Share your thoughts!"
    if not validate_content(post, "content"):
        raise ValueError("Generated post does not meet SEO criteria")
    save_output(post, "facebook_contents", f"facebook_content_{content_topic}_{timestamp()}")
    return post

@tool
async def linkedin_content(content_topic: str, tone: str, professional_insight: str, context: str = "") -> str:
    """Generate LinkedIn content (post) based on topic, tone, insight, and RAG context, focusing on SEO and product."""
    rag_chain = await get_rag_chain(use_case="content", platform="linkedin")
    if not context:
        response = await rag_chain.ainvoke({"query": f"SEO and website builder with {professional_insight}", "platform": "linkedin"})
        context = response.get("result", "")
    post = f"💼 {content_topic} insight: {professional_insight} in a {tone} tone. {context} SEO enhances conversions—use our tool for SEO-friendly sites! #LinkedIn #SEO"
    if not validate_content(post, "content"):
        raise ValueError("Generated post does not meet SEO criteria")
    save_output(post, "linkedin_contents", f"linkedin_content_{content_topic}_{timestamp()}")
    return post

def timestamp():
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d_%H%M%S")