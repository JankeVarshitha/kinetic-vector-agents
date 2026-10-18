import os
import streamlit as st
from huggingface_hub import InferenceClient

class HuggingFaceBridge:
    """Encapsulates secure connection protocol topologies for remote Hugging Face compute engines."""
    def __init__(self, hf_token: str):
        # Swapped to Llama-3.1-8B-Instruct which routes natively on Hugging Face free internal clusters.
        # This acts as an architectural guard against the 402 billing node errors.
        self.client = InferenceClient("meta-llama/Llama-3.1-8B-Instruct", token=hf_token)
        
    def request_inference(self, system_prompt: str, user_prompt: str) -> str:
        """Executes a low-temperature chat completion call optimized for serverless inference structures."""
        try:
            response = self.client.chat_completion(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=2048,
                temperature=0.1,  # Low temperature guarantees syntax strictness
                top_p=0.95
            )
            return response.choices.message.content
        except Exception as e:
            st.error(f"Hugging Face Infrastructure Exception: {str(e)}")
            return ""
