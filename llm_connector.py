import os
import json
import time
from openai import OpenAI

# Load environment variables or tokens
try:
    from tokens import openrouter_key
except ImportError:
    openrouter_key = os.getenv('OPENROUTER_API_KEY')

# Validate environment variables
if not openrouter_key:
    raise ValueError("OpenRouter API Key must be set in environment variables")

class LLMClient:
    def __init__(self, retries=3, delay=1):
        self.client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=openrouter_key)
        self.retries = retries
        self.delay = delay
    
    def get_response(self, user_input):
        system_prompt = (
            "Traduce el mensaje del usuario al portugués brasileño coloquial. No pongas comillas ni corchetes. Tampoco agregues explicaciones ni comentarios."
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Mensaje para traducir: {user_input}"},
        ]

        for attempt in range(self.retries):
            try:
                response = self.client.chat.completions.create(
                    model="deepseek/deepseek-chat",
                    messages=messages
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == self.retries - 1:
                    raise
                time.sleep(self.delay)

def get_llm_response(user_input):
    """Main function to get translation response"""
    try:               
        llm_client = LLMClient()
        response = llm_client.get_response(user_input)
        return response
    except Exception as e:
        print(f"Error in get_llm_response: {e}")
        # Return a fallback message
        fallback_msg = "Lo siento, tuve un problema técnico. Por favor, intentá nuevamente en unos momentos."
        return fallback_msg
