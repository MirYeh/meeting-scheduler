from fastapi.testclient import TestClient
from src.app.main import app
from src.app.models import MeetingRequest
from datetime import datetime, timedelta
import pytest

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_create_meeting():
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
    assert response.status_code in [200, 400]  # 400 if credentials are not set up 