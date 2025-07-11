import streamlit as st
from src.rag_pipeline import setup_rag_pipeline, generate_content
from datetime import datetime

st.title("Productimate Content Generator")

if "pipeline" not in st.session_state:
    st.session_state.pipeline = setup_rag_pipeline()

platform = st.selectbox("Select Platform", ["instagram", "facebook", "linkedin"])
mode = st.selectbox("Select Mode", ["content", "strategy"])
if platform and mode:
    if st.button("Generate Content"):
        input_data = {
            "instagram": {"main_benefit": "Boost SEO", "cta": "DM us!", "content_goals": "Establish authority"},
            "facebook": {"main_benefit": "Drive traffic", "cta": "Visit us!", "content_goals": "Increase awareness"},
            "linkedin": {"business_value": "40% boost", "success_metrics": "60% conversions", "professional_insight": "SEO importance", "content_goals": "Build network"}
        }[platform]
        result = generate_content(st.session_state.pipeline, platform, mode=mode, **{k: v for k, v in input_data.items() if k in kwargs})
        st.write(f"Generated at {datetime.now().strftime('%I:%M %p IST on %B %d, %Y')}:\n{result}")

        