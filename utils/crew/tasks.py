from pydantic import BaseModel

class NoteOutput(BaseModel):
    notes: str

from crewai import Task
from .agents import note_agent, formatting_agent


def get_note_task(transcript_text):
    return Task(
        description=(
            "Format the given YouTube transcript into professional and structured lecture notes. Add only appropriate structure (headings, subheadings, bullets) and correct grammar, but do not add or remove any information from the content. Only structure and beautify it.\n\n"
            f"Transcript:\n{transcript_text}"
        ),
        expected_output="Well-structured, grammatically correct, and formatted notes",
        agent=note_agent,
        output_json=NoteOutput
    )

def get_html_format_task(notes_text):
    return Task(
        description=(
            "You will receive lecture notes in plain text. Format them into clean, structured HTML using appropriate tags.\n"
            "Include:\n"
            "- <h1>, <h2>, <ul>, <p>, etc.\n"
            "- A Table of Contents at the top using internal anchor links\n"
            "- A modern color theme (dark blue headers, black body, white background)\n"
            "- Good spacing between sections\n"
            "⚠️ Do not add or remove any information. Just beautify and structure the input text.\n\n"
            f"Lecture Notes:\n{notes_text}"
        ),
        expected_output="Beautiful, valid HTML string with structure and styling",
        agent=formatting_agent
    )