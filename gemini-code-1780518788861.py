import streamlit as st
from google import genai
from google.genai import types

# -------------------------------------------------------------
# 1. Signature Visual Persona & Spatial CSS
# -------------------------------------------------------------
st.set_page_config(
    page_title="Upfound Content Studio", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500&family=Space+Grotesk:wght@400;500;600&display=swap');
    
    /* Studio Background & Canvas Definition */
    .stApp {
        background-color: #0A0C10;
        color: #E2E8F0;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Header Branding Elements */
    .studio-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 500;
        letter-spacing: -1px;
        color: #FFFFFF;
        margin-top: 1rem;
        margin-bottom: 0.1rem;
    }
    .studio-tagline {
        font-size: 0.8rem;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 3rem;
    }
    
    /* Form Element Subversion */
    div.stSelectbox > label, div.stTextArea > label {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #64748B !important;
        margin-bottom: 0.6rem;
    }
    
    div.stSelectbox div[data-baseweb="select"] {
        background-color: #11141D !important;
        border: 1px solid #1E293B !important;
        border-radius: 4px !important;
        padding: 0.2rem 0;
    }
    
    textarea {
        background-color: #11141D !important;
        border: 1px solid #1E293B !important;
        border-radius: 4px !important;
        color: #E2E8F0 !important;
    }

    /* Action Button - Organic Sage/Matcha Spectrum */
    .stButton>button {
        background: linear-gradient(135deg, #748A71 0%, #5C6E59 100%);
        color: #0A0C10;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 0.9rem;
        letter-spacing: 2px;
        border-radius: 4px;
        border: none;
        padding: 0.8rem 0;
        margin-top: 1.8rem;
        text-transform: uppercase;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: 0 4px 20px rgba(116, 138, 113, 0.1);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #859D82 0%, #748A71 100%);
        box-shadow: 0 6px 24px rgba(116, 138, 113, 0.25);
        transform: translateY(-1px);
        color: #0A0C10;
    }

    /* Premium Content Block Framework */
    .output-frame {
        background-color: #11141D;
        border: 1px solid #1E293B;
        border-top: 2px solid #748A71;
        padding: 2.5rem;
        border-radius: 8px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    }
    
    /* Custom Scrollbar for Studio Aesthetics */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0A0C10;
    }
    ::-webkit-scrollbar-thumb {
        background: #1E293B;
        border-radius: 3px;
    }
    
    .studio-footer {
        margin-top: 6rem;
        font-size: 0.7rem;
        color: #334155;
        text-align: center;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. Re-Engineered Prompt Protocol
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
# 3. Workspace Presentation
# -------------------------------------------------------------
st.markdown('<div class="studio-header">UPFOUND // RAW STUDIO</div>', unsafe_allow_html=True)
st.markdown('<div class="studio-tagline">Content Architecture Ecosystem</div>', unsafe_allow_html=True)

# Asymmetric workspace configuration
col_controls, col_canvas = st.columns([5, 7], gap="large")

with col_controls:
    st.selectbox(
        "Audience Trajectory",
        ["Talent Focus (60% Weighting) — Core Competence, Bypassing Legacy Filters", 
         "Founder Focus (40% Weighting) — Direct Sourcing, Cutting Corporate Noise"],
        key="audience"
    )
    
    st.selectbox(
        "Production Frame & Intensity",
        ["Low Energy — Handheld Content Studio (Single-Take 15s Raw Reel)",
         "Medium Energy — Core Asset Highlight Translation",
         "High Energy — Comprehensive Conceptual Slide Carousel"],
        key="energy"
    )
    
    st.text_area(
        "Raw Cognitive Spark (Context Fragment)",
        placeholder="Drop any incomplete thoughts here, or leave completely blank for a wildcard prompt...",
        height=160,
        key="spark"
    )
    
    generate_btn = st.button("Generate Blueprint")

with col_canvas:
    if generate_btn:
        with st.spinner("Compiling narrative layers..."):
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
                
                st.markdown('<div class="output-frame">', unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"System sync error: {e}")
    else:
        st.markdown(
            '<div style="border: 1px dashed #1E293B; border-radius: 8px; padding: 4.5rem; text-align: center; color: #334155; font-family: \'Space Grotesk\', sans-serif; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem;">'
            'Studio Console Idle. Awaiting Parameter Entry.'
            '</div>', 
            unsafe_allow_html=True
        )

st.markdown('<div class="studio-footer">Artisanal Content Engine // Powered by Gemini 2.5 Flash</div>', unsafe_allow_html=True)