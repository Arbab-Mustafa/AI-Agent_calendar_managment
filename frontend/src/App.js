import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import "./App.css";
import Calendar from "./components/Calendar";
import ChatBot from "./components/ChatBot";
import EventForm from "./components/EventForm";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:5000/api";

function App() {
  const [userId, setUserId] = useState(localStorage.getItem("userId") || null);
  const [events, setEvents] = useState([]);
  const [showEventForm, setShowEventForm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const createNewUser = async () => {
    try {
      const response = await axios.post(`${API_BASE}/users`, {
        email: `user_${Date.now()}@calendar.local`,
        name: "Calendar User",
        preferences: {
          working_hours_start: "09:00",
          working_hours_end: "18:00",
          timezone: "UTC",
        },
      });

      const newUserId = response.data.user_id;
      setUserId(newUserId);
      localStorage.setItem("userId", newUserId);
    } catch (err) {
      setError("Failed to create user: " + err.message);
    }
  };

  const loadUserData = useCallback(async () => {
    if (!userId) return;

    try {
      setLoading(true);

      // Load user info (just to verify user exists)
      await axios.get(`${API_BASE}/users/${userId}`);

      // Load events
      const eventsRes = await axios.get(`${API_BASE}/calendar/${userId}`);
      console.log(
        `📅 Loaded ${eventsRes.data.events.length} events:`,
        eventsRes.data.events,
      );
      setEvents(eventsRes.data.events);

      setError(null);
    } catch (err) {
      // If user not found (404), database was reset - create new user
      if (err.response && err.response.status === 404) {
        console.log("User not found. Database was reset. Creating new user...");
        localStorage.removeItem("userId");
        setUserId(null);
      } else {
        setError("Failed to load data: " + err.message);
      }
    } finally {
      setLoading(false);
    }
  }, [userId]);

  // Initialize user
  useEffect(() => {
    if (!userId) {
      createNewUser();
    } else {
      loadUserData();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userId, loadUserData]);

  const handleCreateEvent = async (eventData) => {
    try {
      console.log("➕ Creating event:", eventData);
      await axios.post(`${API_BASE}/calendar/${userId}/events`, eventData);
      // Only reload events, not full page
      const eventsRes = await axios.get(`${API_BASE}/calendar/${userId}`);
      console.log(
        `✅ Event created. Now have ${eventsRes.data.events.length} events`,
      );
      setEvents(eventsRes.data.events);
      setShowEventForm(false);
      setError(null);
    } catch (err) {
      setError("Failed to create event: " + err.message);
    }
  };

  const handleDeleteEvent = async (eventId) => {
    try {
      console.log("🗑️ Deleting event:", eventId);
      await axios.delete(`${API_BASE}/calendar/${userId}/events/${eventId}`);
      // Only reload events, not full page
      const eventsRes = await axios.get(`${API_BASE}/calendar/${userId}`);
      console.log(
        `✅ Event deleted. Now have ${eventsRes.data.events.length} events`,
      );
      setEvents(eventsRes.data.events);
      setError(null);
    } catch (err) {
      setError("Failed to delete event: " + err.message);
    }
  };

  const handleAgentRequest = async (request) => {
    try {
      console.log("🤖 Agent processing:", request);
      const response = await axios.post(`${API_BASE}/agent/${userId}/process`, {
        request: request,
      });

      // Only reload events, not full page
      const eventsRes = await axios.get(`${API_BASE}/calendar/${userId}`);
      console.log(
        `✅ Agent request completed. Now have ${eventsRes.data.events.length} events`,
      );
      setEvents(eventsRes.data.events);

      return response.data.response;
    } catch (err) {
      throw new Error("Failed to process request: " + err.message);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🗓️ AI Calendar Agent</h1>
        <p>Manage your calendar with natural language</p>
      </header>

      {error && <div className="error-banner">{error}</div>}

      {loading && <div className="loading">Loading...</div>}

      {userId && !loading && (
        <div className="App-container">
          <div className="main-content">
            <Calendar events={events} onDeleteEvent={handleDeleteEvent} />

            <div className="actions">
              <button
                className="btn btn-primary"
                onClick={() => setShowEventForm(!showEventForm)}
              >
                ➕ New Event
              </button>
              <button className="btn btn-secondary" onClick={loadUserData}>
                🔄 Refresh
              </button>
            </div>

            {showEventForm && (
              <EventForm
                onSubmit={handleCreateEvent}
                onCancel={() => setShowEventForm(false)}
              />
            )}
          </div>

          <aside className="sidebar">
            <ChatBot onRequest={handleAgentRequest} />
          </aside>
        </div>
      )}
    </div>
  );
}

export default App;
