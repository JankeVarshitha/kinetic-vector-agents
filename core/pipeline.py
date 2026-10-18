import re
from core.client import HuggingFaceBridge

class MotionLatticeEngine:
    """Orchestrates multi-agent pipelines for multi-tier visual syntax compiling."""
    def __init__(self, hf_token: str):
        self.bridge = HuggingFaceBridge(hf_token=hf_token)

    def build_animation(self, motion_intent: str) -> str:
        """Sequential layout-to-kinetic agent pipeline execution mapping."""
        layout_system = (
            "You are an expert Frontend AI Architect specializing in raw vector layout design. "
            "Generate ONLY valid, clean, modern, semantic SVG code. "
            "Do NOT include any markdown code blocks (like ```xml), no text outside the SVG tags, and no explanations. "
            "Assign explicit semantic IDs to critical animated components (e.g., id='ball', id='wing')."
        )
        base_svg = self.bridge.request_inference(layout_system, f"Asset Target: {motion_intent}")
        base_svg = re.sub(r"```xml|```", "", base_svg).strip()

        animation_system = (
            "You are a Senior SVG Kinetic Designer. Take the provided SVG code and inject a high-performance "
            "<style> block containing fluid, looping CSS @keyframes animations targeting semantic element IDs. "
            "Output ONLY the complete, newly combined raw SVG code. No markdown, no text explanations."
        )
        animated_svg = self.bridge.request_inference(animation_system, f"Theme: '{motion_intent}'.\n\nBase SVG:\n{base_svg}")
        return re.sub(r"```xml|```", "", animated_svg).strip()

    def modify_style(self, current_svg: str, style_modification_prompt: str) -> str:
        """Refactors active vector DOM states by selectively isolating and overriding color definitions."""
        refactor_system = (
            "You are a Senior SVG Technical Lead. Modify the color palette/gradients of the following SVG "
            "strictly adhering to the user's styling instruction. Keep all vector layout geometry, path IDs, "
            "and keyframe animations untouched. Output ONLY the modified complete raw SVG code."
        )
        # Passing is_refactor=True explicitly targets the Cohere North Code model route
        modified_svg = self.bridge.request_inference(refactor_system, f"Mutation Request: {style_modification_prompt}\n\nCurrent SVG:\n{current_svg}", is_refactor=True)
        return re.sub(r"```xml|```", "", modified_svg).strip()

