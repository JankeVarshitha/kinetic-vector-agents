import os
import streamlit as st
from huggingface_hub import InferenceClient

class HuggingFaceBridge:
    """Encapsulates secure connection protocol topologies for remote Hugging Face compute engines."""
    def __init__(self, hf_token: str):
        # Initializing the high-performance remote reasoning architecture
        self.client = InferenceClient("meta-llama/Llama-3.3-70B-Instruct", token=hf_token)
        
    def request_inference(self, system_prompt: str, user_prompt: str) -> str:
        """Executes a low-temperature chat completion call optimized for serverless inference structures."""
        try:
            # Shifted from text_generation to chat_completion to conform to modern routing contracts
            response = self.client.chat_completion(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=2048,
                temperature=0.1,  # Kept low to enforce clean code geometry structures
                top_p=0.95
            )
            # Extracts the clean string payload from the structured chat completion message block
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Hugging Face Infrastructure Exception: {str(e)}")
            return ""
