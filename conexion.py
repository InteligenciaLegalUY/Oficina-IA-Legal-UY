# conexion.py
import os
import openai
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_openai_client():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    return openai

def get_google_services():
    creds = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    drive = build('drive', 'v3', credentials=creds)
    sheets = build('sheets', 'v4', credentials=creds)
    return {"drive": drive, "sheets": sheets}
