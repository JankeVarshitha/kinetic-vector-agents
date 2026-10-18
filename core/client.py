import os
import json
import requests
import streamlit as st

class NIMBridge:
    """Encapsulates raw request protocols targeting remote NVIDIA NIM inference engines."""
    def __init__(self, nim_token: str):
        self.nim_token = nim_token
        self.url = "https://integrate.api.nvidia.com/v1/chat/completions"
        
    def request_inference(self, system_prompt: str, user_prompt: str) -> str:
        """Executes a direct raw HTTP POST request matching the NVIDIA NIM specification exactly."""
        # Maintained the high-fidelity flagship reasoning model variant
        selected_model = "google/gemma-4-31b-it"
        
        headers = {
            "Authorization": f"Bearer {self.nim_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": selected_model,
            "max_tokens": 1024,
            "stream": False,
            "temperature": 0.1,  # Kept low to enforce strict XML/SVG syntax validation
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
            response = requests.post(
                url=self.url,
                headers=headers,
                json=payload,  # Swapped to native json= parameter to handle dump mapping automatically
                stream=False
            )
            
            # Catch raw HTTP protocol errors before attempting a JSON unpack operation
            if response.status_code != 200:
                st.error(f"NVIDIA NIM Gateway Error ({response.status_code}): {response.text}")
                return ""
                
            response_json = response.json()
            
            # --- SYNCHRONIZED PAYLOAD ACCESS ROUTE ---
            # Correctly navigates the list array topology index to capture raw assistant string content
            if 'choices' in response_json and len(response_json['choices']) > 0:
                message_block = response_json['choices'][0]['message']
                return message_block.get('content', '')
            else:
                st.error("NVIDIA NIM Error: Response payload missing choices array topology.")
                return ""
                
        except Exception as e:
            st.error(f"NVIDIA NIM Execution Layer Exception: {str(e)}")
            return ""
