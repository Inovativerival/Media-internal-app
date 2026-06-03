import streamlit as st
from google import genai
from google.genai import types

# -------------------------------------------------------------
# 1. Premium Visual Identity & Custom CSS
# -------------------------------------------------------------
st.set_page_config(page_title="Upfound Content Studio", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Global Typography & Background Override */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&family=Space+Grotesk:wght@400;600&display=swap');
    
    .stApp {
        background-color: #0B0D11;
        color: #E2E8F0;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Elegant Header Branding */
    .brand-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 600;
        letter-spacing: -1px;
        color: #FAFAFA;
        margin-bottom: 0.2rem;
    }
    .brand-subtitle {
        font-size: 0.95rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 2rem;
    }
    
    /* Input Form Customization */
    div.stSelectbox > label, div.stTextArea > label {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #94A3B8 !important;
        margin-bottom: 0.5rem;
    }
    
    div.stSelectbox div[data-baseweb="select"] {
        background-color: #131720 !important;
        border: 1px solid #1E293B !important;
        border-radius: 6px !important;
    }
    
    textarea {
        background-color: #131720 !important;
        border: 1px solid #1E293B !important;
        border-radius: 6px !important;
        color: #E2E8F0 !important;
    }

    /* The Master Action Button - Earthy Matcha Accent */
    .stButton>button {
        background: linear-gradient(135deg, #7A9A77 0%, #638260 100%);
        color: #0B0D11;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 1px;
        border-radius: 6px;
        border: none;
        padding: 0.75rem 0;
        margin-top: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(107, 138, 104, 0.15);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #8BA888 0%, #7A9A77 100%);
        box-shadow: 0 6px 20px rgba(107, 138, 104, 0.3);
        transform: translateY(-1px);
        color: #0B0D11;
    }

    /* Premium Output Canvas */
    .output-canvas {
        background-color: #121620;
        border: 1px solid #1E293B;
        border-left: 3px solid #7A9A77;
        padding: 2.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
    }
    
    .signature-footer {
        margin-top: 4rem;
        font-size: 0.75rem;
        color: #475569;
        text-align: center;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. Back-End Core Architecture
# -------------------------------------------------------------
SYSTEM_PROMPT = """
You are the elite Content Architect for Upfound. Your aesthetic is minimalist, but your message embraces the raw, unfiltered chaos of startup culture. 

Strict Formatting & Writing Rules:
1. Ban Paragraphs: Never write more than two sentences in a row. Break text into single, powerful lines.
2. Cut the Tech Jargon: Speak in plain, high-stakes human terms ("fixing a 2 AM crash").
3. Micro-Hooks: The first 3 seconds must be under 10 words. It must attack a specific pain point immediately.

Output Schema:
### 🎬 Concept: [Punchy Title]
**Target:** [Talent / Founder] | **Format:** [Reel Script / Slide Carousel]

#### 👁️ Visual & Vibe Direction
[Describe the raw aesthetic, camera movement, or minimalist frame composition.]

#### 🧲 The Hook (First 3 Seconds)
"[Under 10 words, bold visual text]"

#### 📝 The Script / Slide Blueprint
[Write line-by-line, short sentences only with explicit line breaks.]
"""

# -------------------------------------------------------------
# 3. Application Layout
# -------------------------------------------------------------
st.markdown('<div class="brand-title">UPFOUND // RAW STUDIO</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-subtitle">The Content Scaffold — Built for the Lazy Days</div>', unsafe_allow_html=True)

# Split screen workspace
col_panel, col_canvas = st.columns([5, 7], gap="large")

with col_panel:
    st.selectbox(
        "Audience Target Matrix",
        ["Talent (60% Weighting) — Core Skills, Bypassing Gatekeepers", 
         "Founders (40% Weighting) — The True Cost of Bad Hiring Noise"],
        key="audience"
    )
    
    st.selectbox(
        "Energy State & Output Architecture",
        ["Low Effort — Walking Content Studio (Raw 15s Single-Take Reel)",
         "Medium Effort — Feature Spotlight Translation",
         "High Effort — Full Macro-Narrative Creative Carousel"],
        key="energy"
    )
    
    st.text_area(
        "Raw Seed Context (Stream of Consciousness Input)",
        placeholder="Type whatever clutter is in your head... or leave empty for a wildcard spark.",
        height=140,
        key="spark"
    )
    
    generate_btn = st.button("✨ FORGE FRESH STORYBOARD")

with col_canvas:
    if generate_btn:
        with st.spinner("Decoding system data and injecting vibe..."):
            try:
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                
                user_prompt = f"""
                Generate an entirely unique content concept based on these parameters:
                Target Audience Context: {st.session_state.audience}
                Energy/Format Profile: {st.session_state.energy}
                Seed Fragment: {st.session_state.spark if st.session_state.spark else "Wildcard request. Surprise me with a highly disruptive idea."}
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        # Temperature ensures infinite creative variance
                        temperature=0.85,
                    )
                )
                
                st.markdown('<div class="output-canvas">', unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Engine connection failure: {e}")
    else:
        st.markdown(
            '<div style="border: 1px dashed #1E293B; border-radius: 12px; padding: 3rem; text-align: center; color: #475569; font-family: \'Space Grotesk\', sans-serif; text-transform: uppercase; letter-spacing: 1px;">'
            'Canvas Idle. Awaiting Parameter Execution.'
            '</div>', 
            unsafe_allow_html=True
        )

st.markdown('<div class="signature-footer">Designed with Passion // Powered by Gemini 2.5 Flash</div>', unsafe_allow_html=True)