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
            "max_tokens": 150, 
        }

        try:
            response = requests.post(f"{self.base_url}/completions", json=data, headers=headers)
            response.raise_for_status()
            print(response.json())
            return response.json()["choices"][0]["text"]
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con xAI: {e}")
            return None
