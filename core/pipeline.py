import re
import ast
import json
import streamlit as st
from core.client import NIMBridge

class KineticVectorEngine:
    """Orchestrates multi-agent pipelines generating dynamic structural layout shapes."""
    
    def __init__(self, nim_token: str):
        self.bridge = NIMBridge(nim_token=nim_token)

    def _compile_to_html(self, config: dict) -> str:
        """Compiles structural layout tokens into complex frontend graphical components."""
        bg = config.get("bg_color", "#0a0a0f")
        animation_speed = config.get("speed_multiplier", 1.0)
        
        css_rules = ""
        html_elements = ""
        
        for idx, component in enumerate(config.get("components", [])):
            c_id = component.get("id", f"element-{idx}")
            color = component.get("color", "#00f3ff")
            width = component.get("width", "100px")
            height = component.get("height", "100px")
            
            # Position offsets (allows stacking elements to form complex objects like heads/eyes)
            top_offset = component.get("top_offset_percent", 50)
            left_offset = component.get("left_offset_percent", 50)
            
            # Dynamic asset styling mapping based on model choices
            shape_type = component.get("shape", "circle").lower()
            border_style = "solid"
            border_radius = "0%"
            clip_path = ""
            bg_gradient = f"background: transparent;"

            if shape_type == "circle":
                border_radius = "50%"
                border_style = component.get("style", "dashed") # solid, dashed, dotted
            elif shape_type == "square":
                border_radius = "8px"
                border_style = "solid"
            elif shape_type == "capsule":
                border_radius = "50px"
                border_style = "solid"
            elif shape_type == "triangle":
                clip_path = "clip-path: polygon(50% 0%, 0% 100%, 100% 100%);"
                border_style = "none"
                bg_gradient = f"background: {color};"
            elif shape_type == "gear-teeth":
                border_radius = "50%"
                border_style = "dashed"
                # Heavy neon styling optimization
                css_rules += f"""
                .{c_id}::before {{
                    content: ''; position: absolute; top: -10px; left: -10px; right: -10px; bottom: -10px;
                    border-radius: 50%; border: 6px dotted {color}; transform: rotate(15deg);
                }}
                """

            direction = "spin-cw" if component.get("direction", "cw") == "cw" else "spin-ccw"
            duration = component.get("duration_seconds", 3.0) / animation_speed
            
            css_rules += f"""
            .{c_id} {{
                position: absolute;
                top: {top_offset}%; left: {left_offset}%;
                width: {width}; height: {height};
                margin-left: -{float(width.replace('px',''))/2}px;
                margin-top: -{float(height.replace('px',''))/2}px;
                border-radius: {border_radius};
                border: 5px {border_style} {color};
                box-shadow: 0 0 25px {color}, inset 0 0 15px {color};
                {bg_gradient}
                {clip_path}
                animation: {direction} {duration}s linear infinite;
            }}
            """
            html_elements += f'<div class="{c_id}"></div>\n'

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ background: {bg}; display: flex; justify-content: center; align-items: center; min-height: 100vh; overflow: hidden; margin: 0; }}
                .container {{ position: relative; width: 400px; height: 400px; border: 1px rgba(255,255,255,0.05) solid; }}
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
            "You are an expert design metadata compiler. Output ONLY a valid JSON object or Python dictionary. "
            "Combine multiple layout shapes together to represent the user's prompt (e.g. if a robot, use square for head, circles for glowing eyes, gear-teeth for time vortex). "
            "Do NOT include markdown syntax wraps (```python) and no conversation.\n\n"
            "Dictionary formatting parameters rules:\n"
            "- shape options: 'circle', 'square', 'capsule', 'triangle', 'gear-teeth'\n"
            "- style options (for circles): 'solid', 'dashed', 'dotted'\n"
            "- direction options: 'cw', 'ccw'\n"
            "- Use top_offset_percent and left_offset_percent (0-100) to arrange parts into an object layout structural sketch.\n\n"
            "Target exact structure framework:\n"
            "{'bg_color': '#hex', 'speed_multiplier': 1.0, 'components': [{'id': 'head', 'shape': 'square', 'color': '#hex', 'width': '120px', 'height': '120px', 'top_offset_percent': 40, 'left_offset_percent': 50, 'direction': 'cw', 'duration_seconds': 0.0}]}"
        )
        
        raw_output = self.bridge.request_inference(layout_system, f"Asset Target: {motion_intent}")
        if not raw_output:
            return ""
            
        dict_match = re.search(r'(\{[\s\S]*\})', raw_output)
        if not dict_match:
            st.error("❌ Failed to isolate config dictionary properties topology structure.")
            return ""
            
        clean_str = dict_match.group(1).strip()
        
        try:
            asset_config = ast.literal_eval(clean_str)
            return self._compile_to_html(asset_config)
        except Exception:
            try:
                asset_config = json.loads(clean_str.replace("'", '"'))
                return self._compile_to_html(asset_config)
            except Exception as e:
                st.error(f"❌ Structural Metadata Translation Failure: {str(e)}")
                return ""
