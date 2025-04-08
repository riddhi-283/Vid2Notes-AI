from crewai import Crew
from .tasks import get_note_task
from .agents import note_agent  # Needed for crew creation

def run_lecture_note_crew(transcript_text: str) -> str:
    task = get_note_task(transcript_text)

    crew = Crew(
        agents=[note_agent],
        tasks=[task],
        verbose=False
    )

    result = crew.kickoff()
    return result
