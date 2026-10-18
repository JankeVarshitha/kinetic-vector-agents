import os
import json
import requests
import streamlit as st

class InferenceBridge:
    """Encapsulates raw request protocols targeting remote OpenRouter compute engines."""
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        
    def request_inference(self, system_prompt: str, user_prompt: str, is_refactor: bool = False) -> str:
        """Executes a direct raw HTTP POST request optimized for OpenRouter free inference models."""
        # Clean fallback routing matrix utilizing the verified free models
        selected_model = "cohere/north-mini-code:free" if is_refactor else "google/gemma-4-26b-a4b-it:free"
        
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://localhost:8501",
            "X-Title": "Motion-Lattice Engine"
        }
        
        payload = {
            "model": selected_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.1,  # Low temperature strictly guarantees deterministic XML layouts
            "reasoning": {"enabled": True}  # Enforces explicit reasoning paths on supported models
        }
        
        try:
            response = requests.post(
                url=self.url,
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )
            
            # Catch HTTP error payloads before parsing json structures
            response.raise_for_status()
            response_json = response.json()
            
            # Direct extraction targeting the assistant message dictionary content block
            if 'choices' in response_json and len(response_json['choices']) > 0:
                message_data = response_json['choices'][0]['message']
                return message_data.get('content', '')
            else:
                st.error("API Error: Response payload missing choices array topology.")
                return ""
                
        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP Infrastructure Exception: {response.status_code} - {response.text}")
            return ""
        except Exception as e:
            st.error(f"Inference Engine Runtime Exception: {str(e)}")
            return ""
