"""
Configuration module for Konsultabot - EVSU DULAG AI Chatbot
Handles application settings and API configurations
"""

import os
import json

# Optional dotenv import with fallback
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

class Config:
    def __init__(self):
        # Load environment variables if dotenv is available
        if DOTENV_AVAILABLE:
            load_dotenv()
        
        # Database settings
        self.DATABASE_PATH = "konsultabot.db"
        
        # Google AI Studio API
        self.GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
        
        # Voice settings
        self.VOICE_ENABLED = True
        self.TTS_RATE = 150  # Words per minute
        
        # Session management
        self.SESSION_FILE = "user_session.json"
        self.REMEMBER_LOGIN = True
        
        # Network detection
        self.CHECK_INTERNET_INTERVAL = 30  # seconds
        self.ONLINE_MODE = True
        self.TTS_VOLUME = 0.8
        self.VOICE_LANGUAGE = 'en'  # Default voice language
        
        # GUI settings
        self.WINDOW_WIDTH = 400
        self.WINDOW_HEIGHT = 600
        self.THEME_COLOR = "#0F1419"
        self.SECONDARY_COLOR = "#1E2328"
        self.ACCENT_COLOR = "#00D4FF"
        self.SUCCESS_COLOR = "#00FF88"
        self.WARNING_COLOR = "#FFB800"
        self.ERROR_COLOR = "#FF4757"
        self.BACKGROUND_COLOR = "#0A0E13"
        self.CARD_COLOR = "#161B22"
        self.TEXT_COLOR = "#E6EDF3"
        self.MUTED_TEXT = "#7D8590"
        self.BORDER_COLOR = "#30363D"
        
        # Application settings
        self.APP_NAME = "Konsultabot"
        self.APP_VERSION = "1.0.0"
        self.CAMPUS_NAME = "EVSU DULAG"
        self.DEFAULT_LANGUAGE = "english"
        self.ONLINE_MODE = True
        
        # Security settings
        self.SESSION_TIMEOUT = 3600  # 1 hour in seconds
        self.MAX_LOGIN_ATTEMPTS = 3
        
        # Voice recognition settings
        self.SPEECH_TIMEOUT = 5  # seconds
        self.SPEECH_PHRASE_TIMEOUT = 1  # seconds
        
    def get_voice_settings(self):
        """Get voice configuration"""
        return {
            'rate': self.TTS_RATE,
            'volume': self.TTS_VOLUME,
            'language': self.VOICE_LANGUAGE
        }
    
    def get_gui_settings(self):
        """Get GUI configuration"""
        return {
            'width': self.WINDOW_WIDTH,
            'height': self.WINDOW_HEIGHT,
            'theme_color': self.THEME_COLOR,
            'accent_color': self.ACCENT_COLOR,
            'text_color': self.TEXT_COLOR,
            'background_color': self.BACKGROUND_COLOR
        }
    
    def save_user_preferences(self, user_id, preferences):
        """Save user-specific preferences"""
        prefs_file = f"user_prefs_{user_id}.json"
        with open(prefs_file, 'w') as f:
            json.dump(preferences, f)
    
    def load_user_preferences(self, user_id):
        """Load user-specific preferences"""
        prefs_file = f"user_prefs_{user_id}.json"
        try:
            with open(prefs_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def validate_api_key(self):
        """Validate if Google API key is configured"""
        return bool(self.GOOGLE_API_KEY and len(self.GOOGLE_API_KEY) > 10)

# Global config instance
config_instance = Config()

# Export config attributes for backward compatibility
APP_NAME = config_instance.APP_NAME
APP_VERSION = config_instance.APP_VERSION
CAMPUS_NAME = config_instance.CAMPUS_NAME
DEFAULT_LANGUAGE = config_instance.DEFAULT_LANGUAGE
ONLINE_MODE = config_instance.ONLINE_MODE
DATABASE_PATH = config_instance.DATABASE_PATH
GOOGLE_API_KEY = config_instance.GOOGLE_API_KEY
THEME_COLOR = config_instance.THEME_COLOR
ACCENT_COLOR = config_instance.ACCENT_COLOR
TEXT_COLOR = config_instance.TEXT_COLOR
BACKGROUND_COLOR = config_instance.BACKGROUND_COLOR
WINDOW_WIDTH = config_instance.WINDOW_WIDTH
WINDOW_HEIGHT = config_instance.WINDOW_HEIGHT

def get_gui_settings():
    return config_instance.get_gui_settings()

def get_voice_settings():
    return config_instance.get_voice_settings()

def validate_api_key():
    return config_instance.validate_api_key()

# Export additional attributes needed by voice_handler and other modules
TTS_RATE = config_instance.TTS_RATE
TTS_VOLUME = config_instance.TTS_VOLUME
VOICE_LANGUAGE = config_instance.VOICE_LANGUAGE
SPEECH_PHRASE_TIMEOUT = config_instance.SPEECH_PHRASE_TIMEOUT
SPEECH_TIMEOUT = config_instance.SPEECH_TIMEOUT
VOICE_ENABLED = config_instance.VOICE_ENABLED
SESSION_TIMEOUT = config_instance.SESSION_TIMEOUT
MAX_LOGIN_ATTEMPTS = config_instance.MAX_LOGIN_ATTEMPTS
