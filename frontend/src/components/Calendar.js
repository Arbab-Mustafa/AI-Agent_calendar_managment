import React, { useState } from "react";
import "./Calendar.css";

function Calendar({ events, onDeleteEvent }) {
  const [currentDate, setCurrentDate] = useState(new Date());

  const getDaysInMonth = (date) => {
    return new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
  };

  const getFirstDayOfMonth = (date) => {
    return new Date(date.getFullYear(), date.getMonth(), 1).getDay();
  };

  const previousMonth = () => {
    setCurrentDate(
      new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1),
    );
  };

  const nextMonth = () => {
    setCurrentDate(
      new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1),
    );
  };

  const goToToday = () => {
    setCurrentDate(new Date());
  };

  const daysInMonth = getDaysInMonth(currentDate);
  const firstDay = getFirstDayOfMonth(currentDate);
  const today = new Date();
  const days = [];

  // Add empty cells for days before month starts
  for (let i = 0; i < firstDay; i++) {
    days.push(null);
  }

  // Add all days in the month
  for (let i = 1; i <= daysInMonth; i++) {
    days.push(new Date(currentDate.getFullYear(), currentDate.getMonth(), i));
  }

  const getEventsForDate = (date) => {
    if (!date) return [];

    return events.filter((event) => {
      const eventDate = new Date(event.start);
      return (
        eventDate.getFullYear() === date.getFullYear() &&
        eventDate.getMonth() === date.getMonth() &&
        eventDate.getDate() === date.getDate()
      );
    });
  };

  const isToday = (date) => {
    if (!date) return false;
    return (
      date.getDate() === today.getDate() &&
      date.getMonth() === today.getMonth() &&
      date.getFullYear() === today.getFullYear()
    );
  };

  const formatTime = (dateString) => {
    const date = new Date(dateString);
    // Get local time components
    let hours = date.getHours();
    const minutes = date.getMinutes();
    const ampm = hours >= 12 ? "PM" : "AM";
    // Convert to 12-hour format
    const displayHours = hours === 0 ? 12 : hours > 12 ? hours - 12 : hours;
    const displayMinutes = minutes.toString().padStart(2, "0");

    console.log(
      `⏰ Formatting time: ${dateString} → Hours: ${hours}, Minutes: ${minutes} → ${displayHours}:${displayMinutes} ${ampm}`,
    );

    return `${displayHours}:${displayMinutes} ${ampm}`;
  };

  const getUpcomingEvents = () => {
    const now = new Date();
    return events
      .filter((event) => new Date(event.start) >= now)
      .sort((a, b) => new Date(a.start) - new Date(b.start))
      .slice(0, 5);
  };

  return (
    <div className="calendar">
      <div className="calendar-header">
        <h2>
          📅{" "}
          {currentDate.toLocaleString("default", {
            month: "long",
            year: "numeric",
          })}
        </h2>
        <div className="calendar-nav">
          <button onClick={previousMonth} title="Previous Month">
            ◀
          </button>
          <button onClick={goToToday} title="Today">
            Today
          </button>
          <button onClick={nextMonth} title="Next Month">
            ▶
          </button>
        </div>
      </div>

      <div className="calendar-weekdays">
        {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((day) => (
          <div key={day} className="weekday">
            {day}
          </div>
        ))}
      </div>

      <div className="calendar-days">
        {days.map((date, index) => (
          <div
            key={index}
            className={`day ${date ? "has-date" : "empty-day"} ${
              isToday(date) ? "today" : ""
            }`}
          >
            {date && (
              <>
                <div className="day-number">{date.getDate()}</div>
                <div className="events">
                  {getEventsForDate(date).map((event) => (
                    <div key={event._id} className="event">
                      <div className="event-content">
                        <span className="event-time">
                          {formatTime(event.start)}
                        </span>
                        <span className="event-title">{event.title}</span>
                      </div>
                      <button
                        className="delete-event"
                        onClick={() => onDeleteEvent(event._id)}
                        title="Delete event"
                      >
                        ✕
                      </button>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        ))}
      </div>

      <div className="upcoming-events">
        <h3>📌 Upcoming Events</h3>
        {getUpcomingEvents().length > 0 ? (
          <div className="upcoming-events-list">
            {getUpcomingEvents().map((event) => (
              <div key={event._id} className="upcoming-event">
                <div className="upcoming-event-title">{event.title}</div>
                <div className="upcoming-event-time">
                  🕒{" "}
                  {new Date(event.start).toLocaleDateString("en-US", {
                    weekday: "short",
                    month: "short",
                    day: "numeric",
                  })}{" "}
                  at {formatTime(event.start)}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="no-events">No upcoming events</div>
        )}
      </div>
    </div>
  );
}

export default Calendar;
