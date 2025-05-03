from src.app.calendar_service import CalendarService
from src.app.models import MeetingRequest
from datetime import datetime, timedelta
import asyncio

async def main():
    # Initialize the calendar service
    service = CalendarService()
    
    # Test creating a meeting
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    
    meeting_request = MeetingRequest(
        summary="Test Meeting",
        description="This is a test meeting",
        start_time=start_time,
        end_time=end_time,
        attendees=["miri.yehezkel+app@gmail.com"],
        timezone="Asia/Jerusalem"
    )
    
    try:
        event = await service.create_meeting(meeting_request)
        print("Meeting created successfully!")
        print(f"Event ID: {event['id']}")
        print(f"Meeting Link: {event.get('htmlLink')}")
    except Exception as e:
        print(f"Error creating meeting: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 