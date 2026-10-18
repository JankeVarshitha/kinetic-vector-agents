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
        # Agent 1 builds the visual layout scaffolding
        layout_system = (
            "You are an expert Frontend Architect specializing in ultra-fast, modern HTML/CSS art. "
            "Generate ONLY a self-contained HTML wrapper containing a centered <div> structure or HTML5 <canvas>. "
            "Do NOT include any markdown blocks (like ```html) and no conversational text explanations. "
            "Ensure elements have clean semantic class names or IDs."
        )
        
        base_html = self.bridge.request_inference(layout_system, f"Asset Target: {motion_intent}")
        base_html = re.sub(r"```html|```", "", base_html).strip()

        # Agent 2 injects the animation stylesheet
        animation_system = (
            "You are a Senior CSS Kinetic Designer. Take the provided HTML snippet and inject a high-performance "
            "<style> block containing fluid, looping CSS @keyframes animations targeting the layout classes. "
            "Output ONLY the newly combined raw, complete HTML string. No markdown wraps, no explanations."
        )
        
        animated_html = self.bridge.request_inference(animation_system, f"Theme: '{motion_intent}'.\n\nBase HTML:\n{base_html}")
        return re.sub(r"```html|```", "", animated_html).strip()


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
