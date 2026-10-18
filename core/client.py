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
        """Executes a direct raw HTTP POST request optimized for fast, zero-timeout layout generation."""
        selected_model = "nvidia/nemotron-3.5-super-vl-120b-a12b"
        headers = {
            "Authorization": f"Bearer {self.nim_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": selected_model,
            "max_tokens": 4096, # Bumped to 1536 to allow large SVG visual assets to compile fully
            "stream": False,  
            "temperature": 0.2, 
            "top_p": 0.95,
            "top_k": 64,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "seed": 42,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
        }

        try:
            response = requests.post(
                url=self.url, 
                headers=headers, 
                json=payload, 
                timeout=60
            )

            if response.status_code != 200:
                st.error(f"❌ NVIDIA NIM Gateway Error ({response.status_code})")
                st.code(response.text, language="json")
                return ""
            
            response_json = response.json()
            
            if 'choices' in response_json and len(response_json['choices']) > 0:
                choice_node = response_json['choices'][0]
                if 'message' in choice_node:
                    content = choice_node['message'].get('content')
                    if content:
                        return content
            
            st.error("❌ NIM Response Topology Conflict or Empty Content Field.")
            st.code(json.dumps(response_json, indent=2), language="json")
            return ""
                
        except requests.exceptions.Timeout:
            st.error("⏳ Connection Timeout: The remote NVIDIA server took too long to respond.")
            return ""
        except Exception as e:
            st.error(f"💥 Client Layer Exception: {str(e)}")
            return ""
