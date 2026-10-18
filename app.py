import os
import sys
import re
import ast
import json

# --- DYNAMIC ROOT DIRECTORY WRAPPER ---
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import streamlit as st
import streamlit.components.v1 as components
from core.pipeline import KineticVectorEngine
from core.validator import VectorValidator

st.set_page_config(page_title="Motion-Lattice Engine", layout="wide", page_icon="🎨")

# Persistent State Initializers
if "active_config" not in st.session_state:
    st.session_state.active_config = None
if "active_svg" not in st.session_state:
    st.session_state.active_svg = None

st.title("Animation Generator")
st.subheader("NVIDIA NIM Multi-Agent Text-to-SVG Kinetic Synthesis Framework")

# --- BACKGROUND AUTHENTICATION BINDING ---
active_token = st.secrets.get("NVIDIA_API_KEY") if "NVIDIA_API_KEY" in st.secrets else os.getenv("NVIDIA_API_KEY")

col_input, col_output = st.columns([1, 1])

with col_input:
    st.markdown("### Generation Controls")
    prompt_raw = st.text_area("Describe your animation concept:", value="A sleek neon cyberpunk loader icon with smooth rotating gears.", height=100)
    
    # MOBILE FIX: Sanitize typography injection (removes smart quotes from mobile keyboards)
    prompt = prompt_raw.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'").strip()
    
    generate_btn = st.button("Compile Kinetic Asset", type="primary")

with col_output:
    st.markdown("### Generated Animation")
    render_placeholder = st.empty()
    if st.session_state.active_svg:
        with render_placeholder.container():
            try:
                # Optimized viewport sizing explicitly designed for mobile responsive scaling
                components.html(st.session_state.active_svg, height=400, scrolling=True)
            except Exception:
                st.caption("Rendering fallback format for mobile viewports:")
                st.html(st.session_state.active_svg)
    else:
        render_placeholder.info("Awaiting pipeline generation directives...")

# --- GENERATION LIFECYCLE CONTROLLER ---
if generate_btn:
    if not active_token:
        st.error("❌ Authentication Refused: Remote credentials unavailable in this context.")
    else:
        # User feedback container optimized to prevent mobile layout shifting
        with st.spinner("Processing multi-agent nodes... Please keep this browser window active."):
            try:
                engine = KineticVectorEngine(nim_token=active_token)
                
                layout_system = (
                    "You are an expert design metadata compiler. Output ONLY a valid JSON object or Python dictionary. "
                    "Combine multiple layout shapes together to represent the user's prompt. Do NOT include markdown syntax wraps (```python) and no conversation.\n\n"
                    "Target exact structure framework:\n"
                    "{'bg_color': '#hex', 'speed_multiplier': 1.0, 'components': [{'id': 'head', 'shape': 'square', 'color': '#hex', 'width': '120px', 'height': '120px', 'top_offset_percent': 40, 'left_offset_percent': 50, 'direction': 'cw', 'duration_seconds': 2.0}]}"
                )
                
                raw_output = engine.bridge.request_inference(layout_system, f"Asset Target: {prompt}")
                
                # Strip absolute empty characters to stabilize mobile packet streams
                raw_output_clean = raw_output.strip()
                dict_match = re.search(r'(\{[\s\S]*\})', raw_output_clean)
                
                if dict_match:
                    try:
                        clean_str = dict_match.group(1).strip()
                        # Sanitize smart characters from the model response array
                        clean_str = clean_str.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
                        
                        try:
                            config = ast.literal_eval(clean_str)
                        except Exception:
                            config = json.loads(clean_str.replace("'", '"'))
                        
                        st.session_state.active_config = config
                        
                        compiled_html = engine._compile_to_html(config)
                        is_valid, final_svg = VectorValidator.validate_svg_syntax(compiled_html)
                        
                        if is_valid:
                            st.session_state.active_svg = final_svg
                            st.slots = {}
                            st.rerun()
                        else:
                            st.error("❌ Generated asset failed markup validation controls.")
                    except Exception as parse_err:
                        st.error(f"❌ Text Parser Error: {str(parse_err)}")
                        st.code(raw_output)
                else:
                    st.error("❌ Topology Conflict: Server output missing structural json boundary targets.")
                    st.code(raw_output)
                    
            except Exception as gateway_err:
                st.error("💥 Pipeline Process Timeout or Gateway Interruption (HTTP 500)")
                st.info("Mobile networks frequently drop long background processes. Ensure your phone remains unlocked with the browser active during generation.")
                st.diagnostic_log = st.expander("View Diagnostic Trace")
                st.diagnostic_log.code(str(gateway_err))

# --- LIVE REFACTORING DIALOG CONTROL HUB ---
if st.session_state.active_svg and st.session_state.active_config:
    st.markdown("---")

    @st.dialog("Refactor Vector Styling State")
    def open_style_modal():
        style_prompt_raw = st.text_input("Styling Instruction:", placeholder="e.g., Change to neon emerald green")
        style_prompt = style_prompt_raw.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'").strip()
        
        if st.button("Submit Refactoring Request", type="primary"):
            if not style_prompt:
                st.error("Please enter a styling instruction.")
                return
                
            with st.spinner("Modifying runtime vectors..."):
                try:
                    engine = KineticVectorEngine(nim_token=active_token)
                    modified_config = engine.modify_style(st.session_state.active_config, style_prompt)
                    
                    compiled_html = engine._compile_to_html(modified_config)
                    is_valid, final_modified_svg = VectorValidator.validate_svg_syntax(compiled_html)
                    
                    if is_valid:
                        st.session_state.active_config = modified_config
                        st.session_state.active_svg = final_modified_svg
                        st.session_state["just_refactored"] = True
                    else:
                        st.error("❌ Refactoring validation failed.")
                except Exception as e:
                    st.error(f"❌ Error during modification: {str(e)}")
            
            if "just_refactored" in st.session_state:
                st.rerun()

    if st.button("Click to Open Customization Tool"):
        open_style_modal()

# Post-dialog evaluation frame cleanup logic
if st.session_state.get("just_refactored"):
    del st.session_state["just_refactored"]
    st.rerun()
