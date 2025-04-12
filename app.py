## MAIN STREAMLIT APP
import streamlit as st
from utils.helpers import extract_transcript, generate_pdf_from_text
from utils.crew.crew_manager import run_lecture_note_crew, run_html_formatter_crew
# from utils.pdf_beautifier import beautify_pdf
from utils.html_formatter import html_to_pdf

st.set_page_config(page_title="YouTube to Notes PDF", layout="centered")
st.title("🎓 YouTube Lecture Notes Generator")

with st.sidebar:
    st.header("📹 Input Video")
    youtube_url = st.text_input("Paste YouTube Video URL")
    confirm = st.button("Confirm")

if confirm and youtube_url:
    st.success("URL received!")

    try:
        #  Step 1: Extract Transcript
        with st.spinner("🔍 Extracting transcript..."):
            raw_transcript = extract_transcript(youtube_url)
            print("Transcript extraction done!")

        #  Step 2: Generate Raw Notes via Crew (GPT-4o)
        with st.spinner("🧠 Generating structured notes with GPT-4o..."):
            formatted_notes = run_lecture_note_crew(raw_transcript)
            print(formatted_notes)
            print("Notes creation done!")

        #  Step 3: Beautify Notes with Gemini Agent
        with st.spinner("🎨 Formatting notes with Gemini agent..."):
            html_string = run_html_formatter_crew(formatted_notes)
            print(html_string)
            print("HTML formatting done!")

        #  Step 4: Convert to Styled PDF
        with st.spinner("📄 Generating Gemini-styled PDF..."):
            pdf_path = html_to_pdf(html_string)
            print("PDF creation done!")
            print("Returning PDF path:", pdf_path)

        
        #  Final download
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

