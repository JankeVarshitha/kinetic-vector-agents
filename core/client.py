import os
import json
import requests
import streamlit as st

class NIMBridge:
    """Encapsulates raw request protocols targeting remote NVIDIA NIM inference engines."""
    def __init__(self, nim_token: str):
        self.nim_token = nim_token
        self.url = "https://nvidia.com"
        
    def request_inference(self, system_prompt: str, user_prompt: str) -> str:
        """Executes a direct raw HTTP POST request optimized for ultra-low latency generation."""
        selected_model = "google/gemma-4-31b-it"
        
        headers = {
            "Authorization": f"Bearer {self.nim_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Speed Optimization: Explicitly command the model to bypass the heavy <|think|> routing layers
        optimized_system = (
            f"{system_prompt}\n"
            "CRITICAL OPERATIONAL CONSTRAINT: DO NOT use internal reasoning, thinking, or chain-of-thought layers. "
            "Bypass the <|think|> tokens entirely. Output the raw graphic vectors immediately without waiting."
        )
        
        payload = {
            "model": selected_model,
            "max_tokens": 512,       # Lower token ceiling drastically reduces processing time
            "stream": False,
            "temperature": 0.3,      # Faster token generation speed
            "top_p": 0.95,
            "seed": 42,
            "messages": [
                {"role": "system", "content": optimized_system},
                {"role": "user", "content": user_prompt}
            ]
        }
        
        try:
            response = requests.post(
                url=self.url,
                headers=headers,
                json=payload,
                stream=False,
                timeout=25  # Lower network window since we expect a rapid execution response
            )
            
            if response.status_code != 200:
                st.error(f"NVIDIA NIM Gateway Error ({response.status_code}): {response.text}")
                return ""
                
            response_json = response.json()
            
            if 'choices' in response_json and len(response_json['choices']) > 0:
                message_block = response_json['choices']['message']
                content = message_block.get('content', '')
                
                # Clean up any leftover thinking tag formatting artifacts if present
                if "<|channel>" in content:
                    content = re.sub(r"<\|channel\>thought\n.*\<channel\|>", "", content, flags=re.DOTALL)
                return content
            else:
                st.error("NVIDIA NIM Error: Response payload missing choices array topology.")
                return ""
                
        except requests.exceptions.Timeout:
            st.error("⏳ High-Latency Timeout: Upstream node is still running heavy calculations. Please re-run.")
            return ""
        except Exception as e:
            st.error(f"NVIDIA NIM Execution Layer Exception: {str(e)}")
            return ""
