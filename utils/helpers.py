from youtube_transcript_api import YouTubeTranscriptApi
from fpdf import FPDF
import re

def extract_transcript(video_url: str) -> str:
    video_id = re.search(r"(?<=v=)[^&#]+", video_url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    transcript = YouTubeTranscriptApi.get_transcript(video_id.group(0))
    full_text = " ".join([segment['text'] for segment in transcript])
    return full_text

def generate_pdf_from_text(formatted_text: str, file_path: str = "lecture_notes.pdf") -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in formatted_text.split('\n'):
        if line.strip() == "":
            pdf.ln()
        else:
            pdf.multi_cell(0, 10, line)
    
    pdf.output(file_path)
    return file_path
