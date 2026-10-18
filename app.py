import os
import sys

# --- DYNAMIC ROOT DIRECTORY WRAPPER ---
# Enforces clean package namespace tracking across Streamlit cloud environments
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Standard entry imports now execute flawlessly without namespace collisions
import streamlit as st
from core.pipeline import KineticVectorEngine
from core.validator import VectorValidator


st.set_page_config(page_title="Motion-Lattice Engine", layout="wide", page_icon="🎨")

if "active_svg" not in st.session_state:
    st.session_state.active_svg = None

st.title("⚡ Motion-Lattice Engine")
st.subheader("NVIDIA NIM Multi-Agent Text-to-SVG Kinetic Synthesis Framework")

st.sidebar.header("🔑 Authentication")
token_input = st.sidebar.text_input("Custom NVIDIA API Key (Optional):", type="password")

# Multi-layer secret variable extraction
secret_token = st.secrets.get("NVIDIA_API_KEY") if "NVIDIA_API_KEY" in st.secrets else os.getenv("NVIDIA_API_KEY")
active_token = token_input if token_input else secret_token

if active_token:
    st.sidebar.success("🔒 Remote NIM Gateway Active")
else:
    st.sidebar.warning("⚠️ Access Key Missing")

# Resolved: Absolute layout columns declaration specified
col_input, col_output = st.columns(2)

with col_input:
    st.markdown("### 📥 Generation Controls")
    prompt = st.text_area("Describe your animation concept:", value="A sleek neon cyberpunk loader icon with smooth rotating gears.", height=100)
    generate_btn = st.button("Compile Kinetic Asset", type="primary")

with col_output:
    st.markdown("### 📺 Viewport")
    render_placeholder = st.empty()
    if st.session_state.active_svg:
        render_placeholder.components.v1.html(st.session_state.active_svg, height=500, scrolling=True)
    else:
        render_placeholder.info("Awaiting pipeline generation directives...")

if generate_btn:
    if not active_token:
        st.error("❌ Authentication Refused: Key parameters uninitialized.")
    else:
        with st.spinner("Processing downstream multi-agent nodes..."):
            engine = KineticVectorEngine(nim_token=active_token)
            generated_output = engine.build_animation(prompt)
            is_valid, final_svg = VectorValidator.validate_svg_syntax(generated_output)
            
            if is_valid:
                st.session_state.active_svg = final_svg
                st.rerun()
            else:
                st.error("❌ Code Generation failed structural XML validation gates.")

if st.session_state.active_svg:
    st.markdown("---")
    @st.dialog("Refactor Vector Styling State")
    def open_style_modal():
        style_prompt = st.text_input("Styling Instruction:", placeholder="e.g., Change to neon emerald green")
        if st.button("Submit Refactoring Request", type="primary"):
            with st.spinner("Modifying runtime vectors..."):
                engine = KineticVectorEngine(nim_token=active_token)
                modified_output = engine.modify_style(st.session_state.active_svg, style_prompt)
                is_valid, final_modified_svg = VectorValidator.validate_svg_syntax(modified_output)
                if is_valid:
                    st.session_state.active_svg = final_modified_svg
                    st.rerun()

    if st.button("🎨 Open Color & Style Customization Tool"):
        open_style_modal()
