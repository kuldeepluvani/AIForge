import requests
import json
import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from clients.ollama_client import call_llama_api
import requests
from bs4 import BeautifulSoup


def fetch_website_data(url):
    """Fetches basic website data from the given URL."""

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the following:
        title = soup.title.string if soup.title else None
        all_headers = [h.text.strip() for h in soup.find_all(["h1", "h2", "h3"])]
        links = [a['href'] for a in soup.find_all('a', href=True)]
        body = soup.find('body')

        if body:
            all_text = body.get_text(separator=" ", strip=True)
        else:
            all_text = "Unable to find body text"

        return {
            'title': title,
            'headers': all_headers,
            'links': links,
            'body_text': all_text
        }

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch data from a URL")
    parser.add_argument("--url", type=str, help="The URL to fetch data from")
    args = parser.parse_args()

    data = fetch_website_data(args.url)
    tldr_response = call_llama_api(prompt=data['body_text'], pre_prompt="Write a summary in 50 words that summarizes ", post_prompt=".")

    if tldr_response is not None:
        # Process the fetched data
        print(f"TLDR response: {tldr_response}")
    else:
        print("Failed to fetch data from the URL")
