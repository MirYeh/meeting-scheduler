from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class MeetingRequest(BaseModel):
    summary: str = Field(..., description="Title of the meeting")
    description: Optional[str] = Field(None, description="Description of the meeting")
    start_time: datetime = Field(..., description="Start time of the meeting")
    end_time: datetime = Field(..., description="End time of the meeting")
    attendees: List[str] = Field(default_factory=list, description="List of attendee email addresses")
    location: Optional[str] = Field(None, description="Location of the meeting")
    timezone: str = Field(default="UTC", description="Timezone for the meeting") 