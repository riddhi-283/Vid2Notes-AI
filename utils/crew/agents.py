# utils/crew/agents.py
import os, json
from crewai import Agent
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0.3)
# gemini_llm = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash-001",
#     temperature=0,
#     convert_system_message_to_human=True
# )

note_agent = Agent(
    role="Lecture Note Expert",
    goal="Convert raw transcript into clean, structured notes with grammar correction, formatting and a final summary section.",
        backstory="You are a senior academic note-taker with years of experience. You also append a concise summary at the end, covering all key points in bullet form. You never add or remove information. You only structure it beautifully with headings, subheadings, and bullet points wherever required.",
    llm=llm,
    verbose=True,
    memory=True,
)


formatting_agent = Agent(
    role="HTML Formatter",
    goal="Transform plain text lecture notes into structured HTML with table of contents and proper formatting.",
    backstory="You are an expert in HTML document design and formatting. You use semantic HTML tags but never alters content, only beautifies it.",
    llm=llm,
    verbose=True,
    memory=True,
)

qa_agent = Agent(
    role="Educational Assistant",
    goal="Answer all the questions asked by user in detail using your best knowledge.",
    backstory=(
        """You're a friendly and helpful AI assistant built to help users with everyday queries, explanations, and academic guidance. You're always helpful, concise, and clear."""
    ),
    llm=llm,
    verbose=True
)
