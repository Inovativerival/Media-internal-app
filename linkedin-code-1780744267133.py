import streamlit as st
from google import genai
from google.genai import types

# -------------------------------------------------------------
# 1. Authentic Minimalist Identity (The Writer's Canvas)
# -------------------------------------------------------------
st.set_page_config(
    page_title="Upfound Editorial Blueprint", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');
    
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
        margin-bottom: 3.5rem;
    }
    
    /* Clean Input Styling */
    div.stSelectbox > label, div.stTextArea > label, div.stTextInput > label {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #555555 !important;
        margin-bottom: 0.5rem;
    }
    
    input, textarea, div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E2E2 !important;
        border-radius: 2px !important;
        color: #2D2D2D !important;
    }
    textarea:focus, input:focus {
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
        margin-top: 1rem;
        text-transform: uppercase;
        transition: background-color 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #72826F;
        color: #FFFFFF;
    }

    /* Content Output Canvas */
    .output-frame {
        background-color: #FFFFFF;
        border: 1px solid #EAEAEA;
        border-top: 4px solid #8A9A86;
        padding: 3.5rem;
        border-radius: 2px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
    }
    
    .output-frame h3 {
        font-family: 'Playfair Display', serif;
        color: #1A1A1A;
        margin-top: 0;
        border-bottom: 1px solid #EAEAEA;
        padding-bottom: 1rem;
    }
    .output-frame h4 {
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 1.5px;
        color: #8A9A86;
        margin-top: 2.5rem;
    }
    .output-frame li {
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. The Semantic Brain (System Instructions)
# -------------------------------------------------------------
SYSTEM_PROMPT = """
You are the elite LinkedIn SEO Architect for Upfound. Your job is to empower the human writer by providing a "Semantic Blueprint." Do NOT write the entire article for her. 

Upfound connects raw, Tier 2/3 talent with startups, bypassing legacy ATS filters and pedigree bias. 

Analyze the user's input and strictly output this Markdown blueprint:

### 📐 The Semantic Blueprint
**Topic:** [Restate the core theme in 5 words]

#### 🎯 The Narrative Angle
[Provide a 2-sentence emotional angle. What is the unspoken frustration here? E.g., "The pain of being ghosted because of a zip code, while founders bleed money searching for talent."]

#### 🧲 Scroll-Stopping Hooks (Choose One)
[Provide 3 highly disruptive, 1-2 sentence opening hooks designed to force the user to click "...see more". No generic greetings.]
1. 
2. 
3. 

#### 🧠 The "Grit" Lexicon (Semantic SEO)
[Provide 5-7 LSI keywords or phrases to weave naturally into the body. Do NOT use generic tags like #Hiring. Use authoritative terms like "legacy ATS tracking", "pedigree bias", "execution grit", "technical latency".]

#### 🏗️ Structural Pacing
- **The Agitation:** [How to introduce the problem]
- **The Industry Myth:** [What is the corporate world doing wrong here?]
- **The Upfound Reality:** [How we solve it without sounding like an ad]

#### ⚡ High-Conversion CTA
[Write a 1-sentence call-to-action directing users strictly to the Upfound platform or AI Profile Score. Do not suggest emailing an admin or support address.]
"""

# -------------------------------------------------------------
# 3. Application Interface
# -------------------------------------------------------------
st.markdown('<div class="studio-header">Editorial Blueprint</div>', unsafe_allow_html=True)
st.markdown('<div class="studio-tagline">Upfound Semantic Architect // LinkedIn Strategy</div>', unsafe_allow_html=True)

col_input, col_canvas = st.columns([4, 6], gap="large")

with col_input:
    st.text_input(
        "The Core Subject",
        placeholder="e.g., Why traditional resumes are failing startups...",
        key="topic"
    )
    
    st.selectbox(
        "Content Objective",
        ["Pain-Point Agitation (Exposing a broken system)", 
         "Thought Leadership (Educating the market)",
         "Platform Integration (Highlighting AI Profile Score / Features)"],
        key="objective"
    )
    
    st.text_area(
        "Raw Brain Dump (Optional)",
        placeholder="Paste rough notes, unfinished sentences, or competitor links here. The engine will synthesize it.",
        height=180,
        key="dump"
    )
    
    generate_btn = st.button("Generate Strategy Blueprint")

with col_canvas:
    if generate_btn and st.session_state.topic:
        with st.spinner("Extracting semantic lexicon and mapping narrative..."):
            try:
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                
                user_prompt = f"""
                Analyze this data and create a LinkedIn Semantic Blueprint:
                Subject: {st.session_state.topic}
                Objective: {st.session_state.objective}
                Raw Notes/Context: {st.session_state.dump if st.session_state.dump else "No raw notes provided. Generate based on subject."}
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.75, # Slightly lower temperature for tighter SEO relevance
                    )
                )
                
                st.markdown(f'<div class="output-frame">{response.text}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Engine sync failure: {e}")
    elif generate_btn and not st.session_state.topic:
        st.warning("Please enter a Core Subject to begin.")
    else:
        st.markdown(
            '<div style="border: 1px solid #EAEAEA; border-radius: 2px; padding: 4rem; text-align: center; color: #999999; font-family: \'Inter\', sans-serif; text-transform: uppercase; letter-spacing: 2px; font-size: 0.75rem; background-color: #FFFFFF;">'
            'Workspace is empty. Waiting for seed topic.'
            '</div>', 
            unsafe_allow_html=True
        )