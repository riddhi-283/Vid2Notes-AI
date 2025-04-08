## MAIN STREAMLIT APP
import streamlit as st
from utils.helpers import extract_transcript, generate_pdf_from_text
from utils.crew.crew_manager import run_lecture_note_crew

st.set_page_config(page_title="YouTube to Notes PDF", layout="centered")
st.title("🎓 YouTube Lecture Notes Generator")

with st.sidebar:
    st.header("📹 Input Video")
    youtube_url = st.text_input("Paste YouTube Video URL")
    confirm = st.button("Confirm")

if confirm and youtube_url:
    try:
        with st.spinner("🔍 Extracting transcript..."):
            raw_transcript = extract_transcript(youtube_url)

        with st.spinner("🧠 Running CrewAI to generate notes..."):
            formatted_notes = run_lecture_note_crew(raw_transcript)

        with st.spinner("📄 Generating PDF..."):
            pdf_path = generate_pdf_from_text(formatted_notes)

        st.success("✅ Notes generated successfully!")
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📥 Download Notes as PDF",
                data=f,
                file_name="Lecture_Notes.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"❌ Error: {e}")
