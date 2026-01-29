import React, { useState, useRef, useEffect } from "react";
import "./ChatBot.css";

function ChatBot({ onRequest }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: "bot",
      text: '👋 Hi! I\'m your AI Calendar Agent. Try saying:\n\n- "Schedule a meeting tomorrow at 3 PM"\n- "Find available slots for 1 hour"\n- "Cancel my 2 PM meeting"\n\n🎤 Click the microphone to use voice!',
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const messagesEnd = useRef(null);
  const recognitionRef = useRef(null);

  // Initialize Speech Recognition
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInput(transcript);
        setIsListening(false);
      };

      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }
  }, []);

  const scrollToBottom = () => {
    messagesEnd.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const toggleVoiceInput = () => {
    if (!recognitionRef.current) {
      alert('Voice recognition is not supported in your browser. Please use Chrome, Edge, or Safari.');
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      setIsListening(true);
      recognitionRef.current.start();
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();

    if (!input.trim() || loading) return;

    // Add user message
    const userMsg = {
      id: messages.length + 1,
      type: "user",
      text: input,
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const response = await onRequest(input);

      const botMsg = {
        id: messages.length + 2,
        type: "bot",
        text: response,
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (error) {
      const errorMsg = {
        id: messages.length + 2,
        type: "bot",
        text: `❌ Error: ${error.message}`,
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chatbot">
      <div className="chat-header">
        <h3>🤖 AI Assistant</h3>
      </div>

      <div className="chat-messages">
        {messages.map((msg) => (
          <div key={msg.id} className={`message ${msg.type}`}>
            <div className="message-content">{msg.text}</div>
          </div>
        ))}
        {loading && (
          <div className="message bot">
            <div className="message-content typing">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEnd} />
      </div>

      <form className="chat-input-form" onSubmit={handleSend}>
        <button 
          type="button" 
          className={`voice-btn ${isListening ? 'listening' : ''}`}
          onClick={toggleVoiceInput}
          title="Voice input"
        >
          {isListening ? '🔴' : '🎤'}
        </button>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={isListening ? "Listening..." : "Type or speak your request..."}
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          {loading ? "⏳" : "📤"}
        </button>
      </form>
    </div>
  );
}

export default ChatBot;
