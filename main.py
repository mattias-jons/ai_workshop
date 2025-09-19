import requests
import os

# Public
OLLAMA_SERVER_URL = "http://" + os.getenv('LLM_SERVER') + "/api/generate"

# Available models: llama3.2, qwen3:30b, gpt-oss:20b, deepseek-r1:8b, deepseek-r1:32b, mistral
payload = {
    "model": "mistral",  # Change to your desired model
    "prompt": "Give me a recipe for a chocolate cake.",
    "stream": False
}

response = requests.post(OLLAMA_SERVER_URL, json=payload)
print(response.json())
print(response.json()['response'])
