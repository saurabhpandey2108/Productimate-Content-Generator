import streamlit as st
import requests
import pandas as pd
import json
import os

st.set_page_config(page_title="Productimate.io Dashboard", layout="wide")

# API base URL
API_URL = "http://localhost:8000"

st.title("Productimate.io Content Generation & Feedback")

# Content Generation
st.header("Generate Content")
platform = st.selectbox("Platform", ["Instagram", "Facebook", "LinkedIn", "Strategy", "Calendar"])
content_topic = st.text_input("Content Topic", "SEO tips")
tone = st.text_input("Tone", "Engaging")
persona = st.text_input("Persona (for Instagram)", "Small business owner")
audience = st.text_input("Audience (for Facebook)", "Entrepreneurs")
professional_insight = st.text_input("Professional Insight (for LinkedIn)", "Industry trends")
content_goals = st.text_input("Content Goals (for Strategy)", "Increase engagement")
brand_summary = st.text_input("Brand Summary (for Calendar)", "SEO-focused SaaS")
topic_list = st.text_input("Topic List (for Calendar)", "SEO, conversions, website optimization")

if st.button("Generate"):
    try:
        if platform == "Instagram":
            response = requests.post(f"{API_URL}/generate_instagram_content/", json={
                "content_topic": content_topic,
                "tone": tone,
                "persona": persona
            })
        elif platform == "Facebook":
            response = requests.post(f"{API_URL}/generate_facebook_content/", json={
                "content_topic": content_topic,
                "tone": tone,
                "audience": audience
            })
        elif platform == "LinkedIn":
            response = requests.post(f"{API_URL}/generate_linkedin_content/", json={
                "content_topic": content_topic,
                "tone": tone,
                "professional_insight": professional_insight
            })
        elif platform == "Strategy":
            response = requests.post(f"{API_URL}/generate_content_strategy/", json={
                "platforms": ["all"],
                "content_goals": content_goals
            })
        else:  # Calendar
            response = requests.post(f"{API_URL}/generate_calendar/", json={
                "brand_summary": brand_summary,
                "topic_list": topic_list
            })
        
        result = response.json()
        st.session_state["output_id"] = result["output_id"]
        st.write("**Generated Content:**")
        content_key = "instagram_caption" if platform == "Instagram" else \
                      "facebook_post" if platform == "Facebook" else \
                      "linkedin_post" if platform == "LinkedIn" else \
                      "content_strategy" if platform == "Strategy" else \
                      "calendar"
        st.write(result[content_key])
    except Exception as e:
        st.error(f"Error generating content: {str(e)}")

# Feedback Submission
st.header("Submit Feedback")
output_id = st.text_input("Output ID", st.session_state.get("output_id", ""))
rating = st.slider("Rating (1-5)", 1, 5, 3)
comment = st.text_area("Comment")
likes = st.number_input("Likes (Engagement)", 0, 1000, 0)
shares = st.number_input("Shares (Engagement)", 0, 1000, 0)

if st.button("Submit Feedback"):
    try:
        response = requests.post(f"{API_URL}/submit_feedback/", json={
            "output_id": output_id,
            "rating": rating,
            "comment": comment,
            "engagement_metrics": {"likes": likes, "shares": shares}
        })
        st.success(response.json()["message"])
    except Exception as e:
        st.error(f"Error submitting feedback: {str(e)}")

# Metrics Visualization
st.header("Performance Metrics")
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
feedback_dir = os.path.join(project_root, "data", "output", "feedback_data")
feedback_files = [f for f in os.listdir(feedback_dir) if f.startswith("feedback_")]
if feedback_files:
    feedback_data = []
    for file in feedback_files:
        with open(os.path.join(feedback_dir, file), "r") as f:
            feedback_data.extend(json.load(f))
    
    df = pd.DataFrame([
        {
            "Platform": d["metadata"]["platform"],
            "Rating": d["metadata"]["feedback"].get("rating", None),
            "Likes": d["metadata"]["feedback"].get("engagement_metrics", {}).get("likes", 0),
            "Shares": d["metadata"]["feedback"].get("engagement_metrics", {}).get("shares", 0),
            "Timestamp": d["metadata"]["timestamp"]
        }
        for d in feedback_data if "feedback" in d["metadata"]
    ])
    
    st.write("**Feedback Summary**")
    st.dataframe(df)
    
    st.write("**Average Rating by Platform**")
    st.bar_chart(df.groupby("Platform")["Rating"].mean())
    
    st.write("**Engagement Trends**")
    st.line_chart(df[["Likes", "Shares"]])
else:
    st.write("No feedback data available.")