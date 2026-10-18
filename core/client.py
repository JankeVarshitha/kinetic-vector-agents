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
        selected_model = "google/gemma-4-31b-it"
        
        headers = {
            "Authorization": f"Bearer {self.nim_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Speed Optimization: Injects the official partner-recommended sampling parameters from documentation
        # to maximize token generation throughput and prevent 45-second network socket timeouts.
        payload = {
            "model": selected_model,
            "max_tokens": 512,       # Locked at 512 tokens to minimize processing latency
            "stream": False,
            "temperature": 1.0,      # Partner-recommended sampling configuration
            "top_p": 0.95,           # Partner-recommended sampling configuration
            "top_k": 64,             # Partner-recommended sampling configuration
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "seed": 42,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
        
        try:
            response = requests.post(
                url=self.url,
                headers=headers,
                json=payload,
                stream=False,
                timeout=60  # Increased socket limit to absorb dense structural computations safely
            )
            
            if response.status_code != 200:
                st.error(f"NVIDIA NIM Gateway Error ({response.status_code}): {response.text}")
                return ""
                
            response_json = response.json()
            
            if 'choices' in response_json and len(response_json['choices']) > 0:
                message_block = response_json['choices'][0]['message']
                return message_block.get('content', '')
            else:
                st.error("NVIDIA NIM Error: Response payload missing choices array topology.")
                return ""
                
        except requests.exceptions.Timeout:
            st.error("⏳ High-Latency Network Timeout: Upstream node took longer than 60s to return. Please re-run.")
            return ""
        except Exception as e:
            st.error(f"NVIDIA NIM Execution Layer Exception: {str(e)}")
            return ""
