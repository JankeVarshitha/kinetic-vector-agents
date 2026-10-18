import os
import json
import requests
import streamlit as st

class NIMBridge:
    """Encapsulates raw request protocols targeting remote NVIDIA NIM inference engines."""
    def __init__(self, nim_token: str):
        self.nim_token = nim_token
        # Direct structural route targeting NVIDIA's cloud completion gateway
        self.url = "https://nvidia.com"
        
    def request_inference(self, system_prompt: str, user_prompt: str) -> str:
        """Executes a low-temperature POST request optimized for NVIDIA NIM free models."""
        # Configured to run the frontier-level reasoning model
        selected_model = "google/gemma-4-31b-it"
        
        headers = {
            "Authorization": f"Bearer {self.nim_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": selected_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            # Configured to conform strictly to partner-recommended sampling guidelines
            "temperature": 0.1,
            "max_tokens": 2048
        }
        
        try:
            response = requests.post(
                url=self.url,
                headers=headers,
                data=json.dumps(payload),
                timeout=45  # Extended threshold for processing dense vector layers
            )
            
            response.raise_for_status()
            response_json = response.json()
            
            # Direct extraction targeting choice array message contents
            if 'choices' in response_json and len(response_json['choices']) > 0:
                message_block = response_json['choices'][0]['message']
                return message_block.get('content', '')
            else:
                st.error("NIM Error: Response payload missing choices array topology.")
                return ""
                
        except requests.exceptions.HTTPError as http_err:
            st.error(f"NIM Gate Exception: {response.status_code} - {response.text}")
            return ""
        except Exception as e:
            st.error(f"NIM Runtime Exception: {str(e)}")
            return ""
