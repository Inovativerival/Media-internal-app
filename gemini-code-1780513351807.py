import streamlit as st
from google import genai
from google.genai import types

# -------------------------------------------------------------
# 1. UI & Aesthetic Configuration (Minimalist & Clean)
# -------------------------------------------------------------
st.set_page_config(page_title="Upfound Content Scaffold", layout="wide")

# Custom CSS for a clean, distraction-free UI with subtle matcha green accents
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stButton>button {
        background-color: #8BA888; /* Matcha Green */
        color: #0E1117;
        font-weight: bold;
        border-radius: 4px;
        border: none;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #A3C4A0;
        color: #0E1117;
    }
    .output-card {
        background-color: #161A22;
        padding: 2rem;
        border-radius: 8px;
        border-left: 4px solid #8BA888;
        font-family: 'Courier New', Courier, monospace;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. System Instructions (The Minimalist Chaos Brain)
# -------------------------------------------------------------
SYSTEM_PROMPT = """
You are the elite Content Architect for Upfound. Your aesthetic is minimalist, but your message embraces the raw, unfiltered chaos of startup culture. 

Strict Formatting & Writing Rules:
1. Ban Paragraphs: Never write more than two sentences in a row. 
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
[Write line-by-line, short sentences only.]
"""

# -------------------------------------------------------------
# 3. Streamlit Interface
# -------------------------------------------------------------
st.title("// UPFOUND RAW STUDIO")
st.markdown("Brutally honest, unpolished, zero-fluff content generator.")
st.divider()

# Set up the split layout: Sidebar for controls, Main area for output
col_input, col_output = st.columns([1, 2], gap="large")

with col_input:
    st.subheader("Seed Constraints")
    
    audience = st.selectbox(
        "Who are we talking to?",
        ["Talent (60% Focus - Resume anxiety, skill passport)", 
         "Founders (40% Focus - Hiring mistakes, filtering noise)"]
    )
    
    energy = st.selectbox(
        "Energy Level & Format",
        ["Low Effort: Walking Content Studio (Raw 15s Reel)",
         "Medium Effort: Product Feature Translation",
         "High Effort: Full Narrative Carousel"]
    )
    
    spark = st.text_area(
        "Raw Spark Thought (Optional)",
        placeholder="Drop a messy, unedited thought here..."
    )
    
    generate_btn = st.button("✨ GENERATE CONCEPT")

# -------------------------------------------------------------
# 4. API Logic & Output Display
# -------------------------------------------------------------
with col_output:
    if generate_btn:
        with st.spinner("Forging storyboard..."):
            try:
                # Initialize the new Google GenAI client (Securely pulls API key from Streamlit Secrets)
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                
                # Construct the user prompt based on simple UI selections
                user_prompt = f"""
                Generate a content concept based on these parameters:
                Target Audience: {audience}
                Energy/Format: {energy}
                Seed Idea: {spark if spark else "Create a completely original, high-impact concept based on Upfound's core mission."}
                """
                
                # Generate content using Gemini 2.5 Flash for high speed and low latency
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.7,
                    )
                )
                
                # Display the output cleanly
                st.markdown('<div class="output-card">', unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error connecting to the Vibe Engine: {e}")
    else:
        # Default empty state
        st.info("Set your parameters on the left and generate a raw concept.")