# 🚀 AI Calendar Agent - Quick Start Checklist

## ✅ Setup Checklist

### Prerequisites (Have These)

- [ ] Ollama installed on your machine
- [ ] Mistral model downloaded (`ollama pull mistral`)
- [ ] Python 3.8+ installed
- [ ] Node.js 14+ installed
- [ ] npm installed

### Backend Setup (5 minutes)

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env if needed
python app.py
```

- [ ] Requirements installed
- [ ] .env file created
- [ ] Backend running on http://localhost:5000
- [ ] See message: "Calendar Agent Backend is running"

### Frontend Setup (5 minutes)

```bash
cd frontend
npm install
cp .env.example .env
npm start
```

- [ ] Dependencies installed
- [ ] .env file created
- [ ] Frontend running on http://localhost:3000
- [ ] Can see calendar UI

### Test It Works

```bash
# In Terminal 1: Ollama should be running
ollama list  # Should show mistral

# In Terminal 2: Backend running
curl http://localhost:5000/api/health  # Should return OK

# In Terminal 3: Frontend running
# Open browser to http://localhost:3000
# Should see purple gradient background with calendar
```

---

## 🧪 Testing the System

### Test 1: Create Event Manually

1. Click "➕ New Event" button
2. Fill in:
   - Title: "Team Meeting"
   - Start: Tomorrow, 2:00 PM
   - End: Tomorrow, 3:00 PM
3. Click "Create Event"
4. Event appears on calendar

### Test 2: Talk to AI Agent

1. In chat box, type: "Schedule a meeting tomorrow at 3 PM"
2. Agent should respond: "✅ Scheduled 'meeting' for tomorrow at 3 PM"
3. Check calendar - new event appears

### Test 3: Check Conflicts

1. Try scheduling at same time as existing event
2. Agent should say: "❌ Time conflict! That slot is already booked."

### Test 4: Find Available Slots

1. Type: "Find available slots for 1 hour tomorrow"
2. Agent lists available times

---

## 🔧 Troubleshooting

### Backend won't start

```bash
# Check Ollama is running
ollama serve  # In separate terminal

# Check Python dependencies
pip install -r requirements.txt

# Check port 5000 is free
netstat -ano | findstr :5000
```

### Frontend won't load

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm start

# Check port 3000 is free
netstat -ano | findstr :3000
```

### Agent doesn't respond

```bash
# Check Ollama has mistral
ollama list

# Download if missing
ollama pull mistral

# Check backend logs for errors
# Look at Terminal 2 output
```

### Events not appearing

```bash
# Check database connection
# Backend should print: "✅ Connected to MongoDB"
# or "💾 Using local in-memory database"

# If using local MongoDB:
mongod  # Start MongoDB service first
```

---

## 📱 What Each Component Does

### Frontend (http://localhost:3000)

- Displays calendar
- Chat interface to AI
- Form to create events manually
- Real-time updates

### Backend (http://localhost:5000)

- Handles API requests
- Runs calendar agent
- Connects to database
- Processes natural language

### Ollama (http://localhost:11434)

- Runs Mistral LLM
- Processes natural language
- Extracts intents from user input

### Database

- Stores users
- Stores events
- Remembers your preferences

---

## 🎯 Commands Reference

### Ollama

```bash
ollama serve                # Start service
ollama pull mistral         # Download model
ollama list                 # List models
ollama run mistral "hello"  # Test model
```

### Backend

```bash
cd backend
python app.py              # Run server
curl http://localhost:5000/api/health  # Test API
```

### Frontend

```bash
cd frontend
npm install               # Install dependencies
npm start                 # Start dev server
npm build                 # Build for production
```

---

## 📊 Expected Output

### When Ollama Starts

```
time=... level=INFO msg="Listening on..."
```

### When Backend Starts

```
============================================================
🗓️  AI CALENDAR AGENT BACKEND
============================================================
Server running on http://localhost:5000
Debug mode: True
============================================================
```

### When Frontend Starts

```
webpack compiled successfully
Compiled successfully!
Local: http://localhost:3000
```

---

## ✨ Example Conversations

### User: "Schedule a meeting tomorrow at 3 PM"

```
Agent: ✅ Scheduled 'meeting' for tomorrow at 3 PM
Calendar: [Updates to show new event]
```

### User: "Find available slots for 1 hour"

```
Agent: 📅 Available slots for 60-min meeting:
Fri 09:00 AM
Fri 10:00 AM
Fri 02:00 PM
...
```

### User: "Schedule at that time" (trying to schedule at conflict)

```
Agent: ❌ Time conflict! That slot is already booked.
```

---

## 🎓 Learning Points

After completing this, you understand:

1. **Frontend** - React components, state, API calls
2. **Backend** - Flask, routes, business logic
3. **Database** - MongoDB, document storage
4. **AI/LLM** - Ollama, intent extraction, agents
5. **Full Stack** - How all pieces work together
6. **APIs** - Design, testing, error handling
7. **Deployment** - How to prepare for cloud

---

## 🚀 Next Steps After Testing

### Deploy to Cloud

1. Create MongoDB Atlas account (free)
2. Deploy backend to Render/Railway
3. Deploy frontend to Vercel
4. Share with friends!

### Add Features

- Recurring events
- Email notifications
- Event reminders
- Calendar sharing
- Google Calendar sync

### Improve AI

- Better NLP
- Context awareness
- User preferences
- Multi-language

---

## 📞 Quick Help

**Stuck?** Check these:

1. `SETUP_GUIDE.md` - Detailed instructions
2. `ARCHITECTURE.md` - How system works
3. `PROJECT_SUMMARY.md` - Complete overview
4. Terminal output - Look for error messages
5. Browser console - Frontend errors (F12)

**Ollama not working?**

- Download from https://ollama.ai
- Run `ollama serve` in terminal
- Wait for "Listening on" message

**Database issues?**

- Local: Run `mongod` first
- Cloud: Add connection string to .env

**API not responding?**

- Check backend terminal for errors
- Verify `http://localhost:5000/api/health` works

---

## 🎉 Success Indicators

When everything works, you'll see:

✅ Calendar grid with current month
✅ Chat box ready for input
✅ Can type messages to agent
✅ Agent responds in chat
✅ Events appear on calendar
✅ Can create events manually
✅ No errors in browser console
✅ No errors in backend terminal

---

## 💪 You Got This!

This is a **real, production-ready application**.

In just a few minutes, you'll have:

- A working calendar app
- AI-powered scheduling
- Real database
- Beautiful UI
- Everything deployable

**Let's go! 🚀**
