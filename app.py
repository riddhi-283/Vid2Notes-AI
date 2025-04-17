## MAIN STREAMLIT APP
import streamlit as st
from utils.helpers import extract_transcript
from utils.crew.crew_manager import run_lecture_note_crew, run_html_formatter_crew, run_qa_agent
import re, os
from utils.html_formatter import html_to_pdf

st.set_page_config(page_title="YouTube to Notes PDF", layout="centered")
st.title("🎓 YouTube Lecture Notes Generator")


st.markdown(
    """
    <style>
    .chat-container {
        position: fixed;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        background-color: #ffffff;
        padding: 10px;
        width: 80%;
        border: 1px solid #ccc;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        z-index: 9999;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# with st.container():
#     st.markdown('<div class="chat-container">', unsafe_allow_html=True)
#     user_question = st.text_input("💬 Chat with Gemini", key="gen_chat_input")
#     if st.button("Ask GPT"):
#         if user_question:
#             with st.spinner("Thinking..."):
#                 response = run_qa_agent(user_question)
#                 st.success(response)
#     st.markdown('</div>', unsafe_allow_html=True)

download_ready = False
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
            print("Notes creation done!")
        
        #  Step 3: Beautify Notes with Gemini Agent
        with st.spinner("🎨 Formatting notes with Gemini agent..."):
            html_string = run_html_formatter_crew(formatted_notes)
            print("HTML formatting done!")

        #  Step 4: Convert to Styled PDF
        with st.spinner("📄 Generating Gemini-styled PDF..."):
            pdf_path = html_to_pdf(html_string)
            print("PDF creation done!")
            download_ready = True

        # Step 5: Get topic from notes to name the PDF
        match = re.search(r"#+\s*(.+)", formatted_notes)
        if match:
            topic_title = match.group(1).strip().lower().replace(" ", "_")
            print(topic_title)
            download_filename = f"{topic_title}_notes.pdf"

        #  Final download
        if(download_ready):
            st.success("✅ Download PDF Notes from sidebar!")
            with st.sidebar:
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Notes as PDF",
                        data=f,
                        file_name=f"{download_filename}.pdf",
                        mime="application/pdf"
                    )
        else:
            st.write("PDF NOT DOWNLOADABLE!!")
        
    except Exception as e:
        st.error(f"❌ Error: {e}")

