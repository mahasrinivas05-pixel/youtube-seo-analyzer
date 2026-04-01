# main.py

import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

# Load local .env only if it exists (for your laptop)
load_dotenv()

def generate_ai_content(concept, keywords, title, description):
    # This line pulls the key directly from the Streamlit "Secrets" box
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except:
        # Fallback for local testing on your laptop
        api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a YouTube SEO + Content Expert.

INPUT:
Concept of Video: {concept}
Keywords: {keywords}
Current Title: {title}
Current Description: {description}

YOUR TASK:
1. Improve the content (DO NOT keyword stuff)
2. Generate 3 BETTER titles (40–60 chars, curiosity + hook)
3. Generate 1 optimized description (250–350 chars)
4. Add hashtags at the end

STRICT FORMAT:
Title 1: ...
Title 2: ...
Title 3: ...

Description:
...

Hashtags:
...
"""

    # CRITICAL: Changed model to gemini-1.5-flash so it doesn't crash
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
    )

    return response.text
