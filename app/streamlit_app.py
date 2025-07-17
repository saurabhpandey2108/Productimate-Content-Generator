import streamlit as st
import requests
from functools import partial
import os

API_URL = os.getenv("CONTENT_API_URL", "https://productimate-content-generator.onrender.com")

st.set_page_config(page_title="Productimate Content Generator", layout="wide")

# ---- Custom CSS for enhanced design with new color scheme and effects ----
custom_css = """
<style>
/* Root variables for color scheme */
:root {
    --primary: #14b8a6; /* Teal */
    --accent: #f43f5e; /* Coral */
    --neutral-dark: #1f2937; /* Dark gray */
    --neutral-light: #f9fafb; /* Off-white */
    --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Main container with gradient background */
.main {
    background: linear-gradient(135deg, var(--neutral-light), #e5e7eb);
    padding: 20px;
    border-radius: 12px;
}

/* Center headers with gradient */
.main h1, .main h2, .main h3 {
    text-align: center;
    background: linear-gradient(45deg, var(--primary), var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 20px;
    font-weight: 700;
}

/* Input styling with shadows and transitions */
textarea, input[type="text"], select {
    border-radius: 8px !important;
    border: 1px solid #d1d5db;
    padding: 12px;
    font-size: 16px;
    box-shadow: var(--shadow);
    transition: all 0.3s ease;
}
textarea:focus, input[type="text"]:focus, select:focus {
    border-color: var(--primary);
    box-shadow: 0 0 8px rgba(20, 184, 166, 0.3);
}

/* Button styling with hover effects */
button {
    background-color: var(--primary);
    color: white;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: bold;
    box-shadow: var(--shadow);
    transition: transform 0.2s ease, background-color 0.3s ease;
}
button:hover {
    background-color: var(--accent);
    transform: scale(1.05);
}

/* Sidebar styling */
.sidebar .sidebar-content {
    background-color: var(--neutral-light);
    padding: 20px;
    border-radius: 8px;
    box-shadow: var(--shadow);
}

/* Input labels */
label {
    font-weight: 600;
    color: var(--neutral-dark);
    margin-bottom: 8px;
    display: block;
}

/* Tooltip styling */
.tooltip {
    position: relative;
    display: inline-block;
    cursor: help;
}
.tooltip .tooltiptext {
    visibility: hidden;
    width: 240px;
    background-color: var(--neutral-dark);
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 8px;
    position: absolute;
    z-index: 1;
    bottom: 125%;
    left: 50%;
    margin-left: -120px;
    opacity: 0;
    transition: opacity 0.3s;
}
.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---- Sidebar ----
st.sidebar.title("🚀 Productimate Content Generator")
st.sidebar.caption("Crafted with ❤️ by Saurabh Pandey")

# --- Quick Promote ---
st.sidebar.markdown("---")
st.sidebar.subheader("⭐ Add to Library")
promote_id = st.sidebar.text_input("Output ID", key="promote_id", placeholder="Enter the Output ID to promote")
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
    else:
        st.sidebar.error("Please enter a valid Output ID.")

brochure_file = st.sidebar.file_uploader("Update Company Brochure (PDF)", type=["pdf"], help="Upload a PDF brochure to update the RAG index.")

social_links = st.sidebar.text_area(
    "Company Social Links (one per line)",
    placeholder="https://linkedin.com/company/...\nhttps://instagram.com/...\n...",
    height=100,
    help="Enter social media URLs, one per line, to include in the RAG context."
)

if st.sidebar.button("(Re)Build RAG Index"):
    if brochure_file:
        tmp_path = "tmp_brochure.pdf"
        with open(tmp_path, "wb") as f:
            f.write(brochure_file.getbuffer())
        resp = requests.post(f"{API_URL}/rebuild_index/", params={"overwrite": True})
        if resp.status_code == 200:
            st.sidebar.success("Index rebuilt successfully!")
        else:
            st.sidebar.error(resp.json().get("detail", "Error rebuilding index"))
    else:
        st.sidebar.warning("Please upload a brochure first.")

st.sidebar.markdown("---")
with st.sidebar.expander("About"):
    st.write(
        """Productimate.io streamlit interface. Generate SEO-optimized social media content, strategies, and calendar plans powered by RAG & GPT-4o."""
    )

# ---- Main ----
TABS = ["Instagram", "Facebook", "LinkedIn", "Strategy", "Calendar", "Feedback / Regenerate"]
choice = st.tabs(TABS)

# Tab 0 – Instagram
with choice[0]:
    st.header("📸 Instagram Caption Generator")
    with st.container():
        st.markdown("**Create engaging Instagram captions optimized for SEO.**")
        topic = st.text_input("Content Topic", placeholder="e.g., Digital Marketing Tips", help="Enter the main topic or theme for your caption.")
        length = st.selectbox("Desired Length", ["short", "medium", "long"], index=1, help="Choose the length of the caption.")
        tone = st.selectbox("Tone", ["neutral", "fun", "professional", "inspirational"], help="Select the tone that matches your brand voice.")
        persona = st.text_input("Persona", placeholder="e.g., Startup Founder, Fitness Coach", help="Specify the target audience or persona for the caption.")

        if "ig_generating" not in st.session_state:
            st.session_state.ig_generating = False

        generate_clicked = st.button("Generate Instagram Caption", disabled=st.session_state.ig_generating)
        if generate_clicked:
            if not topic.strip():
                st.error("Please provide a content topic.")
            else:
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
    with st.container():
        st.markdown("**Generate engaging Facebook posts tailored to your audience.**")
        topic = st.text_input("Content Topic", key="fb_topic", placeholder="e.g., Product Launch", help="Enter the main topic for your post.")
        length_fb = st.selectbox("Desired Length", ["short", "medium", "long"], index=1, key="fb_len", help="Choose the length of the post.")
        tone = st.selectbox("Tone", ["neutral", "casual", "professional"], key="fb_tone", help="Select the tone for the post.")
        audience = st.text_input("Audience", key="fb_aud", placeholder="e.g., Small Business Owners", help="Specify the target audience for the post.")

        if "fb_generating" not in st.session_state:
            st.session_state.fb_generating = False

        fb_clicked = st.button("Generate Facebook Post", disabled=st.session_state.fb_generating)
        if fb_clicked:
            if not topic.strip():
                st.error("Please provide a content topic.")
            else:
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
    with st.container():
        st.markdown("**Craft professional LinkedIn posts to boost engagement and SEO.**")
        topic = st.text_input(
            "Content Topic",
            key="li_topic",
            placeholder="e.g., Leadership Tips, Industry Trends",
            help="Enter the main topic or theme for your LinkedIn post."
        )
        length_li = st.selectbox(
            "Desired Length",
            ["short", "medium", "long"],
            index=1,
            key="li_len",
            help="Choose the length of the post."
        )
        tone = st.selectbox(
            "Tone",
            ["neutral", "thought-leadership", "professional"],
            key="li_tone",
            help="Select the tone that aligns with your professional voice."
        )
        st.markdown(
            """
            <div class="tooltip">
                <label>Professional Insight</label>
                <span class="tooltiptext">Add a unique perspective, industry knowledge, or key takeaway to make your post stand out. For example: 'Why data-driven decisions are critical for startups' or 'The importance of work-life balance in leadership'.</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        insight = st.text_input(
            "Professional Insight",
            key="li_insight",
            placeholder="e.g., Why data-driven decisions are critical for startups",
            help="Provide a unique perspective or key takeaway to enhance your post."
        )
        st.markdown(
            """
            **Example Professional Insights:**
            - "The key to scaling a startup is prioritizing customer feedback over assumptions."
            - "Effective leadership means empowering your team to take risks and innovate."
            - "SEO strategies must evolve with algorithm changes to stay competitive."
            """,
            unsafe_allow_html=True
        )

        if "li_generating" not in st.session_state:
            st.session_state.li_generating = False

        li_clicked = st.button("Generate LinkedIn Post", disabled=st.session_state.li_generating)
        if li_clicked:
            if not topic.strip() or not insight.strip():
                st.error("Please provide both a content topic and a professional insight.")
            else:
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
                        st.session_state.li_last_output = {
                            "linkedin_post": regen_data["content"],
                            "output_id": regen_data["output_id"],
                            "validation_passed": regen_data.get("validation_passed", True)
                        }
                        st.success("Regenerated!")
                        if hasattr(st, "rerun"):
                            st.rerun()
                        elif hasattr(st, "experimental_rerun"):
                            st.experimental_rerun()
                    else:
                        st.error(regen_resp.json().get("detail", "Error"))

