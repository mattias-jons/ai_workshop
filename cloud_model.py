import os
import requests


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"


def call_model(payload):

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload["model"] = "gpt-4"

    return requests.post(OPENAI_ENDPOINT, headers=headers, json=payload)
