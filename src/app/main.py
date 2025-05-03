from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .calendar_service import CalendarService
from .models import MeetingRequest
from .config import settings

app = FastAPI(title="Google Calendar Meeting Scheduler")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

calendar_service = CalendarService()

@app.post("/meetings")
async def create_meeting(meeting_request: MeetingRequest):
    try:
        meeting = await calendar_service.create_meeting(meeting_request)
        return {"message": "Meeting created successfully", "meeting": meeting}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 