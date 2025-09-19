import requests
import os

OLLAMA_SERVER_URL = "http://" + os.getenv('LLM_SERVER') + "/api/chat"

def call_model(payload):
    return requests.post(OLLAMA_SERVER_URL, json=payload)