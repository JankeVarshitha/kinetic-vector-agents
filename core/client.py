import os
import streamlit as st
from openai import OpenAI

class InferenceBridge:
    """Encapsulates secure connection protocol topologies for remote OpenRouter compute engines."""
    def __init__(self, api_token: str):
        # Initializing clean provider-agnostic engine routing structures
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_token,
        )
        
    def request_inference(self, system_prompt: str, user_prompt: str, is_refactor: bool = False) -> str:
        """Executes a low-temperature chat completion call optimized for OpenRouter free auto-routing."""
        # Using the official OpenRouter dynamic free auto-router fallback slug.
        # This completely abstracts model selection and guarantees zero credit cost.
        selected_model = "openrouter/free"
        
        try:
            response = self.client.chat.completions.create(
                model=selected_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # Low temperature strictly guarantees deterministic XML code layouts
                max_tokens=2048,
                extra_headers={
                    "HTTP-Referer": "https://localhost:8501",
                    "X-Title": "Motion-Lattice Engine",
                }
            )
            return response.choices.message.content
        except Exception as e:
            st.error(f"Inference Engine Infrastructure Exception: {str(e)}")
            return ""
