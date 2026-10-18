import re
import streamlit as st
from core.client import NIMBridge

class KineticVectorEngine:
    """Orchestrates multi-agent pipelines for multi-tier visual syntax compiling."""
    
    def __init__(self, nim_token: str):
        self.bridge = NIMBridge(nim_token=nim_token)

    def _extract_svg(self, text: str, agent_name: str) -> str:
        """Helper to reliably isolate the raw SVG element from any model text wrapper."""
        print(f"\n[DEBUG PIPELINE - {agent_name}] Running structural extraction engine on raw LLM payload...")
        if not text:
            print(f"[DEBUG PIPELINE - {agent_name}] Extraction aborted: Source payload is completely empty.")
            return ""
            
        # Tries to aggressively grab everything between <svg and </svg>
        match = re.search(r'(<svg([\s\(\S\)]*?)</svg>)', text, re.IGNORECASE)
        if match:
            extracted = match.group(1).strip()
            print(f"[DEBUG PIPELINE - {agent_name}] Success! Isolated tag from token soup (Extracted size: {len(extracted)} chars).")
            return extracted
            
        print(f"[DEBUG PIPELINE - {agent_name}] Warning: Explicit <svg></svg> pairs not verified via regex. Running markdown fallback filter.")
        fallback = re.sub(r"```xml|```", "", text).strip()
        return fallback

    def build_animation(self, motion_intent: str) -> str:
        """Sequential layout-to-kinetic agent pipeline execution mapping."""
        # Tweaked prompt slightly to discourage long preamble explanations which trigger latency timeouts
        layout_system = (
            "You are an expert Frontend AI Architect specializing in raw vector layout design. "
            "Generate ONLY valid, clean, modern, semantic SVG code. No explanations, no conversation. "
            "Do NOT include any markdown code blocks (like ```xml), and no text outside the SVG tags. "
            "Assign explicit semantic IDs to critical animated components (e.g., id='ball', id='wing')."
        )
        
        print("\n[AGENT 1 START] Requesting Base Vector Layout Design...")
        base_raw = self.bridge.request_inference(layout_system, f"Asset Target: {motion_intent}")
        
        if not base_raw or not isinstance(base_raw, str):
            print("[AGENT 1 FAILED] Return structure was invalid or empty text layout string.")
            st.error("⚠️ Pipeline Failure: Agent 1 failed to compile layout architecture vector structures.")
            return ""
        
        base_svg = self._extract_svg(base_raw, "AGENT 1")
        print(f"[AGENT 1 COMPLETED] Clean Base Vector Struct Size: {len(base_svg)} characters.")
        
        animation_system = (
            "You are a Senior SVG Kinetic Designer. Take the provided SVG code and inject a high-performance "
            "<style> block containing fluid, looping CSS @keyframes animations targeting semantic element IDs. "
            "Output ONLY the complete, newly combined raw SVG code. No markdown, no text explanations, no conversation."
        )
        
        print("\n[AGENT 2 START] Requesting Kinetic Stylesheet Integration...")
        animated_raw = self.bridge.request_inference(animation_system, f"Theme: '{motion_intent}'.\n\nBase SVG:\n{base_svg}")
        
        if not animated_raw or not isinstance(animated_raw, str):
            print("[AGENT 2 FAILED] Return structure was invalid or empty string configuration.")
            st.error("⚠️ Pipeline Failure: Agent 2 failed to compile the kinetic animation stylesheet layer.")
            return ""
            
        final_svg = self._extract_svg(animated_raw, "AGENT 2")
        print(f"[AGENT 2 COMPLETED] Clean Kinetic Vector Struct Size: {len(final_svg)} characters.")
        return final_svg

    def modify_style(self, current_svg: str, style_modification_prompt: str) -> str:
        """Refactors active vector DOM states by selectively isolating and overriding color definitions."""
        refactor_system = (
            "You are a Senior SVG Technical Lead. Modify the color palette/gradients of the following SVG "
            "strictly adhering to the user's styling instruction. Keep all vector layout geometry, path IDs, "
            "and keyframe animations untouched. Output ONLY the modified complete raw SVG code."
        )
        print("\n[AGENT 3 START] Requesting Color State Refactoring Layer...")
        modified_raw = self.bridge.request_inference(
            refactor_system, f"Mutation Request: {style_modification_prompt}\n\nCurrent SVG:\n{current_svg}"
        )
        if not modified_raw or not isinstance(modified_raw, str):
            print("[AGENT 3 FAILED] Style modification variant mapping returned an empty layout payload.")
            st.error("⚠️ Pipeline Failure: Agent 3 style refactoring variant returned an empty payload.")
            return current_svg
            
        return self._extract_svg(modified_raw, "AGENT 3")
