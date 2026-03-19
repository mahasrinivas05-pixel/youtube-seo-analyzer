import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seo_engine as seo  # Importing your backend functions

# --- Page Configuration ---
st.set_page_config(page_title="AI YouTube SEO Analyzer", layout="wide")

# --- Custom Header ---
st.title("📹 AI Powered YouTube SEO Analyzer")
st.markdown("### *For Beginner Creators to Master the Algorithm*")
st.divider()

# --- Input Section ---
with st.container():
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📋 Video Details")
        title_input = st.text_input("Video Title", placeholder="Enter your title here...")
        desc_input = st.text_area("Video Description", placeholder="Enter your description...", height=150)
        
    with col2:
        st.header("🔑 SEO Keywords")
        k_input = st.text_area("Target Keywords (comma separated)", 
                               placeholder="Enter at least 5 keywords...", 
                               help="Keywords help the AI understand your niche.")
        analyze_btn = st.button("🚀 Analyze & Optimize")

# --- Processing Logic ---
if analyze_btn:
    # Convert input string to list
    keywords = [k.strip() for k in k_input.split(",") if k.strip()]
    
    if len(keywords) < 5:
        st.error("⚠️ Please enter at least 5 keywords for an accurate analysis.")
    elif not title_input or not desc_input:
        st.warning("⚠️ Please provide both a title and a description.")
    else:
        # 1. Call Backend Functions
        results, feedback, reach, power_words = seo.vid_iq_checker(title_input, desc_input, keywords)
        ctr = seo.calculate_ctr(title_input)
        viral = seo.viral_score(title_input, ctr, reach)
        
        # 2. Optimization Logic
        best_title, best_score = seo.optimize_title(keywords, power_words, title_input, reach)
        
        # 3. Trends and Recommendations
        trends = seo.find_youtube_trends(keywords)
        recs = seo.title_recommender(keywords, power_words)

        # --- Display Metrics ---
        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric("SEO Reach", f"{reach}%")
        m2.metric("Predicted CTR", f"{ctr}%")
        m3.metric("Viral Score", f"{viral}/100")

        # --- Optimization Result ---
        st.success(f"### 🎯 Best Optimized Title: **{best_title}**")
        st.write(f"**Optimization Viral Score:** {best_score}/100")

        # --- Visualizations ---
        st.divider()
        vis_col1, vis_col2 = st.columns(2)

        with vis_col1:
            st.subheader("📊 SEO Score Breakdown")
            # Creating Plotly Bar Chart
            fig = px.bar(
                x=list(results.values()), 
                y=list(results.keys()), 
                orientation='h',
                labels={'x': 'Score (out of 20)', 'y': 'Metric'},
                color=list(results.values()),
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)

        with vis_col2:
            st.subheader("☁️ Keyword Word Cloud")
            # Creating Word Cloud using Matplotlib
            word_string = " ".join(keywords)
            wc = WordCloud(width=800, height=400, background_color='white', colormap='Reds').generate(word_string)
            
            fig_wc, ax = plt.subplots()
            ax.imshow(wc, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig_wc)

        # --- Suggestions & Content Ideas ---
        st.divider()
        inf_col1, inf_col2 = st.columns(2)

        with inf_col1:
            st.subheader("💡 Improvement Suggestions")
            for item in feedback:
                st.write(f"- {item}")
            
            st.subheader("🔥 Recommended Titles")
            for r in recs:
                st.code(r)

        with inf_col2:
            st.subheader("📈 Trending Topics (Velocity)")
            # Display Trends
            for t in trends:
                st.write(f"**{t['topic']}**")
                st.progress(t['velocity'] / 100)
                st.caption(f"Velocity: {t['velocity']}%")

else:
    st.info("Fill in your video details and click 'Analyze' to begin.")