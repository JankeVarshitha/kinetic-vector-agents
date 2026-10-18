import os
import streamlit as st
from huggingface_hub import InferenceClient

class HuggingFaceBridge:
    """Encapsulates secure connection protocol topologies for remote Hugging Face compute engines."""
    def __init__(self, hf_token: str):
        # Swapped to Mistral-7B-Instruct-v0.3 which handles structured code tasks 
        # beautifully and operates natively outside the premium 402 partner routing layers.
        self.client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.3", token=hf_token)
        
    def request_inference(self, system_prompt: str, user_prompt: str) -> str:
        """Executes a low-temperature chat completion call optimized for serverless inference structures."""
        try:
            response = self.client.chat_completion(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=2048,
                temperature=0.1,  # Strict decoding constraint for valid XML tags
                top_p=0.95
            )
            return response.choices.message.content
        except Exception as e:
            st.error(f"Hugging Face Infrastructure Exception: {str(e)}")
            return ""
