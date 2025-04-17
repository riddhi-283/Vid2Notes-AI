from crewai import Crew
from .tasks import get_note_task, get_html_format_task, get_qa_task
from .agents import note_agent, formatting_agent, qa_agent  # Needed for crew creation
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
    
    # Check its dict representation
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
        st.write("📝 Generated Notes\n")
        st.write(notes)

    return notes

#  Function for AI-Powered HTML formatting for creating beautiful pdfs
def run_html_formatter_crew(plain_text_notes: str) -> str:
    task = get_html_format_task(plain_text_notes)

    crew = Crew(
        agents=[formatting_agent],
        tasks=[task],
        verbose=False
    )

    result = crew.kickoff()

    # Handle result extraction safely
    if hasattr(result, "return_values") and isinstance(result.return_values, dict):
        return result.return_values.get("output") or result.return_values.get("notes")
    elif hasattr(result, "output"):
        return result.output
    else:
        return str(result) 

# Function for handling queries asked by user 
def run_qa_agent(user_query: str) -> str:
    task = get_qa_task(user_query)

    crew = Crew(
        agents=[qa_agent],
        tasks=[task],
        verbose=False
    )

    result = crew.kickoff()
    return result.output if hasattr(result, "output") else result.return_values.get("output", None)
