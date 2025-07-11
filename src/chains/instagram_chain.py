from src.chains.base_chain import BaseChain
from src.prompts.social_media_prompt import instagram_content_prompt, instagram_strategy_prompt
from src.rag_pipeline import get_rag_chain
from src.langchain_utils import save_output, timestamp
import asyncio

class InstagramContentChain(BaseChain):
    def __init__(self):
        self.rag_chain = get_rag_chain(use_case="content", platform="instagram")

    async def get_prompt(self, mode, **kwargs):
        if mode == "content":
            context = await self.rag_chain.ainvoke({"context": "SEO and website builder", "platform": "instagram", **kwargs})
            return instagram_content_prompt.format(context=context["result"], **kwargs)
        elif mode == "strategy":
            context = await self.rag_chain.ainvoke({"context": "content strategy", "platform": "instagram", **kwargs})
            return instagram_strategy_prompt.format(context=context["result"], **kwargs)
        elif mode == "calendar":
            context = await self.rag_chain.ainvoke({"context": "content calendar", "platform": "instagram", **kwargs})
            from src.prompts.social_media_prompt import calendar_prompt
            return calendar_prompt.format(context=context["result"], **kwargs)
        return None

    async def generate(self, mode="content", **kwargs):
        if mode not in ["content", "strategy", "calendar"]:
            raise ValueError("Mode must be 'content', 'strategy', or 'calendar'")
        kwargs.setdefault("feedback_context", "")

        # For calendar we use a dedicated calendar RAG chain targeting the pseudo platform "all"
        if mode == "calendar":
            # Use a generic RAG chain that is configured for calendar creation
            calendar_chain = get_rag_chain(use_case="calendar", platform="all")
            response = await calendar_chain.ainvoke(kwargs)
            result = response["result"]
            output_dir = "data/output/calendars"
            save_output(result, output_dir, "content_calendar")
            return result

        # Default path for content / strategy
        prompt = await self.get_prompt(mode, **kwargs)
        from src.agents.social_media_agent import SocialMediaAgent
        agent = SocialMediaAgent(platform="instagram")
        result = await agent.generate(use_case=mode, **kwargs)
        output_dir = f"data/output/instagram_{mode}s"
        save_output(result, output_dir, f"instagram_{mode}")
        return result