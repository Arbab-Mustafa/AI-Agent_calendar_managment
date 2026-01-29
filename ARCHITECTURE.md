# 🗓️ AI Calendar Agent - Complete Architecture

## Project Overview

An autonomous AI agent that manages your calendar using natural language:

- **Schedule meetings** - "Schedule a meeting with John next Tuesday at 2 PM"
- **Reschedule** - "Move my 3 PM meeting to 4 PM"
- **Cancel** - "Cancel my afternoon meetings"
- **Suggest slots** - "Find a 1-hour slot tomorrow for team standup"
- **Conflict resolution** - Automatically resolves scheduling conflicts

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER BROWSER                         │
│              (React Frontend - Vercel)                   │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST API
                     ↓
┌─────────────────────────────────────────────────────────┐
│              PYTHON BACKEND (Render)                     │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Flask/FastAPI Server                           │   │
│  │  - Calendar Agent (LangChain + Ollama)         │   │
│  │  - Tool calling (calendar operations)          │   │
│  │  - NLP interpretation                          │   │
│  │  - Conflict resolution logic                   │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Local Ollama (Mistral)                         │   │
│  │  - Runs LLM inference for NLP                   │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │ Queries/Inserts
                     ↓
┌─────────────────────────────────────────────────────────┐
│         DATABASE (MongoDB Atlas FREE TIER)              │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Collections:                                     │   │
│  │  - users (name, email, preferences)             │   │
│  │  - events (title, start, end, description)      │   │
│  │  - preferences (user_id, availablity hours)     │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Tech Stack

| Component        | Technology                | Free? |
| ---------------- | ------------------------- | ----- |
| Frontend         | React.js                  | ✅    |
| Backend          | Python (Flask)            | ✅    |
| LLM              | Ollama (Mistral)          | ✅    |
| Agent Framework  | LangChain                 | ✅    |
| Database         | MongoDB Atlas (free tier) | ✅    |
| Frontend Hosting | Vercel                    | ✅    |
| Backend Hosting  | Render or Railway         | ✅    |

---

## 🗂️ Folder Structure

```
ai-agent/
├── frontend/                      # React app
│   ├── src/
│   │   ├── components/
│   │   │   ├── Calendar.js
│   │   │   ├── EventForm.js
│   │   │   ├── Chatbot.js
│   │   │   └── PreferencesModal.js
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   ├── public/
│   ├── package.json
│   └── .env
│
└── backend/                       # Python API
    ├── app.py                     # Flask server
    ├── calendar_agent.py          # LangChain agent logic
    ├── tools.py                   # Calendar tools
    ├── database.py                # MongoDB connection
    ├── requirements.txt
    ├── .env
    └── config.py
```

---

## 🔄 User Flow

```
1. User: "Schedule a team meeting next Friday at 3 PM"
                    ↓
2. Frontend sends request to Backend API
                    ↓
3. Backend Agent:
   - Processes natural language using Ollama
   - Extracts: event_title, date, time, attendees
   - Calls tool: check_conflicts()
   - Calls tool: schedule_event()
                    ↓
4. Database: Stores event
                    ↓
5. Agent responds: "✅ Scheduled team meeting for Friday at 3 PM"
                    ↓
6. Frontend shows updated calendar
```

---

## 🛠️ Calendar Tools (Function Calling)

Agent can call these tools:

1. **get_user_calendar()** - Fetch user's events
2. **schedule_event(title, start, end, attendees)** - Create event
3. **reschedule_event(event_id, new_start, new_end)** - Move event
4. **cancel_event(event_id)** - Delete event
5. **find_available_slots(duration, date_range)** - Get free slots
6. **check_conflicts(start, end)** - Check if time is available
7. **get_user_preferences()** - Get working hours, preferences
8. **set_user_preferences(working_hours, busy_times)** - Update preferences

---

## 📋 Database Schema

### Users Collection

```json
{
  "_id": ObjectId,
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": ISODate,
  "preferences": {
    "working_hours_start": "09:00",
    "working_hours_end": "18:00",
    "timezone": "UTC",
    "min_meeting_duration": 30
  }
}
```

### Events Collection

```json
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "title": "Team Standup",
  "description": "Daily standup meeting",
  "start": ISODate,
  "end": ISODate,
  "attendees": ["attendee1@email.com"],
  "location": "Conference Room A",
  "created_at": ISODate
}
```

---

## 🚀 Development Phases

### Phase 1: Backend Development

- [ ] Flask server setup
- [ ] MongoDB connection
- [ ] Calendar tools implementation
- [ ] LangChain + Ollama integration
- [ ] API endpoints

### Phase 2: Frontend Development

- [ ] React calendar component
- [ ] Chat interface
- [ ] Event creation/edit forms
- [ ] API integration

### Phase 3: Integration

- [ ] Connect frontend to backend
- [ ] End-to-end testing
- [ ] Error handling

### Phase 4: Deployment

- [ ] MongoDB Atlas setup
- [ ] Heroku/Render backend deployment
- [ ] Vercel frontend deployment
- [ ] Environment variables configuration

---

## 🔑 Key Features

✅ **Natural Language Processing** - "Schedule a meeting"
✅ **Conflict Detection** - Prevents double-booking
✅ **Smart Suggestions** - Suggests optimal times
✅ **User Preferences** - Respects working hours
✅ **Persistence** - Saves to database
✅ **Conversational** - Chat-like interaction

---

## 🎯 Success Metrics

- [ ] User can schedule events via natural language
- [ ] Calendar updates in real-time
- [ ] No conflicts occur
- [ ] Agent suggests available slots
- [ ] Preferences are remembered
- [ ] Full deployment working

---

Next: Let's start building the backend! 🏗️
