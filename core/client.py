import os
import streamlit as st
from openai import OpenAI

class InferenceBridge:
    """Encapsulates secure connection protocol topologies for remote OpenRouter compute engines."""
    def __init__(self, api_token: str):
        self.client = OpenAI(
            base_url="https://openrouter.ai/",
            api_key=api_token,
        )
        
    def request_inference(self, system_prompt: str, user_prompt: str, is_refactor: bool = False) -> str:
        """Executes a low-temperature chat completion call optimized for OpenRouter free auto-routing."""
        selected_model = "openrouter/free"
        
        # --- DYNAMIC PRODUCTION REFERER IDENTIFICATION ---
        # Automatically detects the live Streamlit URL or falls back gracefully during local testing
        try:
            # Safely fetches the active request context from the running Streamlit web server
            from streamlit.runtime.scriptrunner import get_script_run_ctx
            ctx = get_script_run_ctx()
            # If deployed in the cloud, extract host details; else default to local port signatures
            referer_url = st.secrets.get("STREAMLIT_APP_URL", "https://localhost:8501")
        except Exception:
            referer_url = "https://localhost:8501"
        
        try:
            response = self.client.chat.completions.create(
                model=selected_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  
                max_tokens=2048,
                extra_headers={
                    "HTTP-Referer": referer_url,
                    "X-Title": "Motion-Lattice Engine",
                }
            )
            
            if not response or not hasattr(response, 'choices'):
                st.error("Invalid structural response packet returned from gateway.")
                return ""
                
            choices = response.choices
            
            # Unpack options list arrays cleanly to verify indices
            if isinstance(choices, list) and len(choices) > 0:
                target_choice = choices[0]
            elif hasattr(choices, '__getitem__') and len(choices) > 0:
                target_choice = choices[0]
            else:
                st.error("Unable to navigate the response choice arrays.")
                return ""
                
            if hasattr(target_choice, 'message') and hasattr(target_choice.message, 'content'):
                return target_choice.message.content
            elif isinstance(target_choice, dict) and 'message' in target_choice:
                msg = target_choice['message']
                return msg.get('content', '') if isinstance(msg, dict) else getattr(msg, 'content', '')
            else:
                return getattr(target_choice, 'text', '')
                
        except Exception as e:
            st.error(f"Inference Engine Infrastructure Exception: {str(e)}")
            return ""
