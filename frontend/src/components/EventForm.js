import React, { useState } from "react";
import "./EventForm.css";

function EventForm({ onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    start: "",
    end: "",
    location: "",
    attendees: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const attendeesArray = formData.attendees
      .split(",")
      .map((a) => a.trim())
      .filter((a) => a);

    onSubmit({
      ...formData,
      attendees: attendeesArray,
      start: new Date(formData.start).toISOString(),
      end: new Date(formData.end).toISOString(),
    });
  };

  return (
    <div className="event-form-overlay">
      <div className="event-form-modal">
        <h2>Create New Event</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="title">Event Title *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              placeholder="e.g., Team Meeting"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Optional event details"
              rows="3"
            ></textarea>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="start">Start Date/Time *</label>
              <input
                type="datetime-local"
                id="start"
                name="start"
                value={formData.start}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="end">End Date/Time *</label>
              <input
                type="datetime-local"
                id="end"
                name="end"
                value={formData.end}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="location">Location</label>
            <input
              type="text"
              id="location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              placeholder="e.g., Conference Room A"
            />
          </div>

          <div className="form-group">
            <label htmlFor="attendees">
              Attendees (comma-separated emails)
            </label>
            <input
              type="text"
              id="attendees"
              name="attendees"
              value={formData.attendees}
              onChange={handleChange}
              placeholder="e.g., john@example.com, jane@example.com"
            />
          </div>

          <div className="form-actions">
            <button type="submit" className="btn-submit">
              ✓ Create Event
            </button>
            <button type="button" className="btn-cancel" onClick={onCancel}>
              ✕ Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default EventForm;
