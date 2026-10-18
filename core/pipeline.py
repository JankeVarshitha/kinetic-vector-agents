import re
import ast
import streamlit as st
from core.client import NIMBridge

class KineticVectorEngine:
    """Orchestrates multi-agent pipelines generating minimal structural metadata."""
    
    def __init__(self, nim_token: str):
        self.bridge = NIMBridge(nim_token=nim_token)

    def _compile_to_html(self, config: dict) -> str:
        """Compiles minimal asset dictionary properties into high-performance HTML/CSS blocks."""
        # Visual theme configurations
        bg = config.get("bg_color", "#0a0a0f")
        animation_speed = config.get("speed_multiplier", 1.0)
        
        # Build style components dynamically from structural lists
        css_rules = ""
        html_elements = ""
        
        for idx, component in enumerate(config.get("components", [])):
            c_id = component.get("id", f"element-{idx}")
            color = component.get("color", "#00f3ff")
            size = component.get("size", "100px")
            direction = "spin-cw" if component.get("direction", "cw") == "cw" else "spin-ccw"
            duration = component.get("duration_seconds", 3.0) / animation_speed
            
            # Map parameters directly into clean CSS layout strings
            css_rules += f"""
            .{c_id} {{
                position: absolute;
                top: 50%; left: 50%;
                width: {size}; height: {size};
                margin-left: -{float(size.replace('px',''))/2}px;
                margin-top: -{float(size.replace('px',''))/2}px;
                border-radius: 50%;
                border: 8px dashed {color};
                box-shadow: 0 0 20px {color};
                animation: {direction} {duration}s linear infinite;
            }}
            """
            html_elements += f'<div class="{c_id}"></div>\n'

        # Full structural web bundle template block wrapper
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ background: {bg}; display: flex; justify-content: center; align-items: center; min-height: 100vh; overflow: hidden; margin: 0; }}
                .container {{ position: relative; width: 300px; height: 300px; }}
                {css_rules}
                @keyframes spin-cw {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
                @keyframes spin-ccw {{ 0% {{ transform: rotate(360deg); }} 100% {{ transform: rotate(0deg); }} }}
            </style>
        </head>
        <body>
            <div class="container">
                {html_elements}
            </div>
        </body>
        </html>
        """

    def build_animation(self, motion_intent: str) -> str:
        """Sequential layout-to-kinetic agent pipeline execution mapping."""
        layout_system = (
            "You are an expert design metadata compiler. Output ONLY a valid Python dictionary containing asset metadata attributes. "
            "Do NOT include any markdown code wraps (like ```python) and no conversation. "
            "Dictionary formatting structure MUST exactly match: "
            "{'bg_color': '#hex', 'speed_multiplier': 1.0, 'components': [{'id': 'gear1', 'color': '#hex', 'size': '160px', 'direction': 'cw', 'duration_seconds': 4.0}]}"
        )
        
        raw_output = self.bridge.request_inference(layout_system, f"Asset Target: {motion_intent}")
        if not raw_output:
            return ""
            
        # Strip code markdown characters if present
        clean_str = re.sub(r"```python|```", "", raw_output).strip()
        
        try:
            # Safely converts the string layout array directly into a live Python dictionary object
            asset_config = ast.literal_eval(clean_str)
            return self._compile_to_html(asset_config)
        except Exception as e:
            st.error(f"❌ Structural Metadata Translation Failure: {str(e)}")
            st.code(clean_str)
            return ""
