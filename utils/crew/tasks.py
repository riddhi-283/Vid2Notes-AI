from pydantic import BaseModel

class NoteOutput(BaseModel):
    notes: str

from crewai import Task
from .agents import note_agent

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
