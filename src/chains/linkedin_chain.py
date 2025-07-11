from src.chains.base_chain import BaseChain
from src.prompts.social_media_prompt import linkedin_content_prompt, linkedin_strategy_prompt
from src.rag_pipeline import get_rag_chain
from src.langchain_utils import save_output, timestamp
import asyncio

class LinkedInContentChain(BaseChain):
    def __init__(self):
        self.rag_chain = get_rag_chain(use_case="content", platform="linkedin")

    async def get_prompt(self, mode, **kwargs):
        if mode == "content":
            context = await self.rag_chain.ainvoke({"context": "professional networking", "platform": "linkedin", **kwargs})
            return linkedin_content_prompt.format(context=context["result"], **kwargs)
        elif mode == "strategy":
            context = await self.rag_chain.ainvoke({"context": "content strategy", "platform": "linkedin", **kwargs})
            return linkedin_strategy_prompt.format(context=context["result"], **kwargs)
        elif mode == "calendar":
            from src.prompts.social_media_prompt import calendar_prompt
            context = await self.rag_chain.ainvoke({"context": "content calendar", "platform": "linkedin", **kwargs})
            return calendar_prompt.format(context=context["result"], **kwargs)
        return None

    async def generate(self, mode="content", **kwargs):
        if mode not in ["content", "strategy", "calendar"]:
            raise ValueError("Mode must be 'content', 'strategy', or 'calendar'")
        # ensure optional keys exist
        kwargs.setdefault("feedback_context", "")
        if mode == "strategy":
            kwargs.setdefault("content_goals", "")

        if mode == "calendar":
            calendar_chain = get_rag_chain(use_case="calendar", platform="all")
            response = await calendar_chain.ainvoke(kwargs)
            result = response["result"]
            output_dir = "data/output/calendars"
            save_output(result, output_dir, "content_calendar")
            return result

        prompt = await self.get_prompt(mode, **kwargs)
        from src.agents.social_media_agent import SocialMediaAgent
        agent = SocialMediaAgent(platform="linkedin")
        result = await agent.generate(use_case=mode, **kwargs)
        output_dir = f"data/output/linkedin_{mode}s"
        save_output(result, output_dir, f"linkedin_{mode}")
        return result