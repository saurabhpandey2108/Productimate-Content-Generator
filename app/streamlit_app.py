import streamlit as st
import requests
from functools import partial
import os

API_URL = os.getenv("CONTENT_API_URL", "https://productimate-content-generator.onrender.com")

st.set_page_config(page_title="Productimate Content Generator", layout="wide")
# ---- Custom CSS for cleaner design ----
custom_css = """
<style>
/* Center headers & add subtle gradient */
.main h1, .main h2, .main h3 {text-align:center; background: -webkit-linear-gradient(45deg,#3b82f6,#ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
/* Rounded text areas */
textarea {border-radius:8px !important;}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)



# ---- Sidebar ----
st.sidebar.title("🚀 Productimate Content Generator")
st.sidebar.caption("Crafted with ❤️ by Saurabh Pandey")

# --- Quick Promote ---
st.sidebar.markdown("---")
st.sidebar.subheader("⭐ Add to Library")
promote_id = st.sidebar.text_input("Output ID", key="promote_id")
if st.sidebar.button("Star & Promote", key="promote_btn"):
    if promote_id:
        payload = {
            "output_id": promote_id,
            "rating": 5,
            "comment": "Promoted via sidebar star",
            "engagement_metrics": {"likes": 100}
        }
        try:
            r = requests.post(f"{API_URL}/submit_feedback/", json=payload)
            if r.ok:
                st.sidebar.success("Promoted! Now in RAG context.")
            else:
                st.sidebar.error(r.json().get("detail", "Error"))
        except Exception as e:
            st.sidebar.error(str(e))

brochure_file = st.sidebar.file_uploader("Update Company Brochure (PDF)", type=["pdf"])

social_links = st.sidebar.text_area(
    "Company Social Links (one per line)",
    placeholder="https://linkedin.com/company/...\nhttps://instagram.com/...\n...",
    height=100,
)

if st.sidebar.button("(Re)Build RAG Index"):
    if brochure_file:
        tmp_path = "tmp_brochure.pdf"
        with open(tmp_path, "wb") as f:
            f.write(brochure_file.getbuffer())
        resp = requests.post(f"{API_URL}/rebuild_index/", params={"overwrite": True})
        if resp.status_code == 200:
            st.sidebar.success("Index rebuilt!")
        else:
            st.sidebar.error(resp.json().get("detail", "Error rebuilding index"))
    else:
        st.sidebar.warning("Please upload a brochure first.")

st.sidebar.markdown("---")
with st.sidebar.expander("About"):
    st.write(
        """Productimate.io streamlit interface. Generate SEO-optimised social media content, whole strategies, and content calendars powered by RAG & GPT-4o."""
    )

# ---- Main ----
TABS = ["Instagram", "Facebook", "LinkedIn", "Strategy", "Calendar", "Feedback / Regenerate"]
choice = st.tabs(TABS)

# Tab 0 – Instagram
with choice[0]:
    st.header("📸 Instagram Caption Generator")
    topic = st.text_input("Content Topic")
    length = st.selectbox("Desired Length", ["short", "medium", "long"], index=1)
    tone = st.selectbox("Tone", ["neutral", "fun", "professional", "inspirational"])
    persona = st.text_input("Persona", placeholder="e.g. Startup Founder")

    # Ensure state flag exists
    if "ig_generating" not in st.session_state:
        st.session_state.ig_generating = False

    generate_clicked = st.button("Generate Instagram Caption", disabled=st.session_state.ig_generating)
    if generate_clicked:
        st.session_state.ig_generating = True
        payload = {"content_topic": topic, "tone": tone, "persona": persona, "length": length}
        with st.spinner("Generating caption ..."):
            r = requests.post(f"{API_URL}/generate_instagram_content/", json=payload)
        st.session_state.ig_generating = False
        if r.ok:
            data = r.json()
            st.success("Generated!")
            st.text_area("Caption", data["instagram_caption"], height=200)
            st.write("Output ID:", data["output_id"])
            if not data.get("validation_passed", True):
                st.warning("This caption did not pass SEO validation. Consider regenerating.")
                if st.button("Regenerate", key=f"regen_ig_{data['output_id']}"):
                    regen_resp = requests.post(f"{API_URL}/regenerate_output/", json={"output_id": data["output_id"]})
                    if regen_resp.ok:
                        regen_data = regen_resp.json()
                        st.success("Regenerated!")
                        st.text_area("New Caption", regen_data["content"], height=200)
                        st.write("New Output ID:", regen_data["output_id"])
                    else:
                        st.error(regen_resp.json().get("detail", "Error"))
        else:
            st.error(r.json().get("detail", "Error"))

# Tab 1 – Facebook
with choice[1]:
    st.header("📘 Facebook Post Generator")
    topic = st.text_input("Content Topic", key="fb_topic")
    length_fb = st.selectbox("Desired Length", ["short", "medium", "long"], index=1, key="fb_len")
    tone = st.selectbox("Tone", ["neutral", "casual", "professional"], key="fb_tone")
    audience = st.text_input("Audience", key="fb_aud")

    if "fb_generating" not in st.session_state:
        st.session_state.fb_generating = False

    fb_clicked = st.button("Generate Facebook Post", disabled=st.session_state.fb_generating)
    if fb_clicked:
        st.session_state.fb_generating = True
        payload = {"content_topic": topic, "tone": tone, "audience": audience, "length": length_fb}
        with st.spinner("Generating post ..."):
            r = requests.post(f"{API_URL}/generate_facebook_content/", json=payload)
        st.session_state.fb_generating = False
        if r.ok:
            data = r.json()
            st.success("Generated!")
            st.text_area("Post", data["facebook_post"], height=200)
            st.write("Output ID:", data["output_id"])
            if not data.get("validation_passed", True):
                st.warning("This post did not pass SEO validation. Consider regenerating.")
                if st.button("Regenerate", key=f"regen_fb_{data['output_id']}"):
                    regen_resp = requests.post(f"{API_URL}/regenerate_output/", json={"output_id": data["output_id"]})
                    if regen_resp.ok:
                        regen_data = regen_resp.json()
                        st.success("Regenerated!")
                        st.text_area("New Post", regen_data["content"], height=200)
                        st.write("New Output ID:", regen_data["output_id"])
                    else:
                        st.error(regen_resp.json().get("detail", "Error"))
        else:
            st.error(r.json().get("detail", "Error"))

# Tab 2 – LinkedIn
with choice[2]:
    st.header("💼 LinkedIn Post Generator")
    topic = st.text_input("Content Topic", key="li_topic")
    length_li = st.selectbox("Desired Length", ["short", "medium", "long"], index=1, key="li_len")
    tone = st.selectbox("Tone", ["neutral", "thought-leadership", "professional"], key="li_tone")
    insight = st.text_input("Professional Insight", key="li_insight")

    if "li_generating" not in st.session_state:
        st.session_state.li_generating = False

    li_clicked = st.button("Generate LinkedIn Post", disabled=st.session_state.li_generating)
    if li_clicked:
        st.session_state.li_generating = True
        payload = {"content_topic": topic, "tone": tone, "professional_insight": insight, "length": length_li}
        with st.spinner("Generating post ..."):
            r = requests.post(f"{API_URL}/generate_linkedin_content/", json=payload)
        st.session_state.li_generating = False
        if r.ok:
            st.session_state.li_last_output = r.json()
        else:
            st.error(r.json().get("detail", "Error"))

    # Show last generated LinkedIn content if available
    if "li_last_output" in st.session_state:
        data = st.session_state.li_last_output
        st.code(data["linkedin_post"], language="markdown")
        st.write("Output ID:", data["output_id"])
        if not data.get("validation_passed", True):
            st.warning("This post did not pass SEO validation. Consider regenerating.")
            if st.button("Regenerate", key=f"regen_li_{data['output_id']}"):
                with st.spinner("Regenerating ..."):
                    regen_resp = requests.post(f"{API_URL}/regenerate_output/", json={"output_id": data["output_id"]})
                if regen_resp.ok:
                    regen_data = regen_resp.json()
                    # Store new result
                    # Validation check of regenerated content
                    passed, _ = True, ""
                    if "validation_passed" in regen_data:
                        passed = regen_data["validation_passed"]
                    st.session_state.li_last_output = {"linkedin_post": regen_data["content"], "output_id": regen_data["output_id"], "validation_passed": passed}
                    st.success("Regenerated!")
                    # Trigger UI refresh compatibly across Streamlit versions
                    if hasattr(st, "rerun"):
                        st.rerun()
                    elif hasattr(st, "experimental_rerun"):
                        st.experimental_rerun()
                else:
                    st.error(regen_resp.json().get("detail", "Error"))

# Tab 3 – Content Strategy
with choice[3]:
    st.header("🧠 Content Strategy Generator")
    platforms = st.multiselect("Platforms", ["instagram", "facebook", "linkedin", "website"])
    goals = st.text_area("Content Goals", placeholder="Increase brand awareness, drive traffic, ...")

    if "strategy_generating" not in st.session_state:
        st.session_state.strategy_generating = False

    strat_clicked = st.button("Generate Strategy", disabled=st.session_state.strategy_generating)
    if strat_clicked:
        st.session_state.strategy_generating = True
        payload = {"platforms": platforms, "content_goals": goals}
        with st.spinner("Generating strategy ..."):
            r = requests.post(f"{API_URL}/generate_content_strategy/", json=payload)
        st.session_state.strategy_generating = False
        if r.ok:
            st.session_state.strategy_last_output = r.json()
        else:
            st.error(r.json().get("detail", "Error"))

    if "strategy_last_output" in st.session_state:
        data = st.session_state.strategy_last_output
        st.code(data["content_strategy"], language="markdown")
        st.write("Output ID:", data["output_id"])

# Tab 4 – Calendar
with choice[4]:
    st.header("🗓️ 7-Day Content Calendar Generator")
    summary = st.text_area("Brand Summary")
    topics = st.text_input("Comma-separated Topic List", placeholder="SEO Basics, Product Demo, Industry Trends")

    if "calendar_generating" not in st.session_state:
        st.session_state.calendar_generating = False

    cal_clicked = st.button("Generate Calendar", disabled=st.session_state.calendar_generating)
    if cal_clicked:
        st.session_state.calendar_generating = True
        payload = {"brand_summary": summary, "topic_list": [t.strip() for t in topics.split(",") if t.strip()]}
        with st.spinner("Generating calendar ..."):
            r = requests.post(f"{API_URL}/generate_calendar/", json=payload)
        st.session_state.calendar_generating = False
        if r.ok:
            st.session_state.calendar_last_output = r.json()
        else:
            st.error(r.json().get("detail", "Error"))

    if "calendar_last_output" in st.session_state:
        data = st.session_state.calendar_last_output
        st.code(data["calendar"], language="markdown")
        st.write("Output ID:", data["output_id"])

# Tab 5 – Feedback / Regenerate
with choice[5]:
    st.header("⭐ Submit Feedback & Regenerate")
    with st.form("feedback_form"):
        output_id = st.text_input("Output ID")
        rating = st.slider("Rating", 1, 5, 4)
        comment = st.text_area("Comment")
        likes = st.number_input("Likes", min_value=0)
        submitted = st.form_submit_button("Submit Feedback")
        if submitted:
            payload = {
                "output_id": output_id,
                "rating": rating,
                "comment": comment,
                "engagement_metrics": {"likes": likes},
            }
            r = requests.post(f"{API_URL}/submit_feedback/", json=payload)
            if r.ok:
                st.success("Feedback submitted!")
            else:
                st.error(r.json().get("detail", "Error"))
    st.markdown("---")
    regen_id = st.text_input("Regenerate from Output ID")
    if st.button("Regenerate"):
        r = requests.post(f"{API_URL}/regenerate_output/", json={"output_id": regen_id})
        if r.ok:
            data = r.json()
            st.success("Regenerated!")
            st.text_area("New Content", data["content"], height=200)
            st.write("New Output ID:", data["output_id"])
        else:
            st.error(r.json().get("detail", "Error"))
