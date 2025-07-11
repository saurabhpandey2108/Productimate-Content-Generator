from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class BaseAgent:
    def __init__(self, tools, prompt_template):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.tools = tools
        self.prompt = PromptTemplate.from_template(prompt_template)
        self.agent = create_react_agent(llm=self.llm, tools=self.tools, prompt=self.prompt)
        self.executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=False)  # Set verbose=False for production

    async def run(self, input_data):
        """
        Execute the agent's chain with the provided input data.
        """
        try:
            # Use ainvoke to handle async execution and multi-key output
            result = await self.executor.ainvoke(input_data)
            # Extract the 'output' key from the agent response
            if isinstance(result, dict) and "output" in result:
                return result["output"]
            return result
        except Exception as e:
            logger.error(f"Error executing agent: {str(e)}")
            raise

    def validate_output(self, output, use_case, platform=None):
        """Validate that the output aligns with the use case, platform, and SEO goals."""
        output_lower = output.lower()
        # Structural validation
        if use_case == "content":
            if platform == "instagram" and "caption" not in output_lower:
                return False, f"Instagram content should include 'caption' (got: {output})"
            elif platform == "facebook" and "post" not in output_lower:
                return False, f"Facebook content should include 'post' (got: {output})"
            elif platform == "linkedin" and "post" not in output_lower:
                return False, f"LinkedIn content should include 'post' (got: {output})"
        elif use_case == "strategy" and not any(k in output_lower for k in ["strategy", "plan", "schedule"]):
            return False, f"Strategy output should include 'strategy', 'plan', or 'schedule' (got: {output})"
        elif use_case == "calendar" and not any(k in output_lower for k in ["day", "schedule", "calendar"]):
            return False, f"Calendar output should include 'day', 'schedule', or 'calendar' (got: {output})"
        # SEO-specific validation
        seo_keywords = ["seo", "conversions", "website"]
        if not any(k in output_lower for k in seo_keywords):
            return False, f"Output should include SEO-related keywords (e.g., 'SEO', 'conversions', 'website') (got: {output})"
        return True, "Output aligns with use case, platform, and SEO goals"