import os
import streamlit as st
from openai import OpenAI

class HuggingFaceBridge:
    """Encapsulates secure connection protocol topologies for remote OpenRouter compute engines."""
    def __init__(self, hf_token: str):
        # We ingest hf_token as our OpenRouter key to maintain compatibility with your Streamlit UI sidebar input/secrets
        self.client = OpenAI(
            base_url="https://openrouter.ai",
            api_key=hf_token,
        )
        
    def request_inference(self, system_prompt: str, user_prompt: str, is_refactor: bool = False) -> str:
        """Executes a low-temperature chat completion call optimized for OpenRouter free inference routing."""
        # Dynamic model fallback routing based on task specialization
        # Gemma for heavy architectural layout synthesis; Cohere Code variant for precise palette updates
        selected_model = "cohere/north-mini-code:free" if is_refactor else "google/gemma-4-26b-a4b-it:free"
        
        try:
            response = self.client.chat.completions.create(
                model=selected_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # Kept low to guarantee deterministic XML layout strings
                max_tokens=2048,
                extra_headers={
                    "HTTP-Referer": "https://localhost:8501", # Optional referral telemetry tags
                    "X-Title": "Motion-Lattice Engine",
                }
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"OpenRouter Infrastructure Exception: {str(e)}")
            return ""
