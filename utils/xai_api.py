import requests
import os
from dotenv import load_dotenv

load_dotenv()

class XAIClient:
    def __init__(self):
        self.api_key = os.getenv("XAI_API_KEY")
        self.base_url = "https://api.x.ai/v1" 

    def send_prompt(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "prompt": prompt,
            "model":"grok-beta",
            "max_tokens": 100,
            "stop": ["<|eos|>"] 
        }

        try:
            response = requests.post(f"{self.base_url}/completions", json=data, headers=headers)
            response.raise_for_status()
            text_response = response.json()["choices"][0]["text"].strip().replace("<|eos|>", "").strip()
            
            return text_response
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con xAI: {e}")
            return None
