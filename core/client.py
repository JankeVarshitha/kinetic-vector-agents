import os
import streamlit as st
from huggingface_hub import InferenceClient

class HuggingFaceBridge:
    """Encapsulates secure connection protocol topologies for remote Hugging Face compute engines."""
    def __init__(self, hf_token: str):
        # Initializing the high-performance remote reasoning architecture
        self.client = InferenceClient("meta-llama/Llama-3.3-70B-Instruct", token=hf_token)
        
    def request_inference(self, system_prompt: str, user_prompt: str) -> str:
        """Executes a low-temperature deterministic decoding call on remote HF nodes."""
        try:
            response = self.client.text_generation(
                prompt=f"<system>{system_prompt}</system>\n<user>{user_prompt}</user>",
                max_new_tokens=2048,
                temperature=0.1,  # Keeps structured outputs from syntax drifting
                top_p=0.95
            )
            return response
        except Exception as e:
            st.error(f"Hugging Face Infrastructure Exception: {str(e)}")
            return ""
