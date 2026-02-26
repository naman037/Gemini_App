import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# --- 1. OPEN THE VAULT ---
# This reads the hidden .env file on your computer
load_dotenv()

# Grab the key from the vault (or from Streamlit Cloud's secrets)
GEMINI_API_KEY = os.getenv(GEMINI_API_KEY)

# --- 2. CONNECT TO GEMINI ---
client = genai.Client(api_key=GEMINI_API_KEY)

# --- 3. BUILD THE UI ---
st.title("🧠 Gemini-Powered Fact Checker")
st.write("Paste a news headline or full article below. Gemini will analyze the context, check for clickbait, and give a verdict!")

user_text = st.text_area("Enter News Text Here:", height=150)

if st.button("Analyze with Gemini"):
    if user_text:
        st.info("Gemini is analyzing the context... 🕵️‍♂️")
        
        try:
            # --- 4. PROMPT ENGINEERING ---
            system_instructions = """
            You are an elite fact-checker and journalist. 
            Analyze the user's news text. 
            Respond strictly in this format:
            VERDICT: [REAL or FAKE]
            CONFIDENCE: [Your confidence percentage]
            REASONING: [Exactly 2 sentences explaining why it seems real or fake based on language, tone, and logic.]
            """
            
            prompt = f"{system_instructions}\n\nHere is the news text:\n{user_text}"
            
            # --- 5. CALL THE API ---
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.3) 
            )
            
            # --- 6. DISPLAY THE RESULT ---
            st.success("Analysis Complete!")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please enter some text first!")