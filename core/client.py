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
            "max_tokens": 512,
            "stream": False,  # Explicitly turned off to allow complete content mapping
            "temperature": 0.2, # Lowered for faster token generation speed
            "top_p": 0.95,
            "top_k": 64,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "seed": 42,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }

        try:
            # Shortened timeout to 30 seconds to fail fast rather than hanging for a minute
            response = requests.post(
                url=self.url, 
                headers=headers, 
                json=payload, 
                timeout=360
            )

            st.code(response)
            
            if response.status_code != 200:
                st.error(f"❌ NVIDIA NIM Gateway Error ({response.status_code})")
                st.code(response.text, language="json")
                return ""
            
            response_json = response.json()
            
            # SAFE TOPOLOGY PARSING: Checks array structures safely to prevent hidden crash loops
            if 'choices' in response_json and len(response_json['choices']) > 0:
                choice_node = response_json['choices'][0]
                if 'message' in choice_node and 'content' in choice_node['message']:
                    return choice_node['message']['content']
            
            st.error("❌ NIM Response Topology Conflict: Missing 'choices[0].message.content'")
            st.code(json.dumps(response_json, indent=2), language="json")
            return ""
                
        except requests.exceptions.Timeout:
            st.error("⏳ Connection Timeout: The remote NVIDIA server took over 30s to process this request.")
            return ""
        except Exception as e:
            st.error(f"💥 Client Layer Exception: {str(e)}")
            return ""
