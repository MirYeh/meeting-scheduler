# Google Calendar Meeting Scheduler

A Python backend service that allows users to create meetings in their Google Calendar through an HTTP API.

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Google Calendar API OAuth 2.0 credentials (credentials.json)

## Setup

1. Clone the repository
2. Set up Google Calendar API:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Calendar API
   - Create OAuth 2.0 credentials:
     - Go to "APIs & Services" > "Credentials"
     - Click "Create Credentials" > "OAuth client ID"
     - Choose "Desktop app" as the application type
     - Name it "Calendar Meeting Scheduler"
     - Download the credentials and save them as `credentials.json` in the project root

## Running with Docker

1. First-time setup:
   ```bash
   docker-compose up --build
   ```
   - The application will print an authorization URL
   - Copy the URL and open it in your browser
   - Sign in with your Google account
   - Grant the requested permissions
   - Copy the authorization code
   - Set it as an environment variable:
     ```bash
     export AUTH_CODE="your_authorization_code"
     ```

2. Run the application:
   ```bash
   docker-compose up
   ```

3. The API will be available at `http://localhost:8000`

## Running Locally

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn src.app.main:app --reload
   ```

## API Endpoints

- `POST /meetings`: Create a new meeting
  ```json
  {
    "summary": "Meeting Title",
    "description": "Meeting Description",
    "start_time": "2024-01-01T10:00:00",
    "end_time": "2024-01-01T11:00:00",
    "attendees": ["attendee@example.com"],
    "location": "Meeting Room",
    "timezone": "UTC"
  }
  ```

- `GET /health`: Health check endpoint

## Running Tests

```bash
pytest tests/
```

## Development

The project structure:
```
.
├── src/
│   └── app/
│       ├── main.py
│       ├── models.py
│       ├── calendar_service.py
│       └── config.py
├── tests/
│   └── test_main.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
``` 