import os
import streamlit as st
from core.pipeline import MotionLatticeEngine
from core.validator import VectorValidator

st.set_page_config(page_title="Motion-Lattice Engine", layout="wide", page_icon="🎨")

if "active_svg" not in st.session_state:
    st.session_state.active_svg = None

st.title("⚡ Motion-Lattice Engine")
st.subheader("Decoupled Architecture Text-to-SVG Agentic Animation Framework")

st.sidebar.header("🔑 Authentication")
api_token_input = st.sidebar.text_input("Custom OpenRouter Token (Optional):", type="password")

# Secure multi-layer token environment fallback loop
secret_token = st.secrets.get("OPENROUTER_TOKEN") if "OPENROUTER_TOKEN" in st.secrets else os.getenv("OPENROUTER_TOKEN")
active_token = api_token_input if api_token_input else secret_token

if active_token:
    st.sidebar.success("🔒 Remote API Engine Linked")
else:
    st.sidebar.warning("⚠️ Access Key Missing")

# Resolved: Explicit positional column width specification injected
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
            engine = MotionLatticeEngine(api_token=active_token)
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
                engine = MotionLatticeEngine(api_token=active_token)
                modified_output = engine.modify_style(st.session_state.active_svg, style_prompt)
                is_valid, final_modified_svg = VectorValidator.validate_svg_syntax(modified_output)
                if is_valid:
                    st.session_state.active_svg = final_modified_svg
                    st.rerun()

    if st.button("🎨 Open Color & Style Customization Tool"):
        open_style_modal()
