import streamlit as st
from google import genai
from google.genai import types

# --- 1. CONNECT TO GEMINI ---
# Replace with your actual Gemini API key from Google AI Studio
GEMINI_API_KEY = "AIzaSyBTQ3ea5Vl0_65_taNO8_h_HTl9W4ZEoUA" 

client = genai.Client(api_key=GEMINI_API_KEY)

# --- 2. BUILD THE UI ---
st.title("🧠 Gemini-Powered Fact Checker")
st.write("Paste a news headline or full article below. Gemini will analyze the context, check for clickbait, and give a verdict!")

user_text = st.text_area("Enter News Text Here:", height=150)

if st.button("Analyze with Gemini"):
    if user_text:
        st.info("Gemini is analyzing the context... 🕵️‍♂️")
        
        try:
            # --- 3. THE "PROMPT ENGINEERING" ---
            # We program Gemini's persona here
            system_instructions = """
            You are an elite fact-checker and journalist. 
            Analyze the user's news text. 
            Respond strictly in this format:
            VERDICT: [REAL or FAKE]
            CONFIDENCE: [Your confidence percentage]
            REASONING: [Exactly 2 sentences explaining why it seems real or fake based on language, tone, and logic.]
            """
            
            # Combine instructions and user text 
            prompt = f"{system_instructions}\n\nHere is the news text:\n{user_text}"
            
            # --- 4. CALL THE API ---
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                # Low temperature keeps the AI logical and strict, not creative
                config=types.GenerateContentConfig(temperature=0.3) 
            )
            
            # --- 5. DISPLAY THE RESULT ---
            st.success("Analysis Complete!")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please enter some text first!")