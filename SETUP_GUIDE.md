# 🗓️ AI Calendar Agent - Complete Setup Guide

## Project Complete! ✅

You now have a **full-stack AI calendar agent**:

- ✅ Python backend with Flask + Ollama integration
- ✅ React frontend with modern UI
- ✅ MongoDB database (ready for cloud)
- ✅ Calendar management with AI agent

---

## 🚀 Quick Start (Development)

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Make sure Ollama is running
# Open new terminal and run: ollama serve

# Run backend server
python app.py
```

Backend runs on: `http://localhost:5000`

### 2. Frontend Setup

```bash
# In new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:5000/api" > .env

# Start React dev server
npm start
```

Frontend runs on: `http://localhost:3000`

---

## 📦 Technology Stack

| Component | Tech             | Status       |
| --------- | ---------------- | ------------ |
| Frontend  | React 18         | ✅ Ready     |
| Backend   | Flask + Python   | ✅ Ready     |
| LLM       | Ollama (Mistral) | ✅ Ready     |
| Database  | MongoDB          | 🔄 Configure |
| Hosting   | TBD              | ⏳ Next      |

---

## 🗄️ Database Setup (MongoDB Atlas - FREE TIER)

### Step 1: Create MongoDB Account

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up (free tier available)
3. Create a new cluster (FREE tier)
4. Wait for cluster to be deployed (~5-10 min)

### Step 2: Get Connection String

1. Click "Connect"
2. Select "Connect your application"
3. Choose "Python" driver
4. Copy the connection string
5. Format: `mongodb+srv://username:password@cluster.mongodb.net/calendar_agent`

### Step 3: Add to Backend .env

```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/calendar_agent?retryWrites=true&w=majority
```

### Step 4: Test Connection

```bash
# Backend will automatically test the connection on startup
python app.py
# Look for: ✅ Connected to MongoDB
```

---

## 🎯 Features Implemented

### ✅ User Management

- Create user profile
- Store preferences (working hours, etc.)
- Retrieve user info

### ✅ Calendar Operations

- View calendar events
- Create new events
- Update existing events
- Delete events
- Check for conflicts

### ✅ AI Agent

- Natural language processing
- Intent extraction (schedule, cancel, etc.)
- Event scheduling via NLP
- Available slot suggestions
- Conflict detection

### ✅ Frontend

- Beautiful calendar view
- Chat interface with AI agent
- Event creation form
- Real-time updates

---

## 🔌 API Endpoints

### Users

- `POST /api/users` - Create user
- `GET /api/users/<user_id>` - Get user
- `PUT /api/users/<user_id>/preferences` - Update preferences

### Calendar

- `GET /api/calendar/<user_id>` - Get events
- `POST /api/calendar/<user_id>/events` - Create event
- `PUT /api/calendar/<user_id>/events/<event_id>` - Update event
- `DELETE /api/calendar/<user_id>/events/<event_id>` - Delete event

### AI Agent

- `POST /api/agent/<user_id>/process` - Process natural language request
- `POST /api/calendar/<user_id>/available-slots` - Find available times
- `POST /api/calendar/<user_id>/check-conflicts` - Check availability

---

## 🧪 Testing the System

### Via Chat Interface (Recommended)

1. Open http://localhost:3000
2. Type in chat: "Schedule a meeting tomorrow at 3 PM"
3. Agent will process and create the event
4. Calendar updates automatically

### Via API (Postman/cURL)

```bash
# Schedule an event
curl -X POST http://localhost:5000/api/agent/USER_ID/process \
  -H "Content-Type: application/json" \
  -d '{"request": "Schedule a meeting tomorrow at 2 PM"}'
```

---

## 🔍 How AI Agent Works

### User Flow:

```
User: "Schedule team meeting tomorrow at 3 PM"
              ↓
Frontend sends to Backend API
              ↓
Backend Agent:
1. Extracts intent: "schedule"
2. Parses: title="team meeting", time="3 PM", date="tomorrow"
3. Checks for conflicts
4. Creates event in database
5. Returns confirmation
              ↓
Frontend updates calendar
```

### Agent Logic:

The agent uses **local Ollama (Mistral)** to:

- Understand natural language
- Extract relevant information
- Determine the intent (schedule, cancel, suggest)
- Make decisions (check conflicts, find slots)

---

## 📊 Folder Structure

```
ai-agent/
├── backend/
│   ├── app.py                 # Flask server
│   ├── calendar_agent.py      # LangChain agent logic
│   ├── database.py            # MongoDB operations
│   ├── config.py              # Configuration
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment template
│   └── README.md              # Backend docs
│
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── Calendar.js
│   │   │   ├── ChatBot.js
│   │   │   ├── EventForm.js
│   │   │   └── *.css
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   ├── public/
│   ├── package.json
│   ├── .env.example
│   └── README.md              # Frontend docs
│
├── ARCHITECTURE.md            # System design
├── SETUP.md                   # This file
└── README.md                  # Project overview
```

---

## 🚢 Deployment (Next Steps)

### Backend Deployment (Render)

1. Push code to GitHub
2. Connect Render to GitHub
3. Deploy backend: `https://your-app.onrender.com`
4. Add environment variables in Render dashboard

### Frontend Deployment (Vercel)

1. Push code to GitHub
2. Connect Vercel to GitHub
3. Deploy frontend
4. Set environment variable: `REACT_APP_API_URL=https://your-app.onrender.com/api`

### Database (MongoDB Atlas)

- Already cloud-based (no deployment needed)
- Just add connection string to environment variables

---

## ⚡ Important Notes

### Ollama Requirements

- Ollama must be running locally (`ollama serve`)
- Mistral model must be downloaded (`ollama pull mistral`)
- Backend expects Ollama on `http://localhost:11434`

### MongoDB Options

- **Local**: `mongodb://localhost:27017/calendar_agent`
- **Cloud (MongoDB Atlas)**: Free tier, 512MB storage
- **Fallback**: In-memory (for testing without MongoDB)

### Frontend Environment

- Set `REACT_APP_API_URL` to your backend URL
- Default: `http://localhost:5000/api`

---

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check Ollama is running
ollama list  # Should show available models

# Check dependencies
pip list  # Should see flask, pymongo, etc.

# Check Python version
python --version  # Should be 3.8+
```

### Frontend won't load

```bash
# Check Node.js
node --version  # Should be 14+
npm list  # Check dependencies

# Clear cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Database connection error

```bash
# Local MongoDB
mongod  # Start MongoDB service

# MongoDB Atlas
# Make sure connection string is correct
# Check IP whitelist in Atlas dashboard
```

---

## 📚 Learning Resources

- [Ollama Docs](https://github.com/ollama/ollama)
- [LangChain Docs](https://python.langchain.com)
- [MongoDB Atlas Docs](https://docs.atlas.mongodb.com)
- [React Docs](https://react.dev)
- [Flask Docs](https://flask.palletsprojects.com)

---

## 🎯 Next Features to Add

- [ ] Recurring events
- [ ] Event notifications
- [ ] Multi-user support
- [ ] Calendar sharing
- [ ] Email integration
- [ ] Google Calendar sync
- [ ] Voice commands
- [ ] Mobile app

---

## 📞 Support

Having issues? Check:

1. Are both backend and frontend running?
2. Is Ollama service running?
3. Is MongoDB connected?
4. Check console for error messages
5. Check network tab in browser DevTools

---

## 🎉 Congratulations!

You've built a real-world AI application!

Next: Deploy it and show it to the world! 🚀
