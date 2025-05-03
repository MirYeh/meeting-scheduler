from fastapi.testclient import TestClient
from src.app.main import app
from datetime import datetime, timedelta
import pytest
from unittest.mock import patch

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_create_meeting_with_mock():
    # Mock the calendar service
    mock_event = {
        "id": "test_event_id",
        "htmlLink": "https://calendar.google.com/event",
        "summary": "Test Meeting",
        "description": "This is a test meeting",
        "start": {"dateTime": "2024-01-01T10:00:00", "timeZone": "UTC"},
        "end": {"dateTime": "2024-01-01T11:00:00", "timeZone": "UTC"},
        "attendees": [{"email": "test@example.com"}]
    }
    
    with patch('src.app.main.calendar_service.create_meeting') as mock_create:
        mock_create.return_value = mock_event
        
        start_time = datetime.now() + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        
        meeting_request = {
            "summary": "Test Meeting",
            "description": "This is a test meeting",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "attendees": ["test@example.com"],
            "timezone": "UTC"
        }
        
        response = client.post("/meetings", json=meeting_request)
        assert response.status_code == 200
        response_data = response.json()
        
        # Check only the static fields that we expect to match
        assert response_data["summary"] == mock_event["summary"]
        assert response_data["description"] == mock_event["description"]
        assert response_data["attendees"] == mock_event["attendees"]

@pytest.mark.asyncio
async def test_create_meeting_validation():
    # Test with invalid data
    invalid_request = {
        "summary": "Test Meeting",
        "start_time": "invalid-date",
        "end_time": "invalid-date",
        "attendees": ["not-an-email"]
    }
    
    response = client.post("/meetings", json=invalid_request)
    assert response.status_code == 422  # Validation error 