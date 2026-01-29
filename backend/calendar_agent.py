"""
Calendar Agent using LangChain + Ollama
Handles natural language calendar requests
"""

from datetime import datetime, timedelta
import json
from typing import Any, List, Dict
import subprocess
from database import Database


class CalendarAgent:
    """AI agent for calendar management"""
    
    def __init__(self, db: Database):
        self.db = db
        self.model = "mistral"
    
    def _call_ollama(self, prompt: str) -> str:
        """Call local Ollama model"""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30
            )
            return result.stdout.strip()
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return "Error processing request"
    
    # ============================================================
    # CALENDAR TOOLS
    # ============================================================
    
    def get_user_calendar(self, user_id: str) -> List[Dict]:
        """Get user's upcoming events"""
        return self.db.get_user_events(user_id)
    
    def schedule_event(self, user_id: str, title: str, start: datetime, 
                      end: datetime, description: str = "", attendees: List[str] = None) -> bool:
        """Schedule a new event"""
        try:
            # Check for conflicts
            if self.check_conflicts(user_id, start, end):
                return False
            
            # Create event
            self.db.create_event(
                user_id=user_id,
                title=title,
                description=description,
                start=start,
                end=end,
                attendees=attendees or []
            )
            return True
        except Exception as e:
            print(f"Error scheduling event: {e}")
            return False
    
    def reschedule_event(self, user_id: str, event_id: str, 
                         new_start: datetime, new_end: datetime) -> bool:
        """Move an event to a different time"""
        try:
            # Check for conflicts
            if self.check_conflicts(user_id, new_start, new_end, exclude_event_id=event_id):
                return False
            
            # Update event
            self.db.update_event(event_id, {
                'start': new_start,
                'end': new_end
            })
            return True
        except Exception as e:
            print(f"Error rescheduling: {e}")
            return False
    
    def cancel_event(self, user_id: str, event_id: str) -> bool:
        """Cancel an event"""
        try:
            self.db.delete_event(event_id)
            return True
        except Exception as e:
            print(f"Error canceling event: {e}")
            return False
    
    def check_conflicts(self, user_id: str, start: datetime, end: datetime, 
                       exclude_event_id: str = None) -> bool:
        """Check if time slot has conflicts"""
        events = self.db.get_user_events(user_id)
        
        for event in events:
            # Skip the event being rescheduled
            if exclude_event_id and str(event['_id']) == exclude_event_id:
                continue
            
            # Check overlap
            if start < event['end'] and end > event['start']:
                return True
        
        return False
    
    def find_available_slots(self, user_id: str, duration_minutes: int = 60, 
                            days_ahead: int = 7) -> List[datetime]:
        """Find available time slots"""
        user = self.db.get_user(user_id)
        if not user:
            return []
        
        prefs = user.get('preferences', {})
        work_start = prefs.get('working_hours_start', '09:00')
        work_end = prefs.get('working_hours_end', '18:00')
        
        available_slots = []
        start_time = datetime.now()
        
        for day in range(days_ahead):
            current_date = start_time + timedelta(days=day)
            
            # Parse working hours
            start_hour, start_min = map(int, work_start.split(':'))
            end_hour, end_min = map(int, work_end.split(':'))
            
            day_start = current_date.replace(hour=start_hour, minute=start_min, second=0)
            day_end = current_date.replace(hour=end_hour, minute=end_min, second=0)
            
            # Find slots within working hours
            current_slot = day_start
            while (current_slot + timedelta(minutes=duration_minutes)) <= day_end:
                slot_end = current_slot + timedelta(minutes=duration_minutes)
                
                if not self.check_conflicts(user_id, current_slot, slot_end):
                    available_slots.append(current_slot)
                
                current_slot += timedelta(minutes=30)  # 30-min intervals
        
        return available_slots[:10]  # Return first 10 slots
    
    def get_user_preferences(self, user_id: str) -> Dict:
        """Get user's calendar preferences"""
        user = self.db.get_user(user_id)
        return user.get('preferences', {}) if user else {}
    
    def set_user_preferences(self, user_id: str, preferences: Dict) -> bool:
        """Update user preferences"""
        try:
            self.db.update_user_preferences(user_id, preferences)
            return True
        except:
            return False
    
    # ============================================================
    # AGENT LOGIC
    # ============================================================
    
    def _extract_intent(self, user_request: str) -> Dict[str, Any]:
        """Extract intent from natural language request"""
        
        # Get current date for context
        today = datetime.now().strftime('%Y-%m-%d')
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        prompt = f"""You are a calendar assistant. Extract information from the user's request.

Today's date: {today}
Tomorrow's date: {tomorrow}

User said: "{user_request}"

Extract these fields:
1. title: The event name (meeting, call, appointment, etc.)
2. date: Use {tomorrow} if they say "tomorrow", {today} if they say "today"
3. time: Convert to 24-hour format:
   - "3 PM" or "3pm" → "15:00"
   - "10 AM" or "10am" → "10:00"
   - "2:30 PM" → "14:30"
   - "noon" or "12 PM" → "12:00"
   - "midnight" or "12 AM" → "00:00"
4. duration: "1 hour"=60, "30 minutes"=30, "2 hours"=120, default=60

YOU MUST return valid JSON with ALL fields filled:

{{"intent":"schedule","title":"meeting","date":"{tomorrow}","time":"15:00","duration":"60","description":"","attendees":[]}}

IMPORTANT TIME CONVERSION EXAMPLES:
- "3 PM" → "15:00" (not "03:00")
- "9 AM" → "09:00"
- "1:30 PM" → "13:30"
- "11 PM" → "23:00"

Do NOT leave fields empty. If no time is mentioned, use "14:00". If no duration mentioned, use "60".

Now extract from: "{user_request}"

JSON:"""
        
        response = self._call_ollama(prompt)
        
        try:
            # Clean the response to extract JSON
            json_str = response.strip()
            
            # Remove markdown code blocks
            if "```" in json_str:
                parts = json_str.split("```")
                for part in parts:
                    if part.strip().startswith("{") or part.strip().startswith("json"):
                        json_str = part.replace("json", "").strip()
                        break
            
            # Find the JSON object in the response
            start_idx = json_str.find("{")
            end_idx = json_str.rfind("}") + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = json_str[start_idx:end_idx]
            
            parsed = json.loads(json_str)
            print(f"✅ Parsed intent: {parsed}")
            return parsed
            
        except Exception as e:
            print(f"❌ Could not parse intent from: {response}")
            print(f"Error: {e}")
            return {"intent": "unknown"}
    
    def process_request(self, user_id: str, user_request: str) -> Dict[str, Any]:
        """Process a natural language calendar request"""
        
        # Extract intent
        intent_data = self._extract_intent(user_request)
        intent = intent_data.get('intent', 'unknown')
        
        print(f"\n📌 Extracted intent: {intent}")
        print(f"Intent data: {intent_data}\n")
        
        try:
            if intent == "schedule":
                return self._handle_schedule(user_id, intent_data)
            
            elif intent == "reschedule":
                return self._handle_reschedule(user_id, intent_data)
            
            elif intent == "cancel":
                return self._handle_cancel(user_id, intent_data)
            
            elif intent == "suggest":
                return self._handle_suggest(user_id, intent_data)
            
            elif intent == "check":
                return self._handle_check(user_id, intent_data)
            
            elif intent == "update_preferences":
                return self._handle_update_prefs(user_id, intent_data)
            
            else:
                return {
                    "response": "I couldn't understand that request. Try: 'Schedule...', 'Reschedule...', 'Cancel...', or 'Suggest times...'",
                    "action_taken": None
                }
        
        except Exception as e:
            print(f"Error processing request: {e}")
            return {
                "response": f"Error: {str(e)}",
                "action_taken": None
            }
    
    def _handle_schedule(self, user_id: str, intent_data: Dict) -> Dict:
        """Handle scheduling a new event"""
        # Extract and validate data with proper defaults
        title = intent_data.get('title', '').strip() or 'Meeting'
        date_str = intent_data.get('date', '').strip()
        time_str = intent_data.get('time', '').strip() or '14:00'
        
        # Handle duration - convert to int safely
        duration_str = str(intent_data.get('duration', '60')).strip()
        try:
            duration = int(duration_str) if duration_str else 60
        except ValueError:
            duration = 60  # Default to 60 minutes
        
        # Validation
        if not date_str or date_str == "Not specified" or date_str == "YYYY-MM-DD":
            return {
                "response": "❌ I need a specific date. Please say 'tomorrow', 'today', or mention a date like 'January 30'.",
                "action_taken": None
            }
        
        try:
            # Parse date and time
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            
            # Parse time with validation
            time_parts = time_str.split(':')
            hour = int(time_parts[0])
            minute = int(time_parts[1]) if len(time_parts) > 1 else 0
            
            # Validate hour and minute
            if hour < 0 or hour > 23:
                raise ValueError(f"Invalid hour: {hour}. Must be 0-23.")
            if minute < 0 or minute > 59:
                raise ValueError(f"Invalid minute: {minute}. Must be 0-59.")
            
            print(f"⏰ Creating event: {title} on {date_str} at {hour:02d}:{minute:02d} (24-hour format)")
            
            start = date_obj.replace(hour=hour, minute=minute, second=0, microsecond=0)
            end = start + timedelta(minutes=duration)
            
            print(f"📅 Start datetime: {start.isoformat()}, End: {end.isoformat()}")
            
            # Schedule event
            if self.schedule_event(user_id, title, start, end):
                # Format date nicely
                date_display = date_obj.strftime('%B %d, %Y')
                time_display = start.strftime('%I:%M %p')
                
                return {
                    "response": f"✅ Scheduled '{title}' for {date_display} at {time_display} ({duration} min)",
                    "action_taken": "schedule",
                    "event": {
                        "title": title,
                        "start": start.isoformat(),
                        "end": end.isoformat()
                    }
                }
            else:
                return {
                    "response": f"❌ Time conflict! That slot is already booked.",
                    "action_taken": None
                }
        except Exception as e:
            print(f"Error in _handle_schedule: {e}")
            return {
                "response": f"❌ Error scheduling: {str(e)}. Please try again with a clear date and time.",
                "action_taken": None
            }
    
    def _handle_reschedule(self, user_id: str, intent_data: Dict) -> Dict:
        """Handle rescheduling an event"""
        return {
            "response": "Rescheduling feature coming soon!",
            "action_taken": None
        }
    
    def _handle_cancel(self, user_id: str, intent_data: Dict) -> Dict:
        """Handle canceling an event"""
        return {
            "response": "Cancellation feature coming soon!",
            "action_taken": None
        }
    
    def _handle_suggest(self, user_id: str, intent_data: Dict) -> Dict:
        """Handle suggesting available times"""
        duration = intent_data.get('duration', 60)
        
        slots = self.find_available_slots(user_id, duration)
        
        if not slots:
            return {
                "response": "No available slots found in the next week.",
                "action_taken": None
            }
        
        # Format slots
        slot_str = "\n".join([s.strftime("%a %I:%M %p") for s in slots[:5]])
        
        return {
            "response": f"📅 Available slots for {duration}-min meeting:\n{slot_str}",
            "action_taken": "suggest"
        }
    
    def _handle_check(self, user_id: str, intent_data: Dict) -> Dict:
        """Handle checking availability"""
        return {
            "response": "Availability check coming soon!",
            "action_taken": None
        }
    
    def _handle_update_prefs(self, user_id: str, intent_data: Dict) -> Dict:
        """Handle updating preferences"""
        return {
            "response": "Preference update coming soon!",
            "action_taken": None
        }
