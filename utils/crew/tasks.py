from pydantic import BaseModel

class NoteOutput(BaseModel):
    notes: str

from crewai import Task
from .agents import note_agent, formatting_agent, qa_agent


def get_note_task(transcript_text):
    return Task(
        description=(
            "Convert the given YouTube transcript into professional and structured lecture notes. "
            "Use headings, subheadings, and bullet points where appropriate, and correct grammar. "
            "At the end, add a clearly marked section titled '## Summary' that summarizes the full lecture in bullet points. "
            "Do not remove or add content except for formatting and the summary.\n\n"
            f"Transcript:\n{transcript_text}"
        ),
        expected_output="Well-structured, grammatically correct, and formatted notes with a final summary section in markdown format",
        agent=note_agent,
        output_json=NoteOutput
    )

def get_qa_task(user_query: str):
    return Task(
        description=(
            f"Answer the following question in a helpful, clear and descriptive way:\n\n"
            f"User: {user_query}"
        ),
        expected_output="A clear, descriptive and factually correct answer.",
        agent=qa_agent
    )

def get_html_format_task(notes_text):
    return Task(
        description=(
            "You will receive full lecture notes in plain text, including a final section titled '## Summary'. "
            "Your task is to convert this text into clean, styled HTML using appropriate semantic tags.\n\n"
            "Make sure to:\n"
            "- Use <h1>, <h2>, <p>, <ul>, and other proper HTML tags.\n"
            "- Include a Table of Contents at the top using internal anchor links to each section.\n"
            "- Apply a modern visual theme: dark blue headers, black body text, white background.\n"
            "- Ensure clean spacing between sections and consistent font styling.\n"
            "- Highlight the final 'Summary' section clearly in its own styled block.\n\n"
            "⚠️ Do NOT remove or invent any content. Only structure and beautify the input notes, keeping the '## Summary' at the end.\n\n"
            f"Lecture Notes:\n{notes_text}"
        ),
        expected_output="Beautiful, valid HTML string with structure and styling",
        agent=formatting_agent
    )