import json
import requests


LLAMA_API_URL = "http://localhost:11434/api/generate"


def call_llama_api(prompt, pre_prompt="", post_prompt=""):
    """Calls the Llama API and returns the TLDR response."""
    # "Write a summary in 50 words that summarizes [topic or keyword]."

    payload = json.dumps(
        {
            "model": "llama2",
            "prompt": f"{pre_prompt} {prompt} {post_prompt}",
            "stream": False
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", LLAMA_API_URL, headers=headers, data=payload)

    return response.json()["response"]
