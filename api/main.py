import os
from fastapi import HTTPException, Query, FastAPI
from pydantic import BaseModel
import logging
from .models import InstagramPostRequest, FacebookPostRequest, LinkedInPostRequest, StrategyRequest, CalendarRequest, RegenerateRequest
from src.chains.linkedin_chain import LinkedInContentChain
from src.chains.instagram_chain import InstagramContentChain
from src.chains.facebook_chain import FacebookContentChain
from src.loaders.retriever import FeedbackRetriever
from src.tools.content_tools import instagram_content, facebook_content, linkedin_content
from src.tools.strategy_tools import content_strategy
from src.tools.calendar_tools import generate_calendar
from src.rag_pipeline import setup_rag_pipeline
import uuid
from datetime import datetime
from src.langchain_utils import validate_content


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title="Content Generation API", description="API for SEO-focused social media content, strategies, and calendars")

# Project root & index path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Adjusted for api/
index_path = os.path.join(project_root, "src", "faiss_index")

# We'll lazily build the FAISS index and FeedbackRetriever during startup to
# avoid blocking import-time execution which can cause lifespan cancellations.
retriever = None  # type: FeedbackRetriever | None

@app.on_event("startup")
async def _startup() -> None:
    """Build/load FAISS index and retriever once the event loop is running."""
    global retriever
    # Build / load the vector store (runs quickly if it already exists)
    setup_rag_pipeline(index_path=index_path)
    retriever = FeedbackRetriever(index_path=index_path)
    logger.info("RAG pipeline & FeedbackRetriever initialised during startup.")

def prepare_generate_params(request_data, additional_data):
    """Prepare a complete parameter set with required fields."""
    base_params = {
        "tool_names": additional_data["tool_names"],
        "tools": additional_data["tools"],
        "agent_scratchpad": additional_data["agent_scratchpad"]
    }
    return {**base_params, **request_data}

# Feedback model
class FeedbackRequest(BaseModel):
    output_id: str
    rating: int = None  # 1-5 scale
    comment: str = None
    engagement_metrics: dict = None  

@app.post("/rebuild_index/")
async def rebuild_index(overwrite: bool = Query(False, description="Set to True to overwrite existing index")):
    try:
        from src.loaders.indexer import create_vector_index
        # Resolve brochure PDF in either <root>/data or <root>/Content/data
        brochure_candidates = [
            os.path.join(project_root, "data", "Productimate Brochure.pdf"),
            os.path.join(project_root, "Content", "data", "Productimate Brochure.pdf")
        ]
        brochure_path = next((p for p in brochure_candidates if os.path.exists(p)), None)
        if not brochure_path:
            raise FileNotFoundError("Productimate Brochure.pdf not found in data folders")

        create_vector_index(
            brochure_path,
            os.path.join(project_root, "src", "faiss_index"),
            overwrite=overwrite
        )
        return {"message": "FAISS index rebuilt successfully"}
    except Exception as e:
        logger.exception("Error rebuilding index")
        raise HTTPException(status_code=500, detail=f"Error rebuilding index: {str(e)}")

@app.post("/generate_instagram_content/")
async def generate_instagram_content(request: InstagramPostRequest):
    try:
        chain = InstagramContentChain()
        caption = await chain.generate(mode="content", **request.dict())
        print(f"Validating: {caption}, use_case: content, platform: instagram")
        is_valid, message = validate_content(caption, "content")
        
        # Store output in FAISS
        output_id = str(uuid.uuid4())
        metadata = {
            "output_id": output_id,
            "platform": "instagram",
            "length": request.length,
            "content_topic": request.content_topic,
            "tone": request.tone,
            "persona": request.persona,
            "timestamp": datetime.utcnow().isoformat(),
            "seo_score": float(validate_content(caption, "content")[0])
        }
        retriever.store_output(caption, metadata)
        
        return {"output_id": output_id, "instagram_caption": caption, "validation_passed": is_valid, "validation_message": message}
    except Exception as e:
        logger.exception("Error generating Instagram content")
        raise HTTPException(status_code=500, detail=f"Error generating Instagram content: {str(e)}")

@app.post("/generate_facebook_content/")
async def generate_facebook_content(request: FacebookPostRequest):
    try:
        chain = FacebookContentChain()
        post = await chain.generate(mode="content", **request.dict())
        print(f"Validating: {post}, use_case: content, platform: facebook")
        is_valid, message = validate_content(post, "content")

        
        # Store output in FAISS
        output_id = str(uuid.uuid4())
        metadata = {
            "output_id": output_id,
            "platform": "facebook",
            "length": request.length,
            "content_topic": request.content_topic,
            "tone": request.tone,
            "audience": request.audience,
            "timestamp": datetime.utcnow().isoformat(),
            "seo_score": float(validate_content(post, "content")[0])
        }
        retriever.store_output(post, metadata)
        
        return {"output_id": output_id, "facebook_post": post, "validation_passed": is_valid, "validation_message": message}
    except Exception as e:
        logger.exception("Error generating Facebook post")
        raise HTTPException(status_code=500, detail=f"Error generating Facebook post: {str(e)}")

