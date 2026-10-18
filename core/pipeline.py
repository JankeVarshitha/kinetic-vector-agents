import re
import streamlit as st
from core.client import NIMBridge

class KineticVectorEngine:
    """Orchestrates multi-agent pipelines for multi-tier visual syntax compiling."""
    
    def __init__(self, nim_token: str):
        self.bridge = NIMBridge(nim_token=nim_token)

    def _extract_svg(self, text: str) -> str:
        """Isolates the raw SVG element from any model text wrapping wrappers."""
        if not text:
            return ""
        
        # Pulls out everything inside <svg> tags case-insensitively across multiple line boundaries
        match = re.search(r'(<svg[\s\(\S\)]*?</svg>)', text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
            
        # Fallback to general markdown cleaning rules
        cleaned = re.sub(r"```xml|```", "", text).strip()
        return cleaned

    def build_animation(self, motion_intent: str) -> str:
        """Sequential layout-to-kinetic agent pipeline execution mapping."""
        layout_system = (
            "detailed thinking off\n" # OFFICIAL DIRECTIVE: Instantly disables internal reasoning tokens
            "You are an expert Frontend AI Architect specializing in raw vector layout design. "
            "Generate ONLY valid, clean, modern, semantic SVG code. No explanations, no conversation. "
            "Do NOT include any markdown code blocks (like ```xml), and no text outside the SVG tags."
        )
        
        base_raw = self.bridge.request_inference(layout_system, f"Asset Target: {motion_intent}")
        if not base_raw:
            st.error("⚠️ Pipeline Failure: Agent 1 failed to build layout structural context.")
            return ""
        
        base_svg = self._extract_svg(base_raw)
        
        animation_system = (
            "You are a Senior SVG Kinetic Designer. Take the provided SVG code and inject a high-performance "
            "<style> block containing fluid, looping CSS @keyframes animations targeting semantic element IDs. "
            "Output ONLY the complete, newly combined raw SVG code. No markdown, no text explanations, no conversation."
        )
        
        animated_raw = self.bridge.request_inference(animation_system, f"Theme: '{motion_intent}'.\n\nBase SVG:\n{base_svg}")
        if not animated_raw:
            st.error("⚠️ Pipeline Failure: Agent 2 failed to compile the kinetic stylesheet animation layer.")
            return ""
            
        return self._extract_svg(animated_raw)

    def modify_style(self, current_svg: str, style_modification_prompt: str) -> str:
        """Refactors active vector DOM states by selectively isolating and overriding color definitions."""
        refactor_system = (
            "You are a Senior SVG Technical Lead. Modify the color palette/gradients of the following SVG "
            "strictly adhering to the user's styling instruction. Keep all vector layout geometry, path IDs, "
            "and keyframe animations untouched. Output ONLY the modified complete raw SVG code."
        )
        modified_raw = self.bridge.request_inference(
            refactor_system, f"Mutation Request: {style_modification_prompt}\n\nCurrent SVG:\n{current_svg}"
        )
        if not modified_raw:
            return current_svg
            
        return self._extract_svg(modified_raw)
