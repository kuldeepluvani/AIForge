from typing import List

import json
import requests


LLAMA_API_URL = "http://localhost:11434/api/generate"
LLAMA_API_CHAT_URL = "http://localhost:11434/api/chat"


def call_llama_api(prompt, pre_prompt="", post_prompt="", model="llama2"):
    """Calls the text gen API"""

    payload = json.dumps(
        {
            "model": model,
            "prompt": f"{pre_prompt} {prompt} {post_prompt}",
            "stream": False
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", LLAMA_API_URL, headers=headers, data=payload)

    return response.json()["response"]


def call_llama_api_chat(messages: List, model="llama2"):
    """Calls the text gen API for chat"""

    payload = json.dumps(
        {
            "model": model,
            "messages": messages,
            "stream": False
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", LLAMA_API_CHAT_URL, headers=headers, data=payload)

    return response.json()