@app.post("/generate_linkedin_content/")
async def generate_linkedin_content(request: LinkedInPostRequest):
    try:
        chain = LinkedInContentChain()
        post = await chain.generate(mode="content", **request.dict())
        print(f"Validating: {post}, use_case: content, platform: linkedin")
        is_valid, message = validate_content(post, "content")

        
        # Store output in FAISS
        output_id = str(uuid.uuid4())
        metadata = {
            "output_id": output_id,
            "platform": "linkedin",
            "length": request.length,
            "content_topic": request.content_topic,
            "tone": request.tone,
            "professional_insight": request.professional_insight,
            "timestamp": datetime.utcnow().isoformat(),
            "seo_score": float(validate_content(post, "content")[0])
        }
        retriever.store_output(post, metadata)
        
        return {"output_id": output_id, "linkedin_post": post, "validation_passed": is_valid, "validation_message": message}
    except Exception as e:
        logger.exception("Error generating LinkedIn post")
        raise HTTPException(status_code=500, detail=f"Error generating LinkedIn post: {str(e)}")

@app.post("/generate_content_strategy/")
async def generate_strategy(request: StrategyRequest):
    try:
        chain = LinkedInContentChain()  # Using LinkedIn chain for strategy as a placeholder
        strategy = await chain.generate(mode="strategy", **request.dict())
        print(f"Validating: {strategy}, use_case: strategy, platform: all")
        is_valid, message = validate_content(strategy, "strategy")
        
        # Store output in FAISS
        output_id = str(uuid.uuid4())
        metadata = {
            "output_id": output_id,
            "platform": "all",
            "content_goals": request.content_goals,
            "timestamp": datetime.utcnow().isoformat(),
            "seo_score": float(validate_content(strategy, "strategy")[0])
        }
        retriever.store_output(strategy, metadata)
        
        return {"output_id": output_id, "content_strategy": strategy, "validation_passed": is_valid, "validation_message": message}
    except Exception as e:
        logger.exception("Error generating strategy")
        raise HTTPException(status_code=500, detail=f"Error generating strategy: {str(e)}")

@app.post("/generate_calendar/")
async def generate_calendar(request: CalendarRequest):
    try:
        chain = LinkedInContentChain()  # Using LinkedIn chain for calendar as a placeholder
        # Convert list to comma-separated string for downstream prompts
        req_data = request.dict()
        req_data["topic_list"] = ", ".join(req_data["topic_list"])
        calendar = await chain.generate(mode="calendar", **req_data)
        print(f"Validating: {calendar}, use_case: calendar, platform: all")
        is_valid, message = validate_content(calendar, "calendar")
        
        # Store output in FAISS
        output_id = str(uuid.uuid4())
        metadata = {
            "output_id": output_id,
            "platform": "all",
            "brand_summary": request.brand_summary,
            "topic_list": request.topic_list,
            "timestamp": datetime.utcnow().isoformat(),
            "seo_score": float(validate_content(calendar, "calendar")[0])
        }
        retriever.store_output(calendar, metadata)
        
        return {"output_id": output_id, "calendar": calendar, "validation_passed": is_valid, "validation_message": message}
    except Exception as e:
        logger.exception("Error generating calendar")
        raise HTTPException(status_code=500, detail=f"Error generating calendar: {str(e)}")

@app.post("/submit_feedback/")
async def submit_feedback(feedback: FeedbackRequest):
    try:
        output_data = retriever.get_output(feedback.output_id)
        if not output_data:
            raise HTTPException(status_code=404, detail="Output not found")
        
        output_data["metadata"]["feedback"] = {
            "rating": feedback.rating,
            "comment": feedback.comment,
            "engagement_metrics": feedback.engagement_metrics,
            "label": determine_label(feedback)
        }
        retriever.update_output(feedback.output_id, output_data)
        
        return {"message": "Feedback submitted successfully", "output_id": feedback.output_id}
    except Exception as e:
        logger.exception("Error submitting feedback")
        raise HTTPException(status_code=500, detail=f"Error submitting feedback: {str(e)}")

def determine_label(feedback: FeedbackRequest) -> str:
    if feedback.rating and feedback.rating >= 4:
        return "high_engagement"
    elif feedback.engagement_metrics and feedback.engagement_metrics.get("likes", 0) > 50:
        return "high_engagement"
    return "needs_improvement"

@app.post("/regenerate_output/")
async def regenerate_output(request: RegenerateRequest):
    try:
        data = retriever.get_output(request.output_id)
        if not data:
            raise HTTPException(status_code=404, detail="Output not found")
        meta = data["metadata"]
        platform = meta.get("platform")
        use_case = "content" if platform in ["facebook", "instagram", "linkedin"] else "strategy"
        chain_map = {
            "instagram": InstagramContentChain,
            "facebook": FacebookContentChain,
            "linkedin": LinkedInContentChain,
            "all": LinkedInContentChain,
        }
        chain_cls = chain_map.get(platform, LinkedInContentChain)
        chain = chain_cls()
        # Build args based on metadata
        generate_args = meta.copy()
        # remove keys not expected
        for key in ["output_id", "platform", "timestamp", "seo_score", "feedback"]:
            generate_args.pop(key, None)
        new_output = await chain.generate(mode=use_case, **generate_args)
        # store as new record
        new_id = str(uuid.uuid4())
        meta["output_id"] = new_id
        meta["regenerated_from"] = request.output_id
        meta["timestamp"] = datetime.utcnow().isoformat()
        retriever.store_output(new_output, meta)
        return {"output_id": new_id, "content": new_output}
    except Exception as e:
        logger.exception("Error regenerating output")
        raise HTTPException(status_code=500, detail=f"Error regenerating output: {str(e)}")