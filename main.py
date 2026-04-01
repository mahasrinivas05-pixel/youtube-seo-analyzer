import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

# 1. Load local .env only if it exists (for your laptop/VS Code)
load_dotenv()

def generate_ai_content(concept, keywords, title, description):
    """
    Fetches the API key from Streamlit Secrets or Environment Variables
    and generates YouTube SEO content using Gemini 1.5 Flash.
    """
    
    # 2. Key Selection Logic (Prioritizes Streamlit Secrets for the Website)
    api_key = None
    
    if "GEMINI_API_KEY" in st.secrets:
        # Use this when running on the Streamlit Cloud website
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        # Use this when running locally in VS Code (from .env or System)
        api_key = os.getenv("GEMINI_API_KEY")

    # 3. Validation: Stop if no key is found
    if not api_key:
        return "❌ ERROR: No API Key found. Please add 'GEMINI_API_KEY' to your Streamlit Secrets dashboard."

    try:
        # 4. Initialize the New Google GenAI Client
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

        # 5. Generate the content using the faster Flash model
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
        )

        return response.text

    except Exception as e:
        # Catch errors like "Invalid API Key" or "Quota Exceeded"
        return f"⚠️ An error occurred with the AI: {str(e)}"
