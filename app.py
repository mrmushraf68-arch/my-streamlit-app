Viewed app.py:1-678

Here is the complete source code for [app.py](file:///C:/Users/DANY/.gemini/antigravity-ide/scratch/ai_creative_studio/app.py):

```python
"""AI Creative Studio - Streamlit Web Application.

A modern, high-aesthetic AI Art Studio featuring multi-screen navigation,
interactive style selection cards, prompt crafting engine, parameter inspector,
and concept generation visualization.
"""

import time
import streamlit as st

# ----------------------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="AI Creative Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------
# Color Palette & Style Metadata
# ----------------------------------------------------------------------
BG_DARK = "#0B0F19"
BG_CARD = "#151D2E"
BG_CARD_HOVER = "#1E2A42"
BG_INPUT = "#0F1626"
BORDER_SUBTLE = "#22314E"
BORDER_ACTIVE = "#6366F1"
PRIMARY = "#6366F1"
PRIMARY_HOVER = "#4F46E5"
PRIMARY_LIGHT = "#818CF8"
SECONDARY = "#8B5CF6"
ACCENT_CYAN = "#06B6D4"
ACCENT_GREEN = "#10B981"
ACCENT_AMBER = "#F59E0B"
ACCENT_PINK = "#EC4899"
TEXT_PRIMARY = "#F8FAFC"
TEXT_SECONDARY = "#94A3B8"
TEXT_MUTED = "#64748B"
TEXT_ACCENT = "#A5B4FC"

STYLES_DATA = {
    "ghibli": {
        "title": "Ghibli",
        "icon": "🌿",
        "tagline": "Lush watercolor backgrounds, nostalgic dreamscapes, hand-painted warmth.",
        "accent": ACCENT_GREEN,
        "tags": ["AnimePastoral", "Watercolor", "Miyazaki"],
        "preview_desc": "Serene composition with vibrant rolling hills, lush foliage, and nostalgic soft lighting.",
        "palette": ["#10B981", "#34D399", "#064E3B", "#FDE047", "#38BDF8"],
        "sample_prompts": [
            "A serene floating island surrounded by golden clouds, ancient cobblestone windmills, and gentle luminescent lanterns at twilight...",
            "Ancient mossy clocktower deep inside an emerald forest with floating spirit orbs and sunbeams.",
            "Sun-drenched coastal train traversing crystal blue waters under puffy summer clouds.",
            "Cozy wooden cottage kitchen with bubbling magical tea and ivy climbing through open windows.",
        ],
        "lighting": "Golden Hour / Soft Diffused",
        "aspect": "16:9 Cinema Wide",
    },
    "anime": {
        "title": "Anime",
        "icon": "⚡",
        "tagline": "Dynamic linework, vibrant cel-shading, and vivid atmospheric glow.",
        "accent": ACCENT_AMBER,
        "tags": ["MakotoShinkai", "CelShaded", "Cinematic"],
        "preview_desc": "High-octane anime visual with crystalline sky reflections and dramatic rim lighting.",
        "palette": ["#F59E0B", "#FBBF24", "#78350F", "#60A5FA", "#EC4899"],
        "sample_prompts": [
            "A futuristic neon-drenched Tokyo skyline during a meteor shower, reflections gleaming on wet asphalt...",
            "Cyberpunk blade warrior standing atop a rain-slicked skyscraper overlooking holographic dragons.",
            "Mecha orbital hangar illuminated by electric blue sparks and vibrant laser calibration beams.",
            "Shinto shrine floating in twilight clouds surrounded by swirling iridescent cherry blossom petals.",
        ],
        "lighting": "Vibrant Neon & Dramatic Rim Light",
        "aspect": "21:9 Ultra-Wide",
    },
    "pixar": {
        "title": "Pixar",
        "icon": "🧸",
        "tagline": "Volumetric lighting, stylized 3D character design, and charming warmth.",
        "accent": PRIMARY_LIGHT,
        "tags": ["3DRender", "SubsurfaceScatter", "Whimsical"],
        "preview_desc": "Rich 3D character render with tactile textures, expressive emotions, and cinematic soft shadows.",
        "palette": ["#818CF8", "#6366F1", "#312E81", "#F472B6", "#FBBF24"],
        "sample_prompts": [
            "A curious little clockwork automaton discovering a glowing dandelion in an enchanted attic workshop...",
            "Fluffy baby yeti playing with a luminescent blue butterfly in the snowy Himalayan peaks.",
            "Brave little yellow submarine navigating an undersea coral kingdom with friendly glowing jellyfish.",
            "Tiny baker mouse decorated with powdered sugar frosting a gigantic strawberry cupcake.",
        ],
        "lighting": "Warm Volumetric & Subsurface Glow",
        "aspect": "4:3 Classic Animation",
    },
    "realistic": {
        "title": "Realistic",
        "icon": "📸",
        "tagline": "Photorealistic fidelity, 8K micro-textures, and optical depth of field.",
        "accent": ACCENT_CYAN,
        "tags": ["Photoreal", "Raytracing", "Hasselblad"],
        "preview_desc": "Hyper-detailed 8K photographic composition with true-to-life optical refraction and natural bokeh.",
        "palette": ["#06B6D4", "#22D3EE", "#164E63", "#F8FAFC", "#334155"],
        "sample_prompts": [
            "Cinematic macro shot of an iridescent crystal beetle perched on a dew-covered volcanic stone at sunrise...",
            "National Geographic portrait of an Arctic fox in a swirling blizzard with sharp crystal eye reflections.",
            "Hyperrealistic interior of an ancient marble observatory with golden sunlight beaming through the dome.",
            "Close-up of a crystal raindrop splashing against a midnight cityscape window with bokeh streetlights.",
        ],
        "lighting": "Natural Optical & Ambient Occlusion",
        "aspect": "16:9 Cinema Master",
    },
}

# ----------------------------------------------------------------------
# Session State Initialization
# ----------------------------------------------------------------------
if "screen" not in st.session_state:
    st.session_state.screen = "home"

if "creator_name" not in st.session_state:
    st.session_state.creator_name = ""

if "selected_style" not in st.session_state:
    st.session_state.selected_style = "ghibli"

if "prompt" not in st.session_state:
    st.session_state.prompt = STYLES_DATA["ghibli"]["sample_prompts"][0]

if "last_generated" not in st.session_state:
    st.session_state.last_generated = None


# ----------------------------------------------------------------------
# Custom CSS Styling (Dark Modern Glassmorphism)
# ----------------------------------------------------------------------
st.markdown(
    f"""
    <style>
        /* Base page background and typography */
        .stApp {{
            background: radial-gradient(circle at 50% 0%, #151D2E 0%, #0B0F19 65%, #070A11 100%);
            color: {TEXT_PRIMARY};
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
        }}

        /* Header element cleanup */
        header, footer {{
            visibility: hidden;
            height: 0px;
        }}
        .block-container {{
            padding-top: 1.8rem;
            padding-bottom: 2.5rem;
            max-width: 1180px;
        }}

        /* Badge Styling */
        .badge-tag {{
            display: inline-flex;
            align-items: center;
            background: {BG_CARD};
            border: 1px solid {BORDER_SUBTLE};
            color: {ACCENT_CYAN};
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            padding: 5px 14px;
            border-radius: 999px;
            margin-bottom: 12px;
            box-shadow: 0 4px 12px rgba(6, 182, 212, 0.08);
        }}

        .active-mode-badge {{
            display: inline-flex;
            align-items: center;
            background: {BG_CARD};
            border: 1px solid {PRIMARY_LIGHT}44;
            color: {PRIMARY_LIGHT};
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            padding: 6px 14px;
            border-radius: 999px;
            box-shadow: 0 0 15px rgba(129, 140, 248, 0.15);
        }}

        /* Hero Typography */
        .hero-title {{
            font-size: 2.75rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: {TEXT_PRIMARY};
            margin-bottom: 6px;
            line-height: 1.15;
            background: linear-gradient(135deg, #FFFFFF 40%, {PRIMARY_LIGHT} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .hero-subtitle {{
            font-size: 1.05rem;
            color: {TEXT_SECONDARY};
            margin-bottom: 28px;
            line-height: 1.5;
        }}

        /* Glassmorphic Cards */
        .glass-card {{
            background: {BG_CARD};
            border: 1px solid {BORDER_SUBTLE};
            border-radius: 16px;
            padding: 26px 30px;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.35);
            backdrop-filter: blur(12px);
        }}

        /* Style Selection Card Styling */
        .style-box {{
            background: {BG_CARD};
            border: 1px solid {BORDER_SUBTLE};
            border-radius: 14px;
            padding: 16px;
            transition: all 0.25s ease;
            height: 100%;
        }}
        .style-box:hover {{
            background: {BG_CARD_HOVER};
            border-color: {PRIMARY_LIGHT};
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        }}
        .style-box-active {{
            background: {BG_CARD_HOVER};
            border: 1.5px solid {PRIMARY};
            border-radius: 14px;
            padding: 16px;
            box-shadow: 0 0 18px rgba(99, 102, 241, 0.25);
            height: 100%;
        }}

        .tag-pill {{
            display: inline-block;
            background: {BG_INPUT};
            color: {TEXT_MUTED};
            font-size: 0.72rem;
            font-weight: 600;
            padding: 2px 7px;
            border-radius: 6px;
            margin-right: 4px;
            margin-top: 4px;
        }}

        /* Palette dots */
        .palette-dot {{
            display: inline-block;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            margin-right: 6px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}

        /* Input styling */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {{
            background-color: {BG_INPUT} !important;
            color: {TEXT_PRIMARY} !important;
            border: 1px solid {BORDER_SUBTLE} !important;
            border-radius: 10px !important;
            font-size: 0.98rem !important;
        }}
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {{
            border-color: {BORDER_ACTIVE} !important;
            box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25) !important;
        }}

        /* Buttons */
        .stButton > button {{
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            letter-spacing: 0.02em !important;
            transition: all 0.2s ease !important;
            border: 1px solid {BORDER_SUBTLE} !important;
            background-color: {BG_CARD} !important;
            color: {TEXT_PRIMARY} !important;
        }}
        .stButton > button:hover {{
            background-color: {BG_CARD_HOVER} !important;
            border-color: {PRIMARY_LIGHT} !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        }}

        /* Primary Action Buttons */
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, {PRIMARY} 0%, {SECONDARY} 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            box-shadow: 0 4px 16px rgba(99, 102, 241, 0.35) !important;
        }}
        .stButton > button[kind="primary"]:hover {{
            background: linear-gradient(135deg, {PRIMARY_HOVER} 0%, #7C3AED 100%) !important;
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
            transform: translateY(-2px) !important;
        }}

        /* Specs table container */
        .specs-table {{
            width: 100%;
            margin-top: 10px;
            font-size: 0.84rem;
        }}
        .specs-row {{
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }}
        .specs-label {{
            color: {TEXT_MUTED};
        }}
        .specs-val {{
            color: {TEXT_ACCENT};
            font-weight: 600;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------
# Navigation Helpers
# ----------------------------------------------------------------------
def go_to_studio():
    if not st.session_state.creator_name.strip():
        st.session_state.creator_name = "Creator"
    st.session_state.screen = "studio"
    st.rerun()


def go_to_home():
    st.session_state.screen = "home"
    st.rerun()


def set_style(style_key):
    st.session_state.selected_style = style_key
    st.session_state.prompt = STYLES_DATA[style_key]["sample_prompts"][0]
    st.rerun()


# ----------------------------------------------------------------------
# Screen 1: Home View
# ----------------------------------------------------------------------
def render_home_view():
    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([1, 2.2, 1])

    with col2:
        # Centered branding badge
        st.markdown(
            '<div style="text-align: center;"><span class="badge-tag">✨ NEXT-GEN AI ART SUITE</span></div>',
            unsafe_allow_html=True,
        )

        # Title & Subtitle
        st.markdown(
            """
            <div style="text-align: center;">
                <div class="hero-title">AI Creative Studio</div>
                <div class="hero-subtitle">Transform ideas into breathtaking art with curated visual styles</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Input Card
        with st.container():
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)

            st.markdown(
                f'<div style="font-size: 0.78rem; font-weight: 700; color: {TEXT_ACCENT}; margin-bottom: 8px; letter-spacing: 0.05em;">ENTER YOUR CREATOR NAME</div>',
                unsafe_allow_html=True,
            )

            name_input = st.text_input(
                "Creator Name",
                value=st.session_state.creator_name,
                placeholder="e.g. Maya, Leonardo, Alex...",
                label_visibility="collapsed",
                key="name_input_box",
            )

            st.markdown(
                f'<div style="font-size: 0.8rem; color: {TEXT_MUTED}; margin-top: 4px; margin-bottom: 18px;">Enter your name or handle to personalize your workspace</div>',
                unsafe_allow_html=True,
            )

            btn_col1, btn_col2 = st.columns([2, 1])
            with btn_col1:
                if st.button("Create New 🚀", type="primary", use_container_width=True):
                    st.session_state.creator_name = name_input.strip() if name_input.strip() else "Creator"
                    go_to_studio()

            with btn_col2:
                if st.button("Quick Start ✨", use_container_width=True):
                    st.session_state.creator_name = "Creator"
                    go_to_studio()

            st.markdown("</div>", unsafe_allow_html=True)

        # Style badges below card
        st.write("")
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; gap: 14px; flex-wrap: wrap; margin-top: 14px;">
                <span style="font-size: 0.84rem; font-weight: 700; color: {ACCENT_GREEN};">🌿 Ghibli</span>
                <span style="font-size: 0.84rem; font-weight: 700; color: {ACCENT_AMBER};">⚡ Anime</span>
                <span style="font-size: 0.84rem; font-weight: 700; color: {PRIMARY_LIGHT};">🧸 Pixar</span>
                <span style="font-size: 0.84rem; font-weight: 700; color: {ACCENT_CYAN};">📸 Realistic</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ----------------------------------------------------------------------
# Screen 2: Studio View
# ----------------------------------------------------------------------
def render_studio_view():
    current_style_key = st.session_state.selected_style
    current_style = STYLES_DATA[current_style_key]
    user_name = st.session_state.creator_name if st.session_state.creator_name else "Creator"

    # Top Navigation Bar
    nav_left, nav_right = st.columns([1, 1])
    with nav_left:
        if st.button("← Back to Home", use_container_width=False):
            go_to_home()
    with nav_right:
        st.markdown(
            '<div style="text-align: right;"><span class="active-mode-badge">✨ STUDIO CANVAS ACTIVE</span></div>',
            unsafe_allow_html=True,
        )

    st.write("")

    # Welcome Header
    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <div style="font-size: 2.1rem; font-weight: 800; color: {TEXT_PRIMARY}; margin-bottom: 4px;">
                Welcome, {user_name}! 🎨
            </div>
            <div style="font-size: 0.98rem; color: {TEXT_SECONDARY};">
                Select an aesthetic style below to tailor your AI creative generation engine.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Section Title
    st.markdown(
        f'<div style="font-size: 0.78rem; font-weight: 700; color: {TEXT_ACCENT}; letter-spacing: 0.08em; margin-bottom: 12px;">STYLE CHOICES</div>',
        unsafe_allow_html=True,
    )

    # 4 Style Selection Cards
    cols = st.columns(4)
    for idx, (key, data) in enumerate(STYLES_DATA.items()):
        with cols[idx]:
            is_active = (key == current_style_key)
            card_class = "style-box-active" if is_active else "style-box"
            status_text = "● SELECTED" if is_active else "○ SELECT"
            status_color = data["accent"] if is_active else TEXT_MUTED

            tags_html = "".join([f'<span class="tag-pill">#{t}</span>' for t in data["tags"]])

            st.markdown(
                f"""
                <div class="{card_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-size: 1.3rem;">{data['icon']} <strong style="font-size: 1.05rem; color: {TEXT_PRIMARY};">{data['title']}</strong></span>
                        <span style="font-size: 0.72rem; font-weight: 700; color: {status_color};">{status_text}</span>
                    </div>
                    <div style="font-size: 0.82rem; color: {TEXT_SECONDARY}; min-height: 48px; line-height: 1.35; margin-bottom: 10px;">
                        {data['tagline']}
                    </div>
                    <div style="margin-bottom: 8px;">
                        {tags_html}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            btn_label = f"Apply {data['title']}" if not is_active else f"✓ Active ({data['title']})"
            if st.button(btn_label, key=f"style_btn_{key}", use_container_width=True, disabled=is_active):
                set_style(key)

    st.write("")
    st.write("")

    # Main Workspace (2-Column Layout)
    left_col, right_col = st.columns([3, 2], gap="large")

    # Left Column: Prompt Crafting & Generation Canvas
    with left_col:
        st.markdown(
            f'<div style="font-size: 0.78rem; font-weight: 700; color: {TEXT_ACCENT}; letter-spacing: 0.08em; margin-bottom: 8px;">CREATIVE PROMPT</div>',
            unsafe_allow_html=True,
        )

        prompt_text = st.text_area(
            "Prompt Input",
            value=st.session_state.prompt,
            height=130,
            label_visibility="collapsed",
            key="studio_prompt_input",
            placeholder="Describe your creative vision in detail...",
        )

        # Quick sample prompt chips
        st.markdown(
            f'<div style="font-size: 0.75rem; color: {TEXT_MUTED}; margin-bottom: 6px; font-weight: 600;">INSPIRATION PRESETS:</div>',
            unsafe_allow_html=True,
        )
        sample_cols = st.columns(len(current_style["sample_prompts"]))
        for p_idx, s_prompt in enumerate(current_style["sample_prompts"]):
            with sample_cols[p_idx]:
                short_label = f"Idea {p_idx+1}"
                if st.button(f"💡 {short_label}", key=f"sample_{p_idx}", help=s_prompt, use_container_width=True):
                    st.session_state.prompt = s_prompt
                    st.rerun()

        st.write("")

        # Action Buttons
        act_col1, act_col2 = st.columns([2, 1])
        with act_col1:
            gen_clicked = st.button("Generate Concept ✨", type="primary", use_container_width=True)
        with act_col2:
            enhance_clicked = st.button("Auto-Enhance 🪄", use_container_width=True)

        if enhance_clicked:
            enhanced_addons = f", trending on Artstation, highly detailed, {current_style['tags'][0]}, volumetric light, 8k resolution"
            st.session_state.prompt = prompt_text.strip() + enhanced_addons
            st.rerun()

        # Generation trigger & visual preview
        if gen_clicked:
            with st.spinner(f"Synthesizing {current_style['title']} concept render..."):
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.008)
                    progress_bar.progress(percent_complete + 1)
                time.sleep(0.2)
                progress_bar.empty()

                st.session_state.last_generated = {
                    "prompt": prompt_text,
                    "style": current_style["title"],
                    "icon": current_style["icon"],
                    "accent": current_style["accent"],
                    "aspect": current_style["aspect"],
                    "timestamp": time.strftime("%H:%M:%S"),
                }
                st.success(f"✨ Concept prepared in {current_style['title']} style!")

        # Render Generated Concept Card
        if st.session_state.last_generated:
            last = st.session_state.last_generated
            st.markdown(
                f"""
                <div class="glass-card" style="margin-top: 20px; border-left: 4px solid {last['accent']};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span style="font-weight: 700; color: {last['accent']}; font-size: 0.9rem;">
                            {last['icon']} {last['style'].upper()} CONCEPT RENDER
                        </span>
                        <span style="font-size: 0.75rem; color: {TEXT_MUTED};">Rendered at {last['timestamp']}</span>
                    </div>
                    <div style="background: {BG_INPUT}; border-radius: 10px; padding: 14px; margin-bottom: 12px; border: 1px solid {BORDER_SUBTLE};">
                        <div style="font-size: 0.88rem; color: {TEXT_PRIMARY}; font-style: italic; line-height: 1.45;">
                            "{last['prompt']}"
                        </div>
                    </div>
                    <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                        <span class="tag-pill">Ratio: {last['aspect']}</span>
                        <span class="tag-pill">Sampler: DPM++ 2M Karras</span>
                        <span class="tag-pill">Steps: 35</span>
                        <span class="tag-pill">CFG: 7.5</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Right Column: Active Preset Inspector & Visual Specs
    with right_col:
        st.markdown(
            f"""
            <div class="glass-card">
                <div style="font-size: 0.76rem; font-weight: 700; color: {ACCENT_CYAN}; letter-spacing: 0.08em; margin-bottom: 4px;">
                    ACTIVE PRESET
                </div>
                <div style="font-size: 1.35rem; font-weight: 800; color: {current_style['accent']}; margin-bottom: 8px;">
                    {current_style['icon']} {current_style['title']} Aesthetic
                </div>
                <div style="font-size: 0.88rem; color: {TEXT_SECONDARY}; line-height: 1.45; margin-bottom: 16px;">
                    {current_style['preview_desc']}
                </div>

                <div style="font-size: 0.76rem; font-weight: 700; color: {TEXT_ACCENT}; letter-spacing: 0.06em; margin-bottom: 8px;">
                    STYLE COLOR PALETTE
                </div>
                <div style="margin-bottom: 16px;">
                    {''.join([f'<span class="palette-dot" style="background-color: {c};" title="{c}"></span>' for c in current_style['palette']])}
                </div>

                <div style="font-size: 0.76rem; font-weight: 700; color: {TEXT_ACCENT}; letter-spacing: 0.06em; margin-bottom: 6px;">
                    SYNTHESIS PARAMETERS
                </div>
                <div class="specs-table">
                    <div class="specs-row">
                        <span class="specs-label">Resolution</span>
                        <span class="specs-val">4K Ultra-HD</span>
                    </div>
                    <div class="specs-row">
                        <span class="specs-label">Engine</span>
                        <span class="specs-val">Neural Diffusion v4.2</span>
                    </div>
                    <div class="specs-row">
                        <span class="specs-label">Aspect Ratio</span>
                        <span class="specs-val">{current_style['aspect']}</span>
                    </div>
                    <div class="specs-row">
                        <span class="specs-label">Lighting Model</span>
                        <span class="specs-val">{current_style['lighting']}</span>
                    </div>
                    <div class="specs-row">
                        <span class="specs-label">Precision</span>
                        <span class="specs-val">FP16 TensorRT</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Advanced Tuner Accordion
        with st.expander("⚙️ Advanced Engine Parameters", expanded=False):
            st.slider("Sampling Steps", min_value=15, max_value=80, value=35, step=5)
            st.slider("Guidance Scale (CFG)", min_value=1.0, max_value=15.0, value=7.5, step=0.5)
            st.selectbox("Upscale Model", ["Latent (bicubic antialiased)", "R-ESRGAN 4x+", "SwinIR 4x"])
            st.text_input("Negative Prompt", value="blurry, distorted, low quality, artifact, oversaturated")


# ----------------------------------------------------------------------
# Main Application Router
# ----------------------------------------------------------------------
def main():
    if st.session_state.screen == "home":
        render_home_view()
    elif st.session_state.screen == "studio":
        render_studio_view()
    else:
        render_home_view()


if __name__ == "__main__":
    main()
```
