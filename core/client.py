import os
import json
import requests
import streamlit as st

class NIMBridge:
    """Encapsulates raw request protocols targeting remote NVIDIA NIM inference engines."""
    def __init__(self, nim_token: str):
        self.nim_token = nim_token
        # CORRECT FIXED ENDPOINT: Injects the official live completion cluster directly from your documentation
        self.url = "https://integrate.api.nvidia.com/v1/chat/completions"
        
    def request_inference(self, system_prompt: str, user_prompt: str) -> str:
        """Executes a direct raw HTTP POST request matching the NVIDIA NIM specification exactly."""
        # Restored the flagship model variant from your target documentation
        selected_model = "google/gemma-4-31b-it"
        
        headers = {
            "Authorization": f"Bearer {self.nim_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": selected_model,
            "max_tokens": 512,
            "stream": False,
            "temperature": 0.3,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "seed": 0,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
        
        try:
            # Executes the network handshake using the explicit JSON payload configuration mapping
            response = requests.post(
                url=self.url,
                headers=headers,
                json=payload,
                stream=False,
                timeout=45  # Injected high threshold to fully accommodate dense token calculation blocks
            )
            
            # Immediately trap network routing failures before unpacking string text variables
            if response.status_code != 200:
                st.error(f"NVIDIA NIM Gateway Error ({response.status_code}): {response.text}")
                return ""
                
            response_json = response.json()
            
            # Navigate the choices list index natively to capture inner assistant string elements
            if 'choices' in response_json and len(response_json['choices']) > 0:
                message_block = response_json['choices'][0]['message']
                return message_block.get('content', '')
            else:
                st.error("NVIDIA NIM Error: Response payload missing choices array topology.")
                return ""
                
        except Exception as e:
            st.error(f"NVIDIA NIM Execution Layer Exception: {str(e)}")
            return ""
