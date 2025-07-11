from langchain_core.prompts import PromptTemplate

instagram_content_prompt = PromptTemplate(
    input_variables=["content_topic", "tone", "persona", "context", "feedback_context"],
    template="""Create a 3-line Instagram caption about this topic: "{content_topic}", focusing on SEO importance, conversion benefits, and our SEO-friendly website product.
Use a {tone} tone and write for a {persona}, leveraging the context provided.
Include emojis, a compelling hook, 1–2 SEO or conversion tips, a call to action (e.g., DM us), and use these high-performing examples for inspiration: {feedback_context}
Suggest 3–5 relevant hashtags.
Context: {context}
"""
)

instagram_strategy_prompt = PromptTemplate(
    input_variables=["platforms", "content_goals", "context", "feedback_context"],
    template="""Create a **30-day Instagram content strategy** to accomplish these goals: {content_goals}.

Respond in **Markdown** with these sections:
1. **Objectives & KPIs**  
2. **Audience Personas** (bullet points)  
3. **Visual Style & Aesthetic** (color, typography, mood)  
4. **Core Content Pillars** – table: Pillar | Example Topics | Desired Outcome  
5. **Format Mix & Cadence** – Reels vs. Carousels vs. Stories; weekly schedule optimized for reach & saves  
6. **Hashtag & SEO Tactics** – keyword placement in caption, 3-tier hashtag sets, alt-text  
7. **Engagement & Algorithm Signals** – early engagement tactics, collabs, UGC, saves/shares  
8. **Measurement & Iteration** – metrics, review cadence  
9. **Next 2-Week Action Plan** – immediate steps

Leverage:  
• High-performing examples: {feedback_context}  
• Context: {context}
"""
)

calendar_prompt = PromptTemplate(
    input_variables=["brand_summary", "topic_list", "context", "feedback_context"],
    template="""Based on the brand_summary and topics below, create a 7-day content plan focusing on SEO, conversions, and our SEO-friendly website product.
Return exactly 7 rows in this format:
Day | Platform | Content Type | Topic | Caption Summary | CTA
Guidelines:
• Use the exact word "SEO" ONLY ONCE in the full 7-row table (preferably in Day 1).
• Do NOT use the words "conversions" or "website" more than ONCE each in the entire table; use synonyms like "sales" or "site" elsewhere.
• Keep each caption summary concise (≤12 words) and avoid keyword stuffing.
Use these high-performing examples for inspiration: {feedback_context}
Brand Summary: {brand_summary}
Topics: {topic_list}
Context: {context}
"""
)

facebook_content_prompt = PromptTemplate(
    input_variables=["content_topic", "tone", "audience", "context", "feedback_context"],
    template="""Create a Facebook post about {content_topic}, emphasizing SEO importance, conversion benefits, and our SEO-friendly website product.
Use a {tone} tone and tailor it to the {audience}, leveraging the context provided.
Include a question to engage readers, a call to action, and use these high-performing examples for inspiration: {feedback_context}
Context: {context}
"""
)

facebook_strategy_prompt = PromptTemplate(
    input_variables=["platforms", "content_goals", "context", "feedback_context"],
    template="""Develop a **90-day Facebook content strategy** to achieve: {content_goals}.

Provide the plan in **Markdown** with these sections:
1. **Objectives & KPIs**  
2. **Audience Segments & Pain-Points**  
3. **Content Pillars** – table: Pillar | Post Types | Goal  
4. **Format & Cadence** – mix of long-form posts, Reels, Lives, Groups; week-by-week schedule  
5. **SEO & Distribution Tactics** – keyword usage, link previews, alt-text, cross-posting  
6. **Engagement & Community Building** – comments, groups, messenger, events  
7. **Paid Amplification** – boosting best posts, audience targeting  
8. **Measurement & Reporting** – metrics, toolset, review cycles  
9. **First 4-Week Roadmap** – tasks & milestones

Resources to consider:  
High-performing examples: {feedback_context}  
Context: {context}
"""
)

linkedin_content_prompt = PromptTemplate(
    input_variables=["content_topic", "tone", "professional_insight", "context", "feedback_context"],
    template="""Draft a professional LinkedIn post about {content_topic}, highlighting SEO importance, conversion benefits, and our SEO-friendly website product.
Maintain a {tone} tone, integrate {professional_insight}, and use the context provided.
Include highlights, stats (if available in context), an inspiring close, and use these high-performing examples for inspiration: {feedback_context}
Context: {context}
"""
)

linkedin_strategy_prompt = PromptTemplate(
    input_variables=["platforms", "content_goals", "context", "feedback_context"],
    template="""Develop a **90-day LinkedIn content strategy** to achieve the following goals: {content_goals}.

Respond in **Markdown** and structure your answer using these sections:

1. **Objectives & KPIs**  
   • …  
2. **Audience Personas** – 2-3 bullet points each  
3. **Core Content Pillars** – table with Pillar | Topic Examples | Goal  
4. **Content Formats & Cadence** – weekly schedule (e.g., Mon-Fri posts, polls, carousels)  
5. **SEO & Conversion Tactics** – keyword approach, hooks, CTAs  
6. **Engagement Plan** – how to interact with comments, communities, influencers  
7. **Measurement** – metrics, tools, review cadence  
8. **Action Plan / Timeline** – next steps for the first 4 weeks

Incorporate the following resources where relevant:
High-performing examples: {feedback_context}
Context: {context}
"""
)

strategy_prompt = PromptTemplate(
    input_variables=["platforms", "content_goals", "context", "feedback_context"],
    template="""Develop a content strategy for {platforms} focusing on {content_goals}, with an emphasis on SEO education, conversion strategies, and promoting our SEO-friendly website product.
Use the context and high-performing examples provided to inform the plan.
High-performing examples: {feedback_context}
Context: {context}
"""
)