from google.oauth2 import service_account
from googleapiclient.discovery import build
import streamlit as st
import os

def export_to_google_docs(notes_text):
    try:
        creds = service_account.Credentials.from_service_account_file(
            "your-credentials.json",
            scopes=["https://www.googleapis.com/auth/documents"]
        )
        service = build("docs", "v1", credentials=creds)

        doc = service.documents().create(body={"title": "Lecture Notes"}).execute()
        doc_id = doc.get("documentId")

        requests = [
            {"insertText": {"location": {"index": 1}, "text": notes_text}}
        ]
        service.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()

        return f"https://docs.google.com/document/d/{doc_id}/edit"
    except Exception as e:
        st.error(f"❌ Error exporting to Google Docs: {e}")
        return None
