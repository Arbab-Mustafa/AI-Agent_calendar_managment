"""
Database Module - MongoDB Connection
Handles all database operations for calendar agent
"""

import os
from datetime import datetime
from typing import List, Dict, Optional
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class Database:
    """MongoDB database handler"""
    
    def __init__(self):
        """Initialize MongoDB connection"""
        mongo_uri = os.getenv('MONGODB_URI', 'mongodb+srv://Arbab:QWV5K0kCUWOdEXsH@cluster0.brxuxmp.mongodb.net/aiagent')
        
        try:
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.admin.command('ping')
            print("✅ Connected to MongoDB")
        except ConnectionFailure:
            print("⚠️  Could not connect to MongoDB. Using local fallback.")
            self.client = None
        
        if self.client:
            self.db = self.client.calendar_agent
            self.users = self.db.users
            self.events = self.db.events
        else:
            # Fallback in-memory database
            self._users_memory = {}
            self._events_memory = {}
    
    # ============================================================
    # USER OPERATIONS
    # ============================================================
    
    def create_user(self, email: str, name: str, preferences: Dict = None) -> Dict:
        """Create a new user"""
        if not preferences:
            preferences = {
                'working_hours_start': '09:00',
                'working_hours_end': '18:00',
                'timezone': 'UTC',
                'min_meeting_duration': 30
            }
        
        user = {
            'email': email,
            'name': name,
            'created_at': datetime.utcnow(),
            'preferences': preferences
        }
        
        if self.client:
            result = self.users.insert_one(user)
            user['_id'] = result.inserted_id
        else:
            user['_id'] = ObjectId()
            self._users_memory[str(user['_id'])] = user
        
        return user
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        try:
            obj_id = ObjectId(user_id)
        except:
            obj_id = user_id
        
        if self.client:
            return self.users.find_one({'_id': obj_id})
        else:
            return self._users_memory.get(str(user_id))
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        if self.client:
            return self.users.find_one({'email': email})
        else:
            for user in self._users_memory.values():
                if user['email'] == email:
                    return user
            return None
    
    def update_user_preferences(self, user_id: str, preferences: Dict) -> bool:
        """Update user preferences"""
        try:
            obj_id = ObjectId(user_id)
        except:
            obj_id = user_id
        
        if self.client:
            self.users.update_one(
                {'_id': obj_id},
                {'$set': {'preferences': preferences}}
            )
        else:
            if str(user_id) in self._users_memory:
                self._users_memory[str(user_id)]['preferences'] = preferences
        
        return True
    
    # ============================================================
    # EVENT OPERATIONS
    # ============================================================
    
    def create_event(self, user_id: str, title: str, description: str, 
                    start: datetime, end: datetime, attendees: List[str] = None,
                    location: str = "") -> Dict:
        """Create a calendar event"""
        try:
            obj_id = ObjectId(user_id)
        except:
            obj_id = user_id
        
        event = {
            'user_id': obj_id,
            'title': title,
            'description': description,
            'start': start,
            'end': end,
            'attendees': attendees or [],
            'location': location,
            'created_at': datetime.utcnow(),
            'status': 'active'
        }
        
        if self.client:
            result = self.events.insert_one(event)
            event['_id'] = result.inserted_id
        else:
            event['_id'] = ObjectId()
            self._events_memory[str(event['_id'])] = event
        
        return event
    
    def get_user_events(self, user_id: str, start_date: datetime = None,
                       end_date: datetime = None) -> List[Dict]:
        """Get user's events"""
        try:
            obj_id = ObjectId(user_id)
        except:
            obj_id = user_id
        
        query = {'user_id': obj_id, 'status': 'active'}
        
        # Filter by date range if provided
        if start_date or end_date:
            date_query = {}
            if start_date:
                date_query['$gte'] = start_date
            if end_date:
                date_query['$lte'] = end_date
            
            if date_query:
                query['$or'] = [
                    {'start': date_query},
                    {'end': date_query}
                ]
        
        if self.client:
            events = list(self.events.find(query).sort('start', 1))
        else:
            events = [e for e in self._events_memory.values() 
                     if str(e['user_id']) == str(user_id) and e['status'] == 'active']
            events.sort(key=lambda x: x['start'])
        
        return events
    
    def get_event(self, event_id: str) -> Optional[Dict]:
        """Get a specific event"""
        try:
            obj_id = ObjectId(event_id)
        except:
            obj_id = event_id
        
        if self.client:
            return self.events.find_one({'_id': obj_id})
        else:
            return self._events_memory.get(str(event_id))
    
    def update_event(self, event_id: str, updates: Dict) -> bool:
        """Update an event"""
        try:
            obj_id = ObjectId(event_id)
        except:
            obj_id = event_id
        
        if self.client:
            self.events.update_one(
                {'_id': obj_id},
                {'$set': updates}
            )
        else:
            if str(event_id) in self._events_memory:
                self._events_memory[str(event_id)].update(updates)
        
        return True
    
    def delete_event(self, event_id: str) -> bool:
        """Delete/archive an event"""
        try:
            obj_id = ObjectId(event_id)
        except:
            obj_id = event_id
        
        if self.client:
            self.events.update_one(
                {'_id': obj_id},
                {'$set': {'status': 'deleted'}}
            )
        else:
            if str(event_id) in self._events_memory:
                self._events_memory[str(event_id)]['status'] = 'deleted'
        
        return True
    
    # ============================================================
    # UTILITY METHODS
    # ============================================================
    
    def get_connection_status(self) -> str:
        """Check database connection status"""
        if self.client:
            try:
                self.client.admin.command('ping')
                return "✅ Connected to MongoDB Atlas"
            except:
                return "⚠️  MongoDB connection lost"
        else:
            return "💾 Using local in-memory database"
    
    def clear_all(self) -> bool:
        """Clear all data (for testing)"""
        try:
            if self.client:
                self.db.drop_collection('users')
                self.db.drop_collection('events')
            else:
                self._users_memory.clear()
                self._events_memory.clear()
            return True
        except Exception as e:
            print(f"Error clearing database: {e}")
            return False
