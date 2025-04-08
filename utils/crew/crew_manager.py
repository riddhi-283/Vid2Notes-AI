from crewai import Crew
from .tasks import get_note_task
from .agents import note_agent  # Needed for crew creation
import streamlit as st
import json

def run_lecture_note_crew(transcript_text: str) -> str:
    task = get_note_task(transcript_text)

    crew = Crew(
        agents=[note_agent],
        tasks=[task],
        verbose=False
    )

    result = crew.kickoff()
    # print(dir(result))
    # print(type(result))
    # print("\n")
    # print(result)

     # 👇 Check its dict representation
    if hasattr(result, "to_dict"):
        result_dict = result.to_dict()
    elif hasattr(result, "return_values") and isinstance(result.return_values, dict):
        result_dict = result.return_values
    else:
        try:
            result_dict = dict(result)
        except:
            st.error("❌ Could not convert result to dictionary.")
            return None

    notes = result_dict.get("notes")

    if not notes:
        st.error("❌ Notes were not generated properly.")
    else:
        st.text_area("📝 Generated Notes", notes, height=500)

    return notes
