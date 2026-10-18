import os
import streamlit as st
from core.pipeline import MotionLatticeEngine
from core.validator import VectorValidator

st.set_page_config(page_title="Motion-Lattice Engine", layout="wide", page_icon="🎨")

if "active_svg" not in st.session_state:
    st.session_state.active_svg = None

st.title("⚡ Motion-Lattice Engine")
st.subheader("Decoupled Architecture Text-to-SVG Agentic Animation Engine")

st.sidebar.header("🔑 Authentication")
hf_token_input = st.sidebar.text_input("Custom HF Token (Optional):", type="password")

secret_token = st.secrets.get("HF_TOKEN") if "HF_TOKEN" in st.secrets else os.getenv("HF_TOKEN")
active_token = hf_token_input if hf_token_input else secret_token

if active_token:
    st.sidebar.success("🔒 System API Engine Linked")
else:
    st.sidebar.warning("⚠️ Access Key Missing")

col_input, col_output = st.columns()

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
        st.error("❌ Authentication Refused.")
    else:
        with st.spinner("Processing downstream multi-agent nodes..."):
            engine = MotionLatticeEngine(hf_token=active_token)
            generated_output = engine.build_animation(prompt)
            is_valid, final_svg = VectorValidator.validate_svg_syntax(generated_output)
            
            if is_valid:
                st.session_state.active_svg = final_svg
                st.rerun()
            else:
                st.error("❌ Code Generation failed AST compiler gate.")

if st.session_state.active_svg:
    st.markdown("---")
    @st.dialog("Refactor Vector Styling State")
    def open_style_modal():
        style_prompt = st.text_input("Styling Instruction:", placeholder="e.g., Change to neon emerald green")
        if st.button("Submit Refactoring Request", type="primary"):
            with st.spinner("Modifying runtime tokens..."):
                engine = MotionLatticeEngine(hf_token=active_token)
                modified_output = engine.modify_style(st.session_state.active_svg, style_prompt)
                is_valid, final_modified_svg = VectorValidator.validate_svg_syntax(modified_output)
                if is_valid:
                    st.session_state.active_svg = final_modified_svg
                    st.rerun()

    if st.button("🎨 Open Color & Style Customization Tool"):
        open_style_modal()
