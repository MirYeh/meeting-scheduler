import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from src.app.calendar_service import CalendarService
from src.app.models import MeetingRequest

@pytest.fixture
def mock_credentials():
    with patch('src.app.calendar_service.Credentials') as mock_creds:
        mock_instance = MagicMock()
        mock_creds.from_authorized_user_info.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_service():
    with patch('src.app.calendar_service.build') as mock_build:
        mock_calendar = MagicMock()
        mock_calendar.events.return_value.insert.return_value.execute.return_value = {
            "id": "test_event_id",
            "htmlLink": "https://calendar.google.com/event"
        }
        mock_build.return_value = mock_calendar
        yield mock_calendar

@pytest.fixture
def calendar_service(mock_credentials, mock_service):
    with patch('builtins.open', create=True), \
         patch('json.load') as mock_json:
        mock_json.return_value = {
            "token": "test_token",
            "refresh_token": "test_refresh",
            "token_uri": "test_uri",
            "client_id": "test_id",
            "client_secret": "test_secret",
            "scopes": ["https://www.googleapis.com/auth/calendar"]
        }
        return CalendarService()

@pytest.fixture
def sample_meeting_request():
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    return MeetingRequest(
        summary="Test Meeting",
        description="This is a test meeting",
        start_time=start_time,
        end_time=end_time,
        attendees=["test@example.com"],
        timezone="UTC"
    )

@pytest.mark.asyncio
async def test_create_meeting(calendar_service, sample_meeting_request, mock_service):
    # Mock the calendar service response
    mock_event = {
        "id": "test_event_id",
        "htmlLink": "https://calendar.google.com/event",
        "summary": sample_meeting_request.summary,
        "start": {
            "dateTime": sample_meeting_request.start_time.isoformat(),
            "timeZone": sample_meeting_request.timezone
        },
        "end": {
            "dateTime": sample_meeting_request.end_time.isoformat(),
            "timeZone": sample_meeting_request.timezone
        }
    }
    
    mock_service.events.return_value.insert.return_value.execute.return_value = mock_event
    
    # Call the create_meeting method
    result = await calendar_service.create_meeting(sample_meeting_request)
    
    # Verify the result
    assert result == mock_event
    
    # Verify the service was called with correct parameters
    mock_service.events.return_value.insert.assert_called_once()
    call_args = mock_service.events.return_value.insert.call_args[1]
    assert call_args['body']['summary'] == sample_meeting_request.summary
    assert call_args['body']['description'] == sample_meeting_request.description
    assert call_args['body']['start']['dateTime'] == sample_meeting_request.start_time.isoformat()
    assert call_args['body']['end']['dateTime'] == sample_meeting_request.end_time.isoformat()
    assert call_args['body']['attendees'][0]['email'] == sample_meeting_request.attendees[0]

@pytest.mark.asyncio
async def test_create_meeting_with_location(calendar_service, mock_service):
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    meeting_request = MeetingRequest(
        summary="Test Meeting",
        description="This is a test meeting",
        start_time=start_time,
        end_time=end_time,
        attendees=["test@example.com"],
        location="Test Location",
        timezone="UTC"
    )
    
    mock_event = {
        "id": "test_event_id",
        "htmlLink": "https://calendar.google.com/event",
        "summary": meeting_request.summary,
        "location": meeting_request.location,
        "start": {
            "dateTime": meeting_request.start_time.isoformat(),
            "timeZone": meeting_request.timezone
        },
        "end": {
            "dateTime": meeting_request.end_time.isoformat(),
            "timeZone": meeting_request.timezone
        }
    }
    
    mock_service.events.return_value.insert.return_value.execute.return_value = mock_event
    
    result = await calendar_service.create_meeting(meeting_request)
    
    assert result == mock_event
    call_args = mock_service.events.return_value.insert.call_args[1]
    assert call_args['body']['location'] == meeting_request.location

@pytest.mark.asyncio
async def test_create_meeting_error_handling(calendar_service, sample_meeting_request, mock_service):
    # Mock an error from the Google Calendar API
    mock_service.events.return_value.insert.return_value.execute.side_effect = Exception("API Error")
    
    with pytest.raises(Exception) as exc_info:
        await calendar_service.create_meeting(sample_meeting_request)
    
    assert str(exc_info.value) == "Failed to create meeting: API Error" 