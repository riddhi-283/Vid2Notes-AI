# utils/crew/agents.py
import os, json
from crewai import Agent
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

note_agent = Agent(
    role="Lecture Note Expert",
    goal="Convert raw transcript into clean, structured notes with grammar correction and formatting",
        backstory="You are a senior academic note-taker with years of experience. You never add or remove information. You only structure it beautifully with headings, subheadings, and bullet points wherever required.",
    llm=llm,
    verbose=True,
    memory=True,
)
