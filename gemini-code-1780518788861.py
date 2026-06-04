import streamlit as st
from google import genai
from google.genai import types

# -------------------------------------------------------------
# 1. Authentic Minimalist Identity (Editorial / Matcha Vibe)
# -------------------------------------------------------------
st.set_page_config(
    page_title="Upfound Content Studio", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* Import clean typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');
    
    /* Hide Streamlit Default Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global Warm Minimalist Background */
    .stApp {
        background-color: #F9F8F6;
        color: #2D2D2D;
        font-family: 'Inter', sans-serif;
    }
    
    /* Editorial Header */
    .studio-header {
        font-family: 'Playfair Display', serif;
        font-size: 2.8rem;
        font-weight: 600;
        color: #1A1A1A;
        margin-top: 2rem;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }
    .studio-tagline {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #666666;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 4rem;
    }
    
    /* Clean Input Styling */
    div.stSelectbox > label, div.stTextArea > label {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #555555 !important;
        margin-bottom: 0.5rem;
    }
    
    /* White inputs with subtle borders */
    div.stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E2E2 !important;
        border-radius: 2px !important;
    }
    
    textarea {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E2E2 !important;
        border-radius: 2px !important;
        color: #2D2D2D !important;
        padding: 1rem !important;
    }
    textarea:focus {
        border-color: #8A9A86 !important;
        box-shadow: none !important;
    }

    /* Signature Action Button - Matcha Green */
    .stButton>button {
        background-color: #8A9A86;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.9rem;
        letter-spacing: 1.5px;
        border-radius: 2px;
        border: none;
        padding: 0.8rem 0;
        margin-top: 1.5rem;
        text-transform: uppercase;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #72826F;
        color: #FFFFFF;
    }

    /* Content Output Canvas */
    .output-frame {
        background-color: #FFFFFF;
        border: 1px solid #EAEAEA;
        border-left: 4px solid #8A9A86;
        padding: 3rem;
        border-radius: 2px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
        margin-top: 1.5rem;
    }
    
    /* Markdown Text Formatting inside Output */
    .output-frame h3 {
        font-family: 'Playfair Display', serif;
        color: #1A1A1A;
        margin-top: 0;
    }
    .output-frame h4 {
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 1px;
        color: #8A9A86;
        margin-top: 2rem;
    }
    
    .studio-footer {
        margin-top: 6rem;
        font-size: 0.7rem;
        color: #999999;
        text-align: center;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. System Prompt Logic
# -------------------------------------------------------------
SYSTEM_PROMPT = """
You are the elite Content Architect for Upfound. Your aesthetic is completely minimalist, but your message embraces the raw, unfiltered chaos of startup culture. 

Strict Content Rules:
1. No Walls of Text: Never write more than two sentences together. Separate ideas cleanly using line breaks.
2. Human Directness: Drop complex technical jargon. Frame real-world situations vividly ("fixing a production crash at 3 AM").
3. Rapid Hooks: Keep initial visual hooks under 10 words. They must puncture a real frustration instantly.

Output Format Requirement:
### 🎬 Concept: [Punchy Title]
**Target:** [Talent / Founder] | **Format:** [Reel Script / Slide Carousel]

#### 👁️ Visual & Vibe Direction
[Describe the raw camera motion, simple text overlays, or sparse spatial composition.]

#### 🧲 The Hook (First 3 Seconds)
"[Under 10 words, high-impact text]"

#### 📝 Script Blueprint
[Line-by-line breakdown. Brief, fast-paced dialogue or layout instructions.]
"""

# -------------------------------------------------------------
# 3. UI Layout & Execution
# -------------------------------------------------------------
st.markdown('<div class="studio-header">Upfound Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="studio-tagline">Content Architecture // Minimalist Chaos</div>', unsafe_allow_html=True)

# Clean, asymmetric layout
col_controls, col_canvas = st.columns([4, 6], gap="large")

with col_controls:
    st.selectbox(
        "Audience Trajectory",
        ["Talent Focus (60% Weight) — Core Skills, Bypassing Legacy Filters", 
         "Founder Focus (40% Weight) — Direct Sourcing, Cutting Corporate Noise"],
        key="audience"
    )
    
    st.selectbox(
        "Production Frame",
        ["Low Energy — Handheld Content Studio (Single-Take 15s Raw Reel)",
         "Medium Energy — Core Asset Highlight Translation",
         "High Energy — Comprehensive Conceptual Slide Carousel"],
        key="energy"
    )
    
    st.text_area(
        "Raw Cognitive Spark",
        placeholder="Drop any incomplete thoughts here...",
        height=140,
        key="spark"
    )
    
    generate_btn = st.button("Generate Blueprint")

with col_canvas:
    if generate_btn:
        with st.spinner("Curating narrative..."):
            try:
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                
                user_prompt = f"""
                Construct a high-retention concept using these exact boundaries:
                Target Lens: {st.session_state.audience}
                Intensity Profile: {st.session_state.energy}
                Context Clutter: {st.session_state.spark if st.session_state.spark else "Wildcard execution. Deliver an unexpected, highly disruptive premise."}
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.88,
                    )
                )
                
                # Render the clean output frame
                st.markdown(f'<div class="output-frame">{response.text}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"System sync error: {e}")
    else:
        # Default empty state that blends into the background nicely
        st.markdown(
            '<div style="border: 1px solid #EAEAEA; border-radius: 2px; padding: 4rem; text-align: center; color: #999999; font-family: \'Inter\', sans-serif; text-transform: uppercase; letter-spacing: 2px; font-size: 0.75rem; background-color: #FFFFFF; margin-top: 1.5rem;">'
            'Canvas is blank. Awaiting seed input.'
            '</div>', 
            unsafe_allow_html=True
        )

st.markdown('<div class="studio-footer">Designed for Upfound // Powered by Gemini</div>', unsafe_allow_html=True)