# Tab 3 – Content Strategy
with choice[3]:
    st.header("🧠 Content Strategy Generator")
    with st.container():
        st.markdown("**Generate a comprehensive content strategy for your brand.**")
        platforms = st.multiselect(
            "Platforms",
            ["instagram", "facebook", "linkedin", "website"],
            help="Select the platforms for your content strategy."
        )
        goals = st.text_area(
            "Content Goals",
            placeholder="e.g., Increase brand awareness, drive traffic, boost engagement",
            help="Specify your marketing goals for the strategy."
        )

        if "strategy_generating" not in st.session_state:
            st.session_state.strategy_generating = False

        strat_clicked = st.button("Generate Strategy", disabled=st.session_state.strategy_generating)
        if strat_clicked:
            if not platforms or not goals.strip():
                st.error("Please select at least one platform and provide content goals.")
            else:
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
    with st.container():
        st.markdown("**Plan a week of content to maximize engagement and SEO.**")
        summary = st.text_area(
            "Brand Summary",
            placeholder="e.g., A tech startup offering AI-driven marketing tools.",
            help="Provide a brief summary of your brand."
        )
        topics = st.text_input(
            "Comma-separated Topic List",
            placeholder="e.g., SEO Basics, Product Demo, Industry Trends",
            help="Enter topics for the content calendar, separated by commas."
        )

        if "calendar_generating" not in st.session_state:
            st.session_state.calendar_generating = False

        cal_clicked = st.button("Generate Calendar", disabled=st.session_state.calendar_generating)
        if cal_clicked:
            if not summary.strip() or not topics.strip():
                st.error("Please provide a brand summary and topic list.")
            else:
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
    with st.container():
        st.markdown("**Provide feedback or regenerate content using an Output ID.**")
        with st.form("feedback_form"):
            output_id = st.text_input("Output ID", placeholder="Enter the Output ID", help="Enter the ID of the generated content.")
            rating = st.slider("Rating", 1, 5, 4, help="Rate the content from 1 to 5.")
            comment = st.text_area("Comment", placeholder="e.g., Great post, but needs more specific examples.", help="Provide feedback on the generated content.")
            likes = st.number_input("Likes", min_value=0, help="Enter the number of likes for engagement metrics.")
            submitted = st.form_submit_button("Submit Feedback")
            if submitted:
                if not output_id.strip():
                    st.error("Please provide an Output ID.")
                else:
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
        regen_id = st.text_input("Regenerate from Output ID", placeholder="Enter the Output ID to regenerate", help="Enter the ID of the content to regenerate.")
        if st.button("Regenerate"):
            if not regen_id.strip():
                st.error("Please provide an Output ID.")
            else:
                r = requests.post(f"{API_URL}/regenerate_output/", json={"output_id": regen_id})
                if r.ok:
                    data = r.json()
                    st.success("Regenerated!")
                    st.text_area("New Content", data["content"], height=200)
                    st.write("New Output ID:", data["output_id"])
                else:
                    st.error(r.json().get("detail", "Error"))