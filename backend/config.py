"""
Configuration file for Calendar Agent
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Database
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/calendar_agent')

# Server
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
PORT = int(os.getenv('PORT', 5000))
HOST = os.getenv('HOST', '0.0.0.0')

# Ollama
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral')
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')

# CORS
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5000').split(',')

print(f"""
╔════════════════════════════════════════════════╗
║   🗓️  CALENDAR AGENT CONFIGURATION            ║
╚════════════════════════════════════════════════╝
Database:  {MONGODB_URI[:50]}...
Ollama:    {OLLAMA_BASE_URL} ({OLLAMA_MODEL})
Server:    {HOST}:{PORT}
Debug:     {DEBUG}
""")
