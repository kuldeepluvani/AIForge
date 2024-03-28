import argparse
from youtube_transcript_api import YouTubeTranscriptApi
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from clients.ollama_client import call_llama_api


class YouTubeVideoSummariser:
    def __init__(self, video_id):
        self.video_id = video_id

    def fetch_transcript(self):
        api_response = YouTubeTranscriptApi.get_transcript(self.video_id)
        transcript = " ".join(item['text'] for item in api_response)
        if not transcript:
            print("Failed to fetch transcript for the given video")
            exit(1)
        return transcript

    def main(self):
        print("Fetching transcript for the given video...")
        transcript = self.fetch_transcript()
        print(f"Transcript fetched, length: {len(transcript)} characters")
        tldr_response = call_llama_api(prompt=transcript, pre_prompt="Write a summary of given youtube video transcript in fewer words that summarizes entire video", post_prompt=".")
        print(f"TLDR response: {tldr_response}")
        return tldr_response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize a YouTube video")
    parser.add_argument("--video_id", type=str, help="The ID of the YouTube video to summarize")
    parser.add_argument("--url", type=str, help="The URL of the YouTube video to summarize")
    args = parser.parse_args()

    if args.video_id is None and args.url is None:
        print("Please provide either a video ID or a video URL")
        exit(1)
    else:
        if args.video_id is None:
            # Extract the video ID from the URL
            # url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            video_id = args.url.split("v=")[1]
            args.video_id = video_id

    summariser = YouTubeVideoSummariser(args.video_id)
    summariser.main()
