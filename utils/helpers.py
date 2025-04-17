from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from fpdf import FPDF
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textwrap import wrap

def extract_transcript(video_url: str) -> str:
    parsed_url = urlparse(video_url)
    
    # Check for short URL like youtu.be/<video_id>
    if "youtu.be" in parsed_url.netloc:
        video_id = parsed_url.path.strip("/")
    # Standard YouTube URL with v=VIDEO_ID
    elif "youtube.com" in parsed_url.netloc:
        query = parse_qs(parsed_url.query)
        video_id = query.get("v", [None])[0]
    else:
        raise ValueError("Unsupported YouTube URL format.")
    
    if not video_id:
        raise ValueError("Could not extract video ID from the URL.")

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        raise RuntimeError(f"Transcript could not be retrieved: {e}")

    full_text = " ".join([segment['text'] for segment in transcript])
    return full_text


## only for checking
# if __name__ == "__main__":
#     print(extract_transcript("https://youtu.be/_d0duu3dED4?si=1L-excA-HnOEhpX0"))
