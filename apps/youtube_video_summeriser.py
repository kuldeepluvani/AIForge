import argparse
import os
from youtube_transcript_api import YouTubeTranscriptApi
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")  # Add parent dir to import path

from clients.ollama_client import call_llama_api


class YouTubeVideoSummariser:
    """
    A class for summarizing YouTube videos using transcripts and a large language model (LLM).
    """

    def __init__(self, video_id):
        """
        Initializes the YouTubeVideoSummariser object.

        Args:
            video_id (str): The ID of the YouTube video to summarize.
        """
        self.video_id = video_id

    def fetch_transcript(self):
        """
        Fetches the transcript for the YouTube video using the YouTube Transcript API.

        Returns:
            str: The concatenated transcript text.

        Raises:
            SystemExit: If the transcript cannot be fetched.
        """
        api_response = YouTubeTranscriptApi.get_transcript(self.video_id)
        transcript = " ".join(item['text'] for item in api_response)
        if not transcript:
            print("Failed to fetch transcript for the given video")
            exit(1)
        return transcript

    def main(self):
        """
        Orchestrates the video summarization process.

        Fetches the transcript, calls the LLM (e.g. Ollama) to generate a summary,
        and prints the summary.

        Returns:
            str: The TLDR (summary) response from the LLM.
        """
        print("Fetching transcript for the given video...")
        transcript = self.fetch_transcript()
        print(f"Transcript fetched, length: {len(transcript)} characters")

        # Construct a clear prompt for the LLM
        prompt = f"Write a summary of this YouTube video transcript in fewer words, summarizing the entire video:\n{transcript}"
        tldr_response = call_llama_api(prompt=prompt)  # Assuming Ollama format

        print(f"TLDR response: {tldr_response}")
        return tldr_response


if __name__ == "__main__":
    """
    Parses command-line arguments and initiates the YouTube video summarization process.
    """
    parser = argparse.ArgumentParser(description="Summarize a YouTube video")
    parser.add_argument("--video_id", type=str, help="The ID of the YouTube video to summarize")
    parser.add_argument("--url", type=str, help="The URL of the YouTube video to summarize")
    args = parser.parse_args()

    if not (args.video_id or args.url):  # Check if either ID or URL is provided
        print("Please provide either a video ID or a video URL")
        exit(1)

    if args.url:  # Handle URL input
        video_id = args.url.split("v=")[1]
        args.video_id = video_id

    summariser = YouTubeVideoSummariser(args.video_id)
    summariser.main()
