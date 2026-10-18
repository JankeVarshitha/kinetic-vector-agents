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
        
        payload = {
            "model": selected_model,
            "max_tokens": 512, 
            "stream": False,  # Kept False to align with single chunk json mapping
            "temperature": 0.2, # Lowered from 1.0 to increase token computation speed and predictability
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
        
        print("\n" + "="*60)
        print(f"[DEBUG NIM CLIENT] Initiating Outbound Request to {selected_model}")
        print(f"[DEBUG NIM CLIENT] Payload Configuration: max_tokens=512, stream=False, temp=0.2")
        print(f"[DEBUG NIM CLIENT] User Prompt Snippet: {user_prompt[:100]}...")
        print("="*60 + "\n")

        try:
            # Lowered socket timeout slightly to crash faster for testing if the node hangs completely
            response = requests.post(
                url=self.url, 
                headers=headers, 
                json=payload, 
                stream=False, 
                timeout=45 
            )
            
            print(f"[DEBUG NIM CLIENT] HTTP Status Code Received: {response.status_code}")
            
            if response.status_code != 200:
                print(f"[DEBUG NIM CLIENT ERROR] Status code unhandled. Raw response text:\n{response.text}")
                st.error(f"NVIDIA NIM Gateway Error ({response.status_code}): {response.text}")
                return ""
            
            response_json = response.json()
            print("[DEBUG NIM CLIENT] JSON successfully parsed from response object.")
            
            if 'choices' in response_json and len(response_json['choices']) > 0:
                message_block = response_json['choices'][0]['message']
                content = message_block.get('content', '')
                
                print("\n" + "-"*40)
                print(f"[DEBUG NIM CLIENT] RAW LLM OUTPUT RECEIVED (Length: {len(content)} chars):")
                print(content)
                print("-"*40 + "\n")
                
                return content
            else:
                print("[DEBUG NIM CLIENT ERROR] Target 'choices' array topology is completely missing from payload.")
                print(f"[DEBUG NIM CLIENT ERROR] Full Payload received:\n{json.dumps(response_json, indent=2)}")
                st.error("NVIDIA NIM Error: Response payload missing choices array topology.")
                return ""
                
        except requests.exceptions.Timeout:
            print("[DEBUG NIM CLIENT TIMEOUT] Upstream connection timed out at socket configuration limits.")
            st.error("⏳ High-Latency Network Timeout: Upstream node took longer than expected to return. Please re-run.")
            return ""
        except Exception as e:
            print(f"[DEBUG NIM CLIENT EXCEPTION] Critical execution failure: {str(e)}")
            st.error(f"NVIDIA NIM Execution Layer Exception: {str(e)}")
            return ""
