from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import json
import pickle
from typing import List, Dict, Any
from .models import MeetingRequest

class CalendarService:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    TOKEN_FILE = 'token.json'
    CREDENTIALS_FILE = 'credentials.json'

    def __init__(self):
        self.credentials = self._get_credentials()
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def _get_credentials(self):
        creds = None
        if os.path.exists(self.TOKEN_FILE):
            with open(self.TOKEN_FILE, 'r') as token:
                creds = Credentials.from_authorized_user_info(json.load(token), self.SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDENTIALS_FILE,
                    self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save the credentials
            with open(self.TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        
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