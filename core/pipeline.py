import re
import streamlit as st
from core.client import NIMBridge

class KineticVectorEngine:
    """Orchestrates multi-agent pipelines for multi-tier visual syntax compiling."""
    def __init__(self, nim_token: str):
        self.bridge = NIMBridge(nim_token=nim_token)

    def build_animation(self, motion_intent: str) -> str:
        """Sequential layout-to-kinetic agent pipeline execution mapping."""
        layout_system = (
            "You are an expert Frontend AI Architect specializing in raw vector layout design. "
            "Generate ONLY valid, clean, modern, semantic SVG code. "
            "Do NOT include any markdown code blocks (like ```xml), no text outside the SVG tags, and no explanations. "
            "Assign explicit semantic IDs to critical animated components (e.g., id='ball', id='wing')."
        )
        base_svg = self.bridge.request_inference(layout_system, f"Asset Target: {motion_intent}")
        
        if not base_svg or not isinstance(base_svg, str):
            st.error("⚠️ Pipeline Failure: Agent 1 failed to compile layout architecture vector structures.")
            return ""
            
        base_svg = re.sub(r"```xml|```", "", base_svg).strip()

        animation_system = (
            "You are a Senior SVG Kinetic Designer. Take the provided SVG code and inject a high-performance "
            "<style> block containing fluid, looping CSS @keyframes animations targeting semantic element IDs. "
            "Output ONLY the complete, newly combined raw SVG code. No markdown, no text explanations."
        )
        animated_svg = self.bridge.request_inference(animation_system, f"Theme: '{motion_intent}'.\n\nBase SVG:\n{base_svg}")
        
        if not animated_svg or not isinstance(animated_svg, str):
            st.error("⚠️ Pipeline Failure: Agent 2 failed to compile the kinetic animation stylesheet layer.")
            return ""
            
        return re.sub(r"```xml|```", "", animated_svg).strip()

    def modify_style(self, current_svg: str, style_modification_prompt: str) -> str:
        """Refactors active vector DOM states by selectively isolating and overriding color definitions."""
        refactor_system = (
            "You are a Senior SVG Technical Lead. Modify the color palette/gradients of the following SVG "
            "strictly adhering to the user's styling instruction. Keep all vector layout geometry, path IDs, "
            "and keyframe animations untouched. Output ONLY the modified complete raw SVG code."
        )
        modified_svg = self.bridge.request_inference(
            refactor_system, 
            f"Mutation Request: {style_modification_prompt}\n\nCurrent SVG:\n{current_svg}"
        )
        
        if not modified_svg or not isinstance(modified_svg, str):
            st.error("⚠️ Pipeline Failure: Agent 3 style refactoring variant returned an empty payload.")
            return current_svg
            
        return re.sub(r"```xml|```", "", modified_svg).strip()
