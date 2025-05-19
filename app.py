import streamlit as st
import openai
import os
import subprocess
import uuid
import re
from pathlib import Path

# Page configuration with custom theme
st.set_page_config(
    page_title="AniMAGIC - From Text to Animation",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="auto"
)

# Custom CSS with improved design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #fafbfc;
        color: #1e293b;
    }
    
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif;
        color: #0f172a;
    }
    
    /* Header styling */
    .main h1 {
        text-align: center;
        font-size: 3.2em;
        font-weight: 700;
        padding-top: 0.5em;
        margin-bottom: 0.1em;
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Logo and sparkle animation */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .sparkle {
        display: inline-block;
        animation: sparkle 2s infinite;
        font-size: 1.6em;
        margin: 0 0.2em;
    }
    
    @keyframes sparkle {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.3); opacity: 0.8; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2em;
        color: #64748b;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Card-like container for the main content */
    .content-card {
        background-color: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
    }
    
    /* Input styling */
    .stTextArea label, .stTextInput label {
        font-weight: 600;
        font-size: 1.05em;
        color: #334155;
        margin-bottom: 0.5rem;
    }
    
    .stTextArea textarea {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        padding: 0.8rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        font-family: 'Inter', sans-serif;
    }
    
    .stTextArea textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #4f46e5, #6366f1);
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: 600;
        padding: 0 1.5em;
        border: none;
        box-shadow: 0 2px 5px rgba(99, 102, 241, 0.3);
        transition: all 0.2s ease;
        width: 100%;
        margin-top: 0.5rem;
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #4338ca, #4f46e5);
        box-shadow: 0 4px 8px rgba(99, 102, 241, 0.4);
        transform: translateY(-1px);
    }
    
    .stButton>button:active {
        transform: translateY(1px);
    }
    
    /* Preview section */
    .preview-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        font-weight: 600;
        color: #0f172a;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .preview-icon {
        margin-right: 0.5rem;
        color: #6366f1;
    }
    
    /* Success message */
    .success-banner {
        background-color: #ecfdf5;
        color: #065f46;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #10b981;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    }
    
    .success-icon {
        margin-right: 0.5rem;
        font-size: 1.2em;
    }
    
    /* Code expander */
    .code-expander {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        overflow: hidden;
    }
    
    .code-header {
        background-color: #f8fafc;
        padding: 0.8rem 1rem;
        font-weight: 600;
        color: #334155;
        border-bottom: 1px solid #e2e8f0;
        display: flex;
        align-items: center;
    }
    
    .code-content {
        padding: 1rem;
        background-color: #f1f5f9;
        font-family: monospace;
        font-size: 0.9em;
        overflow-x: auto;
    }
    
    /* Divider */
    .divider {
        border-top: 1px solid #e2e8f0;
        margin: 2rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        font-size: 0.9em;
        color: #64748b;
        margin-top: 3em;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }
    
    .footer-logo {
        font-weight: 600;
        color: #4f46e5;
    }
    
    .heart {
        color: #ef4444;
        animation: heartbeat 1.5s infinite;
    }
    
    @keyframes heartbeat {
        0% { transform: scale(1); }
        25% { transform: scale(1.1); }
        50% { transform: scale(1); }
        75% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    /* Status alerts */
    .alert {
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header with animated sparkles
st.markdown('<div class="logo-container"><span class="sparkle">✨</span><h1>AniMAGIC</h1><span class="sparkle">✨</span></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Turn your imagination into animated math — describe it, watch it!</div>', unsafe_allow_html=True)

# Initialize OpenAI client
OPENAI_API_KEY = 'KEY'  # Replace with your actual key
client = openai.OpenAI(api_key=OPENAI_API_KEY)
temp_dir = Path("temp_manim")
temp_dir.mkdir(exist_ok=True)

# Check for LaTeX
latex_installed = subprocess.run(["which", "latex"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0
if not latex_installed:
    st.warning("⚠️ Note: LaTeX is not available. Using fallback rendering (Text instead of Tex).")

# Main content card
st.markdown('<div class="content-card">', unsafe_allow_html=True)

user_prompt = st.text_area(
    "🔮 Describe your animation idea",
    placeholder="E.g., A red triangle morphs into a blue circle and fades out.",
    height=120
)

# Add some inspiration examples in an expander
with st.expander("💡 Need inspiration? Try these examples"):
    st.markdown("""
    - A particle moving in a circular motion with a trailing path
    - A square transforming into a star shape through a smooth animation
    - A bouncing ball that changes color with each bounce
    """)

generate_col1, generate_col2 = st.columns([3, 1])
with generate_col1:
    generate = st.button("✨ Generate Animation")

st.markdown('</div>', unsafe_allow_html=True)  # Close content card

if generate and user_prompt:
    try:
        with st.spinner("🧠 Interpreting your prompt and creating Manim code..."):
            # GPT prompt retained as requested
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                {"role": "system", "content": """You are a Manim Python expert. Create minimal, working Manim code that imports all necessary libraries and defines a complete Scene class. Provide ONLY the Python code with no explanations, comments, or markdown formatting. Start with the imports directly.

                IMPORTANT: When creating graphs or text, use Text() instead of Tex() or MathTex(), and for axes, set the numbers_with_elongated_ticks=[] to avoid using LaTeX. For any numerical labels, use DecimalNumber with use_plain_tex=True."""},
                {"role": "user", "content": f"Write a minimal, self-contained manim scene for: {user_prompt}. Include all necessary imports. Return ONLY code, no explanations or markdown. IMPORTANT: Do NOT use LaTeX rendering - use Text() instead of Tex() and avoid LaTeX dependencies. For axes, use numbers_with_elongated_ticks=[] to avoid LaTeX rendering issues. Since ShowCreation method is deprecated, replace it with Create method"}
                ],
                temperature=0.7
            )

        manim_code = response.choices[0].message.content
        code_block = re.search(r'```(?:python)?\n(.*?)\n```', manim_code, re.DOTALL)
        manim_code = code_block.group(1).strip() if code_block else manim_code.strip()

        # Custom styled code expander
        st.markdown('<div class="code-expander">', unsafe_allow_html=True)
        st.markdown('<div class="code-header">🧩 Generated Manim Code</div>', unsafe_allow_html=True)
        st.code(manim_code, language='python')
        st.markdown('</div>', unsafe_allow_html=True)

        # Save the .py script
        script_id = uuid.uuid4().hex[:8]
        script_path = temp_dir / f"scene_{script_id}.py"
        with open(script_path, "w") as f:
            f.write(manim_code)

        # Detect Scene class
        scene_match = re.search(r'class\s+(\w+)\(Scene\):', manim_code)
        if not scene_match:
            st.error("❌ Could not detect a valid Scene class.")
            st.stop()

        scene_name = scene_match.group(1)

        # Progress indicator for rendering
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Render the animation with progress updates
        status_text.text("🎬 Starting Manim rendering process...")
        progress_bar.progress(10)
        
        cmd = [
            "manim",
            "-qm",
            "--disable_caching",
            str(script_path),
            scene_name
        ]
        env = os.environ.copy()
        env["SKIP_LATEX_RENDER"] = "1"

        status_text.text("🎬 Rendering with Manim... Please wait...")
        progress_bar.progress(30)
        
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        
        progress_bar.progress(70)
        status_text.text("🎬 Processing animation output...")

        if result.returncode != 0:
            progress_bar.empty()
            status_text.empty()
            st.error("⚠️ Rendering failed.")
            with st.expander("See error logs"):
                st.text(result.stderr)
            st.stop()

        progress_bar.progress(90)
        status_text.text("🎬 Finalizing animation...")

        # Locate output .mp4
        possible_paths = list(Path("media/videos").rglob("*.mp4"))
        latest_video = max(possible_paths, key=os.path.getmtime) if possible_paths else None

        progress_bar.progress(100)
        progress_bar.empty()
        status_text.empty()

        if latest_video:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="preview-header"><span class="preview-icon">🎥</span> Animation Preview</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-banner"><span class="success-icon">✅</span> Animation rendered successfully!</div>', unsafe_allow_html=True)
            st.video(str(latest_video))
            
            # Download button for the animation
            with open(latest_video, "rb") as file:
                btn = st.download_button(
                    label="💾 Download Animation",
                    data=file,
                    file_name=f"animagic_{script_id}.mp4",
                    mime="video/mp4"
                )
        else:
            st.warning("Generated, but couldn't locate animation in known output folders.")

    except Exception as e:
        st.error("An error occurred:")
        st.exception(e)

# Footer with animated heart
st.markdown('''
<div class="footer">
    <div><span class="footer-logo">AniMAGIC</span> • Made with <span class="heart">❤️</span> using GPT-4 and Manim</div>
    <div>© 2024 • Turn imagination into mathematics</div>
</div>
''', unsafe_allow_html=True)
