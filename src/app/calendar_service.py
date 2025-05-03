from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime
import os
import pickle
from typing import Dict, Any
from .models import MeetingRequest

class CalendarService:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    TOKEN_FILE = 'token.pickle'
    CREDENTIALS_FILE = 'credentials.json'

    def __init__(self):
        self.credentials = self._get_credentials()
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def _get_credentials(self) -> Credentials:
        creds = None
        if os.path.exists(self.TOKEN_FILE):
            with open(self.TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.CREDENTIALS_FILE):
                    raise Exception("credentials.json file not found. Please set up Google Calendar API credentials.")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDENTIALS_FILE, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(self.TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
        
        return creds

    async def create_meeting(self, meeting_request: MeetingRequest) -> Dict[str, Any]:
        event = {
            'summary': meeting_request.summary,
            'description': meeting_request.description,
            'start': {
                'dateTime': meeting_request.start_time.isoformat(),
                'timeZone': meeting_request.timezone,
            },
            'end': {
                'dateTime': meeting_request.end_time.isoformat(),
                'timeZone': meeting_request.timezone,
            },
            'attendees': [{'email': email} for email in meeting_request.attendees],
            'location': meeting_request.location,
        }

        try:
            event = self.service.events().insert(
                calendarId='primary',
                body=event,
                sendUpdates='all'
            ).execute()
            return event
        except Exception as e:
            raise Exception(f"Failed to create meeting: {str(e)}") 