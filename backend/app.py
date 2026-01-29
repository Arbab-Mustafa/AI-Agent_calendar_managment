"""
AI Calendar Agent Backend
Manages calendar scheduling using LangChain + Ollama + MongoDB
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from calendar_agent import CalendarAgent
from database import Database

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize database and agent
db = Database()
agent = CalendarAgent(db)

# ============================================================
# HEALTH CHECK
# ============================================================

@app.route('/api/health', methods=['GET'])
def health():
    """Check if backend is running"""
    return jsonify({
        "status": "✅ Calendar Agent Backend is running",
        "timestamp": datetime.now().isoformat()
    })


# ============================================================
# USER ENDPOINTS
# ============================================================

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.json
        user = db.create_user(
            email=data.get('email'),
            name=data.get('name'),
            preferences=data.get('preferences', {})
        )
        return jsonify({"status": "success", "user_id": str(user['_id'])})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user details"""
    try:
        user = db.get_user(user_id)
        if not user:
            return jsonify({"status": "error", "message": "User not found"}), 404
        user['_id'] = str(user['_id'])
        return jsonify({"status": "success", "user": user})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/api/users/<user_id>/preferences', methods=['PUT'])
def update_preferences(user_id):
    """Update user preferences"""
    try:
        data = request.json
        db.update_user_preferences(user_id, data)
        return jsonify({"status": "success", "message": "Preferences updated"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


# ============================================================
# CALENDAR ENDPOINTS
# ============================================================

@app.route('/api/calendar/<user_id>', methods=['GET'])
def get_calendar(user_id):
    """Get user's calendar events"""
    try:
        events = db.get_user_events(user_id)
        for event in events:
            event['_id'] = str(event['_id'])
            event['user_id'] = str(event['user_id'])
        return jsonify({
            "status": "success",
            "events": events,
            "count": len(events)
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/api/calendar/<user_id>/events', methods=['POST'])
def create_event(user_id):
    """Create a calendar event"""
    try:
        data = request.json
        event = db.create_event(
            user_id=user_id,
            title=data.get('title'),
            description=data.get('description', ''),
            start=datetime.fromisoformat(data.get('start')),
            end=datetime.fromisoformat(data.get('end')),
            attendees=data.get('attendees', []),
            location=data.get('location', '')
        )
        return jsonify({
            "status": "success",
            "message": "Event created",
            "event_id": str(event['_id'])
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/api/calendar/<user_id>/events/<event_id>', methods=['PUT'])
def update_event(user_id, event_id):
    """Update a calendar event"""
    try:
        data = request.json
        # Convert string dates to datetime
        update_data = {}
        if 'title' in data:
            update_data['title'] = data['title']
        if 'start' in data:
            update_data['start'] = datetime.fromisoformat(data['start'])
        if 'end' in data:
            update_data['end'] = datetime.fromisoformat(data['end'])
        if 'location' in data:
            update_data['location'] = data['location']
        if 'description' in data:
            update_data['description'] = data['description']
        
        db.update_event(event_id, update_data)
        return jsonify({
            "status": "success",
            "message": "Event updated"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/api/calendar/<user_id>/events/<event_id>', methods=['DELETE'])
def delete_event(user_id, event_id):
    """Delete a calendar event"""
    try:
        db.delete_event(event_id)
        return jsonify({
            "status": "success",
            "message": "Event deleted"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


# ============================================================
# AI AGENT ENDPOINTS
# ============================================================

@app.route('/api/agent/<user_id>/process', methods=['POST'])
def process_agent_request(user_id):
    """Process natural language request through calendar agent"""
    try:
        data = request.json
        user_request = data.get('request')
        
        if not user_request:
            return jsonify({
                "status": "error",
                "message": "No request provided"
            }), 400
        
        # Process through agent
        response = agent.process_request(user_id, user_request)
        
        return jsonify({
            "status": "success",
            "response": response["response"],
            "action_taken": response.get("action_taken"),
            "event_id": response.get("event_id")
        })
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


# ============================================================
# SMART SUGGESTIONS ENDPOINTS
# ============================================================

@app.route('/api/calendar/<user_id>/available-slots', methods=['POST'])
def get_available_slots(user_id):
    """Find available time slots for scheduling"""
    try:
        data = request.json
        duration_minutes = data.get('duration', 60)  # Default 1 hour
        days_ahead = data.get('days_ahead', 7)  # Default 1 week
        
        slots = agent.find_available_slots(
            user_id=user_id,
            duration_minutes=duration_minutes,
            days_ahead=days_ahead
        )
        
        return jsonify({
            "status": "success",
            "available_slots": [s.isoformat() for s in slots],
            "count": len(slots)
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/api/calendar/<user_id>/check-conflicts', methods=['POST'])
def check_conflicts(user_id):
    """Check if a time slot is available"""
    try:
        data = request.json
        start = datetime.fromisoformat(data.get('start'))
        end = datetime.fromisoformat(data.get('end'))
        
        has_conflict = agent.check_conflicts(user_id, start, end)
        
        return jsonify({
            "status": "success",
            "has_conflict": has_conflict,
            "available": not has_conflict
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"status": "error", "message": "Internal server error"}), 500


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True') == 'True'
    
    print("\n" + "="*60)
    print("🗓️  AI CALENDAR AGENT BACKEND")
    print("="*60)
    print(f"Server running on http://localhost:{port}")
    print(f"Debug mode: {debug}")
    print("="*60 + "\n")
    
    app.run(debug=debug, port=port, host='0.0.0.0')
