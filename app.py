import streamlit as st
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# --- 1. IMPORT YOUR ORIGINAL LOGIC ---
try:
    from main import generate_ai_content
    from code import calculate_score, show_charts, parse_ai_output
except ImportError:
    st.error("Make sure main.py and code.py are in the same folder!")

load_dotenv()

# --- 2. PROFESSIONAL PAGE CONFIG ---
st.set_page_config(
    page_title="ViralVision SEO Pro", 
    page_icon="🎬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a Professional Dashboard Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        color: #ff4b4b;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        border: none;
    }
    div.stMetric {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR BRANDING & INPUTS ---
with st.sidebar:
    st.title("🎬 ViralVision AI")
    st.subheader("YouTube SEO Dashboard")
    st.markdown("---")
    
    u_concept = st.text_input("Video Concept", placeholder="e.g. How to Bake a Cake")
    u_keywords = st.text_area("Keywords (comma separated)", placeholder="recipe, baking, dessert")
    u_title = st.text_input("Current Title")
    u_desc = st.text_area("Current Description", height=100)
    
    st.markdown("---")
    analyze_btn = st.button("🚀 ANALYZE & OPTIMIZE")

# --- 4. MAIN DASHBOARD ---
if not analyze_btn:
    st.title("Welcome to ViralVision Pro")
    st.markdown("### Elevate your YouTube Content with AI-Driven SEO.")
    st.info("👈 Enter your video details on the left to generate your Optimization Report.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 📊 SEO Scoring")
        st.write("Instant feedback on your current metadata using your custom scoring algorithm.")
    with c2:
        st.markdown("### 🤖 AI Brainstorming")
        st.write("Generates high-CTR titles and story-driven descriptions using Gemini.")
    with c3:
        st.markdown("### 📥 One-Click Reports")
        st.write("Export your optimized metadata directly to a report file.")

else:
    # --- PHASE A: ANALYSIS (From code.py) ---
    result = calculate_score(u_keywords, u_title, u_desc)
    
    st.title("📈 SEO Performance Analysis")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Overall Score", f"{result['Final Score']}/100")
    with m2: st.metric("Title SEO", f"{result['Title Score']}/30")
    with m3: st.metric("Hook Strength", f"{result['Hook Score']}/20")
    with m4: st.metric("Curiosity Gap", f"{result['Curiosity Score']}/20")

    col_chart, col_ai = st.columns([1, 1.5], gap="large")
    
    with col_chart:
        st.subheader("Detailed Breakdown")
        show_charts(result)
        st.pyplot(plt.gcf())
        plt.clf()

    # --- PHASE B: AI OPTIMIZATION & REPORT ---
    with col_ai:
        st.subheader("⚡ AI Optimized Content")
        with st.spinner("AI is crafting your viral metadata..."):
            ai_output = generate_ai_content(u_concept, u_keywords, u_title, u_desc)
            
            if ai_output:
                titles, ai_desc, hashtags = parse_ai_output(ai_output)
                
                # Display Results
                tab1, tab2, tab3 = st.tabs(["Option 1", "Option 2", "Option 3"])
                for i, t in enumerate(titles[:3]):
                    if i == 0: tab1.success(f"**Suggested Title:**\n\n{t}")
                    if i == 1: tab2.success(f"**Suggested Title:**\n\n{t}")
                    if i == 2: tab3.success(f"**Suggested Title:**\n\n{t}")

                st.markdown("#### ✨ Optimized Description")
                st.info(ai_desc if ai_desc else "Description generation failed.")
                
                st.markdown("#### #️⃣ Generated Hashtags")
                st.code(hashtags if hashtags else "#youtube #seo #viral")

                # --- 5. REPORT GENERATION SECTION ---
                st.divider()
                st.subheader("📄 Export Your SEO Report")
                
                # Create the report content string
                full_report = f"""
VIRALVISION SEO OPTIMIZATION REPORT
===================================
VIDEO CONCEPT: {u_concept}
FINAL SEO SCORE: {result['Final Score']}/100

SCORES BREAKDOWN:
- Title Score: {result['Title Score']}/30
- Description Score: {result['Description Score']}/30
- Hook Score: {result['Hook Score']}/20
- Curiosity Score: {result['Curiosity Score']}/20

AI SUGGESTED TITLES:
-------------------
{chr(10).join(titles)}

OPTIMIZED DESCRIPTION:
----------------------
{ai_desc}

RECOMMENDED HASHTAGS:
---------------------
{hashtags}
                """
                
                # The actual download button
                st.download_button(
                    label="📥 Download Full SEO Report (.txt)",
                    data=full_report,
                    file_name=f"SEO_Report_{u_concept.replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key="report_download_final"
                )
            else:
                st.error("AI failed to generate content. Please check your API key.")
